#!/usr/bin/env python3
"""Optional chief-of-staff support: the on/off signal, the `### Queue` table in TODO.md's `## Now`
and the `### Asks` table of open decisions directly under it.

Off unless ~/.config/kerd/chief-of-staff.json exists. With no file, `signal()` returns None
and nothing else here runs: callers show nothing and change nothing.

    cos.py status --project P [--scope S]   the signal as JSON; exit 0 on, 3 off
    cos.py write  --project P [--scope S]   rows JSON on stdin; exit 0 written, 2 invalid,
                                            3 off, 4 no TODO.md or no `## Now`, 5 changed underneath
    cos.py ask    --project P [--scope S]   one open decision as JSON on stdin, added to `### Asks`
                  [--again]                 the same id asked again because a fact behind it changed
                  [--answered ID]           that ask leaves the table (no stdin); exit codes as write
    cos.py check  --project P [--scope S]   read-only validation of both tables; exit 0 valid,
                                            2 invalid, 3 off

When on, the signal carries `relay`: "decisions" when kivna/vault.json's
`chief_of_staff_relay` says so in the project (and its root, when scoped), else "none".
Unset is "none"; "none" in either file wins; any other value is "none" with `relay_warning`.
"decisions" means an answer relayed by the chief of staff counts for a decision, never for a
push, release, install or live change. Each `### Asks` row says where its answer counts:
"relay ok" or "this window".

Config ({"repo": abs path, "projects": "all" | [abs paths], "skip": [abs paths]}; unknown keys
ignored; `~` expanded; every path compared after realpath). Precedence, fail closed: missing
file -> off (None); unreadable, invalid JSON or invalid schema -> off with `config_error`;
under `skip` -> off; `"chief_of_staff": false` (or an unreadable or invalid vault.json) in
kivna/vault.json of the project path or the repo root -> off; `projects` is "all" or holds
the project or a parent of it -> on; anything else -> off.

The project is realpath(--project), joined with one --scope when given (a scoped project
is its scope folder). More than one --scope, or a scope outside the project, is off.
`is_cos_repo` is true only when the signal is on and the project is the config's `repo`.

`write` and `ask` are a compare-and-swap at the last moment, not a locked one: each re-checks
the config and compares TODO.md's SHA-256 with the one it read as the very last steps before
os.replace. A write by another program in the microseconds between that final check and the
replace can still be lost; nothing here can stop that, because editors take no lock.

Field grammar: every rendered field is one line; a backslash is refused in every field
(Cosplay's reader unescapes only `\\|`), and `|` is written as `\\|`. `check` reads the same
grammar back. Whole-field patterns use fullmatch, so a trailing newline never slips past `$`.
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
ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{0,39}")  # always fullmatch
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
QUEUE_HEADING = re.compile(r"###[ \t]+Queue[ \t]*")  # fullmatch on a bare line
FENCE = re.compile(r"^\s*(```|~~~)")
UPDATED = re.compile(r"Updated:(.*)")  # fullmatch on a bare line
SEPARATOR_CELL = re.compile(r":?-{3,}:?")  # fullmatch
LINK_CHARS_REFUSED = set("()[]<>|\\\"'`")

ASKS_HEADING = re.compile(r"###[ \t]+Asks[ \t]*")  # fullmatch on a bare line
ASK_COLUMNS = ("Ask id", "Question", "Default", "Why", "Blocks", "Asked", "Answer where")
ASK_KEYS = {"id", "question", "default", "why", "blocks", "link", "operation"}
ASK_STAMPED = {"asked": "asked is stamped from the clock; leave it out",
               "answer_where": "answer_where comes from chief_of_staff_relay; leave it out"}
MAX_ASKS = 50
RELAY_KEY = "chief_of_staff_relay"
RELAY_VALUES = ("none", "decisions")
THIS_WINDOW = "this window"
RELAY_OK = "relay ok"
NO_BLOCKS = NO_DEPENDS
KEEP = object()  # compose_now: keep the existing block as it is


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


def relay_rule(folders) -> tuple:
    """(relay, warning) from `chief_of_staff_relay` in each folder's kivna/vault.json.

    "decisions" only when every file that sets the key says "decisions"; unset is "none" and
    "none" in either file wins (fail closed). Any other value is "none" with a warning."""
    found, warning = [], None
    for folder in folders:
        path = os.path.join(folder, "kivna", "vault.json")
        if not os.path.lexists(path):
            continue
        try:
            with open(path, "rb") as handle:
                data = json.loads(handle.read().decode("utf-8"))
        except (OSError, ValueError):
            return "none", f'{path} could not be read; {RELAY_KEY} read as "none"'
        if not isinstance(data, dict) or RELAY_KEY not in data:
            continue
        value = data[RELAY_KEY]
        if not isinstance(value, str) or value not in RELAY_VALUES:
            warning = warning or f'{path}: {RELAY_KEY} is not "none" or "decisions"; read as "none"'
            found.append("none")
        else:
            found.append(value)
    if warning:
        return "none", warning
    return ("decisions" if found and all(v == "decisions" for v in found) else "none"), None


def _on(is_cos_repo: bool, why: str, folders) -> dict:
    """The on result, with the project's relay rule beside it."""
    result = _result(True, is_cos_repo, why)
    result["relay"], result["relay_warning"] = relay_rule(folders)
    return result


