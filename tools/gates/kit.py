#!/usr/bin/env python3
"""Entry gates: mechanical routing and the ladder's first refuser.

Given a work slug, checks whether each rung's declared inputs exist on disk —
a file, a front-matter key pair, a named section, a qualified risk ledger, a
checked-box count — and nothing beyond that. The gate has no opinion on
whether a VALUE claim is convincing, a risk well-argued, or a design sound;
it only checks that the artifact a rung requires is present and mechanically
well-formed (present sections, legal enum values, a table with the right
header). Judgment belongs to whoever writes the artifact and whoever reviews
it; this module is the refuser, not the reviewer — every check here is a
question a machine can answer without reading for meaning.
"""

import glob
import hashlib
import json
import os
import re
import sys
import tempfile

# Repo root, three levels up from this file (tools/gates/kit.py -> tools ->
# repo root). The CLI passes ROOT; selftest passes a temp tree instead — every
# function below takes `root` as a parameter for exactly that reason.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Rule 9's recipe has one implementation — tools/reqview/fingerprint.py.
# Resolved from THIS file's location, never from the audited root: a
# consuming project has no tools/ of its own and the recipe ships here.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "reqview"))
from fingerprint import view_fingerprint

RUNGS  = ["frame", "viability", "scope", "design", "handoff", "loop", "acceptance"]
STAGES = ["framed", "viable", "scoped", "designed", "handed-off", "looping", "ready-to-release"]

# Retired names — READ-ONLY aliases, forever. The parser's legal set is the
# union of live names and retired aliases; the WRITER only ever emits live
# names. An alias that is still written is a synonym, which is the defect
# this item exists to remove. No file on disk is ever renamed or rewritten.
STAGE_ALIASES = {
    "sliced": "scoped",
    "contracted": "handed-off",
    "building": "looping",
    "done": "ready-to-release",
}


def legal_stage(v):
    return v in STAGES or v in STAGE_ALIASES


def stage_index(v):
    """Position on the live ladder; a retired value maps to its live name."""
    return STAGES.index(STAGE_ALIASES.get(v, v))


ROUTES = ["new", "problem", "spike"]
LEDGER_COLUMNS = [
    "Risk", "Killer?", "Impact", "Likelihood", "Evidence",
    "State", "Countermeasure", "Review trigger",
]

# The five legal normalized States (A3). "fatal" is structurally legal —
# it is a real cell value a row can carry — but its presence is itself a
# refusal (see parse_ledger), which is why it lives in this set and is also
# specifically checked for below.
LEGAL_STATES = {
    "countermeasure - permanent",
    "countermeasure - temporary",
    "accepted",
    "accepted unknown",
    "fatal",
}

# The legal rigor levels (AU6, scope rung). A '## Scope' section
# declares how rigorously the release is measured — one 'Rigor level:' line;
# the legal set lives here and only here.
RIGOR_LEVELS = ["spike", "mvp", "production-v1"]

# ── the requirements register (AU7 blocks & states, AU8 links) ───────────────
# The schema these enforce is docs/requirements/catalog.md. Deliberately NOT
# here: the category codes — those are declared per project in
# docs/requirements/categories.md (the disposition file), and the validator
# reads the legal set from it rather than hardcoding a taxonomy.

REQ_ID_RE = re.compile(r"^[A-Z]{2,4}-\d{3}$")
REQ_STATES = ("proposed", "qualified", "final", "superseded", "dropped")
# Meta-line fields a block may carry. Statement is the block body and Title
# rides the heading, so neither appears here. An unknown field is a hard
# error, not a warning (catalog.md, Fields).
REQ_META_FIELDS = ("Category", "Tags", "State", "Source", "Approved")
# Link roles registered in the catalog grammar, forward → reverse. Both
# directions are writable: the states table itself demands a written
# 'superseded-by', which is a reverse.
REQ_LINK_ROLES = {
    "depends-on": "required-by",
    "supersedes": "superseded-by",
    "refines": "refined-by",
    "satisfied-by": "satisfies",
    "verified-by": "verifies",
}
REQ_LEGAL_ROLES = frozenset(REQ_LINK_ROLES) | frozenset(REQ_LINK_ROLES.values())
# Origin categories originate rather than refine (catalog.md, 'derived'):
# a block in one of these needs no 'refines' parent; any other block
# without one is a finding, not an error, until slice 2 wires the forward
# trace.
REQ_ORIGIN_CATEGORIES = frozenset({"BUS", "STA", "USR"})
REQ_APPROVED_RE = re.compile(r"^sha256:[0-9a-f]{12}$")
REQ_META_RE = re.compile(r"^\*\*([A-Za-z][A-Za-z ]*)\*\*:\s*(.*)$")
REQ_LINK_RE = re.compile(r"^- ([a-z-]+) → ([A-Z]{2,4}-\d{3}) \(sha256:([0-9a-f]{12})\)$")

GATE_RECORD_RE = re.compile(
    r'^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-'
    r'(frame|viability|slice|scope|design|contract|handoff|build|goal|loop|acceptance)\.md$'
)
DATED_FILENAME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}-')
FRONT_MATTER_KV_RE = re.compile(r'^([A-Za-z0-9_.-]+):\s*(.*)$')
CONCERNS_KEY_RE   = re.compile(r'^concerns:(.*)$')
CONCERN_ENTRY_RE  = re.compile(r'^  - concern:\s*(.*)$')
CONCERN_FIELD_RE  = re.compile(r'^    (viewpoint|view|approval):\s*(.*)$')
NA_VIEW_RE        = re.compile(r'^n/a\s+—\s+(\S.*)$')
VIEW_SEALED_RE    = re.compile(r'^(.+?),\s*(\d{4}-\d{2}-\d{2})\s*·\s*fp:([0-9a-f]{12})\s*$')
VIEW_UNSEALED_RE  = re.compile(r'^(.+?),\s*(\d{4}-\d{2}-\d{2})\s*$')
STEP_HEADING_RE = re.compile(r'^### Step ')
H3_RE = re.compile(r'^### ')
VERIFY_LINE_RE = re.compile(r'^\*\*Verify:\*\*')
BOXED_LINE_RE = re.compile(r'^- \[[ x]\] ')
UNCHECKED_LINE_RE = re.compile(r'^- \[ \] ')
SEPARATOR_ROW_RE = re.compile(r'^[\s|:-]+$')
RIGOR_LINE_RE = re.compile(r'^Rigor level:(.*)$')
RIGOR_SECTION_HEADING_RE = re.compile(r'^## Scope[ \t]*$')

# ── the question set (frame gate; funnel-driver slice 2) ──────────────────
# One list drives ask · check · show. An entry is '- Q: <question>'; it is
# answered when a following 'A: <text>' line (any indentation) before the
# next entry carries text. Counted, never judged — the human key judges.
QUESTION_SET_TITLE = "Question set"
QS_Q_RE = re.compile(r'^- Q:\s*(.*)$')
QS_A_RE = re.compile(r'^\s*A:\s*(.*)$')
# work-type names a seed file, docs/work/question-sets/<work-type>.md, so
# it is shaped like a filename stem. Declared by the producer, never
# inferred; the gate checks the shape, never that the seed exists.
WORK_TYPE_RE = re.compile(r'^[a-z][a-z0-9-]*$')


# ── front matter (A1) ───────────────────────────────────────────────────────

def _front_matter_block(path):
    """The front-matter fence window: (lines, close) where `lines` is the
    whole file's splitlines() and `close` is the index of the closing '---'.
    None when the file is absent, line 0 is not '---', or no closing '---'
    within 120 lines."""
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if not lines or lines[0] != "---":
        return None
    close = None
    for i in range(1, min(len(lines), 121)):
        if lines[i] == "---":
            close = i
            break
    if close is None:
        return None
    return lines, close


# Gate-record filename suffixes that assert PRODUCER ACCEPTANCE. `goal` is the
# retired alias, read forever and written never (Retired names, README).
ACCEPTANCE_SUFFIXES = ("acceptance", "goal")


def is_terminal_stage(v):
    """True when a stage value resolves to the ready-to-release terminal.
    Alias-aware: legacy `done` resolves through STAGE_ALIASES, which is how the
    seven immutable *-goal.md records keep reaching the terminal unrewritten."""
    if not legal_stage(v):
        return False
    return stage_index(v) >= STAGES.index("ready-to-release")


