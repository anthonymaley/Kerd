#!/usr/bin/env python3
"""Build the slim Claude Code plugin tree from a committed Kerd release.

Installing Kerd from its marketplace used to copy the whole repository (docs,
images, evals, site, Kerd's own records) into every user's plugin cache. This
tool builds only what the installed plugin reads at runtime, from one exact
commit, into a fresh directory that is a git repository on branch `plugin`.

The new commit's parent is the remote's current `plugin` tip when one exists,
so the branch only ever appends. Nothing is pushed unless --publish is given,
and even then the push is leased on the checked tip
(`--force-with-lease`), so it can only fast-forward what was checked. The source
checkout, its index and user configuration are never changed.

Fail-closed: a file the allowlist cannot classify, a symlink, a missing
required file, a hook script hooks.json names but the tree lacks, or a remote
that cannot be read all refuse the build rather than being treated as absent.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "plugin"
MAIN = "refs/heads/main"

# What the installed plugin reads at runtime. Everything else in the repository
# (the rest of docs/, evals/, site/, examples/, kivna/, tools/, tests/, mods/, CONTEXT.md,
# TODO.md, CHANGELOG.md, ...) stays out of the user's plugin cache.
INCLUDE_FILES = (".claude-plugin/plugin.json", "README.md", "LICENSE",
                 # Kivna names these as its source of truth.
                 "docs/vault-spec.md", "docs/state-contract.md")
INCLUDE_DIRS = ("skills", "agents", "hooks")
# Inside the included directories, these are development-only and skipped.
EXCLUDE_PARTS = ("__pycache__",)
EXCLUDE_NAMES = (".DS_Store",)
EXCLUDE_SKILL_TESTS = re.compile(r"^skills/[^/]+/scripts/tests/")
# A new file type inside an included directory is a decision, not a default.
SUFFIXES = {".md", ".py", ".sh", ".json", ".html", ".txt"}
NAMES = {"LICENSE"}
# Kerd's own working records must never reach users, wherever they sit. A match
# anywhere in an included path refuses the build rather than being skipped, so a
# record that strays into skills/ is seen, not silently shipped or dropped.
# (`kivna` alone is the Kivna skill's own folder, so only its records path counts.)
PRIVATE_NAMES = {"CONTEXT.md", "TODO.md", "MEMORY.md", "CLAUDE.md", "vault.json", "settings.local.json"}
PRIVATE_DIRS = {"sessions", ".claude", ".git", "Sensei Input"}
PRIVATE_PATHS = (("docs", "work"), ("kivna", "sessions"))
REQUIRED = (".claude-plugin/plugin.json", "hooks/hooks.json", "README.md", "LICENSE")
HOOK_PATH = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"'\s]+)")


def release_version(value):
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value):
        raise ValueError("Public plugin releases need a stable MAJOR.MINOR.PATCH version")
    return tuple(map(int, value.split(".")))


def git(repo, *args, input=None):
    result = subprocess.run(["git", "-C", str(repo), *args], input=input, capture_output=True)
    if result.returncode:
        raise ValueError(f"git {' '.join(args[:2])}: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout.decode().strip()


def tracked(repo, commit):
    """Every tracked entry of the commit: path -> (mode, size). Read from git, so
    untracked or uncommitted files in the checkout can never enter the package."""
    out = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-l", "-z", commit],
                         capture_output=True)
    if out.returncode:
        raise ValueError(f"Could not list {commit}: {out.stderr.decode(errors='replace').strip()}")
    entries = {}
    for record in out.stdout.decode().split("\0"):
        if not record:
            continue
        meta, path = record.split("\t", 1)
        mode, kind, _sha, size = meta.split()
        entries[path] = (mode, kind, 0 if size == "-" else int(size))
    if not entries:
        raise ValueError(f"Commit {commit} lists no files; refusing an empty package")
    return entries


def private(path):
    """Why a path is one of Kerd's private records, or None."""
    parts = PurePosixPath(path).parts
    name = parts[-1]
    if name in PRIVATE_NAMES:
        return f"private file name {name}"
    if name.startswith(".env") or re.search(r"\.local(\.|$)", name):
        return f"private file name {name}"
    for part in parts[:-1]:
        if part in PRIVATE_DIRS:
            return f"private folder {part}/"
    for sequence in PRIVATE_PATHS:
        for start in range(len(parts) - len(sequence) + 1):
            if parts[start:start + len(sequence)] == sequence:
                return f"private folder {'/'.join(sequence)}/"
    return None


