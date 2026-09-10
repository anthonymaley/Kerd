#!/usr/bin/env python3
"""Roll a managed build through fresh CLI runs. No transcript resume or live TUI control."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid


def connection():
    path = Path(__file__).resolve().parents[2] / "conductor/scripts/ask.py"
    spec = importlib.util.spec_from_file_location("kerd_roll_connection", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RollError(Exception):
    pass


def project_file(root, value):
    path = (root / value).resolve()
    if path == root or not path.is_relative_to(root) or ".git" in path.relative_to(root).parts:
        raise RollError("Work files must stay inside the project, outside Git metadata")
    if not path.is_file():
        raise RollError(f"Missing work file: {value}")
    return path


def check_state(state, root, previous=None):
    if not isinstance(state, dict):
        raise RollError("Saved place must be a JSON object")
    if state.get("status") not in {"continue", "review", "blocked"}:
        raise RollError("Saved place must be continue, review or blocked")
    for key in ("next_action", "memory"):
        if not isinstance(state.get(key), str) or not state[key].strip():
            raise RollError(f"Saved place needs {key}")
    if not isinstance(state.get("evidence"), list) or any(not isinstance(p, str) for p in state["evidence"]):
        raise RollError("Evidence must list actual project files")
    resolved = set()
    for path in state["evidence"]:
        actual = project_file(root, path)
        if actual in resolved:
            raise RollError("Evidence paths must be unique, including resolved aliases")
        resolved.add(actual)
    if not isinstance(state.get("pending_jobs"), list):
        raise RollError("Saved place needs pending_jobs, empty only when none exist")
    if state["pending_jobs"] and state["status"] != "blocked":
        raise RollError("Pending jobs need reconciliation before another fresh run")
    failures = state.get("failures")
    if not isinstance(failures, dict) or any(
        not isinstance(k, str) or type(v) is not int or v < 0 for k, v in failures.items()
    ):
        raise RollError("Failure counts must be nonnegative integers by measure")
    if state["status"] == "continue" and any(n >= 3 for n in failures.values()):
        raise RollError("Three failed corrections require Conductor reassessment")
    if previous:
        for key, count in previous["failures"].items():
            if failures.get(key, -1) < count:
                raise RollError("A fresh context must not erase failure counts")
        if not set(previous["evidence"]).issubset(state["evidence"]):
            raise RollError("Keep existing evidence references when adding the next result")
        if state == previous:
            raise RollError("No change in saved place; refusing an unchanged loop")
    return state


def parse_reply(reply):
    text = reply.strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise RollError("Worker did not return an unambiguous saved place") from exc


def prepare_prompt(agreement, state, target, context_aware=False):
    instruction = """Continue this agreed build from the saved place below. This is a fresh
