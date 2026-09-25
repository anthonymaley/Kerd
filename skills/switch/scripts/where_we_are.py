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
import json
from datetime import datetime
import os
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
SUBHEADING = re.compile(r"###[ \t]+(\S.*?)[ \t]*")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


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
    # Records write "Stage: Complete." as readily as "Stage: Complete".
    spoken = stage.strip().rstrip(".;,")
    known = next((name for name in STAGES if name.lower() == spoken.lower()), None)
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


def position_of(section):
    """The record's own first subheading inside its status section.

    A heading the record wrote is explicit structure, not prose read for meaning,
    so it can orient a reader when no Stage field exists.
    """
    if section is None:
        return None
    for line in section.splitlines():
        match = SUBHEADING.fullmatch(line.strip())
        if match:
            return match[1]
    return None


def links_of(section, limit=5):
    """Markdown links the status section already carries, as evidence pointers."""
    if section is None:
        return [], 0
    seen = {}
    for label, target in LINK.findall(section):
        seen.setdefault(target, label)
    found = [(label, target) for target, label in seen.items()]
    return found[:limit], len(found)


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
    lines += wrap(stage_note, width) if stage_note else []
    position = position_of(now_part)
    if position and stage_note:
        lines += wrap(f"position, from this record's own Now heading: {position}", width)
    lines.append("")

    if question:
        lines += box("YOU DECIDE", [question, "", "Proposed: " + (proposed or UNRECORDED),
                                    "", "Reply: " + (reply or "Correct / Change")], width) + [""]
    elif agreement and agreement.strip():
        lines += wrap("YOU: no decision is recorded as pending. The standing agreement "
                      "is in the record's Agreement section.", width) + [""]
    else:
        lines += wrap(f"YOU: it is {UNRECORDED} whether you are needed. This record states "
                      "no agreement and no pending question.", width) + [""]

    activity, activity_dup = field(now_part, "Current activity")
    action, action_dup = field(now_part, "Next action")
    for note in (activity_dup, action_dup):
        if note:
            lines += wrap("! " + note, width)
    for label, value in (("doing", activity), ("next ", action)):
        lines += [f"  {label}  {line}" if index == 0 else " " * 9 + line
                  for index, line in enumerate(wrap(value or UNRECORDED, width - 9))]
    lines.append("")

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
    found, total = links_of(parts.get("Now"))
    if found:
        shown = f" (first {len(found)} of {total})" if total > len(found) else ""
        lines += ["", f"LINKS THE RECORD ALREADY CARRIES{shown}"]
        for label, target in found:
            lines += [f"  → {line}" if index == 0 else "    " + line
                      for index, line in enumerate(wrap(f"{target}  ({label})", width - 4))]
    lines += ["", *wrap('Recorded, not observed. "active" means the record said so when it '
                        "was last updated, not that a job is running now.", width)]
    return "\n".join(lines)


def compact(path, text, now, width=80):
    """A few lines for a moment of change: what is happening, who has it, and
    whether the person is needed. Not the full view — that is for asking, this is
    for telling, and repeating everything on every change is the noise it avoids.
    """
    parts, _ = sections(text)
    now_part = parts.get("Now")
    question, _ = field(now_part, "Pending question")
    jobs = jobs_of(parts.get("Jobs")) or []
    lines = []
    for job in [item for item in jobs if item["state"] == "active"]:
        actor = f" · {job['actor']}" if job["actor"] else ""
        lines += wrap(f"● {job['title']}{actor}", width)
    for job in [item for item in jobs if item["state"] == "blocked"]:
        lines += wrap(f"⨯ blocked: {job['title']}"
                      + (f" — {job['detail']}" if job["detail"] else ""), width)
    if not lines:
        lines = wrap(f"● no job recorded as active in {path}", width)
    if question:
        lines += wrap(f"You: a decision is waiting — {question}", width)
    else:
        lines.append("You: nothing needed.")
    lines.append(f"({now}, as recorded — not observed)")
    return "\n".join(lines)


# The renderer's input contract, written down so a caller fills the shape from
# the guide's example instead of reading this module to discover key names.
SUMMARY_KEYS = ("project", "where", "open_work", "recommendation",
                "phase", "task", "task_reason", "state", "state_reason", "team", "now",
                "last_session", "this_session", "question", "documents",
                "warnings", "insight", "source", "updated", "base",
                "restored", "restore_note")
# The keys the plain-English arrival reads (open_work or recommendation present).
# The remaining SUMMARY_KEYS serve the record-driven view and older callers.
OPEN_WORK_KEYS = ("project", "phase", "where", "open_work", "recommendation", "last_session",
                  "team", "question", "documents", "warnings", "insight", "base", "restored",
                  "restore_note")
# The closing box's input contract, the same way: Switch Out fills it from the
# helper's save result and what it just wrote, never from this module.
CLOSING_KEYS = ("project", "branch", "saved", "handoff_ready", "boundary", "phase", "released",
                "this_session", "next", "why", "tree", "warnings", "host")
