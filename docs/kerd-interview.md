# Kerd — the reset interview

**Started 2026-08-13 17:05 EDT.** Called by Tony after a session framed two
solutions in a row and neither party could say whether what exists serves the
goal. His words: *"honestly i feel we are lost here, i have no clue if what we
have build and what the requirments will build is what we need now. the fact
that we are both confused tells me we need a reset."*

**The operating rule for this document:** nothing here is grounded in what
already exists. Not the register, not the board, not the standing decisions, not
any shipped skill. Tony's words are captured verbatim and are the record; the
model does not paraphrase, summarise, or reconcile them against the repo. His
instruction: *"we need to go back to this interview level and not be confused by
any existing knowledge until we capture this as the source of truth."*

Once captured and keyed, **this file is the source of truth** and everything
that exists gets checked against it — not the other way round.

---

## Q1 — What are we building?

**Tony, 2026-08-13 17:05 EDT, verbatim:**

> We are building a skill that will take us from an idea through to the launch
> of an idea. It could be:
> - a product
> - a document
> - a business idea
> - a code project for enhancing something that exists
>
> It doesn't really matter. Idea through a robust but quick and clear and
> concise visual process that allows us to trust what we're building and to make
> it perform incredibly well between human and agent
>
> We also want to make sure we have session memory and contextual memory
> transferred between sessions, and long-term memory of what we've spoken about.
> Right now we have Switch as a skill that works really well but we want to make
> it work perfectly. That's the basis of this skill and it's something we can use
> on its own just for non-conductor (as we call it). It can be anything when we
> design conductor sessions.
>
> The Switch in and Switch out is a super powerful GitHub-based session for:
> - long-term memory
> - context clearing
> - and restarting without losing any context memory

---

## The boundary — stated first, at Tony's insistence

Raised unprompted during Q2, with the instruction to *"Make that super clear
before we answer question two."*

**Tony, 2026-08-13 17:13 EDT, verbatim:**

> Let's make a very important point here: this is a skill that lives in people's
> repos, in their own projects. Kerd is the skill that can live there but the
> Kerd project should never have sessions for any of those other repos or
> projects. Many people should install this and use Kerd inside those projects
> and the boundaries within that repository, that project.

---

## Q2 — What does it have to do?

*Answered in two parts: first on roles and model economy, then the full
idea-to-launch walkthrough.*

**Tony, 2026-08-13 17:07 EDT, verbatim:**

> We also want the conductor role, if we keep that, to To make sure we're not
> wasting tokens by using the correct model and using the correct effort. We also
> control and delegate tasks to agents (sub-agents) of the appropriate level. We
> make sure we're using the best models to design and own the actual solution so
> we're not degrading ideas. If we use lower models, we always push it to the
> correct model

**Tony, 2026-08-13 17:13 EDT, verbatim — the walkthrough:**

> Question two: we start a session. It could be in an existing repo or a new
> repo, but we start with an idea or a request, maybe: "Hey I've got a new
> product. Let's figure out if it's viable." We go through ideation:
> - What is the product?
> - What is the idea?
> - How will it work?
> - Who are the competitors?
>
> Let's do analysis and make sure we understand and capture the requirements, or
> what will become requirements, in a way that we can use to measure the success
> of the next step, which will probably be validation or design. We go through
> that validation or design and make sure that we have everything we need. We
> know all of the goals, the measurements, what makes it successful, whether it
> already exists, and whether we should leverage other technology.
>
> All of that goes into an architecture design phase. It may not be technology.
> It could be, "Hey I want to write a book," but it goes into the next phase, and
> then the next phase, until we have everything the model needs to go and execute
> to build the thing.
>
> It should loop and measure itself against those goals and requirements, and
> design to make sure we build what we agreed we're going to build. That way we
> don't have to be in this constant back-and-forth conversation. We can do all of
> that upfront.
>
> It can take an hour, two minutes, or four weeks. It doesn't matter but we get
> to the point where we are super aligned on:
> - what we're going to build
> - how it has to work
> - what good looks like
>
> Then you just go and build it
>
> Now through all of that process, we need to keep the technical chat to a
> minimum unless that is what's being requested. If we're building a code project
> and a developer wants to use it and see the code, that's a conversation that
> can emerge. Mostly this is a guiding conductor hand that is making sure
> everything is thought through and it's clear what we have to build
>
> To do that we need to visualize each stage. Hey, this is the idea that I heard.
> Does this look right? This is back to how we visualize things in the Toyota
> skill sensei, which is one of my other skills. Very simple, very clear: here's
> the current view, here's the goal. Does that look correct? OK well at least now
> I know we're aligned on what we're trying to achieve
>
> Then we can also use the same thing for problems. Here's what I think is
> happening: we can visualize it.
>
> For the architecture we should have a hybrid diagram showing:
> - the architecture
> - the tech stack
> - the flow between them
> - where we're going to host that
> - the tools we're going to use
>
> All of that should be visualized in a very simple, easy-to-understand diagram
> that the user can approve. Boxes, not code
>
> We need some way to visualize the state:
> - Where are we in the journey?
> - What's happening next?
> - What content or artifacts have we produced and can I view them?
> - Reference numbers
>
> Maybe this is requirements management coming in. This feature: I've changed my
> mind. Even though we have a design, can we look at the impact of changing that
> now or does this go to the next release, the next version? We need to be able
> to manage that
>
> This will stop the inline new solutions happening without all the appropriate
> steps being taken

