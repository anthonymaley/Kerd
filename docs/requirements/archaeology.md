# Requirement archaeology — candidates recovered from CONTEXT.md

**Status: DRAFT. Nothing here is a requirement.** Every entry is a *candidate*
awaiting the producer's key, in batches, by family.

---

## What this is, and the rules it runs under

`CONTEXT.md` holds the standing decisions of this project. Many of them state a
**standing obligation** — something that must hold from now on — and were never
filed as requirements, because the register was filled from the middle of the
chain outward. This file recovers those, so they can be keyed as a set rather
than rediscovered one at a time.

**It runs under the standing decision that licensed it** (CONTEXT.md,
2026-08-07), and that decision's constraints are not negotiable here:

1. **Never from session logs.** Logs are *history* — true when written, with no
   claim about now — so every superseded statement is still present as though
   live. Choosing which survived would be a judgment on the producer's words
   made from a model's summary of them: two layers of paraphrase from the
   source. **Nothing in this file comes from a session log.**
2. **CONTEXT.md only**, because it is *state*: its contract is that superseded
   decisions are struck or removed, so it has already been through supersession
   filtering.
3. **Provenance is marked permanently.** Every candidate carries a
   `Provenance.` line saying it was transcribed from a standing decision and
   **was never stated as a requirement**. That marker does not expire on
   approval. Get this wrong once and the register is untrustworthy with no way
   back.
4. **Framed work, not an ad-hoc pass.** Which is what this file is.
5. **The key lands on batches**, by family, not entry by entry.

**The risk this file is exposed to, stated plainly:** retrofitting manufactures
requirements nobody stated. The countermeasure is that every candidate quotes
the decision it came from, so the producer is always reading the source beside
the derivation — never the derivation alone.

## What is deliberately NOT done here

- **No references are minted.** Candidates are numbered `C-nn`, which is not a
  requirement reference. Rule 2 says filing refuses a block arriving with a
  pre-written number and the tool assigns; minting `R-` numbers here would take
  that decision away from the tool and bake this file's ordering into the
  register permanently.
- **No Whys are invented.** Where CONTEXT.md carries the producer's verbatim
  words, they are quoted and they *are* the Why. Where it carries only the
  model's rationale, the Why says so. **Neither is silently upgraded.**
- **No fingerprints, no approvals.** Nothing here is approvable in place.

## How to read an entry

| Line | Meaning |
|---|---|
| `Statement (proposed).` | The obligation in the adopted format's terms — EARS form, word list applied |
| `Why.` | The reason, with his verbatim words where CONTEXT.md carries them |
| `Traces to.` | The goal or law it serves, from `docs/kerd-goals.md` |
| `Source.` | The CONTEXT.md standing decision, quoted enough to check the derivation |
| `Provenance.` | Permanent. Transcribed, never stated as a requirement |
| `Note.` | Overlap with an existing requirement, or a judgement the producer should overturn if it is wrong |

---

## Batch A — the risk machinery

Six candidates. The 2026-08-03 risk decisions are the densest standing
obligations in CONTEXT.md and **none of them is in the register**, which
currently holds the evaluation matrix's marks but not the risk vocabulary those
marks were built to express.

### C-01 — a risk without a countermeasure is a blocker

**Statement (proposed).** Where a risk carries no countermeasure, the work
shall be blocked until a countermeasure, an acceptance with a named reason, or
an accepted-unknown with a review trigger is recorded against it.

**Why.** It flips the default so silence stops work instead of passing it. The
dangerous state is not an unnamed risk — it is a named, unsized one, because
that reads as managed.

**Traces to.** G1

**Source.** CONTEXT.md, 2026-08-03: *"A risk without a countermeasure is a
BLOCKER. Flips the default so silence stops work instead of passing it. Risks
are not unnamed — they are unmitigated, unqualified (the dangerous one: a
named, unsized risk reads as managed) or accepted unknowns."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

**Note.** The three legal resting states already exist as machinery — `kit.py`
`LEGAL_STATES` — so this candidate is close to describing something built. It
is filed because the *obligation* is nowhere declared: the checker enforces the
vocabulary, nothing declares that an uncountered risk stops work.

### C-02 — evidence qualifies a risk, and likelihood is never multiplied in

**Statement (proposed).** A qualified risk shall carry evidence that is either
a test or an analysis, an impact stated in the declared value's own units, and
a likelihood recorded as a separate value. The tooling shall not combine impact
and likelihood into a single score.

**Why.** Expected value is the wrong arithmetic for a bet taken once —
multiplying a rare catastrophe by its probability produces a number that reads
like a small problem.

**Traces to.** G1, G2

**Source.** CONTEXT.md, 2026-08-03: *"Evidence qualifies a risk, and it is a
test OR an analysis. Qualified = proven AND measured: impact in the value's
units, likelihood recorded separately — never multiplied, because expected
value is the wrong maths for a bet taken once."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

### C-03 — fatal is decided by impact alone

**Statement (proposed).** A risk whose impact equals or exceeds the declared
value of the work shall be classified fatal at any likelihood, and likelihood
shall determine only the response.

**Why.** Tying the class to likelihood lets a catastrophic risk be argued down
by calling it unlikely, which is the argument that is always available and
never checkable in advance.

**Traces to.** G1

