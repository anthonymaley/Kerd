#!/usr/bin/env python3
"""Collect the source receipt after release; never claims laptop execution."""
import argparse
import json
from pathlib import Path
import sys

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import handoff
import roll

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("project", type=Path)
args = parser.parse_args()
root = handoff.root_for(args.project)
ledger = json.loads((root / ".git/roll/run.json").read_text())
if ledger["status"] != "awaiting_destination" or len(ledger["history"]) != 1:
    raise ValueError("Source has not completed a single-worker other-device handoff")
record = ledger["history"][0]
folder = root / ".git/cross-llm/requests" / record["request_id"]
result = json.loads((folder / "result.json").read_text())
if result["status"] != "completed" or not result.get("owned_children_gone") or not roll.group_gone(result):
    raise ValueError("Source release not verified")
receipt = ledger["handoff"]["receipt"]
remote = handoff.git(root, "ls-remote", "--heads", "origin", f"refs/heads/{receipt['branch']}")
if remote.split()[0] != receipt["commit"] or handoff.git(root, "status", "--porcelain"):
    raise ValueError("Source or remote changed after release")
paths = handoff.git(root, "diff", "--name-only", "2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83", receipt["commit"]).splitlines()
if any(not path.startswith("docs/work/switch-trial/device-build/") for path in paths):
    raise ValueError("Changes escaped the authorized trial folder")
place = json.loads((root / ledger["place"]).read_text())
selected = {key: result.get(key) for key in ("status", "model", "started_at", "held_at", "finished_at",
    "checkpoint_requested", "steer_accepted", "owned_children_gone", "reply", "error", "cleanup_error")}
output = dict(source_machine="AnthonyacStudio", source_project=str(root), handoff=ledger["handoff"],
    source=selected, state=place, changed_files=paths, laptop_started=False,
    laptop_reported_before={"project": "/Users/anthonymaley/seinn-test", "clean": True,
        "branch": "kerd-switch-trial-20260906", "commit": "2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83",
        "origin": "git@github.com:anthonymaley/seinn.git"})
roll.connection().save(Path(__file__).with_name("source-observed.json"), output)
request = json.loads((folder / "request.json").read_text())
Path(__file__).with_name("source-prompt.md").write_text(request["prompt"])
print(json.dumps({"commit": receipt["commit"], "source_exited": True,
                  "laptop_started": False, "next_action": place["next_action"]}, indent=2))
