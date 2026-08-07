# Rigor level — the declared level + the refusal

Living design doc. Owner: the `rigor-level` work item
(`docs/product/rigor-level.md`), release slice 1. Parent:
`docs/design/entry-gates.md` (the gate table and audit this piece
extends). Routed here by `gate.py route` — enters at design on the
frame's own artifacts.

## What it does

Makes a release slice's rigor level a **declared, machine-checkable
value**. Every product doc that carries a `## Release slice` section
must declare its level on one line — `Rigor level: mvp` — from a legal
set; the repo-wide audit gains a sixth rule (AU6) demanding and
validating the line, and the design rung's gate check gains an input
row naming it at climb time. A slice whose level is missing, illegal,
duplicated, or misplaced turns the push red with the fix named.
**The rigor question is asked by construction; its answer is data.**

Slice 1 checks *declaration only* — that the level was asked and
answered. What a level requires (the catalog, the per-class disposition
table) is slice 2; measured classes as CI checks are slice 3.

## The declaration

One line inside the `## Release slice` section of
`docs/product/<slug>.md`:

```
Rigor level: mvp
```

- **Shape:** line starts `Rigor level:` (column 0, case-sensitive);
  the value is the rest of the line, whitespace-stripped. Exactly one
  such line per Release slice section, and none elsewhere in the file.
- **Legal set:** `spike` · `mvp` · `production-v1` — a `RIGOR_LEVELS`
  list in `tools/gates/kit.py`, canonically documented in
  `tools/gates/README.md` (the route/stage precedent: hardcoded in the
  tool, written down in the standard). Amendable by commit; the
  refusal messages and fixtures repeat the set as literals, so an
  amendment edits them together *(goal-gate finding, 2026-08-06)*.
- **In slice 1 the value is data.** Level semantics — what `mvp`
  *requires* — arrive with slice 2's catalog. Declaring is the forcing
  function; expansion is deferred.

## The decision — where the declaration lives

Marks (light tier — options not close, no scored matrix):

| Criterion | line in `## Release slice` | front-matter key | new `## Rigor` section |
|---|---|---|---|
| Matches the keyed frame ("declared in the Release slice definition") (M) | ○ | △ near it, not in it | △ |
| No schema/section invented ahead of its need (M) | ○ | × third key breaks the route/stage both-or-nothing pair | × empty section until slice 2 |
| Trivially parseable | ○ prefix match inside one section | ○ | ○ |
| Slice 2 extension | ○ table gets its own home later | △ | ○ but premature |

**The line wins.** A `## Rigor` section stays reserved as the
disposition table's home when slice 2 frames; nothing is built for it
now.

## The decision — uniform rule, honest retrofit

The frame's original no-retrofit clause died at this rung on evidence,
Tony's key (2026-08-05; the frame carries the amendment):
`progress_kit.board_for` re-derives `gate.py route` for **every** slug
on every render, and route inputs are cumulative — a design-rung input
row the three done docs lack would flip their built rungs to "need" on
the board and churn the stale gate.

| Criterion | exempt list in kit | honest retrofit (one line each) | audit-only, no gate row |
|---|---|---|---|
| Board stays truthful (M) | × three journeys forever "never asked" | ○ | ○ |
| Forcing function has teeth (M) | ○ | ○ | × nothing refuses a new slice |
| No permanent special case | × shrinks-never-grows list, still a list | ○ | ○ |
| Respects the frame as keyed | ○ | △ frame amendment, push-wiring precedent | △ weakens it |

**Honest retrofit wins.** A level is one falsifiable value — it cannot
be hollow the way a reconstructed reading list can (grounding's
precedent covers reading lists, not scalars). The retrofit lands in the
**same commit** as the rule, so no pushed tip ever has the rule without
the lines.

Retrofit values, proposed (producer annotates on the canvas if any is
dishonest): `push-wiring: mvp` · `grounding-was-read: mvp` ·
`progress-html: mvp` · `rigor-level: mvp` — internal tooling, in real
use, no hardening pass claimed.

## AU6 — the level audit rule

