#!/usr/bin/env python3
"""Content baseline and change read for a returned edit. Hashes only; never file contents.

baseline records owned paths before dispatch; compare reports what changed since;
discard deletes the baseline once the return is accepted. Baselines are private,
named files inside the Git directory, never in the work tree.
Each tracked owned path keeps two patch hashes: the index against the baseline commit
and the work tree against the index, so staging moves are reported. Owned paths
touched by any commit since the baseline, or by the endpoint diff, are listed in
`committed`; the summary always states whether HEAD moved. Every
non-directory entry under the owned paths, including untracked and ignored ones, is
compared by type, target, size and hash. Entries under a --generated glob are
summarized per top-level directory instead. Outside the owned paths, Git status or
content changes and paths changed by commits since the baseline are reported in
`outside`.
Summary counts: text files to read are added or modified non-binary files that Git
does not track (tracked text is read through its patch); binary/symlink to check are
added, modified or deleted binaries, symlinks and other non-regular entries.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import stat
import subprocess
import sys
import tempfile


SCHEMA = 1
BINARY_PROBE = 8000
EMPTY_PATCH = hashlib.sha256(b"").hexdigest()
FIELDS = {"schema", "root", "head", "paths", "generated", "tracked", "entries",
          "generated_summary", "outside_status"}
ENTRY_FIELDS = {"file": {"kind", "size", "sha256", "binary", "git"},
                "symlink": {"kind", "size", "target", "binary", "git"},
                "other": {"kind", "size", "binary", "git"}}
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
HEX64 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?")
UNMERGED = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


class Refused(Exception):
    pass


def git(root, *args, stdin=None, ok=(0,)):
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    # Owned paths are names, not patterns; check-ignore reads names and refuses the flag.
    literal = [] if args[0] == "check-ignore" else ["--literal-pathspecs"]
    proc = subprocess.run(["git", *literal, "-C", str(root), *args],
                          input=stdin, capture_output=True, env=env)
    if proc.returncode not in ok:
        raise Refused("git " + " ".join(args[:2]) + " failed: "
                      + proc.stderr.decode("utf-8", errors="replace").strip())
    return proc


def split_z(output):
    return [os.fsdecode(item) for item in output.split(b"\0") if item]


def project_root(project):
    proc = subprocess.run(["git", "-C", str(project), "rev-parse", "--show-toplevel"],
                          capture_output=True)
    if proc.returncode != 0 or not Path(project).is_dir():
        raise Refused(f"Not a Git work tree: {project}")
    return Path(os.fsdecode(proc.stdout.strip())).resolve()


def owned(root, value):
    """Return a root-relative POSIX path, refusing anything that could leave ROOT."""
    if not value or "\0" in value:
        raise Refused("Owned paths must be non-empty")
    if ".." in Path(value).parts:
        raise Refused(f"Owned path may not contain '..': {value}")
    candidate = Path(value)
    if candidate.is_absolute():
        parent = Path(os.path.realpath(candidate.parent))
        candidate = parent / candidate.name if candidate.name else parent
        try:
            candidate = candidate.relative_to(root)
        except ValueError:
            raise Refused(f"Owned path is outside the project: {value}") from None
    relative = Path(os.path.normpath(str(candidate)))
    if ".git" in relative.parts:
        raise Refused(f"Owned path may not enter .git: {value}")
    parent = root / relative.parent
    if os.path.realpath(parent) != str(parent):
        raise Refused(f"Owned path passes through a symbolic link: {value}")
    return relative.as_posix()


def glob_regex(glob):
    """Match a root-relative path: ** spans directories, * and ? stay within one."""
    parts, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            parts.append("(?:.*/)?")
            i += 3
        elif glob.startswith("**", i):
            parts.append(".*")
            i += 2
        elif glob[i] == "*":
            parts.append("[^/]*")
            i += 1
        elif glob[i] == "?":
            parts.append("[^/]")
            i += 1
        elif glob[i] == "[" and "]" in glob[i + 2:]:
            end = glob.index("]", i + 2)
            body = glob[i + 1:end].replace("\\", "\\\\")
            parts.append("[" + ("^" + body[1:] if body.startswith("!") else body) + "]")
            i = end + 1
        else:
            parts.append(re.escape(glob[i]))
            i += 1
    return re.compile("".join(parts) + r"\Z", re.S)


def generated_globs(values):
    globs = []
    for value in values:
        parts = value.rstrip("/").split("/")
        if not value.strip("/") or value.startswith("/") or any(p in ("", ".", "..", ".git") for p in parts):
            raise Refused(f"Generated globs must be normalized project-relative paths: {value}")
        globs.append(value + "**" if value.endswith("/") else value)
    return globs


def generated_key(glob, path):
    """The glob's literal leading directories; the entry's first directory otherwise."""
    prefix = []
    for part in glob.split("/")[:-1]:
        if any(ch in part for ch in "*?["):
            break
        prefix.append(part)
    return "/".join(prefix) if prefix else path.split("/")[0]


def under(path, owned_path):
    return owned_path == "." or path == owned_path or path.startswith(owned_path + "/")


def describe(full):
    info = os.lstat(full)
    if os.path.islink(full):
        return {"kind": "symlink", "size": info.st_size, "target": os.readlink(full), "binary": False}
    if not os.path.isfile(full):
        return {"kind": "other", "size": info.st_size, "binary": False}
    digest = hashlib.sha256()
    fd = os.open(full, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as stream:
        first = stream.read(BINARY_PROBE)
        digest.update(first)
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return {"kind": "file", "size": info.st_size, "sha256": digest.hexdigest(), "binary": b"\0" in first}


def walk(root, relative, found):
    """Collect non-directory entries without following symbolic links or entering .git."""
    full = root / relative
    if not os.path.lexists(full):
        return
    if os.path.isdir(full) and not os.path.islink(full):
        with os.scandir(full) as items:
            for item in items:
                if item.name != ".git":
                    walk(root, item.name if relative == "." else relative + "/" + item.name, found)
    else:
        found[relative] = describe(full)


def entry_hash(entry):
    if entry["kind"] == "file":
        return entry["sha256"]
    marker = entry["kind"] + "\0" + entry.get("target", "") + "\0" + str(entry["size"])
    return hashlib.sha256(os.fsencode(marker)).hexdigest()


def status_records(root):
    records = split_z(git(root, "status", "--porcelain=v1", "-z", "--no-renames",
                          "--untracked-files=all").stdout)
    return [[record[:2], record[3:].rstrip("/")] for record in records]


def patch_hash(root, *diff):
    patch = git(root, "diff", "--binary", "--no-color", "--no-ext-diff", "--no-textconv",
                "--no-renames", *diff).stdout
    return hashlib.sha256(patch).hexdigest()


def outside_hash(root, base, path, code):
    """Untracked: the file's hash. Otherwise: the patch hash against base. Deleted or unreadable: None."""
    full = root / path
    if not os.path.lexists(full):
        return None
    try:
        if code == "??":
            if os.path.isdir(full) and not os.path.islink(full):
                return None
            return entry_hash(describe(full))
        return patch_hash(root, base, "--", path)
    except (OSError, Refused):
        return None