def select(entries):
    """Apply the allowlist. Returns the sorted package paths or raises."""
    chosen = []
    for path, (mode, kind, _size) in sorted(entries.items()):
        top = path.split("/", 1)[0]
        if path not in INCLUDE_FILES and top not in INCLUDE_DIRS:
            continue
        pure = PurePosixPath(path)
        if (any(part in EXCLUDE_PARTS for part in pure.parts) or pure.name in EXCLUDE_NAMES
                or EXCLUDE_SKILL_TESTS.match(path)):
            continue
        why = private(path)
        if why:
            raise ValueError(f"Private record in an included folder ({why}): {path}")
        if mode == "120000":
            raise ValueError(f"Linked file is not packaged: {path}")
        if kind != "blob":
            raise ValueError(f"Submodule or non-file entry is not packaged: {path}")
        if path not in INCLUDE_FILES and pure.suffix not in SUFFIXES and pure.name not in NAMES:
            raise ValueError(f"Review new package file type: {path}")
        chosen.append(path)
    return chosen


def strings(value):
    """Every string inside a parsed JSON value, so hook commands are read
    after JSON unescaping rather than from the raw text."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def check_complete(chosen, snapshot):
    """The package must carry everything the installed plugin is known to read."""
    present = set(chosen)
    for path in REQUIRED:
        if path not in present:
            raise ValueError(f"Required package file missing from the commit: {path}")
    skills = {p.split("/")[1] for p in present if p.startswith("skills/")}
    if not skills:
        raise ValueError("No skills in the commit; refusing an empty plugin")
    for name in sorted(skills):
        if f"skills/{name}/SKILL.md" not in present:
            raise ValueError(f"Missing skill entry: skills/{name}/SKILL.md")
    if not any(p.startswith("agents/") and p.endswith(".md") for p in present):
        raise ValueError("No agents in the commit; refusing a package without its routing agents")
    hooks = json.loads((snapshot / "hooks/hooks.json").read_text(encoding="utf-8"))
    for referenced in sorted(set(HOOK_PATH.findall("\n".join(strings(hooks))))):
        if referenced not in present:
            raise ValueError(f"hooks.json runs {referenced}, which the package would not carry")


def prepare(destination, ref="HEAD", repo=ROOT):
    """Write the slim tree for one exact commit into a fresh directory."""
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination exists; left untouched: {destination}")
    commit = git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")
    entries = tracked(repo, commit)
    chosen = select(entries)
    with tempfile.TemporaryDirectory(prefix="kerd-plugin-source-") as temporary:
        snapshot = Path(temporary)
        archive = subprocess.run(["git", "-C", str(repo), "archive", commit],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-xf", "-", "-C", str(snapshot)], input=archive, check=True)
        manifest = json.loads((snapshot / ".claude-plugin/plugin.json").read_text())
        if manifest.get("name") != "kerd":
            raise ValueError("Plugin manifest name must be kerd")
        version = manifest["version"]
        release_version(version)
        marketplace = json.loads((snapshot / ".claude-plugin/marketplace.json").read_text())
        if (marketplace["metadata"]["version"] != version
                or marketplace["plugins"][0]["version"] != version):
            raise ValueError("Source release versions disagree")
        check_complete(chosen, snapshot)
        # Validated before the destination exists, so a refusal leaves nothing behind.
        destination.mkdir(parents=True)
        for path in chosen:
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(snapshot / path, target)
    release = {"version": version, "source_commit": commit}
    (destination / "release.json").write_text(json.dumps(release, indent=2) + "\n")
    report = {"files": len(chosen) + 1,
              "bytes": sum(entries[p][2] for p in chosen) + (destination / "release.json").stat().st_size,
              "source_files": len(entries),
              "source_bytes": sum(size for _mode, _kind, size in entries.values())}
    return release, report


def previous(destination, remote, repo, release, expect=None):
    """The remote's plugin tip to append to, after the same checks Codex uses.
    None only when the remote answered and has no plugin branch yet.

    `expect` is the tip a caller already checked: "" for no branch, a commit for
    that tip. When given, any other tip refuses, so the append can only land on
    the commit the caller looked at."""
    listed = git(repo, "ls-remote", "--heads", remote, f"refs/heads/{BRANCH}")
    tip = listed.split()[0] if listed else ""
    if expect is not None and tip != expect:
        raise ValueError(f"Remote {BRANCH} tip is {tip[:12] or 'absent'}, not the expected "
                         f"{expect[:12] or 'absent'}; it moved. Not appended")
    if not tip:
        return None
    git(destination, "fetch", "-q", "--no-tags", remote, tip)
    parent = git(destination, "rev-parse", "FETCH_HEAD")
    if parent != tip:
        raise ValueError(f"Fetched {parent[:12]}, not the listed tip {tip[:12]}; not appended")
    old = json.loads(git(destination, "show", f"{parent}:release.json"))
    present = subprocess.run(["git", "-C", str(repo), "cat-file", "-e",
                              f"{old['source_commit']}^{{commit}}"], capture_output=True)
    if present.returncode:
        raise ValueError(f"Previous plugin release source {old['source_commit']} is not in this checkout; "
                         "run git fetch origin and retry")
    # An unrelated branch or a rollback needs a separate, deliberate operation.
    ancestor = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor",
                               old["source_commit"], release["source_commit"]])
    if ancestor.returncode:
        raise ValueError("Previous plugin release is not an ancestor of this source")
    if old == release:
        raise ValueError("This source release is already on the plugin branch")
    if old["version"] == release["version"]:
        # Claude Code keys updates on the manifest version: same version, no update.
        raise ValueError("Changed package needs a new release version")
    if release_version(release["version"]) < release_version(old["version"]):
        raise ValueError("Release version would go backwards")
    return parent


def commit(destination, release, remote, repo=ROOT, expect=None):
    """Record the tree as one new commit on the local plugin branch, appended to
    the remote's tip. Pushes nothing."""
    destination = Path(destination).absolute()
    git(destination, "init", "-q", "-b", BRANCH)
    parent = previous(destination, remote, repo, release, expect)
    git(destination, "add", "--all")
    tree = git(destination, "write-tree")
    parents = ["-p", parent] if parent else []
    made = git(destination, "commit-tree", tree, *parents,
               "-m", f"Kerd plugin {release['version']} from {release['source_commit']}")
    git(destination, "update-ref", f"refs/heads/{BRANCH}", made)
    return made, parent


