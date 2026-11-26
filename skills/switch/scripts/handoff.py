#!/usr/bin/env python3
"""Small Git handoff primitives. Memory judgment and session control stay with Switch."""

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


class HandoffError(Exception):
    pass


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if result.returncode:
        raise HandoffError(result.stderr.strip() or f"git {args[0]} failed")
    return result.stdout if "-z" in args else result.stdout.rstrip("\n")


def root_for(path):
    return Path(git(path, "rev-parse", "--show-toplevel")).resolve()


RECORD_CAP_BYTES = 32768  # informational size for the start point (CONTEXT.md); the Read tool fails past 256 KB


def mark_over_cap(sources, picks, sizes, cap):
    """Flag each source over the cap and name them; informational, never a refusal."""
    labels = []
    for source, (path, heading), size in zip(sources, picks, sizes):
        source["over_cap"] = size > cap
        if source["over_cap"]:
            labels.append(path if heading is None else f"{path} \u00a7 {heading}")
    return labels


def require_branch(root, branch):
    if not branch or branch.startswith("-"):
        raise HandoffError("An explicit branch name is required")
    git(root, "check-ref-format", "--branch", branch)
    current = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if current != branch:
        raise HandoffError(f"Expected branch {branch}; current branch is {current}. No checkout performed")


def relative_file(root, value):
    path = root / value
    relative = path.relative_to(root) if path.is_absolute() else path
    if Path(value).is_absolute() or ".." in relative.parts or ".git" in relative.parts or str(relative) in {"", "."}:
        raise HandoffError("Specify individual project-relative files, not directories or Git metadata")
    actual = path.resolve()
    if (not actual.is_relative_to(root) or actual == root or path.is_dir() or path.is_symlink()
            or ".git" in actual.relative_to(root).parts
            or any(parent.is_symlink() for parent in path.parents if parent != root and parent.is_relative_to(root))):
        raise HandoffError("A handoff file cannot escape the project or be a directory/symlink")
    if not path.exists():
        git(root, "ls-files", "--error-unmatch", "--", str(relative))
    return str(relative)


def local_changes(root, *scope):
    """Changed and untracked paths, repo-relative; `scope` narrows to pathspecs under the repo root."""
    spec = ["--", *scope] if scope else []
    changed = set(filter(None, git(root, "diff", "--name-only", "-z", *spec).split("\0")))
    changed.update(filter(None, git(root, "ls-files", "--others", "--exclude-standard", "-z", *spec)
                          .split("\0")))
    return changed


NOTES_PREFIX = "notes:"


def config_bytes(root):
    """kivna/vault.json's bytes, or None only when it is confirmed absent.

    Absent means the path does not exist (nor does `kivna/` as a folder). A
    directory, a dangling or other non-regular entry, or an error reading it is
    not absence: it refuses, so a check never quietly skips the notes repo.
    """
    config = root / "kivna" / "vault.json"
    try:
        os.lstat(config)
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError as exc:
        raise HandoffError(f"Cannot inspect {config}: {exc.strerror or exc}")
    try:
        info = os.stat(config)
        if not stat.S_ISREG(info.st_mode):
            raise HandoffError(f"{config} is not a regular file, so whether notes are kept in the vault "
                               "is unknown")
        return config.read_bytes()
    except OSError as exc:
        raise HandoffError(f"Cannot read {config}: {exc.strerror or exc}")


def notes_location(root, raw=None):
    """(notes root, notes repo) when the project keeps work notes in the vault, else None.

    `"work_notes": "vault"` in kivna/vault.json puts the notes root at
    <vault>/<folder>/work. A confirmed-absent file, or a JSON object without
    the key: no notes root. A file that cannot be inspected or read, is not a
    regular file, or is not a JSON object refuses (see `config_bytes`). A set key whose
    root is missing or outside a Git repo is an error naming the path, never a
    silent fall back to the project. The folder is a plain relative name, no
    part of <folder>/work may be a symlink, the resolved root must stay under
    the resolved vault, and the notes repo cannot be the project's own repo.
    """
    config = root / "kivna" / "vault.json"
    raw = config_bytes(root) if raw is None else raw
    if raw is None:
        return None
    try:
        settings = json.loads(raw.decode("utf-8"))
    except ValueError as exc:
        raise HandoffError(f"Cannot read {config}: {exc}")
    if not isinstance(settings, dict):
        raise HandoffError(f"{config} is not a JSON object, so whether notes are kept in the vault is unknown")
    if "work_notes" not in settings:
        return None
    if settings["work_notes"] != "vault":
        raise HandoffError(f"Unrecognised work_notes value in {config}: {settings['work_notes']!r}; "
                           "the only setting is \"vault\"")
    vault, folder = settings.get("vault"), settings.get("folder")
    if not isinstance(vault, str) or not vault or not isinstance(folder, str) or not folder:
        raise HandoffError(f"{config} sets work_notes but lacks a vault path or folder")
    parts = Path(folder).parts
    if (Path(folder).is_absolute() or not parts or any(part in {".", "..", ".git"} for part in parts)
            or "\\" in folder):
        raise HandoffError(f"The vault folder in {config} must be a plain relative name: {folder!r}")
    base = root / Path(os.path.expanduser(vault))
    notes = base
    for part in (*parts, "work"):
        notes = notes / part
        if notes.is_symlink():
            raise HandoffError(f"The notes root cannot pass through a symlink: {notes}")
    if not notes.is_dir():
        raise HandoffError(f"Notes root does not exist: {notes}")
    notes = notes.resolve()
    if not notes.is_relative_to(base.resolve()):
        raise HandoffError(f"Notes root escapes the vault: {notes}")
    try:
        repo = root_for(notes)
    except HandoffError:
        raise HandoffError(f"Notes root is not in a Git repo: {notes}")
    if repo == Path(root).resolve():
        raise HandoffError(f"The notes root is inside the project's own repo, so its notes would be public: {notes}")
    return notes, repo


def notes_scope(location):
    """Pathspecs that confine a notes-repo check to the notes root."""
    relative = str(location[0].relative_to(location[1]))
    return [] if relative == "." else [":(literal)" + relative]