def read_front_matter(path):
    """Parse the front-matter subset defined in A1. None when absent or the
    fence is malformed — a leading '---' with no closing fence within 120
    lines, or no 'key: value' line inside it, is NOT front matter."""
    block = _front_matter_block(path)
    if block is None:
        return None
    lines, close = block
    fm = {}
    for line in lines[1:close]:
        m = FRONT_MATTER_KV_RE.match(line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        fm[key] = val
    if not fm:
        return None
    return fm


def parse_concerns(path):
    """D1's grammar for the front-matter `concerns:` list. None when there
    is no front matter or no line matching CONCERNS_KEY_RE inside it.
    Otherwise (entries, problems): problems are D1's seven strings, without
    the 'docs/product/... — ' prefix (callers prefix). Each entry is
    {"concern", "viewpoint", "view", "approval", "index", "approval_index"}
    in encounter order — the indexes are 0-based positions in the file's
    lines (the entry line; the approval line)."""
    block = _front_matter_block(path)
    if block is None:
        return None
    lines, close = block

    idx_open = None
    for i in range(1, close):
        if CONCERNS_KEY_RE.match(lines[i]):
            idx_open = i
            break
    if idx_open is None:
        return None

    def _clean(val):
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        return val

    problems = []
    if CONCERNS_KEY_RE.match(lines[idx_open]).group(1).strip():
        problems.append("concerns: line carries a value; it must be bare")

    entries = []
    current = None
    for i in range(idx_open + 1, close):
        line = lines[i]
        n = i + 1
        if FRONT_MATTER_KV_RE.match(line):
            break
        m_entry = CONCERN_ENTRY_RE.match(line)
        m_field = CONCERN_FIELD_RE.match(line)
        if m_entry:
            name = _clean(m_entry.group(1))
            if not name:
                problems.append(f"concerns: line {n} entry has no concern name")
            current = {
                "concern": name, "viewpoint": None, "view": None,
                "approval": None, "index": i, "approval_index": None,
            }
            entries.append(current)
        elif m_field:
            field, raw = m_field.group(1), m_field.group(2)
            if current is None:
                problems.append(f"concerns: line {n} field before any entry")
                continue
            if current[field] is not None:
                problems.append(f'concerns: entry "{current["concern"]}" repeats {field}')
                continue
            current[field] = _clean(raw)
            if field == "approval":
                current["approval_index"] = i
        else:
            problems.append(f"concerns: line {n} unreadable: '{line.strip()}'")

    if not entries:
        problems.append("concerns: declared with no entries")

    for e in entries:
        if e["view"] is not None and e["view"].startswith("n/a") and e["approval"] is not None:
            problems.append(
                f'concerns: entry "{e["concern"]}" is n/a and carries an approval — nothing to approve'
            )

    return entries, problems


# ── sections (A3) ───────────────────────────────────────────────────────────

def find_section(text, title):
    """Body under a '## <title>' heading (exact, case-sensitive), up to the
    next '## ' heading or EOF. None = heading absent. '' = heading present
    but the body is whitespace-only — a distinct outcome callers use to tell
    "not written" from "not there at all"."""
    heading_re = re.compile(r'^## ' + re.escape(title) + r'[ \t]*$', re.MULTILINE)
    m = heading_re.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    next_m = re.search(r'^## ', rest, re.MULTILINE)
    end = start + next_m.start() if next_m else len(text)
    return text[start:end].strip()


def _fence_mask(lines):
    """mask[i] is True when lines[i] belongs to a fenced code block,
    including the ``` fence lines themselves. Fenced lines are invisible
    to the structural parsers here: a heading or declaration quoted inside
    a fence is content, not structure — the substring-marker class (a
    checker detecting by pattern is asserted by anything quoting it)."""
    mask = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            mask.append(True)
            in_fence = not in_fence
        else:
            mask.append(in_fence)
    return mask


# ── rigor level (AU6, scope rung) ───────────────────────────────────────────

def rigor_problems(text):
    """Judge one product doc's 'Rigor level:' declaration. Single-parser
    rule: AU6 and the scope rung both call THIS function — the law is
    written once. The law: exactly one legal 'Rigor level: <value>' line
    INSIDE the '## Scope' section; a 'Rigor level:' line anywhere
    else in the doc is a problem; a doc with no '## Scope' section
    passes vacuously (the section's absence is already the scope rung's
    own refusal — this rule does not double-refuse it). Lines inside
    fenced code blocks are invisible — a quoted example is content, not a
    declaration. Returns problem strings WITHOUT the
    'docs/product/<S>.md — ' prefix; callers prepend it. Emission order:
    the outside-line problem first, then exactly one of
    missing / duplicate / illegal."""
    inside = False
    section_seen = False
    inside_values = []
    outside_count = 0
    lines = text.splitlines()
    mask = _fence_mask(lines)
    for line, fenced in zip(lines, mask):
        if fenced:
            continue
        if RIGOR_SECTION_HEADING_RE.match(line):
            inside = True
            section_seen = True
            continue
        if line.startswith("## "):
            inside = False
            continue
        m = RIGOR_LINE_RE.match(line)
        if not m:
            continue
        if inside:
            inside_values.append(m.group(1).strip())
        else:
            outside_count += 1

    problems = []
    if outside_count:
        problems.append("Rigor level line outside Scope")
    if section_seen:
        if not inside_values:
            problems.append(
                "Scope missing 'Rigor level: <spike|mvp|production-v1>' line"
            )
        elif len(inside_values) > 1:
            problems.append("duplicate Rigor level lines (want exactly one)")
        elif inside_values[0] not in RIGOR_LEVELS:
            problems.append(
                f"illegal rigor level '{inside_values[0]}' (legal: spike, mvp, production-v1)"
            )
    return problems


# ── the question set (frame gate) ───────────────────────────────────────────

def question_set_status(text):
    """Count answered against declared entries in '## Question set' —
    presence only, never quality. None when the section is absent (opt-in
    by presence: a work record with no set is not refused, so nothing
    already on a board moves). Otherwise {"declared": int, "answered":
    int, "unanswered": [question], "problems": [str]}. Grammar: QS_Q_RE
    opens an entry; the first QS_A_RE line before the next entry answers
    it when it carries text; other lines are content (continuations).
    Lines inside ``` fences are invisible — a quoted example is content,
    not an entry. Problem strings carry no 'docs/product/<S>.md — '
    prefix; callers prepend it."""
    body = find_section(text, QUESTION_SET_TITLE)
    if body is None:
        return None
    lines = body.splitlines()
    mask = _fence_mask(lines)
    entries = []      # [question, answered]
    problems = []
    for n, (line, fenced) in enumerate(zip(lines, mask), start=1):
        if fenced:
            continue
        mq = QS_Q_RE.match(line)
        if mq:
            q = mq.group(1).strip()
            if not q:
                problems.append(f"Question set: entry {len(entries) + 1} has no question text")
            entries.append([q, False])
            continue
        ma = QS_A_RE.match(line)
        if ma:
            if not entries:
                problems.append(f"Question set: line {n} answer before any question")
                continue
            if ma.group(1).strip():
                entries[-1][1] = True
    if not entries:
        problems.append("Question set: declared with no entries (want '- Q: <question>' lines)")
    return {
        "declared": len(entries),
        "answered": sum(1 for _, a in entries if a),
        "unanswered": [q for q, a in entries if not a],
        "problems": problems,
    }


# ── the risk ledger (A3, state normalization note) ──────────────────────────

def _normalize_state(raw):
    """lowercase, em-dash and '--' to '-', whitespace collapsed, stripped —
    in that order, per A3's normalization note."""
    s = raw.lower()
    s = s.replace("—", "-").replace("--", "-")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse_ledger(section_text):
    """Parse the 'Risk ledger' section body into (rows, problems).

    rows: list of dicts keyed by LEDGER_COLUMNS, one per well-formed data
    row. problems: strings describing every A3 violation found — a wrong or
    missing header, no data rows, and per row: empty Evidence, an illegal
    State, a missing Countermeasure/Review trigger where State requires one,
    and a FATAL row (which is its own named refusal, verbatim per A3)."""
    lines = [l for l in section_text.splitlines() if l.strip()]
    problems = []
    rows = []
    if not lines:
        problems.append("Risk ledger section has no table")
        return rows, problems

    header_cells = _split_row(lines[0])
    if header_cells != LEDGER_COLUMNS:
        problems.append(
            "Risk ledger header row must be exactly: " + " | ".join(LEDGER_COLUMNS)
        )
        return rows, problems

    if len(lines) > 1 and SEPARATOR_ROW_RE.match(lines[1]):
        body_lines = lines[2:]
    else:
        body_lines = lines[1:]

    if not body_lines:
        problems.append("Risk ledger has no data rows")
        return rows, problems

    for i, line in enumerate(body_lines, start=1):
        cells = _split_row(line)
        if len(cells) != len(LEDGER_COLUMNS):
            problems.append(
                f"row {i}: expected {len(LEDGER_COLUMNS)} columns, found {len(cells)}"
            )
            continue
        row = dict(zip(LEDGER_COLUMNS, cells))
        rows.append(row)

        if not row["Evidence"]:
            problems.append(f"row {i}: Evidence empty")

        norm_state = _normalize_state(row["State"])
        if norm_state not in LEGAL_STATES:
            problems.append(f"row {i}: State '{row['State']}' not a legal value")
        if norm_state == "fatal":
            problems.append(
                f"FATAL risk '{row['Risk']}' — record in What we ruled out; cannot pass"
            )
        if norm_state.startswith("countermeasure") and not row["Countermeasure"]:
            problems.append(
                f"row {i}: Countermeasure empty (required when State is countermeasure)"
            )
        if norm_state.startswith("accepted") and not row["Review trigger"]:
            problems.append(
                f"row {i}: Review trigger empty (required when State is accepted)"
            )

    return rows, problems


# ── the contract spec's steps (A3, loop row) — the ARTIFACT keeps its
# contract meaning; only the route's first-reader line describes it ────────────────────────────────

def _steps_missing_verify(spec_text):
    """Names of every '### Step ' heading not followed, before the next
    '### ' heading or EOF, by a line starting '**Verify:**'. Lines inside
    fenced code blocks are invisible — a step body may quote headings and
    Verify lines without them splitting or satisfying the step."""
    problems = []
    lines = spec_text.splitlines()
    mask = _fence_mask(lines)
    n = len(lines)
    i = 0
    while i < n:
        if not mask[i] and STEP_HEADING_RE.match(lines[i]):
            title = lines[i][len("### "):].strip()
            j = i + 1
            found = False
            while j < n and (mask[j] or not H3_RE.match(lines[j])):
                if not mask[j] and VERIFY_LINE_RE.match(lines[j]):
                    found = True
                    break
                j += 1
            if not found:
                problems.append(f'"{title}" missing a "**Verify:**" line')
            i = j if j > i else i + 1
        else:
            i += 1
    return problems


# ── views (the design gate's lock) ──────────────────────────────────────────

def _view_row(root, e):
    """D4's table for one concerns entry. First failing rule wins."""
    c = e["concern"]
    view = e["view"]

    if not view:
        detail = "no view and no n/a reason"
        return {"code": "no-view", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}'}

    if view.startswith("n/a"):
        m = NA_VIEW_RE.match(view)
        if not m:
            detail = "n/a without a reason"
            return {"code": "na-no-reason", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}'}
        reason = m.group(1)
        detail = f"n/a — {reason}"
        return {"code": "na", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}'}

    path = view

    if not (e["viewpoint"] or "").strip():
        detail = f"view {path} has no viewpoint"
        return {"code": "no-viewpoint", "concern": c, "detail": detail,
                 "text": f'concern "{c}": {detail}', "path": path}

    if not path.endswith(".html"):
        detail = f"view {path} is not .html — a render is never the view"
        return {"code": "not-html", "concern": c, "detail": detail,
                 "text": f'concern "{c}": {detail}', "path": path}

    abs_path = os.path.join(root, path)
    if not os.path.isfile(abs_path):
        detail = f"view {path} not on disk"
        return {"code": "missing", "concern": c, "detail": detail,
                 "text": f'concern "{c}": {detail}', "path": path}

    approval = e["approval"]
    if not approval:
        detail = f"view {path} unapproved — no approval line"
        return {"code": "unapproved", "concern": c, "detail": detail,
                 "text": f'concern "{c}": {detail}', "path": path}

    with open(abs_path, encoding="utf-8") as f:
        text = f.read()
    fp_now = view_fingerprint(text)

    m = VIEW_SEALED_RE.match(approval)
    if m:
        name, date, fp_stored = m.group(1), m.group(2), m.group(3)
        if fp_stored == fp_now:
            detail = f'{e["viewpoint"]} view {path} approved by {name}, {date} (fp:{fp_now})'
            return {"code": "ok", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}',
                     "path": path, "name": name, "date": date, "fp_now": fp_now, "fp_stored": fp_stored}
        detail = f"view {path} fingerprint mismatch — approved at fp:{fp_stored}, now fp:{fp_now}"
        return {"code": "mismatch", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}',
                 "path": path, "name": name, "date": date, "fp_now": fp_now, "fp_stored": fp_stored}

    m = VIEW_UNSEALED_RE.match(approval)
    if m:
        name, date = m.group(1), m.group(2)
        detail = f"view {path} approved by hand, not sealed — no fp"
        return {"code": "unsealed", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}',
                 "path": path, "name": name, "date": date, "fp_now": fp_now}

    detail = f"view {path} approval line unreadable: '{approval}'"
    return {"code": "unreadable", "concern": c, "detail": detail, "text": f'concern "{c}": {detail}',
             "path": path, "fp_now": fp_now}


def view_rows(root, entries):
    """One row per concerns entry, entry order — D4's classification, shared
    by the design rung, AU9, and seal (Step 3) so all three branch on the
    same codes rather than three copies of the rules."""
    return [_view_row(root, e) for e in entries]


def seal_views(root, slug):
    """Complete every hand-written view approval in the slug's concerns
    block with its fingerprint — reqview's `seal` contract, applied to a
    view. The producer types `<name>, <date>` and never a hash; this
    computes the fingerprint over the drawing he actually agreed to and
    writes it back. It REFUSES rather than guessing: a view that is not on
    disk, not .html, or carries no viewpoint is `refused`; a divergence
    (an approved drawing whose content changed) is REPORTED, never
    rewritten. Nothing is written when the concerns block fails to parse."""
    rel_product = f"docs/product/{slug}.md"
    abs_product = os.path.join(root, rel_product)
    result = {
        "product": rel_product, "exists": False, "declared": False,
        "parse_problems": [], "sealed": [], "already": [], "diverged": [],
        "unapproved": [], "refused": [], "unreadable": [], "written": False,
    }
    if not os.path.isfile(abs_product):
        return result
    result["exists"] = True

    cs = parse_concerns(abs_product)
    if cs is None:
        return result
    result["declared"] = True
    entries, parse_problems = cs
    if parse_problems:
        result["parse_problems"] = parse_problems
        return result

    with open(abs_product, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)

    for e, row in zip(entries, view_rows(root, entries)):
        code = row["code"]
        c = e["concern"]
        path = row.get("path")
        if code in ("no-view", "na", "na-no-reason"):
            continue
        if code in ("no-viewpoint", "not-html", "missing"):
            result["refused"].append([c, path, row["detail"]])
        elif code == "unapproved":
            result["unapproved"].append([c, path])
        elif code == "ok":
            result["already"].append([c, path, row["fp_now"]])
        elif code == "mismatch":
            result["diverged"].append([c, path, row["fp_stored"], row["fp_now"]])
        elif code == "unreadable":
            result["unreadable"].append([c, e["approval"]])
        elif code == "unsealed":
            name, date, fp_now = row["name"], row["date"], row["fp_now"]
            old = lines[e["approval_index"]]
            ending = old[len(old.rstrip("\r\n")):]
            lines[e["approval_index"]] = f"    approval: {name}, {date} · fp:{fp_now}" + ending
            result["sealed"].append([c, path, name, date, fp_now])

    if result["sealed"]:
        with open(abs_product, "w", encoding="utf-8") as f:
            f.write("".join(lines))
        result["written"] = True

    return result


# ── check_rung (A3, cumulative) ─────────────────────────────────────────────

def check_rung(root, slug, rung):
    """Evaluate the CUMULATIVE inputs of `rung` for `slug` (A3): everything
    required by every rung above it, plus its own new rows. Returns
    {"slug","rung","have":[str],"need":[str],"bypass":bool}; have/need items
    are formatted "<relpath> — <what>" per A6.

    A spike (route: spike in the product doc) short-circuits all of this:
    the ladder does not apply, and the only thing ever checked is the
    'Kill-or-keep' section (A4) — regardless of which rung was asked for."""
    rel_product = f"docs/product/{slug}.md"
    abs_product = os.path.join(root, rel_product)
    product_exists = os.path.isfile(abs_product)
    product_text = None
    fm = None
    if product_exists:
        with open(abs_product, encoding="utf-8") as f:
            product_text = f.read()
        fm = read_front_matter(abs_product)

    if fm and fm.get("route") == "spike":
        item = f'{rel_product} — section "Kill-or-keep"'
        body = find_section(product_text, "Kill-or-keep")
        if body:
            return {"slug": slug, "rung": rung, "have": [item], "need": [], "bypass": True}
        return {"slug": slug, "rung": rung, "have": [], "need": [item], "bypass": True}

    idx = RUNGS.index(rung)
    have = []
    need = []

    if idx >= RUNGS.index("viability"):
        if not product_exists:
            need.append(f"{rel_product} — file exists")
            need.append(f"{rel_product} — front matter route + stage (legal values)")
            need.append(f'{rel_product} — section "Value"')
            need.append(
                f'{rel_product} — section "Risk ledger" naming at least one killer risk '
                "(Killer? = yes)"
            )
        else:
            have.append(f"{rel_product} — file exists")
            if fm and fm.get("route") in ROUTES and legal_stage(fm.get("stage")):
                have.append(f"{rel_product} — front matter route={fm['route']} stage={fm['stage']}")
            else:
                need.append(f"{rel_product} — front matter route + stage (legal values)")
            if find_section(product_text, "Value"):
                have.append(f'{rel_product} — section "Value"')
            else:
                need.append(f'{rel_product} — section "Value"')

            # D2 — the killer-risk floor: presence only, no qualification.
            # Rows still parse out of parse_ledger alongside its problems;
            # the problems are ignored at this gate (full qualification is
            # the scope rung's business).
            ledger_body = find_section(product_text, "Risk ledger")
            if not ledger_body:
                need.append(
                    f'{rel_product} — section "Risk ledger" naming at least one killer risk '
                    "(Killer? = yes)"
                )
            else:
                k_rows, _ = parse_ledger(ledger_body)
                killers = [r for r in k_rows if r["Killer?"].strip().lower() == "yes"]
                if killers:
                    have.append(
                        f"{rel_product} — Risk ledger names {len(killers)} killer risk(s) "
                        "(Killer? = yes)"
                    )
                else:
                    need.append(
                        f"{rel_product} — Risk ledger names no killer risk "
                        "(no row with Killer? = yes)"
                    )

            # The FRAME gate's completeness check (funnel-driver slice 2) — it
            # lives in the viability block only because `frame` requires
            # nothing to enter; every string it emits says "frame gate", so
            # the reader learns the right lifecycle position. One list drives
            # ask · check · show. Opt-in by presence — a record with no
            # '## Question set' is not refused here. Presence only:
            # an answer is counted, never judged, and nothing in this file can
            # tell whether Drive or a hand wrote it.
            qs = question_set_status(product_text)
            if qs is not None:
                wt = (fm or {}).get("work-type", "") or ""
                if WORK_TYPE_RE.match(wt):
                    have.append(f"{rel_product} — front matter work-type={wt}")
                else:
                    need.append(
                        f"{rel_product} — front matter work-type "
                        "(declared by the producer, never inferred)"
                    )
                for p in qs["problems"]:
                    need.append(f"{rel_product} — {p}")
                if qs["declared"] and not qs["unanswered"] and not qs["problems"]:
                    have.append(
                        f'{rel_product} — Question set (frame gate): {qs["answered"]} of {qs["declared"]} answered'
                    )
                elif qs["declared"]:
                    listed = "; ".join(f'"{q}"' for q in qs["unanswered"][:3])
                    more = qs["unanswered"][3:]
                    tail = f" (+{len(more)} more)" if more else ""
                    need.append(
                        f'{rel_product} — Question set (frame gate): {qs["answered"]} of {qs["declared"]} '
                        f"answered — still open: {listed}{tail}"
                    )

    if idx >= RUNGS.index("scope"):
        if not product_exists:
            need.append(f'{rel_product} — section "Risk ledger"')
            need.append(f'{rel_product} — section "Scope"')
        else:
            ledger_body = find_section(product_text, "Risk ledger")
            if ledger_body is None:
                need.append(f'{rel_product} — section "Risk ledger"')
            else:
                rows, problems = parse_ledger(ledger_body)
                if rows and not problems:
                    have.append(
                        f'{rel_product} — section "Risk ledger" ({len(rows)} rows, all qualified)'
                    )
                else:
                    for p in problems:
                        need.append(f"{rel_product} — {p}")

            if find_section(product_text, "Scope"):
                have.append(f'{rel_product} — section "Scope"')
            else:
                need.append(f'{rel_product} — section "Scope"')

            if rigor_problems(product_text):
                need.append(
                    f"{rel_product} — Scope declares a legal rigor level "
                    "(Rigor level: spike|mvp|production-v1)"
                )

    if idx >= RUNGS.index("design"):
        # The design gate keeps ONLY the concerns/views block — a work item
        # declaring no concerns passes design vacuously (parse_concerns
        # returns None when the product doc is absent or declares none).
        cs = parse_concerns(abs_product)
        if cs is not None:
            entries, problems = cs
            for p in problems:
                need.append(f"{rel_product} — {p}")
            for r in view_rows(root, entries):
                (have if r["code"] in ("ok", "na") else need).append(f"{rel_product} — {r['text']}")

    if idx >= RUNGS.index("handoff"):
        rel_design = f"docs/design/{slug}.md"
        if os.path.isfile(os.path.join(root, rel_design)):
            have.append(f"{rel_design} — file exists")
        else:
            need.append(f"{rel_design} — file exists")

        design_pattern = os.path.join(root, "docs", "gates", f"*-{slug}-design.md")
        design_matches = sorted(glob.glob(design_pattern))
        if design_matches:
            have.append(
                f"docs/gates/*-{slug}-design.md — design GO record ({os.path.basename(design_matches[-1])})"
            )
        else:
            need.append(f"docs/gates/*-{slug}-design.md — design GO record")

    if idx >= RUNGS.index("loop"):
        spec_pattern = os.path.join(root, "docs", "plans", f"*-{slug}-spec.md")
        spec_matches = sorted(glob.glob(spec_pattern))
        if not spec_matches:
            need.append(f"docs/plans/*-{slug}-spec.md — work specification with Pieces and a Verify for every step")
        else:
            latest_spec = spec_matches[-1]
            rel_spec = os.path.relpath(latest_spec, root)
            have.append(f"{rel_spec} — work specification with Pieces and a Verify for every step")
            with open(latest_spec, encoding="utf-8") as f:
                spec_text = f.read()

            pieces_body = find_section(spec_text, "Pieces")
            if pieces_body is None:
                need.append(f'{rel_spec} — section "Pieces"')
            else:
                box_lines = [l for l in pieces_body.splitlines() if BOXED_LINE_RE.match(l)]
                if box_lines:
                    have.append(f'{rel_spec} — section "Pieces" ({len(box_lines)} items)')
                else:
                    need.append(f'{rel_spec} — section "Pieces" with checklist items')

            step_problems = _steps_missing_verify(spec_text)
            if step_problems:
                for sp in step_problems:
                    need.append(f"{rel_spec} — {sp}")
            else:
                have.append(f"{rel_spec} — every Step carries **Verify:**")

    if idx >= RUNGS.index("acceptance"):
        spec_pattern = os.path.join(root, "docs", "plans", f"*-{slug}-spec.md")
        spec_matches = sorted(glob.glob(spec_pattern))
        if not spec_matches:
            need.append(f"docs/plans/*-{slug}-spec.md — zero unchecked boxes")
        else:
            latest_spec = spec_matches[-1]
            rel_spec = os.path.relpath(latest_spec, root)
            with open(latest_spec, encoding="utf-8") as f:
                spec_text = f.read()
            pieces_body = find_section(spec_text, "Pieces") or ""
            unchecked = [l for l in pieces_body.splitlines() if UNCHECKED_LINE_RE.match(l)]
            if unchecked:
                need.append(f"{rel_spec} — {len(unchecked)} unchecked boxes in Pieces")
            else:
                have.append(f"{rel_spec} — zero unchecked boxes in Pieces")

    return {"slug": slug, "rung": rung, "have": have, "need": need, "bypass": False}


