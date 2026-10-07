"""App-server lifecycle regressions using isolated files and fake protocol streams.

No provider processes, network, installed skills, or live sessions are touched.
"""

import contextlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


SCRIPTS = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapter = load("codex_roll_under_test", SCRIPTS / "codex_roll.py")
ask = load("codex_roll_transport_under_test", SCRIPTS.parents[1] / "conductor/scripts/ask.py")
roll = load("codex_roll_loop_under_test", SCRIPTS / "roll.py")


def usage(used, window=1000, cumulative=90000):
    def breakdown(count):
        return {"totalTokens": count, "inputTokens": count, "outputTokens": 0,
                "cachedInputTokens": 0, "reasoningOutputTokens": 0}
    return {"last": breakdown(used), "total": breakdown(cumulative),
            "modelContextWindow": window}


def event(method, **params):
    return {"method": method, "params": {"threadId": "thread-1", **params}}


def reading(used=100, **params):
    return event("thread/tokenUsage/updated", turnId="turn-1",
                 tokenUsage=usage(used), **params)


def final(turn="turn-1"):
    return event("item/completed", turnId=turn, item={"type": "agentMessage",
                 "id": "final-1", "phase": "final_answer", "text": '{"status":"review"}'})


def completion(turn="turn-1", status="completed"):
    return event("turn/completed", turn={"id": turn, "status": status})


class FakeServer:
    def __init__(self, messages):
        self.messages = iter(messages)
        self.sent = []
        self.counter = 0
        self.proc = types.SimpleNamespace(pid=123456789, stdin=io.StringIO(),
                                         stdout=io.StringIO(), wait=Mock(return_value=0), poll=Mock(return_value=None))
        self.reader = Mock()
        self.reader.is_alive.return_value = False

    def send(self, method, params, notification=False):
        self.sent.append((method, params))
        if not notification:
            self.counter += 1
            return self.counter

    def receive(self):
        try:
            message = next(self.messages)
        except StopIteration:
            raise adapter.ProtocolError("Fixture stream exhausted")
        if isinstance(message, BaseException):
            raise message
        if callable(message):
            return message()
        return message


class ContextWatchTests(unittest.TestCase):
    def test_pressure_uses_last_request_and_not_cumulative_spend(self):
        watch = adapter.ContextWatch()
        self.assertFalse(watch.observe(usage(100, cumulative=90000)))
        self.assertTrue(watch.observe(usage(650, cumulative=90000)))
        self.assertFalse(watch.observe(usage(850)))
        self.assertEqual(watch.trigger["last"]["totalTokens"], 650)
        self.assertEqual(len(watch.readings), 3)

    def test_test_trigger_cannot_delay_normal_pressure_threshold(self):
        watch = adapter.ContextWatch(test_tokens=800)
        self.assertTrue(watch.observe(usage(650)))
        self.assertEqual(watch.trigger["threshold"], 650)

    def test_missing_or_invalid_usage_fails_closed(self):
        for used, window in ((None, 1000), (True, 1000), (-1, 1000), (5, None),
                             (5, 0), (5, True), (5, 1.5)):
            with self.subTest(used=used, window=window):
                with self.assertRaises(adapter.ProtocolError):
                    adapter.ContextWatch().observe(usage(used, window))

    def test_invalid_threshold_options_fail_before_launch(self):
        for fraction in (0, -1, 0.9, float("nan"), float("inf")):
            with self.subTest(fraction=fraction), self.assertRaises(ValueError):
                adapter.ContextWatch(fraction)
        for test_tokens in (0, -1, True, 2.5):
            with self.subTest(test_tokens=test_tokens), self.assertRaises(ValueError):
                adapter.ContextWatch(test_tokens=test_tokens)


class AppServerBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-roll-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.stop = Mock()
        stop = self.stop

        class Core:
            def __init__(self, root):
                self.root = root
                self.state = root / ".git/cross-llm"
                (self.state / "sessions").mkdir(parents=True)
                (self.state / "requests").mkdir()

            def session_path(self, alias):
                return self.state / "sessions" / (alias + ".json")

            def request_path(self, ident):
                return self.state / "requests" / ident

            status = ask.Bridge.status
            resolve = ask.Bridge.resolve
            ensure_resolved = ask.Bridge.ensure_resolved

        Core.stop = staticmethod(stop)
        self.transport = types.SimpleNamespace(Bridge=Core, save=ask.save, read=ask.read, now=ask.now,
                                               shutdown_signals=contextlib.nullcontext,
                                               exclusive=ask.exclusive)
        self.bridge = adapter.AppServerBridge(self.root, self.transport)
        self.descendants = self.enterContext(patch.object(adapter, "descendants", return_value={}))
        self.children_gone = self.enterContext(patch.object(adapter, "children_gone", return_value=True))
        self.group_probe = self.enterContext(patch.object(adapter.os, "killpg", side_effect=ProcessLookupError))
        self.stop_children = self.enterContext(patch.object(adapter, "stop_owned_children"))
        self.enterContext(patch.object(adapter.time, "sleep"))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    def prefix(self, **changes):
        result = {"thread": {"id": "thread-1"}, "model": "chosen-model",
                  "approvalPolicy": "never", "cwd": str(self.root),
                  "sandbox": {"type": "workspaceWrite", "writableRoots": [str(self.root)],
                              "networkAccess": False, "excludeTmpdirEnvVar": True,
                              "excludeSlashTmp": True}}
        result.update(changes)
        return [{"id": 1, "result": {}}, {"id": 2, "result": result},
                {"id": 3, "result": {"turn": {"id": "turn-1"}}}]

    def run_stream(self, messages, **kwargs):
        self.server = FakeServer(messages)
        if hasattr(self, "wait_effect"):
            self.server.proc.wait.side_effect = self.wait_effect
        with patch.object(adapter, "AppServer", return_value=self.server):
            return self.bridge.run("codex", "bounded work", "worker", "fresh-alias", "request-1",
                                   writable=True, model="chosen-model", effort="high", **kwargs)

    def assert_stopped(self):
        self.assertTrue(self.server.proc.stdin.closed)
        self.server.proc.wait.assert_called()
        self.server.reader.join.assert_called()

    def test_live_request_steers_same_turn_once_without_pressure_claim(self):
        result = self.run_stream(self.prefix() + [reading(), {"id": 4, "result": {"turnId": "turn-1"}}, final(), completion()],
                                 checkpoint_requested=lambda: True)
        steers = [params for method, params in self.server.sent if method == "turn/steer"]
        self.assertEqual(len(steers), 1)
        self.assertEqual(steers[0]["expectedTurnId"], "turn-1")
        self.assertIsNone(result.get("context_trigger"))
        self.assertEqual(result["status"], "completed")

    def test_live_request_and_pressure_share_one_checkpoint(self):
        result = self.run_stream(self.prefix() + [reading(700), {"id": 4, "result": {"turnId": "turn-1"}}, final(), completion()],
                                 checkpoint_requested=lambda: True)
        self.assertEqual(sum(method == "turn/steer" for method, _ in self.server.sent), 1)
        self.assertEqual(result["status"], "completed")

    def test_hold_keeps_process_stream_and_alias_lock_until_explicit_release(self):
        result = self.run_stream(self.prefix() + [reading(), final(), completion()], hold=True)
        self.assertEqual((result["status"], result["phase"]), ("running", "held"))
        self.assertNotIn("finished_at", result)
        self.assertFalse(self.server.proc.stdin.closed)
        self.server.proc.wait.assert_not_called()
        self.descendants.assert_not_called()
        with self.assertRaises(ask.Busy):
            with ask.exclusive(self.bridge.core.session_path("fresh-alias").with_suffix(".lock")):
                self.fail("Held alias lock was released")
        with self.assertRaises(adapter.ProtocolError):
            self.bridge.run("codex", "new work", "worker", "other", "other")
        released = self.bridge.release_held()
        self.assertEqual(released["status"], "completed")
        self.assertTrue(released["owned_children_gone"])
        self.assert_stopped()
        with ask.exclusive(self.bridge.core.session_path("fresh-alias").with_suffix(".lock")):
            pass

    def test_hold_inspection_uses_same_idle_thread_without_history(self):
        self.run_stream(self.prefix() + [reading(), final(), completion(),
            {"id": 4, "result": {"thread": {"id": "thread-1", "status": {"type": "idle"}}}}], hold=True)
        self.assertTrue(self.bridge.inspect_held()["source_alive"])
        self.assertEqual(self.server.sent[-1], ("thread/read", {"threadId": "thread-1", "includeTurns": False}))
        self.assertFalse(self.server.proc.stdin.closed)
        self.bridge.release_held(abandon=True)

    def test_bad_hold_inspection_does_not_implicitly_release(self):
        self.run_stream(self.prefix() + [reading(), final(), completion(),
            {"id": 4, "result": {"thread": {"id": "thread-1", "status": {"type": "notLoaded"}}}}], hold=True)
        with self.assertRaises(adapter.ProtocolError):
            self.bridge.inspect_held()
        self.assertFalse(self.server.proc.stdin.closed)
        self.assertEqual(self.bridge.release_held(abandon=True)["status"], "cancelled")

    def test_failed_provider_is_not_held(self):
        result = self.run_stream(self.prefix() + [completion(status="failed")], hold=True)
        self.assertEqual(result["status"], "failed")
        self.assert_stopped()
        with self.assertRaises(adapter.ProtocolError):
            self.bridge.held_result()

    def test_unexpected_held_turn_is_latched_and_later_idle_cannot_clear_it(self):
        self.run_stream(self.prefix() + [reading(), final(), completion(),
            event("turn/started", turn={"id": "unexpected"}),
            {"id": 4, "result": {"thread": {"id": "thread-1", "status": {"type": "idle"}}}}], hold=True)
        with self.assertRaises(adapter.ProtocolError):
            self.bridge.inspect_held()
        self.assertEqual(self.bridge.held_result()["phase"], "held_uncertain")
        with self.assertRaises(adapter.ProtocolError):
            self.bridge.inspect_held()
        with self.assertRaises(adapter.ProtocolError):
            self.bridge.release_held()
        self.assertFalse(self.server.proc.stdin.closed)
        self.bridge.release_held(abandon=True)

    def test_failed_held_metadata_save_keeps_owned_process_and_lock(self):
        original = self.transport.save
        def fail_held(path, value):
            if value.get("phase") == "held":
                raise OSError("fixture disk failure")
            return original(path, value)
        with patch.object(self.transport, "save", side_effect=fail_held):
            with self.assertRaises(OSError):
                self.run_stream(self.prefix() + [reading(), final(), completion()], hold=True)
        self.assertFalse(self.server.proc.stdin.closed)
        self.assertEqual(self.bridge.held_result()["phase"], "held")
        self.bridge.release_held(abandon=True)

    def test_failed_release_does_not_report_success_or_unlock(self):
        self.run_stream(self.prefix() + [reading(), final(), completion()], hold=True)
        self.server.reader.is_alive.return_value = True
        result = self.bridge.release_held()
        self.assertEqual(result["status"], "interrupted")
        self.assertIn("cleanup_error", result)
        with self.assertRaises(ask.Busy):
            with ask.exclusive(self.bridge.core.session_path("fresh-alias").with_suffix(".lock")):
                pass
        # Fixture teardown only: uncertain real release remains a controller stop.
        self.bridge._held_lock.__exit__(None, None, None)
        self.bridge._held_lock = None


    def test_fresh_thread_has_explicit_model_effort_and_authority(self):
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "completed")
        sent = dict(self.server.sent)
        self.assertEqual(sent["thread/start"]["model"], "chosen-model")
        self.assertEqual(sent["thread/start"]["sandbox"], "workspace-write")
        self.assertEqual(sent["thread/start"]["approvalPolicy"], "never")
        self.assertIs(sent["thread/start"]["config"]["features.computer_use"], False)
        self.assertFalse(sent["thread/start"]["allowProviderModelFallback"])
        self.assertEqual(sent["turn/start"]["effort"], "high")
        self.assertEqual(result["usage"]["totalTokens"], 90000)
        self.assert_stopped()
        self.stop.assert_not_called()

    def test_pressure_steers_once_and_waits_for_final_completion(self):
        result = self.run_stream(self.prefix() + [reading(700), reading(800),
            {"id": 4, "result": {"turnId": "turn-1"}}, final(), completion()])
        self.assertEqual(result["status"], "completed")
        steers = [params for method, params in self.server.sent if method == "turn/steer"]
        self.assertEqual(len(steers), 1)
        self.assertEqual(steers[0]["expectedTurnId"], "turn-1")
        self.assertTrue(result["steer_accepted"])
        self.assert_stopped()

    def test_conductor_checkpoint_uses_its_contract_not_worker_schema(self):
        instruction = "Return the decision object with action checkpoint and exact ack."
        result = self.run_stream(self.prefix() + [reading(700),
            {"id": 4, "result": {"turnId": "turn-1"}}, final(), completion()],
            checkpoint_instruction=instruction)
        self.assertEqual(result["status"], "completed")
        steer = next(p for m, p in self.server.sent if m == "turn/steer")
        text = steer["input"][0]["text"]
        self.assertIn(instruction, text)
        self.assertNotIn("Use continue", text)

    def test_reply_is_saved_and_read_back_before_source_shutdown(self):
        original = self.bridge._shutdown
        def inspect(server, record):
            saved = ask.read(self.bridge.state / "requests/request-1/result.json")
            self.assertEqual(saved["phase"], "checkpoint_saved")
            self.assertEqual(saved["status"], "running")
            self.assertEqual(saved["checkpoint_candidates"], [final()["params"]["item"]["text"]])
            original(server, record)
        with patch.object(self.bridge, "_shutdown", side_effect=inspect):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "completed")

    def test_accepted_steer_preserves_same_turn_revised_final_candidates(self):
        revised = final()
        revised["params"]["item"].update(id="final-2", text='{"status":"review","revised":true}')
        result = self.run_stream(self.prefix() + [reading(700), final(),
                {"id": 4, "result": {"turnId": "turn-1"}}, revised, completion()])
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["checkpoint_candidates"], [final()["params"]["item"]["text"],
                                                         revised["params"]["item"]["text"]])
        self.assertEqual(result["reply"], revised["params"]["item"]["text"])

    def test_multiple_finals_without_accepted_steer_are_ambiguous(self):
        revised = final()
        revised["params"]["item"]["id"] = "final-2"
        result = self.run_stream(self.prefix() + [reading(), final(), revised, completion()])
        self.assertEqual(result["status"], "failed")

    def test_accepted_steer_does_not_allow_revision_from_another_turn(self):
        revised = final(turn="other-turn")
        revised["params"]["item"]["id"] = "final-2"
        result = self.run_stream(self.prefix() + [reading(700), final(),
                {"id": 4, "result": {"turnId": "turn-1"}}, revised, completion()])
        self.assertEqual(result["status"], "failed")

    def test_natural_completion_can_precede_rejected_steer_response(self):
        result = self.run_stream(self.prefix() + [reading(700), final(), completion(),
                {"id": 4, "error": {"code": -32000, "message": "turn already completed"}}])
        self.assertEqual(result["status"], "completed")
        self.assertIn("steer_race", result)
        self.assert_stopped()

    def test_turn_notification_and_usage_can_precede_start_response(self):
        prefix = self.prefix()
        result = self.run_stream(prefix[:2] + [event("turn/started", turn={"id": "turn-1"}),
                reading(700), prefix[2], {"id": 4, "result": {"turnId": "turn-1"}},
                final(), completion()])
        self.assertEqual(result["status"], "completed")
        self.assert_stopped()

    def test_steer_for_another_turn_cannot_confirm_saved_place(self):
        result = self.run_stream(self.prefix() + [reading(700),
                {"id": 4, "result": {"turnId": "other-turn"}}, final(), completion()])
        self.assertNotEqual(result["status"], "completed")

    def test_second_turn_notification_cannot_replace_owned_turn(self):
        result = self.run_stream(self.prefix() + [event("turn/started", turn={"id": "other-turn"}),
                event("thread/tokenUsage/updated", turnId="other-turn", tokenUsage=usage(100)),
                final(turn="other-turn"), completion(turn="other-turn")])
        self.assertNotEqual(result["status"], "completed")

    def test_delayed_start_response_cannot_change_notified_turn(self):
        prefix = self.prefix()
        prefix[2]["result"]["turn"]["id"] = "other-turn"
        result = self.run_stream(prefix[:2] + [event("turn/started", turn={"id": "turn-1"}),
                                 reading(), prefix[2], final(turn="other-turn"),
                                 completion(turn="other-turn")])
        self.assertNotEqual(result["status"], "completed")
        self.assert_stopped()

    def test_observed_pressure_is_durable_while_worker_still_runs(self):
        def inspect_running_record():
            retained = self.bridge.core.status("request-1")
            self.assertEqual(retained["status"], "running")
            self.assertEqual(retained["context_trigger"]["last"]["totalTokens"], 700)
            self.assertEqual(len(retained["context_readings"]), 1)
            return {"id": 4, "result": {"turnId": "turn-1"}}
        result = self.run_stream(self.prefix() + [reading(700), inspect_running_record,
                                 final(), completion()])
        self.assertEqual(result["status"], "completed")

    def test_compaction_prevents_success_and_stops_owned_process(self):
        result = self.run_stream(self.prefix() + [reading(), event("item/started", turnId="turn-1",
                                                item={"type": "contextCompaction", "id": "compact"})])
        self.assertEqual(result["status"], "failed")
        self.assertIn("compaction", result["error"])
        self.assert_stopped()

    def test_model_reroute_prevents_success(self):
        result = self.run_stream(self.prefix() + [event("model/rerouted", turnId="turn-1")])
        self.assertEqual(result["status"], "failed")
        self.assert_stopped()

    def test_usage_for_another_turn_is_rejected(self):
        result = self.run_stream(self.prefix() + [event("thread/tokenUsage/updated",
                                                turnId="other-turn", tokenUsage=usage(100))])
        self.assertEqual(result["status"], "failed")
        self.assert_stopped()

    def test_an_unknown_phase_is_not_a_final_response_either(self):
        """Same rule as Agent: a renamed or additional phase must not be read
        as the answer just because it is not literally 'commentary'."""
        odd = event("item/completed", turnId="turn-1", item={"type": "agentMessage",
                    "id": "odd", "phase": "analysis", "text": '{"status":"wrong"}'})
        result = self.run_stream(self.prefix() + [reading(), odd, final(), completion()])
        self.assertNotIn("wrong", json.dumps(result))

    def test_commentary_is_not_a_final_response(self):
        commentary = event("item/completed", turnId="turn-1", item={"type": "agentMessage",
                           "id": "commentary", "phase": "commentary", "text": "Working"})
        result = self.run_stream(self.prefix() + [reading(), commentary, final(), completion()])
        self.assertEqual(result["status"], "completed")
        self.assertNotIn("Working", json.dumps(result))

    def test_no_usage_cannot_prove_context_aware_completion(self):
        result = self.run_stream(self.prefix() + [final(), completion()])
        self.assertEqual(result["status"], "failed")
        self.assertIn("No context readings", result["error"])

    def test_cancel_file_stops_owned_process(self):
        def cancel():
            ask.save(self.bridge.core.request_path("request-1") / "cancel.json", {})
            return {}
        result = self.run_stream(self.prefix() + [cancel])
        self.assertEqual(result["status"], "cancelled")
        self.assert_stopped()

    def test_keyboard_interrupt_stops_owned_process(self):
        result = self.run_stream(self.prefix() + [KeyboardInterrupt()])
        self.assertEqual(result["status"], "cancelled")
        self.assert_stopped()

    def test_optional_timeout_stops_without_issuing_a_turn(self):
        with patch.object(adapter.time, "monotonic", side_effect=itertools.count(step=2)):
            result = self.run_stream(self.prefix(), timeout=1)
        self.assertNotEqual(result["status"], "completed")
        self.assertNotIn("turn/start", dict(self.server.sent))
        self.assert_stopped()

    def test_cleanup_error_invalidates_completed_result(self):
        self.wait_effect = [adapter.subprocess.TimeoutExpired("fake-app-server", 5)]
        self.stop.side_effect = OSError("cannot confirm cleanup")
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.stop.assert_called_once_with(self.server.proc)

    def test_signal_fallback_after_eof_timeout_reaps_parent(self):
        self.wait_effect = [adapter.subprocess.TimeoutExpired("fake-app-server", 5), 0]
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "completed")
        self.stop.assert_called_once_with(self.server.proc)
        self.assertEqual(self.server.proc.wait.call_count, 2)
        self.assert_stopped()

    def test_second_wait_timeout_cannot_report_clean_shutdown(self):
        self.wait_effect = [adapter.subprocess.TimeoutExpired("fake-app-server", 5)] * 2
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.stop.assert_called_once_with(self.server.proc)

    def test_surviving_detached_child_prevents_clean_completion(self):
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.return_value = False
        with patch.object(adapter.time, "monotonic", side_effect=itertools.count(step=10)):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.assertIn("child", result["cleanup_error"])
        self.assertFalse(result.get("owned_children_gone", False))
        self.children_gone.assert_called_with(self.descendants.return_value)
        self.stop_children.assert_called_once_with(self.descendants.return_value)
        self.assert_stopped()

    def test_verified_survivor_shutdown_can_finish_before_second_deadline(self):
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.side_effect = [False, True]
        with patch.object(adapter.time, "monotonic", side_effect=itertools.count(step=10)):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["owned_survivor_shutdown_requested"])
        self.assertTrue(result["owned_children_gone"])
        self.stop_children.assert_called_once_with(self.descendants.return_value)
        self.stop.assert_not_called()
        self.assert_stopped()

    def test_verified_survivor_shutdown_permission_error_blocks_continuation(self):
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.return_value = False
        self.stop_children.side_effect = adapter.ProtocolError("Cannot stop verified owned child")
        with patch.object(adapter.time, "monotonic", side_effect=itertools.count(step=10)):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.stop_children.assert_called_once_with(self.descendants.return_value)
        self.assert_stopped()

    def test_descendant_snapshot_failure_still_stops_owned_parent(self):
        self.descendants.side_effect = OSError("cannot snapshot descendants")
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.assert_stopped()

    def test_descendant_inspection_failure_blocks_completion_after_parent_stop(self):
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.side_effect = adapter.ProtocolError("cannot inspect child")
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.assert_stopped()

    def test_disappearing_children_are_confirmed_before_clean_completion(self):
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.side_effect = [False, True]
        with patch.object(adapter.time, "sleep"):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["owned_children_gone"])
        self.assertEqual(self.children_gone.call_count, 2)
        self.assert_stopped()

    def test_present_group_can_disappear_during_bounded_observation(self):
        self.group_probe.side_effect = [None, ProcessLookupError()]
        with patch.object(adapter.time, "sleep"):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["owned_children_gone"])
        self.assertEqual(self.group_probe.call_count, 2)
        self.assertTrue(all(call.args == (self.server.proc.pid, 0)
                            for call in self.group_probe.call_args_list))
        self.stop.assert_not_called()
        self.assert_stopped()

    def test_group_probe_permission_error_is_not_confirmed_absence(self):
        self.group_probe.side_effect = PermissionError("observation denied")
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.assertIn("Cannot inspect owned process group", result["cleanup_error"])
        self.group_probe.assert_called_once_with(self.server.proc.pid, 0)
        self.stop.assert_not_called()
        self.assert_stopped()

    def test_persistent_group_times_out_without_sending_termination_signal(self):
        self.group_probe.side_effect = None
        with patch.object(adapter.time, "monotonic", side_effect=itertools.count(step=10)):
            result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        self.assertFalse(result["provider_completed"])
        self.assertIn("process group is still present", result["cleanup_error"])
        self.assertFalse(result.get("owned_children_gone", False))
        self.assertTrue(all(call.args == (self.server.proc.pid, 0)
                            for call in self.group_probe.call_args_list))
        self.stop.assert_not_called()
        self.stop_children.assert_called_once_with({})
        self.assert_stopped()

    def test_existing_alias_rejected_before_launch(self):
        ask.save(self.bridge.core.session_path("fresh-alias"), {"closed": True})
        with patch.object(adapter, "AppServer") as factory:
            with self.assertRaisesRegex(adapter.ProtocolError, "fresh alias"):
                self.bridge.run("codex", "work", "worker", "fresh-alias", "request-1",
                                model="chosen-model", effort="high")
            factory.assert_not_called()

    def test_session_lock_stays_held_while_provider_runs(self):
        def inspect_lock():
            with self.assertRaises(ask.Busy):
                with ask.exclusive(self.bridge.core.session_path("fresh-alias").with_suffix(".lock")):
                    pass
            return final()
        result = self.run_stream(self.prefix() + [reading(), inspect_lock, completion()])
        self.assertEqual(result["status"], "completed")
        with ask.exclusive(self.bridge.core.session_path("fresh-alias").with_suffix(".lock")):
            pass

    def test_unresolved_request_blocks_alias_even_without_session_file(self):
        old = self.bridge.core.request_path("older-request")
        old.mkdir()
        ask.save(old / "request.json", {"session": "fresh-alias"})
        ask.save(old / "result.json", {"status": "interrupted"})
        with patch.object(adapter, "AppServer") as factory:
            with self.assertRaises(ask.Busy):
                self.bridge.run("codex", "work", "worker", "fresh-alias", "request-1",
                                model="chosen-model", effort="high")
            factory.assert_not_called()

    def test_wrong_effective_model_rejected_before_turn_start(self):
        result = self.run_stream(self.prefix(model="different-model") + [reading(), final(), completion()])
        self.assertNotEqual(result["status"], "completed")
        self.assertNotIn("turn/start", dict(self.server.sent))

    def test_wider_effective_sandbox_rejected_before_turn_start(self):
        result = self.run_stream(self.prefix(sandbox={"type": "dangerFullAccess"}) +
                                 [reading(), final(), completion()])
        self.assertNotEqual(result["status"], "completed")
        self.assertNotIn("turn/start", dict(self.server.sent))

    def test_final_message_for_another_turn_is_rejected(self):
        result = self.run_stream(self.prefix() + [reading(), final(turn="other-turn"), completion()])
        self.assertNotEqual(result["status"], "completed")

    def test_live_reader_after_cleanup_is_not_a_clean_completion(self):
        def final_with_live_reader():
            self.server.reader.is_alive.return_value = True
            return final()
        result = self.run_stream(self.prefix() + [reading(), final_with_live_reader, completion()])
        self.assertNotEqual(result["status"], "completed")

    def test_request_metadata_supports_unknown_result_inspection(self):
        self.run_stream(self.prefix() + [reading(), final(), completion()])
        folder = self.bridge.core.request_path("request-1")
        # Simulate an interrupted first result write, entirely within this fixture.
        (folder / "result.json").unlink()
        result = self.bridge.core.status("request-1")
        self.assertIn(result["status"], {"unknown", "failed", "starting", "interrupted"})

    def test_interrupted_request_can_use_transport_resolution(self):
        self.wait_effect = [adapter.subprocess.TimeoutExpired("fake-app-server", 5)]
        self.stop.side_effect = OSError("cleanup uncertain")
        result = self.run_stream(self.prefix() + [reading(), final(), completion()])
        self.assertEqual(result["status"], "interrupted")
        with patch.object(ask.os, "killpg", side_effect=ProcessLookupError):
            resolved = self.bridge.core.resolve("request-1")
        self.assertEqual(resolved["status"], "abandoned")


class CheckpointCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-roll-candidate-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.initial = {"status": "continue", "next_action": "Finish result", "memory": "Original",
                        "failures": {"quality": 1}, "evidence": ["result.txt"], "pending_jobs": []}
        (self.root / "agreement.md").write_text("Build local result")
        (self.root / "result.txt").write_text("existing evidence")
        (self.root / "extra.txt").write_text("additional evidence")
        ask.save(self.root / "place.json", self.initial)
        bridge = types.SimpleNamespace(root=self.root, state=self.root / ".git/cross-llm",
                                       run=Mock(), close=Mock(), context_aware=True)
        bridge.state.mkdir(parents=True)
        self.enterContext(patch.object(roll, "connection", return_value=ask))
        self.enterContext(patch.object(roll, "group_gone", return_value=True))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))
        self.roller = roll.Roller(self.root, "agreement.md", "place.json", "codex", "chosen-model",
                                  "high", bridge=bridge)
        self.bridge = bridge

    def candidate(self, **changes):
        value = {**self.initial, "status": "review", "memory": "Result ready"}
        value.update(changes)
        return value

    def result(self, candidates):
        replies = [json.dumps(value) if isinstance(value, dict) else value for value in candidates]
        self.bridge.run.return_value = {"status": "completed", "session_id": "thread-1",
                                        "reply": replies[-1], "checkpoint_candidates": replies}

    def assert_rejected_without_saving(self, pattern):
        with self.assertRaisesRegex(roll.RollError, pattern):
            self.roller.run()
        self.assertEqual(ask.read(self.root / "place.json"), self.initial)
        self.assertEqual(ask.read(self.roller.ledger)["status"], "uncertain")
        self.bridge.close.assert_not_called()

    def test_last_valid_revision_is_saved_and_identical_candidates_are_skipped(self):
        first = self.candidate()
        revised = self.candidate(memory="Revised checkpoint", failures={"quality": 2},
                                 evidence=["result.txt", "extra.txt"])
        self.result([first, first, revised])
        self.assertEqual(self.roller.run()["status"], "review")
        self.assertEqual(ask.read(self.root / "place.json"), revised)

    def test_revision_cannot_erase_failure_count_added_by_first_final(self):
        self.result([self.candidate(failures={"quality": 2}), self.candidate()])
        self.assert_rejected_without_saving("failure counts")

    def test_revision_cannot_erase_evidence_added_by_first_final(self):
        self.result([self.candidate(evidence=["result.txt", "extra.txt"]), self.candidate()])
        self.assert_rejected_without_saving("evidence references")

    def test_valid_last_candidate_cannot_hide_malformed_earlier_candidate(self):
        self.result(["not saved-place JSON", self.candidate()])
        self.assert_rejected_without_saving("unambiguous")

    def test_valid_last_candidate_cannot_hide_invalid_earlier_failure_count(self):
        self.result([self.candidate(failures={"quality": -1}), self.candidate()])
        self.assert_rejected_without_saving("nonnegative")


