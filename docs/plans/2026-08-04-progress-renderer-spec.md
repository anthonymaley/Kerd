---
route: new
stage: contracted
---

# Progress renderer — build spec (the score)

Contract for the piece `progress-renderer`: the pull-only progress view
per `docs/design/progress-view.md`. One instrument, three surfaces from
one model: a stdout table, `--json`, and an Excalidraw/SVG pair on the
live canvas. BOARD view: the ladder coloured agreed / built / in-flight /
missing — have/need per rung at a glance. GOAL view: the work-order strip
— landed (green-lit by commit) · in flight · remaining. Derived from DISK
only: git log, `gate.py --json` (imported, not shelled), spec-file Pieces
checklists, `docs/gates/` records. Never self-reported, never prose.
Grows from `tools/diagram/`. No new skill.

**Acceptance bar:** the renderer runs against TODAY'S real tree and
produces a truthful render of the actual current state — absent
`docs/gates/` and `docs/product/` included; that IS today's state, not an
edge case — demonstrated by running it (Step 6), plus the fixture suite
(Step 5). CI stays green: gate selftest + audit + release + the new
progress selftest.

**Deferral (do not re-derive this later):** push wiring is NOT built
here. The stage-close PUSH, the dated gate-close record copies
(`docs/gates/` shape, diffable against the next one), the liveness tick
during a long run, and pushed-vs-local commit annotation all belong to
the conductor-role graduation map. This piece builds the PULL surface
those will call. The grounding-was-read check stays deferred exactly as
`tools/gates/README.md` records.

Design source: `docs/design/progress-view.md`. Canonical vocabulary:
`tools/gates/README.md` — rungs `frame viability slice design contract
build goal loop` and stages `framed viable sliced designed contracted
building done`, verbatim, no synonyms. View-state words come verbatim
from the design doc: board = `agreed / built / in-flight / missing`,
goal = `landed / in flight / remaining`.

Out of scope: any push, any hook, any skill change, root `README.md`
(entry gates added no repo-level-tool line; same call here, stated so it
is a decision and not an omission), `docs/gates/` creation, editing the
two existing spec files.

---

## Terrain — verified on disk at spec time (2026-08-04)

Players never saw the reasoning; these facts ground every step cold.

- `docs/gates/` and `docs/product/` do NOT exist. The renderer must
  render that truthfully, not error on it.
- Three spec contracts match `docs/plans/*-<S>-spec.md` today:
  `2026-07-07-conductor-effort-lever-spec.md` (no `## Pieces` section),
  `2026-08-04-entry-gates-spec.md` (no `## Pieces` section — it predates
  the requirement it introduced), `2026-08-04-ci-refusal-spec.md`
  (`## Pieces` with 11 boxes: 9 checked, 2 unchecked — steps 10 and 11).
  This file adds a fourth. Only ci-refusal and this file carry
  checklists; the renderer shows the other two as having no checklist —
  that is the truth, render it.
- Zero `Piece:` lines exist anywhere in git history (verified with
  `git log --format='%B' | grep -c '^Piece:'` → 0). The shipping commit
  of THIS piece is the first.
- `python3 tools/gates/gate.py route <slug> --json` returns
  `{"slug", "enters_at", "bypass", "rungs": [{"rung", "have", "need"}]}`
  where `have`/`need` are lists of strings and needs are CUMULATIVE per
  rung. Today every slug enters at `frame` (all deeper rungs need the
  absent `docs/product/<S>.md`).
- `tools/gates/kit.py` exposes `route(root, slug)`, `check_rung(root,
  slug, rung)`, `audit(root)`, `release_audit(root)`, `RUNGS`, `ROOT` —
  every function takes `root` as a plain parameter precisely so this
  renderer can import it rather than shell out
  (`tools/gates/README.md`, "Progress view" section).