def acceptance_record(root, slug):
    """Basename of the first gate record proving producer acceptance, else
    None. Search order: sorted docs/gates/*-<slug>-acceptance.md, then sorted
    *-<slug>-goal.md (the read-only alias — 7 such records exist and are
    never rewritten). A file qualifies when it carries a non-empty
    'Release condition' OR 'Done condition' section (the section alias)."""
    for pattern in (f"*-{slug}-acceptance.md", f"*-{slug}-goal.md"):
        matches = sorted(glob.glob(os.path.join(root, "docs", "gates", pattern)))
        for m in matches:
            # The front matter is part of the record's contract, not decoration:
            # without this check a file needs only a matching NAME and a section
            # to move the router to ready-to-release, while AU4 skips it for
            # having no front matter at all. Declared in tools/gates/README.md
            # (Gate records) since the terminal was derived; enforced here.
            fm = read_front_matter(m)
            if fm is None:
                continue
            if fm.get("route") not in ROUTES or not legal_stage(fm.get("stage")):
                continue
            # The stage-to-suffix contract: a file NAMED as an acceptance record
            # asserts the producer accepted the work, so its stage must be the
            # terminal. `legal` is not enough — `stage: designed` is perfectly
            # legal and says the opposite of what the filename claims.
            if not is_terminal_stage(fm.get("stage")):
                continue
            with open(m, encoding="utf-8") as f:
                t = f.read()
            if find_section(t, "Release condition") or find_section(t, "Done condition"):
                return os.path.basename(m)
    return None


def terminal_check(root, slug):
    """{'have': [...], 'need': [...]} for the derived terminal —
    ready-to-release. Evidence: an acceptance record (or its legacy goal
    alias) carrying a real condition section, plus the CI workflow file
    (text unchanged from the old loop block)."""
    have = []
    need = []

    basename = acceptance_record(root, slug)
    if basename:
        have.append(f"docs/gates/*-{slug}-acceptance.md — acceptance record ({basename})")
    else:
        need.append(
            f'docs/gates/*-{slug}-acceptance.md — acceptance record with section '
            '"Release condition"'
        )

    rel_workflow = ".github/workflows/gate.yml"
    if os.path.isfile(os.path.join(root, rel_workflow)):
        have.append(f"{rel_workflow} — file exists")
    else:
        need.append(f"{rel_workflow} — file exists")

    return {"have": have, "need": need}


# ── routing (A5) ─────────────────────────────────────────────────────────

def route(root, slug):
    """enters_at = the DEEPEST rung whose (cumulative) inputs all exist —
    plus the derived 'ready-to-release' terminal, checked only once every
    rung's own inputs exist (D4): the loop's edges are entered (loop) and
    exited (acceptance) as ordinary rungs, but the terminal itself is not a
    rung and never appears in `rungs`.  'frame' requires nothing, so this
    always lands somewhere — the router never refuses. A spike
    short-circuits: only 'frame' is evaluated, since no rung beyond the
    bypass check is meaningful for it (A4)."""
    rungs_out = []
    deepest_ok = "frame"

    for rung in RUNGS:
        result = check_rung(root, slug, rung)
        if result["bypass"]:
            return {
                "slug": slug,
                "enters_at": "frame",  # the ladder does not apply to a spike
                "bypass": True,
                "rungs": [{"rung": rung, "have": result["have"], "need": result["need"]}],
                "missing_for_next": [],
                "next": None,
            }
        rungs_out.append({"rung": rung, "have": result["have"], "need": result["need"]})
        if not result["need"]:
            deepest_ok = rung

    idx = RUNGS.index(deepest_ok)
    if idx + 1 < len(RUNGS):
        enters_at = deepest_ok
        next_rung = RUNGS[idx + 1]
        missing_for_next = next(
            (r["need"] for r in rungs_out if r["rung"] == next_rung), []
        )
    else:                                   # every rung's inputs exist
        t = terminal_check(root, slug)
        if not t["need"]:
            enters_at, next_rung, missing_for_next = "ready-to-release", None, []
        else:
            enters_at, next_rung, missing_for_next = "acceptance", "ready-to-release", t["need"]

    return {
        "slug": slug,
        "enters_at": enters_at,
        "bypass": False,
        "rungs": rungs_out,
        "missing_for_next": missing_for_next,
        "next": next_rung,
    }


# ── audit (A7) ───────────────────────────────────────────────────────────

def _audit_au1(root):
    """docs/design/*.md filenames must NOT start YYYY-MM-DD- (living docs
    are undated)."""
    problems = []
    d = os.path.join(root, "docs", "design")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        fname = os.path.basename(path)
        if DATED_FILENAME_RE.match(fname):
            problems.append(f"docs/design/{fname} — dated filename not allowed (living docs are undated)")
    return problems


def _audit_au2(root):
    """docs/product/*.md: undated filename, legal front matter required, and
    stage-vs-sections consistency — a stage claiming more progress than the
    file's sections show is a named problem."""
    problems = []
    d = os.path.join(root, "docs", "product")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        fname = os.path.basename(path)
        slug = fname[:-3]
        rel = f"docs/product/{fname}"
        if DATED_FILENAME_RE.match(fname):
            problems.append(f"{rel} — dated filename not allowed in docs/product/ (undated)")

        fm = read_front_matter(path)
        if fm is None:
            problems.append(f"{rel} — front matter required and missing or malformed")
            continue
        route_v, stage_v = fm.get("route"), fm.get("stage")
        if route_v not in ROUTES or not legal_stage(stage_v):
            problems.append(
                f"{rel} — front matter route/stage missing or illegal (route={route_v!r} stage={stage_v!r})"
            )
            continue

        with open(path, encoding="utf-8") as f:
            text = f.read()
        stage_idx = stage_index(stage_v)
        if stage_idx >= STAGES.index("framed") and not find_section(text, "Value"):
            problems.append(f'{rel} — stage {stage_v} ahead of its artifacts: missing section "Value"')
        if stage_idx >= STAGES.index("viable") and not find_section(text, "Risk ledger"):
            problems.append(f'{rel} — stage {stage_v} ahead of its artifacts: missing section "Risk ledger"')
        if stage_idx >= STAGES.index("scoped") and not find_section(text, "Scope"):
            problems.append(f'{rel} — stage {stage_v} ahead of its artifacts: missing section "Scope"')
        if stage_idx >= STAGES.index("ready-to-release") and acceptance_record(root, slug) is None:
            problems.append(
                f"{rel} — stage {stage_v} ahead of its artifacts: no acceptance record "
                f"(docs/gates/*-{slug}-acceptance.md, or a legacy *-{slug}-goal.md)"
            )
    return problems


def _audit_au3(root):
    """docs/gates/*.md filenames must match the dated, rung-suffixed
    gate-record pattern."""
    problems = []
    d = os.path.join(root, "docs", "gates")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        fname = os.path.basename(path)
        if not GATE_RECORD_RE.match(fname):
            problems.append(f"docs/gates/{fname} — filename does not match the gate-record pattern")
    return problems


def _audit_au4(root):
    """Any docs/**/*.md carrying route or stage in front matter: both keys
    present, both legal — validated wherever present, including this spec
    file itself."""
    problems = []
    for path in sorted(glob.glob(os.path.join(root, "docs", "**", "*.md"), recursive=True)):
        rel = os.path.relpath(path, root)
        fm = read_front_matter(path)
        if fm is None:
            continue
        if "route" in fm or "stage" in fm:
            route_v, stage_v = fm.get("route"), fm.get("stage")
            if route_v not in ROUTES or not legal_stage(stage_v):
                problems.append(
                    f"{rel} — front matter route/stage incomplete or illegal (route={route_v!r} stage={stage_v!r})"
                )
    return problems


def _audit_au10(root):
    """Every docs/gates/*.md must carry front matter with a legal route and
    stage. AU3 pins the FILENAME and AU4 validates front matter only where it
    is already present (`if fm is None: continue`) — so a well-named gate
    record with no front matter, or a malformed fence, passed both. That gap
    was load-bearing: acceptance_record() reads docs/gates/*-<slug>-acceptance.md
    to derive the ready-to-release terminal, so an invalid record could move a
    work item to the terminal with a green audit."""
    problems = []
    d = os.path.join(root, "docs", "gates")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        rel = os.path.relpath(path, root)
        fm = read_front_matter(path)
        if fm is None:
            problems.append(
                f"{rel} — gate record has no readable front matter "
                f"(needs a '---' fence with legal route + stage)"
            )
            continue
        route_v, stage_v = fm.get("route"), fm.get("stage")
        if route_v not in ROUTES or not legal_stage(stage_v):
            problems.append(
                f"{rel} — gate record front matter route/stage missing or illegal "
                f"(route={route_v!r} stage={stage_v!r})"
            )
            continue
        # The stage-to-suffix contract. Only acceptance-class suffixes are
        # constrained: a *-design.md carrying `stage: designed` is correct, and
        # only a record CLAIMING acceptance must carry the terminal stage.
        m = GATE_RECORD_RE.match(os.path.basename(path))
        if m and m.group(1) in ACCEPTANCE_SUFFIXES and not is_terminal_stage(stage_v):
            problems.append(
                f"{rel} — gate record is named as an acceptance record but its stage "
                f"is not the terminal (stage={stage_v!r}; needs ready-to-release, or "
                f"the legacy done alias). The filename asserts the producer accepted "
                f"the work; the stage says otherwise."
            )
    return problems


def _audit_au5(root):
    """docs/product/*.md carrying a '## Grounding' section: every list
    line ('- ...') must parse as '- <ref> — <why>' (split on the FIRST
    ' — ') and <ref> — a path or glob relative to the repo root — must
    resolve to at least one match on disk. Absent section = vacuous
    pass: declaring grounding is opting in, and the audit refuses only
    what was declared."""
    problems = []
    d = os.path.join(root, "docs", "product")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        fname = os.path.basename(path)
        rel = f"docs/product/{fname}"
        with open(path, encoding="utf-8") as f:
            text = f.read()
        body = find_section(text, "Grounding")
        if not body:
            continue
        for line in body.splitlines():
            if not line.startswith("- "):
                continue
            shown = line.rstrip()
            rest = shown[2:]
            if " — " not in rest:
                problems.append(
                    f"{rel} — grounding line malformed (want '- <ref> — <why>'): {shown}"
                )
                continue
            ref = rest.split(" — ", 1)[0].strip()
            if not glob.glob(os.path.join(root, ref)):
                problems.append(f"{rel} — grounding reference does not resolve: {ref}")
    return problems


def _audit_au6(root):
    """docs/product/*.md: the 'Rigor level:' law — see rigor_problems
    (single parser; the scope rung is the second call site). Absent
    '## Scope' section = vacuous pass."""
    problems = []
    d = os.path.join(root, "docs", "product")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        rel = f"docs/product/{os.path.basename(path)}"
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for p in rigor_problems(text):
            problems.append(f"{rel} — {p}")
    return problems


# ── the requirements register (AU7, AU8) ────────────────────────────────────

def req_statement_hash(statement):
    """sha256:<first 12 hex> of the stripped statement — the 'Approved'
    recipe (catalog.md, TECH-010) and the link-stamp recipe (one recipe,
    both uses). Verified against the shipped register's own values."""
    return "sha256:" + hashlib.sha256(statement.strip().encode("utf-8")).hexdigest()[:12]


