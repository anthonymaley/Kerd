import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("roll_status.py").resolve()


class RollStatusTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.repo = Path(self.tempdir.name) / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)

    def git_dir(self, repo=None):
        repo = repo or self.repo
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        return Path(result.stdout.strip())

    def write_record(self, record, repo=None):
        roll_dir = self.git_dir(repo) / "roll"
        roll_dir.mkdir(parents=True, exist_ok=True)
        path = roll_dir / "run.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def run_status(self, repo=None):
        repo = repo or self.repo
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(repo)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    @staticmethod
    def base_record(status="running", next_action="Wait for the active worker."):
        return {"status": status, "next_action": next_action, "history": []}

    def test_clone_style_git_directory_and_readable_running_panel(self):
        self.write_record(self.base_record())
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Project: {self.repo.resolve()}", result.stdout)
        self.assertIn("Current: Running", result.stdout)
        self.assertIn("Next: Wait for the active worker.", result.stdout)
        self.assertNotIn("{\"status\"", result.stdout)

    def test_worktree_git_file_uses_worktree_private_directory(self):
        self.write_record(self.base_record(next_action="Main worktree action."))
        subprocess.run(
            [
                "git",
                "-C",
                str(self.repo),
                "-c",
                "user.name=Roll Status Test",
                "-c",
                "user.email=roll-status@example.invalid",
                "commit",
                "-q",
                "--allow-empty",
                "-m",
                "synthetic fixture commit",
            ],
            check=True,
        )
        worktree = Path(self.tempdir.name) / "linked"
        subprocess.run(
            ["git", "-C", str(self.repo), "worktree", "add", "-q", "--detach", str(worktree)],
            check=True,
        )
        self.assertTrue((worktree / ".git").is_file())
        private_record = self.write_record(
            self.base_record(status="paused", next_action="Resume this linked worktree."),
            worktree,
        )
        self.assertIn("worktrees", str(private_record))

        result = self.run_status(worktree)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Current: Paused", result.stdout)
        self.assertIn("Next: Resume this linked worktree.", result.stdout)
        self.assertNotIn("Main worktree action", result.stdout)

    def test_all_known_states_have_truthful_output_and_exact_next_action(self):
        expected = {
            "running": "A worker is currently working",
            "paused": "paused",
            "continue": "useful work remains",
            "review": "awaiting independent assessment; it has not been accepted",
            "blocked": "blocker is resolved",
            "uncertain": "could not establish a reliable state",
            "failed": "failed",
        }
        for status, phrase in expected.items():
            with self.subTest(status=status):
                action = f"Exact action for {status}."
                self.write_record(self.base_record(status, action))
                result = self.run_status()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(phrase, result.stdout)
                self.assertIn(f"Next: {action}", result.stdout)

    def test_history_summary_context_trigger_and_private_ids_are_not_shown(self):
        record = self.base_record("continue", "Start the next bounded worker.")
        record["history"] = [
            {
                "status": "continue",
                "context_trigger": None,
                "context_readings": None,
                "session_id": "NATIVE-SESSION-SECRET",
                "request_id": "NATIVE-REQUEST-SECRET",
                "error": "PRIVATE-ERROR-CONTENT",
            },
            {
                "status": "review",
                "context_trigger": {"reason": "threshold"},
                "context_readings": [{"used": 90}],
                "session_id": "SECOND-SESSION-SECRET",
            },
        ]
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Completed workers: 2", result.stdout)
        self.assertIn("Last returned status: Review (awaiting assessment, not accepted)", result.stdout)
        self.assertIn("Context-triggered Roll observed: Yes", result.stdout)
        self.assertIn("not proof of quality", result.stdout)
        for secret in ("NATIVE-SESSION-SECRET", "NATIVE-REQUEST-SECRET", "PRIVATE-ERROR-CONTENT"):
            self.assertNotIn(secret, result.stdout + result.stderr)

    def test_older_optional_history_fields_are_labeled_unknown(self):
        record = self.base_record("continue", "Continue safely.")
        record["history"] = [{"model": "older"}, {"status": "future-state"}]
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Completed workers: 2", result.stdout)
        self.assertIn("Last returned status: Unknown", result.stdout)
        self.assertIn("Context-triggered Roll observed: Unknown", result.stdout)
        self.assertNotIn("future-state", result.stdout)

    def test_absent_history_is_unknown_and_valid(self):
        record = {"status": "continue", "next_action": "Continue safely."}
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Completed workers: Unknown (history not recorded)", result.stdout)
        self.assertIn("Last returned status: Unknown", result.stdout)

    def test_ansi_and_control_characters_are_suppressed(self):
        action = "Inspect \x1b[31mred\x1b[0m\nthen\x00 continue."
        self.write_record(self.base_record("continue", action))
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Next: Inspect red then continue.", result.stdout)
        self.assertNotIn("\x1b", result.stdout + result.stderr)
        self.assertNotIn("\x00", result.stdout + result.stderr)

    def test_command_leaves_project_data_untouched(self):
        record_path = self.write_record(self.base_record())
        sentinel = self.repo / "sentinel.txt"
        sentinel.write_text("unchanged", encoding="utf-8")
        before = {
            path: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in (record_path, sentinel, self.repo / ".git" / "config")
        }
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {
            path: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in before
        }
        self.assertEqual(before, after)
        self.assertFalse((self.repo / "run.json").exists())

    def test_missing_record_is_nonzero_and_does_not_create_fallback(self):
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("No managed Roll record", result.stderr)
        self.assertFalse((self.git_dir() / "roll" / "run.json").exists())

    def test_invalid_json_is_nonzero_without_traceback_or_private_content(self):
        roll_dir = self.git_dir() / "roll"
        roll_dir.mkdir()
        (roll_dir / "run.json").write_text('{"private": "DO-NOT-PRINT",', encoding="utf-8")
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("DO-NOT-PRINT", result.stderr)
        self.assertIn("not valid JSON", result.stderr)

    def test_unknown_current_status_is_nonzero_not_completion(self):
        self.write_record(self.base_record("complete", "Assume it passed."))
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Assume it passed", result.stdout + result.stderr)
        self.assertIn("unknown status", result.stderr)

    def test_expected_json_types_are_validated_without_traceback(self):
        invalid_records = [
            [],
            {"status": 1, "next_action": "x"},
            {"status": "running", "next_action": ["x"]},
            {"status": "running", "next_action": "x", "history": {}},
            {"status": "running", "next_action": "x", "history": [1]},
            {"status": "running", "next_action": "x", "history": [{"status": 2}]},
            {"status": "running", "next_action": "x", "history": [{"context_trigger": "yes"}]},
            {"status": "running", "next_action": "x", "history": [{"context_readings": {}}]},
        ]
        for record in invalid_records:
            with self.subTest(record=record):
                self.write_record(record)
                result = self.run_status()
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_non_git_directory_has_concise_nonzero_error(self):
        outside = Path(self.tempdir.name) / "not-a-repo"
        outside.mkdir()
        result = self.run_status(outside)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("not a readable Git worktree", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
