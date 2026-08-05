---
route: new
stage: done
---

# Push wiring — build spec (the score)

Contract for the piece `push-wiring`, release slice 1: the staleness
refuser. A `stale` subcommand on the progress renderer that byte-compares
a fresh temp-dir render against the committed pair, three fixtures, a
seventh CI step, and the shallow-clone fix the design caught.

Design source: `docs/design/push-wiring.md`. Parent:
`docs/design/progress-view.md`.

Out of scope: any auto-push mechanism · `gate.py` rendering through the
progress view · conductor/switch skill files · README.md (no plugin
capability change) · stage bookkeeping in `docs/product/push-wiring.md`.

Piece-to-step mapping: piece 1 = Step 1 · piece 2 = Step 2 · piece 3 =
Steps 4+5 · piece 4 = Step 6. Step 3 (review) belongs to no piece.
Piece numbers are positional in the `## Pieces` checklist below; `Piece:
push-wiring/<n>` trailers must use those positions.

---

## Part A — definitions this spec settles

### A1. CLI and exit codes

```
python3 tools/diagram/progress.py stale
```

No flags. Exit 0 — committed pair matches a fresh render byte-for-byte.
Exit 1 — any difference, or either file missing. Exit 2 — any other argv
shape (`stale --json` is a usage error): print the module docstring, the
renderer's existing convention. Check-only: mutates nothing anywhere
under the repo; the fresh render goes to a `tempfile.TemporaryDirectory`.

### A2. Output lines (exact strings)

Exit 0 prints exactly one line:

```
render current
```

Exit 1 prints, in this order — `progress.excalidraw` line first, then
`progress.svg` line, then the fix line last. Per file: absent →
`missing: <relpath>`; present but bytes differ → `stale: <relpath>`;
identical → no line. A file is stale or missing, never both.

```
stale: docs/plans/progress.excalidraw
stale: docs/plans/progress.svg
run: python3 tools/diagram/progress.py && git add docs/plans/progress.excalidraw docs/plans/progress.svg && git commit
```

The fix line is VERBATIM from the design doc — every byte above, single
line, no trailing punctuation.

### A3. Compare semantics

Compare against **disk** (`docs/plans/progress.{excalidraw,svg}` under
root), never `HEAD:`. One semantics everywhere: in CI the checkout is the
pushed tip, so disk IS the tip; locally the answer is "would CI refuse
this tree?".

### A4. The single-serializer rule

The byte-compare is only sound if the temp render and the committed
render come from the SAME serialization — same doc envelope, same
`json.dump(doc, f, indent=2)`, same `to_svg` call. Two hand-kept copies
of that code would drift and make converged trees compare unequal. So
this build MOVES the pair-writing out of `progress.py:_cmd_render` into
one function, `progress_kit.write_pair(canvas, dir_path)`, and both the
render and `stale` write through it. This deliberately amends the old
split ("progress.py owns the writes") — `build_canvas`'s docstring
parenthetical must be updated to say `write_pair` owns serialization.

### A5. `.github/workflows/gate.yml` — final content (exact, byte-for-byte)

Two changes: the checkout gains `fetch-depth: 0` (actions/checkout@v4
defaults to depth 1; the renderer derives landed pieces from `git log`
trailers, so a shallow clone sees one commit, derives an emptier model,
and refuses every push — the defect the design caught), and a seventh
step after Matrix audit.

```yaml
name: entry-gate
on: [push, pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Gate selftest
        run: python3 tools/gates/gate.py selftest
      - name: Repo audit
        run: python3 tools/gates/gate.py audit
      - name: Release rules
        run: python3 tools/gates/gate.py release
      - name: Progress selftest
        run: python3 tools/diagram/progress.py selftest
      - name: Matrix selftest
        run: python3 tools/design/matrix.py selftest
      - name: Matrix audit
        run: python3 tools/design/matrix.py audit
      - name: Progress render current
        run: python3 tools/diagram/progress.py stale
```

### A6. Fixtures F11–F13

Extend `progress_kit.selftest()` in the established temp-git-tree idiom
(each case builds its own tree, `_git_init` + `_git_commit` with explicit
identity). Selftest total becomes 13; final line `selftest: 13 ok`.

