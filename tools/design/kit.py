#!/usr/bin/env python3
"""The evaluation matrix's refuser — mechanical only, per the gates
philosophy: it checks presence, legality, and arithmetic. It has no
opinion on whether a basis is convincing — judgment belongs to whoever
fills the matrix.

Stdlib only. Every function takes its inputs as parameters (root, text)
so the selftest can run in temp trees — the gates idiom. The gates
parsing idiom (find_section, _split_row, separator-row skip) is
reimplemented locally rather than imported from tools/gates/kit — the
two refusers stay uncoupled (the CI-choice rationale in the spec).
"""

import glob
import importlib.util
import json
import os
import re
import tempfile
import textwrap

# Repo root, three levels up from this file (tools/design/kit.py -> tools ->
# repo root), same formula as tools/gates/kit.py line 24.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MATRIX_HEADING_RE = re.compile(r'^## Evaluation matrix[ \t]*$', re.MULTILINE)

# M1 — the seven required sections, in file order.
SECTION_ORDER = [
    "Criteria",
    "Options",
    "Evaluation matrix",
    "Preferred solution",
    "Proposal and next steps",
    "Risks and countermeasures required",
    "Countermeasures",
]

CRITERIA_COLUMNS = ["Criterion", "Group", "Target / Minimum", "Category", "Weight"]
OPTIONS_COLUMNS = ["Option", "Description", "Architecture overview"]
COUNTERMEASURES_COLUMNS = [
    "Option", "Criterion", "Countermeasure", "Type", "Confidence", "Return condition",
]

# M4 — mark, optional score on the declared 1-5 scale with a mandatory
# em-dash-separated basis.
MARK_CELL_RE = re.compile(r'^([○△×])(?:[ \t]+([1-5])[ \t]+—[ \t]+(\S.*))?$')

OPTION_ID_RE = re.compile(r'^[A-Z][A-Za-z0-9-]*$')

SEPARATOR_ROW_RE = re.compile(r'^[\s|:-]+$')


# ── the gates parsing idiom, reimplemented locally ──────────────────────────

def find_section(text, title):
    """Body under a '## <title>' heading (exact, case-sensitive), up to the
    next '## ' heading or EOF. None = heading absent. '' = heading present
    but the body is whitespace-only."""
    heading_re = re.compile(r'^## ' + re.escape(title) + r'[ \t]*$', re.MULTILINE)
    m = heading_re.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    next_m = re.search(r'^## ', rest, re.MULTILINE)
    end = start + next_m.start() if next_m else len(text)
    return text[start:end].strip()


def _heading_start(text, title):
    """Start offset of the (first) '## <title>' heading line, or None."""
    m = re.search(r'^## ' + re.escape(title) + r'[ \t]*$', text, re.MULTILINE)
    return m.start() if m else None


def _split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def has_matrix(text):
    """MATRIX_HEADING_RE search — whether a doc opts in."""
    return bool(MATRIX_HEADING_RE.search(text))


# ── M2 — ## Criteria ─────────────────────────────────────────────────────

def _parse_criteria(section_text, rel):
    """(criteria, problems). criteria: list of
    {"name","group","target","category","weight"} (weight: int or None)."""
    problems = []
    criteria = []
    lines = [l for l in section_text.splitlines() if l.strip()]
    if not lines:
        problems.append(f"{rel} — Criteria: no table")
        return criteria, problems

    header = _split_row(lines[0])
    if header != CRITERIA_COLUMNS:
        problems.append(f"{rel} — Criteria header must be exactly: " + " | ".join(CRITERIA_COLUMNS))
        return criteria, problems

    body_lines = lines[1:]
    if body_lines and SEPARATOR_ROW_RE.match(body_lines[0]):
        body_lines = body_lines[1:]
    if not body_lines:
        problems.append(f"{rel} — Criteria: no data rows")
        return criteria, problems

    names_seen = set()
    weight_empty_flags = []
    for i, line in enumerate(body_lines, start=1):
        cells = _split_row(line)
        if len(cells) != len(CRITERIA_COLUMNS):
            problems.append(f"{rel} — Criteria row {i}: expected {len(CRITERIA_COLUMNS)} columns, found {len(cells)}")
            continue
        name, group, target, category, weight_raw = cells

        if not name:
            problems.append(f"{rel} — Criteria row {i}: Criterion empty")
        elif name in names_seen:
            problems.append(f"{rel} — Criteria row {i}: Criterion '{name}' duplicated")
        else:
            names_seen.add(name)

        if not group:
            problems.append(f"{rel} — Criteria row {i}: Group empty")
        if not target:
            problems.append(f"{rel} — Criteria row {i}: Target / Minimum empty")
        if category not in ("M", "D"):
            problems.append(f"{rel} — Criteria row {i}: Category must be M or D, found '{category}'")

        weight_empty_flags.append(weight_raw == "")
        weight = None
        if weight_raw:
            if weight_raw.isdigit() and int(weight_raw) > 0:
                weight = int(weight_raw)
            else:
                problems.append(f"{rel} — Criteria row {i}: Weight must be a positive integer or empty")

        criteria.append({
            "name": name, "group": group, "target": target,
            "category": category, "weight": weight,
        })

    if weight_empty_flags and any(weight_empty_flags) and not all(weight_empty_flags):
        problems.append(
            f"{rel} — Weight: mixed across Criteria rows — either all rows empty "
            "(criteria weigh equally) or all rows positive integers"
        )

    return criteria, problems


# ── M3 — ## Options ──────────────────────────────────────────────────────

