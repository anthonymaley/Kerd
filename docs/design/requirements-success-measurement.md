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
**approval fingerprint** at link time, stored on the *source* — and the recipe
is **category-aware** (2026-09-01 ruling below): a requirement target keeps the
existing statement-only fingerprint byte-for-byte, while an `MSC` target uses
the full four-field fingerprint, because a statement-only stamp would let
Measure, Baseline or Target change without ever making the source link suspect.
Verified at
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

Five states before acceptance, then **two decisions yielding three outcomes** —
`docs/design/requirements-success-measurement/condition-lifecycle.html`. It
spans five of the ladder's seven rungs (`frame` and `viability` sit before it),
and **the design gate is the producer's key *at* the design rung — a transition,
not a rung of its own.**

| Where | State | What makes it true |
|---|---|---|
| scope | `UNDECLARED` | the requirement exists; nothing says how we will know |
| design | `DECLARED` | statement · measure · baseline · target, register state `proposed` |
| design gate *(a key, not a rung)* | `KEYED` | the producer approves; the versioned **MSC approval fingerprint** over the condition's four owned fields — **owed, not present** (see `## The approval fingerprint`) |
| work handoff | `CARRIED` | the spec names it on every step whose work affects it |
| loop | `TRACKED` | the thing the build is aimed at |
| acceptance | *two decisions* | **is a reading linked? then: does it satisfy the target?** — three outcomes below |

**`KEYED` freezes the predeclared target; the `Observed result` holds the later
reading; `PROVEN` records that the comparison satisfied the target.**
That separation is the lifecycle's whole point, and it is why the promise and
the proof live on different objects.

**Acceptance is two decisions, not one — and the second is the capability's
entire purpose.**

```
is an Observed result linked?
├─ no  → NOT ASSESSABLE
└─ yes → does the result satisfy the target frozen at KEYED?
          ├─ yes → PROVEN
          └─ no  → NOT MET
```

**A linked reading proves only that the condition was ASSESSABLE. It never
proves the target was met** — a linked result can perfectly well show failure.
Collapsing these two questions into one was a real defect in an earlier draft of
this design, caught at the review on 2026-08-31, and it would have shipped a
capability that could confirm somebody recorded a number while being structurally
unable to report that the number was bad.

**`NOT MET` is a real, reportable outcome, not a process failure.** Measurement
must be able to demonstrate an *unmet expectation*; a design in which the only
outcomes are "proven" and "couldn't tell" is a design that cannot say no.

The four invariants this rests on:

1. **`KEYED` freezes the target** — it cannot move later to meet the reading.
2. **The `Observed result` supplies the reading** — separate object, so the
   proof cannot overwrite the promise.
3. **The comparison decides `PROVEN` versus `NOT MET`.**
4. **The absence of a reading yields `NOT ASSESSABLE`** — never a passed row,
   and never grounds for authoring a target after the build (the `gate-visuals`
   precedent, 2026-08-30).

Ordering matters and is not cosmetic: `PROVEN` is *defined by* a satisfied
comparison, so neither `NOT ASSESSABLE` nor `NOT MET` can branch out of it. That is the precedent set at `gate-visuals`' acceptance gate on
2026-08-30, where an absent measurement declaration was closed as an explicit
producer exception rather than invented retroactively. This design is the
upstream countermeasure to that exception.

## The approval fingerprint — ruled 2026-09-01

**The defect this answers, found while converting this design into its work
specification.** The lifecycle above claimed `KEYED` freezes the target, and the
sealed views said an `Approved` hash over the condition's words is what makes
that true. It would not have been. Verified in three places on 2026-09-01:
`tools/gates/kit.py:1191` — `req_statement_hash(statement)` hashes **the
stripped statement alone**; `docs/requirements/catalog.md:178` — `final`
requires "an `Approved` hash matching the statement"; and
`tools/reqview/fingerprint.py`'s docstring, which names `req_statement_hash` as
a separate recipe for the register's Approved hash and link stamps. On that
recipe an `MSC`'s Measure, Baseline and Target sit **outside** the hash: all
three could be edited after the producer's key with nothing diverging. The
freeze was hollow, and both the drawing and this document asserted it.

**The producer's ruling.** One versioned approval-fingerprint mechanism with
artifact-specific canonical payloads — `approval_fingerprint(category, fields)`:

- **Existing requirements keep the legacy payload** — normalized Statement only.
  Their hashes stay **byte-for-byte unchanged**; no approved record is re-keyed.
- **`MSC` v1 uses a canonical payload of exactly four fields** — Statement ·
  Measure · Baseline · Target. Changing any of the four invalidates `Approved`.