**Source.** CONTEXT.md, 2026-08-03: *"Fatal = impact >= declared value, at any
likelihood; likelihood sets the response, not the class."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

### C-04 — a temporary countermeasure carries a return condition

**Statement (proposed).** A countermeasure shall be recorded as permanent or as
temporary, and a temporary one shall carry the condition under which it is
revisited. A countermeasure recorded without that marking shall be treated as
permanent.

**Why.** An unmarked temporary countermeasure becomes permanent by neglect —
nobody decides to keep it, it simply stops being looked at.

**Traces to.** G2, G7

**Source.** CONTEXT.md, 2026-08-03: *"Countermeasures are permanent or
TEMPORARY (carrying a return condition; an unmarked temporary one is permanent
by neglect)."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

**Note.** The paired obligation — *accepted risks carry a review trigger*
(CONTEXT.md, 2026-08-04) — is the same mechanism aimed at a different state and
is folded in here rather than filed twice. Split them if the producer wants the
accepted state to carry its own row.

### C-05 — one risk state cannot be accepted by name

**Statement (proposed).** A risk carrying high impact, high likelihood and no
countermeasure shall not be resolved by acceptance.

**Why.** It is the one state where acceptance is not a decision but a
description of a dead project. Every other risk can be accepted by someone
willing to name the reason; this one cannot, because there is nothing to accept
*to*.

**Traces to.** G1

**Source.** CONTEXT.md, 2026-08-03: *"The limit on acceptance: high impact +
high likelihood + no countermeasure = dead project — the one blocker that
cannot be accepted by name."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

### C-06 — a gate blocks from outside the model

**Statement (proposed).** A gate shall be enforced by a mechanism that runs
outside the model. Advisory output shall not be recorded as a gate.

**Why.** The producer's measured finding, and the reason CI exists in this
repo: *"Nothing in the system can refuse, and nothing counts"* — every gate
that is prompt-layer is a model choosing to comply, which is not a check.

**Traces to.** Law 3, G1

**Source.** CONTEXT.md, 2026-08-03/04: *"every gate on the rung must block from
outside the model; advisory output is not a check (absorbs 'Refuse bad work';
CI is its first instance)"*, and 2026-08-02: *"Nothing in the system can
refuse, and nothing counts. 0 CI workflows and 0 pre-commit hooks across every
repo. Every gate in Kerd is prompt-layer — a model choosing to comply."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03/04.
Never stated as a requirement.

**Note — overlap, and the producer should decide which survives.** `R-0051`
says a *completeness check* binds on countable facts from outside the model.
This candidate is the general form of the same rule, applied to every gate.
Either C-06 subsumes R-0051, or R-0051 is the specific instance worth keeping
beside it. Filing both unchanged would put a general law and its own special
case in the register as peers, which is how a set starts contradicting itself.

---

## Batch B — the record: what is kept, what is dropped, and what is derived

Seven candidates. This family is the one the reset was about: the machinery
that decides whether a thing said today is still reachable next week.

### C-07 — derived from disk, never self-reported

**Statement (proposed).** Where the position of work is reported, it shall be
derived from artifacts on disk. A position declared by the party doing the work
shall not be recorded as the position.

**Why.** A self-reported position is the one fact that is always available and
never checkable, and the whole reason it was banned: the machine can recover
commits, files and gate records without anyone choosing to write them down.

**Traces to.** G5, Law 3

**Source.** CONTEXT.md, 2026-08-04: *"progress is DERIVED FROM DISK, never
self-reported"*, and 2026-08-04 on the mode cut: *"step tracker → self-reported
position, forbidden by derived-from-disk."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-04.
Never stated as a requirement.

**Note — this candidate carries the producer's own limit on itself.** His
2026-08-07 root cause: *"we solve for code level but all the context is not
code — much of it is human input that we lose."* Derived-from-disk works
because code leaves artifacts; human input leaves none. The rule is right and
its reach is narrower than it sounds, and that should be recorded with it
rather than discovered again.

### C-08 — what was ruled out is kept, and stays ruled out

**Statement (proposed).** An approach that is rejected or that fails shall be
recorded as a ruled-out concept with the reason it died, and shall be read as
grounding by any later work that proposes an approach. A ruled-out concept
shall not be re-adopted unless a return condition recorded against it has
fired.

**Why.** Two decisions that are one mechanism. A rejected approach and a failed
fix are the same thing — an option eliminated, one by analysis and one by a
test — and the unit is the concept, because concepts outlive codebases. And
without the second half, a dead approach comes back as a building block and the
project goes in circles.

**Traces to.** G2, G7

**Source.** CONTEXT.md, 2026-08-03: *"'What we ruled out, and why' is its own
artifact… A rejected approach and a failed fix are the same thing… The unit is
the concept, not the attempt and not the code; concepts outlive codebases…
Read in GROUNDING by everything that proposes, which makes it an input rather
than a graveyard"*; and 2026-08-04: *"Standing principle (Tony): dead solutions
stay dead — a cut or ruled-out approach is not a future building block unless a
named return condition fires."*

**Provenance.** Transcribed from two CONTEXT.md standing decisions, 2026-08-03
and 2026-08-04. Never stated as a requirement.

