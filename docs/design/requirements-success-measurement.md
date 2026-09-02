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
| **Observed result** | the reading actually taken · its evidence · the digest of that evidence | new; **an entry in the immutable acceptance record** |

**The requirement block gains no field.** That is the constraint most likely to
erode under later convenience, so it is stated in the drawing as well as here.

**`Method` is not on the condition.** A success condition answers *what
observable result counts as success*; a test answers *how will we test this*.
Putting the method on the condition would re-merge the two artifacts one field
at a time.

**Evidence is not a field on the condition.** It is a separate `Observed
result`, recorded as an entry in the immutable acceptance record. A field that
mutates from empty to populated inside an approved condition would let later
evidence overwrite what was promised — the predeclared target and its later
proof must stay separable, which is the whole reason there are four objects and
not three. **The producer's own first wording said "three artifacts" while his
arrows drew four; the arrows were the intended model (confirmed 2026-08-31).**
Its home was left open at the GO and was **settled on 2026-09-01** — the
immutable acceptance record, never a register block. See
`## The observed-result entry`.

## The edges

| Role | Reverse | Source → target | Status |
|---|---|---|---|
| `measured-by` | `measures` | Requirement → Success condition | **new · two stored edges** |
| `verified-by` | `verifies` | Success condition → Test / method | **re-sourced** |

**There is no third edge, and that is a change from the GO.** An earlier version
of this table carried `evidenced-by` / `evidences`, Success condition → Observed
result. **It is removed** (ruled 2026-09-01, below): the `Observed result` is not
a register block, so there is nothing for an ID-only link role to point at, and
the producer refused both cheap paths — forcing `evidenced-by` through today's
grammar, and pretending the suspect-link stamp supports a file reference. The
binding runs the other way and is not stored link grammar at all; see
`## The observed-result entry`. **Nothing in `docs/requirements/catalog.md`
changes as a result** — `evidenced-by` was never declared there (only
`verified-by` is, at `:204`), and no link role appears anywhere under `tools/`.

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

**`measured-by` / `measures` is stored as TWO edges, and that is a departure
from the incumbent convention rather than an application of it.** The catalog's
grammar section, on the StrictDoc precedent, makes a role and its reverse ONE
stored edge with two reading directions — *"its `REVERSE_ROLE` gives both
reading directions from one declaration."* This pair cannot work that way,
because the two directions carry **different fingerprint payloads**:
Requirement `--measured-by-->` `MSC` stores the `MSC`'s full four-field
fingerprint, while `MSC` `--measures-->` Requirement stores the requirement's
legacy statement-only fingerprint. The audit **requires both directions for this
role pair**; a missing reciprocal edge or a stale stamp is a **finding**, at the
existing suspect-link severity, deliberately not inflated into a refusal in this
slice. Existing role pairs are **not** retrofitted — broader reciprocal
enforcement stays separate work.

**n:m falls out of the edge and could not fall out of a field.** One condition
can serve several requirements; one requirement can need several conditions. A
field forces 1:1 permanently.

## The observed-result entry

**The binding runs from the immutable record TO the condition, never the
reverse** — ruled 2026-09-01. The producer's reason: *"The living MSC must not
be edited after acceptance merely to point at a dated record."* A reading is an
event; the condition is a living predeclared threshold. Making the condition
reach forward into history would mutate an approved artifact to record something
that happened after its key.

So the `MSC` gains **no outbound file reference and no post-key mutation**.
Discovery is **derived**: scan the immutable acceptance records for entries
naming the `MSC` ID. `tools/gates/kit.py:892` already globs and parses those
records, so this needs no new grammar — which is precisely why the outbound edge
was unnecessary as well as unbuildable.

The entry carries **seven fields and nine required facts** — the `Condition`
line carries two (the ID and the frozen fingerprint) and `Observed` carries two
(the value and its unit):

```
Condition:       MSC-007 (fingerprint:<64 lowercase hex>)
Observed:        <value> <unit>
Method:          TST-014
Taken:           YYYY-MM-DD
Evidence:        <repo-relative path>
Evidence-SHA256: <64 lowercase hex>
Outcome:         PROVEN | NOT MET
```

**An entry QUALIFIES only when every one of these EIGHT holds**, and the parser
checks all of them. **Nine required facts, eight conditions** — the value and its
unit are two facts checked by one condition:

