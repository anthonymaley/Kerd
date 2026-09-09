"""Tests for the prepared-pickup preview library and command line interface."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pickup_preview import (
    _MARKDOWN_ACTIVE,
    summarize,
    summarize_json,
    summarize_markdown,
)


ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "pickup_preview.py"
EXAMPLE = json.loads((ROOT / "example.json").read_text(encoding="utf-8"))


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

    def test_literal_backslash_escape_text_is_distinct_from_a_control(self) -> None:
        output = summarize(packet(branch=r"literal\u001B", commit="\x1b"))

        self.assertIn(r"Branch: literal\\u001B", output)
        self.assertIn(r"Revision: \u001B", output)
        self.assertNotIn("Revision: \\u001b", output)

    def test_non_bmp_controls_use_eight_digit_uppercase_u_notation(self) -> None:
        language_tag = "\U000e0001"
        output = summarize(
            packet(
                branch="readable café 計画 🌍",
                sources=[
                    {
                        "file": f"name{language_tag}.md",
                        "selection": r"literal\U000E0001",
                        "content": "x",
                    }
                ],
            )
        )

        self.assertIn("Branch: readable café 計画 🌍", output)
        self.assertNotIn(language_tag, output)
        self.assertIn(r"name\U000E0001.md", output)
        self.assertIn(r"literal\\U000E0001", output)

    def test_surrogate_label_is_visible_and_utf8_encodable(self) -> None:
        output = summarize(packet(branch="label\ud800"))
        self.assertIn(r"Branch: label\uD800", output)
        self.assertNotIn("\ud800", output)
        output.encode("utf-8")

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
            for render in (summarize, summarize_json, summarize_markdown):
                with self.subTest(value=value, render=render.__name__):
                    with self.assertRaises(ValueError):
                        render(value)

    def test_booleans_must_be_actual_booleans(self) -> None:
        for name in ("clean_at_check", "synchronized"):
            for bad_value in (0, 1, "true", None):
                with self.subTest(name=name, value=bad_value):
                    with self.assertRaises(ValueError):
                        summarize(packet(**{name: bad_value}))


class JsonSummaryTests(unittest.TestCase):
    def test_documented_metadata_and_utf8_byte_counts(self) -> None:
        value = packet(
            branch="feature/café",
            commit="abc123",
            clean_at_check=False,
            synchronized=True,
            sources=[
                {"file": "café.md", "selection": "complete file", "content": "café"},
                {"file": "計画.md", "selection": "§ Now", "content": "🌍\n"},
            ],
        )

        output = json.loads(summarize_json(value))

        self.assertEqual(
            output,
            {
                "branch": "feature/café",
                "revision": "abc123",
                "clean_at_check": False,
                "synchronized": True,
                "selected_sources": [
                    {"file": "café.md", "selection": "complete file", "utf8_bytes": 5},
                    {"file": "計画.md", "selection": "§ Now", "utf8_bytes": 5},
                ],
                "total_utf8_bytes": 10,
            },
        )

    def test_labels_round_trip_without_terminal_escaping(self) -> None:
        branch = "safe\\literal\x1b\nbranch"
        revision = "revision\\literal\t\x1b"
        filename = "name\\part\x00.md"
        selection = "part\u202esecret"
        output = json.loads(
            summarize_json(
                packet(
                    branch=branch,
                    commit=revision,
                    sources=[
                        {"file": filename, "selection": selection, "content": "x"}
                    ],
                )
            )
        )

        self.assertEqual(output["branch"], branch)
        self.assertEqual(output["revision"], revision)
        self.assertEqual(output["selected_sources"][0]["file"], filename)
        self.assertEqual(output["selected_sources"][0]["selection"], selection)

    def test_content_note_and_unknown_fields_are_absent(self) -> None:
        secrets = ("PRIVATE-BODY-9f8bd", "PRIVATE-NOTE-72ca", "UNKNOWN-SECRET-c431")
        value = packet(
            sources=[
                {
                    "file": "CONTEXT.md",
                    "selection": "complete file",
                    "content": secrets[0],
                    "unknown_source_field": secrets[2],
                }
            ],
            note=secrets[1],
            unknown_packet_field=secrets[2],
        )

        serialized = summarize_json(value)
        output = json.loads(serialized)

        for secret in secrets:
            self.assertNotIn(secret, serialized)
        self.assertEqual(
            set(output),
            {
                "branch",
                "revision",
                "clean_at_check",
                "synchronized",
                "selected_sources",
                "total_utf8_bytes",
            },
        )
        self.assertEqual(
            set(output["selected_sources"][0]), {"file", "selection", "utf8_bytes"}
        )


EXPECTED_ACTIVE = set("&<>|`") | {"\\"} | set('*_[]~":.')


def markdown_tables(output: str) -> list[list[list[str]]]:
    """Split rendered Markdown into tables, rows and raw cells.

    Cells are split on the literal pipe character, which is how a Markdown
    table parser finds cell boundaries: it splits the raw line before any
    character reference is decoded. Counting cells this way therefore measures
    real injection rather than a friendlier approximation of it.
    """
    tables: list[list[list[str]]] = []
    current: list[list[str]] | None = None
    for line in output.splitlines():
        if line.startswith("|"):
            if current is None:
                current = []
                tables.append(current)
            current.append([cell.strip() for cell in line.strip()[1:-1].split("|")])
        else:
            current = None
    return tables


class MarkdownSummaryTests(unittest.TestCase):
    """M2/M3: Markdown shows the required metadata, inertly, and nothing else."""

    def assertWellFormedTables(self, output: str, source_count: int) -> None:
        tables = markdown_tables(output)
        self.assertEqual(len(tables), 2, "expected a state table and a source table")
        state, sources = tables
        self.assertEqual(len(state), 8, "state table must be header, rule and six rows")
        for row in state:
            self.assertEqual(len(row), 2, f"state row gained cells: {row}")
        self.assertEqual(len(sources), 2 + source_count, "source table gained rows")
        for row in sources:
            self.assertEqual(len(row), 4, f"source row gained cells: {row}")

    def assertQuotedCellsAreInert(self, output: str) -> None:
        """No active character survives inside a quoted label cell."""
        quoted = [
            cell
            for table in markdown_tables(output)
            for row in table
            for cell in row
            if cell.startswith('"') and cell.endswith('"') and len(cell) >= 2
        ]
        self.assertTrue(quoted, "expected at least one quoted label cell")
        for cell in quoted:
            # Drop the "&#" that begins each reference we emitted, so the only
            # remaining active character would be one that escaped the filter.
            data = cell[1:-1].replace("&#", "")
            for active in EXPECTED_ACTIVE:
                self.assertNotIn(active, data, f"{active!r} survived in {cell!r}")

    def test_declared_active_set_is_exactly_the_expected_one(self) -> None:
        self.assertEqual(set(_MARKDOWN_ACTIVE), EXPECTED_ACTIVE)
        for character, reference in _MARKDOWN_ACTIVE.items():
            self.assertEqual(reference, f"&#{ord(character)};")

    def test_markdown_presents_the_required_metadata_and_byte_counts(self) -> None:
        value = packet(
            branch="feature/café",
            commit="abc123",
            clean_at_check=False,
            synchronized=True,
            sources=[
                {"file": "CONTEXT.md", "selection": "complete file", "content": "café"},
                {"file": "計画.md", "selection": "§ Now", "content": "\U0001f30d\n"},
            ],
        )

        output = summarize_markdown(value)

        self.assertTrue(output.startswith("# Prepared pickup preview\n"))
        self.assertIn('| Branch | "feature/café" |', output)
        self.assertIn('| Revision | "abc123" |', output)
        self.assertIn("| Working tree at check | not clean |", output)
        self.assertIn("| Synchronization | synchronized |", output)
        self.assertIn("| Selected sources | 2 |", output)
        self.assertIn("| Total source text | 10 UTF-8 bytes |", output)
        self.assertIn('| 1 | "CONTEXT&#46;md" | "complete file" | 5 |', output)
        self.assertIn('| 2 | "計画&#46;md" | "§ Now" | 5 |', output)
        self.assertTrue(output.endswith("\nPrepared does not mean restored or accepted."))
        self.assertWellFormedTables(output, 2)

    def test_markdown_clean_and_local_only_state_are_explicit(self) -> None:
        output = summarize_markdown(packet(clean_at_check=True, synchronized=False))

        self.assertIn("| Working tree at check | clean |", output)
        self.assertIn("| Synchronization | local-only (not synchronized) |", output)

    def test_markdown_pipes_and_newlines_cannot_add_cells_or_rows(self) -> None:
        value = packet(
            branch="a | b",
            commit="row |\n| INJECTED | ROW |",
            sources=[
                {
                    "file": "f | g\n| SECOND | INJECTED | ROW |",
                    "selection": "s | t",
                    "content": "x",
                }
            ],
        )

        output = summarize_markdown(value)

        self.assertWellFormedTables(output, 1)
        self.assertQuotedCellsAreInert(output)
        self.assertIn("&#124;", output)
        self.assertIn("&#92;u000A", output)
        self.assertNotIn("\n| INJECTED", output)
        self.assertNotIn("\n| SECOND", output)

    def test_markdown_backticks_html_and_emphasis_stay_data(self) -> None:
        value = packet(
            branch="`code` <script>alert(1)</script>",
            commit='*em* _u_ [l](x) ~~s~~ &amp; "q"',
            sources=[{"file": "<b>f</b>", "selection": "`s`", "content": "x"}],
        )

        output = summarize_markdown(value)

        self.assertQuotedCellsAreInert(output)
        self.assertWellFormedTables(output, 1)
        self.assertIn("&#96;code&#96;", output)
        self.assertIn("&#60;script&#62;alert(1)&#60;/script&#62;", output)
        self.assertIn("&#42;em&#42;", output)
        self.assertIn("&#95;u&#95;", output)
        self.assertIn("&#91;l&#93;(x)", output)
        self.assertIn("&#126;&#126;s&#126;&#126;", output)
        self.assertIn("&#38;amp;", output)
        self.assertIn("&#34;q&#34;", output)

    def test_markdown_keeps_readable_unicode_readable(self) -> None:
        output = summarize_markdown(
            packet(
                branch="readable café 計画 \U0001f30d",
                sources=[
                    {"file": "計画.md", "selection": "§ Now", "content": "x"}
                ],
            )
        )

        self.assertIn('| Branch | "readable café 計画 \U0001f30d" |', output)
        self.assertIn('"計画&#46;md"', output)
        self.assertIn('"§ Now"', output)

    def test_markdown_control_escapes_match_the_text_convention(self) -> None:
        output = summarize_markdown(
            packet(
                branch="safe\x1b[31mbranch",
                commit="literal\\u001B",
                sources=[
                    {
                        "file": "name\x00\U000e0001.md",
                        "selection": "part‮secret",
                        "content": "x",
                    }
                ],
            )
        )

        self.assertNotIn("\x1b", output)
        self.assertNotIn("\x00", output)
        self.assertNotIn("‮", output)
        self.assertNotIn("\U000e0001", output)
        self.assertIn("safe&#92;u001B&#91;31mbranch", output)
        self.assertIn("literal&#92;&#92;u001B", output)
        self.assertIn("name&#92;u0000&#92;U000E0001&#46;md", output)
        self.assertIn("part&#92;u202Esecret", output)

    def test_markdown_surrogate_label_is_visible_and_utf8_encodable(self) -> None:
        output = summarize_markdown(packet(branch="label\ud800"))

        self.assertIn("label&#92;uD800", output)
        self.assertNotIn("\ud800", output)
        output.encode("utf-8")

    def test_markdown_automatic_url_and_email_links_stay_data(self) -> None:
        value = packet(branch="https://example.com", commit="person@example.com",
            sources=[{"file": "see www.example.com", "selection": "HTTP://example.com", "content": "x"}])
        output = summarize_markdown(value)
        self.assertWellFormedTables(output, 1)
        self.assertQuotedCellsAreInert(output)
        self.assertNotIn("https://", output)
        self.assertNotIn("HTTP://", output)
        self.assertNotIn("www.", output)
        self.assertNotIn("@", output)
        self.assertIn("https&#58;//example&#46;com", output)
        self.assertIn("person&#92;u0040example&#46;com", output)

    def test_markdown_email_display_escape_is_distinct_from_literal_text(self) -> None:
        output = summarize_markdown(packet(branch="person@example.com", commit=r"person\u0040example.com"))
        self.assertIn("person&#92;u0040example&#46;com", output)
        self.assertIn("person&#92;&#92;u0040example&#46;com", output)

    def test_markdown_empty_sources_keep_the_table_header_only(self) -> None:
        output = summarize_markdown(packet(sources=[]))

        self.assertIn("| Selected sources | 0 |", output)
        self.assertIn("| Total source text | 0 UTF-8 bytes |", output)
        self.assertWellFormedTables(output, 0)

    def test_markdown_omits_bodies_notes_private_ids_and_unknown_fields(self) -> None:
        secrets = ("PRIVATE-BODY-9f8bd", "PRIVATE-NOTE-72ca", "UNKNOWN-SECRET-c431")
        value = packet(
            sources=[
                {
                    "file": "CONTEXT.md",
                    "selection": "complete file",
                    "content": secrets[0],
                    "unknown_source_field": secrets[2],
                }
            ],
            note=secrets[1],
            session_id="session-private-72ca",
            unknown_packet_field=secrets[2],
        )

        output = summarize_markdown(value)

        for secret in secrets:
            self.assertNotIn(secret, output)
        self.assertNotIn("session-private-72ca", output)
        self.assertNotIn("Note", output)
        self.assertIn(f"| {len(secrets[0].encode('utf-8'))} |", output)


class CliTests(unittest.TestCase):
    def run_cli(self, path: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PROGRAM), str(path), *arguments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_cli_success(self) -> None:
        result = self.run_cli(ROOT / "example.json")
        explicit = self.run_cli(ROOT / "example.json", "--format", "text")
        self.assertEqual((explicit.returncode, explicit.stdout, explicit.stderr),
                         (result.returncode, result.stdout, result.stderr))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("Prepared pickup preview", result.stdout)
        self.assertIn("CONTEXT.md", result.stdout)
        self.assertNotIn("Seinn", result.stdout)
        self.assertNotIn("private session", result.stdout)

    def test_cli_json_format(self) -> None:
        result = self.run_cli(ROOT / "example.json", "--format", "json")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        output = json.loads(result.stdout)
        self.assertEqual(output["branch"], "kerd-switch-trial-20260906")
        self.assertEqual(output["total_utf8_bytes"], 9100)
        self.assertNotIn("content", result.stdout)

    def test_cli_markdown_format(self) -> None:
        result = self.run_cli(ROOT / "example.json", "--format", "markdown")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertTrue(result.stdout.startswith("# Prepared pickup preview\n"))
        self.assertIn('| Branch | "kerd-switch-trial-20260906" |', result.stdout)
        self.assertIn("| Total source text | 9100 UTF-8 bytes |", result.stdout)
        self.assertIn('| 1 | "CONTEXT&#46;md" | "complete file" | 7156 |', result.stdout)
        # "#" is left readable on purpose: headings are block constructs and
        # cannot start inside a table cell, so escaping it would only cost clarity.
        self.assertIn(
            '| 2 | "TODO&#46;md" | "## Now (including child sections)" | 1944 |',
            result.stdout,
        )
        self.assertNotIn("Seinn", result.stdout)
        self.assertNotIn("Caller-selected", result.stdout)

    def test_cli_text_and_json_are_unchanged_by_the_markdown_route(self) -> None:
        """M1: adding a format must not alter the two that existed before it."""
        text = self.run_cli(ROOT / "example.json", "--format", "text")
        as_json = self.run_cli(ROOT / "example.json", "--format", "json")

        self.assertEqual(text.stdout, summarize(EXAMPLE) + "\n")
        self.assertEqual(as_json.stdout, summarize_json(EXAMPLE) + "\n")
        self.assertNotIn("|", as_json.stdout)
        self.assertNotIn("# Prepared", text.stdout)

    def test_cli_invalid_packet_fails_in_both_formats_without_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid-packet.json"
            path.write_text(json.dumps(packet(branch="")), encoding="utf-8")
            for arguments in ((), ("--format", "json"), ("--format", "markdown")):
                with self.subTest(arguments=arguments):
                    result = self.run_cli(path, *arguments)

                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("pickup_preview: error:", result.stderr)

    def test_cli_invalid_format_has_usage_error_without_stdout(self) -> None:
        result = self.run_cli(ROOT / "example.json", "--format", "yaml")

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid choice", result.stderr)

    def test_cli_invalid_packet_has_stderr_error_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"status": ', encoding="utf-8")
            for arguments in ((), ("--format", "json"), ("--format", "markdown")):
                with self.subTest(arguments=arguments):
                    result = self.run_cli(path, *arguments)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("pickup_preview: error:", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_cli_missing_file_has_stderr_error_without_traceback(self) -> None:
        for arguments in ((), ("--format", "json"), ("--format", "markdown")):
            with self.subTest(arguments=arguments):
                result = self.run_cli(ROOT / "does-not-exist.json", *arguments)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("pickup_preview: error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