def notes_tree(location, revision="HEAD"):
    """The committed tree of the notes root at a revision; None only when confirmed absent.

    `rev-parse --verify` answers "Needed a single revision" alike for a missing
    path and a bad revision, so the two are read apart: the revision must
    resolve to a commit (any failure raises), then `ls-tree` lists the path,
    where a successful empty listing is the one confirmed absence and any
    other failure raises. Two failed reads therefore never compare as equal.
    """
    repo = location[1]
    relative = location[0].relative_to(repo).as_posix()
    commit = git(repo, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    if relative == ".":
        return git(repo, "rev-parse", "--verify", "--end-of-options", f"{commit}^{{tree}}")
    listed = [entry for entry in git(repo, "--literal-pathspecs", "ls-tree", "-z", commit, "--", relative)
              .split("\0") if entry]
    if not listed:
        return None
    entries = [entry for entry in listed if entry.partition("\t")[2] == relative]
    if len(entries) != 1:  # a listing that names something else is not a reading of this path
        raise HandoffError(f"Could not read the notes root {relative} at {revision} in {repo}")
    return entries[0].partition("\t")[0].split()[2]


def notes_unsaved(location):
    scope = notes_scope(location)
    spec = ["--", *scope] if scope else []
    staged = filter(None, git(location[1], "diff", "--cached", "--name-only", "-z", *spec).split("\0"))
    return sorted(local_changes(location[1], *scope) | set(staged))


def full_commit(value, label):
    if value is not None and (not isinstance(value, str)
                              or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value)):
        raise HandoffError(f"The {label} must be a full Git commit ID, not a branch or abbreviated name")


def ready_notes(location, sync=False, expected=None):
    """Bring the notes repo to a state a pickup may read; never reset, merge, stash or rebase.

    Unsaved changes inside the notes root refuse. With sync, the notes branch is
    fetched and fast-forwarded only; ahead or diverged history refuses. A saved
    notes commit, when given, is a pin: the notes repo HEAD must contain it and
    the notes root's tree must be the same at both, so a later change to these
    notes refuses while a later commit elsewhere in the vault does not.
    """
    notes_root, repo = location
    if notes_unsaved(location):
        raise HandoffError(f"Unsaved changes inside the notes root {notes_root}; "
                           "no pull, stash, reset or merge performed")
    if sync:
        branch = subprocess.run(["git", "-C", str(repo), "symbolic-ref", "--quiet", "--short", "HEAD"],
                                text=True, capture_output=True).stdout.strip()
        if not branch:
            raise HandoffError(f"The notes repo {repo} is not on a branch; nothing fetched or moved")
        git(repo, "fetch", "origin", f"refs/heads/{branch}")
        local, remote = git(repo, "rev-parse", "HEAD"), git(repo, "rev-parse", "FETCH_HEAD")
        if git(repo, "merge-base", local, remote) != local:
            raise HandoffError(f"The notes repo {repo} is ahead of or diverged from its remote; "
                               "resolve it before pickup")
        git(repo, "merge", "--ff-only", "--no-overwrite-ignore", remote)
    head = git(repo, "rev-parse", "HEAD")
    if expected is not None:
        probe = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", expected, head],
                               text=True, capture_output=True)
        if probe.returncode:
            raise HandoffError(f"The notes repo {repo} does not contain the saved notes commit {expected}"
                               + ("" if sync else "; pick up with --sync to fetch it"))
        if notes_tree(location, expected) != notes_tree(location, head):
            raise HandoffError(f"The vault's notes changed after this Out (recorded {expected}, now {head}); "
                               "pick up the newer Out or pass its commit")
    return head


def notes_unchanged(location, head):
    if git(location[1], "rev-parse", "HEAD") != head or notes_unsaved(location):
        raise HandoffError("Notes changed while reading the pickup; no pickup returned")


def resolve_source(root, value, location=None):
    """(value as named, directory, relative path, location) for a project or notes: source."""
    if not value.startswith(NOTES_PREFIX):
        relative = relative_file(root, value)
        return relative, root, relative, location
    location = location or notes_location(root)
    if location is None:
        raise HandoffError("A notes: source needs a notes root; set \"work_notes\": \"vault\" "
                           "in kivna/vault.json: " + value)
    relative = relative_file(location[0], value[len(NOTES_PREFIX):])
    return NOTES_PREFIX + relative, location[0], relative, location


def require_tracked(base, relative, where):
    """The same tracked rule for every reading-set source, project or notes."""
    try:
        git(base, "ls-files", "--error-unmatch", "--", ":(literal)" + relative)
    except HandoffError:
        raise HandoffError(f"Not tracked in {where}: {relative}")


def scoped(root, folders):
    """Pathspecs confining a pickup's unsaved-changes check to named folders.

    For a project whose records sit in a repo it shares with other projects
    (a vault): only changes inside these folders refuse the pickup. Each must be
    an existing folder inside the project, named exactly, not the project root,
    Git metadata or a symlink. None given: the whole project, unchanged.
    """
    specs = []
    for value in folders:
        path = root / value
        if Path(value).is_absolute() or ".." in Path(value).parts or ".git" in Path(value).parts:
            raise HandoffError("A scope is a folder inside the project, named relative to it: " + str(value))
        if not path.is_dir() or path.is_symlink() or any(
                parent.is_symlink() for parent in path.parents if parent != root and parent.is_relative_to(root)):
            raise HandoffError("A scope must be an existing folder in the project, not a file or symlink: "
                               + str(value))
        parent = root
        for part in Path(os.path.normpath(value)).parts:  # Git compares case; this filesystem may not
            if part not in os.listdir(parent):
                raise HandoffError("Spell a scope exactly as the folder is named on disk: " + str(value))
            parent = parent / part
        relative = path.resolve().relative_to(root).as_posix()
        if relative in {"", "."}:
            raise HandoffError("A scope narrows the project; the project root is not a scope")
        specs.append(":(literal)" + relative)
    if len(specs) != len(set(specs)):
        raise HandoffError("List each scope once")
    return specs


def unsaved(root, keep, scope):
    """Unsaved paths within the scope: staged always, changed and untracked less the preserved ones."""
    spec = ["--", *scope] if scope else []
    staged = set(filter(None, git(root, "diff", "--cached", "--name-only", "-z", *spec).split("\0")))
    return sorted(staged | (local_changes(root, *scope) - set(keep)))


def in_scope(relative, scope):
    folders = [spec[len(":(literal)"):] for spec in scope]
    return not scope or any(relative == f or relative.startswith(f + "/") for f in folders)


