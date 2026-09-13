# Kerd

"Ceird" means skill in Gaelic. Respelled.

![Kerd — the whole system](docs/design/kerd-map.svg)

**What is Kerd?** Twelve workflow skills for Claude Code, plus the working method they serve. The skills handle the operational side of working across sessions and machines: when to pull, what to commit, where to put notes, how to audit for drift, and how Claude and Codex contribute through their native sessions. Underneath them, every piece of work climbs the same seven-rung ladder (frame → viability → scope → design → handoff → loop → acceptance), and the repo carries machinery that can actually say no: gates that route work by what exists on disk, audits that turn silence into a named red light, and a progress board derived from disk rather than self-reported.

**Why should you care?** Because AI-assisted work has a silence problem. Things pass as "done" when nothing was in place to ask the question: was the risk sized? was the background read? was security ever even mentioned? A model choosing to comply is not a check. Kerd's answer is refusal from outside the model: CI that goes red at the exact push that broke a promise, with the fix named in the message. The skills keep you fast; the machinery keeps you honest.

## Install

```
claude plugins add-marketplace anthonymaley/Kerd
claude plugins install kerd
```

**Try a version before adopting it**, without touching your global setup:

```
claude --plugin-dir /absolute/path/to/kerd
```

A same-name local plugin takes precedence for that session only. Closing it
restores the ordinary setup; nothing is installed or disabled globally.

**Rollback is a Git reference, never a cached plugin file.** Claude Code garbage-
collects old versions out of `~/.claude/plugins/cache/`, so a version you can see
there today may be gone tomorrow — that is what silently killed hooks across eleven
repos before v0.96.0. Roll back by pinning the marketplace to a tagged commit:

| Want | Reference |
|---|---|
| The last commit before Conductor/Switch were replaced | `716a099` on `origin/main` |
| Undo the release, keep the history | `git revert <release commit>` |
| Pin a consumer repo to the old behaviour | marketplace `source.url` at `716a099` |

This repo carries **no tags** — `git tag` returns nothing — so a commit SHA is the
only durable reference today. If you want `v0.107.0` to be tag-addressable, the tag
has to be created and pushed as part of publishing; until then, cite the SHA.
Confirm what a reference points at with `git show --stat <ref>` before relying on it.

## What's New (v0.121.0)

### v0.121.0

**Arrival as a status grid.** Switch In's chat view opens with an explicit
completion heading and a PROJECT / PHASE / STATE / TEAM grid, then three bullets:
LAST SESSION, THIS SESSION and NOW, with owner-labelled numbered actions nested
under NOW. NOW holds only immediate actions and necessary follow-through;
detailed procedures, future-event checks and unrelated later work stay behind
Open work, while immediate limits stay visible. The explicit END and the single
question after it remain. Plain terminal output and Out are unchanged. Older
`task` context and `question.proposed` limits still survive under NOW.

**Delegation you can see.** Conductor shows a task / route / model requested /
effort / status grid when it splits work, with short updates at real
transitions: guidance checked, prompt briefs saved, dispatched, returned and
checked. Shareable briefs sit beside the work; Agent's full requests stay in its
private store. Unknown effort stays unverified, a native subagent is never
labelled as a Kerd Agent request, and queued is not running.

Fixture checks and two Claude review rounds cover the change. How long grid
cells wrap in your client, and both grids in ordinary use, remain to be observed.

### v0.120.0

**A compact arrival, without YOU.** Switch In's dashboard drops the separate YOU
box. NOW is the action list: pressing work and logical next steps in priority
order, each owner written as `**Owner:** action`, not an evidence checklist.
Plain colon text never gets owner emphasis; the renderer assigns no owner.
TEAM is one line, `Claude (role) + Codex (role)`; session IDs and routine
notice status stay in Agent's details, and a routing problem appears under
ATTENTION only when it affects the next action. The one question follows END OF
PICKUP as a bold speech-bubble callout, in chat and terminal alike.

Older callers keep their scope: a `question.proposed` value still renders under
NOW with its paragraphs and lists intact. Agent routing, arrival notices and Out
are unchanged. Fixture checks and two Claude review rounds cover the change; the
new layout in ordinary use remains to be observed.

### v0.119.0

**See your team at arrival.** Switch In's completion box now shows providers,
roles and short session IDs, plus the outcome of a one-way arrival notice.
An explicit partner selection wins; otherwise Agent uses an unambiguous existing
pairing, preferring a recorded role. Multiple candidates remain unresolved and
unsent. Repeating In with the same IDs reuses the earlier notice rather than
sending again. No reply is requested, no dormant session is resumed, and a queued
notice does not prove the peer is online. Native delivery can still trigger a
recipient turn or hold the message; no zero-token guarantee is made.

**YOU recommends, without a reply menu.** The box presents one recommended action,
numbered steps when useful, and a separately spaced scope limit. One direct
question follows END OF PICKUP. No “or later?” alternative or REPLY menu; you can
decline or redirect naturally. Agreeing to perform a check is not a passing result.

Fixture checks and independent Claude review cover the changes. Live arrival
notice delivery and the new layout in ordinary use remain to be observed.

### v0.118.0

**Out checks who holds the role before saving.** Before editing the handoff,
Switch Out verifies its own session against any existing pairing role. The same
ID keeps it; an explicit replacement choice already given is reused without
asking again; Out alone never takes a role. When only pairing is unresolved, the
memory save still goes ahead and the choice goes in the closing next action.
After the final save, whether successor designation succeeded, was unavailable
or did not apply is reported in the existing next text.

**Out collects contributions before it writes.** The closeout owner names the
sessions that contributed, reuses accounts already captured, and requests only
a missing delta through Agent before drafting, so you no longer have to ask each
agent. It shows one line saying who is captured and what is missing. A known
pending job is covered by its owner, state and where its result lands. An
unavailable participant is a recorded gap only when the available evidence
preserves the necessary context; otherwise the handoff is not ready. A delta
arriving after the save reopens the account and needs re-designation.

Fixture checks, a Claude review and one real run of the checkpoint on a Kerd
closeout passed. Model compliance in ordinary use remains unobserved.

### v0.117.0

**The question comes last, and NOW is a to-do list.** Switch In's chat arrival
ends on END OF PICKUP followed immediately by its one question; YOU keeps the
scope, proposal and reply guidance. With nothing to ask, it stops at the marker.
NOW is a numbered list of next actions in priority order, not a report of
observations or deferred rows. Terminal output keeps `--question-below` opt-in.

**A lost session no longer loses its role.** A record-based adoption keeps a
private restart receipt in the same binding. If that Claude session is lost and
another restarts, In can recover the same alias and role when the saved account
is unchanged, the machine matches and the predecessor is no longer natively
listed. Retired IDs cannot reclaim it automatically; a new Out, cancellation or
explicit replacement supersedes it. Refusals show their reason. This recovers
routing, not unsaved work. Codex new-ID crash recovery stays unsupported, and a
binding consumed before this release has no receipt to recover from.

Fixture checks and Claude reviews passed. A real restart recovery and the
experience of the new arrival remain unobserved.

### v0.116.0

**Keep the role when the session changes.** Agent verifies the current host's
session ID. Out can designate its existing role for continuation after saving;
In keeps the same ID or adopts the designated role with an expected-old-ID check.
Changed handoff records and competing replacements refuse. Old requests keep
their original targets; roles and IDs stay private to the worktree and machine.
No session is launched, stopped or granted new permissions by this update.

**Decide who builds, not just who reviews.** Conductor considers useful bounded
implementation contributions at delivery start, including established partners.
Owners and edit boundaries stay visible; small coupled edits can remain inline.
The controller integrates and checks the work; independent review stays separate.
No worker quota or new staffing approval step.

**A clarification is not permission.** A project name does not approve an install;
“not now” defers that action. Human-owned checks are labelled as yours. In restores
existing pairing context without contacting peers, loading Agent for contributions
and its short succession guide only when the local binding needs it.

Fixture checks and Claude reviews passed. Live clear/restart succession, actual
delivery of this release to installed clients, and delegation cost improvements
remain unverified; source publication is not installation or an experience verdict.

### v0.115.0

**A compact welcome, with a clear finish.** Switch In's chat view has a tight
completion box, short Last/This session summaries, NOW, essential warnings,
a separate YOU box and document links. END OF PICKUP marks the transition to
the session without authorizing work. Structure no longer depends on colour.

**One closeout for collaborating sessions.** The Out owner reuses recorded
contributions and retrieves material missing detail from the established partner,
then saves one resumable handoff. Read-only contributors return their account;
they do not rewrite shared pointers. MEMORY readiness is separate from the Git
SAVED verdict: the clear-context hint requires both a confirmed save and an
explicitly ready handoff. Missing necessary context remains visible.

