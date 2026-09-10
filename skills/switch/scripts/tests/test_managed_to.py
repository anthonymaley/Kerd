"""Real disposable Git boundaries with a fake already-paused source."""
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import handoff
import managed_to


class ManagedToTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="held-handoff-test-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name).resolve()
        self.root, self.dest, self.remote = [self.folder / x for x in ("source", "dest", "remote.git")]
        handoff.git(self.folder, "init", "--bare", "-q", str(self.remote))
        handoff.git(self.folder, "init", "-q", "-b", "trial", str(self.root))
        for key, value in (("user.name", "Trial"), ("user.email", "trial@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
            handoff.git(self.root, "config", key, value)
        self.previous = dict(status="continue", next_action="Make artifact", memory="Agreed task",
                             evidence=["agreement.md"], failures={"M1": 1}, pending_jobs=[])
        (self.root / "agreement.md").write_text("Make and test the artifact")
        (self.root / "place.json").write_text(json.dumps(self.previous))
        handoff.git(self.root, "add", ".")
        handoff.git(self.root, "commit", "-qm", "Initial")
        handoff.git(self.root, "remote", "add", "origin", str(self.remote))
        handoff.git(self.root, "push", "-qu", "origin", "trial")
        handoff.git(self.folder, "clone", "-q", "--branch", "trial", str(self.remote), str(self.dest))
        (self.root / "artifact.txt").write_text("Useful unfinished work")
        self.after = dict(self.previous, next_action="Test artifact", evidence=["agreement.md", "artifact.txt"])
        self.record = dict(status="running", phase="held", provider_completed=True, reply=json.dumps(self.after))
        self.bridge = types.SimpleNamespace(root=self.root,
            held_result=Mock(side_effect=lambda: self.record), held_cancelled=Mock(return_value=False),
            inspect_held=Mock(return_value={"source_alive": True}),
            release_held=Mock(return_value=dict(status="completed", owned_children_gone=True, process_id=987654321)),
            transport=types.SimpleNamespace(save=lambda path, value: path.write_text(json.dumps(value))))
        self.transfer = managed_to.ManagedTo(self.bridge, "trial", "place.json", self.previous,
            ["place.json", "artifact.txt"], "Save working place", {"agreement.md": (self.root / "agreement.md").read_bytes()})
        self.enterContext(patch.object(managed_to.roll, "group_gone", return_value=True))

    def assert_held(self):
        self.bridge.release_held.assert_not_called()
        self.assertIsNone(self.transfer.receipt)
        before = handoff.git(self.dest, "rev-parse", "HEAD")
        with self.assertRaises(handoff.HandoffError):
            self.transfer.prepare_destination(self.dest)
        self.assertEqual(handoff.git(self.dest, "rev-parse", "HEAD"), before)

    def test_failed_push_retains_source_then_retry_releases_and_restores(self):
        handoff.git(self.root, "remote", "set-url", "--push", "origin", str(self.folder / "unavailable.git"))
        with self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assert_held()
        commit = handoff.git(self.root, "rev-parse", "HEAD")
        handoff.git(self.root, "remote", "set-url", "--push", "origin", str(self.remote))
        receipt = self.transfer.save_and_release()
        self.assertEqual(receipt["commit"], commit)
        self.bridge.release_held.assert_called_once()
        packet = self.transfer.prepare_destination(self.dest, files=["agreement.md"])
        self.assertEqual(packet["commit"], commit)

    def test_failed_commit_preserves_index_and_source(self):
        handoff.git(self.root, "config", "user.name", "")
        with self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assertTrue(handoff.git(self.root, "diff", "--cached", "--name-only"))
        self.assert_held()

    def test_duplicate_replies_do_not_prevent_same_source_save(self):
        self.record["checkpoint_candidates"] = [json.dumps(self.after), json.dumps(self.after)]
        self.assertTrue(self.transfer.save_and_release()["source_session_exited"])

    def test_duplicate_original_without_progress_remains_held(self):
        self.record["checkpoint_candidates"] = [json.dumps(self.previous), json.dumps(self.previous)]
        with self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assert_held()

    def test_failed_remote_verification_retains_source(self):
        original = handoff.git
        def mismatch(root, *args):
            return "" if args[0] == "ls-remote" else original(root, *args)
        with patch.object(handoff, "git", side_effect=mismatch), self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assert_held()

    def test_failed_place_write_retains_source(self):
        self.bridge.transport.save = Mock(side_effect=OSError("Disk failure"))
        with self.assertRaises(OSError):
            self.transfer.save_and_release()
        self.assert_held()

    def test_changed_agreement_retains_source(self):
        (self.root / "agreement.md").write_text("Changed agreement")
        with self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assert_held()

    def test_invalid_checkpoint_retains_source(self):
        self.record["reply"] = "not JSON"
        with self.assertRaises(Exception):
            self.transfer.save_and_release()
        self.assert_held()

    def test_cancellation_is_not_handoff_success(self):
        self.bridge.held_cancelled.return_value = True
        with self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assert_held()

    def test_explicit_move_can_preserve_unchanged_working_place(self):
        self.transfer.allow_unchanged = True
        self.record["reply"] = json.dumps(self.previous)
        self.assertTrue(self.transfer.save_and_release()["source_session_exited"])

    def test_caller_cancellation_during_push_prevents_release(self):
        stopped = False
        original = handoff.git
        def cancel_after_push(root, *args):
            nonlocal stopped
            value = original(root, *args)
            if args[0] == "push":
                stopped = True
            return value
        self.transfer.cancelled = lambda: stopped
        with patch.object(handoff, "git", side_effect=cancel_after_push), self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        self.assert_held()

    def test_changed_committed_place_is_caught_before_push(self):
        original = handoff.git
        pushed = []
        def alter_commit(root, *args):
            if args[0] == "commit":
                (self.root / "place.json").write_text(json.dumps(dict(self.after, memory="Unapproved replacement")))
                original(root, "add", "place.json")
                value = original(root, *args)
                # Working tree matches the expected content; committed blob does not.
                (self.root / "place.json").write_text(json.dumps(self.after))
                return value
            if args[0] == "push":
                pushed.append(args)
            return original(root, *args)
        with patch.object(handoff, "git", side_effect=alter_commit), self.assertRaisesRegex(handoff.HandoffError, "Committed handoff"):
            self.transfer.save_and_release()
        self.assertEqual(pushed, [])
        self.assert_held()

    def test_evidence_missing_from_commit_prevents_release(self):
        self.transfer.files.remove("artifact.txt")
        handoff.git(self.root, "config", "core.excludesFile", str(self.folder / "ignore"))
        (self.folder / "ignore").write_text("artifact.txt\n")
        with self.assertRaises(Exception):
            self.transfer.save_and_release()
        self.assert_held()

    def test_failed_release_never_admits_destination(self):
        self.bridge.release_held.return_value = dict(status="interrupted", cleanup_error="Child remains")
        with self.assertRaises(handoff.HandoffError):
            self.transfer.save_and_release()
        with self.assertRaises(handoff.HandoffError):
            self.transfer.prepare_destination(self.dest)

    def test_changed_remote_after_release_is_not_a_different_handoff(self):
        self.transfer.save_and_release()
        before = handoff.git(self.dest, "rev-parse", "HEAD")
        content = (self.dest / "place.json").read_bytes()
        handoff.git(self.root, "commit", "--allow-empty", "-qm", "Other change")
        handoff.git(self.root, "push", "-q", "origin", "trial")
        with self.assertRaises(handoff.HandoffError):
            self.transfer.prepare_destination(self.dest)
        self.assertEqual(handoff.git(self.dest, "rev-parse", "HEAD"), before)
        self.assertEqual((self.dest / "place.json").read_bytes(), content)

    def test_cancellation_during_destination_preparation_is_not_success(self):
        self.transfer.save_and_release()
        original = handoff.prepare
        def cancel_during_prepare(*args, **kwargs):
            packet = original(*args, **kwargs)
            self.transfer.cancelled = lambda: True
            return packet
        with patch.object(handoff, "prepare", side_effect=cancel_during_prepare), self.assertRaisesRegex(handoff.HandoffError, "cancelled during pickup"):
            self.transfer.prepare_destination(self.dest)


if __name__ == "__main__":
    unittest.main()