def outside_scope(root, values, scope):
    """Refuse, before anything moves, a project source a scope leaves unchecked."""
    folders = scoped(root, scope)
    if not folders:
        return
    outside = sorted({value for value in values if not value.startswith(NOTES_PREFIX)
                      and not in_scope(relative_file(root, value), folders)})
    if outside:
        raise HandoffError("Sources outside the scope, where unsaved changes go unchecked: " + ", ".join(outside))


def config_saved(root):
    """A scoped pickup trusts kivna/vault.json, which names the notes repo, only as saved.

    It sits outside the scope, so the scoped check never sees it: require it
    tracked, not a symlink and unchanged from HEAD, whatever --preserve names.
    """
    config = root / "kivna" / "vault.json"
    if not config.exists() and not config.is_symlink():
        if git(root, "ls-files", "--", ":(literal)kivna/vault.json") or subprocess.run(
                ["git", "-C", str(root), "cat-file", "-e", "HEAD:kivna/vault.json"],
                capture_output=True).returncode == 0:
            raise HandoffError("kivna/vault.json names the notes repo and is deleted here; "
                               "a scoped pickup needs it saved, unchanged")
        return
    if config.is_symlink():
        raise HandoffError("kivna/vault.json names the notes repo; it cannot be a symlink in a scoped pickup")
    try:
        git(root, "ls-files", "--error-unmatch", "--", ":(literal)kivna/vault.json")
        git(root, "diff", "--quiet", "HEAD", "--", ":(literal)kivna/vault.json")
    except HandoffError:
        raise HandoffError("kivna/vault.json names the notes repo and must be saved, unchanged, "
                           "for a scoped pickup")


def acknowledged(root, paths):
    """Exact untracked paths the project keeps locally: never saved, never touched.

    An acknowledgement is a decision already made about specific files, not a
    rule. It is project-local and exact: no pattern, no directory, no ignore
    entry, no deletion and no stash. Tracked or missing paths are refused so an
    acknowledgement cannot quietly hide real work or a typo.
    """
    kept = []
    for value in paths:
        # Existence is checked before path resolution so a typo reports itself
        # rather than surfacing Git's "did you forget to add" pathspec error.
        if not (root / value).exists():
            raise HandoffError("Preserved path does not exist here: " + str(value))
        path = relative_file(root, value)
        if git(root, "ls-files", "--", ":(literal)" + path):
            raise HandoffError("Preserved path is tracked work, not a local leftover: " + path)
        kept.append(path)
    if len(kept) != len(set(kept)):
        raise HandoffError("List each preserved path once")
    return kept