def _result(on: bool, is_cos_repo: bool, why: str, config_error=None) -> dict:
    """`is_cos_repo` is reported only when on: a skipped, opted-out or unlisted repo shows no role."""
    return {"on": on, "is_cos_repo": bool(on and is_cos_repo), "why": why, "config_error": config_error}


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
    folders = list(dict.fromkeys([identity, root]))
    if config["projects"] == "all":
        return _on(is_cos_repo, 'projects is "all"', folders)
    for entry in config["projects"]:
        if _under(identity, entry):
            return _on(is_cos_repo, f"listed in projects: {entry}", folders)
    return _result(False, is_cos_repo, "not in projects")


def off_payload(sig) -> dict:
    return {"on": False, "why": "no config"} if sig is None else sig


# --------------------------------------------------------------- field grammar

def escape(text: str) -> str:
    """One table cell's text: `|` written as `\\|`. A backslash never reaches here (refused)."""
    return text.replace("|", "\\|")


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
    if "\\" in value:
        errors.append(f"{where}: {key} has a backslash")
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
        if not isinstance(task_id, str) or not ID_PATTERN.fullmatch(task_id):
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
    """(Now heading index or None, index where Now ends, `### Queue` heading indexes in Now)."""
    return scan_now(lines)[:3]


def scan_now(lines: list) -> tuple:
    """(Now heading index or None, index where Now ends, `### Queue` and `### Asks` heading
    indexes in Now). Lines inside ``` or ~~~ fences are never headings."""
    fence, now, end, queues, asks = None, None, len(lines), [], []
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
        if QUEUE_HEADING.fullmatch(line):
            queues.append(i)
        elif ASKS_HEADING.fullmatch(line):
            asks.append(i)
    return now, end, queues, asks


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
    if j < stop and UPDATED.fullmatch(_bare(lines[j])):
        end = j + 1
    return end


def _first_child(lines: list, now: int, queue: int) -> bool:
    return all(_blank(line) for line in lines[now + 1:queue])


# --------------------------------------------------------------------- parsing