| # | Tree | Assert |
|---|---|---|
| F11 | `_mk_f8_tree` → render pair via `write_pair` into `<d>/docs/plans/` → commit | `stale(d)` returns `(0, ["render current"])`; `git status --porcelain` empty after (check-only proven) |
| F12 | `_mk_f8_tree` + alpha contract (all unchecked) committed → render pair, commit → check box 1 in the WORKTREE only (no re-render) | `(1, [...])` — exactly the two `stale:` lines then the fix line, asserted as a SPELLED-OUT literal, not via the `FIX_LINE` constant |
| F13 | `_mk_f8_tree` only — no render ever written | `(1, [...])` — exactly the two `missing:` lines then the fix line |

F12's literal-not-constant rule is deliberate: asserting against
`FIX_LINE` would pass even if the constant itself were wrong.

### A7. The ship flow and its trap

**The trap, named:** this build itself lands the seventh CI step, and its
own edits (this spec file — a new `*-push-wiring-spec.md` contract — plus
checked Pieces boxes and `Piece:` trailers) CHANGE the derived render.
Pushing before a render refresh means the new refuser refuses its own
birth commit. The ship sequence is therefore fixed:

work commits (with trailers, boxes checked) → run the renderer → commit
the refreshed pair (NO trailer — render-only commits carry no trailer;
that is what bounds refresh divergence at depth 1) → **ONE push** →
verify CI green on the pushed SHA, all seven steps.

Before the push, refusal is demonstrated both ways on the real tree: the
build's own staleness gives exit 1 naming both files; the refreshed pair
gives exit 0. Piece 4's trailer cannot ride the work commit (CI isn't
green yet, so "shipped" would be a lie) — it lands in a follow-up commit
after CI verifies, which re-stales the render, so the record round
repeats the same shape: record commit → refresh → render commit → one
push → CI green. Ship is structurally two push rounds.

### A8. Version and release rules

`0.77.0` → `0.78.0` (MINOR: new feature) in exactly three places:
`.claude-plugin/plugin.json` `version`, `.claude-plugin/marketplace.json`
`metadata.version`, `.claude-plugin/marketplace.json`
`plugins[0].version`. NO change to either capability-list `description`
(repo-internal tooling, not a plugin capability), no README change.
`python3 tools/gates/gate.py release` must print `release: clean`.

---

## Part B — implementation shape (exact)

### progress_kit.py additions

Add `json` to the stdlib import block. After the existing
`from kit import ...` line add:

```python
from to_svg import to_svg  # noqa: E402
```

New module-level constant and two functions (place after `derive`, before
`render_table`):

```python
FIX_LINE = ("run: python3 tools/diagram/progress.py && "
            "git add docs/plans/progress.excalidraw "
            "docs/plans/progress.svg && git commit")


def write_pair(canvas, dir_path):
    """Serialize `canvas` to progress.excalidraw + progress.svg in
    `dir_path`. The ONLY serializer of the pair — the render and the
    stale check both write through here, so the byte-compare can never
    be defeated by two drifting serializations. Returns
    (excalidraw_path, svg_path, w, h)."""
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
    return out, svg_out, w, h


def stale(root):
    """Check-only staleness verdict: render the pair to a temp directory
    (never the working tree) and byte-compare each file against the
    committed pair on disk under `root`. Returns (0, ["render current"])
    when both are identical; else (1, lines) — 'stale: <relpath>' /
    'missing: <relpath>' per file, excalidraw first, FIX_LINE last.
    Mutates nothing under `root`."""
    model = derive(root)
    canvas = build_canvas(model)
    problems = []
    with tempfile.TemporaryDirectory() as td:
        tmp_ex, tmp_svg, _w, _h = write_pair(canvas, td)
        for tmp, rel in ((tmp_ex, "docs/plans/progress.excalidraw"),
                         (tmp_svg, "docs/plans/progress.svg")):
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

`FIX_LINE`'s concatenation must evaluate to exactly the A2 fix line —
note the space placement in the fragments. Update `build_canvas`'s
docstring parenthetical to: "(write_pair owns the .excalidraw/.svg
serialization; the render and the stale check both write through it)".

### progress.py changes

1. Docstring usage block gains a third line:
   `    python3 tools/diagram/progress.py stale      # check-only: fresh temp render vs committed pair — exit 0 current / 1 stale`
   and the paragraph gains: "stale is the refuser: it renders to a temp
   directory, byte-compares against the committed pair, and exits 1
   naming each differing or missing file plus the fix command; it
   mutates nothing."
