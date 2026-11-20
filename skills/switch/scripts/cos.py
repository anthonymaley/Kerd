#!/usr/bin/env python3
"""Optional chief-of-staff support: the on/off signal and the `### Queue` table in TODO.md's `## Now`.

Off unless ~/.config/kerd/chief-of-staff.json exists. With no file, `signal()` returns None
and nothing else here runs: callers show nothing and change nothing.

    cos.py status --project P [--scope S]   the signal as JSON; exit 0 on, 3 off
    cos.py write  --project P [--scope S]   rows JSON on stdin; exit 0 written, 2 invalid,
                                            3 off, 4 no TODO.md or no `## Now`, 5 changed underneath
    cos.py check  --project P [--scope S]   read-only validation; exit 0 valid, 2 invalid, 3 off

Config ({"repo": abs path, "projects": "all" | [abs paths], "skip": [abs paths]}; unknown keys
ignored; `~` expanded; every path compared after realpath). Precedence, fail closed: missing
file -> off (None); unreadable, invalid JSON or invalid schema -> off with `config_error`;
under `skip` -> off; `"chief_of_staff": false` (or an unreadable or invalid vault.json) in
kivna/vault.json of the project path or the repo root -> off; `projects` is "all" or holds
the project or a parent of it -> on; anything else -> off.

The project is realpath(--project), joined with one --scope when given (a scoped project
is its scope folder). More than one --scope, or a scope outside the project, is off.
Standard library only.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import unicodedata


CONFIG_PATH = "~/.config/kerd/chief-of-staff.json"

EXIT_OK = 0
EXIT_INVALID = 2
EXIT_OFF = 3
EXIT_NO_NOW = 4
EXIT_CHANGED = 5

STATUSES = ("queued", "in progress", "blocked")
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")
COLUMNS = ("Rank", "Task id", "Task", "Outcome", "Status", "ETA", "Depends on")
NO_DEPENDS = "—"  # an em dash, as `## Now` writes "none"
UNKNOWN_ETA = "unknown"
MAX_TEXT = 120
MAX_ETA = 30
MAX_QUALIFIER = 60
MAX_ROWS = 500  # Cosplay's reader refuses a longer table
ROW_KEYS = {"id", "task", "link", "outcome", "status", "qualifier", "eta", "depends"}

NOW_HEADING = re.compile(r"^##[ \t]+now\b", re.I)
SECTION_END = re.compile(r"^#{1,2}(?:[ \t]|$)")
QUEUE_HEADING = re.compile(r"^###[ \t]+Queue[ \t]*$")
FENCE = re.compile(r"^\s*(```|~~~)")
UPDATED = re.compile(r"^Updated:(.*)$")
SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
LINK_CHARS_REFUSED = set("()[]<>|\\\"'`")


class ConfigError(Exception):
    """The config file exists but cannot be used; the message names which and the bad key."""


# ------------------------------------------------------------------ the signal

def _under(path: str, base: str) -> bool:
    """True when `path` is `base` or a folder beneath it (prefix on whole path components)."""
    if path == base:
        return True
    prefix = base if base.endswith(os.sep) else base + os.sep
    return path.startswith(prefix)


def _real(value: str) -> str:
    return os.path.realpath(os.path.expanduser(value))


def _config_path(key: str, value) -> str:
    if not isinstance(value, str):
        raise ConfigError(f"invalid schema: {key} is not a string")
    expanded = os.path.expanduser(value)
    if not expanded or not os.path.isabs(expanded):
        raise ConfigError(f"invalid schema: {key} is not an absolute path")
    try:
        return os.path.realpath(expanded)
    except (OSError, ValueError):
        raise ConfigError(f"invalid schema: {key} is not a usable path")


def _path_list(key: str, value) -> list:
    if not isinstance(value, list):
        raise ConfigError(f"invalid schema: {key} is not a list")
    return [_config_path(f"{key}[{n}]", item) for n, item in enumerate(value)]


def load_config(path: str) -> dict:
    """Read and validate the config; raises ConfigError naming unreadable, invalid JSON or invalid schema."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as error:
        raise ConfigError("unreadable: " + (error.strerror or type(error).__name__))
    try:
        data = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError:
        raise ConfigError("invalid JSON: not UTF-8")
    except ValueError as error:
        raise ConfigError(f"invalid JSON: {error}")
    if not isinstance(data, dict):
        raise ConfigError("invalid schema: the top level is not an object")
    for key in ("repo", "projects"):
        if key not in data:
            raise ConfigError(f"invalid schema: {key} is missing")
    config = {"repo": _config_path("repo", data["repo"])}
    projects = data["projects"]
    if projects == "all":
        config["projects"] = "all"
    elif isinstance(projects, str):
        raise ConfigError('invalid schema: projects is neither "all" nor a list')
    else:
        config["projects"] = _path_list("projects", projects)
    config["skip"] = _path_list("skip", data.get("skip", []))
    return config


