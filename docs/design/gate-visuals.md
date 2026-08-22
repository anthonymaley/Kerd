# Gate visuals — design

The design package for `docs/product/gate-visuals.md`. Frame, viability and
slice all pass; this is the design rung.

**Its own drawings are in `docs/design/gate-visuals/`**, and they are the
argument — this file is what a drawing cannot carry.

## Grounding

- `docs/design/talk-formats.md` — the narrative layer this composes with
- `docs/design/diagram-toolkit-spike-findings.md` — the spike that made a
  drawing affordable, and the operator rule that governs every one here
- `docs/design/diagram-types-by-rung.md` — the type-to-rung map
- `docs/design/requirement-shape.md` rule 9 — the fingerprint recipe reused
  unchanged

## The two settled mechanisms

### 1. The life of a gate visual

![the life of a gate visual](gate-visuals/visual-lifecycle.png)

`DRAWN → LOCKED → edited → DRAWN` is the requirement lifecycle, unchanged.
The only addition is `REDRAWN`, which takes a fingerprint from what was actually
built and compares it to the one that was agreed.

**`DIVERGED` is a question, not a fault**, and it has two exits because which
side is wrong is the thing being decided — the design may stand and the build be
fixed, or the design may have been wrong and need editing and re-approving.
Tony, 2026-08-22: *"yes conductor or composer can validate and decide and if
not, bring the producer in to decide."*

**Its firing frequency is the measurement.** *"If requirments are correct and
visuals are approved then it shouldnt happen."* Same rule as the promotion beat:
a well-run item never trips it, so an item that trips it often has a broken
process upstream rather than a noisy check.

### 2. What the design gate refuses

![what the design gate refuses](gate-visuals/design-gate-check.png)

Three questions, and **every one is a count rather than a judgement** — which is
`R-0051`, already approved: a check binds on countable facts produced outside the
model and never rests on a question the model answers about itself.

The escape hatch is `R-0048`'s shape: a declared aspect marked `n/a` with a named
reason owes no drawing. Skipping stays possible and stays visible.

## The vocabulary — ADOPTED from ISO/IEC/IEEE 42010, 2026-08-22

Tony asked what an aspect actually is: *"elements, features, processes, tools
systems?"* The honest answer was that the word was doing too much work — the
frame's table mixed a **database** (a part), a **lifecycle** (behaviour) and
**permissions** (something true across parts) without noticing they are not the
same kind of object.

**They never needed to be.** The architecture-description standard already has
this vocabulary, and its completeness rule is the design gate word for word:

| 42010 | Definition | What we were calling it |
|---|---|---|
| **concern** | *"a matter of relevance or importance regarding an entity of interest to a stakeholder"* | aspect |
| **viewpoint** | *"the set of conventions for the creation, interpretation and use of an architecture view, to frame one or more concerns"* | diagram type |
| **view** | *"a representation of the architecture from the perspective of a particular viewpoint"* | the drawing |

> **"Each identified concern must be framed by at least one viewpoint so that
> all identified concerns are covered."**

That sentence is this design's first gate question. **ADOPTED whole** — the
vocabulary and the rule — rather than invented, which is Law 4's third step
before its fourth.

**Why a concern is deliberately not a kind of thing.** It is whatever matters to
someone about this work. That is why the list resists being a taxonomy of parts,
and why trying to make it one produced a mixed table. A diagram type is a
*viewpoint* precisely because it carries conventions — which is also why the
spike's operator rule holds: obeying a type's layout rules is not style
compliance, it is what makes the drawing a view of something rather than a
picture.

**And it settles the closed-list question differently than this design first
proposed.** 42010 has no universal taxonomy of concerns, because concerns come
from stakeholders. So **the list is declared per work item**, which is exactly
the mechanism below.