class RecoveryTests(unittest.TestCase):
    candidate = CheckpointCandidateTests.candidate

    def setUp(self):
        CheckpointCandidateTests.setUp(self)
        self.enterContext(patch.dict(sys.modules, {"codex_roll": adapter}))
        self.probe = self.enterContext(patch.object(roll.os, "killpg", side_effect=ProcessLookupError))
        self.prior = {"status": "uncertain", "agreement": "agreement.md", "place": "place.json",
                      "request_id": "failed-request", "error": "original failure", "target": "codex",
                      "history": [], "artifact_snapshots": [self.roller.artifact_snapshot(self.initial)]}
        ask.save(self.roller.ledger, self.prior)
        self.request = self.bridge.state / "requests/failed-request"
        self.request.mkdir(parents=True)
        self.provider = {"status": "abandoned", "process_id": 123456789, "session_id": "retired-session",
                         "request_id": "failed-request", "project": str(self.root), "target": "codex",
                         "owned_children_gone": True, "route": "app-server-stdio"}
        self.save_provider()
        self.prepared = self.candidate(status="continue", memory="Inspected failed operation",
                                        failures={"quality": 2})
        ask.save(self.root / "prepared.json", self.prepared)

    def save_provider(self, **changes):
        self.provider.update(changes)
        ask.save(self.request / "result.json", self.provider)

    def recover(self):
        return self.roller.recover("prepared.json", "Inspected cause; prior jobs have ended")

    def assert_unchanged(self):
        self.assertEqual(ask.read(self.root / "place.json"), self.initial)
        self.assertEqual(ask.read(self.roller.ledger), self.prior)
        self.bridge.run.assert_not_called()

    def test_recovery_retains_cause_request_original_place_and_retired_identity(self):
        retained_provider = (self.request / "result.json").read_bytes()
        self.assertEqual(self.recover()["status"], "paused")
        ledger = ask.read(self.roller.ledger)
        self.assertEqual(ledger["error"], "original failure")
        self.assertEqual(ledger["request_id"], "failed-request")
        self.assertEqual(ledger["recoveries"][0]["previous_place"], self.initial)
        self.assertEqual(ledger["recoveries"][0]["previous_error"], "original failure")
        self.assertEqual(ledger["retired_sessions"], ["retired-session"])
        self.assertEqual((self.request / "result.json").read_bytes(), retained_provider)
        self.assertEqual(ask.read(self.root / "place.json"), self.prepared)
        self.bridge.run.assert_not_called()

    def test_uncertain_or_running_provider_cannot_be_recovered(self):
        for status in ("running", "starting", "unknown", "interrupted"):
            with self.subTest(status=status):
                self.save_provider(status=status)
                with self.assertRaises(roll.RollError):
                    self.recover()
                self.assert_unchanged()

    def test_live_former_process_group_blocks_recovery(self):
        self.probe.side_effect = None
        with self.assertRaisesRegex(roll.RollError, "still exists"):
            self.recover()
        self.assert_unchanged()

    def test_recovery_cannot_erase_saved_failure_counts_or_evidence(self):
        for changes in ({"failures": {}}, {"evidence": []}):
            with self.subTest(changes=changes):
                ask.save(self.root / "prepared.json", {**self.prepared, **changes})
                with self.assertRaises(roll.RollError):
                    self.recover()
                self.assert_unchanged()

    def test_recovery_cannot_dispatch_with_unresolved_pending_jobs(self):
        ask.save(self.root / "prepared.json", {**self.prepared, "pending_jobs": [{"id": "job-1"}]})
        with self.assertRaisesRegex(roll.RollError, "Pending jobs"):
            self.recover()
        self.assert_unchanged()

    def test_recovery_cannot_use_protected_file_as_build_evidence(self):
        ask.save(self.root / "prepared.json", {**self.prepared, "evidence": ["result.txt", "place.json"]})
        with self.assertRaisesRegex(roll.RollError, "cannot count"):
            self.recover()
        self.assert_unchanged()

    def test_retired_provider_session_cannot_be_reused_after_recovery(self):
        self.recover()
        self.bridge.run.return_value = {"status": "completed", "session_id": "retired-session",
                                        "reply": json.dumps(self.candidate(failures={"quality": 2}))}
        with self.assertRaisesRegex(roll.RollError, "Fresh session"):
            self.roller.run()
        self.assertEqual(ask.read(self.root / "place.json"), self.prepared)
        self.assertEqual(ask.read(self.roller.ledger)["retired_sessions"], ["retired-session"])

    def test_recovery_provenance_survives_successful_fresh_run(self):
        self.recover()
        self.bridge.run.return_value = {"status": "completed", "session_id": "new-session",
                                        "reply": json.dumps(self.candidate(failures={"quality": 2}))}
        self.assertEqual(self.roller.run()["status"], "review")
        self.assertEqual(ask.read(self.roller.ledger)["recoveries"][0]["previous_error"], "original failure")

    def test_failed_recovery_ledger_write_keeps_old_checkpoint_recoverable(self):
        original_save = ask.save

        def fail_ledger(path, value):
            if path == self.roller.ledger:
                raise OSError("recovery ledger write failed")
            return original_save(path, value)

        with patch.object(ask, "save", side_effect=fail_ledger):
            with self.assertRaisesRegex(OSError, "ledger write failed"):
                self.recover()
        self.assertEqual(ask.read(self.roller.ledger)["status"], "uncertain")
        self.bridge.run.assert_not_called()
        # Recovery must either preserve the old place or retain a durable before-image.
        retained = [ask.read(self.root / "place.json")]
        retained.extend(ask.read(path) for path in self.roller.local.rglob("*.json"))
        self.assertTrue(any(value == self.initial or self.initial in
                            [entry.get("previous_place") for entry in value.get("recoveries", [])]
                            for value in retained), "Old checkpoint lost when recovery ledger write failed")

    def test_failed_final_recovery_commit_retains_before_image_and_blocks_dispatch(self):
        original_save = ask.save
        ledger_writes = 0

        def fail_final_ledger(path, value):
            nonlocal ledger_writes
            if path == self.roller.ledger:
                ledger_writes += 1
                if ledger_writes == 2:
                    raise OSError("final recovery commit failed")
            return original_save(path, value)

        with patch.object(ask, "save", side_effect=fail_final_ledger):
            with self.assertRaisesRegex(OSError, "final recovery commit failed"):
                self.recover()
        ledger = ask.read(self.roller.ledger)
        self.assertEqual(ledger["status"], "uncertain")
        self.assertEqual(ledger["recoveries"][0]["previous_place"], self.initial)
        self.assertEqual(ask.read(self.root / "place.json"), self.prepared)
        with self.assertRaisesRegex(roll.RollError, "Previous Roll"):
            self.roller.run()
        self.bridge.run.assert_not_called()

    def test_abandoned_provider_with_uncleared_detached_child_is_not_recoverable(self):
        self.save_provider(owned_children_gone=False,
                           cleanup_error="Owned detached child is still present; no fresh worker may start")
        with self.assertRaises(roll.RollError):
            self.recover()
        self.assert_unchanged()

    def test_persisted_child_identities_are_rechecked_before_recovery(self):
        self.save_provider(owned_children_gone=False, owned_children={"987654321": "child-start"})
        with patch.object(adapter, "children_gone", return_value=False) as inspect:
            with self.assertRaises(roll.RollError):
                self.recover()
            inspect.assert_called_once_with({"987654321": "child-start"})
        self.assert_unchanged()

    def test_confirmed_exit_of_persisted_children_allows_inspected_recovery(self):
        self.save_provider(owned_children_gone=False, owned_children={"987654321": "child-start"})
        with patch.object(adapter, "children_gone", return_value=True) as inspect:
            self.assertEqual(self.recover()["status"], "paused")
            inspect.assert_called_once_with({"987654321": "child-start"})
        self.bridge.run.assert_not_called()

    def test_completed_provider_after_roll_validation_failure_has_explicit_recovery(self):
        self.save_provider(status="completed")
        self.assertEqual(self.recover()["status"], "paused")
        self.bridge.run.assert_not_called()

    def test_retained_provider_from_different_project_cannot_authorize_recovery(self):
        self.save_provider(project=str(self.root / "different-project"))
        with self.assertRaises(roll.RollError):
            self.recover()
        self.assert_unchanged()


