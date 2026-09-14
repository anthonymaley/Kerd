"""Managed Conductor lifecycle fixtures. No native model or network calls."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("managed_conductor_tested", SCRIPTS / "conductor_roll.py")
managed = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(managed)


class FakeBridge:
    context_aware = True

    def __init__(self, root):
        self.root = root
        self.state = root / ".git/cross-llm"
        self.state.mkdir(exist_ok=True)
        self.calls, self.closed, self.outputs = [], [], []

    def run(self, target, prompt, role, session, request_id, **kwargs):
        self.calls.append(dict(target=target, prompt=prompt, role=role, session=session,
                               request_id=request_id, **kwargs))
        value = self.outputs.pop(0)
        if callable(value):
            value = value(self.calls[-1])
        result = dict(status="completed", request_id=request_id, project=str(self.root),
                    session_id=f"native-{len(self.calls)}", process_id=123456789,
                    reply=json.dumps(value), context_readings=[{"last": {"totalTokens": 100}}],
                    owned_children_gone=True)
        folder = self.state / "requests" / request_id
        folder.mkdir(parents=True)
        (folder / "result.json").write_text(json.dumps(result))
        return result

    def close(self, alias):
        self.closed.append(alias)


class ManagedConductorTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="managed-conductor-test-")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "agreement.md").write_text("Build result.txt; local files only. No publish.\n")
        (self.root / "result.txt").write_text("before")
        self.initial = self.place()
        (self.root / "place.json").write_text(json.dumps(self.initial))
        self.bridge = FakeBridge(self.root)
        self.config = dict(coordinator_model="test-coordinator", coordinator_effort="high",
                           worker_model="test-worker", worker_effort="high",
                           review_provider="codex", review_model="test-reviewer", review_effort="high")
        self.driver = managed.ManagedConductor(self.root, "agreement.md", "place.json",
                                               self.config, coordinator=self.bridge, reviewer=self.bridge)
        self.enterContext(patch.object(managed.roll.os, "killpg", side_effect=ProcessLookupError))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    def place(self, **changes):
        value = dict(status="continue", next_action="Build result.txt", memory="Original decision",
                     evidence=["result.txt"], failures={}, pending_jobs=[])
        value.update(changes)
        return value

    def decision(self, action, **changes):
        def reply(call):
            payload = json.loads(call["prompt"].split("\n# Current input\n", 1)[1])
            latest = payload["latest_contribution"]
            value = dict(action=action, place=payload["place"], task="Do the agreed result.txt work",
                         ack={"request_id": latest["request_id"], "disposition": "Retained the finding"}
                         if latest else None)
            value["place"] = {**value["place"], "memory": f"Decision {len(self.bridge.calls)}"}
            value.update(changes)
            return value
        return reply

    def worker(self, content, failures=None):
        def reply(call):
            (self.root / "result.txt").write_text(content)
            return self.place(status="review", memory=content, failures=failures or {})
        return reply

    def record(self):
        return json.loads(self.driver.ledger.read_text())

    def test_correction_review_loop_needs_no_control_chat_turn(self):
        self.bridge.outputs = [self.decision("implement"), self.worker("first"),
            self.decision("review"), dict(verdict="changes", summary="Fix missing newline", findings=["missing newline"]),
            self.decision("implement"), self.worker("fixed", {"independent_review": 1}),
            self.decision("review"), dict(verdict="pass", summary="Correction checked", findings=[]),
            self.decision("complete")]
        result = self.driver.run()
        self.assertEqual(result["status"], "complete")
        self.assertEqual(len(self.bridge.calls), 9)
        self.assertIn("missing newline", self.bridge.calls[4]["prompt"])
        self.assertIn("Retained the finding", json.dumps(self.record()))
        self.assertEqual(len(self.record()["contributions"]), 4)
        self.assertEqual(len(set(c["session"] for c in self.bridge.calls)), 9)
        self.assertEqual(len(self.bridge.closed), 9)
        self.assertEqual([c["writable"] for c in self.bridge.calls], [False, True, False, False, False, True, False, False, False])

    def test_checkpoint_starts_fresh_decision_with_saved_memory(self):
        self.bridge.outputs = [self.decision("checkpoint", place=self.place(memory="Keep a discovered constraint")),
                               self.decision("blocked", place=self.place(status="blocked", memory="Keep a discovered constraint"))]
        self.assertEqual(self.driver.run()["status"], "blocked")
        self.assertIn("Keep a discovered constraint", self.bridge.calls[1]["prompt"])
        self.assertIn("checkpoint", self.bridge.calls[0]["checkpoint_instruction"])

    def test_cannot_complete_without_independent_review(self):
        self.bridge.outputs = [self.decision("complete") for _ in range(3)]
        self.assertEqual(self.driver.run()["status"], "blocked")
        self.assertEqual(len(self.record()["completion_refusals"]), 3)

    def test_failed_review_cannot_be_called_complete(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Wrong", findings=["Wrong"]),
                               *[self.decision("complete") for _ in range(3)]]
        self.assertEqual(self.driver.run()["status"], "blocked")

    def test_unacknowledged_contribution_stops_before_next_job(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="pass", summary="OK", findings=[]),
                               self.decision("complete", ack=None)]
        with self.assertRaisesRegex(managed.roll.RollError, "acknowledge"):
            self.driver.run()
        self.assertEqual(len(self.bridge.calls), 3)

    def test_source_cleanup_must_finish_before_successor(self):
        self.bridge.outputs = [self.decision("checkpoint")]
        with patch.object(managed.roll, "group_gone", return_value=False):
            with self.assertRaisesRegex(managed.roll.RollError, "shutdown"):
                self.driver.run()
        self.assertEqual(len(self.bridge.calls), 1)

    def test_uncertain_record_does_not_redispatch(self):
        self.bridge.outputs = [dict(bad="shape")]
        with self.assertRaises(managed.roll.RollError):
            self.driver.run()
        with self.assertRaisesRegex(managed.roll.RollError, "inspection"):
            self.driver.run()
        self.assertEqual(len(self.bridge.calls), 1)

    def test_refuses_legacy_roll_record_even_when_paused(self):
        self.driver.transport.save(self.driver.ledger, dict(status="paused"))
        with self.assertRaisesRegex(managed.roll.RollError, "different"):
            self.driver.run()
        self.assertEqual(self.bridge.calls, [])

    def test_agreement_change_stops_with_last_good_place(self):
        def mutate(call):
            (self.root / "agreement.md").write_text("Broader authority")
            return self.decision("checkpoint")(call)
        self.bridge.outputs = [mutate]
        with self.assertRaisesRegex(managed.roll.RollError, "protected"):
            self.driver.run()
        self.assertEqual(json.loads((self.root / "place.json").read_text()), self.initial)

    def test_safe_limit_is_paused_and_resume_retains_contribution(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="pass", summary="Known result", findings=[])]
        self.assertEqual(self.driver.run(max_cycles=1)["status"], "paused")
        self.bridge.outputs = [self.decision("complete")]
        self.assertEqual(self.driver.run()["status"], "complete")
        self.assertIn("Known result", self.bridge.calls[-1]["prompt"])

    def test_repeated_checkpoint_only_cycles_stop_for_reassessment(self):
        self.bridge.outputs = [self.decision("checkpoint") for _ in range(3)]
        self.assertEqual(self.driver.run()["status"], "blocked")
        self.assertEqual(len(self.bridge.calls), 3)

    def test_open_findings_survive_implementation_receipt_replacing_latest_review(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Fix it", findings=["Keep this unresolved"]),
            self.decision("implement"), lambda call: self.place(status="review", memory="New work", failures={"independent_review": 1}),
            self.decision("blocked", place=self.place(status="blocked", memory="Need decision", failures={"independent_review": 1}))]
        self.assertEqual(self.driver.run()["status"], "blocked")
        payload = json.loads(self.bridge.calls[-1]["prompt"].split("\n# Current input\n")[1])
        self.assertEqual(payload["latest_contribution"]["kind"], "implementation")
        self.assertEqual(payload["open_findings"][0]["finding"], "Keep this unresolved")
        self.assertEqual(len(self.record()["dispositions"]), 2)

    def test_review_is_bound_to_non_evidence_files_too(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="pass", summary="OK", findings=[])]
        self.driver.run(max_cycles=1)
        (self.root / "another.txt").write_text("unreviewed")
        self.bridge.outputs = [self.decision("complete") for _ in range(3)]
        self.assertEqual(self.driver.run()["status"], "blocked")
        self.assertIn("current tree", self.record()["next_action"])

    def test_readonly_review_cannot_modify_files(self):
        def changed(call):
            (self.root / "result.txt").write_text("reviewer edit")
            return dict(verdict="pass", summary="OK", findings=[])
        self.bridge.outputs = [self.decision("review"), changed]
        with self.assertRaisesRegex(managed.roll.RollError, "read-only"):
            self.driver.run()

    def test_worker_cannot_erase_review_failure_counts(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Wrong", findings=["Wrong"]),
                               self.decision("implement"), self.worker("drops failure history")]
        with self.assertRaisesRegex(managed.roll.RollError, "failure counts"):
            self.driver.run()

    def test_write_ahead_identity_exists_before_launch_and_uncertainty_keeps_it(self):
        def crash(call):
            pending = self.record()["pending"]
            self.assertEqual(pending["request_id"], call["request_id"])
            raise KeyboardInterrupt("host lost")
        self.bridge.outputs = [crash]
        with self.assertRaises(KeyboardInterrupt):
            self.driver.run()
        self.assertEqual(self.record()["pending"]["request_id"], self.bridge.calls[0]["request_id"])
        self.assertEqual(self.record()["status"], "uncertain")

    def test_stop_only_request_checkpoints_then_pauses_without_work_dispatch(self):
        def stop(call):
            self.driver.transport.save(self.driver.local / "stop.json", {"run_id": self.record()["run_id"], "request_id": "stop-1"})
            self.assertTrue(call["checkpoint_requested"]())
            return self.decision("implement")(call)
        self.bridge.outputs = [stop]
        self.assertEqual(self.driver.run()["status"], "paused")
        self.assertEqual(len(self.bridge.calls), 1)
        self.assertEqual(self.record()["last_stop"], "stop-1")

    def test_fresh_native_identity_required_for_every_role(self):
        original = self.bridge.run
        def reused(*args, **kwargs):
            value = original(*args, **kwargs)
            value["session_id"] = "same"
            return value
        self.bridge.run = reused
        self.bridge.outputs = [self.decision("review"), dict(verdict="pass", summary="OK", findings=[])]
        with self.assertRaisesRegex(managed.roll.RollError, "identity"):
            self.driver.run()

    def test_provider_and_effort_choices_are_not_changed_by_model(self):
        self.bridge.outputs = [self.decision("implement"), self.worker("done")]
        self.driver.run(max_cycles=1)
        self.assertEqual(self.bridge.calls[0]["model"], "test-coordinator")
        self.assertEqual(self.bridge.calls[1]["model"], "test-worker")
        self.assertTrue(all(call["effort"] == "high" for call in self.bridge.calls))

    def test_legacy_worker_roll_refuses_managed_record(self):
        self.driver.transport.save(self.driver.ledger, dict(kind="conductor", status="paused"))
        worker = managed.roll.Roller(self.root, "agreement.md", "place.json", "codex", "test", "high", bridge=self.bridge)
        with self.assertRaisesRegex(managed.roll.RollError, "Managed Conductor"):
            worker.run()
        with self.assertRaisesRegex(managed.roll.RollError, "Managed Conductor"):
            worker.recover("place.json", "inspection")

    def test_changed_result_receipt_is_not_replayed(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="pass", summary="OK", findings=[])]
        self.driver.run(max_cycles=1)
        receipt = self.record()["contributions"][-1]
        path = self.bridge.state / "requests" / receipt["request_id"] / "result.json"
        path.write_text(path.read_text() + " ")
        with self.assertRaisesRegex(managed.roll.RollError, "changed after capture"):
            self.driver.run()

    def test_cli_bad_input_is_a_reported_failure_not_a_traceback(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(managed.main(["--project", str(self.root)]), 2)

    def test_invalid_worker_result_stays_linked_as_unvalidated(self):
        def invalid(call):
            (self.root / "result.txt").write_text("partially changed")
            state = self.place()
            del state["failures"]
            return state
        self.bridge.outputs = [self.decision("implement"), invalid]
        with self.assertRaises(managed.roll.RollError):
            self.driver.run()
        contribution = self.record()["contributions"][-1]
        self.assertEqual(contribution["kind"], "implementation")
        self.assertFalse(contribution["validated"])
        self.assertEqual(contribution["request_id"], self.bridge.calls[-1]["request_id"])

    def test_invalid_review_stays_linked_as_unvalidated(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="maybe")]
        with self.assertRaises(managed.roll.RollError):
            self.driver.run()
        self.assertEqual(self.record()["contributions"][-1]["kind"], "review")
        self.assertFalse(self.record()["contributions"][-1]["validated"])

    def test_unchanged_tree_review_shopping_does_not_clear_finding(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Wrong", findings=["Missing newline"]),
            self.decision("review"), dict(verdict="pass", summary="Actually fine", findings=[]),
            *[self.decision("complete") for _ in range(3)]]
        self.assertEqual(self.driver.run()["status"], "blocked")
        self.assertEqual(len(self.record()["open_findings"]), 1)

    def test_explicit_evidenced_rejection_can_resolve_conflicting_reviews(self):
        def reject(call):
            payload = json.loads(call["prompt"].split("\n# Current input\n")[1])
            return self.decision("complete", reject_findings=[dict(id=payload["open_findings"][0]["id"],
                reason="Original agreement does not require a newline", evidence=["agreement.md"])])(call)
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Add newline", findings=["Missing newline"]),
            self.decision("review"), dict(verdict="pass", summary="No newline obligation", findings=[]), reject]
        self.assertEqual(self.driver.run()["status"], "complete")
        self.assertEqual(len(self.record()["finding_dispositions"]), 1)

    def test_exact_open_findings_reach_correction_worker(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Fix", findings=["UNIQUE-FINDING-XYZ"]),
            self.decision("implement"), self.worker("fixed", {"independent_review": 1})]
        self.driver.run(max_cycles=2)
        self.assertIn("UNIQUE-FINDING-XYZ", self.bridge.calls[-1]["prompt"])

    def test_revised_acknowledgements_are_retained_not_overwritten(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="pass", summary="OK", findings=[]), self.decision("checkpoint")]
        self.driver.run(max_cycles=2)
        def revised(call):
            value = self.decision("complete")(call)
            value["ack"]["disposition"] = "Reconsidered against the agreement"
            return value
        self.bridge.outputs = [revised]
        self.driver.run()
        self.assertEqual(len(next(iter(self.record()["dispositions"].values()))), 2)

    def test_current_review_gate_is_explicit_after_implementation(self):
        self.bridge.outputs = [self.decision("implement"), self.worker("done"),
                               self.decision("blocked", place=self.place(status="blocked"))]
        self.driver.run()
        payload = json.loads(self.bridge.calls[-1]["prompt"].split("\n# Current input\n")[1])
        self.assertFalse(payload["review_gate"]["current_tree_reviewed"])
        self.assertIsNone(payload["review_gate"]["verdict"])

    def test_refused_complete_retries_without_promoting_its_place(self):
        self.bridge.outputs = [self.decision("complete", place=self.place(memory="Wrongly says all done")),
            self.decision("review"), dict(verdict="pass", summary="Evidence checked", findings=[]), self.decision("complete")]
        self.assertEqual(self.driver.run()["status"], "complete")
        payload = json.loads(self.bridge.calls[1]["prompt"].split("\n# Current input\n")[1])
        self.assertEqual(payload["place"]["memory"], "Original decision")
        self.assertIn("independent review", payload["review_gate"]["refused_complete"])
        self.assertEqual(len(self.record()["completion_refusals"]), 1)

    def test_same_tree_reviews_do_not_reset_completion_refusals(self):
        self.bridge.outputs = [self.decision("review"), dict(verdict="changes", summary="Missing newline", findings=["Missing newline"])]
        for _ in range(5):
            self.bridge.outputs += [self.decision("complete"), self.decision("review"),
                                    dict(verdict="pass", summary="Actually OK", findings=[])]
        result = self.driver.run()
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["refusal_count"], 3)
        self.assertEqual(len(result["completion_refusals"]), 3)
        self.assertEqual(len(result["open_findings"]), 1)


if __name__ == "__main__":
    unittest.main()