Sources: [42010 conceptual model](http://www.iso-architecture.org/42010/cm/) ·
[arc42 on 42010](https://quality.arc42.org/standards/iso-42010)

## Where the aspect list comes from — DECIDED 2026-08-22

The load-bearing question the second drawing deliberately did not answer: if a
work item declares its own aspects in free text, the gate degrades back into a
judgement.

**Tony's answer:** *"does the conductor / composer decide before design based on
the work and agree with producer?"* — yes.

```
  conductor or composer reads the work
        │
        ├── proposes what it touches          the analysis is the model's
        │
        ▼
  the producer agrees the list                the key is his
        │
        ▼
  THE AGREED LIST IS THE DECLARED TRUTH       and the design gate counts
                                              drawings against it
```

This is the contract rung's own rule — *measured against an upstream
declaration* — arriving one rung early, which is what makes the design gate
countable at all.

**Superseded by 42010, same day.** This design first argued the concern list
had to be a closed vocabulary, on the reasoning that an unmappable concern owes
no drawing and so skips the gate silently. The standard answers it better:
concerns are declared per work item and **agreed**, and the gate counts views
against *that* declaration rather than against a universal list. An invented
concern is caught by the agreement, not by a vocabulary — and a closed list
would have been wrong anyway, since it would forbid a project from caring about
something we had not thought of.

What survives from the original argument is the escape hatch: a declared concern
either owes a view or carries a written reason it does not.

**The frame's sixteen-row table stops being a closed list and becomes what it
always actually was: the mapping from a common concern to the viewpoint that
frames it.** Its seventeenth row still has no viewpoint — see the open question
below.

## Open questions

1. ~~**The UI aspect has no type.**~~ **Answered 2026-08-22 by the
   standards-grounding spike, and it is a named build, not an open question.**
   None of the 39 draws a screen — no wireframe, no layout, no navigation map,
   no component hierarchy. Tony named UI alongside database and architecture,
   so this is a gap in a common case, not an edge. Law 4's first three steps
   ran: ISO 9241-210 (read in full) establishes *that* the UI concern belongs
   on the list — its Table 1 names personas, scenarios, prototypes and a UI
   specification as output categories — and supplies a drawing convention for
   none of them; it says in its own text it provides no methods. No ISO
   standard defining a wireframe or screen-layout grammar exists. So steps four
   and five remain: **the UI viewpoint is built**, borrowing notation from
   design practice, as its own item. Until it lands, a design whose agreed
   concerns include UI cannot pass this gate — which is the gate working, not
   a hole in it. (`docs/design/standards-grounding-findings.md`)
2. ~~**Where the agreed aspect list is stored.**~~ **Answered at contract,
   2026-08-22: the product doc's front matter.** `docs/product/<slug>.md`
   carries a `concerns:` list — one entry per view: concern, viewpoint,
   view path or `n/a — <reason>`, approval — read by the design rung of
   `tools/gates/kit.py`; `gate.py seal <slug>` completes a hand-written
   approval with rule 9's fingerprint over the `.html`. Schema and rows:
   `tools/gates/README.md`, Views.

## What this design does NOT do

- **No new approval machinery.** A visual's fingerprint is `requirement-shape.md`
  rule 9, unchanged, over the drawing's content instead of a block's.
- **No board.** Build's visual is derived from disk and therefore cannot be
  approved — nobody authored it, so there is nothing to agree to. Named so nobody
  later "fixes" this by making a fact approvable.
- **No evaluation matrix.** Ours already, machine-checked since v0.77.0.

## The limit, stated

**Nothing here checks that a drawing is a *diagram* rather than a slide.** Both
of this package's own drawings passed the source linter; one of the two earlier
ones passed it, rendered perfectly, and was still prose in rectangles — the
producer's verdict, *"text on the screen with box that made no sense to the
subject"*.

There is no machine check for *does this box mean anything*. The gate can count
that a drawing exists, that it is approved and that it has not changed. It cannot
count that it was worth drawing. **That is the producer's key doing work no
fingerprint can do**, and it is the same declared limit as reachability: the
check proves the artifact is there, never that it was understood.