def _parse_options(section_text, rel):
    """(options, problems). options: list of {"id","description","overview"}."""
    problems = []
    options = []
    lines = [l for l in section_text.splitlines() if l.strip()]
    if not lines:
        problems.append(f"{rel} — Options: no table")
        return options, problems

    header = _split_row(lines[0])
    if header != OPTIONS_COLUMNS:
        problems.append(f"{rel} — Options header must be exactly: " + " | ".join(OPTIONS_COLUMNS))
        return options, problems

    body_lines = lines[1:]
    if body_lines and SEPARATOR_ROW_RE.match(body_lines[0]):
        body_lines = body_lines[1:]
    if len(body_lines) < 2:
        problems.append(f"{rel} — Options: at least 2 data rows required (one option is not a comparison)")

    ids_seen = set()
    for i, line in enumerate(body_lines, start=1):
        cells = _split_row(line)
        if len(cells) != len(OPTIONS_COLUMNS):
            problems.append(f"{rel} — Options row {i}: expected {len(OPTIONS_COLUMNS)} columns, found {len(cells)}")
            continue
        opt_id, desc, overview = cells

        if not OPTION_ID_RE.match(opt_id):
            problems.append(f"{rel} — Options row {i}: Option '{opt_id}' does not match ^[A-Z][A-Za-z0-9-]*$")
        elif opt_id in ids_seen:
            problems.append(f"{rel} — Options row {i}: Option '{opt_id}' duplicated")
        else:
            ids_seen.add(opt_id)

        if not desc:
            problems.append(f"{rel} — Options row {i}: Description empty")
        if not overview:
            problems.append(f"{rel} — Options row {i}: Architecture overview empty")

        options.append({"id": opt_id, "description": desc, "overview": overview})

    return options, problems


# ── M4 — ## Evaluation matrix ────────────────────────────────────────────

def _parse_evaluation_matrix(section_text, rel, criteria, options):
    """(cells, mode, problems, extra_rows). cells: {option_id: {criterion:
    {"mark","score","basis"}}}. extra_rows: {"overall": row_or_None,
    "rank": row_or_None} — the raw declared OVERALL/RANK rows, for
    _compute_arithmetic to check drift against."""
    problems = []
    option_ids = [o["id"] for o in options]
    criterion_names = [c["name"] for c in criteria]
    cells = {oid: {} for oid in option_ids}
    extra_rows = {"overall": None, "rank": None}

    lines = [l for l in section_text.splitlines() if l.strip()]
    if not lines:
        problems.append(f"{rel} — Evaluation matrix: no table")
        return cells, "marks", problems, extra_rows

    expected_header = ["Criterion"] + option_ids
    header = _split_row(lines[0])
    if header != expected_header:
        problems.append(
            f"{rel} — Evaluation matrix header must be exactly: " + " | ".join(expected_header)
        )
        return cells, "marks", problems, extra_rows

    body_lines = lines[1:]
    if body_lines and SEPARATOR_ROW_RE.match(body_lines[0]):
        body_lines = body_lines[1:]

    all_rows = [_split_row(l) for l in body_lines]

    tail_start = None
    for idx, r in enumerate(all_rows):
        if r and r[0] in ("OVERALL", "RANK"):
            tail_start = idx
            break
    if tail_start is None:
        crit_rows, tail_rows = all_rows, []
    else:
        crit_rows, tail_rows = all_rows[:tail_start], all_rows[tail_start:]

    if tail_rows:
        names = [r[0] if r else "" for r in tail_rows]
        if names != ["OVERALL", "RANK"]:
            problems.append(
                f"{rel} — Evaluation matrix: expected exactly OVERALL then RANK after "
                f"the criterion rows, found {names}"
            )
        else:
            extra_rows["overall"] = tail_rows[0]
            extra_rows["rank"] = tail_rows[1]

    row_by_name = {}
    for r in crit_rows:
        if r:
            row_by_name[r[0]] = r

    # a scored criterion tracing to no declaration
    for name in row_by_name:
        if name not in criterion_names:
            problems.append(f"{rel} — Evaluation matrix: scored criterion '{name}' has no declaration")

    # a declared criterion with no row
    for name in criterion_names:
        if name not in row_by_name:
            problems.append(f"{rel} — Evaluation matrix: declared criterion '{name}' has no row")

    has_score = False
    has_unscored = False

    for name in criterion_names:
        row = row_by_name.get(name)
        if row is None:
            continue
        if len(row) != len(expected_header):
            problems.append(
                f"{rel} — Evaluation matrix row '{name}': expected {len(expected_header)} "
                f"columns, found {len(row)}"
            )
            continue
        for idx, oid in enumerate(option_ids, start=1):
            raw = row[idx]
            m = MARK_CELL_RE.match(raw)
            if not m:
                if raw[:1] in ("○", "△", "×"):
                    problems.append(
                        f"{rel} — Evaluation matrix cell '{name}'/'{oid}': score without basis "
                        f"(found '{raw}')"
                    )
                else:
                    problems.append(f"{rel} — Evaluation matrix cell '{name}'/'{oid}': invalid mark '{raw}'")
                continue
            mark = m.group(1)
            score = int(m.group(2)) if m.group(2) else None
            basis = m.group(3)
            if score is not None:
                has_score = True
            else:
                has_unscored = True
            cells[oid][name] = {"mark": mark, "score": score, "basis": basis}

    if has_score and has_unscored:
        problems.append(
            f"{rel} — Evaluation matrix: mode mixed — every cell must be scored, or none "
            "(marks always, scores when the stakes are real)"
        )

    mode = "scored" if has_score else "marks"
    return cells, mode, problems, extra_rows


