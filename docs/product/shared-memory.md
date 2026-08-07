---
route: new
stage: framed
---

# Shared memory — the room has a wall, and both of us can see it

## Value

Tony's requirement, in his words (2026-08-07, given as a metaphor after the
session established that the boundary loses human input):

> You are sitting beside me in a room, with a whiteboard, and we are pairing
> on a project. We start with ideation and we draw on the whiteboard to
> capture current condition and show the ideal, and then we figure out the
> gaps that stop ideal from becoming reality. We then design the solution
> (and research, and do viability studies etc) and then we plan the
> solution's implementation, in releases. **BUT this is the key point: we are
> talking back and forth all the time, and we SHARE ALL THE CONTEXT
> together.**

The failure, in his words, and it is stated as a feeling because the feeling
is the cost:

> We go to lunch and come back to the room and… I hope you remember what we
> did before lunch, and have to check and ask you and remind you and worry
> that you forgot all the amazing things we agreed and discovered and planned
> that got me super excited. I'm nervous, and then I get dejected because I
> feel like I wasted my time and we lost the opportunity.

The target state:

> We walk into the room and continue, with perhaps a quick recap to get
> things moving, but we remember everything. We don't need to explain the
> idea, the gaps, the analysis, **the big picture that it could lead to — and
> not just the next task.** We have all of that in our SHARED MEMORY.

### What these pages are for

**Primary function: state visualization.** Tony, stated directly when an
earlier draft of this document called them an input channel: *"its primary
function is state visualization."* The pages show where things are. They are
not a form, not a console, and not where direction is entered — direction is
given in conversation, as it always has been.

What they change is the *quality* of that conversation. In his words, about
the visual stories: *"we also need to tell our stories visually, like the
sensei story layouts I shared, so we have shared alignment. I know you don't
need this but I do — this is how I give you what you need."* Seeing true
state is what lets him direct well. The direction is still spoken; the wall is
what makes it well-aimed.

The design consequence is narrower than an input channel would imply, and
sharper: **every page is judged on whether the state it shows is true and
obvious**, not on what can be done to it. A page that is accurate and
unreadable fails. A page with affordances for entering data is out of scope
unless something else argues for it.

### Two people, two views, one state

Stated by Tony as the framing for the whole item: *"we need different
things."*

- **The model's view** is mechanical — files, diffs, gate records, derived
  position, code. It already exists and works.
- **The human's view** is the product — current condition, ideal, gaps,
  releases, journey, architecture, risks, what we considered. It does not
  exist.
- **When we speak, we speak the product**, never the code: *"when we speak we
  don't speak in code, we use the whiteboard, we speak in the language of the
  product, not in LLM or deep tech code."*

One shared state, rendered twice. This is not two sources of truth — every
human-facing page is a rendering of the same on-disk state the machine reads.

### Roles, as Tony stated them

- **His:** guide in plain English, see gaps, have ideas that may be
  breakthroughs or may be distractions — *"so we need a way to capture those
  and assess and decide when we do it"* — and feel confident that progress is
  being made on the product goals, *"see that and hear the right things all
  the time, or I get nervous."*
- **The model's:** ideation, analysis, design, build execution. *"There is a
  lot on your plate, you need all the context and the memory, all the big
  picture, to be able to make sure we are doing the right things at the right
  time. But you also need to know the focus for this session and this release
  and get that done."*

Both halves matter and they pull in opposite directions: all the big picture,
*and* a narrow focus for the session. A view that shows only the next task
fails the first; a view that shows everything fails the second. The journey
must carry both altitudes at once.

### Value, in units

- **Re-explanations required per pickup: 1 observed → 0.** Baseline measured
  on this session's own pickup (2026-08-07): Tony asked *"tell me what we
  worked on last session and why it was important"* because the pickup had
  reported a 28-item menu instead of the thread. The information was loaded;
  it was not surfaced.
- **Human-facing views of project state: 0 of 10 → all 10.** Enumerated in
  the gap list below. Two loose HTML pages exist; neither is reachable as a
  surface.
