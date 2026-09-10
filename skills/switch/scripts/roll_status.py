#!/usr/bin/env python3
"""Print a small, read-only status panel for a managed Roll."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from typing import Any


KNOWN_STATES = {
    "awaiting_destination": "Awaiting destination - source released; other-device pickup has not started.",
    "handed_off": "Handed off - source released and destination pickup prepared; continuation belongs to Conductor.",
    "running": "Running - a worker is active.",
    "paused": "Paused - waiting to resume.",
    "continue": "Continue - ready for another useful piece.",
    "review": "Review - awaiting independent assessment (not accepted).",
    "blocked": "Blocked - the recorded blocker needs attention.",
    "uncertain": "Uncertain - the recorded state needs clarification.",
    "failed": "Failed - the Roll did not complete successfully.",
}

# CSI, OSC, and the remaining single-character ANSI escape forms.  Removing the
# whole sequence avoids turning an escaped colour code into misleading text.
ANSI_ESCAPE = re.compile(
    r"(?:\x1b\[[0-?]*[ -/]*[@-~]|\x9b[0-?]*[ -/]*[@-~]|"
    r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[@-_])"
)


class StatusError(Exception):
    """An expected, safely reportable status-reading failure."""


def safe_text(value: str) -> str:
    """Return saved text that cannot issue controls or create extra lines."""
    value = ANSI_ESCAPE.sub("", value)
    cleaned = []
    for character in value:
        category = unicodedata.category(character)
        if category.startswith("C") or category in {"Zl", "Zp"}:
            cleaned.append(" ")
        else:
            cleaned.append(character)
    return "".join(cleaned)


def git_value(project: str, option: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", project, "rev-parse", option],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        raise StatusError("Git could not be run; the Roll status was not read.") from exc

    values = result.stdout.splitlines()
    if result.returncode != 0 or len(values) != 1 or not values[0]:
        raise StatusError("The project is not a readable Git worktree.")
    return values[0]


def resolve_git_paths(project: str) -> tuple[Path, Path]:
    """Ask Git for both paths so linked worktrees and normal clones behave alike."""
    root = Path(git_value(project, "--show-toplevel"))
    git_dir = Path(git_value(project, "--absolute-git-dir"))
    return root, git_dir


def read_record(git_dir: Path) -> dict[str, Any]:
    ledger_path = git_dir / "roll" / "run.json"
    try:
        raw = ledger_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise StatusError("No Roll status record was found for this worktree.") from exc
    except (OSError, UnicodeError) as exc:
        raise StatusError("The Roll status record could not be read.") from exc

    try:
        record = json.loads(raw)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise StatusError("The Roll status record is not valid JSON.") from exc
    if not isinstance(record, dict):
        raise StatusError("The Roll status record must be a JSON object.")
    return record


def validate_record(record: dict[str, Any]) -> tuple[str, str, list[Any] | None]:
    status = record.get("status")
    if not isinstance(status, str):
        raise StatusError("The Roll status record has no valid status.")
    if status not in KNOWN_STATES:
        raise StatusError("The Roll status is unknown; no outcome was inferred.")

    next_action = record.get("next_action")
    if not isinstance(next_action, str) or not next_action:
        raise StatusError("The Roll status record has no valid next action.")

    if "history" not in record:
        history = None
    else:
        history = record["history"]
        if not isinstance(history, list):
            raise StatusError("The Roll status record has invalid history.")

    if history is not None:
        for item in history:
            if not isinstance(item, dict):
                raise StatusError("The Roll status record has invalid history.")
            prior_status = item.get("status")
            if prior_status is not None and (
                not isinstance(prior_status, str)
            ):
                raise StatusError("The Roll status record has invalid history.")
            if "context_trigger" in item and not (
                item["context_trigger"] is None
                or isinstance(item["context_trigger"], dict)
            ):
                raise StatusError("The Roll status record has invalid history.")
            if "context_readings" in item and not (
                item["context_readings"] is None
                or isinstance(item["context_readings"], list)
            ):
                raise StatusError("The Roll status record has invalid history.")

    return status, next_action, history


def history_lines(history: list[Any] | None) -> list[str]:
    if history is None:
        return ["History: unknown (not recorded)"]
    if not history:
        return ["History: no completed workers recorded"]

    last_status = history[-1].get("status")
    shown_last = last_status if last_status in KNOWN_STATES else "unknown"

    triggers = [item.get("context_trigger", "missing") for item in history]
    if any(isinstance(trigger, dict) for trigger in triggers):
        observed = "yes"
    elif any(trigger == "missing" for trigger in triggers):
        observed = "unknown"
    else:
        observed = "no"

    return [
        "History:",
        f"  Completed workers: {len(history)}",
        f"  Last returned status: {shown_last}",
        f"  Context-triggered Roll observed: {observed}",
    ]


def make_panel(root: Path, record: dict[str, Any]) -> str:
    status, next_action, history = validate_record(record)
    lines = [
        "Roll status",
        f"Project: {safe_text(os.fspath(root))}",
        f"State: {KNOWN_STATES[status]}",
        f"Next action: {safe_text(next_action)}",
        *history_lines(history),
        "Read result only; this does not mean the work passed.",
    ]
    return "\n".join(lines)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read a managed Roll's status without changing the project."
    )
    parser.add_argument("--project", required=True, help="path inside the Git worktree")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root, git_dir = resolve_git_paths(args.project)
        record = read_record(git_dir)
        panel = make_panel(root, record)
    except StatusError as exc:
        print(f"Roll status unavailable: {exc}", file=sys.stderr)
        return 1

    print(panel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