ANSI = {"cyan": "36", "green": "32", "amber": "33", "red": "31", "dim": "2", "bold": "1"}
BORDERS = "\u256d\u2570\u251c\u250c\u2514"


def ink(text, *tones, on=True):
    """Colour is applied to already-padded text, never before, so an escape
    sequence can never be counted as a column."""
    if not on or not tones:
        return text
    return "\x1b[" + ";".join(ANSI[tone] for tone in tones) + "m" + text + "\x1b[0m"


def md(text):
    """Treat summary values as text, not Markdown instructions or headings."""
    value = re.sub(r"([\\`*_\[\]<>|~])", r"\\\1", " ".join(str(text).split()))
    value = re.sub(r"^(#{1,6}|[-+]+)(?=\s|$)", r"\\\1", value)
    return re.sub(r"^(\d+)([.)])(?=\s|$)", r"\1\\\2", value)


def code(text):
    value = " ".join(str(text).split())
    fence = "`" * (max((len(run) for run in re.findall(r"`+", value)), default=0) + 1)
    return f"{fence} {value} {fence}"


def markdown_panel(title, rows):
    # Rules bound YOU separately from the optional, theme-coloured Insight.
    lines = [f"### {title}", ""]
    for row in rows:
        if row:
            lines += [md(row), ""]
    return ["---", ""] + lines + ["---"] if title == "YOU" else lines


def chat_box(title, rows, width, prewrapped=False):
    lines = ["┌─ " + title + " " + "─" * max(0, width - columns(title) - 5) + "┐"]
    for row in rows:
        for line in ([row] if prewrapped else wrap(row, width - 4)):
            lines.append("│ " + pad(line, width - 4) + " │")
    lines.append("└" + "─" * (width - 2) + "┘")
    # A value containing backticks must not close the surrounding code block.
    fence = "`" * max(3, 1 + max((len(run) for line in lines
                                 for run in re.findall(r"`+", line)), default=0))
    return [fence + "text", *lines, fence]


def panel(title, rows, width, tone=None, on=True, prewrapped=False):
    """A titled box whose border carries the tone and whose content does not."""
    inner = width - 4
    dashes = max(0, width - 5 - columns(title))
    lines = ["\u256d\u2500 " + title + " " + "\u2500" * dashes + "\u256e"]
    for row in rows:
        for line in ([row] if prewrapped else [""] if row == "" else wrap(row, inner)):
            lines.append("\u2502 " + pad(line, inner) + " \u2502")
    lines.append("\u2570" + "\u2500" * (width - 2) + "\u256f")
    if not on or tone is None:
        return lines
    painted = []
    for line in lines:
        if line[0] in BORDERS or line[0] == "\u2570":
            painted.append(ink(line, tone, on=True))
        else:
            painted.append(ink(line[0], tone, on=True) + line[1:-1] + ink(line[-1], tone, on=True))
    return painted


def resolve_links(found, record):
    """Split the record's own links into what a reader can open and what they
    cannot. A target that does not resolve is a defect in the record, so it is
    reported rather than quietly dropped."""
    base = Path(record)
    open_able, broken = [], []
    for label, target in found:
        if target.startswith(("http://", "https://", "mailto:")):
            open_able.append((label, target))
        elif (base / target.split("#", 1)[0]).exists():
            open_able.append((label, target))
        else:
            broken.append((label, target))
    return open_able, broken


def nothing_first(value):
    """Split a value the record opened with "none" from the reason it gave.

    Reading the word the record wrote is not interpretation; treating the
    sentence after it as a task would be. Returns (is_nothing, reason).
    """
    if not value:
        return True, None
    match = re.match(r"(none|nothing|n/a|-)\s*[.;:,\u2014-]\s*(\S.*)$", value.strip(), re.I)
    if match:
        return True, match[2].strip()
    return False, value


def stated(section, name):
    """Whether the record wrote the field at all. Absent and "none" are different
    claims: one is silence, the other is an answer."""
    if section is None:
        return False
    return any((match := FIELD_LINE.fullmatch(line)) and match[1] == name
               for line in section.splitlines())


