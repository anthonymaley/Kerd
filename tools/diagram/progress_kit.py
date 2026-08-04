#!/usr/bin/env python3
"""Progress renderer — derivation.

Derived from disk, never self-reported: a checked box in the working tree
is a claim; a commit is evidence. This module holds every decision (the
commit-to-piece mapping, board state, slug discovery, the --json model
schema); progress.py only parses argv, writes files, and prints.
"""

import glob
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

# D8: import the diagram kit normally — the gates kit (loaded by path in
# load_gates_kit below) is the one that needs the by-path trick, because
# both files are named kit.py and a bare sys.path insert of both dirs would
# silently shadow one.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, INK, RED, GREEN, GREY  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))      # default root; every function takes root

PIECE_RE = re.compile(r'^- \[( |x)\] (.*)$')
TRAILER_RE = re.compile(r'^Piece:\s*([a-z0-9][a-z0-9-]*)/([1-9][0-9]*)\s*$')

# Not part of the A8 signature list, but needed locally: slug discovery
# (A3) and Pieces-section scanning use these two patterns.
_SPEC_FILE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}-([a-z0-9][a-z0-9-]*)-spec\.md$')
_PIECES_HEADING_RE = re.compile(r'^## Pieces[ \t]*$', re.MULTILINE)
_NEXT_HEADING_RE = re.compile(r'^## ', re.MULTILINE)

_gates_kit = None