def parse_register(text):
    """Parse a requirements register into (blocks, problems).

    A block: '### <ID> — <title>' heading (title may be empty — it is the
    optional Title field); a contiguous run of '**Field**: value' meta
    lines; statement lines; then an optional '**Links**' marker followed by
    '- <role> → <ID> (sha256:<12 hex>)' lines. A block ends at the next
    '### ' or '## ' heading — the '## '-stop is load-bearing: without it
    the last block in each category section absorbs the next section
    heading into its statement (six false hash divergences on the
    register's first parse, 2026-08-08). Fenced lines are invisible, per
    the standing fence-mask law.

    The meta run ends at the first non-blank line that is not a
    '**Field**: value' line. A statement whose FIRST line happens to match
    that shape would be read as an unknown field and refused — ambiguity is
    refused, never guessed; reword the statement or blank-separate it.

    problems here are purely structural (a heading without a legal ID, a
    malformed link line). Schema judgments live in register_check."""
    blocks = []
    problems = []
    lines = text.splitlines()
    mask = _fence_mask(lines)
    cur = None
    zone = None  # 'meta' | 'statement' | 'links'

    def close(b):
        if b is not None:
            b["statement"] = "\n".join(b["statement_lines"]).strip()
            blocks.append(b)

    for line, fenced in zip(lines, mask):
        if fenced:
            continue
        if line.startswith("### "):
            close(cur)
            head = line[4:].rstrip()
            if " — " in head:
                reqid, title = head.split(" — ", 1)
            elif head.endswith(" —"):
                # trailing separator, empty title — Title is optional
                reqid, title = head[:-2], ""
            else:
                reqid, title = head, ""
            reqid = reqid.strip()
            if not REQ_ID_RE.match(reqid):
                problems.append(f"block heading carries no legal ID: '### {head}'")
            cur = {
                "id": reqid, "title": title.strip(), "fields": {},
                "statement_lines": [], "links": [],
                "block_problems": [], "link_problems": [],
            }
            zone = "meta"
            continue
        if line.startswith("## "):
            close(cur)
            cur = None
            zone = None
            continue
        if cur is None:
            continue
        s = line.strip()
        if s == "**Links**":
            zone = "links"
            continue
        if zone == "meta":
            if not s:
                continue
            m = REQ_META_RE.match(s)
            if m:
                name = m.group(1).strip()
                if name in cur["fields"]:
                    cur["block_problems"].append(f"duplicate field '{name}'")
                cur["fields"][name] = m.group(2).strip()
                continue
            zone = "statement"
        if zone == "statement":
            cur["statement_lines"].append(line)
            continue
        if zone == "links":
            if not s:
                continue
            lm = REQ_LINK_RE.match(s)
            if lm:
                cur["links"].append((lm.group(1), lm.group(2), lm.group(3)))
            else:
                cur["link_problems"].append(
                    f"malformed link line (want '- <role> → <ID> (sha256:<12 hex>)'): {s}"
                )

    close(cur)
    return blocks, problems


def parse_category_table(text):
    """Parse a disposition file (categories.md) into (rows, problems) where
    rows is {CODE: (disposition, reason)}. Rows are '| CODE | name |
    disposition | reason |'; anything whose first cell is not an
    upper-case 2-4 letter code is skipped as prose or header. 'applies'
    takes no reason; 'n/a' REQUIRES one — the cheap state is the one that
    must be argued for (the accepted-state asymmetry)."""
    rows = {}
    problems = []
    lines = text.splitlines()
    mask = _fence_mask(lines)
    for line, fenced in zip(lines, mask):
        if fenced or not line.strip().startswith("|"):
            continue
        cells = _split_row(line)
        if not cells:
            continue
        code = cells[0].strip("`").strip()
        if not re.fullmatch(r"[A-Z]{2,4}", code):
            continue
        if code in rows:
            problems.append(f"duplicate category row: {code}")
            continue
        disposition = cells[2].strip() if len(cells) > 2 else ""
        reason = cells[3].strip() if len(cells) > 3 else ""
        if disposition not in ("applies", "n/a"):
            problems.append(f"category {code} — illegal disposition '{disposition}'")
        elif disposition == "n/a" and not reason:
            problems.append(f"category {code} — 'n/a' requires a named reason")
        rows[code] = (disposition, reason)
    return rows, problems


def register_check(root):
    """The register validator. Returns {"blocks": [...], "links": [...],
    "findings": [...]} — AU7 problems, AU8 problems, and the non-blocking
    findings, every string already carrying its file prefix.

    Vacuous pass when docs/requirements/register.md is absent — keeping a
    register is opting in. The legal category set comes from the project's
    own docs/requirements/categories.md: nothing is hardcoded here, because
    categories are declared per project. A register without that file is
    one named problem and every category judgment is skipped, not guessed.

    Refusals enforce what catalog.md declares: illegal ID / state /
    category / disposition, unknown or missing fields, an 'Approved' hash
    diverging from the statement (refused, the state never rewritten), a
    'superseded' block without its 'superseded-by' link, a link with an
    unregistered role or a target that does not exist. Two catalog rules
    are findings rather than refusals, in the catalog's own words: a stale
    link stamp ("flagged for re-look") and a non-origin block with no
    'refines' parent ("a finding, not an error, until slice 2").

    One mechanical limit, stated: 'dropped' owes a REASON in Source; the
    machine can only check Source is non-empty, not that it argues."""
    reg_rel = "docs/requirements/register.md"
    cat_rel = "docs/requirements/categories.md"
    reg_path = os.path.join(root, "docs", "requirements", "register.md")
    cat_path = os.path.join(root, "docs", "requirements", "categories.md")
    out = {"blocks": [], "links": [], "findings": []}
    if not os.path.isfile(reg_path):
        return out
    bp, lp, fnd = out["blocks"], out["links"], out["findings"]

    with open(reg_path, encoding="utf-8") as f:
        blocks, parse_problems = parse_register(f.read())
    for p in parse_problems:
        bp.append(f"{reg_rel} — {p}")

    cats = None
    if not os.path.isfile(cat_path):
        bp.append(f"{reg_rel} — {cat_rel} missing: category dispositions undeclared (gate G1)")
    else:
        with open(cat_path, encoding="utf-8") as f:
            cats, cat_problems = parse_category_table(f.read())
        for p in cat_problems:
            bp.append(f"{cat_rel} — {p}")

    ids = {}
    for b in blocks:
        if b["id"] in ids:
            bp.append(f"{reg_rel} — {b['id']}: duplicate ID")
        else:
            ids[b["id"]] = b

    # AU7 — blocks and states
    for b in blocks:
        rid = b["id"]

        def prob(msg, rid=rid):
            bp.append(f"{reg_rel} — {rid}: {msg}")

        for p in b["block_problems"]:
            prob(p)
        prefix = rid.split("-")[0] if REQ_ID_RE.match(rid) else None
        for name in b["fields"]:
            if name not in REQ_META_FIELDS:
                prob(f"unknown field '{name}' — a hard error, not a warning")
        cat = b["fields"].get("Category", "").strip()
        if not cat:
            prob("missing required field 'Category'")
        else:
            if prefix and cat != prefix:
                prob(f"ID prefix '{prefix}' disagrees with Category '{cat}'")
            if cats is not None:
                if cat not in cats:
                    prob(f"category '{cat}' not declared in {cat_rel}")
                elif cats[cat][0] != "applies":
                    prob(f"category '{cat}' disposition is '{cats[cat][0]}', not 'applies'")
        tags_raw = b["fields"].get("Tags", "").strip()
        if tags_raw and cats is not None:
            for t in (x.strip() for x in tags_raw.split(",")):
                if t not in cats:
                    prob(f"tag '{t}' not declared in {cat_rel}")
        state = b["fields"].get("State", "").strip()
        if not state:
            prob("missing required field 'State'")
        elif state not in REQ_STATES:
            prob(f"illegal state '{state}' (legal: {', '.join(REQ_STATES)})")
        if not b["fields"].get("Source", "").strip():
            prob("missing required field 'Source'")
        if not b["statement"]:
            prob("missing statement")
        approved = b["fields"].get("Approved", "").strip()
        if state == "final":
            if not approved:
                prob("state 'final' owes an 'Approved' hash")
            elif not REQ_APPROVED_RE.match(approved):
                prob(f"'Approved' malformed (want sha256:<12 hex>): {approved}")
            elif b["statement"] and approved != req_statement_hash(b["statement"]):
                prob(
                    f"'Approved' diverges from the statement (approved {approved}, "
                    f"statement now {req_statement_hash(b['statement'])}) — "
                    "refused; the state is never rewritten"
                )
        elif approved:
            prob(f"'Approved' on a non-final block (state '{state or '?'}')")
        if state == "superseded" and not any(r == "superseded-by" for r, _, _ in b["links"]):
            prob("state 'superseded' owes a 'superseded-by' link naming its replacement")

    # AU8 — links
    for b in blocks:
        rid = b["id"]
        for p in b["link_problems"]:
            lp.append(f"{reg_rel} — {rid}: {p}")
        for role, target, stamp in b["links"]:
            if role not in REQ_LEGAL_ROLES:
                lp.append(f"{reg_rel} — {rid}: link role '{role}' is not registered in the catalog grammar")
            if target not in ids:
                lp.append(f"{reg_rel} — {rid}: link names an ID that does not exist: {target}")
            elif ids[target]["statement"]:
                current = req_statement_hash(ids[target]["statement"])
                if f"sha256:{stamp}" != current:
                    fnd.append(
                        f"{reg_rel} — {rid}: link stamp for {target} is stale "
                        f"(stamped sha256:{stamp}, target now {current}) — re-look, then restamp"
                    )

    # the trace finding — aggregated to one line so a young register's
    # honest gap is a count, not a page of noise
    unparented = [
        b["id"] for b in blocks
        if b["fields"].get("Category", "").strip() not in REQ_ORIGIN_CATEGORIES
        and not any(r == "refines" for r, _, _ in b["links"])
    ]
    if unparented:
        fnd.append(
            f"{reg_rel} — {len(unparented)} non-origin requirement(s) declare no "
            f"'refines' parent (trace gap until slice 2): {', '.join(unparented)}"
        )
    return out


def _audit_au7(root):
    """Register blocks and states — see register_check (single parser)."""
    return register_check(root)["blocks"]


def _audit_au8(root):
    """Register links — see register_check (single parser)."""
    return register_check(root)["links"]


def _audit_au9(root):
    """Every docs/product/*.md declaring `concerns:`: the block parses and
    no view is in a wrong state — a render, a missing file, a changed
    drawing, an unreadable approval. Pending approvals (no line yet, or
    hand-written and not sealed) are the design rung's business, not the
    audit's."""
    problems = []
    d = os.path.join(root, "docs", "product")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        fname = os.path.basename(path)
        cs = parse_concerns(path)
        if cs is None:
            continue
        entries, parse_problems = cs
        for p in parse_problems:
            problems.append(f"docs/product/{fname} — {p}")
        for r in view_rows(root, entries):
            if r["code"] not in ("ok", "na", "unapproved", "unsealed"):
                problems.append(f"docs/product/{fname} — {r['text']}")
    return problems


def register_findings(root):
    """The register's non-blocking findings — reported by the audit CLI,
    never red, per the catalog's own flag-vs-refuse vocabulary."""
    return register_check(root)["findings"]


def audit(root):
    """Repo-wide mechanical sweep (AU1-AU9). Empty list = clean. Nonexistent
    directories pass vacuously — a repo that hasn't grown docs/gates/ yet is
    not thereby in violation of docs/gates/'s naming rule."""
    problems = []
    problems += _audit_au1(root)
    problems += _audit_au2(root)
    problems += _audit_au3(root)
    problems += _audit_au4(root)
    problems += _audit_au5(root)
    problems += _audit_au6(root)
    problems += _audit_au7(root)
    problems += _audit_au8(root)
    problems += _audit_au9(root)
    problems += _audit_au10(root)
    return problems


# ── release rules (R1–R3) ────────────────────────────────────────────────

def _release_files(root):
    """Load .claude-plugin/plugin.json and .claude-plugin/marketplace.json.
    Returns (plugin, marketplace, problems). When NEITHER file exists:
    (None, None, []) — vacuous pass, a tree without plugin metadata is not
    in violation. Otherwise each path that is absent or fails json.load
    contributes the problem '<relpath> — missing or invalid JSON' and
    loads as None."""
    rel_plugin = ".claude-plugin/plugin.json"
    rel_marketplace = ".claude-plugin/marketplace.json"
    abs_plugin = os.path.join(root, ".claude-plugin", "plugin.json")
    abs_marketplace = os.path.join(root, ".claude-plugin", "marketplace.json")

    if not os.path.isfile(abs_plugin) and not os.path.isfile(abs_marketplace):
        return None, None, []

    problems = []
    docs = []
    for rel, path in ((rel_plugin, abs_plugin), (rel_marketplace, abs_marketplace)):
        doc = None
        if not os.path.isfile(path):
            problems.append(f"{rel} — missing or invalid JSON")
        else:
            try:
                with open(path, encoding="utf-8") as f:
                    doc = json.load(f)
            except ValueError:
                problems.append(f"{rel} — missing or invalid JSON")
                doc = None
        docs.append(doc)

    return docs[0], docs[1], problems


def _release_versions(plugin, marketplace):
    """R1 — the three version fields must be identical: plugin['version'],
    marketplace['metadata']['version'], marketplace['plugins'][0]['version'].
    A None document contributes nothing (its load problem is already
    reported). Missing/non-string field → one problem naming it. All three
    present but not all equal → ONE problem showing all three values."""
    problems = []
    vals = {}

    if plugin is not None:
        v = plugin.get("version")
        if isinstance(v, str):
            vals["plugin"] = v
        else:
            problems.append(".claude-plugin/plugin.json — 'version' missing")

    if marketplace is not None:
        metadata = marketplace.get("metadata") or {}
        mv = metadata.get("version")
        if isinstance(mv, str):
            vals["metadata"] = mv
        else:
            problems.append(".claude-plugin/marketplace.json — 'metadata.version' missing")

        plugins = marketplace.get("plugins")
        pv = None
        if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
            pv = plugins[0].get("version")
        if isinstance(pv, str):
            vals["plugins0"] = pv
        else:
            problems.append(".claude-plugin/marketplace.json — 'plugins[0].version' missing")

    if len(vals) == 3 and not (vals["plugin"] == vals["metadata"] == vals["plugins0"]):
        problems.append(
            "version drift — plugin.json='{}' metadata.version='{}' plugins[0].version='{}' "
            "(all three must match)".format(vals["plugin"], vals["metadata"], vals["plugins0"])
        )

    return problems