def split_cells(line: str):
    """Cells of a table row with escapes kept, or None when the row is not `| ... |`.

    Split as Cosplay's reader splits: a `|` right after a backslash is part of the cell, every
    other `|` ends one. Any other backslash stays in the cell, for `unescape` to refuse."""
    text = line.strip()
    if not (text.startswith("|") and text.endswith("|")) or len(text) < 2:
        return None
    cells, current, i = [], "", 1
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text) and text[i + 1] == "|":
            current += "\\|"
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
    """Undo `escape`; None for any backslash that is not `\\|` (write refuses backslashes)."""
    out, i = "", 0
    while i < len(raw):
        if raw[i] == "\\":
            if i + 1 < len(raw) and raw[i + 1] == "|":
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
    if not ID_PATTERN.fullmatch(task_id):
        errors.append(f"{where}: task id {task_id!r} must match {ID_PATTERN.pattern}")
    row["id"] = task_id
    linked = re.fullmatch(r"\[([^\[\]]*)\]\(([^()]*)\)", task_raw)
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
    status = re.fullmatch(r"(queued|in progress|blocked)(?: \((.*)\))?", status_raw)
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
    if not lines or not QUEUE_HEADING.fullmatch(lines[0]):
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
    if i < len(lines) and UPDATED.fullmatch(lines[i]):
        value = UPDATED.fullmatch(lines[i]).group(1).strip()
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
    if separator is None or len(separator) != len(COLUMNS) or not all(SEPARATOR_CELL.fullmatch(c) for c in separator):
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


# ------------------------------------------------------------ the Asks table

def _id_list(value, where: str, key: str, errors: list) -> list:
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        errors.append(f"{where}: {key} must be a list of task ids")
        return []
    seen = []
    for item in value:
        if not ID_PATTERN.fullmatch(item):
            errors.append(f"{where}: {key} {item!r} must match {ID_PATTERN.pattern}")
        elif item in seen:
            errors.append(f"{where}: {key} lists {item} twice")
        seen.append(item)
    return value


def validate_ask(data) -> tuple:
    """(normalized ask, errors) for one open decision: id, question, default and why are
    required (a decision without a default is refused); blocks lists task ids; link and
    operation (true for a push, release, install or live change) are optional."""
    errors, where = [], "ask"
    if not isinstance(data, dict):
        return None, ["the ask must be one JSON object"]
    for key in sorted(set(data) & set(ASK_STAMPED)):
        errors.append(f"{where}: {ASK_STAMPED[key]}")
    unknown = sorted(set(data) - ASK_KEYS - set(ASK_STAMPED))
    if unknown:
        errors.append(f"{where}: unknown key(s) {', '.join(unknown)}")
    ask = {}
    ask_id = data.get("id")
    if not isinstance(ask_id, str) or not ID_PATTERN.fullmatch(ask_id):
        errors.append(f"{where}: id must match {ID_PATTERN.pattern}")
    ask["id"] = ask_id
    question = _text(data, "question", where, errors, MAX_TEXT)
    if question is not None and ("[" in question or "]" in question):
        errors.append(f"{where}: question has a square bracket")
    ask["question"] = question
    if "link" in data:
        link = data["link"]
        if not isinstance(link, str):
            errors.append(f"{where}: link is not a string")
        else:
            problem = link_problem(link)
            if problem:
                errors.append(f"{where}: link {problem}")
            ask["link"] = link
    default = _text(data, "default", where, errors, MAX_TEXT)
    if "default" not in data:
        errors[-1] = f"{where}: default is missing; every ask carries the default that runs unless he objects"
    ask["default"] = default
    ask["why"] = _text(data, "why", where, errors, MAX_TEXT)
    for key in ("default", "why"):
        if ask[key] == NO_BLOCKS:
            errors.append(f"{where}: {key} is only a dash")
    ask["blocks"] = _id_list(data.get("blocks", []), where, "blocks", errors)
    operation = data.get("operation", False)
    if not isinstance(operation, bool):
        errors.append(f"{where}: operation is not true or false")
    ask["operation"] = operation is True
    return ask, errors


def render_asks(asks: list) -> list:
    """The `### Asks` block as lines without line endings (no Updated line: each row is stamped)."""
    lines = ["### Asks", "", "| " + " | ".join(ASK_COLUMNS) + " |", "|" + "---|" * len(ASK_COLUMNS)]
    for ask in asks:
        question = escape(ask["question"])
        if ask.get("link"):
            question = f"[{question}]({ask['link']})"
        cells = [ask["id"], question, escape(ask["default"]), escape(ask["why"]),
                 ", ".join(ask["blocks"]) or NO_BLOCKS, ask["asked"], ask["answer_where"]]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def _stamp_problem(value: str):
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        parsed = None
    if parsed is None or parsed.tzinfo is None or "T" not in value:
        return "is not an ISO 8601 time with an offset"
    return None


