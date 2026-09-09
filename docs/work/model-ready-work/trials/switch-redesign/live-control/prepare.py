#!/usr/bin/env python3
"""Prepare isolated inputs; execution must use the actual live Roll CLI channel."""
import json
from pathlib import Path
import shutil
import sys
import tempfile

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import handoff
import roll


def main():
    folder = Path(tempfile.mkdtemp(prefix="kerd-live-control-")).resolve()
    source, destination, remote = [folder / name for name in ("source", "destination", "remote.git")]
    branch = "live-control-trial"
    handoff.git(folder, "init", "--bare", "-q", str(remote))
    handoff.git(folder, "init", "-q", "-b", branch, str(source))
    for key, value in (("user.name", "Isolated Switch Trial"), ("user.email", "trial@example.invalid"),
                       ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
        handoff.git(source, "config", key, value)
    seed = Path(__file__).resolve().parents[1] / "failed-save/output"
    for name in ("pickup_preview.py", "test_pickup_preview.py", "USAGE.md", "example.json"):
        shutil.copyfile(seed / name, source / name)
    shutil.copyfile(Path(__file__).with_name("agreement.md"), source / "agreement.md")
    (source / ".gitignore").write_text("__pycache__/\n")
    state = dict(status="continue", next_action="Add and prove the machine-readable pickup preview",
                 memory="Existing privacy-conscious text preview has 13 tests. M3=1 is seeded history, not a new failure.",
                 evidence=["pickup_preview.py", "test_pickup_preview.py", "USAGE.md"],
                 failures={"M3": 1}, pending_jobs=[])
    roll.connection().save(source / "place.json", state)
    handoff.git(source, "add", ".")
    handoff.git(source, "commit", "-qm", "Prepare machine-readable preview trial")
    handoff.git(source, "remote", "add", "origin", str(remote))
    handoff.git(source, "push", "-qu", "origin", branch)
    handoff.git(folder, "clone", "-q", "--branch", branch, str(remote), str(destination))
    handoff.git(source, "remote", "set-url", "--push", "origin", str(folder / "unavailable.git"))
    result = dict(folder=str(folder), source=str(source), destination=str(destination), remote=str(remote),
                  initial_commit=handoff.git(source, "rev-parse", "HEAD"), branch=branch,
                  request=dict(action="to", branch=branch, destination=str(destination),
                               message="Save actual live-controller working place",
                               files=["place.json", "pickup_preview.py", "test_pickup_preview.py", "USAGE.md"]))
    roll.connection().save(folder / "fixture.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