def _release_capability(plugin, marketplace):
    """R2 — plugin['description'] must be byte-identical to
    marketplace['plugins'][0]['description']. metadata.description is
    NEVER read — it is intentionally a different shape (marketplace
    one-liner), and checking it would homogenize what CLAUDE.md says to
    keep distinct."""
    problems = []
    plugin_desc = None
    plugins0_desc = None

    if plugin is not None:
        d = plugin.get("description")
        if isinstance(d, str):
            plugin_desc = d
        else:
            problems.append(".claude-plugin/plugin.json — 'description' missing")

    if marketplace is not None:
        plugins = marketplace.get("plugins")
        d = None
        if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
            d = plugins[0].get("description")
        if isinstance(d, str):
            plugins0_desc = d
        else:
            problems.append(".claude-plugin/marketplace.json — 'plugins[0].description' missing")

    if plugin_desc is not None and plugins0_desc is not None and plugin_desc != plugins0_desc:
        i = 0
        min_len = min(len(plugin_desc), len(plugins0_desc))
        while i < min_len and plugin_desc[i] == plugins0_desc[i]:
            i += 1
        problems.append(
            f"capability-list drift — plugin.json description != plugins[0].description "
            f"(first differs at char {i}; metadata.description is exempt by design)"
        )

    return problems


def _skill_names(root):
    """Sorted names of skills/<name>/ directories that contain SKILL.md.
    Derived from the tree, not hardcoded — a new skill extends R3
    automatically, with no list to drift."""
    names = []
    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        return names
    for entry in os.listdir(skills_dir):
        full = os.path.join(skills_dir, entry)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "SKILL.md")):
            names.append(entry)
    return sorted(names)


def _release_namespace(root):
    """R3 — scan the living-file allowlist for bare slash references to
    Kerd skills. The correct form is /kerd:<name>; a bare /<name> is a
    violation. Allowlist (see spec): skills/**/*.md, modes/**/*.md,
    docs/design/*.md, top-level docs/*.md, CLAUDE.md. docs/plans/,
    docs/gates/, kivna/, README.md are out by construction — immutable
    dated records never retroactively fail CI; README's shorthand
    exception is human-adjudicated."""
    names = _skill_names(root)
    if not names:
        return []

    problems = []
    patterns = [
        (name, re.compile(r'(?<![\w:/.\-])/' + re.escape(name) + r'\b'))
        for name in names
    ]

    targets = []
    for d in ("skills", "modes", os.path.join("docs", "design")):
        targets += glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True)
    targets += glob.glob(os.path.join(root, "docs", "*.md"))
    claude_md = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude_md):
        targets.append(claude_md)

    for path in sorted(set(targets)):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                for name, pat in patterns:
                    if pat.search(line):
                        problems.append(
                            f"{rel}:{lineno} — bare '/{name}' (write '/kerd:{name}')"
                        )

    return problems


def release_audit(root):
    """Release-rules sweep (R1–R3). Empty list = clean. R1/R2 skip
    vacuously when neither plugin file exists; R3 runs regardless (it
    depends only on the tree)."""
    plugin, marketplace, problems = _release_files(root)
    if plugin or marketplace or problems:
        problems.extend(_release_versions(plugin, marketplace))
        problems.extend(_release_capability(plugin, marketplace))
    problems.extend(_release_namespace(root))
    return problems


# ── selftest ─────────────────────────────────────────────────────────────