def _compute_dead(criteria, options, cells):
    """{option_id: criterion_name} for the first M-category criterion where
    that option's cell mark is ×. An option here is DEAD regardless of
    OVERALL — M7's rule, computed independent of mode."""
    dead = {}
    m_criteria = [c for c in criteria if c["category"] == "M"]
    for opt in options:
        oid = opt["id"]
        for c in m_criteria:
            cell = cells.get(oid, {}).get(c["name"])
            if cell and cell["mark"] == "×":
                dead[oid] = c["name"]
                break
    return dead


# ── M5 — arithmetic ──────────────────────────────────────────────────────

def _compute_arithmetic(rel, criteria, options, cells, mode, extra_rows):
    """(overall, rank, problems) — RECOMPUTED overall/rank in scored mode
    (empty dicts in marks mode), plus drift/shape problems against the
    declared OVERALL/RANK rows."""
    problems = []
    option_ids = [o["id"] for o in options]
    overall = {}
    rank = {}

    if mode == "marks":
        if extra_rows.get("overall") is not None or extra_rows.get("rank") is not None:
            problems.append(
                f"{rel} — Evaluation matrix: marks-only mode must not carry OVERALL/RANK rows"
            )
        return overall, rank, problems

    if mode != "scored":
        return overall, rank, problems

    weights = {c["name"]: (c["weight"] if c["weight"] is not None else 1) for c in criteria}
    for oid in option_ids:
        total = 0
        for c in criteria:
            cell = cells.get(oid, {}).get(c["name"])
            if cell and cell["score"] is not None:
                total += cell["score"] * weights[c["name"]]
        overall[oid] = total

    sorted_ids = sorted(option_ids, key=lambda o: -overall[o])
    for i, oid in enumerate(sorted_ids):
        if i == 0:
            rank[oid] = 1
        else:
            prev = sorted_ids[i - 1]
            rank[oid] = rank[prev] if overall[oid] == overall[prev] else i + 1

    overall_row = extra_rows.get("overall")
    rank_row = extra_rows.get("rank")
    if overall_row is None or rank_row is None:
        problems.append(f"{rel} — Evaluation matrix: scored mode requires OVERALL and RANK rows")
        return overall, rank, problems

    if len(overall_row) - 1 != len(option_ids):
        problems.append(f"{rel} — Evaluation matrix: OVERALL row column count mismatch")
    else:
        declared_overall = dict(zip(option_ids, overall_row[1:]))
        for oid in option_ids:
            raw = declared_overall[oid]
            try:
                dv = int(raw.strip())
            except ValueError:
                problems.append(f"{rel} — Evaluation matrix: OVERALL value for '{oid}' is not an integer ('{raw}')")
                continue
            if dv != overall[oid]:
                problems.append(
                    f"{rel} — Evaluation matrix: OVERALL drift for '{oid}' — "
                    f"declared {dv}, recomputed {overall[oid]}"
                )

    if len(rank_row) - 1 != len(option_ids):
        problems.append(f"{rel} — Evaluation matrix: RANK row column count mismatch")
    else:
        declared_rank = dict(zip(option_ids, rank_row[1:]))
        for oid in option_ids:
            raw = declared_rank[oid]
            try:
                dv = int(raw.strip())
            except ValueError:
                problems.append(f"{rel} — Evaluation matrix: RANK value for '{oid}' is not an integer ('{raw}')")
                continue
            if dv != rank[oid]:
                problems.append(
                    f"{rel} — Evaluation matrix: RANK drift for '{oid}' — "
                    f"declared {dv}, recomputed {rank[oid]}"
                )

    return overall, rank, problems


# ── M6 — ## Countermeasures ──────────────────────────────────────────────

def _parse_countermeasures(section_text, rel, triangle_set):
    """(rows, problems). Every (option_id, criterion_name) in triangle_set
    (the △ cells) requires exactly one row; a row citing a cell not in
    triangle_set is a violation. When triangle_set is empty, no table is
    required — the section body just must be non-empty."""
    problems = []
    rows_out = []
    seen = set()

    if not triangle_set:
        if not section_text.strip():
            problems.append(f"{rel} — Countermeasures: section body must be non-empty")
        return rows_out, problems

    lines = [l for l in section_text.splitlines() if l.strip()]
    if not lines:
        problems.append(f"{rel} — Countermeasures: no table but △ cells exist")
    else:
        header = _split_row(lines[0])
        if header != COUNTERMEASURES_COLUMNS:
            problems.append(
                f"{rel} — Countermeasures header must be exactly: " + " | ".join(COUNTERMEASURES_COLUMNS)
            )
        else:
            body_lines = lines[1:]
            if body_lines and SEPARATOR_ROW_RE.match(body_lines[0]):
                body_lines = body_lines[1:]
            for i, line in enumerate(body_lines, start=1):
                cells = _split_row(line)
                if len(cells) != len(COUNTERMEASURES_COLUMNS):
                    problems.append(
                        f"{rel} — Countermeasures row {i}: expected {len(COUNTERMEASURES_COLUMNS)} "
                        f"columns, found {len(cells)}"
                    )
                    continue
                opt, crit, cm, typ, conf, ret = cells

                if (opt, crit) not in triangle_set:
                    problems.append(
                        f"{rel} — Countermeasures row {i}: countermeasure cites '{opt}'/'{crit}' "
                        "which is not marked △"
                    )
                else:
                    seen.add((opt, crit))

                if not cm:
                    problems.append(f"{rel} — Countermeasures row {i}: Countermeasure empty")
                if typ not in ("permanent", "temporary"):
                    problems.append(f"{rel} — Countermeasures row {i}: Type must be permanent or temporary")
                if not conf:
                    problems.append(f"{rel} — Countermeasures row {i}: Confidence empty")
                if typ == "temporary" and not ret:
                    problems.append(
                        f"{rel} — Countermeasures row {i}: Return condition empty "
                        "(required when Type is temporary)"
                    )

                rows_out.append({
                    "option": opt, "criterion": crit, "countermeasure": cm,
                    "type": typ, "confidence": conf, "return_condition": ret,
                })

    missing = triangle_set - seen
    for (opt, crit) in sorted(missing):
        problems.append(
            f"{rel} — Countermeasures: △ cell '{opt}'/'{crit}' has no countermeasure row"
        )

    return rows_out, problems


