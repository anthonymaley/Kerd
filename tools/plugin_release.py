#!/usr/bin/env python3
"""Build the slim Claude Code plugin tree from a committed Kerd release.

Installing Kerd from its marketplace used to copy the whole repository (docs,
images, evals, site, Kerd's own records) into every user's plugin cache. This
tool builds only what the installed plugin reads at runtime, from one exact
commit, into a fresh directory that is a git repository on branch `plugin`:
`.claude-plugin/plugin.json`, `skills/`, `agents/`, `hooks/`, README.md,
LICENSE, the two docs Kivna reads, `release.json`, overtone's tracked folder
`mods/overtone/`, and a `.claude-plugin/marketplace.json`.

That marketplace.json makes the branch a marketplace of its own
(`claude plugin marketplace add owner/repo#plugin`). It is generated from the
same commit's `.claude-plugin/marketplace.json`, never kept by hand: same
`name`, `owner` and `metadata`; the kerd entry's source becomes `"./"` (the
branch root, where plugin.json sits) and overtone keeps `./mods/overtone`. Any
other plugin entry, field or source form refuses the build.

The new commit's parent is the remote's current `plugin` tip when one exists,
so the branch only ever appends. Nothing is pushed unless --publish is given,
and even then the push is leased on the checked tip
(`--force-with-lease`), so it can only fast-forward what was checked. The source
checkout, its index and user configuration are never changed.

Fail-closed: a file the allowlist cannot classify, a symlink, a missing
required file, a hook script hooks.json names but the tree lacks, a marketplace
entry or source the generator cannot classify, or a remote that cannot be read
all refuse the build rather than being treated as absent.
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
# (the rest of docs/, evals/, site/, examples/, kivna/, tools/, tests/, the rest of mods/,
# CONTEXT.md, TODO.md, CHANGELOG.md, ...) stays out of the user's plugin cache.
INCLUDE_FILES = (".claude-plugin/plugin.json", "README.md", "LICENSE",
                 # Kivna names these as its source of truth.
                 "docs/vault-spec.md", "docs/state-contract.md")
INCLUDE_DIRS = ("skills", "agents", "hooks")
# Companion plugins the generated marketplace lists by relative source: entry name
# -> folder. Each folder is copied exactly as tracked, through the same allowlist.
MODS = {"overtone": "mods/overtone"}
# Inside the included directories, these are development-only and skipped.
EXCLUDE_PARTS = ("__pycache__",)
EXCLUDE_NAMES = (".DS_Store",)
EXCLUDE_SKILL_TESTS = re.compile(r"^skills/[^/]+/scripts/tests/")
# A new file type inside an included directory is a decision, not a default.
SUFFIXES = {".md", ".py", ".sh", ".json", ".html", ".txt"}
NAMES = {"LICENSE"}
# Decision (slim marketplace): a mod is a hooks module written in TypeScript
# (`.ts`, `.tsx`, and `.d.ts`, whose suffix is `.ts`). Allowed inside a MODS folder
# only; anywhere else they still refuse as a new type.
MOD_SUFFIXES = {".ts", ".tsx"}
# Kerd's own working records must never reach users, wherever they sit. A match
# anywhere in an included path refuses the build rather than being skipped, so a
# record that strays into skills/ is seen, not silently shipped or dropped.
# (`kivna` alone is the Kivna skill's own folder, so only its records path counts.)
PRIVATE_NAMES = {"CONTEXT.md", "TODO.md", "MEMORY.md", "CLAUDE.md", "vault.json", "settings.local.json"}
PRIVATE_DIRS = {"sessions", ".claude", ".git", "Sensei Input"}
PRIVATE_PATHS = (("docs", "work"), ("kivna", "sessions"))
REQUIRED = (".claude-plugin/plugin.json", "hooks/hooks.json", "README.md", "LICENSE",
            *(f"{folder}/.claude-plugin/plugin.json" for folder in MODS.values()))
HOOK_PATH = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"'\s]+)")
MARKETPLACE = ".claude-plugin/marketplace.json"


def _text(value):
    return isinstance(value, str) and bool(value.strip())


# The generated marketplace.json knows exactly these fields, at every level. A field
# it does not list, a missing required one or a wrong type refuses the build rather
# than being dropped or copied unread. Each schema: field -> (required, what, check).
TEXT = ("a non-empty string", _text)
FLAG = ("true or false", lambda value: isinstance(value, bool))
OBJECT = ("an object", lambda value: isinstance(value, dict))
LIST = ("a list", lambda value: isinstance(value, list))
MARKETPLACE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
MARKETPLACE_KEYS = ("name", "owner", "metadata", "plugins")
MARKETPLACE_SCHEMA = {
    "name": (True, "a marketplace name (letters, digits, . _ -, no ..)",
             lambda value: isinstance(value, str) and bool(MARKETPLACE_NAME.fullmatch(value))
             and ".." not in value),
    "owner": (True, *OBJECT), "metadata": (False, *OBJECT), "plugins": (True, *LIST)}
OWNER_SCHEMA = {"name": (True, *TEXT), "email": (False, *TEXT), "url": (False, *TEXT)}
METADATA_SCHEMA = {"description": (False, *TEXT), "version": (False, *TEXT)}
ENTRY_SCHEMA = {"name": (True, *TEXT), "source": (True, "a source", lambda value: value is not None),
                "description": (False, *TEXT), "version": (False, *TEXT), "strict": (False, *FLAG)}
# The kerd entry on main points Claude Code at this branch; these are the only
# remote forms the generator turns into "./", each with exactly these fields.
GITHUB_URL = re.compile(r"https://github\.com/[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/"
                        r"(?![.]{1,2}(?:\.git)?$)[A-Za-z0-9._-]+?(?:\.git)?")
GITHUB_REPO = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/(?![.]{1,2}$)[A-Za-z0-9._-]+")
KERD_SOURCE_SCHEMAS = {
    "url": {"source": (True, *TEXT),
            "url": (True, "an https://github.com/owner/name URL",
                    lambda value: isinstance(value, str) and bool(GITHUB_URL.fullmatch(value))),
            "ref": (True, *TEXT)},
    "github": {"source": (True, *TEXT),
               "repo": (True, "owner/name",
                        lambda value: isinstance(value, str) and bool(GITHUB_REPO.fullmatch(value))),
               "ref": (True, *TEXT)},
}


def check_schema(value, schema, label):
    """Refuse an object with a field the schema does not list, a missing required
    field, or a field whose value fails its check."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object, got {type(value).__name__}")
    unknown = sorted(set(value) - set(schema))
    if unknown:
        raise ValueError(f"{label}: unknown field(s) {', '.join(unknown)}; "
                         "teach the generator before shipping them")
    for field, (required, what, check) in schema.items():
        if field not in value:
            if required:
                raise ValueError(f"{label}: missing {field}")
            continue
        if not check(value[field]):
            raise ValueError(f"{label}: {field} must be {what}, got {value[field]!r}")


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


