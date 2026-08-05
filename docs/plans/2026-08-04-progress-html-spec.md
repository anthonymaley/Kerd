---
route: new
stage: contracted
---

# Progress HTML — build spec (the score)

Contract for the piece `progress-html`, release slice 1: the committed,
self-contained page `docs/plans/progress.html` joins the render as the
third surface. `write_pair` becomes `write_surfaces(model, canvas,
dir_path)` — the single serializer of ALL committed view surfaces — the
byte-compare set grows from the pair to the trio, and the page carries a
model-derived freshness line (newest landed-piece commit + md5 state
fingerprint — never HEAD, never timestamps).

Design source: `docs/design/progress-html.md`. Parent:
`docs/design/progress-view.md`. Sibling amended by this build:
`docs/design/push-wiring.md` (its "both files" language becomes the trio).

Out of scope: live refresh / watch mode / any server / any control that
mutates · replacing the SVG or terminal surfaces · skill files · README
and both capability-list descriptions · `tools/diagram/gen_progress_html.py`
(the design's own diagram generator) · stage bookkeeping in
`docs/product/progress-html.md`.

Piece-to-step mapping: piece 1 = Step 1 · piece 2 = Step 2 · piece 3 =
Steps 4+5 · piece 4 = Step 6. Step 3 (review) belongs to no piece. Piece
numbers are positional in the `## Pieces` checklist below; `Piece:
progress-html/<n>` trailers must use those positions.

---

## Part A — definitions this spec settles

### A1. `write_surfaces` and the single-serializer rule

`progress_kit.write_pair(canvas, dir_path)` is RENAMED and grown to:

```
write_surfaces(model, canvas, dir_path)
  -> (excalidraw_path, svg_path, html_path, w, h)
```

It writes `progress.excalidraw`, `progress.svg`, and `progress.html`
into `dir_path` — the ONLY serializer of the trio. The render
(`progress.py:_cmd_render`) and `stale` both write through it; the
byte-compare set is whatever it writes, so the trio is covered by the
existing seventh CI step with NO workflow change. `model` joins the
signature because the HTML needs data the canvas does not carry. After
this build, `grep -c write_pair tools/diagram/progress.py
tools/diagram/progress_kit.py` is 0 and 0 — no alias, no wrapper.

### A2. Output strings (exact)

`FIX_LINE` grows to stage all three files. The evaluated value, verbatim,
single line, no trailing punctuation:

```
run: python3 tools/diagram/progress.py && git add docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html && git commit
```

`stale` exit 0 still prints exactly `render current`. Exit 1 prints one
line per differing/missing file in FILE order — `progress.excalidraw`,
then `progress.svg`, then `progress.html` — each `stale: <relpath>` or
`missing: <relpath>` (a file is stale or missing, never both; identical →
no line), then the fix line last. Exit codes unchanged: 0 current, 1 any
difference or any file missing, 2 usage (`stale --json` stays a usage
error).

### A3. Model growth (all additive — no key removed, renamed, or retyped)

The HTML inlines everything at generation, and `write_surfaces` has no
`root` parameter, so every datum the page needs must ride in the model:

1. **`piece_evidence(root)` returns a dict, no longer a set:**
   `{(slug, n): {"sha": <short-sha>, "subject": <subject>}}`, scanning
   `git log` newest-first; when a pair is named by more than one commit
   the NEWEST wins (first seen). Dict insertion order IS recency order —
   the first entry inserted comes from the newest trailer-carrying
   commit. Membership tests and `(s, n)` key iteration keep the old set
   semantics, so `goal_for` needs no logic change. Empty dict on git
   failure — never an exception.
2. **`model["newest"]`** — `{"sha": ..., "subject": ...}` of the newest
   landed-piece commit (`next(iter(evidence.values()))`), or `None` when
   no trailer commit exists. This is the freshness anchor: render-only
   commits carry no trailer, so it converges by construction.
3. **`goals[].pieces[]` gain `"evidence_sha"`** — the trailer commit's
   short sha, or `None` (legacy-mode landings have no trailer commit).
4. **`board[].rungs[]` gain `"have_items"` and `"need_items"`** — the
   gate route's named have/need line lists, verbatim, from the
   `route_result` `board_for` already holds in-process. The existing
   `"have"`/`"need"` COUNTS stay untouched (F8 compares `need >= 1`;
   `render_table`/`build_canvas` read the counts).

**Forced fixture amendment, named:** F2 asserts
`piece_evidence(d) == set()`; the container type change makes that
`piece_evidence(d) == {}` (message text: "expected empty evidence on a
zero-commit repo"). This is the ONE touch outside F11–F14, it is one
token plus the message, and it lands in Step 1 with the type change.

### A4. Determinism and the freshness fingerprint (exact canonicalization)

The page must be BYTE-DETERMINISTIC: no HEAD, no timestamps, no
randomness, no unsorted iteration. `render_html(model)` is a pure
function of the model — every varying byte derives from `model` alone.

- **Canonical model JSON:**
  `json.dumps(model, sort_keys=True, separators=(",", ":"))` — exactly
  those arguments, nothing else.
- **State fingerprint:**
  `hashlib.md5(canonical.encode("utf-8")).hexdigest()` — full 32 hex
  chars, shown in the freshness line. The fingerprint is computed FROM
  the model, never stored IN it (no self-reference).
- **Inlined data block:**
  `<script type="application/json" id="progress-data">` +
  `canonical.replace("</", "<\\/")` + `</script>`. The `</` escape keeps
  any embedded `</script>` from terminating the block; it is applied to
  the block only — the fingerprint hashes the UNescaped canonical string.
- **Escaping:** every model-derived string interpolated into markup goes
  through `html.escape` (stdlib `html` module).
- **Iteration:** model lists in stored order (already slug-sorted) or
  `sorted(...)` — NEVER iterate a set or an unsorted `os.listdir`
  anywhere in the html path. Same-process F14 cannot catch
  hash-seed-dependent set ordering; Step 2's verify adds a two-process
  generate-and-`cmp` for exactly that hole. Cross-platform byte-identity
  (Mac committed vs Linux fresh) stays proven only by the first green CI
  run on the pushed SHA — same residual, same named fallback as
  push-wiring: normalize-before-compare in a follow-up, never a semantic
  diff.

### A5. The page (structure and exact strings)

Self-contained: one `<!doctype html>` document, inline CSS, inline
vanilla JS, zero external requests of any kind, works cold over
`file://`. System font stack. Colour grammar: page colours interpolate
the kit constants — base text `INK`, `.red` = `RED`, `.green` = `GREEN`,
borders/fills `GREY`. RED marks missing/cost ONLY (missing cells, need
lines, drift, nonzero audit, no-contract/no-checklist notes, remaining
glyphs); agreed `G` is green; nothing else is coloured.

- **Header:** `<h1>Progress — derived from disk</h1>`, then the
  freshness line — with `newest`:
  `newest landed piece: <sha> — <subject> · state <fingerprint>`;
  without: `no landed pieces yet · state <fingerprint>` — then
  `audit: clean` or `audit: <n> problems` (red when nonzero).
- **Board:** legend `[G] agreed · [#] built · [>] in-flight · [.] missing`;
  a rung × slug table, cells `#` (built), `>` (in-flight),
  `. need <n>` (missing, red), with ` G` appended (green) when agreed.
  Bypass slugs render no column — one line each:
  `SPIKE <slug> — ladder bypassed`.
- **Goal strips:** one `.goal` block per goal, in model order. Header row
  (`.goal-head`, click target): slug · glyph strip (`#` landed, `>` in
  flight, `.` remaining in red) · counts
  `<l> landed · <i> in flight · <r> remaining`. Degenerate goals show
  `no contract on disk` / `no Pieces checklist in <contract>` in red.
- **Click a goal → detail panel** (`.detail`, hidden until `.open`): its
  pieces — `<n> [<state>] <text>` plus ` · <sha>` when `evidence_sha` is
  non-null — then, per rung of that slug's board entry, the rung name and
  the gate's named lines verbatim: `have: <item>` / `need: <item>` (need
  in red). A bypass slug's panel shows `SPIKE — ladder bypassed`.
- **Drift:** one red `drift: <line>` per model drift entry, else
  `drift: none`.
- **Empty model:** `no work orders on disk` in place of board/goals.
- **JS:** expand/collapse toggles ONLY — one delegated click handler
  toggling `.open` on the clicked goal. Nothing polls, nothing mutates,
  nothing refreshes.

### A6. Fixtures — F2 token, F11–F13 amended, F14 new

Selftest total becomes 14; final line `selftest: 14 ok`.

| # | Change | Assert |
|---|---|---|
| F2 | forced token (A3) | `piece_evidence(d) == {}` |
| F11 | `write_surfaces(model, canvas, ...)` replaces the `write_pair` call | unchanged: `(0, ["render current"])`, porcelain empty |
| F12 | same call replacement | `(1, [...])` — exactly THREE `stale:` lines (excalidraw, svg, html) then the fix line as a SPELLED-OUT literal, never the `FIX_LINE` constant |
| F13 | none needed beyond expectation | `(1, [...])` — exactly THREE `missing:` lines then `FIX_LINE` (the constant here, mirroring push-wiring's deliberate F12/F13 asymmetry) |
| F14 | NEW | two consecutive generations byte-identical: derive + build_canvas + `write_surfaces` run twice into two temp dirs, all three files compared as bytes |

F12's literal-not-constant rule stands: asserting the constant against
itself proves nothing.

### A7. The ship flow and its trap

Same trap as push-wiring (A7 there): this build's own edits — this spec
file, checked boxes, trailers — change the derived render, and
`progress.html` has never been committed at all. Way-one refusal on the
real tree therefore has a MIXED verdict, spelled here so nobody misreads
the missing-line as a defect:

```
stale: docs/plans/progress.excalidraw
stale: docs/plans/progress.svg
missing: docs/plans/progress.html
run: python3 tools/diagram/progress.py && git add docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html && git commit
```

Ship sequence is fixed: work commit (trailers 1–3, boxes 1–3 checked) →
way-one refusal (above, exit 1) → refresh → render commit staging ALL
THREE surfaces, NO trailer (render-only commits carry no trailer — that
is what keeps the freshness anchor and the byte-compare convergent) →
way-two (`render current`, exit 0) → ONE push → CI green on the pushed
SHA, all seven steps — no new step; the seventh compares the trio
because `stale` compares whatever `write_surfaces` writes. Piece 4's
trailer lands only after CI verifies, so the record round repeats the
shape: record commit → refresh → render commit → one push → CI green.
Ship is structurally two push rounds. After the final green: hand
`/Users/anthonymaley/Kerd/docs/plans/progress.html` to Tony for the cold
`file://` open — the expert-user acceptance of the product's first Value
row (human step, outside CI).

### A8. Version and release rules

`0.78.0` → `0.79.0` (MINOR: new feature) in exactly three places:
`.claude-plugin/plugin.json` `version`, `.claude-plugin/marketplace.json`
`metadata.version`, `.claude-plugin/marketplace.json`
`plugins[0].version`. NO change to either capability-list `description`
(repo-internal tooling, not a plugin capability), no
`metadata.description` change, no README change.
`python3 tools/gates/gate.py release` must print `release: clean`.

### A9. Cross-doc amendment (exact text and location)

In `/Users/anthonymaley/Kerd/docs/design/push-wiring.md`, at the END of
the section `## The stale subcommand` (immediately after the paragraph
ending `prints usage, exit 2.`), insert a blank line and this one
paragraph, verbatim:

```
*(Amended by the `progress-html` build, 2026-08-04: `write_pair` became
`write_surfaces`, and the compare set grew from the pair to the trio —
`docs/plans/progress.{excalidraw,svg,html}`. Read "both files" here as
"all three"; the fix line now stages all three files.)*
```

No other edit to that file — living-doc amendment pattern, matching its
existing goal-gate note.

---

## Part B — implementation shape (exact)

### progress_kit.py — imports

The stdlib import block gains `hashlib` and `html` (alphabetical order):
`glob, hashlib, html, importlib.util, json, os, re, subprocess, sys,
tempfile`.

### progress_kit.py — piece_evidence (full replacement)

```python
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
```

### progress_kit.py — goal_for (one block replaced)

The `pieces.append({...})` call becomes:

```python
        ev = evidence.get((slug, n))
        pieces.append({
            "n": n, "text": text,
            "checked_worktree": checked_wt, "checked_head": checked_head,
            "state": state,
            "evidence_sha": ev["sha"] if ev else None,
        })
```

### progress_kit.py — board_for (one block replaced)

The `rungs.append({...})` call becomes:

```python
        rungs.append({
            "rung": rung_name, "state": state,
            "have": len(r["have"]), "need": len(r["need"]),
            "have_items": list(r["have"]), "need_items": list(r["need"]),
            "agreed": agreed,
        })
```

### progress_kit.py — derive (return block replaced; docstring lists the new key)

```python
    return {
        "audit_problems": len(gates_kit.audit(root)),
        "newest": next(iter(evidence.values())) if evidence else None,
        "slugs": slugs,
        "board": board,
        "goals": goals,
        "drift": drift,
    }
```

Docstring: "The full model: audit_problems, newest, slugs, board, goals,
drift."

### progress_kit.py — FIX_LINE, write_surfaces, stale (replace write_pair and stale wholesale)

```python
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
```

`build_canvas`'s docstring parenthetical becomes: "(write_surfaces owns
the .excalidraw/.svg/.html serialization; the render and the stale check
both write through it)".

### progress_kit.py — the page (place after build_canvas, before the selftest block)

`_CSS` and `_JS` module constants plus `render_html(model)`. `render_html`
verbatim:

```python
def render_html(model):
    """The self-contained progress page (docs/design/progress-html.md):
    header + freshness line, board grid, goal strips with click-to-expand
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

        out.append("<h2>GOALS</h2>")
        board_by_slug = {b["slug"]: b for b in model["board"]}
        for g in model["goals"]:
            out.append('<div class="goal">')
            head = ['<div class="goal-head"><span class="slug">'
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
```

`_JS` verbatim:

```python
_JS = ("document.querySelectorAll('.goal-head').forEach(function (h) { "
       "h.addEventListener('click', function () { "
       "h.parentNode.classList.toggle('open'); }); });")
```

`_CSS` is a single string constant built with `+ INK +` / `+ RED +` /
`+ GREEN +` / `+ GREY +` concatenation of the kit colour constants (no
other colour literals for content). Required rules — layout beyond them
is the player's, kept plain: body uses the system font stack
(`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica,
Arial, sans-serif`), base colour `INK`, readable max-width; `.red`
colour `RED`; `.green` colour `GREEN`; table borders `GREY`, cells and
`.strip`/`.sha` in a ui-monospace stack; `.goal-head { cursor: pointer }`;
`.goal .detail { display: none }`; `.goal.open .detail { display: block }`.
No `@import`, no `url(...)`, no external anything.

### progress.py — changes

1. Docstring render line becomes:
   `python3 tools/diagram/progress.py [--json]   # render: writes docs/plans/progress.{excalidraw,svg,html}; prints table (or the model as JSON)`
   The stale line and the prose paragraph swap "committed pair" for
   "committed trio" (both occurrences).
2. In `_cmd_render`, the write call becomes:

```python
    out, svg_out, html_out, w, h = progress_kit.write_surfaces(
        model, canvas, os.path.join(progress_kit.REPO, "docs", "plans"))
```

3. After the `print("wrote", svg_out, ...)` line, add:

```python
    print("wrote", html_out)
```

Nothing else in progress.py changes.

### Fixtures (Step 1 makes the F2 token; Step 2 copies the rest)

F2, one assertion amended:

```python
        assert piece_evidence(d) == {}, "expected empty evidence on a zero-commit repo"
```

F11–F14, full bodies:

```python
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
```

Case-list entries — F12/F13 lines REPLACED (their names change), F14
appended:

```python
        (_f11, "stale: converged tree — render current, exit 0"),
        (_f12, "stale: drifted tree — exit 1 naming all three files and the verbatim fix"),
        (_f13, "stale: missing trio — exit 1 naming all three missing files"),
        (_f14, "determinism: two consecutive write_surfaces runs byte-identical"),
```

Final print becomes `selftest: 14 ok`; the `selftest()` docstring count
becomes F1–F14 / 14; the fixture-block header comment becomes "(F1-F10;
F11-F13 from the push-wiring spec, amended to the trio, and F14 added by
the progress-html spec)".