def project_identity(project: str, scopes) -> tuple:
    """(root, project path, None) or (root, None, why off).

    The project path is realpath(project), or its one scope folder. A scope must be a folder
    inside the project, named relative to it; it is never the root and never leaves the root.
    """
    root = _real(project)
    scopes = list(scopes or [])
    if not scopes:
        return root, root, None
    if len(scopes) > 1:
        return root, None, "more than one --scope names no single project"
    scope = scopes[0]
    if not isinstance(scope, str) or not scope or os.path.isabs(scope) or "\0" in scope:
        return root, None, f"refused: scope {scope!r} is not a folder named relative to the project"
    target = os.path.realpath(os.path.join(root, scope))
    if target == root:
        return root, None, "refused: the project root is not a scope"
    if not _under(target, root):
        return root, None, f"refused: scope {scope!r} is outside the project"
    if not os.path.isdir(target):
        return root, None, f"refused: scope {scope!r} is not a folder in the project"
    return root, target, None


def vault_opt_out(folder: str) -> tuple:
    """(opted out, problem) for folder/kivna/vault.json. A problem (unreadable, invalid) means off."""
    path = os.path.join(folder, "kivna", "vault.json")
    if not os.path.lexists(path):
        return False, None
    try:
        with open(path, "rb") as handle:
            data = json.loads(handle.read().decode("utf-8"))
    except OSError as error:
        return False, f"{path} is unreadable ({error.strerror or type(error).__name__})"
    except ValueError:
        return False, f"{path} is not valid JSON"
    if not isinstance(data, dict):
        return False, f"{path} is not a JSON object"
    if "chief_of_staff" not in data:
        return False, None
    value = data["chief_of_staff"]
    if not isinstance(value, bool):
        return False, f"{path}: chief_of_staff is not true or false"
    return (not value), None


def _result(on: bool, is_cos_repo: bool, why: str, config_error=None) -> dict:
    return {"on": on, "is_cos_repo": is_cos_repo, "why": why, "config_error": config_error}


def signal(project: str, scopes: list[str] | None = None, config_path: str | None = None) -> dict | None:
    """The chief-of-staff signal for one project, read fresh. None when the config file is
    absent or cannot even be stat'ed: the silent off path, where callers show nothing."""
    path = os.path.expanduser(config_path or CONFIG_PATH)
    try:
        os.stat(path)
    except (OSError, ValueError):
        return None
    try:
        config = load_config(path)
    except ConfigError as error:
        return _result(False, False, f"config error: {error}", str(error))

    root, identity, refused = project_identity(project, scopes)
    if identity is None:
        return _result(False, False, refused)
    is_cos_repo = identity == config["repo"]

    for entry in config["skip"]:
        if _under(identity, entry):
            return _result(False, is_cos_repo, f"skipped: under {entry}")
    for folder in dict.fromkeys([identity, root]):
        opted, problem = vault_opt_out(folder)
        if problem:
            return _result(False, is_cos_repo, f"off: {problem}")
        if opted:
            return _result(False, is_cos_repo,
                           f"opted out: chief_of_staff is false in {os.path.join(folder, 'kivna', 'vault.json')}")
    if config["projects"] == "all":
        return _result(True, is_cos_repo, 'projects is "all"')
    for entry in config["projects"]:
        if _under(identity, entry):
            return _result(True, is_cos_repo, f"listed in projects: {entry}")
    return _result(False, is_cos_repo, "not in projects")