def summary_from_record(path, text):
    """Everything the dashboard shows, read from one record."""
    parts, duplicated = sections(text)
    now_part = parts.get("Now")
    jobs = jobs_of(parts.get("Jobs")) or []
    activity, activity_note = field(now_part, "Current activity")
    action, action_note = field(now_part, "Next action")
    question, question_note = field(now_part, "Pending question")
    phase, phase_note = field(now_part, "Phase")
    stage, stage_note = field(now_part, "Stage")
    updated, updated_note = field(now_part, "Record updated")
    active = [job for job in jobs if job["state"] == "active"]
    blocked = [job for job in jobs if job["state"] == "blocked"]
    done = [job for job in jobs if job["state"] == "done"]

    # No current activity is not the same claim as no selected task: work can be
    # agreed and paused, waiting on a review, or blocked. Only an explicit
    # nothing-value with no job open supports "Not selected yet".
    task_reason = None
    if activity:
        is_nothing, reason = nothing_first(activity)
        if not is_nothing:
            task = activity
        elif active or blocked:
            task = " \u00b7 ".join(job["title"] for job in active + blocked)
        else:
            task, task_reason = "Not selected yet", reason
    elif active:
        task, task_reason = " \u00b7 ".join(job["title"] for job in active), None
    elif blocked:
        task, task_reason = " \u00b7 ".join(job["title"] for job in blocked), None
    elif stated(now_part, "Current activity"):
        task, task_reason = "Not selected yet", None
    else:
        task, task_reason = UNRECORDED, None

    state_reason = None
    if question:
        state = "Decision pending"
    elif blocked and not active:
        first = blocked[0]
        state = "Blocked" + (f" \u2014 {first['detail']}" if first["detail"]
                             else f" \u2014 blocker {UNRECORDED}")
    elif action:
        is_nothing, reason = nothing_first(action)
        state, state_reason = (UNRECORDED, reason) if is_nothing else (action, None)
    else:
        state = UNRECORDED

    warnings = [f'the record has more than one "## {name}" section, so nothing is read from it'
                for name in sorted(duplicated)]
    warnings += [note for note in (phase_note, stage_note, activity_note, action_note,
                                   question_note, updated_note) if note]
    warnings += [f"blocked: {job['title']}"
                 + (f" \u2014 {job['detail']}" if job["detail"] else f" \u2014 blocker {UNRECORDED}")
                 for job in blocked]
    found, _ = links_of(now_part, limit=8)
    insight, _ = field(now_part, "Insight")
    proposed, _ = field(now_part, "Proposed answer")
    reply, _ = field(now_part, "Reply with")
    return {
        "phase": phase or stage or UNRECORDED,
        "task": task, "task_reason": task_reason,
        "state": state, "state_reason": state_reason,
        "last_session": (done[-1]["title"] + (f" \u2014 {done[-1]['detail']}"
                                              if done[-1]["detail"] else "")) if done else None,
        "this_session": " \u00b7 ".join(job["title"] for job in active) if active else None,
        "question": {"text": question, "proposed": proposed, "reply": reply} if question else None,
        "documents": [list(pair) for pair in found],
        "warnings": warnings, "insight": insight,
        "source": str(path), "updated": updated, "base": str(Path(path).resolve().parent),
    }


def timestamp_warning(updated, now):
    """Compare displayed wall times only; zone labels are not timezone rules."""
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) ([A-Za-z0-9_+/-]+)"
    stamps = [re.fullmatch(pattern, value) if isinstance(value, str) else None
              for value in (updated, now)]
    if not all(stamps) or stamps[0][2] != stamps[1][2]:
        return None
    try:
        source, rendered = [datetime.strptime(stamp[1], "%Y-%m-%d %H:%M") for stamp in stamps]
    except ValueError:
        return None
    if source > rendered:
        return ("Source update time sorts after render time in the same displayed zone; "
                "verify the source timestamp or clock. Neither value was corrected.")
    return None


def recommendation_rows(text, width):
    """Keep supplied paragraph/list structure; never infer steps from prose."""
    rows = []
    for line in str(text).splitlines():
        if not line.strip():
            if rows and rows[-1] != "":
                rows.append("")
            continue
        match = re.match(r"^\s*(\d+[.)] |[-*] )(.*)$", line)
        prefix, value = match.groups() if match else ("", line)
        for index, part in enumerate(wrap(value, max(1, width - columns(prefix)))):
            rows.append((prefix if index == 0 else " " * columns(prefix)) + part)
    return rows


def recommendation_markdown(text):
    """Preserve explicit list markers while escaping their content."""
    rows = []
    for line in str(text).splitlines():
        match = re.match(r"^\s*(\d+[.)] |[-*] )(.*)$", line)
        if match:
            prefix, value = match.groups()
            rows.append(prefix + md(value))
        else:
            rows.append(md(line) if line.strip() else "")
    return rows


def team_rows(team):
    """Compact roster only; identity and delivery details remain in Agent."""
    if team is None:
        return [("TEAM", "not recorded", None)]
    if not team:
        return [("TEAM", "No established pairing", None)]
    members = {}
    for index, member in enumerate(team):
        key = (member.get("provider"), member.get("id") or index)
        if key not in members:
            members[key] = member
    labels = []
    for member in members.values():
        label = str(member.get("provider") or member.get("alias") or "Partner")
        label = {"claude": "Claude", "codex": "Codex"}.get(label, label)
        role = member.get("role") or ("partner · role unassigned" if member.get("id")
                                      else "recipient not selected")
        role = {"established partner (role not defined)": "partner · role unassigned",
                "role not defined": "role unassigned"}.get(role, role)
        labels.append(f"{label} ({role})")
    return [("TEAM", " + ".join(labels), None)]


