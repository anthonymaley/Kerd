#!/usr/bin/env python3
"""Real managed-source save failure/retry in disposable local Git repositories."""
import argparse
import json
from pathlib import Path
import shutil
import sys

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import codex_roll
import handoff
import managed_to
import roll


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True)
    args = parser.parse_args()
    folder = Path(args.folder).resolve()
    if not folder.is_dir() or any(folder.iterdir()):
        raise ValueError("Use an existing empty disposable directory")
    source, dest, remote = [folder / x for x in ("source", "destination", "remote.git")]
    branch = "failed-save-trial"
    transport = roll.connection()
    events = []
    def event(name, **data):
        events.append(dict(event=name, at=transport.now(), **data))
        transport.save(folder / "events.json", events)
        print(json.dumps(events[-1]), flush=True)
    handoff.git(folder, "init", "--bare", "-q", str(remote))
    handoff.git(folder, "init", "-q", "-b", branch, str(source))
    for key, value in (("user.name", "Isolated Switch Trial"), ("user.email", "trial@example.invalid"),
                       ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
        handoff.git(source, "config", key, value)
    for name in ("pickup_preview.py", "test_pickup_preview.py", "USAGE.md", "example.json"):
        shutil.copyfile(Path(__file__).with_name("seed") / name, source / name)
    shutil.copyfile(Path(__file__).with_name("agreement.md"), source / "agreement.md")
    (source / ".gitignore").write_text("__pycache__/\n")
    initial = dict(status="continue", next_action="Improve escaping then freeze before tests and usage",
        memory="Follow agreement.md. M3=1 is seeded history, not a newly failed attempt.",
        evidence=["agreement.md"], failures={"M3": 1}, pending_jobs=[])
    transport.save(source / "place.json", initial)
    handoff.git(source, "add", ".")
    handoff.git(source, "commit", "-qm", "Initialize bounded label improvement")
    initial_commit = handoff.git(source, "rev-parse", "HEAD")
    handoff.git(source, "remote", "add", "origin", str(remote))
    handoff.git(source, "push", "-qu", "origin", branch)
    handoff.git(folder, "clone", "-q", "--branch", branch, str(remote), str(dest))
    protected = {name: (source / name).read_bytes() for name in ("agreement.md", "example.json", ".gitignore")}
    bridge = codex_roll.AppServerBridge(source, transport)
    prompt = "Read agreement.md and the existing deliverables. Complete only the source piece, then return the exact unfinished saved-place JSON.\n" + json.dumps(initial)
    transport.save(folder / "source-prompt.json", {"prompt": prompt})
    try:
        event("source_start")
        src = bridge.run("codex", prompt, "Implement label improvement and freeze", "source", "source-1",
                         writable=True, model="gpt-5.6-sol", effort="high", hold=True)
        if src.get("phase") != "held" or handoff.git(source, "rev-parse", "HEAD") != initial_commit:
            raise RuntimeError("Source did not pause with unchanged Git history")
        if (source / "place.json").read_text() != json.dumps(initial, indent=2) + "\n":
            raise RuntimeError("Source rewrote the controller's saved place")
        identity = (src["process_id"], src["session_id"])
        event("source_held", **bridge.inspect_held())
        transfer = managed_to.ManagedTo(bridge, branch, "place.json", initial,
            ["pickup_preview.py", "place.json"], "Save label improvement before tests", protected)
        # Fail only the push route; no change to fetch, authority or actual work.
        handoff.git(source, "remote", "set-url", "--push", "origin", str(folder / "unavailable.git"))
        try:
            transfer.save_and_release()
        except handoff.HandoffError as exc:
            event("save_failed", reason=str(exc), **bridge.inspect_held())
        else:
            raise RuntimeError("Failure injection did not fail")
        try:
            transfer.prepare_destination(dest, files=["agreement.md"])
        except handoff.HandoffError:
            event("destination_blocked", destination_started=False)
        else:
            raise RuntimeError("Destination admitted after failed save")
        retained = bridge.held_result()
        if (retained["process_id"], retained["session_id"]) != identity:
            raise RuntimeError("Source identity changed during failed save")
        # No model rerun, no manual user go-ahead. Repair only the injected fault.
        failed_commit = handoff.git(source, "rev-parse", "HEAD")
        handoff.git(source, "remote", "set-url", "--push", "origin", str(remote))
        event("same_source_before_retry", same_process_and_thread=True, **bridge.inspect_held())
        receipt = transfer.save_and_release()
        if receipt["commit"] != failed_commit:
            raise RuntimeError("Retry unexpectedly created another work commit")
        event("save_verified_and_source_released", commit=receipt["commit"], owned_children_gone=transfer.result["owned_children_gone"])
        bridge.close("source")
        packet = transfer.prepare_destination(dest, files=["agreement.md"])
        frozen = (dest / "place.json").read_bytes()
        before = json.loads(frozen)
        prompt = "Continue the supplied exact working place under agreement.md. Source is verified stopped. Finish the missing tests and usage, run tests, correct supported defects, and return review when genuinely ready. No routine user go-ahead is needed.\n" + json.dumps(packet)
        transport.save(folder / "destination-prompt.json", {"prompt": prompt})
        event("destination_start", exact_saved_revision=True)
        other = codex_roll.AppServerBridge(dest, transport)
        dst = other.run("codex", prompt, "Complete and verify handed-off label improvement", "destination", "destination-1",
                        writable=True, model="gpt-5.6-sol", effort="high")
        if dst.get("status") != "completed" or not dst.get("owned_children_gone") or not roll.group_gone(dst):
            raise RuntimeError("Destination did not complete with verified cleanup")
        other.close("destination")
        after = before
        for candidate in dst.get("checkpoint_candidates") or [dst["reply"]]:
            parsed = roll.parse_reply(candidate)
            if parsed != after:
                after = roll.check_state(parsed, dest, after)
        if after["status"] != "review" or dst["session_id"] == identity[1]:
            raise RuntimeError("Distinct fresh destination did not reach review")
        if handoff.git(dest, "rev-parse", "HEAD") != receipt["commit"] or (dest / "place.json").read_bytes() != frozen:
            raise RuntimeError("Destination changed history or saved place")
        if any((dest / name).read_bytes() != content for name, content in protected.items()):
            raise RuntimeError("Destination changed protected inputs")
        for label, result in (("source", transfer.result), ("destination", dst)):
            transport.save(folder / (label + "-result.json"), {key: result.get(key) for key in
                ("status", "phase", "model", "started_at", "held_at", "finished_at", "context_readings", "owned_children_gone", "reply", "error", "cleanup_error")})
        event("destination_ready_for_review", fresh_thread=True, failure_count_preserved=after["failures"].get("M3", 0) >= 1)
    except BaseException:
        # Disposable trial teardown is explicitly abandonment, never a successful To.
        if bridge._held is not None:
            event("trial_abandoned", reason="Unexpected trial failure; no handoff pass")
            bridge.release_held(abandon=True)
        raise


if __name__ == "__main__":
    main()