1. `Condition` names an `MSC` ID that exists in the register.
2. Its stored fingerprint **matches the `MSC` version used for the decision** —
   the exact frozen four-field fingerprint, not `req_statement_hash`.
3. `Evidence` resolves to a repo-relative file that exists.
4. `Evidence-SHA256` **recomputes** over that file's raw bytes and matches.
5. `Observed` carries both a value and a unit.
6. `Method` names a `TST`.
7. `Taken` is a valid date in `YYYY-MM-DD` form.
8. `Outcome` is exactly `PROVEN` or `NOT MET`.

**Condition 7 was missing from the first draft of this section and of the anatomy
view**, which listed `Taken` as a required field and then wrote a seven-condition
contract that never validated it — caught by the producer at the combined eye on
2026-09-01. A required fact the parser does not check is not a requirement; it is
a comment. The prose and the parser contract must state the same number.

**A non-qualifying entry yields `NOT ASSESSABLE` — never `PROVEN`, never
`NOT MET`.** That is the second derivation path for `NOT ASSESSABLE`; the first
is no entry at all. A missing evidence file and a digest mismatch both land
here, which is the point: an unverifiable reading is not a bad reading, it is
not a reading.

**Two digests, two jobs, and they must not be merged.** The **approval
fingerprint** is a canonical payload over declared *fields* and protects
**target identity** — what was promised. **`Evidence-SHA256`** is a plain
SHA-256 over an artifact's **raw bytes** and protects **evidence identity** —
what was actually judged. Both are required for an assessable comparison. A
location answers *where* the evidence was found; only the digest answers *what*
was judged, and without it a mutable file, URL or CI artifact could be replaced
while the record went on reporting `PROVEN`.

**External evidence must be captured as a stable local snapshot before
acceptance.** A bare URL or a mutable CI-run location is **insufficient in this
slice** — there are no stable bytes to hash, and a digest that cannot be
recomputed is decoration. Supporting remote or provider-native immutable
evidence is **deferred**, and its home is the existing out-of-repo-artifacts
problem, not this design.

**The phrase "the `MSC` is evidenced by the result" may stay as explanatory
prose.** It describes a **derived** relationship, not stored link grammar, and
the design says so rather than letting a convenient sentence re-introduce the
edge that was removed.

## Register artifact extensions — `categories.md` stops being a list of categories

`docs/requirements/catalog.md`'s companion, `docs/requirements/categories.md`,
frames itself today as *"the twenty categories this project owes requirements
in."* `MSC` makes twenty-one filing codes and introduces a **non-requirement
artifact**, so that framing and every count in the file become false the moment
the disposition lands.

**The framing splits in two** (ruled 2026-09-01): **twenty shipped requirement
categories**, and **register artifact extensions, currently `MSC`**. `MSC` sits
`applies` under the extension heading. The producer's constraint on the
execution: *"it must not quietly describe MSC as another requirement category."*

**The file is not edited by this design.** Like the catalog supersession below,
the edit belongs to the later schema implementation.

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

So: a new code, `MSC` (Measurable Success Condition). **The category
vocabulary review was run as the Step 1 gate on 2026-09-01 and closed the
question:** all twenty deciding questions in `catalog.md` were applied to an
`MSC` statement and none returns yes. The decisive argument turned out to be
coherence rather than semantics — the obligation *"Measure, Baseline or Target
on any non-`MSC` block is a refusal"* is written **in terms of the category**,
so folding conditions into `TST` would make that refusal unwritable without a
sub-type discriminator inside `TST`. Introducing it owes a `categories.md`
disposition and schema work. **This design does not build either.**

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
| acceptance | *two decisions* | **is a qualifying reading recorded? then: does it satisfy the target?** — three outcomes below |

**`KEYED` freezes the predeclared target; the `Observed result` holds the later
reading; `PROVEN` records that the comparison satisfied the target.**
That separation is the lifecycle's whole point, and it is why the promise and
the proof live on different objects.

**Acceptance is two decisions, not one — and the second is the capability's
entire purpose.**

```
is a QUALIFYING observed-result entry recorded?
  (names the MSC · carries its exact frozen fingerprint · evidence file
   resolves · Evidence-SHA256 recomputes · value, unit, method, legal outcome)
├─ no  → NOT ASSESSABLE          ← no entry, OR an entry that does not qualify
└─ yes → does the reading satisfy the target frozen at KEYED?
          ├─ yes → PROVEN         ← the PRODUCER decides this, not the machine
          └─ no  → NOT MET
```