def off_payload(sig) -> dict:
    return {"on": False, "why": "no config"} if sig is None else sig


# --------------------------------------------------------------- field grammar

def escape(text: str) -> str:
    """One table cell's text: backslash and pipe escaped."""
    return text.replace("\\", "\\\\").replace("|", "\\|")


def _single_line(text: str) -> bool:
    return not any(unicodedata.category(c) in ("Cc", "Zl", "Zp") for c in text)


def link_problem(link: str):
    """Why a link is refused, or None. A relative path, a `notes:` path or an https URL."""
    if not link:
        return "is empty"
    if not _single_line(link) or any(c.isspace() for c in link):
        return "has a space or a line break"
    if any(c in LINK_CHARS_REFUSED for c in link):
        return "has a bracket, parenthesis, quote, pipe or backslash"
    if link.startswith("notes:"):
        return None if len(link) > len("notes:") else "names no notes path"
    if link.startswith("https://"):
        return None if len(link) > len("https://") and not link[len("https://")].startswith("/") \
            else "names no host"
    if link.startswith("/"):
        return "is an absolute path; use a path relative to the project"
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link):
        return "is neither a relative path, a notes: path nor an https URL"
    return None


def _text(row: dict, key: str, where: str, errors: list, limit: int, required: bool = True,
          empty_ok: bool = False):
    if key not in row:
        if required:
            errors.append(f"{where}: {key} is missing")
        return None
    value = row[key]
    if not isinstance(value, str):
        errors.append(f"{where}: {key} is not a string")
        return None
    if not _single_line(value):
        errors.append(f"{where}: {key} has a line break or control character")
        return None
    value = value.strip()
    if not value and not empty_ok:
        errors.append(f"{where}: {key} is empty")
        return None
    if len(value) > limit:
        errors.append(f"{where}: {key} is longer than {limit} characters")
        return None
    return value


def validate_rows(data) -> tuple:
    """(normalized rows, errors). Rank is the array order. Normalized: text trimmed, empty eta -> unknown."""
    errors = []
    if not isinstance(data, list):
        return [], ["the table must be a JSON array of rows"]
    if len(data) > MAX_ROWS:
        return [], [f"more than {MAX_ROWS} rows"]
    rows, ids = [], []
    for n, row in enumerate(data, 1):
        where = f"row {n}"
        if not isinstance(row, dict):
            errors.append(f"{where}: not an object")
            ids.append(None)
            continue
        unknown = sorted(set(row) - ROW_KEYS)
        if unknown:
            errors.append(f"{where}: unknown key(s) {', '.join(unknown)}")
        out = {}
        task_id = row.get("id")
        if not isinstance(task_id, str) or not ID_PATTERN.match(task_id):
            errors.append(f"{where}: id must match {ID_PATTERN.pattern}")
            task_id = None
        elif task_id in ids:
            errors.append(f"{where}: id {task_id} appears twice")
        ids.append(task_id)
        out["id"] = task_id
        task = _text(row, "task", where, errors, MAX_TEXT)
        if task is not None and ("[" in task or "]" in task):
            errors.append(f"{where}: task has a square bracket")
        out["task"] = task
        if "link" in row:
            link = row["link"]
            if not isinstance(link, str):
                errors.append(f"{where}: link is not a string")
            else:
                problem = link_problem(link)
                if problem:
                    errors.append(f"{where}: link {problem}")
                out["link"] = link
        out["outcome"] = _text(row, "outcome", where, errors, MAX_TEXT)
        status = row.get("status")
        if status == "done":
            errors.append(f"{where}: a done row is refused; write the table without it")
        elif status not in STATUSES:
            errors.append(f"{where}: status must be one of {', '.join(STATUSES)}")
        out["status"] = status
        if "qualifier" in row:
            qualifier = _text(row, "qualifier", where, errors, MAX_QUALIFIER)
            if qualifier is not None and ("|" in qualifier or ")" in qualifier):
                errors.append(f"{where}: qualifier has | or )")
            out["qualifier"] = qualifier
        eta = _text(row, "eta", where, errors, MAX_ETA, empty_ok=True)
        out["eta"] = eta or UNKNOWN_ETA
        depends = row.get("depends", [])
        if not isinstance(depends, list) or not all(isinstance(d, str) for d in depends):
            errors.append(f"{where}: depends must be a list of task ids")
            depends = []
        out["depends"] = depends
        rows.append(out)
    known = set(i for i in ids if i)
    for n, row in enumerate(rows, 1):
        seen = set()
        for dep in row["depends"]:
            if dep == row["id"]:
                errors.append(f"row {n}: depends on itself")
            elif dep not in known:
                errors.append(f"row {n}: depends on {dep!r}, which is not a task id in the table")
            elif dep in seen:
                errors.append(f"row {n}: depends lists {dep} twice")
            seen.add(dep)
    return rows, errors