**Note.** The adopted requirement format already implements the recording half
— the graveyard, whose *what was learned* field exists precisely to stop a dead
idea being re-proposed. This candidate is the general obligation across all
work, not only requirements. Worth checking whether the producer wants one rule
or two.

### C-09 — a record is dated; a living document is not

**Statement (proposed).** A document that records an event shall carry its date
and shall not be rewritten. A document that states what is currently true shall
carry no date and shall be revised in place.

**Why.** The test is one question — *would rewriting this tomorrow be correct,
or falsifying the record?* Correct means living; falsifying means it is a
record. Mixing the two is how a project loses the ability to tell what it
decided from what it believes.

**Traces to.** G2

**Source.** CONTEXT.md, 2026-08-03: *"Date records of events. Never date living
documents. Test: would rewriting this tomorrow be correct, or falsifying the
record? Correct → living, no date, git history is the archive. Falsifying → a
record, dated, never rewritten."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

**Note.** CI already enforces the undated half for `docs/design/`. The
obligation itself is declared nowhere.

### C-10 — the state file grows except at a licensed event

**Statement (proposed).** Content shall be removed from the state file only at
a licensed event — a goal record landing, or a drop the producer has agreed —
and each removal shall be named in that session's record.

**Why.** Erosion and unbounded growth are the same dial. A short session that
prunes can silently delete an agreed point a deeper session recorded, and that
loss is exactly what the boundary exists to prevent. A short session is
structurally not a licensed event, so it cannot prune.

**Traces to.** G2

**Source.** CONTEXT.md, 2026-08-07: *"CONTEXT.md became append-only between
licensed prune events — a goal record landing or an explicit agreed drop —
after measurement showed the prune instruction had never once fired in 34
revisions (5,074 → 54,566 bytes, 12 → 59 decisions, monotonic)."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

### C-11 — history is archive, and the durable net is elsewhere

**Statement (proposed).** The pickup shall read the state file, the work file
and the newest session record. Older session records shall be read on demand
rather than at every pickup, and a durable warning shall be written to the
living guide rather than left only in a session record.

**Why.** Forward-only discipline is what makes the small read set safe:
anything still live was carried forward, so an old log holds nothing a pickup
needs. That guarantee fails for warnings, which is why the mirror check exists
— an unmirrored gotcha is effectively lost.

**Traces to.** G2, G5

**Source.** CONTEXT.md: *"Older session logs are archive, never per-session
load. Safe because forward-only discipline carries live items and the playbook
is the durable gotcha net — switch-out verifies gotcha mirroring before commit
(hardening after Test 1 found a five-day-old unmirrored gotcha)."*

**Provenance.** Transcribed from a CONTEXT.md standing decision. Never stated
as a requirement.

### C-12 — a warning surfaces where its subject is touched

**Statement (proposed).** A warning that must be known at every session shall
live in the file the harness loads automatically. A warning about a specific
area shall live in the living guide and shall name its subject well enough to
be found when that area is touched.

**Why.** The producer's own framing: a gotcha surfaces when you are about to
touch the thing it is about, not at every pickup. It also resolves a real
circularity — the boundary verifies every warning reaches the guide, while the
pickup declares the guide unread and cites that as the reason old logs are
skipped.

**Traces to.** G5, G2

**Source.** CONTEXT.md, 2026-08-07: *"A gotcha surfaces when you are about to
touch the thing it is about, not at every pickup… a gotcha that must always be
known belongs in CLAUDE.md, which loads automatically; one about a specific
area stays in docs/playbook.md and must name its subject well enough to be
found by grep at the moment of touching it."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

### C-13 — a system-wide change owes a repo-wide sweep at design time

**Statement (proposed).** Where a change alters behaviour across the system,
its design shall include a repository-wide search for every site the change
affects, and that search shall happen before the build rather than after it.

**Why.** It is the oldest recurring failure in this repo — an edit map written
from memory misses the documents that actually route the behaviour. It was
promoted from a warning to a design obligation after a review found four
boundary claims and four contract rows that the map had missed.

**Traces to.** Law 3, G2