def diff_base(root, head):
    if head:
        return head
    return os.fsdecode(git(root, "hash-object", "-t", "tree", "/dev/null").stdout.strip())


def current_head(root):
    proc = git(root, "rev-parse", "--verify", "-q", "HEAD", ok=(0, 1))
    return os.fsdecode(proc.stdout.strip()) or None


def snapshot(root, paths, generated, head):
    """head is the commit patches are taken against; None means the empty tree."""
    base = diff_base(root, head)
    index = set(split_z(git(root, "ls-files", "-z", "--", *paths).stdout))
    listed = index | (set(split_z(git(root, "ls-tree", "-r", "-z", "--name-only", head, "--", *paths).stdout))
                      if head else set())
    tracked = {path: {"staged": EMPTY_PATCH, "unstaged": EMPTY_PATCH} for path in listed}
    for path in split_z(git(root, "diff", "--cached", "--name-only", "-z", "--no-renames", base, "--", *paths).stdout):
        tracked.setdefault(path, {"staged": EMPTY_PATCH, "unstaged": EMPTY_PATCH})
        tracked[path]["staged"] = patch_hash(root, "--cached", base, "--", path)
    for path in split_z(git(root, "diff", "--name-only", "-z", "--no-renames", "--", *paths).stdout):
        tracked.setdefault(path, {"staged": EMPTY_PATCH, "unstaged": EMPTY_PATCH})
        tracked[path]["unstaged"] = patch_hash(root, "--", path)

    found = {}
    for path in paths:
        walk(root, path, found)
    untracked = [path for path in found if path not in index]
    ignored = set(split_z(git(root, "check-ignore", "-z", "--stdin",
                              stdin=b"".join(os.fsencode(p) + b"\0" for p in untracked),
                              ok=(0, 1)).stdout)) if untracked else set()
    patterns = [(glob, glob_regex(glob)) for glob in generated]
    entries, groups = {}, {}
    for path in sorted(found):
        entry = found[path]
        glob = next((g for g, pattern in patterns if pattern.match(path)), None)
        if glob:
            groups.setdefault(generated_key(glob, path), []).append((path, entry_hash(entry)))
            continue
        entry["git"] = "tracked" if path in index else "ignored" if path in ignored else "untracked"
        entries[path] = entry
    summary = {}
    for key, pairs in groups.items():
        digest = hashlib.sha256()
        for path, value in sorted(pairs):
            digest.update(os.fsencode(path) + b"\0" + value.encode() + b"\n")
        summary[key] = {"count": len(pairs), "sha256": digest.hexdigest()}
    outside = [[code, path, outside_hash(root, base, path, code)] for code, path in status_records(root)
               if not any(under(path, p) for p in paths)]
    return {"schema": SCHEMA, "root": str(root), "head": head, "paths": paths, "generated": generated,
            "tracked": tracked, "entries": entries, "generated_summary": summary,
            "outside_status": outside}


