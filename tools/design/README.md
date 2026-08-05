# The evaluation matrix — format standard and refuser

This document is the canonical write-down of the evaluation matrix format, the machine half of the design instrument (`docs/design/design-instrument.md`). The evaluation matrix settles which approach wins on evidence. The conversation half — approach generation — is convention; this tool checks only the artifact.

## Usage

```
python3 tools/design/matrix.py check <file> [--json]   # validate one doc — exit 0 clean / 1 problems
python3 tools/design/matrix.py audit [--json]           # sweep docs/design/*.md — exit 0 clean / 1 problems
python3 tools/design/matrix.py render <file>            # movement-9-style table -> .excalidraw + .svg — exit 0 / 1 (refuses an invalid matrix)
python3 tools/design/matrix.py selftest                 # fixture suite in temp trees — exit 0 / 1
```

Any other invocation prints usage and exits 2.

## Opting in — and the scope

A document opts in to evaluation matrix validation by carrying a `## Evaluation matrix` heading (exact, case-sensitive). The `audit` command scans `docs/design/*.md` ONLY. Records (`docs/plans/`, `docs/gates/`, `kivna/`), fixtures, and this README's own worked example are never scanned. A tree with no opted-in document passes vacuously.

## The seven sections

A document that opts in must carry ALL seven sections, non-empty, in this file order (M1):

`## Criteria` < `## Options` < `## Evaluation matrix` < `## Preferred solution` < `## Proposal and next steps` < `## Risks and countermeasures required` < `## Countermeasures`

Criteria-before-options-before-scores is the file-order encoding of "targets and weights are declared BEFORE any option is scored".

## Criteria

**M2 — `## Criteria`.** Header exactly `Criterion | Group | Target / Minimum | Category | Weight`. ≥1 data row.

Per row: Criterion non-empty and unique; Group non-empty; Target / Minimum non-empty (the declared bar); Category ∈ {`M`, `D`}; Weight either empty or a positive integer — and across the table, ALL empty (criteria weigh equally, weight 1) or ALL integers. Mixed is a violation.

## Options

**M3 — `## Options`.** Header exactly `Option | Description | Architecture overview`. ≥2 data rows (one option is not a comparison).

Option ID matches `^[A-Z][A-Za-z0-9-]*$`, unique. Description non-empty. Architecture overview is a repo-relative path to a file that EXISTS — the drawn overview is a matrix requirement, not decoration.

## The matrix cells

**M4 — `## Evaluation matrix`.** Header exactly `Criterion` followed by the declared option IDs, in declared order. One data row per declared criterion, in declared order — a row whose Criterion traces to no declaration is a named refusal ("scored criterion with no declaration"), a declared criterion with no row is a named refusal.

Cell grammar: `^([○△×])(?:[ \t]+([1-5])[ \t]+—[ \t]+(\S.*))?$` — mark ○ (U+25CB), △ (U+25B3), × (U+00D7); optional score on the declared 1–5 scale with a mandatory em-dash-separated basis.

Mode is uniform: every cell scored, or no cell scored ("marks always, scores when the stakes are real"). A score whose basis is absent fails the cell grammar and is named as "score without basis".

The three marks and their meanings:
- ○ meets, no countermeasure needed
- △ meets only WITH a countermeasure, named, with confidence
- × cannot meet, no countermeasure — on an M criterion the option is DEAD regardless of score

## Arithmetic

**M5 — arithmetic.** Scored mode: exactly two extra rows after the criterion rows, `OVERALL` then `RANK`. The validator RECOMPUTES: OVERALL(option) = Σ score × weight; RANK by competition ranking on OVERALL (highest = 1, ties share). Declared values must equal recomputed — drift is a named refusal.

Marks-only mode: OVERALL/RANK rows must be absent.

## Countermeasures

**M6 — `## Countermeasures`.** Every △ cell requires exactly one row; a row citing a cell not marked △ is a violation. Header exactly `Option | Criterion | Countermeasure | Type | Confidence | Return condition`.

Countermeasure non-empty; Type ∈ {`permanent`, `temporary`}; Confidence non-empty (the confidence statement); Type `temporary` requires Return condition non-empty.

When zero △ cells exist, no table is required — the section body just must be non-empty (state that no countermeasures were needed).

## Preferred solution

**M7 — `## Preferred solution`.** First non-blank line matches `^<OptionID> — ` where OptionID is declared. An option carrying × on any M-category criterion is DEAD: it must not be preferred, regardless of OVERALL — the named refusal is "dead option preferred" and it names the M criterion.

Scored mode: the preferred option's OVERALL must be ≥ every other LIVING option's OVERALL (rank decides among the living).

Marks-only mode: preferred must merely be living.

Problem strings follow the gates idiom: `<relpath> — <what>`.

## Worked example

This complete example document (note: in a real document the two overview paths must exist on disk):

```
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
```

Arithmetic is real: A = 4·1 + 5·3 + 1·2 = 21; B = 3·1 + 5·3 + 4·2 = 26. A's × sits on a D criterion, so A is alive but outranked; the example's verdict is also this build's recorded CI decision.

## Rendering

`render` draws options as rows and criteria as columns in the movement-9 table idiom (row height follows the tallest cell), writing `<stem>-matrix.excalidraw` + `.svg` beside the doc.

Colour grammar honoured: RED marks cost — × cells, dead option rows, and the header of any criteria group named `cost`; GREEN is reserved for Tony's hand annotations and is never generated; BLUE marks text changed since the last reviewed snapshot (the diagram kit's mark_deltas). The three layout checks (overflow, box collision, text overlap) run on every render.

## CI

Two workflow steps fire on every push: Matrix selftest and Matrix audit. A broken matrix in a living design doc fails the build on GitHub's infrastructure, not inside a session.