- Plugin versions are `0.70.0` in all three fields.
- Both `tools/diagram/kit.py` and `tools/gates/kit.py` are named
  `kit.py`. A bare `sys.path` insert of both dirs silently shadows one.
  D8 below gives the required loader.

---

## Part A — decisions this spec settles

### A1. Commit→piece mapping (the design decision, and the point)

The entry-gates spec declared its own simplification: the `goal` rung
counts checked boxes "until the progress view cross-checks git". This
build is that cross-check arriving. A checked box in the WORKING TREE is
the working model's live claim — self-report, which the iron rule bans as
a landing signal. A commit is evidence: a hung model produces no commits,
and a claim that has not survived a commit has not landed.

Piece n of slug S, where the contract is the latest-by-filename
`docs/plans/*-<S>-spec.md` and pieces are the `^- \[[ x]\] ` lines of its
`## Pieces` section in order, 1-indexed:

| Mode | Applies when | `landed` means |
|---|---|---|
| **trailer** | ≥1 line matching `^Piece:\s*S/[0-9]+\s*$` exists anywhere in `git log --format=%B` output | a line `Piece: S/n` exists there. A single commit may carry many `Piece:` lines. |
| **legacy** | zero `Piece: S/…` lines in history | box n is checked in the HEAD version of the contract (`git show HEAD:<contract-path>`) — the claim itself has been committed, and every push runs the gates |

Then, both modes:

- **in flight** — not landed, AND box n is checked in the working tree
  (a live claim awaiting git ratification — the cross-check state).
- **remaining** — neither.
- **drift** (a named line, not a strip state) — landed but the box is
  unchecked in the working tree: render the strip cell as landed plus a
  line `drift: S/n — landed in git, box unchecked in working tree`.

Why checkbox-in-HEAD for legacy rather than "checked anywhere": if the
contract is committed at approval with boxes unchecked, a box checked
mid-build in the working tree must read *in flight*, never landed — the
false-green this mapping exists to kill. Why trailers at all: piece-level
evidence with zero ambiguity, written by the conductor per verified
piece; legacy exists only because two pre-trailer specs are already in
history, and it switches off for a slug the moment its first trailer
lands. Evidence regex (exact): `^Piece:\s*([a-z0-9][a-z0-9-]*)/([1-9][0-9]*)\s*$`
scanned per line over the whole `git log --format=%B` output; which
commit carried the line is not tracked in v1 (existence is the signal).

Declared simplification: landed = evidence reachable from HEAD.
Distinguishing pushed from local commits is deferred with push wiring
(see the deferral note above).

### A2. Board derivation — per (slug, rung), from the gates seam

Call `gates_kit.route(root, S)` (imported per D8). Its cumulative-input
semantics make the pass prefix monotone, so with `E = enters_at`:

- rungs shallower than `E` → **built** — their outputs exist on disk (a
  rung's outputs are the next rung's inputs, and the next rung passes).
- rung `E` → **in-flight** — inputs present, outputs not; the rung
  performable now.
- rungs deeper than `E` → **missing** — carry `need = len(rung["need"])`.
- **agreed** — an overlay, not a fourth exclusive state: glob
  `docs/gates/*-<S>-<rung>.md` non-empty means that rung's close was
  ratified by a dated GO record. Absent directory → no rung anywhere is
  agreed. Today that is every rung — truthful.
- `bypass: true` in the route result → the slug renders as one line
  `SPIKE <S> — ladder bypassed`, no rung cells.

### A3. Slug discovery

Union of: `S` from filenames matching
`^\d{4}-\d{2}-\d{2}-([a-z0-9][a-z0-9-]*)-spec\.md$` in `docs/plans/`, and
basenames (minus `.md`) of `docs/product/*.md`. Absent directories
contribute nothing (vacuous pass — the gates precedent). Sorted
alphabetically. No config file, no registry: the disk is the registry.

### A4. Output surfaces — one model, three renders

The decision the format constraint asks for: **all three**, from one
derived model, no second code path (the `--json` precedent in gate.py).

