# In: useful context

Contents:

- [In](#in): named handoffs first, a managed Roll record, Git synchronization, the pickup reading set and the coverage check
  - [Compose the arrival in Switch](#compose-the-arrival-in-switch): weigh every open item, one recommendation
  - [Restore the existing team](#restore-the-existing-team): pairing, succession and the arrival notice
  - [Enter Conductor from the answer](#enter-conductor-from-the-answer): what each answer to the arrival question opens
  - [Welcome back: the screen summary](#welcome-back-the-screen-summary): the renderer, its JSON shape, the question and picker

Closing a sitting is in [Out](out.md); To and Roll are in [To and Roll](to-roll.md).

## In

For a precise To handoff, read the entry and destination instructions in
[To and Roll](to-roll.md). Use its exact saved revision with the helper's `--commit`
option; don't replace it with “whatever is latest”. Require source-release evidence
before continuing active work. Ordinary latest-state pickup is unchanged.

A specifically named handoff takes precedence over generic pickup discovery.
Check its supplied repo, branch and record first, using only necessary local
identity checks and explicitly authorized Git synchronization. Missing or wrong:
stop before reading a legacy checklist as the task. A machine being reachable or
able to build does not prove that the intended handoff was restored. Once found,
read the handoff's authority before acting on linked project instructions; standing
project notes cannot expand a read-only trial into probes, builds or deployment.

Resolve the current project and branch. When the restored work is a concert on
its own branch, a checked-out branch other than the one its sketchbook records is
a consequential contradiction for ATTENTION, not a place to continue or save.
Before any fast-forward or work proposal,
check whether `git rev-parse --git-path roll/run.json` names an existing managed
Roll record in this worktree. If present, use the packaged `roll_status.py
--project /absolute/project` read-only. Recorded running/held, blocked/failed/uncertain
or handed_off/awaiting_destination state is not permission to adopt a controller, change
its checkout or propose competing work. Keep restoration local/read-only, show
the recorded ownership issue in ATTENTION, and make the next action inspection
of that ownership rather than starting the same build. Unreadable or unknown
state remains unresolved; do not treat it as no run. A recorded status is not
a live-process check or permission to kill anything. Follow the Roll recovery
guide if recovery becomes the selected work. A paused/continue checkpoint resumes
through the managed Roll path after ownership is established, not ordinary inline
delivery from a stale TODO. Review means independent assessment is next, not
acceptance or permission for another implementation; reconcile that saved place
before proposing its assessment. Private Agent identity/succession/arrival may
still follow their existing authority, but do not transfer managed-run ownership.
With no record, add no discovery or setup step. An unclaimed chat roll marker
(`roll/chat.json`) is shown in ATTENTION and never acted on by ordinary In; only
`/kerd:switch roll in` claims it. Do not infer completion merely
because the worker stopped; a reconciled finished run need not stay a warning.

For a typed managed-Conductor record, paused continuation uses
`conductor_roll.py`, not the legacy worker `roll.py`. A complete record is a
reported result: reconcile the evidence and retire the retained owner record
before a new run, as the managed-Conductor guide describes. Do not silently
reuse it or treat a completion label as proof of acceptance.

An explicitly requested Git-backed pickup
includes synchronization under the agreed Git authority. Inspect local changes,
staged work and remote identity first; preserve them. Fast-forward only when safe.
Don't auto-stash, force-reset, resolve a meaningful conflict by guessing, or quietly
claim local memory is current with GitHub when sync failed. An offline/local-only
pickup can proceed only as such, with that limitation visible.

Read the project's existing current-context/handoff pointer, its designated
project active list (by convention `TODO.md`'s `## Now`, including child
sections), and explicitly current work records linked from that pointer/list.
Do not scan every repository `work.md`. Recover current stage, actual user
agreement, last result, pending question or next action, failure/resource state,
relevant current decisions, standing constraints and known risks. A missing or
old pointer can require a bounded lookup for the current project list and linked
records. Saved `read_args` identify where to begin; they do not authorize omission
of that active work. Follow necessary evidence links and retrieve the complete
relevant entry when proposing from it; avoid loading the full log archive and
every retired plan. If bounded local retrieval cannot establish the missing
coverage, name that gap honestly rather than sweeping history. An explicitly stale
or contradictory pointer must be reconciled with current artifacts and dated
evidence before work continues. What makes a pointer stale is
an obsolete next action, not an old revision: `overtaken_revisions` in a pickup or
prepared packet is a diagnostic hint, and citing history or a pre-save position is
legitimate. Reach an exhaustive changed-file list with `git show --name-only` on
the named boundary rather than reading a manifest copied into memory.

Local files a project has deliberately kept out of Git do not block a pickup.
Name those exact paths with `--preserve` and the helper proceeds, reporting them
as local only; it stops, untouched, if the incoming revision carries one of them,
because that collision is a real decision. Unnamed changes still stop a pickup.

The start point names a **pickup reading set** — the exact files and complete
sections Out chose for this next action and wider active-work orientation (see
[Leave a lean start point](out.md#leave-a-lean-start-point) in Out). A reading-set entry written `notes:<path>`
is read from the notes root (`kivna/vault.json`'s `work_notes`), not the repo.
Reading one also fetches the vault repo that holds it: refuse to read unsaved
vault notes, or a vault missing the commit Out recorded, rather than showing a
stale or partial sketchbook.
Pass that commit to `prepare` or `pickup` as `--notes-commit <sha>` (with `--sync` to
fetch it and fast-forward only).
When the handoff includes the helper's `read_args`, use those exact file/heading
selections, not a broader paraphrase. They are arguments to `prepare` (with the
current project and branch supplied), or the boundaries for reading normally.
Read those first, in full. They are a saved navigation aid, not a ban on further
reading: also cover the pointer-designated active list and child sections, its
explicitly current linked work records, governing current decisions, standing
constraints and known risks; check linked detail when a
contradiction, orientation gap or recommendation requires it. Where the host can
assemble those named sources before starting the fresh worker, use `prepare`
(see [the helper notes](out.md#default-verified-save-when-pushing-is-authorized)) so the model receives their text once. Otherwise read them normally.
For a long work record, locate its current-position section before reading from
the top. Then load its named agreement and supporting sections. A supplied record
path is not by itself a reason to load every prior implementation observation.

Restore saved state; do not re-audit every citation during pickup. A current,
sourced handoff can establish what the last sitting recorded. Open supporting
history when the current record is missing, contradictory, or insufficient for
the next action or its authority—not merely because it contains a link. Keep
saved observations distinct from fresh verification. If no build is active,
there is no reason to load its whole stage history or neighboring backlog work.
When deeper retrieval is needed, read the complete relevant entry, not a broad
range of adjacent tasks; a few very long lines can still load pages of material.

Ordinary In ends with restored memory, the open work and one recommendation on
screen, stopped at its arrival question. It does not load Conductor or its
journey guide to compose it. It does not execute the plan, draft replies, start
reviews, repair files or investigate backlog issues. Keep checks to safe requested
Git synchronization and resolving facts necessary to restore position; flag other
uncertainty for the work itself. Do not measure pickup cost inside every pickup;
assess the session logs afterward unless measurement was requested. A user
explicitly asking to continue after In can proceed through Conductor without
another approval. Managed To/Roll remains separate and keeps its agreed
continuation. When nothing actionable is open, say so rather than
manufacturing work. Existing project restrictions
still apply.

Context-cost targets come from the work agreement, not a universal magic number.
Report added input separately from host overhead where measurable. The Switch trial
uses 8,000 additional input tokens and 5% of observable usable context, plus correct
restoration. A shorter but incomplete read fails; unknown usage is not a pass.

When the caller already supplies complete current records and verified local Git
identity, use that material directly rather than discovering and reading it again.
Keep its file/section labels and saved-versus-current distinction. Supporting
links remain available for genuine gaps; a prepared pickup is not a declaration
that historical sources can never matter. The caller selects from the project's
existing memory structure, not a universal fixed list of filenames.

Before calling restoration complete, check the answer against the supplied current
records for the pointer-designated active list (including child sections), its
explicitly current linked work records, unresolved decisions, owed work, standing
constraints and known risks. Keep these in the
restored working state, even when the user-facing summary only shows the next one.
Preserve explicit prohibitions, parked choices, unknowns and not-yet-authorized
actions; do not silently replace them with defaults or drop them for brevity.
Keep the short screen summary separate from retained working state. The existing
source records remain authoritative: keep their named complete selections linked,
and preserve operative conditions in source wording when a portable restoration
record must carry them. Never replace them with labels such as "settled privacy
decisions" that hide an open experience choice or an exception. Open decisions,
settled constraints and instructions for retrieving deeper detail stay distinct.
Do not create another living rules file merely to repeat the same source text.
The short display may show only the next action; it must not imply that omitted
choices are settled or that it is the complete working state.
This is a coverage check of material already loaded, not an instruction to read
the whole archive. A small input is useful only if its meaning survives.

### Compose the arrival in Switch

Switch chooses and presents an orientation from the restored material itself.
Do not load Conductor, its journey guide or another skill for composition.
Carry the project, open work, agreement, restrictions and pending decisions
forward in context; no extra record or repeated pickup reading set.

The arrival tells the person, in plain product English, where things stand, what
work is open and what Switch recommends doing next and why. Describe what the
product does and what is left before its next milestone, never the agent's own
activity: "nothing is being built" is agent state, not a position a person can
use. Name work by what it changes for the person (“the risk-rating change”), not
by its internal slug, unless they need the slug to find it. It does not repeat the last
session's saved next action merely because it was saved.

**Weigh every open item, the saved one included.** Take the designated active
list (with child sections) and any [saved selection](out.md#save-the-selected-continuation),
with the other choices Out previewed beside it, as candidates. For each, ask: does it move the product or the person's work
forward, and why would it come before the others? Current user direction takes
precedence; recorded priority, dependency and authority inform the order. A saved
selection is one candidate with its recorded reasons, not the answer. Work that
only proves the project's own mechanics (a self-check, a record tidy, evidence
bookkeeping) does not lead unless it blocks the product work or the person asked
for it. If evidence shows the saved selection stale or completed, say so plainly.

**Watching is not buildable.** An item that waits for behaviour to be seen in real
use (“watch X in real use”, “keep using it”) or for the person's own decision is
open work, never the recommendation: nothing can be built on it now. When no item
in the active list is buildable, **Where things stand** says so plainly (“nothing
in Now can be built; it holds things to watch and your decisions”). Recommend the
saved selection when it is a concrete item; when it too is a watch item or
missing, read the project's Backlog section (that one section, not the archive)
and recommend one concrete item from it, with Out's other previewed concrete
items or the Backlog's next ones as the picker's other options. Still none: the
recommendation is `null`, never a meta-item such as “use Kerd on real work”.

**Open work** lists the items that move the work, one plain line each, in
recommended order, with no file names, line numbers or internal labels unless the
person needs them to recognize the item. Keep a human-owned check or a pending
decision in the list as what it is; do not dress it as agent work. Items
omitted from the screen stay open behind the documents link; omission changes
neither their status nor the saved priority.

Where the restored material says where an open item stands, its line says so in
plain words: what is settled and what is still open (“the season picker: goals
and design settled, constraints still open”). Do not grade it or add a meter.

**Recommended** names exactly one item and **Why** gives the reason it comes
first, in one or two sentences a person can check. A recommendation is not
agreement or permission. Recommend the first actionable item when nothing else
distinguishes them; if nothing is actionable, say so rather than inventing work.
For a saved unresolved choice, recommend one grounded route, leaving alternatives
behind its link. An unresolved design is not permission to build; a project name
supplies a target, not permission to install or launch.

This arrival stops at one question: **“Start a Conductor session?”**, with the
recommendation as its proposed answer. Every answer that chooses work goes
through Conductor; only a deferral or the person's explicit refusal of Conductor leaves it. It does not
select work, create a native session, execute project work, launch workers or
grant permission. Private Agent routing maintenance below is not work
authorization. Compose the arrival using the
[summary rules](#welcome-back-the-screen-summary), return its renderer output
unchanged and stop; no second list, task menu or narration.

### Restore the existing team

If collaboration is already established, restore it too. Resolve the local
pairing directory with `git rev-parse --git-path kerd-agent/partners` in the
current project; if it exists, read its binding metadata, not request archives
or transcripts. Use only bindings for this project; malformed or conflicting
metadata is unresolved, not a reason to guess a peer. The directory is local to
this Git worktree, not shared with linked worktrees or transferred by Git.
With an existing binding, retain the sibling [Agent](../../agent/SKILL.md) as
the route for later contributions; load its full instructions when a contribution
is requested, not merely to display a pairing. Retain the exact
provider, alias, session ID, recorded ongoing role and any recorded review cadence
privately in context. TEAM still shows provider and role only; the cadence is for
Conductor's review planning, not the dashboard.
First compare the actual host's session variable (`CLAUDE_CODE_SESSION_ID` or
`CODEX_THREAD_ID`) with the bindings, and look for a `handoff` designation or
`recovery` receipt (including its retired IDs).
When an ID matches or either form of continuity evidence exists, read the short
[succession guide](../../agent/references/session-succession.md) and check its
verified identity. Same ID keeps the binding; an authorized successor uses its
prepared handoff, eligible restart receipt or explicit selection. A retired
session reports the moved role instead of reclaiming it. Only this private routing update is
permitted during In alongside the informational arrival notice below, never a
project repair or plan execution.
This restores routing, not a running job or a Conductor mode. The succession
helper's native identity/absence check is allowed for restart recovery. Do not
otherwise discover or resume peers merely to validate a binding.
Availability stays unverified until Agent checks the selected target for work.
Missing roles stay undefined; ambiguous bindings remain a choice when a
contribution is requested. No binding means no Agent setup question during In.
After identity and any required adoption, run Agent's bounded
[arrival notice](../../agent/references/session-succession.md#arrival-notice-and-team-display)
for the selected established partners, or the helper's unambiguous private
pairing default when the restored context names none. The caller does not
enumerate aliases as recipients; the helper reads private binding metadata and
selects only an unambiguous partner, never by title or recency. Show the team
in the arrival grid's TEAM cell: `Claude (role) + Codex (role)`. Use brief faithful role labels,
not new assignments; a missing role stays unassigned. IDs and routine notice status
remain in Agent details, not the dashboard or project records. Surface a routing
problem in ATTENTION only when it affects the recommendation. A failed notice does not make restored memory incomplete.

### Enter Conductor from the answer

Resolve the whole answer to **“Start a Conductor session?”** against the open
work and any explicit authority it carries. Every answer that
chooses work goes through Conductor, so a person wanting guidance always has one
way in:

- **Chooses work** (“yes”, the recommendation's picker option, another open
  item's picker option, “the migration sign-off”, or new work in their own
  words): invoke `/kerd:conductor` through the host's skill
  mechanism at Shape for that work. Naming or accepting the work
  selects it; it does not approve its operations. Conductor shows the shape and
  asks its own scoped approval before builds, installs, pushes or other
  consequential actions. A plain yes accepts the recommendation as the work to
  shape, nothing more.
- **Chooses and authorizes** (“sign off the migration, go ahead”, “design the
  alert, no deployment”): invoke Conductor for that actual work at its actual
  stage, carrying the approval and its exclusions. For example: “Start the
  approved alert-design work in this project from the restored work record.
  Design only; no implementation or deployment. Enter the work without repeating
  pickup or intake. Read Kerd's orchestration startup and relevant
  job-split/work-view sections if not already loaded, then begin with Conductor ·
  Shape, current model/effort evidence, owner, intended design result, stopping
  boundary and work split. Only then start substantive project research.” For
  underway work, say resume.
- **Asks for guidance without choosing** (“Something else” from the picker,
  “not sure”, “help me decide”): invoke
  Conductor at Understand/Shape for direction-setting with the full open-work
  context; it recommends from local context before asking for recorded facts.
- **Defers** (“not now”) or **reports a fact**: start nothing. A fact or
  human-check result is usable evidence within existing authority to record it;
  show what it changes, but it is not a work choice unless the person also makes one.
- **Explicitly declines Conductor for named work** (“no, just fix the typo”):
  the person's own refusal, not a route the arrival offers. Carry only the
  approval the person actually stated for that task, and its limits, into
  ordinary host work. Never infer it from an answer
  that simply names work; naming work is **Chooses work** above.

Pass the restored project, full open-work context, the chosen work and pointer,
known authority, exclusions and unresolved questions. Resolve Conductor from this
distribution, not another cache's file. Do not ask a second time what to move
forward, and do not substitute related backlog work for an excluded item. When
native invocation is unavailable, read Conductor's work-entry section and the
relevant guide explicitly and disclose the fallback. Missing Conductor is a
stated limitation, not a silent replacement workflow. Availability for a
human-owned check is not an agent-work approval or its result. Managed To/Roll
goes straight to its authorized continuation, never through this arrival question.

### Welcome back: the screen summary

After restoration, orient before detail, in plain English. The arrival opens with
its heading, then a one-row grid, then the text:

- **Heading:** the project, the completion state, and the Kerd version the
  renderer read from its own package manifest (for example `Kerd 0.150.0`), or “Kerd version
  not read” when none is readable. The caller supplies nothing for it; it names
  the build that drew the screen, never one remembered from a record.

- **Grid:** PROJECT; PHASE, the recommended work item's rung on the project's
  ladder (frame, viability, scope, design, handoff, loop, acceptance, or the
  project's own stage names), `null` when the item has none; NEXT, the
  recommendation; TEAM, the restored pairing.
- **Where things stand:** one or two sentences on position in the wider work, in
  product terms: what the product does now and what is left before its next
  milestone. Not the agent's activity.
- **Last session:** what changed for the person, one sentence.
- **Open work:** the items that move the work, one line each, in recommended
  order (see [weighing](#compose-the-arrival-in-switch)).
- **Recommended** and **Why:** one item and the reason it comes first.

Close with the document links, on one line in chat Markdown; the task list carries the label **Open work**
and points at the existing work/status page — HTML where one exists, otherwise
the Markdown record or task list. Resolve a real target; don't invent a page or
build one during In. The backlog and audit evidence live behind that link.
Being short does not suspend the rules above: a contradiction, failed
synchronization or restriction still appears on screen.

Write each line for a reader who has not opened the source. Keep each item to
the action and its outcome; move procedures (clicks, restart sequences) and pass
criteria (expected values or states) to the linked task detail. Keep details
needed to identify the right target, distinguish scope or avoid an immediate
safety or permission mistake. Where an item has an established owner who is not
the agent, say so in the line (“Anthony: check the stats panel on the TV”); the
renderer displays `**Owner:** action` notation when supplied but neither assigns
owners nor chooses priorities.

**ATTENTION** covers material limits on the recommendation or on safe
restoration: failed synchronization, a consequential contradiction, a falsely
recorded decision. Also retain risks the restored record itself flags as urgent
or imminent, even outside the recommendation, unless already resolved by
available evidence. Keep each brief and distinguish the dated saved observation
from a fresh check; this is not permission to relabel every owed item urgent or
re-audit them at pickup. Open items that are merely owed belong in Open work,
not ATTENTION.

An **Insight** is optional: one source-grounded learning, implication or tradeoff
in its own callout — never compulsory, never a hidden question.
A log preserves a reported claim; it does not prove someone observed the event.
Missing logs do not make verification impossible, and reconstructing a log does
not resolve conflicting claims. Keep the uncertainty visible or omit the Insight.

Render it with the packaged renderer, [scripts/where_we_are.py](../scripts/where_we_are.py),
resolved relative to this skill so it travels with the package. Finish weighing
and composing **before** this call:

```sh
printf '%s' "$summary" | python3 "$SKILL_DIR/scripts/where_we_are.py" --summary - --markdown
```

The complete stdout from this call **is the final assistant message**. Return
it unchanged: no paraphrasing, added intro or second question. The screen is reply text: paste the rendered output into the message itself, before the picker in the same message; output left in a tool result has not been shown, since the host folds it away. Rendering is the
last step of In, not material for another writing pass. If content needs
correcting, change the summary and render again; use that latest complete
output. If the tool output is truncated, retrieve the complete result rather
than reconstructing missing text. A genuinely unavailable renderer uses the
disclosed plain-text fallback below, not a claimed renderer result. Use
`--markdown` in assistant chat; terminal output is the plain-text fallback. The
client may style numbered lists as letters; do not rewrite content to undo
client styling.

The screen ends on the single question, as a bold speech-bubble blockquote:
`> 💬 **Start a Conductor session?**`. Nothing follows it: no footer, render
time or end marker. Ordinary In always supplies this question, including when
nothing is actionable. Do not add a second question; the open items are its
context, the recommendation its proposed answer. The renderer places the
question; do not append it yourself. Where the host offers a native picker,
follow the rendered output with up to four options: **“Yes — <the recommended
work>”**, naming the work it opens; up to two other open items from this
arrival's weighing, each named by the work it opens with a one-line why; and
**“Something else”**, which opens Conductor to ask what. The host's free-form
route stays open. Picking any work opens Conductor at Shape for that work and
approves none of its operations; where the picker carries descriptions, each
work option's says so, so an action-worded item (“Release 0.137.0”) is never
read as approval. A plain yes still means the recommendation. The other items
are this arrival's own weighing, not the saved preview copied: the saved
choices stay candidates, and the recommendation stays one item. The picker never
replaces or precedes the bubble, and never stands in for the screen: a picker
with no screen in the reply above it is a skipped arrival. Without picker support, the bubble is answered
normally.

The question ends restoration, not the session, and starts no work. Partial or
unknown restoration shows SWITCH IN INCOMPLETE in the heading and its gap in
ATTENTION. Keep
values brief; the renderer wraps rather than truncates. `--color` forces ANSI,
`--no-color` or `NO_COLOR` disables it. Markdown never emits ANSI.

`$summary` is the shape below, filled from what pickup already read. **Copy it
from here; do not open the script to work out the keys.** The example is one
coherent sitting. Use `null` or `[]` for anything the work has nothing for.

```json
{
  "project": "Kerd",
  "phase": "acceptance",
  "where": "Kerd is released and working. Five steps stand before launch and none is done; the first is signing off the risk-rating change, which shipped two weeks ago.",
  "open_work": [
    "Sign off the risk-rating change with real evidence, the first launch step.",
    "Try the 0.134.0 diagram rules on a real diagram; they have never been exercised.",
    "Anthony: decide whether the 2026-09-13 \"prove Kerd first\" hold is lifted."
  ],
  "recommendation": {
    "text": "Sign off the risk-rating change.",
    "why": "It is the oldest product commitment, and every later launch step waits on it."
  },
  "last_session": "Released 0.134.0, the Visuals contract correction, after two review rounds.",
  "team": [
    {"provider": "claude", "id": "11111111-1111-4111-8111-111111111111", "role": "current session", "self": true, "status": "identity verified"},
    {"provider": "codex", "id": "22222222-2222-4222-8222-222222222222", "role": "expert review", "status": "submitted-unconfirmed"}
  ],
  "question": {
    "text": "Start a Conductor session?",
    "proposed": null
  },
  "documents": [
    ["Open work", "TODO.md"],
    ["Launch plan", "docs/design/launch-plan.md"]
  ],
  "warnings": ["The installed version is a saved observation, not rechecked during pickup."],
  "insight": "The migration shipped two weeks ago; only its acceptance record is missing.",
  "base": ".",
  "restored": "yes",
  "restore_note": null
}
```

`project` is the project already restored, never inferred from the renderer's
installation path. `phase` is the recommended item's rung, shown in the grid;
`where` is the position sentence; `open_work` a list of plain
lines (a single string is one item); `recommendation` carries `text` and `why`,
or `null` when nothing is actionable, which the renderer states. `question.text`
is the one arrival question; leave `proposed` null, since the recommendation is
already on screen. `documents` are `[label, path]` pairs resolved against
`base`; a path that does not exist is reported as a warning rather than offered
as a link. Supplying `open_work` or `recommendation` selects this layout; the
renderer's older grid keys (`task`, `state`, `now`, `this_session`, `source`,
`updated`) remain only for record-driven views and older callers, and new
arrivals do not use them.

`team` uses the Agent arrival result's array; the fictional IDs above illustrate
its input shape only. A caller may shorten a role's wording faithfully for
display, without modifying its private binding or assigning new responsibility.
Do not synthesize the team from project history or a legacy bridge's
collaborator names. The renderer groups identical identities and displays
providers and roles only. Use `[]` for no established pairing and `null` for
unread/unresolved state. A consequential routing problem belongs in `warnings`;
routine unconfirmed notice delivery is not a blocker or an availability claim.

Given a correctly shaped JSON object, fields are not required: a missing or null
one degrades to a plain “not recorded” line or an explicit “nothing open”
statement rather than an error. Malformed JSON exits 2 with a message. Where
things stand, Last session, Open work, Recommended and the grid always render; only
the attention panel, documents and Insight are omitted when empty.

It reads stdin, so nothing is written to disk. Do not re-read files to fill it,
and do not stop for approval before showing it. Only if rendering fails or the
renderer is unavailable, disclose that failure and present the restored facts
and single question as plain text.

`restored` states whether the necessary context was recovered. Use `yes` when
the necessary position, authority and open work were recovered, even with a dirty
tree, unpushed commits, pending approval or a missing log whose necessary content
was recovered elsewhere. Use `partial` or `no` only for a material context gap,
and name it in `restore_note`. Missing session paperwork alone is not a failed
restoration. Never turn a reconstructed claim into verified evidence merely to
make the banner complete.