def publish(root, branch, files, message, push=False, verify_commit=None, preserve=()):
    require_branch(root, branch)
    paths = [relative_file(root, value) for value in files]
    if not paths or len(paths) != len(set(paths)):
        raise HandoffError("Supply a nonempty unique list of handoff files")
    if not message.strip():
        raise HandoffError("Commit message must not be blank")
    if git(root, "diff", "--cached", "--name-only"):
        raise HandoffError("Index already contains staged work; preserve it and resolve the boundary first")
    keep = acknowledged(root, preserve)
    if set(paths) & set(keep):
        raise HandoffError("A file cannot be both saved and preserved: " + ", ".join(sorted(set(paths) & set(keep))))
    unexpected = local_changes(root) - set(paths) - set(keep)
    if unexpected:
        raise HandoffError("Unassigned changes need a decision: " + ", ".join(sorted(unexpected)))
    git(root, "add", "--", *paths)
    if git(root, "diff", "--cached", "--name-only"):
        git(root, "commit", "-m", message)
    commit = git(root, "rev-parse", "HEAD")
    if verify_commit is not None:
        verify_commit(commit)
    result = {"status": "saved_locally", "branch": branch, "commit": commit,
              "source_session_exited": False, "preserved_local_only": keep,
              "note": "Git save does not exit the caller or stop jobs"}
    if keep:
        result["note"] += "; preserved paths are local only and were not saved"
    if push:
        git(root, "push", "origin", f"HEAD:refs/heads/{branch}")
        remote = git(root, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
        if not remote or remote.split()[0] != commit:
            raise HandoffError("Push could not be verified at the remote branch; do not release source")
        result["status"] = "saved_to_remote"
    return result


FETCH_TIMEOUT = 60  # seconds; a fetch that hangs on a prompt or dead network counts as failed


def unsaved_paths(root, keep=(), scope=()):
    """Changed, untracked and staged paths within the scope, less the preserved ones."""
    spec = ["--", *scope] if scope else []
    return sorted((local_changes(root, *scope)
                   | set(filter(None, git(root, "diff", "--cached", "--name-only", "-z", *spec).split("\0"))))
                  - set(keep))


def current_branch(root):
    """The checked-out branch, or None for a detached HEAD; any other failure raises."""
    found = subprocess.run(["git", "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"],
                           text=True, capture_output=True)
    if found.returncode == 0:
        return found.stdout.strip() or None
    if found.returncode == 1:  # --quiet: exit 1, silently, means HEAD is detached
        return None
    raise HandoffError(found.stderr.strip() or "git symbolic-ref failed")


def default_branch(root):
    """The checked-out branch for a pickup given no --branch; a detached HEAD is an error."""
    found = current_branch(root)
    if not found:
        raise HandoffError("No --branch given and HEAD is detached; name the branch with --branch")
    return found


def remote_config(root):
    """Every `remote.*` setting (URLs, fetch refspecs and the rest), as Git prints them.

    `git config --get-regexp` exits 1 when nothing matches, which here means no
    remote settings at all; any other failure raises.
    """
    found = subprocess.run(["git", "-C", str(root), "config", "--get-regexp", r"^remote\."],
                           text=True, capture_output=True)
    if found.returncode == 0 or (found.returncode == 1 and not found.stdout and not found.stderr):
        return found.stdout
    raise HandoffError(found.stderr.strip() or "git config failed")


def remote_settings(config):
    """(remote name, variable, value) for each `remote.<name>.<variable>` line.

    Git prints the variable in lower case and keeps the name's case; a name may
    hold dots, so the variable is the part after the last one. A setting
    written with no value prints with no space and reads as "".
    """
    for line in config.splitlines():
        key, _, value = line.partition(" ")
        if key.startswith("remote.") and key.count(".") >= 2:
            name, _, variable = key[len("remote."):].rpartition(".")
            yield name, variable, value


FALSE_VALUES = {"false", "no", "off", "0"}


def unprovable_remotes(names, config):
    """Configurations under which a fetch here cannot prove the tracking refs current.

    Kerd does not model every Git fetch rule; it refuses instead. A negative
    refspec can leave a stale ref that still matches a positive destination,
    `skipDefaultUpdate` keeps a remote out of default fetches, and a refspec
    with more than one `*` on a side is a form this check does not read.
    """
    found = [f"remote {name} has a name that reads as an option" for name in sorted(names)
             if name.startswith("-")]
    for name, variable, value in remote_settings(config):
        if name not in names:
            continue
        if variable == "fetch" and value.startswith("^"):
            found.append(f"remote {name} has a negative fetch refspec ({value})")
        elif variable == "fetch" and any(side.count("*") > 1 for side in value.split(":", 1)):
            found.append(f"remote {name} has a fetch refspec this check does not read ({value})")
        elif variable == "skipdefaultupdate" and value.strip().lower() not in FALSE_VALUES:
            found.append(f"remote {name} sets skipDefaultUpdate")
    return found


def tracking_patterns(names, config):
    """Destinations of each configured remote's fetch refspecs, e.g. refs/remotes/origin/*.

    Only these refs are refreshed (and pruned) by fetching that remote with
    --prune; a leftover ref from a removed remote or outside the refspec is not.
    A refspec with no destination, or one outside refs/remotes/, adds nothing.
    """
    patterns = []
    for name, variable, value in remote_settings(config):
        if variable != "fetch" or name not in names or not value or value.startswith("^") or ":" not in value:
            continue
        destination = value.split(":", 1)[1]
        if destination.startswith("refs/remotes/"):
            patterns.append(destination)
    return patterns


def refreshed_ref(ref, patterns):
    for pattern in patterns:
        if "*" in pattern:
            head, _, tail = pattern.partition("*")
            if len(ref) > len(head) + len(tail) and ref.startswith(head) and ref.endswith(tail):
                return True
        elif ref == pattern:
            return True
    return False


def repo_state(root, keep=(), scope=()):
    """What a boundary verdict rests on, read so it can be compared again at the end."""
    return {"remotes": git(root, "remote"), "remote_config": remote_config(root),
            "commit": git(root, "rev-parse", "HEAD"), "unsaved": unsaved_paths(root, keep, scope)}


def repo_checks(root, keep=(), scope=(), allow_local_only=False):
    """The boundary checks for one repo: fetch, HEAD on a remote ref, nothing unsaved.

    Fetch and remote containment are repo-wide; `scope` (pathspecs) narrows only
    the unsaved-changes check, so a shared vault's other folders cannot refuse.
    With `allow_local_only`, a repo with no remote configured at all is checked
    as a local-only save: there is nothing to fetch or push to, so those two
    checks are not failures, and only the clean-tree check can refuse. A repo
    that has a remote keeps every check, whatever this flag says.

    Every git read here raises when it fails, so no verdict is returned; a
    detached HEAD is reported as no branch, not a failure. HEAD and the remote
    list are read first and the checks run against those values (containment
    against the captured commit, not a fresh HEAD). The returned `state` is what
    `boundary` reads again after every repo is checked.
    """
    failures = []
    remotes = git(root, "remote")
    config = remote_config(root)
    commit = git(root, "rev-parse", "HEAD")
    local_only = allow_local_only and not remotes
    if local_only:
        fetched, containing = False, []
    else:
        names = remotes.splitlines()
        for reason in unprovable_remotes(set(names), config):
            failures.append("The check can't prove the remote refs are current for this configuration ("
                            + reason + "); push and confirm by hand.")
        # Each captured remote is fetched by name, so none is left out the way
        # `fetch --all` leaves out a remote it skips.
        fetched = bool(names)
        for name in names:
            if name.startswith("-"):  # refused above; never passed to git as an argument
                fetched = False
                continue
            try:
                fetch = subprocess.run(["git", "-C", str(root), "fetch", "--quiet", "--prune", name], text=True,
                                       capture_output=True, timeout=FETCH_TIMEOUT,
                                       env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
                fetched = fetched and fetch.returncode == 0
            except subprocess.TimeoutExpired:
                fetched = False
        if not fetched:
            failures.append("The fetch failed, so the remote state is unknown; cached refs are not verification.")
        # Containment counts only refs this fetch refreshes: a configured remote's
        # fetch-refspec destinations. A leftover tracking ref proves nothing.
        patterns = tracking_patterns(set(remotes.splitlines()), config)
        containing = [ref[len("refs/remotes/"):] for ref in
                      git(root, "for-each-ref", "--contains", commit, "--format=%(refname)",
                          "refs/remotes").splitlines()
                      if ref and not ref.endswith("/HEAD") and refreshed_ref(ref, patterns)]
        if not containing:
            failures.append("No branch on a configured remote, as checked by this fetch, contains this "
                            "commit.")
    left = unsaved_paths(root, keep, scope)
    if left:
        failures.append(f"The working tree is not clean: {len(left)} unsaved "
                        + ("path" if len(left) == 1 else "paths") + ".")
    stashes = len([line for line in git(root, "stash", "list").splitlines() if line])
    return {"branch": current_branch(root), "commit": commit, "fetched": fetched,
            "remote_refs_containing_head": containing, "unsaved_paths": left, "stashes": stashes,
            "failures": failures, "local_only": local_only,
            "state": {"remotes": remotes, "remote_config": config, "commit": commit, "unsaved": left}}


def changed_since(root, state, keep=(), scope=()):
    """Failures for anything a verdict rested on that is different now."""
    now = repo_state(root, keep, scope)
    found = []
    if now["remotes"] != state["remotes"] or now["remote_config"] != state["remote_config"]:
        found.append("The list of remotes or their settings (URLs, fetch refspecs) changed during the "
                     "check, so its result is not reliable; run the check again.")
    if now["commit"] != state["commit"]:
        found.append("HEAD moved during the check, so its result is not reliable; run the check again.")
    if now["unsaved"] != state["unsaved"]:
        found.append("The working tree changed during the check, so its result is not reliable; "
                     "run the check again.")
    return found


def verdict_of(failures, local_only):
    return "refused" if failures else "local_only" if local_only else "ok"


def boundary(root, preserve=()):
    """Prove the end of a sitting: is HEAD on a remote, checked by a fetch just now?

    Refuses when the fetch fails (cached remote refs are not verification), when
    no branch on a configured remote contains HEAD, or when the tree carries
    changes other than the exact preserved paths. Stashes are counted as
    information, never a refusal. Nothing is pushed, staged or moved.
    A repo with no remote configured at all cannot be pushed, so its committed,
    clean save is the confirmed end of the sitting on this computer: that repo's
    verdict is `local_only`, and only the clean-tree check applies to it. A repo
    that has a remote keeps every check: a failed fetch or an unpushed HEAD still
    refuses.
    When the project keeps work notes in the vault, the notes repo gets the same
    checks, local-only rule included, and its failures join the list, each
    prefixed with the notes repo. Its unsaved-changes check covers the notes root
    only; fetch and remote containment stay repo-wide. Whether notes are kept is
    read from kivna/vault.json, which must be confirmed absent or readable: a
    directory, unreadable file or malformed JSON refuses.

    After every repo is checked, kivna/vault.json and each repo's remote list,
    HEAD and unsaved paths are read again; any change refuses that repo.

    Each repo's verdict is `refused` (any failure), `local_only` or `ok`. The
    combined status is `boundary_ok` only when every repo is `ok`;
    `boundary_local_only` (exit 0) when none is refused and at least one is
    `local_only`; otherwise `boundary_refused`.
    """
    keep = acknowledged(root, preserve)
    raw = config_bytes(root)
    location = notes_location(root, raw) if raw is not None else None
    checked = repo_checks(root, keep, allow_local_only=True)
    notes = None
    if location:
        notes_root, notes_repo = location
        notes = {"root": str(notes_root), "repo": str(notes_repo),
                 **repo_checks(notes_repo, scope=notes_scope(location), allow_local_only=True)}
    # Every check is done; nothing a verdict rests on may have moved meanwhile
    # (the notes fetch alone can take a minute).
    checked["failures"] += changed_since(root, checked.pop("state"), keep)
    if config_bytes(root) != raw:
        checked["failures"].append("kivna/vault.json changed during the check, so which repos it covers "
                                   "is not reliable; run the check again.")
    if notes:
        notes["failures"] += changed_since(notes_repo, notes.pop("state"), scope=notes_scope(location))
    failures = checked.pop("failures")
    local_only = checked.pop("local_only")
    verdicts = {"project": verdict_of(failures, local_only)}
    if notes:
        notes["verdict"] = verdicts["notes"] = verdict_of(notes["failures"], notes["local_only"])
        failures = failures + [f"Notes repo {notes_repo}: {item}" for item in notes["failures"]]
    found = set(verdicts.values())
    status = ("boundary_refused" if "refused" in found or failures else
              "boundary_local_only" if "local_only" in found else "boundary_ok")
    note = "Stashes are information, not a refusal; preserved paths are local only"
    unremoted = [{"project": "the project", "notes": "the notes repo"}[name]
                 for name, verdict in verdicts.items() if verdict == "local_only"]
    if unremoted:
        note += ("; no Git remote is configured for " + " or ".join(unremoted)
                 + ", so that save is on this computer only")
    result = {"status": status, "branch": checked["branch"],
              "commit": checked["commit"], "fetched": checked["fetched"],
              "remote_refs_containing_head": checked["remote_refs_containing_head"],
              "unsaved_paths": checked["unsaved_paths"], "stashes": checked["stashes"],
              "preserved_local_only": keep, "failures": failures, "local_only": local_only,
              "verdicts": verdicts, "note": note,
              "notes": notes, "notes_commit": notes["commit"] if notes else None}
    return result


def source_text(path):
    # Repo memory is UTF-8; keep source line endings rather than normalizing them.
    with path.open(encoding="utf-8", newline="") as stream:
        return stream.read()


def overtaken_revisions(root, content, head):
    """Full commit IDs the record names that are already in this checkout's history.

    A diagnostic hint, nothing more. Naming an ancestor is ordinary and usually
    correct: a record cites historical revisions and states the position observed
    before its own save. So this is not a staleness test and never a refusal —
    what makes a handoff wrong is an obsolete next action, which no hash can
    show. Unknown IDs, such as another project's HEAD, stay unreported.
    """
    found = []
    for value in dict.fromkeys(re.findall(r"(?<![0-9a-zA-Z])[0-9a-f]{40}(?![0-9a-zA-Z])", content)):
        if value == head:
            continue
        probe = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", value, head],
                               text=True, capture_output=True)
        if probe.returncode == 0:
            found.append(value)
    return found


def pickup(root, branch, record, sync=False, expected_commit=None, preserve=(), notes_commit=None,
           notes_needed=False, scope=(), record_cap=RECORD_CAP_BYTES):
    record_size(0, record_cap)
    branch = branch or default_branch(root)
    full_commit(expected_commit, "saved revision")
    full_commit(notes_commit, "saved notes commit")
    require_branch(root, branch)
    keep = acknowledged(root, preserve)
    folders = scoped(root, scope)
    outside_scope(root, [record], scope)
    notes_wanted = record.startswith(NOTES_PREFIX) or notes_needed or notes_commit is not None
    if folders and notes_wanted:
        config_saved(root)
    if unsaved(root, keep, folders):
        raise HandoffError("Local changes exist"
                           + (" inside the scope" if folders else "")
                           + "; no pull, stash, reset or merge performed")
    if sync:
        git(root, "fetch", "origin", f"refs/heads/{branch}")
        local = git(root, "rev-parse", "HEAD")
        remote = git(root, "rev-parse", "FETCH_HEAD")
        if expected_commit is not None and remote != expected_commit:
            raise HandoffError("Remote branch differs from the saved handoff revision; checkout not updated")
        collisions = [path for path in keep
                      if git(root, "ls-tree", "--name-only", "-z", remote, "--", path).strip("\0")]
        if collisions:
            raise HandoffError("The incoming revision carries preserved local files: "
                               + ", ".join(sorted(collisions))
                               + ". Nothing was merged, moved or overwritten; decide these paths first")
        ancestor = git(root, "merge-base", local, remote)
        if ancestor != local:
            raise HandoffError("Local history is ahead or diverged; resolve ownership before pickup")
        git(root, "merge", "--ff-only", "--no-overwrite-ignore", remote)
    commit = git(root, "rev-parse", "HEAD")
    if expected_commit is not None and commit != expected_commit:
        raise HandoffError("Local revision differs from the saved handoff; no record loaded")
    location = None
    if record.startswith(NOTES_PREFIX) or notes_needed or notes_commit is not None:
        location = notes_location(root)
        if location is None:
            raise HandoffError("A notes: source needs a notes root; set \"work_notes\": \"vault\" "
                               "in kivna/vault.json")
    notes_head = ready_notes(location, sync, notes_commit) if location else None
    named, base, relative, location = resolve_source(root, record, location)
    if record.startswith(NOTES_PREFIX):  # a sketchbook in the notes root must be saved there
        require_tracked(base, relative, f"the notes repo {location[1]}")
    path = base / relative
    if not path.is_file():
        raise HandoffError("Saved handoff record is missing")
    content = source_text(path)
    if not content.strip():
        raise HandoffError("Saved handoff record is empty; no fallback pickup performed")
    # Every pickup, with or without a saved revision: an edit that lands while the
    # record is read must not acquire the earlier clean check. A record named with
    # --preserve is invisible to the unsaved check, so its own bytes are read again
    # first; the project checks come last, after every read.
    if not path.is_file() or source_text(path) != content:
        raise HandoffError("Project changed while reading the saved handoff; no pickup returned")
    require_branch(root, branch)
    if git(root, "rev-parse", "HEAD") != commit or unsaved(root, keep, folders):
        raise HandoffError("Project changed while reading the saved handoff; no pickup returned")
    if notes_head:
        notes_unchanged(location, notes_head)
    if folders and notes_wanted:
        config_saved(root)
    result = {"status": "record_loaded", "branch": branch, "commit": commit, "notes_commit": notes_head,
              "record": record, "bytes": len(content.encode()), "content": content,
              **record_size(len(content.encode()), record_cap),
              "overtaken_revisions": overtaken_revisions(root, content, commit),
              "preserved_local_only": keep,
              "scope": [spec[len(":(literal)"):] for spec in folders],
              "note": "Record loading is not proof of complete context restoration or permission to execute"}
    if result["overtaken_revisions"]:
        result["hint"] = ("Diagnostic only: the record names revisions already in this checkout's "
                          "history. Historical citations and a pre-save position are legitimate, so "
                          "this is not a staleness finding. Check whether the record's next action is "
                          "still open; that, not the hash, is what would make it obsolete")
    return result


def named_section(content, heading):
    """Select one exact ATX heading and all its children, excluding fenced code."""
    pattern = r"^ {0,3}(#{1,6})[ \t]+\S.*$"
    target = re.fullmatch(pattern, heading)
    if not target:
        raise HandoffError("Use an exact Markdown heading, including its # prefix")
    lines = content.splitlines(keepends=True)
    headings = []
    fence = None
    for index, line in enumerate(lines):
        text = line.rstrip("\r\n")
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*", text):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", text)
        if opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = opening[1]
            continue
        match = re.fullmatch(pattern, text)
        if match:
            headings.append((index, len(match[1]), text))
    matches = [entry for entry in headings if entry[2].rstrip() == heading.rstrip()]
    if len(matches) != 1:
        raise HandoffError("Named section must occur exactly once outside fenced code")
    start, level, _ = matches[0]
    end = next((index for index, depth, _ in headings if index > start and depth <= level), len(lines))
    if not "".join(lines[start + 1:end]).strip():
        raise HandoffError("Named section is empty")
    return "".join(lines[start:end])


