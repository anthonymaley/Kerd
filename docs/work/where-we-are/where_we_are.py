#!/usr/bin/env python3
"""Render one work record as a glanceable "Where we are" view.

The view reports what a record states explicitly and nothing else. Missing or
ambiguous information is labelled rather than interpreted, an assigned model
never implies a running job, and no process is observed: "rendered at" is this
clock, "record updated" is only what the record's own status section says.

A record states a job on one line, and the separators need spaces around them
so ordinary punctuation in a title is left alone:

    - [done] Title · actor — detail → evidence

Only the bracketed state carries meaning. Anything else is kept and labelled.
"""

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys
import unicodedata

STAGES = ("Understand", "Shape", "Agree", "Deliver", "Complete")
MARKS = {"done": "✓ done", "active": "● active", "next": "○ next", "blocked": "⨯ blocked"}
ORDER = ("done", "active", "next", "blocked")
UNRECORDED = "not recorded"
NOTHING = {"none", "none.", "n/a", "nothing", "-"}
HEADING = re.compile(r"##[ \t]+(\S.*?)[ \t]*")
FIELD_LINE = re.compile(r"([A-Za-z][A-Za-z ]{0,40}):[ \t]*(.*)")


def columns(text):
    """Terminal columns, not codepoints: a wide glyph occupies two, a mark none."""
    total = 0
    for char in text:
        if unicodedata.category(char) in ("Mn", "Me", "Cf"):
            continue
        total += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
    return total


def pad(text, width):
    return text + " " * max(0, width - columns(text))


def split_word(word, width):
    """Hard-split a word too long to fit, so a border can never be pushed out."""
    pieces, current = [], ""
    for char in word:
        if columns(current + char) > width and current:
            pieces.append(current)
            current = char
        else:
            current += char
    return pieces + ([current] if current else [])


def wrap(text, width):
    lines, line = [], ""
    for word in text.split():
        for piece in ([word] if columns(word) <= width else split_word(word, width)):
            candidate = f"{line} {piece}".strip()
            if columns(candidate) > width and line:
                lines.append(line)
                line = piece
            else:
                line = candidate
    return lines + [line] if line else lines or [""]


def sections(text):
    """Level-2 sections, with fenced code removed so quoted Markdown cannot pose as
    record state — neither as a heading nor as a field or job line.

    A heading used twice makes its content ambiguous. Rather than silently keeping
    one of them, the name is returned as duplicated and nothing is read from it.
    """
    found, duplicated, current, body, fence = {}, set(), None, [], None
    for line in text.splitlines():
        stripped = line.rstrip("\r\n")
        if fence:
            # Fenced content is dropped entirely, not just skipped for headings:
            # a quoted example must not supply fields or jobs either.
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*", stripped):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", stripped)
        if opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = opening[1]
            continue
        heading = HEADING.fullmatch(stripped)
        if heading:
            if current is not None:
                found[current] = "\n".join(body)
            if heading[1] in found:
                duplicated.add(heading[1])
            current, body = heading[1], []
        elif current is not None:
            body.append(stripped)
    if current is not None:
        found[current] = "\n".join(body)
    for name in duplicated:
        found.pop(name, None)
    return found, duplicated


def field(section, name):
    """One explicit `Name:` field, as (value, note).

    A value runs to the end of its line and on through following lines until a
    blank line or the next field, so a question written across three lines is not
    silently shown as its first line. Absent, empty or an explicit "none" is no
    value. Stated twice is ambiguous and is not read: choosing between them would
    be interpretation, which this view does not do. Whether a field sits under
    narrative prose is deliberately not judged — that reading is exactly what the
    record's own convention replaces.
    """
    if section is None:
        return None, None
    lines, values, index = section.splitlines(), [], 0
    while index < len(lines):
        match = FIELD_LINE.fullmatch(lines[index])
        index += 1
        if not match or match[1] != name:
            continue
        parts = [match[2].strip()]
        while index < len(lines) and lines[index].strip() and not FIELD_LINE.fullmatch(lines[index]):
            parts.append(lines[index].strip())
            index += 1
        values.append(" ".join(part for part in parts if part).strip())
    if len(values) > 1:
        return None, f"{name.lower()} is recorded {len(values)} times; not read"
    if not values or not values[0] or values[0].lower() in NOTHING:
        return None, None
    return values[0], None


def outcome_of(text):
    match = re.search(r"^#[ \t]+Work:[ \t]*(\S.*?)[ \t]*$", text, re.MULTILINE)
    return match[1] if match else None


def parse_job(line):
    """One job line. Separators must be spaced, so "A·B" in a title stays in the title."""
    match = re.fullmatch(r"-[ \t]+\[([a-z]+)\][ \t]*(\S.*?)[ \t]*", line.strip())
    if not match:
        return {"state": None, "title": line.strip().lstrip("- ").strip() or UNRECORDED,
                "actor": None, "detail": None, "evidence": None}
    rest, evidence, detail, actor = match[2], None, None, None
    if " → " in rest:
        rest, _, evidence = rest.rpartition(" → ")
    if " — " in rest:
        rest, _, detail = rest.partition(" — ")
    if " · " in rest:
        rest, _, actor = rest.partition(" · ")
    return {"state": match[1], "title": rest.strip() or UNRECORDED,
            "actor": (actor or "").strip() or None, "detail": (detail or "").strip() or None,
            "evidence": (evidence or "").strip() or None}


