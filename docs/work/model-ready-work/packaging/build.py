#!/usr/bin/env python3
"""Build the four core skills into a fresh portable plugin or Codex catalog.

The four skills come from the repository's own `skills/`, which is the single
maintained source since v0.107.0 — packaging consumes it rather than keeping a
second copy that would drift. Guidance ships inside Conductor's references.

Development packaging only: no install, config changes, network or model calls.
"""
import argparse
import json
from pathlib import Path
import shutil

PACK = Path(__file__).resolve().parents[1]
SKILLS = ("conductor", "switch", "visuals", "agent")
SUFFIXES = {".md", ".py", ".html"}
REVIEWED_FILES = {Path("skills/agent/scripts/requirements.txt")}


def inputs(pack):
    repo = pack.parents[2]
    result = {}
    sources = [(repo, f"skills/{name}") for name in SKILLS]
    for root, relative in sources:
        folder = root / relative
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError(f"Missing or linked source directory: {relative}")
        for path in sorted(folder.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Linked source is not packaged: {path}")
            if "__pycache__" in path.parts or path.name == ".DS_Store":
                continue
            if path.is_file():
                if (path.suffix not in SUFFIXES and path.name != "LICENSE"
                        and path.relative_to(root) not in REVIEWED_FILES):
                    raise ValueError(f"Review new package file type: {path}")
                result[path.relative_to(root)] = path
    for name in SKILLS:
        if Path(f"skills/{name}/SKILL.md") not in result:
            raise ValueError(f"Missing skill entry: {name}")
    for host in ("claude", "codex"):
        path = pack / "packaging" / f"{host}-plugin.json"
        if json.loads(path.read_text())["name"] != "kerd":
            raise ValueError("Plugin name must match the kerd directory")
        result[Path(f".{host}-plugin/plugin.json")] = path
    result[Path("README.md")] = pack / "packaging" / "START.md"
    result[Path("LICENSE")] = pack.parents[2] / "LICENSE"
    for path in result.values():
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or linked package input: {path}")
    return result


def build(destination, pack=PACK):
    destination = Path(destination).absolute()
    if destination.name != "kerd":
        raise ValueError("Destination directory must be named kerd")
    selected = inputs(pack)  # Validate all sources before creating output.
    version = json.loads((pack.parents[2] / ".claude-plugin/plugin.json").read_text())["version"]
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists; left untouched: {destination}")
    destination.mkdir(parents=True, exist_ok=False)
    for relative, source in selected.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative in (Path(".claude-plugin/plugin.json"), Path(".codex-plugin/plugin.json")):
            manifest = json.loads(source.read_text())
            manifest["version"] = version  # One release version; no stale candidate pin.
            target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        else:
            shutil.copy2(source, target)
    return len(selected), sum((destination / path).stat().st_size for path in selected)


def build_marketplace(destination, pack=PACK):
    """Generate an installable catalog artifact, never register or install it."""
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists; left untouched: {destination}")
    count, size = build(destination / "plugins" / "kerd", pack)
    catalog = {"name": "kerd-core", "interface": {"displayName": "Kerd core"},
               "plugins": [{"name": "kerd", "source": {"source": "local", "path": "./plugins/kerd"},
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                            "category": "Productivity"}]}
    path = destination / ".agents" / "plugins" / "marketplace.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    return count + 1, size + path.stat().st_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New directory ending in /kerd")
    parser.add_argument("--codex-marketplace", action="store_true",
                        help="Build a catalog root containing plugins/kerd; no install or settings writes")
    args = parser.parse_args()
    try:
        count, size = (build_marketplace if args.codex_marketplace else build)(args.destination)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"Not packaged: {exc}\n")
    print(f"Prepared {args.destination}: {count} files, {size} bytes. Not installed.")