def reading_picks(root, record, files, sections):
    picks = [(record, None)] + [(value, None) for value in files] + [tuple(pair) for pair in sections]
    location = None
    normalized = []
    for value, heading in picks:
        value, _, _, location = resolve_source(root, value, location)
        normalized.append((value, heading.rstrip() if heading is not None else None))
    if len(set(normalized)) != len(normalized):
        raise HandoffError("Supply each source once; a repeated file or section would be counted twice")
    return normalized, location


def source_base(root, location, path):
    """Where a pick lives: (directory, relative path, what its tracked check names)."""
    if path.startswith(NOTES_PREFIX):
        return location[0], path[len(NOTES_PREFIX):], f"the notes repo {location[1]}"
    return root, path, "the project"


def tracked_source(root, location, path, heading, require=True):
    """Measurement and preparation resolve the same bytes, never a prose excerpt.

    Preparation requires the source tracked; measurement reports it instead,
    because Switch Out measures a sketchbook it has written but not yet saved.
    """
    base, relative, where = source_base(root, location, path)
    try:
        require_tracked(base, relative, where)
        tracked = True
    except HandoffError:
        if require:
            raise
        tracked = False
    source = selected_source(base, relative, heading, label=path)
    if not require:
        source["tracked"] = tracked
        if not tracked:
            if where == "the project":
                later = "and pickup reads it only as a record named with --preserve"
            else:
                later = "and so does pickup"
            source["warning"] = f"Not tracked in {where}; prepare refuses it until saved, {later}"
    return source