- **Field names, order, separators, normalization and version are fixed
  centrally**, so an alternate implementation cannot invent a different byte
  stream. (Rule 9 already has two implementations tested against each other by
  nothing — this mechanism must not repeat that.)
- **`Method` and observed evidence stay outside the payload**, because they
  belong to separate objects. That is the four-object model holding.
- **Link stamps targeting an `MSC` use the same full `MSC` fingerprint**, never
  `req_statement_hash(Statement)` — otherwise Measure, Baseline and Target could
  change without making the source link suspect. Links targeting a requirement
  keep their current hash, the requirement payload being statement-only.

**Two limits, stated so they are not read as more than they are.** This
generalises the existing recipe into one category-aware implementation while
preserving every existing requirement hash — it is **owed work, not present
machinery**, and every surface here labels it so. And it does **not** make
protection bidirectional: a richer target fingerprint still only flags the
source when the target moves. **Reciprocal stamping remains separately owed.**

## The assurance boundary

`docs/design/requirements-success-measurement/assurance-boundary.html` names,
for every rung, what assures the condition and by what — machine-checked
(something on disk refuses), producer-agreed (a human key, nothing outside the
model enforcing it), or no enforcement at all.

**Thirteen assurance questions, counted by tense — because the design-gate
question is dual-marked, and counting both markers as two lines would make
proposed assurance read as present assurance.**

- **Today:** five machine-checked, two producer-agreed, six unenforced —
  **eight of thirteen rest on agreement or on nothing.**
- **Once the versioned MSC fingerprint is built:** six machine-checked, two
  producer-agreed, five unenforced — **seven of thirteen will.**

The one line that moves between those two readings is the design gate's *has the
keyed target drifted since approval* — machine-checkable once the fingerprint
exists, unenforced until then. It is marked both ways in the drawing for exactly
that reason.

**The comparison itself is among the unenforced.** Whether the observed reading
actually satisfies the target frozen at the design gate is checked by nothing in
this slice — it was added to the assurance view on 2026-08-31, when the
two-decision model exposed it as an assurance question the drawing had been
silently omitting.

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
  evidence artifact. It is a fourth object either way; the home is open —
  settled: see the ruling of 2026-09-01 below.
- **Whether `MSC` is the right code**, pending the category vocabulary review
  — settled: see the ruling of 2026-09-01 below.
- **Any enforcement.** Eight of thirteen assurance questions rest on agreement
  or nothing today — seven of thirteen once the MSC fingerprint is built — by
  design, at `mvp`, including the comparison of reading against target, which is
  the one a machine could most plausibly do once `MSC` exists in the register —
  that comparison alone is settled: see the ruling of 2026-09-01 below; the bullet's
  other assurance gaps remain open.
- **The approval fingerprint's BUILD.** Its shape is settled (above, 2026-09-01)
  and none of it exists yet. Until it is built, `KEYED` does not freeze anything
  a machine would notice.
- **Reciprocal link stamping**, owed so the suspect-link check becomes
  symmetric — settled: see the ruling of 2026-09-01 below.

## Rulings after the GO

The design above is what was agreed at the GO of 2026-08-31. Each line below is
a producer ruling taken after it, settling one of the things the GO recorded as
open. The GO record itself is dated and is never edited.

- **RULED 2026-09-01 — the category code:** the code is `MSC`, reader-facing name
  **Measurable Success Condition**, disposition `applies`. On the naming
  question the producer's words: *"'Acceptance criterion' has broader currency,
  but it collides with Kerd's acceptance rung and can include non-measurable
  conditions. 'Measurable Success Condition' names this artifact's exact
  obligation and keeps the three objects distinct."* The disposition row he
  keyed, verbatim, for `docs/requirements/categories.md`:

  > \| MSC \| Measurable Success Condition \| applies \| Kerd needs a first-class
  > artifact for the predeclared threshold against which an observed result is
  > judged. It is neither a requirement category such as NFR nor a check or
  > method such as TST: the requirement states what must hold, MSC states the
  > measure, baseline and target that count as met, and TST states how the
  > reading is taken. Its distinct field obligations require a distinct filing
  > key. \|

  **A consequence he attached, binding on the row's execution:** `categories.md`
  today frames itself as *"the twenty categories this project owes requirements
  in."* `MSC` makes twenty-one filing codes and introduces a **non-requirement
  artifact**. The framing and every count must be updated honestly — *"it must
  not quietly describe MSC as another requirement category."*

