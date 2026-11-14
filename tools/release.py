#!/usr/bin/env python3
"""Kerd's release steps as one script, so a release is not typed by hand.

    python3 tools/release.py check
    python3 tools/release.py prep VERSION --note FILE
    python3 tools/release.py ship [--codex] [--plugin] [--deadline SECONDS]

`check` runs the named `run:` steps `.github/workflows/gate.yml` lists, read from
the file itself; a step in a form it cannot read (unnamed, multi-line) stops it
rather than being skipped. Each step's output goes to its own log file and its own
exit code is kept; each runs under `pipefail`, so a piped step fails when any
part of its pipe fails. Exit 0 only when every step passed.

`prep` bumps the version in the three manifest fields, writes the release note
into README's "What's New" and CHANGELOG.md (the same text in both), then runs
`check`. Every file and the workflow are read and checked before anything is
written; a failing `check` afterwards leaves the edits in place to fix. It
commits nothing and touches nothing outside the working tree.

`ship` is outward: it runs only on the person's go for that release. It refuses
a tree with uncommitted tracked changes, a failing release check or (with
`--codex`/`--plugin`) a branch other than `main`; prints what it will do; pushes
the exact checked commit to the branch and confirms the remote now holds it;
finds an `entry-gate` push run for that commit that did not exist before the
push (or, when the remote already held the commit, says so and uses its newest
run) and waits for it, the deadline bounding the waiting and every `gh` call
bounded too; before each publish it reads the run again and stops if its
attempt or result changed; on failure prints the failed steps' log
lines and stops; on success, with `--codex`, publishes the Codex package from
that exact commit, and with `--plugin`, updates Kerd in Claude Code while the
remote branch still holds that commit, then reads the installed commit back and
reports any difference (the update itself follows the marketplace, so this is a
check after the fact, not a lock).

When the shipped commit's marketplace.json gives the kerd source `"ref": "plugin"`,
Claude Code users install from the generated `plugin` branch, so ship on main
keeps that branch in step: after CI passes (re-read first, like the Codex
publish) it appends a commit built by tools/plugin_release.py from the shipped
commit, and `--plugin` then expects the installed commit to be that branch
commit, not main's. If origin has no plugin branch yet, ship creates it before
pushing main, from what origin/main already serves, so no install ever points
at a missing branch. An unreadable marketplace.json, or a ref or sha ship does
not know, refuses before anything is pushed. Every stop says what was already published. Anything
it cannot read or parse stops it: it never guesses a run or reports a pass it
did not see.

Exit codes: 0 done, 1 a step or CI failed, 2 refused before doing anything
outward (bad arguments, unreadable state), 3 pushed but no CI result seen in
time, 4 pushed but CI state unreadable, changed or the branch moved (the stop
line lists anything already published).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ".github/workflows/gate.yml"
MANIFESTS = ((".claude-plugin/plugin.json", 1), (".claude-plugin/marketplace.json", 2))
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class Refused(Exception):
    """Stop before anything outward happens (exit 2)."""


def gh_cmd():
    return os.environ.get("KERD_RELEASE_GH", "gh")


def claude_cmd():
    return os.environ.get("KERD_RELEASE_CLAUDE", "claude")


def poll_seconds():
    return float(os.environ.get("KERD_RELEASE_POLL", "10"))


def run(cmd, root, **kw):
    """A program that cannot start is an ordinary failure (exit 127), never a traceback."""
    try:
        return subprocess.run(cmd, cwd=root, capture_output=True, text=True, **kw)
    except OSError as error:
        return subprocess.CompletedProcess(cmd, 127, "", f"could not start {cmd[0]}: {error}")


# ── check ───────────────────────────────────────────────────────────────

def gate_steps(root):
    """(name, command) pairs from the workflow's `- name:` / `run:` steps."""
    path = Path(root) / WORKFLOW
    try:
        lines = path.read_text().splitlines()
    except OSError as error:
        raise Refused(f"cannot read {WORKFLOW}: {error}")
    steps, name = [], None
    run_lines = sum(1 for line in lines if re.match(r"^\s*(-\s*)?run:", line))
    for number, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("- "):
            name = None  # every list item is a new step; a name never carries over
        named = re.match(r"^- name:\s*(.+)$", stripped)
        if named:
            name = named.group(1).strip()
            continue
        command = re.match(r"^(- )?run:\s*(.*)$", stripped)
        if command:
            value = command.group(2).strip()
            if not value or value[0] in "|>":
                raise Refused(f"{WORKFLOW}: multi-line run blocks are not supported")
            if command.group(1) or name is None:
                raise Refused(f"{WORKFLOW}: an unnamed run step is not supported")
            key_indent = len(line) - len(line.lstrip())
            following = next((l for l in lines[number + 1:] if l.strip() and not l.strip().startswith("#")), None)
            if following is not None and len(following) - len(following.lstrip()) > key_indent:
                raise Refused(f"{WORKFLOW}: a run command continued on the next line is not supported")
            steps.append((name, value))
            name = None
    if not steps:
        raise Refused(f"{WORKFLOW}: no run steps found")
    if len(steps) != run_lines:
        raise Refused(f"{WORKFLOW}: read {len(steps)} of {run_lines} run steps")
    return steps


