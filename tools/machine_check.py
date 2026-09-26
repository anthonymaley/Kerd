#!/usr/bin/env python3
"""Check this machine's Kerd setup after a move (docs/machine-setup.md, sections 3 to 5).

Reads settings as JSON, so the enabled-plugin line never reads as a hand-wired hook.
Checks: no Kerd hook (command or prompt) in the user-global `hooks` key or any product
repo's `.claude/settings.json` or `.claude/settings.local.json`; the plugin is enabled, every installed entry is this repo's
version and its install directory exists; `~/eolas/vault` resolves. Flags leftover files nothing reads (`kivna/.pair`).
Reads only; changes nothing. Exit 0 when every check passes, 1 on any failure.
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "kerd@kerd-marketplace"
LEFTOVERS = ["kivna/.pair"]


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return None


def kerd_hooks(settings):
    """Hook commands in a settings object that mention Kerd."""
    found = []
    for groups in ((settings or {}).get("hooks") or {}).values():
        for group in groups or []:
            for hook in (group or {}).get("hooks") or []:
                text = " ".join(str(v) for v in (hook or {}).values() if isinstance(v, str))
                if "kerd" in text.lower():
                    found.append(text)
    return found


def check(home, repo=REPO_ROOT):
    """(failures, notes) for this machine."""
    home, repo = Path(home), Path(repo)
    failures, notes = [], []
    user = load(home / ".claude/settings.json")
    if user is None:
        failures.append("~/.claude/settings.json is missing or not JSON")
    for command in kerd_hooks(user):
        failures.append(f"Hand-wired Kerd hook in ~/.claude/settings.json: {command}")
    product = home / "development/product"
    for local in sorted(list(product.glob("*/.claude/settings.local.json")) + list(product.glob("*/.claude/settings.json"))):
        for command in kerd_hooks(load(local)):
            failures.append(f"Hand-wired Kerd hook in {local}: {command}")
    if (user or {}).get("enabledPlugins", {}).get(PLUGIN) is not True:
        failures.append(f"{PLUGIN} is not enabled in ~/.claude/settings.json")
    installed = (load(home / ".claude/plugins/installed_plugins.json") or {}).get("plugins", {}).get(PLUGIN) or []
    entries = [entry for entry in installed if isinstance(entry, dict)]
    versions = sorted({str(entry.get("version")) for entry in entries})
    wanted = (load(repo / ".claude-plugin/plugin.json") or {}).get("version")
    if versions != [wanted]:
        failures.append(f"Installed Kerd {', '.join(versions) or 'none'} does not match this repo's {wanted}")
    for entry in entries:
        path = str(entry.get("installPath") or "").strip()
        if not path or not Path(path).is_absolute() or not Path(path).is_dir():
            failures.append(f"Kerd's install directory is missing: {entry.get('installPath') or 'not recorded'}")
    if not (home / "eolas/vault").is_dir():
        failures.append("~/eolas/vault does not resolve")
    for leftover in LEFTOVERS:
        if (repo / leftover).exists():
            notes.append(f"{leftover} is left over; nothing reads it, safe to delete")
    return failures, notes


def main():
    failures, notes = check(Path.home())
    for line in failures:
        print(f"FAIL  {line}")
    for line in notes:
        print(f"note  {line}")
    print("machine: clean" if not failures else f"machine: {len(failures)} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