class OwnedChildShutdownTests(unittest.TestCase):
    def setUp(self):
        self.inspect = self.enterContext(patch.object(adapter.subprocess, "run"))
        self.kill = self.enterContext(patch.object(adapter.os, "kill"))
        self.killpg = self.enterContext(patch.object(adapter.os, "killpg"))
        self.inspect.return_value = types.SimpleNamespace(returncode=0, stdout=" child-stamp \n")

    def test_matching_owned_child_gets_only_sigterm(self):
        adapter.stop_owned_children({"987654321": "child-stamp  "})
        self.kill.assert_called_once_with(987654321, adapter.signal.SIGTERM)
        self.killpg.assert_not_called()

    def test_reused_pid_with_different_start_identity_is_not_signalled(self):
        self.inspect.return_value.stdout = "new-start-stamp"
        adapter.stop_owned_children({987654321: "child-stamp"})
        self.kill.assert_not_called()
        self.killpg.assert_not_called()

    def test_already_disappeared_child_is_not_signalled(self):
        self.inspect.return_value = types.SimpleNamespace(returncode=1, stdout="")
        adapter.stop_owned_children({987654321: "child-stamp"})
        self.kill.assert_not_called()
        self.killpg.assert_not_called()

    def test_permission_failure_is_not_silently_accepted(self):
        self.kill.side_effect = PermissionError("denied")
        with self.assertRaisesRegex(adapter.ProtocolError, "Cannot stop verified"):
            adapter.stop_owned_children({987654321: "child-stamp"})
        self.kill.assert_called_once_with(987654321, adapter.signal.SIGTERM)
        self.killpg.assert_not_called()

    def test_inspection_failure_does_not_authorize_signalling(self):
        self.inspect.return_value = types.SimpleNamespace(returncode=2, stdout="")
        with self.assertRaisesRegex(adapter.ProtocolError, "Cannot verify"):
            adapter.stop_owned_children({987654321: "child-stamp"})
        self.kill.assert_not_called()
        self.killpg.assert_not_called()

    def test_child_disappearing_after_inspection_is_harmless(self):
        self.kill.side_effect = ProcessLookupError()
        adapter.stop_owned_children({987654321: "child-stamp"})
        self.kill.assert_called_once_with(987654321, adapter.signal.SIGTERM)
        self.killpg.assert_not_called()