2. Import line becomes
   `from to_svg import overflow_report, collision_report, text_overlap_report`
   (`to_svg` itself is no longer called here).
3. In `_cmd_render`, replace the `doc = {...}` envelope, the
   `json.dump` write, and the `to_svg(...)` call with:

```python
    out, svg_out, w, h = progress_kit.write_pair(
        canvas, os.path.join(progress_kit.REPO, "docs", "plans"))
```

   Everything else in `_cmd_render` (table, `--json`, fault reports)
   stays byte-identical. The `json` import stays (used by `--json`).
4. New function and one new dispatch line in `main` (after the selftest
   line, before the render line):

```python
def _cmd_stale():
    code, lines = progress_kit.stale(progress_kit.REPO)
    for line in lines:
        print(line)
    return code
```

```python
    if argv == ["stale"]:
        return _cmd_stale()
```

### Fixture code (Step 2 copies this)

```python
def _f11():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        model = derive(d)
        canvas = build_canvas(model)
        write_pair(canvas, os.path.join(d, "docs", "plans"))
        _git_commit(d, "render pair")
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
        write_pair(canvas, os.path.join(d, "docs", "plans"))
        _git_commit(d, "render pair")
        _sw(os.path.join(d, _ST_CONTRACT_REL), _pieces_md([True, False, False]))
        code, lines = stale(d)
        assert code == 1, f"expected exit 1, got {code}: {lines}"
        assert lines == [
            "stale: docs/plans/progress.excalidraw",
            "stale: docs/plans/progress.svg",
            "run: python3 tools/diagram/progress.py && git add "
            "docs/plans/progress.excalidraw docs/plans/progress.svg && git commit",
        ], lines


def _f13():
    with tempfile.TemporaryDirectory() as d:
        _mk_f8_tree(d)
        code, lines = stale(d)
        assert code == 1, f"expected exit 1, got {code}: {lines}"
        assert lines == [
            "missing: docs/plans/progress.excalidraw",
            "missing: docs/plans/progress.svg",
            FIX_LINE,
        ], lines
```

Case-list additions, appended after `_f10`'s entry:

```python
        (_f11, "stale: converged tree — render current, exit 0"),
        (_f12, "stale: drifted tree — exit 1 naming both files and the verbatim fix"),
        (_f13, "stale: missing pair — exit 1 naming both missing files"),
```

Change the final print to `selftest: 13 ok`; update the `selftest()`
docstring's count and the fixture-block header comment ("Part B fixtures
(F1-F10)") to note F11–F13 come from this spec.

---

## Standing cautions (every step, every player)

- `python3`, never `python`.
- **Never run bare `python3 tools/diagram/progress.py` (or `--json`)
  before Step 6** — both overwrite the committed pair in the working
  tree. If run by accident:
  `git checkout -- docs/plans/progress.excalidraw docs/plans/progress.svg`,
  then confirm with `git status --porcelain` on those two paths (empty).
- Run every Verify command and compare against EXPECTED. If actual
  contradicts expected: STOP and report actual vs expected — never
  self-judge PASS, never patch around it.
- Touch only the files your step names. Working directory for every
  command: `/Users/anthonymaley/Kerd`.
- Before re-dispatching any failed step: `git status --porcelain` first —
  a dead player can leave residue.

---

## Pieces

- [x] stale verdict: write_pair + stale(root) in progress_kit.py, stale subcommand in progress.py
- [x] fixtures F11-F13: converged / drifted / missing pair
- [x] CI seventh step + fetch-depth 0 + version 0.78.0
- [x] shipped: both-ways refusal on the real tree, one push, CI green on the pushed SHA

---

## Steps

