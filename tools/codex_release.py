#!/usr/bin/env python3
"""Prepare a Codex marketplace from a committed Kerd release.

Offline by default. --publish additionally appends it to origin's generated
codex branch and pushes that branch only. Never force-pushes, installs a plugin,
changes user configuration, or changes the source checkout/index.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGING = "docs/work/model-ready-work/packaging"
MAIN = "refs/heads/main"


def release_version(value):
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value):
        raise ValueError("Public Codex releases need a stable MAJOR.MINOR.PATCH version")
    return tuple(map(int, value.split(".")))


def git(repo, *args, input=None):
    result = subprocess.run(["git", "-C", str(repo), *args],
                            input=input, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip())
    return result.stdout.decode().strip()


def prepare(destination, ref="HEAD", repo=ROOT):
    """Build only tracked inputs from one exact commit; preserve old artifacts."""
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination exists; left untouched: {destination}")
    commit = git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")
    with tempfile.TemporaryDirectory(prefix="kerd-codex-source-") as temporary:
        snapshot = Path(temporary)
        archive = subprocess.run(["git", "-C", str(repo), "archive", commit],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-xf", "-", "-C", str(snapshot)], input=archive, check=True)
        manifest = json.loads((snapshot / ".claude-plugin/plugin.json").read_text())
        version = manifest["version"]
        release_version(version)
        marketplace = json.loads((snapshot / ".claude-plugin/marketplace.json").read_text())
        if (marketplace["metadata"]["version"] != version
                or marketplace["plugins"][0]["version"] != version):
            raise ValueError("Source release versions disagree")
        spec = importlib.util.spec_from_file_location("kerd_package", snapshot / PACKAGING / "build.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.build_marketplace(destination)
    release = {"version": version, "source_commit": commit}
    (destination / "release.json").write_text(json.dumps(release, indent=2) + "\n")
    return release


def publish(destination, release, repo=ROOT):
    """Append to the generated branch; a concurrent publisher makes push refuse."""
    destination = Path(destination).absolute()
    remote = git(repo, "remote", "get-url", "origin")
    previous = git(repo, "ls-remote", "--heads", remote, "refs/heads/codex")
    git(destination, "init", "-q", "-b", "codex")
    # Fetched fresh into the package repo, so the source checkout stays untouched.
    git(destination, "fetch", "--no-tags", remote, MAIN)
    on_main = subprocess.run(["git", "-C", str(destination), "merge-base", "--is-ancestor",
                              release["source_commit"], "FETCH_HEAD"], capture_output=True)
    if on_main.returncode:
        raise ValueError(f"Source {release['source_commit']} is not on origin's main; push it first. Not pushed")
    parents = []
    if previous:
        git(destination, "fetch", "--no-tags", remote, "refs/heads/codex")
        parent = git(destination, "rev-parse", "FETCH_HEAD")
        old = json.loads(git(destination, "show", f"{parent}:release.json"))
        present = subprocess.run(["git", "-C", str(repo), "cat-file", "-e",
                                  f"{old['source_commit']}^{{commit}}"], capture_output=True)
        if present.returncode:
            raise ValueError(f"Previous Codex release source {old['source_commit']} is not in this checkout; "
                             "run git fetch origin and retry. Not pushed")
        # An unrelated branch or a rollback needs a separate, deliberate operation.
        ancestor = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor",
                                   old["source_commit"], release["source_commit"]])
        if ancestor.returncode:
            raise ValueError("Previous Codex release is not an ancestor of this source; not pushed")
        if old == release:
            raise ValueError("This source release is already published; not pushed")
        if old["version"] == release["version"]:
            raise ValueError("Changed package needs a new release version; not pushed")
        if release_version(release["version"]) < release_version(old["version"]):
            raise ValueError("Release version would go backwards; not pushed")
        parents = ["-p", parent]
    git(destination, "add", "--all")
    tree = git(destination, "write-tree")
    commit = git(destination, "commit-tree", tree, *parents,
                 "-m", f"Kerd core {release['version']} from {release['source_commit']}")
    git(destination, "update-ref", "refs/heads/codex", commit)
    git(destination, "push", remote, "refs/heads/codex:refs/heads/codex")
    return commit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Fresh output directory; older builds are kept")
    parser.add_argument("--ref", default="HEAD", help="Exact committed release to package")
    parser.add_argument("--publish", action="store_true", help="Push only origin's codex branch; needs publication approval")
    args = parser.parse_args()
    try:
        release = prepare(args.destination, args.ref)
        print(f"Prepared Kerd {release['version']} from {release['source_commit']} in {args.destination}")
        if args.publish:
            commit = publish(args.destination, release)
            print(f"Published codex branch: {commit}")
        else:
            print("Not published or installed. --publish requires a separate publication go.")
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"Not completed: {exc}\n")


if __name__ == "__main__":
    main()
