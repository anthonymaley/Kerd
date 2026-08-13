# Kerd — the goals

**Source:** `docs/kerd-interview.md`, the reset interview with Tony, 2026-08-13.
Every goal below is grounded in a quoted phrase from that interview and nothing
else — no existing artifact, decision, or skill was consulted.

**Status: DRAFTED BY THE MODEL, NOT YET KEYED BY TONY.** Nothing here is binding
until he has read each goal, corrected it or confirmed it, and keyed it.

## How to read a goal — corrected 2026-08-13 18:06

A goal here names a **failure to be prevented by construction**, and it carries
a **design input** — the thing baked into the process so the failure cannot
happen. It does **not** carry a metric.

The first draft of this file gave each goal a measure, mostly a count of
failures trending to zero. Tony rejected that: *"these are not measurement,
these are inouts to design to avoid what those g1-g8 from happening, they cant
be measured."* Counting occurrences after the fact is the wrong instrument —
by the time you are counting false approvals, the process already permitted
them. The design inputs below are his words, quoted, one per goal.

**A straw-man of the rejected version, kept because it shows why the correction
matters:** four of the eight measures (G1, G2, G4, G7) counted only the absence
of a failure, so a system that produced nothing at all would have scored
perfectly on every one.

## The law — not a goal, and not scored

**Every project has its own repo.** Kerd installs into a user's own project and
operates inside that repository's boundaries; the Kerd project never holds
sessions for anybody else's work. Tony raised this unprompted, interrupted his
own answer to insist on it, and ruled on it directly: *"the way i work, every
project has its own repo, its non negotiable."*

It is listed here rather than among the goals because it is obeyed, not
achieved.

---

## G1 — We trust what we're building

From idea to launch, what is being built is what was agreed. New solutions never
appear inline without the agreed steps; *"just make that change"* never happens.

**Design input, his words:** *"strong visuals and specs for approval so we are
clear with each other"*

**Grounded in:** *"a robust but quick and clear and concise visual process that
allows us to trust what we're building"* · *"This will stop the inline new
solutions happening without all the appropriate steps being taken"* · *"Hey can
we change this skill to do this thing the way I like it? Just make that change.
That's verboten."*

## G2 — Nothing we've learned is ever lost, and nothing is guessed

We can work on a project forever without losing what we gained along the way.
When knowledge is needed we go and get it, and Tony never re-explains something
already settled.

**Design input, his words:** *"agents should not guess or infer from memory
something, they should never have to, we shoudl ensure the spec has those memory
items in the work"*

The sharp part: the countermeasure is not a better memory search. It is that
**the spec carries the memory items the work needs**, so the agent is never in
a position where guessing is even available to it.

**Grounded in:** *"a way to work together on a project forever without losing the
knowledge that we've gained along the way"* · *"We don't guess. We go back to the
desk to get that knowledge"* · *"You should instinctively know or know how to
know about what we're talking about"* · *"feel safe that the effort is not lost"*

## G3 — One path, sized to the work

The path from idea to launch is walked the same way every time — no small-work
exception, no skipped stages — and yet a small clear change never costs an hour
of process. A stage whose inputs are already clear passes instantly; a stage
whose inputs are missing stops and gets them instead of inventing them.

**Design input, his words:** *"the process should allow and recognize and
understand for small changes without breaking the process or cirumventing it.
example. color or text change or spacing chnage on app, this is fine tuning, so
maybe we have a process that handles this aspect or we need to be able to
quickly advance from step 1 to step 8 to make those changes and not havea huge
overhead to make them but also not let these small changes break the design spec
or the archtecure or requirments without agreed change"*

**The mechanism this names is classification, and it comes with its own guard.**
The process must *recognise* small work as a class — he calls it **fine
tuning** — and let it move without either breaking the process or circumventing
it.

**The guard, sharpened by Tony immediately afterwards:** *"imagine for g3 if the
design spec designer saw his font being changed without his approval....."*