class ChildIdentityTests(unittest.TestCase):
    def test_snapshot_normalizes_ps_timestamp_padding(self):
        stamp = "Mon Sep  7 10:00:00 2026"
        rows = f"100 1 owner-stamp\n200 100 {stamp}   \t\n"
        with patch.object(adapter.subprocess, "run", return_value=types.SimpleNamespace(stdout=rows)):
            self.assertEqual(adapter.descendants(100), {200: stamp})

    def test_padded_retained_timestamp_cannot_falsely_report_live_child_gone(self):
        stamp = "Mon Sep  7 10:00:00 2026"
        result = types.SimpleNamespace(returncode=0, stdout=f" {stamp}\n")
        with patch.object(adapter.subprocess, "run", return_value=result):
            self.assertFalse(adapter.children_gone({200: f" {stamp}   \t"}))

    def test_descendant_snapshot_includes_nested_children_only(self):
        rows = "1 0 system\n200 100 child-stamp\n100 1 owner-stamp\n300 200 grandchild-stamp\n400 1 unrelated\n"
        with patch.object(adapter.subprocess, "run", return_value=types.SimpleNamespace(stdout=rows)):
            self.assertEqual(adapter.descendants(100), {200: "child-stamp", 300: "grandchild-stamp"})

    def test_same_child_identity_is_still_present(self):
        result = types.SimpleNamespace(returncode=0, stdout=" child-stamp\n")
        with patch.object(adapter.subprocess, "run", return_value=result):
            self.assertFalse(adapter.children_gone({200: "child-stamp"}))

    def test_disappeared_or_reused_pid_is_not_the_owned_child(self):
        for result in (types.SimpleNamespace(returncode=1, stdout=""),
                       types.SimpleNamespace(returncode=0, stdout="new-start-stamp\n")):
            with self.subTest(result=result):
                with patch.object(adapter.subprocess, "run", return_value=result):
                    self.assertTrue(adapter.children_gone({200: "child-stamp"}))

    def test_process_inspection_error_is_not_proof_of_child_exit(self):
        result = types.SimpleNamespace(returncode=2, stdout="")
        with patch.object(adapter.subprocess, "run", return_value=result):
            with self.assertRaises(adapter.ProtocolError):
                adapter.children_gone({200: "child-stamp"})


