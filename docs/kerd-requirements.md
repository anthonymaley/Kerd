# Kerd — the requirements

**Source:** `docs/kerd-goals.md` (APPROVED by Tony 2026-08-13 18:30) and
`docs/kerd-interview.md` (the reset interview, confirmed as source of truth
2026-08-13 17:41). Nothing else in this repo was read. Drafted 2026-08-13.

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
letter tells you the neighbourhood without a lookup.

**On the grouping:** requirements are grouped by **the question a reviewer is
asking when he reads them** — "what are the ground rules?" (A), "what happens
between idea and launch?" (B), "how do small changes move?" (C), "what makes
an approval real?" (D), "what can I see?" (E), "what is remembered?" (F),
"who checks the work?" (G), "what does it cost?" (H), "when is it done?" (I),
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

**A4.** The governing documents always describe what actually exists. An
artifact that has drifted from its spec is a defect in itself, whatever
caused it.
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
*Traces to: G3 and G2.* Grounded in his diagnosis of the benchmark's failure:
*"it immedialy kicks in to 'brainstorm' and build 'spec' then 'imolementation
plan' etc etc even when its a small thing or we dont have all the input."*

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

**C4.** Approval for the fine-tune class sits with the composer or conductor
roles, not the producer — *"the composer or conductor roles (if we keep them)
should have the approval"* — which is what keeps the fast path fast when the
spec's owner is not in the room. (The roles themselves are provisional; his
own parenthesis says so.)
*Traces to: G3.*

**C5.** When the work is aligned and clear, it goes — immediately, without
overhead: *"if we can agree quickly and it aligns to the existing
requirements and architecture and its clear what to do.. go !"* When it is
not aligned or not clear, the process takes the time.
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

**E3.** Produced artifacts and requirements carry reference numbers, so they
can be pointed at unambiguously. His word: *"Reference numbers."*
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
we don't just infer things. We don't guess. We go back to the desk to get
that knowledge."*
*Traces to: G2 and G7.*

**F5.** Tony never re-explains something already settled: *"You should
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

## G — Self-checks: who catches the mistakes

*These exist so the producer's approval is not the only quality gate — the
one gate the interview says cannot bear the whole weight.*

**G-1.** Three self-check mechanisms are baked into the process, and the
weight of the work selects the tier — his words: *"doing a thing, check it
yourself, doing a bigger thing, strawman, doing a critical thing, get
adveserial model to check."* The third tier is *"a formal review (even
advesrial) by a subagent at appropraite model/effort baked in."*
*Traces to: G4 and G7, via the self-check ladder in the approved goals.*

**G-2.** The checks fire because the process triggers them, never because
the model remembers to. His diagnosis: *"many times if i ask you 'is that
true' or 'explain that' you see a flaw in your work, but if its not asked you
wouldnt see."* The mechanism supplies the prompt to look, not a capability.
*Traces to: G4 and G7, via the self-check ladder in the approved goals.*

---

## H — Effort: the work costs what it should

**H1.** Every piece of work runs at the correct model and the correct
effort — *"make sure we're not wasting tokens by using the correct model and
using the correct effort"* — and nothing is over-built or done for the sake
of it.
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

**J4.** The process is ours and it is visible: *"i just want the process to
be ours and visable."* Borrowing capability never means surrendering the
process or its visibility.
*Traces to: G8 and G5.*

**J5.** The user never has to remember which supporting capability to
invoke — routing is the tool's job: *"the conductor should know how and when
yo use them."*
*Traces to: G8 and G5.*

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
3. **J4 (the process is ours).** As written it is barely testable — "ours"
   is a feeling about ownership, and the observable half (visible) is
   already E4/E5/J3's guard clause. It records direction-of-travel on the
   open Q4 decision more than it states what must be true of the thing.

**The one I am least confident in: C4.** It assigns fine-tune approval to
"the composer or conductor roles" — roles Tony himself marked provisional
(*"if we keep them"*). A requirement that names provisional machinery is
standing on sand. Worse, the goals file records an **unresolved straw-man
directly against it**: C4 puts classification and approval in the same
hands, so the model both decides a change is a fine tune and approves it,
with the producer out of the loop for a class the model defines — under
standing pressure to pick the cheap path. I have carried the requirement
because his words state it, but it must not be read as settling that
tension. It doesn't.

**Where the list bends its own rules.**

- **G-1 and G-2 trace to a section, not a goal.** Law 2 as applied to this
  document says every requirement traces to a goal or a law. The self-check
  ladder is neither — it is its own section of the approved goals file. I
  traced the pair to G4 and G7 "via the ladder", which is honest but
  stretched. If Tony wants the tracing strict, the ladder should be promoted
  to a law or a goal; as it stands it is approved content without a letter.
- **D4 (the ASCII border) is presentation-level HOW.** I kept it because it
  is a verbatim design input, and design inputs are the one place the goals
  deliberately carry mechanism. But it is the most concrete sentence in the
  document and a reviewer could fairly ask why a border earned a reference
  number when the fine-tuning delivery shape did not.

**Where it may over-reach.** B4's quote is Tony describing what is wrong
with superpowers, not stating a requirement — I converted a criticism into
an obligation. I believe the conversion is safe because the goals file makes
the same move ("a stage whose inputs are missing stops and gets them" is
approved G3 text), but the quoted evidence under B4 is diagnostic, not
prescriptive, and a strict reader should know that.

**Where it under-specifies.** Group C describes how fine tunes are
classified, guarded, and approved — and never says how they *move*, because
the goals deliberately leave the delivery shape open. So C is a set of
constraints on a mechanism that does not exist yet. That is correct per the
goals, but it means C cannot be verified against anything until the open
question in Gaps is answered, and a reviewer should not mistake C's
completeness of *constraints* for completeness of *behaviour*.

**The count itself.** Fifty-one requirements existed before the reset;
this list lands at 53. I did not aim at that number, but the proximity is
suspicious enough to name: a composer who knows a register existed may
unconsciously produce register-shaped output. The defence is that every
entry above carries a trace and most carry verbatim words — but the
grouping into ten letters, in particular, is my taxonomy, and taxonomies
are where invented structure hides.

## Gaps

What the goals and interview do not determine, and I would have had to
invent. Per the brief, none of these became requirements.

1. **The delivery shape of fine tuning.** Two candidates floated, neither
   chosen: a dedicated fine-tuning process, or rapid traversal of the normal
   path. Group C is written to be true under either.
2. **Build vs adopt (Q4).** Open. Also unstated: what evidence settles it
   and who takes the decision. This whole document is written to be the
   yardstick for that decision, not its outcome.
3. **Who owns each governing document.** C3 requires "the agreement of
   whoever owns it" — but ownership of the spec, the design, and the
   requirements is never assigned. When the producer is the only human in
   the project, it is undefined who the "design spec designer" of his own
   example actually is.
4. **Separation of classification and approval.** The unresolved straw-man
   under C4 (see above). The goals name the self-check ladder as the nearest
   countermeasure but never assign it. Whether a fine-tune approval by the
   conductor draws a check, and at which tier, is undecided.
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
   stages there are and what each is called is undetermined.
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
