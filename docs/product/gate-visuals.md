---
route: new
stage: framed
---

# A visual at every gate, approved and locked

## Value

**Design is agreed in diagrams, and today a diagram costs a Python file.**
Measured 2026-08-22: 27 hand-written generators, 5,961 lines, one per drawing.
That is why *"design is agreed in diagrams, not prose"* keeps losing to prose —
the paragraph is free and the picture is a program.

The diagram-toolkit spike (`docs/design/diagram-toolkit-spike-findings.md`)
closed that: a drawing now costs a prompt and a lint pass.

**This item is what that unlocks.** Tony, 2026-08-22: *"EACH gate needs a
corresponding visual(s) that users can approve and lock in"* and *"we MUST have
visuals for the work that is in the design, so DB design needed, then we need to
show it, architecture needed, diagram must exist etc then we can compare design
with built."*

**Winning:** every gate has a picture the producer approved, the design is
declared truth rather than description, and a build that drifts from its own
design is detectable rather than discovered later.

## The prescription — Kerd is opinionated about the funnel

His constraint, 2026-08-22: *"kerd needs to be super onionated about what visuals
it shows for the funnel."* A menu means every session picks differently and the
funnel never looks like one thing twice.

**Opinionated means the vocabulary is closed, not that the count is one.**
Tony, 2026-08-22: *"gates can have MANY visuals, design and viablity and idea
etc."* A gate draws as many as the work needs — from its own declared set, and
from nowhere else.

| Gate | Its declared set | How many |
|---|---|---|
| **frame** | `it-state` the before picture · `fishbone` root cause · `journey` what a person does and feels · `venn` where two things overlap · `pyramid` what sits above what | as many as the idea needs — a frame with a legacy landscape *and* a root cause owes both |
| **viability** | `quadrant` impact against likelihood · `wardley` build, buy or outsource · `sankey` where the cost goes · `treemap` where the effort goes | one per question being answered. A build-versus-buy call and a cost question are two drawings, not one |
| **slice** | `story-map` release bands and the cut · `pyramid` when the cut is by rank · `treemap` when the cut is by size | usually one, more when the cut is argued on two grounds |
| **design** | `db-schema` · `er` · `architecture` · `deployment` · `sequence` · `state` · `flowchart` · `process` · `nested` · `dependency` · `swimlane` · `layers` · `tree` | **one per aspect the work touches.** The set is derived from the work, never chosen by whoever is drawing |
| **contract** | `dependency` what lands before what · `org-chart` which role and model plays each piece · `swimlane` who owns which handoff | as many as the handoff needs |
| **build** | the progress board | exactly one, and it is **the exception** — see below |
| **goal** | the design set **redrawn from what was built** · `bar` measured against target · `line` the trend · `scatter` the relationship · `timeline` what shipped | one redraw per design drawing, plus whatever the measurement needs |
| **loop** | `loop` where the last step feeds the first · `fishbone` when the loop was entered because something failed · `timeline` release history | as many as the learning needs |

**AS-IS AND TO-BE ARE A PAIR, AND BOTH ARE OWED.** Tony, 2026-08-22:
*"peoblem solving, as is - to be all need visuals."* An earlier version of this
table carried `it-state` — the before picture — and nothing for the after, so
there was nothing to compare it against. That is half a proposal.

The pair is already the house grammar: the A3 shape is *current situation drawn ·
numbered pains · proposal drawn · targets in units*, and a change stated in the
user's terms is *current → new → what changes*.

Three rules govern it:

1. **Where a change is proposed, both states are drawn.** As-is at **frame**;
   to-be at **frame** in outline and at **design** in full.
2. **Both are drawn in the SAME type.** An as-is in `it-state` and a to-be in
   `architecture` cannot be laid side by side — the difference between them
   reads as a difference in notation. Same type, same layout, so the only thing
   that changes between the two pictures is the thing that actually changed.
3. **The delta is named, not left to the eye.** What moved, what died, what is
   new. The colour grammar already carries this: red is cost, blue is changed
   since the producer last reviewed.

**Problem-solving work owes its own pair.** `fishbone` for the causes, plus the
current condition and the target condition in the same type — which is the
sensei route this repo already declares for a problem that survived a few
attempts to fix it. A root cause with no target condition is an explanation, not
a proposal.

**Two rules make this opinionated rather than a menu:**

1. **The set is closed.** A gate draws from its own row and from nowhere else.
   Reaching outside it is a defect, not a judgement call.