---

## Standing cautions (every step, every player)

- `python3`, never `python`.
- **Never run bare `python3 tools/diagram/progress.py` (or `--json`)
  before Step 6** — both overwrite the committed surfaces in the working
  tree, and as of this build that is THREE files: the pair plus
  `docs/plans/progress.html`. If run by accident:
  `git checkout -- docs/plans/progress.excalidraw docs/plans/progress.svg`
  and `rm -f docs/plans/progress.html` (until Step 6's render commit the
  html is untracked, so checkout cannot restore it), then confirm with
  `git status --porcelain` on the three paths (empty).
- Run every Verify command and compare against EXPECTED. If actual
  contradicts expected: STOP and report actual vs expected — never
  self-judge PASS, never patch around it.
- Touch only the files your step names. Working directory for every
  command: `/Users/anthonymaley/Kerd`.
- Before re-dispatching any failed step: `git status --porcelain` first —
  a dead player can leave residue.

---

## Pieces

- [x] model growth: trailer evidence carries sha+subject, newest landed piece, evidence_sha per piece, named have/need per rung
- [x] write_surfaces trio: progress.html generation, FIX_LINE and stale grown to three files, fixtures F11-F14
- [x] cross-doc trio amendment in the push-wiring design + version 0.79.0
- [ ] shipped: both-ways refusal naming all three files, one push per round, CI green on the pushed SHA

