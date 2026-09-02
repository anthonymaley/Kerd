# Inline composer — design

**Status: PROPOSED, awaiting the producer's key at the design rung.** Nothing
here is agreed until that key lands. The GO record is drafted outside
`docs/gates/` and moves only on the key, per the 2026-08-25 rule.

This design settles three questions. The first is the item's frame. The second
is its risk ledger's third row, whose review trigger reads *"Fires at the design
rung — the decision must be taken there, not deferred again."* The third arrived
2026-09-02 as a producer ruling and is folded in here because it has no other
home.

---

## 1. The minimal inline score — one artifact, not a second kind

**The score for inline work is a work specification. It is the same artifact,
the same filename convention and the same gate as a delegated score; it is
simply short.**

**One artifact type, sized by content rather than renamed by size.** It carries
`## Pieces` and a `**Verify:**` on every step because that is what makes any
score build-ready, long or short. Two or three Pieces is a legal score. Twenty
is a legal score. The rung never asked for size, and a short score answers the
handoff question as honestly as a long one.

`docs/plans/YYYY-MM-DD-<slug>-spec.md` is the home. Today's machinery already
reads that glob, which is convenient — but the reason is that there is one kind
of thing here, not that a glob exists.

**Why not a second artifact type.** A `*-score.md` beside `*-spec.md` would be
two homes for one thing, joined by convention — this repo's most-measured defect
class, and the test it fails is the standing one: *what breaks if one side is
renamed?* Nothing. The board derives landed counts from the spec glob, so a
second home would also make inline work invisible to the progress render, which
is the symptom that motivated the frame.

**What makes a score "inline" is the call, not the file.** The delegated path
buys two composer passes — scoping, then the score. Inline work buys **one**:
the conductor sends intent, boundaries and the files it already has open, and
the composer returns a short score written straight to disk. Pass 1 exists to
stop a conductor-curated brief becoming the composer's blind spot on unfamiliar
terrain; on a small inline change the conductor is already standing in the
terrain, so the pass buys nothing and costs a round trip.

**Sized like every other call.** Model and effort go in the dispatch, as they do
for players and for the delegated composer. A one-file wording change earns a
middling effort; a small change with a real decision in it earns high. This is
the existing lever, not a new one.

**The composer-unavailable rule applies unchanged** — the conductor writes the
score itself and says so explicitly at the approval gate, so the producer knows
they are approving the lesser artifact.

### What this removes

Two sentences in `skills/conductor/SKILL.md`, both of which assert a false
premise:

- `:214` — *"No composer call, no spec file."*
- `:247` — *"Skip the composer call entirely for lean/inline tasks — if there's
  no score to write, there's no one to summon."*

There is always a score to write. The reasoning exists; today it is spent once
in conversation and then lost. The count of scores left by inline work is zero,
and it is zero **by rule** rather than by accident.

---

## 2. Two questions, two approvals — and one file may answer both

This is risk 3, answered rather than deferred a third time. **An earlier draft of
this design answered it wrongly and the producer refused it; the refutation is
recorded here because the wrong answer is instructive.**

**The rejected argument:** *a score cannot satisfy the design rung because the
composer writes it and the composer is not the producer.* **That is false.**
Model-drafted design documents are in exactly the same position — every design
package in this repo was typed by a model — and they satisfy the design rung
fine. **What makes a design agreed is the producer's key, not who typed the
proposal.** Authorship was never the test.

**The rejected shape also recreated this item's own killer risk.** Requiring a
ten-field waiver for every inline change would make the short route carry more
ceremony than the score it exists to produce — which is risk 1 verbatim: *a
composer call on every small task becomes ceremony, so users abandon conductor
for inline work.* A design that reintroduces the risk it was framed to avoid is
not a proportionate design.

### The shape

- **The short spec remains ONE artifact.** No second file, no second type.
- **When the work carries design judgment, the spec carries a concise,
  explicitly labelled design decision** — a short section stating what was
  decided and why, not a package.
- **The producer keys that decision separately from approving the work
  specification.** Two keys are not owed; the *questions* are distinct and the
  approvals are distinct acts even when one of them is a machine check.
- **One file may supply evidence at two rungs, and the two questions stay
  distinct.** *Have we agreed what we are building?* is the design question and
  the producer answers it. *Is this build-ready?* is the handoff question and
  the machine answers it against `## Pieces` and a `**Verify:**` per step.
- **If there truly is no design to agree, the producer may issue a waiver.**
  That is the **exception**, not the inline default. §2b defines it.

**Stated as a conceptual route, deliberately.** Whether today's gate machinery
can recognise one file as evidence at two rungs is **later implementation
work**, and this design does not distort the route to fit today's file-glob
behaviour. The earlier draft derived its shape from `kit.py`'s spec glob, which
is designing backwards from an implementation detail.

## 2b. The waiver — the exception, not the route

Reserved for a rung **deliberately skipped**: the producer decides there is
nothing to agree, and the decision goes on the record. Per the producer's
ruling of 2026-09-02 the machine renders **`design waived`, never `design
pass`**; a valid waiver may permit routing forward, but every later handoff and
acceptance record retains it as **visible debt** and it never makes the missing
evidence appear to exist.

Ten required fields. A waiver missing any of them is not a waiver:

