# Requirements success measurement — the design

Every requirement declares how we will know it was met, before design starts.
This document and the three sealed views under
`docs/design/requirements-success-measurement/` are one deliverable in two
renderings: the drawings are how the design was agreed, this is how it is kept.

**Rigor level: `mvp`** (declared by the producer, 2026-08-31, in the work
record's `## Scope`). **Nothing here is built by this slice.**

## The question this answers, and how long it stood open

`docs/requirements/catalog.md` records, in `## Fields`:

> Deferred, each with a return condition — … Acceptance Criteria and
> Verification Method (the forward trace, slice 2)

and, four sections later, in `## Link roles`:

| `satisfied-by` | `satisfies` | requirement → the contract piece that builds it *(slice 2)* |
| `verified-by` | `verifies` | requirement → the test that proves it *(slice 2)* |

**Those are two incompatible answers to one question, under one return
condition, in one file** — deferred *fields on the requirement block* versus a
typed *edge to a separate object*. Neither was ever built, which is why the
contradiction went unnoticed. The 2026-08-14 requirements research had already
ruled that a requirement and its acceptance criterion are two artifacts —
*"do not build one schema trying to be both"* — and closed on the unanswered
question *"what carries the acceptance criterion?"*.

**The producer's ruling, 2026-08-31: the edge wins.** A requirement and its
measurable success condition stay separate, joined by typed links.

## The four objects

| Object | Owns | Status |
|---|---|---|
| **Requirement** `<CODE>-nnn` | ID · Category · State · Statement · Source · Approved · Tags | exists; **gains nothing** |
| **Success condition** `MSC-nnn` | Statement · **Measure** · **Baseline** · **Target** | new category |
| **Test / method** `TST-nnn` | **Method** — how the reading is taken | exists |
| **Observed result** | the reading actually taken | new; home open |

**The requirement block gains no field.** That is the constraint most likely to
erode under later convenience, so it is stated in the drawing as well as here.

**`Method` is not on the condition.** A success condition answers *what
observable result counts as success*; a test answers *how will we test this*.
Putting the method on the condition would re-merge the two artifacts one field
at a time.

**Evidence is not a field on the condition.** It is a linked `Observed result`.
A field that mutates from empty to populated inside an approved condition would
let later evidence overwrite what was promised — the predeclared target and its
later proof must stay separable, which is the whole reason there are four
objects and not three. **The producer's own first wording said "three
artifacts" while his arrows drew four; the arrows were the intended model
(confirmed 2026-08-31).** The `Observed result` may turn out to be an external
evidence artifact rather than a register category — that home is deliberately
left open — but it remains a fourth object either way.

## The edges

| Role | Reverse | Source → target | Status |
|---|---|---|---|
| `measured-by` | `measures` | Requirement → Success condition | **new** |
| `verified-by` | `verifies` | Success condition → Test / method | **re-sourced** |
| `evidenced-by` | `evidences` | Success condition → Observed result | **new** |

**`verified-by` is re-sourced, not renamed.** The catalog declares it today as
*requirement → the test that proves it*; under this design its source moves to
the success condition. That is a live declared role changing meaning, which the
read-only-alias rule does not cover — aliases are for retired *names*, and this
name is not retired. It is called out in the drawing rather than allowed to
change quietly.

**Each edge carries the suspect-link stamp, and it protects ONE direction
only.** The stamp is `- measured-by → MSC-007 (sha256:…)`: the *target's*
statement hash at link time, stored on the *source*. Verified at
`tools/gates/kit.py:1445`, which compares the stored stamp against the target's
current hash. So:

- **edit the target** → every link pointing at it diverges → the **source** is
  flagged for re-look ✓
- **edit the source** → nothing diverges, and the target's dependents learn
  nothing ✗

**For this design the unprotected direction is the dangerous one.** If
`FUN-010`'s statement changes, the `MSC` measuring it may now be measuring words
that no longer exist — and on today's mechanism nothing flags that. **Reciprocal
stamped links are therefore owed**, and are recorded here as owed rather than
assumed. An earlier draft of this document and of the anatomy view claimed
symmetry ("edit either end and the other is flagged"); that claim was false and
is corrected, having been challenged at the design review on 2026-08-31.

The one direction that does work is not new machinery — the catalog already
specifies it for links generally. What was missing was anything on the far end
of the arrow.

**n:m falls out of the edge and could not fall out of a field.** One condition
can serve several requirements; one requirement can need several conditions. A
field forces 1:1 permanently.

## Why `MSC` and not `TST`

`TST`'s decision question in the catalog is *"whoever decides what will count as
proof"*, which reads close enough to be tempting, and reusing it would inherit
the register's whole machinery — five states, the `Approved` hash, AU7/AU8
refusal, suspect links — for free.

**Rejected by the producer, 2026-08-31, and the reason is worth keeping:** `TST`
answers *how will we test this*; a measurable success condition answers *what
observable result counts as success*. They are related and distinct. Buying the
machinery by overloading the code would purchase a semantic contradiction — the
same defect class this repo has paid for repeatedly, where one name carries two
meanings and a reader cannot tell which is meant.

So: a new code, `MSC` (Measurable Success Condition), **unless the category
vocabulary review finds a better existing term.** Introducing it owes a
`categories.md` disposition and schema work. **This session designs that; it
does not build it.**

## The lifecycle

Five states before acceptance, then a **decision** with two outcomes —
`docs/design/requirements-success-measurement/condition-lifecycle.html`. It
spans five of the ladder's seven rungs (`frame` and `viability` sit before it),
and **the design gate is the producer's key *at* the design rung — a transition,
not a rung of its own.**

| Where | State | What makes it true |
|---|---|---|
| scope | `UNDECLARED` | the requirement exists; nothing says how we will know |
| design | `DECLARED` | statement · measure · baseline · target, register state `proposed` |
| design gate *(a key, not a rung)* | `KEYED` | the producer approves; an `Approved` hash over its words |
| work handoff | `CARRIED` | the spec names it on every step whose work affects it |
| loop | `TRACKED` | the thing the build is aimed at |
| acceptance | *decision* | **is an `Observed result` linked?** — evaluated, with two outcomes below |

**`KEYED` freezes the predeclared target; `PROVEN` holds the later reading.**
That separation is the lifecycle's whole point and it is why the two live on
different objects.

**Acceptance is a decision, not a state that fails afterwards.** It asks one
question — *is an `Observed result` linked?* — and yields one of two outcomes:

- **yes → `PROVEN`.** The reading, not an assertion.
- **no → `NOT ASSESSABLE`.** Never a passed row, and never a target authored
  after the build.

Ordering matters here and is not cosmetic: `PROVEN` is *defined by* a linked
observed result, so `NOT ASSESSABLE` cannot branch out of it. The fork sits
before both. That is the precedent set at `gate-visuals`' acceptance gate on
2026-08-30, where an absent measurement declaration was closed as an explicit
producer exception rather than invented retroactively. This design is the
upstream countermeasure to that exception.

## The assurance boundary

`docs/design/requirements-success-measurement/assurance-boundary.html` names,
for every rung, what assures the condition and by what — machine-checked
(something on disk refuses), producer-agreed (a human key, nothing outside the
model enforcing it), or no enforcement at all.

**Of thirteen lines: six machine-checked, two producer-agreed, five with no
enforcement. Seven of the thirteen rest on agreement or on nothing.**

**This slice adds no automated per-rigor floor.** The control is the producer
declaring the rigor level and agreeing a proportionate success condition at
scope. It binds by agreement at one gate. **Drive does not structurally
guarantee compliance** — the same sentence the work record's risk ledger
carries, on the producer's instruction, so the limit is recorded in both the
design and the risk it answers.

The drawing exists precisely so this limit cannot later be mistaken for
machinery. Its countermeasure is `countermeasure - temporary`, and its return
condition is `rigor-level` slice 2 defining enforceable per-level floors.

## Proposed supersession — recorded, deliberately NOT executed

The catalog's deferred merged-fields row is superseded by this design. **The
catalog is not edited in this session.** The edit belongs to the later schema
implementation, and when it lands it takes this form — original text preserved
verbatim inside the strike:

> ~~Acceptance Criteria and Verification Method (the forward trace, slice 2)~~
> **Superseded** by the separate MSC artifact and typed links: the success
> condition owns statement, measure, baseline, and target; TST owns the
> verification method; observed results are linked evidence. See
> `docs/design/requirements-success-measurement.md`.

**And a standing rule the producer attached to it, 2026-08-31, which reaches
past this item:** *"If a checker mistakes struck text for a live claim, teach
the checker to distinguish retired text; do not rewrite history to satisfy a raw
text scan."* This answers the 2026-08-30 gotcha — *preserving a struck claim
verbatim trips any checker that hunts the claim* — in the opposite direction
from the one that gotcha implied. **The record is authoritative and the checker
adapts to it, never the reverse.**

## What this design does not settle

- **Where the `Observed result` lives** — a register category or an external
  evidence artifact. It is a fourth object either way; the home is open.
- **Whether `MSC` is the right code**, pending the category vocabulary review.
- **Any enforcement.** Seven of thirteen assurance lines rest on agreement or
  nothing, by design, at `mvp`.