**Tony, 2026-08-13 17:16 EDT, verbatim — asked what is different between a
two-minute pass and a four-week one, after the model proposed that the stages
never get skipped and only compress:**

> No I agree with everything you say there. My two minutes or four weeks, it
> doesn't matter. How long does it take to capture the idea? I don't care if
> that's a two-minute thing, a four-hour thing, or a four-week thing. We do it
> the same way
>
> And we need to avoid. Hey can we change this skill to do this thing the way I
> like it? Just make that change. That's verboten. We cannot do that

**Settled by this answer:** duration varies, the path never does. The stages are
walked the same way every time; what changes is how long capture takes, not how
many stages there are. There is no small-work exception, and "just make that
change" is prohibited outright.

---

## Q3 — What does good look like?

**Tony, 2026-08-13 17:22 EDT, verbatim:**

> If this works, we have a way to work together on a project forever without
> losing the knowledge that we've gained along the way. The changes, what we
> built, what worked, and what didn't work: we have all of that knowledge and we
> refer to it in the appropriate way.
>
> We don't read the whole book of what we've done every session but we know how
> to find that and we don't just infer things. We don't guess. We go back to the
> desk to get that knowledge so that we know what we're doing.
>
> Now what does good look like in that situation? We have a new idea or a
> problem/enhancement and you release. We can instantly work on that together as
> if we are sitting across the desk from each other in a paired way. We can
> whiteboard together and share ideas back and forward but then we'll lock it and
> go, "Oh that sounds like what we're building. This is what it looks like. This
> is how we measure it. This is how it's going to work from an architecture point
> of view."
>
> Formalize all of those back-and-forth conversations into a spec that becomes
> measurable, linked to the goals and the requirements, and then we can build it
> together. That usually means you and the subagent are building that but I can
> see the progress and the artifacts as you make them. I can be clear that we're
> building the right thing and I can start planning the next release in my head.
> I never feel that you don't understand me when I speak.
>
> What I mean by that is we've already spoken about this and we've already agreed
> you understand me. You don't have to reinvent something, change your mind, or
> infer it. You should instinctively know or know how to know about what we're
> talking about. Switch-ins and switch-outs should be really fast and clear but
> they should wait on quality, not speed. We should make sure it's as fast as it
> can be without losing that quality so we don't cut corners. We optimize to make
> sure that session knowledge is captured exactly the way we need it so that we
> don't have to guess the next time We should also make sure that we have quick
> things to work on.
>
> Hey, can we change the font on the screen? I've got a better idea!
>
> It doesn't take us one hour to go through a process. We should be able to
> fast-track that by making sure the goal is clear, the architecture is clear, and
> the measurement is clear. We shouldn't be doing things for the sake of it. We
> should be doing things the right way.
>
> That change requires recording and checking everything but we shouldn't be
> overly building and testing without checking to see what comes next. Let's not
> do a build and check if the next thing is to change the spacing on that font. We
> need to optimize when we test and when we build to test

---

## Q4 — Why not use another existing skill?

