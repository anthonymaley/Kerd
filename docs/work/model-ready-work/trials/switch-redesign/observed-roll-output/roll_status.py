#!/usr/bin/env python3
"""Print a small, human-readable status panel for a managed Roll."""

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
    "running": (
        "Running",
        "A worker is currently working on this Roll.",
    ),
    "paused": (
        "Paused",
        "The Roll is paused and will not advance until it is resumed.",
    ),
    "continue": (
        "Continue",
        "The last worker stopped at a safe boundary; useful work remains.",
    ),
    "review": (
        "Review",
        "The work is awaiting independent assessment; it has not been accepted.",
    ),
    "blocked": (
        "Blocked",
        "The Roll cannot advance until its blocker is resolved.",
    ),
    "uncertain": (
        "Uncertain",
        "The runtime could not establish a reliable state.",
    ),
    "failed": (
        "Failed",
        "The Roll stopped because the worker or runtime failed.",
    ),
}

# CSI and OSC are the common terminal escape forms. Remaining control/format
# characters are removed separately below.
ANSI_ESCAPE = re.compile(
    r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\)?)"
)


class RecordError(Exception):
    """A ledger record is absent or cannot be displayed safely."""


def safe_text(value: str) -> str:
    """Turn saved text into one terminal-safe, readable line."""
    value = ANSI_ESCAPE.sub("", value)
    value = "".join(" " if unicodedata.category(char).startswith("C") else char for char in value)
    return " ".join(value.split())


def git_locations(project: str) -> tuple[Path, Path]:
    """Ask Git for the worktree root and its actual private Git directory."""
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                project,
                "rev-parse",
                "--show-toplevel",
                "--absolute-git-dir",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, ValueError) as exc:
        raise RecordError("Git could not inspect the project.") from exc

    lines = result.stdout.splitlines()
    if result.returncode != 0 or len(lines) != 2 or not all(lines):
        raise RecordError("The project is not a readable Git worktree.")
    return Path(lines[0]), Path(lines[1])


def read_record(git_dir: Path) -> dict[str, Any]:
    record_path = git_dir / "roll" / "run.json"
    try:
        with record_path.open("r", encoding="utf-8") as handle:
            record = json.load(handle)
    except FileNotFoundError as exc:
        raise RecordError("No managed Roll record was found for this worktree.") from exc
    except json.JSONDecodeError as exc:
        raise RecordError("The managed Roll record is not valid JSON.") from exc
    except (OSError, UnicodeError) as exc:
        raise RecordError("The managed Roll record could not be read.") from exc

    if not isinstance(record, dict):
        raise RecordError("The managed Roll record must be a JSON object.")
    return record


def validate_current(record: dict[str, Any]) -> tuple[str, str]:
    status = record.get("status")
    if not isinstance(status, str):
        raise RecordError("The managed Roll record has a missing or invalid status.")
    if status not in KNOWN_STATES:
        raise RecordError("The managed Roll record contains an unknown status.")

    next_action = record.get("next_action")
    if not isinstance(next_action, str) or not next_action:
        raise RecordError("The managed Roll record has a missing or invalid next action.")
    next_action = safe_text(next_action)
    if not next_action:
        raise RecordError("The managed Roll record has no displayable next action.")
    return status, next_action


def history_summary(record: dict[str, Any]) -> tuple[str, str, str]:
    """Return worker count, last status, and context-trigger observation."""
    if "history" not in record:
        return "Unknown (history not recorded)", "Unknown", "Unknown"

    history = record["history"]
    if not isinstance(history, list):
        raise RecordError("The managed Roll record has invalid history.")

    saw_context_trigger = False
    context_known = True
    last_status = "None (no worker returns)"

    for entry in history:
        if not isinstance(entry, dict):
            raise RecordError("The managed Roll record has an invalid history entry.")

        returned_status = entry.get("status")
        if "status" in entry and not isinstance(returned_status, str):
            raise RecordError("The managed Roll record has an invalid historical status.")

        if "context_trigger" not in entry:
            context_known = False
        else:
            trigger = entry["context_trigger"]
            if trigger is not None and not isinstance(trigger, dict):
                raise RecordError("The managed Roll record has an invalid context trigger.")
            if isinstance(trigger, dict):
                saw_context_trigger = True

        if "context_readings" in entry:
            readings = entry["context_readings"]
            if readings is not None and not isinstance(readings, list):
                raise RecordError("The managed Roll record has invalid context readings.")

    if history:
        returned_status = history[-1].get("status")
        if returned_status in KNOWN_STATES:
            last_status = KNOWN_STATES[returned_status][0]
            if returned_status == "review":
                last_status += " (awaiting assessment, not accepted)"
        else:
            last_status = "Unknown"

    if saw_context_trigger:
        context_result = "Yes"
    elif not history:
        context_result = "No (no worker returns)"
    elif context_known:
        context_result = "No"
    else:
        context_result = "Unknown"

    return str(len(history)), last_status, context_result


def render(project_root: Path, record: dict[str, Any]) -> str:
    status, next_action = validate_current(record)
    workers, last_status, context_triggered = history_summary(record)
    label, explanation = KNOWN_STATES[status]
    project = safe_text(str(project_root))
    return "\n".join(
        [
            "Roll status",
            f"Project: {project}",
            f"Current: {label} — {explanation}",
            f"Next: {next_action}",
            "",
            f"Completed workers: {workers}",
            f"Last returned status: {last_status}",
            f"Context-triggered Roll observed: {context_triggered}",
            "History records workflow state, not proof of quality.",
        ]
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read a managed Roll's status.")
    parser.add_argument("--project", required=True, metavar="REPO", help="path inside the Git worktree")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        project_root, git_dir = git_locations(args.project)
        record = read_record(git_dir)
        panel = render(project_root, record)
    except RecordError as exc:
        print(f"Roll status unavailable: {exc}", file=sys.stderr)
        return 2

    print(panel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