# ------------------------------------------------------------------- rendering

def _status_cell(row: dict) -> str:
    qualifier = row.get("qualifier")
    return row["status"] + (f" ({escape(qualifier)})" if qualifier else "")


def render_block(rows: list, stamp: str) -> list:
    """The `### Queue` block as lines without line endings."""
    lines = ["### Queue", "", "| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    for rank, row in enumerate(rows, 1):
        task = escape(row["task"])
        if row.get("link"):
            task = f"[{task}]({row['link']})"
        depends = ", ".join(row["depends"]) or NO_DEPENDS
        cells = [str(rank), row["id"], task, escape(row["outcome"]), _status_cell(row),
                 escape(row["eta"]), depends]
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", f"Updated: {stamp}"]
    return lines


def clock_stamp(now: datetime | None = None) -> str:
    """ISO 8601 with offset, to the second, from the clock (local time)."""
    moment = now if now is not None else datetime.now().astimezone()
    if moment.tzinfo is None:
        moment = moment.astimezone()
    return moment.replace(microsecond=0).isoformat()


# -------------------------------------------------------------- locating Now

def _blank(line: str) -> bool:
    return not line.strip()


def _bare(line: str) -> str:
    return line.rstrip("\r\n")


def scan(lines: list) -> tuple:
    """(Now heading index or None, index where Now ends, `### Queue` heading indexes in Now).
    Lines inside ``` or ~~~ fences are never headings."""
    fence, now, end, queues = None, None, len(lines), []
    for i, raw in enumerate(lines):
        line = _bare(raw)
        marker = FENCE.match(line)
        if marker:
            if fence is None:
                fence = marker.group(1)
            elif marker.group(1) == fence:
                fence = None
            continue
        if fence is not None:
            continue
        if now is None:
            if NOW_HEADING.match(line):
                now = i
            continue
        if SECTION_END.match(line):
            end = i
            break
        if QUEUE_HEADING.match(line):
            queues.append(i)
    return now, end, queues


def block_end(lines: list, start: int, stop: int) -> int:
    """End (exclusive) of the block whose heading is lines[start]: the heading, blank lines, the
    contiguous pipe-table lines, then blank lines and one `Updated:` line when present. Never
    takes anything else, so hand-written Now content after a damaged block is kept."""
    end = start + 1
    i = end
    while i < stop and _blank(lines[i]):
        i += 1
    while i < stop and lines[i].lstrip().startswith("|"):
        i += 1
        end = i
    j = end
    while j < stop and _blank(lines[j]):
        j += 1
    if j < stop and UPDATED.match(_bare(lines[j])):
        end = j + 1
    return end


def _first_child(lines: list, now: int, queue: int) -> bool:
    return all(_blank(line) for line in lines[now + 1:queue])


# --------------------------------------------------------------------- parsing

def split_cells(line: str):
    """Cells of a table row with escapes kept, or None when the row is not `| ... |`."""
    text = line.strip()
    if not (text.startswith("|") and text.endswith("|")) or len(text) < 2:
        return None
    cells, current, i = [], "", 1
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text):
            current += text[i:i + 2]
            i += 2
            continue
        if char == "|":
            cells.append(current.strip())
            current = ""
        else:
            current += char
        i += 1
    if current.strip():
        return None  # the closing pipe was escaped
    return cells


