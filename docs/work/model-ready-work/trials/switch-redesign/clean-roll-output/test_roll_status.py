from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("roll_status.py").resolve()


class RollStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.git("init", str(self.repo), cwd=self.base)
        self.git("-C", str(self.repo), "config", "user.email", "fixture@example.test")
        self.git("-C", str(self.repo), "config", "user.name", "Fixture")
        self.git("-C", str(self.repo), "commit", "--allow-empty", "-m", "fixture")

    def git(self, *args: str, cwd: Path | None = None) -> str:
        result = subprocess.run(
            ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
        if result.returncode:
            self.fail(f"fixture git command failed: {' '.join(args)}\n{result.stderr}")
        return result.stdout.strip()

    def git_dir(self, repo: Path | None = None) -> Path:
        repo = repo or self.repo
        return Path(self.git("-C", str(repo), "rev-parse", "--absolute-git-dir"))

    def write_record(self, record: object, repo: Path | None = None) -> Path:
        path = self.git_dir(repo) / "roll" / "run.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def run_status(self, repo: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(repo or self.repo)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )

    def snapshot(self, root: Path) -> dict[str, tuple[int, int, str]]:
        result = {}
        for path in sorted(root.rglob("*")):
            if path.is_file() and not path.is_symlink():
                stat = path.stat()
                result[str(path.relative_to(root))] = (
                    stat.st_mode, stat.st_mtime_ns,
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
        return result

    def valid_record(self, status: str = "continue") -> dict[str, object]:
        return {
            "status": status,
            "next_action": "Implement the next bounded piece.",
            "history": [
                {
                    "status": "continue",
                    "context_trigger": None,
                    "context_readings": None,
                    "session_id": "NATIVE-SESSION-SECRET",
                    "request_id": "NATIVE-REQUEST-SECRET",
                },
                {
                    "status": "review",
                    "context_trigger": {"reason": "usage"},
                    "context_readings": [],
                },
            ],
        }

    def test_clone_style_git_directory_and_history(self) -> None:
        self.assertTrue((self.repo / ".git").is_dir())
        self.write_record(self.valid_record())
        result = self.run_status()
        resolved_root = self.git("-C", str(self.repo), "rev-parse", "--show-toplevel")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Project: {resolved_root}", result.stdout)
        self.assertIn("State: Continuing", result.stdout)
        self.assertIn("Next action: Implement the next bounded piece.", result.stdout)
        self.assertIn("Completed workers: 2", result.stdout)
        self.assertIn("Last returned status: review (not proof of quality)", result.stdout)
        self.assertIn("Context-triggered Roll observed: yes", result.stdout)
        self.assertNotIn("NATIVE-SESSION-SECRET", result.stdout + result.stderr)
        self.assertNotIn("NATIVE-REQUEST-SECRET", result.stdout + result.stderr)

    def test_worktree_style_git_file_uses_private_worktree_git_dir(self) -> None:
        worktree = self.base / "linked"
        self.git("-C", str(self.repo), "worktree", "add", "--detach", str(worktree))
        self.assertTrue((worktree / ".git").is_file())
        record_path = self.write_record(self.valid_record("paused"), worktree)
        result = self.run_status(worktree)
        resolved_root = self.git("-C", str(worktree), "rev-parse", "--show-toplevel")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Project: {resolved_root}", result.stdout)
        self.assertIn(f"Record: {record_path}", result.stdout)
        self.assertIn("State: Paused", result.stdout)

    def test_command_leaves_repository_data_untouched(self) -> None:
        self.write_record(self.valid_record())
        before = self.snapshot(self.repo)
        result = self.run_status()
        after = self.snapshot(self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, after)

    def test_missing_record_is_nonzero_and_does_not_create_fallback(self) -> None:
        expected = self.git_dir() / "roll" / "run.json"
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No managed Roll record", result.stderr)
        self.assertFalse(expected.exists())
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_json_and_wrong_root_type_are_concise(self) -> None:
        path = self.git_dir() / "roll" / "run.json"
        path.parent.mkdir()
        for content in ("{broken", "[]"):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                result = self.run_status()
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_unknown_current_state_is_nonzero_without_echoing_it(self) -> None:
        record = self.valid_record("secret-state\x1b[31m")
        self.write_record(record)
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown status", result.stderr)
        self.assertNotIn("secret-state", result.stdout + result.stderr)
        self.assertNotIn("\x1b", result.stdout + result.stderr)

    def test_all_known_states_are_readable_and_next_action_is_exact(self) -> None:
        expected_words = {
            "running": "currently active",
            "paused": "waiting to be resumed",
            "continue": "another useful piece",
            "review": "awaiting independent assessment, not accepted",
            "blocked": "blocker",
            "uncertain": "needs clarification",
            "failed": "stopped after a failure",
        }
        for status, phrase in expected_words.items():
            with self.subTest(status=status):
                record = self.valid_record(status)
                record["next_action"] = f"Exact action for {status}."
                self.write_record(record)
                result = self.run_status()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(phrase, result.stdout)
                self.assertIn(f"Next action: Exact action for {status}.", result.stdout)

    def test_review_is_honest_and_exit_zero_is_scoped(self) -> None:
        self.write_record(self.valid_record("review"))
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("awaiting independent assessment, not accepted", result.stdout)
        self.assertIn("does not mean the work passed", result.stdout)

    def test_unknown_historical_status_is_labeled_unknown(self) -> None:
        record = self.valid_record()
        record["history"] = [{"status": "future-private-status", "context_trigger": None}]
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Last returned status: unknown", result.stdout)
        self.assertNotIn("future-private-status", result.stdout)
        self.assertIn("Context-triggered Roll observed: no", result.stdout)

    def test_absent_optional_history_fields_are_unknown(self) -> None:
        record = self.valid_record()
        record["history"] = [{}]
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Last returned status: unknown", result.stdout)
        self.assertIn("Context-triggered Roll observed: unknown", result.stdout)

    def test_control_sequences_are_suppressed(self) -> None:
        record = self.valid_record()
        record["next_action"] = "Keep \x1b[31mred\x1b[0m\nthen\x00 safe."
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Next action: Keep red then  safe.", result.stdout)
        self.assertNotIn("\x1b", result.stdout)
        self.assertNotIn("\x00", result.stdout)

    def test_invalid_expected_types_are_rejected_without_private_leakage(self) -> None:
        cases = [
            {"status": 1, "next_action": "x", "history": []},
            {"status": "running", "next_action": [], "history": []},
            {"status": "running", "next_action": "x", "history": {}},
            {"status": "running", "next_action": "x", "history": ["PRIVATE"]},
            {"status": "running", "next_action": "x", "history": [{"status": 3}]},
            {"status": "running", "next_action": "x", "history": [{"context_trigger": "PRIVATE"}]},
            {"status": "running", "next_action": "x", "history": [{"context_readings": "PRIVATE"}]},
        ]
        for record in cases:
            with self.subTest(record=record):
                self.write_record(record)
                result = self.run_status()
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("PRIVATE", result.stdout + result.stderr)

    def test_non_repository_is_concise(self) -> None:
        result = self.run_status(self.base)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Could not resolve", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