def asks_end(lines: list, start: int, stop: int) -> int:
    """End (exclusive) of the `### Asks` block at lines[start]: the heading, blank lines and the
    contiguous pipe-table lines. Nothing else, so hand-written Now content after it is kept."""
    end = start + 1
    i = end
    while i < stop and _blank(lines[i]):
        i += 1
    while i < stop and lines[i].lstrip().startswith("|"):
        i += 1
        end = i
    return end


def parse_asks(lines: list) -> tuple:
    """(asks, errors) for a `### Asks` block (lines without endings), in render_asks' grammar."""
    errors = []
    if not lines or not ASKS_HEADING.fullmatch(lines[0]):
        return [], ["no ### Asks heading"]
    table = [line for line in lines[1:] if not _blank(line)]
    if len(table) < 2:
        return [], ["no table under ### Asks (needs the header row and the separator)"]
    header = split_cells(table[0])
    if header is None or tuple(header) != ASK_COLUMNS:
        return [], ["Asks columns must be: " + " | ".join(ASK_COLUMNS)]
    separator = split_cells(table[1])
    if separator is None or len(separator) != len(ASK_COLUMNS) or \
            not all(SEPARATOR_CELL.fullmatch(c) for c in separator):
        return [], ["the second Asks table line is not the separator row"]
    body = table[2:]
    if len(body) > MAX_ASKS:
        return [], [f"more than {MAX_ASKS} asks"]
    asks, seen = [], set()
    for n, line in enumerate(body, 1):
        where = f"ask {n}"
        cells = split_cells(line)
        if cells is None or len(cells) != len(ASK_COLUMNS):
            errors.append(f"{where}: expected {len(ASK_COLUMNS)} cells")
            continue
        ask_id, question_raw, default_raw, why_raw, blocks_raw, asked, answer_where = cells
        ask = {"id": ask_id}
        if not ID_PATTERN.fullmatch(ask_id):
            errors.append(f"{where}: ask id {ask_id!r} must match {ID_PATTERN.pattern}")
        elif ask_id in seen:
            errors.append(f"{where}: ask id {ask_id} appears twice")
        seen.add(ask_id)
        linked = re.fullmatch(r"\[([^\[\]]*)\]\(([^()]*)\)", question_raw)
        link = None
        if linked:
            question_raw, link = linked.group(1), linked.group(2)
            problem = link_problem(link)
            if problem:
                errors.append(f"{where}: link {problem}")
        elif "[" in question_raw or "]" in question_raw:
            errors.append(f"{where}: question has a square bracket outside a link")
        for key, raw in (("question", question_raw), ("default", default_raw), ("why", why_raw)):
            value = unescape(raw)
            if value is None:
                errors.append(f"{where}: {key} has a stray backslash")
            elif not value.strip() or value == NO_BLOCKS or len(value) > MAX_TEXT:
                errors.append(f"{where}: {key} is empty or longer than {MAX_TEXT} characters")
            ask[key] = value
        if link is not None:
            ask["link"] = link
        ask["blocks"] = [] if blocks_raw == NO_BLOCKS else [b.strip() for b in blocks_raw.split(",")]
        _id_list(ask["blocks"], where, "blocks", errors)
        problem = _stamp_problem(asked)
        if problem:
            errors.append(f"{where}: asked {asked!r} {problem}")
        ask["asked"] = asked
        if answer_where not in (THIS_WINDOW, RELAY_OK):
            errors.append(f"{where}: answer where must be {THIS_WINDOW!r} or {RELAY_OK!r}")
        ask["answer_where"] = answer_where
        asks.append(ask)
    return asks, errors


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
    """(new text, problem kind, message) for a Queue write: the block is replaced or created as
    Now's first child, an Asks block directly under it moves with it, and every byte outside
    the two blocks is kept."""
    return compose_now(text, render_block(rows, stamp), KEEP)


