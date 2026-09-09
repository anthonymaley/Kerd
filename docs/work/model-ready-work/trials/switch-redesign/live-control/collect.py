#!/usr/bin/env python3
"""Collect selected proof after a real CLI-driven trial; never drives the handoff."""
import argparse
import json
from pathlib import Path
import shutil
import sys

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import handoff
import roll


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    folder = args.folder.resolve()
    fixture = json.loads((folder / "fixture.json").read_text())
    source, destination = (Path(fixture[name]) for name in ("source", "destination"))
    source_ledger = json.loads((source / ".git/roll/run.json").read_text())
    destination_ledger = json.loads((destination / ".git/roll/run.json").read_text())
    # Ledger filename is a private implementation detail, not a portable identity.
    if source_ledger["status"] != "handed_off" or destination_ledger["status"] != "review":
        raise ValueError("Actual source and destination have not reached their required states")
    source_history, destination_history = source_ledger["history"], destination_ledger["history"]
    if len(source_history) != 1 or not destination_history:
        raise ValueError("Unexpected worker history")
    if source_history[0]["session_id"] in {item["session_id"] for item in destination_history}:
        raise ValueError("Destination did not use a fresh session")
    receipt = source_ledger["handoff"]["receipt"]
    for root in (source, destination):
        if handoff.git(root, "rev-parse", "HEAD") != receipt["commit"]:
            raise ValueError("Trial history moved beyond the saved revision")
    for name in ("agreement.md", "example.json", ".gitignore"):
        if (source / name).read_bytes() != (destination / name).read_bytes():
            raise ValueError("Protected input differs")
    state = json.loads((destination / "place.json").read_text())
    if state["failures"].get("M3", 0) < 1 or state["pending_jobs"]:
        raise ValueError("Lost history or unresolved jobs")
    output = Path(__file__).with_name("output")
    output.mkdir(exist_ok=True)
    save = roll.connection().save
    for name in ("pickup_preview.py", "test_pickup_preview.py", "USAGE.md", "example.json"):
        shutil.copyfile(destination / name, output / name)
    summaries = []
    for label, root, history in (("source", source, source_history), ("destination", destination, destination_history)):
        for number, item in enumerate(history, 1):
            request_folder = root / ".git/cross-llm/requests" / item["request_id"]
            result = json.loads((request_folder / "result.json").read_text())
            request = json.loads((request_folder / "request.json").read_text())
            if result["status"] != "completed" or not result.get("owned_children_gone") or not roll.group_gone(result):
                raise ValueError("Owned source cleanup is not verified")
            selected = {key: result.get(key) for key in ("status", "phase", "model", "started_at", "held_at", "finished_at",
                "checkpoint_requested", "steer_accepted", "context_trigger", "context_readings", "owned_children_gone", "reply", "error", "cleanup_error")}
            selected["effort"] = request["effort"]
            selected["label"] = f"{label}-{number}"
            summaries.append(selected)
            (Path(__file__).parent / f"{label}-{number}-prompt.md").write_text(request["prompt"])
    save(Path(__file__).with_name("observed.json"), dict(
        fixture=fixture, handoff=receipt, failures=source_ledger.get("handoff_failures", []),
        fresh_destination=True, seeded_failure_preserved=True, source_workers=len(source_history),
        destination_workers=len(destination_history), final_state=state, workers=summaries))
    review_path = destination / ".git/cross-llm/requests/live-control-artifact-review-1/result.json"
    if review_path.is_file():
        review = json.loads(review_path.read_text())
        save(Path(__file__).with_name("review-observed.json"), {key: review.get(key) for key in
             ("status", "model", "requested_effort", "started_at", "finished_at", "reply", "exit_code")})
        (Path(__file__).parent / "review-artifact.md").write_text(review["reply"] + "\n")
    followup_path = destination / ".git/cross-llm/requests/live-control-artifact-review-2/result.json"
    if followup_path.is_file():
        followup = json.loads(followup_path.read_text())
        save(Path(__file__).with_name("review-followup-observed.json"), {key: followup.get(key) for key in
             ("status", "model", "requested_effort", "started_at", "finished_at", "reply", "exit_code")})
        (Path(__file__).parent / "review-followup.md").write_text(followup["reply"] + "\n")
    print(json.dumps({"saved": str(Path(__file__).parent), "fresh_destination": True,
                      "source_workers": len(source_history), "destination_workers": len(destination_history)}))


if __name__ == "__main__":
    main()
