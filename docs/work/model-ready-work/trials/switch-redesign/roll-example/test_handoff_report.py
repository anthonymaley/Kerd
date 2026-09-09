"""Tests for the read-only handoff report renderer and CLI."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from handoff_report import ValidationError, render_report


PROJECT_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = PROJECT_DIR / "handoff_report.py"


def valid_record(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "project": "Fictional Moon Garden",
        "stage": "Implementation",
        "next_action": "Ask a reviewer to inspect the handoff.",
        "tasks": [],
    }
    record.update(overrides)
    return record


class RenderReportTests(unittest.TestCase):
    def test_renders_all_groups_in_fixed_order_and_preserves_group_order(self) -> None:
        data = valid_record(
            tasks=[
                {"id": "q-1", "title": "Queue seeds", "status": "queued"},
                {"id": "d-1", "title": "Draw garden", "status": "done"},
                {"id": "a-1", "title": "Plant craters", "status": "active"},
                {"id": "d-2", "title": "Label domes", "status": "done"},
                {"id": "b-1", "title": "Await moonlight", "status": "blocked"},
                {"id": "q-2", "title": "Water seedlings", "status": "queued"},
            ]
        )

        report = render_report(data)

        expected = """# Handoff: Fictional Moon Garden

Stage: Implementation

## Done

- `d-1`: Draw garden
- `d-2`: Label domes

## Active

- `a-1`: Plant craters

## Blocked

- `b-1`: Await moonlight

## Queued

- `q-1`: Queue seeds
- `q-2`: Water seedlings

## Next action

Ask a reviewer to inspect the handoff.
"""
        self.assertEqual(report, expected)

    def test_omits_empty_status_headings(self) -> None:
        report = render_report(
            valid_record(
                tasks=[
                    {"id": "a-1", "title": "Plant craters", "status": "active"}
                ]
            )
        )

        self.assertIn("## Active", report)
        self.assertNotIn("## Done", report)
        self.assertNotIn("## Blocked", report)
        self.assertNotIn("## Queued", report)
        self.assertIn("## Next action", report)

    def test_accepts_empty_tasks_and_still_renders_next_action(self) -> None:
        report = render_report(valid_record())

        self.assertEqual(
            report,
            "# Handoff: Fictional Moon Garden\n\n"
            "Stage: Implementation\n\n"
            "## Next action\n\n"
            "Ask a reviewer to inspect the handoff.\n",
        )
        for heading in ("Done", "Active", "Blocked", "Queued"):
            self.assertNotIn(f"## {heading}", report)

    def test_rejects_duplicate_task_ids(self) -> None:
        data = valid_record(
            tasks=[
                {"id": "same", "title": "First", "status": "done"},
                {"id": "same", "title": "Second", "status": "queued"},
            ]
        )

        with self.assertRaisesRegex(ValidationError, "duplicate task id: same"):
            render_report(data)

    def test_rejects_invalid_status(self) -> None:
        data = valid_record(
            tasks=[{"id": "x", "title": "Unknown", "status": "finished"}]
        )

        with self.assertRaisesRegex(ValidationError, "status must be one of"):
            render_report(data)

    def test_rejects_missing_or_blank_required_strings(self) -> None:
        cases = [
            (valid_record(project=None), "project"),
            (valid_record(stage=""), "stage"),
            (valid_record(next_action="   \t"), "next_action"),
            (
                valid_record(tasks=[{"title": "Task", "status": "done"}]),
                r"tasks\[0\]\.id",
            ),
            (
                valid_record(tasks=[{"id": "x", "title": " ", "status": "done"}]),
                r"tasks\[0\]\.title",
            ),
            (
                valid_record(tasks=[{"id": "x", "title": "Task"}]),
                r"tasks\[0\]\.status",
            ),
        ]

        for data, message_pattern in cases:
            with self.subTest(message_pattern=message_pattern):
                with self.assertRaisesRegex(ValidationError, message_pattern):
                    render_report(data)

    def test_rejects_wrong_data_types(self) -> None:
        cases = [
            ([], "input must be a JSON object"),
            (valid_record(project=7), "project must be a string"),
            (valid_record(stage=False), "stage must be a string"),
            (valid_record(next_action=[]), "next_action must be a string"),
            (valid_record(tasks={}), "tasks must be a list"),
            (valid_record(tasks=["task"]), r"tasks\[0\] must be an object"),
            (
                valid_record(tasks=[{"id": 1, "title": "Task", "status": "done"}]),
                r"tasks\[0\]\.id must be a string",
            ),
            (
                valid_record(tasks=[{"id": "x", "title": 1, "status": "done"}]),
                r"tasks\[0\]\.title must be a string",
            ),
            (
                valid_record(tasks=[{"id": "x", "title": "Task", "status": 1}]),
                r"tasks\[0\]\.status must be a string",
            ),
        ]

        for data, message_pattern in cases:
            with self.subTest(message_pattern=message_pattern):
                with self.assertRaisesRegex(ValidationError, message_pattern):
                    render_report(data)

    def test_rejects_embedded_newlines_in_every_string_field(self) -> None:
        cases = [
            valid_record(project="Moon\nGarden"),
            valid_record(stage="Build\rReview"),
            valid_record(next_action="Run\r\ntests"),
            valid_record(
                tasks=[{"id": "task\n1", "title": "Task", "status": "done"}]
            ),
            valid_record(
                tasks=[{"id": "task-1", "title": "Two\nlines", "status": "done"}]
            ),
            valid_record(
                tasks=[{"id": "task-1", "title": "Task", "status": "do\nne"}]
            ),
        ]

        for data in cases:
            with self.subTest(data=data):
                with self.assertRaisesRegex(ValidationError, "single-line string"):
                    render_report(data)


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *arguments],
            cwd=PROJECT_DIR,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_cli_renders_valid_file_without_modifying_it(self) -> None:
        original = json.dumps(valid_record(), indent=2) + "\n"
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "record.json"
            input_path.write_text(original, encoding="utf-8")

            result = self.run_cli(str(input_path))

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertEqual(input_path.read_text(encoding="utf-8"), original)
            self.assertEqual(result.stdout, render_report(valid_record()))

    def test_malformed_json_exits_two_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "broken.json"
            input_path.write_text('{"project": ', encoding="utf-8")

            result = self.run_cli(str(input_path))

        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith("error: "))
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_invalid_input_exits_two_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "invalid.json"
            input_path.write_text(json.dumps(valid_record(stage="")), encoding="utf-8")

            result = self.run_cli(str(input_path))

        self.assertEqual(result.returncode, 2)
        self.assertIn("error: stage must not be blank", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_missing_path_argument_exits_two(self) -> None:
        result = self.run_cli()

        self.assertEqual(result.returncode, 2)
        self.assertIn("error: expected exactly one JSON input path", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_extra_path_argument_exits_two(self) -> None:
        result = self.run_cli("one.json", "two.json")

        self.assertEqual(result.returncode, 2)
        self.assertIn("error: expected exactly one JSON input path", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