- **Sources populated behind those views: 3 of 10 → 10 of 10.** Today only
  ladder position, risk ledgers, and the three-fix rule have real content.
  Seven views would render blank if built now.
- **Evidence that the model is up to speed at pickup: none → shown.** Tony,
  2026-08-07: *"I also need to know when we start a new session you are up to
  speed and know what's next."* A pickup that *claims* to be up to speed is
  indistinguishable from one that invented something plausible — he tested
  exactly this during the session that produced this document.
- **Ideas captured at the moment they are had: 0 → all of them.** There is no
  inbox. An idea spoken mid-session survives only if a model chooses to write
  it down.

Explicitly *not* value here: prettier output. Every page must change what
Tony can see or decide; a page that only looks better is out of scope.

## Grounding

- docs/product/switch-fidelity.md — the root cause this item inherits, and the boundary half of the same problem
- docs/plans/2026-08-05-journey-view-mock.html — the agreed shape of the journey page, converged over four live iterations and parked
- docs/design/talk-formats.md — the sensei story grammar; the visual vocabulary these pages must speak
- docs/design/progress-view.md — the decided design for the progress rendering
- tools/diagram/progress.py — the machine-side derived board; the model's half of the same state
- tools/design/README.md — the evaluation matrix standard, built and CI-enforced
- tools/gates/README.md — the ladder vocabulary the journey renders
- CONTEXT.md — standing decisions bind: derived-from-disk, a release is a grouping, a risk without a countermeasure is a blocker, design is agreed in diagrams

## The gap list

Ten views Tony named on 2026-08-07, measured the same day. Each row states
what exists, not what is planned.

### Gap 1 — the master plan has no artifact, and the decision saying it should is four days old

Tony wants *"a screen on the wall or a constantly updated printout that shows
the master plan — all the things we are going to do and what release they are
in."*

"A release is a GROUPING, not a time axis" was decided 2026-08-03 with five
deciding factors and an assembled-not-authored done condition. **There is no
artifact.** Product docs each carry a per-item `## Release slice` section;
nothing groups items into a release, so no file anywhere answers "what is in
release 1".

Tony's amendment (2026-08-07): this is the same artifact as the kanban board
in gap 8 — *"1 maps to the kanban release planning point also, can be new or
unplanned."* New and unplanned items land on the same board as planned ones.

### Gap 2 — the journey view is mocked, agreed, and parked

Tony wants *"the simple high level non-technical language of what the stages
are and the steps within them, and where we are in that journey — and for
each step what the status is and what was achieved. Should be very basic
visually but incredibly obvious. The master plan items should make their way
through this visualization until goal and I should be able to see that. I can
also drill into the items to see the results if needed."*

`docs/plans/2026-08-05-journey-view-mock.html` is that page, converged over
four live iterations: story head (current situation → proposal → measured in
use), then the ladder as sections — Idea, Validated, Scoped, Designed,
Spec'd, Built, Proven, Live — with a what's-cooking card set above it.

It was parked 2026-08-05 pending "more journeys on the ladder." Five journeys
have since walked it, so the parking condition is met on its own terms. What
changed independently is weight: the page was treated as optional tooling, and
this document establishes that it is one half of the shared memory rather than
a nice-to-have rendering of the machine's half.

Prerequisite, and it is thinner than it looked. The status word Tony wants —
*on plan / taking longer / encountered issues* — has three legs and only one
of them needs timing:

- **"encountered issues"** is derivable today: a refused gate, a risk in the
  `fatal` state, or a risk with no countermeasure — all machine-readable now.
- **"on plan"** is the default when neither of the others fires.
- **"taking longer"** needs a comparison basis, which is what time-awareness
  (v0.88.0/v0.89.0) exists to produce. Tony, 2026-08-07: *"that's why we added
  time to things recently — start/end allows us to compare and estimate
  better."* The mechanism is right and the corpus is one day old.

Measured 2026-08-07: **5 per-task actuals** exist across all 34 session logs,
all written after the mechanism shipped. **2 of 15 gate records** carry a
`**Clock:**` line. And gate-record filenames are day-granular, so 6 of the 7
completed journeys show design and goal on the *same date* — day resolution
collapses almost every journey to zero elapsed and cannot support the
comparison at all.

