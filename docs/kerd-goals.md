# Kerd — the goals

**Source:** `docs/kerd-interview.md`, the reset interview with Tony, 2026-08-13.
Every goal below is grounded in a quoted phrase from that interview and nothing
else — no existing artifact, decision, or skill was consulted.

**Status: APPROVED BY TONY, 2026-08-13 18:30.** His word: *"approved"*. He also
added a second design input to G1 directly into this file in the same beat.
These goals may now be cited as settled by everything downstream, including the
still-open decision of whether to build Kerd or adopt something existing.

**Recorded because it is a defect worth not repeating:** the model asked for
approval three times without ever clearly asking him to *read the file* — *"didnt
see you ask for a reviwe of that file"*. An approval requested without an
explicit request to review is the same failure as an unreadable gate message
under G4: the ask cannot be acted on properly, so whatever comes back is worth
less than it appears.

**Tony, 2026-08-13 18:18, on what an approval gate has to be:** *"the process
demand approval or push back until approval, 'not yet keyed' suggests recored as
status and moved on"*. An approval that can be deferred by recording that it is
outstanding is not a gate. The process demands the answer; it does not note its
absence and continue.

*(Vocabulary note: this file previously said "keyed", which is the repo's own
jargon and not language Tony uses. It says approval now. Machine vocabulary in a
gate is the same defect as an over-technical gate message under G4 — it makes
the ask harder to act on than it needs to be.)*

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

## The laws — not goals, and not scored

Listed here rather than among the goals because they are obeyed, not achieved.

### Law 1 — Every project has its own repo

Kerd installs into a user's own project and operates inside that repository's
boundaries; the Kerd project never holds sessions for anybody else's work. Tony
raised this unprompted, interrupted his own answer to insist on it, and ruled on
it directly: *"the way i work, every project has its own repo, its non
negotiable."*

### Law 2 — Every change lands in the spec, the design, or the requirements

**Tony, 2026-08-13 18:15 EDT:** *"so each change should result in a chnage to
spec or design or requirement"*

Stated while sharpening G3, but it is not a fine-tuning rule — it is universal.
Nothing changes in the artifact without the governing document changing with it.
This is the anti-drift law, and it is what makes the other goals mean anything:
G2's promise that nobody has to guess holds only while the documents are true,
and G6's *"should not look different or behave differt fromt he agreed spec"* is
empty once the spec has drifted from what exists.

**Tony, immediately after:** *"but doesnt have to be huge process"*

**Which resolves the obvious objection, and resolves it better than the model's
version of it.** The model's straw-man was that enforcing this on trivia
manufactures the overhead G3 exists to prevent — so there must be a threshold
below which the law does not apply. There isn't one. **The law is absolute; the
ceremony is proportionate.** Every change updates its governing document; for a
small change that update may be one line and a quick confirmation.

The scaling dial is on the *process*, never on *whether the document stays
true*. That distinction is what keeps Law 2 from decaying into "significant
changes only" — a judgement call, and therefore a hole.

### Law 3 — Check your own work before it counts

**Added by Tony 2026-08-13 22:39**, resolving the fact that the self-check
ladder was approved content with no status — requirements could only trace to a
*section*, which bent Law 2 as applied to this document. His ruling: *"self
checking can be a law"*.

The law, in his words: *"check your work, use self analysis, askyourself is this
correct?, use a straw man to explain your work and see if there are gaps, use an
agent in advesrial review to challenge your thinking where appropraite."*

And a named set of simple questions the work has to survive:

- **"did i infer that"**
- **"did i read from file or stale memory"**
- **"have we tried this before"**
- **"has this already been answered or recorded"**

Those four are worth their own line because each names a specific way confident
output goes wrong: inference dressed as knowledge, a stale recollection standing
in for a read, repeating a dead end, and re-deriving something already settled.