> ⚠ **READ THIS SECTION AS EXPERIENCE, NOT AS REQUIREMENT.** Tony ruled on this
> at 22:39: *"i am not critisizing; i am sharing my expereince with it... my
> words are not laws or requirements there but frustrations or experiences."*
> Everything below is **input to the analysis** of superpowers and other tools,
> to be weighed when that evaluation is done. No requirement may be derived from
> it. The model made this mistake once already — converting his description of
> what frustrates him into standing obligations.

**Tony, 2026-08-13 17:22 EDT, verbatim:**

> Another measurement and benchmark is superpowers brainstorming and
> problem-solving. The tests it writes are great but it's just too much for how we
> work. I would like people to say, "Oh are you superpowers but what you're using
> is way better for how we work? Can we try that because that looks great?"

**The benchmark, therefore:** superpowers, beaten on *fit* rather than on
capability — its test-writing is named as genuinely good. The win condition is
an observer's reaction, and it is partly visual: *"that looks great."*

**Tony, 2026-08-13 17:23 EDT, verbatim — correcting the model's reading of what
this question is for:**

> q4: Great question but this is what we have to answer. Do we stick with
> superpowers? Is it perfect or do we build this?

**Q4 IS AN OPEN DECISION, not a justification to be collected.** Whether Kerd
should exist at all is unsettled and this interview has to answer it. The
options on the table are: stick with superpowers, or build this. Nothing in this
document may assume the answer.

*Noted for honesty rather than as an answer:* a prior evaluation of superpowers
exists in this repo from before the reset. It is deliberately not being used to
settle this, because it was made under the assumptions the reset is questioning.
It gets re-examined as evidence when this decision is actually taken, not
treated as precedent.

**Tony, 2026-08-13 17:25 EDT, verbatim — asked what is happening in the moment
superpowers feels like too much:**

> it immedialy kicks in to "brainstorm" and build "spec" then "imolementation
> plan" etc etc even when its a small thing or we dont have all the input

**Two distinct failures named, and the second is the sharper one:** it runs the
pipeline when the work is small, *and* it runs the pipeline when the inputs do
not exist — producing a spec and a plan out of information it does not have.

**Tony, 2026-08-13 17:32 EDT, verbatim — the first movement toward answering
the Q4 decision:**

> superpowers does some great things, testing covergae, showing options, showing
> progress through build etc. so we can learn from it, i just want the process to
> be ours and visable

**Three superpowers strengths named as worth learning from:** test coverage,
showing options, showing progress through the build. **The stated want:** the
process is *ours* and it is *visible*. This is not a decision to build
everything from scratch, and it is not adoption — it is ownership of the process
with deliberate borrowing. The Q4 decision remains formally open until it is
taken with evidence, but this is the direction of travel and the grounds are
ownership plus visibility rather than capability.

**Tony, 2026-08-13 17:25 EDT, verbatim — continuing:**

> so it feels labourous and its not clear what or why its doing in a black box
> way

