#!/usr/bin/env python3
"""Prepare named isolated GitHub trial files, without publishing or launching."""
import argparse
import json
from pathlib import Path
import shutil
import sys

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import handoff
import roll

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("project", type=Path)
args = parser.parse_args()
root = handoff.root_for(args.project)
handoff.require_branch(root, "kerd-switch-trial-20260906")
if handoff.git(root, "rev-parse", "HEAD") != "2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83" or handoff.git(root, "status", "--porcelain"):
    raise ValueError("Require the identified clean trial checkpoint")
if handoff.git(root, "remote", "get-url", "origin") != "git@github.com:anthonymaley/seinn.git":
    raise ValueError("Wrong trial origin")
relative = Path("docs/work/switch-trial/device-build")
folder = root / relative
folder.mkdir()
seed = Path(__file__).resolve().parents[1] / "live-control/output"
for name in ("pickup_preview.py", "test_pickup_preview.py", "USAGE.md", "example.json"):
    shutil.copyfile(seed / name, folder / name)
for name in ("agreement.md", "pickup.md"):
    shutil.copyfile(Path(__file__).with_name(name), folder / name)
state = dict(status="continue", next_action="Add the safe Markdown report format, tests and usage under the agreement",
    memory="Text and JSON preview already have 19 passing tests. Add Markdown without changing their behaviour. This is isolated trial work, not a Seinn task.",
    evidence=[str(relative / name) for name in ("pickup_preview.py", "test_pickup_preview.py", "USAGE.md")],
    failures={"M3": 1}, pending_jobs=[])
roll.connection().save(folder / "place.json", state)
print(json.dumps({"project": str(root), "files": [str(path.relative_to(root)) for path in sorted(folder.iterdir())]}))
