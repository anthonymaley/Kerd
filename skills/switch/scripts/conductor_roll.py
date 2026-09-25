#!/usr/bin/env python3
"""Serial managed Conductor: fresh decision contexts, durable contributions.

No TUI takeover, no daemon, no automatic recovery of uncertain dispatch.
"""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import uuid

import roll
from codex_roll import AppServerBridge


DECISION_GUIDE = Path(__file__).resolve().parents[2] / "conductor/references/managed-decision.md"
CHECKPOINT = ("Finish the current read and return the decision JSON with action checkpoint. "
              "Preserve compact place, exact latest-contribution acknowledgement, decisions, "
              "open findings and failures. Do not dispatch or start more analysis.")


def fingerprint(root, excluded):
    """Tracked and nonignored untracked content; never follow a symlink outside root."""
    result = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                            cwd=root, capture_output=True, check=True)
    digest = hashlib.sha256()
    for raw in sorted(set(result.stdout.split(b"\0")) - {b""}):
        path = root / os.fsdecode(raw)
        if path in excluded:
            continue
        digest.update(raw + b"\0")
        if path.is_symlink():
            digest.update(b"link:" + os.fsencode(os.readlink(path)))
        elif path.is_file():
            digest.update(str(path.stat().st_mode).encode() + b":")
            with path.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(block)
        elif path.exists():
            raise roll.RollError("Unsupported nested worktree/submodule in review fingerprint")
        else:
            digest.update(b"missing")
        digest.update(b"\0")
    return digest.hexdigest()


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review_result(value):
    if (not isinstance(value, dict) or value.get("verdict") not in {"pass", "changes", "blocked"}
            or not isinstance(value.get("summary"), str) or not value["summary"].strip()
            or not isinstance(value.get("findings"), list)
            or any(not isinstance(f, str) or not f.strip() for f in value["findings"])):
        raise roll.RollError("Invalid independent review result")
    if (value["verdict"] == "pass" and value["findings"]) or (value["verdict"] == "changes" and not value["findings"]):
        raise roll.RollError("Review verdict contradicts its findings")
    return value