**Two dimensions of checking, both required** — the second added at the same
moment (*"we should ask what is absent. we should also compare to what best
practices do, other skills, standard methodologies, emerging thinking in AI human
pairing process"*):

- **Inward** — is what is here correct, and **what is absent?** The omission pass
  exists because self-criticism structurally audits only what made it in. Proven
  live 2026-08-13: the requirements straw-man attacked five things it had
  written and missed three things it had never written; an independent reviewer
  found all three.
- **Outward** — how does this compare to best practice, other skills, standard
  methodologies, and emerging thinking in AI-human pairing? Measuring the work
  only against our own stated intent cannot detect that the intent itself is
  behind the field.

*Wording drafted by the model from his ruling and his content; the ruling and the
content are his, the phrasing is not yet confirmed.*

### Law 4 — Learn from what exists before designing anything

**Added by Tony 2026-08-14 08:35, verbatim, and it governs every aspect of the
project:**

> we always need to 1. assess and learn from industry standards, leading
> approaches, emerging approahes 2. decide what fits for us 3. consume/adopt
> whole if perfect  or be inspired by them, 4. design or adapt for our gaps 5.
> build for the gaps.   do this for every aspect of our project

**The five steps, in order:**

1. **Assess and learn** — industry standards, leading approaches, emerging
   approaches.
2. **Decide what fits us.**
3. **Consume or adopt whole if it is perfect** — otherwise take inspiration.
4. **Design or adapt** for what is left.
5. **Build for the gaps** — and only for the gaps.

**Build is what remains after adoption and adaptation, never the starting
point.** His earlier framing was the principle — *"we should consume what we can
and build the differentitor but never at the cost of meeting our goals or
quality"*; this is its method. His own image for it: *"lets not invernt fire to
make meal, lets turn on the stove to cook one."*

**Why it is a law and not a preference:** step 1 is the only step that can reveal
an approach we have not conceived. Skipping it means every design is bounded by
what the two of us already imagined, and neither of us can see that boundary from
inside. This is Law 3's outward dimension applied *before* the work rather than
as a check on it.

**Cost, stated rather than hidden:** it front-loads research onto everything, and
it will feel slow at the start of each aspect. The proportionality of G3 applies
— the depth of step 1 scales to the weight of the aspect — but *skipping* it does
not scale down to zero, or the law is a preference again.

**And the second half, added 2026-08-14 08:36:** *"dont just assume we are
correct unless an explicit requirement states this is the only way"*.

**Our own conclusions are not privileged.** Agreeing something between us does
not make it right, and having written it down does not either. The only thing
that licenses skipping step 1 is **an explicit requirement stating this is the
only way** — a stated constraint, not a shared assumption and not a preference
either of us holds strongly.

This closes the loophole the law would otherwise have: without it, "we already
decided that" becomes a reason not to look, and the boundary of our imagination
becomes the boundary of the design. Two people agreeing is the weakest evidence
in the system, not the strongest — the repo has already measured this once, on
2026-08-08, when three independent agents agreed on eight category moves and six
attackers killed five of them.

**It indicts work already done.** The goals in this file and the requirement
shape in `docs/design/requirement-shape.md` were both drafted from Tony's words
alone, with no step 1. He caught that himself: *"dont just take 'he asked for
them' as fact that is the best way."* Provenance is not justification.

### Law 4's ordering rule — the analysis outranks what was said before it

**Tony, 2026-08-14 13:10:**

> so we need to understand that you interviwed me before you did the analysis,
> if the analysis proved a better way, then we go agaist what i said before, we
> chnage the rule

**An interview held before the research is evidence about intent, not a
constraint on the answer.** Where step 1 finds a better way, **the earlier
statement yields — including his own, and including anything already written
down as a requirement.** The rule changes; the finding stands.

**Why this needed saying out loud:** without it, every pre-research statement
becomes untouchable simply by having been recorded first, and Law 4 collapses
into decoration — we would research diligently and then be forbidden to act on
what we found. It also removes the temptation to quietly reinterpret an old
statement until it agrees with new evidence, which is the dishonest version of
the same move.

**He had already done this twice to himself before stating it as a rule**,
which is what makes it credible rather than convenient: he withdrew
`DRAFT / ACCEPTED / FINAL v1.0` as *"my thinking without research"*, and again
as *"already discounted"*.

**And the superseding must be visible — Tony, 2026-08-14 13:11:**

> if wer agree a better way then we superseed and strike off prior comments for
> sure. otherwise we go in loops

**Striking off is not tidiness, it is the loop-prevention mechanism.** A prior
statement left standing beside the thing that replaced it is an invitation to
re-argue a settled question — and the decision-record literature names exactly
this failure, where a settled matter is re-litigated because nobody can tell
what is still live. He arrived at it independently and stated the consequence
himself: *"otherwise we go in loops."*

So a superseded statement is **struck, in place, with what replaced it named**
— never silently deleted, and never quietly left alive. Both failures produce
the same symptom later: a reader who cannot tell which of two statements
governs.

**What it does NOT license.** This governs statements superseded **by
evidence**, never by preference, convenience, or a model finding an earlier
ruling inconvenient. The bar is that step 1 *proved a better way* — and the
superseded statement does not vanish. It goes to the graveyard, killed by
**analysis**, with what was learned recorded, exactly as his graveyard ruling
requires. A rule that changes without leaving a body is indistinguishable from
drift.

---

## G1 — We trust what we're building

From idea to launch, what is being built is what was agreed. New solutions never
appear inline without the agreed steps; *"just make that change"* never happens.

**Design input, his words:** *"strong visuals and specs for approval so we are
clear with each other"*

**Second design input, added by Tony directly into this file, 2026-08-13
18:30:** *"a user never feels overwhelmed by the process"*

This is a distinct requirement from G4's false approval, though they share a
cause. G4 is about a single message being unreadable. This is about the
*cumulative* weight of the process — a user can understand every individual step
and still be worn down by how many there are. A process that is clear at every
point and exhausting in aggregate fails G1 even though no single gate failed.

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

> ⚠ **SUPERSEDED THE SAME EVENING — 2026-08-13 22:39.** He closed this: *"fine
> tunes move the way everything else does, just faster, assuming they dont break
> the specs etc."* **Not a separate process — the same path, traversed faster,
> conditional on the specs holding.** The paragraph below records the state
> before that ruling and is kept for the record only.
>
> *This line was stale for fourteen hours and a composer read it as current,
> reproducing an answered question as an open one. A Law 2 violation in the file
> that carries Law 2 — found by the fidelity audit of 2026-08-14, not by us.*

Two candidate designs were floated in his words and **neither was chosen**: a
dedicated process for fine tuning, or rapid traversal of the normal path from
first step to last. That choice is design work.

### What decides a change is a fine tune

**Tony, 2026-08-13 18:22, verbatim:**

> have we already built the item and are looking to change it? does the change go
> agaist the spec or design or requirment? how much effort or impact is the
> change, how critical is the chage, are users blocked or having poor experience?
>
> the composer or conductor roles (if we keep them) should have the approval

**The classifier is a set of questions, not a size threshold:**

1. Have we already built the item and are we changing it?
2. **Does the change go *against* the spec, design, or requirements?**
3. How much effort or impact does it carry?
4. How critical is it?
5. Are users blocked or having a poor experience?

**Question 2 is the discriminator**, and it resolves what looked like a
contradiction earlier. Every change *lands in* the spec (Law 2) — but that is
not the same as going *against* it. A font choice the spec left open is filling
detail in: fine tuning, recorded. A font change that contradicts what the spec
says is a change to the agreement, and it goes the long way round with the
agreement's owner. Question 5 admits urgency as a legitimate input: users
blocked or suffering is grounds to move.

**Who approves a fine tune:** *"the composer or conductor roles (if we keep
them) should have the approval"* — not the producer. The agent roles hold
approval for this class, which is what makes the fast path fast when the spec's
owner is not in the room.

