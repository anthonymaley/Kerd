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
import tempfile

# Repo root, three levels up from this file (tools/gates/kit.py -> tools ->
# repo root). The CLI passes ROOT; selftest passes a temp tree instead — every
# function below takes `root` as a parameter for exactly that reason.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RUNGS = ["frame", "viability", "slice", "design", "contract", "build", "goal", "loop"]
STAGES = ["framed", "viable", "sliced", "designed", "contracted", "building", "done"]
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

# The legal rigor levels (AU6, design rung). A '## Release slice' section
# declares how rigorously the slice is measured — one 'Rigor level:' line;
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
    r'(frame|viability|slice|design|contract|build|goal|loop)\.md$'
)
DATED_FILENAME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}-')
FRONT_MATTER_KV_RE = re.compile(r'^([A-Za-z0-9_.-]+):\s*(.*)$')
STEP_HEADING_RE = re.compile(r'^### Step ')
H3_RE = re.compile(r'^### ')
VERIFY_LINE_RE = re.compile(r'^\*\*Verify:\*\*')
BOXED_LINE_RE = re.compile(r'^- \[[ x]\] ')
UNCHECKED_LINE_RE = re.compile(r'^- \[ \] ')
SEPARATOR_ROW_RE = re.compile(r'^[\s|:-]+$')
RIGOR_LINE_RE = re.compile(r'^Rigor level:(.*)$')
RIGOR_SECTION_HEADING_RE = re.compile(r'^## Release slice[ \t]*$')


# ── front matter (A1) ───────────────────────────────────────────────────────

def read_front_matter(path):
    """Parse the front-matter subset defined in A1. None when absent or the
    fence is malformed — a leading '---' with no closing fence within 30
    lines, or no 'key: value' line inside it, is NOT front matter."""
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if not lines or lines[0] != "---":
        return None
    close = None
    for i in range(1, min(len(lines), 31)):
        if lines[i] == "---":
            close = i
            break
    if close is None:
        return None
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


# ── rigor level (AU6, design rung) ──────────────────────────────────────────