**Define the partner's role once.** Agent remembers an ongoing implementation,
review or other agreed responsibility alongside the existing private pairing.
It stays separate from each job's role and grants neither permissions nor
Switch Out ownership. No tracked session-ID roster is created.

### v0.114.0

**Colour and emphasis on arrival and closeout.** Switch In and Out can now
render theme-styled Markdown directly in chat: accented identity, bold status,
a distinct YOU section and linked documents. The existing ANSI terminal boxes
remain available. The client chooses the palette; status stays explicit in
words, including unknown or failed saves. No extra dashboard or memory reads.

**Pickup reflects what just happened.** Arrival checks observed during In are
shown with their remaining assessment or recording, not as untouched future
work. Setup approvals name the installation scope and target project. A source
update time later than the render time in the same displayed zone gets a warning;
unknown times stay unknown. No automatic project edits or installation changes.

**Recognize the partner, not its old title.** Agent leads with provider, pairing
role, alias and short ID, labels saved native titles as potentially old, and
groups aliases for one session. Switch Out retains useful collaboration results
in its existing handoff, without a second tracker or public session IDs.

### v0.113.0

**Codex gets a native core package.** Build a relocatable Codex marketplace
artifact with Conductor, Switch, Visuals and Agent from the same maintained
`skills/` tree. The package inherits the release version, includes Agent's
optional dependency declaration, and excludes all eight legacy skills and
Claude hooks. Building is not installation or publication; use the
[Codex setup and update guide](docs/work/model-ready-work/packaging/START.md#install-in-codex).
Native model jobs now depend on the host's actual capabilities, and the Out
completion hint no longer assumes a Claude-only context command.

**Measure the selection you hand off.** Switch Out saves the helper's reusable
read arguments beside its measurement. Measurement and preparation share the
same selector; a section reaching EOF is labelled rather than treated as a
short excerpt. Evidence archives stay intact and available on demand.

**Clarify without accidentally approving.** A factual answer during pickup does
not authorize the next proposed job. The arrival question appears once, with a
`--question-below` option for hosts requiring it outside the panel. Insights
keep reported claims distinct from verified observations.

Package and regression checks do not prove a successful install, automatic
discovery, user-visible arrival or token savings. Those require an ordinary
session running the installed version.

### v0.112.0

**One arrival, one decision.** Switch In now loads Conductor before rendering
the dashboard, and the YOU box carries the arrival decision — *“Starting on X —
approve?”* with the scope of X. The 0.110.0 two-step arrival gave two answers
to “am I needed”: a dashboard saying nothing was needed, then Conductor asking
for approval underneath. A fresh pickup on another project showed the cost. The
proposed action keeps its saved scope (an unresolved design means designing,
not building and deploying), stages carry no tick the record does not support,
and no second brief, journey strip or copy of the task list follows. **What it
means:** the dashboard is the whole arrival; say yes and work runs. Changed,
not yet observed on a released pickup.

**Switch Out ends on the saved-place box again.** 0.107.0 dropped the old
close banner; Out ended on the helper's JSON. It now renders one box, from the
helper's own save result: SESSION SAVED when the remote is verified to carry
the exact commit, SAVED LOCALLY when only committed, NOT SAVED otherwise, each
in words as well as tone; the tree state, the paths kept out of Git, the next
action with its named reading set and measured size, and the day's log. It ends
by saying the session is still open with the free-context hint. It never says
the session exited or the context was cleared.

**Four review findings fixed, one reproduced by the reviewer that would have
swallowed its own review.** Agent could archive an inline mention of the reply
markers followed by an ordinary update as a completed review of one word, and
then ignore the real reply; the buffer now keeps the marker's line prefix.
Oversized Claude socket requests are refused before a delivery record exists (a
lock file may remain; the guide says so). Portable packaging reads the guidance
from its home under Conductor's references, so the build is green again.
`measure` refuses normalized aliases of the same source and names whole-file
plus section overlap. Living pointers in TODO.md and `docs/product/` follow the
0.111.0 memory move; their grounding lines became bare paths because the audit
resolves those by glob. Codex implemented from a spec both sessions reviewed;
the spec and both reviews are under `docs/work/release-111-followup/` and
`docs/work/model-ready-work/trials/`.

### v0.111.0

**Switch Out leaves a lean, measured start point.** Every pickup was paying for
the whole pointer file: on Kerd itself `## Key Decisions` had grown to 210 KB,
97 percent of CONTEXT.md, and a 2026-09-01 measurement had already shown that
pruning old entries was aimed at the wrong variable, while naming the untried
option — keep the ruling in the loaded file, move the case out. Out now does
exactly that, in four moves: rulings stay in CONTEXT.md only while they govern
the next work, with the full case in a living `docs/decisions.md` indexed by
ruling; Backlog rows the closure review judges done or dead move to
`docs/backlog-archive.md` with their verdict and evidence; the start point names
the exact reading set for the next sitting; and a new `handoff.py measure`
sizes that set against the pickup target (bytes exact, tokens estimated at four
bytes each and labelled so) and records the reading. Over target is information,
never a refused save. In reads the named set first and nothing else by default.
**What it means:** the boundary, not the reader, is responsible for pickup cost.
**Named as a loss:** a ruling in CONTEXT.md no longer carries its argument; the
argument is one link away, and the 2026-09-01 row records the known risk that a
reachable record can sit unread. The first run was on Kerd's own files at this
release; the measured reading is in CONTEXT.md.

### v0.110.1

**The shipped skills stop calling themselves a candidate.** Conductor, Switch
and Visuals still carried "development candidate" headers and told the model not
to invoke installed Conductor — the very skill Switch In loads. A Fable review of
the four 0.107–0.110 skills found that and fourteen more; the report is at
`docs/work/model-ready-work/trials/2026-09-11-fable-skill-review.md`. Fixed in
this release: the candidate wording; the In approval line's precedence (saved
next action, then first NOW item, then "no task selected"); its stated reason,
now a deliberate check-in on arrival rather than an authority claim that
contradicted "don't require a second yes"; the In rule living in one place
(Conductor's SKILL.md) with the other three copies pointing at it; Conductor's
model-guidance links, which pointed at a directory that shipped nowhere — the
guidance now lives under `skills/conductor/references/guidance/` and ships; a
`docs/work/SESSION.md` pointer Switch never writes; the closing link's three
names, now one (*Open work*); and this README's "How They Fit Together", which
still described the pre-0.107 loop. Three reproduced script defects fixed with
tests: a `now` written as one string rendered a bullet per letter; `agent.py
status` on an unknown request left an empty lock file in the store; a section
heading with trailing spaces failed the handoff helper with a misleading
message. **Named as a loss:** the Slainte claim below is corrected rather than
built — Conductor has no close-out hook, so the release pass runs on demand.

### v0.110.0

**Switch In opens a Conductor session and stops on one line.** 0.108.0 had In
restore your place and stop dead, leaving you to ask for the work yourself —
correct on authority, but it lost the focus: nothing on screen said what the
sitting was for. In now shows the dashboard, then opens Conductor on the restored
place — journey strip, brief, task list — and ends on exactly one line:
*“Starting on X — approve?”*, where X is the saved next action. One proposal,
never two options, never an “or”. Your approval starts the work; the line is a
deliberate check-in on arrival, so an already-authorized plan waits for the same
line. `switch to` and Roll keep their agreed continuation untouched. **What it
means:** every pickup lands in a session with its next move named, and the only
thing between you and work is “yes”.

**The dashboard shows the immediate work.** A `NOW` block lists the bullets
under the project's `## Now` heading, between the frame and last session; the
backlog stays behind the *Open work* link. It is part of the frame, so a project
with nothing under Now shows that gap rather than hiding it. The guide's
copy-ready example and its value-binding tests carry the new `now` list.

### v0.109.0

**Agent can now reach the Codex session in your terminal.** 0.108.0 talked to
Codex only through the app-server daemon — and on a machine where every Codex
is a TUI, that meant it could reach none of them. Agent now discovers the
sessions you opened from Codex's own store, pairs one under a local name, sends
through `codex queue --thread`, and reads the answer back out of that session's
native transcript by request markers. No daemon, no reply file, no mailbox.
Proven live on an earlier state of the tree: a request to a running TUI came
back `reply-received` in twenty seconds; the Claude route was re-proven after
every fix, the Codex route is owed a re-run when Codex has tokens. **What it means:** "ask Codex" works against the Codex you are actually
using, through the one command that ships with Kerd, on any machine — no vault
script, no symlink, nothing a consumer repo has to know about.

**Five corrections from Codex's review of the design, all shipped; one more
from a guard test after Codex ran out of tokens mid-review; eight from an
Opus 5 review of the finished build; eight more from a Fable 5.1 review of the
0.108.0 foundation beneath it; and eight from Fable's final pass over the whole
diff — including a blocker in the fix for Opus's blocker.** The guard test caught an uncertain
daemon send falling through to a second enqueue on the CLI route — the exact
hazard Codex had named. The Opus review caught a deleted refusal: a thread a
daemon reports offline was being handed to `codex queue`, which may be able to
start a session — restored, so the CLI route serves only threads no daemon can
see. Among the rest: a marker quoted in Codex's *commentary* stream was being
archived as a final reply — only `final_answer` (and unphased older events)
count now. From the Fable rounds, four changes you will notice: a reply's
markers must now sit on their own lines (an inline mention of both markers
parsed as a reply of one word); a message above about a million characters
is refused before anything is recorded; a slow Claude launch keeps its short
id and waits fifteen seconds instead of five; and no error names a private
path or repeats your prompt. **Conductor's players are subagents again.** The
rework routed every delegated job through a fresh CLI session; the Conductor
it replaced spun players up as native subagents at a sized model and effort,
and that is the better default — the work stays in the session and returns
to the caller. Restored for Claude players; the CLI runner remains for Codex,
resumable, sandboxed and persistent jobs. A regression fixed, not a feature. Discovery lists only threads a person opened, not the subagents they
spawned. And an uncertain enqueue — a timeout mid-send — is retained as
`delivery-uncertain` and never followed by a second send on another route.
**Stated, not glossed:** a thread in the store is a *selectable* conversation,
not proof anyone is at the keyboard; it is labelled `saved thread — activity
unknown`, and `codex queue` exit 0 means enqueued, not answered. The vault's
reply-file bridge stays available for repos not yet on Agent.

### v0.108.0

**Ask the partner that already knows the work.** New `/kerd:agent` discovers
local Claude/Codex sessions, pairs an existing conversation, or starts a fresh
worker or ongoing partner. “Ask Claude to review” uses the established project
partner; if the target is unclear, Kerd shows sessions to choose from. “Fresh”
is a deliberate choice, not a silent substitute. `/kerd:agent help` explains
the short requests, setup and limitations. Native queues carry requests; Kerd
retrieves complete replies without a new inbox service or terminal takeover.
Codex partners need an optional WebSocket dependency. Existing Claude partners
may hold inbound requests for approval; pairing does not grant native trust.

**Switch In restores your place and stops there.** It was telling itself to
continue an active build in the same turn, which contradicted the welcome-back
summary it had just shown you — so a pickup could start executing work before you
had read where things stood. In now ends with memory, status and the saved plan
on screen. **What it means:** arriving is arriving. Ask to continue and it hands
over to Conductor without a second approval; `switch to` and Roll keep their
agreed continuation untouched. **Named as a loss:** a pickup no longer resumes an
authorized build by itself — if you relied on In carrying straight on, that is now
one sentence from you.

In also loads Conductor for orientation only, using the already-restored place;
it does not start intake or execution. Later work stays under Conductor, with
supporting skills supplying methods rather than replacing the workflow. This
adds instruction reading, so reduced overall pickup time or tokens is not yet
claimed. Ordinary-use comparisons remain to be observed.

**The welcome-back dashboard stopped making Switch read code to use it.** The
pickup guide now carries a complete, copy-ready example of the renderer's input,
so filling it needs no trip through `where_we_are.py`. Two measured pickups spent
three to four minutes getting oriented, with rediscovering those inputs among the
avoidable work. The example is bound to the renderer by tests that compare whole
rendered values, so the two cannot drift apart quietly. An absent `source` now
reads `not recorded` instead of `None`, and the guide separates what a caller
should supply from what the renderer actually checks.

### v0.107.0

**Conductor and Switch are replaced, Visuals joins them, and Kerd is eleven skills.**
Conductor now guides **Understand → Shape → Agree → Deliver → Complete** instead of
orient → plan → execute → close, holds a real conversation about what you want
before building, and handles a small explicit change without dragging it through a
full intake. Switch In opens with a welcome-back dashboard — phase, task, state,
last session, this session, and a box that says whether you are needed — instead of
an exhaustive report of every backlog row. Switch Out gains explicit-file saves,
acknowledged local-only paths that are never staged, and a remote check that the
branch carries the exact commit. Visuals draws the direction so it can be agreed at
a glance. **What it means:** the everyday surface is the conversation and the
dashboard; the ladder, gates and board are still there, still derived from disk,
and still run by `drive` and the tools.

**Named as losses — four automatic triggers are gone by decision, not oversight.**
The new Conductor and Switch call no other skill, and restoring the triggers was
considered and declined: Switch Out stays explicit, and release checks belong to
the release task rather than firing on ordinary completion. (1) Conductor's close-out no
longer invokes the release close-out pass, so `/kerd:slainte release` is yours to
run at a version bump or an acceptance record. (2) Conductor's close-out no longer
runs the session boundary; `/kerd:switch out` is standalone again, as it was before
v0.84.0. (3) Switch Out no longer self-migrates legacy `## Current Session` /
`### Context` shapes in TODO.md — `/kerd:tend` still detects them, but the healing
step is gone. (4) Conductor no longer writes the `conductor: <phase> @ <time>`
marker into `kivna/.active-modes`, which the same-turn time rule names as one of
its legal time sources and which the SessionStart hook reads — read the clock
instead. Nothing goes red
when any of these stops happening, which is why they are written down here.

### v0.106.0

**A risk's severity and its treatment are two facts, not one field.** The ledger's one `State` column mixed how bad with what we are doing about it, so a risk that was genuinely fatal and genuinely treated could not be stated truthfully — whichever value the cell carried lied about the other fact. Now a row carries `Severity` (fatal / non-fatal) and `Treatment` (the four), `Evidence` renames to `Risk evidence`, and a new `Treatment evidence` column holds what proves the treatment: the honest `planned — <what will exist> · <expected location>` declaration before the proof can exist, a resolving citation once it does. A fatal risk advances from viability on a planned treatment; acceptance is where the citation must resolve. All 21 work records migrated in the same commit as the checker and its fixtures — no committed tree ever held mixed schemas — and every severity the old vocabulary never recorded was keyed by hand in a review worksheet committed with the migration, so a reviewed value stays distinguishable from a stated one. **What it means:** a fatal, treated risk no longer forces the ledger to lie, and a treatment is never called proven merely because its field is populated. **The limit, stated:** the machine verifies that a citation resolves; the producer decides whether it supports the treatment.

### v0.105.0

**Status has a template.** Session status — the switch-in summary, conductor's orient, a task report — now follows one format from the talk-format library: **Work item · Stage · Issue · Resolution path**, in plain language that works without the repository open, and the message ends on exactly one question — never a compound "X, or Y?". Born from a real correction: a status spoken in repo shorthand ("scope refused on the FATAL row") was unreadable to its own reader, and the same facts restated in this shape worked first time. **What it means:** you can act on a status message without the codebase open, and every status ends with one clear ask instead of a menu bolted onto a question. The format is canonical in `docs/design/talk-formats.md`; conductor and switch both point at it.

### v0.104.0

**The funnel has a driver.** `/kerd:drive <slug>` is a new skill that owns one work item across the whole ladder — frame → viability → scope → design → work handoff → loop → acceptance — over as many sessions as it takes, and hands each sitting's work to `/kerd:conductor` without changing a line of it. At the frame gate it asks a short question set: you declare the work type (never guessed), the set is copied from a seed into the work record, you edit it before anything is asked, and the frame gate counts answered against declared until every entry has an answer — the item stays at `frame` until then. One list drives what is asked, what counts as finished, and the `now > frame, next viability, after scope` line you see. **What it means:** an idea can enter the funnel by being asked six questions rather than by someone remembering the sections, and nothing already on the board moves — the check applies only to a record that carries the section. **The limit, stated:** the gate counts presence, never quality; it cannot tell whether an answer is true, and it cannot tell whether Drive or a hand wrote the section. One seed exists (`software-change`); the other gates' sets are following slices.

### v0.103.0

**The router told newcomers to satisfy `handoff` by producing a `contract`.** When work stops at the handoff rung, the gate names what it still needs — and it named it "contract spec", a phrase built from a rung name that was retired three days earlier. It is the first place the ladder speaks to someone who wasn't in the room, and it spoke in a word the ladder no longer uses. The line now describes the artifact instead of naming it: *work specification with Pieces and a Verify for every step*. **What it means:** the gate tells you what to make rather than what to call it, so you can act on the sentence without being taught the vocabulary first. **Deliberately unchanged:** the artifact is still the contract, and conductor and the handoff flow still say so — that is where the delegation relationship is explained and where the word earns its keep. Only the first-reader line moved.

### v0.102.0

**Completing v0.101.0: a record can be well-formed and still claim the opposite of its own filename.** AU10 started requiring a legal `route` and `stage` on every gate record. But `stage: designed` is perfectly legal — and on a file named `*-acceptance.md`, which exists to say the producer accepted the work, it says the reverse. The router took it anyway. Now a record whose name asserts acceptance must carry the terminal stage: `ready-to-release`, or `done` through the read-only alias that keeps the seven immutable legacy records working. Other suffixes are untouched, so a design record saying `stage: designed` is still exactly right. **What it means:** the name of a gate record and the stage inside it can no longer disagree — the filename is a claim, and the front matter now has to back it. **The limit, stated:** this checks that the two agree, never that either is true.

### v0.101.0

**A gate record could be invalid and still move a work item to the finish line.** The audit pinned gate-record *filenames*, and validated front matter only on files that already had some — so a record with a perfectly good name and no front matter at all fell through the gap between the two checks. That gap was load-bearing rather than cosmetic: the `ready-to-release` terminal is derived by reading the acceptance record, so an invalid file could report a work item finished while the audit stayed green. Now every `docs/gates/` record must carry a legal `route` and `stage` — AU10 refuses the ones that don't, and the terminal will not qualify a record that fails it. The retired `-goal.md` name reads under the same contract, not a weaker one. **What it means:** a gate record either meets the shape the gates README has always described, or it doesn't count — the contract was written down long before anything enforced it. **The limit, stated:** this checks the record's shape, never that its Release condition is true.

### v0.100.0

**A journey page could tell you a stage had no steps while the steps sat four lines away — and every gate stayed green.** The journey pages read their step definitions out of one file and look them up by the stage's display name. Rename a stage on one side and the lookup quietly misses: the page prints "Rungs not defined for this stage yet" over work that is fully written down. That is exactly what happened when the ladder folded to seven rungs — three stages were renamed, the definitions file kept the old headings, and every journey page shipped two false panels. Regenerating the pages could never have caught it, because regenerating only proves the pages match the source; it cannot notice that the source stopped matching the code. Now a check refuses the mismatch in both directions — a stage with no definition, and a definition matching no stage — and it runs in CI on every push. **What it means:** when you rename a stage, the build stops and tells you which headings to move, instead of publishing pages that quietly claim the work was never defined. **The limit, stated:** it checks that every stage *has* steps defined, never that the steps are the right ones.

**Eleven places said the ladder still had eight rungs.** The seven-rung fold swept its enumerated list of sites perfectly and missed their neighbours — a stale count in the playbook, a retired `build` and `goal` inside a diagram generator, conductor still teaching that the frame must carry a fully qualified risk ledger when that check moved a rung down to scope, the README claiming `stage: done` was gone when it is still a readable alias, and the gates README telling you the router picks the *lowest* passing rung when its own code and its own line 63 both say *deepest*. All corrected. **What it means:** the documents describing the seven-rung ladder now agree with the machine that implements it, and with each other.

### v0.99.0

**The ladder is seven rungs now, and the two that disappeared were always doing one job.** Work used to climb `frame → viability → slice → design → contract → build → goal → loop`. Eight gates, but `build` and `goal` split a single stretch of work between them — build the thing, check the boxes, go round again — and the human-sounding name sat on the machine test. Now they fold into **`loop`**, a container checked only at its two edges: you enter with a spec whose every step carries a `Verify:`, you leave with zero unchecked pieces. What used to be called `loop` becomes **`acceptance`**, the producer's last gate. `slice` is renamed **`scope`**, `contract` is renamed **`handoff`**. **What it means:** the rung names say what happens at them. Build, verify and adjust are execution mechanics, not checkpoints to report through, so the router stopped pretending they were — and because the checks themselves never moved, every work item's reported position changed label, not substance.

**Scope is where you lock in what you're building, and the gates were holding the wrong things.** The scope gate used to check your risk ledger while the *design* gate checked what you had committed to build — so the machine asked "what could kill this" where "what are we building" belonged, and asked for the commitment one rung late. Now `## Release slice` is renamed **`## Scope`** and is checked at the scope gate, with the rigor level travelling with it; design checks only that every declared concern has a sealed drawing. Viability gains its first real check too: your risk ledger must **name** a killer risk — presence only, no sizing, no evidence, because you cannot qualify the risks of a thing you have not defined yet. **What it means:** risk is read twice at two depths — named cheaply at viability, fully qualified at scope — and the rung called scope is finally the one where scope is agreed.

**A retired name reads old records forever; it never writes a new one.** `slice`, `contract`, `build` and `goal` stay legal in every parser so the seven existing `-goal.md` gate records keep working, and no file on disk was renamed or rewritten. But every *trigger* moved the same day: conductor, slainte and switch now fire their completion behaviour on `docs/gates/*-acceptance.md`, because a trigger still watching a retired name is a second live name wearing an alias costume — it would have gone quiet with every drawing and gate record still looking correct. **Named as a loss:** you can no longer declare a work item finished. `stage: done` is retired — still readable on records that already carry it, never written as current — and the terminal is `ready-to-release`, which is *derived* — the machine reports it only when an acceptance record is actually on disk, and refuses the claim when it is not. Typing that you are done was a real thing you could do yesterday, and it is now something you have to produce evidence for. **The limit, stated:** the filename check validates shape, not intent — a freshly written `-goal.md` would still pass it. The machine holds the read side; the write discipline lives in `tools/gates/README.md` and the skills.

### v0.98.0

**Conductor now advises the session down, not just up — and effort joins the model in every sizing call.** Before, the model advisory only pushed one way: it could tell an underpowered session to move up to Opus, but a session opened at Fable on high effort for routine work sailed through unremarked — and silence approves the burn. Now conductor sizes the *pair*, model and reasoning effort together: it states what it believes the session is running (and why that belief can be stale — a mid-session `/model` switch is invisible to it), has you confirm the actual pair in the same breath as the existing gate, and names the downgrade explicitly when you're overpowered — "conducting this needs Opus medium; difficulty is bought per-call." The composer call now carries its own sized effort too, the same two levers player steps always had: tier buys capability, effort buys deliberation. **What it means:** the four-role cost model finally closes — nobody idles at premium rates between the calls that need them, and the expensive tiers are bought back per-call at exactly the effort the work earns. **The limit, stated:** no harness surface exposes the session's current model or effort to a skill, so this is stated belief plus your one-word confirmation, never detection — if that surface ever appears, detection replaces asking (the return condition is in the frame's risk ledger).

**The requirements register's rules now have a refuser.** Since v0.95.0 the register (`docs/requirements/`) has declared its own law — "an unknown field is a hard error", "the audit REFUSES" when an approved statement is edited — and nothing enforced any of it: the rules were prose, exactly the gap the register itself exists to close. Now two audit rules (AU7, AU8) ride the same CI sweep as every other refusal, at no new CI step: an illegal ID or state, an unknown field, a missing Source, an `Approved` hash that no longer matches the statement it approved, a `superseded` block that never names its replacement, or a link pointing at a requirement that does not exist all turn the push red, with the exact block and defect named. Two of the catalog's rules are deliberately *reports*, not refusals, matching its own words: a link whose stamp has gone stale ("flagged for re-look") and a requirement with no parent in the trace — those print as findings and never block. Nothing is hardcoded: the legal category set comes from each project's own `categories.md`, so a consuming project's taxonomy is its own. **What it means:** editing a keyed requirement's words now gets caught by the machine, not by the producer's memory. **The limit, stated:** the hash proves the words haven't changed since approval; it cannot prove they were the right words — only reading it back can.

**Kerd's hooks now ship the standard way, so updating Kerd never breaks them again.** The old mechanism wired each repo's hooks by pasting an absolute path to a specific plugin-cache version into `settings.local.json` — and Claude Code garbage-collects old cache versions, so the moment your installed version was pruned, every hook in every repo pointing at it went silently dead, including repos you never touched. That is what happened: eleven repos with broken hooks and a `/switch out` reminder that named a command that no longer exists. The fix is the mechanism plugins are *supposed* to use — `hooks/hooks.json` in the plugin, which Claude Code auto-registers the instant the plugin is enabled and resolves at runtime, so there is no version-pinned path anywhere to rot. You wire nothing; updating Kerd changes nothing to keep in sync. **What it means:** enable Kerd and its hooks work, everywhere, forever. `/kerd:tend` now *removes* leftover manual wiring instead of adding it. **Named as a loss:** the Stop hook is gone — it was the only thing that nudged "you have uncommitted changes, run switch" at turn-end, but it fired after every response (not once when you left), its reminder pointed at a dead command, and its mode half was already covered by the statusline. The uncommitted-work safety net is the thing you're giving up; the switch discipline itself is unchanged.

### v0.95.0

**The release pass ran on four releases at once, and what it found was a counting problem.** v0.93.0 added an eighth CI step and never swept the places that said there were seven — the README, the system map's rendered box, two design docs, and the state file. That is the exact failure this repo made a standing rule against: a change to system-wide behaviour owes a cross-cutting grep before it ships. The pass fixed all of them, and where a doc only meant "this feature adds no step", the absolute number is gone rather than corrected — a count in prose rots on someone else's release. It also mirrored five gotchas that never reached the playbook, corrected eight ownership cells in `docs/state-contract.md` against what the skills actually do (kivna's import writes TODO and the session log; conductor does not read session logs at orient), and gave `tend` its missing fourth hook: a repo wired with three of four passed hook hygiene, because the check enumerated a list that stopped being complete. **What it means:** the narrative surface now describes the repo that exists. **What this is not:** a check — nothing in CI reads the playbook or the README, so the next count to rot will rot silently too.

### v0.94.0

**New work now gets a frame the machine can see, instead of a line in TODO.** Kerd could route work through eight funnel stages, check every one, and render the board — and no skill had ever written the artifact that puts work *on* that board. Framing was de-skilled at v0.73.0 and moved to "the frame flow", a flow with no owner. The cost was not hypothetical: the decision to give the funnel a driver was taken in full, specced, and sat unbuilt for three days, not because anyone forgot but because it never entered through a frame, so no gate demanded anything of it and no render showed it missing. Now, when a repo routes work through entry gates, conductor asks the gates whether the work is tracked and — if it is not — the framing conversation produces the frame artifact itself: the value in your own words and in units, the grounding, a risk ledger where every risk is sized and in exactly one state, and the smallest valuable slice with its exclusions named. Your key belongs at that gate; the value statement is yours and the model's job is to write it down accurately, not author it. Where no gates exist, nothing changes. **Named as still unowned:** the design and handoff stages — nothing writes a design doc, a GO record, or a Scope section yet. Conductor sheds one piece at a time, which is its own spec's rule, not caution.

### v0.93.0

**The boundary now checks that it recorded what the session produced.** Switch out has always written the handoff and never verified it — the work item that fixed the boundary said so plainly, and shipped unverified because of it. On 2026-08-07 that cost something real: a session with 23 unrecorded commits could not safely be closed, because nothing could say whether closing it would lose them. Now `tools/gates/fidelity.py` compares every file the session changed against what `CONTEXT.md`, `TODO.md` and the session log actually name, and refuses at the boundary when something was produced that nothing a pickup reads points at. Its first honest run caught seven, including two tools built that day that the next session would never have found. It runs in CI on every push and skips itself unless the commit writes a session log, so it bites at the boundary and stays quiet during normal work. **What it cannot do, named:** it proves *reachability*, never *comprehension* — a path mentioned in a sentence passes even if the sentence misdescribes it. The same declared limit as grounding-was-read, and claiming more would be a green tick over a model choosing to comply.

### v0.92.0

**The four roles are renamed, because the old names inverted under reading.** You were the *composer* and the spec-writing agent was the *orchestrator*. In practice that swapped: asked to describe the model, the person who chose those names used "composer" for the spec-writer and "orchestrator" for the driver, in one sentence. Now the names say what the words already mean — **you are the producer** (the idea or the input, and the approvals that keep it the show you wanted to make), the **composer** is the top-tier model called as a subagent to write the score, the **conductor** is the session model directing the performance, and **players** are subagents spun up per step at a sized model and effort. Nothing about the architecture changed: the composer was always Fable, the conductor always Opus, the players always sized — only the labels were wrong. What it means: the model tiers are now stated in the roles table rather than buried in prose, and instructions that tell one role to call another can be written without inheriting a name that reads backwards.

### v0.91.0

**Conductor asks the machine before it asks you, and its commits name what they landed.** Two things a decision from 2026-08-04 had already called for and nothing had built. Before, conductor opened every session by asking you for anything the work might need — including things already sitting on disk, which the entry gates have been able to report since v0.69.0. Now the pre-flight inventory runs `gate.py route` first where a repo has gates, reads what it says, and asks you only for what no file can answer: credentials, hardware state, fixtures. Where no gates exist the behaviour is unchanged. Separately, a work commit running against a contract with numbered pieces now carries a `Piece: <slug>/<n>` trailer — a checked box is a claim, a commit trailer is a fact, and it is the one progress signal that cannot be falsified by ticking a box. What this is *not*, named: the driver. Conductor still does not know which work item it is on or which stage that item is at — that is framed at `docs/product/funnel-driver.md` and deliberately not built here, because conductor is the only working instance of half this system's functions and it sheds one piece at a time.

### v0.90.0

**The boundary lost its cheap modes, and that is a real loss.** `/switch out light` and `/switch in low` are gone — the argument is told in full under [On cheap boundaries](#how-they-fit-together). The same release put ladder position on both halves of the boundary (the old steps named two progress files that had never existed here, so they silently did nothing while the derived board went unread), made CONTEXT.md append-only between licensed prune events, added a no-silent-truncation rule to "read in full", and gave closure inference its fourth verdict, `dead`, for a row that is undone but whose reason has gone. Switch got shorter while gaining four rules, because deleting the modes deleted every "skip this if light" clause with them.

### v0.89.0

**The session's clock stays honest between phases.** Before, conductor was told once — in a section near the top of its own skill — to write its phase marker to disk. A session that drifted past that one instruction left the marker sitting at an early phase, and close-out then read a stamp that no longer matched reality; on this feature's own first live use the model went one worse and invented a stamp that had never been written. Now the write instruction sits at every phase transition, where the write actually has to happen, and close-out states the consequence plainly: if the marker is not at `execute`, no open time exists, so the session log records a close time alone rather than a plausible-looking range. Gate records gained their missing write-side instruction too — the `**Clock:**` line is now owed by the skill that writes records, not merely documented by the standard that defines it. What it means: the times in your session logs and the durations derived from your gate records come from stamps that were actually taken. What this is *not*, named: a check. `kivna/.active-modes` is gitignored, so no CI step and no hook can refuse a stale marker — this is discipline moved to where it gets used, and its honest test is whether the next session's log carries a real range.

### v0.88.0

**The machine consults a clock, and effort becomes data.** Before, nothing in a session knew what time it was: session logs got headings like "late-evening sitting" written at midday, and how long a task actually took was unrecoverable. Now the clock is captured where artifacts are already written — the conductor's phase marker carries a real stamp (`conductor: execute @ 2026-08-06 15:17 EDT`), which is the task's start; the work commit's git timestamp is its end; session-log headings and the switch-out banner carry real times; and new gate records can carry an optional `**Clock:**` line, so how long a rung took becomes derivable. One rule governs all of it, defined once: a time is written only when a machine produced it in the same turn — a `date` run, or a machine-written record read that turn. A remembered or estimated time is never written. There is also an opt-in statusline segment (`hooks/statusline.sh`) that shows you the time, and **composes** rather than claims the slot — hand it your existing statusline command and it prints both. What you don't get yet, named: estimates. This slice captures honest actuals; using them to predict how long the next task will take is the next slice.

### v0.87.0

**Trim is gone.** The token-cleanup skill's jobs all dissolved into machinery that runs anyway: completed specs are dated immutable records the gates and the progress board read in place (moving them to an archive would turn CI red by construction — the handoff and loop rungs require them where they are); switch's closure inference cleans TODO with evidence at every boundary; doc-drift pruning belongs to the release pass. What you lose, named: `/trim` no longer answers, and nothing archives docs to `docs/archive/` anymore — deliberately, because nothing should. Kerd is nine skills now. Dead solutions stay dead; the return condition is a cleanup need the boundary, the gates, and the release pass cannot answer.

### v0.86.0

**The release pass now fires when a feature closes, not only when a version ships.** Before, close-out ran the doc-surface pass only if the session's work bumped the plugin version — so the session that lands a feature's acceptance record (its formal "closed as complete" moment, usually a doc-only diff with no bump) got no pass, exactly when the narrative surfaces most need checking. Now either moment fires it: a version bump, or an acceptance record landing. One definition of "release" stays (the version-field diff, CI's R1); the completion clause is a second firing moment, not a second release heuristic. What it means: no feature closes without its story being checked.

### v0.85.0

**Releases now check their own story.** Before, slainte was a read-only audit you had to remember to run — and nobody did: the mechanical checks moved into CI, and the judgment layer (does the README still describe what shipped? is What's New honest?) ran never. Now the release moment itself triggers it: when a conductor session's work bumps the plugin version, close-out runs tend's drift check and slainte's narrative pass before the boundary. Slainte fixes what drifted — as normal work commits under the verification gate, with skriv auditing any prose it writes — and its report names what it deliberately left alone, so restraint is visible instead of assumed. The hand-kept `.slainte` config file is gone; audit targets derive from the repo. What it means: the doc surface gets one honest pass per release instead of zero, CI keeps the mechanical layer, and `/slainte` still answers on demand.

*Release notes for v0.84.0 and earlier live in git history — `git log --follow README.md`.*

## Skills

### drive (Work Item Umbrella)

Drive walks one work item from idea to acceptance, across as many sessions as it takes, and calls conductor for each sitting's work without changing it. It reads the item's rung from disk (`gate.py route`, never the board renderer), shows `now > X, next Y, after Z`, and at the frame gate runs a question set: you declare the work type from the seeds in `docs/work/question-sets/`, the set is copied into the work record's `## Question set`, you edit it first, and the frame gate holds the item at `frame` until every entry carries an answer. Counted, never judged — the answers are yours. Conductor owns the session; switch owns the session boundary; Drive owns the item.

```
/drive <slug>        # pick the item up where disk says it is, or start it
/drive               # list every item and where it sits
```

### conductor (Session Discipline)

During delegation, Conductor shows a task/route/model-requested/effort/status
grid and updates it through actual dispatch, return and checked results. Short
updates show applicable prompt guidance being checked and how many prompt briefs
or full requests were saved, distinguishing shareable files from private records.
Unknown effort stays unknown; a native subagent is not
mislabelled as a Kerd Agent request. These updates expose real work, not a
mandatory worker count or a new approval step.

Conductor guides repo-based work from a request — "build an app", "create a guide",
"plan a project" — through **Understand → Shape → Agree → Deliver → Complete**. It
holds the conversation that works out what you actually want, agrees it before
building, delivers, and gets an independent assessment. Work can be software,
research, a commercial offer, a process or any other repo-based outcome.

It handles small explicit changes directly rather than dragging them through a full
intake, and a status or review request does not start one either. Interrupted work
resumes where it stopped.

At delivery start it decides what stays inline and what a worker or established
implementation partner can usefully own. It shows the split, avoids overlapping
edits and keeps integration and independent review explicit. Small coupled work
does not need an extra agent; resumed builds reuse settled assignments.

```
/kerd:conductor              # start, or resume saved work
```

Supporting detail lives beside the skill: `references/understanding.md` (the
intake conversation), `references/journey.md` (how a build is laid out),
`references/execution.md` (delivery and checking), `references/model-jobs.md`
(which model does which job), `references/work-record.md` (what gets written down).

### agent (Claude/Codex Partners)

Get a contribution from an existing session with context, a fresh independent
worker, or a new ongoing partner. Kerd handles session IDs, prompt preparation
using the applicable model guidance, native submission and result retrieval.
Established project partners are the default; ambiguous targets are shown as
session choices. A review request does not authorize edits or publication.
Session choices lead with pairing role, alias and short ID; the saved native
title is secondary and may describe old work. Known recent exchanges are labelled
as recorded, not current activity.
Define the ongoing role when pairing ("Use Codex as reviewer"), then reuse it;
a one-off job does not change it. Roles and IDs stay in private pairing metadata,
not a tracked roster, and neither roles nor aliases grant permissions.
After a clear or restart, Agent verifies the host's actual ID rather than guessing
from the terminal lifetime. A saved role designation or explicit replacement
selection lets the successor update that private binding; stale expectations
refuse and old request targets remain intact. See
[session succession](skills/agent/references/session-succession.md) for the
supported hosts, handoff checks and limits. Record-based adoption retains a
private restart receipt: Claude can recover the same role after another loss
when the saved account and machine match and its predecessor is no longer
natively listed. Retired IDs cannot automatically reclaim it. This recovers
routing, not unsaved work; Codex new-ID crash recovery remains unsupported.

```text
/kerd:agent help
/kerd:agent show sessions
/kerd:agent ask Claude to review, RO
/kerd:agent start a Codex pairing partner
/kerd:agent anything back from Codex?
```

These are conversational examples, not fixed subcommands. See the
[user guide](skills/agent/references/user-guide.md) for everyday use and
[native-session reference](skills/agent/references/native-sessions.md) for setup.
Both providers use their existing CLI sign-in. Discovery covers Claude native
sessions, Codex's shared server, and the Codex sessions you opened in terminals
(reached by `codex queue`, activity unknown until they answer) — not every
desktop/IDE session. New partners
default to read-only; the Claude launcher has file tools, not shell tests or
nested delegation. Missing dependencies and held messages require disclosed
setup, never a silent settings change. The separate three-skill trial package
does not include Agent; this marketplace release does.

### interrogate (Risk Ledger)

Interrogate qualifies the risks of a plan or idea until every one is sized, evidenced, with Severity and Treatment each stated — because a named, unsized risk reads as managed, and that is the failure this skill exists to stop. The interview engine is unchanged: one question per turn, no extrapolation, graduated adversarial lean (gather → probe → stress-test → adversarial), user-veto on stop, deterministic pause/resume from frontmatter session state, and row-by-row recitation before co-sign. The output is the tiered risk ledger: ten columns (Risk / Killer? / Impact / Likelihood / Risk evidence / Severity / Treatment / Countermeasure / Treatment evidence / Review trigger), Severity fatal or non-fatal, Treatment one of four with its evidence carried from `planned — …` to a resolving citation, killer assumption first, always.

Two tiers. Everyday work fills the ledger inside the framing conversation — no skill invocation — directly into the living `## Risk ledger` section of `docs/product/<slug>.md`. A large bet runs the full interrogate session, exhaustive across the viability axes (technical, business, legal, operational), producing a dated session record at `docs/interrogations/YYYY-MM-DD-<slug>.md` whose co-signed ledger is copied into the living section at sign-off. Impact is denominated in the units of the declared value (the `## Value` section of `docs/product/<slug>.md`); fatal severity means impact ≥ that value at any likelihood — set by impact alone, never by multiplying in likelihood. Interrogate does not produce the implementation plan — after sign-off the work moves down the walk to slicing and design with its risks pre-chewed, never re-assessed there.

Design at `docs/design/risk-ledger.md`; the interview engine's original design at `docs/plans/2026-05-02-interrogate-design.md`.

```
/kerd:interrogate              # zero-path: interview from an idea
/kerd:interrogate <plan-ref>   # interrogate an existing plan
```

### switch (Session Handoff)

Switch saves, restores or moves repo-based work between sittings and devices. It
keeps the work continuous while leaving room in the next context window, handles
explicitly authorized Git handoffs, and distinguishes closing out from continuing
mid-work exactly where you stopped.

```
/kerd:switch in              # pick the work back up
/kerd:switch out             # save the place
```

**In** opens with a welcome-back dashboard rather than a full report: phase, task,
state, owner-labelled actions in priority order under NOW, what happened last
session and what this session is for. No separate YOU box.
Chat uses a PROJECT / PHASE / STATE / TEAM grid under the explicit completion
heading, then three bullets: LAST SESSION, THIS SESSION and NOW, with numbered
owner-labelled actions nested beneath NOW.
END OF PICKUP · SESSION READY closes restoration; the one pending question
follows as a bold speech-bubble blockquote. With no question, stop at the marker.
The grid and sections are native Markdown, not fenced ASCII boxes. A missing
log alone does not make restoration incomplete when its necessary context was
recovered elsewhere. Terminal output keeps explicit status and the question after END.
Colours follow the client, while status stays explicit in words.
It ends with links and visible paths to the documents the
work already names; the backlog lives behind the *Open work* link.
`scripts/where_we_are.py` renders it from a summary Switch already holds, so
nothing extra is read and no status file is written. Conductor is loaded before
rendering and supplies *“Starting on X — approve?”* as the next-action question,
with its scope in NOW or THIS SESSION. A missing fact is asked as a clarification, not an
approval; supplying a project name alone does not start an install or launch.
A check belonging to you is labelled as yours, preserving any per-occasion
permission rather than presenting it as an agent job.
NOW holds short, owner-labelled actions for this sitting and their necessary
follow-through. Detailed checks, future-event work and later projects stay behind
Open work; immediate permission limits and blockers remain visible.
The single question after END asks directly about the recommendation;
you can decline or redirect without choosing from an offered alternative.
Existing local Agent bindings restore pairing context, with Agent loaded when a
contribution is requested. TEAM is one compact grid cell: Claude (role) + Codex (role).
Session IDs and notice status stay in Agent details. After restoring routing, In sends the established partners one
informational identity notice, with no work or reply requested. A repeated In
with the same sender/recipient IDs does not resend. Notice status is not peer
availability; a routing problem appears in ATTENTION when it affects the next action,
without making restored memory incomplete.
No dormant peer is resumed, and private IDs are not saved in project records.
For its own designated role, In verifies the actual session ID and can replace
the old binding from Out's prepared handoff or an eligible restart receipt;
genuine ambiguity needs a selection. Out
prepares that private handoff only after saving the final account. Old requests
keep their original session targets. Saved roles
are not live availability or permission to act. No second report follows. Roll keeps its
agreed continuation instead of stopping there.

**Out** reads what actually changed, preserves the agreement, decisions, exact next
action and open questions, and appends an evidence-backed account to the project's
history. Before editing the handoff, it checks ownership of any existing pairing
role, reusing an explicit replacement choice already given rather than asking
again. Out alone does not authorize taking a role. After the final save it reports
whether successor designation succeeded, was unavailable or was not applicable.
The saved account has a lean start point: rulings stay in CONTEXT.md while the
full case moves to `docs/decisions.md`, closed Backlog rows move to
`docs/backlog-archive.md` with their reason, the reading set for the next sitting
is named, and `handoff.py measure` records its size against the pickup target.
The handoff keeps the helper's exact `read_args` alongside that size so In reads
the measured selection, not a broader paraphrase. A lone heading includes the
remainder of its file; Out must narrow an oversized selection with real heading
boundaries or explain why it is needed, without discarding the evidence.
`scripts/handoff.py` does the Git work: explicit-file saves, safe fast-forward,
acknowledged local-only paths that are never staged, and a check that the remote
carries the exact commit. Out ends on the saved-place box: SESSION SAVED, SAVED
LOCALLY, NOT SAVED or SAVE STATUS NOT RECORDED in words, the tree, the local-only
leftovers, the next action and its reading set, and a reminder that the session
is still open. The Out owner combines participating sessions' contributions
under the [coordinated-closeout rule](skills/switch/references/in-out.md#one-coordinated-closeout).
Before drafting that account, the owner collects any missing contributor deltas
directly, reuses adequate returned results, and shows who is captured or missing.
The person should not have to chase each agent. Missing necessary material stays
explicitly incomplete; a late contribution reopens the check before finalizing.
MEMORY readiness is distinct from the Git save result; only a confirmed save
with a ready handoff suggests clearing context. Out retains its Markdown-in-chat
/ ANSI-in-terminal presentation.

### visuals (Diagrams)

Visuals makes readable product, process and system diagrams — connected-parts
views, responsibility flows, scope boundaries, decision paths. It produces an
actual rendered view, not a document made of text boxes. A lightweight Kerd
adaptation of Cathryn Lavery's diagram-design, with no CI, hooks, seals, branding
onboarding or approval schema required.

```
/kerd:visuals                # draw the thing being discussed
```

### kivna (Knowledge Management)

Kivna owns the project's knowledge layer, stored in an Obsidian vault at `~/eolas/vault/[project]/`. The vault is a human knowledge base. Every file answers a question someone would actually ask. No symlinks, no append-only logs, no session dumps. Files are living, updated in place.

Save (`/kivna save`) updates the vault's Status.md, updates the Weekly tracker (achievements and risks by week for quick status report generation), and writes updates to other vault files (Architecture Decisions, Playbook, etc.) — each change is shown in the save report, no approval prompt; anything marked "don't save this to vault" during the session stays out. Save is deliberate and on-demand — switch no longer calls it at the session boundary (v0.83.0); a vault is exactly as fresh as its last save. Scaffold (`/kivna scaffold`) creates the vault folder and the spine — MOC, Status.md, and Weekly.md — seeded from a short batched intake interview (≤5 open questions, one round), then suggests what other files might fit the project. Import (`/kivna in`) reads files from `kivna/input/` and integrates relevant knowledge, including structured `.kif.json` imports. Export (`/kivna out`) produces two files: `.kif.toon` (token-efficient for LLM handoff) and `.kif.json` (machine-parseable for cross-project import). Exports are repo-grounded: TODO.md, session logs, playbook, and vault status are read first, with conversation context filling gaps.

The folder structure:

```
kivna/
  vault.json   # vault config (points to ~/eolas/vault/[project]/)
  sessions/    # session logs from switch (committed)
  input/       # drop files here for import (gitignored)
  output/      # exports land here (gitignored)
```

```
/kivna in                                          # import from inbox (.kif.json, .md, .pdf, etc.)
/kivna out                                         # export as .kif.toon + .kif.json
/kivna out --full                                  # export all sections (adds playbook, architecture, memory, mode)
/kivna save                                        # update vault
/kivna scaffold                                    # set up Obsidian vault
```

### slainte (Project Health)

Slainte is the release pass, plus on-demand health audits. Run `/kerd:slainte release` when a version bump or an acceptance record lands — Conductor does not trigger it on its own — and it sweeps the repo's own narrative surfaces — README sections and What's New, the playbook, the state contract, the capability lists, any living design doc the release touched — fixes what is drift, and names in its report what it deliberately left untouched, so restraint is visible instead of assumed. Fixes land as normal work commits under the caller's verification gate, and prose it writes passes skriv's one-shot audit first. The mechanical layer stays CI's (version sync, capability lists, namespaces — R1–R3 and AU1–AU10); slainte owns the judgment layer: skill-count claims, frontmatter drift, marketplace URL, hook template currency, and cross-doc claim verification. There is no config file — targets derive from the repo.

The on-demand area audits (docs, code, site, deps, playbook, release) still run any time, report-only by default. Everything gets a severity grade: high (factually wrong, broken build, security vulnerability), medium (stale but not misleading), low (nitpick).

```
/slainte docs         # audit docs area
/slainte playbook     # audit the playbook
/slainte release      # the release pass's judgment checks, on demand
/slainte all          # audit everything
```

### skriv (Writing Voice)

Skriv enforces a human writing voice. It has a kill list of words no one actually uses in conversation (leverage, facilitate, delve, holistic, the whole lot), bans all dashes as punctuation (em, en, and double hyphens) along with five-paragraph essay structure, catches synonym cycling and chatbot residue, and runs a self-audit ("what still sounds machine-made?") before cutting 20%. The goal is prose that reads like a first draft by someone who's been in the room, not something generated.

Three modes. Audit reviews a file and reports violations with line numbers. Fix rewrites the file in place. Session mode applies the rules to everything you write for the rest of the conversation. When session mode is on, skriv shows `[skriv: active]` at the top of responses and `[skriv: off]` when it ends.

```
/skriv README.md       # audit against the rules
/skriv fix README.md   # rewrite applying the rules
/skriv on              # session mode on
```

### tend (Structural Health)

Tend audits repo infrastructure against current Kerd conventions and fixes what's drifted. Run it on a new repo to set up everything from scratch, or on an existing repo to catch drift after a Kerd update. It checks nine categories: directory structure, required files, vault integration, deprecated patterns, naming consistency, stray/stale files, .gitignore hygiene, skill hygiene, and hook hygiene.

The report shows each category as passing (✓), failing (✗), or warning (⚠). Failing and warning items get a current-vs-proposed table with reasons. After the report, choose to fix all, pick individually, or skip. Tend makes changes but never commits — unlike conductor's work commits, structural convergence has no verification gate behind it, so it stays in the working tree for you to review.

```
/tend
```

### lorg (Skill Gap Analysis)

Lorg scans the current project and recommends skills or plugins you should be using but aren't. It works in three tiers, each runnable independently. Tier 1 checks what's already installed but underused (not invoked in the last 30 days). Tier 2 searches the Claude Code marketplace and a curated list of repos you maintain for plugins that fit your project's tech and themes. Tier 3 goes wider: GitHub and web search for trending or new plugins you haven't heard of yet.

The default (`/lorg`) runs Tier 1 only: fast, cheap, no web dependency, most actionable. Use subcommands for wider search. Each tier tracks its own freshness date, and running one tier preserves the others in the report.

The recommendations aren't just based on file types. Lorg reads your README, playbook, TODO, session logs, and vault decisions to extract work themes (fundraising, compliance, content creation, whatever keeps coming up). Results are ranked by relevance (theme match + tech match + recency boost - install friction) so the strongest matches appear first. Weak matches below a threshold are dropped.

The report is saved to `docs/lorg-report.md` (committed) and the Obsidian vault (searchable). Updates are incremental: only scanned tiers get overwritten.

```
/lorg                # Tier 1 only (installed but unused)
/lorg installed      # same as default
/lorg available      # Tier 2 (marketplace + curated sources)
/lorg explore        # Tier 3 (GitHub + web). Opt-in research.
/lorg all            # full scan across all tiers
/lorg report         # show last saved report
```

### pair (Partner Mode)

Pair toggles how you and Claude work together. Off by default — the full, show-your-reasoning style stays the resting state so you keep learning. Turn it on to move fast: Claude keeps its thinking internal (surfacing it only when it changes your decision, it's stuck, or you ask), asks one clear question at a time — open by default, offering a tight set of 2-4 crisp options only when a menu genuinely clarifies a choice that's yours to make (never a lazy binary or a vague, verbose list) — interrupts early to flag or check in, and works like someone sitting beside you rather than narrating every step. It's per-repo state (`kivna/.pair`), enforced by an opt-in `UserPromptSubmit` hook that re-injects the partner-mode reminder each prompt while on. Pair governs interaction style only — your `CLAUDE.md` thinking discipline applies either way. (Renamed from `focus` in v0.64.0 to avoid colliding with the harness's native focus mode.)

```
/pair on             # rapid partner mode
/pair off            # back to full reasoning
/pair                # show current state
```

## Hooks

Kerd ships three hooks that provide session boundary awareness and the pair toggle. They **auto-load from the plugin** — the moment the Kerd plugin is enabled, Claude Code registers them from `hooks/hooks.json`. There is no per-repo wiring, and nothing to keep in sync when Kerd updates: the standard plugin-hook mechanism resolves the path at runtime, so it never version-rots. Each hook is silent unless the repo carries Kerd state, so they no-op cleanly in non-Kerd repos.

**SessionStart hook:** On same-machine resume, checks if the local branch is behind remote, reads the last session date from TODO.md, and reports any interrupted mode. Suggests `/kerd:switch in` when there's stale state. Silent on a fresh start.

**Skill completion hook:** When a mode is active and you complete the current step's skill, shows your progress and what's next. Read-only — it never writes `.active-modes`.

**Pair hook (`UserPromptSubmit`):** While pair is on for the repo (`kivna/.pair` = `on`), injects the partner-mode reminder into every prompt. Silent when pair is off or absent. See the pair skill above.

Older repos may still carry manual hook entries in `.claude/settings.local.json` from the pre-0.96.0 wiring mechanism — version-pinned cache paths that break the moment Claude Code garbage-collects that cache version. `/tend` (category 9) detects and removes those; the plugin provides the hooks itself now.

**Statusline segment (`hooks/statusline.sh`):** not a hook — it sits beside them and wires into `statusLine`, never into `hooks`. It prints the wall-clock time as `HH:MM`, and it **composes rather than claims** the slot: hand it an existing statusline command as its single argument and it prints `HH:MM · <that command's output>`, forwarding the context JSON on stdin unchanged. Machine-local and opt-in — `/tend` does not register it.

Free slot — point `statusLine` at the script:

```json
"statusLine": {
  "type": "command",
  "command": "/absolute/path/to/Kerd/hooks/statusline.sh"
}
```

Slot already taken — pass the command that is there now as the argument, quoted:

```json
"statusLine": {
  "type": "command",
  "command": "/absolute/path/to/Kerd/hooks/statusline.sh '/absolute/path/to/existing/statusline.sh'"
}
```

Both paths must be absolute and already resolved: `${CLAUDE_PLUGIN_ROOT}` does not expand inside a settings file (the v0.29.1 hook-path gotcha).

The three hooks are covered by a bash test harness, `tests/hooks_test.sh` (path resolution under unset/empty `CLAUDE_PROJECT_DIR`, missing-file branches, behind-remote detection, the SessionStart staleness report, the pair toggle's on/off/absent branches, and a check that every script named in `hooks/hooks.json` exists and is executable). Run `bash tests/hooks_test.sh` — it shellcheck-lints the hooks as part of the run.

## Entry gates (tools/gates/)

Entry gates route work by construction. Given a work slug, `tools/gates/gate.py` runs the gate table in series and enters at the lowest rung whose declared inputs all exist on disk — front matter, named sections, a qualified risk ledger, a declared rigor level, a checked-box count. It has no opinion on whether a claim is convincing or a design is sound, only whether the artifact is present; a refusal names exactly what's missing for the next rung, never a vague "not ready."

It's the first check in the system that blocks from outside the model. The repo-wide audit (rules AU1–AU10) runs on every push: dated filenames in `docs/design/`, malformed gate records, broken `## Grounding` references, a `## Scope` without its `Rigor level:` line, and a requirements register drifting from its declared schema — an unknown field, an illegal state, an `Approved` hash diverging from the statement it approved, a link naming an ID that does not exist — all fail the build before a human or a model catches them in review. CI runs nine steps in total — the three gate sweeps, the progress and matrix checks below, the journey stage-schema check (`gen_journey.py check`, which refuses when the step definitions stop matching the stages they render), and the handoff fidelity check (`tools/gates/fidelity.py`), which skips itself unless the push writes a session log.

```
python3 tools/gates/gate.py route <slug>
python3 tools/gates/gate.py check <slug> <rung>
python3 tools/gates/gate.py audit
```

## Progress board (tools/diagram/)

Position is derived, never asserted. `tools/diagram/progress.py` computes every work item's place on the ladder from git log, gate routes, contract checklists, and gate records, and renders it as a committed trio (Excalidraw + SVG + HTML). CI byte-compares a fresh render against the committed pair at every push — a stale board is a red build with the fix quoted. The same kit draws the design packages reviewed on the live canvas.

```
python3 tools/diagram/progress.py          # render the board (three files)
python3 tools/diagram/progress.py stale    # the CI check
```

## Design matrix (tools/design/)

The evaluation matrix is how options are compared — criteria with declared targets and M/D categories set before any option is scored, options as rows each with a drawn architecture overview, Toyota marks per cell (○ = meets · △ = meets only with a named countermeasure · × = cannot meet), scores citing evidence, and a recomputed OVERALL/RANK. The tool refuses what the format forbids: undeclared criteria, scores without basis, △ without countermeasure + confidence, arithmetic drift, and a dead option (× on a Mandatory criterion) named Preferred. Validation fires wherever a matrix section exists in `docs/design/*.md` — on every push, in CI.

```
python3 tools/design/matrix.py check <file>    # validate one design doc
python3 tools/design/matrix.py audit           # sweep docs/design/ — the CI step
python3 tools/design/matrix.py render <file>   # movement-9-style table → .excalidraw + .svg
```

## How They Fit Together

**Starting a project:** Create a repo, clone it, run `/tend`. It checks what's missing, shows you the plan, and sets up the full structure with your approval. Run `/lorg` to find plugins that fit your stack. Then `/conductor` and say what you want to make happen.

**Day to day:** You sit down and run `/switch in`. It syncs the branch, reads the project's current-context pointer (CONTEXT.md by convention), the `## Now` section of TODO.md and the newest session log, plus whatever reading set the last session named, and loads Conductor to compose the welcome-back dashboard. NOW carries owner-labelled next actions; the single arrival question — *"Starting on X — approve?"* — follows END as a bold speech-bubble callout, without a second report. Say yes and the work runs under Conductor, with decisions recorded in the work record and CONTEXT.md as they're made. When you're done, `/switch out` writes the session log, tidies the active lists, names the next session's start point and reading set, and commits and pushes the named files. Run `/slainte docs` any time to check nothing drifted, and `/slainte release` after a version bump. The Obsidian vault refreshes only when you ask — `/kivna save`. Next session, same state, on this machine or another. Periodically run `/lorg` to check if new skills have emerged that would help with the project.

**On cheap boundaries — a capability that's gone.** Until v0.90.0 you could run `/switch out light` or `/switch in low` to spend fewer tokens at the boundary. Those modes are removed, and that is a real reduction in what you can ask for, not a tidy-up. They went because each one bought its saving by recording less or reading less, and a boundary that records less is exactly how a fresh session ends up contradicting something you already decided. Cost is handled instead by the read set staying small — the pointer, `## Now`, the newest log and the named reading set — and by Switch Out moving each decision's case to `docs/decisions.md` once it stops governing the next work, so those files don't grow without bound. If a boundary feels expensive, the fix is a leaner start point at the next Out — not a shallower read.

**The layers:** The session boundary is defined once, in switch — sync on switch-in, the named-file save and remote check at switch out — and you call it directly. Conductor owns the sitting: understanding, agreement, delivery and assessment, committing its own work as it verifies. Kivna owns the knowledge vault. Above them sits the ladder: every piece of work is a slug climbing frame → viability → scope → design → handoff → loop → acceptance, with `python3 tools/gates/gate.py route <slug>` reading what is on disk and naming the rung where the work enters, the progress board showing derived position, and CI refusing at every push what a document promised and the tree no longer delivers. Every skill works standalone.

## Naming

Gaelic-inspired where it adds character:
- **Kerd**: skill (ceird)
- **Kivna**: memory (cuimhne)
- **Conductor**: keeps one session in tempo (renamed from *dian*, Gaelic for intense/rigorous)
- **Skriv**: the act of writing (scríobh)
- **Switch**: session handoff
- **Slainte**: health (slàinte)
- **Tend**: from English "to tend" (care for, maintain)
- **Lorg**: to seek, track down

## License

MIT