def selected_source(root, path, heading, label=None):
    text = source_text(root / path)
    content = text if heading is None else named_section(text, heading)
    label = label or path
    if not content.strip():
        raise HandoffError("Selected source is empty: " + label)
    return {"file": label,
            "selection": "complete file" if heading is None else heading + " (including child sections)",
            "content": content,
            "reaches_eof": text.endswith(content)}


def prepare(root, branch, record, files=(), sections=(), sync=False, expected_commit=None, preserve=(),
            notes_commit=None, scope=(), record_cap=RECORD_CAP_BYTES):
    """Assemble caller-selected raw sources; never choose or summarise memory."""
    needed = any(value.startswith(NOTES_PREFIX) for value in [*files, *(pair[0] for pair in sections)])
    outside_scope(root, [*files, *(pair[0] for pair in sections)], scope)
    branch = branch or default_branch(root)
    loaded = pickup(root, branch, record, sync, expected_commit, preserve, notes_commit, needed, scope,
                    record_cap)
    keep = loaded["preserved_local_only"]
    folders = scoped(root, scope)
    picks, location = reading_picks(root, record, files, sections)
    sources = [tracked_source(root, location, path, heading) for path, heading in picks]
    over_cap_sources = mark_over_cap(sources, picks, [len(source["content"].encode()) for source in sources],
                                     loaded["record_cap_bytes"])
    if loaded["notes_commit"]:
        notes_unchanged(location, loaded["notes_commit"])
    # A concurrent edit must not silently acquire the earlier clean/commit claim.
    require_branch(root, branch)
    if unsaved(root, keep, folders) or git(root, "rev-parse", "HEAD") != loaded["commit"]:
        raise HandoffError("Project changed while preparing pickup; no packet returned")
    if folders and location:
        config_saved(root)
    packet = {"status": "pickup_prepared", "branch": branch, "commit": loaded["commit"],
              "notes_commit": loaded["notes_commit"],
              "record_bytes": loaded["record_bytes"], "record_cap_bytes": loaded["record_cap_bytes"],
              "record_over_cap": loaded["record_over_cap"],
              "over_cap_sources": over_cap_sources,
              "clean_at_check": True, "synchronized": sync, "sources": sources,
              "preserved_local_only": keep,
              "scope": loaded["scope"],
              "overtaken_revisions": loaded["overtaken_revisions"],
              "note": "Caller-selected saved records, not fresh operational verification. "
                      "Selection completeness and restored meaning still need assessment. "
                      "No session is resumed and no execution authority is granted by this packet."}
    if "hint" in loaded:
        packet["hint"] = loaded["hint"]
    return packet