def action_text(item, markdown=False):
    """Only explicit **Owner:** notation declares a display label."""
    match = re.fullmatch(r"\*\*([^*\n]+):\*\* (.+)", item, re.S)
    if match:
        owner, action = match.groups()
        return f"**{md(owner)}:** {md(action)}" if markdown else f"{owner}: {action}"
    return md(item) if markdown else item


def render_dashboard(summary, now, width=80, color=True, question_below=False, markdown=False):
    """One composed panel from a summary already in hand.

    Switch passes what it has just read; nothing is written to disk for this.
    The banner states whether the necessary context was recovered. It is never
    proved by rendering succeeding, and it is not a claim about which
    presentation ran.
    """
    get = summary.get
    if any(key in summary for key in ("where", "open_work", "recommendation")):
        return "\n".join(open_work_head(summary, width, color, markdown)
                         + dashboard_tail(summary, now, width, color, markdown, arrival=True))
    # --question-below remains accepted for older callers; this older grid
    # puts the question after its end marker, the arrival ends on it.
    question = get("question")
    restored = get("restored")
    version = kerd_version()
    loaded = f"Kerd {version}" if version else "Kerd version not read"
    if restored == "yes":
        badge, tone = "SESSION RESTORED \u2713 ", "green"
    elif restored in ("partial", "no"):
        badge, tone = "PICKUP INCOMPLETE ", "amber"
    else:
        badge, tone = "", None
    lines = [ink(pad(" KERD \u00b7 " + loaded, width - columns(badge)), "bold", "cyan", on=color)
             + ink(badge, tone, on=color and tone is not None),
             ink("\u2501" * width, "cyan", on=color), ""]
    if markdown:
        status = ("SWITCH IN COMPLETE ✓" if restored == "yes" else
                  "SWITCH IN INCOMPLETE" if restored in ("partial", "no") else
                  "SWITCH IN STATUS UNKNOWN")
        status += " \u00b7 " + loaded
        state = str(get("state") or UNRECORDED)
        if get("state_reason"):
            state += " — " + str(get("state_reason"))
        cells = [get("project") or UNRECORDED, get("phase") or UNRECORDED,
                 state, team_rows(get("team"))[0][1]]
        lines = [f"**KERD · {status}**", "",
                 "| PROJECT | PHASE | STATE | TEAM |",
                 "| --- | --- | --- | --- |",
                 "| " + " | ".join(md(value) for value in cells) + " |", ""]
        for label, value, empty in (("LAST SESSION", get("last_session"), "no completed job is recorded"),
                                   ("THIS SESSION", get("this_session"), "Nothing agreed yet.")):
            lines += [f"- **{label}**", "", f"  {md(value or empty)}", ""]

    rows = (("PROJECT", get("project") or UNRECORDED, None),
            ("PHASE", get("phase") or UNRECORDED, None),
            ("TASK", get("task") or UNRECORDED, get("task_reason")),
            ("STATE", get("state") or UNRECORDED, get("state_reason")),
            *team_rows(get("team")))
    for label, value, reason in rows:
        if markdown:
            continue
        for index, line in enumerate(wrap(str(value), width - 10)):
            lines.append(" " + ink(pad(label if index == 0 else "", 7), "dim", on=color)
                         + " " + line)
        for line in wrap("\u2014 " + reason, width - 10) if reason else []:
            lines.append(" " * 9 + ink(line, "dim", on=color))
    lines.append("")

    # The immediate work is part of the frame: it always renders, so a project
    # with nothing under its Now heading shows that gap rather than hiding it.
    # The backlog is deliberately not here; it stays behind the documents link.
    lines.append("- **NOW**\n" if markdown else ink(" NOW", "dim", on=color))
    now_items = get("now") or []
    if isinstance(now_items, str):  # one item written as prose, not a typo per character
        now_items = [now_items]
    items = [str(item) for item in now_items if item]
    if markdown:
        # The grid has no duplicate TASK column. Retain old-input task context
        # unless a NOW action is identical, and never drop limits.
        task = str(get("task") or "")
        covered = []
        for item in items:
            owner = re.fullmatch(r"\*\*([^*\n]+):\*\* (.+)", item, re.S)
            covered.append(owner.group(2) if owner else item)
        if task and task != UNRECORDED and not any(task == text for text in covered):
            lines += [f"  Focus: {md(task)}", ""]
        if get("task_reason"):
            lines += [f"  Task context: {md(get('task_reason'))}", ""]
    for position, item in enumerate(items, 1):
        if markdown:
            lines.append(f"  {position}. {action_text(item, markdown=True)}")
            continue
        prefix = f"   {position}. "
        for index, line in enumerate(wrap(action_text(item), width - len(prefix))):
            lines.append((prefix if index == 0 else " " * len(prefix)) + line)
    if not items:
        lines.append("  no immediate work recorded" if markdown else "   no immediate work recorded")
    lines.append("")
    # Older callers placed consequential limits in YOU. Preserve those under
    # NOW, without inferring ownership or turning the prose into extra tasks.
    if question and question.get("proposed"):
        lines += ["  **Scope / recommendation**" if markdown else " Scope / recommendation", ""]
        proposal = str(question["proposed"])
        lines += (["  " + line if line else "" for line in recommendation_markdown(proposal)] if markdown else
                  ["   " + line if line else "" for line in recommendation_rows(proposal, width - 3)])
        lines.append("")

    for label, value, empty in (("LAST SESSION", get("last_session"),
                                 "no completed job is recorded"),
                                ("THIS SESSION", get("this_session"), "Nothing agreed yet.")):
        if markdown:
            continue
        lines.append(ink(" " + label, "dim", on=color))
        lines += ["   " + line for line in wrap(value or empty, width - 3)]
    lines.append("")
    return "\n".join(lines + dashboard_tail(summary, now, width, color, markdown))


