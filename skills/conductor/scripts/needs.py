#!/usr/bin/env python3
"""What waits for the person, for the status line.

    needs.py set   --project P "short label"   write this session's pending question
    needs.py clear --project P                 remove it
    needs.py show  --project P [--line]        print the combined labels

Combined = the session's label file (`<git dir>/kerd/needs-you`, one line) plus the open
rows of TODO.md's `### Asks` table under `## Now`. Quiet by design: it never raises,
and a missing file or folder means nothing waits. No network, no git fetch.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

LABEL_MAX = 60
SHORT_WORDS = 6
SHORT_CHARS = 40


def _git(project, *args):
    try:
        out = subprocess.run(["git", "-C", project, *args], capture_output=True, text=True, timeout=3)
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def label_path(project):
    rel = _git(project, "rev-parse", "--git-path", "kerd/needs-you")
    if not rel:
        return None
    return rel if os.path.isabs(rel) else os.path.join(project, rel)


def clean(text, limit=LABEL_MAX):
    text = " ".join(str(text).split())
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
    """Question cells of the `### Asks` table under `## Now`; tolerant, never raises."""
    questions, in_now, in_asks, header_seen, fence = [], False, False, False, False
    for raw in todo_text.splitlines():
        line = raw.strip()
        if line.startswith("```") or line.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if re.match(r"##\s+Now\b", line):
            in_now, in_asks, header_seen = True, False, False
            continue
        if in_now and re.match(r"##\s+\S", line) and not line.startswith("###"):
            break
        if not in_now:
            continue
        if re.fullmatch(r"###\s+Asks\s*", line):
            in_asks, header_seen = True, False
            continue
        if line.startswith("###"):
            in_asks = False
            continue
        if not in_asks or not line.startswith("|"):
            continue
        cells = split_row(line)
        if not cells or len(cells) < 2:
            continue
        if re.fullmatch(r":?-{2,}:?", cells[0].strip()) or all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        if not header_seen:
            header_seen = True
            continue
        q = re.sub(r"^\[([^\]]*)\]\([^)]*\)$", r"\1", cells[1])
        q = shorten(q)
        if q:
            questions.append(q)
    return questions


def read_label(project):
    path = label_path(project)
    if not path:
        return ""
    try:
        with open(path, encoding="utf-8") as f:
            return clean(f.readline())
    except Exception:
        return ""


def todo_text(project):
    for base in (project, _git(project, "rev-parse", "--show-toplevel")):
        if base:
            try:
                with open(os.path.join(base, "TODO.md"), encoding="utf-8") as f:
                    return f.read()
            except Exception:
                continue
    return ""


def combined(project):
    labels = []
    own = read_label(project)
    if own:
        labels.append(own)
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
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if args.cmd == "set":
            path, label = label_path(args.project), clean(args.label)
            if not path or not label:
                return 1
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(label + "\n")
        elif args.cmd == "clear":
            path = label_path(args.project)
            if path and os.path.exists(path):
                os.remove(path)
        else:
            labels = combined(args.project)
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
