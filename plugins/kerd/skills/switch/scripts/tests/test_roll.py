"""Isolated Roll lifecycle tests; never launch a provider or use the network.

These lifecycle and regression checks are not a whole-product proof.
"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, call, patch


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

    def test_waiting_chat_roll_prevents_launch(self):
        self.roller.local.mkdir(parents=True, exist_ok=True)
        (self.roller.local / "chat.json").write_text("{}")
        with self.assertRaisesRegex(roll.RollError, "chat roll is waiting"):
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


class ParseReplyTests(unittest.TestCase):
    PLACE = {"status": "review", "next_action": "Review", "memory": "m", "evidence": [],
             "failures": {}, "pending_jobs": []}

    def body(self):
        return json.dumps(self.PLACE, indent=2)

    def test_bare_and_whole_fenced_json_still_parse(self):
        self.assertEqual(roll.parse_reply(self.body()), self.PLACE)
        self.assertEqual(roll.parse_reply("```json\n" + self.body() + "\n```"), self.PLACE)

    def test_prose_around_exactly_one_json_fence_parses(self):
        reply = "All six notes exist.\n\n```json\n" + self.body() + "\n```\nDone."
        self.assertEqual(roll.parse_reply(reply), self.PLACE)

    def test_ambiguous_or_malformed_replies_are_refused(self):
        refused = {
            "prose without a fence": "All done, status review.",
            "loose JSON in prose": "Here it is: " + self.body(),
            "two json fences": "```json\n" + self.body() + "\n```\n```json\n" + self.body() + "\n```",
            "another fence beside it": "```python\nx = 1\n```\n```json\n" + self.body() + "\n```",
            "untagged fence": "Result:\n```\n" + self.body() + "\n```",
            "unclosed fence": "Result:\n```json\n" + self.body(),
            "invalid JSON in the fence": "Result:\n```json\n{not json}\n```",
            "not text": None,
            "conflicting JSON before the fence": json.dumps(dict(self.PLACE, status="continue"))
                                                 + "\n```json\n" + self.body() + "\n```",
            "conflicting JSON after the fence": "```json\n" + self.body() + "\n```\n"
                                                + json.dumps(dict(self.PLACE, status="blocked")),
            "a JSON array in the prose": "Evidence [\"notes/1.md\"]\n```json\n" + self.body() + "\n```",
        }
        for label, reply in refused.items():
            with self.subTest(label), self.assertRaisesRegex(roll.RollError, "unambiguous"):
                roll.parse_reply(reply)


class RecordingBridge:
    """Stub bridge class: records constructor arguments, never launches a provider."""
    instances = []
    context_aware = True

    def __init__(self, *args):
        self.args = args
        type(self).instances.append(self)


def stub_module(name, **attributes):
    module = types.ModuleType(name)
    for key, value in attributes.items():
        setattr(module, key, value)
    return module


class ContextAwareWiringTests(unittest.TestCase):
    """roll.main route selection and the --control refusal; no Roll is run."""

    def setUp(self):
        self.claude_bridge = type("ClaudeStreamBridge", (RecordingBridge,), {"instances": []})
        self.codex_bridge = type("AppServerBridge", (RecordingBridge,), {"instances": []})
        self.live_control = Mock(name="LiveControl")
        self.enterContext(patch.dict(sys.modules, {
            "claude_roll": stub_module("claude_roll", ClaudeStreamBridge=self.claude_bridge),
            "codex_roll": stub_module("codex_roll", AppServerBridge=self.codex_bridge),
            "roll_control": stub_module("roll_control", LiveControl=self.live_control)}))
        self.transport = object()
        self.enterContext(patch.object(roll, "connection", return_value=self.transport))
        self.roller_class = self.enterContext(patch.object(roll, "Roller"))
        self.roller_class.return_value.run.return_value = {"status": "review"}
        self.stdout = self.enterContext(contextlib.redirect_stdout(io.StringIO()))
        self.stderr = self.enterContext(contextlib.redirect_stderr(io.StringIO()))

    def main(self, target, *extra):
        argv = ["roll.py", "--project", "/nonexistent-project", "--agreement", "agreement.md",
                "--place", "place.json", "--target", target, "--model", "m", "--effort", "high", *extra]
        with patch.object(sys, "argv", argv):
            return roll.main()

    def test_claude_context_aware_constructs_claude_stream_bridge(self):
        code = self.main("claude", "--context-aware", "--context-fraction", "0.5",
                         "--test-roll-at-tokens", "1000")
        self.assertEqual(code, 0)
        self.assertEqual([b.args for b in self.claude_bridge.instances],
                         [("/nonexistent-project", self.transport, 0.5, 1000)])
        self.assertEqual(self.codex_bridge.instances, [])
        self.assertIs(self.roller_class.call_args.kwargs["bridge"], self.claude_bridge.instances[0])

    def test_claude_control_is_refused_before_live_control(self):
        code = self.main("claude", "--context-aware", "--control")
        self.assertEqual(code, 2)
        error = json.loads(self.stderr.getvalue())
        self.assertEqual(error["status"], "blocked")
        self.assertEqual(error["error"], "Live control and held sources are Codex-only; "
                                         "Claude context-aware Roll has no retainable source")
        self.live_control.assert_not_called()
        self.roller_class.return_value.run.assert_not_called()

    def test_codex_context_aware_still_constructs_app_server_bridge(self):
        code = self.main("codex", "--context-aware", "--context-fraction", "0.5",
                         "--test-roll-at-tokens", "1000")
        self.assertEqual(code, 0)
        self.assertEqual([b.args for b in self.codex_bridge.instances],
                         [("/nonexistent-project", self.transport, 0.5, 1000)])
        self.assertEqual(self.claude_bridge.instances, [])
        self.assertIs(self.roller_class.call_args.kwargs["bridge"], self.codex_bridge.instances[0])


class HeldSourceRefusalTests(unittest.TestCase):
    setUp = RollLifecycleTests.setUp
    state = RollLifecycleTests.state
    write_place = RollLifecycleTests.write_place

    def test_control_without_release_held_is_refused_before_dispatch(self):
        self.bridge.context_aware = True
        self.assertFalse(hasattr(self.bridge, "release_held"))
        control = Mock()
        with self.assertRaisesRegex(roll.RollError, "Live control requires the held-source Codex adapter"):
            self.roller.run(control=control)
        self.assertEqual(self.bridge.calls, [])
        control.ensure_connected.assert_not_called()
        self.assertFalse(self.roller.ledger.exists())


class ContextAwareRecoveryTests(unittest.TestCase):
    """Mirrors test_codex_roll.RecoveryTests setup, with codex_roll stubbed."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="switch-roll-recovery-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.initial = {"status": "continue", "next_action": "Finish result", "memory": "Original",
                        "failures": {"quality": 1}, "evidence": ["result.txt"], "pending_jobs": []}
        (self.root / "agreement.md").write_text("Build local result")
        (self.root / "result.txt").write_text("existing evidence")
        self.bridge = types.SimpleNamespace(root=self.root, state=self.root / ".git/cross-llm",
                                            run=Mock(), close=Mock(), context_aware=True)
        self.bridge.state.mkdir(parents=True)
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))
        self.ask = roll.connection()
        self.ask.save(self.root / "place.json", self.initial)
        self.roller = roll.Roller(self.root, "agreement.md", "place.json", "claude", "chosen-model",
                                  "high", bridge=self.bridge)
        self.children_gone = Mock(return_value=False)
        self.enterContext(patch.dict(sys.modules, {
            "codex_roll": stub_module("codex_roll", children_gone=self.children_gone)}))
        self.enterContext(patch.object(roll.os, "killpg", side_effect=ProcessLookupError))
        self.prior = {"status": "uncertain", "agreement": "agreement.md", "place": "place.json",
                      "request_id": "failed-request", "error": "original failure", "target": "claude",
                      "history": [], "artifact_snapshots": [self.roller.artifact_snapshot(self.initial)]}
        self.ask.save(self.roller.ledger, self.prior)
        self.request = self.bridge.state / "requests/failed-request"
        self.request.mkdir(parents=True)
        self.provider = {"status": "failed", "process_id": 123456789, "session_id": "retired-session",
                         "request_id": "failed-request", "project": str(self.root), "target": "claude",
                         "route": "claude-stream-json", "owned_children": {"987654321": "child-start"}}
        self.save_provider()
        self.prepared = {**self.initial, "memory": "Inspected failed operation", "failures": {"quality": 2}}
        self.ask.save(self.root / "prepared.json", self.prepared)

    def save_provider(self, **changes):
        self.provider.update(changes)
        self.ask.save(self.request / "result.json", self.provider)

    def recover(self):
        return self.roller.recover("prepared.json", "Inspected cause; prior jobs have ended")

    def assert_unchanged(self):
        self.assertEqual(self.ask.read(self.root / "place.json"), self.initial)
        self.assertEqual(self.ask.read(self.roller.ledger), self.prior)
        self.bridge.run.assert_not_called()

    def test_claude_stream_result_without_cleanup_evidence_is_refused(self):
        self.assertNotIn("owned_children_gone", self.provider)
        with self.assertRaisesRegex(roll.RollError, "Owned child shutdown remains uncertain"):
            self.recover()
        self.children_gone.assert_called_once_with({"987654321": "child-start"})
        self.assert_unchanged()

    def test_claude_stream_result_with_confirmed_child_exit_is_recovered(self):
        self.children_gone.return_value = True
        self.assertEqual(self.recover()["status"], "paused")
        self.children_gone.assert_called_once_with({"987654321": "child-start"})
        ledger = self.ask.read(self.roller.ledger)
        self.assertEqual(ledger["retired_sessions"], ["retired-session"])
        self.assertEqual(ledger["recoveries"][0]["previous_place"], self.initial)
        self.assertEqual(self.ask.read(self.root / "place.json"), self.prepared)
        self.bridge.run.assert_not_called()

    ROUTES = ("claude-stream-json", "app-server-stdio")
    START = "Tue Sep 15 16:00:00 2026"

    def lost_after_receipt(self, provider_route, **changes):
        """A controller killed after the checkpoint_saved receipt: ledger and request left running."""
        self.prior = {**self.prior, "status": "running"}
        self.prior.pop("error", None)
        self.ask.save(self.roller.ledger, self.prior)
        self.ask.save(self.root / "place.json", self.initial)
        self.provider = {"status": "running", "phase": "checkpoint_saved", "provider_completed": True,
                         "process_id": 123456789, "owner_pid": 234567890, "session_id": "retired-session",
                         "request_id": "failed-request", "project": str(self.root), "target": "claude",
                         "route": provider_route, "owned_children": {"987654321": "child-start"},
                         "checkpoint_candidates": [json.dumps({**self.initial, "memory": "Receipt candidate"})]}
        self.save_provider(**changes)
        self.children_gone.return_value = True
        self.children_gone.reset_mock()

    def assert_receipt_refused(self, pattern, reason="Inspected cause; prior jobs have ended"):
        with self.assertRaisesRegex(roll.RollError, pattern):
            self.roller.recover("prepared.json", reason)
        self.assert_unchanged()

    def test_receipt_recovery_is_accepted_when_every_condition_holds(self):
        for route in self.ROUTES:
            with self.subTest(route=route):
                self.lost_after_receipt(route)
                with patch.object(roll.os, "kill", side_effect=ProcessLookupError) as owner_probe:
                    self.assertEqual(self.recover()["status"], "paused")
                owner_probe.assert_called_once_with(234567890, 0)
                self.children_gone.assert_called_once_with({"987654321": "child-start"})
                ledger = self.ask.read(self.roller.ledger)
                self.assertEqual(ledger["status"], "paused")
                self.assertEqual(ledger["recoveries"][-1]["previous_status"], "running")
                self.assertEqual(ledger["recoveries"][-1]["previous_phase"], "checkpoint_saved")
                self.assertEqual(ledger["retired_sessions"], ["retired-session"])
                # No promotion: the prepared state is saved, never the receipt's candidate.
                self.assertEqual(self.ask.read(self.root / "place.json"), self.prepared)
                self.assertEqual(self.ask.read(self.request / "result.json"), self.provider)
                self.bridge.run.assert_not_called()

    def test_receipt_recovery_refuses_each_missing_condition(self):
        cases = (
            ("live owner", {}, {"kill": None}, "controller may still be alive"),
            ("unprobeable owner", {}, {"kill": PermissionError}, "controller may still be alive"),
            ("missing owner", {"owner_pid": None}, {}, "controller may still be alive"),
            ("group present", {}, {"killpg": None}, "still exists"),
            ("children present", {}, {"children_gone": False}, "Owned child shutdown remains uncertain"),
            ("children unrecorded", {"owned_children": None}, {}, "Owned child shutdown remains uncertain"),
            ("children claimed gone but present", {"owned_children_gone": True}, {"children_gone": False},
             "Owned child shutdown remains uncertain"),
            ("wrong phase", {"phase": "held"}, {}, "Resolve the retained provider request"),
            ("no phase", {"phase": None}, {}, "Resolve the retained provider request"),
            ("provider not completed", {"provider_completed": False}, {}, "lacks a completed"),
            ("non context-aware route", {"route": "cli"}, {}, "lacks a completed"),
            ("different project", {"project": "/elsewhere"}, {}, "different work"),
        )
        for route in self.ROUTES:
            for name, provider_changes, probes, pattern in cases:
                with self.subTest(route=route, case=name):
                    self.lost_after_receipt(route, **provider_changes)
                    self.children_gone.return_value = probes.get("children_gone", True)
                    kill = patch.object(roll.os, "kill", side_effect=probes.get("kill", ProcessLookupError))
                    killpg = patch.object(roll.os, "killpg", side_effect=probes.get("killpg", ProcessLookupError))
                    with kill, killpg:
                        self.assert_receipt_refused(pattern)

    def test_receipt_recovery_refuses_bad_prepared_state_or_missing_reason(self):
        for route in self.ROUTES:
            for name, prepared, reason, pattern in (
                    ("erased failures", {**self.prepared, "failures": {}}, "Inspected", "failure counts"),
                    ("pending jobs", {**self.prepared, "pending_jobs": [{"id": "job-1"}]}, "Inspected", "Pending jobs"),
                    ("protected evidence", {**self.prepared, "evidence": ["result.txt", "place.json"]},
                     "Inspected", "cannot count"),
                    ("no reason", self.prepared, " ", "inspected cause")):
                with self.subTest(route=route, case=name):
                    self.lost_after_receipt(route)
                    self.ask.save(self.root / "prepared.json", prepared)
                    with patch.object(roll.os, "kill", side_effect=ProcessLookupError):
                        self.assert_receipt_refused(pattern, reason)

    def test_running_ledger_without_receipt_is_still_refused(self):
        for status in ("running", "failed", "abandoned", "completed"):
            with self.subTest(status=status):
                self.lost_after_receipt("claude-stream-json", status=status, phase=None)
                with patch.object(roll.os, "kill", side_effect=ProcessLookupError):
                    self.assert_receipt_refused("Resolve the retained provider request")

    def test_uncertain_ledger_with_receipt_keeps_existing_refusal(self):
        self.lost_after_receipt("claude-stream-json")
        self.prior["status"] = "uncertain"
        self.ask.save(self.roller.ledger, self.prior)
        with patch.object(roll.os, "kill", side_effect=ProcessLookupError):
            self.assert_receipt_refused("Resolve the retained provider request")

    def test_reused_leader_with_different_start_time_allows_recovery(self):
        self.lost_after_receipt("claude-stream-json", process_start=self.START)
        with patch.object(roll.os, "kill", side_effect=ProcessLookupError), \
             patch.object(roll.os, "killpg", return_value=None) as group_probe, \
             patch.object(roll, "process_start", return_value="Tue Sep 15 17:30:00 2026") as start, \
             patch.object(roll.os, "getpgid", return_value=123456789):
            self.assertEqual(self.recover()["status"], "paused")
        start.assert_called_once_with(123456789)
        # Only the existence probe; the reused PID is never signalled.
        self.assertEqual(group_probe.call_args_list, [call(123456789, 0)])
        self.assertEqual(self.ask.read(self.root / "place.json"), self.prepared)

    def test_leader_start_time_refusals(self):
        for name, recorded, current, group in (
                ("same start time", self.START, self.START, 123456789),
                ("no recorded start", None, "Tue Sep 15 17:30:00 2026", 123456789),
                ("unreadable current start", self.START, "", 123456789),
                ("reused pid not leading its group", self.START, "Tue Sep 15 17:30:00 2026", 1)):
            with self.subTest(case=name):
                self.lost_after_receipt("claude-stream-json", process_start=recorded)
                with patch.object(roll.os, "kill", side_effect=ProcessLookupError), \
                     patch.object(roll.os, "killpg", return_value=None), \
                     patch.object(roll, "process_start", return_value=current), \
                     patch.object(roll.os, "getpgid", return_value=group):
                    self.assert_receipt_refused("still exists")

    def test_reused_leader_exception_does_not_apply_outside_receipt_path(self):
        self.save_provider(owned_children_gone=True, process_start=self.START)
        with patch.object(roll.os, "killpg", return_value=None), \
             patch.object(roll, "process_start", return_value="Tue Sep 15 17:30:00 2026"), \
             patch.object(roll.os, "getpgid", return_value=123456789):
            with self.assertRaisesRegex(roll.RollError, "still exists"):
                self.recover()
        self.assert_unchanged()


if __name__ == "__main__":
    unittest.main()
