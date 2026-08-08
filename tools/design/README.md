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

**`M` is MANDATORY; `D` is DESIRABLE.** The letter describes the *criterion's status* — mandatory versus nice-to-have — and never the option's performance against it. A `×` on an `M` kills the option outright; a `×` on a `D` does not. This was never written down until a reader asked on 2026-08-08 whether `M` meant "meets", which is the natural reading and a dangerous one, since *meets* is already the definition of `○`. The markdown keeps the letters because the machine parses them; **the render spells them out**, because the canvas is read by a person.

## Options

**M3 — `## Options`.** Header exactly `Option | Description | Architecture overview`. ≥2 data rows (one option is not a comparison).

Option ID matches `^[A-Z][A-Za-z0-9-]*$`, unique. Description non-empty. Architecture overview is a repo-relative path to a file that EXISTS — the drawn overview is a matrix requirement, not decoration.

## The matrix cells

**M4 — `## Evaluation matrix`.** Header exactly `Criterion` followed by the declared option IDs, in declared order. One data row per declared criterion, in declared order — a row whose Criterion traces to no declaration is a named refusal ("scored criterion with no declaration"), a declared criterion with no row is a named refusal.

Cell grammar: `^((?:◎|○[+\-−]?|△[+\-−]?|×))(?:[ \t]+(?:([1-5])[ \t]+)?—[ \t]+(\S.*))?$` — a mark from the set below, then an optional em-dash-separated basis which may itself carry a score on the declared 1–5 scale. So `○`, `△- — reason`, and `◎ 5 — reason` are all legal shapes.

**Only `◎` and bare `○` may stand without a reason** (2026-08-08). Everything else — including the refinements `○+` and `○-` — is a named refusal without one: *"'△+' with no reason (only ◎ and ○ may stand bare)"*. An unqualified pass needs no explanation because the Criteria table already declares the target it met; a refinement carries no information at all without one. Tony's rule: *"when we give a rating in a cell we need to say why if its not circle, just a few words"* — and *"the point of the table is to avoid the reading of lots of text to understand the eval"*, so reasons are a few words, not a sentence. Fixtures F15 and F16 pin it.

The score being optional **inside** the basis group is what lets a marks-only matrix carry reasons without being forced into scored mode — which would have obliged a 1–5 score and a basis on every cell, plus OVERALL/RANK, to earn a four-word reason.

Mode is uniform: every cell scored, or no cell scored ("marks always, scores when the stakes are real"). A score whose basis is absent fails the cell grammar and is named as "score without basis".

### The mark set

Defined by the producer, 2026-08-08. The classic four-mark scale, with refinements available when three marks do not separate the options finely enough.

| Mark | Name | Means |
|---|---|---|
| `◎` | double circle | a **perfect fit** — exceeds the declared target. The conventional form of `○+`. |
| `○` | circle | **fully meets** the target as it stands, nothing added. Refine with `○+` / `○-`. |
| `△` | triangle | **can meet it, but only with a countermeasure.** Refine with `△+` (cheap, likely) / `△-` (expensive, uncertain). |
| `×` | cross | **cannot meet it, even with a countermeasure.** On an M criterion the option is DEAD regardless of score. |

**`×` takes no modifier** — "cross is always just cross", because there is no degree of impossibility. `×-` is a named refusal that says so, rather than the misleading "score without basis" the generic branch would have produced.

**The decisive test between `×` and `△`:** is there *any* countermeasure that reaches the declared target? If yes the mark is `△`, however expensive. `×` is reserved for genuine impossibility. **"We have not built it yet" is not `×`** — it is `△` with the build as the countermeasure, and that distinction is what the producer's 2026-08-08 definition exists to force.

**Building the missing piece ourselves IS a legal countermeasure** — the producer's ruling, 2026-08-08, which overrode a draft rule of mine that forbade it:

> *"If the fix is 'also build a register' yes but it does make it viable, we would reflect that as TRIANGLE - and then show more effort in complexity, cost, due date to weight it down compared to build. but it could mean that everything else with that option is double circle and we just need to invest in build on one aspect and it could be ideal kind of thing"*

So an option that reaches the target only because we build the gap ourselves is `△-`, never `×`. **The cost of that investment is not hidden in the mark — it is carried by the summary criteria** (Cost, Quality, Due date), which weigh the option down against the pure build.

**Why the draft rule was wrong, recorded because it is the instructive part:** forbidding option-swap countermeasures marks the gap `×`, and an M-category `×` kills the option outright. That would erase exactly the shape worth finding — an option that is `◎` on twelve criteria and `△-` on one, where the right answer is *use the tool for what it is excellent at and build the one missing piece*. A rule that hides the best hybrid is worse than a rule that lets a weak option survive to be judged on cost.

The consequence is that **`×` becomes rare**, and that is intended. Reserve it for genuine impossibility: a grammar the vendor controls and will not change, a target stated in absolute terms that no investment can reach (*"nothing beyond Python 3 stdlib"* cannot be reached by anything requiring an install), a dead project that will never ship the feature.

Every rule in `kit.py` keys off `mark_family()` — `circle` / `triangle` / `cross` — never the exact glyph, so adding or retiring a refinement can never silently change which options are dead or which cells owe a countermeasure.

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

**Colour grammar — amended 2026-08-08 on Tony's call** (*"boxes never colored, the circle is green, triangle yellow and cross is red — make the size of them at least 40-50% of the box they are in"*). The verdict lives in the mark, not in the border:

- **Boxes are never coloured.** Every rectangle strokes INK, including cost-group headers and dead option rows, both of which used to stroke RED.
- **`○` GREEN · `△` YELLOW · `×` RED**, and in marks-only mode the mark is drawn at **half the cell** (bounded by the narrower axis, floor 18pt) as the cell's own bound text. Bound rather than floating is what keeps `collision_report` clean — it exempts bound text, and a free glyph over a small box is a fault by that checker's definition. `Canvas.box` cannot express this because it paints border and text from one `stroke`; `_marked_box` exists for exactly that split. A mark that is not `○` **must carry a reason** — `△ — needs a stdlib checker` is legal in marks-only mode as of 2026-08-08, the score being optional inside the basis group, and the checker refuses a bare `△` or `×`. Column and row headings render as headings (`FIT: SAME FILES`, `OPTION 1: BUILD`), and the preferred option's cell in the criteria group named `verdict` is filled green.
- **GREEN is no longer reserved for hand annotations in a matrix.** That reservation still holds everywhere else in `tools/diagram/`; if a matrix ever needs to distinguish generated green from annotated green, the annotation colour is the one that has to move.
- **BLUE** still marks text changed since the last reviewed snapshot (the diagram kit's `mark_deltas`).

The three layout checks (overflow, box collision, text overlap) run on every render.

## CI

Two workflow steps fire on every push: Matrix selftest and Matrix audit. A broken matrix in a living design doc fails the build on GitHub's infrastructure, not inside a session.