def baseline_file(root, name, create=False):
    """NAME.json in the Git directory's private store; refused if it would sit in the work tree."""
    if not isinstance(name, str) or not NAME.fullmatch(name):
        raise Refused("Baseline names are 1-64 letters, digits, '.', '_' or '-', starting with a letter or digit")
    relative = os.fsdecode(git(root, "rev-parse", "--git-path", "kerd-conductor/baselines").stdout.strip())
    git_dir = Path(os.path.realpath(os.fsdecode(git(root, "rev-parse", "--absolute-git-dir").stdout.strip())))

    def checked():
        store = Path(os.path.realpath(root / relative))
        in_git_dir = git_dir in store.parents
        in_tree = root in store.parents
        dot_git = root / ".git"
        if not in_git_dir or (in_tree and not (store.relative_to(root).parts[0] == ".git"
                                               and dot_git.is_dir() and not dot_git.is_symlink())):
            raise Refused("Baseline storage would sit inside the work tree or outside the Git directory; refused")
        return store

    store = checked()
    if create:
        try:
            for folder in (store.parent, store):
                folder.mkdir(mode=0o700, exist_ok=True)
                os.chmod(folder, 0o700)
        except OSError as exc:
            raise Refused(f"Could not prepare baseline storage: {exc.strerror}") from None
        store = checked()
    return store / (name + ".json")


def write_baseline(path, name, value, replace):
    """Atomic 0600 write; without replace, an existing NAME is never overwritten."""
    try:
        fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".writing-")
    except OSError as exc:
        raise Refused(f"Could not write baseline {name}: {exc.strerror}") from None
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        if replace:
            os.replace(temp, path)
        else:
            os.link(temp, path)
    except FileExistsError:
        raise Refused(f"A baseline named {name} already exists; pass --replace to overwrite it") from None
    except OSError as exc:
        raise Refused(f"Could not write baseline {name}: {exc.strerror}") from None
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def baseline(project, paths, generated, name, replace=False):
    root = project_root(project)
    paths = list(dict.fromkeys(owned(root, p) for p in paths))
    generated = generated_globs(generated)
    path = baseline_file(root, name, create=True)
    if path.exists() and not replace:
        raise Refused(f"A baseline named {name} already exists; pass --replace to overwrite it")
    record = snapshot(root, paths, generated, current_head(root))
    write_baseline(path, name, record, replace)
    return record


def identity_problem(st):
    if stat.S_ISLNK(st.st_mode):
        return "it is a symbolic link"
    if not stat.S_ISREG(st.st_mode):
        return "it is not a regular file"
    if st.st_uid != os.getuid():
        return "it is not owned by the current user"
    if st.st_mode & 0o077:
        return "it is accessible to group or other users"
    return None