**Source.** CONTEXT.md, 2026-08-06: *"Standing rule born: any slice touching
system-wide behaviour owes a cross-cutting `grep -rn` sweep at design time (the
playbook's oldest gotcha, now a design-rung obligation)."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-06.
Never stated as a requirement.

---

## Batch C — the working relationship

Seven candidates. This family is almost entirely absent from the register, and
it is the family the producer interacts with every session.

### C-14 — the division of labour is declared, and the human key lands upstream

**Statement (proposed).** The producer shall hold the frame, viability, slice
and design rungs and the evaluation at the goal rung. The model shall hold the
contract and build rungs. A build piece shall not require a producer approval.

**Why.** His words: *"I don't want to see the code being built, that's your job;
mine is the spec and the design of the product/feature/problem definition and
then to evaluate your result."*

**Traces to.** G3, G5

**Source.** CONTEXT.md, 2026-08-07: *"The division of labour, stated by Tony
2026-08-07 and now standing: his rungs are frame, viability, slice and design —
spec, direction, problem definition — plus evaluation at the goal rung;
contract and build are the model's."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

**Note.** `R-0014` (approving the design is enough) is the same decision seen
from the gate side. This candidate states who owns which rung; R-0014 states
that the plan gate is gone. They are compatible and may want merging.

### C-15 — build mechanics are not narrated to the producer

**Statement (proposed).** Where work is reported to the producer, the report
shall carry decisions, findings and results. Search output, edit-by-edit
progress and verification transcripts shall be left in the commit record.

**Why.** It follows directly from the division of labour: reporting the build
in detail to someone who has said the build is not theirs to watch spends their
attention on the one rung they do not hold. Observed rather than theorised — a
session did exactly this the day the rule was stated.

**Traces to.** G1, G5

**Source.** CONTEXT.md, 2026-08-07: *"What changes is conduct: do not narrate
build mechanics to Tony. Greps, edit-by-edit reporting and verification output
belong in commits, not in the conversation; bring decisions, findings and
results. Observed failure: the 2026-08-07 session reported its own build in
detail to a producer who had said the build was not his to watch."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

### C-16 — a message asking for a decision carries what is being decided

**Statement (proposed).** A message that asks the producer for a decision shall
contain the findings the decision rests on, in the same message as the request.

**Why.** A real three-way failure, not a style preference: the harness can show
the producer only a turn's final message, so analysis written between tool
calls is invisible; a rule against burying the question was read as licence to
strip the findings out of that final message; and the approval gate makes the
question the turn's last beat. The result was a session with near-zero
communication — analysis done, then straight to *"execute the plan?"*.

**Traces to.** G4, G5

**Source.** CONTEXT.md, 2026-07-19: *"The gate message carries the content —
findings are not framing… a conductor session in `~/3of3` showed near-zero
communication — analysis done, then straight to 'execute the plan?'."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-07-19.
Never stated as a requirement.

**Note.** This one has already been implemented twice (conductor's plan-phase
rule and the global instruction file) and is still worth filing, because the
obligation is what survives a rewrite of either.

### C-17 — a change is stated in the vocabulary of using the thing

**Statement (proposed).** Where a change alters what the producer can do, it
shall be stated as what is true now, what changed, and what that means, in the
vocabulary of using the thing. A capability that is removed shall be named as a
loss.

**Why.** Without the second sentence a removal disappears into the good news —
the release notes describe what was gained and the thing that went away is
simply absent, which is indistinguishable from nobody noticing.

**Traces to.** G4, G5

**Source.** CONTEXT.md, 2026-08-02: *"Say it in the user's terms… Any change
altering what the user can do is stated as now / the change / what it means, in
the vocabulary of using the thing; a removed capability must be named as a loss
or it disappears into the good news."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-02.
Never stated as a requirement.

### C-18 — a question the producer alone can answer

**Statement (proposed).** Where a question can be answered from the code or the
records, it shall be answered there rather than asked. A question shall reach
the producer only where answering it needs a decision that is his.

**Why.** His own test: *could they answer it without reading the code?* If not,
it is your call, not theirs. Asking a question whose answer is already
committed spends the scarcest thing in the project on something a machine
could have read.

**Traces to.** G1, G5

**Source.** CONTEXT.md, 2026-08-02: *"Question test: could they answer it
without reading the code? If not, it is your call, not theirs."* Reinforced
2026-08-07 by the entry-gate rule: *"It derives from disk, so it never asks a
question whose answer is already committed. Prefer it over asking."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-02.
Never stated as a requirement.

### C-19 — the parked pile wakes as a phase, never as an interrupt

**Statement (proposed).** Parked work shall be reviewed during design and
planning, and shall not be surfaced during a release that is already sliced.

**Why.** The sequence he gave: roadmap, release plan, review the pile for what
has become more feasible or more relevant, pull candidates into the release.
Once a release is sliced the pile goes invisible and the work is focused solely
on what made the release. It is an event, not a judgement call and not a
notification.

**Traces to.** G1, G7

**Source.** CONTEXT.md, 2026-08-07: *"The someday/maybe pile wakes as a phase,
never as a notification… This is a design-and-planning-phase task only; once a
release is sliced, the pile goes invisible and work is focused solely on what
made the release until 'release shipped' is met."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

### C-20 — a tool is invoked on a declared match, never because it exists

**Statement (proposed).** A tool shall declare the route it serves, and shall
be invoked where the work matches that route. A tool shall not be invoked as an
obligation.

**Why.** It is the general form of a rule the project has already needed twice:
the reachability finding (a skill nobody routes to is an orphan) and the
superpowers finding (a tool that injects *"you MUST use this"* wins on
injection rather than on merit).

**Traces to.** G3, G8

**Source.** CONTEXT.md, 2026-08-03: *"A tool declares the route it serves and
is invoked on match — not because it exists, and never as an obligation. Same
rule for superpowers and every external tool."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

---

## Batch D — release, done, and how options are judged

Eight candidates.

### C-21 — a release is a grouping

**Statement (proposed).** A release shall be defined as a set of work items.
Time shall be attached to a release as an optional property rather than as its
definition.

**Why.** Five factors decide membership and they work three ways: dependency
forbids, user comprehension caps — a release can be too big even when
everything in it is finished, because the bound comes from the receiving side —
and effort, risk and opportunity shape it.

**Traces to.** G6

**Source.** CONTEXT.md, 2026-08-03: *"A release is a GROUPING, not a time axis
(corrects 08-02). Time may be attached later, or never."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

**Note.** The adopted requirement format already reached the same position
independently — selection is release membership held on the release — and OSLC
arrived there too. This candidate is the project-wide form of it. It also has
**no artifact**: nothing groups items into a release today.

### C-22 — done is assembled, never authored

**Statement (proposed).** A work item shall enter the done state only where
each of its parts has been checked against a declaration made before the work.
An item that nothing declared shall not enter the done state.

**Why.** An item nothing declared cannot be checked, so it passes by assertion —
and a state that can be reached by assertion is not a state, it is a claim.

**Traces to.** G6, G1

**Source.** CONTEXT.md, 2026-08-03: *"The DONE condition is ASSEMBLED, never
authored — every item a conformance check against an upstream declaration.
Nothing may be in DONE that nothing declared: it cannot be checked, so it
passes by assertion."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

### C-23 — work is ranked on outcome, and effort is not one of the axes

**Statement (proposed).** Work shall be ranked on consequence — what it costs
not to do it — and on value. Effort shall be used as a tiebreaker and as a
slicing factor, and shall not be used as a ranking axis. Each item shall name
what is lost by not choosing it. Blocked items shall be separated rather than
ranked.

**Why.** An input measure sitting beside outcome measures makes the grid
incoherent and flatters cheap work. Tested rather than argued: on the real
backlog, *repin three repos* rose under effort as a cheap win and fell
correctly under value to pure hygiene.

**Traces to.** G7, G8

**Source.** CONTEXT.md, 2026-08-03: *"Choose what matters next: two constant
axes, both OUTCOME — consequence x value… Effort is not an axis — an input
measure beside outcome measures makes the grid incoherent and flatters cheap
work; it survives as a tiebreaker and as a slicing factor."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

**Note.** `R-0049` (due date, not effort) is the evaluation-matrix instance of
the same principle. This is the general ranking rule.

### C-24 — the colour grammar is fixed, and its meanings do not collide

**Statement (proposed).** In a rendered view, red shall mean cost, green shall
mean producer input, and blue shall mean changed since the producer last
reviewed. Where two apply, red and green shall take precedence over blue, and a
suppressed change shall be reported rather than dropped. The baseline for blue
shall be an explicit review mark rather than a commit or a regeneration.

**Why.** Blue rather than red for deltas because red is load-bearing, and
because everything is new once — red would creep across the board and stop
signalling cost at all. Permanent meanings beat temporary ones on collision.
The baseline is explicit because commits and regenerations both move far more
often than the producer reads.

**Traces to.** G4, G5

**Source.** CONTEXT.md, 2026-08-03: *"Colour grammar: red = cost, green =
Tony's input, blue = changed since last reviewed… Red and green outrank blue on
collision (permanent meanings beat temporary ones) and suppressed deltas are
reported, not dropped. Blue's baseline is an explicit `mark_reviewed`, never a
commit or a regeneration."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

**Note — a live tension the producer should resolve.** `R-0028` says that in
the evaluation matrix the box is never coloured and the mark carries the
verdict. This candidate colours things. The two are compatible only if the
matrix is a declared exception to the colour grammar, which nothing currently
says.

### C-25 — evaluation mechanisms layer in

**Statement (proposed).** An evaluation shall carry marks. Scores shall be
added where options are close. Weights shall be added where criteria differ in
importance.

**Why.** Each layer costs something to maintain and buys nothing when the layer
below already separates the options — so the mechanism is added when it is
needed rather than by default.

**Traces to.** G4, G7

**Source.** CONTEXT.md, 2026-08-04: *"evaluation mechanisms LAYER IN — marks
always · scores when options are close · weights only when criteria differ in
importance."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-04.
Never stated as a requirement.

### C-26 — a score cites its basis and never overrules a mark

**Statement (proposed).** Weights and targets shall be declared before scoring
begins. Each score shall cite the basis it rests on. Where a score and a mark
disagree, the mark shall stand.

**Why.** Declaring after scoring lets the weights be chosen to produce the
answer already wanted, and a score that can overrule a mark makes the mark
decorative.

**Traces to.** G4

**Source.** CONTEXT.md, 2026-08-04: *"weights and targets pre-declared, every
score cites its basis, scores never overrule marks."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-04.
Never stated as a requirement.

**Note.** `tools/design/` enforces most of this already. The obligation is
declared nowhere, which is the same gap as C-01.

### C-27 — an annotation is a queue entry, not an archive entry

**Statement (proposed).** An annotation shall be read, acted on, and removed
within one cycle, and its disposition shall be appended to the annotation log.

**Why.** It dissolved a defect rather than mitigating it: preserved annotations
kept absolute position but not attachment, so a comment slid away from what it
annotated on reflow. A comment that lives one cycle cannot drift, so the
anchoring machinery was never needed.

**Traces to.** G2, G7

**Source.** CONTEXT.md, 2026-08-03: *"Annotations are a queue, not an archive.
Read → act → delete, disposition appended to `docs/plans/annotations/log.md`."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-03.
Never stated as a requirement.

### C-28 — one writer per derived artifact

**Statement (proposed).** A derived artifact shall have exactly one component
that writes it.

**Why.** A second serialization lets two converged trees compare unequal, which
turns a byte-comparison refuser into a source of false refusals — and a refuser
that cries wolf is turned off.

**Traces to.** G1, G2

**Source.** CONTEXT.md, 2026-08-04: *"the single-serializer rule
(`progress_kit.write_pair` is the ONLY writer of the pair — a second
serialization would let converged trees compare unequal)."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-04.
Never stated as a requirement.

---

## Batch E — method and structure

Nine candidates, taken from the decisions that state how work is checked and
how the system is shaped.

### C-29 — the self-check tier is chosen by the weight of the work

**Statement (proposed).** Work shall be checked by the model that produced it.
Work of greater weight shall additionally be checked by that model arguing
against its own output. Critical work shall additionally be checked by an
independent adversarial reviewer.

**Why.** His own three tiers, verbatim: *"doing a thing, check it yourself,
doing a bigger thing, strawman, doing a critical thing, get adveserial model to
check."* The third tier exists for a measured reason rather than a cautious
one: **self-criticism structurally audits only what made it in, so absence is
invisible to it.** On its first run the self-straw-man found five things wrong
with what it had written and missed three things the producer had said that it
had never written; an independent reviewer found all three.

**Traces to.** Law 3, G1

**Source.** CONTEXT.md, 2026-08-13: *"The self-check ladder is REAL and its
tiers have measurably different reach… Triggers are Tony's… the weight of the
work, not the stage and not a cost budget."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-13.
Never stated as a requirement.

**Note.** The trigger is explicitly **not** a cost budget. Any implementation
that sizes the tier by token spend inverts the rule.

### C-30 — agreement between reviewers is not evidence

**Statement (proposed).** Where several reviewers are used to test a
conclusion, they shall be given distinct briefs, each hunting a named failure.
Agreement between reviewers working from one brief shall not be recorded as
evidence.

**Why.** Measured, and it corrected a tactic adopted the same day: three
independent agents agreed on eight category moves, which looked like strong
evidence until attackers showed all three had made the same lexical error.
**Independent readers sharing a brief fail the same way, so their agreement
measures the brief rather than the truth.** Inverted to one drafter and six
attackers, only three of the eight survived.

**Traces to.** Law 3, G2

**Source.** CONTEXT.md, 2026-08-08: *"Convergence of proposers is worthless;
surviving attack is the signal… Consequence for the heavy completeness check:
spend the agents on attackers, not proposers."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-08.
Never stated as a requirement.

### C-31 — capture is continuous and free; ruling is a separate beat

**Statement (proposed).** Durable input from the producer shall be recorded as
a proposed requirement at the moment it is given, without interrupting the work
and without requiring his attention. Ruling that requirement final or dropped
shall be a separate, later act performed by the producer.

**Why.** His words, and the sharp half is the second one: *"it should be
recorded as a potential requirement and then confirmed or rejected"*, then
*"it should alert and warn and if the user wants to ignore and continue they
must approve — but really its a process issue, that should only happen if we
get requirements wrong?"* Evidence that one beat cannot work: all twenty-eight
of one session's requirements arrived mid-conversation, so a beat riding task
framing would have caught none of them.

**Traces to.** G2, G1

**Source.** CONTEXT.md, 2026-08-07: *"The promotion beat is TWO beats, and the
machine's role is to DETECT that the first one didn't run — not to perform
it."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

**Note.** The detector's firing frequency is the process-health measurement —
his *"that should only happen if we get requirements wrong"* means a well-run
session never sees it. That property should survive into whatever implements
this.

### C-32 — a recovered requirement stays marked as recovered

**Statement (proposed).** A requirement transcribed from an existing record
rather than stated by the producer shall carry a permanent marker saying so,
and shall be keyed in batches by family rather than one at a time.

**Why.** The risk it answers: retrofitting manufactures requirements nobody
stated, and a fabricated row cannot be told from a real one. Get the marking
wrong once and the register is untrustworthy with no way back.

**Traces to.** G2, G4

**Source.** CONTEXT.md, 2026-08-07: *"provenance is marked permanently so a
transcribed decision stays distinguishable from a stated requirement forever
(get this wrong once and the register is untrustworthy with no way back); and
the producer's key lands on batches by category."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

**Note.** This file is the first thing that would be governed by it.

### C-33 — the project type is the project's state, and a goal advances it

**Statement (proposed).** A project shall declare one type, chosen at the start
where the project has not already begun. Achieving a goal shall advance that
type to the next. A work item shall inherit the project's current type rather
than declaring its own.

**Why.** His words: *"the correct project type that can increment upon goal
achieved to the next appropriate project type and avoid the confusion."* It
dissolves a retrofit cost rather than paying it — there are no typeless work
items to fix, because the type was never per-item.

**Traces to.** G3, G6

**Source.** CONTEXT.md, 2026-08-07 (annotations on `project-types.excalidraw`).

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

**Note.** Its stated consequence is a subtraction: `route` and `Rigor level`
become derived from the type, so three declarations collapse to one.

### C-34 — a capability is written for a project that is not this one

**Statement (proposed).** A capability shall be specified in terms of what it
gives a consuming project. Anything specific to a project — a category scheme,
a slug, a threshold — shall be declared by that project rather than fixed in
the tooling.

**Why.** His correction, verbatim: *"KERD is the skill that people use to build
things. Kerd needs to give those projects this capability (perversely we need
it to build Kerd too) so I am talking about the scope of the skill here all the
time."* Using the capability here is evidence it works — never the definition
of what it is.

**Traces to.** G8, Law 1

**Source.** CONTEXT.md, 2026-08-07.

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-07.
Never stated as a requirement.

**Note.** It is a repeatable mistake precisely because this repo is the one on
screen. `R-0036` and `R-0038` are the two instances already filed; this is the
rule they are instances of.

### C-35 — the vocabulary of roles is fixed and each name means its own word

**Statement (proposed).** The four roles shall be named producer, composer,
conductor and players, and each name shall carry the meaning that word already
has outside this project.

**Why.** First-party evidence that a vocabulary failed: asked to describe the
model he had ratified, the producer used both role names swapped, in one
sentence. His own naming of his seat closed it: *"I am the producer, I have the
idea or input to the work and approval to ensure we are making the show we
want."*

**Traces to.** G5, G4

**Source.** CONTEXT.md, 2026-08-07/v0.92.0.

**Provenance.** Transcribed from a CONTEXT.md standing decision. Never stated
as a requirement.

**Note.** Its lesson generalises past role names, and that may be the more
valuable requirement: a term the producer cannot reproduce unprompted is not a
shared term. The blocker phrased as *"driver item"* — vocabulary he said
*"means nothing to me"* — stalled a decision for three days for exactly this
reason.

### C-36 — a living document never writes a bare reference to a checked pattern

**Statement (proposed).** Where a document must show a form that a checker
detects by pattern, it shall use a placeholder that the checker does not match.

**Why.** A checker detecting by pattern is asserted by any prose quoting the
pattern — so a document illustrating the wrong form triggers the rule about it.
The sweep has no waiver mechanism by design.

**Traces to.** G2

**Source.** CONTEXT.md, 2026-08-04: *"R3 quoting convention: living docs never
write a bare skill reference, even to illustrate it… the same class as the
substring-marker gotcha."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-08-04.
Never stated as a requirement.

**Note.** The machine-layer sibling shipped later — fence-aware parsers, where
a line inside a code fence is content rather than structure. One rule, two
layers.

### C-37 — state, work and history are three things with one file each

**Statement (proposed).** What is currently true, what remains to be done, and
what happened shall each be held in one file, and no file shall hold more than
one of them. The record of what happened shall not be rewritten.

**Why.** Completeness comes from full-fidelity history plus the version history
of the state file, so nothing is lost by keeping the read set small. The sharp
edge, and the failure it prevents: **the state file must never become a diary.**

**Traces to.** G2, G5

**Source.** CONTEXT.md, 2026-07-03: *"State/work/history are different things —
one file each… Completeness comes from full-fidelity session logs + git history
of CONTEXT.md (pruned content is never lost); efficiency comes from reading
less, not storing less."*

**Provenance.** Transcribed from a CONTEXT.md standing decision, 2026-07-03.
Never stated as a requirement.

**Note.** `R-0024` states the boundary records everything agreed; this states
where each kind of thing goes. Related, not duplicate.

---

## Coverage — all 88 standing decisions accounted for

**The Backlog row says 74 standing decisions. There are 88.** Counted from
`CONTEXT.md`'s `## Key Decisions` section at 2026-08-14. The number grew while
the row sat, which is worth knowing before anyone plans against it.

Every one is classified below, so this file can be checked for what it *skipped*
and not only read for what it contains. Five verdicts:

- **candidate** — recovered above, with its `C-nn`
- **already filed** — the register holds it; the reference is named
- **history** — a record of what was built, cut or decided-and-done; there is no
  standing obligation left to file
- **dead** — superseded, or killed at the 2026-08-14 triage
- **REMAINDER** — it yields a requirement and **it is not written yet**

| # | Decision (abbreviated) | Verdict |
|---|---|---|
| 1 | Law 4 and its ordering rule | not a requirement — it is a law |
| 2 | The requirements capability is built | history |
| 3 | The format refuses ambiguity | already filed — `requirement-shape.md` rule 14 |
| 4 | The reset | history |
| 5 | The self-check ladder is real | **C-29** |
| 6 | AU7/AU8 shipped | history |
| 7 | The trace gap fills top-down | history (a plan, not an obligation) |
| 8 | Conductor advises the pair | already filed — R-0023 |
| 9 | Category taxonomy is prefix + tags | dead — taxonomy killed 2026-08-14 |
| 10 | The twenty categories' definitions | dead — same |
| 11 | Convergence is worthless; attack is the signal | **C-30** |
| 12 | The completeness check is tiered | already filed — R-0050, R-0051 |
| 13 | Build the register; adopt none | history (its re-open condition is live) |
| 14 | The promotion beat is two beats | **C-31** |
| 15 | Archaeology: never from session logs | **C-32** |
| 16 | Project type is state; a goal increments it | **C-33** |
| 17 | The alignment gate is a shared structure | already filed — R-0006 |
| 18 | Never route to superpowers | dead — R-0039 killed |
| 19 | Funnel state belongs to the user's project | already filed — R-0036, R-0038, R-0042 |
| 20 | "Capability" means what the skill gives users | **C-34** |
| 21 | The plan-approval gate is deleted | already filed — R-0014, R-0015 |
| 22 | The four roles | **C-35** |
| 23 | The funnel has no driver | history |
| 24 | The division of labour | **C-14** |
| 25 | Root cause: human input leaves no artifact | observation — carried as C-07's note |
| 26 | 90% of input is the thinking layer | observation — same |
| 27 | The someday pile wakes as a phase | **C-19** |
| 28 | A gotcha surfaces where its subject is | **C-12** |
| 29 | switch-fidelity slice 1 built | history + **C-10** |
| 30 | Refusal surface is prompt-layer in consumers | history (an accepted risk) |
| 31 | time-awareness done | history |
| 32 | trim cut | history |
| 33 | release-closeout done | history |
| 34 | The gate parsers are fence-aware | history + **C-36** (same rule, machine layer) |
| 35 | vault-unhook done | history |
| 36 | rigor-level slice 1 built | history |
| 37 | rigor-level framed and sliced | history |
| 38 | AU5 live — grounding-was-read | **REMAINDER** — the grounding obligation is unfiled |
| 39 | The journey view parked | history |
| 40 | The staleness refuser is live | history + **C-28** (its single-serializer rule) |
| 41 | The graduation map fires zero graduations | history |
| 42 | The evaluation matrix is machine-checked | history |
| 43 | Talk moments name their format | **REMAINDER** |
| 44 | mode cut | history |
| 45 | sherpa cut | history |
| 46 | capturerequirements cut | history + **C-08** (dead solutions stay dead) |
| 47 | Interrogate is the tiered risk ledger | history |
| 48 | The R3 quoting convention | **C-36** |
| 49 | The ladder vocabulary is canonical | **REMAINDER** |
| 50 | Rules born in the specs | **C-25**, **C-26**, **C-07**, **C-04** + **REMAINDER** (grounding) |
| 51 | Post-walk tooling: six decisions | history |
| 52 | Skill changes are defined after the walk | history |
| 53 | The walk's late findings | **REMAINDER** — four talk rules, state-in-declared-artifacts, liveness |
| 54 | The design rung is one function | **REMAINDER** — the package and its two-key GO |
| 55 | Contract: no human gate when measurable | **C-14** + **REMAINDER** (the escalation contract) |
| 56 | Build: two functions + a property | **C-06** + **REMAINDER** (done = measured against every relevant spec) |
| 57 | No solution vocabulary during the walk | history |
| 58 | Consequence x value | **C-23** |
| 59 | A release is a grouping | **C-21** |
| 60 | A risk without a countermeasure is a blocker | **C-01** |
| 61 | What we ruled out is its own artifact | **C-08** |
| 62 | Hold product truth: cut | history (return condition named) |
| 63 | A requirement row has four fields | dead — superseded by the six-element shape |
| 64 | Date records, never living documents | **C-09** |
| 65 | The colour grammar | **C-24** |
| 66 | Annotations are a queue | **C-27** |
| 67 | A tool declares the route it serves | **C-20** |
| 68 | Kerd's gap is above the contract rung | history |
| 69 | Don't adopt the four frameworks | history (a ruled-out record) |
| 70 | Nothing can refuse, and nothing counts | **C-06** |
| 71 | Design is agreed in diagrams | already filed — R-0006 supersedes it |
| 72 | conductor-boundary slice 1 built | history |
| 73 | Conductor commits its work; switch keeps the boundary | **REMAINDER** |
| 74 | Say it in the user's terms | **C-17**, **C-18** |
| 75 | Conductor re-seated: four roles | **C-35** |
| 76 | The gate message carries the content | **C-16** |
| 77 | Model advisory replaces the toggle | already filed — R-0023 |
| 78 | Switch-in ends with a numbered pick-list | **REMAINDER** |
| 79 | State, work, history — one file each | **C-37** |
| 80 | Closure inference is a list, never a prompt | **REMAINDER** |
| 81 | kivna save writes without approval | **REMAINDER** — with 83 |
| 82 | Conductor's decisions live in CONTEXT.md | **REMAINDER** |
| 83 | The vault is never read at switch-in | **REMAINDER** — with 81 |
| 84 | Older logs are archive | **C-11** |
| 85 | Validate is risk-driven, not menu-driven | **REMAINDER** |
| 86 | Memory tools: adopt none | history (a ruled-out record) |
| 87 | skriv voice profile held | history (blocked) |
| 88 | TODO is forward-only | **C-37** |

### The tally

| Verdict | Count |
|---|---|
| candidate, written above | 37 covering 30 decisions |
| already filed in the register | 8 |
| history — nothing left to file | 34 |
| dead — superseded or killed | 4 |
| observation, not an obligation | 2 |
| **REMAINDER — yields, not yet written** | **13** |

**The remainder is named rather than left implied.** Thirteen decisions still
carry an unfiled obligation: the grounding-declaration rule (38, 50), talk
formats per moment (43), the ladder vocabulary (49), the walk's four talk rules
and state-in-declared-artifacts (53), the design package and its two-key GO
(54), the escalation contract (55), done-measured-against-every-relevant-spec
(56), who commits what (73), the pick-list (78), closure inference (80), the
vault's opt-in contract (81, 83), conductor's decision home (82), and
risk-driven validation (85).

They stopped here because the batch was long, not because they were judged
lower value — several are stronger than entries already written. **Do not read
the tally as "the archaeology is done".**