---

## Steps

### Step 1: model growth in the derivation [delegate, model: sonnet, effort: medium]
**What:** Edit `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py` only, per Part A3/Part B: replace `piece_evidence` with the dict version (verbatim block); add `evidence_sha` to `goal_for`'s piece dict, `have_items`/`need_items` to `board_for`'s rung dict, and `newest` to `derive`'s return (verbatim blocks); update `derive`'s docstring; amend F2's assertion to `== {}` with the new message. Touch nothing else — `write_pair`, `stale`, and F11–F13 stay exactly as they are in this step.
**Why:** The container change is additive everywhere except F2's `== set()` equality — dict membership and key iteration preserve the old semantics, so `goal_for` and mode detection need no logic change. Insertion order is the recency channel `newest` reads; do not re-sort the evidence dict.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py selftest; echo "exit=$?"` → ends `selftest: 13 ok`, `exit=0`. Then `python3 - <<'EOF'` / `import sys; sys.path.insert(0, "tools/diagram"); import progress_kit as pk; m = pk.derive(pk.REPO); print("newest", m["newest"]); b = next(x for x in m["board"] if not x["bypass"]); print("rung", sorted(b["rungs"][0])); g = next(x for x in m["goals"] if x["pieces"]); print("piece", sorted(g["pieces"][0]))` / `EOF` → `newest` is a non-None dict with `sha` (short hex) and `subject`; rung keys include `have_items` and `need_items`; piece keys include `evidence_sha`. Then `git status --porcelain docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html` → empty (derive is read-only; nothing rendered).