Consequence for the page: it shows **a fact and a comparison, never a
verdict** — "frame: 4 min · typical 4 min (n=1)" with the sample size
visible, so the reader can see how much the comparison is worth. A bare
"taking longer" with no arithmetic behind it is the class of thing that makes
a wall lie. The leg gets stronger every session at no extra cost, because the
actuals are already being written.

### Gap 3 — there is no diagram of what we are building

Tony wants *"a view of the architecture diagram, what we are building and how
it all connects, high-level blocks with lines, this way I know what is being
built and what the components are and how they interact — a hybrid view of
tech stack, conceptual and physical."*

`tools/diagram/` holds 23 generators. **Every one renders a process flow** —
the design flow, the build flow, the session flow, the ladder, per-feature
stage flows. Not one renders the thing being built.

Evidence: `ls tools/diagram/gen_*.py` and a read of each generator's subject,
2026-08-07.

Tony has offered further examples of the shape he means; the three altitudes
(conceptual, physical, stack) in one hybrid view is not a form this repo has
drawn before.

### Gap 4 — risks have data and no view, and issues have neither

Tony wants *"the risks and issues list, to see the risks we have or had and
what the impact and countermeasure is or will be or not — if no countermeasure
is available then we have a blocker. Traffic lights is the way to show good to
blocker."*

**Risks:** the data exists and is good — eight-column ledgers in product docs,
five legal states, gate-checked, killer-first. It is markdown in a file he
does not read. The five states map onto a traffic light without inventing
anything.

**Issues:** no list exists anywhere. The repo tracks risks (what might go
wrong) and has no concept of an issue (what is wrong now). Everything
currently wrong lives in TODO prose or in a session log.

### Gap 5 — the evaluation matrix is enforced, empty, and has no exemption

Tony wants *"the evaluation matrix of what we considered and why we chose it.
We should do this for all critical items unless we agree it's a reference
design item — i.e. we are building a tvOS app, we use Swift, no need to
evaluate choices."*

`tools/design/` is built, fixture-tested and CI-enforced. `matrix audit`
reports **0 matrices**. A checker guarding an artifact nobody produces reports
clean forever (inherited as switch-fidelity gap 10).

**New in Tony's statement: the reference-design exemption.** No such concept
exists in the standard today. Without it the rule is all-or-nothing, and an
all-or-nothing rule that demands a matrix for "use Swift on tvOS" will be
ignored, which is how the machinery ended up at zero. The exemption is what
makes the requirement survivable — and it must be an *agreed* exemption, not
a silent skip, or it becomes the same hollow-waiving risk already named in
rigor-level.

### Gap 6 — three tries then root cause is specced and has never fired

Tony wants *"when we solve problems we need to follow a process. We can move
quickly to fix, but if we are not getting a solution after 3 tries we need to
follow sensei problem solving to find root cause."*

This already exists: conductor's 3-fix limit stops after three attempts, and
`docs/design/talk-formats.md` names three-survived-fixes as the problem-tier
trigger routing to a point-of-cause tool. **No instance has ever fired.**
Whether that is because the rule works, because problems are resolving in
under three attempts, or because the rule is being skipped, is unmeasured.

### Gap 7 — the story grammar exists as a library and is rendered once

Tony wants *"to tell our stories visually, like the sensei story layouts I
shared, so we have shared alignment."*

`docs/design/talk-formats.md` is the canonical library. Its only rendered
instance is the head of the parked journey mock. Every other use is a *spoken*
format in a gate message — correct, and invisible on a wall.

### Gap 8 — release planning has no board

Tony wants *"to see all the items and where we have them bucketed for release
— kanban style — this way we can build a release, or see we are not
forgetting. Can also trim features easily that way."*

Nothing exists. This is gap 1's artifact given a shape: the master plan *is*
the board, and the board is where new and unplanned items land.

**The one piece here that is not a rendering:** dragging a card writes state
back into the repo from a browser. Every other page in this document is
read-only. Tony's position (2026-08-07): *"how we move things we can analyse
and discuss, but we need a visual to see the overview"* — the overview is the
requirement, the drag mechanism is open.

