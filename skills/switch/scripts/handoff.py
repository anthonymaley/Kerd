#!/usr/bin/env python3
"""Small Git handoff primitives. Memory judgment and session control stay with Switch."""

import argparse
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


def notes_location(root):
    """(notes root, notes repo) when the project keeps work notes in the vault, else None.

    `"work_notes": "vault"` in kivna/vault.json puts the notes root at
    <vault>/<folder>/work. Absent file or key: no notes root. A set key whose
    root is missing or outside a Git repo is an error naming the path, never a
    silent fall back to the project. The folder is a plain relative name, no
    part of <folder>/work may be a symlink, the resolved root must stay under
    the resolved vault, and the notes repo cannot be the project's own repo.
    """
    config = root / "kivna" / "vault.json"
    if not config.is_file():
        return None
    try:
        settings = json.loads(config.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise HandoffError(f"Cannot read {config}: {exc}")
    if not isinstance(settings, dict) or "work_notes" not in settings:
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
    """The committed tree of the notes root at a revision; None when nothing is committed there."""
    relative = location[0].relative_to(location[1]).as_posix()
    spec = f"{revision}^{{tree}}" if relative == "." else f"{revision}:{relative}"
    found = subprocess.run(["git", "-C", str(location[1]), "rev-parse", "--verify", "--quiet", spec],
                           text=True, capture_output=True)
    return found.stdout.strip() or None


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
        git(repo, "merge", "--ff-only", remote)
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


def repo_checks(root, keep=(), scope=()):
    """The boundary checks for one repo: fetch, HEAD on a remote ref, nothing unsaved.

    Fetch and remote containment are repo-wide; `scope` (pathspecs) narrows only
    the unsaved-changes check, so a shared vault's other folders cannot refuse.
    """
    failures = []
    try:
        fetch = subprocess.run(["git", "-C", str(root), "fetch", "--quiet", "--all", "--prune"], text=True,
                               capture_output=True, timeout=FETCH_TIMEOUT,
                               env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        fetched = fetch.returncode == 0 and bool(git(root, "remote"))
    except subprocess.TimeoutExpired:
        fetched = False
    if not fetched:
        failures.append("The fetch failed, so the remote state is unknown; cached refs are not verification.")
    commit = git(root, "rev-parse", "HEAD")
    containing = [ref for ref in git(root, "for-each-ref", "--contains", "HEAD", "--format=%(refname:short)",
                                     "refs/remotes").splitlines()
                  if ref and not ref.endswith("/HEAD")]
    if not containing:
        failures.append("No remote branch contains this commit; the work exists only on this machine.")
    spec = ["--", *scope] if scope else []
    left = sorted((local_changes(root, *scope)
                   | set(filter(None, git(root, "diff", "--cached", "--name-only", "-z", *spec).split("\0"))))
                  - set(keep))
    if left:
        failures.append(f"The working tree is not clean: {len(left)} unsaved "
                        + ("path" if len(left) == 1 else "paths") + ".")
    stashes = len([line for line in git(root, "stash", "list").splitlines() if line])
    branch = subprocess.run(["git", "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"],
                            text=True, capture_output=True).stdout.strip() or None
    return {"branch": branch, "commit": commit, "fetched": fetched, "remote_refs_containing_head": containing,
            "unsaved_paths": left, "stashes": stashes, "failures": failures}


def boundary(root, preserve=()):
    """Prove the end of a sitting: is HEAD on a remote, checked by a fetch just now?

    Refuses when the fetch fails (cached remote refs are not verification), when
    no remote ref contains HEAD (the work exists only on this machine), or when
    the tree carries changes other than the exact preserved paths. Stashes are
    counted as information, never a refusal. Nothing is pushed, staged or moved.
    When the project keeps work notes in the vault, the notes repo gets the same
    checks and its failures join the list, each prefixed with the notes repo.
    Its unsaved-changes check covers the notes root only; fetch and remote
    containment stay repo-wide.
    """
    keep = acknowledged(root, preserve)
    location = notes_location(root)
    checked = repo_checks(root, keep)
    failures = checked.pop("failures")
    notes = None
    if location:
        notes_root, notes_repo = location
        notes = {"root": str(notes_root), "repo": str(notes_repo),
                 **repo_checks(notes_repo, scope=notes_scope(location))}
        failures += [f"Notes repo {notes_repo}: {item}" for item in notes["failures"]]
    result = {"status": "boundary_refused" if failures else "boundary_ok", "branch": checked["branch"],
              "commit": checked["commit"], "fetched": checked["fetched"],
              "remote_refs_containing_head": checked["remote_refs_containing_head"],
              "unsaved_paths": checked["unsaved_paths"], "stashes": checked["stashes"],
              "preserved_local_only": keep, "failures": failures,
              "note": "Stashes are information, not a refusal; preserved paths are local only",
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
           notes_needed=False):
    full_commit(expected_commit, "saved revision")
    full_commit(notes_commit, "saved notes commit")
    require_branch(root, branch)
    keep = acknowledged(root, preserve)
    if git(root, "diff", "--cached", "--name-only") or (local_changes(root) - set(keep)):
        raise HandoffError("Local changes exist; no pull, stash, reset or merge performed")
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
        git(root, "merge", "--ff-only", remote)
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
    if expected_commit is not None:
        require_branch(root, branch)
        if (git(root, "rev-parse", "HEAD") != commit or git(root, "diff", "--cached", "--name-only")
                or (local_changes(root) - set(keep))):
            raise HandoffError("Project changed while reading the saved handoff; no pickup returned")
    if notes_head:
        notes_unchanged(location, notes_head)
    result = {"status": "record_loaded", "branch": branch, "commit": commit, "notes_commit": notes_head,
              "record": record, "bytes": len(content.encode()), "content": content,
              "overtaken_revisions": overtaken_revisions(root, content, commit),
              "preserved_local_only": keep,
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
            notes_commit=None):
    """Assemble caller-selected raw sources; never choose or summarise memory."""
    needed = any(value.startswith(NOTES_PREFIX) for value in [*files, *(pair[0] for pair in sections)])
    loaded = pickup(root, branch, record, sync, expected_commit, preserve, notes_commit, needed)
    keep = loaded["preserved_local_only"]
    picks, location = reading_picks(root, record, files, sections)
    sources = [tracked_source(root, location, path, heading) for path, heading in picks]
    if loaded["notes_commit"]:
        notes_unchanged(location, loaded["notes_commit"])
    # A concurrent edit must not silently acquire the earlier clean/commit claim.
    require_branch(root, branch)
    if (git(root, "diff", "--cached", "--name-only") or (local_changes(root) - set(keep))
            or git(root, "rev-parse", "HEAD") != loaded["commit"]):
        raise HandoffError("Project changed while preparing pickup; no packet returned")
    packet = {"status": "pickup_prepared", "branch": branch, "commit": loaded["commit"],
              "notes_commit": loaded["notes_commit"],
              "clean_at_check": True, "synchronized": sync, "sources": sources,
              "preserved_local_only": keep,
              "overtaken_revisions": loaded["overtaken_revisions"],
              "note": "Caller-selected saved records, not fresh operational verification. "
                      "Selection completeness and restored meaning still need assessment. "
                      "No session is resumed and no execution authority is granted by this packet."}
    if "hint" in loaded:
        packet["hint"] = loaded["hint"]
    return packet


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


def measure(root, record, files=(), sections=(), target=TARGET_TOKENS, carry=()):
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
    return {"status": "measured", "sources": sources, "read_args": read_args, "total_bytes": total,
            "approx_tokens": estimate, "target_tokens": target,
            "within_target": estimate <= target,
            "method": "bytes counted exactly per selection, including any whole-file/section or nested-section overlap; "
                      "tokens estimated at four bytes each, not a tokenizer reading",
            "carry": carried,
            "warnings": [f"{source['file']}: {source['warning']}" for source in sources if "warning" in source]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    sub = parser.add_subparsers(dest="action", required=True)
    save = sub.add_parser("save")
    save.add_argument("--branch", required=True)
    save.add_argument("--file", action="append", required=True)
    save.add_argument("--message", required=True)
    save.add_argument("--push", action="store_true")
    save.add_argument("--preserve", action="append", default=[],
                      help="Exact untracked path this project keeps locally; never saved or touched")
    load = sub.add_parser("pickup")
    load.add_argument("--branch", required=True)
    load.add_argument("--record", required=True)
    load.add_argument("--sync", action="store_true")
    load.add_argument("--commit", help="Exact saved revision for a named handoff; omit for ordinary latest-state In")
    load.add_argument("--notes-commit", help="Notes repo commit recorded at Out (boundary notes_commit); "
                                             "the notes repo must contain it")
    load.add_argument("--preserve", action="append", default=[],
                      help="Exact untracked path to keep; a collision in the incoming revision stops the pickup")
    packet = sub.add_parser("prepare", help="Gather caller-selected sources for a fresh reader")
    packet.add_argument("--branch", required=True)
    packet.add_argument("--record", required=True)
    packet.add_argument("--file", action="append", default=[])
    packet.add_argument("--section", nargs=2, action="append", default=[], metavar=("FILE", "HEADING"))
    packet.add_argument("--sync", action="store_true")
    packet.add_argument("--commit", help="Exact saved revision; checked before updating the checkout")
    packet.add_argument("--notes-commit", help="Notes repo commit recorded at Out (boundary notes_commit); "
                                               "the notes repo must contain it")
    packet.add_argument("--preserve", action="append", default=[],
                        help="Exact untracked path to keep; a collision in the incoming revision stops the pickup")
    # No abbreviation: a retired `--carry PHRASE` must not be taken as `--carry-file` and put a phrase in argv.
    size = sub.add_parser("measure", help="Size the pickup reading set in the working tree; never blocks",
                          allow_abbrev=False)
    size.add_argument("--record", required=True)
    size.add_argument("--file", action="append", default=[])
    size.add_argument("--section", nargs=2, action="append", default=[], metavar=("FILE", "HEADING"))
    size.add_argument("--target", type=int, default=TARGET_TOKENS,
                      help="Token allowance to compare against (default: the trial's %(default)s)")
    size.add_argument("--carry-file", action="append", default=[], metavar="PATH",
                      help="Owner-only (0600) file of exact phrases the pickup must carry, one per line, "
                           "or - for stdin; reports which source holds each, never blocks")
    check = sub.add_parser("boundary", help="Fetch, then refuse unless a remote ref contains HEAD and the tree is clean")
    check.add_argument("--preserve", action="append", default=[],
                       help="Exact untracked path this project keeps locally; not counted as unsaved")
    args = parser.parse_args()
    try:
        root = root_for(args.project)
        if args.action == "boundary":
            result = boundary(root, args.preserve)
            print(json.dumps(result, indent=2))
            return 1 if result["failures"] else 0
        if args.action == "measure":
            carry = [phrase for value in args.carry_file for phrase in carry_phrases(value)]
            result = measure(root, args.record, args.file, args.section, args.target, carry)
        elif args.action == "save":
            result = publish(root, args.branch, args.file, args.message, args.push, preserve=args.preserve)
        elif args.action == "prepare":
            result = prepare(root, args.branch, args.record, args.file, args.section, args.sync,
                             args.commit, args.preserve, args.notes_commit)
        else:
            result = pickup(root, args.branch, args.record, args.sync, args.commit, args.preserve,
                            args.notes_commit)
        print(json.dumps(result, indent=2))
        return 0
    except (HandoffError, OSError, ValueError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