def kerd_version():
    """The Kerd version this renderer was loaded from, read from the package's
    own manifest beside it, so an arrival names the build that drew it rather
    than one remembered from a record. None when no manifest can be read."""
    root = Path(__file__).resolve().parents[3]
    for manifest in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        try:
            version = json.loads((root / manifest).read_text(encoding="utf-8")).get("version")
        except (OSError, ValueError, AttributeError):
            continue
        if isinstance(version, str) and version.strip():
            return version.strip()
    return None


def open_work_head(summary, width, color, markdown):
    """The arrival: a grid (project, phase, next, team), then where things
    stand, the open work, one recommendation and why. No copied saved step;
    the caller has already weighed every open item, the saved one included."""
    get = summary.get
    restored = get("restored")
    status = ("SWITCH IN COMPLETE \u2713" if restored == "yes" else
              "SWITCH IN INCOMPLETE" if restored in ("partial", "no") else
              "SWITCH IN STATUS UNKNOWN")
    version = kerd_version()
    status += f" \u00b7 Kerd {version}" if version else " \u00b7 Kerd version not read"
    project = str(get("project") or UNRECORDED)
    work = get("open_work")
    if isinstance(work, str):  # one item written as prose, not a list of letters
        work = [work]
    items = [str(item) for item in (work or []) if item]
    recommendation = get("recommendation") or {}
    if isinstance(recommendation, str):
        recommendation = {"text": recommendation}
    nothing = "No recommendation: nothing actionable is open."
    blocks = (("Where things stand", get("where"), "not recorded"),
              ("Last session", get("last_session"), "no completed job is recorded"))
    grid = (("PROJECT", project), ("PHASE", str(get("phase") or UNRECORDED)),
            ("NEXT", str(recommendation.get("text") or "Nothing actionable is open")),
            ("TEAM", team_rows(get("team"))[0][1]))
    if markdown:
        lines = [f"**{md(project.upper())} \u00b7 {status}**", "",
                 "| " + " | ".join(label for label, _ in grid) + " |",
                 "| --- | --- | --- | --- |",
                 "| " + " | ".join(md(value) for _, value in grid) + " |", ""]
        for label, value, empty in blocks:
            lines += [f"**{label}:** {md(value or empty)}", ""]
        lines += ["**Open work**", ""]
        lines += [f"{index}. {action_text(item, markdown=True)}" for index, item in enumerate(items, 1)]
        if not items:
            lines.append("No open work is recorded.")
        lines.append("")
        lines += [f"**Recommended:** {md(recommendation.get('text') or nothing)}"]
        if recommendation.get("text") and recommendation.get("why"):
            lines += ["", f"**Why:** {md(recommendation['why'])}"]
        return lines + [""]
    tone = "green" if restored == "yes" else "amber"
    name = " " + project.upper()
    if columns(name) + columns(status) + 2 <= width:
        lines = [ink(pad(name, width - columns(status)), "bold", "cyan", on=color)
                 + ink(status, tone, on=color)]
    else:
        lines = [ink(" " + line, "bold", "cyan", on=color) for line in wrap(project.upper(), width - 1)]
        lines += [ink(" " + line, tone, on=color) for line in wrap(status, width - 1)]
    lines += [ink("\u2501" * width, "cyan", on=color), ""]
    for label, value in grid:
        for index, line in enumerate(wrap(value, width - 10)):
            lines.append(" " + ink(pad(label if index == 0 else "", 7), "dim", on=color) + " " + line)
    lines.append("")
    for label, value, empty in blocks:
        lines.append(ink(" " + label.upper(), "dim", on=color))
        lines += ["   " + line for line in wrap(str(value or empty), width - 3)]
        lines.append("")
    lines.append(ink(" OPEN WORK", "dim", on=color))
    for position, item in enumerate(items, 1):
        prefix = f"   {position}. "
        for index, line in enumerate(wrap(action_text(item), width - len(prefix))):
            lines.append((prefix if index == 0 else " " * len(prefix)) + line)
    if not items:
        lines.append("   No open work is recorded.")
    lines.append("")
    lines.append(ink(" RECOMMENDED", "dim", on=color))
    lines += ["   " + line for line in wrap(str(recommendation.get("text") or nothing), width - 3)]
    if recommendation.get("text") and recommendation.get("why"):
        lines += ["   " + line for line in wrap("Why: " + str(recommendation["why"]), width - 3)]
    return lines + [""]