A font **is** the design spec. So the fast path is not "fine tunes avoid the
spec" — it is:

- A fine tune **still lands in the spec** and still gets the agreement of
  whoever owns it. The speed comes from the approval being *proportionate*, not
  from it being skipped.
- The spec stays **the truth**. An artifact that changes without the spec
  changing with it is silent drift, and enough of it leaves a spec describing
  something that no longer exists.

The failure being prevented is not slowness. It is a spec quietly becoming a
lie — which would also defeat G6, since "does not look or behave differently
from the agreed spec" means nothing once the spec has stopped being accurate.

Two candidate designs are floated in his words and **neither is chosen**: a
dedicated process for fine tuning, or rapid traversal of the normal path from
first step to last. That choice is design work.

*Superseded:* the model's earlier "stages satisfied, not performed" reading was
invented to serve this goal. It survives only where it agrees with the input
above — the input is his and the reading was not.

**Grounded in:** *"My two minutes or four weeks, it doesn't matter... We do it
the same way"* · *"Hey, can we change the font on the screen?... It doesn't take
us one hour to go through a process"* · *"i dont mind robust, i just mind
overhead and overwork"* · *"if we can agree quickly and it aligns to the existing
requirements and architecture and its clear what to do.. go!"*

## G4 — Every approval is real

When Tony says "approved" it is because he read it, mapped it, and meant it —
never because the message was too long or too technical and agreeing was easier
than admitting it lost him.

**Design input, his words:** *"Clear communication, questions and requests,
visual confirmations, status etc vs wall of noise text and an 'approve?'"*

**Also his, as a presentation rule:** *"when we ask for inout, put a flag or
ascii border aroud the questions to ensure users dont think its noise."*

**Grounded in:** *"what i really dont want is a super verbose complex technical
response or questions that lose the audience and results in 'sure' or 'approved'
becuase the user feels dumb or cant read all the text"* · *"then approve or
change, or even coach them to the answer"* · *"brevity is good as it shows we
understand, but not explaining properly or too technical can result in the wring
agreements"*

## G5 — In control the whole time, with nothing hidden

At every moment Tony can see where we are, what's next, what has been made, and
what the tool itself can do. Nothing is a black box, and no capability exists
that he doesn't know exists.

**Design input, his words:** *"show the work, show the state, show the tools
being used"*

**Grounded in:** *"feel in control the whole time"* · *"Where are we in the
journey? What's happening next? What content or artifacts have we produced and
can I view them?"* · *"its not clear what or why its doing in a black box way"* ·
*"the visual control should explain the process and the capablities too. nothing
you dont know exists"*

## G6 — The outcome is launchable, exactly as expected

When something is ruled done it is genuinely ready — releasable to customers,
sendable to a client — and it is exactly what was expected.

**Design input, his words:** *"we have a spec and the measurement of done is
clear, should not look different or behave differt fromt he agreed spec"*

Note what this demands: the agreed spec covers **how it looks and how it
behaves**, and the build is checked against it *while it runs* — *"design UI/UX
etc needs to be part of the pre build and measurable by the model during build"*.

**Grounded in:** *"ready for use to react to and approve as done or not"* · *"the
results are professional and complete"*

## G7 — No wasted effort, no degraded ideas

Effort and cost match the work: nothing is over-built or done for the sake of
it, and cheaper help never dilutes the thinking.

**Design input, his words:** *"never sumarize memories or requirments or
achievements etc"*

This is a harder rule than it looks. Summarising is the default way a model
economises, and it is exactly how a requirement quietly becomes a paraphrase of
a requirement. Fidelity outranks compression everywhere these three kinds of
record are concerned.

**Grounded in:** *"make sure we're not wasting tokens by using the correct model
and using the correct effort"* · *"we're using the best models to design and own
the actual solution so we're not degrading ideas"* · *"we shouldn't be overly
building and testing without checking to see what comes next"*