def _adjacent(lines: list, first, second) -> bool:
    return second[0] >= first[1] and all(_blank(line) for line in lines[first[1]:second[0]])


def compose_now(text: str, queue, asks) -> tuple:
    """(new text, problem kind, message). `queue` is the rendered Queue block's lines, or None to
    keep the existing one; `asks` is the open asks to render ([] removes the block), or KEEP.

    The Queue block is Now's first child and the Asks block sits directly under it (first,
    when there is no Queue yet). When both already stand there, the two are replaced in place;
    otherwise exactly their lines are lifted out and they are placed first."""
    lines = text.splitlines(keepends=True)
    now, end, queues, asks_at = scan_now(lines)
    if now is None:
        return None, EXIT_NO_NOW, "TODO.md has no ## Now section"
    if len(queues) > 1:
        return None, EXIT_INVALID, "## Now holds more than one ### Queue block; keep one and retry"
    if len(asks_at) > 1:
        return None, EXIT_INVALID, "## Now holds more than one ### Asks block; keep one and retry"
    newline = "\r\n" if lines[now].endswith("\r\n") else "\n"

    def raw(span):
        chunk = "".join(lines[span[0]:span[1]])
        return chunk if chunk.endswith("\n") else chunk + newline

    q = (queues[0], block_end(lines, queues[0], end)) if queues else None
    a = (asks_at[0], asks_end(lines, asks_at[0], end)) if asks_at else None
    q_text = newline.join(queue) + newline if queue is not None else (raw(q) if q else None)
    if asks is KEEP:
        a_text = raw(a) if a else None
    else:
        a_text = newline.join(render_asks(asks)) + newline if asks else None
    adjacent = bool(q and a and _adjacent(lines, q, a))
    gap = ("".join(lines[q[1]:a[0]]) if adjacent else "") or newline
    unit = (q_text or "") + (gap if q_text and a_text else "") + (a_text or "")
    spans = sorted(span for span in (q, a) if span)

    if spans and _first_child(lines, now, spans[0][0]) and (len(spans) == 1 or adjacent):
        start, stop = spans[0][0], spans[-1][1]
        tail = lines[stop:]
        if not unit and start > now + 1:  # the Asks block alone left: no doubled gap behind it
            while tail and _blank(tail[0]):
                tail = tail[1:]
        elif a_text and tail and not _blank(tail[0]):
            unit += newline  # a table never runs into the next line
        return "".join(lines[:start]) + unit + "".join(tail), None, None
    for span in reversed(spans):  # lift out exactly the blocks' lines, then place them first
        lines = lines[:span[0]] + lines[span[1]:]
    if not unit:
        return "".join(lines), None, None
    head = lines[now]
    if not head.endswith("\n"):
        head += newline
    after = lines[now + 1:]
    inserted = newline + unit
    if after and not _blank(after[0]):
        inserted += newline
    return "".join(lines[:now]) + head + inserted + "".join(after), None, None


def _current_hash(path: str) -> str | None:
    try:
        with open(path, "rb") as current:
            return _hash(current.read())
    except OSError:
        return None


def _commit(path: str, updated: str, original_hash, project: str, scopes, config_path,
            before_commit=None, relay=None):
    """None when TODO.md was replaced, else (exit code, payload). `before_commit` is a test seam
    called after the temp file is written, before the final config re-check and hash compare.

    Compare-and-swap at the last moment: the config re-check and the hash compare are the very
    last steps before os.replace, with nothing in between but comparing values already read. A
    write by another program in the microseconds between the final check and the replace can
    still be lost; no lock is taken, because the other writers (editors, an agent's edit tool)
    take none. With `relay` given (an ask), a relay rule changed since the read is refused too."""
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
        # The last moment: config re-check, hash compare, replace. Nothing goes between them.
        sig = signal(project, scopes, config_path)
        if sig is None or not sig["on"]:
            return EXIT_OFF, off_payload(sig)
        if relay is not None and sig.get("relay") != relay:
            return EXIT_CHANGED, {"error": "chief_of_staff_relay changed underneath; retry"}
        if _current_hash(path) != original_hash:
            return EXIT_CHANGED, {"error": "TODO.md changed underneath; re-read and retry"}
        os.replace(temp, path)
        temp = None
    finally:
        if temp is not None:
            try:
                os.unlink(temp)
            except OSError:
                pass
    return None


