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
check after the fact, not a lock). Every stop says what was already published. Anything
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
    version = current_version(root)
    already = remote_sha(root, branch) == sha
    print(f"ship: {version} at {sha[:8]} on {branch}")
    print(f"    will: push {sha[:8]} to {branch}; wait for entry-gate on {sha[:8]}"
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
        if codex:
            if not still_green(root, run_id, sha, attempt):
                return stop(4, f"ci: run {run_id} changed before the codex publish")
            # The publisher runs from a worktree at the checked commit, so its own code is what CI checked.
            scratch = Path(tempfile.mkdtemp(prefix="kerd-codex-"))
            tree = scratch / "tree"
            added = run(["git", "worktree", "add", "--detach", str(tree), sha], root)
            if added.returncode != 0:
                return stop(1, f"codex: could not check out {sha[:8]}: {added.stderr.strip()}")
            try:
                result = run([sys.executable, "tools/codex_release.py", "--ref", sha, "--publish",
                              str(scratch / "build")], tree)
            finally:
                run(["git", "worktree", "remove", "--force", str(tree)], root)
            print(result.stdout.strip())
            if result.returncode != 0:
                return stop(1, f"codex: publish FAILED (exit {result.returncode}): {result.stderr.strip()}")
            published.append(f"codex at {sha[:8]}")
        if plugin:
            for command in (["plugin", "marketplace", "update", "kerd-marketplace"],
                            ["plugin", "update", "kerd@kerd-marketplace"]):
                if not still_green(root, run_id, sha, attempt) or remote_sha(root, branch) != sha:
                    return stop(4, f"ci: run {run_id} or origin/{branch} changed before claude {' '.join(command)}")
                updated = run([claude_cmd(), *command], root)
                if updated.returncode != 0:
                    return stop(1, f"plugin: claude {' '.join(command)} FAILED: {updated.stderr.strip()}")
            got = installed_commit()
            if got != sha:
                published.append(f"Claude Code plugin at {got or 'an unread commit'}")
                return stop(4, f"plugin: installed commit is {got or 'unreadable'}, not the checked {sha[:8]}")
            published.append(f"Claude Code plugin at {sha[:8]} (loads on restart)")
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
