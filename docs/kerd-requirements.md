# Kerd — the requirements

**Source:** `docs/kerd-goals.md` (APPROVED by Tony 2026-08-13 18:30; Law 3
added 22:39) and `docs/kerd-interview.md` (the reset interview, confirmed as
source of truth 2026-08-13 17:41; six rulings added 22:39). Nothing else in
this repo was read. Drafted 2026-08-13; revised the same day for the
adversarial review and again for Tony's six rulings.

**Status: AWAITING TONY'S REVIEW AND APPROVAL — BLOCKING.**
Nothing downstream may cite this document until Tony has read it and said so.
Per his own rule on gates: *"the process demand approval or push back until
approval"* — this document is not approved because it exists, and recording
that approval is outstanding does not discharge the gate.

**Tony: please read this file — the whole file, including the straw-man and
the gaps — and then approve it, change it, or ask to be walked through it.**

**One thing to hold while reading:** the build-vs-adopt decision (interview Q4
— *"Do we stick with superpowers? Is it perfect or do we build this?"*) is
still open. These requirements do not assume the answer. They describe what
the thing must do — whichever thing ends up doing it — and they are the
yardstick that decision gets measured against.

## How to read this document

Each requirement says **what must be true**, never how it is achieved. Each
carries: a reference, the requirement in one or two sentences, the goal or law
it traces to (Law 2 applied to this document: a requirement that traces to
nothing was not allowed in), and Tony's quoted words where they carry it.

**On the reference numbers:** Tony asked for reference numbers in the
interview (*"Reference numbers"*). The **scheme** below — a group letter plus
a sequence number, `A1`, `B3` — is my proposal and needs his confirmation. I
chose it because it is short enough to say out loud ("that fails B4") and the
letter tells you the neighbourhood without a lookup. **Two collisions the
scheme has to dodge, both flagged for his ruling:** the goals are already
named G1–G8, so no requirement group may use the letter G — spoken aloud,
"that fails G2" must never be ambiguous between a goal and a requirement.
The self-check group is therefore lettered **S**, and the letters run
A–F, S, H–J. Q is avoided too, because the interview's questions are Q1–Q6.

**On the grouping:** requirements are grouped by **the question a reviewer is
asking when he reads them** — "what are the ground rules?" (A), "what happens
between idea and launch?" (B), "how do small changes move?" (C), "what makes
an approval real?" (D), "what can I see?" (E), "what is remembered?" (F),
"who checks the work?" (S), "what does it cost?" (H), "when is it done?" (I),
"why would anyone want it?" (J). Each group can be approved or challenged as a
set, which is the point: these are review units, not architecture units.

---

## A — The ground rules

*The two laws, made operational. Everything else stands on these.*

**A1.** The tool lives and operates entirely inside the user's own project
repository. The Kerd project itself never holds sessions, state, or knowledge
for anyone else's work.
*Traces to: Law 1.* His words: *"the way i work, every project has its own
repo, its non negotiable"* and *"the Kerd project should never have sessions
for any of those other repos or projects."*

**A2.** Every change to what is being built results in a change to the spec,
the design, or the requirements. There is no size threshold below which a
change may leave its governing document untouched.
*Traces to: Law 2.* His words: *"so each change should result in a chnage to
spec or design or requirement."*

**A3.** The ceremony around that document update scales with the work. For a
small change it may be one line and a quick confirmation; the scaling dial is
on the process, never on whether the document stays true.
*Traces to: Law 2.* His words: *"but doesnt have to be huge process."*

**A4.** The governing documents and the artifact never disagree. Before the
build they describe what is agreed to be built; from the moment something
exists they describe it as it actually is. An artifact that has drifted from
its spec is a defect in itself, whatever caused it.
*Traces to: Law 2 and G6.* His words: *"should not look different or behave
differt fromt he agreed spec."*

---

## B — The path from idea to launch

*What happens between "I've got an idea" and "approve as done".*

**B1.** There is one path from idea to launch, walked the same way every
time. Duration varies; the stages do not. There is no small-work exception.
*Traces to: G3.* His words: *"My two minutes or four weeks, it doesn't
matter... We do it the same way."*

**B2.** The path works for anything being built — *"a product, a document, a
business idea, a code project for enhancing something that exists. It doesn't
really matter."*
*Traces to: G8 and G1.*

