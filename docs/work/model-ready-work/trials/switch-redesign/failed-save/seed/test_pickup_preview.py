"""Tests for the prepared-pickup preview library and command line interface."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pickup_preview import summarize


ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "pickup_preview.py"


def packet(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "status": "pickup_prepared",
        "branch": "feature/pickup",
        "commit": "0123456789abcdef",
        "clean_at_check": True,
        "synchronized": False,
        "sources": [
            {
                "file": "CONTEXT.md",
                "selection": "complete file",
                "content": "private body",
            }
        ],
    }
    value.update(changes)
    return value


class SummarizeTests(unittest.TestCase):
    def test_realistic_unicode_multiple_sources_and_byte_counts(self) -> None:
        value = packet(
            branch="feature/café",
            commit="abc123",
            synchronized=True,
            sources=[
                {"file": "CONTEXT.md", "selection": "complete file", "content": "café"},
                {"file": "計画.md", "selection": "§ Now", "content": "🌍\n"},
            ],
            note="Recorded state only",
        )

        output = summarize(value)

        self.assertIn("Branch: feature/café", output)
        self.assertIn("Revision: abc123", output)
        self.assertIn("Synchronization: synchronized", output)
        self.assertIn("Selected sources: 2 sources", output)
        self.assertIn("CONTEXT.md — complete file — 5 UTF-8 bytes", output)
        self.assertIn("計画.md — § Now — 5 UTF-8 bytes", output)
        self.assertIn("Total source text: 10 UTF-8 bytes", output)
        self.assertIn("Note: Recorded state only", output)
        self.assertTrue(output.endswith("Prepared does not mean restored or accepted."))

    def test_empty_sources_and_empty_content_are_valid(self) -> None:
        no_sources = summarize(packet(sources=[]))
        empty_content = summarize(
            packet(sources=[{"file": "EMPTY.md", "selection": "complete file", "content": ""}])
        )

        self.assertIn("Selected sources: 0 sources", no_sources)
        self.assertIn("Total source text: 0 UTF-8 bytes", no_sources)
        self.assertIn("Selected sources: 1 source", empty_content)
        self.assertIn("EMPTY.md — complete file — 0 UTF-8 bytes", empty_content)

    def test_local_only_and_dirty_state_are_explicit(self) -> None:
        output = summarize(packet(clean_at_check=False, synchronized=False))

        self.assertIn("Working tree at check: not clean", output)
        self.assertIn("Synchronization: local-only (not synchronized)", output)

    def test_private_content_session_ids_and_unknown_fields_are_not_shown(self) -> None:
        secret_body = "PRIVATE-BODY-9f8bd"
        private_session = "session-private-72ca"
        unknown_secret = "UNKNOWN-SECRET-c431"
        value = packet(
            sources=[
                {
                    "file": "CONTEXT.md",
                    "selection": "complete file",
                    "content": secret_body,
                    "unknown_source_field": unknown_secret,
                }
            ],
            session_id=private_session,
            unknown_packet_field=unknown_secret,
        )

        output = summarize(value)

        self.assertNotIn(secret_body, output)
        self.assertNotIn(private_session, output)
        self.assertNotIn(unknown_secret, output)
        self.assertIn(f"{len(secret_body.encode('utf-8'))} UTF-8 bytes", output)

    def test_terminal_controls_in_every_displayed_label_are_escaped(self) -> None:
        value = packet(
            branch="safe\x1b[31m\nbranch",
            commit="rev\r\t42",
            sources=[
                {
                    "file": "name\x00.md",
                    "selection": "part\u202esecret",
                    "content": "x",
                }
            ],
            note="note\u2066hidden\u2069",
        )

        output = summarize(value)

        self.assertNotIn("\x1b", output)
        self.assertNotIn("\r", output)
        self.assertNotIn("\t", output)
        self.assertNotIn("\x00", output)
        self.assertNotIn("\u202e", output)
        self.assertNotIn("\u2066", output)
        self.assertIn(r"safe\u001B[31m\u000Abranch", output)
        self.assertIn(r"rev\u000D\u000942", output)
        self.assertIn(r"name\u0000.md", output)
        self.assertIn(r"part\u202Esecret", output)
        self.assertIn(r"note\u2066hidden\u2069", output)

    def test_malformed_packets_raise_value_error(self) -> None:
        bad_packets: list[object] = [
            None,
            [],
            packet(status="continue"),
            packet(branch=""),
            packet(commit=3),
            packet(sources=None),
            packet(sources=["not an object"]),
            packet(sources=[{"selection": "all", "content": "x"}]),
            packet(sources=[{"file": "x", "content": "x"}]),
            packet(sources=[{"file": "x", "selection": "all", "content": 1}]),
            packet(sources=[{"file": "x", "selection": "all", "content": "\ud800"}]),
            packet(note=1),
        ]

        for value in bad_packets:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize(value)

    def test_booleans_must_be_actual_booleans(self) -> None:
        for name in ("clean_at_check", "synchronized"):
            for bad_value in (0, 1, "true", None):
                with self.subTest(name=name, value=bad_value):
                    with self.assertRaises(ValueError):
                        summarize(packet(**{name: bad_value}))


class CliTests(unittest.TestCase):
    def run_cli(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PROGRAM), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_cli_success(self) -> None:
        result = self.run_cli(ROOT / "example.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("Prepared pickup preview", result.stdout)
        self.assertIn("CONTEXT.md", result.stdout)
        self.assertNotIn("Seinn", result.stdout)
        self.assertNotIn("private session", result.stdout)

    def test_cli_invalid_packet_has_stderr_error_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"status": ', encoding="utf-8")
            result = self.run_cli(path)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("pickup_preview: error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_missing_file_has_stderr_error_without_traceback(self) -> None:
        result = self.run_cli(ROOT / "does-not-exist.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("pickup_preview: error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