def document_href(target, base):
    """A clickable target: URLs as given, local paths resolved against base."""
    from urllib.parse import quote
    if target.startswith(("http://", "https://", "mailto:")):
        return quote(target, safe="/:#?=&%+@")
    path, sep, fragment = target.partition("#")
    href = quote(str((Path(base) / path).resolve()), safe="/")
    return href + ("#" + quote(fragment, safe="/") if sep else "")


def dashboard_tail(summary, now, width, color, markdown, arrival=False):
    """Attention, documents, insight and the one question, shared by both
    layouts. The older grid keeps its source footer and end marker; the
    arrival ends on its question, with documents on one line."""
    get = summary.get
    question = get("question")
    restored = get("restored")
    lines = []
    warnings = list(get("warnings") or [])
    time_warning = None if arrival else timestamp_warning(get("updated"), now)
    if time_warning:
        warnings.append(time_warning)
    if get("restore_note"):
        warnings.insert(0, str(get("restore_note")))
    elif restored in ("partial", "no"):
        warnings.insert(0, "Missing context: not recorded.")
    elif arrival and restored != "yes":
        # The arrival has no end marker, so an unconfirmed pickup says so here.
        warnings.insert(0, "Restoration not confirmed.")
    base = get("base") or "."
    open_able, broken = resolve_links([tuple(pair) for pair in (get("documents") or [])], base)
    warnings += [f"cannot be opened: {target} ({label})" for label, target in broken]
    if warnings:
        lines += (["**ATTENTION**\n"] + [f"- {md(warning)}" for warning in warnings] if markdown else
                  panel("\u26a0 NEEDS ATTENTION", warnings, width, "red", color)) + [""]

    if open_able and arrival and markdown:
        lines += ["**Documents:** " + " \u00b7 ".join(
            f"[{md(label)}](<{document_href(target, base)}>)" for label, target in open_able), ""]
        open_able = []
    if open_able:
        labels = " \u00b7 ".join(label for label, _ in open_able)
        lines.append("**DOCUMENTS**\n" if markdown else (" " + ink(pad("DOCUMENTS", 11), "dim", on=color)
                     + ink(labels, "cyan", on=color) if columns(labels) <= width - 12
                     else " " + ink("DOCUMENTS", "dim", on=color)))
        for label, target in open_able:
            if markdown:
                lines.append(f"- [{md(label)}](<{document_href(target, base)}>) · {code(target)}")
                continue
            lines += ["   " + line for line in wrap(f"\u2192 {target}  ({label})", width - 3)]
        lines.append("")

    if get("insight"):
        lines += (["> **★ Insight**", ">", f"> {md(get('insight'))}"] if markdown else
                  [" " + ink("\u2605", "amber", on=color) + " " + line if index == 0
                  else "   " + line
                  for index, line in enumerate(wrap(get("insight"), width - 3))])
        lines.append("")

    if arrival:
        if question and question.get("text"):
            lines += ([f"> 💬 **{md(question['text'])}**"] if markdown else
                      [ink("💬 " + line if index == 0 else "   " + line, "bold", on=color)
                       for index, line in enumerate(wrap(question["text"], width - 3))])
        return lines
    lines.append("---\n" if markdown else ink("\u2501" * width, "cyan", on=color))
    stamps = f"updated {get('updated') or 'unknown'} \u00b7 rendered {now}"
    source = get("source") or UNRECORDED
    one = f"read: {source} \u00b7 {stamps}"
    block = [one] if columns(one) <= width - 1 else [f"read: {source}", stamps]
    lines += ([f"**Read:** {md(source)}", "", md(stamps)] if markdown else
              [ink(" " + line, "dim", on=color)
               for entry in block for line in wrap(entry, width - 1)])
    ending = ("END OF PICKUP · SESSION READY" if restored == "yes" else
              "END OF PICKUP · RESTORATION INCOMPLETE" if restored in ("partial", "no") else
              "END OF PICKUP · RESTORATION UNCONFIRMED")
    if markdown:
        lines += ["", "```text", "━━ " + ending + " ━━", "```"]
    else:
        lines += [""] + [ink(line, "cyan", on=color) for line in wrap(ending, width)]
    if question and question.get("text"):
        lines += [""] + ([f"> 💬 **{md(question['text'])}**"] if markdown else
                          [ink("💬 " + line if index == 0 else "   " + line, "bold", on=color)
                           for index, line in enumerate(wrap(question["text"], width - 3))])
    return lines