1. **stdout table** (default) — the terminal pull. The design doc itself
   says a table whose rows carry verdicts is already a
   have/need/progress render. Never prose: every line is a labelled row.
2. **`--json`** — `json.dumps(model)`; prints nothing else, so it pipes.
3. **canvas pair** — `docs/plans/progress.excalidraw` + `.svg`, written
   on every render run, both modes. The human's review modality is
   drawings on the live canvas; the SVG reviews headlessly (command in
   `tools/diagram/README.md`). Undated filenames: this is the LIVING
   view; dated copies are the gate-close records, deferred with push
   wiring. `mark_deltas` is NOT applied: progress state is itself the
   delta signal, and blue-on-every-tick would drown the one meaning blue
   has. No timestamps anywhere in output — git already dates the data,
   and a timestamp string would churn every regeneration.

Colour mapping, preserving the kit grammar (colour marks COST; GREEN is
Tony's input; containment over arrows):

| State | Render |
|---|---|
| built / landed | INK stroke, GREY fill — the have |
| in-flight / in flight | INK stroke, dashed, strokeWidth 2 — the seam being worked |
| missing / remaining | RED stroke — the need is the cost |
| agreed | GREEN stroke replacing INK on that cell — a GO record is the human's input |
| drift lines | RED text — a named problem is cost |

### A5. Model schema (exact — this is the `--json` contract)

```json
{
  "audit_problems": 0,
  "slugs": ["ci-refusal", "conductor-effort-lever", "..."],
  "board": [
    {"slug": "ci-refusal", "bypass": false, "enters_at": "frame",
     "rungs": [
       {"rung": "frame", "state": "in-flight", "have": 0, "need": 0,
        "agreed": false},
       {"rung": "viability", "state": "missing", "have": 0, "need": 3,
        "agreed": false}
     ]}
  ],
  "goals": [
    {"slug": "ci-refusal",
     "contract": "docs/plans/2026-08-04-ci-refusal-spec.md",
     "mode": "legacy",
     "pieces": [
       {"n": 1, "text": "Step 1: ...", "checked_worktree": true,
        "checked_head": true, "state": "landed"}
     ],
     "counts": {"landed": 9, "in_flight": 0, "remaining": 2}},
    {"slug": "entry-gates",
     "contract": "docs/plans/2026-08-04-entry-gates-spec.md",
     "mode": null, "pieces": [], "counts": null}
  ],
  "drift": []
}
```

`mode: null` + empty `pieces` + `counts: null` = contract exists but has
no `## Pieces` checklist (≥1 box line). `contract: null` = no contract
file at all. State strings verbatim: board `agreed`/`built`/`in-flight`/
`missing` (agreed only ever appears via the boolean, never replaces the
exclusive state), goal `landed`/`in flight`/`remaining`. `audit_problems`
= `len(gates_kit.audit(root))` — the gates README names audit problem
lines as part of what this view consumes.

### A6. Table format (exact)

```
progress — derived from disk: git log · gate route · Pieces checklists · docs/gates/
audit: clean

BOARD   [G] agreed  [#] built  [>] in-flight  [.] missing
rung        ci-refusal    conductor-effort-lever    entry-gates
frame       >             >                         >
viability   . need 3      . need 3                  . need 3
...all eight rungs, ladder order, one row each...

GOAL  ci-refusal              #########..    9 landed · 0 in flight · 2 remaining
GOAL  conductor-effort-lever  —              no Pieces checklist in docs/plans/2026-07-07-conductor-effort-lever-spec.md
GOAL  entry-gates             —              no Pieces checklist in docs/plans/2026-08-04-entry-gates-spec.md

drift: none
```

Rules: `audit: clean` or `audit: <n> problems`. Board cells: built `#`,
in-flight `>`, missing `. need <n>`, with ` G` appended when agreed;
column widths pad to content, two-space minimum gap (verify greps target
GOAL/audit/drift lines, not board alignment). Strip glyphs: `#` landed ·
`>` in flight · `.` remaining, one glyph per piece in order. Counts line
verbatim `<L> landed · <I> in flight · <R> remaining` (middle dots).
Drift: `drift: none` or one `drift: <slug>/<n> — landed in git, box
unchecked in working tree` line each. A slug with no contract renders
`GOAL  <slug>  —  no contract on disk`. Spike slugs: `SPIKE <slug> —
ladder bypassed` in place of board cells, goal strip unaffected.

### A7. Canvas layout

Build with `kit.Canvas` (tools/diagram), render via `to_svg`, run all
three layout checks. Geometry (constants; adjust only if a layout check
fires): `X = 300`. Title `"Progress — derived from disk"` size 24;
legend lines size 14 restating the colour mapping (one line per meaning,
in its own colour, the Flow-class precedent). Board: rung-label column
at X width 150 (labels size 13); one column per slug, width 230, header
= slug name size 12; cell 230×40, 8px vertical gap; built = rect GREY
fill; in-flight = box `"enters at"` dashed sw 2; missing = box
`"need <n>"` RED; agreed cell stroke GREEN. Goal strips below the board,
one per slug: slug name size 16, then piece cells 26×26 in a row, 4px
gap, coloured per A4; counts line size 13 beneath; no-checklist slugs
get one RED text line instead of cells. Drift lines RED size 13 at the
bottom. Output doc structure copies the gen_excalidraw tail exactly:
`{"type": "excalidraw", "version": 2, "source":
"https://excalidraw.com", "elements": els, "appState": {"gridSize":
None, "viewBackgroundColor": "#ffffff"}, "files": {}}`.

### A8. Architecture and CLI

The gates split, exactly: every decision in `progress_kit.py`;
`progress.py` only parses argv, writes files, prints.

```
python3 tools/diagram/progress.py [--json]   # render: writes docs/plans/progress.{excalidraw,svg}; prints table (or the model as JSON)
python3 tools/diagram/progress.py selftest   # fixture suite in temp trees — exit 0 / 1
```

Render always exits 0 — it is a report, like `route`; drift is shown,
never failed on (the refusers are the gates). Any other argv: print the
module docstring, exit 2. With `--json` the canvas pair is still written
but nothing except the JSON is printed.

`tools/diagram/progress_kit.py` — exact signatures:

```python
REPO = "/Users/anthonymaley/Kerd"      # default root; every function takes root
PIECE_RE   # re for '^- \[( |x)\] (.*)$'
TRAILER_RE # re from A1

def load_gates_kit():                  # D8 loader, cached module global
def discover_slugs(root) -> list[str]  # A3
def contract_for(root, slug) -> str | None   # repo-relative path, latest by filename
def parse_pieces(text) -> list[tuple[bool, str]]  # (checked, text) from '## Pieces'; [] if no section/boxes
def head_text(root, relpath) -> str | None   # git show HEAD:<relpath>; None on any git failure
def piece_evidence(root) -> set[tuple[str, int]]  # all (slug, n) from git log --format=%B; empty set on git failure
def goal_for(root, slug, evidence) -> dict   # one A5 goals entry
def board_for(root, slug, gates_kit) -> dict # one A5 board entry
def derive(root) -> dict                     # the full A5 model
def render_table(model) -> str               # A6, exact
def build_canvas(model):                     # -> kit.Canvas per A7
def selftest() -> int                        # Part B; prints per-case lines
```

Git calls use `subprocess.run(["git", "-C", root, ...],
capture_output=True, text=True)`; any nonzero returncode means "no
evidence" / "no HEAD version", never an exception — a fresh `git init`
with zero commits is a legal tree (fixture F2).

**D8 — the two-kit trap.** `progress_kit` imports the diagram kit
normally (`sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`
then `from kit import Canvas, INK, RED, GREEN, GREY`) and loads the
gates kit BY PATH, because both files are named `kit.py`:

```python
import importlib.util
def load_gates_kit():
    p = os.path.join(REPO, "tools", "gates", "kit.py")
    spec = importlib.util.spec_from_file_location("gates_kit", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
```

The gates kit always loads from the real repo (its functions take
fixture roots as parameters); only the DATA root varies.

---

## Part B — selftest: the 10 cases

Fixture pattern: the gates precedent, plus git — each case builds a tree
in a `tempfile.TemporaryDirectory`, runs `git -C d init -q`, and commits
with explicit identity (`git -C d -c user.name=selftest -c
user.email=selftest@kerd commit -q -m <msg>`) — CI runners have no git
identity configured, so bare `git commit` fails there. Slug `alpha`,
contract `docs/plans/2026-01-02-alpha-spec.md`. Each case prints one
`ok <n> — <name>` line; any assertion failure prints `FAIL <n> — <name>`
and the suite exits 1, else `selftest: 10 ok` exit 0.

| # | Tree | Assert |
|---|---|---|
| F1 | git init only, no `docs/` | `derive` → `slugs == []`; `render_table` output contains `no work orders on disk`; no exception (today's absent-dirs class) |
| F2 | contract with 3 unchecked pieces, NOT committed | zero-commit repo: `piece_evidence` → empty set, `head_text` → None, all 3 `remaining` |
| F3 | contract committed with boxes unchecked, then 2 boxes checked in worktree only | legacy mode, both `in flight`, 1 `remaining` — the false-green kill |
| F4 | contract committed WITH boxes 1–2 checked | legacy mode, 2 `landed`, 1 `remaining` |
| F5 | F3 tree + empty commit whose message body carries `Piece: alpha/2` | trailer mode: piece 2 `landed`; piece 1 (checked, no trailer) `in flight` — legacy off the moment a trailer exists |
| F6 | commit carrying `Piece: alpha/1` AND `Piece: alpha/3` lines in one message | both landed — multi-trailer commits legal |
| F7 | trailer `Piece: alpha/2` present, box 2 UNCHECKED in worktree | piece 2 `landed` + drift list contains `alpha/2 — landed in git, box unchecked in working tree` |
| F8 | + `docs/product/alpha.md` with legal front matter and a `## Value` section, committed | board: `frame` → `built`, `viability` → `in-flight` (= `enters_at`), `slice` → `missing` with `need ≥ 1` |
| F9 | F8 + `docs/gates/2026-01-01-alpha-viability.md` | `viability` rung `agreed: true`; other rungs `agreed: false` |
| F10 | F8 model → `build_canvas` → `overflow_report`, `collision_report`, `text_overlap_report` | all three empty — the generating-blind fix, enforced in fixtures |

---

## Steps

### Step 1: tools/diagram/progress_kit.py — derivation [delegate, model: sonnet, effort: high]
**What:** create `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py` with the A8 signatures: constants, `load_gates_kit` (D8 exactly), `discover_slugs`, `contract_for`, `parse_pieces`, `head_text`, `piece_evidence`, `goal_for`, `board_for`, `derive`. Mapping per A1, board per A2, discovery per A3, model per A5. Module docstring states the one-line why: derived from disk, never self-reported; checkbox is a claim, commit is evidence. No `render_table`/`build_canvas`/`selftest` yet (Steps 2–4).
**Why:** the model is the whole instrument; the three surfaces are only prints of it.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 -c "import sys; sys.path.insert(0,'tools/diagram'); import progress_kit as pk; m=pk.derive(pk.REPO); print(m['slugs']); g={x['slug']:x for x in m['goals']}; print(g['ci-refusal']['mode'], g['ci-refusal']['counts']); print(g['entry-gates']['mode'], g['entry-gates']['counts']); print({b['slug']: b['enters_at'] for b in m['board']}['ci-refusal'], m['audit_problems'])"` → slugs list containing `ci-refusal`, `conductor-effort-lever`, `entry-gates`, `progress-renderer` (alphabetical); then `legacy {'landed': 9, 'in_flight': 0, 'remaining': 2}`; then `None None`; then `frame 0`.

### Step 2: render_table — the terminal pull [delegate, model: sonnet, effort: medium]
**What:** add `render_table(model)` to `progress_kit.py`, format per A6 exactly, including the `no work orders on disk` line for an empty model and the SPIKE line for bypass slugs.
**Why:** a table whose rows carry verdicts is already a have/need/progress render — the design doc's own words; never prose.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 -c "import sys; sys.path.insert(0,'tools/diagram'); import progress_kit as pk; print(pk.render_table(pk.derive(pk.REPO)))" | grep -cF '9 landed · 0 in flight · 2 remaining'` → `1`, and the same pipe with `grep -c '^audit: clean$'` → `1`.

### Step 3: build_canvas — the drawing [delegate, model: sonnet, effort: high]
**What:** add `build_canvas(model)` to `progress_kit.py` per A7, importing `Canvas` and colours from the diagram `kit` (D8 import order). Returns the `Canvas`; writes nothing.
**Why:** the human's review modality is drawings on the live canvas; the render must be an artifact he can open, not only a scrollback.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 -c "import sys; sys.path.insert(0,'tools/diagram'); import progress_kit as pk; from to_svg import overflow_report, collision_report, text_overlap_report; c=pk.build_canvas(pk.derive(pk.REPO)); print(len(c.els) > 0, overflow_report(c.els), collision_report(c.els), text_overlap_report(c.els))"` → `True [] [] []`.

### Step 4: tools/diagram/progress.py — the shell [delegate, model: sonnet, effort: medium]
**What:** create `/Users/anthonymaley/Kerd/tools/diagram/progress.py`: docstring = the A8 usage block; argv per A8 (`[--json]` | `selftest` | else docstring + exit 2). Render path: `derive` → write `docs/plans/progress.excalidraw` (json.dump, indent 2, A7 doc structure) and `.svg` via `to_svg` → print table + `wrote <path>` lines + the three layout-check reports (the gen_excalidraw tail pattern), or with `--json` print ONLY `json.dumps(model)`.
**Why:** one invocation, three surfaces, one model — the `--json` promise: same data, not a second code path.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py --json | python3 -c "import json,sys; m=json.load(sys.stdin); print(sorted(m.keys()))"` → `['audit_problems', 'board', 'drift', 'goals', 'slugs']`, and `ls docs/plans/progress.excalidraw docs/plans/progress.svg` lists both.

### Step 5: selftest — the fixture suite [delegate, model: sonnet, effort: high]
**What:** add `selftest()` to `progress_kit.py` implementing F1–F10 per Part B; wire `progress.py selftest` to `sys.exit(progress_kit.selftest())`.
**Why:** the gates' fixture pattern is the precedent — anything with logic proves itself in a temp tree, from outside the model, before CI ever runs it.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py selftest; echo exit=$?` → ten `ok` lines, `selftest: 10 ok`, `exit=0`.

### Step 6: the truthful render — today's tree [delegate, model: haiku, effort: low]
**What:** run `python3 tools/diagram/progress.py` from `/Users/anthonymaley/Kerd` and check the output against today's verified terrain. Do not fix the renderer here; if a check fails, report the diff between expected and actual and stop.
**Why:** the acceptance bar is a truthful render of the ACTUAL current state, demonstrated by running it — empty gate records and all.
**Verify:** the run prints, among its lines: `audit: clean`; a `frame` board row whose cells are all `>` (every slug enters at frame — docs/product absent); NO ` G` marker anywhere (docs/gates absent); `GOAL` line for `ci-refusal` containing `#########..` and `9 landed · 0 in flight · 2 remaining`; `no Pieces checklist in docs/plans/2026-08-04-entry-gates-spec.md`; a `GOAL` line for `progress-renderer` with `0 landed` (this piece's shipping commit does not exist yet); `no bound-text overflow`, `no text/box collisions`, `no text/text overlaps`; both `wrote` lines.

### Step 7: docs travel with code — README + CI [delegate, model: sonnet, effort: low]
**What:** (1) `/Users/anthonymaley/Kerd/tools/diagram/README.md`: add a `## Progress renderer` section documenting the two invocations, the three surfaces, the A1 mapping in two sentences (trailer `Piece: <slug>/<n>` primary; legacy HEAD-checkbox for pre-trailer specs; checkbox alone never lands a piece), the deferral note (push wiring → conductor graduation map), and the headless-Chrome line for `docs/plans/progress.svg`. (2) `/Users/anthonymaley/Kerd/.github/workflows/gate.yml`: append step `- name: Progress selftest` / `run: python3 tools/diagram/progress.py selftest` after the Release rules step. No `/kerd:` references are needed in either file; `docs/plans/` is R3-exempt.
**Why:** docs travel with code in the same commit; the selftest only refuses from outside the model once CI runs it.
**Verify:** `cd /Users/anthonymaley/Kerd && grep -c "Progress renderer" tools/diagram/README.md` → `≥1`; `grep -c "progress.py selftest" .github/workflows/gate.yml` → `1`; then the full local CI trio+1: `python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest; echo exit=$?` → `exit=0`.

### Step 8: release checklist [delegate, model: haiku, effort: low]
**What:** MINOR bump `0.70.0` → `0.71.0` (current-at-execution + minor, if another piece landed first) in exactly three fields: `.claude-plugin/plugin.json` `version`, `.claude-plugin/marketplace.json` `metadata.version`, `.claude-plugin/marketplace.json` `plugins[0].version`. Do NOT touch either `description` field — no skill surface changed. Root `README.md` untouched (decision recorded in scope).
**Why:** a new repo tool is a feature; R1 is machine-enforced on every push.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py release` → `release: clean`, and `python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])"` → `0.71.0`.

### Step 9: canvas + collateral review [keep]
**What:** open/screenshot `docs/plans/progress.svg` (headless-Chrome command from `tools/diagram/README.md`) and put the drawing in front of the human on the live canvas; walk the board and strips against the Step 6 truths. Then review the full collateral diff (`git status` + `git diff`) — every touched file justified by a step above, nothing else.
**Why:** judgment seam — the render's whole job is to be read by the human; only he can say the drawing tells the truth legibly.
**Verify:** explicit human GO recorded in the session before Step 10 runs.

### Step 10: ship — the first trailer commit [keep]
**What:** check box 10 below, then ONE commit of all touched files (the entry-gates precedent: the piece ships whole, docs with code). Commit message: subject `Progress renderer: the pull view — board and goal strips from disk (0.71.0)`; body ends with ten trailer lines `Piece: progress-renderer/1` … `Piece: progress-renderer/10`. Push immediately (CLAUDE.md rule). Watch CI: four steps green (gate selftest, audit, release, progress selftest). Then re-run `python3 tools/diagram/progress.py`.
**Why:** the shipping commit is the first live `Piece:` evidence in history — the build lands inside its own instrument, and the re-render proves the cross-check end to end.
**Verify:** CI green on the pushed commit, and the post-push re-render's `GOAL` line for `progress-renderer` reads `10 landed · 0 in flight · 0 remaining` (trailer mode) with `drift: none`.

---

## Pieces

- [x] Step 1: progress_kit.py — derivation
- [x] Step 2: render_table — the terminal pull
- [x] Step 3: build_canvas — the drawing
- [x] Step 4: progress.py — the shell
- [x] Step 5: selftest — the fixture suite
- [x] Step 6: the truthful render — today's tree
- [x] Step 7: docs travel with code — README + CI
- [x] Step 8: release checklist
- [x] Step 9: canvas + collateral review
- [x] Step 10: ship — the first trailer commit