def unescape(raw: str):
    """Undo `escape`; None when a backslash escapes anything but a backslash or a pipe."""
    out, i = "", 0
    while i < len(raw):
        if raw[i] == "\\":
            if i + 1 < len(raw) and raw[i + 1] in "\\|":
                out += raw[i + 1]
                i += 2
                continue
            return None
        out += raw[i]
        i += 1
    return out


def _parse_row(cells: list, n: int, errors: list) -> dict:
    where = f"row {n}"
    rank, task_id, task_raw, outcome_raw, status_raw, eta_raw, depends_raw = cells
    row = {}
    if rank != str(n):
        errors.append(f"{where}: rank is {rank!r}, expected {n}")
    if not ID_PATTERN.match(task_id):
        errors.append(f"{where}: task id {task_id!r} must match {ID_PATTERN.pattern}")
    row["id"] = task_id
    linked = re.match(r"^\[([^\[\]]*)\]\(([^()]*)\)$", task_raw)
    if linked:
        task_raw, link = linked.group(1), linked.group(2)
        problem = link_problem(link)
        if problem:
            errors.append(f"{where}: link {problem}")
    elif "[" in task_raw or "]" in task_raw:
        errors.append(f"{where}: task has a square bracket outside a link")
        link = None
    else:
        link = None
    task = unescape(task_raw)
    if task is None:
        errors.append(f"{where}: task has a stray backslash")
    elif not task.strip() or len(task) > MAX_TEXT:
        errors.append(f"{where}: task is empty or longer than {MAX_TEXT} characters")
    row["task"] = task
    if link is not None:
        row["link"] = link
    outcome = unescape(outcome_raw)
    if outcome is None:
        errors.append(f"{where}: outcome has a stray backslash")
    elif not outcome.strip() or len(outcome) > MAX_TEXT:
        errors.append(f"{where}: outcome is empty or longer than {MAX_TEXT} characters")
    row["outcome"] = outcome
    status = re.match(r"^(queued|in progress|blocked)(?: \((.*)\))?$", status_raw)
    if status_raw == "done" or status_raw.startswith("done "):
        errors.append(f"{where}: a done row should have left the table")
        row["status"] = "done"
    elif not status:
        errors.append(f"{where}: status {status_raw!r} is not one of {', '.join(STATUSES)} "
                      "with an optional (qualifier)")
        row["status"] = status_raw
    else:
        row["status"] = status.group(1)
        if status.group(2) is not None:
            qualifier = unescape(status.group(2))
            if qualifier is None or not qualifier.strip() or ")" in qualifier or "|" in qualifier \
                    or len(qualifier) > MAX_QUALIFIER:
                errors.append(f"{where}: qualifier must be 1-{MAX_QUALIFIER} characters without | or )")
            row["qualifier"] = qualifier
    eta = unescape(eta_raw)
    if eta is None or not eta.strip() or len(eta) > MAX_ETA:
        errors.append(f"{where}: ETA must be 1-{MAX_ETA} characters (unknown when not known)")
    row["eta"] = eta
    if depends_raw == NO_DEPENDS:
        row["depends"] = []
    else:
        row["depends"] = [d.strip() for d in depends_raw.split(",")]
    return row