### Gap 9 — there is no surface, only two loose files

Tony wants *"this to be super visual and accessible — HTML pages, not
markdown (for me; you can have markdown for your items), diagrams embedded,
story at the top, journey below, risks, issues etc. as other pages."*

Two HTML files exist: `docs/plans/progress.html` (the machine's board,
rendered for CI staleness comparison) and the parked journey mock. Neither
links to the other. There is no index, no navigation, and nothing that a
person could leave open on a second screen.

The format split is explicit and worth recording as a standing rule: **markdown
is the model's medium, HTML is the human's.** They render the same state.

### Gap 10 — nothing shows that the model is up to speed

Tony, 2026-08-07: *"I also need to know when we start a new session you are up
to speed and know what's next."*

He tested this during the session that produced this document, asking whether
the model had the context already or had only read it because he asked. The
honest answer was that it had been loaded at pickup — but **the two cases are
indistinguishable from his seat**, because both produce a fluent answer.

This is the same accepted-unknown risk switch-fidelity records as the fidelity
check, seen from the other side: switch-fidelity asks *did the pickup restore
what the close recorded*; this asks *can Tony tell.* A claim cannot answer it.
Only showing him the plan, the position and the open thread — and letting him
spot what is wrong in seconds — can.

### Gap 11 — the why is recorded, and the pickup cannot reach it

Demonstrated live during the framing of this document, 2026-08-07, by the
model writing it. Tony's naming of it: *"time is another example of forgetting
key things we worked on and why."*

The model asked Tony how a page could honestly say "taking longer" when
nothing declares what "on time" was. That question was answered on
2026-08-06 in `docs/product/time-awareness.md` `## Value`, quoting Tony at
approval: *"task start and end give duration; accumulated durations are the
base that makes effort estimates for future tasks accurate instead of
guessed"* — with a declared unit, *effort actuals per conducted task: 0 →
captured*. The record was correct, in his words, and one day old.

Three distinct failures, none of them a missing record:

1. **The read-set structurally cannot reach it.** Switch-in reads CONTEXT.md,
   TODO.md, the newest session log and the derived board. It never opens a
   product doc. Ten product docs carry ten `## Value` sections — the single
   most reliable human input in the repo, because `gate.py` refuses a rung
   without one — and **zero are read at pickup.**
2. **CONTEXT.md records mechanism and drops purpose.** Its time-awareness
   entry is among the longest in the file — same-turn rule, cold-eyes blocks,
   marker restamping, statusline, four amendments — and contains no statement
   of what the feature was *for*. The file that is read carries the how; the
   why stayed in the file that is not.
3. **Append-only preserves falsified claims beside their falsifiers.** The
   2026-08-05 line "progress % and time-left have no on-disk home" still sits
   twenty lines from the 2026-08-06 entry that made it false, with nothing
   marking which won. The model read both and reasoned from the older one.
   This is a cost of the licensed-prune rule shipped in v0.90.0 and was not
   named when that rule was designed.

The bias is the same one named in the root cause, one level up: **when a
decision is retold, the machine-checkable part survives the retelling and the
human part does not.** Mechanism is easy to restate because it is verifiable;
purpose is a sentence someone has to choose to carry forward.

Consequence for this item: a journey page that shows position and status but
not *why each thing exists* would not have prevented this. The why has to be
on the wall, next to the thing, permanently.