def render_closing(summary, now, width=80, color=True, markdown=False):
    """The end of Switch Out: how far the save reached, what changed, what next.

    A grid (project, save, phase, released), this session's changes in product
    terms, the next step with its reason, then one closing line. Save
    mechanics stay in the records; a problem (a save that did not reach the
    remote, memory not ready, work left behind) appears under Attention only
    when it is true. The box never claims the session exited or the context
    was cleared: that is the person's action, named in the closing line only
    after a confirmed save with memory ready.
    """
    get = summary.get
    saved = get("saved")
    branch = get("branch")
    if saved == "remote-verified":
        badge, tone, cell = "SESSION SAVED \u2713", "green", f"Pushed to {branch}" if branch else "Pushed"
    elif saved == "committed":
        badge, tone, cell = "SAVED LOCALLY", "amber", "Committed, not pushed"
    elif saved == "not-saved":
        badge, tone, cell = "NOT SAVED", "red", "Not saved"
    else:  # absent or unrecognised: unknown is not evidence that nothing was saved
        badge, tone, cell = "SAVE STATUS NOT RECORDED", "amber", "Not recorded"
        saved = "unknown"
    ready = get("handoff_ready")
    # `boundary` is handoff.py boundary's verdict: exactly "passed" on exit 0,
    # otherwise its failures. Anything else, absent included, withholds the ✓
    # and the restart: a save that no fetch has shown on a remote is not proven.
    proven = get("boundary") == "passed"
    if not proven:
        badge, tone = badge.replace(" \u2713", ""), ("amber" if tone == "green" else tone)
    attention = []
    if saved == "committed":
        attention.append("The save is committed on this machine but not verified on the remote; "
                         "push before switching devices.")
    elif saved == "not-saved":
        attention.append("Nothing was committed: this session's work is only in the working tree.")
    elif saved == "unknown":
        attention.append("The save status was not recorded, so it cannot be treated as saved.")
    if ready is False:
        attention.append("Memory for the next session is incomplete; the next step names what is missing.")
    elif ready is not True:
        attention.append("Whether memory is ready for the next session was not recorded.")
    tree = get("tree")
    if tree and str(tree).strip().rstrip(".").lower() != "clean":
        attention.append(f"Left in the working tree: {tree}")
    if not proven:
        failed = get("boundary")
        if isinstance(failed, str):
            failed = [failed]
        failed = [str(item) for item in (failed or []) if item]
        attention += ([f"Boundary check failed: {item}" for item in failed] if failed else
                      ["The boundary check was not recorded, so the save is not proven on a remote."])
    attention += [str(item) for item in (get("warnings") or []) if item]

    confirmed = saved in ("remote-verified", "committed") and ready is True and proven
    if confirmed:
        # Only Claude has /clear; any other or unrecognised host gets the
        # host-neutral line, and an unrecorded host is taken as Claude.
        host = str(get("host") or "claude").strip().lower()
        closing = ("Exit and restart or /clear and /kerd:switch in to pick up from here."
                   if host == "claude" else
                   "Exit and restart, then switch in to pick up from here.")
    elif saved not in ("remote-verified", "committed"):
        closing = "Keep this session open and resolve the save before clearing context."
    elif not proven:
        closing = "Keep this session open and resolve the boundary check before clearing context."
    elif ready is False:
        closing = "Keep this session open and resolve the missing handoff context before clearing context."
    else:
        closing = "Keep this session open and record handoff readiness before clearing context."

    project = str(get("project") or "Kerd")
    # The next step lives once, in "Next time" with its reason; the grid's
    # fourth cell says what this sitting released.
    grid = (("PROJECT", project), ("SAVED", cell), ("PHASE", str(get("phase") or UNRECORDED)),
            ("RELEASED", str(get("released") or "Nothing released")))
    changes = get("this_session")
    if isinstance(changes, str):  # one change written as prose, not a list of letters
        changes = [changes]
    changes = [str(item) for item in (changes or []) if item]
    why = get("why")

    if markdown:
        lines = [f"**{md(project.upper())} \u00b7 {badge}**", "",
                 "| " + " | ".join(label for label, _ in grid) + " |",
                 "| --- | --- | --- | --- |",
                 "| " + " | ".join(md(value) for _, value in grid) + " |", "",
                 "**This session**", ""]
        lines += [f"- {md(item)}" for item in changes] or ["Nothing recorded."]
        lines.append("")
        lines.append(f"**Next time:** {md(get('next') or UNRECORDED)}"
                     + (f" **Why:** {md(why)}" if why and get("next") else ""))
        lines.append("")
        if attention:
            lines += ["**ATTENTION**", ""] + [f"- {md(item)}" for item in attention] + [""]
        lines.append(md(closing))
        return "\n".join(lines)

    lines = [ink(pad(" " + project.upper(), width - columns(badge)), "bold", "cyan", on=color)
             + ink(badge, tone, on=color)] if columns(project) + columns(badge) + 2 <= width else \
            [ink(" " + line, "bold", "cyan", on=color) for line in wrap(project.upper(), width - 1)] + \
            [ink(" " + line, tone, on=color) for line in wrap(badge, width - 1)]
    lines += [ink("\u2501" * width, "cyan", on=color), ""]
    for label, value in grid:  # RELEASED is eight wide
        for index, line in enumerate(wrap(value, width - 11)):
            lines.append(" " + ink(pad(label if index == 0 else "", 8), "dim", on=color) + " " + line)
    lines += ["", ink(" THIS SESSION", "dim", on=color)]
    for item in changes or ["Nothing recorded."]:
        lines += ["   \u00b7 " + line if index == 0 else "     " + line
                  for index, line in enumerate(wrap(item, width - 5))]
    lines += ["", ink(" NEXT TIME", "dim", on=color)]
    lines += ["   " + line for line in wrap(get("next") or UNRECORDED, width - 3)]
    if why and get("next"):
        lines += ["   " + line for line in wrap("Why: " + str(why), width - 3)]
    lines.append("")
    if attention:
        lines += panel("\u26a0 NEEDS ATTENTION", ["\u00b7 " + item for item in attention],
                       width, "red", color) + [""]
    lines.append(ink("\u2501" * width, "cyan", on=color))
    lines += [ink(" " + line, "bold", on=color) for line in wrap(closing, width - 1)]
    return "\n".join(lines)