def parse_block(lines: list) -> tuple:
    """(rows, Updated stamp, errors) for a `### Queue` block (lines without endings), in the
    grammar `render_block` writes."""
    errors = []
    if not lines or not QUEUE_HEADING.match(lines[0]):
        return [], None, ["no ### Queue heading"]
    i = 1
    while i < len(lines) and _blank(lines[i]):
        i += 1
    table = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        table.append(lines[i])
        i += 1
    while i < len(lines) and _blank(lines[i]):
        i += 1
    stamp = None
    if i < len(lines) and UPDATED.match(lines[i]):
        value = UPDATED.match(lines[i]).group(1).strip()
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            parsed = None
        if parsed is None or parsed.tzinfo is None or "T" not in value:
            errors.append(f"Updated {value!r} is not an ISO 8601 time with an offset")
        stamp = value
    else:
        errors.append("missing Updated: line after the table")
    if len(table) < 2:
        errors.append("no table under ### Queue (needs the header row and the separator)")
        return [], stamp, errors
    header = split_cells(table[0])
    if header is None or tuple(header) != COLUMNS:
        errors.append("columns must be: " + " | ".join(COLUMNS))
        return [], stamp, errors
    separator = split_cells(table[1])
    if separator is None or len(separator) != len(COLUMNS) or not all(SEPARATOR_CELL.match(c) for c in separator):
        errors.append("the second table line is not the separator row")
        return [], stamp, errors
    body = table[2:]
    if len(body) > MAX_ROWS:
        errors.append(f"more than {MAX_ROWS} rows")
        return [], stamp, errors
    rows = []
    for n, line in enumerate(body, 1):
        cells = split_cells(line)
        if cells is None or len(cells) != len(COLUMNS):
            errors.append(f"row {n}: expected {len(COLUMNS)} cells")
            continue
        rows.append(_parse_row(cells, n, errors))
    seen = set()
    for n, row in enumerate(rows, 1):
        if row["id"] in seen:
            errors.append(f"row {n}: task id {row['id']} appears twice")
        seen.add(row["id"])
    for n, row in enumerate(rows, 1):
        listed = set()
        for dep in row["depends"]:
            if dep == row["id"]:
                errors.append(f"row {n}: depends on itself")
            elif dep not in seen:
                errors.append(f"row {n}: depends on {dep!r}, which is not a task id in the table")
            elif dep in listed:
                errors.append(f"row {n}: depends lists {dep} twice")
            listed.add(dep)
    return rows, stamp, errors


# -------------------------------------------------------------------- actions

def todo_path(project: str, scopes) -> str:
    return os.path.join(project_identity(project, scopes)[1], "TODO.md")


def _read_todo(path: str) -> tuple:
    """(bytes, text, problem). A problem means exit 4."""
    try:
        info = os.lstat(path)
    except OSError:
        return None, None, f"no TODO.md at {path}"
    if not stat.S_ISREG(info.st_mode):
        return None, None, f"{path} is not a regular file (a symlink or folder); not touched"
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as error:
        return None, None, f"cannot read {path}: {error.strerror or error}"
    try:
        return data, data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, None, f"{path} is not UTF-8"


def _hash(data) -> str | None:
    return None if data is None else hashlib.sha256(data).hexdigest()


def compose(text: str, rows: list, stamp: str) -> tuple:
    """(new text, problem kind, message). Replaces or creates the block as Now's first child;
    every byte outside the block is kept."""
    lines = text.splitlines(keepends=True)
    now, end, queues = scan(lines)
    if now is None:
        return None, EXIT_NO_NOW, "TODO.md has no ## Now section"
    if len(queues) > 1:
        return None, EXIT_INVALID, "## Now holds more than one ### Queue block; keep one and retry"
    newline = "\r\n" if lines[now].endswith("\r\n") else "\n"
    block = newline.join(render_block(rows, stamp)) + newline
    if queues and _first_child(lines, now, queues[0]):
        start = queues[0]
        stop = block_end(lines, start, end)
        return "".join(lines[:start]) + block + "".join(lines[stop:]), None, None
    if queues:  # the block exists further down Now: lift it out, then place it first
        start = queues[0]
        stop = block_end(lines, start, end)
        if start > 0 and _blank(lines[start - 1]):
            while stop < len(lines) and stop < end and _blank(lines[stop]):
                stop += 1
        lines = lines[:start] + lines[stop:]
    head = lines[now]
    if not head.endswith("\n"):
        head += newline
    after = lines[now + 1:]
    inserted = newline + block
    if after and not _blank(after[0]):
        inserted += newline
    return "".join(lines[:now]) + head + inserted + "".join(after), None, None


