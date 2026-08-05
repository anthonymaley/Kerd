---
route: new
stage: contracted
---

# The design instrument's machine half — spec

Builds the evaluation matrix as a machine-checked artifact per
`docs/design/design-instrument.md` (post-walk decision 2, form A — a tool,
not a skill). Three deliverables: a structured matrix section format living
inside living design docs, `tools/design/` (kit + CLI + canonical README +
fixture selftest, on the tools/gates precedent), and CI wiring so validation
fires wherever a matrix section exists. Plus the one-time prompt-set salvage
from the superpowers brainstorming skill, and the v0.77.0 release.

Version: 0.76.0 → **0.77.0** (MINOR — new feature; three version locations).

**Capability list: NO change.** Precedent is decisive — tools/gates (v0.75.0
era) and the progress renderer shipped without touching the capability list;
it describes skills, and this release adds a tool. `plugin.json` and
`marketplace.json` descriptions are untouched; only versions move.

**CI wiring choice: new workflow steps, not gate.py audit.** A standalone
audit keeps tools/gates self-contained (AU1–AU4 remain its whole contract,
its README stays true without edits), follows the progress-selftest
precedent of one workflow entry per tool, and avoids coupling two kits the
directory split just separated. The worked example in the new README records
this same comparison as the format's first filled matrix.

**Validation scope (composer-ruled):** living design docs only —
`docs/design/*.md`. Dated records (`docs/plans/`, `docs/gates/`),
`kivna/`, fixtures, and the README's own example are never scanned. A doc
opts in by carrying a `## Evaluation matrix` heading (exact, the
find_section idiom); everything else passes vacuously — the front-matter
"validated wherever present" shape, with "wherever" bounded to living
design docs.

**Composer amendment governs every rewritten passage**: a wrong line does
not survive; no-touch protection is for correct content only. Every doc
edit below is exact text, validated against disk at spec-writing time
(2026-08-04). If a step's verify does not produce its expected output, or
an old string does not match the file, the player STOPS and hands back to
the orchestrator. No improvisation.

## Surface

The diff may touch ONLY these files (plus this spec file itself):

