---
route: new
stage: framed
story: proposal
concerns:
  - concern: why the driver sits above conductor rather than inside it
    viewpoint: nested
    view: docs/design/funnel-driver/why-an-umbrella.html
    approval: Tony, 2026-08-23 · fp:54f84887b8b8
  - concern: how one gate behaves, end to end
    viewpoint: swimlane
    view: docs/design/funnel-driver/gate-loop.html
    approval: Tony, 2026-08-23 · fp:47883502cf4b
---

# The funnel has no driver — nothing walks an item from idea to launch

## Value

Tony's statement of what the whole Kerd rewrite was for (2026-08-07, given
after four hours of building instruments made it clear it had never been
written down):

> The actual idea was to rework or remove the Kerd skills to provide an
> orchestrated flow from idea/problem to launch with a defined funnel and goal
> and loop structure.

And on shape, the same day: *"not a skill per stage no — one skill for all,
and remove dependencies where we can do better (superpowers etc)"*, arrived at
by *"evaluating what we have"* rather than by designing fresh.

**This is not a new idea. It was decided, specced, and never built.**
`docs/design/conductor-role.md` was written 2026-08-04 out of the requirements
walk. Its own words: *"CONDUCTOR — the driving role (this spec)"*, with a
graduation map of which functions move into it and when. Post-walk decision 6
ratified it. Nothing was built.

**Why it stalled is the point, and it is not that anyone forgot.** There is no
`docs/product/conductor-role.md`. It has no frame, no risk ledger, no release
slice, no gate record, and it is not among the 18 slugs on the board. The
funnel never routed it, the gates never demanded anything of it, and the
progress render never showed it as unbuilt. A design-rung artifact for a work
item that never entered the funnel, sitting where nothing reads it.

That is the root cause of `switch-fidelity` at the highest altitude in the
system: **the decision to give the funnel a driver is human input that was
recorded properly and then vanished, because the only machinery capable of
noticing it hadn't been built tracks nothing that did not enter through a
frame.** This document is the frame that was missing.

### Value, in units

- **Funnel stages with an owner: 5 of 8 → 8 of 8.** Three stages have no owner
  in any skill. `grep -rn "Release slice" skills/` returns zero hits;
  `grep -rn "docs/design/" skills/` returns one, and it is an audit target.
  Nothing in `skills/` writes `docs/product/<slug>.md` — that job was
  de-skilled at v0.73.0 when capturerequirements was cut, moved to "the frame
  flow", and the flow has no owner.
- **Skills that know the funnel exists: 2 of 9 → the driver.** Measured
  2026-08-07: `interrogate` (8 references) and `switch` (7, only since this
  morning). `conductor` scores 3 and all three are false positives — "gate"
  meaning an approval beat, "step" meaning a plan step. Five skills score zero.
- **Graduation triggers that have fired and shed nothing: 1 → 0.** The entry
  gates landed at v0.69.0 and run in CI on every push; conductor's pre-flight
  inventory still asks the human for what `gate.py route` prints without
  asking anyone.
- **Standing decisions contradicted by shipped skill text: 1 → 0.** The
  unconditional plan gate.
- **Work commits carrying machine-readable piece progress: 0 → every one.**
  `git log --format=%B -50 | grep -c '^Piece:'` returns 0, so the only
  falsification-resistant progress signal in the repo is unfed.

Explicitly *not* value here: a bigger conductor. If the driver ends up larger
than the sum of what it absorbs, the evaluation was wrong.

## The mechanism — DECIDED 2026-08-23: an umbrella ABOVE conductor

**Everything below the gap list was written on the assumption that the driver
arrives by moving functions *into* conductor.** That assumption is dead. The
change is the producer's:

> if its working as is today (maybe not ideal though, but working) maybe we
> should have this as a separate branch/command or an overriding one (umbrella)
> for what we have today … that forces the stages and uses conductor and the
> other tools withing the skill, without breaking conductor basic as it is now
> … then we can keep building one bit at a time under that umbrella, while
> keeping what is there useful still

**Why this is a different answer rather than a rephrasing.** The two killer
risks below pull in opposite directions, and that is what made the slicing hard:
*breaking the seedbed* argues for changing conductor as little as possible,
*obliging nothing* argues for changing enough to matter. An umbrella that
**calls** conductor without **changing** it answers both at once — there is no
edit to conductor, so there is nothing to break, and the umbrella **forces** the
stages rather than advising them.

**The rule this is built under:**

