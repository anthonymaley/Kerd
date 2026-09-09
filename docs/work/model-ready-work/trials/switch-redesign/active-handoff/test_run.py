"""Destination admission checks; these fixtures are not live handoff proof."""
import importlib.util
from pathlib import Path
import unittest
import tempfile
import json
import subprocess
import sys
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("active_handoff_trial", Path(__file__).with_name("run.py"))
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


class ReleaseTests(unittest.TestCase):
    def test_completed_clean_gone_source_is_admitted(self):
        with patch.object(trial.roll, "group_gone", return_value=True):
            trial.require_release({"status": "completed", "owned_children_gone": True})

    def test_incomplete_failed_and_unknown_results_are_refused(self):
        for status in (None, "running", "failed", "interrupted"):
            with self.subTest(status=status), patch.object(trial.roll, "group_gone", return_value=True):
                with self.assertRaises(RuntimeError):
                    trial.require_release({"status": status, "owned_children_gone": True})

    def test_parent_completion_without_child_proof_is_refused(self):
        for children in (None, False, "true", 1):
            with self.subTest(children=children), patch.object(trial.roll, "group_gone", return_value=True):
                with self.assertRaises(RuntimeError):
                    trial.require_release({"status": "completed", "owned_children_gone": children})

    def test_cleanup_error_is_not_overridden_by_success_fields(self):
        with patch.object(trial.roll, "group_gone", return_value=True):
            with self.assertRaises(RuntimeError):
                trial.require_release({"status": "completed", "owned_children_gone": True,
                                       "cleanup_error": "uncertain source"})

    def test_live_group_is_refused_even_when_record_says_gone(self):
        with patch.object(trial.roll, "group_gone", return_value=False):
            with self.assertRaises(RuntimeError):
                trial.require_release({"status": "completed", "owned_children_gone": True})


class PreservationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="handoff-preservation-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        trial.handoff.git(self.root, "init", "-q")
        for key, value in (("user.name", "Test"), ("user.email", "test@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
            trial.handoff.git(self.root, "config", key, value)
        (self.root / "handoff.json").write_bytes(b"original")
        trial.handoff.git(self.root, "add", "--", "handoff.json")
        trial.handoff.git(self.root, "commit", "-qm", "initial")
        self.commit = trial.handoff.git(self.root, "rev-parse", "HEAD")

    def test_unchanged_inputs_allow_new_deliverable(self):
        (self.root / "result.txt").write_text("new work")
        trial.check_preserved(self.root, self.commit, {"handoff.json": b"original"})

    def test_changed_saved_place_is_refused(self):
        (self.root / "handoff.json").write_bytes(b"changed")
        with self.assertRaisesRegex(RuntimeError, "protected inputs"):
            trial.check_preserved(self.root, self.commit, {"handoff.json": b"original"})

    def test_worker_commit_is_refused_even_if_content_unchanged(self):
        trial.handoff.git(self.root, "commit", "--allow-empty", "-qm", "unapproved worker commit")
        with self.assertRaisesRegex(RuntimeError, "Git history"):
            trial.check_preserved(self.root, self.commit, {"handoff.json": b"original"})


class SupplementalArtifactTests(unittest.TestCase):
    def setUp(self):
        self.output = Path(__file__).with_name("output")
        spec = importlib.util.spec_from_file_location("preview_checked", self.output / "pickup_preview.py")
        self.preview = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.preview)

    def test_every_required_top_level_field_is_actually_required(self):
        packet = json.loads((self.output / "example.json").read_text())
        for key in ("status", "branch", "commit", "clean_at_check", "synchronized", "sources"):
            with self.subTest(key=key):
                missing = dict(packet)
                del missing[key]
                with self.assertRaises(ValueError):
                    self.preview.summarize(missing)

    def test_missing_path_error_does_not_emit_raw_terminal_controls(self):
        result = subprocess.run([sys.executable, str(self.output / "pickup_preview.py"),
                                 "missing-\x1b[31m-\n\u202e.json"], cwd=self.output,
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("\x1b", result.stderr)
        self.assertNotIn("\u202e", result.stderr)
        self.assertEqual(result.stderr.count("\n"), 1)


if __name__ == "__main__":
    unittest.main()