class AppServerProtocolTests(unittest.TestCase):
    def test_file_worker_disables_computer_use_in_child_startup_only(self):
        with patch.object(adapter.subprocess, "Popen") as popen:
            with patch.object(adapter.threading, "Thread"):
                adapter.AppServer(Path("/isolated-fixture"), io.StringIO())
        self.assertEqual(popen.call_args.args[0],
                         ["codex", "app-server", "--stdio", "--disable", "computer_use"])
        self.assertTrue(popen.call_args.kwargs["start_new_session"])

    def test_malformed_json_stream_reports_error_then_eof(self):
        server = adapter.AppServer.__new__(adapter.AppServer)
        server.messages = adapter.queue.Queue()
        server.proc = types.SimpleNamespace(stdout=io.StringIO("not-json\n"))
        server._read()
        with self.assertRaisesRegex(adapter.ProtocolError, "Invalid app-server stream"):
            server.receive()
        with self.assertRaisesRegex(adapter.ProtocolError, "exited"):
            server.receive()

    def test_host_request_is_rejected_without_granting_authority(self):
        server = adapter.AppServer.__new__(adapter.AppServer)
        server.messages = adapter.queue.Queue()
        server.proc = types.SimpleNamespace(stdin=io.StringIO())
        server.messages.put({"id": "approval-1", "method": "item/commandExecution/requestApproval",
                             "params": {}})
        with self.assertRaisesRegex(adapter.ProtocolError, "decision"):
            server.receive()
        answer = json.loads(server.proc.stdin.getvalue())
        self.assertEqual(answer["id"], "approval-1")
        self.assertIn("error", answer)
        self.assertNotIn("result", answer)


if __name__ == "__main__":
    unittest.main()