**The first decision is entirely the machine's and the second is entirely the
producer's**, and the split is deliberate: the machine proves the comparison is
bound to the right *frozen* target and that the evidence record is *complete*;
the producer judges the *result*.

**A recorded reading proves only that the condition was ASSESSABLE. It never
proves the target was met** — a qualifying result can perfectly well show failure.
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
4. **The absence of a QUALIFYING reading yields `NOT ASSESSABLE`** — never a
   passed row, and never grounds for authoring a target after the build (the
   `gate-visuals` precedent, 2026-08-30). *Qualifying* is doing real work here:
   an entry whose evidence file is missing, or whose `Evidence-SHA256` does not
   recompute, or whose stored fingerprint does not match the `MSC` version used
   for the decision, lands here too. An unverifiable reading is not a bad
   reading; it is not a reading.

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
for every rung, what assures the condition and by what — **machine-refused**
(something on disk refuses and blocks), **machine-detected** (machinery emits a
finding but does not refuse), **producer-agreed** (a human key, nothing outside
the model enforcing it), or **no enforcement** at all.

**There are FOUR sources, not three, and the fourth exists because a check that
FINDS is not a check that REFUSES.** The drawing's legend defined
machine-checked as *"something on disk refuses"* while reciprocal stamping
explicitly produces a **finding**, deliberately not a refusal — and both claims
could not stand. Caught by the producer at the combined eye on 2026-09-01. The
taxonomy now reads: **machine-refused** (something on disk refuses and blocks) ·
**machine-detected** (machinery emits a finding but does not refuse) ·
**producer-agreed** (a human key, nothing outside the model enforcing it) ·
**no enforcement**. Reciprocal stamping is the one machine-detected line and is
**not counted among the refusal-backed checks**.

**Fifteen assurance questions, counted by tense — because four of them are
dual-marked, and counting both markers as two lines would make proposed
assurance read as present assurance.** The count was **thirteen** at the GO of
2026-08-31, under the three-way split. Every figure below is **re-derived from
the drawing's rows**, never adjusted arithmetically from the old totals.

- **Today:** five machine-refused, zero machine-detected, three producer-agreed,
  seven unenforced — **ten of fifteen rest on agreement or on nothing.**
- **Once the designed machinery is built:** eight machine-refused, **one
  machine-detected**, three producer-agreed, three unenforced.

**Four lines move between those two readings**, and each is designed-but-unbuilt
rather than absent by choice:

1. the design gate's *has the keyed target drifted since approval* — needs the
   versioned `MSC` approval fingerprint;
2. *an `Observed result` entry exists, names the `MSC` and carries its exact
   frozen fingerprint* — needs the structural acceptance-record parser;
3. *the Requirement ↔ `MSC` link is stamped in both directions and neither stamp
   is stale* — needs reciprocal stamping, ruled built-now on 2026-09-01;
4. *the evidence artifact is the one that was judged* — needs the parser to
   recompute `Evidence-SHA256` over the referenced file's raw bytes.

Each is marked both ways in the drawing for exactly that reason.

**The comparison is producer-agreed, not unenforced — corrected 2026-09-01.**
The drawing marked *whether the reading satisfies the frozen target* as having
no enforcement, which was true while nobody had decided who performs it. Ruling
4 settles that: the producer explicitly judges it and keys the outcome into the
acceptance record, which is a human key with nothing outside the model enforcing
it — the drawing's own definition of producer-agreed. The producer's own
statement of the line: *"the comparison is not assured by nothing… what remains
absent is machine recomputation of that semantic comparison."*

**Three questions remain genuinely unenforced, in both tenses**, and naming them
is the point of the drawing: that a success condition was declared at all · that
the condition is named on the steps it affects · that the work is actually aimed
at the condition.

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
> verification method; observed results are entries in the immutable acceptance
> record, bound to the condition by its frozen fingerprint. See
> `docs/design/requirements-success-measurement.md`.

**The proposed wording was corrected on 2026-09-01** — it said *"observed
results are linked evidence"*, which the binding-direction ruling falsified: they
are not linked, they are recorded. Correcting a *proposed* edit inside a living
design doc is not rewriting history; the catalog itself is still untouched.