- `tools/design/README.md` (new — the canonical format standard)
- `tools/design/kit.py` (new — parse, validate, render, selftest)
- `tools/design/matrix.py` (new — CLI)
- `.github/workflows/gate.yml` (two steps appended)
- `docs/design/design-instrument.md` (prompt-set salvage + tool pointer)
- `README.md` (What's New v0.77.0 + Design matrix tools section)
- `.claude-plugin/plugin.json` (version only)
- `.claude-plugin/marketplace.json` (versions only)

**Deliberately not touched**: `tools/gates/` (its README declares AU1–AU4
as its whole audit contract — folding matrix rules in would falsify it);
`skills/conductor/SKILL.md` (seedbed rule — the protocol sheds pieces only
as replacements prove, and nothing here replaces a conductor piece);
every other `skills/*/SKILL.md` (no new skill, no routing changes — the
conversation half stays convention this release); `docs/playbook.md`
(its line-130 superpowers mention is the shakh-rename lesson's context —
editing it rewrites why the lesson happened); `docs/lorg-report.md` (a
generated scan report — its superpowers hits are marketplace listing data,
not routing); `tools/diagram/*` (the render imports the diagram kit,
never edits it).

**Records — never edited**: `kivna/sessions/`, dated `docs/plans/` files
(this spec included), `docs/gates/`, README What's New history entries
(the `superpowers:writing-plans` mention at README:118 sits inside the
v0.39.0 entry — a record, LEFT). **Session state — not spec steps**:
`CONTEXT.md` and `TODO.md` are the conductor's own close-out updates,
excluded from this spec and its surface.

## Pieces

- [x] 1. Format standard: tools/design/README.md
- [x] 2. kit.py — parse + validate + selftest (F1–F13)
- [x] 3. kit.py — renderer + glyph fixture (F14)
- [x] 4. matrix.py — CLI
- [x] 5. CI wiring + refusal demonstrated both ways
- [x] 6. Salvage: the prompt set lands in design-instrument.md
- [x] 7. Superpowers living-doc sweep (verify-only)
- [x] 8. README: What's New v0.77.0 + Design matrix section
- [x] 9. Manifests: triple version bump
- [x] 10. Collateral diff review
- [x] 11. Ship

## The format, normatively (shared by steps 1, 2, 4)

A doc opts in with a `## Evaluation matrix` heading. Once opted in, ALL
seven sections are required, non-empty (find_section semantics: `## <title>`
exact and case-sensitive, body before the next `## `), and in this file
order (M1):

`## Criteria` < `## Options` < `## Evaluation matrix` <
`## Preferred solution` < `## Proposal and next steps` <
`## Risks and countermeasures required` < `## Countermeasures`

Criteria-before-options-before-scores is the file-order encoding of
"targets and weights are declared BEFORE any option is scored".

Tables use the risk-ledger pipe idiom: exact header row, optional
`|---|` separator skipped, `_split_row` cell splitting, no `|` inside
cells.

**M2 — `## Criteria`.** Header exactly
`Criterion | Group | Target / Minimum | Category | Weight`. ≥1 data row.
Per row: Criterion non-empty and unique; Group non-empty;
Target / Minimum non-empty (the declared bar); Category ∈ {`M`, `D`};
Weight either empty or a positive integer — and across the table, ALL
empty (criteria weigh equally, weight 1) or ALL integers. Mixed is a
violation.

**M3 — `## Options`.** Header exactly
`Option | Description | Architecture overview`. ≥2 data rows (one option
is not a comparison). Option ID matches `^[A-Z][A-Za-z0-9-]*$`, unique.
Description non-empty. Architecture overview is a repo-relative path to a
file that EXISTS — the drawn overview is a matrix requirement, not
decoration.

**M4 — `## Evaluation matrix`.** Header exactly `Criterion` followed by
the declared option IDs, in declared order. One data row per declared
criterion, in declared order — a row whose Criterion traces to no
declaration is a named refusal ("scored criterion with no declaration"),
a declared criterion with no row is a named refusal. Cell grammar:
`^([○△×])(?:[ \t]+([1-5])[ \t]+—[ \t]+(\S.*))?$` — mark ○ (U+25CB),
△ (U+25B3), × (U+00D7); optional score on the declared 1–5 scale with a
mandatory em-dash-separated basis. Mode is uniform: every cell scored, or
no cell scored ("marks always, scores when the stakes are real"). A score
whose basis is absent fails the cell grammar and is named as "score
without basis".

**M5 — arithmetic.** Scored mode: exactly two extra rows after the
criterion rows, `OVERALL` then `RANK`. The validator RECOMPUTES:
OVERALL(option) = Σ score × weight; RANK by competition ranking on
OVERALL (highest = 1, ties share). Declared values must equal recomputed
— drift is a named refusal. Marks-only mode: OVERALL/RANK rows must be
absent.

**M6 — `## Countermeasures`.** Every △ cell requires exactly one row;
a row citing a cell not marked △ is a violation. Header exactly
`Option | Criterion | Countermeasure | Type | Confidence | Return condition`.
Countermeasure non-empty; Type ∈ {`permanent`, `temporary`}; Confidence
non-empty (the confidence statement); Type `temporary` requires
Return condition non-empty. When zero △ cells exist, no table is
required — the section body just must be non-empty (state that no
countermeasures were needed).

**M7 — `## Preferred solution`.** First non-blank line matches
`^<OptionID> — ` where OptionID is declared. An option carrying × on any
M-category criterion is DEAD: it must not be preferred, regardless of
OVERALL — the named refusal is "dead option preferred" and it names the
M criterion. Scored mode: the preferred option's OVERALL must be ≥ every
other LIVING option's OVERALL (rank decides among the living). Marks-only
mode: preferred must merely be living.

Problem strings follow the gates idiom: `<relpath> — <what>`.

## Steps

All commands run from `/Users/anthonymaley/Kerd`. `python3`, never
`python`. Check each Pieces box as its step's Verify passes.

### Step 1 — Format standard: tools/design/README.md [delegate, model: haiku, effort: low]

Create `tools/design/README.md`. It is the canonical write-down of the
format (this spec is the dated record it came from; the README, like the
gates README, becomes the standard). Required content, in order:

1. Title `# The evaluation matrix — format standard and refuser` and an
   intro naming what it is: the machine half of the design instrument
   (`docs/design/design-instrument.md`), the artifact that settles which
   approach wins on evidence; the conversation half (approach generation)
   is convention, this tool checks only the artifact.
2. A `## Usage` section with the four CLI lines and exit codes:

       python3 tools/design/matrix.py check <file> [--json]   # validate one doc — exit 0 clean / 1 problems
       python3 tools/design/matrix.py audit [--json]           # sweep docs/design/*.md — exit 0 clean / 1 problems
       python3 tools/design/matrix.py render <file>            # movement-9-style table -> .excalidraw + .svg — exit 0 / 1 (refuses an invalid matrix)
       python3 tools/design/matrix.py selftest                 # fixture suite in temp trees — exit 0 / 1

   Any other invocation prints usage and exits 2.
3. A `## Opting in — and the scope` section: the `## Evaluation matrix`
   heading is the trigger; audit scans `docs/design/*.md` ONLY; records
   (`docs/plans/`, `docs/gates/`, `kivna/`), fixtures, and this README's
   own example are never scanned; a tree with no opted-in doc passes
   vacuously.
4. A `## The seven sections` section carrying the M1 order rule verbatim
   from this spec's normative block.
5. Sections `## Criteria`, `## Options`, `## The matrix cells`,
   `## Arithmetic`, `## Countermeasures`, `## Preferred solution`
   carrying M2–M7 exactly as written in this spec's normative block —
   including the cell regex, the three marks with their meanings
   (○ meets, no countermeasure needed · △ meets only WITH a
   countermeasure, named, with confidence · × cannot meet, no
   countermeasure — on an M criterion the option is DEAD regardless of
   score), and the mode-uniformity and declared-before-scored rules.
6. A `## Worked example` section containing this complete example doc in
   one fence, with the note that in a real doc the two overview paths
   must exist on disk (the selftest writes stubs for them):

       # Example — where the matrix validation should live

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

   (Arithmetic is real: A = 4·1 + 5·3 + 1·2 = 21; B = 3·1 + 5·3 + 4·2
   = 26. A's × sits on a D criterion, so A is alive but outranked; the
   example's verdict is also this build's recorded CI decision.)
7. A `## Rendering` section: `render` draws options as rows and criteria
   as columns in the movement-9 table idiom (row height follows the
   tallest cell), writing `<stem>-matrix.excalidraw` + `.svg` beside the
   doc. Colour grammar honored: RED marks cost — × cells, dead option
   rows, and the header of any criteria group named `cost`; GREEN is
   reserved for Tony's hand annotations and is never generated; BLUE
   marks text changed since the last reviewed snapshot (the diagram
   kit's mark_deltas). The three layout checks (overflow, box collision,
   text overlap) run on every render.
8. A `## CI` section showing the two workflow steps (Matrix selftest,
   Matrix audit) and the sentence: a broken matrix in a living design
   doc fails the build on GitHub's infrastructure, not inside a session.

**Verify:**

```
grep -c '^## ' tools/design/README.md
grep -n 'Criterion | Group | Target / Minimum | Category | Weight' tools/design/README.md
grep -n 'Option | Description | Architecture overview' tools/design/README.md
grep -n 'Option | Criterion | Countermeasure | Type | Confidence | Return condition' tools/design/README.md
grep -c '○' tools/design/README.md; grep -c '△' tools/design/README.md; grep -c '×' tools/design/README.md
grep -n 'OVERALL | 21 | 26' tools/design/README.md
```

Expected: ≥9 sections; two hits for each of the three header rows (the
normative definition + the worked example); nonzero counts for all three
marks; the OVERALL row present with 21 and 26.

### Step 2 — tools/design/kit.py: parse + validate + selftest [delegate, model: sonnet, effort: high]

Create `tools/design/kit.py`. Module docstring: the refuser for the
evaluation-matrix format — mechanical only, per the gates philosophy (it
checks presence, legality, arithmetic; it has no opinion on whether a
basis is convincing — judgment belongs to whoever fills the matrix).
Stdlib only (`glob`, `os`, `re`, `tempfile`). Every function takes its
inputs as parameters (`root`, `text`) so the selftest can run in temp
trees — the gates idiom.

Constants: `ROOT` (three `os.path.dirname` up, as gates kit line 24);
`MATRIX_HEADING_RE = re.compile(r'^## Evaluation matrix[ \t]*$', re.MULTILINE)`;
`SECTION_ORDER` (the seven titles, M1 order); the three header-cell
lists; `MARK_CELL_RE` per M4; `OPTION_ID_RE = re.compile(r'^[A-Z][A-Za-z0-9-]*$')`.
Reuse the gates parsing idiom by local reimplementation (`find_section`,
`_split_row`, separator-row skip) — do NOT import tools/gates/kit;
the two refusers stay uncoupled (the CI-choice rationale above).

Public functions:

- `has_matrix(text)` → bool — MATRIX_HEADING_RE search.
- `parse_matrix(text, rel)` → `(model, problems)`. Model dict:
  `{"file": rel, "mode": "scored"|"marks", "criteria": [{"name","group","target","category","weight"}], "options": [{"id","description","overview"}], "cells": {option_id: {criterion: {"mark","score","basis"}}}, "overall": {option_id: int}, "rank": {option_id: int}, "dead": [option_id], "preferred": option_id_or_None, "countermeasures": [rows]}`
  — `overall`/`rank` are the RECOMPUTED values (empty dicts in marks
  mode). Implements M1–M7 except the overview-file-exists check (that
  needs `root`); every problem string is `f"{rel} — <what>"`. Named
  problem phrasings that fixtures assert on: `"no declaration"` (M4
  undeclared criterion), `"score without basis"`, `"OVERALL"` (drift),
  `"dead option"` + the M criterion's name (M7), `"section order"`,
  `"Weight"` (mixed), `"countermeasure"` (△ without row / row fields).
- `check_file(root, relpath)` → problems list — reads the file, runs
  `parse_matrix`, then the M3 overview-exists check against `root`. A
  file without a matrix heading returns
  `[f"{relpath} — no ## Evaluation matrix section"]`.
- `audit_matrices(root)` → `(problems, count)` — scans
  `sorted(glob.glob(os.path.join(root, "docs", "design", "*.md")))`,
  runs `check_file` on each file where `has_matrix` is true; `count` is
  the number of opted-in files. Absent directory or zero opt-ins →
  `([], 0)`, vacuous pass.
- `selftest()` — cases F1–F13 below, each in its own
  `tempfile.TemporaryDirectory` where needed (no git required — matrices
  are pure files). Per-case output on the progress-renderer idiom:
  `ok <n> — <name>` per case, `FAIL <n> — <name>: <why>` + return 1 on
  first failure, `selftest: 13 ok` + return 0 on success. (Step 3 extends
  to 14.) The docstring names what the suite does NOT cover, rather than
  silently skipping it: a living-but-not-top preferred option in scored
  mode, and OVERALL ties, have no F-case here.

Fixtures — F1 is the step-1 worked example VERBATIM (byte-identical to
the README fence), with the tree containing stub files
`docs/design/example-option-a.svg` and `docs/design/example-option-b.svg`:

- F1 valid scored — `check_file` returns `[]`; model asserts: mode
  `scored`, preferred `B`, recomputed overall `{"A": 21, "B": 26}`,
  rank `{"B": 1, "A": 2}`, dead `[]`.
- F2 valid marks-only — F1 with every score+basis stripped from cells
  and the OVERALL/RANK rows removed → `[]`; mode `marks`.
- F3 undeclared criterion — F1 plus matrix row
  `| Latency | ○ 4 — x | ○ 4 — x |` → a problem containing
  `no declaration` and `Latency`.
- F4 declared-but-unscored — F1 with the `Render legibility` matrix row
  deleted (OVERALL/RANK adjusted to recompute-clean is NOT needed; the
  missing-row problem is what's asserted) → a problem naming
  `Render legibility`.
- F5 △ without countermeasure — F1 with the Countermeasures table's data
  row deleted (section keeps a prose line so M1 passes) → a problem
  containing `countermeasure` and naming `B` and `Setup cost`.
- F6 temporary without return — F1's countermeasure row with Type
  `temporary` and Return condition left empty → a problem containing
  `Return condition`.
- F7 dead option preferred — F1 with `Render legibility` Category
  changed `D`→`M` and Preferred solution first line changed to
  `A — extends what exists.` → a problem containing `dead option`, `A`,
  and `Render legibility`. (The ×-on-M-ranked-winner refusal.)
- F8 score without basis — F1 with one cell rewritten to `○ 4` → a
  problem containing `score without basis`.
- F9 arithmetic drift — F1 with declared `| OVERALL | 22 | 26 |` → a
  problem containing `OVERALL` and both `22` and `21`.
- F10 section order — F1 with the whole `## Options` section moved above
  `## Criteria` → a problem containing `section order`.
- F11 mixed weights — F1 with `Setup cost`'s Weight cell emptied (others
  keep integers) → a problem containing `Weight`.
- F12 missing overview file — F1 tree WITHOUT the
  `example-option-b.svg` stub → a problem containing
  `example-option-b.svg`.
- F13 audit sweep — one temp tree holding: F1's doc (valid), a broken
  doc (F3's content), and a matrix-free doc (`# Notes` only) →
  `audit_matrices` returns count 2 and exactly the broken doc's
  problems, each prefixed with the broken doc's relpath.

**Verify:**

```
python3 -c "import sys; sys.path.insert(0, 'tools/design'); import kit; sys.exit(kit.selftest())"
```

Expected: thirteen `ok <n> — <name>` lines, then `selftest: 13 ok`,
exit 0.

### Step 3 — kit.py: the renderer + glyph fixture [delegate, model: sonnet, effort: high]

Extend `tools/design/kit.py` (no other file). The diagram toolkit is
loaded BY PATH via `importlib.util` — the D8 idiom from
`tools/diagram/progress_kit.py::load_gates_kit` — because this module is
itself named `kit.py`, and a bare sys.path insert of `tools/diagram`
would silently shadow one kit with the other. Load
`tools/diagram/kit.py` (as `diagram_kit`) and `tools/diagram/to_svg.py`
(as `diagram_to_svg`), once, cached in module globals.

New functions:

- `build_canvas(model, title)` → a `diagram_kit.Canvas`. Contract, not
  pixel geometry (the layout checks are the verify): title text
  `<title> — evaluation matrix` (size 32) with the three-line colour
  legend under it (RED cost / GREEN Tony's input / BLUE changed since
  reviewed — the Flow.__init__ pattern); a header band with one column
  per criterion showing group, name, and `(M|D · <target> · w<weight>)`;
  one row per OPTION (options as rows, criteria as columns — the design
  doc's orientation): a box with the option ID + description at the
  left, one cell per criterion showing the mark (plus `score` in scored
  mode) with the basis as small text beneath, then OVERALL and RANK
  columns in scored mode. Row height follows the tallest cell
  (the movement-9 `_rowh` idiom — fixed spacing is the known stacking
  fault). Colour: × cells RED; a dead option's row boxes RED; criteria
  whose Group is `cost` get a RED header; the preferred option's row box
  gets GREY fill and a `PREFERRED` tag. Below the table: the Preferred
  solution banner line, then one text block per countermeasure row
  (option · criterion · countermeasure · type · confidence · return
  condition). GREEN is never emitted.
- `render(root, relpath)` → `(problems, out, svg_out, dims, deltas)`.
  Runs `check_file` first; problems → `(problems, None, None, None,
  None)` and no file is written (the render refuses an invalid matrix).
  Clean → builds the canvas, calls `diagram_kit.mark_deltas(els,
  out)` (blue honored; returns the (marked, suppressed) counts), writes
  `<dir>/<stem>-matrix.excalidraw` (the gen_excalidraw doc dict shape:
  `{"type": "excalidraw", "version": 2, "source":
  "https://excalidraw.com", "elements": els, "appState": {...},
  "files": {}}`) and `<stem>-matrix.svg` via `diagram_to_svg.to_svg`.

New fixture:

- F14 render — in F1's temp tree, `render` the valid doc: assert
  problems `[]`, both output files exist, `overflow_report`,
  `collision_report`, `text_overlap_report` all return `[]` on the
  canvas elements, and the written SVG text contains all three glyphs
  `○`, `△`, `×` (the glyph-survival assertion — a mark that dies in SVG
  export dies here, not on Tony's canvas).

Update the selftest case list and final line to `selftest: 14 ok`.

**Verify:**

```
python3 -c "import sys; sys.path.insert(0, 'tools/design'); import kit; sys.exit(kit.selftest())"
```

Expected: fourteen `ok` lines ending `ok 14 — render: layout clean, glyphs survive to SVG`, then `selftest: 14 ok`, exit 0.

### Step 4 — tools/design/matrix.py: the CLI [delegate, model: haiku, effort: medium]

Create `tools/design/matrix.py` on the gate.py pattern exactly: module
docstring = usage text (the four subcommand lines from step 1's Usage
section plus the exit-code sentence); `sys.path.insert(0,
os.path.dirname(os.path.abspath(__file__)))` then `import kit`; a
`COMMANDS` dict; `main(argv)` printing the docstring and returning 2 on
unknown/malformed invocations; every decision lives in kit.py — this
module only parses argv and renders.

- `check <file> [--json]` — `<file>` is repo-relative or absolute;
  compute relpath against `kit.ROOT`. Clean: print
  `matrix: clean — <relpath> (<o> options × <c> criteria, <mode>)`,
  exit 0. Problems: one `problem: <p>` line each, then
  `matrix: <n> problems`, exit 1. `--json` dumps the model dict (with a
  `"problems"` key added), exit 0/1 by problems.
- `audit [--json]` — `kit.audit_matrices(kit.ROOT)`. Clean:
  `matrix audit: clean (<count> matrices)`, exit 0. Problems: `problem:`
  lines + `matrix audit: <n> problems`, exit 1. `--json` dumps the
  problems list.
- `render <file>` — `kit.render`. Problems: print them + exit 1.
  Clean: print `wrote <out>`, `wrote <svg_out> (<w>x<h>)`, the delta
  counts (`deltas: <marked> marked, <suppressed> suppressed` — or
  `never reviewed` when both are 0 and no snapshot exists), and the
  three layout reports in the progress.py output shape. Exit 0.
- `selftest` — `sys.exit(kit.selftest())`.

**Verify:**

```
python3 tools/design/matrix.py selftest
python3 tools/design/matrix.py audit; echo "exit: $?"
python3 tools/design/matrix.py check docs/design/design-instrument.md; echo "exit: $?"
python3 tools/design/matrix.py bogus; echo "exit: $?"
```

Expected: `selftest: 14 ok`; `matrix audit: clean (0 matrices)` then
`exit: 0` (no living doc has opted in yet — and this proves the trigger
is the exact heading: design-instrument.md's `## Half two — the
evaluation matrix` does NOT trip it); the check prints
`problem: docs/design/design-instrument.md — no ## Evaluation matrix section`
then `matrix: 1 problems` then `exit: 1`; usage text then `exit: 2`.

### Step 5 — CI wiring + refusal demonstrated both ways [keep]

Edit `.github/workflows/gate.yml`. Old (the file's last two lines):

```
      - name: Progress selftest
        run: python3 tools/diagram/progress.py selftest
```

New:

```
      - name: Progress selftest
        run: python3 tools/diagram/progress.py selftest
      - name: Matrix selftest
        run: python3 tools/design/matrix.py selftest
      - name: Matrix audit
        run: python3 tools/design/matrix.py audit
```

Then the refusal demo, both ways (the entry-gates canary pattern):

Way 1 — CLI, on the real tree. Pre-check `git status --short docs/design/`
is empty (the plant/revert gotcha: verify the tree before and after any
step that mutates uncommitted files). Write
`docs/design/zz-matrix-canary.md`:

```
# ZZ canary — refusal demo, never committed

## Evaluation matrix

| Criterion | A |
|---|---|
| Undeclared thing | ○ |
```

Run `python3 tools/design/matrix.py audit` — must exit 1 with problems
naming `docs/design/zz-matrix-canary.md`. Then
`rm docs/design/zz-matrix-canary.md`, run audit again — must print
`matrix audit: clean (0 matrices)` and exit 0, and
`git status --short docs/design/` must be empty again.

Way 2 — the CI path: the same command now runs on every push. The
ship step (11) verifies the headSha-matched run shows BOTH new steps
executed green; command identity plus Way 1 is the refusal evidence — a
red commit is not pushed to prove it.

**Verify:** the gate.yml diff shows exactly the two appended steps
(`git diff .github/workflows/gate.yml` — 4 added lines, 0 removed); the
Way-1 sequence produced exit 1 naming the canary, then exit 0, with a
clean `docs/design/` tree after.

### Step 6 — Salvage: the prompt set lands in design-instrument.md [delegate, model: haiku, effort: low]

Three edits to `docs/design/design-instrument.md`, exact text (old
strings validated against disk 2026-08-04).

Edit A — the salvage note flips to past tense. Old:

```
- One-time salvage: brainstorming's probing questions get mined into this
  instrument's prompt set; after that the superpowers dependency is cut.
```

New:

```
- One-time salvage (done 2026-08-04): brainstorming's probing questions
  were mined into *The prompt set* below; the superpowers tie is cut.
```

Edit B — insert the prompt set as a new section. Immediately before the
line `## Half two — the evaluation matrix`, insert (with one blank line
after the inserted block, preserving the existing blank line above the
Half-two heading):

```
## The prompt set

Mined once from the superpowers brainstorming skill (2026-08-04), adapted
to this system's grammar: one question per turn, open questions — never
multiple-choice menus, which pre-narrow the answer space. Used while
generating approaches, before anything is scored.

**Framing probes** — before any approach exists:

- What is this for — what changes for whom when it works?
- Which constraints are actually fixed (platform, budget, standing
  decisions), as opposed to habits worth questioning?
- What does success look like, in the declared VALUE's units?
- Is this ONE piece of work? If it hides several independent subsystems,
  decompose first and evaluate the first piece — a matrix over a bundle
  compares nothing.

**Independence probes** — while generating the 2–3 approaches:

- What is this approach's riskiest assumption? If two approaches share
  it, they are one approach — generate a genuinely different mechanism.
- What does each approach look like drawn? No architecture overview, no
  option row.
- What is the smallest version of each approach that still wins its case
  — what survives YAGNI?

**Boundary probes** — per approach, before scoring:

- For each unit: what does it do, how is it used, what does it depend on?
- Could someone understand a unit without reading its internals? Could
  the internals change without breaking consumers? If not, the
  boundaries need work before the option is scoreable.
- Does the approach follow the patterns of the code it touches, or
  import a foreign idiom — and if foreign, is that cost on the matrix?

**Self-review scans** — on the filled matrix, before the verdict:

- Placeholder scan: any TBD, any vague target, any score without basis?
- Consistency scan: does any closing section contradict a mark?
- Ambiguity scan: could any criterion's target be read two ways? Pick
  one reading and write it down.

```

Edit C — the Rendering section names the instrument. Old:

```
A movement-9-style table via the diagram toolkit (`tools/diagram/`) —
never a spreadsheet. The matrix is an everyday-tier render during the
design conversation; the design package's copy is part of the package
document.
```

New:

```
A movement-9-style table via the diagram toolkit (`tools/diagram/`) —
never a spreadsheet. The instrument is `tools/design/matrix.py`: `check`
validates a matrix section, `audit` sweeps every living design doc on
every push (the CI instance), `render` draws the table to Excalidraw +
SVG beside the doc. The section format standard is
`tools/design/README.md`. The matrix is an everyday-tier render during
the design conversation; the design package's copy is part of the
package document.
```

**Verify:**

```
grep -n '^## The prompt set' docs/design/design-instrument.md
grep -n 'One-time salvage (done 2026-08-04)' docs/design/design-instrument.md
grep -n 'tools/design/matrix.py' docs/design/design-instrument.md
grep -c 'superpowers' docs/design/design-instrument.md
grep -n '^## ' docs/design/design-instrument.md
```

Expected: the new heading present between the Half-one and Half-two
sections; the past-tense note; the tool pointer in Rendering; exactly
`2` superpowers mentions (the past-tense note + the prompt-set
provenance line — both historical, neither routing); the heading list
shows all previous `## ` sections surviving in order with `## The prompt
set` added (the insert-before-heading gotcha: confirm the `## Half two`
heading survived).

### Step 7 — Superpowers living-doc sweep (verify-only) [delegate, model: haiku, effort: low]

No edit. Post-salvage acceptance: zero superpowers ROUTING references in
living docs; records exempt. A routing reference is the invocation form
(`superpowers:<skill>`) or an instruction to use the plugin; a historical
mention is not routing.

**Verify:**

```
grep -rn 'superpowers:' skills/ docs/design/ docs/playbook.md docs/state-contract.md docs/vault-spec.md CLAUDE.md; echo "exit: $?"
grep -rn 'superpowers' skills/ CLAUDE.md docs/state-contract.md docs/vault-spec.md; echo "exit: $?"
grep -rn 'superpowers' docs/design/ docs/playbook.md docs/lorg-report.md
grep -n 'superpowers' README.md
grep -n '^## Skills' README.md
```

Expected, exactly:

- Line 1: no hits, `exit: 1` — zero routing-form references anywhere in
  the living set.
- Line 2: no hits, `exit: 1` — skills/, CLAUDE.md, state-contract,
  vault-spec carry no superpowers text at all.
- Line 3: hits ONLY in `docs/design/design-instrument.md` (the two
  historical mentions from step 6), `docs/playbook.md:130` (the
  shakh-rename lesson's context — LEAVE), and `docs/lorg-report.md`
  (two hits, marketplace listing data in a generated report — LEAVE).
- Lines 4–5: README hits sit at line numbers ABOVE the `## Skills`
  heading — inside What's New history entries only (the v0.39.0 record
  at ~:118, plus the new v0.77.0 entry once step 8 lands). Any hit at or
  below `## Skills` ⇒ FAIL, hand back.

Any other outcome ⇒ FAIL, hand back — do not improvise a fix.

### Step 8 — README: What's New v0.77.0 + Design matrix section [delegate, model: haiku, effort: medium]

Two edits to `README.md`, in this order.

**Verify:** run the command block at the end of this step after both
edits land; every expected line must match. (This marker sits here
because the insertion payload below carries a `### v0.77.0` line, and
the gates' line-based step scanner stops at the first `###` it meets —
the fence is invisible to it.)

Edit A — What's New. Change line 14 from `## What's New (v0.76.0)` to
`## What's New (v0.77.0)`, then insert immediately after it (before
`### v0.76.0`):

```

### v0.77.0

**The evaluation matrix becomes machine-checked — new tool `tools/design/matrix.py`.** The design instrument (`docs/design/design-instrument.md`) settles which approach wins on evidence; its artifact now has a format standard and a refuser. A living design doc opts in by carrying a `## Evaluation matrix` section; the tool then validates the whole complex — criteria declared BEFORE options, each with a Target/Minimum, an M/D category and optional weights; options as rows with drawn architecture overviews; Toyota marks (○/△/×) per cell, scores citing a basis; recomputed OVERALL and RANK; every △ carrying a named countermeasure with a confidence statement; and the closing sections in the exemplar's order (Preferred solution · Proposal and next steps · Risks and countermeasures required · Countermeasures). The named refusals: a scored criterion tracing to no declaration, a score without basis, a △ without countermeasure + confidence, arithmetic drift, and a dead option (× on a Mandatory criterion) named Preferred — dead options cannot win, regardless of score. `check` validates one doc, `audit` sweeps `docs/design/` on every push as two new CI steps beside the gate and progress checks, `render` draws the movement-9-style table to Excalidraw + SVG via the diagram toolkit, refusing an invalid matrix. Format standard: `tools/design/README.md`. Scope, deliberate: validation covers living design docs only — records and fixtures are exempt — and the conversation half (approach generation) stays convention this release; its prompt set was mined once from the superpowers brainstorming skill into the design-instrument doc, and that tie is now cut.
```

Edit B — the tools section. Immediately before the line
`## How They Fit Together`, insert:

```
## Design matrix (tools/design/)

The evaluation matrix is how options are compared — criteria with declared targets and M/D categories set before any option is scored, options as rows each with a drawn architecture overview, Toyota marks per cell (○ = meets · △ = meets only with a named countermeasure · × = cannot meet), scores citing evidence, and a recomputed OVERALL/RANK. The tool refuses what the format forbids: undeclared criteria, scores without basis, △ without countermeasure + confidence, arithmetic drift, and a dead option (× on a Mandatory criterion) named Preferred. Validation fires wherever a matrix section exists in `docs/design/*.md` — on every push, in CI.

```
python3 tools/design/matrix.py check <file>    # validate one design doc
python3 tools/design/matrix.py audit           # sweep docs/design/ — the CI step
python3 tools/design/matrix.py render <file>   # movement-9-style table → .excalidraw + .svg
```

```

(The fence inside this insertion is a plain triple-backtick command
block, matching the Entry gates section's shape; keep exactly one blank
line between the inserted block and `## How They Fit Together`.)

**Verify:**

```
sed -n '14p' README.md
grep -n '### v0.77.0' README.md
grep -n '^## Design matrix (tools/design/)' README.md
grep -n '^## Entry gates (tools/gates/)' README.md
grep -n '^## How They Fit Together' README.md
sed -n '5p' README.md | cut -c1-3
```

Expected: `## What's New (v0.77.0)`; the new entry at ~line 16; the new
section heading sits BETWEEN the Entry gates heading and How They Fit
Together; line 5 still starts `Ten` (the skill count is untouched — this
release adds a tool, not a skill).

### Step 9 — Manifests: triple version bump [delegate, model: haiku, effort: low]

Version `0.76.0` → `0.77.0` in all three places: `plugin.json` →
`version`; `marketplace.json` → `metadata.version`; `marketplace.json` →
`plugins[0].version`. BOTH `description` fields and
`metadata.description` are untouched (capability list: no change — this
release adds a tool, and the tooling layer has never been in the
capability list).

**Verify:**

```
python3 -c "
import json
a=json.load(open('.claude-plugin/plugin.json')); b=json.load(open('.claude-plugin/marketplace.json'))
print(a['version'], b['metadata']['version'], b['plugins'][0]['version'])
print(a['description']==b['plugins'][0]['description'])
print(a['description'].startswith('Opinionated workflow toolkit:'))
print('matrix' in a['description'])"
```

Expected:

```
0.77.0 0.77.0 0.77.0
True
True
False
```

### Step 10 — Collateral diff review [keep]

```
git add -A -n; git status --short
```

Expected changed paths, exactly and only: `tools/design/README.md` (new),
`tools/design/kit.py` (new), `tools/design/matrix.py` (new),
`.github/workflows/gate.yml`, `docs/design/design-instrument.md`,
`README.md`, `.claude-plugin/plugin.json`,
`.claude-plugin/marketplace.json`,
`docs/plans/2026-08-04-design-instrument-spec.md` (new, this spec) —
plus possibly `CONTEXT.md`/`TODO.md` (session state, never staged with
this commit). `tools/design/__pycache__/` is covered by the existing
`__pycache__/` gitignore rule and must NOT appear. Any other path ⇒
FAIL, hand back.

Then read the full diff (`git diff` + the new files) for drift against
this spec's exact strings: the canary file must be gone, gate.yml must
show only the two appended steps, no edit outside the surface.

**Verify:** the status list matches the expected set exactly;
`test -e docs/design/zz-matrix-canary.md && echo STILL-THERE || echo GONE`
prints `GONE`.

### Step 11 — Ship [keep]

1. Run the full local gate — the four checks CI enforced before this
   release plus the two this release adds. All must exit 0; any failure
   ⇒ hand back, do not ship:

```
python3 tools/gates/gate.py selftest
python3 tools/gates/gate.py audit
python3 tools/gates/gate.py release
python3 tools/diagram/progress.py selftest
python3 tools/design/matrix.py selftest
python3 tools/design/matrix.py audit
```

2. Check Pieces box 11 in this spec, then stage by name:

```
git add tools/design/README.md tools/design/kit.py tools/design/matrix.py .github/workflows/gate.yml docs/design/design-instrument.md README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json docs/plans/2026-08-04-design-instrument-spec.md
```

3. Commit with piece trailers (conductor appends its own session trailer
   per its conventions). Trailers cover pieces 1–10 only: a commit cannot
   witness its own landing, so `Piece: design-instrument/11` is
   explicitly assigned to the follow-up render-refresh commit — the
   sherpa and mode cuts hit exactly this:

```
Build the evaluation matrix's machine half (v0.77.0)

tools/design/ lands on the gates precedent: a format standard
(README), a kit that parses, validates and renders the evaluation
matrix, a CLI, and a 14-case fixture selftest in temp trees. A living
design doc opts in with an Evaluation matrix section; CI then refuses
undeclared criteria, scores without basis, triangles without named
countermeasures + confidence, arithmetic drift, and a dead option
named Preferred. Render draws the movement-9 table to Excalidraw +
SVG, glyph survival fixture-checked. The brainstorming prompt set is
salvaged into the design-instrument doc and the superpowers tie cut;
the living-doc sweep confirms zero routing references remain.

Piece: design-instrument/1
Piece: design-instrument/2
Piece: design-instrument/3
Piece: design-instrument/4
Piece: design-instrument/5
Piece: design-instrument/6
Piece: design-instrument/7
Piece: design-instrument/8
Piece: design-instrument/9
Piece: design-instrument/10
```

4. Push, then verify CI against the PUSHED sha — `gh run list` right
   after a push can return the previous run (playbook gotcha):

```
git push
git rev-parse HEAD
gh run list --limit 3
```

   Match the run's `headSha` to the pushed sha before `gh run watch
   <run-id>`. The run must be green with all SIX steps listed —
   including `Matrix selftest` and `Matrix audit` (Way 2 of the step-5
   refusal demonstration: the refusing command now fires on GitHub's
   infrastructure on every push).

5. Follow-up — the living progress render (the new spec's 11 pieces now
   appear on the board, derived from disk):

```
python3 tools/diagram/progress.py
git add docs/plans/progress.excalidraw docs/plans/progress.svg
git commit -m "Refresh the living progress render; land the instrument's ship piece

Piece: design-instrument/11"
git push
```

   Verify this second push's run goes green the same headSha-matched way.

**Verify:** all six gate commands exit 0; after the ship commit,
`git status --short` shows nothing staged and no surface file modified
(only `CONTEXT.md`/`TODO.md` may remain dirty — session state, committed
later by switch); both pushes accepted; both headSha-matched CI runs
green with six steps.