2. **`quadrant` at viability keeps its axes.** Its own examples are Impact ×
   Effort; ours are impact against likelihood, **recorded separately and never
   multiplied** — expected value is the wrong maths for a bet taken once — and
   fatal is a band (impact ≥ declared value at any likelihood), not a cell.

**Three traps, excluded by name so nobody reaches for them:** `gantt` at slice
(a release is a grouping, not a time axis — a gantt makes time the definition);
`kanban` anywhere (a state census, which is the board, derived); `radar` at
viability (comparison between options is the evaluation matrix, ours, with 24
criteria and marks this has no equivalent for).

**Outside the funnel, nothing is prescribed.** A project using Kerd draws its own
system however it likes, with the full type set. Kerd is opinionated about its
own process and silent about your product.

**The design rung's gate is unchanged by this** — its two-key GO already says
*every aspect drawn and nothing left to annotate*. What changes is that the
aspect list is derived from what the work touches rather than chosen by whoever
is drawing.

**Outside the funnel, nothing is prescribed.** A project using Kerd draws its own
system however it likes, with the full type set. Kerd is opinionated about its
own process and silent about your product.

## Approve and lock — reusing what already works

A visual becomes declared truth the same way a requirement does: **a fingerprint
over its content**, computed at approval, never typed. Change the drawing and the
approval invalidates, exactly as it does on a requirement today.

This is not new machinery. It is rule 9, `seal`, and invalidation, pointed at
pictures instead of blocks.

## Design against built

```
design gate   draw it · producer approves · fingerprint locks it
build         the thing gets built
goal gate     redraw from what was built · fingerprint that · compare
```

**How checkable each aspect is, stated rather than promised:**

| Aspect | Built side derivable from | Strength |
|---|---|---|
| `db-schema` | migrations / DDL | strong |
| `dependency` | imports | strong |
| `deployment` | manifests / compose files | medium |
| `sequence` | traces, where they exist | weak |
| `architecture` | nothing — it is intent | eyeball only |

**Divergence is rare by design, and its frequency is the measurement.** Tony,
2026-08-22: *"if requirments are correct and visuals are approved then it
shouldnt happen and if it does it should be dealt with by conductor/composer."*
This is the same rule as the promotion beat (2026-08-07, *"really its a process
issue, that should only happen if we get requirements wrong?"*): a well-run item
never trips it, so an item that trips it often has a broken process upstream
rather than a noisy check.

**Who resolves it:** conductor or composer. The producer hears about it only when
neither can answer — the escalation contract already in the register.

## The one exception, kept visible rather than smoothed over

**Build's visual is the progress board, which is derived from disk and therefore
cannot be approved or locked** — nobody authored it, so there is nothing to
fingerprint an agreement to. Every other gate's visual is authored, approved and
fingerprinted. That asymmetry is real. It is named here so nobody later "fixes"
it by making the board approvable, which would mean approving a fact.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| A visual is approved without being read — the rubber-stamp failure, at picture speed | yes | an agreed drawing nobody looked at becomes declared truth, and every later comparison is against a fiction | medium | the register's own answer to false approval is presentational, named as an accepted residue on 2026-08-13 | accepted unknown | none yet — the producer's own ruling is that proper management plus strong pairing mitigates and does not cure | the first time a divergence traces back to an approved visual nobody had read |
| Prescribing one visual per gate makes a gate unpassable for work that genuinely has no such picture | no | a rung blocks on ceremony | medium | design already allows an aspect-driven set rather than a fixed one | countermeasure - permanent | the gate demands a visual **for each aspect the work touches**; work touching no such aspect owes none, the same way `n/a` with a named reason works elsewhere | |
| Redrawing from the built side is only strong for two aspects | no | the comparison is partial and could read as complete | high | measured in the table above | countermeasure - permanent | the strength column ships with the feature, so a weak comparison is labelled weak | |

## Release slice

Rigor level: mvp

**Slice 1 — the design rung only.** One gate, the aspect-driven set, approval and
fingerprint locking. No comparison yet.

**Slice 2** — the goal-gate redraw and comparison, starting with `db-schema` and
`dependency`, the two strong ones.

**Slice 3** — the remaining gates.

## Deliberately not in this item

- **The progress board.** Derived, byte-compared, not approvable — and the spike
  closed it to this toolkit permanently.
- **The evaluation matrix.** Ours already, machine-checked since v0.77.0.
- **Visuals outside the funnel.** A project's own domain drawings are free.