**And a standing rule the producer attached to it, 2026-08-31, which reaches
past this item:** *"If a checker mistakes struck text for a live claim, teach
the checker to distinguish retired text; do not rewrite history to satisfy a raw
text scan."* This answers the 2026-08-30 gotcha — *preserving a struck claim
verbatim trips any checker that hunts the claim* — in the opposite direction
from the one that gotcha implied. **The record is authoritative and the checker
adapts to it, never the reverse.**

## What this design does not settle

**Five of the things this section listed at the GO of 2026-08-31 are now
settled** — the `Observed result`'s home, whether `MSC` is the right code,
reciprocal link stamping, the comparison mechanism, and the evidence reference.
Each closed by a producer ruling recorded below, and each is now written into
the body above. What follows is what genuinely remains open.

- **The BUILD of every mechanism designed here.** The versioned approval
  fingerprint, the structural acceptance-record parser, reciprocal
  Requirement ↔ `MSC` stamping and `Evidence-SHA256` recomputation are all
  **owed work, not present machinery**, and every surface here labels them so.
  Until they exist, `KEYED` does not freeze anything a machine would notice and
  no observed-result entry is checked by anything.
- **Three assurance questions, by design, at `mvp`** — that a success condition
  was declared at all · that the condition is named on the steps it affects ·
  that the work is actually aimed at the condition. Named rather than closed;
  the drawing exists so this cannot later be mistaken for machinery.
- **Machine recomputation of the comparison.** `PROVEN` versus `NOT MET` stays
  the producer's judgment. The return condition, in his words: *"Revisit machine
  comparison when the `MSC` target grammar is explicitly typed and at least one
  real condition requires a repeatable comparison that the acceptance producer
  should not perform by judgment alone."* That needs an operator, a value type,
  unit normalization and rules for nonnumeric conditions — free-text targets
  cannot support a trustworthy comparator.
- **Remote and provider-native immutable evidence.** This slice requires a
  stable local snapshot with a recomputable digest; a bare URL or a mutable
  CI-run location is insufficient. Supporting provider-native immutability is
  deferred to the existing out-of-repo-artifacts problem, which is where that
  question already lives.

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

- **RULED 2026-09-01 — the binding direction:** the binding runs **from the
  immutable observed-result entry TO the `MSC`**, never the reverse. The
  producer's reason: *"The living MSC must not be edited after acceptance merely
  to point at a dated record… the record binds itself to the exact predeclared
  condition; the condition does not reach forward into history."*

  This resolved an apparent conflict inside his own Step 2 ruling, raised at the
  gate rather than papered over: the hand-back asked design to define *"how an
  `MSC` references that immutable record"* — an outbound edge — while the seven
  required fields put the `MSC` ID and its frozen fingerprint **on the record
  entry**, which is an inbound reference. The inbound direction wins.

  **The consequences he named, all of them binding:** `evidenced-by` /
  `evidences` is **removed as a stored register link role** · the anatomy
  arrow **reverses** to Observed result → `MSC`, labelled an acceptance-record
  binding rather than a catalog link · the `MSC` gains **no outbound file
  reference and no post-key mutation** · discovery is **derived** by scanning
  immutable acceptance records for entries naming the `MSC` ID · a result
  qualifies **only** when its stored fingerprint matches the `MSC` version used
  for the decision · no qualifying entry yields `NOT ASSESSABLE` · the phrase
  *"the `MSC` is evidenced by the result"* may remain explanatory prose, being a
  **derived** relationship rather than stored link grammar.

  **Verified before the edit, not assumed:** `evidenced-by` was never declared
  in `docs/requirements/catalog.md` (only `verified-by`, at `:204`), and no link
  role appears anywhere under `tools/`. So the removal touches this design's own
  edges table and nothing else — the catalog stays untouched, preserving the
  2026-08-31 rule that the catalog edit belongs to the later schema
  implementation.