def summary_of(text):
    """The last line that says how many ran or that all is well, if any."""
    found = ""
    for line in text.splitlines():
        if re.search(r"\b\d+ tests?\b|All green|release: |selftest: |problem", line):
            found = line.strip()
    return found


def check(root, log_dir=None):
    root = Path(root)
    steps = gate_steps(root)
    log_dir = Path(log_dir or tempfile.mkdtemp(prefix="kerd-check-"))
    log_dir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for number, (name, command) in enumerate(steps, 1):
        log = log_dir / f"{number}-{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')}.log"
        result = run(["bash", "-o", "pipefail", "-c", command], root)
        log.write_text(result.stdout + result.stderr)
        status = "ok" if result.returncode == 0 else "FAILED"
        if result.returncode != 0:
            failed += 1
        print(f"{status}: {name} — exit {result.returncode}; {summary_of(result.stdout + result.stderr) or 'no count line'}")
        print(f"    log: {log}")
    print(f"check: {len(steps) - failed} of {len(steps)} steps passed")
    return 0 if failed == 0 else 1


# ── prep ────────────────────────────────────────────────────────────────

def current_version(root):
    data = json.loads((Path(root) / ".claude-plugin/plugin.json").read_text())
    return data["version"]


def as_tuple(version):
    return tuple(int(part) for part in version.split("."))


def prep(root, version, note, run_check=True):
    root = Path(root)
    if not SEMVER.match(version):
        raise Refused(f"version must look like 1.2.3, got {version!r}")
    old = current_version(root)
    if as_tuple(version) <= as_tuple(old):
        raise Refused(f"version {version} is not newer than {old}")
    note = note.strip()
    if not note:
        raise Refused("the release note is empty")
    edits = {}
    for name, count in MANIFESTS:
        text = (root / name).read_text()
        needle = f'"version": "{old}"'
        if text.count(needle) != count:
            raise Refused(f"{name}: expected {count} × {needle}, found {text.count(needle)}")
        edits[name] = text.replace(needle, f'"version": "{version}"')
    readme = (root / "README.md").read_text()
    header = f"## What's New (v{old})"
    if readme.count(header) != 1:
        raise Refused(f"README.md: expected one {header!r}")
    readme = readme.replace(header, f"## What's New (v{version})")
    first_entry = readme.find("\n### v", readme.find(f"## What's New (v{version})"))
    if first_entry < 0:
        raise Refused("README.md: no ### v entry under What's New")
    edits["README.md"] = readme[:first_entry + 1] + f"### v{version}\n\n{note}\n\n" + readme[first_entry + 1:]
    changelog = (root / "CHANGELOG.md").read_text()
    first = changelog.find("\n## ")
    if first < 0:
        raise Refused("CHANGELOG.md: no ## entry")
    edits["CHANGELOG.md"] = changelog[:first + 1] + f"## {version}\n\n{note}\n\n" + changelog[first + 1:]
    if run_check:
        gate_steps(root)
    for name, text in edits.items():
        temporary = root / (name + ".release-tmp")
        temporary.write_text(text)
        os.replace(temporary, root / name)
    print(f"prep: {old} → {version} in {', '.join(edits)}")
    return check(root) if run_check else 0