> The umbrella may CALL conductor, but must never REQUIRE conductor to change.

Without this line stated, "umbrella" becomes "graduation" over a few months of
individually reasonable conveniences and nobody notices the crossover.

**Proportionality becomes the door you walk through, not a setting.** A repo that
will never pass MVP keeps plain conductor and pays no process cost at all; a
product that needs the funnel enters through the umbrella — the concrete answer
to *"without it becomeing a 100year project"*. Consistent with the 2026-08-07
shape rule, *"not a skill per stage no — one skill for all"*.

**NAMED 2026-08-23: Drive — `/kerd:drive`, `skills/drive`.** Tony's call.
`concert` was refused as an invented name; `product` names a domain rather than
an action; `stagegate` is gate-centric and corporate. Drive names the active
thing — guide, keep moving, steer, hold accountable. The slug stays
`funnel-driver`, because slugs name work items and not skills.

**How it works is the design's business, not the frame's:
`docs/design/funnel-driver.md`.** That package carries the item-versus-session
split, what Drive is, how it calls conductor, where the question set lives, how
the completeness check reads it, and the canonical language below.

## The canonical language — DECIDED 2026-08-23

Drive moves things that are not products. The vocabulary is **work item** (the
thing Drive moves), **work record** (its living artifact), canonically at
`docs/work/<slug>.md` — with `docs/product/` named as current physical storage
that has not migrated yet, never as the concept.

**`project type` is superseded and retired as a field name**, split into three
independent axes: **work type** (what kind of thing this is — software change,
enhancement, content plan, business plan, document, repair), **route** (how it
enters the ladder: `new | problem | spike`), and **lifecycle position** (where
the thing is in its life — the only axis that advances). The fifteen written
types become migration evidence rather than canon. Reasoning and the eight/seven
split: `docs/design/funnel-driver.md`.

## How one gate behaves — DECIDED 2026-08-23

Agreed by walking a drawing, and corrected by the producer at five of its eight
steps. **In:** a sentence plus whatever material the person already has —
documents, links, pictures — read and played back, so context arrives as
artifacts rather than as an interrogation. **A short question set**, sized to do
two jobs: judge whether the idea is worth pursuing, and become the first
requirements. **Then the loop, which IS the gate:** start the package, open it on
the person's screen, shape the idea back at them, take their comments, reshape.
*"nearly, but change this"* is the normal answer, and **a comment is not a
rejection**. **Out: a package the person recognises, agreed for now — NOT
locked** — *"idea still shapng at this point though … not locked."* Every picture
already agreed travels forward.

