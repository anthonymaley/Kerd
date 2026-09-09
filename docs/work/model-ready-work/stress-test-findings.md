# Findings from the launch story, failure story, and website

These three artifacts were used as product tests:

- [Launch story](launch-story.md): can the value be explained simply?
- [Failure story](failure-story.md): which assumptions could kill the product?
- [Draft website](website/): can an ordinary person understand the experience
  without reading the design?

## What became clearer

The product is not a prompt tool for software teams. Its intended audience is
anyone commissioning meaningful work: product and project teams, leaders,
operators, researchers, creators, and builders. The shared need is to define a
result, give a model the right work, and receive understandable proof.

The simplest useful promise is:

> Create what you want, not the perfect prompt.

The strongest experience is the live work view: what are we building, where
are we, what is happening, what has been proven, and what needs the person.

## What could still kill it

### 1. Safe assumptions have no operational boundary

“Proceed on safe assumptions” is not enough. A confident Conductor could encode
a product decision as a reversible default.

Required correction: define an assumption test. An assumption is safe only when
it is reversible inside the current slice, does not change a success measure or
boundary, creates no external commitment, and would not reasonably change the
person's decision to run the work. Otherwise ask.

### 2. Coverage can prove preservation but not requirement quality

A coverage report can prove that the prepared prompt contains the brief. It
cannot prove the brief describes the right work.

Required correction: readiness needs separate checks for provenance,
measurability, contradiction, decision ownership, and evidence—not merely field
presence.

### 3. Work levels can be gamed

People may label consequential work Quick to avoid review, while an overly
cautious system may classify ordinary work Important/Deep.

Required correction: derive a recommended level from consequence,
reversibility, uncertainty, external commitment, and proof strength. A person
may override it, but a lower-safety override must name the lost protection and
may be refused for hard safety boundaries.

### 4. Progressive disclosure can become progressive concealment

All views can share correct data while the high-level summary omits the fact
that would change approval.

Required correction: define promotion rules. Unmet mandatory outcomes, material
losses, unresolved producer decisions, weak proof, external commitments,
blocked dependencies, and changed safeguards always appear at every approval
level.

### 5. Cross-model work needs evidence admission and a budget

Bounded jobs prevent endless chat, but Conductor still needs a rule for what
enters product truth and when another model is worth its cost.

Required correction: model output enters the product record only when it maps
to a declared measure, resolves a named uncertainty, or supplies independently
verifiable evidence. Every cross-model plan declares a time/token ceiling and
the expected measure it improves.

### 6. Speed must measure time to an accepted outcome

Time to model completion can look excellent while rework, integration failure,
and delayed human decisions make the product slower.

Required correction: the primary speed measure is elapsed time from initial
request to an accepted, usable outcome. Model-run time remains diagnostic.

### 7. The promise may be too broad

“Create what you want” is compelling but risks implying that one process works
equally well for strategy, research, operations, creative work, and software.

Required correction: keep the general ambition, label portability as a
hypothesis, and require mixed-domain trials before making the broad launch
claim.

### 8. The website shows understanding, not actual use

The draft explains the product and makes visual depth tangible. It does not yet
let a person conduct an interview, approve a brief, dispatch work, or observe a
real changing state.

Required correction: the first interactive product slice should be one guided
interview that produces a readiness verdict and live work view—not a larger
marketing site.

## Changes to the smallest viable product

The first usable slice becomes:

1. One adaptive interview for a Standard job.
2. Assumption classification with provenance.
3. Readiness checks beyond field completeness.
4. A derived Product-level work view with mandatory fact promotion.
5. One prepared model job and coverage report.
6. One evidence-mapped outcome report.
7. Elapsed time to an accepted outcome.

Feature maps, all four visual depths, automated cross-model routing, and broad
profile optimization remain designed but should follow only after this slice
works.

## Current verdict

**Revise before a build trial; ready for independent design review after status
and prototype boundaries are corrected.** The central product idea survives all
three tests. The fatal uncertainty is not prompt preparation; it is whether the
guided interview can achieve enough requirement quality without moving the
burden back onto the person.