- **RULED 2026-09-01 — the evidence location carries a content digest:**
  mandatory, with no `none` escape. His reason: *"A location answers where the
  evidence was found; the digest identifies what was actually judged. Without
  it, a mutable file, URL, or CI artifact could be replaced while the acceptance
  record continued to report PROVEN."*

  **The mvp shape:** `Evidence: <repo-relative path>` and
  `Evidence-SHA256: <64 lowercase hex>`. **Rules, his:** hash the artifact's raw
  bytes with SHA-256 · the acceptance parser **recomputes** the digest for
  repo-relative files · a missing file or a mismatch makes the result **invalid
  and therefore `NOT ASSESSABLE`, never `PROVEN` or `NOT MET`** · external
  evidence must be captured as a **stable local snapshot before acceptance**, a
  bare URL or mutable CI-run location being insufficient in this slice ·
  supporting remote or provider-native immutable evidence remains **deferred to
  the existing out-of-repo-artifacts problem**.

  **The two-digest split, in his words:** *"The digest protects evidence
  identity; the stored MSC fingerprint protects target identity. Both are
  required for an assessable comparison."* They are separate mechanisms and must
  not be merged — the approval fingerprint is a canonical payload over declared
  *fields*, `Evidence-SHA256` is a plain hash over an artifact's *raw bytes*.

  **This overruled the session's own proposal**, which offered an optional
  digest with an explicit `digest: none — <reason>` escape for unhashable
  evidence, on the argument that a fabricated digest is worse than none. He
  refused the escape and closed the gap the other way: snapshot the evidence
  locally so there are always bytes to hash.

- **RULED 2026-09-01 — the comparison is producer-agreed, not unenforced:** the
  assurance drawing's row for *whether the reading satisfies the frozen target*
  moves from `none` to `producer`. His reason: *"The comparison is not assured by
  nothing: the producer explicitly judges whether the observed reading satisfies
  the frozen target and keys that outcome in the acceptance record. What remains
  absent is machine recomputation of that semantic comparison."*

  **The three-way split he stated:** the machine checks that the target
  fingerprint, result entry, value and unit, method reference, evidence digest
  and legal outcome are **structurally valid** · the producer decides `PROVEN`
  versus `NOT MET` · **nothing independently verifies the producer's comparison
  in this slice**.

  **Consequence for the tally, re-derived from the drawing's rows rather than
  adjusted:** fifteen assurance questions with four dual-marked. Today five
  machine-checked, three producer-agreed, seven unenforced — ten of fifteen on
  agreement or nothing. ~~Once the designed machinery is built: nine, three,
  three — six of fifteen.~~ **The designed-state figure is SUPERSEDED an hour
  later by the taxonomy ruling below:** eight machine-refused, one
  machine-detected, three producer-agreed, three unenforced. The today figure
  stands unchanged, machine-detected being zero today.

- **RULED 2026-09-01 — a check that FINDS is not a check that REFUSES, and the
  assurance taxonomy splits in two:** the producer refused his key at the
  combined eye on a contradiction the drawing carried against itself. Its legend
  defined machine-checked as *"something on disk refuses"*, while the reciprocal
  stamping row it had just gained explicitly produces a **finding, not a
  refusal**. His finding: *"Those claims cannot both stand… Do not count
  reciprocal stamping among refusal-backed machine checks."*

  **The split:** **machine-refused** — something on disk refuses and blocks ·
  **machine-detected** — machinery emits a finding but does not refuse ·
  **producer-agreed** · **no enforcement**. Applied everywhere the taxonomy
  appears: the drawing's markers, its legend, its `<desc>`, and this document.

  **The re-derived totals, his:** today **five machine-refused, three
  producer-agreed, seven unenforced**; once the designed machinery is built
  **eight machine-refused, one machine-detected, three producer-agreed, three
  unenforced**. Fifteen questions, nineteen markers, four dual-marked.

  **Why this is substantive rather than cosmetic, and it is the same class as the
  tally ruling that preceded it:** a non-blocking check counted under a
  refusal-promising label makes weaker assurance read as stronger assurance —
  exactly what counting a dual-marked row as two lines did on 2026-09-01 morning.
  The drawing exists to state the honest picture, so a label that overstates its
  own strength defeats the artifact.

- **RULED 2026-09-01 — a required fact the parser does not check is not a
  requirement:** the producer refused his key on the anatomy view for omitting
  `Taken` from the qualification contract. The entry declared seven fields, the
  prose claimed eight required facts, and the qualification box then listed seven
  conditions that never validated the date the reading was taken.

  **His count, and it is the correct one:** **nine** required facts — the `MSC`
  ID · the `MSC` fingerprint · the observed value · the unit · the method · the
  taken date · the evidence path · the evidence digest · the outcome. **Eight
  qualification conditions**, the value and its unit being two facts checked by
  one condition. `Taken` gains condition 7: a valid `YYYY-MM-DD` value.

  **The rule he attached:** *"The prose and parser contract must match."* A field
  listed as required and then left unchecked is a comment wearing a
  requirement's clothes — the same defect class as the hollow `KEYED` freeze
  caught earlier the same day, one altitude down.
