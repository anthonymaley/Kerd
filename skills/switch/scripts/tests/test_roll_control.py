"""Live command parsing and cancellation using an actual open pipe, no providers."""
import json
import os
from pathlib import Path
import queue
import sys
import unittest
from unittest.mock import Mock, patch
import roll_control

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from roll_control import LiveControl, ControlEnded
import handoff
import test_roll


class LiveControlTests(unittest.TestCase):
    def setUp(self):
        incoming, outgoing = os.pipe()
        self.reader = os.fdopen(incoming)
        self.writer = os.fdopen(outgoing, "w", buffering=1)
        self.events = queue.Queue()
        self.control = LiveControl(self.reader, self.events.put)
        self.control.start()
        self.event("connected")
        self.addCleanup(self.cleanup)

    def cleanup(self):
        self.writer.close()
        self.control.reader.join(timeout=2)
        self.reader.close()

    def event(self, status):
        value = self.events.get(timeout=2)
        self.assertEqual(value["status"], status)
        return value

    def send(self, **value):
        self.writer.write(json.dumps(value) + "\n")

    def test_to_requests_checkpoint_and_retains_exact_target(self):
        command = dict(action="to", branch="trial", destination="/tmp/destination",
                       message="Save", files=["place.json", "artifact.txt"])
        self.send(**command)
        self.event("received")
        self.assertTrue(self.control.checkpoint_requested.is_set())
        self.assertEqual(self.control.boundary(), command)
        self.event("handoff_pending")

    def test_unknown_authority_fields_rejected_without_checkpoint(self):
        self.send(action="to", force=True)
        self.event("rejected")
        self.assertFalse(self.control.checkpoint_requested.is_set())
        self.assertIsNone(self.control.boundary())

    def test_other_device_path_is_retained_without_local_resolution(self):
        self.send(action="to", pickup="on_destination", destination="/another-device/project",
                  branch="trial", message="Save", files=["place.json"])
        self.event("received")
        self.assertEqual(self.control.boundary()["destination"], "/another-device/project")

    def test_relative_other_device_path_is_rejected(self):
        self.send(action="to", pickup="on_destination", destination="project",
                  branch="trial", message="Save", files=["place.json"])
        self.event("rejected")
        self.assertIsNone(self.control.boundary())

    def test_abandon_is_visible_before_boundary_consumes_it(self):
        self.send(action="abandon")
        self.event("received")
        with self.assertRaises(ControlEnded):
            self.control.ensure_connected()
        with self.assertRaises(ControlEnded):
            self.control.wait_for_recovery("failed save")

    def test_eof_stops_dispatch_without_needing_boundary(self):
        self.writer.close()
        self.control.reader.join(timeout=2)
        with self.assertRaises(ControlEnded):
            self.control.ensure_connected()

    def test_retry_only_applies_to_failed_save(self):
        self.send(action="retry")
        self.event("received")
        self.assertIsNone(self.control.boundary())
        self.event("rejected")
        self.send(action="retry")
        self.event("received")
        self.control.wait_for_recovery("injected failure")
        self.assertFalse(self.control.stopping.is_set())


class ControlledLoopTests(unittest.TestCase):
    state = test_roll.RollLifecycleTests.state
    write_place = test_roll.RollLifecycleTests.write_place
    read_place = test_roll.RollLifecycleTests.read_place
    result = test_roll.RollLifecycleTests.result
    ledger = test_roll.RollLifecycleTests.ledger

    def setUp(self):
        test_roll.RollLifecycleTests.setUp(self)
        for key, value in (("user.name", "Trial"), ("user.email", "trial@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
            handoff.git(self.root, "config", key, value)
        handoff.git(self.root, "add", ".")
        handoff.git(self.root, "commit", "-qm", "Initial")
        self.bridge.context_aware = True
        self.bridge._held = None
        self.control = LiveControl(emit=Mock())
        def release(abandon=False):
            result = dict(self.bridge._held, status="cancelled" if abandon else "completed")
            self.bridge._held = None
            return result
        self.bridge.release_held = Mock(side_effect=release)

    def hold(self, state, number):
        self.bridge._held = self.result(state, number, status="running", phase="held")
        return self.bridge._held

    def test_no_move_still_releases_and_automatically_continues(self):
        def outcome(number):
            (self.root / "result.txt").write_text(f"Result {number}")
            return self.hold(self.state(memory=f"Piece {number}", status="continue" if number == 1 else "review"), number)
        self.bridge.outcome = outcome
        result = self.roller.run(control=self.control)
        self.assertEqual(result["status"], "review")
        self.assertEqual(len(self.bridge.calls), 2)
        self.assertEqual(self.bridge.release_held.call_count, 2)
        self.assertTrue(all(call[1]["hold"] for call in self.bridge.calls))

    def test_disconnected_caller_never_dispatches(self):
        self.control.stopping.set()
        with self.assertRaises(ControlEnded):
            self.roller.run(control=self.control)
        self.assertEqual(self.bridge.calls, [])

    def test_cancel_at_boundary_abandons_owned_source_and_stops_loop(self):
        def outcome(number):
            self.control.stopping.set()
            return self.hold(self.state(memory="Safe boundary"), number)
        self.bridge.outcome = outcome
        with self.assertRaises(ControlEnded):
            self.roller.run(control=self.control)
        self.bridge.release_held.assert_called_once_with(abandon=True)
        self.assertEqual(len(self.bridge.calls), 1)
        self.assertEqual(self.ledger()["status"], "uncertain")

    def test_review_returns_without_fabricating_destination(self):
        self.control.pending = {"action": "to"}
        self.bridge.outcome = lambda number: self.hold(self.state(status="review"), number)
        self.assertEqual(self.roller.run(control=self.control)["status"], "review")
        self.assertTrue(any(call.args[0]["status"] == "handoff_not_performed" for call in self.control.emit.call_args_list))

    def test_relinquished_source_never_automatically_restarts(self):
        for status in ("awaiting_destination", "handed_off"):
            self.roller.transport.save(self.roller.ledger, {"status": status})
            with self.assertRaisesRegex(test_roll.roll.RollError, "relinquished"):
                self.roller.run(control=self.control)
        self.assertEqual(self.bridge.calls, [])

    def test_other_device_save_releases_without_any_destination_probe(self):
        self.control.pending = dict(action="to", pickup="on_destination", branch="trial",
            destination="/another-device/project", files=["place.json"], message="Save")
        transfer = Mock()
        transfer.result = {"status": "completed"}
        transfer.save_and_release.return_value = {"commit": "a" * 40, "source_session_exited": True}
        with patch.object(roll_control, "ManagedTo", return_value=transfer), \
             patch.object(handoff, "root_for", side_effect=AssertionError("Foreign path probed")), \
             patch.object(handoff, "git", return_value="git@example:repo") as git:
            moved = self.control.handoff(self.roller, self.initial, b"agreement", {})
        transfer.save_and_release.assert_called_once()
        transfer.prepare_destination.assert_not_called()
        git.assert_called_once_with(self.root, "remote", "get-url", "origin")
        self.assertEqual(moved["pickup"], "on_destination")
        self.assertNotIn("packet", moved)
