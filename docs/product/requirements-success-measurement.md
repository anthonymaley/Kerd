---
route: new
stage: designed
work-type: software-change
concerns:
  - concern: what the measurable condition contains and what artifact carries it
    viewpoint: nested
    view: docs/design/requirements-success-measurement/condition-anatomy.html
    approval: Tony, 2026-08-31 · fp:fefa90380fe3
  - concern: how that condition travels from declaration to demonstrated proof
    viewpoint: state
    view: docs/design/requirements-success-measurement/condition-lifecycle.html
    approval: Tony, 2026-08-31 · fp:0a91dbcac981
  - concern: where assurance comes from at each rung, and where it does not
    viewpoint: flowchart
    view: docs/design/requirements-success-measurement/assurance-boundary.html
    approval: Tony, 2026-08-31 · fp:c9b8d06ebfb6
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
| The process is too long or too much friction for the user, and not obvious enough what is happening — no visibility of state, progress and measurements (A5) | yes | the capability is skipped or waived every time, so 0 of 52 stays 0 of 52 while the machinery reads as complete — the "shipped an instrument nobody was obliged to use" failure, measured twice in this repo. This is the WHOLE of the declared value, not a fraction of it, which is what makes the row killer rather than merely serious | high with no control — every declared-per-project ask so far has drifted to the cheapest state. The producer judges it medium with the countermeasure below. That figure is an explicit producer judgment, not a derived or measured one: the control binds by agreement at one gate and nothing machine-enforces it, so Drive does not structurally guarantee compliance | `docs/product/funnel-driver.md` gap 8; `rigor-level` slice 2 (per-level floors) specced 2026-08-05 and never built; `grep -i floor tools/gates/*.py` returns nothing | countermeasure - temporary | For this slice, the producer declares the item's rigor level and agrees the smallest measurable success condition proportionate to it during scope. Drive carries that condition through design, handoff, loop and acceptance. No automated per-rigor floor is claimed | Replace the manual proportionality decision when `rigor-level` slice 2 lands and defines enforceable per-level measurement floors; integration with those floors must then be explicitly scoped |
| It touches conductor and superpowers (A6), and the umbrella rule forbids requiring conductor to change | no | any design that needs conductor to carry a measurement step re-opens the retired killer risk of `funnel-driver`. Below the declared value: it costs the umbrella rule, not the 0-of-52 outcome — which is why this row is not killer | medium — the pull is real (A6 names conductor and superpowers as what this touches) but it is a design choice, made once, at a gate that reads this row | the rule at `docs/design/funnel-driver.md` — *Drive may CALL conductor, never REQUIRE it to change* | countermeasure - permanent | The measurement lives in the work record and the gates, read by Drive, never inside conductor's protocol. This depends on nothing unbuilt, which is why it is permanent rather than temporary | The first design that proposes carrying a measurement step inside conductor's own protocol |

## Scope

Rigor level: mvp

**Declared by the producer, 2026-08-31.** It exceeds a spike — this ships a real
capability and must prove one measurable requirement end to end, where a spike
forbids a build and requires findings instead. It falls short of
`production-v1` — the deliberately narrow proof, the named exclusions and the
deferred general scaling policy do not justify full release rigor.

**The smallest thing that proves it**, in the producer's own words at the frame
gate (A4, quoted, not paraphrased into a target he did not give):

> One requirement with a measurable aspect going through the whole lifecycle,
> with its measurements proven. Left out: any other requirements not needed to
> prove the end-to-end result.

So the commitment is: **one requirement carries a measurable success condition,
declared before design, and that condition is visibly carried through design,
work handoff, loop and acceptance — with the measurement actually taken at the
end rather than asserted.**

**Deliberately out of this scope, each with its reason:**

- **`rigor-level` slice 2 — the enforceable per-level measurement floors.**
  Absorbing it would merge two work items, enlarge the smallest proof, and make
  this scope depend on machinery it was not framed to build. This item proves
  one measurable requirement end to end at ONE declared rigor level; it does not
  build the general scaling policy. The dependency is held visible instead, as
  the review trigger on risk row 1.
- **Every other requirement in the register.** The proof is end-to-end depth on
  one, not coverage across 52. Coverage is what the value statement targets;
  it is not what this slice buys.
- **Any change to conductor's protocol.** The umbrella rule binds: Drive may
  call conductor, never require it to change (risk row 2).
- **The design itself.** This scope gate settles what we are committing to
  build, not how. No design authored here.

## Grounding

- docs/product/requirements-traceability.md — the register whose 52 blocks carry no target; the six-element shape this adds a seventh to
- docs/product/rigor-level.md — the empty socket: the declared level that nothing hangs off
- docs/design/funnel-driver.md — the umbrella rule this must build under
- docs/product/gate-visuals.md — the `Product measurements met` row with no upstream declaration, the same gap seen from the acceptance side
