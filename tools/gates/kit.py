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
    '### ' heading or EOF, by a line starting '**Verify:**'."""
    problems = []
    lines = spec_text.splitlines()
    n = len(lines)
    i = 0
    while i < n:
        if STEP_HEADING_RE.match(lines[i]):
            title = lines[i][len("### "):].strip()
            j = i + 1
            found = False
            while j < n and not H3_RE.match(lines[j]):
                if VERIFY_LINE_RE.match(lines[j]):
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


def audit(root):
    """Repo-wide mechanical sweep (AU1-AU4). Empty list = clean. Nonexistent
    directories pass vacuously — a repo that hasn't grown docs/gates/ yet is
    not thereby in violation of docs/gates/'s naming rule."""
    problems = []
    problems += _audit_au1(root)
    problems += _audit_au2(root)
    problems += _audit_au3(root)
    problems += _audit_au4(root)
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
        _sw(product, ledger_good + "\n## Release slice\n\nShip the caching path first.\n")
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


def selftest():
    """Run the 12 fixture-built cases in temporary trees. Prints
    'selftest: 12 cases passed' and returns 0 on success; on the first
    failed assertion, prints which case failed and returns 1."""
    try:
        _selftest_body()
    except AssertionError as e:
        print(f"selftest: FAILED — {e}")
        return 1
    print("selftest: 12 cases passed")
    return 0
