#!/usr/bin/env python3
"""Progress renderer — derivation.

Derived from disk, never self-reported: a checked box in the working tree
is a claim; a commit is evidence. This module holds every decision (the
commit-to-piece mapping, board state, slug discovery, the --json model
schema); progress.py only parses argv, writes files, and prints.
"""

import glob
import hashlib
import html
import importlib.util
import json
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
from to_svg import to_svg  # noqa: E402

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
    """Landed-piece evidence: dict {(slug, n): {"sha": short_sha,
    "subject": subject}} from scanning every commit body of `git log`
    (newest first) against TRAILER_RE; when a pair is named by more than
    one commit the newest wins. Insertion order IS recency order — the
    first entry inserted comes from the newest trailer-carrying commit,
    which is what derive's `newest` reads. Membership tests and (slug, n)
    key iteration keep the old set semantics. Empty dict on git failure
    (e.g. a zero-commit repo) — never an exception."""
    result = subprocess.run(
        ["git", "-C", root, "log", "--format=%x01%h%x02%s%x02%B"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {}

    evidence = {}
    for record in result.stdout.split("\x01"):
        if not record:
            continue
        parts = record.split("\x02", 2)
        if len(parts) != 3:
            continue
        sha, subject, body = parts
        for line in body.splitlines():
            m = TRAILER_RE.match(line)
            if m:
                key = (m.group(1), int(m.group(2)))
                if key not in evidence:
                    evidence[key] = {"sha": sha, "subject": subject}
    return evidence


def piece_strip_for(root, slug, evidence):
    """One A5 piece_strips entry for `slug`. Mapping per A1: mode is 'trailer' when
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

        ev = evidence.get((slug, n))
        pieces.append({
            "n": n, "text": text,
            "checked_worktree": checked_wt, "checked_head": checked_head,
            "state": state,
            "evidence_sha": ev["sha"] if ev else None,
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
    e_idx = len(gates_kit.RUNGS) if enters_at == "ready-to-release" \
        else gates_kit.RUNGS.index(enters_at)
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
            "have_items": list(r["have"]), "need_items": list(r["need"]),
            "agreed": agreed,
        })

    return {"slug": slug, "bypass": False, "enters_at": enters_at, "rungs": rungs}


def derive(root):
    """The full model: audit_problems, newest, slugs, board, piece_strips,
    drift."""
    gates_kit = load_gates_kit()
    slugs = discover_slugs(root)
    evidence = piece_evidence(root)

    board = [board_for(root, slug, gates_kit) for slug in slugs]
    piece_strips = [piece_strip_for(root, slug, evidence) for slug in slugs]

    drift = []
    for g in piece_strips:
        for p in g["pieces"]:
            if p["state"] == "landed" and not p["checked_worktree"]:
                drift.append(
                    f"{g['slug']}/{p['n']} — landed in git, box unchecked in working tree"
                )

    return {
        "audit_problems": len(gates_kit.audit(root)),
        "newest": next(iter(evidence.values())) if evidence else None,
        "slugs": slugs,
        "board": board,
        "piece_strips": piece_strips,
        "drift": drift,
    }


FIX_LINE = ("run: python3 tools/diagram/progress.py && "
            "git add docs/plans/progress.excalidraw "
            "docs/plans/progress.svg docs/plans/progress.html && git commit")


def write_surfaces(model, canvas, dir_path):
    """Serialize the committed view surfaces — progress.excalidraw,
    progress.svg, progress.html — into `dir_path`. The ONLY serializer
    of the trio: the render and the stale check both write through here,
    so the byte-compare can never be defeated by two drifting
    serializations. Returns (excalidraw_path, svg_path, html_path, w, h)."""
    os.makedirs(dir_path, exist_ok=True)
    doc = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": canvas.els,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    out = os.path.join(dir_path, "progress.excalidraw")
    with open(out, "w") as f:
        json.dump(doc, f, indent=2)
    svg_out = os.path.join(dir_path, "progress.svg")
    w, h = to_svg(canvas.els, svg_out)
    html_out = os.path.join(dir_path, "progress.html")
    with open(html_out, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_html(model))
    return out, svg_out, html_out, w, h


def stale(root):
    """Check-only staleness verdict: render the trio to a temp directory
    (never the working tree) and byte-compare each file against the
    committed surfaces on disk under `root`. Returns
    (0, ["render current"]) when all three are identical; else
    (1, lines) — 'stale: <relpath>' / 'missing: <relpath>' per file —
    excalidraw, then svg, then html — FIX_LINE last. Mutates nothing
    under `root`."""
    model = derive(root)
    canvas = build_canvas(model)
    problems = []
    with tempfile.TemporaryDirectory() as td:
        tmp_ex, tmp_svg, tmp_html, _w, _h = write_surfaces(model, canvas, td)
        for tmp, rel in ((tmp_ex, "docs/plans/progress.excalidraw"),
                         (tmp_svg, "docs/plans/progress.svg"),
                         (tmp_html, "docs/plans/progress.html")):
            committed = os.path.join(root, rel)
            if not os.path.exists(committed):
                problems.append(f"missing: {rel}")
                continue
            with open(tmp, "rb") as a, open(committed, "rb") as b:
                if a.read() != b.read():
                    problems.append(f"stale: {rel}")
    if not problems:
        return 0, ["render current"]
    return 1, problems + [FIX_LINE]


def render_table(model):
    """A6: the terminal pull, exact. Board glyphs: '#' built, '>'
    in-flight, '. need <n>' missing, with ' G' appended when agreed.
    A bypass (spike) slug renders one 'SPIKE <slug> — ladder bypassed'
    line in place of board cells; its piece strip is unaffected. Piece
    glyphs: '#' landed, '>' in flight, '.' remaining, one per piece in
    order. An empty model (no slugs on disk) renders a single
    'no work orders on disk' line in place of BOARD/PIECES."""
    lines = [
        "progress — derived from disk: git log · gate route · "
        "Pieces checklists · docs/gates/",
    ]
    if model["audit_problems"] == 0:
        lines.append("audit: clean")
    else:
        lines.append(f"audit: {model['audit_problems']} problem{'' if model['audit_problems'] == 1 else 's'}")
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

    slug_width = max(len(g["slug"]) for g in model["piece_strips"])
    rows = []
    for g in model["piece_strips"]:
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
            f"PIECES  {slug.ljust(slug_width)}  {strip.ljust(strip_width)}  {message}"
        )

    lines.append("")

    if model["drift"]:
        for d in model["drift"]:
            lines.append(f"drift: {d}")
    else:
        lines.append("drift: none")

    return "\n".join(lines)


def build_canvas(model):
    """A7: title, legend, board grid, piece strips, drift lines — the drawing
    on the live canvas. Returns the kit.Canvas; writes nothing
    (write_surfaces owns the .excalidraw/.svg/.html serialization; the
    render and the stale check both write through it)."""
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

    # ── piece strips ─────────────────────────────────────────────────────
    for g in model["piece_strips"]:
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


_CSS = (
    "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', "
    "Roboto, Helvetica, Arial, sans-serif; color: " + INK + "; "
    "max-width: 960px; margin: 0 auto; padding: 24px 20px 60px; "
    "line-height: 1.5; }"
    "h1, h2 { font-weight: 600; }"
    "h2 { margin-top: 40px; border-bottom: 1px solid " + GREY + "; "
    "padding-bottom: 6px; }"
    ".fresh, .audit, .legend { font-size: 14px; }"
    ".red { color: " + RED + "; }"
    ".green { color: " + GREEN + "; }"
    "table { border-collapse: collapse; margin: 16px 0; }"
    "th, td { border: 1px solid " + GREY + "; padding: 6px 12px; "
    "font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; "
    "text-align: left; }"
    ".strip, .sha { font-family: ui-monospace, SFMono-Regular, Menlo, "
    "Consolas, monospace; }"
    ".piece-strip { border-top: 1px solid " + GREY + "; padding: 12px 0; }"
    ".piece-strip-head { cursor: pointer; display: flex; gap: 16px; "
    "align-items: baseline; }"
    ".slug { font-weight: 600; }"
    ".piece-strip .detail { display: none; padding: 8px 0 4px 16px; }"
    ".piece-strip.open .detail { display: block; }"
    ".piece, .rung-name, .have, .need, .spike { margin: 4px 0; }"
    ".rung-name { font-weight: 600; }"
)


_JS = ("document.querySelectorAll('.piece-strip-head').forEach(function (h) { "
       "h.addEventListener('click', function () { "
       "h.parentNode.classList.toggle('open'); }); });")


def render_html(model):
    """The self-contained progress page (docs/design/progress-html.md):
    header + freshness line, board grid, piece strips with click-to-expand
    detail, drift; model inlined as a JSON block. Pure function of
    `model` — no time, no HEAD, no randomness, no set iteration; every
    model-derived string is HTML-escaped."""
    e = html.escape
    canonical = json.dumps(model, sort_keys=True, separators=(",", ":"))
    fingerprint = hashlib.md5(canonical.encode("utf-8")).hexdigest()

    if model["newest"] is not None:
        fresh = ("newest landed piece: " + e(model["newest"]["sha"]) + " — "
                 + e(model["newest"]["subject"]) + " · state " + fingerprint)
    else:
        fresh = "no landed pieces yet · state " + fingerprint

    out = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Progress — derived from disk</title>",
        "<style>", _CSS, "</style>",
        "</head>",
        "<body>",
        "<h1>Progress — derived from disk</h1>",
        '<p class="fresh">' + fresh + "</p>",
    ]

    if model["audit_problems"] == 0:
        out.append('<p class="audit">audit: clean</p>')
    else:
        out.append('<p class="audit red">audit: '
                   + str(model["audit_problems"]) + " problems</p>")

    if not model["slugs"]:
        out.append("<p>no work orders on disk</p>")
    else:
        non_bypass = [b for b in model["board"] if not b["bypass"]]
        bypass = [b for b in model["board"] if b["bypass"]]

        out.append("<h2>BOARD</h2>")
        out.append('<p class="legend">[G] agreed · [#] built · '
                   "[&gt;] in-flight · [.] missing</p>")
        if non_bypass:
            out.append("<table>")
            out.append("<tr><th>rung</th>"
                       + "".join("<th>" + e(b["slug"]) + "</th>" for b in non_bypass)
                       + "</tr>")
            rung_names = [r["rung"] for r in non_bypass[0]["rungs"]]
            for ridx, rung_name in enumerate(rung_names):
                cells = []
                for b in non_bypass:
                    r = b["rungs"][ridx]
                    if r["state"] == "built":
                        text, cls = "#", "built"
                    elif r["state"] == "in-flight":
                        text, cls = "&gt;", "inflight"
                    else:
                        text, cls = ". need " + str(r["need"]), "red"
                    if r["agreed"]:
                        text += ' <span class="green">G</span>'
                    cells.append('<td class="' + cls + '">' + text + "</td>")
                out.append("<tr><th>" + e(rung_name) + "</th>"
                           + "".join(cells) + "</tr>")
            out.append("</table>")
        for b in bypass:
            out.append('<p class="spike">SPIKE ' + e(b["slug"])
                       + " — ladder bypassed</p>")

        out.append("<h2>PIECES</h2>")
        board_by_slug = {b["slug"]: b for b in model["board"]}
        for g in model["piece_strips"]:
            out.append('<div class="piece-strip">')
            head = ['<div class="piece-strip-head"><span class="slug">'
                    + e(g["slug"]) + "</span>"]
            if g["contract"] is None:
                head.append('<span class="red">no contract on disk</span>')
            elif g["counts"] is None:
                head.append('<span class="red">no Pieces checklist in '
                            + e(g["contract"]) + "</span>")
            else:
                strip = []
                for p in g["pieces"]:
                    if p["state"] == "landed":
                        strip.append("#")
                    elif p["state"] == "in flight":
                        strip.append("&gt;")
                    else:
                        strip.append('<span class="red">.</span>')
                c = g["counts"]
                head.append('<span class="strip">' + "".join(strip) + "</span>")
                head.append('<span class="counts">' + str(c["landed"])
                            + " landed · " + str(c["in_flight"])
                            + " in flight · " + str(c["remaining"])
                            + " remaining</span>")
            head.append("</div>")
            out.append("".join(head))

            detail = ['<div class="detail">']
            for p in g["pieces"]:
                line = str(p["n"]) + " [" + e(p["state"]) + "] " + e(p["text"])
                if p["evidence_sha"] is not None:
                    line += ' · <span class="sha">' + e(p["evidence_sha"]) + "</span>"
                detail.append('<p class="piece">' + line + "</p>")
            b = board_by_slug[g["slug"]]
            if b["bypass"]:
                detail.append('<p class="spike">SPIKE — ladder bypassed</p>')
            else:
                for r in b["rungs"]:
                    detail.append('<p class="rung-name">' + e(r["rung"]) + "</p>")
                    for item in r["have_items"]:
                        detail.append('<p class="have">have: ' + e(item) + "</p>")
                    for item in r["need_items"]:
                        detail.append('<p class="need red">need: ' + e(item) + "</p>")
            detail.append("</div>")
            out.append("".join(detail))
            out.append("</div>")

        out.append("<h2>DRIFT</h2>")
        if model["drift"]:
            for d in model["drift"]:
                out.append('<p class="red">drift: ' + e(d) + "</p>")
        else:
            out.append("<p>drift: none</p>")

    out.append('<script type="application/json" id="progress-data">'
               + canonical.replace("</", "<\\/") + "</script>")
    out.append("<script>" + _JS + "</script>")
    out.append("</body>")
    out.append("</html>")
    return "\n".join(out) + "\n"


# ── selftest ─────────────────────────────────────────────────────────────
#
# Part B fixtures (F1-F10; F11-F13 from the push-wiring spec, amended to
# the trio, and F14 added by the progress-html spec): the gates' own
# fixture idiom (tools/gates/kit.py's _selftest_body), plus git — each
# case builds its tree in a tempfile.TemporaryDirectory, `git init`s it,
# and commits with an explicit identity, because CI runners carry no git
# identity and a bare `git commit` fails there. Slug 'alpha', contract
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


def _piece_strip(model, slug=_ST_SLUG):
    return next(g for g in model["piece_strips"] if g["slug"] == slug)


def _board(model, slug=_ST_SLUG):
    return next(b for b in model["board"] if b["slug"] == slug)


def _piece(strip, n):
    return next(p for p in strip["pieces"] if p["n"] == n)


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
        assert piece_evidence(d) == {}, "expected empty evidence on a zero-commit repo"
        assert head_text(d, _ST_CONTRACT_REL) is None, \
            "expected head_text None on a zero-commit repo"
        model = derive(d)
        g = _piece_strip(model)
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
        g = _piece_strip(model)
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
        g = _piece_strip(model)
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
        g = _piece_strip(model)
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
        g = _piece_strip(model)
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
        g = _piece_strip(model)
        assert _piece(g, 2)["state"] == "landed", f"piece 2: {_piece(g, 2)}"
        expected = "alpha/2 — landed in git, box unchecked in working tree"
        assert expected in model["drift"], f"expected drift line {expected!r}, got {model['drift']}"


_F8_PRODUCT = (
    "---\nroute: new\nstage: framed\n---\n\n"
    "## Value\n\nSaves 10 hours a week across the team.\n\n"
    "## Risk ledger\n\n"
    "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |\n"
    "|---|---|---|---|---|---|---|---|---|---|\n"
    "| Adoption risk | yes | high | medium |  |  | accepted |  |  |  |\n"
)


def _mk_f8_tree(d):
    """docs/product/alpha.md with legal front matter, a Value section, and
    a named-but-unqualified killer ledger row, committed — enough for
    gates routing to place alpha at viability (frame's inputs are
    satisfied trivially; viability's killer-presence check passes on the
    named row, but scope's full ledger qualification does not)."""
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
        assert by_rung["scope"]["state"] == "missing", by_rung["scope"]
        assert by_rung["scope"]["need"] >= 1, by_rung["scope"]


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


def _f11():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        model = derive(d)
        canvas = build_canvas(model)
        write_surfaces(model, canvas, os.path.join(d, "docs", "plans"))
        _git_commit(d, "render trio")
        code, lines = stale(d)
        assert code == 0, f"expected exit 0, got {code}: {lines}"
        assert lines == ["render current"], lines
        assert _git(d, "status", "--porcelain") == "", \
            "stale mutated the fixture tree"


def _f12():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        _sw(os.path.join(d, _ST_CONTRACT_REL), _pieces_md([False, False, False]))
        _git_commit(d, "add alpha contract, all unchecked")
        model = derive(d)
        canvas = build_canvas(model)
        write_surfaces(model, canvas, os.path.join(d, "docs", "plans"))
        _git_commit(d, "render trio")
        _sw(os.path.join(d, _ST_CONTRACT_REL), _pieces_md([True, False, False]))
        code, lines = stale(d)
        assert code == 1, f"expected exit 1, got {code}: {lines}"
        assert lines == [
            "stale: docs/plans/progress.excalidraw",
            "stale: docs/plans/progress.svg",
            "stale: docs/plans/progress.html",
            "run: python3 tools/diagram/progress.py && git add "
            "docs/plans/progress.excalidraw docs/plans/progress.svg "
            "docs/plans/progress.html && git commit",
        ], lines


def _f13():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        code, lines = stale(d)
        assert code == 1, f"expected exit 1, got {code}: {lines}"
        assert lines == [
            "missing: docs/plans/progress.excalidraw",
            "missing: docs/plans/progress.svg",
            "missing: docs/plans/progress.html",
            FIX_LINE,
        ], lines


def _f14():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        with tempfile.TemporaryDirectory() as ta, \
                tempfile.TemporaryDirectory() as tb:
            model_a = derive(d)
            first = write_surfaces(model_a, build_canvas(model_a), ta)
            model_b = derive(d)
            second = write_surfaces(model_b, build_canvas(model_b), tb)
            for pa, pb in zip(first[:3], second[:3]):
                with open(pa, "rb") as a, open(pb, "rb") as b:
                    assert a.read() == b.read(), \
                        f"consecutive generations differ: {os.path.basename(pa)}"


def _f15():
    """board: ready-to-release terminal — all rungs built. A full tree
    that clears every rung (frame through acceptance) plus the derived
    terminal's own evidence (an acceptance record and the CI workflow),
    per D4: `route()` reports enters_at == "ready-to-release", and
    `board_for`'s e_idx fix (len(RUNGS), not RUNGS.index(...), which
    would raise ValueError on a name that isn't a rung) must render all
    seven rungs 'built' with no in-flight cell."""
    ledger_good = (
        "---\nroute: new\nstage: framed\n---\n\n"
        "## Value\n\nSaves 10 hours/week.\n\n"
        "## Risk ledger\n\n"
        "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n"
        "| Adoption risk | yes | high | medium | 3 interviews | non-fatal | accepted |  |  | check Q2 |\n"
        "| Perf risk | no | medium | low | benchmark done | non-fatal | countermeasure - permanent | caching added |  |  |\n"
    )
    product_text = ledger_good + "\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n"
    spec_text = (
        "# Alpha — build spec\n\n"
        "## Pieces\n\n"
        "- [x] Step 1\n\n"
        "### Step 1: do the thing\n"
        "**What:** do it.\n"
        "**Verify:** `true`\n"
    )
    with tempfile.TemporaryDirectory() as d:
        _git_init(d)
        _sw(os.path.join(d, "docs", "product", f"{_ST_SLUG}.md"), product_text)
        _sw(os.path.join(d, "docs", "design", f"{_ST_SLUG}.md"), "# Alpha design\n\nHow it works.\n")
        _sw(
            os.path.join(d, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nDesign approved.\n",
        )
        _sw(os.path.join(d, _ST_CONTRACT_REL), spec_text)
        _sw(
            os.path.join(d, "docs", "gates", "2026-01-03-alpha-acceptance.md"),
            "---\nroute: new\nstage: ready-to-release\n---\n\n"
            "## Release condition\n\nAll steps verified and merged.\n",
        )
        _sw(os.path.join(d, ".github", "workflows", "gate.yml"), "name: entry-gate\n")
        _git_commit(d, "alpha clears every rung to ready-to-release")

        model = derive(d)
        b = _board(model)
        assert b["enters_at"] == "ready-to-release", \
            f"expected enters_at ready-to-release, got {b['enters_at']!r}"
        for r in b["rungs"]:
            assert r["state"] == "built", f"{r['rung']}: expected built, got {r}"
        render_table(model)  # must not raise


def selftest():
    """Part B: F1-F15, each built fresh in its own temp tree (git init +
    committed history, per case). Prints one 'ok <n> — <name>' line per
    case; on the first failed assertion prints 'FAIL <n> — <name>: <why>'
    and returns 1. On full success prints 'selftest: 15 ok' and returns 0.

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
        (_f8, "board: frame built, viability in-flight, scope missing"),
        (_f9, "agreed overlay: a docs/gates GO record marks only its own rung"),
        (_f10, "canvas layout checks clean on the F8 model"),
        (_f11, "stale: converged tree — render current, exit 0"),
        (_f12, "stale: drifted tree — exit 1 naming all three files and the verbatim fix"),
        (_f13, "stale: missing trio — exit 1 naming all three missing files"),
        (_f14, "determinism: two consecutive write_surfaces runs byte-identical"),
        (_f15, "board: ready-to-release terminal — all rungs built"),
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
    print("selftest: 15 ok")
    return 0
