#!/usr/bin/env python3
"""One disposable local active-handoff rehearsal; not a production To controller."""
import argparse
import json
from pathlib import Path
import shutil
import sys

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import codex_roll
import handoff
import roll


def require_release(result):
    if (result.get("status") != "completed" or result.get("cleanup_error")
            or result.get("owned_children_gone") is not True or not roll.group_gone(result)):
        raise RuntimeError("Source shutdown is not proved; destination must not start")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True, help="An existing empty disposable directory")
    args = parser.parse_args()
    folder = Path(args.folder).resolve()
    if not folder.is_dir() or any(folder.iterdir()):
        raise ValueError("Use a fresh empty disposable directory")
    transport = roll.connection()
    source, dest, remote = [folder / name for name in ("source", "destination", "remote.git")]
    branch = "active-handoff-trial"
    handoff.git(folder, "init", "--bare", "-q", str(remote))
    handoff.git(folder, "init", "-q", "-b", branch, str(source))
    for key, value in (("user.name", "Isolated Switch Trial"), ("user.email", "trial@example.invalid"),
                       ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
        handoff.git(source, "config", key, value)
    shutil.copyfile(Path(__file__).with_name("agreement.md"), source / "agreement.md")
    shutil.copyfile(PACK / "trials/switch-redesign/pickup-budget/prepared-packet.json", source / "example.json")
    handoff.git(source, "add", "--", "agreement.md", "example.json")
    handoff.git(source, "commit", "-qm", "Initialize isolated preview task")
    handoff.git(source, "remote", "add", "origin", str(remote))
    handoff.git(source, "push", "-qu", "origin", branch)
    handoff.git(folder, "clone", "-q", "--branch", branch, str(remote), str(dest))
    agreement = (source / "agreement.md").read_bytes()
    example = (source / "example.json").read_bytes()
    events = []

    def event(name, **data):
        events.append({"event": name, "at": transport.now(), **data})
        transport.save(folder / "events.json", events)
        print(json.dumps(events[-1]), flush=True)

    initial = {"status": "continue", "next_action": "Implement the preview CLI, then freeze before adding tests or usage.",
               "memory": "A deliberate mid-work handoff test. No output exists yet. M3=1 is a seeded historical test count, not a new failed implementation.",
               "evidence": ["agreement.md", "example.json"], "failures": {"M3": 1}, "pending_jobs": []}
    base_prompt = "Follow agreement.md. Return only the saved-place JSON it specifies.\n"
    source_prompt = base_prompt + "Implement pickup_preview.py, then freeze for a planned handoff before writing tests/usage. This is a useful unfinished checkpoint, not completion.\n" + json.dumps(initial)
    transport.save(folder / "source-prompt.json", {"prompt": source_prompt})
    original_server = codex_roll.AppServer
    saved = {}

    class SaveBeforeShutdown(original_server):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self.turn = None
            self.thread = None
            self.replies = {}

        def receive(self, *a, **kw):
            message = super().receive(*a, **kw)
            method, params = message.get("method"), message.get("params", {})
            if method == "turn/started":
                if self.turn is not None:
                    raise RuntimeError("Unexpected second source turn")
                self.turn, self.thread = params["turn"]["id"], params["threadId"]
            elif method == "item/completed":
                item = params.get("item", {})
                if item.get("type") == "agentMessage" and item.get("phase") != "commentary":
                    if params.get("turnId") != self.turn or params.get("threadId") != self.thread:
                        raise RuntimeError("Foreign source reply")
                    self.replies[item["id"]] = item.get("text", "")
            elif method == "turn/completed":
                if (params.get("threadId") != self.thread or params["turn"]["id"] != self.turn
                        or params["turn"]["status"] != "completed" or len(self.replies) != 1):
                    raise RuntimeError("Uncertain source turn; no handoff save")
                place = roll.check_state(roll.parse_reply(next(iter(self.replies.values()))), source, initial)
                if place["status"] != "continue":
                    raise RuntimeError("Source did not leave a valid unfinished place")
                if (source / "agreement.md").read_bytes() != agreement or (source / "example.json").read_bytes() != example:
                    raise RuntimeError("Source changed protected inputs")
                transport.save(source / "handoff.json", place)
                event("source_checkpoint_ready", source_parent_alive=self.proc.poll() is None)
                saved.update(handoff.publish(source, branch, ["pickup_preview.py", "handoff.json"],
                                              "Save unfinished preview and exact working place", push=True))
                event("remote_save_verified", commit=saved["commit"], source_parent_alive=self.proc.poll() is None)
                if self.proc.poll() is not None:
                    raise RuntimeError("Source already exited before verified save")
            return message

    try:
        codex_roll.AppServer = SaveBeforeShutdown
        bridge = codex_roll.AppServerBridge(source, transport)
        src = bridge.run("codex", source_prompt, "Source piece and exact handoff", "source", "source-1",
                         writable=True, model="gpt-5.6-sol", effort="high")
    finally:
        codex_roll.AppServer = original_server
    require_release(src)
    if saved.get("status") != "saved_to_remote":
        raise RuntimeError("No verified remote save; destination must not start")
    bridge.close("source")
    event("source_shutdown_confirmed")
    packet = handoff.prepare(dest, branch, "handoff.json", files=["agreement.md"], sync=True)
    if packet["commit"] != saved["commit"]:
        raise RuntimeError("Destination did not restore the exact saved revision")
    before = json.loads((dest / "handoff.json").read_text())
    destination_prompt = base_prompt + "Continue this active task from the supplied saved place and agreement. Finish the meaningful tests and usage, correct supported defects, run tests and return review when ready. No new user go-ahead is needed. The source is confirmed stopped. Do not edit handoff.json or the protected inputs.\n" + json.dumps(packet)
    transport.save(folder / "destination-prompt.json", {"prompt": destination_prompt})
    event("destination_start", commit=packet["commit"])
    other = codex_roll.AppServerBridge(dest, transport)
    dst = other.run("codex", destination_prompt, "Continue handed-off preview task", "destination", "destination-1",
                    writable=True, model="gpt-5.6-sol", effort="high")
    require_release(dst)
    other.close("destination")
    after = roll.check_state(roll.parse_reply(dst["reply"]), dest, before)
    if after["status"] != "review" or src["session_id"] == dst["session_id"]:
        raise RuntimeError("Distinct fresh destination did not reach review")
    if (dest / "agreement.md").read_bytes() != agreement or (dest / "example.json").read_bytes() != example:
        raise RuntimeError("Destination changed protected inputs")
    for label, result in (("source", src), ("destination", dst)):
        transport.save(folder / (label + "-result.json"), {k: result.get(k) for k in
            ("status", "model", "started_at", "finished_at", "context_readings", "owned_children_gone", "error", "cleanup_error", "reply")})
    event("destination_ready_for_review", fresh_session=True, failure_count_preserved=after["failures"].get("M3", 0) >= 1)


if __name__ == "__main__":
    main()