def write_queue(project: str, scopes, rows_json: str, config_path: str | None = None,
                now: datetime | None = None, before_commit=None) -> tuple:
    """(exit code, payload). The rows replace the whole `### Queue` table; see `_commit` for the
    compare-and-swap at the last moment, not a lock."""
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
    original_hash = _hash(original)
    stamp = clock_stamp(now)
    updated, kind, message = compose(text, rows, stamp)
    if kind is not None:
        return kind, ({"errors": [message]} if kind == EXIT_INVALID else {"error": message})
    failed = _commit(path, updated, original_hash, project, scopes, config_path, before_commit)
    if failed:
        return failed
    return EXIT_OK, {"written": path, "rows": rows, "updated": stamp}


def _open_asks(text: str) -> tuple:
    """(asks, problem kind, message) read from the existing `### Asks` block; none is []."""
    lines = text.splitlines(keepends=True)
    now, end, _, asks_at = scan_now(lines)
    if now is None:
        return None, EXIT_NO_NOW, "TODO.md has no ## Now section"
    if len(asks_at) > 1:
        return None, EXIT_INVALID, "## Now holds more than one ### Asks block; keep one and retry"
    if not asks_at:
        return [], None, None
    stop = asks_end(lines, asks_at[0], end)
    asks, errors = parse_asks([_bare(line) for line in lines[asks_at[0]:stop]])
    if errors:
        return None, EXIT_INVALID, "the ### Asks table is damaged: " + "; ".join(errors)
    return asks, None, None


def ask_decision(project: str, scopes, ask_json: str | None = None, answered: str | None = None,
                 again: bool = False, config_path: str | None = None, now: datetime | None = None,
                 before_commit=None) -> tuple:
    """(exit code, payload). Adds one open decision to `### Asks` (or, with `again`, replaces the
    open one with its id and a fresh time), or with `answered` removes that one. The same
    gating and compare-and-swap at the last moment as `write`. An id already open is refused:
    a decision is asked once, and asked again only when a fact behind it changes (`again`)."""
    sig = signal(project, scopes, config_path)
    if sig is None or not sig["on"]:
        return EXIT_OFF, off_payload(sig)
    relay = sig.get("relay", "none")
    new = None
    if answered is not None:
        if again:
            return EXIT_INVALID, {"errors": ["--answered and --again do not go together"]}
        if not isinstance(answered, str) or not ID_PATTERN.fullmatch(answered):
            return EXIT_INVALID, {"errors": [f"--answered must match {ID_PATTERN.pattern}"]}
    else:
        try:
            data = json.loads(ask_json if ask_json is not None else "")
        except ValueError as error:
            return EXIT_INVALID, {"errors": [f"stdin is not valid JSON: {error}"]}
        new, errors = validate_ask(data)
        if errors:
            return EXIT_INVALID, {"errors": errors}
    path = todo_path(project, scopes)
    original, text, problem = _read_todo(path)
    if problem:
        return EXIT_NO_NOW, {"error": problem}
    asks, kind, message = _open_asks(text)
    if kind is not None:
        return kind, ({"errors": [message]} if kind == EXIT_INVALID else {"error": message})
    ids = [ask["id"] for ask in asks]
    if answered is not None:
        if answered not in ids:
            return EXIT_INVALID, {"errors": [f"no open ask {answered}"]}
        asks = [ask for ask in asks if ask["id"] != answered]
    else:
        operation = new.pop("operation")
        new["asked"] = clock_stamp(now)
        new["answer_where"] = RELAY_OK if relay == "decisions" and not operation else THIS_WINDOW
        if new["id"] in ids and not again:
            asked = asks[ids.index(new["id"])]["asked"]
            return EXIT_INVALID, {"errors": [
                f"ask {new['id']} is already open, asked {asked}: it is not asked again. "
                "When a fact behind it changes, send it with --again"]}
        if again and new["id"] not in ids:
            return EXIT_INVALID, {"errors": [f"no open ask {new['id']} to ask again"]}
        if again:
            asks[ids.index(new["id"])] = new
        else:
            asks.append(new)
    if len(asks) > MAX_ASKS:
        return EXIT_INVALID, {"errors": [f"more than {MAX_ASKS} open asks"]}
    if relay != "decisions":  # fail closed: a relay rule taken back reaches every open row
        for ask in asks:
            ask["answer_where"] = THIS_WINDOW
    updated, kind, message = compose_now(text, None, asks)
    if kind is not None:
        return kind, ({"errors": [message]} if kind == EXIT_INVALID else {"error": message})
    failed = _commit(path, updated, _hash(original), project, scopes, config_path, before_commit,
                     relay=relay)
    if failed:
        return failed
    return EXIT_OK, {"written": path, "asks": asks, "relay": relay}