## G8 — Build something valuable that people actually want

**Design input, his words:** *"build something valuable that there is a need for
that does a thing that people want and can use easily without deep knowledge"*

This input reframes the goal. The first draft made G8 *"worth choosing over what
exists"* — a decision about whether Kerd should exist. His input makes it an
outcome the thing must achieve: real need, real want, usable **without deep
knowledge**.

The build-or-adopt decision remains open and is recorded in the interview as
Q4, but it is a decision to be taken, not this goal.

**Grounded in:** *"Do we stick with superpowers? Is it perfect or do we build
this?"* · *"superpowers does some great things... so we can learn from it, i just
want the process to be ours and visable"* · *"we should consume what we can and
build the differentitor... but never at the cost of meeting our goals or
quality"*

---

## The self-check ladder

Named by Tony as critical steps in the process, not as conduct advice. Three
mechanisms, graded cheap-and-frequent to expensive-and-rare:

1. **"Are you sure?"** — occasional, lightweight, the model challenging its own
   claim in passing.
2. **Self-reflection and straw-manning** — the model examines its own reasoning
   and argues against its own proposal before presenting it.
3. **Formal, optionally adversarial review** — an independent subagent at a
   sized model and effort, *"baked in"*.

**His reason, which is a precise diagnosis rather than a preference:** *"many
times if i ask you 'is that true' or 'explain that' you see a flaw in your work,
but if its not asked you wouldnt see. so these mechanisims are important to help
you review and not just produce as done."*

The flaw is **already visible** to the model; what is missing is the prompt to
look. So these mechanisms supply a trigger, not a capability — which is why
baking them in works at all, and why relying on the model to remember to do them
would not.

Whether the tiers fire by stage, by risk, or by cost is a design question and is
not answered here.

---

## Tensions

Real pulls between goals, named and deliberately not resolved. Resolving them is
design work.

1. **Speed against quality (G2 vs G3).** Handovers *"should be really fast and
   clear but they should wait on quality, not speed"*. His ordering is quality
   first, then as fast as possible — but where the line sits is undecided.
2. **Brevity against false approval (inside G4).** Brevity signals
   understanding; under-explaining causes wrong agreements; over-explaining
   causes rubber stamps. Tony named this himself: *"we need to find a way to
   communicate that solves for this."*
3. **One unvarying path against the two-minute change (inside G3).** The stages
   never vary, yet a font change must not take an hour. G3's design input
   assigns a resolution — recognise fine tuning as a class, guarded by "may not
   change the spec, architecture or requirements without agreed change" — but
   *how* that is delivered is undecided between a dedicated fine-tuning path and
   fast traversal of the normal one.
4. **Consume-before-build against owning the process (G8 vs G1/G5).** *"we
   should consume what we can and build the differentitor"* against *"i just
   want the process to be ours and visable"*. Bounded by *"never at the cost of
   meeting our goals or quality"*, but no individual case is settled.
5. **Token economy against never degrading ideas (inside G7).** Every delegation
   decision sits inside this pull — and G7's own design input forbids the
   cheapest economy of all, summarising.

## Open questions

1. **Which shape does fine tuning take?** G3's input floats two and chooses
   neither: a dedicated process for fine tuning, or rapid traversal of the
   normal path. Also unstated: what decides that a change *is* a fine tune, and
   who makes that call when it is borderline.
2. **Who is "someone else", and does adoption count?** *"Many people should
   install this"*, and G8 now requires real need and real want — but whether
   Kerd fails if only Tony ever uses it is unstated.
3. **What evidence settles build-vs-adopt, and who takes the decision?** Q4 is
   explicitly open. The prior evaluation in this repo is to be re-examined as
   evidence, not treated as precedent.
4. **What triggers each tier of the self-check ladder?** By stage, by risk, by
   cost — unanswered.
