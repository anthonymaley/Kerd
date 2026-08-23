---
route: new
stage: designed
---

# Design GO — funnel-driver, 2026-08-23

**Clock:** 2026-08-23 17:14 EDT

Design approved — Tony's key, 2026-08-23 evening sitting, on the word *"go"*.
Package: `docs/design/funnel-driver.md` with three drawings beside it, all
sealed the same day: `why-an-umbrella` (`fp:54f84887b8b8`), `gate-loop`
(`fp:47883502cf4b`) and `span-vs-slice` (`fp:5adeb340c7ee`).

**The third view was drawn at this gate and is why the GO waited.** The first
two were sealed at midday, before the item-versus-session formulation existed.
Asked for the GO, the producer's answer was *"hmmm i need one of your diagrams,
this is important"* — and the drawing that followed made the architecture
argument countable rather than asserted: a work item is a horizontal span across
many sittings, a session is a vertical slice across several items, and the two
are perpendicular. Nesting one inside the other is a category error, not a
preference. Declaring the concern dropped the item design → slice; sealing on
his approval (*"great diagram. yes agree"*) returned it. Third live firing of
the view lock.

**What the GO covers beyond the drawings** — three calls made at the design rung
by the model and ruled on here:

1. **Drive invokes `/kerd:conductor` through the Skill tool** with a task framed
   from the work record — the same invoke pattern conductor already uses for
   `/kerd:switch out`. Conductor is unchanged and does not know where the task
   came from. Build check: a diff on `skills/conductor/SKILL.md` in any Drive
   slice is a refusal, not a review comment.
2. **The question set lives in the work record** as `## Question set`. The work
   type's set at `docs/work/question-sets/<work-type>.md` is a seed, copied in at
   intake and never read again.
3. **The completeness check counts** answered entries against declared entries in
   the same section. It never judges whether an answer is good — that is the
   human key at the gate.

**The machine key is met at four of five, and the fifth is a declared gap rather
than an invented target.** *Standing decisions contradicted by shipped skill
text: 1 → 0* is the unconditional plan gate, which lives inside conductor; the
umbrella rule forbids touching it, so Drive cannot close it. Recorded as a named
gap. This is deliberately the opposite of what `gate-visuals` did at its own
design rung, where a `Product measurements met` row had no upstream declaration
to read from.

**Two decisions ride into this GO and are recorded in CONTEXT.md rather than
here.** The umbrella is named **Drive** (`/kerd:drive`, `skills/drive`); the slug
stays `funnel-driver` because slugs name work items, not skills. And
`project type` is **superseded as written and retired as a field name**, split
into three independent axes — work type, route, and lifecycle position — with the
fifteen written types demoted from canon to migration evidence.

**Two following slices are named and measured rather than promised:** the
`docs/product` → `docs/work` migration (~180 references, 20-file move, and the
board derives every slug from `docs/product/*.md` filenames so a half-done
migration turns the render red), and the fifteen-type split.

Hands to CONTRACT.