Extends `kit.audit` (AU1–AU5 precedent), swept over every
`docs/product/*.md`:

1. Any line starting `Rigor level:` **outside** the `## Release slice`
   section → problem:
   `docs/product/<S>.md — Rigor level line outside Release slice`
2. `## Release slice` section present (via `find_section`) → exactly
   one `Rigor level:` line inside it:
   - none → `docs/product/<S>.md — Release slice missing 'Rigor level: <spike|mvp|production-v1>' line`
   - more than one → `docs/product/<S>.md — duplicate Rigor level lines (want exactly one)`
   - illegal value → `docs/product/<S>.md — illegal rigor level '<v>' (legal: spike, mvp, production-v1)`
3. No `## Release slice` section (stage < sliced, or a spike) →
   vacuous pass for this rule.

Runs wherever audit already runs — `gate.py audit`, CI step two. **CI
gains no step**; the level rides the existing refusal surface.

## The gate row — design rung

`check`/`route` design-rung inputs gain one row, sharing AU6's kit
function (single-parser rule — two call sites, one implementation):

```
need: docs/product/<S>.md — Release slice declares a legal rigor level (Rigor level: spike|mvp|production-v1)
```

The audit is the tip-level backstop (fires on every push); the gate row
names the same fact at climb time, where the author is looking. Both
refusals quote the fix verbatim.

## Testing strategy

Fixture cases extend the selftest (temp-tree pattern, currently 18):

1. **Legal line** — `Rigor level: mvp` inside Release slice → design
   check passes, audit clean.
2. **Missing line** — Release slice without one → AU6 problem verbatim
   + design check refuses with the need row.
3. **Illegal value** — `Rigor level: prod` → named problem quoting the
   value and the legal set.
4. **Duplicate lines** — two legal lines → named problem.
5. **Misplaced line** — `Rigor level: mvp` under `## Value` → named
   problem.
6. **No Release slice section** — framed-only doc → vacuous pass
   (asserts the demand keys off the section, not the doc).

At build, the refusal is demonstrated both ways on the real tree (the
0.70.0 pattern): strip one retrofit line → audit exits 1 naming it;
restore → clean. **Dogfood:** `docs/product/rigor-level.md`'s own
Release slice declares its level in the same commit.

## Named answers — the stage-1 measurements

| Measurement (product doc, Value) | Target | Named answer |
|---|---|---|
| A Release slice without a declared, legal level at a pushed tip | named refusal within one CI run | AU6 inside `gate.py audit` — CI step two — demands exactly one legal line in every Release slice section; fixture 2 asserts the message verbatim; both-ways demo at ship. |
| The three done journeys' board render across the rule landing | unchanged | retrofit lines land in the same commit as the rule; `gate.py route` for push-wiring · grounding-was-read · progress-html shows identical `enters_at` before/after (run at build); the stale harness byte-compares the committed render at the tip. |
| Validation wherever a declaration appears | every malformed shape named | fixtures 3–5 (illegal, duplicate, misplaced), each asserting its verbatim problem line. |

## Build shape

Files the contract will touch: `tools/gates/kit.py` (RIGOR_LEVELS +
one parse-and-judge function + AU6 wiring + design-row wiring) ·
selftest fixtures (+6, 18 → 24) · `tools/gates/README.md` (gate table
design row, audit table AU6 row, a Rigor level section) · four product
docs (one line each) · three version fields (MINOR, tool change).
`.github/workflows/gate.yml` untouched.

## Out of scope, named

- **The rigor catalog + disposition table** — slice 2. The legal-set
  home moves from the kit constant to the catalog when the catalog
  exists (named seam); the reserved `## Rigor` section becomes the
  table's home.
- **Measured classes as CI checks** — slice 3.
- **Folding `route: spike` into the rigor axis** — the frame notes the
  generalization; unframed, untouched here. A spike doc without a
  Release slice section passes AU6 vacuously today.
- **Level semantics** — what a level requires is the catalog's business;
  slice 1 refuses only silence and illegality, never judges fit.