**Three attributes of "too much", now complete:** it is **heavy** (the full
pipeline for small work), it is **ungrounded** (it proceeds without the inputs),
and it is **opaque** — laborious to sit through, with no visibility into what it
is doing or why. The third connects directly to the Q2 requirement that every
stage is visualized and confirmed (*"this is the idea that I heard. Does this
look right?"*): the visual gate is the countermeasure to the black box, not
decoration on top of the process.

**The model's reading of how this reconciles with "we do it the same way"
(Tony to confirm or correct):** the stages are **satisfied, not performed**. A
stage whose inputs are already clear is already met and costs nothing to pass;
a stage whose inputs are missing **stops and gets them** rather than generating
the artifact anyway. superpowers performs each stage on schedule regardless of
whether it is already met or cannot yet be met. That is the difference between
"too much" and "the same way every time" — and it means the fast-track for a
font change and the refusal to guess are the same mechanism, not two.

---

## Q5 — Why would you use it?

**Tony, 2026-08-13 17:30 EDT, verbatim:**

> i dont mind robust, i just mind overhead and overwork. if we can agree quickly
> and it aligns to the existing requirements and architecture and its clear what
> to do.. go !  but if it doesnt then take our time and make sure we understand
> what to do.  what i really dont want is a super verbose complex technical
> response or questions that lose the audience and results in "sure" or
> "approved" becuase the user feels dumb or cant read all the text and map it
> quickly so jsut agrees.  we need to present options and explain then concicely,
> clearly and visual if possible, give them time to react and think and answer.
> then approve or change, or even coach them to the answer. but brevity is good
> as it shows we understand, but not explaining properly or too technical can
> result in the wring agreements. so we need to find a way to communicate that
> solves for this

**The failure mode named here is FALSE APPROVAL, and it is load-bearing for the
whole system.** A verbose or over-technical gate message produces "sure" /
"approved" from a user who could not read it, did not map it, and felt stupid
saying so. Every gate in the process depends on approval meaning something; if
approvals are rubber stamps, every gate is theatre and the alignment the whole
front-loaded process exists to buy was never actually bought.

**The stated tension, which forbids the easy answer:** brevity is itself a
signal of understanding — but under-explaining causes *wrong* agreements. So
"be brief" is not the solution and neither is "be thorough". Tony's own framing:
*"we need to find a way to communicate that solves for this."*

**Also stated:** the response to a gate is not binary. Approve, change, **or be
coached to the answer** — the user may not know what they want yet, and that is
a supported path rather than a failure.

**And the go condition, stated plainly:** aligned to existing requirements and
architecture + clear what to do → **go**. Not aligned or not clear → take the
time. Robustness is welcome; overhead and overwork are not.

---

## Confirmation of the read-back, and what it opened

**Tony, 2026-08-13 17:41 EDT, verbatim — answering "does this look right?" on
the model's summary of Q1–Q6:**

> yes, we can havce multiple commands that support the main skill, like we have
> already in conductor, skriv, slainte, tend, kiva, switch etc.  thats okay but
> the conductor should know how and when yo use them. they can be used on there
> own too possibly or as an option inline (skriv for writting in users voice or
> with persona rules etc) but we can consider all of this and build the best
> solution. nothing is a sacred cow. we can also start from scratch in new repo
> and build a clean solution if that makes it easier to do, no noise.
>
> we can also consider calling other skills or tools that meet our needs vs
> build, we should consume what we can and build the differentitor but never at
> the cost of meeting our goals or quality.

**The read-back is confirmed — this document is the source of truth from here.**

**Four things this opened:**

1. **Supporting commands are legitimate.** One main skill with commands beneath
   it, possibly usable standalone or inline. **The conductor must know how and
   when to use them** — routing is the conductor's job, not the user's memory.
2. **Nothing is a sacred cow.** Every existing skill, artifact and decision is a
   candidate for change or removal.
3. **A clean-repo restart is a live option** if it produces a better solution
   with no noise.
4. **Consume before building.** Call other skills or tools where they meet the
   need; build only the differentiator — **but never at the cost of the goals or
   the quality.**

---

## What "launch" means — the span of the process

Asked because the goals are bounded by it, and the answer changes how much of
the process exists.

**Tony, 2026-08-13 17:48 EDT, verbatim:**

> launch: product, feature, document, olan or whatever we are building is ready
> for use to react to and approve as done or not. i does bring up a thought
> though, design UI/UX etc needs to be part of the pre build and measurable by
> the model during build so that the end result is exactly what we expect and we
> can have an outcome that is launcable - release to customers, send to client
> etc

**Launch is the approve-as-done moment, not market release.** The thing is ready
for the producer to react to and rule done. What that produces must itself be
*releasable* — to customers, to a client — but putting it in front of them is
outside the span.

**A new requirement surfaced by the question:** design, including UI/UX, is a
**pre-build artifact that the model measures against during the build**. Not a
picture reviewed once and set aside — something the build is checked against
while it runs, so the end result is exactly what was expected and the outcome is
launchable. This makes the design spec machine-checkable, which is a
considerably stronger claim than "we drew it and agreed".

---

## Self-reflection and straw-manning

**Tony, 2026-08-13 17:50 EDT, verbatim:**

> self reflection and straw man steps are critical for this too.

**Why this matters against the rest of the interview:** the producer has already
named false approval as the system's central failure — a gate message the user
cannot parse buys a signature instead of alignment. Self-reflection and
straw-manning attack that same failure from the other side. If the model
examines its own reasoning for error, and argues against its own proposal before
presenting it, then catching mistakes is no longer the producer's job alone. A
process where the only quality check is the human's approval has put its entire
weight on the one gate this interview says cannot bear it.

Both are stated as **critical steps in the process**, not as conduct advice.

**Tony, 2026-08-13 17:53 EDT, verbatim — extending it:**

> can even have a formal review (even advesrial) by a subagent at appropraite
> model/effort baked in

So the quality check is not only the model examining itself. A **formal,
optionally adversarial review by an independent subagent, sized to the work, is
baked into the process** rather than invoked when someone remembers. This is the
same staffing principle as the rest of the model economy — the reviewer gets the
model and effort the review deserves — applied to quality rather than to
production.

**Tony, 2026-08-13 17:52 EDT, verbatim — the third one:**

> and the occasional "are you sure" check by the model to itself

**Three quality mechanisms are now named, and they form a graded ladder** —
cheap and frequent at one end, expensive and rare at the other, which is the
same shape as the model economy applied to correctness:

1. **"Are you sure?"** — occasional, lightweight, the model challenging its own
   claim in passing. Costs almost nothing.
2. **Self-reflection and straw-manning** — structured, the model examining its
   own reasoning and arguing against its own proposal before presenting it.
3. **Formal, optionally adversarial review** — an independent subagent at a
   sized model and effort, baked into the process.

Whether the tiers fire by stage, by risk, or by cost is a design question and is
not answered here.

---

## Correction — the goals are not measured, they are designed against

The model drafted G1–G8 each carrying a *measure*, mostly counts of failures
trending to zero. Tony rejected the framing outright.

**Tony, 2026-08-13 18:06 EDT, verbatim:**

> 1. these are not measurement, these are inouts to design to avoid what those
> g1-g8 from happening, they cant be measured. we need to bake into the process
> g1: strong visuals and specs for approval so we are clear with each other.  g2:
> agents should not guess or infer from memory something, they should never have
> to, we shoudl ensure the spec has those memory items in the work g4. Clear
> communication, questions and requests, visual confirmations, status etc vs wall
> of noise text and an "approve?" g5. show the work, show the state, show the
> tools being used g6. we have a spec and the measurement of done is clear,
> should not look different or behave differt fromt he agreed spec. g7. never
> sumarize memories or requirments or achievements etc g8. build something
> valuable that there is a need for that does a thing that people want and can
> use easily without deep knowledge
>
> 2. dont understand that either. the way i work, every project has its own repo,
> its non negotiable.
>
> 3. for me any mechanisim we can use to bake in self checks is good, many times
> if i ask you "is that true" or "explain that" you see a flaw in your work, but
> if its not asked you wouldnt see. so these mechanisims are important to help you
> review and not just produce as done.

**What this settles:**

- **A goal does not carry a metric; it carries a design input.** The goals name
  failures to be *prevented by construction*, and each one converts into
  something baked into the process. Counting occurrences after the fact was the
  wrong instrument — his words: *"they cant be measured"*.
- **The repo boundary is a law, not a goal.** *"every project has its own repo,
  its non negotiable."* It is not scored; it is obeyed.
- **Self-checks are wanted wherever they can be baked in**, and his reason is a
  precise observation about how the failure works: *"many times if i ask you 'is
  that true' or 'explain that' you see a flaw in your work, but if its not asked
  you wouldnt see."* The flaw is already visible to the model — what is missing
  is the prompt to look. So the mechanism's job is to **trigger the look**, not
  to supply capability the model lacks. Its purpose is *"to help you review and
  not just produce as done."*

**Tony, 2026-08-13 18:14 EDT, verbatim — G3's design input, supplied after the
model flagged it as the one goal without one:**

> g3 is simple, the process should allow and recognize and understand for small
> changes without breaking the process or cirumventing it. example. color or text
> change or spacing chnage on app, this is fine tuning, so maybe we have a
> process that handles this aspect or we need to be able to quickly advance from
> step 1 to step 8 to make those changes and not havea huge overhead to make them
> but also not let these small changes break the design spec or the archtecure or
> requirments without agreed change

**This names a class and a guard.** *Fine tuning* is recognised work — a colour,
text or spacing change — that moves without breaking or circumventing the
process. What licenses the speed is the guard: a fine tune may not change the
design spec, the architecture, or the requirements **without agreed change**.
The moment it would, it stops being a fine tune. Two delivery shapes are floated
and neither chosen: a dedicated fine-tuning process, or fast traversal of the
normal path.

**Tony, 2026-08-13 18:16 EDT, verbatim — sharpening it immediately:**

> imagine for g3 if the design spec designer saw his font being changed without
> his approval.....

**This corrects the model's reading of its own paragraph above.** The model had
split the world into fine tunes that *don't* touch the spec (fast) and changes
that *do* (slow). But a font **is** the design spec. The designer who owns that
spec would object to it changing without their approval — and they would be
right.

So the guard is not "fine tunes avoid the spec". It is:

- A fine tune **still lands in the spec**, and still gets the agreement of
  whoever owns it. What makes it fast is that the approval is *proportionate*,
  not that it is skipped.
- The spec must remain **the truth**. A change that alters the artifact without
  being reflected back into the spec creates silent drift, and after enough of
  them the spec describes something that no longer exists.

The failure this prevents is not slowness. It is a spec quietly becoming a lie.

**Tony, 2026-08-13 18:15 EDT, generalising it into a law:**

> so each change should result in a chnage to spec or design or requirement

and immediately:

> but doesnt have to be huge process

**The law is absolute; the ceremony is proportionate.** Every change lands in
the spec, the design, or the requirements — there is no threshold below which a
change may leave its governing document untouched. What scales with the size of
the work is the *process* around that update, which for a small change may be a
one-line edit and a quick confirmation.

The model had straw-manned this as needing a threshold ("surely not for a
typo"), which would have decayed into "significant changes only" — a judgement
call, and therefore a hole. Tony's version puts the dial on the ceremony and
never on whether the document stays true.

**Tony, 2026-08-13 18:22, verbatim — what decides a change is a fine tune, and
who approves it:**

> have we already built the item and are looking to change it? does the change go
> agaist the spec or design or requirment? how much effort or impact is the
> change, how critical is the chage, are users blocked or having poor experience?
>
> the composer or conductor roles (if we keep them) should have the approval

The classifier is five questions rather than a size threshold, and the second —
*does the change go against the spec, design or requirement?* — is the one that
discriminates. It also dissolves an apparent contradiction: every change **lands
in** the spec under Law 2, but that is not the same as going **against** it.
Filling in detail the spec left open is fine tuning; contradicting what the spec
says is a change to the agreement. Urgency is admitted as an input — *"are users
blocked or having poor experience?"*

Approval for this class sits with **the composer or conductor roles**, not the
producer — which is what lets the fast path stay fast when the spec's owner is
not in the room. The roles are still provisional: *"if we keep them"*.

---

## Six rulings, 2026-08-13 22:39

Given in response to the reviewed requirements draft. Verbatim, then what each
settles.

> yeah Tension C-T1 :  when i say composer or conducter can approve, what i mean
> by that, if there is a gap in the spec or a conflict or issue implementingm the
> sub agent can ask for help to conductor who can either correct the sub agent or
> ask the composer to tweak the solutuon to fix the issue, thats what approval
> means in that context. other approvals can be conductor checking artifacts
> against spec etc.  2. "S1 and S2 trace to a section, not a goal" self checking
> can be a law - "check your work, use self analysis, askyourself is this
> correct?, use a straw man to explain your work and see if there are gaps, use an
> agent in advesrial review to challenge your thinking where appropraite., ask
> simple questions, "did i infer that", "did i read from file or stale memory",
> "have we tried this before", "Has this already been answered or recorded" etc
> d4: the border as you have it above on PLEASE READ is perfect if that is what
> you mean.
>
> on superpowers, i am not critisizing; i am sharing my expereince with it. these
> words should be used when the analysis of superpowers and other tools is done as
> an input, for consideration. my words are not laws or requirements there but
> frustrations or experiences.
>
> fine tunes move the way everything else does, just faster, assuming they dont
> break the specs etc.
>
> we should ask what is absent. we should also compare to what best practices do,
> other skills, standard methodologies, emerging thinking in AI human pairing
> process.

**1 — Tension C-T1 DISSOLVES; it was never a contradiction.** Both the composer
and the model read *"the composer or conductor roles should have the approval"*
as authority over the agreements — the agent approving a change to the spec in
the producer's place. That is not what it meant. In that context **approval is
operational**: a sub-agent hits a gap in the spec, a conflict, or an
implementation problem, and asks the conductor for help; the conductor either
corrects the sub-agent or asks the composer to tweak the solution. Plus
conformance work — *"conductor checking artifacts against spec"*. The producer's
authority over the agreements is untouched, so B1's "no small-work exception"
never conflicted with it. The requirement must be rewritten, and the tension
closed as dissolved rather than compromised.

**2 — Self-checking becomes a LAW,** which fixes S1/S2 tracing to a section. Its
content is his: *check your work · use self analysis · ask yourself is this
correct? · use a straw man to explain your work and see if there are gaps · use
an agent in adversarial review to challenge your thinking where appropriate*.
And a named set of simple questions: **"did I infer that?" · "did I read from
file or stale memory?" · "have we tried this before?" · "has this already been
answered or recorded?"**

**3 — The border format is confirmed.** The bordered PLEASE READ block used in
conversation is the shape he wants for input requests.

**4 — THE SUPERPOWERS COMMENTARY IS EXPERIENCE, NOT REQUIREMENT.** *"i am not
critisizing; i am sharing my expereince with it... my words are not laws or
requirements there but frustrations or experiences."* They are **input to the
analysis** of superpowers and other tools, for consideration when that
evaluation is done. Any requirement derived from the superpowers passages is
mis-sourced and must be re-grounded elsewhere or reclassified — this hits the
testing requirement, the "runs without inputs" requirement, and the observer
reaction.

**5 — Fine tuning has its delivery shape:** *"fine tunes move the way everything
else does, just faster, assuming they dont break the specs etc."* Not a separate
process. The same path, traversed faster, on condition the specs hold. This
closes the open question that floated two candidates.

**6 — Analysis owes an outward look, not only an inward one.** *"we should ask
what is absent. we should also compare to what best practices do, other skills,
standard methodologies, emerging thinking in AI human pairing process."* The
omission pass is confirmed, and a second dimension joins it: measure the work
against outside practice, not only against our own stated intent.

---

## Three rulings, 2026-08-13 22:58

**Tony, verbatim:**

> "Nothing we've written requires an approval to demonstrate mapping." sure it
> does, every requirement is traceable through analysis, verification, design,
> spec, plannong, releases build testing etc etc. we build in measurements and
> tracability to use to check goals and requirments are met - what am i missing
> still?
>
> what document are you referring too? we cannot consider this markdown file as
> how we capture and version and work on requirements. we need a robust and easy
> to engage with solution. pre reset we did a day of work on evakuating
> requirements and tooling and process for this very issue
>
> goals are inputs to requirements, they are vision and wants and outcomes, they
> need to be translated, drafted, worked on and finalized as requirements.

**1 — Traceability and consent are different failures, and only one of them is
covered.** His traceability point is correct and stronger than the model had
credited: requirements traced through analysis, verification, design, spec,
planning, release, build and test, with measurements built in, is a real chain
and it does prove something. What it proves is that **we built what the spec
says**. It cannot prove that **the spec says what he meant**. The approval gate
is where meaning enters the system, and it is the only link in that chain
carrying no verification — the sole evidence he understood what he approved is
that he said yes. That is precisely the failure he named himself: *"not
explaining properly or too technical can result in the wring agreements."*
Drift is covered. Wrong agreement at the gate is not. Whether that needs a
countermeasure is his call, not the model's.

**His ruling on it, 23:03, verbatim:**

> "It cannot prove the spec says what you meant."  yes great point. if we can
> manage requirments properly, with strong pairing, this can reduce this issue,
> it wont stop lazy or confused approvals later though but it gives us a strong
> backbone

**So the countermeasure is a mitigation and is accepted as one, with the residue
named rather than papered over.** Proper requirements management plus strong
pairing **reduces** wrong agreement; it does not eliminate it. A lazy or
confused approval remains possible and is accepted. What the backbone buys is
that such an approval is *recoverable* — a wrong agreement caught later can be
traced to what was agreed, when, and against which goal, instead of being
indistinguishable from a change of mind.

This is the first accepted residual risk of the reset, and it is accepted with
its limit stated, which is the discipline the goals ask for everywhere else.

**And he immediately corrected the framing, 23:05, verbatim:**

> it also allows us to change our mind. but in a controlled way. change
> requirement x and the impact can be measured and planned

**The backbone is not primarily a recovery mechanism — it is what makes changing
your mind a first-class operation.** The model had framed it defensively
(a wrong agreement becomes traceable rather than archaeological). That is true
and it is the smaller half. The larger half is that **deliberate change becomes
safe**: change requirement X, and the impact of that change can be *measured and
planned* rather than discovered.

Without it, changing your mind is indistinguishable from disruption, so the
pressure is always to leave the decision alone — which is how a project ends up
executing an agreement nobody still believes in. This is the same capability the
walkthrough asked for in Q2: *"This feature: I've changed my mind. Even though we
have a design, can we look at the impact of changing that now or does this go to
the next release, the next version? We need to be able to manage that"*.

**2 — THE MARKDOWN FILE IS NOT THE REQUIREMENTS SYSTEM.** *"we cannot consider
this markdown file as how we capture and version and work on requirements. we
need a robust and easy to engage with solution."* `docs/kerd-requirements.md` is
a drafting artifact, not the mechanism. The model had let a working document
stand in for the capability, which is the same substitution the whole reset
exists to stop.

**And the bracketing rule now expires on this point:** *"pre reset we did a day
of work on evakuating requirements and tooling and process for this very issue."*
That evaluation was deliberately excluded while the interview was being captured
— its assumptions were the ones under question. The interview is captured and
the goals are approved, so the evaluation is now legitimate **input**, to be
re-examined against the approved goals rather than treated as precedent.

**3 — Goals are INPUTS to requirements, not requirements.** *"they are vision
and wants and outcomes, they need to be translated, drafted, worked on and
finalized as requirements."* So the composer's pass produced a **draft**, and
finalisation is a worked process rather than one dispatch and an approval. The
document's own status line ("awaiting approval") overstates how close it is:
what is awaited is the working-through, not a yes.

---

## Law 4 — the standing method, 2026-08-14 08:35

**Tony, verbatim:**

> we always need to 1. assess and learn from industry standards, leading
> approaches, emerging approahes 2. decide what fits for us 3. consume/adopt
> whole if perfect  or be inspired by them, 4. design or adapt for our gaps 5.
> build for the gaps.   do this for every aspect of our project

Recorded as **Law 4** in `docs/kerd-goals.md`. **Build is what remains after
adoption and adaptation, never the starting point.** Preceded by his framing of
the same idea: *"lets not invernt fire to make meal, lets turn on the stove to
cook one"*, and by the correction that produced it — *"dont just take 'he asked
for them' as fact that is the best way"*, i.e. **provenance is not
justification**.

It indicts work already done: the goals in this file and the requirement shape
were both drafted from his words alone, with no step 1.

**Also stated, as a presentation rule:**

> when we ask for inout, put a flag or ascii border aroud the questions to ensure
> users dont think its noise.

Requests for input carry a visible flag or ASCII border so they are not lost in
the surrounding text. This is the same defect as the buried "X or Y" question:
an ask the user does not notice is an ask that gets a reflex answer.

---

## Q6 — Why would someone else want it?

**Tony, 2026-08-13 17:34 EDT, verbatim:**

> someone else would want it to help them manage and build a product or project
> and feel in control the whole time, feel safe that the effort is not lost, the
> interface is clear, the output is clear and the results are professional and
> complete.  it needs to make sense, be understandable, be optinal where options
> are possible but not so complex you dont use have the features or know they
> exist. the visual control should explain the process and the capablities too.
> nothing you dont know exists etc

**The visual layer now carries three jobs, not one.** It is the alignment gate
(*"does this look right?"*), it is the state view (where we are, what artifacts
exist), and it is **the discovery mechanism for the tool's own capabilities** —
*"nothing you don't know exists"*. A feature the user never learns about is
functionally absent, and the visual control is what prevents that.

**The felt requirements, which are outcomes rather than features:** in control
the whole time · safe that the effort is not lost · interface clear · output
clear · results professional and complete. "Effort is not lost" is the same
requirement as the memory foundation in Q1, stated from the user's side.