def publish(destination, release, remote):
    """Push the plugin branch only. The push carries a lease on the new commit's
    own parent: the remote must still hold exactly that tip (or no branch, for a
    first commit), so the update is always a fast-forward of what was checked. A
    tip that moved after the fetch makes the push refuse; nothing is overwritten."""
    git(destination, "fetch", "-q", "--no-tags", remote, MAIN)
    on_main = subprocess.run(["git", "-C", str(destination), "merge-base", "--is-ancestor",
                              release["source_commit"], "FETCH_HEAD"], capture_output=True)
    if on_main.returncode:
        raise ValueError(f"Source {release['source_commit']} is not on the remote's main; push it first. Not pushed")
    line = git(destination, "rev-list", "--parents", "-n", "1", f"refs/heads/{BRANCH}").split()
    if len(line) > 2:
        raise ValueError("The plugin commit has more than one parent; not pushed")
    lease = line[1] if len(line) == 2 else ""  # empty: the branch must not exist yet
    git(destination, "push", f"--force-with-lease=refs/heads/{BRANCH}:{lease}", remote,
        f"refs/heads/{BRANCH}:refs/heads/{BRANCH}")


def mib(count):
    return f"{count / (1024 * 1024):.2f} MiB"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("destination", type=Path, help="Fresh output directory; older builds are kept")
    parser.add_argument("--ref", default="HEAD", help="Exact committed release to package")
    parser.add_argument("--remote", help="Repository whose plugin branch to append to (default: origin's URL)")
    parser.add_argument("--expect-tip", metavar="COMMIT|none",
                        help="Refuse unless the remote's plugin tip is exactly this commit ('none': no branch yet)")
    parser.add_argument("--publish", action="store_true",
                        help="Push only the remote's plugin branch; needs publication approval")
    args = parser.parse_args(argv)
    destination = args.destination.absolute()
    # Only a folder this run created is removed on a refusal; an existing one is never touched.
    fresh = not (destination.exists() or destination.is_symlink())
    try:
        remote = args.remote or git(ROOT, "remote", "get-url", "origin")
        release, report = prepare(destination, args.ref, repo=ROOT)
        print(f"Prepared Kerd plugin {release['version']} from {release['source_commit']} in {destination}")
        print(f"Size: {report['files']} files, {mib(report['bytes'])} "
              f"(source commit: {report['source_files']} files, {mib(report['source_bytes'])})")
        expect = None if args.expect_tip is None else ("" if args.expect_tip == "none" else args.expect_tip)
        made, parent = commit(destination, release, remote, repo=ROOT, expect=expect)
        print(f"Committed {made} on local branch {BRANCH}"
              + (f", appended to {parent}" if parent else ", first commit (remote has no plugin branch)"))
        if args.publish:
            publish(destination, release, remote)
            print(f"Published {BRANCH} branch: {made}")
        else:
            print("Not published or installed. --publish requires a separate publication go.")
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        if fresh and (destination.exists() or destination.is_symlink()):
            shutil.rmtree(destination, ignore_errors=True)
            exc = f"{exc} (removed the refused build at {destination})"
        parser.exit(2, f"Not completed: {exc}\n")


if __name__ == "__main__":
    main()