**B3.** Before building starts, producer and agent are aligned on what will
be built, how it has to work, and what good looks like — and that alignment
is bought up front so building does not need constant back-and-forth.
*Traces to: G1.* His words: *"we get to the point where we are super aligned
on: what we're going to build, how it has to work, what good looks like.
Then you just go and build it."*

**B4.** A stage whose inputs are missing stops and gets them. The process
never generates a stage's artifact out of information it does not have.
*Traces to: G3 and G2.* Re-grounded after Tony's ruling that the superpowers
passages are experience, not requirement: this now stands on approved G3
text — *"a stage whose inputs are missing stops and gets them instead of
inventing them"* — and on G2's design input that agents *"should never have
to"* guess. The superpowers experience that first surfaced it is recorded in
the tool-analysis input below, where it now belongs.

**B5.** New solutions never appear inline without the agreed steps. *"Hey can
we change this skill to do this thing the way I like it? Just make that
change. That's verboten."*
*Traces to: G1.*

**B6.** During the build, the work is continuously measured against the
agreed goals, requirements, and design — *"It should loop and measure itself
against those goals and requirements, and design to make sure we build what
we agreed we're going to build."*
*Traces to: G6 and G1.*

**B7.** Design — including UI/UX and how the thing looks and behaves — is
agreed before the build and is checkable by the model **while the build
runs**, not reviewed once and set aside.
*Traces to: G6.* His words: *"design UI/UX etc needs to be part of the pre
build and measurable by the model during build."*

**B8.** A change of mind mid-journey is managed, not absorbed: the producer
can ask for the impact of changing an agreed thing now, or defer it — *"can
we look at the impact of changing that now or does this go to the next
release, the next version? We need to be able to manage that."*
*Traces to: G1.*

**B9.** Technical talk is kept to a minimum unless the user asks for it —
*"we need to keep the technical chat to a minimum unless that is what's being
requested."* The default register is the producer's, not the implementer's.
*Traces to: G4.*

**B10.** Ideation has substance, not just a slot on the path: it establishes
whether the idea is viable, who the competitors are, *"whether it already
exists, and whether we should leverage other technology"*. His opening move:
*"Hey I've got a new product. Let's figure out if it's viable... What is the
product? What is the idea? How will it work? Who are the competitors?"*
*Traces to: G8 and G1.*

**B11.** The path begins as free back-and-forth — *"we can whiteboard
together and share ideas back and forward"* — and then has an explicit lock
moment: *"but then we'll lock it"*. What the lock produces is not a
transcript but a formalisation: *"Formalize all of those back-and-forth
conversations into a spec that becomes measurable, linked to the goals and
the requirements."* The spec's linkage to goals and requirements is itself
required — the traceability this document practises, the product must have.
*Traces to: G1 and Law 2.*

**B12.** What each stage captures is usable to measure the success of the
stage that follows it — *"capture the requirements, or what will become
requirements, in a way that we can use to measure the success of the next
step, which will probably be validation or design."* Measurement is
stage-by-stage along the path, not only at the end (I3 covers the end).
*Traces to: G6 and G1.*

---

## C — Fine tuning: how small changes move

*The one path (B1) never bends; this is how small work travels it fast
without breaking it.*

**C1.** The process recognises fine tuning as a class of work, decided by
Tony's five questions, not by a size threshold: *"have we already built the
item and are looking to change it? does the change go agaist the spec or
design or requirment? how much effort or impact is the change, how critical
is the chage, are users blocked or having poor experience?"*
*Traces to: G3.*

**C2.** The discriminating question is the second: a change that goes
**against** the spec, design, or requirements is a change to the agreement
and goes the long way round with the agreement's owner. Filling in detail
the spec left open is fine tuning.
*Traces to: G3 and Law 2.*

**C3.** A fine tune still lands in its governing document (per A2) and still
gets the agreement of whoever owns that document. Its speed comes from the
approval being proportionate, never from it being skipped. His warning:
*"imagine for g3 if the design spec designer saw his font being changed
without his approval....."*
*Traces to: G3 and Law 2.*

**C4.** The approval held by the composer or conductor roles is
**operational, never contractual**. Tony's ruling, 22:39: *"if there is a
gap in the spec or a conflict or issue implementing... the sub agent can ask
for help to conductor who can either correct the sub agent or ask the
composer to tweak the solution to fix the issue, thats what approval means
in that context. other approvals can be conductor checking artifacts against
spec etc."* So the agent roles may unblock a stuck sub-agent, route a spec
defect back to the composer, and check artifacts against the spec — and they
may never change what was agreed with the producer. (The roles themselves
remain provisional: *"if we keep them"*.)
*Traces to: G3 and G6.*

