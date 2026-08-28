---
route: new
stage: framed
work-type: software-change
---

# Requirements success measurement — every requirement declares how we will know it was met, before design starts

## Question set

- Q: What is the perceived problem, in the words of the person who has it?
  A: Drift, and unmet expectation between what the user asked for and what was built or how it performed. Users see Kerd as a black box: it helps them build and execute ideas, but the results can be misaligned to their vision or expectations. Measurable requirements force that alignment — and force the result the user actually wanted.
- Q: Who experiences it, and how often does it bite?
  A: Every Kerd user running conductor or Drive who is trying to create an outcome. It bites every session that produces an artifact.
- Q: What would be different if this worked — in units or outcomes someone could measure?
  A: Users can provide all the outcome measurements within the requirements, and see them being measured and accounted for through design and work handoff. Then they can trust the loop to execute and produce a shippable artifact that meets the requirements and expectations.
- Q: What is the smallest thing that would prove it, and what is deliberately left out?
  A: One requirement with a measurable aspect going through the whole lifecycle, with its measurements proven. Left out: any other requirements not needed to prove the end-to-end result.
- Q: What could make this not worth doing at all?
  A: If the process were too long for the user to do, too much friction, not obvious enough to them what is happening — and no visibility of state, progress and measurements.
- Q: What already exists that this touches or replaces?
  A: The superpowers skill, and the kerd:conductor skill.
  (Added by the model, not named by the producer — repository surfaces this also touches: the requirements register `docs/requirements/`, the gate checks in `tools/gates/kit.py`, the rigor levels, the design and work-handoff artifacts, and loop verification.)

## Value

The producer's words, at the frame gate on 2026-08-28 (the question set above
is the source; nothing here is paraphrased into a target he did not give):

> Drift, and unmet expectation between what the user asked for and what was
> built or how it performed. Users see Kerd as a black box: it helps them build
> and execute ideas, but the results can be misaligned to their vision or
> expectations. Measurable requirements force that alignment — and force the
> result the user actually wanted.

And the standing statement of 2026-08-23 (CONTEXT.md): *Kerd should make sure
that anyone using it declares, before design starts, how they'll know each
requirement was actually met — asking for as much or as little as the size of
the job warrants.*

### Value, in units

- **Requirements carrying a measurable success condition: 0 of 52 → every
  requirement in a release.** Measured 2026-08-23: 52 register blocks carry a
  statement, a reason, links and an approval; none carries a number or a target.
- **The proof, smallest form: one requirement** with a measurable aspect going
  through the whole lifecycle, with its measurements proven. Any other
  requirements not needed to prove the end-to-end result are out.
- **What it buys the user (A3):** the outcome measures are given inside the
  requirements, seen carried through design and work handoff, and the loop can
  be trusted to produce a shippable artifact that meets the requirements and
  expectations.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| The process is too long or too much friction for the user, and not obvious enough what is happening — no visibility of state, progress and measurements (A5) | yes | the capability is skipped or waived every time, so 0 of 52 stays 0 of 52 while the machinery reads as complete — the "shipped an instrument nobody was obliged to use" failure, measured twice in this repo | high without a countermeasure — every declared-per-project ask so far has drifted to the cheapest state | `docs/product/funnel-driver.md` gap 8; `rigor-level` slice 2 (per-level floors) specced 2026-08-05 and never built; `grep -i floor tools/gates/*.py` returns nothing | unqualified — named only, per the frame-gate floor | to be sized at scope: the ask is scaled by the declared rigor level (a wired, empty socket), and state/progress/measurement are shown on the derived board | scope gate |
| It touches conductor and superpowers (A6), and the umbrella rule forbids requiring conductor to change | no | any design that needs conductor to carry a measurement step re-opens the retired killer risk of `funnel-driver` | medium | the rule at `docs/design/funnel-driver.md` — *Drive may CALL conductor, never REQUIRE it to change* | unqualified — named only | to be sized at scope: the measurement lives in the work record and the gates, read by Drive, never inside conductor's protocol | scope gate |

## Grounding

- docs/product/requirements-traceability.md — the register whose 52 blocks carry no target; the six-element shape this adds a seventh to
- docs/product/rigor-level.md — the empty socket: the declared level that nothing hangs off
- docs/design/funnel-driver.md — the umbrella rule this must build under
- docs/product/gate-visuals.md — the `Product measurements met` row with no upstream declaration, the same gap seen from the acceptance side