Boundary half of the fix — reading product-doc `## Value` at pickup — belongs
to switch-fidelity, not here.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| The views get built over empty sources — seven of the ten render blank because the state they display is never captured | yes | the whole item delivers nothing: a wall of empty pages is worse than no wall, because it looks like coverage and reports clean forever | high — this has already happened once at smaller scale: the evaluation matrix is built, fixture-tested and CI-enforced and holds zero matrices after four days | measured 2026-08-07: matrix audit reports 0 matrices; 0 ruled-out artifacts against a 2026-08-03 decision; no release grouping artifact; no issues list; no architecture diagram among 23 generators | countermeasure - permanent | slice order is driven by source population, not by page appeal: the first slice renders only from sources that already hold real content, and every later slice pairs each new view with the capture that fills it in the same slice | any slice proposing a view whose source is empty at slice time re-argues this row |
| Capture stays discipline-dependent — a model must choose to record human input, and the model least likely to record it is one already drifting | yes | the root cause is untouched and every view decays to stale, which returns Tony to checking and reminding, the exact failure this item exists to remove | high — this is the measured status quo, and the only human input that reliably survives today survives because gate.py refuses without it | switch-fidelity's root-cause section, confirmed first-party by Tony 2026-08-07: "all of the x's are where I see the problem regularly, I drive input and direction and we revisit next session" | countermeasure - permanent | capture becomes a declared artifact with a gate, on the Value precedent — a rung cannot pass while its human-input artifact is absent, so recording is refused-into rather than remembered | the first gate that passes with an empty human-input artifact re-argues this row |
| The human view and the machine view drift apart and become two sources of truth | no | Tony reads a wall that contradicts the repo, which is worse than no wall — he would be making decisions on stale state without knowing it | medium — the repo already has one instance: docs/playbook.md Current Status duplicates CONTEXT.md and is the section that rotted, claiming v0.60.0 against a repo at 0.89.0 | gap 9 of switch-fidelity, measured at the release pass of 2026-08-06 | countermeasure - permanent | every human-facing page is derived from disk and CI-refused if stale, on the progress.py precedent — no page holds a fact of its own, and a page that cannot be derived is not built | the first page that needs a hand-maintained value re-argues this row |
| Drag-and-drop requires a write path from a browser into the repo, which nothing here has ever needed | no | either the board is read-only and Tony edits it by speaking, or a new and unproven mechanism enters the system | medium — the requirement is the overview, not the dragging, and Tony has explicitly left the mechanism open | Tony 2026-08-07: "how we move things we can analyse and discuss, but we need a visual to see the overview" | accepted unknown | | the slice that builds the board must decide read-only versus write-back before it starts |
| The reference-design exemption becomes a silent skip and the matrix stays empty | no | gap 5 persists behind a rule that now looks satisfied, which is worse than an unmet rule because it reports clean | medium — the identical failure was named and countered in rigor-level as hollow waiving, so the pattern is known and recurring | rigor-level's killer risk, 2026-08-05: waived-by-name is the cheapest state and is therefore the licensed habit | countermeasure - permanent | an exemption is a declared artifact carrying its reason, machine-checked in the same sweep as a matrix, reusing the accepted-state discipline verbatim — never an absence | the first exemption declared without a reason re-argues this row |

## Killer risk, read out

Two killers, and they are the same failure at two ends of one pipe.

**Empty sources** kills from the view end: build the wall first and it renders
blank, which is the most expensive possible way to learn that capture was the
real problem.

**Discipline-dependent capture** kills from the source end: fill the wall by
remembering to fill it, and it decays exactly as the evaluation matrix already
has — built, enforced, and empty after four days.

Both have permanent countermeasures and both countermeasures are the same
shape: **pair every view with the gated capture that fills it, in the same
slice, and order slices by which sources already hold content.** Remove that
pairing rule and this work item is dead by its own standard — it becomes a
website over an empty repo.

## Release slice

Rigor level: mvp

**Slice 1 — the journey page, rendered from sources that are already
populated.** Chosen on evidence rather than appeal: it is the only view in the
gap list whose sources hold real content today.

- Ladder position for every slug — `tools/diagram/progress.py` derives it from
  disk and CI refuses it if stale
- The story head — `## Value` is gate-refused when absent, so every product
  doc has one
- Risks with traffic lights — risk ledgers are gate-checked eight-column
  tables with five legal states, in every product doc
- What was achieved per rung — gate records exist in `docs/gates/`, dated and
  immutable

That is four of the five things Tony asked the journey to show, from sources
that cannot be blank.