# ── M7 — ## Preferred solution ───────────────────────────────────────────

def _parse_preferred(section_text, rel, options, dead_map):
    """(preferred_id_or_None, problems). First non-blank line must match
    '^<OptionID> — ' with a declared OptionID. A dead option (× on any
    M-category criterion) preferred is a named refusal regardless of
    OVERALL."""
    problems = []
    option_ids = {o["id"] for o in options}
    lines = [l for l in section_text.splitlines() if l.strip()]
    if not lines:
        problems.append(f"{rel} — Preferred solution: section is empty")
        return None, problems

    m = re.match(r'^(\S+) — ', lines[0])
    if not m or m.group(1) not in option_ids:
        problems.append(
            f"{rel} — Preferred solution: first line must match '<OptionID> — ...' "
            "with a declared Option"
        )
        return None, problems

    preferred = m.group(1)
    if preferred in dead_map:
        problems.append(
            f"{rel} — dead option preferred: '{preferred}' carries × on Mandatory "
            f"criterion '{dead_map[preferred]}' — a dead option cannot be preferred, "
            "regardless of OVERALL"
        )
    return preferred, problems


# ── the public parser ────────────────────────────────────────────────────

def parse_matrix(text, rel):
    """(model, problems). Implements M1-M7 except the overview-file-exists
    check (that needs `root`; see check_file). Every problem string is
    f"{rel} — <what>"."""
    problems = []

    # M1 — section order, presence, non-empty.
    positions = {}
    missing_titles = []
    for title in SECTION_ORDER:
        pos = _heading_start(text, title)
        if pos is None:
            missing_titles.append(title)
        else:
            positions[title] = pos
    if missing_titles:
        problems.append(f"{rel} — section order: missing section(s) " + ", ".join(missing_titles))
    else:
        ordered = [positions[t] for t in SECTION_ORDER]
        if ordered != sorted(ordered):
            problems.append(
                f"{rel} — section order: sections must appear in order "
                + " < ".join(f"## {t}" for t in SECTION_ORDER)
            )

    bodies = {}
    for title in SECTION_ORDER:
        body = find_section(text, title)
        bodies[title] = body
        if body is not None and not body.strip():
            problems.append(f"{rel} — section '{title}' is empty")

    criteria, p = _parse_criteria(bodies["Criteria"] or "", rel)
    problems += p

    options, p = _parse_options(bodies["Options"] or "", rel)
    problems += p

    cells, mode, p, extra_rows = _parse_evaluation_matrix(
        bodies["Evaluation matrix"] or "", rel, criteria, options
    )
    problems += p

    dead_map = _compute_dead(criteria, options, cells)

    overall, rank, p = _compute_arithmetic(rel, criteria, options, cells, mode, extra_rows)
    problems += p

    triangle_set = set()
    for oid, crit_cells in cells.items():
        for cname, cell in crit_cells.items():
            if cell["mark"] == "△":
                triangle_set.add((oid, cname))
    countermeasures, p = _parse_countermeasures(bodies["Countermeasures"] or "", rel, triangle_set)
    problems += p

    preferred, p = _parse_preferred(bodies["Preferred solution"] or "", rel, options, dead_map)
    problems += p

    # M7 — scored mode: preferred's OVERALL must be >= every other living
    # option's OVERALL (rank decides among the living). Marks-only mode:
    # preferred merely needs to be living, already covered by the dead check.
    if preferred is not None and mode == "scored" and preferred not in dead_map:
        living_ids = [o["id"] for o in options if o["id"] not in dead_map and o["id"] in overall]
        if living_ids:
            best = max(overall[o] for o in living_ids)
            if overall.get(preferred) is not None and overall[preferred] < best:
                problems.append(
                    f"{rel} — preferred option '{preferred}' does not have the highest "
                    f"OVERALL among living options (has {overall[preferred]}, best living {best})"
                )

    model = {
        "file": rel,
        "mode": mode,
        "criteria": criteria,
        "options": options,
        "cells": cells,
        "overall": overall,
        "rank": rank,
        "dead": list(dead_map.keys()),
        "preferred": preferred,
        "countermeasures": countermeasures,
    }
    return model, problems


def check_file(root, relpath):
    """problems list. Reads the file, runs parse_matrix, then the M3
    overview-exists check against root. A file without a matrix heading
    returns [f"{relpath} — no ## Evaluation matrix section"]."""
    abs_path = os.path.join(root, relpath)
    with open(abs_path, encoding="utf-8") as f:
        text = f.read()

    if not has_matrix(text):
        return [f"{relpath} — no ## Evaluation matrix section"]

    model, problems = parse_matrix(text, relpath)

    for opt in model["options"]:
        overview = opt["overview"]
        if not overview:
            continue
        if not os.path.isfile(os.path.join(root, overview)):
            problems.append(f"{relpath} — Options: architecture overview '{overview}' does not exist")

    return problems