### Step 1: stale verdict in the toolkit [delegate, model: sonnet, effort: high]
**What:** Edit `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py` and `/Users/anthonymaley/Kerd/tools/diagram/progress.py` exactly per Part B: add `json` import and `from to_svg import to_svg` to progress_kit; add `FIX_LINE`, `write_pair`, `stale` verbatim from the Part B blocks; update `build_canvas`'s docstring parenthetical; in progress.py update the docstring, narrow the to_svg import, route `_cmd_render`'s writes through `progress_kit.write_pair`, add `_cmd_stale` and the `["stale"]` dispatch. No fixtures yet.
**Why:** The single-serializer rule (A4) is the load-bearing choice: `_cmd_render` MUST call the same `write_pair` that `stale` calls — a second copy of the envelope/`json.dump(indent=2)` serialization would drift and make converged trees compare unequal. Do not "leave _cmd_render alone and duplicate".
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py selftest; echo "exit=$?"` → ends `selftest: 10 ok`, `exit=0` (existing suite unbroken). Then `python3 tools/diagram/progress.py stale; echo "exit=$?"` → exactly the three A2 exit-1 lines (`stale: docs/plans/progress.excalidraw`, `stale: docs/plans/progress.svg`, the verbatim fix line), `exit=1` — this spec file already sits in the worktree, so the committed render is genuinely stale; exit 0 here means the compare is broken: STOP. Then `python3 tools/diagram/progress.py stale --json; echo "exit=$?"` → usage text, `exit=2`. Then `git status --porcelain docs/plans/progress.excalidraw docs/plans/progress.svg` → empty (check-only proven), and `python3 tools/gates/gate.py audit` → `audit: clean`.

### Step 2: fixtures F11–F13 [delegate, model: sonnet, effort: medium]
**What:** Edit `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py` only: add `_f11`, `_f12`, `_f13` and the three case-list entries verbatim from Part B's fixture block; final print becomes `selftest: 13 ok`; update the selftest docstring count and the fixture-block header comment.
**Why:** F12 spells the fix line as a literal instead of referencing `FIX_LINE` on purpose — asserting the constant against itself would pass even if the constant were wrong. Keep the literal exactly as written.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py selftest; echo "exit=$?"` → output contains `ok 11 — stale: converged tree — render current, exit 0`, `ok 12 — stale: drifted tree — exit 1 naming both files and the verbatim fix`, `ok 13 — stale: missing pair — exit 1 naming both missing files`, ends `selftest: 13 ok`, `exit=0`. Then `git status --porcelain docs/plans/progress.excalidraw docs/plans/progress.svg` → empty.

### Step 3: diff review against Part A/B [keep]
**What:** Conductor reads the full Step 1–2 diff of both files against this spec line by line: `_cmd_render` writes through `write_pair` (no second serializer anywhere); `stale` writes only inside `TemporaryDirectory`; output strings byte-match A2 including line order; `stale --json` reaches the usage/exit-2 path; F12's fix-line assert is a spelled literal; no edits outside the two named files; docstrings updated as specified.
**Why:** The commands can't catch a quietly duplicated envelope or a paraphrased message string — spec-drift review is the conductor's job; any miss → re-dispatch the owning step, never patch in review.
**Verify:** Checklist above fully ticked; `git diff --stat` names only `tools/diagram/progress.py` and `tools/diagram/progress_kit.py` (plus this spec file if boxes were pre-staged — they must NOT be: boxes stay unchecked until Step 6).

### Step 4: gate.yml — fetch-depth 0 + seventh step [delegate, model: haiku, effort: low]
**What:** Replace the contents of `/Users/anthonymaley/Kerd/.github/workflows/gate.yml` with the A5 block, byte-for-byte.
**Why:** `fetch-depth: 0` is not optional polish — with the default shallow clone the renderer derives an emptier model from one commit of history and would refuse every push.
**Verify:** `cd /Users/anthonymaley/Kerd && grep -n 'fetch-depth: 0' .github/workflows/gate.yml && grep -n 'Progress render current' .github/workflows/gate.yml && grep -c 'run: python3' .github/workflows/gate.yml` → first two greps hit (fetch-depth on the line after `with:`), count is `7`. Then `python3 tools/diagram/progress.py selftest` → `selftest: 13 ok` (cross-checks Step 2 still green).

### Step 5: version 0.78.0 [delegate, model: haiku, effort: low]
**What:** Bump `"0.77.0"` → `"0.78.0"` in `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (`version`) and `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (`metadata.version` AND `plugins[0].version`). Touch nothing else in either file — both `description` fields stay byte-identical to what they are.
**Why:** MINOR bump: new feature (the stale subcommand + CI step), no interface break. Repo-internal tooling is not a plugin capability, so the capability lists do not change.
**Verify:** `cd /Users/anthonymaley/Kerd && grep -c '"0.78.0"' .claude-plugin/plugin.json .claude-plugin/marketplace.json` → `1` and `2`; `grep -c '"0.77.0"' .claude-plugin/plugin.json .claude-plugin/marketplace.json` → `0` and `0`; `python3 tools/gates/gate.py release; echo "exit=$?"` → `release: clean`, `exit=0`.