def load_gates_kit():
    """Load tools/gates/kit.py by path (D8): both this file and the gates
    module are named kit.py, so a bare sys.path insert of both dirs would
    silently shadow one. Loaded once, cached in a module global."""
    global _gates_kit
    if _gates_kit is None:
        p = os.path.join(REPO, "tools", "gates", "kit.py")
        spec = importlib.util.spec_from_file_location("gates_kit", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _gates_kit = m
    return _gates_kit


def discover_slugs(root):
    """A3: union of S from docs/plans/<date>-<S>-spec.md filenames and
    basenames (minus .md) of docs/product/*.md. Absent directories
    contribute nothing (vacuous pass). Sorted alphabetically."""
    slugs = set()

    plans_dir = os.path.join(root, "docs", "plans")
    if os.path.isdir(plans_dir):
        for fname in os.listdir(plans_dir):
            m = _SPEC_FILE_RE.match(fname)
            if m:
                slugs.add(m.group(1))

    product_dir = os.path.join(root, "docs", "product")
    if os.path.isdir(product_dir):
        for fname in os.listdir(product_dir):
            if fname.endswith(".md"):
                slugs.add(fname[:-3])

    return sorted(slugs)


def contract_for(root, slug):
    """Repo-relative path to the latest-by-filename
    docs/plans/*-<slug>-spec.md, or None if no contract file exists."""
    pattern = os.path.join(root, "docs", "plans", f"*-{slug}-spec.md")
    matches = sorted(glob.glob(pattern))
    if not matches:
        return None
    return os.path.relpath(matches[-1], root)


def parse_pieces(text):
    """(checked, text) tuples, in order, for every '- [ ] '/'- [x] ' line
    under the first '## Pieces' heading in `text`. [] when the heading is
    absent, or present with no checklist lines under it."""
    m = _PIECES_HEADING_RE.search(text)
    if not m:
        return []
    rest = text[m.end():]
    next_m = _NEXT_HEADING_RE.search(rest)
    body = rest[:next_m.start()] if next_m else rest

    pieces = []
    for line in body.splitlines():
        pm = PIECE_RE.match(line)
        if pm:
            pieces.append((pm.group(1) == "x", pm.group(2)))
    return pieces


def head_text(root, relpath):
    """git show HEAD:<relpath>; None on any git failure — no HEAD, no such
    path at HEAD, a zero-commit repo — never an exception."""
    result = subprocess.run(
        ["git", "-C", root, "show", f"HEAD:{relpath}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def piece_evidence(root):
    """All (slug, n) pairs found by scanning every line of
    `git log --format=%B` against TRAILER_RE. Empty set on git failure
    (e.g. a zero-commit repo) — never an exception."""
    result = subprocess.run(
        ["git", "-C", root, "log", "--format=%B"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return set()

    evidence = set()
    for line in result.stdout.splitlines():
        m = TRAILER_RE.match(line)
        if m:
            evidence.add((m.group(1), int(m.group(2))))
    return evidence


def goal_for(root, slug, evidence):
    """One A5 goals entry for `slug`. Mapping per A1: mode is 'trailer' when
    >=1 (slug, n) pair is in `evidence`, else 'legacy'. landed = evidence
    reachable from HEAD — trailer mode checks (slug, n) in `evidence`;
    legacy mode checks the box in the HEAD version of the contract. A box
    checked only in the working tree is 'in flight', never 'landed'."""
    contract = contract_for(root, slug)
    if contract is None:
        return {"slug": slug, "contract": None, "mode": None, "pieces": [], "counts": None}

    abs_contract = os.path.join(root, contract)
    with open(abs_contract, encoding="utf-8") as f:
        worktree_text = f.read()
    worktree_pieces = parse_pieces(worktree_text)

    if not worktree_pieces:
        return {"slug": slug, "contract": contract, "mode": None, "pieces": [], "counts": None}

    head_full = head_text(root, contract)
    head_pieces = parse_pieces(head_full) if head_full is not None else []

    mode = "trailer" if any(s == slug for (s, _n) in evidence) else "legacy"

    pieces = []
    counts = {"landed": 0, "in_flight": 0, "remaining": 0}
    for n, (checked_wt, text) in enumerate(worktree_pieces, start=1):
        checked_head = head_pieces[n - 1][0] if n - 1 < len(head_pieces) else False

        if mode == "trailer":
            landed = (slug, n) in evidence
        else:
            landed = checked_head

        if landed:
            state = "landed"
            counts["landed"] += 1
        elif checked_wt:
            state = "in flight"
            counts["in_flight"] += 1
        else:
            state = "remaining"
            counts["remaining"] += 1

        pieces.append({
            "n": n, "text": text,
            "checked_worktree": checked_wt, "checked_head": checked_head,
            "state": state,
        })

    return {"slug": slug, "contract": contract, "mode": mode, "pieces": pieces, "counts": counts}


def board_for(root, slug, gates_kit):
    """One A5 board entry for `slug`, per A2. `gates_kit.route`'s
    cumulative-input semantics make the pass prefix monotone, so with
    E = enters_at: rungs shallower than E are 'built', rung E is
    'in-flight', rungs deeper than E are 'missing' (carrying
    need = len(rung['need'])). `agreed` is an overlay from a
    docs/gates/*-<slug>-<rung>.md GO record, never a fourth exclusive
    state. A bypass (spike) slug carries no rung cells."""
    route_result = gates_kit.route(root, slug)

    if route_result["bypass"]:
        return {"slug": slug, "bypass": True, "enters_at": route_result["enters_at"], "rungs": []}

    enters_at = route_result["enters_at"]
    e_idx = gates_kit.RUNGS.index(enters_at)
    by_rung = {r["rung"]: r for r in route_result["rungs"]}

    rungs = []
    for i, rung_name in enumerate(gates_kit.RUNGS):
        r = by_rung[rung_name]
        if i < e_idx:
            state = "built"
        elif i == e_idx:
            state = "in-flight"
        else:
            state = "missing"

        agreed_pattern = os.path.join(root, "docs", "gates", f"*-{slug}-{rung_name}.md")
        agreed = bool(glob.glob(agreed_pattern))

        rungs.append({
            "rung": rung_name, "state": state,
            "have": len(r["have"]), "need": len(r["need"]),
            "agreed": agreed,
        })

    return {"slug": slug, "bypass": False, "enters_at": enters_at, "rungs": rungs}


def derive(root):
    """The full A5 model: audit_problems, slugs, board, goals, drift."""
    gates_kit = load_gates_kit()
    slugs = discover_slugs(root)
    evidence = piece_evidence(root)

    board = [board_for(root, slug, gates_kit) for slug in slugs]
    goals = [goal_for(root, slug, evidence) for slug in slugs]

    drift = []
    for g in goals:
        for p in g["pieces"]:
            if p["state"] == "landed" and not p["checked_worktree"]:
                drift.append(
                    f"{g['slug']}/{p['n']} — landed in git, box unchecked in working tree"
                )

    return {
        "audit_problems": len(gates_kit.audit(root)),
        "slugs": slugs,
        "board": board,
        "goals": goals,
        "drift": drift,
    }


def render_table(model):
    """A6: the terminal pull, exact. Board glyphs: '#' built, '>'
    in-flight, '. need <n>' missing, with ' G' appended when agreed.
    A bypass (spike) slug renders one 'SPIKE <slug> — ladder bypassed'
    line in place of board cells; its goal strip is unaffected. Goal
    glyphs: '#' landed, '>' in flight, '.' remaining, one per piece in
    order. An empty model (no slugs on disk) renders a single
    'no work orders on disk' line in place of BOARD/GOAL."""
    lines = [
        "progress — derived from disk: git log · gate route · "
        "Pieces checklists · docs/gates/",
    ]
    if model["audit_problems"] == 0:
        lines.append("audit: clean")
    else:
        lines.append(f"audit: {model['audit_problems']} problems")
    lines.append("")

    if not model["slugs"]:
        lines.append("no work orders on disk")
        lines.append("")
        lines.append("drift: none")
        return "\n".join(lines)

    lines.append("BOARD   [G] agreed  [#] built  [>] in-flight  [.] missing")

    non_bypass = [b for b in model["board"] if not b["bypass"]]
    bypass = [b for b in model["board"] if b["bypass"]]

    if non_bypass:
        rung_names = [r["rung"] for r in non_bypass[0]["rungs"]]
        col_slugs = [b["slug"] for b in non_bypass]

        cell_text = {}
        for b in non_bypass:
            for r in b["rungs"]:
                if r["state"] == "built":
                    text = "#"
                elif r["state"] == "in-flight":
                    text = ">"
                else:
                    text = f". need {r['need']}"
                if r["agreed"]:
                    text += " G"
                cell_text[(r["rung"], b["slug"])] = text

        label_width = max(len("rung"), max(len(r) for r in rung_names))
        col_width = {}
        for slug in col_slugs:
            w = len(slug)
            for rung in rung_names:
                w = max(w, len(cell_text[(rung, slug)]))
            col_width[slug] = w

        gap = "  "
        header = "rung".ljust(label_width) + gap + gap.join(
            slug.ljust(col_width[slug]) for slug in col_slugs
        )
        lines.append(header.rstrip())
        for rung in rung_names:
            row = rung.ljust(label_width) + gap + gap.join(
                cell_text[(rung, slug)].ljust(col_width[slug]) for slug in col_slugs
            )
            lines.append(row.rstrip())

    for b in bypass:
        lines.append(f"SPIKE {b['slug']} — ladder bypassed")

    lines.append("")

    slug_width = max(len(g["slug"]) for g in model["goals"])
    rows = []
    for g in model["goals"]:
        if g["contract"] is None:
            strip = "—"
            message = "no contract on disk"
        elif g["counts"] is None:
            strip = "—"
            message = f"no Pieces checklist in {g['contract']}"
        else:
            glyphs = []
            for p in g["pieces"]:
                if p["state"] == "landed":
                    glyphs.append("#")
                elif p["state"] == "in flight":
                    glyphs.append(">")
                else:
                    glyphs.append(".")
            strip = "".join(glyphs)
            c = g["counts"]
            message = (
                f"{c['landed']} landed · {c['in_flight']} in flight · "
                f"{c['remaining']} remaining"
            )
        rows.append((g["slug"], strip, message))

    strip_width = max(len(strip) for (_slug, strip, _msg) in rows)
    for slug, strip, message in rows:
        lines.append(
            f"GOAL  {slug.ljust(slug_width)}  {strip.ljust(strip_width)}  {message}"
        )

    lines.append("")

    if model["drift"]:
        for d in model["drift"]:
            lines.append(f"drift: {d}")
    else:
        lines.append("drift: none")

    return "\n".join(lines)


def build_canvas(model):
    """A7: title, legend, board grid, goal strips, drift lines — the drawing
    on the live canvas. Returns the kit.Canvas; writes nothing (progress.py
    owns the .excalidraw/.svg writes, per A8's gates-style split)."""
    X = 300
    LABEL_W = 150
    COL_W = 230
    CELL_H = 40
    ROW_GAP = 8
    PIECE = 26
    PIECE_GAP = 4

    c = Canvas()
    c.txt("Progress — derived from disk", X, 80, 24)

    # Legend: one line per A4 colour meaning, in its own colour — the
    # Flow-class precedent (kit.Flow.__init__).
    legend = [
        ("built / landed — INK stroke, GREY fill: the have", INK),
        ("in-flight / in flight — INK stroke, dashed, strokeWidth 2: "
         "the seam being worked", INK),
        ("missing / remaining — RED stroke: the need is the cost", RED),
        ("agreed — GREEN stroke replacing INK on that cell: a GO record "
         "is the human's input", GREEN),
        ("drift — RED text: a named problem is cost", RED),
    ]
    y = 130
    for text, colour in legend:
        c.txt(text, X, y, 14, colour)
        y += 20

    y += 20

    if not model["slugs"]:
        c.txt("no work orders on disk", X, y, 16)
        return c

    # ── board grid ───────────────────────────────────────────────────────
    board = model["board"]
    header_y = y
    c.txt("rung", X, header_y, 12)
    for i, b in enumerate(board):
        col_x = X + LABEL_W + i * COL_W
        if b["bypass"]:
            c.txt(f"SPIKE {b['slug']}\n— ladder bypassed", col_x + 4,
                  header_y, 11)
        else:
            c.txt(b["slug"], col_x + 4, header_y, 12)

    non_bypass = [b for b in board if not b["bypass"]]
    rung_names = [r["rung"] for r in non_bypass[0]["rungs"]] if non_bypass else []
    rows_y0 = header_y + 30

    for ridx, rung_name in enumerate(rung_names):
        row_y = rows_y0 + ridx * (CELL_H + ROW_GAP)
        c.txt(rung_name, X, row_y + 12, 13)
        for i, b in enumerate(board):
            if b["bypass"]:
                continue
            col_x = X + LABEL_W + i * COL_W
            r = b["rungs"][ridx]
            if r["state"] == "built":
                stroke = GREEN if r["agreed"] else INK
                c.rect(col_x, row_y, COL_W, CELL_H, stroke=stroke, bg=GREY)
            elif r["state"] == "in-flight":
                stroke = GREEN if r["agreed"] else INK
                c.box("enters at", col_x, row_y, COL_W, CELL_H,
                      stroke=stroke, sw=2, dashed=True, size=13)
            else:  # missing
                stroke = GREEN if r["agreed"] else RED
                c.box(f"need {r['need']}", col_x, row_y, COL_W, CELL_H,
                      stroke=stroke, size=13)

    board_bottom = rows_y0 + len(rung_names) * (CELL_H + ROW_GAP) if rung_names \
        else header_y + 30
    y = board_bottom + 40

    # ── goal strips ──────────────────────────────────────────────────────
    for g in model["goals"]:
        c.txt(g["slug"], X, y, 16)
        y += 16 * 1.25 + 10

        if g["contract"] is None:
            c.txt("no contract on disk", X, y, 13, RED)
            y += 13 * 1.25 + 24
            continue
        if g["counts"] is None:
            c.txt(f"no Pieces checklist in {g['contract']}", X, y, 13, RED)
            y += 13 * 1.25 + 24
            continue

        for k, p in enumerate(g["pieces"]):
            cx = X + k * (PIECE + PIECE_GAP)
            if p["state"] == "landed":
                c.rect(cx, y, PIECE, PIECE, stroke=INK, bg=GREY)
            elif p["state"] == "in flight":
                c.rect(cx, y, PIECE, PIECE, stroke=INK, sw=2, dashed=True)
            else:  # remaining
                c.rect(cx, y, PIECE, PIECE, stroke=RED)
        y += PIECE + 10

        counts = g["counts"]
        c.txt(f"{counts['landed']} landed · {counts['in_flight']} in flight "
              f"· {counts['remaining']} remaining", X, y, 13)
        y += 13 * 1.25 + 24

    # ── drift ────────────────────────────────────────────────────────────
    if model["drift"]:
        for d in model["drift"]:
            c.txt(d, X, y, 13, RED)
            y += 13 * 1.25 + 6
    else:
        c.txt("drift: none", X, y, 13)

    return c


# ── selftest ─────────────────────────────────────────────────────────────
#
# Part B fixtures (F1-F10): the gates' own fixture idiom (tools/gates/
# kit.py's _selftest_body), plus git — each case builds its tree in a
# tempfile.TemporaryDirectory, `git init`s it, and commits with an
# explicit identity, because CI runners carry no git identity and a bare
# `git commit` fails there. Slug 'alpha', contract
# docs/plans/2026-01-02-alpha-spec.md, per Part B.

_ST_SLUG = "alpha"
_ST_CONTRACT_REL = "docs/plans/2026-01-02-alpha-spec.md"


def _sw(path, content):
    """Write a fixture file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _git(root, *args):
    """Run a git command in a fixture tree; a nonzero exit reads as a case
    failure (via AssertionError) like any other broken fixture setup."""
    result = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    assert result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr}"
    return result.stdout


def _git_init(root):
    _git(root, "init", "-q")


def _git_commit(root, message):
    """Stage everything and commit with an explicit identity — CI runners
    have no git identity configured, so a bare `git commit` fails there."""
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=selftest", "-c", "user.email=selftest@kerd",
         "commit", "-q", "-m", message)


def _git_commit_empty(root, message):
    """An empty commit (no staging) carrying trailer lines in its body,
    without touching whatever uncommitted worktree edits are in place —
    the F5/F6/F7 shape: a checkpoint commit that adds evidence without
    landing (or disturbing) the working tree."""
    _git(root, "-c", "user.name=selftest", "-c", "user.email=selftest@kerd",
         "commit", "-q", "--allow-empty", "-m", message)


def _pieces_md(checked):
    """A '## Pieces' checklist for the shared alpha fixture contract, one
    box per entry in `checked`."""
    labels = ["Step 1: do the first thing", "Step 2: do the second thing",
              "Step 3: do the third thing"]
    lines = ["# Alpha — build spec", "", "## Pieces", ""]
    for c, label in zip(checked, labels):
        lines.append(f"- [{'x' if c else ' '}] {label}")
    return "\n".join(lines) + "\n"


def _goal(model, slug=_ST_SLUG):
    return next(g for g in model["goals"] if g["slug"] == slug)


def _board(model, slug=_ST_SLUG):
    return next(b for b in model["board"] if b["slug"] == slug)


def _piece(goal, n):
    return next(p for p in goal["pieces"] if p["n"] == n)


def _f1():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        model = derive(d)
        assert model["slugs"] == [], f"expected slugs == [], got {model['slugs']}"
        table = render_table(model)
        assert "no work orders on disk" in table, \
            f"expected 'no work orders on disk' in table:\n{table}"


def _f2():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        contract_abs = os.path.join(d, _ST_CONTRACT_REL)
        _sw(contract_abs, _pieces_md([False, False, False]))
        assert piece_evidence(d) == set(), "expected empty evidence set on a zero-commit repo"
        assert head_text(d, _ST_CONTRACT_REL) is None, \
            "expected head_text None on a zero-commit repo"
        model = derive(d)
        g = _goal(model)
        assert g["counts"] == {"landed": 0, "in_flight": 0, "remaining": 3}, g["counts"]
        for n in (1, 2, 3):
            assert _piece(g, n)["state"] == "remaining", f"piece {n}: {_piece(g, n)}"


def _f3():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        contract_abs = os.path.join(d, _ST_CONTRACT_REL)
        _sw(contract_abs, _pieces_md([False, False, False]))
        _git_commit(d, "add alpha contract, all unchecked")
        _sw(contract_abs, _pieces_md([True, True, False]))  # worktree only
        model = derive(d)
        g = _goal(model)
        assert g["mode"] == "legacy", f"expected legacy mode, got {g['mode']!r}"
        assert _piece(g, 1)["state"] == "in flight", f"piece 1: {_piece(g, 1)}"
        assert _piece(g, 2)["state"] == "in flight", f"piece 2: {_piece(g, 2)}"
        assert _piece(g, 3)["state"] == "remaining", f"piece 3: {_piece(g, 3)}"
        assert g["counts"] == {"landed": 0, "in_flight": 2, "remaining": 1}, g["counts"]


def _f4():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        contract_abs = os.path.join(d, _ST_CONTRACT_REL)
        _sw(contract_abs, _pieces_md([True, True, False]))
        _git_commit(d, "add alpha contract, boxes 1-2 checked")
        model = derive(d)
        g = _goal(model)
        assert g["mode"] == "legacy", f"expected legacy mode, got {g['mode']!r}"
        assert _piece(g, 1)["state"] == "landed", f"piece 1: {_piece(g, 1)}"
        assert _piece(g, 2)["state"] == "landed", f"piece 2: {_piece(g, 2)}"
        assert _piece(g, 3)["state"] == "remaining", f"piece 3: {_piece(g, 3)}"
        assert g["counts"] == {"landed": 2, "in_flight": 0, "remaining": 1}, g["counts"]


def _f5():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        contract_abs = os.path.join(d, _ST_CONTRACT_REL)
        _sw(contract_abs, _pieces_md([False, False, False]))
        _git_commit(d, "add alpha contract, all unchecked")
        _sw(contract_abs, _pieces_md([True, True, False]))  # worktree only, as F3
        _git_commit_empty(d, "checkpoint\n\nPiece: alpha/2")
        model = derive(d)
        g = _goal(model)
        assert g["mode"] == "trailer", f"expected trailer mode, got {g['mode']!r}"
        assert _piece(g, 2)["state"] == "landed", f"piece 2: {_piece(g, 2)}"
        assert _piece(g, 1)["state"] == "in flight", f"piece 1: {_piece(g, 1)}"


def _f6():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        contract_abs = os.path.join(d, _ST_CONTRACT_REL)
        _sw(contract_abs, _pieces_md([False, False, False]))
        _git_commit(d, "add alpha contract, all unchecked")
        _git_commit_empty(d, "checkpoint\n\nPiece: alpha/1\nPiece: alpha/3")
        model = derive(d)
        g = _goal(model)
        assert g["mode"] == "trailer", f"expected trailer mode, got {g['mode']!r}"
        assert _piece(g, 1)["state"] == "landed", f"piece 1: {_piece(g, 1)}"
        assert _piece(g, 3)["state"] == "landed", f"piece 3: {_piece(g, 3)}"


def _f7():
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        contract_abs = os.path.join(d, _ST_CONTRACT_REL)
        _sw(contract_abs, _pieces_md([False, False, False]))
        _git_commit(d, "add alpha contract, all unchecked")
        _git_commit_empty(d, "checkpoint\n\nPiece: alpha/2")
        model = derive(d)
        g = _goal(model)
        assert _piece(g, 2)["state"] == "landed", f"piece 2: {_piece(g, 2)}"
        expected = "alpha/2 — landed in git, box unchecked in working tree"
        assert expected in model["drift"], f"expected drift line {expected!r}, got {model['drift']}"


_F8_PRODUCT = (
    "---\nroute: new\nstage: framed\n---\n\n"
    "## Value\n\nSaves 10 hours a week across the team.\n"
)


def _mk_f8_tree(d):
    """docs/product/alpha.md with legal front matter and a Value section,
    committed — enough for gates routing to place alpha at viability
    (frame's inputs are satisfied trivially; slice's Risk ledger is not)."""
    _git_init(d)
    _sw(os.path.join(d, "docs", "product", f"{_ST_SLUG}.md"), _F8_PRODUCT)
    _git_commit(d, "add alpha product doc")


def _f8():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        model = derive(d)
        b = _board(model)
        assert b["enters_at"] == "viability", f"expected enters_at viability, got {b['enters_at']!r}"
        by_rung = {r["rung"]: r for r in b["rungs"]}
        assert by_rung["frame"]["state"] == "built", by_rung["frame"]
        assert by_rung["viability"]["state"] == "in-flight", by_rung["viability"]
        assert by_rung["slice"]["state"] == "missing", by_rung["slice"]
        assert by_rung["slice"]["need"] >= 1, by_rung["slice"]


def _f9():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        _sw(
            os.path.join(d, "docs", "gates", "2026-01-01-alpha-viability.md"),
            "---\nroute: new\nstage: viable\n---\n\n## GO\n\nViability approved.\n",
        )
        _git_commit(d, "add alpha viability GO record")
        model = derive(d)
        b = _board(model)
        for r in b["rungs"]:
            expected = r["rung"] == "viability"
            assert r["agreed"] == expected, f"{r['rung']}: expected agreed={expected}, got {r}"


def _f10():
    from to_svg import overflow_report, collision_report, text_overlap_report
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        model = derive(d)
        canvas = build_canvas(model)
        o, c_, t = (overflow_report(canvas.els), collision_report(canvas.els),
                    text_overlap_report(canvas.els))
        assert o == [], o
        assert c_ == [], c_
        assert t == [], t


def selftest():
    """Part B: F1-F10, each built fresh in its own temp tree (git init +
    committed history, per case). Prints one 'ok <n> — <name>' line per
    case; on the first failed assertion prints 'FAIL <n> — <name>: <why>'
    and returns 1. On full success prints 'selftest: 10 ok' and returns 0.

    Two things this suite does NOT cover, named rather than silently
    skipped: a bypass (spike) slug — `route()`'s bypass:true path, which
    renders a board entry with rungs: [] and a SPIKE line in render_table
    — has no F-case in Part B and none is invented here; both stay
    untested by this suite."""
    cases = [
        (_f1, "no docs/ on disk"),
        (_f2, "uncommitted contract, zero-commit repo"),
        (_f3, "legacy mode: worktree-checked boxes stay in flight until committed"),
        (_f4, "legacy mode: boxes checked at commit time land"),
        (_f5, "trailer mode switches on: legacy piece without a trailer stays in flight"),
        (_f6, "multi-trailer commit: two Piece lines in one message both land"),
        (_f7, "drift: landed in git, box unchecked in the working tree"),
        (_f8, "board: frame built, viability in-flight, slice missing"),
        (_f9, "agreed overlay: a docs/gates GO record marks only its own rung"),
        (_f10, "canvas layout checks clean on the F8 model"),
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
    print("selftest: 10 ok")
    return 0
