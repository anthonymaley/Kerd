# Shared memory — design

Living document. Product doc: `docs/product/shared-memory.md`. Slice 1 is the
journey page; this records what the page must be, and why, as it converges.

## Annotation round 1 — Tony on the first rendered page, 2026-08-07

The page was `docs/plans/journey-switch-fidelity.html`, generated from disk.
Five reactions, each with its disposition. Read → act → record, on the
established annotation discipline.

### 1. "Why this exists" — keep the mock's visual, not a wall of quote

> *"This is essentially the idea current-to-ideal view. We did a good job in
> the journey mock-up of visualising this — we need to retain that approach.
> Should be a visual with a statement, shorter than what you have here,
> elevator-pitch level."*

**Taken.** The rendered page put the requirement in verbatim as a long
blockquote. The agreed mock instead drew it: a *Current situation* panel (a
small SVG plus numbered pains) beside a *Proposal* panel (a small SVG plus
targets in units plus the cost named). That is the A3 Proposal head from
`docs/design/talk-formats.md`, and it works because it is seen rather than
read.

**Open, and it is the one genuine blocker in this round: a drawing has no
source on disk.** Every other field on the page is derived. A drawing cannot
be derived from a markdown file — someone has to draw it. Until that has a
declared home, the head cannot be generated.

### 2. "What winning looks like" — the block failed outright

> *"Means exactly zero to me. Don't understand what it is or what it's telling
> me."*

**Taken — cut as a standalone block.** It rendered the product doc's declared
units (`2 observed → 0`) stripped of the sentence that gave them meaning. A
unit without its claim is noise. Where those numbers belong is inside the
Proposal panel, as targets, exactly as the mock had them.

What Tony expected in that slot is the more important half of the note:

> *"I would have thought this is where we show stage 1 and its steps as a
> tracker? Is that rung complete or in progress still? Traffic light for each
> step, and show with links what was produced. So stage one is Idea, so we
> should see diagrams, eval matrix, research, right? … The horizontal tracker
> is good but the stages themselves are shallow and don't show the level of
> detail needed. Maybe this is because we don't have much for this goal? Same
> for Design — we need an architecture diagram (high level) etc. Plan stage
> too."*

Two causes, and separating them matters because only one is a rendering
problem:

- **A defect, found by rendering a second journey to compare.** The entry
  gates report requirements *cumulatively* — each rung's list contains every
  earlier rung's. Rendered literally, "The idea is written down" appeared on
  all eight rungs and the stages read as identical. Fixed: each rung now shows
  only what it **added** over the one before it. `time-awareness` now reads as
  a story — risks sized at Scoped, solution designed and signed off at Spec'd,
  contract written and broken into 11 pieces at Built, every piece checked at
  Proven.
- **The killer risk, confirmed by looking at it.** Tony's own hypothesis was
  right: the artifacts he expects at each rung — diagrams, an evaluation
  matrix, research, a high-level architecture diagram — do not exist for any
  item in this repo. The page is honestly showing that. This is the empty-
  sources risk from the product doc, observed rather than predicted, on the
  first artifact built under the frame.

### 3. Risks — right idea, too wordy

> *"Good, like this, but we can be punchier: Title (short), Impact: short,
> Likelihood: estimate or fact, Countermeasure: do we have one and what is it,
> Status: circle / triangle / cross."*

**Taken.** Five fields, tight. The status glyphs are the evaluation matrix's
own vocabulary — ○ meets · △ meets only with a countermeasure · × cannot meet
— which means the system gains **one symbol set** rather than two competing
ones. The eight-column ledger stays as the written record; the page renders
five of its columns, compressed.

Note carried from the render: an accepted-unknown row has no countermeasure by
definition, and the page showed "— none —". That is correct and should stay
visible under △/×, not softened.

### 4. The ladder is the page

> *"All the spec, proven etc. should be inline to the stage ladder/rung, not
> separate."*

**Taken.** The ladder is not one section among several — it is the spine, and
per-rung content belongs inside its rung. Combined with note 2: each rung
carries its own status, its steps with a light each, and links to what that
rung actually produced.

### 5. What we considered and threw away — off the page

> *"Don't think we need this. It's planning, design etc. — we work on that
> together, we don't need to track it in the visualisation."*

**Taken, with one distinction recorded so a later reader does not
over-apply it.** The *view* is cut; the *artifact* is not. "What we ruled out
and why is its own artifact" remains a standing decision from 2026-08-03, and
`switch-fidelity` names it as one of seven things that must not be lost. What
Tony ruled out is showing it on the wall — it is worked through in
conversation, not monitored. Cutting the record would be a different decision
and was not made.

### 6. The drawing is the alignment gate, not decoration

> *"The visual at the start of the page forces alignment. If we don't agree on
> that drawing we won't agree on the solution."*

Tony, 2026-08-07, and it settles what an undrawn head means. The drawing is not
a nicer presentation of text that already exists — it is the thing that makes
disagreement visible early enough to be cheap. Prose lets two people read the
same sentence and picture different systems; a diagram does not.

Consequence, taken: an undrawn panel no longer renders as a soft grey note. It
renders as a blocker — "not drawn, so this is not agreed" — because everything
agreed below an unagreed head is softer than it looks.

Measured the same day: **all three journeys rendered so far have no drawing at
all.** So alignment has never actually been forced at the head of any of them,
including the two that are done. That is not a rendering gap; it is a real one,
and this note is the first time it has been named.

### 7. Every stage is agreed by a drawing, not just the head

> *"And that is true for each stage on the funnel — a diagram or drawing can
> secure alignment before the next stage."*

Tony, 2026-08-07, generalising note 6. The head's drawing agrees the *problem*;
each stage's drawing agrees *that stage's output* before the next one opens.

This turns an existing standing decision into a special case. "Design is agreed
in diagrams, not prose" (2026-08-02) was recorded as a fact about the design
rung specifically. It is not — it is the general rule, and design was simply
where it was first noticed. Every stage has the same failure mode: two people
read one sentence and picture two different things, and the divergence is only
discovered downstream where it is expensive.

Taken: every stage carries its own drawing slot,
`docs/plans/journey-<slug>-<stage>.svg`, embedded in the stage card. A started
stage with no drawing renders as a blocker — "not drawn, so this stage is not
agreed". Not-started stages are silent, because there is nothing to agree yet.

Consequence not yet paid: **no stage of any journey has a drawing today.** Under
this rule every completed journey in the repo passed its stages without the
thing that secures agreement. That is a real finding about how the work has been
done, not a rendering gap, and it is the second one this page has surfaced by
being honest about what is absent.

## Open at design

- **Where a drawing lives.** Blocks note 1, and therefore the head of every
  journey page. Every other field is derived; this one cannot be.
- **Whether a rung shows its empty slots.** If Idea should show "diagrams,
  eval matrix, research", the page must decide between listing those slots as
  missing (making the gap visible from across the room) and showing only what
  exists (keeping the page clean but silent about what was skipped).
- **The architecture diagram** (product doc gap 3) has no prior art here and
  three altitudes to reconcile — conceptual, physical, stack. Tony has offered
  further examples; the frame for it should start from those.