class ManagedConductor:
    def __init__(self, project, agreement, place, config, coordinator=None, reviewer=None):
        self.transport = roll.connection()
        self.coordinator = coordinator or AppServerBridge(project, self.transport)
        self.reviewer = reviewer or self.transport.Bridge(project)
        self.root = self.coordinator.root
        self.agreement = roll.project_file(self.root, agreement)
        self.place = roll.project_file(self.root, place)
        if self.agreement == self.place:
            raise roll.RollError("Agreement and place must be separate")
        required = {"coordinator_model", "coordinator_effort", "worker_model", "worker_effort",
                    "review_provider", "review_model", "review_effort"}
        if set(config) != required or any(not isinstance(v, str) or not v.strip() for v in config.values()):
            raise roll.RollError("Explicit coordinator, worker and reviewer model/effort required")
        if config["review_provider"] not in {"codex", "claude"}:
            raise roll.RollError("Unsupported review provider")
        self.config = config
        self.local = self.coordinator.state.parent / "roll"
        self.local.mkdir(mode=0o700, exist_ok=True)
        self.ledger = self.local / "run.json"

    def tree(self):
        return fingerprint(self.root, {self.place})

    def emit(self, status, **values):
        print(json.dumps({"controller": "conductor", "status": status, **values}), flush=True)

    def persist(self):
        self.transport.save(self.ledger, self.record)

    def save_place(self, value):
        self.transport.save(self.place, value)
        if json.loads(self.place.read_text()) != value:
            raise roll.RollError("Saved place read-back failed")
        self.record["place_digest"] = digest_file(self.place)
        self.record["next_action"] = value["next_action"]
        self.persist()

    def stopped(self):
        stop = self.transport.read(self.local / "stop.json")
        return bool(stop and stop.get("run_id") == self.record["run_id"]
                    and stop.get("request_id") != self.record.get("last_stop"))

    def receipt_value(self, receipt):
        path = self.coordinator.state / "requests" / receipt["request_id"] / "result.json"
        if receipt.get("digest") and digest_file(path) != receipt["digest"]:
            raise roll.RollError("Retained contribution changed after capture")
        result = self.transport.read(path)
        if not result or result.get("request_id") != receipt["request_id"] or result.get("project") != str(self.root):
            raise roll.RollError("Retained contribution is missing or belongs to different work")
        reply = result.get("reply")
        if not isinstance(reply, str) or len(reply.encode()) > 65536:
            raise roll.RollError("Contribution needs inspected compaction; refusing loss or oversized replay")
        return {**receipt, "reply": reply}

    def dispatch(self, kind, prompt, *, writable=False):
        decision = kind == "decision"
        review = kind == "review"
        provider = self.config["review_provider"] if review else "codex"
        prefix = "review" if review else "coordinator" if decision else "worker"
        model, effort = self.config[prefix + "_model"], self.config[prefix + "_effort"]
        bridge = self.reviewer if review else self.coordinator
        request_id = "conductor-" + uuid.uuid4().hex
        protected = (self.agreement.read_bytes(), self.place.read_bytes())
        before = self.tree()
        head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=self.root, capture_output=True).stdout
        index = subprocess.run(["git", "diff", "--cached", "--binary"], cwd=self.root, capture_output=True, check=True).stdout
        self.record.update(status="running", phase=kind, request_id=request_id,
                           pending={"request_id": request_id, "kind": kind,
                                    "result": f"requests/{request_id}/result.json"})
        self.persist()  # Write-ahead identity: never retry uncertain dispatch under a new ID.
        self.emit("dispatching", task=kind, route="fresh " + provider, model_requested=model,
                  effort_requested=effort, prompt_bytes=len(prompt.encode()))
        kwargs = {} if review else {"checkpoint_requested": self.stopped}
        if decision:
            kwargs["checkpoint_instruction"] = CHECKPOINT
        result = bridge.run(provider, prompt, "Managed Conductor " + kind, request_id, request_id,
                            writable=writable, model=model, effort=effort, timeout=self.timeout, **kwargs)
        if (result.get("status") != "completed" or not roll.group_gone(result)
                or (not review and result.get("owned_children_gone") is not True)):
            raise roll.RollError("Provider shutdown unverified; inspect retained request, never redispatch")
        if result.get("request_id") != request_id or result.get("project") != str(self.root):
            raise roll.RollError("Foreign provider result")
        sid = result.get("session_id")
        if not isinstance(sid, str) or not sid or sid in self.record["sessions"]:
            raise roll.RollError("Fresh provider identity not established")
        if protected != (self.agreement.read_bytes(), self.place.read_bytes()):
            raise roll.RollError("Job changed protected agreement or place")
        after = self.tree()
        if not writable and after != before:
            raise roll.RollError("Content changed during a read-only job (job or another editor); review is invalid")
        if (subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=self.root, capture_output=True).stdout != head
                or subprocess.run(["git", "diff", "--cached", "--binary"], cwd=self.root, capture_output=True, check=True).stdout != index):
            raise roll.RollError("Job changed Git history or staging")
        receipt = {"request_id": request_id, "kind": kind, "tree": after,
                   "digest": digest_file(self.coordinator.state / "requests" / request_id / "result.json"),
                   "capabilities": "file inspection only; no tests" if review and provider == "claude"
                   else "read-only inspection; no write-producing tests" if not writable else "local implementation and tests"}
        # Provider result.json is the receipt. Verify it before retiring the source alias.
        self.receipt_value(receipt)
        candidates = result.get("checkpoint_candidates", [result["reply"]])
        if not isinstance(candidates, list) or not candidates:
            raise roll.RollError("Missing checkpoint candidates")
        bridge.close(request_id)
        self.record["sessions"].append(sid)
        self.record["history"].append({**receipt, "status": "review" if review else "continue",
            "model_requested": model, "model_observed": result.get("model"), "effort_requested": effort,
            "prompt_bytes": len(prompt.encode()), "context_readings": result.get("context_readings"),
            "context_trigger": result.get("context_trigger")})
        if kind != "decision":
            receipt["validated"] = False
            self.record["contributions"].append(receipt)
        self.record["pending"] = None
        self.persist()
        self.emit("returned", task=kind)
        return receipt, [roll.parse_reply(candidate) for candidate in candidates]

    def check_decision(self, value, state, latest):
        if not isinstance(value, dict) or value.get("action") not in {"implement", "review", "checkpoint", "complete", "blocked"}:
            raise roll.RollError("Invalid Conductor decision")
        following = value.get("place")
        roll.check_state(following, self.root)
        if following != state:
            roll.check_state(following, self.root, state)
        if following["pending_jobs"]:
            raise roll.RollError("Conductor cannot leave unresolved jobs")
        if (value["action"] == "blocked") != (following["status"] == "blocked"):
            raise roll.RollError("Decision and saved place disagree about blocker")
        if value["action"] in {"implement", "review"} and (not isinstance(value.get("task"), str) or not value["task"].strip()):
            raise roll.RollError("Delegated task must retain outcome and boundaries")
        ack = value.get("ack")
        if latest:
            if (not isinstance(ack, dict) or ack.get("request_id") != latest["request_id"]
                    or not isinstance(ack.get("disposition"), str) or not ack["disposition"].strip()):
                raise roll.RollError("Conductor must acknowledge the exact latest contribution")
        elif ack is not None:
            raise roll.RollError("No contribution exists to acknowledge")
        return following

    def reject_findings(self, decisions):
        if not isinstance(decisions, list):
            raise roll.RollError("Finding rejections must be explicit records")
        for decision in decisions:
            if (not isinstance(decision, dict) or not isinstance(decision.get("reason"), str)
                    or not decision["reason"].strip() or not isinstance(decision.get("evidence"), list)
                    or not decision["evidence"] or any(not isinstance(p, str) for p in decision["evidence"])):
                raise roll.RollError("Rejecting a finding requires its ID, reason and actual evidence paths")
            for path in decision["evidence"]:
                roll.project_file(self.root, path)
            matches = [f for f in self.record["open_findings"] if f["id"] == decision.get("id")]
            if len(matches) != 1:
                raise roll.RollError("Finding rejection does not name one open finding")
            self.record["finding_dispositions"][decision["id"]] = {**decision, "finding": matches[0]}
            self.record["open_findings"].remove(matches[0])

    def run(self, max_cycles=None, timeout=None):
        if max_cycles is not None and (type(max_cycles) is not int or max_cycles <= 0):
            raise roll.RollError("Cycle limit must be positive")
        if timeout is not None and (not math.isfinite(timeout) or timeout <= 0):
            raise roll.RollError("Timeout must be positive and finite")
        self.timeout = timeout
        with self.transport.exclusive(self.local / "owner.lock"):
            if (self.local / "chat.json").exists():
                raise roll.RollError("A chat roll is waiting to be picked up here; claim or cancel it first")
            prior = self.transport.read(self.ledger)
            identity = dict(kind="conductor", agreement=str(self.agreement.relative_to(self.root)),
                            place=str(self.place.relative_to(self.root)), config=self.config)
            if prior and any(prior.get(k) != v for k, v in identity.items()):
                raise roll.RollError("Retained Roll belongs to different work or controller")
            if prior and prior.get("status") != "paused":
                raise roll.RollError("Retained Conductor needs inspection; only safe pauses resume automatically")
            if prior and (prior["agreement_digest"] != digest_file(self.agreement)
                          or prior["place_digest"] != digest_file(self.place) or prior.get("pending")):
                raise roll.RollError("Saved agreement/place changed or pending job requires inspection")
            state = roll.check_state(json.loads(self.place.read_text()), self.root)
            if state["pending_jobs"] or state["status"] == "blocked":
                raise roll.RollError("Resolve saved blocker/pending jobs before managed entry")
            self.record = prior or {**identity, "run_id": uuid.uuid4().hex, "status": "running",
                "agreement_digest": digest_file(self.agreement), "place_digest": digest_file(self.place),
                "next_action": state["next_action"], "history": [], "sessions": [], "contributions": [],
                "dispositions": {}, "finding_dispositions": {}, "open_findings": [], "review": None,
                "checkpoint_count": 0, "pending": None}
            self.record.setdefault("completion_refusals", [])
            self.record.setdefault("refusal_count", 0)
            agreement = self.agreement.read_text()
            cycles = 0
            try:
                while True:
                    if self.stopped() or (max_cycles is not None and cycles >= max_cycles):
                        if self.stopped():
                            self.record["last_stop"] = self.transport.read(self.local / "stop.json")["request_id"]
                        self.record.update(status="paused", phase="safe boundary")
                        self.persist()
                        return self.record
                    if digest_file(self.agreement) != self.record["agreement_digest"] or digest_file(self.place) != self.record["place_digest"]:
                        raise roll.RollError("Agreement/place changed between decisions")
                    latest = self.record["contributions"][-1] if self.record["contributions"] else None
                    payload = {"agreement": agreement, "place": state,
                               "latest_contribution": self.receipt_value(latest) if latest else None,
                               "open_findings": self.record["open_findings"],
                               "review_gate": {"verdict": self.record["review"]["verdict"] if self.record["review"] else None,
                                   "current_tree_reviewed": bool(self.record["review"] and self.record["review"]["verdict"] == "pass"
                                                                 and self.record["review"]["tree"] == self.tree()),
                                   "open_findings_count": len(self.record["open_findings"]),
                                   "refused_complete": self.record["completion_refusals"][-1]["reason"] if self.record["refusal_count"] else None,
                                   "rule": "After every implementation, request review again before complete. Builder review status is not a review receipt."},
                               "routes": self.config}
                    prompt = DECISION_GUIDE.read_text() + "\n# Current input\n" + json.dumps(payload, ensure_ascii=False)
                    decision_receipt, candidates = self.dispatch("decision", prompt)
                    prior_state = state
                    for value in candidates:
                        state = self.check_decision(value, state, latest)
                    action = value["action"]
                    before_decision = copy.deepcopy(self.record)
                    if latest:
                        dispositions = self.record["dispositions"].setdefault(latest["request_id"], [])
                        if value["ack"]["disposition"] not in dispositions:
                            dispositions.append(value["ack"]["disposition"])
                    self.reject_findings(value.get("reject_findings", []))
                    if action == "complete":
                        review = self.record["review"]
                        if not review or review["verdict"] != "pass" or review["tree"] != self.tree() or self.record["open_findings"]:
                            # Clean read-only decision, no dispatch: retry the judgment
                            # with explicit feedback, not a human ownership inspection.
                            state, self.record = prior_state, before_decision
                            reason = "Completion requires passing independent review of the current tree and resolved findings"
                            self.record["completion_refusals"].append({"request_id": decision_receipt["request_id"], "reason": reason})
                            self.record["refusal_count"] += 1
                            cycles += 1
                            if self.record["refusal_count"] >= 3:
                                self.record.update(status="blocked", phase="reassessment", next_action=reason + "; three refused decisions require reassessment")
                                self.persist()
                                return self.record
                            self.record["phase"] = "decision refused"
                            self.persist()
                            self.emit("decision_refused", reason=reason)
                            continue
                    if len(self.record["open_findings"]) < len(before_decision["open_findings"]):
                        self.record["refusal_count"] = 0
                    self.save_place(state)
                    cycles += 1
                    if action in {"complete", "blocked"}:
                        self.record.update(status=action, phase="stopped")
                        self.persist()
                        return self.record
                    if action == "checkpoint":
                        self.record["checkpoint_count"] += 1
                        if self.record["checkpoint_count"] >= 3:
                            self.record.update(status="blocked", next_action="Reassess repeated decision checkpoints; inspect prompt sizes", phase="stopped")
                            self.persist()
                            return self.record
                        self.persist()
                        self.emit("rolling_in", next_action=state["next_action"])
                        continue
                    self.record["checkpoint_count"] = 0
                    if self.stopped():
                        continue
                    if action == "implement":
                        self.record["review"] = None
                        implementation_before = self.tree()
                        prompt = roll.prepare_prompt(agreement, state, "codex", context_aware=True)
                        prompt += "\n# Conductor's scoped contribution\n" + value["task"]
                        prompt += "\n# Open independent-review findings\n" + json.dumps(self.record["open_findings"])
                        receipt, candidates = self.dispatch("implementation", prompt, writable=True)
                        for candidate in candidates:
                            state = roll.check_state(candidate, self.root, state)
                        if receipt["tree"] != implementation_before:
                            self.record["refusal_count"] = 0
                        self.save_place(state)
                    else:
                        prompt = ("Independently review the original agreement against the actual artifacts. Read-only; "
                            "no edits or write-producing tests. Inspect, do not trust builder claims. Return ONLY JSON "
                            "with verdict (pass, changes, blocked), summary (evidence and limits), findings (strings; "
                            "empty only for pass/no specific findings). Pass requires evidence of the agreed checks; "
                            "do not assert you ran tests.\n<agreement>" + agreement + "</agreement>\n<task>" + value["task"]
                            + "</task>\n<saved_place>" + json.dumps(state) + "</saved_place>\n<open_findings>"
                            + json.dumps(self.record["open_findings"]) + "</open_findings>")
                        receipt, candidates = self.dispatch("review", prompt)
                        if len(candidates) != 1:
                            raise roll.RollError("Ambiguous review result")
                        verdict = review_result(candidates[0])
                        self.record["review"] = {**receipt, **verdict, "validated": True}
                        if verdict["verdict"] == "pass":
                            # A contradictory pass on the same tree cannot silently
                            # discard a finding. Explicit rejection needs evidence.
                            self.record["open_findings"] = [f for f in self.record["open_findings"] if f["tree"] == receipt["tree"]]
                        else:
                            self.record["open_findings"].extend({"id": receipt["request_id"] + ":" + str(i),
                                "request_id": receipt["request_id"], "tree": receipt["tree"], "finding": f}
                                for i, f in enumerate(verdict["findings"]))
                            if verdict["verdict"] == "changes":
                                state["failures"]["independent_review"] = state["failures"].get("independent_review", 0) + 1
                            if verdict["verdict"] == "blocked" or state["failures"].get("independent_review", 0) >= 3:
                                state.update(status="blocked", next_action="Conductor reassessment: " + verdict["summary"])
                            self.save_place(state)
                    receipt["validated"] = True
                    self.record["phase"] = "awaiting disposition"
                    self.persist()
                    if state["status"] == "blocked":
                        self.record.update(status="blocked", next_action=state["next_action"])
                        self.persist()
                        return self.record
            except BaseException as exc:
                self.record.update(status="uncertain", error=str(exc), phase="inspection required")
                self.persist()
                raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--agreement")
    parser.add_argument("--place")
    parser.add_argument("--stop", action="store_true", help="request a safe boundary stop; no new authority")
    for key in ("coordinator-model", "coordinator-effort", "worker-model", "worker-effort", "review-provider", "review-model", "review-effort"):
        parser.add_argument("--" + key)
    parser.add_argument("--max-cycles", type=int)
    parser.add_argument("--timeout", type=float)
    args = parser.parse_args(argv)
    try:
        if args.stop:
            transport = roll.connection()
            local = transport.Bridge(args.project).state.parent / "roll"
            record = transport.read(local / "run.json")
            if not record or record.get("kind") != "conductor" or record.get("status") != "running":
                raise roll.RollError("No recorded running managed Conductor to stop")
            transport.save(local / "stop.json", {"run_id": record["run_id"], "request_id": uuid.uuid4().hex})
            print("Safe stop requested; not proof of delivery or source shutdown.")
            return 0
        config = {key: getattr(args, key) for key in ("coordinator_model", "coordinator_effort", "worker_model",
                  "worker_effort", "review_provider", "review_model", "review_effort")}
        if not args.agreement or not args.place:
            raise roll.RollError("Agreement and saved place are required")
        result = ManagedConductor(args.project, args.agreement, args.place, config).run(args.max_cycles, args.timeout)
        print(json.dumps({"status": result["status"], "next_action": result["next_action"]}))
        return 0 if result["status"] in {"complete", "paused"} else 1
    except (roll.RollError, ValueError, OSError, RuntimeError) as exc:
        print(f"Managed Conductor stopped: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