# ── ship ────────────────────────────────────────────────────────────────

def git(root, *args):
    result = run(["git", *args], root)
    if result.returncode != 0:
        raise Refused(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


class Unread(Exception):
    """After the push: CI state could not be read (exit 4)."""


def gh_json(root, *args):
    try:
        result = run([gh_cmd(), *args], root, timeout=60)
    except subprocess.TimeoutExpired:
        raise Unread(f"gh {' '.join(args)} gave no answer within 60 s")
    if result.returncode != 0:
        raise Unread(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise Unread(f"gh {' '.join(args)} returned unreadable output")


def pause(deadline):
    time.sleep(max(0.0, min(poll_seconds(), deadline - time.monotonic())))


def list_runs(root, branch, sha):
    """Push runs of the entry-gate workflow for this commit, every entry checked."""
    runs = gh_json(root, "run", "list", "--workflow", Path(WORKFLOW).name, "--branch", branch,
                   "--limit", "50", "--json", "databaseId,headSha,status,conclusion,event")
    if not isinstance(runs, list):
        raise Unread("gh run list did not return a list")
    for r in runs:
        if not (isinstance(r, dict) and isinstance(r.get("databaseId"), int)
                and isinstance(r.get("headSha"), str) and isinstance(r.get("event"), str)):
            raise Unread(f"gh run list returned an unreadable entry: {r!r}")
    return [r for r in runs if r["headSha"] == sha and r["event"] == "push"]


def find_run(root, branch, sha, deadline, exclude=()):
    """The newest entry-gate push run for exactly this commit whose ID is not in
    `exclude` (runs that existed before this push); None when time runs out."""
    while True:  # looks at least once; the deadline bounds the waiting
        mine = [r for r in list_runs(root, branch, sha) if r["databaseId"] not in exclude]
        if mine:
            return max(mine, key=lambda r: r["databaseId"])
        if time.monotonic() >= deadline:
            return None
        pause(deadline)


RUNNING = {"queued", "in_progress", "waiting", "requested", "pending"}


def view_run(root, run_id):
    state = gh_json(root, "run", "view", str(run_id), "--json", "status,conclusion,headSha,attempt")
    if not isinstance(state, dict) or not isinstance(state.get("status"), str):
        raise Unread(f"run {run_id}: unreadable state")
    if state["status"] != "completed" and state["status"] not in RUNNING:
        raise Unread(f"run {run_id} has an unknown status {state['status']!r}")
    if state["status"] == "completed" and not (isinstance(state.get("attempt"), int) and state["attempt"] >= 1):
        raise Unread(f"run {run_id}: unreadable attempt {state.get('attempt')!r}")
    return state


def wait_run(root, run_id, deadline):
    while True:
        state = view_run(root, run_id)
        if state["status"] == "completed":
            return state
        if time.monotonic() >= deadline:
            return None
        pause(deadline)


def still_green(root, run_id, sha, attempt):
    """Re-read the run right before publishing: same commit, same attempt, success."""
    state = view_run(root, run_id)
    return (state.get("headSha") == sha and state.get("attempt") == attempt
            and state["status"] == "completed" and state.get("conclusion") == "success")


def installed_commit():
    path = Path(os.environ.get("KERD_RELEASE_INSTALLED",
                               Path.home() / ".claude/plugins/installed_plugins.json"))
    try:
        entries = json.loads(path.read_text())["plugins"]["kerd@kerd-marketplace"]
        return entries[0]["gitCommitSha"]
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return None


def remote_sha(root, branch):
    out = git(root, "ls-remote", "origin", f"refs/heads/{branch}")
    return out.split()[0] if out else None


PLUGIN_BRANCH = "plugin"


def repository_identity(url):
    """One spelling for a git remote, so https, ssh and scp-style forms of the same
    repository compare equal: ("host", "path") with the host lowercased and any
    `.git` or trailing slash dropped; GitHub paths are case-insensitive, so they
    are lowercased too. A local path or file:// URL becomes ("file", real path).
    None when the form is not one of these."""
    if not isinstance(url, str) or not url.strip():
        return None
    url = url.strip()
    if url.startswith("file://"):
        path = url[len("file://"):]
    elif url.startswith("/"):
        path = url
    else:
        path = None
    if path is not None:
        return ("file", re.sub(r"\.git$", "", str(Path(path).resolve()).rstrip("/")))
    match = (re.match(r"^(?:https?|ssh|git)://(?:[^@/]+@)?([^/:]+)(?::\d+)?/(.+)$", url)
             or re.match(r"^(?:[^@/]+@)?([^/:]+):(?!/)(.+)$", url))
    if not match:
        return None
    host, path = match.group(1).lower(), match.group(2).rstrip("/")
    path = re.sub(r"\.git$", "", path).strip("/")
    if not path or ".." in path.split("/"):
        return None
    return (host, path.lower() if host == "github.com" else path)


def push_destination(root):
    """The one URL `git push origin` reaches, proven equal to the one ship reads
    from. Several URLs, or a pushurl naming another repository, leave ship unable
    to prove where the push goes, so that refuses."""
    fetch = [u for u in git(root, "remote", "get-url", "--all", "origin").splitlines() if u.strip()]
    push = [u for u in git(root, "remote", "get-url", "--push", "--all", "origin").splitlines() if u.strip()]
    if len(fetch) != 1 or len(push) != 1:
        raise Refused(f"origin has {len(fetch)} fetch and {len(push)} push URLs; can't prove where the push goes; "
                      "set one URL")
    if repository_identity(push[0]) is None or repository_identity(push[0]) != repository_identity(fetch[0]):
        raise Refused(f"origin pushes to {push[0]!r} but reads from {fetch[0]!r}; can't prove where the push goes; "
                      "set one URL")
    return push[0]


def plugin_ref(root, sha):
    """The push URL when the shipped commit's marketplace sends Claude Code users to the
    generated plugin branch (`"ref": "plugin"` on the kerd entry), False when the
    entry has no ref (None). Anything unreadable or unexpected refuses: guessing here
    could point every install at a branch this ship never fills. With the ref,
    the source must be a `url` or `github` source naming the very repository ship
    pushes to (origin), or the branch ship fills is not the one users read."""
    name = ".claude-plugin/marketplace.json"
    try:
        data = json.loads(git(root, "show", f"{sha}:{name}"))
    except ValueError as error:
        raise Refused(f"{name} at {sha[:8]} is not readable JSON: {error}")
    plugins = data.get("plugins") if isinstance(data, dict) else None
    if not isinstance(plugins, list):
        raise Refused(f"{name}: no plugins list")
    entries = [p for p in plugins if isinstance(p, dict) and p.get("name") == "kerd"]
    if len(entries) != 1:
        raise Refused(f"{name}: expected one kerd entry, found {len(entries)}")
    source = entries[0].get("source")
    if not isinstance(source, dict):
        raise Refused(f"{name}: the kerd entry's source is not an object: {source!r}")
    if "sha" in source:
        raise Refused(f"{name}: a pinned sha on the kerd source would freeze users; ship does not handle it")
    ref = source.get("ref")
    if ref is None:
        return None
    if ref != PLUGIN_BRANCH:
        raise Refused(f"{name}: the kerd source names ref {ref!r}; ship only knows {PLUGIN_BRANCH!r}")
    kind = source.get("source")
    if kind == "url":
        named = source.get("url")
    elif kind == "github":
        repo = source.get("repo")
        named = f"https://github.com/{repo}" if isinstance(repo, str) and repo.count("/") == 1 else None
    else:
        raise Refused(f"{name}: a {kind!r} kerd source with ref {PLUGIN_BRANCH!r} is not one ship fills "
                      "(url or github only)")
    origin = push_destination(root)
    wanted, have = repository_identity(named), repository_identity(origin)
    if wanted is None or have is None:
        raise Refused(f"{name}: cannot compare the kerd source {named!r} with origin {origin!r}")
    if wanted != have:
        raise Refused(f"{name}: the kerd source names {named!r}, but ship pushes to origin {origin!r}")
    return origin


def is_ancestor(root, older, newer):
    return run(["git", "merge-base", "--is-ancestor", older, newer], root).returncode == 0


def from_commit(root, sha, *args):
    """Run a tools/ script from a worktree at the checked commit, so the code that
    publishes is the code CI checked, never the working tree. Its scratch output
    is removed afterwards."""
    scratch = Path(tempfile.mkdtemp(prefix="kerd-release-"))
    tree = scratch / "tree"
    try:
        added = run(["git", "worktree", "add", "--detach", str(tree), sha], root)
        if added.returncode != 0:
            return subprocess.CompletedProcess(args, 1, "", f"could not check out {sha[:8]}: {added.stderr.strip()}")
        try:
            return run([sys.executable, *[str(a).replace("{scratch}", str(scratch)) for a in args]], tree)
        finally:
            run(["git", "worktree", "remove", "--force", str(tree)], root)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def manifest_version(text, label):
    try:
        data = json.loads(text)
    except ValueError as error:
        raise Refused(f"{label} is not readable JSON: {error}")
    version = data.get("version") if isinstance(data, dict) else None
    if not (isinstance(version, str) and SEMVER.match(version)):
        raise Refused(f"{label} has no MAJOR.MINOR.PATCH version: {version!r}")
    return data, version


def plugin_package(root, tip, history):
    """Validate origin's plugin tip as a Kerd package before main moves: it must
    carry release.json, .claude-plugin/plugin.json (name kerd, same version) and
    hooks/hooks.json, and be built from a commit in `history` (origin/main's
    history). Returns (version, source commit). Anything else refuses."""
    fetched = run(["git", "fetch", "-q", "--no-tags", "origin", tip], root)
    if fetched.returncode != 0:
        raise Refused(f"could not fetch {PLUGIN_BRANCH} tip {tip[:8]}: {fetched.stderr.strip()}")
    label = f"{PLUGIN_BRANCH} tip {tip[:8]}"
    release, version = manifest_version(git(root, "show", f"{tip}:release.json"), f"{label} release.json")
    manifest, manifest_v = manifest_version(git(root, "show", f"{tip}:.claude-plugin/plugin.json"),
                                            f"{label} plugin.json")
    if manifest.get("name") != "kerd" or manifest_v != version:
        raise Refused(f"{label}: plugin.json ({manifest.get('name')!r} {manifest_v}) does not match "
                      f"release.json ({version})")
    git(root, "cat-file", "-e", f"{tip}:hooks/hooks.json")
    source = release.get("source_commit")
    if not (isinstance(source, str) and re.fullmatch(r"[0-9a-f]{40}", source)):
        raise Refused(f"{label}: unreadable source_commit {source!r}")
    if run(["git", "cat-file", "-e", f"{source}^{{commit}}"], root).returncode != 0:
        raise Refused(f"{label} was built from {source[:8]}, which is not in this checkout; run git fetch origin")
    if not is_ancestor(root, source, history):
        raise Refused(f"{label} was built from {source[:8]}, which is not in origin/main's history")
    return version, source


def append_plugin(root, sha, source, before, destination, version):
    """Append one plugin-branch commit built from `source`, using the publisher in
    the shipped commit `sha`, pushed to `destination` onto exactly the tip
    `before` that ship checked (None: no branch yet). The publisher refuses any
    other tip and its push carries a lease on it. Afterwards the commit it names
    must be origin's tip, have `before` as its only parent and carry this
    source and version. Returns (new tip, None) or (None, why it failed)."""
    result = from_commit(root, sha, "tools/plugin_release.py", "--ref", source, "--remote", destination,
                         "--expect-tip", before or "none", "--publish", "{scratch}/build")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        return None, f"exit {result.returncode}: {result.stderr.strip()}"
    named = re.findall(r"^Published plugin branch: ([0-9a-f]{40})$", result.stdout, re.M)
    if len(named) != 1:
        return None, "the publisher did not name exactly one published commit"
    made = named[0]
    after = remote_sha(root, PLUGIN_BRANCH)
    if after != made:
        return None, f"origin/{PLUGIN_BRANCH} is {after and after[:8]}, not the published {made[:8]}"
    fetched = run(["git", "fetch", "-q", "--no-tags", "origin", made], root)
    if fetched.returncode != 0:
        return None, f"could not fetch the published {made[:8]}: {fetched.stderr.strip()}"
    parents = git(root, "rev-list", "--parents", "-n", "1", made).split()[1:]
    if parents != ([before] if before else []):
        return None, f"the published {made[:8]} has parents {parents}, not {before or 'none'}"
    try:
        release = json.loads(git(root, "show", f"{made}:release.json"))
    except ValueError as error:
        return None, f"the published {made[:8]} has no readable release.json: {error}"
    if release != {"version": version, "source_commit": git(root, "rev-parse", f"{source}^{{commit}}")}:
        return None, f"the published {made[:8]} records {release}, not {version} from {source[:8]}"
    return made, None


def ship(root, codex=False, plugin=False, deadline_seconds=900):
    root = Path(root)
    if not (isinstance(deadline_seconds, (int, float)) and 0 <= deadline_seconds < 86400):
        raise Refused(f"deadline must be 0 to 86400 seconds, got {deadline_seconds!r}")
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if branch == "HEAD":
        raise Refused("detached HEAD: check out a branch first")
    if (codex or plugin) and branch != "main":
        raise Refused(f"--codex and --plugin publish from main only; this is {branch}")
    sha = git(root, "rev-parse", "HEAD")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise Refused("tracked files have uncommitted changes")
    rules = run([sys.executable, "tools/release_check.py"], root)
    if rules.returncode != 0:
        raise Refused("release check failed:\n" + rules.stdout + rules.stderr)
    if git(root, "rev-parse", "HEAD") != sha or git(root, "status", "--porcelain", "--untracked-files=no"):
        raise Refused("HEAD or tracked files changed while checking; run ship again")
    # Read from the commit being shipped, not the working tree, so nothing that
    # changes on disk after the checks above can alter what is compared below.
    _manifest, version = manifest_version(git(root, "show", f"{sha}:.claude-plugin/plugin.json"),
                                          f"plugin.json at {sha[:8]}")
    already = remote_sha(root, branch) == sha
    # The plugin branch is what Claude Code users install once the marketplace
    # names it. Read from the shipped commit; unreadable refuses (exit 2).
    destination = plugin_ref(root, sha)
    if destination and branch != "main":
        print(f"ship: marketplace names the {PLUGIN_BRANCH} branch; it is appended only from main, not {branch}")
        destination = None
    slim = bool(destination)
    plugin_tip = remote_sha(root, PLUGIN_BRANCH) if slim else None
    bootstrap = None
    if slim:
        # Everything the plugin path depends on is proven here, before main moves:
        # after the main push there is no taking it back.
        history = remote_sha(root, branch)
        if history is None:
            raise Refused(f"origin has no {branch}")
        if run(["git", "cat-file", "-e", f"{history}^{{commit}}"], root).returncode != 0:
            raise Refused(f"origin/{branch} {history[:8]} is not in this checkout; run git fetch origin")
        if not is_ancestor(root, history, sha):
            raise Refused(f"origin/{branch} {history[:8]} is not an ancestor of {sha[:8]}")
        have = label = None
        if plugin_tip:
            have, _source = plugin_package(root, plugin_tip, history)
            label = f"origin/{PLUGIN_BRANCH}"
        elif not already:  # the first plugin commit will be built from origin/main
            _data, have = manifest_version(git(root, "show", f"{history}:.claude-plugin/plugin.json"),
                                           f"origin/{branch} {history[:8]} plugin.json")
            label = f"origin/{branch} {history[:8]}"
        if have is not None and as_tuple(version) <= as_tuple(have):
            # Claude Code updates on a new version only: an equal or lower one
            # would leave users on the old package while main says otherwise.
            raise Refused(f"version {version} is not newer than {have} on {label}; bump the version (prep) first")
    if slim and plugin_tip is None:
        if already:
            print(f"ship: WARNING origin/{branch} already names a {PLUGIN_BRANCH} branch that does not exist; "
                  "it is created after CI passes")
        else:
            # First switch: pushing main would point every install at a missing
            # branch, so the branch is created first, from what origin/main already
            # serves (the release users install today), before main moves.
            bootstrap = history
            _data, bootstrap_version = manifest_version(
                git(root, "show", f"{bootstrap}:.claude-plugin/plugin.json"), f"origin/{branch} plugin.json")
    print(f"ship: {version} at {sha[:8]} on {branch}")
    print(f"    will: "
          + (f"create {PLUGIN_BRANCH} from origin/{branch} {bootstrap[:8]}; " if bootstrap else "")
          + f"push {sha[:8]} to {branch}; wait for entry-gate on {sha[:8]}"
          + (f"; append {PLUGIN_BRANCH} from {sha[:8]}" if slim else "")
          + ("; publish codex" if codex else "") + ("; update Kerd in Claude Code" if plugin else ""))
    published = []

    def stop(code, message):
        done = ", ".join(published) if published else "nothing"
        print(f"{message}; published: {done}")
        return code

    exclude = set()
    if not already:
        try:
            exclude = {r["databaseId"] for r in list_runs(root, branch, sha)}
        except Unread as error:
            raise Refused(f"before pushing: {error}")
    try:
        if bootstrap:
            if remote_sha(root, branch) != bootstrap:
                return stop(4, f"origin/{branch} moved before the {PLUGIN_BRANCH} branch was created; {branch} not pushed")
            plugin_tip, why = append_plugin(root, sha, bootstrap, None, destination, bootstrap_version)
            if why:
                return stop(1, f"{PLUGIN_BRANCH}: first build from {bootstrap[:8]} FAILED ({why}); {branch} not pushed")
            published.append(f"{PLUGIN_BRANCH} branch at {plugin_tip[:8]} from {bootstrap[:8]}")
        if already:
            print(f"pushed: not needed, origin/{branch} already holds {sha[:8]}; using its newest push run")
        else:
            pushed = run(["git", "push", "origin", f"{sha}:refs/heads/{branch}"], root)
            if pushed.returncode != 0:
                return stop(1, f"push FAILED: {pushed.stderr.strip()}")
            print(f"pushed: {sha[:8]} to {branch}")
        if remote_sha(root, branch) != sha:
            return stop(4, f"push: origin/{branch} does not hold {sha[:8]}")
        deadline = time.monotonic() + deadline_seconds
        found = find_run(root, branch, sha, deadline, exclude)
        if found is None:
            return stop(3, f"ci: no new entry-gate run for {sha[:8]} seen within {deadline_seconds:.0f} s")
        run_id = found["databaseId"]
        print(f"ci: run {run_id} found")
        state = wait_run(root, run_id, deadline)
        if state is None:
            return stop(3, f"ci: run {run_id} still running after {deadline_seconds:.0f} s")
        if state.get("headSha") != sha:
            return stop(1, f"ci: run {run_id} is for {state.get('headSha')}, not {sha}")
        if state.get("conclusion") != "success":
            print(f"ci: run {run_id} FAILED ({state.get('conclusion')})")
            try:
                log = run([gh_cmd(), "run", "view", str(run_id), "--log-failed"], root, timeout=60)
                if log.returncode == 0 and log.stdout.strip():
                    print("\n".join(log.stdout.splitlines()[-60:]))
                else:
                    print(f"ci: failing lines not retrieved (exit {log.returncode}): {log.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print("ci: failing lines not retrieved: gh gave no answer within 60 s")
            return stop(1, "ci: failed")
        attempt = state.get("attempt")
        print(f"ci: run {run_id} attempt {attempt} passed")
        target = sha  # The commit Claude Code should report as installed.
        if slim:
            if (not still_green(root, run_id, sha, attempt) or remote_sha(root, branch) != sha
                    or remote_sha(root, PLUGIN_BRANCH) != plugin_tip):
                return stop(4, f"ci: run {run_id}, origin/{branch} or origin/{PLUGIN_BRANCH} changed "
                               f"before the {PLUGIN_BRANCH} append")
            new, why = append_plugin(root, sha, sha, plugin_tip, destination, version)
            if why:
                return stop(1, f"{PLUGIN_BRANCH}: append FAILED ({why})")
            published.append(f"{PLUGIN_BRANCH} branch at {new[:8]} from {sha[:8]}")
            plugin_tip = target = new
        if codex:
            if not still_green(root, run_id, sha, attempt):
                return stop(4, f"ci: run {run_id} changed before the codex publish")
            # The publisher runs from a worktree at the checked commit, so its own code is what CI checked.
            result = from_commit(root, sha, "tools/codex_release.py", "--ref", sha, "--publish", "{scratch}/build")
            print(result.stdout.strip())
            if result.returncode != 0:
                return stop(1, f"codex: publish FAILED (exit {result.returncode}): {result.stderr.strip()}")
            published.append(f"codex at {sha[:8]}")
        if plugin:
            for command in (["plugin", "marketplace", "update", "kerd-marketplace"],
                            ["plugin", "update", "kerd@kerd-marketplace"]):
                if (not still_green(root, run_id, sha, attempt) or remote_sha(root, branch) != sha
                        or (slim and remote_sha(root, PLUGIN_BRANCH) != plugin_tip)):
                    return stop(4, f"ci: run {run_id} or origin/{branch} changed before claude {' '.join(command)}")
                updated = run([claude_cmd(), *command], root)
                if updated.returncode != 0:
                    return stop(1, f"plugin: claude {' '.join(command)} FAILED: {updated.stderr.strip()}")
            got = installed_commit()
            if got != target:
                published.append(f"Claude Code plugin at {got or 'an unread commit'}")
                expected = f"the {PLUGIN_BRANCH} branch commit {target[:8]}" if slim else f"the checked {sha[:8]}"
                return stop(4, f"plugin: installed commit is {got or 'unreadable'}, not {expected}")
            published.append(f"Claude Code plugin at {target[:8]} (loads on restart)")
        return stop(0, "ship: done")
    except (Unread, Refused) as error:
        return stop(4, f"ci: {error}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", default=str(ROOT))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    prep_parser = sub.add_parser("prep")
    prep_parser.add_argument("version")
    prep_parser.add_argument("--note", required=True, help="file holding the release note")
    ship_parser = sub.add_parser("ship")
    ship_parser.add_argument("--codex", action="store_true")
    ship_parser.add_argument("--plugin", action="store_true")
    ship_parser.add_argument("--deadline", type=float, default=900)
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            return check(args.root)
        if args.command == "prep":
            return prep(args.root, args.version, Path(args.note).read_text())
        return ship(args.root, args.codex, args.plugin, args.deadline)
    except Refused as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
