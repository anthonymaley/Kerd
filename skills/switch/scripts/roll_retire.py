#!/usr/bin/env python3
"""Retire a finished worker Roll record while holding the owner lock.

Takes `roll/owner.lock` (non-blocking), re-reads `roll/run.json` and its saved place, and moves
the record to a dated `retired-…json` beside it only when it is a worker record in `review` or
`blocked` with no pending job. Never deletes. Running, uncertain and failed records go through
recovery instead; a managed Conductor record is refused.
"""
import argparse
from datetime import date
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roll  # noqa: E402


def roll_dir(project):
    out = subprocess.run(["git", "rev-parse", "--git-path", "roll"], cwd=project,
                         capture_output=True, text=True, check=True).stdout.strip()
    path = Path(out)
    return path if path.is_absolute() else Path(project) / path


def retire(project, label="worker", today=None):
    project = Path(project).resolve()
    local = roll_dir(project)
    ledger = local / "run.json"
    if not ledger.is_file():
        raise roll.RollError("No Roll record to retire")
    transport = roll.connection()
    try:
        with transport.exclusive(local / "owner.lock"):
            record = json.loads(ledger.read_text())
            if record.get("kind") == "conductor":
                raise roll.RollError("Managed Conductor record; inspect and retire it through its own guide")
            if record.get("status") not in {"review", "blocked"}:
                raise roll.RollError(f"Record is {record.get('status')!r}; only review or blocked retire, others go through recovery")
            place = record.get("place")
            if not isinstance(place, str) or not place.strip():
                raise roll.RollError("Record names no saved place; cannot show that no job is pending")
            state = json.loads(roll.project_file(project, place).read_text())
            if not isinstance(state, dict) or not isinstance(state.get("pending_jobs"), list):
                raise roll.RollError("Saved place has no pending_jobs list; cannot show that no job is pending")
            if state["pending_jobs"]:
                raise roll.RollError("Saved place still lists pending jobs; reconcile them first")
            stamp = (today or date.today()).isoformat()
            safe = "".join(c for c in label if c.isalnum() or c == "-") or "worker"
            target = local / f"retired-{stamp}-{safe}-run.json"
            n = 2
            while target.exists():
                target = local / f"retired-{stamp}-{safe}-{n}-run.json"
                n += 1
            os.rename(ledger, target)
            return target
    except transport.Busy:
        raise roll.RollError("Owner lock is held: a Roll is running; nothing retired") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--label", default="worker", help="Short word for the retired file name")
    args = parser.parse_args()
    try:
        target = retire(args.project, args.label)
    except (roll.RollError, OSError, ValueError) as exc:
        print(f"Not retired: {exc}", file=sys.stderr)
        return 1
    print(f"Retired: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