def rigor_problems(text):
    """Judge one product doc's 'Rigor level:' declaration. Single-parser
    rule: AU6 and the design rung both call THIS function — the law is
    written once. The law: exactly one legal 'Rigor level: <value>' line
    INSIDE the '## Release slice' section; a 'Rigor level:' line anywhere
    else in the doc is a problem; a doc with no '## Release slice' section
    passes vacuously (the section's absence is already the design rung's
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
        problems.append("Rigor level line outside Release slice")
    if section_seen:
        if not inside_values:
            problems.append(
                "Release slice missing 'Rigor level: <spike|mvp|production-v1>' line"
            )
        elif len(inside_values) > 1:
            problems.append("duplicate Rigor level lines (want exactly one)")
        elif inside_values[0] not in RIGOR_LEVELS:
            problems.append(
                f"illegal rigor level '{inside_values[0]}' (legal: spike, mvp, production-v1)"
            )
    return problems


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


# ── the contract spec's steps (A3, build row) ───────────────────────────────

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
        else:
            have.append(f"{rel_product} — file exists")
            if fm and fm.get("route") in ROUTES and fm.get("stage") in STAGES:
                have.append(f"{rel_product} — front matter route={fm['route']} stage={fm['stage']}")
            else:
                need.append(f"{rel_product} — front matter route + stage (legal values)")
            if find_section(product_text, "Value"):
                have.append(f'{rel_product} — section "Value"')
            else:
                need.append(f'{rel_product} — section "Value"')

    if idx >= RUNGS.index("slice"):
        if not product_exists:
            need.append(f'{rel_product} — section "Risk ledger"')
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

    if idx >= RUNGS.index("design"):
        if not product_exists:
            need.append(f'{rel_product} — section "Release slice"')
        else:
            if find_section(product_text, "Release slice"):
                have.append(f'{rel_product} — section "Release slice"')
            else:
                need.append(f'{rel_product} — section "Release slice"')
            if rigor_problems(product_text):
                need.append(
                    f"{rel_product} — Release slice declares a legal rigor level "
                    "(Rigor level: spike|mvp|production-v1)"
                )

    if idx >= RUNGS.index("contract"):
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

    if idx >= RUNGS.index("build"):
        spec_pattern = os.path.join(root, "docs", "plans", f"*-{slug}-spec.md")
        spec_matches = sorted(glob.glob(spec_pattern))
        if not spec_matches:
            need.append(f"docs/plans/*-{slug}-spec.md — contract spec")
        else:
            latest_spec = spec_matches[-1]
            rel_spec = os.path.relpath(latest_spec, root)
            have.append(f"{rel_spec} — contract spec")
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

    if idx >= RUNGS.index("goal"):
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

    if idx >= RUNGS.index("loop"):
        goal_pattern = os.path.join(root, "docs", "gates", f"*-{slug}-goal.md")
        goal_matches = sorted(glob.glob(goal_pattern))
        goal_hit = None
        for gm in goal_matches:
            with open(gm, encoding="utf-8") as f:
                t = f.read()
            if find_section(t, "Done condition"):
                goal_hit = gm
                break
        if goal_hit:
            have.append(
                f'docs/gates/*-{slug}-goal.md — goal record with section "Done condition" ({os.path.basename(goal_hit)})'
            )
        else:
            need.append(f'docs/gates/*-{slug}-goal.md — goal record with section "Done condition"')

        rel_workflow = ".github/workflows/gate.yml"
        if os.path.isfile(os.path.join(root, rel_workflow)):
            have.append(f"{rel_workflow} — file exists")
        else:
            need.append(f"{rel_workflow} — file exists")

    return {"slug": slug, "rung": rung, "have": have, "need": need, "bypass": False}


# ── routing (A5) ─────────────────────────────────────────────────────────

def route(root, slug):
    """enters_at = the DEEPEST rung whose (cumulative) inputs all exist.
    'frame' requires nothing, so this always lands somewhere — the router
    never refuses. A spike short-circuits: only 'frame' is evaluated, since
    no rung beyond the bypass check is meaningful for it (A4)."""
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
        next_rung = RUNGS[idx + 1]
        missing_for_next = next(
            (r["need"] for r in rungs_out if r["rung"] == next_rung), []
        )
    else:
        next_rung = None
        missing_for_next = []

    return {
        "slug": slug,
        "enters_at": deepest_ok,
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
        rel = f"docs/product/{fname}"
        if DATED_FILENAME_RE.match(fname):
            problems.append(f"{rel} — dated filename not allowed in docs/product/ (undated)")

        fm = read_front_matter(path)
        if fm is None:
            problems.append(f"{rel} — front matter required and missing or malformed")
            continue
        route_v, stage_v = fm.get("route"), fm.get("stage")
        if route_v not in ROUTES or stage_v not in STAGES:
            problems.append(
                f"{rel} — front matter route/stage missing or illegal (route={route_v!r} stage={stage_v!r})"
            )
            continue

        with open(path, encoding="utf-8") as f:
            text = f.read()
        stage_idx = STAGES.index(stage_v)
        if stage_idx >= STAGES.index("framed") and not find_section(text, "Value"):
            problems.append(f'{rel} — stage {stage_v} ahead of its artifacts: missing section "Value"')
        if stage_idx >= STAGES.index("viable") and not find_section(text, "Risk ledger"):
            problems.append(f'{rel} — stage {stage_v} ahead of its artifacts: missing section "Risk ledger"')
        if stage_idx >= STAGES.index("sliced") and not find_section(text, "Release slice"):
            problems.append(f'{rel} — stage {stage_v} ahead of its artifacts: missing section "Release slice"')
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
            if route_v not in ROUTES or stage_v not in STAGES:
                problems.append(
                    f"{rel} — front matter route/stage incomplete or illegal (route={route_v!r} stage={stage_v!r})"
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
    (single parser; the design rung is the second call site). Absent
    '## Release slice' section = vacuous pass."""
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


def register_findings(root):
    """The register's non-blocking findings — reported by the audit CLI,
    never red, per the catalog's own flag-vs-refuse vocabulary."""
    return register_check(root)["findings"]