**Straw-man, unresolved:** this puts classification *and* approval in the same
hands. If the conductor decides a change is a fine tune and also approves its
spec update, the producer is out of the loop for a class of changes the
conductor itself defines — and the cheap path is the one the model is under
standing pressure to pick. Nothing here yet separates those two authorities.
The self-check ladder (critical work draws an adversarial reviewer) is the
nearest available countermeasure but has not been assigned to this.

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

**What triggers each tier — answered by Tony, 2026-08-13 18:18:** *"doing a
thing, check it yourself, doing a bigger thing, strawman, doing a critical
thing, get adveserial model to check"*

| The work | The check |
|---|---|
| Doing a thing | Check it yourself |
| Doing a bigger thing | Straw-man it |
| Doing a critical thing | Adversarial model checks it |

So the trigger is the **weight of the work**, not the stage it sits in and not
a cost budget. The ladder is staffed the same way production is — the check
gets the effort the work deserves.

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
2. **What evidence settles build-vs-adopt, and who takes the decision?** Q4 is
   explicitly open. The prior evaluation in this repo is to be re-examined as
   evidence, not treated as precedent.

**Closed 2026-08-13 18:18:**

- ~~*Does adoption by others count?*~~ **Yes** — *"adoption by other yes
  important"*. Kerd being used only by Tony is a failure against G8.
- ~~*What triggers each tier of the self-check ladder?*~~ **The weight of the
  work** — see the ladder table above.
- ~~*Effort against meeting the requirements*~~ — already answered by *"never at
  the cost of meeting our goals or quality"*; effort is a constraint on how, not
  on whether.
