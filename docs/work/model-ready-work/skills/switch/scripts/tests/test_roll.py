"""Isolated Roll lifecycle tests; never launch a provider or use the network.

These lifecycle and regression checks are not a whole-product proof.
"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "roll.py"
SPEC = importlib.util.spec_from_file_location("switch_roll_tested", SCRIPT)
roll = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(roll)


class FakeBridge:
    def __init__(self, root):
        self.root = root
        self.state = root / ".git" / "cross-llm"
        self.state.mkdir()
        self.calls = []
        self.closed = []
        self.outcome = None

    def run(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.outcome(len(self.calls))

    def close(self, alias):
        self.closed.append(alias)


class RollLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="switch-roll-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "agreement.md").write_text("Build a local result. No network or commits.\n")
        (self.root / "result.txt").write_text("existing result\n")
        self.initial = self.state()
        self.write_place(self.initial)
        self.bridge = FakeBridge(self.root)
        self.roller = roll.Roller(self.root, "agreement.md", "place.json", "codex",
                                  "test-model", "high", bridge=self.bridge)
        # Fake provider groups are always already gone. Never signal a real PID.
        self.killpg = self.enterContext(patch.object(roll.os, "killpg", side_effect=ProcessLookupError))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    def state(self, **changes):
        value = {"status": "continue", "next_action": "Complete the result",
                 "memory": "Keep the original decision", "evidence": ["result.txt"],
                 "failures": {"quality": 1}, "pending_jobs": []}
        value.update(changes)
        return value

    def write_place(self, value):
        (self.root / "place.json").write_text(json.dumps(value))

    def read_place(self):
        return json.loads((self.root / "place.json").read_text())

    def ledger(self):
        return json.loads(self.roller.ledger.read_text())

    def result(self, state, number=1, **changes):
        value = {"status": "completed", "session_id": f"fresh-{number}",
                 "reply": json.dumps(state), "process_id": 123456789}
        value.update(changes)
        return value

    def test_two_runs_use_unique_aliases_and_saved_place(self):
        def outcome(number):
            (self.root / "result.txt").write_text(f"result version {number}\n")
            return self.result(self.state(status="continue" if number == 1 else "review",
                                          memory=f"Completed piece {number}"), number)
        self.bridge.outcome = outcome
        result = self.roller.run()
        self.assertEqual(result["status"], "review")
        self.assertEqual(len(self.bridge.calls), 2)
        first, second = (call[0] for call in self.bridge.calls)
        self.assertNotEqual(first[3], second[3])
        self.assertEqual(first[3], first[4])
        self.assertEqual(second[3], second[4])
        self.assertIn("Completed piece 1", second[1])
        self.assertEqual(self.bridge.closed, [first[3], second[3]])
        self.assertEqual(self.read_place()["failures"], self.initial["failures"])

    def test_reused_native_session_stops_and_preserves_last_good_place(self):
        def outcome(number):
            (self.root / "result.txt").write_text(f"version {number}")
            return self.result(self.state(memory=f"piece {number}"), session_id="reused")
        self.bridge.outcome = outcome
        with self.assertRaisesRegex(roll.RollError, "Fresh session"):
            self.roller.run()
        self.assertEqual(len(self.bridge.calls), 2)
        self.assertEqual(self.read_place()["memory"], "piece 1")
        self.assertEqual(self.ledger()["status"], "uncertain")

    def test_interruption_blocks_automatic_relaunch(self):
        def interrupted(number):
            (self.root / "result.txt").write_text("partial work")
            raise KeyboardInterrupt("simulated interruption")
        self.bridge.outcome = interrupted
        with self.assertRaises(KeyboardInterrupt):
            self.roller.run()
        self.assertEqual(self.read_place(), self.initial)
        with self.assertRaisesRegex(roll.RollError, "Previous Roll needs inspection"):
            self.roller.run()
        self.assertEqual(len(self.bridge.calls), 1)

    def test_prior_running_uncertain_and_failed_ledgers_prevent_launch(self):
        for status in ("running", "uncertain", "failed"):
            with self.subTest(status=status):
                self.roller.transport.save(self.roller.ledger, {"status": status})
                with self.assertRaisesRegex(roll.RollError, "Previous Roll"):
                    self.roller.run()
        self.assertEqual(self.bridge.calls, [])

    def test_live_provider_group_blocks_handoff(self):
        self.killpg.side_effect = None
        self.bridge.outcome = lambda n: self.result(self.state(status="review"), n)
        with self.assertRaisesRegex(roll.RollError, "did not finish cleanly"):
            self.roller.run()
        self.assertEqual(self.read_place(), self.initial)

    def test_provider_timeout_blocks_handoff_and_retry(self):
        self.bridge.outcome = lambda n: self.result(self.state(status="review"), n,
                                                   status="timed_out")
        with self.assertRaises(roll.RollError):
            self.roller.run()
        with self.assertRaisesRegex(roll.RollError, "Previous Roll"):
            self.roller.run()
        self.assertEqual(len(self.bridge.calls), 1)

    def test_pending_jobs_prevent_new_run(self):
        self.write_place(self.state(pending_jobs=[{"id": "uncertain-job"}]))
        with self.assertRaisesRegex(roll.RollError, "Pending jobs"):
            self.roller.run()
        self.assertEqual(self.bridge.calls, [])

    def test_worker_cannot_erase_failures_or_evidence(self):
        for changes, message in (({"failures": {}}, "failure counts"),
                                 ({"evidence": []}, "evidence references")):
            with self.subTest(changes=changes):
                self.roller.transport.save(self.roller.ledger, {"status": "paused"})
                self.bridge.outcome = lambda n: self.result(self.state(status="review", **changes), n)
                with self.assertRaisesRegex(roll.RollError, message):
                    self.roller.run()
                self.assertEqual(self.read_place(), self.initial)

    def test_three_failed_corrections_cannot_continue(self):
        self.bridge.outcome = lambda n: self.result(self.state(failures={"quality": 3}), n)
        with self.assertRaisesRegex(roll.RollError, "Three failed corrections"):
            self.roller.run()
        self.assertEqual(self.read_place(), self.initial)

    def test_worker_modification_of_protected_file_stops(self):
        def outcome(number):
            (self.root / "agreement.md").write_text("unauthorized change")
            return self.result(self.state(status="review"), number)
        self.bridge.outcome = outcome
        with self.assertRaisesRegex(roll.RollError, "protected agreement"):
            self.roller.run()
        self.assertEqual(self.read_place(), self.initial)
        self.assertEqual(self.ledger()["status"], "uncertain")

    def test_failed_place_save_retains_previous_place_and_blocks_retry(self):
        original_save = self.roller.transport.save
        def fail_place_save(path, value):
            if path == self.roller.place:
                raise OSError("simulated disk full")
            return original_save(path, value)
        self.bridge.outcome = lambda n: self.result(self.state(status="review"), n)
        with patch.object(self.roller.transport, "save", side_effect=fail_place_save):
            with self.assertRaisesRegex(OSError, "disk full"):
                self.roller.run()
        self.assertEqual(self.read_place(), self.initial)
        self.assertEqual(self.ledger()["status"], "uncertain")
        self.assertEqual(self.bridge.closed, [])

    def test_existing_owner_lock_prevents_second_launch(self):
        with self.roller.transport.exclusive(self.roller.local / "owner.lock"):
            with self.assertRaises(self.roller.transport.Busy):
                self.roller.run()
        self.assertEqual(self.bridge.calls, [])

    def test_same_evidence_bytes_stop_first_run_in_one_invocation(self):
        self.bridge.outcome = lambda n: self.result(self.state(memory=f"rephrased {n}"), n)
        with self.assertRaisesRegex(roll.RollError, "No new artifact evidence"):
            self.roller.run(max_runs=4)
        self.assertEqual(len(self.bridge.calls), 1)

    def test_unchanged_existing_evidence_should_not_justify_first_continuation(self):
        self.bridge.outcome = lambda n: self.result(self.state(memory="only a new sentence"), n)
        with self.assertRaisesRegex(roll.RollError, "No new artifact evidence"):
            self.roller.run(max_runs=1)

    def test_progress_check_should_survive_invocation_boundaries(self):
        self.bridge.outcome = lambda n: self.result(self.state(memory=f"only sentence {n}"), n)
        for _ in range(4):
            try:
                self.roller.run(max_runs=1)
            except roll.RollError:
                break
        self.assertLessEqual(len(self.bridge.calls), 2,
                             "unchanged result bytes advanced through four invocations")

    def test_saved_place_should_not_count_as_new_build_evidence(self):
        self.initial = self.state(evidence=["place.json"])
        self.write_place(self.initial)
        self.bridge.outcome = lambda n: self.result(
            self.state(memory=f"only sentence {n}", evidence=["place.json"]), n)
        with self.assertRaises(roll.RollError):
            self.roller.run(max_runs=4)

    def test_duplicate_evidence_paths_should_not_count_as_progress(self):
        self.bridge.outcome = lambda n: self.result(
            self.state(memory=f"only sentence {n}", evidence=["result.txt"] * (n + 1)), n)
        with self.assertRaises(roll.RollError):
            self.roller.run(max_runs=4)

    def test_duplicate_aliases_are_rejected_before_launch(self):
        (self.root / "result-alias.txt").symlink_to("result.txt")
        for alias in ("./result.txt", "result-alias.txt"):
            with self.subTest(alias=alias):
                self.write_place(self.state(evidence=["result.txt", alias]))
                with self.assertRaisesRegex(roll.RollError, "unique"):
                    self.roller.run()
        self.assertEqual(self.bridge.calls, [])

    def test_protected_file_aliases_are_rejected_before_launch(self):
        (self.root / "place-alias.json").symlink_to("place.json")
        (self.root / "agreement-alias.md").symlink_to("agreement.md")
        for alias in ("./place.json", "place-alias.json", "agreement-alias.md"):
            with self.subTest(alias=alias):
                self.write_place(self.state(evidence=[alias]))
                with self.assertRaisesRegex(roll.RollError, "cannot count as build evidence"):
                    self.roller.run()
        self.assertEqual(self.bridge.calls, [])

    def test_actual_progress_history_survives_new_roller_instances(self):
        versions = {1: "first real change", 2: "second real change", 3: "first real change"}
        def outcome(number):
            (self.root / "result.txt").write_text(versions[number])
            return self.result(self.state(memory=f"piece {number}"), number)
        self.bridge.outcome = outcome
        for number in (1, 2):
            fresh_roller = roll.Roller(self.root, "agreement.md", "place.json", "codex",
                                      "test-model", "high", bridge=self.bridge)
            result = fresh_roller.run(max_runs=1)
            self.assertEqual(result["status"], "paused")
            self.assertEqual(len(self.ledger()["artifact_snapshots"]), number + 1)
        restored_roller = roll.Roller(self.root, "agreement.md", "place.json", "codex",
                                     "test-model", "high", bridge=self.bridge)
        with self.assertRaisesRegex(roll.RollError, "No new artifact evidence"):
            restored_roller.run(max_runs=1)
        self.assertEqual(len(self.bridge.calls), 3)
        self.assertEqual(self.read_place()["memory"], "piece 2")
        self.assertEqual(self.ledger()["status"], "uncertain")

    def test_prior_record_for_different_work_prevents_launch(self):
        self.roller.transport.save(self.roller.ledger, {
            "status": "paused", "agreement": "different-agreement.md", "place": "place.json"})
        with self.assertRaisesRegex(roll.RollError, "different work"):
            self.roller.run()
        self.assertEqual(self.bridge.calls, [])


if __name__ == "__main__":
    unittest.main()