**One list decides what gets asked, what counts as finished, and what is shown**
— the producer's correction, *"this needs to be based on step 2 as well right?"*,
plus his third use: *"now > x, next Y, after Z"*. The set is **data the person
owns and edits before starting**, never skippable during (*"yeah i was wrong on
skip"*), and the work type is **declared, never inferred** — a guessing system is
wrong about a third of the time and fails silently. Mechanics and homes:
`docs/design/funnel-driver.md`.


## Grounding

- docs/design/conductor-role.md — the 2026-08-04 spec this builds; the design rung is already done
- tools/gates/README.md — the funnel vocabulary and the gate record schema
- docs/design/funnel-steps.md — the steps inside each stage, defined 2026-08-07
- skills/conductor/SKILL.md — the seedbed being changed, and the thing a wrong edit breaks
- docs/product/shared-memory.md — the root cause this item is an instance of
- docs/plans/2026-08-04-post-walk-tooling.md — decision 6, which seated the driving role
- CONTEXT.md — the four-role seating, the human-gate map, derived-from-disk, no-rip

## The gap list

Measured 2026-08-07 by five parallel readers against the spec, the skill, the
funnel's machine surface, the other eight skills, and every standing decision.

### Gap 1 — RESOLVED 2026-08-07: the conductor drives. The role NAMES are the real defect.

**Tony, closing it:** *"I think I used orchestrator when I meant conductor
earlier. What I thought we had decided was that the conductor would drive from
idea to goal and manage the other roles as sub agents, including the composer
who writes the specs etc."*

So the seat matches post-walk decision 6 and `conductor-role.md` unchanged: the
**conductor** is the driving role, it drives **idea → goal**, and it manages
every other role as subagents it calls — including whichever agent writes the
specs.

That also reconciles the two ladders, which are not in conflict once read
correctly:

```
Tony
  ↑
intent-holder — an agent above the conductor with declared adjustment power.
  DOES NOT EXIST. Graduation row 6's trigger has not fired.
  ↑
CONDUCTOR — drives idea → goal
  ↓ calls, as subagents
the spec-writer  ·  players  ·  tools
```

The intent-holder sits **above** the conductor; the spec-writer is **called
by** it. They were never the same seat — the frame's first draft treated them
as a contradiction because nothing on disk says which direction each sits.

**The real defect this exposed is the naming.** Kerd assigns *Composer* to
Tony and *Orchestrator* to the agent that writes specs. Tony used *composer*
for the spec-writer and *orchestrator* for the driver — both swapped, in one
sentence, by the person who ratified the names at v0.66.0. That is first-party
evidence that the vocabulary does not survive contact with its own author, and
a driver skill whose whole job is coordinating these roles cannot afford
names that invert under use.

Musically his usage is the correct one: a composer writes the score, a
conductor directs the performance. The current assignment fights the metaphor
it borrowed.

**RESOLVED and shipped, v0.92.0.** Tony named his own seat: *"I am the
producer, I have the idea or input to the work and approval to ensure we are
making the show we want."* That completes the metaphor and every name now does
the job its word already means:

| Role | Who | Owns |
|---|---|---|
| **Producer** | Tony | the idea or the input, and the approvals |
| **Composer** | a top-tier model (Fable), called as a subagent | the score |
| **Conductor** | the session model (Opus) | the performance |
| **Players** | subagents at a sized model and effort | one step each |

Swept across 9 living files, 67 replacements, ordered composer→producer before
orchestrator→composer so the new names could not be overwritten by the second
pass. Session logs and gate records are immutable and keep their original
wording. This document is deliberately **not** swept: the quotations above are
the record of why the rename happened, and rewriting them would erase the
evidence.

Nothing about the architecture changed — the composer was always Fable, the
conductor always Opus, the players always sized. Only the labels were wrong.
The model tiers are now stated in the roles table rather than left in prose.

**Scope, stated as an assumption:** the driver covers **idea → goal**, seven
stages. `Live`/loop is excluded, because `funnel-steps.md` leaves that stage
deliberately empty — no flow was ever drawn for it — and the unattended tempo
that would live there is blocked behind its own undefined gate.

### Gap 2 — a graduation trigger fired at v0.69.0 and nothing shed

Graduation row 1 (`conductor-role.md:47`): pre-flight inventory moves to the
entry gates when the mechanical gate check lands — files, front matter,
sections, CI-able.

It landed. `tools/gates/gate.py` plus `.github/workflows/gate.yml` have run on
every push since v0.69.0. And `SKILL.md:81` still reads *"Pre-flight inventory:
Ask the user for anything execution will need"*.

Verified live: `gate.py route <slug>` prints the exact missing-input list
without asking a human anything.

Second-order: `docs/design/entry-gates.md:57-58` still calls conductor's
inventory the gate's *"only living instance"*. That statement is now false and
has been for three weeks.

### Gap 3 — a standing decision is contradicted by shipped skill text

Graduation row 4 (`conductor-role.md:50`): the plan-gate approval is **deleted,
not moved** — replaced by an upstream design-package GO (two keys) plus
downstream pieces the machine can measure. Reinforced twice: `funnel-steps.md`
Spec'd step 5, *"approval by machine key alone — no human gate where the
machine can measure"*, and the CONTRACT decision in CONTEXT.md.

`SKILL.md:138` and `:211` make it unconditional: *"Wait for user approval
before executing. Do not proceed until the user confirms the plan."*

This is not an unbuilt decision. It is a live contradiction, shipped, and it
gets rediscovered rather than resolved.

### Gap 4 — the only falsification-resistant progress signal is unfed

`conductor-role.md:32-33` makes work commits the liveness signal, and
`progress-view.md:48` names the strip's source as the work order's piece
checklist plus `git log`.

Conductor commits per verified task and stages by name — but writes no
machine-readable link to a piece. `grep -rn 'Piece:' skills/` returns nothing;
`git log --format=%B -50 | grep -c '^Piece:'` returns 0. `progress_kit.py`'s
trailer mode exists and has never received a single trailer.

This is the cheapest real gap in the list: one line, additive, no graduation,
no rule-4 conflict.

### Gap 5 — three funnel stages have no owner in any skill

Not "a weak owner" — none.

| stage | artifact nothing writes | evidence |
|---|---|---|
| frame | `docs/product/<slug>.md` | de-skilled at v0.73.0 when capturerequirements was cut; job moved to "the frame flow", which has no owner |
| design | `docs/design/<slug>.md` + the GO record | `grep -rn "docs/design/" skills/` → one hit, an audit target in slainte |
| contract | `## Release slice` | `grep -rn "Release slice" skills/` → zero hits |

Every item that has walked the funnel wrote these by improvisation.

### Gap 6 — the driver's own position oracle would dirty the tree

`tools/diagram/progress.py` writes `docs/plans/progress.{excalidraw,svg,html}`
on **every** invocation including `--json` (`progress.py:38-43`); there is no
read-only flag. A driver polling position mid-build would contaminate the
collateral diff read that conductor's verification gate depends on
(`SKILL.md:236`).

`gate.py route` is verified read-only and is the correct oracle. Naming this
now prevents a build that looks right and quietly breaks the safety check.

### Gap 7 — two spec clauses cannot be built as written

- **"two-tier access"** (`conductor-role.md:49`) is a required property of the
  work order and appears in **no other file in the repo**. Its acceptance
  criterion is not derivable from disk. A trigger nobody can test never fires.
- **The unattended tempo** (`conductor-role.md:34-37`) is enterable only
  through the loop's gate. `loop` is the eighth stage, and `funnel-steps.md`
  leaves its steps deliberately empty because no flow was ever drawn for it.
  Blocked, not merely unstarted.

Also unreconciled: the spec's central instrument is a **work order**. That
string appears in no skill file. Conductor dispatches from a spec file at
`docs/plans/YYYY-MM-DD-<slug>-spec.md`. They may be the same instrument under
two names, or a real gap — the spec names properties (per-piece checks plus
two-tier access) the spec file does not carry, so they cannot simply be assumed
identical.

### Gap 8 — shipping an instrument produces nothing unless a role is obliged to use it

Direct precedent, measured the same day: the design instrument shipped complete
with 11 pieces landed, and `matrix.py audit` reports **clean (0 matrices)**.
`switch-fidelity` shipped as v0.90.0 with **zero gate records** — invisible to
every machine surface in the repo.

A driver that reads the funnel but obliges nothing repeats this at larger
scale. Every slice must pair the instrument with the obligation that consumes
it.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Editing conductor breaks the only working instance of half the system's functions | yes | the daily working protocol goes down in three repos at once with no fallback, and the damage is invisible until a session tries to plan | medium — every edit to a 353-line load-bearing skill carries it, and the skill is in active daily use | conductor-role.md transition rule 4 states it directly: breaking it breaks the only working instance of half the system's functions; ~/leru holds 6 spec files written under this protocol | countermeasure - permanent | **RETIRED BY CONSTRUCTION 2026-08-23 — the driver is an umbrella ABOVE conductor and never edits it, so there is no edit to get wrong.** ~~one graduation at a time, and only a row whose trigger has demonstrably fired; every funnel-touching edit uses switch's proven conditional idiom; additions and guarded substitutions only~~ — that discipline was load-bearing on every future edit forever, and is now unnecessary rather than merely satisfied | the first slice that requires a change INSIDE conductor re-argues this row in full |
| The four role names invert under use — Composer is assigned to the human while the spec-writing agent is the Orchestrator | no | the driver's whole job is coordinating these roles, and instructions written in names that swap under reading will be misread by the model exactly as they were by their author | high — observed first-party on 2026-08-07, both names swapped in one sentence by the person who ratified them at v0.66.0 | Tony: "I used orchestrator when I meant conductor... including the composer who writes the specs"; conductor-role.md's own ladder avoids "composer" entirely and names Tony as himself | countermeasure - temporary | slice 1 touches no roles table and no role name, so nothing is built on the ambiguous vocabulary; the rename is queued as its own cross-cutting item under the standing grep-sweep obligation | the first slice that must instruct the driver to call another role by name — at that point the rename lands first or the instruction inherits the defect |
| A driver that reads the funnel but obliges nothing leaves the machinery unwalked | yes | the whole item delivers a better-informed skill and zero behaviour change, which is the failure this repo has already shipped twice | high — measured twice on this repo: 0 evaluation matrices against built and CI-enforced machinery, and switch-fidelity live at v0.90.0 with zero gate records | matrix.py audit reports clean with 0 matrices; docs/gates/ holds no record for switch-fidelity | countermeasure - permanent | every slice pairs the instrument with the obligation that consumes it — the gate becomes the inventory's source rather than an optional reference, and the commit trailer makes skipping it visible as a stalled progress strip | the first slice shipping a capability with no obligation attached re-argues this row |
| Prompt-layer instruction is not a call — a skill telling the model to run gate.py is advice it can skip | no | funnel awareness reads as a guarantee in the skill text while being a suggestion in practice, and in consuming repos the tool does not exist at all | high — this is the measured status quo, named as a standing limit already | CONTEXT.md 2026-08-06: the refusal surface is Kerd's own and prompt-layer-only in consuming projects is the intended contract; grep of skills/ for tool invocations returns zero | accepted | | the first time the funnel is driven in a repo that is not Kerd |
| The queued funnel rename silently rewrites the authority model | no | the role ladder becomes a role funnel by accident and the seat diagram changes meaning without a decision | medium — the rename is queued and conductor-role.md uses rung and ladder to mean authority, not work position | funnel-steps.md queues the cross-cutting rename; conductor-role.md lines 9, 12 and 52 use the words for the seat, not the stage | countermeasure - permanent | an explicit out-of-scope line lands in conductor-role.md before any sweep runs, and the 2026-08-06 standing rule already requires a cross-cutting grep sweep at design time | the sweep touching any line of conductor-role.md re-argues this row |
| Two spec clauses cannot be built as written — two-tier access is undefined and the unattended tempo is gated behind an undefined stage | no | a build either stalls at those rows or invents a meaning, and an invented meaning silently becomes the standard | certain — both are on disk today with no resolving definition anywhere | two-tier access appears in no file but conductor-role.md:49; funnel-steps.md leaves Live deliberately empty | countermeasure - permanent | refuse to build either row; amend the doc to mark the trigger untestable until defined, rather than resolving by guess | the first attempt to build row 3 or the unattended tempo re-argues this row |

## Killer risk, read out

Two killers, and they pull in opposite directions, which is what makes the
slicing hard rather than merely careful.

**Breaking the seedbed** argues for changing as little as possible. Conductor
is the only working instance of half the system's functions, in three repos,
and its own spec says so.

**Obliging nothing** argues for changing enough to matter. This repo has twice
shipped complete, CI-enforced machinery that produced zero artifacts, because
nothing was obliged to use it.

Both have permanent countermeasures and the countermeasures are compatible:
**take only graduations whose trigger has demonstrably fired, make each one an
addition or a guarded substitution, and pair every one with the obligation that
consumes it.** A slice that changes conductor without obliging anything, or
that obliges something by removing a working behaviour, fails one killer or the
other.

## Release slice

Rigor level: mvp

**SLICE 1 SHIPPED at v0.91.0** — the entry gates took the pre-flight inventory
and work commits gained the `Piece:` trailer. It was cut under the old mechanism
(graduations into conductor). Everything after it is re-cut under the umbrella
decision of 2026-08-23 above.

**Slice 2 — one gate's question set, written by hand, used once for real.**
The smallest thing that proves the loop and leaves something behind.

- **The question set for the FIRST gate**, as a file in the repo rather than
  prose in a skill. Short — enough to judge the idea, and enough to become the
  first requirements.
- **The completeness check reads that same file**, so what is asked and what
  counts as finished cannot drift apart.
- **Run it once on a real item**, end to end, and keep what it produces.

**Why the first gate and not another:** of the funnel's eight stages, the three
with no owner in any skill are `frame`, `slice` and `design` — the three at the
front, where a person starts. The producer's answer when asked which gate to
walk first: *"all of them in order? we start at the start of the funnel and work
though it?"*

**Deliberately excluded from slice 2, each with its reason:**

- **A template system.** There is no question set for any gate yet. Building the
  abstraction before the first instance is the failure this repo has shipped
  twice — 27 hand-written diagram generators before anyone reached for a toolkit,
  and a 20-item topic checklist killed because it measured at zero. Write one,
  use it, then see what generalises.
- **Inferring the project's shape.** Refused on the 33.8% misclassification
  evidence above. Declared, never inferred.
- **Opening it in the browser.** The showing step is real and agreed, but the
  requirements editor already proves that shape exists and works; slice 2 does
  not need to rebuild it to prove the question set.
- **The remaining seven gates.** One loop proven beats eight declared.
- **Anything inside conductor.** The rule of the mechanism section: call it,
  never change it.

**Slice 3 — the `docs/work` migration.** Canonical storage moves from
`docs/product/<slug>.md` to `docs/work/<slug>.md`. **Measured 2026-08-23 so
nobody re-derives the cost: ~180 references** — `tools/gates/kit.py` 127,
`gate.py` 9, `fidelity.py` 3, two skill files (`conductor`, `interrogate`), 40
files under `docs/design/` including text baked into `.excalidraw` and `.svg`
renders, plus `README.md`, `CLAUDE.md` and `docs/playbook.md` — and a 20-file
move. **The board derives every slug from `docs/product/*.md` filenames, so a
half-done migration turns the render red.** Deliberately not ridden into the
design slice: it would have swallowed it.

**Slice 4 — split the fifteen project types onto their three axes.** Eight are
lifecycle positions, seven are work types wrongly filed, and the non-software
work types (content plan, business plan, document) have no entry at all. Retires
the `project type` field name. Depends on slice 3 only for where the templates
live.

---

**Slice 1, as originally cut and now shipped** — kept below as the record of what
was actually built, not as pending work. Deliberately seat-neutral: every step is
true whichever role ends up driving.

- **This document.** The item becomes tracked, appears on the board, and is
  visible as unbuilt — which is the single thing whose absence killed the
  2026-08-04 spec.
- **Correct two false statements on disk.** `entry-gates.md:57-58` calls
  conductor's inventory the gate's only living instance; that has been false
  since v0.69.0. `conductor-role.md:49` names an untestable trigger; mark it as
  such rather than leaving a clause nobody can act on.
- **Protect the spec from the queued rename.** An out-of-scope line, before any
  sweep runs, so "rung" and "ladder" keep meaning authority in that file.
- **Graduation row 1: the entry gates own the pre-flight inventory.** Conductor
  stops asking the human for what `gate.py route` prints. Written with switch's
  conditional idiom so a repo without the tool degrades to today's exact text.
- **The `Piece:` trailer on work commits.** One line, additive, feeding the
  progress machinery that has never received a trailer.

**Deliberately excluded, each with its reason:**

- **The role rename.** Gap 1 resolved the seat but exposed a naming defect
  that inverts under use. Renaming is cross-cutting and owes a grep sweep;
  slice 1 touches no role name, so nothing is built on the ambiguity.
- **Removing the plan gate.** Gap 3 is a real contradiction, and no-rip
  requires the replacement to prove itself in real use first. Zero design GO
  records exist for any driver item, so the replacement has never run. Recorded
  with its own trigger so it stops being rediscovered.
- **Owning the three unowned stages.** The largest and most valuable change,
  and it cannot be seat-neutral.
- **The work order, two-tier access, and the unattended tempo.** Blocked by gap
  7.
- **Any cut of another skill.** The coverage table is evidence for that
  decision, not the decision. It lives in the design doc.

## What we ruled out

**Re-evaluating the nine skills before building.** Proposed by the model and
rejected by Tony, 2026-08-07: *"but we did all this with fable… we reviewed
each skill and cut or updated them to support the funnel approach, we updated
the roles etc — now we are back at the start."* Correct on the record: the
walk happened, four skills were cut, the roles were updated, and the driving
role was specced. Re-running the evaluation would have re-derived a conclusion
already reached and deepened the exact loop he was naming.

**Making the evaluation matrix the centrepiece.** Same exchange: *"the eval
matrix is a tool and method for making and evaluating tools or solutions etc —
it's not the whole answer, just a tool to help define the answer."* The model
had elevated an instrument into a plan. The matrix remains the right form for
the coverage table when a cut is actually proposed.

**A skill per funnel stage.** Rejected by Tony the same day — *"not a skill per
stage no, one skill for all"*. Eight skills would multiply the reachability
problem that already lets superpowers win: `using-superpowers` injects "you
MUST use this before any creative work" at session start, which is why it beats
skills that wait to be named.

**Building straight from the 2026-08-04 spec without framing it.** Tempting,
since the design already exists and framing looks like ceremony. It is the
precise thing that killed it the first time: untracked work is invisible to
every machine surface in this repo, so nothing can notice it stalled.

## What this is not

- **Not a rewrite of conductor.** The killer risk forbids it. Slice 1 touches
  `SKILL.md` in two places, both additions or guarded substitutions.
- **Not a decision about which skills die.** The coverage table is evidence
  gathered for that decision and belongs to the design rung.
- **Not the four-role seating.** Gap 1 is named and left open deliberately;
  resolving it by build would be deciding it by accident.