**C5.** When the work is aligned and clear, it goes — immediately, without
overhead: *"if we can agree quickly and it aligns to the existing
requirements and architecture and its clear what to do.. go !"* When it is
not aligned or not clear, the process takes the time.
*Traces to: G3.*

**Note — the former Tension C-T1, dissolved 22:39.** This document, and the
adversarial review before it, recorded a formal contradiction here: C4 was
read as moving approval of the agreements from the producer to the agent
roles, which collided with B1 ("no small-work exception") and E6 ("confirmed
before it counts"). The contradiction was **apparent, not real** — both
readers over-read the one word *approval* as authority over the agreements,
when in Tony's usage it is operational: unblocking, routing defects to the
composer, checking artifacts against the spec (see C4 as now written). The
producer's authority over what was agreed was never in question, so there
was nothing for B1 or E6 to conflict with. Dissolved, not resolved — no
compromise was needed and none is in place.

**C6.** Fine tunes have their delivery shape, ruled 22:39: *"fine tunes move
the way everything else does, just faster, assuming they dont break the
specs etc."* Not a separate process — the same path as everything else,
traversed faster, on condition the specs, design, and requirements hold.
*Traces to: G3.*

---

## D — Approvals: what makes a "yes" real

*Every gate in the process depends on approval meaning something. These
requirements exist because false approval is the named central failure.*

**D1.** An approval gate demands its answer. The process pushes back until
approval or change is given; it never records that approval is outstanding
and moves on. His words: *"the process demand approval or push back until
approval, 'not yet keyed' suggests recored as status and moved on."*
*Traces to: G4.*

**D2.** An approval request explicitly asks the person to **read the thing
being approved**, and names it. An approval collected without that ask is
worth less than it appears — this exact defect is recorded in the goals file
(*"didnt see you ask for a reviwe of that file"*).
*Traces to: G4.*

**D3.** A gate message is concise, clear, and visual where possible — never
*"wall of noise text and an 'approve?'"*. Options are presented and explained
*"concicely, clearly and visual if possible"*, and the user is given *"time
to react and think and answer."*
*Traces to: G4.* Design input, his words: *"Clear communication, questions
and requests, visual confirmations, status etc vs wall of noise text and an
'approve?'"*

**D4.** Every request for input carries a visible flag so it cannot be
mistaken for surrounding text: *"when we ask for inout, put a flag or ascii
border aroud the questions to ensure users dont think its noise."*
Confirmed by Tony 22:39 with a concrete instance: *"the border as you have
it above on PLEASE READ is perfect if that is what you mean"* — the bordered
block is the shape he wants.
*Traces to: G4.*

**D5.** The response to a gate is never only yes-or-no. The user may approve,
change, **or be coached to the answer** — *"then approve or change, or even
coach them to the answer"* — and not knowing yet is a supported path, not a
failure.
*Traces to: G4.*

**D6.** The cumulative weight of the process never overwhelms the user. A
process clear at every individual gate and exhausting in aggregate has
failed. Design input, his words: *"a user never feels overwhelmed by the
process."*
*Traces to: G1 (second design input).*

---

## E — Visibility: what the user can always see

**E1.** At every moment the user can see where we are in the journey and
what happens next: *"Where are we in the journey? What's happening next?"*
*Traces to: G5.*

**E2.** The user can see what has been produced and open it — during the
build, not only after: *"What content or artifacts have we produced and can
I view them?"* and *"I can see the progress and the artifacts as you make
them."*
*Traces to: G5.*

**E3.** What has been produced carries reference numbers, so it can be
pointed at unambiguously. His word — *"Reference numbers"* — sits inside the
state-view list (journey, next, artifacts), so that is what it grounds.
Extending reference numbers to the requirements themselves, as this document
does, is my extension and needs his confirmation alongside the scheme.
*Traces to: G5.*

**E4.** Nothing operates as a black box. The work, the state, and the tools
in use are all shown. Design input, his words: *"show the work, show the
state, show the tools being used."*
*Traces to: G5.*

**E5.** The visual control also explains the process itself and the tool's
own capabilities — *"nothing you dont know exists."* A feature the user never
learns about is functionally absent. Options are offered *"where options are
possible but not so complex you dont use have the features or know they
exist."*
*Traces to: G5 and G8.*

**E6.** Every stage is visualized and confirmed before it counts: *"Hey,
this is the idea that I heard. Does this look right?"* — *"here's the current
view, here's the goal. Does that look correct?"* The same visual form is used
for problems: *"Here's what I think is happening: we can visualize it."*
*Traces to: G1 and G5.*

**E7.** The architecture is presented for approval as one simple,
easy-to-understand diagram — *"Boxes, not code"* — covering, in his words,
*"the architecture, the tech stack, the flow between them, where we're going
to host that, the tools we're going to use."*
*Traces to: G1 and G4.*

---

## F — Memory: what is never lost and never guessed

**F1.** Work on a project can continue forever without losing the knowledge
gained along the way — *"The changes, what we built, what worked, and what
didn't work: we have all of that knowledge and we refer to it in the
appropriate way."*
*Traces to: G2.*

**F2.** A session can end and a later session pick up cold with full
context — *"context clearing and restarting without losing any context
memory"* — as if it were the same conversation continuing.
*Traces to: G2.*

**F3.** Agents never guess or infer from memory. Design input, his words:
*"agents should not guess or infer from memory something, they should never
have to, we shoudl ensure the spec has those memory items in the work."* The
work's spec carries the memory items the work needs, so guessing is never
even available.
*Traces to: G2.*

**F4.** Knowledge is fetched, not re-read wholesale: *"We don't read the
whole book of what we've done every session but we know how to find that and
we don't just infer things. We don't guess. We go back to the disk to get
that knowledge."*
*Traces to: G2 and G7.*

**F5.** Tony shouldnt have to re-explain something already settled: *"You should
instinctively know or know how to know about what we're talking about."*
*Traces to: G2.*

**F6.** Session handovers are as fast as possible **after** quality is
satisfied, never instead of it: *"Switch-ins and switch-outs should be really
fast and clear but they should wait on quality, not speed."*
*Traces to: G2.*

**F7.** Memories, requirements, and achievements are never summarised. Where
the record matters, fidelity outranks compression, always. Design input, his
words: *"never sumarize memories or requirments or achievements etc."*
*Traces to: G7.*

**F8.** The session-memory capability is usable on its own, outside the full
idea-to-launch process: *"it's something we can use on its own just for
non-conductor."*
*Traces to: G2.*

---

## S — Self-checks: who catches the mistakes

*These exist so the producer's approval is not the only quality gate — the
one gate the interview says cannot bear the whole weight. Lettered S, not G,
so no requirement here can ever be confused with a goal (see the scheme
note). Since 22:39 this group traces to* ***Law 3 — check your own work
before it counts*** *— which closes the tracing defect the first draft
confessed: these entries no longer hang off a section.*

**S1.** Three self-check mechanisms are baked into the process, and the
weight of the work selects the tier — his words: *"doing a thing, check it
yourself, doing a bigger thing, strawman, doing a critical thing, get
adveserial model to check."* The third tier is *"a formal review (even
advesrial) by a subagent at appropraite model/effort baked in"*, used
*"where appropraite"*.
*Traces to: Law 3.*

**S2.** The checks fire because the process triggers them, never because
the model remembers to. His diagnosis: *"many times if i ask you 'is that
true' or 'explain that' you see a flaw in your work, but if its not asked you
wouldnt see."* The mechanism supplies the prompt to look, not a capability.
*Traces to: Law 3.*

**S3.** Work has to survive Law 3's four named questions before it counts,
each naming a specific way confident output goes wrong: *"did i infer
that"* · *"did i read from file or stale memory"* · *"have we tried this
before"* · *"has this already been answered or recorded"*. Inference dressed
as knowledge, a stale recollection standing in for a read, repeating a dead
end, and re-deriving something already settled.
*Traces to: Law 3.*

**S4.** Checking runs in both of Law 3's required dimensions. **Inward:** is
what is here correct, and *"we should ask what is absent"* — self-criticism
that audits only what made it in structurally misses omissions. **Outward:**
*"we should also compare to what best practices do, other skills, standard
methodologies, emerging thinking in AI human pairing process"* — work
measured only against its own stated intent cannot detect that the intent is
behind the field.
*Traces to: Law 3.*

---

## H — Effort: the work costs what it should

**H1.** Every piece of work runs at the correct model and the correct
effort — *"make sure we're not wasting tokens by using the correct model and
using the correct effort"* — and nothing is over-built or done for the sake
of it. ("Correct" has no sizing authority yet — who or what judges the
weight of a piece of work is open; see Gap 5.)
*Traces to: G7.*

**H2.** The best models design and own the actual solution, so ideas are
never degraded by economy: *"we're using the best models to design and own
the actual solution so we're not degrading ideas. If we use lower models, we
always push it to the correct model."*
*Traces to: G7.*

**H3.** Work is delegated to sub-agents *"of the appropriate level"* — the
sizing applies to helpers the same as to the lead.
*Traces to: G7.*

**H4.** Building and testing are sequenced against what comes next, not run
for their own sake: *"we shouldn't be overly building and testing without
checking to see what comes next. Let's not do a build and check if the next
thing is to change the spacing on that font."*
*Traces to: G7.*

---

## I — Done: what launch means

**I1.** Launch is the moment the thing is *"ready for use to react to and
approve as done or not"* — the producer's approve-as-done ruling, not market
release.
*Traces to: G6.*

**I2.** What is ruled done is itself releasable beyond the desk —
*"launcable - release to customers, send to client etc"* — and *"the results
are professional and complete."*
*Traces to: G6.*

**I3.** The measurement of done is clear in the spec before the build, and
done means the result does not *"look different or behave differt fromt he
agreed spec"* — how it looks and how it behaves are both covered.
*Traces to: G6.*

**I4.** The work is tested, and testing is what earns the claim that the
result does not *"look different or behave differt fromt he agreed spec"* —
done cannot be ruled without it. Testing exists in his own non-superpowers
words: *"That change requires recording and checking everything"* and *"We
need to optimize when we test and when we build to test"* (Q3, on how good
looks) — you cannot optimise when you test unless testing is a standing part
of the work. **Re-grounding note, reasoning stated per the ruling:** this
requirement was first grounded in his praise of superpowers' tests. That
praise is experience, not requirement, and has moved to the tool-analysis
input below. The requirement survives without it because G6 demands a
checked outcome and Law 2 demands the documents and artifact agree — both
unverifiable without testing. What moved is the *standard* ("tests worth
learning from"): that was superpowers-derived and is now analysis input, not
obligation.
*Traces to: G6 and Law 2.*

---

## J — Value: why anyone would want it

**J1.** The thing is *"something valuable that there is a need for that does
a thing that people want and can use easily without deep knowledge."* No
prior expertise in the tool is required to get its value.
*Traces to: G8.*

**J2.** Adoption by others counts. His ruling: *"adoption by other yes
important"* — used only by Tony is a failure against this goal.
*Traces to: G8.*

**J3.** Where existing skills or tools meet a need, they are consumed rather
than rebuilt; only the differentiator is built — *"we should consume what we
can and build the differentitor but never at the cost of meeting our goals or
quality."*
*Traces to: G8.*

**J4.** *Moved, 22:39 revision — not silently deleted.* This entry required
"the process is ours and it is visible", quoting *"i just want the process
to be ours and visable"*. That sentence sits inside the Q4 superpowers
passage, which Tony has ruled is experience, not requirement — so it may not
ground an entry here. The visibility half is already carried by E4 and E5;
the ownership half is recorded in the tool-analysis input below, where it
weighs on the build-vs-adopt decision. The number is retained so J5 does not
shift.

**J5.** The user never has to remember which supporting capability to
invoke — routing is the tool's job: *"the conductor should know how and when
yo use them."*
*Traces to: G8 and G5.*

---

## Input to the tool analysis

Not requirements. Tony's ruling, 22:39: *"on superpowers, i am not
critisizing; i am sharing my expereince with it. these words should be used
when the analysis of superpowers and other tools is done as an input, for
consideration. my words are not laws or requirements there but frustrations
or experiences."* Everything here is experience to weigh when the
build-vs-adopt evaluation (interview Q4, still open) is actually taken.
Recorded rather than deleted, per the same ruling's spirit: nothing moves
silently.

- **What he rates in superpowers:** *"The tests it writes are great"* and
  *"superpowers does some great things, testing covergae, showing options,
  showing progress through build etc. so we can learn from it."* The
  "tests worth learning from" standard, formerly part of I4, lives here now.
- **His frustrations with it:** *"it immedialy kicks in to 'brainstorm' and
  build 'spec' then 'imolementation plan' etc etc even when its a small
  thing or we dont have all the input"* and *"it feels labourous and its not
  clear what or why its doing in a black box way."* These experiences first
  surfaced what became B4 and reinforce E4/E6 — but those requirements now
  stand on the goals, not on this.
- **The ownership want, formerly J4:** *"i just want the process to be ours
  and visable."* Direction-of-travel for the Q4 decision; the visibility
  half is required independently by E4/E5.
- **The observer reaction he'd like:** *"Oh are you superpowers but what
  you're using is way better for how we work? Can we try that because that
  looks great?"* An aspiration to weigh, not a requirement to meet.

---

## Straw-man

Where this list is wrong, weakest, or padded. Written against my own output,
as the process requires.

**The three I would cut if forced.**

1. **E7 (the boxes diagram).** It is the closest thing here to a HOW. Tony
   sketched a solution shape — a hybrid diagram with five named contents —
   and I promoted the sketch to a requirement because his words were vivid.
   The requirement underneath it is really E6 (every stage visualized and
   confirmed) applied to the architecture stage. If E7 survives review, it
   should survive as *his stated design input for how E6 lands at that
   stage*, not as an independent requirement.
2. **H3 (sub-agents at the appropriate level).** It is H1 restated for
   helpers. One quoted clause, no independent content. It exists because the
   quote exists, which is padding logic, not requirement logic.
3. **J4 (the process is ours).** As written it was barely testable — "ours"
   is a feeling about ownership, and the observable half (visible) is
   already E4/E5/J3's guard clause. It recorded direction-of-travel on the
   open Q4 decision more than it stated what must be true of the thing.
   *(Since 22:39 this cut has been executed for a stronger reason: its
   grounding quote is superpowers commentary, which Tony ruled is
   experience, not requirement. J4 now lives in the tool-analysis input.)*

**The one I was least confident in: C4 — and the lesson survives its
repair.** Two drafts running, C4 was this document's weakest entry: first
flagged as standing on provisional roles, then formally recorded (as Tension
C-T1) as contradicting B1 and E6. Tony's 22:39 ruling dissolved all of it —
both the reviewer and I had over-read the single word *approval* as
authority over the agreements, when he meant operational approval:
unblocking, defect routing, conformance checking. What remains worth keeping
from the episode: an entire named tension, carried through an adversarial
review, was manufactured by one word read in the wrong register. That is
precisely the paraphrase failure G7 warns about, occurring not in a summary
but in a *reading* — and neither the inward pass nor the adversarial review
caught it; only asking Tony did. The residual soft spot in C4 is unchanged:
it names roles he still marks provisional (*"if we keep them"*).

**Where the list bends its own rules.**

- **S1 and S2 traced to a section, not a goal — RESOLVED 22:39.** The first
  draft confessed that the self-check entries hung off a section of the
  goals file rather than a goal or a law, and said the fix was promotion to
  a law. Tony did exactly that: *"self checking can be a law"* — Law 3 now
  exists and the whole S group traces to it. Kept here because it is the one
  straw-man item that produced a change upstream instead of downstream.
- **D4 (the ASCII border) is presentation-level HOW.** I kept it because it
  is a verbatim design input, and design inputs are the one place the goals
  deliberately carry mechanism. Tony has since confirmed the shape
  explicitly (*"perfect if that is what you mean"*), which settles the
  keep — and the fine-tuning delivery shape it was unfavourably compared to
  now has its own entry (C6), so the asymmetry this bullet complained about
  is gone.

**Where it over-reached — confirmed and repaired.** The first draft flagged
that B4 converted a superpowers criticism into an obligation; Tony's 22:39
ruling confirmed the class of error was real and bigger than one entry:
*"my words are not laws or requirements there but frustrations or
experiences."* B4 survived only because it could be re-grounded on approved
G3 and G2 text; I4 survived on G6 and Law 2 with its superpowers-derived
standard stripped out; J4 could not be re-grounded and moved to the
tool-analysis input. **D2 performs a similar conversion** — a recorded
process defect (*"didnt see you ask for a reviwe of that file"*) turned into
a standing obligation — but its source is different in kind: the defect is
recorded in the **approved goals file** as *"a defect worth not
repeating"*, which is prescriptive intent inside an approved document, not
experience commentary Tony has ruled off-limits. D2 therefore stands, on
that stated justification. If Tony rejects the reading, D2 falls to Gaps.

**Where it under-specified — since repaired.** The first two drafts of
Group C described how fine tunes are classified, guarded, and approved, but
never how they *move*, because the goals then left the delivery shape open.
Tony's 22:39 ruling closed it (*"fine tunes move the way everything else
does, just faster"*), carried as C6 — so C now covers classification,
guard, approval, and movement. The paragraph is kept because the pattern
generalises: constraints on an unbuilt mechanism can look complete while
the mechanism itself is undefined, and Group C sat in that state for two
drafts without either straw-man noticing.

**The count itself, and its provenance.** Fifty-one requirements existed
before the reset — **that number was supplied in the composer's brief; the
register itself was not read**, and the isolation claim in the header
stands. This list first landed at 53, suspiciously near it, rose to 57 after
the omission pass below added four, and now stands at 59 active entries
after the six rulings (C6, S3, S4 added; J4 moved to the tool-analysis
input, its number retained as a tombstone). The residual worry is not
the number but the shape: a composer who knows a register existed may
unconsciously produce register-shaped output. The defence is that every
entry above carries a trace and most carry verbatim words — but the
grouping into ten letters, in particular, is my taxonomy, and taxonomies
are where invented structure hides. And I should be honest about what that
confession costs me: nothing. Regrouping loses no content, so admitting the
taxonomy is invented is the cheapest self-criticism in this section.

**The omission pass — the structural blind spot of the first straw-man.**
Every criticism above attacks something *present*: cut this entry, that one
is shaky, this trace is stretched. None of it asked what is **absent** —
and checking presence never catches absence. An adversarial review caught
three omissions by running the interview forward, passage by passage, and
asking what each demands that no requirement carried. All three are now in
the list: **testing** (I4 — dropped entirely from my first draft; since
re-grounded on G6 and Law 2 after the superpowers ruling), **the whiteboard
and the lock** (B11 — the lock moment and the spec's required linkage to goals and
requirements; my document practised traceability and never required it of
the product), and **viability and competitors** (B10 — stage *content* Tony
stated, which my Gap 9 had wrongly filed under stage *names*). I then ran
the same pass myself over the full interview. Beyond those three it found:
**per-stage measurability** (added as B12 — requirements captured so they
measure the success of the *next step*, which no end-state requirement
covered); *"make it perform incredibly well between human and agent"* —
an outcome with no stated content, moved to Gaps (15) rather than invented
into a requirement; and *"We should also make sure that we have quick
things to work on"* — a sentence whose meaning I genuinely cannot pin
(quick wins kept available? small tasks queued?), also under Gap 15,
flagged for Tony to gloss rather than for me to guess. This pass is now a
standing part of the straw-man, not a one-off repair.

**The outward pass — required by Law 3's second dimension.** Where this
document falls short measured against outside practice, not its own intent.
Four concrete findings:

1. **Verifiability.** Standard requirements practice (the IEEE-style rule
   that every requirement must be verifiable) fails several entries as
   written: D6 ("never overwhelmed"), J1 ("valuable... people want"), and
   F5 ("never re-explains") state felt outcomes with no way to tell pass
   from fail. The goals deliberately carry no metrics — *"they cant be
   measured"* — but that ruling was about **goals**; whether *requirements*
   may inherit unverifiability is a distinct question nobody has answered,
   and this document quietly assumed yes.
2. **Traceability runs one direction.** Best practice is bidirectional:
   trace each requirement up, and check each goal is carried down. This
   document only did the first, so I ran the second for this pass: every
   goal and law now has at least one carrying requirement (G1→B3/B5/D6,
   G2→group F, G3→B1/group C, G4→group D, G5→group E, G6→group I/B7/B12,
   G7→F7/group H, G8→J1–J3/B10, Law 1→A1, Law 2→A2–A4, Law 3→group S). The
   check passes today, but nothing makes it re-run when either file
   changes — coverage is a snapshot, not a property.
3. **Register hygiene.** Standard registers carry per-entry status,
   priority, and change history. This document has one document-level
   status and no per-entry lifecycle — yet B8 *requires the product* to
   manage requirement changes (impact, defer, versions). The register
   demands of the product a discipline it does not practise on itself.
4. **AI-human pairing.** Current thinking on human-in-the-loop review
   treats rubber-stamping as an *attention* failure with known
   countermeasures that make confirmation active — the human selects,
   states back, or answers a question about the content — rather than
   passive ("approve?"). Group D attacks false approval almost entirely
   through presentation: borders, brevity, visuals. Only D5's coaching path
   gestures at active confirmation. Nothing here requires that an approval
   demonstrate mapping, which is the field's stronger tool against exactly
   the failure G4 names. That may be a deliberate design question rather
   than a missing requirement — but the outward comparison says our D group
   is one generation behind the failure it targets.

## Gaps

What the goals and interview do not determine, and I would have had to
invent. Per the brief, none of these became requirements.

1. ~~**The delivery shape of fine tuning.**~~ **CLOSED 22:39** by Tony's
   ruling: *"fine tunes move the way everything else does, just faster,
   assuming they dont break the specs etc."* Same path, faster traversal,
   conditional on the specs holding — now carried as C6.
2. **Build vs adopt (Q4).** Open. Also unstated: what evidence settles it
   and who takes the decision. This whole document is written to be the
   yardstick for that decision, not its outcome.
3. **Who owns each governing document.** C3 requires "the agreement of
   whoever owns it" — but ownership of the spec, the design, and the
   requirements is never assigned. When the producer is the only human in
   the project, it is undefined who the "design spec designer" of his own
   example actually is.
4. **Separation of classification and approval — mostly dissolved 22:39,
   one residue.** The alarming version (the agent approving changes to the
   agreements it also classifies) rested on the misreading dissolved with
   Tension C-T1: conductor approval is operational, and the producer's
   authority over the agreements is untouched. What remains open is
   smaller: who classifies a **borderline** fine tune, and whether an
   operational approval (a conductor unblocking a sub-agent, or accepting a
   composer tweak) itself draws a Law 3 check, and at which tier.
5. **Who judges the weight of the work.** The ladder's trigger is settled
   (the weight of the work), but who or what assesses that weight — and what
   counts as "critical" for the adversarial tier — is not.
6. **Where the quality/speed line sits in handovers.** F6 states the
   ordering (quality first, then fast); the goals explicitly leave the line
   undecided (Tension 1).
7. **The communication shape that solves brevity vs false approval.** Tony:
   *"we need to find a way to communicate that solves for this."* D3 states
   the outcome; the way is design work (Tension 2).
8. **What "visual" concretely means.** Stages are visualized, state is
   visualized, questions are bordered — but the medium (terminal output,
   rendered pages, diagrams, something else) is nowhere fixed, beyond
   "Boxes, not code" and the sensei skill named as a style reference.
9. **The stage list itself.** The walkthrough sketches ideation → analysis/
   requirements → validation or design → architecture → build, with "the
   next phase, and then the next phase" explicitly open-ended. How many
   stages there are and what each is called is undetermined. (What the
   stated stages must *contain* is not deferred here — B10, B11 and B12
   carry it; this gap is only the count and the names.)
10. **The roles.** Producer, composer, conductor are used throughout and
    marked provisional in the same breath (*"if we keep them"*). Whether
    the role structure survives is a design decision the requirements must
    not pre-empt — C4 and J5 are the two entries most exposed if it falls.
11. **How overwhelm is detected.** D6 requires the user never feel
    overwhelmed by the process in aggregate; nothing states how the process
    would notice that it is happening, or what it sheds when it does.
12. **What "managed" means for a mid-journey change of mind.** B8 requires
    impact-or-defer handling; releases and versions are mentioned once and
    never defined.
13. **The reference numbering scheme.** Wanted (E3), but the scheme —
    including the one used in this very document — is proposed, not chosen.
14. **What memory is kept where, and its retention.** F1–F4 require
    permanence and precise retrieval; what distinguishes session memory,
    contextual memory, and long-term memory (his three terms) and how long
    each lives is not determined by the goals.
15. **Two interview phrases whose content is undetermined.** *"make it
    perform incredibly well between human and agent"* — an outcome the
    whole system serves, but with no stated content beyond what D, E and F
    already carry; and *"We should also make sure that we have quick things
    to work on"* — a sentence I cannot confidently gloss (quick wins kept
    available? small tasks queued between big ones?). Both need Tony's own
    words expanding them before they can become requirements; inventing a
    reading would be exactly the paraphrase failure G7 forbids.