def audit_matrices(root):
    """(problems, count) — scans sorted(glob docs/design/*.md), runs
    check_file on each file where has_matrix is true. count is the number
    of opted-in files. Absent directory or zero opt-ins -> ([], 0)."""
    d = os.path.join(root, "docs", "design")
    if not os.path.isdir(d):
        return [], 0

    problems = []
    count = 0
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if has_matrix(text):
            count += 1
            problems.extend(check_file(root, rel))
    return problems, count


# ── D8: load the diagram toolkit by path ────────────────────────────────
# tools/diagram/kit.py and tools/diagram/to_svg.py, loaded once and cached
# in module globals. This module is itself named kit.py, so a bare
# sys.path insert of tools/diagram would silently shadow one kit with the
# other — the D8 idiom (tools/diagram/progress_kit.py::load_gates_kit).

_diagram_kit = None
_diagram_to_svg = None


def _load_diagram_kit():
    """Load tools/diagram/kit.py by path. Loaded once, cached in a module
    global."""
    global _diagram_kit
    if _diagram_kit is None:
        p = os.path.join(ROOT, "tools", "diagram", "kit.py")
        spec = importlib.util.spec_from_file_location("design_diagram_kit", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _diagram_kit = m
    return _diagram_kit


def _load_diagram_to_svg():
    """Load tools/diagram/to_svg.py by path. Loaded once, cached in a
    module global."""
    global _diagram_to_svg
    if _diagram_to_svg is None:
        p = os.path.join(ROOT, "tools", "diagram", "to_svg.py")
        spec = importlib.util.spec_from_file_location("design_diagram_to_svg", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _diagram_to_svg = m
    return _diagram_to_svg


# ── the renderer ─────────────────────────────────────────────────────────

def _doc_title(text, relpath):
    """The doc's H1 line with the leading '# ' stripped, or relpath if the
    doc carries no H1 as its first line."""
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip()
    return relpath


def _wrap(text, width=34):
    """Word-wrap to a fixed character width. Never returns an empty list —
    an empty line list breaks the height math in _footprint below."""
    if not text:
        return [""]
    return textwrap.wrap(text, width) or [""]


def _footprint(lines, size):
    """(text_width, text_height) at font `size`, computed with the exact
    metrics kit.Canvas.txt/box (tools/diagram/kit.py) and to_svg.py use —
    so a box sized from this footprint never overflows: the layout checks
    are the verify, and the geometry is built to satisfy them by
    construction rather than by luck."""
    tw = max((len(l) for l in lines), default=1) * size * 0.55
    th = len(lines) * size * 1.25
    return tw, th


def build_canvas(model, title):
    """Contract, not pixel geometry (the layout checks are the verify):
    title text `<title> — evaluation matrix` (size 32) with a three-line
    RED/GREEN/BLUE colour legend under it (the Flow.__init__ pattern); a
    header band with one column per criterion showing group, name, and
    `(M|D · <target> · w<weight>)`; one row per OPTION (options as rows,
    criteria as columns), each a box with the option ID + description at
    the left, one cell per criterion showing the mark (plus score in
    scored mode) with the basis as small text beneath, then OVERALL and
    RANK columns in scored mode. Row height follows the tallest cell (the
    movement-9 `_rowh` idiom, applied on both axes here since criteria are
    columns rather than rows). Colour: × cells RED; a dead option's row
    boxes RED; criteria whose Group is `cost` get a RED header; the
    preferred option's row box gets GREY fill and a PREFERRED tag. Below
    the table: the Preferred solution banner line, then one text block per
    countermeasure row. GREEN is never emitted for generated content —
    only the legend names what it would mean."""
    dk = _load_diagram_kit()
    Canvas, INK, RED, GREEN, BLUE, GREY = (
        dk.Canvas, dk.INK, dk.RED, dk.GREEN, dk.BLUE, dk.GREY,
    )

    HEADER_SIZE = 13
    BODY_SIZE = 12
    PAD_W, PAD_H = 24, 16
    COL_GAP, ROW_GAP = 12, 10
    X = 300

    c = Canvas()
    c.txt(f"{title} — evaluation matrix", X, 80, 32)

    legend = [
        ("RED — cost: × cells, dead option rows, cost-group criteria headers", RED),
        ("GREEN — reserved for Tony's hand annotations, never generated", GREEN),
        ("BLUE — text changed since the last reviewed snapshot", BLUE),
    ]
    ly = 132
    for text, colour in legend:
        c.txt(text, X, ly, 14, colour)
        ly += 20

    criteria = model["criteria"]
    options = model["options"]
    scored = model["mode"] == "scored"
    dead_ids = set(model["dead"])
    preferred = model["preferred"]

    # ── column content: (key, header_lines, body_lines_per_option, crit) ──
    label_bodies = []
    for opt in options:
        lines = _wrap(f"{opt['id']} — {opt['description']}")
        if opt["id"] == preferred:
            lines = lines + ["PREFERRED"]
        label_bodies.append(lines)
    columns = [("__label__", ["Option"], label_bodies, None)]

    for crit in criteria:
        weight = crit["weight"] if crit["weight"] is not None else 1
        header_lines = [crit["group"], crit["name"]] + _wrap(
            f"({crit['category']} · {crit['target']} · w{weight})"
        )
        bodies = []
        for opt in options:
            cd = model["cells"].get(opt["id"], {}).get(crit["name"])
            if cd is None:
                bodies.append(["—"])
                continue
            head = f"{cd['mark']} {cd['score']}" if cd["score"] is not None else cd["mark"]
            lines = [head] + (_wrap(cd["basis"]) if cd.get("basis") else [])
            bodies.append(lines)
        columns.append((crit["name"], header_lines, bodies, crit))

    if scored:
        columns.append(("OVERALL", ["OVERALL"],
                         [[str(model["overall"][o["id"]])] for o in options], None))
        columns.append(("RANK", ["RANK"],
                         [[str(model["rank"][o["id"]])] for o in options], None))

    # ── column widths, row heights — the movement-9 idiom, on both axes ──
    col_widths = []
    for _key, header_lines, bodies, _crit in columns:
        w = _footprint(header_lines, HEADER_SIZE)[0]
        for lines in bodies:
            w = max(w, _footprint(lines, BODY_SIZE)[0])
        col_widths.append(int(w) + PAD_W)

    header_h = int(max(_footprint(hl, HEADER_SIZE)[1] for _, hl, _, _ in columns)) + PAD_H

    row_heights = []
    for i in range(len(options)):
        h = max(_footprint(bodies[i], BODY_SIZE)[1] for _, _, bodies, _ in columns)
        row_heights.append(int(h) + PAD_H)

    col_x = []
    cx = X
    for w in col_widths:
        col_x.append(cx)
        cx += w + COL_GAP

    # ── draw: header band ────────────────────────────────────────────────
    table_y0 = ly + 20
    for (_key, header_lines, _bodies, crit), x, w in zip(columns, col_x, col_widths):
        stroke = RED if (crit and crit["group"] == "cost") else INK
        c.box("\n".join(header_lines), x, table_y0, w, header_h, stroke=stroke, size=HEADER_SIZE)

    # ── draw: option rows ────────────────────────────────────────────────
    ry = table_y0 + header_h + ROW_GAP
    for i, opt in enumerate(options):
        rh = row_heights[i]
        is_dead = opt["id"] in dead_ids
        is_pref = opt["id"] == preferred
        bg = GREY if is_pref else "transparent"

        for (_key, _hl, bodies, crit), x, w in zip(columns, col_x, col_widths):
            text = "\n".join(bodies[i])
            if crit is not None:
                cd = model["cells"].get(opt["id"], {}).get(crit["name"])
                is_cross = cd is not None and cd["mark"] == "×"
                stroke = RED if (is_cross or is_dead) else INK
            else:
                stroke = RED if is_dead else INK
            c.box(text, x, ry, w, rh, stroke=stroke, bg=bg, size=BODY_SIZE)
        ry += rh + ROW_GAP

    # ── below the table: preferred banner, countermeasures ──────────────
    y = ry + 20
    if preferred is not None:
        c.txt(f"PREFERRED SOLUTION: {preferred}", X, y, 18)
    else:
        c.txt("No preferred solution declared", X, y, 18, RED)
    y += int(18 * 1.25) + 16

    if model["countermeasures"]:
        for cm in model["countermeasures"]:
            block = _wrap(
                f"{cm['option']} · {cm['criterion']} · {cm['countermeasure']} · "
                f"{cm['type']} · {cm['confidence']} · "
                f"{cm['return_condition'] or '—'}",
                width=90,
            )
            c.txt("\n".join(block), X, y, 12)
            y += int(_footprint(block, 12)[1]) + 12
    else:
        c.txt("No countermeasures", X, y, 12)

    return c


def render(root, relpath):
    """(problems, out, svg_out, dims, deltas). Runs check_file first;
    problems -> (problems, None, None, None, None) and no file is written
    (the render refuses an invalid matrix). Clean: builds the canvas,
    calls diagram_kit.mark_deltas(els, out) (blue honored; returns the
    (marked, suppressed) counts), writes <dir>/<stem>-matrix.excalidraw
    (the gen_excalidraw doc dict shape) and <stem>-matrix.svg via
    diagram_to_svg.to_svg."""
    problems = check_file(root, relpath)
    if problems:
        return problems, None, None, None, None

    abs_path = os.path.join(root, relpath)
    with open(abs_path, encoding="utf-8") as f:
        text = f.read()
    model, _ = parse_matrix(text, relpath)

    diagram_kit = _load_diagram_kit()
    diagram_to_svg = _load_diagram_to_svg()

    canvas = build_canvas(model, _doc_title(text, relpath))

    stem = os.path.splitext(abs_path)[0]
    out = f"{stem}-matrix.excalidraw"
    svg_out = f"{stem}-matrix.svg"

    deltas = diagram_kit.mark_deltas(canvas.els, out)

    doc = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": canvas.els,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    with open(out, "w") as f:
        json.dump(doc, f, indent=2)

    dims = diagram_to_svg.to_svg(canvas.els, svg_out)

    return [], out, svg_out, dims, deltas


# ── selftest ─────────────────────────────────────────────────────────────

def _sw(path, content):
    """Write a fixture file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# F1 — the step-1 worked example, VERBATIM (byte-identical to the README
# fence this spec pins). Options A and B each declare an architecture
# overview path; a real doc needs those files to exist on disk, so every
# fixture that reuses this text also writes the two stubs unless the case
# is specifically about a missing overview (F12).
_F1_TEXT = """# Example — where the matrix validation should live

## Criteria

| Criterion | Group | Target / Minimum | Category | Weight |
|---|---|---|---|---|
| Setup cost | cost | ≤ 1 session to land | D | 1 |
| Refusal fires in CI | quality | planted violation exits 1 on push | M | 3 |
| Render legibility | quality | reviewable at a glance on the canvas | D | 2 |

## Options

| Option | Description | Architecture overview |
|---|---|---|
| A | Extend gate.py audit with matrix rules | docs/design/example-option-a.svg |
| B | Standalone tools/design tool, own CI steps | docs/design/example-option-b.svg |

## Evaluation matrix

| Criterion | A | B |
|---|---|---|
| Setup cost | ○ 4 — one rule block added, measured on a branch | △ 3 — new directory, but the kit idiom is proven twice |
| Refusal fires in CI | ○ 5 — canary refused in the T12 fixture | ○ 5 — canary refused via its own audit step |
| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |
| OVERALL | 21 | 26 |
| RANK | 2 | 1 |

## Preferred solution

B — a standalone tool keeps the gates self-contained and gives the render room.

## Proposal and next steps

Build tools/design/ on the gates precedent; wire two CI steps; render via the diagram toolkit.

## Risks and countermeasures required

One risk carried: a second tool directory to keep in idiom with the first — countermeasured below.

## Countermeasures

| Option | Criterion | Countermeasure | Type | Confidence | Return condition |
|---|---|---|---|---|---|
| B | Setup cost | reuse the gates kit's parsing idiom wholesale | permanent | high — same idiom shipped in tools/gates and tools/diagram | |

"""

_STUB_A_REL = "docs/design/example-option-a.svg"
_STUB_B_REL = "docs/design/example-option-b.svg"


def _write_stubs(root, a=True, b=True):
    if a:
        _sw(os.path.join(root, _STUB_A_REL), "<svg/>\n")
    if b:
        _sw(os.path.join(root, _STUB_B_REL), "<svg/>\n")


def _f1():
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), _F1_TEXT)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert problems == [], f"expected clean, got {problems}"
        model, _ = parse_matrix(_F1_TEXT, rel)
        assert model["mode"] == "scored", f"expected scored, got {model['mode']!r}"
        assert model["preferred"] == "B", f"expected B, got {model['preferred']!r}"
        assert model["overall"] == {"A": 21, "B": 26}, model["overall"]
        assert model["rank"] == {"B": 1, "A": 2}, model["rank"]
        assert model["dead"] == [], model["dead"]


def _f2():
    old = (
        "| Criterion | A | B |\n"
        "|---|---|---|\n"
        "| Setup cost | ○ 4 — one rule block added, measured on a branch | △ 3 — new directory, but the kit idiom is proven twice |\n"
        "| Refusal fires in CI | ○ 5 — canary refused in the T12 fixture | ○ 5 — canary refused via its own audit step |\n"
        "| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |\n"
        "| OVERALL | 21 | 26 |\n"
        "| RANK | 2 | 1 |\n"
    )
    new = (
        "| Criterion | A | B |\n"
        "|---|---|---|\n"
        "| Setup cost | ○ | △ |\n"
        "| Refusal fires in CI | ○ | ○ |\n"
        "| Render legibility | × | ○ |\n"
    )
    text = _F1_TEXT.replace(old, new)
    assert text != _F1_TEXT, "F2 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert problems == [], f"expected clean, got {problems}"
        model, _ = parse_matrix(text, rel)
        assert model["mode"] == "marks", f"expected marks, got {model['mode']!r}"


def _f3():
    old = "| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |\n| OVERALL"
    new = "| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |\n| Latency | ○ 4 — x | ○ 4 — x |\n| OVERALL"
    text = _F1_TEXT.replace(old, new)
    assert text != _F1_TEXT, "F3 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("no declaration" in p and "Latency" in p for p in problems), problems


def _f4():
    old = "| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |\n"
    text = _F1_TEXT.replace(old, "")
    assert text != _F1_TEXT, "F4 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("Render legibility" in p for p in problems), problems


def _f5():
    old = (
        "## Countermeasures\n\n"
        "| Option | Criterion | Countermeasure | Type | Confidence | Return condition |\n"
        "|---|---|---|---|---|---|\n"
        "| B | Setup cost | reuse the gates kit's parsing idiom wholesale | permanent | high — same idiom shipped in tools/gates and tools/diagram | |\n"
    )
    new = (
        "## Countermeasures\n\n"
        "A countermeasure is still owed for B's Setup cost triangle, but the table was dropped by mistake.\n"
    )
    text = _F1_TEXT.replace(old, new)
    assert text != _F1_TEXT, "F5 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("countermeasure" in p and "B" in p and "Setup cost" in p for p in problems), problems


def _f6():
    old = "| B | Setup cost | reuse the gates kit's parsing idiom wholesale | permanent | high — same idiom shipped in tools/gates and tools/diagram | |"
    new = "| B | Setup cost | reuse the gates kit's parsing idiom wholesale | temporary | high — same idiom shipped in tools/gates and tools/diagram | |"
    text = _F1_TEXT.replace(old, new)
    assert text != _F1_TEXT, "F6 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("Return condition" in p for p in problems), problems


def _f7():
    text = _F1_TEXT.replace(
        "| Render legibility | quality | reviewable at a glance on the canvas | D | 2 |",
        "| Render legibility | quality | reviewable at a glance on the canvas | M | 2 |",
    ).replace(
        "B — a standalone tool keeps the gates self-contained and gives the render room.",
        "A — extends what exists.",
    )
    assert text != _F1_TEXT, "F7 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("dead option" in p and "A" in p and "Render legibility" in p for p in problems), problems


def _f8():
    old = "| Setup cost | ○ 4 — one rule block added, measured on a branch | △ 3 — new directory, but the kit idiom is proven twice |"
    new = "| Setup cost | ○ 4 | △ 3 — new directory, but the kit idiom is proven twice |"
    text = _F1_TEXT.replace(old, new)
    assert text != _F1_TEXT, "F8 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("score without basis" in p for p in problems), problems


def _f9():
    text = _F1_TEXT.replace("| OVERALL | 21 | 26 |", "| OVERALL | 22 | 26 |")
    assert text != _F1_TEXT, "F9 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("OVERALL" in p and "22" in p and "21" in p for p in problems), problems


def _f10():
    criteria_block = (
        "## Criteria\n\n"
        "| Criterion | Group | Target / Minimum | Category | Weight |\n"
        "|---|---|---|---|---|\n"
        "| Setup cost | cost | ≤ 1 session to land | D | 1 |\n"
        "| Refusal fires in CI | quality | planted violation exits 1 on push | M | 3 |\n"
        "| Render legibility | quality | reviewable at a glance on the canvas | D | 2 |\n\n"
    )
    options_block = (
        "## Options\n\n"
        "| Option | Description | Architecture overview |\n"
        "|---|---|---|\n"
        "| A | Extend gate.py audit with matrix rules | docs/design/example-option-a.svg |\n"
        "| B | Standalone tools/design tool, own CI steps | docs/design/example-option-b.svg |\n\n"
    )
    combined = criteria_block + options_block
    assert combined in _F1_TEXT, "F10 setup: combined block not found"
    text = _F1_TEXT.replace(combined, options_block + criteria_block)
    assert text != _F1_TEXT, "F10 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("section order" in p for p in problems), problems


def _f11():
    old = "| Setup cost | cost | ≤ 1 session to land | D | 1 |"
    new = "| Setup cost | cost | ≤ 1 session to land | D | |"
    text = _F1_TEXT.replace(old, new)
    assert text != _F1_TEXT, "F11 setup: replace target not found"
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), text)
        _write_stubs(root)
        problems = check_file(root, rel)
        assert any("Weight" in p for p in problems), problems


def _f12():
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), _F1_TEXT)
        _write_stubs(root, a=True, b=False)
        problems = check_file(root, rel)
        assert any("example-option-b.svg" in p for p in problems), problems


def _f13():
    with tempfile.TemporaryDirectory() as root:
        _write_stubs(root)
        _sw(os.path.join(root, "docs", "design", "valid.md"), _F1_TEXT)

        old = "| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |\n| OVERALL"
        new = "| Render legibility | × 1 — audit output is line-based, no canvas | ○ 4 — movement-9 table, layout checks clean |\n| Latency | ○ 4 — x | ○ 4 — x |\n| OVERALL"
        broken_text = _F1_TEXT.replace(old, new)
        assert broken_text != _F1_TEXT, "F13 setup: replace target not found"
        _sw(os.path.join(root, "docs", "design", "broken.md"), broken_text)

        _sw(os.path.join(root, "docs", "design", "notes.md"), "# Notes\n\nJust a note, no matrix.\n")

        problems, count = audit_matrices(root)
        assert count == 2, f"expected count 2, got {count}"
        expected = check_file(root, "docs/design/broken.md")
        assert problems == expected, f"expected exactly the broken doc's problems {expected}, got {problems}"
        assert all(p.startswith("docs/design/broken.md — ") for p in problems), problems


def _f14():
    with tempfile.TemporaryDirectory() as root:
        rel = "docs/design/case.md"
        _sw(os.path.join(root, rel), _F1_TEXT)
        _write_stubs(root)

        problems, out, svg_out, dims, deltas = render(root, rel)
        assert problems == [], f"expected clean, got {problems}"
        assert os.path.isfile(out), f"expected {out} to exist"
        assert os.path.isfile(svg_out), f"expected {svg_out} to exist"

        with open(out, encoding="utf-8") as f:
            doc = json.load(f)
        els = doc["elements"]

        diagram_to_svg = _load_diagram_to_svg()
        o = diagram_to_svg.overflow_report(els)
        assert o == [], f"overflow: {o}"
        col = diagram_to_svg.collision_report(els)
        assert col == [], f"collision: {col}"
        t = diagram_to_svg.text_overlap_report(els)
        assert t == [], f"text overlap: {t}"

        with open(svg_out, encoding="utf-8") as f:
            svg_text = f.read()
        for glyph in ("○", "△", "×"):
            assert glyph in svg_text, f"glyph {glyph!r} missing from written SVG — a mark that " \
                "dies in SVG export dies here, not on Tony's canvas"


def selftest():
    """Runs F1-F14, each in its own tempfile.TemporaryDirectory (no git
    required — matrices are pure files). Prints one 'ok <n> — <name>' line
    per case; on the first failure prints 'FAIL <n> — <name>: <why>' and
    returns 1. On full success prints 'selftest: 14 ok' and returns 0.

    Not covered here, named rather than silently skipped: a living-but-not-
    top preferred option in scored mode, and OVERALL ties, have no F-case
    in this suite."""
    cases = [
        (_f1, "valid scored — clean, recomputed overall/rank/preferred/dead match"),
        (_f2, "valid marks-only — clean, mode marks"),
        (_f3, "undeclared criterion — 'no declaration' names it"),
        (_f4, "declared-but-unscored — missing-row problem names it"),
        (_f5, "△ without countermeasure row"),
        (_f6, "temporary countermeasure without Return condition"),
        (_f7, "dead option (× on M) preferred — named refusal"),
        (_f8, "score without basis"),
        (_f9, "arithmetic drift — declared OVERALL disagrees with recomputed"),
        (_f10, "section order — Options moved above Criteria"),
        (_f11, "mixed weights — one row emptied, others integers"),
        (_f12, "missing architecture overview file"),
        (_f13, "audit sweep — count and problems scoped to the broken doc"),
        (_f14, "render: layout clean, glyphs survive to SVG"),
    ]
    for i, (fn, name) in enumerate(cases, start=1):
        try:
            fn()
        except AssertionError as e:
            print(f"FAIL {i} — {name}: {e}")
            return 1
        except Exception as e:
            print(f"FAIL {i} — {name}: unexpected {type(e).__name__}: {e}")
            return 1
        print(f"ok {i} — {name}")
    print("selftest: 14 ok")
    return 0