def in_mod(path):
    return any(path.startswith(folder + "/") for folder in MODS.values())


def select(entries):
    """Apply the allowlist. Returns the sorted package paths or raises."""
    chosen = []
    for path, (mode, kind, _size) in sorted(entries.items()):
        top = path.split("/", 1)[0]
        mod = in_mod(path)
        if path not in INCLUDE_FILES and top not in INCLUDE_DIRS and not mod:
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
        if (path not in INCLUDE_FILES and pure.suffix not in SUFFIXES and pure.name not in NAMES
                and not (mod and pure.suffix in MOD_SUFFIXES)):
            raise ValueError(f"Review new package file type: {path}")
        chosen.append(path)
    return chosen


def relative_source(value, label):
    """A relative plugin source as Claude Code reads one: starts with ./, no
    `..`, forward slashes only. Returns the folder it names ("" for the root)."""
    if not isinstance(value, str) or not value.startswith("./"):
        raise ValueError(f"{label}: a relative source must start with ./, got {value!r}")
    if ".." in value or "\\" in value or "//" in value[1:]:
        raise ValueError(f"{label}: relative source {value!r} may not contain .., a backslash or //")
    return value[2:].rstrip("/")


def branch_marketplace(source, chosen):
    """The plugin branch's own marketplace.json, generated from the shipped
    commit's: same name, owner and metadata; kerd at the branch root ("./");
    each mod at its own folder. Fail-closed on anything it cannot classify."""
    check_schema(source, MARKETPLACE_SCHEMA, f"{MARKETPLACE} (top level)")
    check_schema(source["owner"], OWNER_SCHEMA, f"{MARKETPLACE} owner")
    if "metadata" in source:
        check_schema(source["metadata"], METADATA_SCHEMA, f"{MARKETPLACE} metadata")
    plugins = source["plugins"]
    for index, entry in enumerate(plugins):
        check_schema(entry, ENTRY_SCHEMA, f"{MARKETPLACE} plugins[{index}]")
    names = [entry["name"] for entry in plugins]
    expected = sorted(["kerd", *MODS])
    if sorted(map(str, names)) != expected:
        raise ValueError(f"{MARKETPLACE}: plugin entries must be exactly {', '.join(expected)}; "
                         f"found {', '.join(map(str, names)) or 'none'}")
    present = set(chosen)
    generated = []
    for entry in plugins:
        name = entry["name"]
        label = f"{MARKETPLACE} entry {name}"
        src = entry["source"]
        if name == "kerd":
            kind = src.get("source") if isinstance(src, dict) else None
            if kind not in KERD_SOURCE_SCHEMAS:
                raise ValueError(f"{label}: source {src!r} is not a form the generator can classify")
            check_schema(src, KERD_SOURCE_SCHEMAS[kind], f"{label} source ({kind})")
            if src["ref"] != BRANCH:
                raise ValueError(f"{label}: source ref must be {BRANCH!r}, got {src.get('ref')!r}")
            generated.append({key: ("./" if key == "source" else value) for key, value in entry.items()})
            continue
        folder = relative_source(src, label)
        if folder != MODS[name] or src != f"./{MODS[name]}":
            raise ValueError(f"{label}: source must be ./{MODS[name]}, got {src!r}")
        if f"{folder}/.claude-plugin/plugin.json" not in present:
            raise ValueError(f"{label}: {folder}/.claude-plugin/plugin.json is not in the package")
        generated.append(dict(entry))
    return {key: (generated if key == "plugins" else source[key])
            for key in MARKETPLACE_KEYS if key in source}


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
        marketplace = json.loads((snapshot / MARKETPLACE).read_text())
        if (marketplace["metadata"]["version"] != version
                or marketplace["plugins"][0]["version"] != version):
            raise ValueError("Source release versions disagree")
        check_complete(chosen, snapshot)
        catalog = json.dumps(branch_marketplace(marketplace, chosen), indent=2, ensure_ascii=False) + "\n"
        # Validated before the destination exists, so a refusal leaves nothing behind.
        destination.mkdir(parents=True)
        for path in chosen:
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(snapshot / path, target)
        (destination / MARKETPLACE).write_text(catalog, encoding="utf-8")
    release = {"version": version, "source_commit": commit}
    (destination / "release.json").write_text(json.dumps(release, indent=2) + "\n")
    written = ("release.json", MARKETPLACE)
    report = {"files": len(chosen) + len(written),
              "bytes": sum(entries[p][2] for p in chosen)
              + sum((destination / name).stat().st_size for name in written),
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