def open_baseline(path, name):
    """lstat the stored file, open it without following links, and confirm the same private file."""
    def refuse(reason):
        raise Refused(f"Refused baseline {name}: {reason}")

    try:
        linked = os.lstat(path)
    except FileNotFoundError:
        raise Refused(f"No baseline named {name}") from None
    except OSError as exc:
        raise Refused(f"Could not inspect baseline {name}: {exc.strerror}") from None
    problem = identity_problem(linked)
    if problem:
        refuse(problem)
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    except FileNotFoundError:
        raise Refused(f"No baseline named {name}") from None
    except OSError as exc:
        raise Refused(f"Could not open baseline {name}: {exc.strerror}") from None
    opened = os.fstat(fd)
    problem = identity_problem(opened)
    if problem or (opened.st_dev, opened.st_ino) != (linked.st_dev, linked.st_ino):
        os.close(fd)
        refuse(problem or "it changed while being opened")
    return fd


def discard(project, name):
    root = project_root(project)
    path = baseline_file(root, name)
    os.close(open_baseline(path, name))
    try:
        os.unlink(path)
    except FileNotFoundError:
        raise Refused(f"No baseline named {name}") from None
    except OSError as exc:
        raise Refused(f"Could not discard baseline {name}: {exc.strerror}") from None
    return {"discarded": name}


def clean_path(value, allow_root=False):
    if not isinstance(value, str) or not value or "\0" in value or value.startswith("/"):
        return False
    if value == ".":
        return allow_root
    parts = value.split("/")
    return posixpath.normpath(value) == value and ".." not in parts and ".git" not in parts


def is_digest(value, nullable=False):
    return (nullable and value is None) or (isinstance(value, str) and HEX64.fullmatch(value) is not None)


def is_status(code):
    """Git porcelain v1 pairs: untracked, unmerged, or X and Y from ' MTADRC' but not both blank."""
    if not isinstance(code, str) or len(code) != 2:
        return False
    if code == "??" or code in UNMERGED:
        return True
    return code != "  " and all(ch in " MTADRC" for ch in code)


def is_count(value):
    return type(value) is int and value >= 0


def validate(root, name, record):
    def invalid(reason):
        raise Refused(f"Invalid baseline {name}: {reason}")

    if not isinstance(record, dict):
        invalid("not a JSON object")
    if type(record.get("schema")) is not int or record["schema"] != SCHEMA:
        invalid(f"schema must be {SCHEMA}")
    if set(record) != FIELDS:
        invalid("fields are missing or unexpected")
    if record["root"] != str(root):
        invalid("it belongs to another project")
    if not (record["head"] is None or (isinstance(record["head"], str) and COMMIT.fullmatch(record["head"]))):
        invalid("head must be a commit ID or null")
    paths = record["paths"]
    if not isinstance(paths, list) or not paths or not all(clean_path(p, allow_root=True) for p in paths):
        invalid("owned paths must be normalized project-relative paths")
    for path in paths:
        if owned(root, path) != path:
            invalid(f"owned path {path!r} is not normalized")

    def inside(path):
        return any(under(path, p) for p in paths)

    generated = record["generated"]
    if not isinstance(generated, list) or not all(isinstance(g, str) for g in generated):
        invalid("generated globs must be strings")
    try:
        normalized = generated_globs(generated)
    except Refused:
        normalized = None
    if normalized != generated:
        invalid("generated globs must be normalized project-relative globs")
    tracked = record["tracked"]
    if not isinstance(tracked, dict):
        invalid("tracked must be an object")
    for path, patches in tracked.items():
        if not clean_path(path) or not inside(path):
            invalid(f"tracked path {path!r} is not a normalized path under an owned path")
        if not isinstance(patches, dict) or set(patches) != {"staged", "unstaged"} \
                or not all(is_digest(v) for v in patches.values()):
            invalid(f"tracked path {path!r} needs staged and unstaged SHA-256 digests")
    entries = record["entries"]
    if not isinstance(entries, dict):
        invalid("entries must be an object")
    for path, entry in entries.items():
        if not clean_path(path) or not inside(path):
            invalid(f"entry {path!r} is not a normalized path under an owned path")
        if not isinstance(entry, dict) or not isinstance(entry.get("kind"), str) \
                or entry["kind"] not in ENTRY_FIELDS \
                or set(entry) != ENTRY_FIELDS[entry["kind"]]:
            invalid(f"entry {path!r} has missing or unexpected fields for its kind")
        if not is_count(entry["size"]) or not isinstance(entry["binary"], bool) \
                or entry["git"] not in ("tracked", "untracked", "ignored"):
            invalid(f"entry {path!r} has an invalid size, binary flag or git status")
        if entry["kind"] == "file" and not is_digest(entry["sha256"]):
            invalid(f"entry {path!r} needs a SHA-256 digest")
        if entry["kind"] == "symlink" and not isinstance(entry["target"], str):
            invalid(f"entry {path!r} needs a string symlink target")
    summary = record["generated_summary"]
    if not isinstance(summary, dict):
        invalid("generated_summary must be an object")
    for key, group in summary.items():
        if not clean_path(key) or not isinstance(group, dict) or set(group) != {"count", "sha256"} \
                or not is_count(group["count"]) or not is_digest(group["sha256"]):
            invalid(f"generated summary {key!r} needs a normalized key, a count and a SHA-256 digest")
    outside = record["outside_status"]
    if not isinstance(outside, list):
        invalid("outside_status must be a list")
    for row in outside:
        if not isinstance(row, list) or len(row) != 3:
            invalid("outside status rows must be [code, path, digest]")
        code, path, digest = row
        if not is_status(code):
            invalid(f"outside status code {code!r} is not a Git porcelain v1 code")
        if not clean_path(path) or inside(path):
            invalid(f"outside path {path!r} is not a normalized path outside the owned paths")
        if not is_digest(digest, nullable=True):
            invalid(f"outside path {path!r} needs a SHA-256 digest or null")
    if record["head"] and git(root, "cat-file", "-e", record["head"] + "^{commit}", ok=(0, 1)).returncode:
        invalid("its commit is not in this repository")
    return record


