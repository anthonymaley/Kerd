---
route: new
stage: framed
---

# DESIGN WAIVER — switch-fidelity

**Keyed by the producer 2026-09-02.** This is a **waiver**, not a gate record.

**Why it lives in `docs/gates/waivers/` and not in `docs/gates/`.** `AU3`
requires every filename directly under `docs/gates/` to match
`^\d{4}-\d{2}-\d{2}-<slug>-<rung>\.md$`, whose only legal suffixes are rung
names. **A waiver has no legal gate-record filename today** — the same gap
CONTEXT.md already records as *"gate records can only say GO: a refused gate has
no dated home."* A waived gate has no home either. Filing it here keeps the
audit honest (AU3's glob is non-recursive, so this is correctly not counted as a
gate record) without inventing a filename that the design-GO glob would read as
a pass. Verified 2026-09-02: `glob('docs/gates/*-switch-fidelity-design.md')`
returns empty with this file in place.

> **THIS IS NOT A DESIGN GO RECORD AND MUST NEVER BE READ AS ONE.**
> No design package was written, no view was drawn, no concern was declared and
> nothing was approved before the build. This record does not supply the missing
> evidence, and it does not claim the design gate passed. It records that the
> producer **deliberately skipped** the rung, and it carries what that cost.

---

## 1. Work item and exact rung waived

`switch-fidelity` · the **`design`** rung · **slice 1 only**.

Slice 2 is not covered. The `viability`, `scope` and goal rungs are not
covered — the goal gate was explicitly kept.

## 2. Dates

- **Skip decided:** 2026-08-07, mid-session, before the build proceeded.
- **Waiver recorded:** 2026-09-02 — twenty-six days later, once a mechanism
  existed to record it honestly. The delay is itself part of the record: before
  the `inline-composer` design was keyed on 2026-09-02, this repo had no way to
  say *"skipped on purpose"* and the item sat blocked demanding a GO record it
  was never going to get.

## 3. The producer's decision, verbatim

> as many as we can do, lets fill the gaps before we lose the window

## 4. Why the rung was skipped

The gaps were already diagnosed and enumerated in the frame. The producer judged
that closing as many as possible was worth more than agreeing a design for
closing them, **because the diagnosis was the expensive part and it was already
done** — and because the session's remaining context was the binding constraint.

## 5. Evidence the skip was deliberate rather than forgotten

Three independent records, all written the same day, before or during the build:

- **The session log, 2026-08-07:** *"Slice 1 skipped the design rung on Tony's
  call ('as many as we can do, lets fill the gaps before we lose the window'),
  **flagged before proceeding**. First work item to do so. The goal gate is
  kept."* — raised and settled in advance, not discovered afterwards.
- **CONTEXT.md's standing decision** names it in the item's own headline: *"the
  first item to skip the design rung, on Tony's call."*
- **The goal gate was consciously retained**, which is the tell that a choice
  was made between gates rather than a gate being missed. A forgotten rung does
  not come with a decision about which other rung survives.

## 6. Assurance lost

**The sharpest loss is one the item declared about itself and then broke.** Its
risk ledger closes with:

> The three accepted unknowns all carry the design rung as their review trigger.
> **None may reach the build rung unanswered.**

Slice 1 shipped at v0.90.0 (`47b30ad`) with **all three unanswered**:

1. Reading more at pickup fills the window faster, forcing more boundaries.
2. The fidelity property stays unfalsifiable — no check proves a pickup restored
   what the close recorded, so every countermeasure ships unverified.
3. "Read in full" gets silently bounded by the reader when the target is large.

**Also lost:**

- **No agreed model of the fix before the build.** In the item's own words:
  *"slice 1's value rests on the gaps being correctly diagnosed, not on the
  fixes being measured."* If a gap was diagnosed wrongly, nothing in the process
  would have caught it.
- **No drawing, no declared concern, nothing agreed at a glance.** This repo's
  standing finding is that every substantive structural correction of the last
  month came from a picture rather than from prose.

## 7. Compensating evidence

Real, and deliberately not inflated into a substitute for design.

- **The four gaps are verifiable as closed in the live skill text**, measured
  2026-09-02: the derived board joins both ends of the boundary, the
  no-silent-truncation rule is present, the licensed-prune rule is present, and
  the `light`/`low` modifiers are gone with only their removal record
  remaining. **The build is checkable even though the design was not agreed.**
- **The scope rung was passed normally** — the four gaps were enumerated and
  gate-checked before the build.
- **Two of the three accepted unknowns have since been measured rather than
  left assumed.** Unknown 1 was quantified 2026-09-01: a pickup costs ~17% of
  the window, and CONTEXT.md has grown 54KB → 177KB since the risk was written —
  **the risk materialised as predicted.** Unknown 3's rule held at the
  2026-09-01 pickup, which read all three files in full and said so.
- **Unknown 2 remains genuinely open.** `fidelity.py` was built since and runs
  in CI, but it proves *artifact reachability*, never that a pickup restored
  what the close recorded. It is not compensation for this loss and is not
  offered as such.

## 8. Scope — no precedent inferred

This waiver covers **`switch-fidelity`'s `design` rung, slice 1, and nothing
else.** It is not authority for any other item, any other rung, or any future
skip on this item. It does not establish that design may be skipped under time
pressure. The 2026-09-02 keyed design is explicit that **a waiver is an
exception, never a route**.

## 9. Review / expiry trigger

**This waiver expires when `switch-fidelity` slice 2 is framed.** Slice 2 may
not enter design carrying slice 1's three unreviewed unknowns — that would let a
one-time exception become the item's standing condition, which is precisely what
§8 forbids. At that frame, the three accepted unknowns are answered or
explicitly re-accepted with their own trigger.

## 10. Downstream obligation — the debt stays visible

**Every later `switch-fidelity` record must carry this waiver by name**: any
handoff record, any acceptance record, and slice 2's frame. The item's design
rung reads **`design waived`**, never `design pass`, on every surface that
reports it.

**Known limit, and the producer required it recorded rather than implied: the
machine cannot see this waiver, and no derived rung changes until waiver-aware
routing is built.**

Measured with this record in place, 2026-09-02, not asserted:

```
$ python3 tools/gates/gate.py route switch-fidelity
enters at: design
need: docs/design/switch-fidelity.md — file exists
need: docs/gates/*-switch-fidelity-design.md — design GO record
```

**The machine still reports the missing design GO, and that is correct.** This
waiver records the truth before the machinery can recognise it; it must not
masquerade as a GO merely to move the board. `tools/gates/` was untouched by the
2026-09-02 key. Rendering `design waived`, permitting routing forward, and
carrying the debt into downstream records are all designed and unbuilt.
**Until they are built this obligation is prompt-layer and nothing enforces
it** — the same declared limit every unenforced surface in this repo carries.

---

**Producer key:** Tony, 2026-09-02

**Clock:** 15:01 EDT