def dashboard(path, text, now, width=80, color=True, restored=None, restore_note=None,
              question_below=False, markdown=False):
    summary = summary_from_record(path, text)
    summary["restored"], summary["restore_note"] = restored, restore_note
    return render_dashboard(summary, now, width, color, question_below, markdown)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", help="Path to one work record")
    parser.add_argument("--summary", metavar="PATH_OR_DASH",
                        help='Dashboard from a summary already in hand; "-" reads JSON '
                             "on stdin, so the caller writes no file")
    parser.add_argument("--closing", metavar="PATH_OR_DASH",
                        help='The Switch Out box from a closing summary; "-" reads JSON on stdin')
    parser.add_argument("--restored", choices=("yes", "partial", "no"),
                        help="Whether the necessary context was recovered. Not which presentation ran, and never proved by rendering succeeding")
    parser.add_argument("--restore-note", help="What is missing when the pickup is not complete")
    parser.add_argument("--width", type=int, default=80)
    parser.add_argument("--compact", action="store_true",
                        help="A few lines for a change of state, not the whole view")
    parser.add_argument("--dashboard", action="store_true",
                        help="One composed panel on arrival, for switch-in")
    parser.add_argument("--question-below", action="store_true",
                        help="Compatibility flag: questions always come last")
    parser.add_argument("--color", action="store_true",
                        help="Force colour on when output is piped or captured")
    parser.add_argument("--no-color", action="store_true",
                        help="Plain text; also implied by NO_COLOR or a non-terminal")
    parser.add_argument("--markdown", action="store_true",
                        help="Chat presentation: theme-styled Markdown, no ANSI; client controls colour and wrapping")
    args = parser.parse_args()
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    color = args.color or not (
        args.no_color or os.environ.get("NO_COLOR") or not sys.stdout.isatty())
    if args.closing:
        raw = sys.stdin.read() if args.closing == "-" else Path(args.closing).read_text("utf-8")
        try:
            closing = json.loads(raw)
        except json.JSONDecodeError as error:
            print(f"Closing summary is not readable JSON: {error}", file=sys.stderr)
            return 2
        print(render_closing(closing, now, args.width, color, args.markdown))
        return 0
    if args.summary:
        raw = sys.stdin.read() if args.summary == "-" else Path(args.summary).read_text("utf-8")
        try:
            summary = json.loads(raw)
        except json.JSONDecodeError as error:
            print(f"Summary is not readable JSON: {error}", file=sys.stderr)
            return 2
        summary.setdefault("restored", args.restored)
        summary.setdefault("restore_note", args.restore_note)
        print(render_dashboard(summary, now, args.width, color, args.question_below, args.markdown))
        return 0
    if not args.record:
        print("Give --record <path> or --summary -", file=sys.stderr)
        return 2
    path = Path(args.record)
    if not path.is_file():
        print(f"No work record at {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    if args.dashboard:
        print(dashboard(path, text, now, args.width, color, args.restored, args.restore_note,
                        args.question_below, args.markdown))
        return 0
    print((compact if args.compact else render)(path, text, now, args.width))
    return 0


if __name__ == "__main__":
    sys.exit(main())