def load_baseline(root, name):
    fd = open_baseline(baseline_file(root, name), name)
    try:
        with os.fdopen(fd, "r") as stream:
            text = stream.read()
    except OSError as exc:
        raise Refused(f"Could not read baseline {name}: {exc.strerror}") from None
    try:
        record = json.loads(text)
    except ValueError:
        raise Refused(f"Invalid baseline {name}: not valid JSON") from None
    return validate(root, name, record)


def item(path, entry):
    return {"path": path, "kind": entry["kind"], "git": entry["git"],
            "binary": entry["binary"], "size": entry["size"]}


def outside_changes(root, before, after, committed):
    """Status or content changes outside the owned paths, plus paths changed by new commits.

    A path absent from a status list was clean against HEAD at that moment. Its missing
    baseline hash is the empty patch when the baseline commit tracked it (None otherwise);
    its missing current hash is measured now against the baseline commit. So a commit of
    already-dirty content reads as unchanged content, and a revert reads as changed.
    """
    base = diff_base(root, before["head"])
    was = {path: (code, digest) for code, path, digest in before["outside_status"]}
    now = {path: (code, digest) for code, path, digest in after["outside_status"]}
    candidates = set(was) | set(now) | committed
    unseen = sorted(candidates - set(was))
    in_baseline_commit = (set(split_z(git(root, "ls-tree", "-r", "-z", "--name-only", before["head"],
                                          "--", *unseen).stdout))
                          if before["head"] and unseen else set())
    rows = []
    for path in sorted(candidates):
        code_before, hash_before = was.get(path) or (None, EMPTY_PATCH if path in in_baseline_commit else None)
        code_after, hash_after = now.get(path) or (None, outside_hash(root, base, path, None))
        if code_before != code_after or hash_before != hash_after or path in committed:
            rows.append({"path": path, "before": code_before, "after": code_after,
                         "changed_content": hash_before != hash_after, "committed": path in committed})
    return rows


def head_movement(root, before, after):
    """Commits since the baseline commit, or None when histories diverged; paths they touched.

    Paths come from every commit in the range (so a change and its revert still count)
    unioned with the endpoint diff (so rewritten or divergent history still counts).
    """
    if before == after:
        return 0, set()
    paths = set(split_z(git(root, "diff", "--name-only", "-z", "--no-renames",
                            diff_base(root, before), diff_base(root, after)).stdout))
    if after is None:
        return None, paths
    if before is None:
        span = [after]
    elif git(root, "merge-base", "--is-ancestor", before, after, ok=(0, 1)).returncode == 0:
        span = [before + ".." + after]
    else:
        return None, paths
    commits = int(git(root, "rev-list", "--count", *span).stdout.strip())
    history = split_z(git(root, "log", "--format=", "--name-only", "-z", "--no-renames", *span, "--").stdout)
    return commits, paths | set(history)