### Step 2: write_surfaces, the page, fixtures F11–F14 [delegate, model: sonnet, effort: high]
**What:** Edit `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py` and `/Users/anthonymaley/Kerd/tools/diagram/progress.py` per Part A1/A2/A4/A5/A6 and Part B: imports (`hashlib`, `html`); `FIX_LINE`, `write_surfaces`, `stale` verbatim (write_pair GONE); `_CSS`/`_JS`/`render_html` after `build_canvas` (`render_html` verbatim, `_JS` verbatim, `_CSS` per its contract with kit colour constants); `build_canvas` docstring parenthetical; progress.py docstring, `write_surfaces` unpack, third `wrote` print; fixtures F11–F14 and case-list entries verbatim, final print `selftest: 14 ok`, docstring and header comment counts.
**Why:** The single-serializer rule is load-bearing: render and stale MUST share `write_surfaces`, and the html bytes are never asserted against a spec literal — only self-consistency — so hidden nondeterminism is the failure mode that matters. F14 runs in ONE process and cannot catch hash-seed-dependent set iteration; the two-process cmp below exists for exactly that hole. F12 spells the fix line as a literal on purpose.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py selftest; echo "exit=$?"` → contains `ok 12 — stale: drifted tree — exit 1 naming all three files and the verbatim fix`, `ok 14 — determinism: two consecutive write_surfaces runs byte-identical`, ends `selftest: 14 ok`, `exit=0`. Then `python3 tools/diagram/progress.py stale; echo "exit=$?"` → exactly the four A7 lines (`stale:` excalidraw, `stale:` svg, `missing:` html, the A2 fix line), `exit=1`; exit 0 here means the compare is broken: STOP. Then `python3 tools/diagram/progress.py stale --json; echo "exit=$?"` → usage text, `exit=2`. Then the two-process determinism cmp: `P=/private/tmp/claude-501/-Users-anthonymaley-Kerd/cc36aaf8-9e62-4e15-ae94-8fead64fe15e/scratchpad && python3 -c "import sys; sys.path.insert(0,'tools/diagram'); import progress_kit as pk; m=pk.derive(pk.REPO); pk.write_surfaces(m, pk.build_canvas(m), '$P/gen1')" && python3 -c "import sys; sys.path.insert(0,'tools/diagram'); import progress_kit as pk; m=pk.derive(pk.REPO); pk.write_surfaces(m, pk.build_canvas(m), '$P/gen2')" && cmp $P/gen1/progress.html $P/gen2/progress.html && cmp $P/gen1/progress.svg $P/gen2/progress.svg && cmp $P/gen1/progress.excalidraw $P/gen2/progress.excalidraw && echo TRIO-IDENTICAL` → `TRIO-IDENTICAL`. Then `grep -c write_pair tools/diagram/progress.py tools/diagram/progress_kit.py` → `0` and `0`; `git status --porcelain docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html` → empty; `python3 tools/gates/gate.py audit` → `audit: clean`.

### Step 3: diff review against Part A/B [keep]
**What:** Conductor reads the full Step 1–2 diff of both files against this spec line by line: one serializer (no envelope/`json.dump` of the doc outside `write_surfaces`; grep `write_pair` → nothing); `stale` writes only inside `TemporaryDirectory`; output strings byte-match A2/A7 including file order; F12's fix line is a spelled literal naming three files, F13 uses the constant; F2's amendment is exactly the one assertion; `render_html` is pure — no `time`/`datetime`/`random` import, no set iteration in the html path, `html.escape` on every interpolated model string, the `</` escape on the data block, canonical `json.dumps` args exact; model additions additive only (no key removed/renamed/retyped); `_CSS` uses kit constants, no external URL anywhere; no edits outside the two named files; Pieces boxes still unchecked. Then open `$P/gen1/progress.html` (Step 2's scratchpad copy — NOT a fresh repo render) in a browser for one sanity look: board glyphs, red only on missing/cost, goal click expands and collapses, freshness line shows sha + 32-hex state.
**Why:** The commands cannot catch a quietly duplicated serializer, a paraphrased string, or hash-seed-lucky set iteration — spec-drift review is the conductor's job; any miss → re-dispatch the owning step, never patch in review.
**Verify:** Checklist above fully ticked; `git diff --stat` names only `tools/diagram/progress.py` and `tools/diagram/progress_kit.py` (this spec file appears as untracked, not modified).

### Step 4: push-wiring design amendment [delegate, model: haiku, effort: low]
**What:** In `/Users/anthonymaley/Kerd/docs/design/push-wiring.md`, insert the A9 paragraph verbatim at the A9 location. No other edit — the original "both files" sentences stay; the amendment paragraph reinterprets them, matching the doc's existing goal-gate amendment pattern.
**Why:** Living design docs are amended in place with a named source, not rewritten — the trio reading must be traceable to this build.
**Verify:** `cd /Users/anthonymaley/Kerd && grep -c 'Amended by the .progress-html. build' docs/design/push-wiring.md` → `1`; `git diff --stat docs/design/push-wiring.md` → only that file, insertions only; `python3 tools/gates/gate.py audit` → `audit: clean`; `python3 tools/gates/gate.py release` → `release: clean`.

### Step 5: version 0.79.0 [delegate, model: haiku, effort: low]
**What:** Bump `"0.78.0"` → `"0.79.0"` in `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (`version`) and `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (`metadata.version` AND `plugins[0].version`). Touch nothing else in either file — all `description` fields stay byte-identical to what they are.
**Why:** MINOR bump: new feature (the third surface + grown refuser), no interface break. Repo-internal tooling is not a plugin capability, so the capability lists do not change.
**Verify:** `cd /Users/anthonymaley/Kerd && grep -c '"0.79.0"' .claude-plugin/plugin.json .claude-plugin/marketplace.json` → `1` and `2`; `grep -c '"0.78.0"' .claude-plugin/plugin.json .claude-plugin/marketplace.json` → `0` and `0`; `python3 tools/gates/gate.py release; echo "exit=$?"` → `release: clean`, `exit=0`.

### Step 6: ship — both-ways refusal, one push per round, CI on the SHA, record round [keep]
**What:** All commands from `/Users/anthonymaley/Kerd`, in this exact order. The trap this ordering defuses (A7): this build's own edits change the derived render and the html has never been committed — the refuser must not refuse its own birth commit, and way-one's verdict is MIXED (two stale + one missing), which is expected, not a defect.
1. Residue check: `git status --porcelain` → only the expected build files (`tools/diagram/progress.py`, `tools/diagram/progress_kit.py`, `docs/design/push-wiring.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and this spec file untracked). The three surface paths must NOT appear. Anything else → stop and report.
2. Local six: `python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit` → all exit 0, incl. `audit: clean`, `release: clean`, progress `selftest: 14 ok`.
3. In this spec file, flip Pieces boxes 1–3 to `[x]` (box 4 stays unchecked — CI is not green yet; its trailer lands in the record round).
4. Work commit, staged by name: `git add tools/diagram/progress.py tools/diagram/progress_kit.py docs/design/push-wiring.md .claude-plugin/plugin.json .claude-plugin/marketplace.json docs/plans/2026-08-04-progress-html-spec.md` then commit with message `Progress HTML: the committed page joins the render trio` and body trailers `Piece: progress-html/1`, `Piece: progress-html/2`, `Piece: progress-html/3` (one per line; extra harness trailers are harmless — the trailer scan matches only `Piece:` lines).
5. Refusal, way one: `python3 tools/diagram/progress.py stale; echo "exit=$?"` → exactly the four A7 lines (`stale:` excalidraw, `stale:` svg, `missing:` html, the grown fix line), `exit=1`.
6. Refresh: `python3 tools/diagram/progress.py` → table shows `GOAL  progress-html` with strip `###.` and `3 landed · 0 in flight · 1 remaining`, `drift: none`, three `wrote` lines (excalidraw, svg, html), and the three no-fault lines (`no bound-text overflow`, `no text/box collisions`, `no text/text overlaps`). Any `!!` fault line → STOP, report (layout finding).
7. Render commit, NO trailer, all THREE surfaces: `git add docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html` then commit `Refresh progress render` — render-only commits carry no `Piece:` trailer; that is what keeps the freshness anchor and the byte-compare convergent.
8. Refusal, way two: `python3 tools/diagram/progress.py stale; echo "exit=$?"` → `render current`, `exit=0`. Then `git status --porcelain` → empty.
9. ONE push: `git push`.
10. CI on the pushed SHA: poll `gh run list --workflow=entry-gate --limit 1 --json status,conclusion,headSha` until `completed` — expect `success` and `headSha` equal to `git rev-parse HEAD`; `gh run view <run-id>` lists all seven steps green — no new step; `Progress render current` now compares the trio. If that step alone is red while local exit was 0, that is the cross-platform/cross-process determinism finding (A4): STOP and report — the named fallback is normalize-before-compare in a follow-up, never weakening to a semantic diff, never a hotfix inside this step.
11. Record round: flip box 4 to `[x]`; `git add docs/plans/2026-08-04-progress-html-spec.md`; commit `Record progress-html ship` with trailer `Piece: progress-html/4`; refresh (`python3 tools/diagram/progress.py` → `GOAL  progress-html` strip `####`, `4 landed · 0 in flight · 0 remaining`); `git add docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html`; commit `Refresh progress render` (no trailer); `python3 tools/diagram/progress.py stale` → `render current`, exit 0; `git push`; same CI check green on the new SHA. Two-push shape, as push-wiring.
12. Hand-off: report `/Users/anthonymaley/Kerd/docs/plans/progress.html` for Tony's cold `file://` open — the expert-user acceptance of the product's first Value row (human step, outside CI; not a gate on this spec's boxes).
**Why:** Judgment step: it interprets a live mixed refusal, decides finding-vs-defect at the CI boundary, and owns the two-round push shape — not command-checkable by a cold player. Before any retry after a failure here, re-run item 1's residue check: a dead player or aborted sub-step can leave a planted-stale surface or half-staged tree behind.
**Verify:** `gh run list --workflow=entry-gate --limit 2` shows both runs `completed` / `success`, the newest on the SHA of `git rev-parse HEAD`; `git status --porcelain` → empty; `python3 tools/diagram/progress.py stale` → `render current`, exit 0; `git show HEAD:docs/plans/progress.html | head -1` → `<!doctype html>`.