- **RULED 2026-09-01 — the Observed result's home:** it lives in the **immutable
  acceptance record**, not as a register block. The producer's reason:
  *"A reading is an event: changing it tomorrow would falsify the record. It
  belongs with the dated acceptance evidence and producer key, while the MSC
  remains the living predeclared threshold."* **No `OBS` code is added** —
  observed results do not live in the register.

  **The observed-result entry must carry enough identity to bind the
  comparison**, his list: the `MSC` ID · the frozen `MSC` fingerprint used for
  the decision · the observed value and unit · the `TST`/method reference ·
  when the reading was taken · the evidence source or location · the comparison
  outcome, `PROVEN` or `NOT MET`.

  **The instruction he attached, and it is a refusal of the cheap path:** *"Do
  not force `evidenced-by` through today's ID-only link grammar or pretend the
  existing suspect-link stamp supports a file reference."* The work
  specification is therefore **handed back to design** for four things: define
  the canonical acceptance-record shape for observed results · define how an
  `MSC` references that immutable record · decide whether the reference needs a
  content digest and what canonical bytes it covers · preserve
  `NOT ASSESSABLE` when no result entry exists.

  **And a consequence for `categories.md` beyond the Step 1 ruling:** the file
  must stop treating every filing code as a requirement category. The framing
  splits in two — **twenty shipped requirement categories**, and **register
  artifact extensions, currently `MSC`**. `MSC` stays `applies` under the
  extension section.

- **RULED 2026-09-01 — reciprocal stamping:** **build it now, scoped narrowly to the
  new Requirement <-> `MSC` relationship.** The producer's reason, and it is
  why this is not incidental hardening: *"The pilot's purpose is alignment
  between the requirement and its measurable condition. If the requirement can
  change during ordinary refinement while the MSC silently measures the old
  wording, the smallest proof does not establish that alignment."* It is *"the
  integrity mechanism that lets the pilot survive requirement refinement
  between declaration and acceptance."*

  **Required behaviour, his list:** Requirement `--measured-by-->` `MSC` stores
  the `MSC`'s full four-field fingerprint · `MSC` `--measures-->` Requirement
  stores the requirement's legacy statement fingerprint · the audit **requires
  both directions for this role pair** · a missing reciprocal edge or a stale
  stamp produces a **finding**, matching the existing suspect-link severity —
  *"Do not inflate it into a refusal in this slice."*

  **The scope limit he set:** *"Existing link-role pairs are not retrofitted
  wholesale; broader reciprocal enforcement remains separate work unless the
  composer proves the implementation can be safely generalized without
  expanding the slice."*

  **An interaction the composer must absorb, surfaced at the gate rather than
  assumed:** today a role and its reverse are ONE stored edge with two reading
  directions — `catalog.md`'s grammar section, on the StrictDoc precedent where
  *"its `REVERSE_ROLE` gives both reading directions from one declaration."*
  This ruling requires **two stored edges** for this pair, each carrying a
  different fingerprint payload. That is a departure from the incumbent
  convention, not an application of it, and the audit clause ("requires both
  directions") is what makes it explicit.

  Handed back to the composer alongside the Step 2 amendment.

- **RULED 2026-09-01 — the comparison:** it stays **producer-performed in this
  slice**. The acceptance-record parser *"should enforce structure, not invent
  semantics"* — his list: confirm the observed-result entry exists when an
  assessable outcome is claimed · confirm it names the `MSC` and carries the
  **exact frozen `MSC` fingerprint** · confirm value and unit are present ·
  confirm the outcome is one of `PROVEN` or `NOT MET` · preserve
  `NOT ASSESSABLE` when no valid reading is linked · record the producer's key
  as the authority for whether the reading satisfies the target.

  **The limit, and its reason:** *"The machine must not recompute PROVEN versus
  NOT MET until Target has a typed comparison grammar — operator, value type,
  unit normalization, and rules for nonnumeric conditions. Free-text targets
  cannot support a trustworthy comparator."*

  **Return condition, his words:**

  > Revisit machine comparison when the `MSC` target grammar is explicitly typed
  > and at least one real condition requires a repeatable comparison that the
  > acceptance producer should not perform by judgment alone.

  **What this buys, stated so the mvp posture is not read as neglect:** the
  machine proves the comparison is bound to the right **frozen** target and that
  the evidence record is **complete**; the producer judges the **result**.

  **And an instruction to the composer, arising from the Step 3 ruling rather
  than from this one:** the hand-back must revisit the assurance view.
  Reciprocal Requirement <-> `MSC` checking *"is new machine assurance and
  cannot be omitted merely because it does not change the comparison ruling. If
  added to the view, re-derive its counts rather than editing the totals by
  hand."*