# The optional chief of staff (design: kerd/work/chief-of-staff/design.md).
# cos.py owns the config and its rules; this helper only asks it, after a
# successful prepare or pickup, and adds its answer. The config's existence is
# checked here first, with one stat: with no config file (or one that cannot be
# stat'ed) cos.py is never loaded, the answer is None and the output keeps
# 0.199.0's bytes. A missing or broken cos.py is the same silent off: nothing it
# does can change the off path, print into this output or leave bytecode beside it.
COS_SCRIPT = Path(__file__).resolve().with_name("cos.py")
COS_CONFIG = "~/.config/kerd/chief-of-staff.json"  # the same path as cos.CONFIG_PATH
QUEUE_MD = Path("docs") / "work" / "queue.md"


def chief_of_staff_config():
    """The config path when it can be stat'ed, else None (absent: cos.py is not loaded)."""
    try:
        path = os.path.expanduser(COS_CONFIG)
        os.stat(path)
    except (OSError, ValueError):
        return None
    return path


def chief_of_staff_signal(root, scope):
    """cos.signal for this project, or None (off, nothing shown) on any failure.

    No config file means None before cos.py is imported or run."""
    config = chief_of_staff_config()
    if config is None:
        return None
    writes = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            spec = importlib.util.spec_from_file_location("kerd_switch_cos", COS_SCRIPT)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            signal = module.signal(str(root), list(scope) or None, config)
        if not isinstance(signal, dict) or not isinstance(signal.get("on"), bool):
            return None
        json.dumps(signal)
        return signal
    except (Exception, SystemExit):
        return None
    finally:
        sys.dont_write_bytecode = writes


def with_chief_of_staff(result, root):
    """Add the signal key, and queue_md_present when on; unchanged when None.

    The project is the scope folder when there is exactly one scope (design
    v2.1 C); cos.py decides on/off for more than one, and only reads presence
    of docs/work/queue.md, never its contents.
    """
    scope = result.get("scope") or []
    signal = chief_of_staff_signal(root, scope)
    if signal is None:
        return result
    result["chief_of_staff"] = signal
    if signal["on"] is True:
        project = root / scope[0] if len(scope) == 1 else root
        try:
            result["queue_md_present"] = (project / QUEUE_MD).is_file()
        except OSError:
            result["queue_md_present"] = False
    return result


def private_problem(info):
    if stat.S_ISLNK(info.st_mode):
        return "it is a symbolic link"
    if not stat.S_ISREG(info.st_mode):
        return "it is not a regular file"
    if info.st_uid != os.getuid():
        return "it is not owned by the current user"
    if info.st_mode & 0o077:
        return "it is readable or writable by group or other users; use mode 0600"
    return None