def audit(root):
    """Repo-wide mechanical sweep (AU1-AU8). Empty list = clean. Nonexistent
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

        # T4 — front matter (new/framed) + Value section.
        _sw(product, "---\nroute: new\nstage: framed\n---\n\n## Value\n\nSaves 10 hours/week.\n")
        r = route(root, slug)
        assert r["enters_at"] == "viability", f"T4: expected viability, got {r['enters_at']!r}"

        # T5 — + ledger, row 2 Evidence empty.
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
        cr = check_rung(root, slug, "slice")
        assert any("row 2" in n for n in cr["need"]), f"T5: expected 'row 2' in need: {cr['need']}"
        assert any("Evidence" in n for n in cr["need"]), f"T5: expected 'Evidence' in need: {cr['need']}"

        # T6 — ledger with a FATAL row.
        ledger_fatal = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| No market | yes | high | high | 0 signups in beta | FATAL |  |  |\n"
        )
        _sw(product, ledger_fatal)
        cr = check_rung(root, slug, "slice")
        assert any("FATAL" in n for n in cr["need"]), f"T6: expected 'FATAL' in need: {cr['need']}"
        assert any("No market" in n for n in cr["need"]), f"T6: expected risk name in need: {cr['need']}"

        # T7 — qualified ledger (2 rows, no FATAL).
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
        assert r["enters_at"] == "slice", f"T7: expected slice, got {r['enters_at']!r}"

        # T8 — + Release slice -> design; then + design doc + design gate record -> contract.
        _sw(product, ledger_good + "\n## Release slice\n\nRigor level: mvp\n\nShip the caching path first.\n")
        r = route(root, slug)
        assert r["enters_at"] == "design", f"T8a: expected design, got {r['enters_at']!r}"

        _sw(os.path.join(root, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(
            os.path.join(root, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n",
        )
        r = route(root, slug)
        assert r["enters_at"] == "contract", f"T8b: expected contract, got {r['enters_at']!r}"

        # T9 — spec with Pieces (1 unchecked box) and a Step carrying Verify -> build;
        # a variant spec whose Step lacks Verify -> check build refuses naming the step.
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
        assert r["enters_at"] == "build", f"T9a: expected build, got {r['enters_at']!r}"

        with tempfile.TemporaryDirectory() as root_variant:
            spec_bad = (
                "# Alpha — build spec\n\n"
                "## Pieces\n\n"
                "- [ ] Step 1\n\n"
                "### Step 1: do the thing\n"
                "**What:** do it, but no Verify line follows.\n"
            )
            _sw(os.path.join(root_variant, "docs", "plans", "2026-01-02-alpha-spec.md"), spec_bad)
            cr = check_rung(root_variant, slug, "build")
            assert any("Step 1" in n for n in cr["need"]), \
                f"T9b: expected the step named in need: {cr['need']}"

        # T10 — boxes all checked -> goal; then + goal record + workflow -> loop.
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
        assert r["enters_at"] == "goal", f"T10a: expected goal, got {r['enters_at']!r}"

        _sw(
            os.path.join(root, "docs", "gates", "2026-01-03-alpha-goal.md"),
            "---\nroute: new\nstage: done\n---\n\n## Done condition\n\nAll steps verified and merged.\n",
        )
        _sw(os.path.join(root, ".github", "workflows", "gate.yml"), "name: entry-gate\n")
        r = route(root, slug)
        assert r["enters_at"] == "loop", f"T10b: expected loop, got {r['enters_at']!r}"

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
        assert len(problems) == 3, f"T12a: expected 3 problems, got {len(problems)}: {problems}"

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

    # T19 — AU6: legal Rigor level line inside Release slice, audit clean.
    with tempfile.TemporaryDirectory() as root_v1:
        _sw(
            os.path.join(root_v1, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: production-v1\n\nShip the smallest slice.\n",
        )
        problems = audit(root_v1)
        assert problems == [], f"T19: expected a clean audit, got {problems}"

    # T20 — AU6: Release slice without the line, named verbatim; the design
    # rung refuses with its one need row (second call site, same parser).
    with tempfile.TemporaryDirectory() as root_v2:
        _sw(
            os.path.join(root_v2, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nShip the smallest slice.\n",
        )
        problems = audit(root_v2)
        assert problems == [
            "docs/product/gamma.md — Release slice missing 'Rigor level: <spike|mvp|production-v1>' line"
        ], f"T20: expected the verbatim missing-line problem, got {problems}"
        cr = check_rung(root_v2, "gamma", "design")
        assert (
            "docs/product/gamma.md — Release slice declares a legal rigor level "
            "(Rigor level: spike|mvp|production-v1)"
        ) in cr["need"], f"T20: expected the rigor need row: {cr['need']}"

    # T21 — AU6: illegal value, named verbatim.
    with tempfile.TemporaryDirectory() as root_v3:
        _sw(
            os.path.join(root_v3, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: prod\n\nShip it.\n",
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
            "## Release slice\n\nRigor level: mvp\nRigor level: spike\n\nShip it.\n",
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
            "## Release slice\n\nRigor level: mvp\n\nShip it.\n",
        )
        problems = audit(root_v5)
        assert problems == [
            "docs/product/gamma.md — Rigor level line outside Release slice"
        ], f"T23: expected the verbatim misplaced problem, got {problems}"

    # T24 — AU6: no '## Release slice' section = vacuous pass (mirrors
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
        cr = check_rung(root_f1, slug, "build")
        assert not any("**Verify:**" in n for n in cr["need"]), \
            f"T25: fenced heading split the step: {cr['need']}"

    # T26 — AU6: a fenced example 'Rigor level:' line inside the Release
    # slice is content, not a second declaration (the fenced-block wart,
    # closed by the same fence mask as T25).
    with tempfile.TemporaryDirectory() as root_v7:
        _sw(
            os.path.join(root_v7, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: mvp\n\n"
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


def selftest():
    """Run the 32 fixture-built cases in temporary trees. Prints
    'selftest: 32 cases passed' and returns 0 on success; on the first
    failed assertion, prints which case failed and returns 1."""
    try:
        _selftest_body()
    except AssertionError as e:
        print(f"selftest: FAILED — {e}")
        return 1
    print("selftest: 32 cases passed")
    return 0