context, not a new assignment. Do one useful bounded piece of the next action,
then freeze at a safe boundary. Choose the method. Do not replay completed work.
Use only the project files needed for that action; do not inspect native session
history, .git/cross-llm logs, or unrelated archives to reconstruct a transcript.
Do not modify the agreement or saved-place file; the caller saves your response.
Do not launch background processes, other agents, network calls, commits or pushes.
Preserve outstanding decisions, failure counts, constraints and cumulative evidence.
The agreement remains authoritative, including its limits and stopping condition.
Return ONLY a JSON object with these fields:
status: 'continue' for another useful piece, 'review' when ready for independent
assessment (not an assertion of acceptance), or 'blocked' for a genuine blocker;
next_action: the exact next action or review/blocker needed;
memory: concise useful working context, decisions and findings for the next run;
evidence: cumulative relative paths to actual result/evidence files;
failures: cumulative failed-correction counts by measure (preserve existing keys);
pending_jobs: [] only if no jobs remain. Any unresolved job means blocked.
Do not invent test results. Tools unavailable to this run are an explicit limit,
not a reason to declare an unchecked result verified.
"""
    if context_aware:
        instruction = instruction.replace(
            "Do one useful bounded piece of the next action,\nthen freeze at a safe boundary. Choose the method.",
            "Continue useful work toward the agreed outcome. Choose the method.\n"
            "The controller observes context usage and may ask you to Roll. On that\n"
            "request, finish the current safe operation and return your saved place.\n"
            "You may also return early at a genuine blocker or a useful safe boundary.\n"
            "Do not manufacture pieces or extra work to force a transition.")
    payload = json.dumps(state, ensure_ascii=False, indent=2)
    if target == "claude":
        return f"{instruction}\n<agreement>\n{agreement}\n</agreement>\n<saved_place>\n{payload}\n</saved_place>"
    return f"{instruction}\n# Agreed work\n{agreement}\n# Saved place\n{payload}\n"


def group_gone(result):
    if result.get("cleanup_warning") or result.get("cleanup_error"):
        return False
    pid = result.get("process_id")
    if not isinstance(pid, int) or pid <= 1:
        return False
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    return False


class Roller:
    def __init__(self, project, agreement, place, target, model, effort, bridge=None):
        self.transport = connection()
        self.bridge = bridge or self.transport.Bridge(project)
        self.root = self.bridge.root
        self.agreement = project_file(self.root, agreement)
        self.place = project_file(self.root, place)
        if self.agreement == self.place:
            raise RollError("Agreement and saved place must be separate files")
        self.target, self.model, self.effort = target, model, effort
        self.local = self.bridge.state.parent / "roll"
        self.local.mkdir(mode=0o700, exist_ok=True)
        self.ledger = self.local / "run.json"

    def artifact_snapshot(self, state):
        snapshot = {}
        for value in state["evidence"]:
            path = project_file(self.root, value)
            if path in {self.agreement, self.place}:
                raise RollError("Agreement or saved place cannot count as build evidence")
            # Local progress identity only, not a requirement fingerprint or approval.
            snapshot[str(path.relative_to(self.root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        return snapshot

    def recover(self, prepared_state, reason):
        """Explicit Conductor recovery after inspection; never a blind rerun."""
        if not isinstance(reason, str) or not reason.strip():
            raise RollError("Recovery requires the inspected cause and disposition of jobs")
        with self.transport.exclusive(self.local / "owner.lock"):
            prior = self.transport.read(self.ledger)
            if not prior or prior.get("status") not in {"uncertain", "failed"}:
                raise RollError("Only an inspected failed/uncertain Roll can be recovered")
            if any(prior.get(k) != str(v.relative_to(self.root)) for k, v in
                   (("agreement", self.agreement), ("place", self.place))):
                raise RollError("Recovery record belongs to different work")
            request = prior.get("request_id")
            result = self.transport.read(self.bridge.state / "requests" / str(request) / "result.json")
            if not result or result.get("status") not in {"abandoned", "failed", "cancelled", "timed_out", "completed"}:
                raise RollError("Resolve the retained provider request before preparing continuation")
            if result.get("project") != str(self.root) or result.get("request_id") != request:
                raise RollError("Retained provider result belongs to different work")
            pid = result.get("process_id")
            if type(pid) is not int or pid <= 1:
                raise RollError("Missing provider identity; no safe automatic recovery")
            try:
                os.killpg(pid, 0)
            except ProcessLookupError:
                pass
            else:
                raise RollError("Prior provider group still exists; no recovery or dispatch")
            if result.get("route") == "app-server-stdio" and not result.get("owned_children_gone"):
                from codex_roll import children_gone
                identities = result.get("owned_children")
                if not isinstance(identities, dict) or not children_gone(identities):
                    raise RollError("Owned child shutdown remains uncertain; inspect before recovery")
            old_state = check_state(json.loads(self.place.read_text()), self.root)
            state = check_state(json.loads(project_file(self.root, prepared_state).read_text()), self.root, old_state)
            self.artifact_snapshot(state)
            recoveries = prior.get("recoveries", [])
            recoveries.append({"at": self.transport.now(), "reason": reason,
                               "request_id": request, "previous_status": prior["status"],
                               "previous_error": prior.get("error"), "previous_place": old_state})
            # Preserve the before-image while still refusing dispatch, before changing place.
            prior["recoveries"] = recoveries
            self.transport.save(self.ledger, prior)
            self.transport.save(self.place, state)
            if json.loads(self.place.read_text()) != state:
                raise RollError("Recovered place failed read-back verification")
            retired = prior.get("retired_sessions", [])
            if result.get("session_id") and result["session_id"] not in retired:
                retired.append(result["session_id"])
            prior.update(status="paused", next_action=state["next_action"], recoveries=recoveries,
                         retired_sessions=retired)
            self.transport.save(self.ledger, prior)
            return {"status": "paused", "next_action": state["next_action"],
                    "note": "Inspected recovery saved; original request and error retained, no job launched"}

    def run(self, max_runs=None, timeout=None, control=None):
        if max_runs is not None and (type(max_runs) is not int or max_runs <= 0):
            raise RollError("Optional max-runs must be a positive integer")
        if control is not None and not getattr(self.bridge, "context_aware", False):
            raise RollError("Live control requires the held-source Codex adapter")
        with self.transport.exclusive(self.local / "owner.lock"):
            prior = self.transport.read(self.ledger)
            if prior and prior.get("status") in {"running", "uncertain", "failed"}:
                raise RollError("Previous Roll needs inspection; no automatic rerun of uncertain work")
            if prior and prior.get("status") in {"handed_off", "awaiting_destination"}:
                raise RollError("This source relinquished the work; continue at its recorded destination")
            frozen_agreement = self.agreement.read_text()
            frozen_agreement_bytes = self.agreement.read_bytes()
            state = check_state(json.loads(self.place.read_text()), self.root)
            baseline = self.artifact_snapshot(state)
            if prior and any(prior.get(k) != str(v.relative_to(self.root))
                             for k, v in (("agreement", self.agreement), ("place", self.place))
                             if k in prior):
                raise RollError("Local Roll record belongs to different work; inspect before changing owner")
            if state["status"] != "continue":
                return {"status": state["status"], "next_action": state["next_action"], "runs": 0}
            history = prior.get("history", []) if prior else []
            known_sessions = {item["session_id"] for item in history}
            known_sessions.update(prior.get("retired_sessions", []) if prior else [])
            snapshots = list(prior.get("artifact_snapshots", [])) if prior else []
            if baseline not in snapshots:
                snapshots.append(baseline)
            turns = 0
            record = {"status": "running", "history": history,
                      "recoveries": prior.get("recoveries", []) if prior else [],
                      "retired_sessions": prior.get("retired_sessions", []) if prior else [],
                      "artifact_snapshots": snapshots,
                      "agreement": str(self.agreement.relative_to(self.root)),
                      "place": str(self.place.relative_to(self.root)),
                      "target": self.target, "requested_model": self.model,
                      "requested_effort": self.effort}
            try:
                while state["status"] == "continue":
                    if control is not None:
                        control.ensure_connected()
                    if max_runs is not None and turns >= max_runs:
                        record.update(status="paused", next_action=state["next_action"])
                        self.transport.save(self.ledger, record)
                        return record
                    if self.agreement.read_text() != frozen_agreement:
                        raise RollError("Agreement changed; do not continue under stale authority")
                    place_before = self.place.read_bytes()
                    if control is not None:
                        from handoff import git
                        before_commit = git(self.root, "rev-parse", "HEAD")
                    prompt = prepare_prompt(frozen_agreement, state, self.target,
                                            context_aware=getattr(self.bridge, "context_aware", False))
                    alias = "roll-" + uuid.uuid4().hex
                    record.update(status="running", request_id=alias, next_action=state["next_action"])
                    self.transport.save(self.ledger, record)
                    print(json.dumps({"status": "working", "run": len(history) + 1,
                                      "next_action": state["next_action"]}), flush=True)
                    result = self.bridge.run(self.target, prompt, "Continue the agreed build through a fresh context",
                                             alias, alias, writable=True, model=self.model,
                                             effort=self.effort, timeout=timeout,
                                             **({"hold": True, "checkpoint_requested": control.checkpoint_requested.is_set}
                                                if control is not None else {}))
                    held = control is not None and result.get("status") == "running" and result.get("phase") == "held"
                    if not held and (result.get("status") != "completed" or not group_gone(result)):
                        raise RollError("Provider did not finish cleanly; inspect the retained request before recovery")
                    sid = result.get("session_id")
                    if not sid or sid in known_sessions:
                        raise RollError("Fresh session identity was not established")
                    if self.agreement.read_text() != frozen_agreement or self.place.read_bytes() != place_before:
                        raise RollError("Worker changed protected agreement or saved place; inspect before continuing")
                    if control is not None and (git(self.root, "rev-parse", "HEAD") != before_commit
                                               or self.agreement.read_bytes() != frozen_agreement_bytes):
                        raise RollError("Worker changed Git history or protected agreement bytes")
                    request = control.boundary() if control is not None else None
                    next_state = state
                    for reply in result.get("checkpoint_candidates", [result["reply"]]):
                        candidate = parse_reply(reply)
                        if candidate != next_state:
                            next_state = check_state(candidate, self.root, next_state)
                    if next_state == state and request is None:
                        raise RollError("No change in saved place; refusing an unchanged loop")
                    # A changed sentence is not build progress: require changed result bytes.
                    snapshot = self.artifact_snapshot(next_state)
                    if request is None and next_state["status"] == "continue" and (not snapshot or snapshot in snapshots):
                        raise RollError("No new artifact evidence for continuation; return a review or blocker instead")
                    snapshots.append(snapshot)
                    moved = None
                    if control is not None:
                        if request is not None and next_state["status"] == "continue":
                            moved = control.handoff(self, state, frozen_agreement_bytes, record)
                            result = control.released_result
                        elif request is not None:
                            control.emit({"status": "handoff_not_performed", "note": "Worker reached review or a blocker; returned to Conductor without starting a destination"})
                    if moved is None:
                        self.transport.save(self.place, next_state)
                    if json.loads(self.place.read_text()) != next_state:
                        raise RollError("Saved place failed read-back verification")
                    if held and moved is None:
                        control.ensure_connected()
                        result = self.bridge.release_held()
                    if result.get("status") != "completed" or not group_gone(result):
                        raise RollError("Source release is uncertain; no continuation")
                    known_sessions.add(sid)
                    history.append({"session_id": sid, "request_id": alias,
                                    "status": next_state["status"], "usage": result.get("usage"),
                                    "model": result.get("model"), "prompt_bytes": len(prompt.encode()),
                                    "context_readings": result.get("context_readings"),
                                    "context_trigger": result.get("context_trigger"),
                                    "route": result.get("route", "cli"),
                                    "estimated_cost_usd": result.get("estimated_cost_usd")})
                    self.bridge.close(alias)
                    state = next_state
                    turns += 1
                    record.update(status=state["status"], next_action=state["next_action"])
                    if moved is not None:
                        record.update(status="awaiting_destination" if moved.get("pickup") == "on_destination" else "handed_off", handoff=moved)
                    self.transport.save(self.ledger, record)
                    print(json.dumps({"status": "saved", "run": len(history),
                                      "next": state["status"], "next_action": state["next_action"]}), flush=True)
                    if moved is not None:
                        return record
                return record
            except BaseException as exc:
                if control is not None and getattr(self.bridge, "_held", None) is not None:
                    from roll_control import ControlEnded
                    try:
                        if not isinstance(exc, (ControlEnded, KeyboardInterrupt, BrokenPipeError)):
                            control.wait_for_recovery(exc, retry=False)
                    except (ControlEnded, KeyboardInterrupt, BrokenPipeError):
                        pass
                    # Only explicit abandonment, cancellation or loss of the caller
                    # channel reaches here; a save failure alone stays held above.
                    self.bridge.release_held(abandon=True)
                record.update(status="uncertain", error=str(exc))
                self.transport.save(self.ledger, record)
                raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--agreement", required=True, help="Existing project-relative agreed-work file")
    parser.add_argument("--place", required=True, help="Existing project-relative saved-place JSON")
    parser.add_argument("--target", choices=["codex", "claude"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--max-runs", type=int, help="Optional invocation limit; no limit by default")
    parser.add_argument("--timeout", type=float, help="Optional timeout per run")
    parser.add_argument("--context-aware", action="store_true", help="Use observed Codex context usage via local stdio")
    parser.add_argument("--control", action="store_true", help="Accept live Conductor commands on stdin; keep this command channel open")
    parser.add_argument("--context-fraction", type=float, default=0.65, help="Roll request threshold; leave room to save")
    parser.add_argument("--test-roll-at-tokens", type=int, help="Explicit lower threshold for exercising the mechanism, not a production context limit")
    parser.add_argument("--recover-state", help="Explicit inspected recovery from a prepared project-relative saved place")
    parser.add_argument("--recovery-reason", help="Inspected cause, artifact state and disposition of outstanding jobs")
    args = parser.parse_args()
    try:
        bridge = None
        if args.context_aware:
            if args.target != "codex":
                raise RollError("Observed-pressure Roll currently supports Codex only; Claude remains on bounded CLI pieces")
            from codex_roll import AppServerBridge
            bridge = AppServerBridge(args.project, connection(), args.context_fraction, args.test_roll_at_tokens)
        elif args.test_roll_at_tokens is not None:
            raise RollError("A test context trigger requires --context-aware")
        roller = Roller(args.project, args.agreement, args.place, args.target, args.model, args.effort, bridge=bridge)
        if args.control:
            if not args.context_aware or args.recover_state:
                raise RollError("Live control requires --context-aware and cannot be combined with recovery")
            from roll_control import LiveControl
            control = LiveControl()
            control.start()
            with roller.transport.shutdown_signals():
                result = roller.run(args.max_runs, args.timeout, control=control)
        else:
            result = (roller.recover(args.recover_state, args.recovery_reason) if args.recover_state
                      else roller.run(args.max_runs, args.timeout))
        # Do not leak private native session identifiers into user/shared summaries.
        print(json.dumps({k: v for k, v in result.items() if k not in {"history", "request_id", "artifact_snapshots", "recoveries", "retired_sessions"}}, indent=2))
        return 0 if result["status"] in {"review", "paused", "handed_off", "awaiting_destination"} else 1
    except (RollError, ValueError, OSError, subprocess.SubprocessError, RuntimeError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