def write_queue(project: str, scopes, rows_json: str, config_path: str | None = None,
                now: datetime | None = None, before_commit=None) -> tuple:
    """(exit code, payload). `before_commit` is a test seam called after the read, before the
    final config re-check and hash compare."""
    sig = signal(project, scopes, config_path)
    if sig is None or not sig["on"]:
        return EXIT_OFF, off_payload(sig)
    try:
        data = json.loads(rows_json)
    except ValueError as error:
        return EXIT_INVALID, {"errors": [f"stdin is not valid JSON: {error}"]}
    rows, errors = validate_rows(data)
    if errors:
        return EXIT_INVALID, {"errors": errors}
    path = todo_path(project, scopes)
    original, text, problem = _read_todo(path)
    if problem:
        return EXIT_NO_NOW, {"error": problem}
    stamp = clock_stamp(now)
    updated, kind, message = compose(text, rows, stamp)
    if kind is not None:
        return kind, ({"errors": [message]} if kind == EXIT_INVALID else {"error": message})
    folder = os.path.dirname(path)
    mode = stat.S_IMODE(os.stat(path).st_mode)
    handle, temp = tempfile.mkstemp(prefix=".TODO.md.", suffix=".cos", dir=folder)
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(updated.encode("utf-8"))
            out.flush()
            os.fsync(out.fileno())
        os.chmod(temp, mode)
        if before_commit is not None:
            before_commit()
        sig = signal(project, scopes, config_path)
        if sig is None or not sig["on"]:
            return EXIT_OFF, off_payload(sig)
        try:
            with open(path, "rb") as current:
                now_bytes = current.read()
        except OSError:
            now_bytes = None
        if _hash(now_bytes) != _hash(original):
            return EXIT_CHANGED, {"error": "TODO.md changed underneath; re-read and retry"}
        os.replace(temp, path)
        temp = None
    finally:
        if temp is not None:
            try:
                os.unlink(temp)
            except OSError:
                pass
    return EXIT_OK, {"written": path, "rows": rows, "updated": stamp}


def check_queue(project: str, scopes, config_path: str | None = None) -> tuple:
    """(exit code, payload). Read-only: never writes."""
    sig = signal(project, scopes, config_path)
    if sig is None or not sig["on"]:
        return EXIT_OFF, off_payload(sig)
    path = todo_path(project, scopes)
    _, text, problem = _read_todo(path)
    if problem:
        return EXIT_INVALID, {"valid": False, "errors": [problem]}
    lines = text.splitlines(keepends=True)
    now, end, queues = scan(lines)
    if now is None:
        return EXIT_INVALID, {"valid": False, "errors": ["TODO.md has no ## Now section"]}
    if not queues:
        return EXIT_INVALID, {"valid": False, "errors": ["## Now has no ### Queue heading"]}
    errors = []
    if len(queues) > 1:
        errors.append("## Now holds more than one ### Queue block")
    if not _first_child(lines, now, queues[0]):
        errors.append("### Queue is not the first block of ## Now")
    stop = block_end(lines, queues[0], end)
    rows, stamp, block_errors = parse_block([_bare(line) for line in lines[queues[0]:stop]])
    errors += block_errors
    if errors:
        return EXIT_INVALID, {"valid": False, "errors": errors}
    return EXIT_OK, {"valid": True, "rows": rows, "updated": stamp}


# ------------------------------------------------------------------------ CLI

def main(argv=None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--project", required=True, help="Project root (Kerd's --project)")
    common.add_argument("--scope", action="append", default=[], metavar="FOLDER",
                        help="The scoped project's folder, relative to the project; more than one is off")
    common.add_argument("--config", default=None, help=argparse.SUPPRESS)  # tests: never the real file
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("status", parents=[common], help="Print the signal; exit 0 on, 3 off")
    sub.add_parser("write", parents=[common], help="Write the ### Queue block from rows JSON on stdin")
    sub.add_parser("check", parents=[common], help="Validate the ### Queue block; never writes")
    args = parser.parse_args(argv)

    if args.action == "status":
        sig = signal(args.project, args.scope, args.config)
        code, payload = (EXIT_OK if sig and sig["on"] else EXIT_OFF), off_payload(sig)
    elif args.action == "write":
        code, payload = write_queue(args.project, args.scope, sys.stdin.read(), args.config)
    else:
        code, payload = check_queue(args.project, args.scope, args.config)
    print(json.dumps(payload, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