def check_queue(project: str, scopes, config_path: str | None = None) -> tuple:
    """(exit code, payload) for the `### Queue` table and, when present, the `### Asks` table
    directly under it. Read-only: never writes."""
    sig = signal(project, scopes, config_path)
    if sig is None or not sig["on"]:
        return EXIT_OFF, off_payload(sig)
    path = todo_path(project, scopes)
    _, text, problem = _read_todo(path)
    if problem:
        return EXIT_INVALID, {"valid": False, "errors": [problem]}
    lines = text.splitlines(keepends=True)
    now, end, queues, asks_at = scan_now(lines)
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
    relay, asks = sig.get("relay", "none"), []
    if len(asks_at) > 1:
        errors.append("## Now holds more than one ### Asks block")
    elif asks_at:
        span = (asks_at[0], asks_end(lines, asks_at[0], end))
        if not _adjacent(lines, (queues[0], stop), span):
            errors.append("### Asks does not directly follow the ### Queue block")
        asks, ask_errors = parse_asks([_bare(line) for line in lines[span[0]:span[1]]])
        errors += ask_errors
        if relay != "decisions":
            errors += [f"ask {n}: answer where says {RELAY_OK!r}, but this project's "
                       f'{RELAY_KEY} is "none"' for n, ask in enumerate(asks, 1)
                       if ask.get("answer_where") == RELAY_OK]
    if errors:
        return EXIT_INVALID, {"valid": False, "errors": errors}
    return EXIT_OK, {"valid": True, "rows": rows, "updated": stamp, "asks": asks, "relay": relay}


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
    ask = sub.add_parser("ask", parents=[common],
                         help="Add one open decision to ### Asks from JSON on stdin")
    ask.add_argument("--again", action="store_true",
                     help="Ask the open decision with this id again: a fact behind it changed")
    ask.add_argument("--answered", metavar="ID", help="The ask with this id leaves the table; no stdin")
    sub.add_parser("check", parents=[common], help="Validate the ### Queue and ### Asks blocks; never writes")
    args = parser.parse_args(argv)

    if args.action == "status":
        sig = signal(args.project, args.scope, args.config)
        code, payload = (EXIT_OK if sig and sig["on"] else EXIT_OFF), off_payload(sig)
    elif args.action == "write":
        code, payload = write_queue(args.project, args.scope, sys.stdin.read(), args.config)
    elif args.action == "ask":
        stdin = None if args.answered is not None else sys.stdin.read()
        code, payload = ask_decision(args.project, args.scope, stdin, args.answered, args.again,
                                     args.config)
    else:
        code, payload = check_queue(args.project, args.scope, args.config)
    print(json.dumps(payload, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
