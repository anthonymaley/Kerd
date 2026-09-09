#!/usr/bin/env python3
"""Copy the candidate's supported files into a fresh portable plugin directory.

Development packaging only: no install, config changes, network or model calls.
"""
import argparse
import json
from pathlib import Path
import shutil

PACK = Path(__file__).resolve().parents[1]
SKILLS = ("conductor", "switch", "visuals")
SUFFIXES = {".md", ".py", ".html"}


def inputs(pack):
    result = {}
    for relative in [*(f"skills/{name}" for name in SKILLS), "guidance"]:
        folder = pack / relative
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError(f"Missing or linked source directory: {relative}")
        for path in sorted(folder.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Linked source is not packaged: {path}")
            if "__pycache__" in path.parts or path.name == ".DS_Store":
                continue
            if path.is_file():
                if path.suffix not in SUFFIXES and path.name != "LICENSE":
                    raise ValueError(f"Review new package file type: {path}")
                result[path.relative_to(pack)] = path
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
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists; left untouched: {destination}")
    destination.mkdir(parents=True, exist_ok=False)
    for relative, source in selected.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return len(selected), sum(path.stat().st_size for path in selected.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New directory ending in /kerd")
    args = parser.parse_args()
    try:
        count, size = build(args.destination)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"Not packaged: {exc}\n")
    print(f"Prepared {args.destination}: {count} files, {size} bytes. Not installed.")