| Field | Why it is required |
|---|---|
| Work item and **exact rung** waived | A waiver is never item-wide |
| Date recorded, and the date the skip was decided if different | The record dates the event, not the writing |
| Producer's **verbatim** decision | The model does not paraphrase the key |
| Why the rung was skipped | Reason, not permission |
| Evidence the skip was **deliberate rather than forgotten** | The field that separates a waiver from a hole |
| **Assurance lost** by skipping it | The debt, stated in the record that creates it |
| Compensating evidence, if any | Often none; then say none |
| Scope: this item and rung only, **no precedent inferred** | Stops one waiver becoming a route |
| Review or expiry trigger | The accepted-risk discipline, applied to a gate |
| Producer key and `**Clock:**` line | The same-turn time rule |

**Three cases stay distinct, and conflating them is the failure this design
exists to prevent:**

1. **A deliberate skip** → a waiver. `switch-fidelity` is this case.
2. **Shipped before the obligation existed** → **not** a waiver. Nothing was
   decided, so a waiver would fabricate a decision. See §3.
3. **A gate simply forgotten** → neither GO nor waiver. **It stays blocked.**
   There is no record type for an oversight; inventing one would make
   forgetting the cheapest route through the ladder.

**Risk 3's countermeasure moves from `temporary` to `permanent`** at this gate,
and its review trigger is discharged.

## 3. Legacy shipped-inline work — an honest dated closure

`model-effort-advisory` shipped complete at v0.98.0. All five of its scope
bullets are live in `skills/conductor/SKILL.md` today, verified line by line. It
has no design record and never will have an honest one, because **no design was
agreed and no skip was decided** — the score mechanism did not exist yet. Its
frame says so: it closes *"through whatever this produces, in their own
sitting."*

**A waiver would be a lie in the field that matters most** — *evidence that the
skip was deliberate*. Nothing was decided. The obligation did not exist.

**What the record is for:** it documents history and permits honest migration.
**It closes the legacy ROUTING gap** — the item moves forward rather than sitting
blocked forever on evidence that was never going to arrive. **It does not close
the historical EVIDENCE gap**, which stays open and visible in every later
record. **What it must never do is imply that the missing design evidence has
appeared, or recreate it.** Those are two different gaps and only one of them is
closable.

**The proposal: a `legacy-closure` record.** Dated, producer-keyed, and
explicitly **not** a design record. It carries:

- what shipped, when, and in which commits — derived, not recalled;
- that **no score was written because none was owed at the time**, with the date
  the obligation began;
- what reasoning was therefore **not preserved** — stated as what it is: the
  process did not require or retain it. **Not that nobody could have produced a
  design.** They could have; nothing obliged them to, and nothing kept it;
- what **can** still be verified against the shipped code today, and the command
  that verifies it;
- the item's onward route, carrying the absence as named debt.

It never claims prior design, and it is not a precedent: the record's own scope
line says the mechanism it closes under has since been built, so no later item
can reach it.

**What separates the three records, in one line each:** a **GO** says the
evidence exists and the producer read it · a **waiver** says the producer chose
not to produce it · a **legacy closure** says the process never required or kept
it, and closes the routing gap while leaving the evidence gap open.

---

## What this design does NOT settle

- **The machinery.** No change to `tools/gates/` in this slice — the frame
  excluded it deliberately, and it stands. Rendering `design waived` rather than
  `design pass`, and carrying a waiver forward into later handoff and acceptance
  records, is **designed here and built later**. Until it is built, a waiver is
  a document the machine cannot see, and this design says so rather than
  implying otherwise.
- **A refuser that checks the score was written.** Risk 4, unenforced in slice
  1 by design, and named as such on every surface. Its review trigger stands:
  it fires once slice 1 has run on real inline work and the score's shape is
  known.
- **`hooks-autoload`'s closure.** Named in the frame alongside
  `model-effort-advisory`, and it closes the same way, in its own sitting. Not
  scoped here.
- **Whether `switch-fidelity`'s waiver is granted.** This design defines the
  record; the producer decides whether that rung is waived. Two separate acts.

## Views

**One view, and the earlier `n/a` refusal is withdrawn.** It was refused on the
grounds that the artifact is a record format whose content is its structure —
the producer rejected that, correctly: **GO, waiver and legacy closure are a
three-way decision with different downstream consequences**, which is precisely
what a drawing carries and a table does not. A table lists fields; it cannot show
that one branch routes forward with debt attached, one routes forward carrying an
absence, and one does not route at all.

| Concern | Viewpoint | View |
|---|---|---|
| How inline work reaches a keyed design, and the two paths that are not it | flowchart | `docs/design/inline-composer/inline-routes.html` |

The orientation artifact drawn this sitting is **temporary and does not replace
this** — it is a dated snapshot of where five items sit, not a durable design
view of a mechanism.

## Named answers — the stage-1 measurements

Targets, with a number and a scope each.

| What is measured | Baseline | Target | Scope and how it is read |
|---|---|---|---|
| Inline-routed work that leaves a valid score | **0** — zero scores exist, by rule | **100%** of inline-routed items begun after this slice ships | Scope: items conductor routes lean/inline after the release. Read by pairing each such item against `docs/plans/*-<slug>-spec.md`. Items begun before the release are out of scope — they are §3's business |
| Items stuck at a rung with no record of why | **3** — `model-effort-advisory`, `switch-fidelity`, `hooks-autoload` | **0** | Scope: these three named items only, no others implied. Read by `gate.py route <slug>` demanding a rung with no GO, waiver or legacy closure on disk |
| Waivers carrying all ten required fields | n/a — no waiver exists yet | **100%** of waivers written | Scope: every waiver, from the first. **Not enforced in this slice** — nothing on disk checks a waiver's fields, so this target rests on the producer reading the record. Declared limit, not an oversight; the checker is the machinery slice |

The third target is weaker than the other two by construction, and it is
labelled rather than quietly equalised.