def jobs_of(section):
    if section is None:
        return None
    found = [parse_job(line) for line in section.splitlines() if line.strip().startswith("-")]
    return found or None


def box(title, rows, width):
    """A fully bounded box: content wrapped to columns, then every row padded equally."""
    inner = width - 4
    out = ["┌" + "─" * (width - 2) + "┐", "│ " + pad(title, inner) + " │",
           "├" + "─" * (width - 2) + "┤"]
    for row in rows:
        for line in ([""] if row == "" else wrap(row, inner)):
            out.append("│ " + pad(line, inner) + " │")
    return out + ["└" + "─" * (width - 2) + "┘"]


def journey_strip(stage):
    plain = " → ".join(STAGES)
    if stage is None:
        return plain, f"stage {UNRECORDED}"
    known = next((name for name in STAGES if name.lower() == stage.lower()), None)
    if known is None:
        return plain, f'recorded stage "{stage}" is not one of these'
    return " → ".join(f"[NOW: {name}]" if name == known else name for name in STAGES), None


def job_block(job, state, width):
    indent = " " * 13
    label = MARKS[state] if state in MARKS else "? unlab"
    lines = [f"  {label:<10} {line}" if index == 0 else indent + line
             for index, line in enumerate(wrap(job["title"], width - 13))]
    if job["actor"]:
        actor = job["actor"] + (" (assigned, not started)" if state == "next" else "")
        lines += [indent + line for line in wrap("by: " + actor, width - 13)]
    if job["detail"]:
        lines += [indent + line for line in wrap(job["detail"], width - 13)]
    if state == "blocked" and not job["detail"]:
        lines.append(indent + f"blocker {UNRECORDED}")
    if job["evidence"]:
        lines += [indent + line for line in wrap("→ " + job["evidence"], width - 13)]
    if state not in MARKS:
        shown = f'"{job["state"]}"' if job["state"] else "no status"
        lines += [indent + line for line in
                  wrap(f"{shown} is not a recorded state; read the record itself", width - 13)]
    return lines


def render(path, text, now, width=80):
    parts, duplicated = sections(text)
    now_part, agreement = parts.get("Now"), parts.get("Agreement")
    stage, stage_dup = field(now_part, "Stage")
    updated, updated_dup = field(now_part, "Record updated")
    question, question_dup = field(now_part, "Pending question")
    proposed, _ = field(now_part, "Proposed answer")
    reply, _ = field(now_part, "Reply with")

    lines = ["KERD · Where we are", *wrap(outcome_of(text) or f"outcome {UNRECORDED}", width),
             *wrap(f"record: {path}", width)]
    stamps = f"rendered at: {now}    record updated: {updated or 'unknown'}"
    lines += ([stamps] if columns(stamps) <= width
              else [f"rendered at: {now}", f"record updated: {updated or 'unknown'}"])
    for name in sorted(duplicated):
        lines += wrap(f'! the record has more than one "## {name}" section, so nothing '
                      f"is read from it; open the record itself", width)
    for note in (stage_dup, updated_dup, question_dup):
        if note:
            lines += wrap("! " + note, width)

    strip, stage_note = journey_strip(stage)
    lines += ["", *wrap(strip, width)]
    lines += (wrap(stage_note, width) if stage_note else []) + [""]

    if question:
        lines += box("YOU DECIDE", [question, "", "Proposed: " + (proposed or UNRECORDED),
                                    "", "Reply: " + (reply or "Correct / Change")], width) + [""]
    elif agreement and agreement.strip():
        lines += wrap("YOU: no decision is recorded as pending. The standing agreement "
                      "is in the record's Agreement section.", width) + [""]
    else:
        lines += wrap(f"YOU: it is {UNRECORDED} whether you are needed. This record states "
                      "no agreement and no pending question.", width) + [""]

    lines.append("JOBS (as recorded — not observed)")
    jobs = jobs_of(parts.get("Jobs"))
    if jobs is None:
        lines.append("  no jobs recorded in this record"
                     if "Jobs" not in duplicated else "  jobs not read; see the note above")
    else:
        for state in ORDER:
            for job in [item for item in jobs if item["state"] == state]:
                lines += job_block(job, state, width)
        for job in [item for item in jobs if item["state"] not in MARKS]:
            lines += job_block(job, job["state"], width)
    lines += ["", *wrap('Recorded, not observed. "active" means the record said so when it '
                        "was last updated, not that a job is running now.", width)]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True, help="Path to one work record")
    parser.add_argument("--width", type=int, default=80)
    args = parser.parse_args()
    path = Path(args.record)
    if not path.is_file():
        print(f"No work record at {path}", file=sys.stderr)
        return 2
    print(render(path, path.read_text(encoding="utf-8"),
                 datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"), args.width))
    return 0


if __name__ == "__main__":
    sys.exit(main())
