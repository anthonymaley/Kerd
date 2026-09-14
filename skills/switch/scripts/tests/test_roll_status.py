from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "roll_status.py"


def command(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        check=False,
    )


def git(repo: Path, *args: str) -> str:
    result = command("git", "-C", str(repo), *args)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def snapshot(directory: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(directory)): path.read_bytes()
        for path in directory.rglob("*")
        if path.is_file()
    }


class RollStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        result = command("git", "init", "-q", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_record(self, record: object, git_dir: Path | None = None) -> Path:
        if git_dir is None:
            git_dir = Path(git(self.repo, "rev-parse", "--absolute-git-dir"))
        destination = git_dir / "roll" / "run.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(record), encoding="utf-8")
        return destination

    def run_status(self, project: Path | None = None) -> subprocess.CompletedProcess[str]:
        return command(
            sys.executable,
            str(SCRIPT),
            "--project",
            str(project or self.repo),
        )

    def valid_record(self, **changes: object) -> dict[str, object]:
        record: dict[str, object] = {
            "status": "continue",
            "next_action": "Run the next bounded worker.",
            "history": [],
        }
        record.update(changes)
        return record

    def test_clone_style_git_directory_and_nested_project_path(self) -> None:
        nested = self.repo / "one" / "two"
        nested.mkdir(parents=True)
        self.write_record(self.valid_record())
        before = snapshot(self.repo)

        result = self.run_status(nested)

        self.assertEqual(result.returncode, 0, result.stderr)
        actual_root = git(nested, "rev-parse", "--show-toplevel")
        self.assertIn(f"Project: {actual_root}", result.stdout)
        self.assertIn("State: Continue - ready for another useful piece.", result.stdout)
        self.assertIn("Next action: Run the next bounded worker.", result.stdout)
        self.assertEqual(snapshot(self.repo), before)

    def test_worktree_git_file_uses_private_worktree_git_directory(self) -> None:
        git(self.repo, "config", "user.name", "Roll Test")
        git(self.repo, "config", "user.email", "roll@example.invalid")
        tracked = self.repo / "tracked.txt"
        tracked.write_text("fixture\n", encoding="utf-8")
        git(self.repo, "add", "tracked.txt")
        git(self.repo, "commit", "-q", "-m", "fixture")
        worktree = self.base / "linked"
        git(self.repo, "worktree", "add", "-q", "--detach", str(worktree))
        self.assertTrue((worktree / ".git").is_file())
        private_git_dir = Path(git(worktree, "rev-parse", "--absolute-git-dir"))
        self.write_record(self.valid_record(next_action="Inspect the linked worktree."), private_git_dir)
        before = snapshot(self.base)

        result = self.run_status(worktree)

        self.assertEqual(result.returncode, 0, result.stderr)
        actual_root = git(worktree, "rev-parse", "--show-toplevel")
        self.assertIn(f"Project: {actual_root}", result.stdout)
        self.assertIn("Next action: Inspect the linked worktree.", result.stdout)
        self.assertEqual(snapshot(self.base), before)

    def test_all_known_states_are_friendly_and_successful(self) -> None:
        expected = {
            "running": "Recorded running - worker liveness has not been checked.",
            "paused": "Paused - waiting to resume.",
            "continue": "Continue - ready for another useful piece.",
            "review": "Review - awaiting independent assessment (not accepted).",
            "blocked": "Blocked - the recorded blocker needs attention.",
            "uncertain": "Uncertain - the recorded state needs clarification.",
            "failed": "Failed - the Roll did not complete successfully.",
        }
        for state, label in expected.items():
            with self.subTest(state=state):
                self.write_record(self.valid_record(status=state))
                result = self.run_status()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"State: {label}", result.stdout)
                self.assertIn("Read result only; this does not mean the work passed.", result.stdout)

    def test_history_summary_and_native_ids_do_not_leak(self) -> None:
        record = self.valid_record(
            history=[
                {
                    "status": "continue",
                    "context_trigger": None,
                    "context_readings": [],
                    "session_id": "SECRET-SESSION",
                    "request_id": "SECRET-REQUEST",
                },
                {
                    "status": "review",
                    "context_trigger": {"reason": "threshold"},
                    "context_readings": [{"used": 80}],
                },
            ],
            session_id="ROOT-SECRET",
            error="PRIVATE ERROR CONTENT",
        )
        self.write_record(record)

        result = self.run_status()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Completed workers: 2", result.stdout)
        self.assertIn("Last returned status: review", result.stdout)
        self.assertIn("Context-triggered Roll observed: yes", result.stdout)
        self.assertNotIn("SECRET", result.stdout + result.stderr)
        self.assertNotIn("PRIVATE ERROR CONTENT", result.stdout + result.stderr)

    def test_absent_optional_history_fields_are_unknown(self) -> None:
        self.write_record(
            self.valid_record(history=[{}, {"status": "paused", "context_readings": []}])
        )
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Last returned status: paused", result.stdout)
        self.assertIn("Context-triggered Roll observed: unknown", result.stdout)

        self.write_record(self.valid_record(history=[{}]))
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Last returned status: unknown", result.stdout)

        record = self.valid_record()
        del record["history"]
        self.write_record(record)
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("History: unknown (not recorded)", result.stdout)

    def test_unknown_historical_status_is_reported_as_unknown(self) -> None:
        self.write_record(
            self.valid_record(history=[{"status": "future-runtime-status"}])
        )

        result = self.run_status()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("State: Continue - ready for another useful piece.", result.stdout)
        self.assertIn("Last returned status: unknown", result.stdout)
        self.assertNotIn("future-runtime-status", result.stdout + result.stderr)

    def test_null_context_readings_are_accepted_as_unavailable(self) -> None:
        self.write_record(
            self.valid_record(
                history=[
                    {
                        "status": "continue",
                        "context_trigger": None,
                        "context_readings": None,
                    }
                ]
            )
        )

        result = self.run_status()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Last returned status: continue", result.stdout)
        self.assertIn("Context-triggered Roll observed: no", result.stdout)

    def test_explicit_null_context_triggers_report_no(self) -> None:
        self.write_record(
            self.valid_record(
                history=[
                    {"status": "continue", "context_trigger": None},
                    {"status": "paused", "context_trigger": None},
                ]
            )
        )
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Context-triggered Roll observed: no", result.stdout)

    def test_saved_text_cannot_emit_ansi_or_control_characters(self) -> None:
        action = "Review \x1b[31mred\x1b[0m\nthen\tstop\x00now"
        self.write_record(self.valid_record(next_action=action))
        result = self.run_status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("\x1b", result.stdout)
        self.assertNotIn("\x00", result.stdout)
        self.assertNotIn("[31m", result.stdout)
        self.assertIn("Next action: Review red then stop now", result.stdout)
        self.assertEqual(len([line for line in result.stdout.splitlines() if "Next action:" in line]), 1)

    def test_missing_record_is_nonzero_and_does_not_create_fallback(self) -> None:
        before = snapshot(self.repo)
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("No Roll status record", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(snapshot(self.repo), before)

    def test_unknown_state_is_nonzero_and_does_not_infer_completion(self) -> None:
        self.write_record(self.valid_record(status="complete"))
        result = self.run_status()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("status is unknown", result.stderr)
        self.assertNotIn("passed", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_managed_conductor_completion_and_phase_are_explicit(self) -> None:
        self.write_record(self.valid_record(status="complete", kind="conductor", phase="stopped"))
        result = self.run_status()
        self.assertEqual(result.returncode, 0)
        self.assertIn("Managed Conductor status", result.stdout)
        self.assertIn("reports completion after review", result.stdout)
        self.assertIn("Phase: stopped", result.stdout)

    def test_invalid_json_and_schema_are_concise_nonzero_errors(self) -> None:
        invalid_cases = [
            ("not-json", "not valid JSON"),
            (json.dumps([]), "must be a JSON object"),
            (json.dumps({"next_action": "x"}), "no valid status"),
            (json.dumps({"status": "continue", "next_action": 3}), "no valid next action"),
            (json.dumps(self.valid_record(history={})), "invalid history"),
            (json.dumps(self.valid_record(history=["bad"])), "invalid history"),
            (
                json.dumps(self.valid_record(history=[{"context_trigger": "yes"}])),
                "invalid history",
            ),
            (
                json.dumps(self.valid_record(history=[{"context_readings": {}}])),
                "invalid history",
            ),
            (
                json.dumps(self.valid_record(history=[{"status": ["continue"]}])),
                "invalid history",
            ),
        ]
        ledger = Path(git(self.repo, "rev-parse", "--absolute-git-dir")) / "roll" / "run.json"
        ledger.parent.mkdir(parents=True, exist_ok=True)
        for raw, message in invalid_cases:
            with self.subTest(message=message, raw=raw):
                ledger.write_text(raw, encoding="utf-8")
                result = self.run_status()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_non_git_project_is_a_concise_nonzero_error(self) -> None:
        outside = self.base / "not-a-repo"
        outside.mkdir()
        result = self.run_status(outside)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("not a readable Git worktree", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