def compare(project, name):
    root = project_root(project)
    before = load_baseline(root, name)
    after = snapshot(root, before["paths"], before["generated"], before["head"])
    head = current_head(root)
    commits, committed_paths = head_movement(root, before["head"], head)
    inside = {p for p in committed_paths if any(under(p, o) for o in before["paths"])}
    old, new = before["entries"], after["entries"]
    clean = {"staged": EMPTY_PATCH, "unstaged": EMPTY_PATCH}
    tracked_changed = []
    for path in sorted(set(before["tracked"]) | set(after["tracked"])):
        a, b = before["tracked"].get(path, clean), after["tracked"].get(path, clean)
        if a != b:
            tracked_changed.append({"path": path, "staged": a["staged"] != b["staged"],
                                    "unstaged": a["unstaged"] != b["unstaged"]})
    added = [item(p, new[p]) for p in sorted(set(new) - set(old))]
    deleted = [item(p, old[p]) for p in sorted(set(old) - set(new))]
    modified = []
    for path in sorted(set(old) & set(new)):
        a, b = old[path], new[path]
        if (a["kind"], a.get("sha256"), a.get("target"), a["size"]) != (b["kind"], b.get("sha256"), b.get("target"), b["size"]):
            changed = item(path, b)
            changed["binary"] = a["binary"] or b["binary"]
            if a["git"] == "ignored":
                changed["git"] = "ignored"
            modified.append(changed)
    symlinks = [{"path": p, "before": old.get(p, {}).get("target"), "after": new.get(p, {}).get("target")}
                for p in sorted({i["path"] for i in added + modified + deleted})
                if "symlink" in (old.get(p, {}).get("kind"), new.get(p, {}).get("kind"))]
    groups = set(before["generated_summary"]) | set(after["generated_summary"])
    generated = {}
    for key in sorted(groups):
        a, b = before["generated_summary"].get(key), after["generated_summary"].get(key)
        generated[key] = {"before": a, "after": b, "changed": a != b}
    unexpected = [{**i, "change": change} for change, items in
                  (("added", added), ("modified", modified), ("deleted", deleted))
                  for i in items if i["git"] == "ignored"]
    outside = outside_changes(root, before, after, committed_paths - inside)
    to_read = sum(1 for i in added + modified if i["kind"] == "file" and not i["binary"] and i["git"] != "tracked")
    to_check = sum(1 for i in added + modified + deleted if i["binary"] or i["kind"] != "file")
    head_note = ("unchanged" if before["head"] == head else
                 "changed (diverged)" if commits is None else f"changed ({commits} commits)")
    summary = (f"Change read · {len(tracked_changed)} tracked paths changed, {to_read} text files to read, "
               f"{to_check} binary/symlink to check, generated "
               f"{'changed' if any(g['changed'] for g in generated.values()) else 'unchanged'}, "
               f"unexpected: {len(unexpected) or 'none'}, head: {head_note}")
    return {"baseline": name, "head": {"before": before["head"], "after": head, "changed": before["head"] != head,
                                       "commits": commits},
            "tracked_changed": tracked_changed, "committed": sorted(inside), "added": added,
            "modified": modified, "deleted": deleted, "symlinks_changed": symlinks, "generated": generated,
            "unexpected": unexpected, "outside": outside, "summary": summary}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default=".", help="Git work tree; resolved to its top level")
    sub = parser.add_subparsers(dest="action", required=True)
    name_help = "Baseline name: letters, digits, '.', '_' or '-' (max 64)"
    base = sub.add_parser("baseline", help="Record owned paths before dispatch")
    base.add_argument("--name", required=True, help=name_help)
    base.add_argument("--path", action="append", required=True,
                      help="Owned path inside the project; repeatable")
    base.add_argument("--generated", action="append", default=[],
                      help="Declared generated glob, e.g. 'build/**'; repeatable")
    base.add_argument("--replace", action="store_true", help="Overwrite an existing baseline of this name")
    check = sub.add_parser("compare", help="Report changes since a named baseline")
    check.add_argument("--name", required=True, help=name_help)
    drop = sub.add_parser("discard", help="Delete a named baseline after the return is accepted")
    drop.add_argument("--name", required=True, help=name_help)
    args = parser.parse_args(argv)
    try:
        if args.action == "baseline":
            record = baseline(args.project, args.path, args.generated, args.name, args.replace)
            result = {"baseline": args.name, "head": record["head"], "tracked_paths": len(record["tracked"]),
                      "entries": len(record["entries"]), "generated": record["generated_summary"]}
        elif args.action == "compare":
            result = compare(args.project, args.name)
        else:
            result = discard(args.project, args.name)
        print(json.dumps(result, indent=2))
        return 0
    except (Refused, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
