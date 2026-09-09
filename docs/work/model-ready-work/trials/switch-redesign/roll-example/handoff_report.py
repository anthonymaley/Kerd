#!/usr/bin/env python3
"""Render a saved JSON work record as a read-only Markdown handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


STATUSES = ("done", "active", "blocked", "queued")
HEADINGS = {
    "done": "Done",
    "active": "Active",
    "blocked": "Blocked",
    "queued": "Queued",
}


class ValidationError(ValueError):
    """Raised when an input value does not match the handoff schema."""


def _required_string(value: Any, location: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{location} must be a string")
    if not value.strip():
        raise ValidationError(f"{location} must not be blank")
    if "\n" in value or "\r" in value:
        raise ValidationError(f"{location} must be a single-line string")
    return value


def _validate(data: Any) -> tuple[str, str, str, list[dict[str, str]]]:
    if not isinstance(data, dict):
        raise ValidationError("input must be a JSON object")

    project = _required_string(data.get("project"), "project")
    stage = _required_string(data.get("stage"), "stage")
    next_action = _required_string(data.get("next_action"), "next_action")

    tasks_value = data.get("tasks")
    if not isinstance(tasks_value, list):
        raise ValidationError("tasks must be a list")

    tasks: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for index, task_value in enumerate(tasks_value):
        location = f"tasks[{index}]"
        if not isinstance(task_value, dict):
            raise ValidationError(f"{location} must be an object")

        task_id = _required_string(task_value.get("id"), f"{location}.id")
        title = _required_string(task_value.get("title"), f"{location}.title")
        status = _required_string(task_value.get("status"), f"{location}.status")
        if status not in STATUSES:
            allowed = ", ".join(STATUSES)
            raise ValidationError(f"{location}.status must be one of: {allowed}")
        if task_id in seen_ids:
            raise ValidationError(f"duplicate task id: {task_id}")
        seen_ids.add(task_id)
        tasks.append({"id": task_id, "title": title, "status": status})

    return project, stage, next_action, tasks


def render_report(data: Any) -> str:
    """Validate *data* and return its Markdown handoff report."""

    project, stage, next_action, tasks = _validate(data)
    lines = [f"# Handoff: {project}", "", f"Stage: {stage}"]

    for status in STATUSES:
        matching = [task for task in tasks if task["status"] == status]
        if not matching:
            continue
        lines.extend(("", f"## {HEADINGS[status]}", ""))
        lines.extend(f"- `{task['id']}`: {task['title']}" for task in matching)

    lines.extend(("", "## Next action", "", next_action))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("error: expected exactly one JSON input path", file=sys.stderr)
        return 2

    try:
        with Path(args[0]).open("r", encoding="utf-8") as input_file:
            data = json.load(input_file)
        report = render_report(data)
    except (OSError, UnicodeError, json.JSONDecodeError, ValidationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