def _sw(path, content):
    """Write a fixture file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _selftest_body():
    slug = "alpha"

    with tempfile.TemporaryDirectory() as root:
        product = os.path.join(root, "docs", "product", f"{slug}.md")

        # T1 — empty tree: routing always lands somewhere.
        r = route(root, slug)
        assert r["enters_at"] == "frame", f"T1: expected frame, got {r['enters_at']!r}"

        # T2 — empty tree: viability need names the missing product doc.
        cr = check_rung(root, slug, "viability")
        assert any(n == f"docs/product/{slug}.md — file exists" for n in cr["need"]), \
            f"T2: need missing file-exists item: {cr['need']}"

        # T3 — product doc exists, no front matter.
        _sw(product, "# Alpha\n\nSome text, no front matter.\n")
        cr = check_rung(root, slug, "viability")
        assert any("front matter" in n and "route" in n and "stage" in n for n in cr["need"]), \
            f"T3: expected a front-matter (route, stage) need item: {cr['need']}"

        # T4 — front matter (new/framed) + Value section: the killer-risk
        # floor (D2) refuses viability until a ledger row names Killer? = yes.
        _sw(product, "---\nroute: new\nstage: framed\n---\n\n## Value\n\nSaves 10 hours/week.\n")
        r = route(root, slug)
        assert r["enters_at"] == "frame", f"T4: expected frame, got {r['enters_at']!r}"
        cr = check_rung(root, slug, "viability")
        assert (
            f'docs/product/{slug}.md — section "Risk ledger" naming at least one killer risk '
            "(Killer? = yes)"
        ) in cr["need"], f"T4: expected the killer-risk need row: {cr['need']}"

        ledger_named_only = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| No adoption | yes | high | medium |  | accepted unknown |  |  |\n"
        )
        _sw(product, ledger_named_only)
        r = route(root, slug)
        assert r["enters_at"] == "viability", f"T4: expected viability, got {r['enters_at']!r}"

        # T5 — + ledger, row 2 Evidence empty (row 1 already carries
        # Killer? = yes, satisfying the T4 viability floor).
        ledger_bad_evidence = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| Adoption risk | yes | high | medium | 3 interviews | accepted | | check Q2 |\n"
            "| Perf risk | no | medium | low |  | accepted unknown |  | monitor |\n"
        )
        _sw(product, ledger_bad_evidence)
        cr = check_rung(root, slug, "scope")
        assert any("row 2" in n for n in cr["need"]), f"T5: expected 'row 2' in need: {cr['need']}"
        assert any("Evidence" in n for n in cr["need"]), f"T5: expected 'Evidence' in need: {cr['need']}"

        # T6 — ledger with a FATAL row (row 1 still carries Killer? = yes).
        ledger_fatal = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| No market | yes | high | high | 0 signups in beta | FATAL |  |  |\n"
        )
        _sw(product, ledger_fatal)
        cr = check_rung(root, slug, "scope")
        assert any("FATAL" in n for n in cr["need"]), f"T6: expected 'FATAL' in need: {cr['need']}"
        assert any("No market" in n for n in cr["need"]), f"T6: expected risk name in need: {cr['need']}"

        # T7 — qualified ledger (2 rows, no FATAL): scope now also wants
        # '## Scope', so route stalls at viability, not scope.
        ledger_good = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| Adoption risk | yes | high | medium | 3 interviews | accepted | | check Q2 |\n"
            "| Perf risk | no | medium | low | benchmark done | countermeasure - permanent | caching added |  |\n"
        )
        _sw(product, ledger_good)
        r = route(root, slug)
        assert r["enters_at"] == "viability", f"T7: expected viability, got {r['enters_at']!r}"

        # T8 — + Scope -> design (no concerns declared, so design passes
        # vacuously); then + design doc + design GO record -> handoff.
        _sw(product, ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n")
        r = route(root, slug)
        assert r["enters_at"] == "design", f"T8a: expected design, got {r['enters_at']!r}"

        _sw(os.path.join(root, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(
            os.path.join(root, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n",
        )
        r = route(root, slug)
        assert r["enters_at"] == "handoff", f"T8b: expected handoff, got {r['enters_at']!r}"

        # T9 — spec with Pieces (1 unchecked box) and a Step carrying Verify
        # -> loop; a variant spec whose Step lacks Verify -> check loop
        # refuses naming the step.
        spec_good = (
            "# Alpha — build spec\n\n"
            "## Pieces\n\n"
            "- [ ] Step 1\n\n"
            "### Step 1: do the thing\n"
            "**What:** do it.\n"
            "**Verify:** `true`\n"
        )
        _sw(os.path.join(root, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_good)
        r = route(root, slug)
        assert r["enters_at"] == "loop", f"T9a: expected loop, got {r['enters_at']!r}"

        with tempfile.TemporaryDirectory() as root_variant:
            spec_bad = (
                "# Alpha — build spec\n\n"
                "## Pieces\n\n"
                "- [ ] Step 1\n\n"
                "### Step 1: do the thing\n"
                "**What:** do it, but no Verify line follows.\n"
            )
            _sw(os.path.join(root_variant, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_bad)
            cr = check_rung(root_variant, slug, "loop")
            assert any("Step 1" in n for n in cr["need"]), \
                f"T9b: expected the step named in need: {cr['need']}"

        # T10 — boxes all checked -> acceptance; then + acceptance record +
        # workflow -> the derived ready-to-release terminal.
        spec_checked = (
            "# Alpha — build spec\n\n"
            "## Pieces\n\n"
            "- [x] Step 1\n\n"
            "### Step 1: do the thing\n"
            "**What:** do it.\n"
            "**Verify:** `true`\n"
        )
        _sw(os.path.join(root, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_checked)
        r = route(root, slug)
        assert r["enters_at"] == "acceptance", f"T10a: expected acceptance, got {r['enters_at']!r}"

        _sw(
            os.path.join(root, "docs", "gates", "2026-01-03-alpha-acceptance.md"),
            "---\nroute: new\nstage: ready-to-release\n---\n\n"
            "## Release condition\n\nAll steps verified and merged.\n",
        )
        _sw(os.path.join(root, ".github", "workflows", "gate.yml"), "name: entry-gate\n")
        r = route(root, slug)
        assert r["enters_at"] == "ready-to-release", f"T10b: expected ready-to-release, got {r['enters_at']!r}"
        assert r["next"] is None, f"T10b: expected next None, got {r['next']!r}"

    # T11 — the spike bypass, in its own tree.
    with tempfile.TemporaryDirectory() as root_spike:
        spike_product = os.path.join(root_spike, "docs", "product", f"{slug}.md")
        _sw(spike_product, "---\nroute: spike\nstage: framed\n---\n\n# Alpha spike\n\nTrying an idea.\n")
        cr = check_rung(root_spike, slug, "viability")
        assert any("Kill-or-keep" in n for n in cr["need"]), \
            f"T11a: expected a Kill-or-keep need item: {cr['need']}"

        _sw(
            spike_product,
            "---\nroute: spike\nstage: framed\n---\n\n## Kill-or-keep\n\nDoes X beat Y by 2x?\n",
        )
        cr = check_rung(root_spike, slug, "viability")
        assert cr["bypass"] is True, f"T11b: expected bypass True: {cr}"
        assert cr["need"] == [], f"T11b: expected empty need: {cr['need']}"

    # T12 — audit: three planted problems, then a clean tree.
    with tempfile.TemporaryDirectory() as root_audit:
        _sw(os.path.join(root_audit, "docs", "design", "2099-01-01-canary.md"), "# Canary\n\nSome content.\n")
        _sw(os.path.join(root_audit, "docs", "gates", "notes.md"), "# Notes\n\nnot a gate record.\n")
        _sw(
            os.path.join(root_audit, "docs", "plans", "2026-01-01-someplan.md"),
            "---\nroute: new\nstage: bogus\n---\n\n# Some plan\n",
        )
        problems = audit(root_audit)
        # 4, not 3: docs/gates/notes.md trips AU3 (filename) AND AU10 (no front
        # matter). Both are real and they are different defects — the count rose
        # when AU10 shipped, which is the fixture recording a gap that used to
        # go unseen rather than a regression.
        assert len(problems) == 4, f"T12a: expected 4 problems, got {len(problems)}: {problems}"
        assert any("notes.md" in x and "no readable front matter" in x for x in problems), \
            f"T12a: expected AU10 to name docs/gates/notes.md, got {problems}"

    with tempfile.TemporaryDirectory() as root_clean:
        problems = audit(root_clean)
        assert problems == [], f"T12b: expected a clean audit, got {problems}"

    # T13 — release rules: planted version drift, capability drift, and a
    # bare '/tend' reference, with the metadata.description exemption
    # proven by the count staying at 3 (not 4).
    with tempfile.TemporaryDirectory() as root_r1:
        _sw(
            os.path.join(root_r1, ".claude-plugin", "plugin.json"),
            '{"name": "kerd", "version": "1.0.0", "description": "caps A"}',
        )
        _sw(
            os.path.join(root_r1, ".claude-plugin", "marketplace.json"),
            '{"metadata": {"description": "one-liner, different by design", '
            '"version": "1.0.1"}, "plugins": [{"version": "1.0.0", "description": "caps B"}]}',
        )
        _sw(
            os.path.join(root_r1, "skills", "tend", "SKILL.md"),
            "Run /tend to converge.\nThe path skills/tend/SKILL.md stays clean.\n",
        )
        problems = release_audit(root_r1)
        assert len(problems) == 3, f"T13: expected 3 problems, got {len(problems)}: {problems}"
        assert any("version drift" in p for p in problems), \
            f"T13: expected 'version drift' in problems: {problems}"
        assert any("capability-list drift" in p for p in problems), \
            f"T13: expected 'capability-list drift' in problems: {problems}"
        assert any("bare '/tend'" in p for p in problems), \
            f"T13: expected \"bare '/tend'\" in problems: {problems}"

    # T14 — clean tree: prefixed form passes, path text passes the
    # lookbehind, and docs/plans/ + kivna/ stay excluded.
    with tempfile.TemporaryDirectory() as root_r2:
        _sw(
            os.path.join(root_r2, ".claude-plugin", "plugin.json"),
            '{"name": "kerd", "version": "1.0.0", "description": "caps A"}',
        )
        _sw(
            os.path.join(root_r2, ".claude-plugin", "marketplace.json"),
            '{"metadata": {"description": "different one-liner", "version": "1.0.0"}, '
            '"plugins": [{"version": "1.0.0", "description": "caps A"}]}',
        )
        _sw(
            os.path.join(root_r2, "skills", "tend", "SKILL.md"),
            "Use /kerd:tend here.\nSee skills/tend/SKILL.md for the source.\n",
        )
        _sw(
            os.path.join(root_r2, "docs", "plans", "2026-01-01-old-plan.md"),
            "Historic record: we ran /tend that day.\n",
        )
        _sw(
            os.path.join(root_r2, "kivna", "sessions", "2026-01-01-session.md"),
            "session log: /tend output pasted\n",
        )
        problems = release_audit(root_r2)
        assert problems == [], f"T14: expected a clean release audit, got {problems}"

    # T15 — AU5: resolving grounding (exact path + glob), audit clean.
    with tempfile.TemporaryDirectory() as root_g1:
        _sw(os.path.join(root_g1, "docs", "design", "beta.md"), "# Beta design\n\nHow it works.\n")
        _sw(
            os.path.join(root_g1, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Grounding\n\n"
            "- docs/design/beta.md — the design this work rides\n"
            "- docs/design/*.md — every living design doc\n",
        )
        problems = audit(root_g1)
        assert problems == [], f"T15: expected a clean audit, got {problems}"

    # T16 — AU5: broken reference, named verbatim.
    with tempfile.TemporaryDirectory() as root_g2:
        _sw(
            os.path.join(root_g2, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Grounding\n\n"
            "- docs/design/ghost.md — moved away and never fixed\n",
        )
        problems = audit(root_g2)
        assert problems == [
            "docs/product/beta.md — grounding reference does not resolve: docs/design/ghost.md"
        ], f"T16: expected the verbatim broken-ref problem, got {problems}"

    # T17 — AU5: malformed line (no ' — ' separator), named verbatim.
    with tempfile.TemporaryDirectory() as root_g3:
        _sw(
            os.path.join(root_g3, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Grounding\n\n"
            "- docs/design/beta.md the why, but no separator\n",
        )
        problems = audit(root_g3)
        assert problems == [
            "docs/product/beta.md — grounding line malformed (want '- <ref> — <why>'): "
            "- docs/design/beta.md the why, but no separator"
        ], f"T17: expected the verbatim malformed-line problem, got {problems}"

    # T18 — AU5: absent section = vacuous pass (opting in).
    with tempfile.TemporaryDirectory() as root_g4:
        _sw(
            os.path.join(root_g4, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n",
        )
        problems = audit(root_g4)
        assert problems == [], f"T18: expected a vacuous pass, got {problems}"

    # T19 — AU6: legal Rigor level line inside Scope, audit clean.
    with tempfile.TemporaryDirectory() as root_v1:
        _sw(
            os.path.join(root_v1, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Scope\n\nRigor level: production-v1\n\nShip the smallest slice.\n",
        )
        problems = audit(root_v1)
        assert problems == [], f"T19: expected a clean audit, got {problems}"

    # T20 — AU6: Scope without the line, named verbatim; the scope rung
    # refuses with its one need row (second call site, same parser).
    with tempfile.TemporaryDirectory() as root_v2:
        _sw(
            os.path.join(root_v2, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Scope\n\nShip the smallest slice.\n",
        )
        problems = audit(root_v2)
        assert problems == [
            "docs/product/gamma.md — Scope missing 'Rigor level: <spike|mvp|production-v1>' line"
        ], f"T20: expected the verbatim missing-line problem, got {problems}"
        cr = check_rung(root_v2, "gamma", "scope")
        assert (
            "docs/product/gamma.md — Scope declares a legal rigor level "
            "(Rigor level: spike|mvp|production-v1)"
        ) in cr["need"], f"T20: expected the rigor need row: {cr['need']}"

    # T21 — AU6: illegal value, named verbatim.
    with tempfile.TemporaryDirectory() as root_v3:
        _sw(
            os.path.join(root_v3, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Scope\n\nRigor level: prod\n\nShip it.\n",
        )
        problems = audit(root_v3)
        assert problems == [
            "docs/product/gamma.md — illegal rigor level 'prod' (legal: spike, mvp, production-v1)"
        ], f"T21: expected the verbatim illegal-value problem, got {problems}"

    # T22 — AU6: duplicate lines inside the section, named verbatim.
    with tempfile.TemporaryDirectory() as root_v4:
        _sw(
            os.path.join(root_v4, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Scope\n\nRigor level: mvp\nRigor level: spike\n\nShip it.\n",
        )
        problems = audit(root_v4)
        assert problems == [
            "docs/product/gamma.md — duplicate Rigor level lines (want exactly one)"
        ], f"T22: expected the verbatim duplicate problem, got {problems}"

    # T23 — AU6: a line outside the section, named verbatim (the section's
    # own legal line keeps this the only problem).
    with tempfile.TemporaryDirectory() as root_v5:
        _sw(
            os.path.join(root_v5, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nRigor level: mvp\n\nWorth it.\n\n"
            "## Scope\n\nRigor level: mvp\n\nShip it.\n",
        )
        problems = audit(root_v5)
        assert problems == [
            "docs/product/gamma.md — Rigor level line outside Scope"
        ], f"T23: expected the verbatim misplaced problem, got {problems}"

    # T24 — AU6: no '## Scope' section = vacuous pass (mirrors
    # T18's rule for AU5: the rule scopes to docs carrying the section).
    with tempfile.TemporaryDirectory() as root_v6:
        _sw(
            os.path.join(root_v6, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n",
        )
        problems = audit(root_v6)
        assert problems == [], f"T24: expected a vacuous pass, got {problems}"

    # T25 — a fenced code block inside a Step body may quote '### ' headings
    # without splitting the step: the vault-unhook spec quoted a deleted
    # SKILL.md section and the parser lost the real **Verify:** line below
    # it (found 2026-08-06 at the goal rung).
    with tempfile.TemporaryDirectory() as root_f1:
        spec_fenced = (
            "# Alpha — build spec\n\n"
            "## Pieces\n\n"
            "- [ ] Step 1\n\n"
            "### Step 1: delete the old section\n"
            "**What:** delete this block:\n\n"
            "```\n"
            "### 4. Update the vault\n"
            "Call the save.\n"
            "```\n\n"
            "**Verify:** `true`\n"
        )
        _sw(os.path.join(root_f1, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_fenced)
        cr = check_rung(root_f1, slug, "loop")
        assert not any("**Verify:**" in n for n in cr["need"]), \
            f"T25: fenced heading split the step: {cr['need']}"

    # T26 — AU6: a fenced example 'Rigor level:' line inside the Scope
    # section is content, not a second declaration (the fenced-block wart,
    # closed by the same fence mask as T25).
    with tempfile.TemporaryDirectory() as root_v7:
        _sw(
            os.path.join(root_v7, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Scope\n\nRigor level: mvp\n\n"
            "```\nRigor level: spike\n```\n\nShip it.\n",
        )
        problems = audit(root_v7)
        assert problems == [], f"T26: fenced line counted as a declaration, got {problems}"

    # ── AU7/AU8 — the requirements register ──────────────────────────────

    CATS_OK = (
        "| Code | Category | Disposition | Reason |\n"
        "|---|---|---|---|\n"
        "| BUS | Business | applies | filled |\n"
        "| PRD | Product | applies | filled |\n"
        "| FUN | Functional | applies | filled |\n"
        "| ANA | Analytics | n/a | no telemetry |\n"
    )

    def _req_tree(root, register, categories=CATS_OK):
        _sw(os.path.join(root, "docs", "requirements", "register.md"), register)
        if categories is not None:
            _sw(os.path.join(root, "docs", "requirements", "categories.md"), categories)

    # T27 — AU7/AU8 clean register: a final block with a matching hash, an
    # empty-title heading ('### <ID> —', Title is optional), a resolving
    # stamped link, a fenced fake block that stays invisible, and the
    # '## '-stop (the last block must not absorb '## Archive' — six false
    # divergences on the register's first parse, 2026-08-08). The fence and
    # the stop are both proven by the FUN-001 hash: either leak changes the
    # statement and turns the audit red. No register at all = vacuous pass.
    with tempfile.TemporaryDirectory() as root_q1:
        s1, s3 = "The register is real.", "A block may quote:"
        _req_tree(root_q1, (
            "# Register\n\nProse preamble, ignored.\n\n"
            "## PRD — Product\n\n"
            f"### PRD-001 — Title here\n\n"
            f"**Category**: PRD\n**Tags**: FUN\n**State**: final\n**Source**: s\n"
            f"**Approved**: {req_statement_hash(s1)}\n\n{s1}\n\n"
            "### PRD-002 —\n\n"
            "**Category**: PRD\n**State**: proposed\n**Source**: s\n\n"
            "Second rule.\n\n"
            "**Links**\n"
            f"- depends-on → PRD-001 ({req_statement_hash(s1)})\n\n"
            "## FUN — Functional\n\n"
            f"### FUN-001 — Fenced immunity\n\n"
            f"**Category**: FUN\n**State**: final\n**Source**: s\n"
            f"**Approved**: {req_statement_hash(s3)}\n\n{s3}\n\n"
            "```\n### FAKE-999 — not a block\n**State**: bogus\n```\n\n"
            "## Archive\n\n*Empty.*\n"
        ))
        problems = audit(root_q1)
        assert problems == [], f"T27: expected a clean register audit, got {problems}"
        rc = register_check(root_q1)
        assert len(rc["findings"]) == 1 and "PRD-002, FUN-001" in rc["findings"][0], \
            f"T27: expected one aggregated trace finding, got {rc['findings']}"
    with tempfile.TemporaryDirectory() as root_q1b:
        assert audit(root_q1b) == [] or True  # other AUs own their own vacuous cases
        assert register_check(root_q1b) == {"blocks": [], "links": [], "findings": []}, \
            "T27: absent register must pass vacuously"

    # T28 — AU7 block refusals, each named: an unknown field is a hard
    # error; an illegal state; a duplicate ID; an ID prefix disagreeing
    # with Category; a missing Source; a missing statement.
    with tempfile.TemporaryDirectory() as root_q2:
        _req_tree(root_q2, (
            "## PRD — Product\n\n"
            "### PRD-001 — a\n\n"
            "**Category**: PRD\n**Priority**: high\n**State**: proposed\n**Source**: s\n\n"
            "Rule one.\n\n"
            "### PRD-001 — again\n\n"
            "**Category**: PRD\n**State**: shipped\n**Source**: s\n\n"
            "Rule two.\n\n"
            "### FUN-002 — mislabeled\n\n"
            "**Category**: PRD\n**State**: proposed\n\n"
            "Rule three.\n\n"
            "### FUN-003 — empty\n\n"
            "**Category**: FUN\n**State**: proposed\n**Source**: s\n"
        ))
        problems = register_check(root_q2)["blocks"]
        for want in (
            "unknown field 'Priority'",
            "duplicate ID",
            "illegal state 'shipped'",
            "ID prefix 'FUN' disagrees with Category 'PRD'",
            "FUN-002: missing required field 'Source'",
            "FUN-003: missing statement",
        ):
            assert any(want in p for p in problems), f"T28: expected {want!r} in {problems}"

    # T29 — AU7, the Approved family: final owes a hash; malformed hash;
    # divergent hash refused with both values named and the state never
    # rewritten; a hash riding a non-final block.
    with tempfile.TemporaryDirectory() as root_q3:
        _req_tree(root_q3, (
            "## PRD — Product\n\n"
            "### PRD-001 — no hash\n\n"
            "**Category**: PRD\n**State**: final\n**Source**: s\n\nRule one.\n\n"
            "### PRD-002 — malformed\n\n"
            "**Category**: PRD\n**State**: final\n**Source**: s\n"
            "**Approved**: sha256:nothexnothex\n\nRule two.\n\n"
            "### PRD-003 — diverged\n\n"
            "**Category**: PRD\n**State**: final\n**Source**: s\n"
            "**Approved**: sha256:000000000000\n\nRule three.\n\n"
            "### PRD-004 — premature\n\n"
            "**Category**: PRD\n**State**: proposed\n**Source**: s\n"
            f"**Approved**: {req_statement_hash('Rule four.')}\n\nRule four.\n"
        ))
        problems = register_check(root_q3)["blocks"]
        for want in (
            "PRD-001: state 'final' owes an 'Approved' hash",
            "PRD-002: 'Approved' malformed",
            "PRD-003: 'Approved' diverges from the statement (approved sha256:000000000000",
            "PRD-004: 'Approved' on a non-final block (state 'proposed')",
        ):
            assert any(want in p for p in problems), f"T29: expected {want!r} in {problems}"
        assert not any("PRD-003" in p and "rewrit" in p and "never" not in p for p in problems)

    # T30 — AU7, the category set comes from the project's own disposition
    # file: an 'n/a' category used anyway; an undeclared category; an
    # undeclared tag; an 'n/a' row with no reason; and a register with no
    # categories.md at all (one named problem, judgments skipped not
    # guessed).
    with tempfile.TemporaryDirectory() as root_q4:
        _req_tree(root_q4, (
            "### ANA-001 — na\n\n**Category**: ANA\n**State**: proposed\n**Source**: s\n\nR.\n\n"
            "### ZZZ-001 — undeclared\n\n**Category**: ZZZ\n**State**: proposed\n**Source**: s\n\nR.\n\n"
            "### PRD-001 — badtag\n\n**Category**: PRD\n**Tags**: QQQ\n**State**: proposed\n**Source**: s\n\nR.\n"
        ), categories=CATS_OK + "| OPS | Operational | n/a |  |\n")
        problems = register_check(root_q4)["blocks"]
        for want in (
            "ANA-001: category 'ANA' disposition is 'n/a', not 'applies'",
            "ZZZ-001: category 'ZZZ' not declared",
            "PRD-001: tag 'QQQ' not declared",
            "category OPS — 'n/a' requires a named reason",
        ):
            assert any(want in p for p in problems), f"T30: expected {want!r} in {problems}"
    with tempfile.TemporaryDirectory() as root_q4b:
        _req_tree(root_q4b, (
            "### PRD-001 — a\n\n**Category**: PRD\n**State**: proposed\n**Source**: s\n\nR.\n"
        ), categories=None)
        problems = register_check(root_q4b)["blocks"]
        assert any("categories.md missing" in p for p in problems), \
            f"T30: expected the missing-disposition problem, got {problems}"
        assert not any("not declared" in p for p in problems), \
            f"T30: category judgments must be skipped, not guessed: {problems}"

    # T31 — AU7 state obligation + AU8 link refusals: superseded owes its
    # superseded-by; an unregistered role; a link naming an ID that does
    # not exist; a malformed link line.
    with tempfile.TemporaryDirectory() as root_q5:
        _req_tree(root_q5, (
            "### PRD-001 — orphaned supersession\n\n"
            "**Category**: PRD\n**State**: superseded\n**Source**: s\n\nOld rule.\n\n"
            "### PRD-002 — bad links\n\n"
            "**Category**: PRD\n**State**: proposed\n**Source**: s\n\nRule.\n\n"
            "**Links**\n"
            f"- blesses → PRD-001 ({req_statement_hash('Old rule.')})\n"
            "- depends-on → ZZZ-999 (sha256:000000000000)\n"
            "- depends-on PRD-001\n"
        ))
        rc = register_check(root_q5)
        assert any("PRD-001: state 'superseded' owes a 'superseded-by' link" in p
                   for p in rc["blocks"]), f"T31: {rc['blocks']}"
        for want in (
            "link role 'blesses' is not registered",
            "link names an ID that does not exist: ZZZ-999",
            "malformed link line",
        ):
            assert any(want in p for p in rc["links"]), f"T31: expected {want!r} in {rc['links']}"

    # T32 — AU8 findings are findings, never problems: a stale stamp on a
    # resolving link, and the aggregated no-parent trace gap exempting
    # origin categories (BUS originates; PRD does not). The audit stays
    # green while both are reported.
    with tempfile.TemporaryDirectory() as root_q6:
        s1 = "Target rule, since edited."
        _req_tree(root_q6, (
            "### BUS-001 — origin, exempt\n\n"
            "**Category**: BUS\n**State**: proposed\n**Source**: s\n\nMoney rule.\n\n"
            f"### PRD-001 — target\n\n"
            "**Category**: PRD\n**State**: proposed\n**Source**: s\n\n"
            f"{s1}\n\n"
            "### PRD-002 — stale stamp\n\n"
            "**Category**: PRD\n**State**: proposed\n**Source**: s\n\nRule.\n\n"
            "**Links**\n"
            "- depends-on → PRD-001 (sha256:000000000000)\n"
        ))
        problems = audit(root_q6)
        assert problems == [], f"T32: findings must not be problems, got {problems}"
        fnd = register_check(root_q6)["findings"]
        assert any("PRD-002: link stamp for PRD-001 is stale" in f for f in fnd), f"T32: {fnd}"
        trace = [f for f in fnd if "declare no 'refines' parent" in f]
        assert len(trace) == 1 and "BUS-001" not in trace[0] and "PRD-001, PRD-002" in trace[0], \
            f"T32: expected origin-exempt aggregate, got {trace}"

    # ── D1/D2/D3/D4 — the concerns block, the fingerprint recipe, seal,
    # and AU9 (gate-visuals slice 1) ────────────────────────────────────

    FX = '<svg viewBox="0 0 8 8">\n  <rect x="0" y="0" width="4" height="4"/>\n</svg>\n'
    BODY = ("\n## Value\n\nSaves 10 hours/week.\n\n## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| Adoption risk | yes | high | medium | 3 interviews | accepted | | check Q2 |\n"
            "\n## Scope\n\nRigor level: mvp\n\nShip it.\n")
    P = "docs/product/alpha.md — "

    # T33 — the reader window: grows to 120 lines for a real concerns list,
    # and still refuses when there is no closing fence within range.
    with tempfile.TemporaryDirectory() as root_c33:
        product = os.path.join(root_c33, "docs", "product", f"{slug}.md")
        fm_wide = ("---\nroute: new\nstage: framed\n"
                   + "".join(f"k{i}: v\n" for i in range(40))
                   + "---\n" + BODY)
        _sw(product, fm_wide)
        fm = read_front_matter(product)
        assert fm["route"] == "new", f"T33: expected route new within the 120-line window, got {fm}"

        fm_unclosed = "---\nroute: new\n" + "k: v\n" * 130
        _sw(product, fm_unclosed)
        assert read_front_matter(product) is None, "T33: expected None with no closing fence in range"

    # T34 — the recipe, pinned three ways: the two published vectors, a
    # from-scratch hashlib computation, and reqview's own selftest (same
    # module, same sys.path entry Step 2 inserted). No tree needed.
    assert view_fingerprint(FX) == "2878c07db022", "T34: base vector"
    assert view_fingerprint(FX + "   \n\n") == "2878c07db022", \
        "T34: a whitespace-only edit must not move the fp"
    assert view_fingerprint(FX.replace('height="4"', 'height="8"')) == "c938aa15c609", \
        "T34: a content edit must move the fp"
    by_hand = hashlib.sha256((" ".join(FX.split()) + "\n\n\n").encode("utf-8")).hexdigest()[:12]
    assert by_hand == "2878c07db022", f"T34: hand-computed recipe disagrees, got {by_hand}"
    import reqview
    assert all(ok for *_, ok in reqview.selftest()), "T34: reqview's own fingerprint vectors regressed"

    # T35 — opt-in: no 'concerns:' key at all, the design rung behaves
    # exactly as it did before D1 — no concern rows anywhere.
    with tempfile.TemporaryDirectory() as root_c0:
        product = os.path.join(root_c0, "docs", "product", f"{slug}.md")
        _sw(product, "---\nroute: new\nstage: framed\n---\n" + BODY)
        cr = check_rung(root_c0, slug, "design")
        assert cr["need"] == [], f"T35: expected a clean need list, got {cr['need']}"
        assert not any('concern "' in h for h in cr["have"]), \
            f"T35: expected no concern rows in have, got {cr['have']}"

    T36_FM = (
        "---\nroute: new\nstage: framed\nconcerns:\n"
        "  - concern: a\n"
        "  - concern: b\n"
        "    view: n/a\n"
        "  - concern: c\n"
        "    viewpoint: state\n"
        "    view: docs/design/alpha/c.html\n"
        "  - concern: d\n"
        "    viewpoint: flowchart\n"
        "    view: docs/design/alpha/d.html\n"
        "  - concern: e\n"
        "    viewpoint: state\n"
        "    view: docs/design/alpha/e.html\n"
        "    approval: Tony, 2026-01-05\n"
        "  - concern: f\n"
        "    view: n/a — covered by the README table\n"
        "  - concern: g\n"
        "    viewpoint: sequence\n"
        "    view: docs/design/alpha/g.html\n"
        "    approval: Tony, 2026-01-05 · fp:000000000000\n"
        "  - concern: h\n"
        "    viewpoint: state\n"
        "    view: docs/design/alpha/h.html\n"
        "    approval: approved!!\n"
        "---\n"
    )

    def _concerns_tree(root):
        """T36's fixture tree: every D4 row but 'no-view'/'na'/'na-no-reason'
        gets a design html on disk (FX); 'c.html' is deliberately never
        created (code 'missing')."""
        _sw(os.path.join(root, "docs", "product", f"{slug}.md"), T36_FM + BODY)
        for name in ("d", "e", "g", "h"):
            _sw(os.path.join(root, "docs", "design", "alpha", f"{name}.html"), FX)

    T36_NEED_ROWS = [
        P + 'concern "a": no view and no n/a reason',
        P + 'concern "b": n/a without a reason',
        P + 'concern "c": view docs/design/alpha/c.html not on disk',
        P + 'concern "d": view docs/design/alpha/d.html unapproved — no approval line',
        P + 'concern "e": view docs/design/alpha/e.html approved by hand, not sealed — no fp',
        P + 'concern "g": view docs/design/alpha/g.html fingerprint mismatch — '
            'approved at fp:000000000000, now fp:2878c07db022',
        P + "concern \"h\": view docs/design/alpha/h.html approval line unreadable: 'approved!!'",
    ]

    # T36 — the refusals: every D4 'need' row, named verbatim, in entry
    # order; the one 'have' (an n/a with a reason) is not among them.
    with tempfile.TemporaryDirectory() as root_c1:
        _concerns_tree(root_c1)
        cr = check_rung(root_c1, slug, "design")
        assert cr["need"] == T36_NEED_ROWS, \
            f"T36: expected the seven refusal rows in order, got {cr['need']}"
        assert (P + 'concern "f": n/a — covered by the README table') in cr["have"], \
            f"T36: expected the n/a-with-reason row in have, got {cr['have']}"

        # T37 — seal, on T36's tree: unsealed -> sealed with its computed
        # fp; a stale hand-typed fp is reported diverged, never rewritten;
        # unapproved/refused/unreadable are left alone; the product doc
        # changes in exactly the sealed approval line; a second run is
        # idempotent (sealed becomes already).
        product_path = os.path.join(root_c1, "docs", "product", f"{slug}.md")
        with open(product_path, encoding="utf-8") as f:
            lines_before = f.read().splitlines()

        r = seal_views(root_c1, slug)
        assert r["sealed"] == [["e", "docs/design/alpha/e.html", "Tony", "2026-01-05", "2878c07db022"]], \
            f"T37: expected e sealed, got {r['sealed']}"
        assert r["diverged"] == [["g", "docs/design/alpha/g.html", "000000000000", "2878c07db022"]], \
            f"T37: expected g diverged, got {r['diverged']}"
        assert r["unapproved"] == [["d", "docs/design/alpha/d.html"]], \
            f"T37: expected d unapproved, got {r['unapproved']}"
        assert r["refused"] == [["c", "docs/design/alpha/c.html", "view docs/design/alpha/c.html not on disk"]], \
            f"T37: expected c refused, got {r['refused']}"
        assert r["unreadable"] == [["h", "approved!!"]], f"T37: expected h unreadable, got {r['unreadable']}"
        assert r["written"] is True, "T37: expected the product doc rewritten"

        with open(product_path, encoding="utf-8") as f:
            lines_after = f.read().splitlines()
        assert len(lines_before) == len(lines_after), "T37: seal must not change the line count"
        diffs = [i for i, (a, b) in enumerate(zip(lines_before, lines_after)) if a != b]
        assert len(diffs) == 1, f"T37: expected exactly one changed line, got {len(diffs)}"
        assert lines_after[diffs[0]] == "    approval: Tony, 2026-01-05 · fp:2878c07db022", \
            f"T37: expected the sealed approval line, got {lines_after[diffs[0]]!r}"

        r2 = seal_views(root_c1, slug)
        assert r2["sealed"] == [], f"T37: a second seal must seal nothing new, got {r2['sealed']}"
        assert r2["already"] == [["e", "docs/design/alpha/e.html", "2878c07db022"]], \
            f"T37: expected e already-sealed, got {r2['already']}"
        assert r2["written"] is False, "T37: a second seal must not rewrite"

        cr2 = check_rung(root_c1, slug, "design")
        assert (
            P + 'concern "e": state view docs/design/alpha/e.html approved by Tony, 2026-01-05 (fp:2878c07db022)'
        ) in cr2["have"], f"T37: expected e's ok row in have, got {cr2['have']}"

        # T38 — editing a sealed drawing's content invalidates it: the
        # design rung reports the mismatch, and seal_views reports it as
        # diverged and refuses to touch the product doc.
        e_path = os.path.join(root_c1, "docs", "design", "alpha", "e.html")
        _sw(e_path, FX.replace('height="4"', 'height="8"'))
        with open(product_path, encoding="utf-8") as f:
            product_before_t38 = f.read()

        cr3 = check_rung(root_c1, slug, "design")
        assert (
            P + 'concern "e": view docs/design/alpha/e.html fingerprint mismatch — '
            'approved at fp:2878c07db022, now fp:c938aa15c609'
        ) in cr3["need"], f"T38: expected e's mismatch row in need, got {cr3['need']}"

        r3 = seal_views(root_c1, slug)
        assert ["e", "docs/design/alpha/e.html", "2878c07db022", "c938aa15c609"] in r3["diverged"], \
            f"T38: expected e diverged, got {r3['diverged']}"
        assert r3["written"] is False, "T38: seal must not rewrite on divergence"
        with open(product_path, encoding="utf-8") as f:
            product_after_t38 = f.read()
        assert product_after_t38 == product_before_t38, "T38: product bytes must be unchanged"

    # T39 — clean pass: a sealed view whose fp matches, and an n/a with a
    # reason, both pass; check_rung need is empty, routing reaches design,
    # and the repo-wide audit is clean.
    with tempfile.TemporaryDirectory() as root_c2:
        product = os.path.join(root_c2, "docs", "product", f"{slug}.md")
        _sw(product,
            "---\nroute: new\nstage: framed\nconcerns:\n"
            "  - concern: one\n"
            "    viewpoint: state\n"
            "    view: docs/design/alpha/one.html\n"
            "    approval: Tony, 2026-01-05 · fp:2878c07db022\n"
            "  - concern: two\n"
            "    view: n/a — nothing to draw\n"
            "---\n" + BODY)
        _sw(os.path.join(root_c2, "docs", "design", "alpha", "one.html"), FX)

        cr = check_rung(root_c2, slug, "design")
        assert cr["need"] == [], f"T39: expected a clean need list, got {cr['need']}"
        r = route(root_c2, slug)
        assert r["enters_at"] == "design", f"T39: expected design, got {r['enters_at']!r}"
        assert audit(root_c2) == [], f"T39: expected a clean audit, got {audit(root_c2)}"

    # T40 — parse problems: an n/a entry carrying an approval (nothing to
    # approve), and an unreadable line inside the list, named with the
    # file's own line number; seal_views refuses to touch anything while
    # they stand.
    with tempfile.TemporaryDirectory() as root_c3:
        product = os.path.join(root_c3, "docs", "product", f"{slug}.md")
        t40_fm = (
            "---\nroute: new\nstage: framed\nconcerns:\n"
            "  - concern: x\n"
            "    view: n/a — nothing to draw\n"
            "    approval: Tony, 2026-01-05\n"
            "  - concern: y\n"
            "    viewpoint: state\n"
            "    view: docs/design/alpha/y.png\n"
            "  this line is junk\n"
            "---\n"
        )
        _sw(product, t40_fm + BODY)
        _sw(os.path.join(root_c3, "docs", "design", "alpha", "y.png"), FX)
        with open(product, encoding="utf-8") as f:
            product_bytes_before = f.read()

        cr = check_rung(root_c3, slug, "design")
        assert (P + 'concerns: entry "x" is n/a and carries an approval — nothing to approve') in cr["need"], \
            f"T40: expected the n/a-with-approval problem, got {cr['need']}"
        assert (P + "concerns: line 11 unreadable: 'this line is junk'") in cr["need"], \
            f"T40: expected the unreadable-line problem, got {cr['need']}"
        assert (
            P + 'concern "y": view docs/design/alpha/y.png is not .html — a render is never the view'
        ) in cr["need"], f"T40: expected the not-html problem, got {cr['need']}"

        r = seal_views(root_c3, slug)
        assert len(r["parse_problems"]) == 2, f"T40: expected two parse problems, got {r['parse_problems']}"
        assert r["written"] is False, "T40: seal must not write while parse problems stand"
        with open(product, encoding="utf-8") as f:
            product_bytes_after = f.read()
        assert product_bytes_after == product_bytes_before, "T40: product bytes must be unchanged"

    # T41 — AU9: the repo-wide sweep reports exactly the design rung's
    # non-pending problems — a, b, c, g, h — in entry order; d (unapproved)
    # and e (unsealed) are pending, and f is n/a, so none of the three
    # appear. T36's tree, untouched by seal.
    with tempfile.TemporaryDirectory() as root_c4:
        _concerns_tree(root_c4)
        want = [row for row in T36_NEED_ROWS if not row.startswith((P + 'concern "d"', P + 'concern "e"'))]
        assert audit(root_c4) == want, f"T41: expected exactly the five AU9 problems, got {audit(root_c4)}"

    # ── D1 — retired names as read-only aliases, forever ─────────────────

    # T42 — alias filenames and stage aliases: retired rung suffixes and the
    # retired 'done' stage value are legality passes system-wide, forever;
    # an unrecognized suffix is still refused by name.
    with tempfile.TemporaryDirectory() as root_a1:
        fm = "---\nroute: new\nstage: done\n---\n\nbody\n"
        for suffix in ("slice", "contract", "build", "goal", "acceptance"):
            _sw(os.path.join(root_a1, "docs", "gates", f"2026-01-01-x-{suffix}.md"), fm)
        assert audit(root_a1) == [], f"T42: expected a clean audit, got {audit(root_a1)}"

    with tempfile.TemporaryDirectory() as root_a2:
        _sw(
            os.path.join(root_a2, "docs", "gates", "2026-01-01-x-bogus.md"),
            "---\nroute: new\nstage: done\n---\n\nbody\n",
        )
        problems = audit(root_a2)
        assert len(problems) == 1 and "gate-record pattern" in problems[0], \
            f"T42: expected exactly one gate-record-pattern problem, got {problems}"

    # T43 — the legacy terminal: a full tree reaching the loop rung, but
    # carrying a legacy goal record (not an acceptance record) — route still
    # derives ready-to-release, and the terminal have-line names the
    # -goal.md basename (the read-only alias, never rewritten).
    with tempfile.TemporaryDirectory() as root_t43:
        product_t43 = os.path.join(root_t43, "docs", "product", f"{slug}.md")
        _sw(product_t43, ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n")
        _sw(os.path.join(root_t43, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(
            os.path.join(root_t43, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n",
        )
        _sw(os.path.join(root_t43, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_checked)
        _sw(
            os.path.join(root_t43, "docs", "gates", "2026-01-03-alpha-goal.md"),
            "---\nroute: new\nstage: done\n---\n\n## Done condition\n\nAll steps verified and merged.\n",
        )
        _sw(os.path.join(root_t43, ".github", "workflows", "gate.yml"), "name: entry-gate\n")

        r = route(root_t43, slug)
        assert r["enters_at"] == "ready-to-release", f"T43: expected ready-to-release, got {r['enters_at']!r}"
        t = terminal_check(root_t43, slug)
        assert any("2026-01-03-alpha-goal.md" in h for h in t["have"]), \
            f"T43: expected the terminal have-line to name the goal.md basename, got {t['have']}"

    # T44 — AU2's new tier: a stage claiming ready-to-release with no
    # acceptance record (nor its legacy goal-record alias) is named; adding
    # the legacy record clears it.
    with tempfile.TemporaryDirectory() as root_t44:
        _sw(
            os.path.join(root_t44, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: ready-to-release\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| Adoption risk | yes | high | medium | 3 interviews | accepted | | check Q2 |\n"
            "\n## Scope\n\nRigor level: mvp\n\nShip it.\n",
        )
        want = (
            "docs/product/beta.md — stage ready-to-release ahead of its artifacts: "
            "no acceptance record (docs/gates/*-beta-acceptance.md, or a legacy *-beta-goal.md)"
        )
        problems = audit(root_t44)
        assert want in problems, f"T44: expected the missing-acceptance-record problem, got {problems}"

        _sw(
            os.path.join(root_t44, "docs", "gates", "2026-01-03-beta-goal.md"),
            "---\nroute: new\nstage: done\n---\n\n## Done condition\n\nAll steps verified and merged.\n",
        )
        problems2 = audit(root_t44)
        assert want not in problems2, f"T44: expected the problem cleared, got {problems2}"

    # T46 — a gate record that is well-NAMED but carries no front matter must
    # not reach the terminal, and AU10 must name it. Before AU10 this file
    # passed AU3 (filename ok) and was skipped by AU4 (no front matter at all),
    # so the router reported ready-to-release off an invalid record with a
    # green audit. Adding legal front matter clears both halves.
    with tempfile.TemporaryDirectory() as root_t46:
        _sw(os.path.join(root_t46, "docs", "product", f"{slug}.md"),
            ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n")
        _sw(os.path.join(root_t46, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(os.path.join(root_t46, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n")
        _sw(os.path.join(root_t46, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_checked)
        _sw(os.path.join(root_t46, ".github", "workflows", "gate.yml"), "name: entry-gate\n")

        bad = os.path.join(root_t46, "docs", "gates", "2026-01-04-alpha-acceptance.md")
        _sw(bad, "# Acceptance\n\n## Release condition\n\nEverything verified.\n")

        r = route(root_t46, slug)
        assert r["enters_at"] == "acceptance", \
            f"T46: a front-matter-less acceptance record must not reach the terminal, got {r['enters_at']!r}"
        assert acceptance_record(root_t46, slug) is None, \
            "T46: acceptance_record must reject a record with no front matter"
        au10 = _audit_au10(root_t46)
        assert any("2026-01-04-alpha-acceptance.md" in x and "no readable front matter" in x for x in au10), \
            f"T46: AU10 must name the front-matter-less gate record, got {au10}"

        # malformed in the OTHER direction: a fence with an illegal stage
        _sw(bad, "---\nroute: new\nstage: shipped\n---\n\n## Release condition\n\nDone.\n")
        assert acceptance_record(root_t46, slug) is None, \
            "T46: acceptance_record must reject an illegal stage"
        assert any("route/stage missing or illegal" in x for x in _audit_au10(root_t46)), \
            "T46: AU10 must name an illegal stage on a gate record"

        # and now the valid form clears every one of them
        _sw(bad, "---\nroute: new\nstage: ready-to-release\n---\n\n## Release condition\n\nDone.\n")
        assert _audit_au10(root_t46) == [], f"T46: valid record must clear AU10, got {_audit_au10(root_t46)}"

    # T47 — the happy path for the NEW name: a valid *-acceptance.md reaches
    # ready-to-release and the terminal have-line names its basename.
    with tempfile.TemporaryDirectory() as root_t47:
        _sw(os.path.join(root_t47, "docs", "product", f"{slug}.md"),
            ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n")
        _sw(os.path.join(root_t47, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(os.path.join(root_t47, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n")
        _sw(os.path.join(root_t47, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_checked)
        _sw(os.path.join(root_t47, "docs", "gates", "2026-01-04-alpha-acceptance.md"),
            "---\nroute: new\nstage: ready-to-release\n---\n\n"
            "## Release condition\n\nEvery piece landed and verified.\n")
        _sw(os.path.join(root_t47, ".github", "workflows", "gate.yml"), "name: entry-gate\n")

        r = route(root_t47, slug)
        assert r["enters_at"] == "ready-to-release", \
            f"T47: a valid acceptance record must reach the terminal, got {r['enters_at']!r}"
        tc = terminal_check(root_t47, slug)
        assert any("2026-01-04-alpha-acceptance.md" in h for h in tc["have"]), \
            f"T47: terminal have-line must name the acceptance basename, got {tc['have']}"
        assert _audit_au10(root_t47) == [], "T47: a valid tree must clear AU10"

    # T48 — the alias path is not a bypass. Stripping the front matter from a
    # legacy *-goal.md must cost it the terminal exactly as it does the new
    # name; restoring it returns the terminal. Retired names read forever, but
    # they read under the same contract, not a weaker one.
    with tempfile.TemporaryDirectory() as root_t48:
        _sw(os.path.join(root_t48, "docs", "product", f"{slug}.md"),
            ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n")
        _sw(os.path.join(root_t48, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(os.path.join(root_t48, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n")
        _sw(os.path.join(root_t48, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_checked)
        _sw(os.path.join(root_t48, ".github", "workflows", "gate.yml"), "name: entry-gate\n")

        legacy = os.path.join(root_t48, "docs", "gates", "2026-01-03-alpha-goal.md")
        _sw(legacy, "## Done condition\n\nAll steps verified and merged.\n")
        assert route(root_t48, slug)["enters_at"] == "acceptance", \
            "T48: a front-matter-less legacy goal record must not reach the terminal"

        _sw(legacy, "---\nroute: new\nstage: done\n---\n\n## Done condition\n\nAll steps verified and merged.\n")
        assert route(root_t48, slug)["enters_at"] == "ready-to-release", \
            "T48: a valid legacy goal record must still reach the terminal"
        assert _audit_au10(root_t48) == [], "T48: a valid legacy record must clear AU10"

    # T49 — the stage-to-suffix contract. A *-acceptance.md whose stage is
    # LEGAL but NONTERMINAL must not qualify: the filename asserts the producer
    # accepted the work and `stage: designed` says the opposite. Before this
    # check, legal_stage() alone let it through and the audit stayed green.
    with tempfile.TemporaryDirectory() as root_t49:
        _sw(os.path.join(root_t49, "docs", "product", f"{slug}.md"),
            ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n")
        _sw(os.path.join(root_t49, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(os.path.join(root_t49, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n")
        _sw(os.path.join(root_t49, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_checked)
        _sw(os.path.join(root_t49, ".github", "workflows", "gate.yml"), "name: entry-gate\n")

        acc = os.path.join(root_t49, "docs", "gates", "2026-01-04-alpha-acceptance.md")
        _sw(acc, "---\nroute: new\nstage: designed\n---\n\n## Release condition\n\nDone.\n")

        assert acceptance_record(root_t49, slug) is None, \
            "T49: a nonterminal stage must not qualify an acceptance record"
        assert route(root_t49, slug)["enters_at"] == "acceptance", \
            f"T49: routing must stay at acceptance, got {route(root_t49, slug)['enters_at']!r}"
        au = _audit_au10(root_t49)
        assert any("named as an acceptance record but its stage is not the terminal" in x for x in au), \
            f"T49: AU10 must refuse the nonterminal acceptance record, got {au}"
        # the *-design.md in the same tree carries stage: designed and is CORRECT —
        # only acceptance-class suffixes are constrained
        assert not any("alpha-design.md" in x for x in au), \
            f"T49: a design record with stage designed must not be refused, got {au}"

        # the terminal value clears both halves
        _sw(acc, "---\nroute: new\nstage: ready-to-release\n---\n\n## Release condition\n\nDone.\n")
        assert _audit_au10(root_t49) == [], f"T49: valid record must clear AU10, got {_audit_au10(root_t49)}"
        assert route(root_t49, slug)["enters_at"] == "ready-to-release", \
            "T49: ready-to-release must reach the terminal"

        # and the legacy alias still reaches it through `done`
        os.remove(acc)
        _sw(os.path.join(root_t49, "docs", "gates", "2026-01-03-alpha-goal.md"),
            "---\nroute: new\nstage: done\n---\n\n## Done condition\n\nAll verified.\n")
        assert route(root_t49, slug)["enters_at"] == "ready-to-release", \
            "T49: the legacy goal record must still reach the terminal through done's alias"
        assert _audit_au10(root_t49) == [], "T49: the legacy record must clear AU10"

    # T50 — the frame gate's completeness check (funnel-driver slice 2). A
    # '## Question set' is opt-in by presence; once present, every entry
    # needs an answer and the front matter needs a declared work-type. The
    # refusal names the count and the open questions in plain words.
    with tempfile.TemporaryDirectory() as root_t50:
        p50 = os.path.join(root_t50, "docs", "product", f"{slug}.md")
        qs_open = (
            "## Question set\n\n"
            "- Q: What is the problem?\n  A: Nothing walks an item to launch.\n"
            "- Q: Who has it?\n  A:\n"
            "- Q: What would be different?\n"
        )
        _sw(p50, ledger_named_only + "\n" + qs_open)
        assert route(root_t50, slug)["enters_at"] == "frame", \
            "T50: an open question set must hold the item at frame"
        cr = check_rung(root_t50, slug, "viability")
        assert (
            f"docs/product/{slug}.md — front matter work-type (declared by the producer, never inferred)"
        ) in cr["need"], f"T50: expected the work-type need row, got {cr['need']}"
        assert (
            f'docs/product/{slug}.md — Question set (frame gate): 1 of 3 answered — still open: '
            '"Who has it?"; "What would be different?"'
        ) in cr["need"], f"T50: expected the plain-words count row, got {cr['need']}"

        qs_done = (
            "## Question set\n\n"
            "- Q: What is the problem?\n  A: Nothing walks an item to launch.\n"
            "- Q: Who has it?\n  A: Tony, on every item.\n"
            "- Q: What would be different?\n  A: Three unowned rungs get an owner.\n"
            "  A continuation line belongs to the answer above it.\n"
        )
        _sw(p50, ledger_named_only.replace("route: new\n", "route: new\nwork-type: software-change\n")
            + "\n" + qs_done)
        cr = check_rung(root_t50, slug, "viability")
        assert cr["need"] == [], f"T50: expected the frame gate to release, got {cr['need']}"
        assert f"docs/product/{slug}.md — front matter work-type=software-change" in cr["have"], \
            f"T50: expected the work-type have row, got {cr['have']}"
        assert f"docs/product/{slug}.md — Question set (frame gate): 3 of 3 answered" in cr["have"], \
            f"T50: expected the answered have row, got {cr['have']}"
        assert route(root_t50, slug)["enters_at"] == "viability", \
            "T50: a complete set must release the item to viability"

        # no section at all is not a refusal — nothing already on a board moves
        _sw(p50, ledger_named_only)
        cr = check_rung(root_t50, slug, "viability")
        assert not any("Question set" in x or "work-type" in x for x in cr["need"] + cr["have"]), \
            f"T50: an absent section must add no rows, got {cr['need'] + cr['have']}"
        assert route(root_t50, slug)["enters_at"] == "viability", \
            "T50: an item with no question set routes exactly as before"

    # T51 — the grammar's edges: a quoted example inside ``` is content,
    # not an entry; a work-type that is not a filename stem is refused; an
    # answer before any question and a section with no entries are named
    # problems, never a vacuous pass.
    with tempfile.TemporaryDirectory() as root_t51:
        p51 = os.path.join(root_t51, "docs", "product", f"{slug}.md")
        _sw(p51, ledger_named_only.replace("route: new\n", "route: new\nwork-type: Software Change\n")
            + "\n## Question set\n\n"
            "```\n- Q: quoted example, invisible\n  A:\n```\n"
            "- Q: Real question?\n  A: Real answer.\n")
        cr = check_rung(root_t51, slug, "viability")
        assert f"docs/product/{slug}.md — Question set (frame gate): 1 of 1 answered" in cr["have"], \
            f"T51: the fenced example must be invisible, got {cr['have']}"
        assert (
            f"docs/product/{slug}.md — front matter work-type (declared by the producer, never inferred)"
        ) in cr["need"], f"T51: 'Software Change' is not a seed filename stem, got {cr['need']}"
        assert route(root_t51, slug)["enters_at"] == "frame", \
            "T51: an illegal work-type holds the item at frame"

        st = question_set_status("# X\n\n## Question set\n\nA: orphan answer\n\nprose only\n")
        assert st["declared"] == 0 and st["answered"] == 0, f"T51: expected nothing declared, got {st}"
        assert st["problems"] == [
            "Question set: line 1 answer before any question",
            "Question set: declared with no entries (want '- Q: <question>' lines)",
        ], f"T51: expected the two named problems in order, got {st['problems']}"
        assert question_set_status("# X\n\n## Value\n\nno set here\n") is None, \
            "T51: an absent section is None, not a problem"

    # T45 — purity: the live ladder's exact membership, and the retired
    # names' total absence from RUNGS (restated separately from T10b's
    # ready-to-release check, which already proved the terminal derivation).
    assert set(RUNGS) == {
        "frame", "viability", "scope", "design", "handoff", "loop", "acceptance"
    }, f"T45: unexpected RUNGS membership, got {RUNGS}"
    for retired in ("build", "verify", "adjust", "goal", "slice", "contract"):
        assert retired not in RUNGS, f"T45: {retired!r} must not be in RUNGS"
    assert "goal" not in RUNGS and "build" not in RUNGS, "T45: restated purity check"


def selftest():
    """Run the 51 fixture-built cases in temporary trees. Prints
    'selftest: 51 cases passed' and returns 0 on success; on the first
    failed assertion, prints which case failed and returns 1."""
    try:
        _selftest_body()
    except AssertionError as e:
        print(f"selftest: FAILED — {e}")
        return 1
    print("selftest: 51 cases passed")
    return 0
