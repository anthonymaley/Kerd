#!/usr/bin/env python3
"""Print a small, read-only status panel for a managed Roll."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any


KNOWN_STATES = {
    "running": "Running — a worker is currently active.",
    "paused": "Paused — the Roll is waiting to be resumed.",
    "continue": "Continuing — another useful piece of work is expected.",
    "review": "Ready for review — awaiting independent assessment, not accepted.",
    "blocked": "Blocked — progress needs the stated blocker to be resolved.",
    "uncertain": "Uncertain — the saved state needs clarification.",
    "failed": "Failed — the Roll stopped after a failure.",
}

# CSI and OSC are the terminal-control forms most likely to occur in saved text.
ANSI_RE = re.compile(
    r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\)?)"
)


class StatusError(Exception):
    """A concise, user-facing error that must not include private record data."""


def safe_text(value: str) -> str:
    """Remove terminal controls while retaining ordinary saved text."""
    value = ANSI_RE.sub("", value)
    return "".join(
        " " if unicodedata.category(char) in {"Cc", "Cf"} else char
        for char in value
    )


def git_value(project: Path, argument: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(project), "rev-parse", argument],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
    except (OSError, UnicodeError):
        raise StatusError("Could not resolve the requested Git repository.") from None

    value = result.stdout.rstrip("\r\n")
    if result.returncode != 0 or not value:
        raise StatusError("Could not resolve the requested Git repository.")
    return value


def resolve_repository(project: Path) -> tuple[Path, Path]:
    root = Path(git_value(project, "--show-toplevel"))
    git_dir = Path(git_value(project, "--absolute-git-dir"))
    if not root.is_absolute() or not git_dir.is_absolute():
        raise StatusError("Git returned an invalid repository location.")
    return root, git_dir


def read_record(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise StatusError("No managed Roll record was found for this repository.") from None
    except (OSError, UnicodeError):
        raise StatusError("The managed Roll record could not be read.") from None

    try:
        record = json.loads(raw)
    except (json.JSONDecodeError, RecursionError):
        raise StatusError("The managed Roll record is not valid JSON.") from None
    if not isinstance(record, dict):
        raise StatusError("The managed Roll record must be a JSON object.")
    return record


def validate_record(record: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    status = record.get("status")
    if not isinstance(status, str):
        raise StatusError("The managed Roll record has an invalid status.")
    if status not in KNOWN_STATES:
        raise StatusError("The managed Roll record has an unknown status.")

    next_action = record.get("next_action")
    if not isinstance(next_action, str) or not next_action.strip():
        raise StatusError("The managed Roll record has an invalid next action.")

    history_value = record.get("history", [])
    if not isinstance(history_value, list):
        raise StatusError("The managed Roll record has invalid history.")

    history: list[dict[str, Any]] = []
    for entry in history_value:
        if not isinstance(entry, dict):
            raise StatusError("The managed Roll record has invalid history.")
        if "status" in entry and not isinstance(entry["status"], str):
            raise StatusError("The managed Roll record has invalid history.")
        if "context_trigger" in entry and entry["context_trigger"] is not None:
            if not isinstance(entry["context_trigger"], dict):
                raise StatusError("The managed Roll record has invalid history.")
        if "context_readings" in entry and entry["context_readings"] is not None:
            if not isinstance(entry["context_readings"], list):
                raise StatusError("The managed Roll record has invalid history.")
        history.append(entry)

    return status, next_action, history


def history_lines(history: list[dict[str, Any]]) -> list[str]:
    if not history:
        return ["Completed workers: 0", "Last returned status: unknown (no history)",
                "Context-triggered Roll observed: unknown (no history)"]

    last_value = history[-1].get("status")
    last_status = last_value if last_value in KNOWN_STATES else "unknown"

    saw_trigger = any(isinstance(item.get("context_trigger"), dict) for item in history)
    all_reported = all("context_trigger" in item for item in history)
    trigger = "yes" if saw_trigger else ("no" if all_reported else "unknown")

    return [
        f"Completed workers: {len(history)}",
        f"Last returned status: {last_status} (not proof of quality)",
        f"Context-triggered Roll observed: {trigger}",
    ]


def make_panel(root: Path, git_dir: Path, record: dict[str, Any]) -> str:
    status, next_action, history = validate_record(record)
    lines = [
        "Roll status",
        "-----------",
        f"Project: {safe_text(str(root))}",
        f"Record: {safe_text(str(git_dir / 'roll' / 'run.json'))}",
        f"State: {KNOWN_STATES[status]}",
        f"Next action: {safe_text(next_action)}",
        *history_lines(history),
        "Note: exit 0 means the status was read; it does not mean the work passed.",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read a managed Roll's private ledger and print a safe status panel."
    )
    parser.add_argument("--project", required=True, metavar="REPO", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root, git_dir = resolve_repository(args.project)
        record = read_record(git_dir / "roll" / "run.json")
        print(make_panel(root, git_dir, record))
        return 0
    except StatusError as error:
        print(f"Roll status unavailable: {error}", file=sys.stderr)
        return 1
    except Exception:
        # Malformed input and platform read/Git failures must never expose a traceback.
        print("Roll status unavailable: the status could not be read safely.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
