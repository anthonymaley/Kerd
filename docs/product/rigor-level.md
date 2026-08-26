---
route: new
stage: ready-to-release
---

# Rigor level — silence stops passing DONE

## Value

Born at the 2026-08-05 boundary (Tony's opener: spikes, MVPs and
production releases need different measurement levels, and an unasked
level means an insecure app passes DONE by silence). The gap, measured
against the DONE rule: DONE is assembled from upstream declarations —
nothing may be in DONE that nothing declared — so an undeclared rigor
class fails nothing. It is not waived, not failed, just never asked.
Today zero of the three product docs on the ladder declare any
measurement level; security, performance and data integrity have never
been asked once, and nothing went red.

Value, in units:

- **The level question cannot be skipped** — today: no scope declares a
  rigor level and nothing refuses; target: a `## Scope` section without a
  declared, legal rigor level is a named refusal, uniformly across the
  board *(amended at the design rung, 2026-08-05, and again at the goal
  gate, 2026-08-06: mechanically the check lands on two surfaces — the
  repo-wide audit, AU6, at every push, which is the surface that
  delivers "uniformly" — and the design gate's input row at climb time;
  the new-work-only carve-out died with the no-retrofit clause below;
  **2026-08-25: that input row moved with its section — the check now
  rides the SCOPE gate, `## Release slice` having been renamed `## Scope`
  and lifted one rung**)*.
- **Every rigor class in exactly one state** (slice 2) —
  measured-with-target · waived-by-name · n/a-with-reason; a class in
  no state is a named refusal. Silence becomes structurally impossible:
  an insecure app can still ship, but only past a waiver that says so
  by name.

Named honestly: **slice 1 does not yet make class-silence impossible** —
it makes *level*-silence impossible and lays the declaration substrate.
An unasked security check still fails nothing until slice 2's
disposition table exists. Slice 1's own win is that the question "how
rigorous is this?" is asked by construction, answered in data, and
refused when absent.

Cheapness preserved (rigor rises, ceremony low): a spike's declaration
costs one line — its classes pre-fill to waived-by-name from the
catalog, the producer touches nothing.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Hollow waiving: waived-by-name is the cheapest state, so a model or rushed human waives everything — the table goes green and the level means nothing (an "MVP" that is a spike in substance) | yes | the forcing function's value inverted — a declared level certifies rigor that was never applied; worse than today's silence because it looks checked | medium — the same pressure that produced hollow-stamping's row, and waiving IS the designed cheap path for spikes, so the habit is licensed | analysis 2026-08-05: the state machinery cannot distinguish a considered waiver from a reflex one; what is checkable — a waiver names its reason and review trigger (the accepted-state pattern), and the catalog can declare per-level floors: classes a level cannot waive | countermeasure - permanent | waived-by-name reuses the ledger's accepted discipline verbatim (named reason + review trigger, both non-empty, machine-checked); the catalog declares per-level floors — a disposition below the floor for its level is a refusal (production-v1 cannot waive security), so hollow waiving at level is caught structurally; the level choice itself stays a human key | |
| Catalog is thin or wrong: expansions derive from the catalog, so a class the catalog never names is never asked anywhere — the silence gap reappears one level up | no | class coverage capped by catalog quality; the gap moves rather than closes | medium — no catalog exists yet; its first content is guesswork refined by use | analysis 2026-08-05: the catalog is a living doc, so each discovered miss is one amendment that upgrades every future slice at once — centralised, versus today where the miss recurs silently per slice | accepted | | the first shipped slice whose incident traces to a class the catalog never named re-argues this row |
| Ceremony creep: the disposition table grows until declaring a level costs more than the judgment it forces — spikes route around the ladder | no | rigor-rises-ceremony-low violated; adoption dies at the cheap end | low — the pre-fill design exists precisely against this | analysis 2026-08-05: spike cost is bounded by design at one declared line + zero deviations | accepted | | a spike whose rigor declaration takes more than one line to satisfy re-argues this row |

## Scope

Rigor level: mvp

Smallest valuable slice — **slice 1: the declared level + the refusal**
(proposed; the fork below is the producer's call): a `## Scope` section
carries a machine-readable rigor level from a declared legal set
(starter set: `spike` · `mvp` · `production-v1`; `RIGOR_LEVELS` in
`kit.py` is what the checker tests against — the refusal messages,
fixtures, and the gates standard repeat the set as literals, so an
amendment edits them all in one commit; *goal-gate amendment
2026-08-06: the earlier "lives in one declared place" claim was
false in the shipped code and nothing machine-checks the literals
against the constant*); the scope gate — where the `## Scope`
section is an input — refuses work whose scope lacks a legal
level, uniformly; the audit demands and validates the declaration in
every work record that carries a `## Scope`; the three existing
product docs each receive one honest retrofit line *(amended at the
design rung, 2026-08-05, Tony's key: the original no-retrofit clause
borrowed grounding's hollow-declaration precedent, but a level is one
falsifiable value, not a reconstructed reading list — and the progress
board re-derives the route for every slug on every render, so an
exemption would either live forever in the checker or falsify three
done journeys on the board)*. Win: **the rigor question is asked by
construction, and its answer is data** — the substrate slices 2 and 3
stand on.

The fork, named: slice 1 could instead ship a minimal catalog and
disposition table for one level, making class-silence impossible
immediately for that level. Cost: the catalog's shape (living doc,
floors, per-class defaults) gets designed under slice pressure instead
of on its own rung — and grounding's precedent (declarations first,
instrument second) argues thin. Producer decides.

Deliberately excluded, named:

- **The rigor catalog + pre-filled disposition table** — slice 2:
  living doc per level, on disk; expansion derived from the artifact,
  never model memory; each class forced into exactly one state;
  per-level floors; producer key on deviations only.
- **Measured classes become CI checks** — slice 3: a
  measured-with-target class lands as a red light with the fix named.
- **Any proof the measurement itself was competent** — never: the
  check's claim is that the question was asked and answered in data,
  not that the answer is good — the same declared-limit class as
  retrieval-not-comprehension.

## Grounding

- tools/gates/README.md — the gate table and audit this refusal lands in
- docs/product/grounding-was-read.md — the declarations-first slice precedent and the opt-in-versus-retrofit reasoning this reuses
- docs/design/risk-ledger.md — the state vocabulary the disposition states mirror (a named waiver = accepted + review trigger)
- CONTEXT.md — standing decisions bind: derived-from-disk, refusal-from-outside-the-model, rigor-rises-ceremony-low