The fifth — the status word — is mostly derivable too, as gap 2 records: two
of its three legs read off gates and risk states that already exist. Only
"taking longer" waits on a comparison basis, and that basis is now being
written automatically by time-awareness (5 actuals on disk, one day in). Slice
1 therefore carries the status word with the timing leg **shown with its
sample size** rather than omitted or estimated. Progress percentage stays out
until it has a declared home; a percentage with nothing declaring the
denominator is an estimate wearing a fact's clothes.

One measured finding worth carrying into design: **gate-record dates are
day-granular and that is too coarse** — 6 of 7 completed journeys show design
and goal on the same date. The `**Clock:**` line is the finer signal and sits
at 2 of 15 records. Making it routine costs nothing and is the difference
between a rung-duration comparison that works and one that reads zero forever.

Slice 1 also answers gap 10: a page showing the plan, the position and the
open thread is what makes "up to speed" checkable in seconds instead of
claimed in a sentence.

**Deliberately excluded from slice 1, each named with its reason:**

- **The master plan and kanban board (gaps 1, 8)** — its source does not
  exist. The release grouping artifact must be designed and populated before a
  board can render it, and the write-back question must be settled first.
- **The architecture diagram (gap 3)** — no prior art in this repo and three
  altitudes to reconcile. Tony has offered further examples; the frame for it
  should start from those rather than from a guess.
- **The issues list (gap 4, second half)** — needs its own small frame: what
  an issue is, how it differs from a risk, and where it is written.
- **The evaluation matrix exemption (gap 5)** — a change to a CI-enforced
  standard, and it belongs with the slice that starts producing matrices, not
  with a view.
- **The site shell (gap 9)** — slice 1 produces one page. A navigation
  surface is worth building when there are three pages to navigate.
- **Anything measuring gap 6** — the three-fix rule is already specced and
  correct; whether it fires is a measurement question, not a build.

## What we ruled out

**Notifying Tony when a parked item becomes relevant** — rejected 2026-08-07
in favour of a phase. The someday/maybe review happens at roadmap and release
planning; once a release is sliced the pile goes invisible until it ships. An
interrupt would destroy the focus the slicing exists to create. Carried
forward from switch-fidelity, where it was first recorded.

**Markdown for the human-facing views** — rejected by Tony 2026-08-07:
*"HTML pages, not markdown (for me; you can have markdown for your items)."*
The split is now a standing rule rather than a preference: markdown is the
model's medium, HTML is the human's, both rendered from one state.

**Framing the pages as an input channel** — rejected by Tony 2026-08-07, in
the framing conversation, against an earlier draft of this document that made
it the centerpiece. The claim was the model's extrapolation from his line
*"this is how I give you what you need,"* not something he said: seeing true
state lets him direct well, which is not the same as the page being where
direction lands. His correction: *"its primary function is state
visualization."* Recorded because the extrapolation had already produced a
design question (whether the mock's agreed shape needed to change) that had no
premise under it — a rejected option that was one step from becoming work.

**Building the wall before fixing capture** — rejected on the killer risk
above. It is the obvious first move and it is wrong: seven of the ten views
render blank today, and a blank page that looks like coverage is worse than an
acknowledged gap.

**Treating this as switch-fidelity slice 2** — rejected 2026-08-07 during the
framing conversation. Slice 2 of switch-fidelity was scoped as "capture the
thinking layer at the boundary." Three of the four needs Tony named are not
boundary problems at all: speaking the product language happens every turn,
idea capture happens the moment an idea is had, and progress confidence is
continuous. Folding them into a document about session handoff would hide
them.

## What this is not

- **Not a redesign of the model's tooling.** The derived board, the gates and
  the generators work. This adds a second rendering of the same state; it
  changes nothing about how the machine reads it.
- **Not a second source of truth.** Every page here is derived from disk. A
  page that would need its own hand-maintained fact is not built until that
  fact has a declared home.
- **Not a console.** State visualization is the primary function (Tony,
  2026-08-07). The pages show where things are; direction continues to be
  given in conversation. Affordances for entering or editing data are out of
  scope unless a specific need argues for them — the kanban board in gap 8 is
  the one open case.
- **Not the boundary.** switch-fidelity continues separately and keeps the
  handoff mechanics. This item is about what exists to hand over.