### Step 6: ship — both-ways refusal, one push, CI on the SHA, record round [keep]
**What:** All commands from `/Users/anthonymaley/Kerd`, in this exact order. The trap this ordering defuses (A7): this build's own edits change the derived render, so a push before the render refresh is refused by the CI step this build just added — the refuser must not refuse its own birth commit.
1. Residue check: `git status --porcelain` → only the expected build files (`tools/diagram/progress.py`, `tools/diagram/progress_kit.py`, `.github/workflows/gate.yml`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `docs/plans/2026-08-04-push-wiring-spec.md`); the render pair paths must NOT appear. Anything else → stop and report.
2. Local seven: `python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit` → all exit 0, incl. `audit: clean`, `release: clean`, `selftest: 13 ok`.
3. In this spec file, flip Pieces boxes 1–3 to `[x]` (box 4 stays unchecked — CI is not green yet, and its trailer lands in the record round).
4. Work commit, staged by name: `git add tools/diagram/progress.py tools/diagram/progress_kit.py .github/workflows/gate.yml .claude-plugin/plugin.json .claude-plugin/marketplace.json docs/plans/2026-08-04-push-wiring-spec.md` then commit with message `Push wiring: the staleness refuser (stale subcommand + CI seventh step)` and body trailers `Piece: push-wiring/1`, `Piece: push-wiring/2`, `Piece: push-wiring/3` (one per line; extra harness trailers are harmless — the trailer scan matches only `Piece:` lines).
5. Refusal, way one: `python3 tools/diagram/progress.py stale; echo "exit=$?"` → exactly the three A2 exit-1 lines, `exit=1`.
6. Refresh: `python3 tools/diagram/progress.py` → table shows a `GOAL  push-wiring` line with strip `###.` and `3 landed · 0 in flight · 1 remaining`, `drift: none`, and the three no-fault lines (`no bound-text overflow`, `no text/box collisions`, `no text/text overlaps`). Any `!!` fault line → STOP, report (layout finding).
7. Render commit, NO trailer: `git add docs/plans/progress.excalidraw docs/plans/progress.svg` then commit `Refresh progress render` — render-only commits carry no `Piece:` trailer; that is what bounds refresh divergence at depth 1.
8. Refusal, way two: `python3 tools/diagram/progress.py stale; echo "exit=$?"` → `render current`, `exit=0`. Then `git status --porcelain` → empty.
9. ONE push: `git push`.
10. CI on the pushed SHA: poll `gh run list --workflow=entry-gate --limit 1 --json status,conclusion,headSha` until `completed` — expect `success` and `headSha` equal to `git rev-parse HEAD`; `gh run view <run-id>` lists all seven steps green including `Progress render current`. If that step alone is red while local exit was 0, that is the cross-platform determinism finding (A7/design): STOP and report — the named fallback is normalize-before-compare in a follow-up, never weakening to a semantic diff, and never a hotfix inside this step.
11. Record round: flip box 4 to `[x]`; `git add docs/plans/2026-08-04-push-wiring-spec.md`; commit `Record push-wiring ship` with trailer `Piece: push-wiring/4`; refresh (`python3 tools/diagram/progress.py` → `GOAL  push-wiring` strip `####`, `4 landed · 0 in flight · 0 remaining`); `git add docs/plans/progress.excalidraw docs/plans/progress.svg`; commit `Refresh progress render` (no trailer); `python3 tools/diagram/progress.py stale` → `render current`, exit 0; `git push`; same CI check green on the new SHA.
**Why:** Judgment step: it interprets a live refusal, decides finding-vs-defect, and owns the two-round push shape — not command-checkable by a cold player. Before any retry after a failure here, re-run step 1's residue check: a dead player (or an aborted sub-step) can leave a planted-stale pair or half-staged tree behind.
**Verify:** `gh run list --workflow=entry-gate --limit 2` shows both runs `completed` / `success`, the newest on the SHA of `git rev-parse HEAD`; `git status --porcelain` → empty; `python3 tools/diagram/progress.py stale` → `render current`, exit 0.