def carry_phrases(value, stdin=None):
    """Phrases from an owner-only file, or stdin for "-": one per line, blank lines skipped.

    Phrases may be private notes, so they never travel in argv, where the
    process list would show them.
    """
    if value == "-":
        text = (stdin or sys.stdin).read()
    else:
        try:
            linked = os.lstat(value)
        except OSError as exc:
            raise HandoffError(f"Cannot read the carry file {value}: {exc.strerror}")
        problem = private_problem(linked)
        if problem:
            raise HandoffError(f"Refused the carry file {value}: {problem}")
        fd = os.open(value, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        opened = os.fstat(fd)
        problem = private_problem(opened)
        if problem or (opened.st_dev, opened.st_ino) != (linked.st_dev, linked.st_ino):
            os.close(fd)
            raise HandoffError(f"Refused the carry file {value}: {problem or 'it changed while being opened'}")
        with os.fdopen(fd, encoding="utf-8", newline="") as stream:
            text = stream.read()
    return [line for line in (raw.rstrip("\r\n") for raw in text.splitlines(keepends=True)) if line.strip()]


TARGET_TOKENS = 8000  # the Switch trial's pickup allowance, from the In guide


def record_size(size, cap=RECORD_CAP_BYTES):
    """Informational keys for the record's size; never a refusal."""
    if not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0:
        raise ValueError("Record cap must be a positive integer number of bytes")
    return {"record_bytes": size, "record_cap_bytes": cap, "record_over_cap": size > cap}


def measure(root, record, files=(), sections=(), target=TARGET_TOKENS, carry=(), scope=(),
            record_cap=RECORD_CAP_BYTES):
    """Size the pickup reading set as it stands in the working tree.

    Bytes are counted exactly; tokens are estimated at four bytes each, which
    is a proxy and is labelled as one. An over-target set is information for
    the person closing the sitting, not a refusal: the result never blocks.
    An untracked source is measured and reported (`tracked: false` with a
    warning), never refused; `prepare` still refuses it. Each carry phrase is
    looked up as an exact substring of the selected bytes; a miss is reported,
    never a refusal.
    """
    if not isinstance(target, int) or target <= 0:
        raise ValueError("Target must be a positive integer number of tokens")
    if any(not phrase for phrase in carry):
        raise HandoffError("A carry phrase must not be empty")
    outside_scope(root, [record, *files, *(pair[0] for pair in sections)], scope)
    picks, location = reading_picks(root, record, files, sections)
    sources, total, read_args, contents = [], 0, [], []
    for index, (path, heading) in enumerate(picks):
        source = tracked_source(root, location, path, heading, require=False)
        content = source.pop("content")
        contents.append(content)
        size = len(content.encode("utf-8"))
        total += size
        source.update(bytes=size, approx_tokens=-(-size // 4))
        sources.append(source)
        read_args += (["--record", path] if index == 0 else
                      ["--file", path] if heading is None else ["--section", path, heading])
    carried = []
    for phrase in dict.fromkeys(carry):
        found = [{"file": source["file"], "selection": source["selection"]}
                 for source, content in zip(sources, contents) if phrase in content]
        carried.append({"phrase": phrase, "found_in": found,
                        "result": "in the reading set" if found else "not in the reading set"})
    estimate = -(-total // 4)
    for folder in (spec[len(":(literal)"):] for spec in scoped(root, scope)):
        read_args += ["--scope", folder]
    sizes = record_size(sources[0]["bytes"], record_cap)
    over = mark_over_cap(sources, picks, [source["bytes"] for source in sources], record_cap)
    return {"status": "measured", **sizes, "over_cap_sources": over, "sources": sources, "read_args": read_args, "total_bytes": total,
            "approx_tokens": estimate, "target_tokens": target,
            "within_target": estimate <= target,
            "method": "bytes counted exactly per selection, including any whole-file/section or nested-section overlap; "
                      "tokens estimated at four bytes each, not a tokenizer reading",
            "carry": carried,
            "warnings": [f"{source['file']}: {source['warning']}" for source in sources if "warning" in source]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project")
    sub = parser.add_subparsers(dest="action", required=True)
    save = sub.add_parser("save")
    save.add_argument("--branch", required=True)
    save.add_argument("--file", action="append", required=True)
    save.add_argument("--message", required=True)
    save.add_argument("--push", action="store_true")
    save.add_argument("--preserve", action="append", default=[],
                      help="Exact untracked path this project keeps locally; never saved or touched")
    load = sub.add_parser("pickup")
    load.add_argument("--branch", help="Default: the checked-out branch")
    load.add_argument("--record", required=True)
    load.add_argument("--sync", action="store_true")
    load.add_argument("--commit", help="Exact saved revision for a named handoff; omit for ordinary latest-state In")
    load.add_argument("--notes-commit", help="Notes repo commit recorded at Out (boundary notes_commit); "
                                             "the notes repo must contain it")
    load.add_argument("--scope", action="append", default=[], metavar="FOLDER",
                      help="Folder inside the project that the unsaved-changes check covers (repeatable); "
                           "for records in a repo shared with other projects. Default: the whole project")
    load.add_argument("--preserve", action="append", default=[],
                      help="Exact untracked path to keep; a collision in the incoming revision stops the pickup")
    packet = sub.add_parser("prepare", help="Gather caller-selected sources for a fresh reader")
    packet.add_argument("--branch", help="Default: the checked-out branch")
    packet.add_argument("--record", required=True)
    packet.add_argument("--file", action="append", default=[])
    packet.add_argument("--section", nargs=2, action="append", default=[], metavar=("FILE", "HEADING"))
    packet.add_argument("--sync", action="store_true")
    packet.add_argument("--commit", help="Exact saved revision; checked before updating the checkout")
    packet.add_argument("--notes-commit", help="Notes repo commit recorded at Out (boundary notes_commit); "
                                               "the notes repo must contain it")
    packet.add_argument("--scope", action="append", default=[], metavar="FOLDER",
                      help="Folder inside the project that the unsaved-changes check covers (repeatable); "
                           "for records in a repo shared with other projects. Default: the whole project")
    packet.add_argument("--preserve", action="append", default=[],
                        help="Exact untracked path to keep; a collision in the incoming revision stops the pickup")
    # No abbreviation: a retired `--carry PHRASE` must not be taken as `--carry-file` and put a phrase in argv.
    size = sub.add_parser("measure", help="Size the pickup reading set in the working tree; never blocks",
                          allow_abbrev=False)
    size.add_argument("--record", required=True)
    size.add_argument("--file", action="append", default=[])
    size.add_argument("--section", nargs=2, action="append", default=[], metavar=("FILE", "HEADING"))
    size.add_argument("--scope", action="append", default=[], metavar="FOLDER",
                      help="Carried into read_args for prepare; a source outside it is refused")
    size.add_argument("--target", type=int, default=TARGET_TOKENS,
                      help="Token allowance to compare against (default: the trial's %(default)s)")
    size.add_argument("--record-cap", type=int, default=RECORD_CAP_BYTES, metavar="N",
                      help="Informational record size in bytes (default: %(default)s); never blocks")
    size.add_argument("--carry-file", action="append", default=[], metavar="PATH",
                      help="Owner-only (0600) file of exact phrases the pickup must carry, one per line, "
                           "or - for stdin; reports which source holds each, never blocks")
    check = sub.add_parser("boundary", help="Fetch, then refuse unless a remote ref contains HEAD and the tree is "
                                            "clean; with no remote configured, a clean tree is a local-only save")
    check.add_argument("--preserve", action="append", default=[],
                       help="Exact untracked path this project keeps locally; not counted as unsaved")
    for each in (save, load, packet, size, check):
        each.add_argument("--project", dest="project_after", help=argparse.SUPPRESS)
    for each in (load, packet):
        each.add_argument("--record-cap", type=int, default=RECORD_CAP_BYTES, metavar="N",
                          help="Informational record size in bytes (default: %(default)s); never blocks")
    args = parser.parse_args()
    try:
        if args.project and args.project_after and args.project != args.project_after:
            raise HandoffError("--project given twice with different values; name one project")
        args.project = args.project or args.project_after
        if not args.project:
            parser.error("--project is required")
        root = root_for(args.project)
        if args.action == "boundary":
            result = boundary(root, args.preserve)
            print(json.dumps(result, indent=2))
            return 1 if result["failures"] else 0
        if args.action == "measure":
            carry = [phrase for value in args.carry_file for phrase in carry_phrases(value)]
            result = measure(root, args.record, args.file, args.section, args.target, carry, args.scope, args.record_cap)
        elif args.action == "save":
            result = publish(root, args.branch, args.file, args.message, args.push, preserve=args.preserve)
        elif args.action == "prepare":
            result = with_chief_of_staff(
                prepare(root, args.branch, args.record, args.file, args.section, args.sync,
                        args.commit, args.preserve, args.notes_commit, scope=args.scope, record_cap=args.record_cap), root)
        else:
            result = with_chief_of_staff(
                pickup(root, args.branch, args.record, args.sync, args.commit, args.preserve,
                       args.notes_commit, scope=args.scope, record_cap=args.record_cap), root)
        print(json.dumps(result, indent=2))
        return 0
    except (HandoffError, OSError, ValueError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
