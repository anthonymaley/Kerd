#!/usr/bin/env python3
"""What waits for the person, for the status line.

    needs.py set   --project P "short label"   write this session's pending question
    needs.py clear --project P                 remove it
    needs.py show  --project P [--line]        print the combined labels

Combined = this session's label file (`<git dir>/kerd/needs-you/<session id>`, one line each) plus the open
rows of TODO.md's `### Asks` table under `## Now`. Quiet by design: it never raises,
and a missing file or folder means nothing waits. No network, no git fetch.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time

LABEL_MAX = 60
SHORT_WORDS = 6
SHORT_CHARS = 40


SESSION_ENV = ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID")
PRUNE_SECONDS = 30 * 24 * 3600
_ESC = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]?")
_CTRL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]")


def find_git(project):
    """(toplevel, git dir) found by walking up for `.git`; no git process. (None, None) if none."""
    try:
        here = os.path.abspath(project)
        while True:
            dot = os.path.join(here, ".git")
            if os.path.isdir(dot):
                return here, dot
            if os.path.isfile(dot):
                with open(dot, encoding="utf-8") as f:
                    first = f.readline().strip()
                if first.startswith("gitdir:"):
                    target = first[7:].strip()
                    return here, target if os.path.isabs(target) else os.path.normpath(os.path.join(here, target))
            parent = os.path.dirname(here)
            if parent == here:
                return None, None
            here = parent
    except Exception:
        return None, None


def raw_session_id():
    for key in SESSION_ENV:
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return ""


def session_file(raw):
    """Collision-proof file name for a session id: sanitized, plus a short sha256 of the raw id
    when sanitizing changed it."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "", raw)[:100]
    if safe != raw or not safe:
        safe = (safe + "-" if safe else "") + hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()[:8]
    return safe


def needs_base(project):
    _, gitdir = find_git(project)
    return os.path.join(gitdir, "kerd", "needs-you") if gitdir else None


def clean(text, limit=LABEL_MAX):
    text = _ESC.sub("", str(text))
    text = re.sub(r"[\t\n\r\x0b\x0c]", " ", text)
    text = _CTRL.sub("", text)
    text = " ".join(text.split())
    return text[:limit].rstrip()


def shorten(text):
    """A few words, cut at SHORT_WORDS words or SHORT_CHARS characters."""
    words = clean(text, 400).split(" ")
    out = " ".join(words[:SHORT_WORDS])
    if len(out) > SHORT_CHARS:
        out = out[:SHORT_CHARS].rstrip()
    return out


def split_row(line):
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells, cur, esc = [], "", False
    for ch in line[1:]:
        if esc:
            cur += ch if ch == "|" else "\\" + ch
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        cells.append(cur.strip())
    return cells


def asks_questions(todo_text):
    """Question cells of the `### Asks` table under `## Now`: only the contiguous pipe-table
    rows directly under the heading. Tolerant, never raises."""
    questions, in_now, fence, table = [], False, False, None
    for raw in todo_text.splitlines():
        line = raw.strip()
        if line.startswith("```") or line.startswith("~~~"):
            fence = not fence
            if table is not None:
                break
            continue
        if fence:
            continue
        if table is not None:
            if not line.startswith("|"):
                if not line and not table:
                    continue          # blank lines between heading and table
                break
            table.append(line)
            continue
        if re.match(r"##\s+now\b", line, re.I):
            in_now = True
            continue
        if in_now and re.match(r"#{1,2}(?:\s|$)", line):
            break
        if in_now and re.fullmatch(r"###\s+asks\s*", line, re.I):
            table = []
    for n, line in enumerate(table or []):
        cells = split_row(line)
        if n < 2 or not cells or len(cells) < 2:
            continue                  # header row, separator row, junk
        q = re.sub(r"^\[([^\]]*)\]\([^)]*\)$", r"\1", cells[1])
        q = shorten(q)
        if q:
            questions.append(q)
    return questions


def read_labels(project, session=""):
    """This session's label only: <git dir>/kerd/needs-you/<file for the id>. No id, no label.
    (An old single `needs-you` file cannot be attributed to a session, so it is ignored.)"""
    base = needs_base(project)
    if not base or not session:
        return []
    try:
        with open(os.path.join(base, session_file(session)), encoding="utf-8", errors="replace") as f:
            label = clean(f.readline())
    except Exception:
        return []
    return [label] if label else []


def prune(base, keep):
    """Remove other sessions' files not touched for 30 days."""
    now = time.time()
    try:
        for name in os.listdir(base):
            path = os.path.join(base, name)
            if name != keep and os.path.isfile(path) and now - os.path.getmtime(path) > PRUNE_SECONDS:
                os.remove(path)
    except Exception:
        pass


def todo_text(project):
    top, _ = find_git(project)
    here, seen = os.path.abspath(project), []
    while True:                       # the folder itself, then up to the repo top
        seen.append(here)
        parent = os.path.dirname(here)
        if here == top or parent == here or top is None:
            break
        here = parent
    for base in seen:
        try:
            with open(os.path.join(base, "TODO.md"), encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception:
            continue
    return ""


def combined(project, session=""):
    labels = list(read_labels(project, session))
    try:
        labels.extend(q for q in asks_questions(todo_text(project)) if q not in labels)
    except Exception:
        pass
    return labels


def line(labels):
    if not labels:
        return ""
    text = "💬 Needs you: " + " · ".join(labels[:2])
    if len(labels) > 2:
        text += f" +{len(labels) - 2}"
    return text


def main(argv=None):
    p = argparse.ArgumentParser(prog="needs.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("set")
    s.add_argument("--project", required=True)
    s.add_argument("label")
    c = sub.add_parser("clear")
    c.add_argument("--project", required=True)
    h = sub.add_parser("show")
    h.add_argument("--project", required=True)
    h.add_argument("--line", action="store_true")
    h.add_argument("--session", default="")
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if args.cmd in ("set", "clear"):
            raw = raw_session_id()
            if not raw:
                print("needs.py: no session id (CLAUDE_CODE_SESSION_ID or CODEX_THREAD_ID is not set); "
                      "refusing to write a label shared by every session", file=sys.stderr)
                return 2
            base = needs_base(args.project)
            if not base:
                return 1 if args.cmd == "set" else 0
            keep = session_file(raw)
            mine = os.path.join(base, keep)
            if args.cmd == "set":
                label = clean(args.label)
                if not label:
                    return 1
                if os.path.isfile(base):          # old single shared file: ignored, replaced
                    os.remove(base)
                os.makedirs(base, exist_ok=True)
                with open(mine, "w", encoding="utf-8") as f:
                    f.write(label + "\n")
                prune(base, keep)
            elif os.path.isfile(mine):
                os.remove(mine)
        else:
            labels = combined(args.project, args.session)
            if args.line:
                out = line(labels)
                if out:
                    print(out)
            else:
                for label in labels:
                    print(label)
    except Exception:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
