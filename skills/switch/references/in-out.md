# In and Out: useful context, clean boundaries

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

Resolve the current project and branch. An explicitly requested Git-backed pickup
includes synchronization under the agreed Git authority. Inspect local changes,
staged work and remote identity first; preserve them. Fast-forward only when safe.
Don't auto-stash, force-reset, resolve a meaningful conflict by guessing, or quietly
claim local memory is current with GitHub when sync failed. An offline/local-only
pickup can proceed only as such, with that limitation visible.

Read the project's existing current-context/handoff pointer and selected active
work. Recover current stage, actual user agreement, last result, pending question
or next action, failure/resource state and relevant project constraints. Follow
necessary evidence links; avoid loading the full log archive and every retired
plan. An explicitly stale or contradictory pointer must be reconciled with current
artifacts and dated evidence before work continues. What makes a pointer stale is
an obsolete next action, not an old revision: `overtaken_revisions` in a pickup or
prepared packet is a diagnostic hint, and citing history or a pre-save position is
legitimate. Reach an exhaustive changed-file list with `git show --name-only` on
the named boundary rather than reading a manifest copied into memory.

Local files a project has deliberately kept out of Git do not block a pickup.
Name those exact paths with `--preserve` and the helper proceeds, reporting them
as local only; it stops, untouched, if the incoming revision carries one of them,
because that collision is a real decision. Unnamed changes still stop a pickup.

The start point names a **pickup reading set** — the exact files and complete
sections Out chose for this next action (see "Leave a lean start point" below).
When the handoff includes the helper's `read_args`, use those exact file/heading
selections, not a broader paraphrase. They are arguments to `prepare` (with the
current project and branch supplied), or the boundaries for reading normally.
Read those first, in full, and nothing else by default. It is a saved navigation aid, not a ban on further reading: check linked
detail when a contradiction or the next action requires it. Where the host can
assemble those named sources before starting the fresh worker, use `prepare`
below so the model receives their text once. Otherwise read them normally.
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

Ordinary In ends with restored memory, status and the saved plan on screen, and
a Conductor session open on that place, stopped at its dashboard decision as described
below. It does not execute the plan before that approval, draft replies, start
reviews, repair files or investigate backlog issues. Keep checks to safe requested
Git synchronization and resolving facts necessary to restore position; flag other
uncertainty for the work itself. Do not measure pickup cost inside every pickup;
assess the session logs afterward unless measurement was requested. A user
explicitly asking to continue after In can proceed through Conductor without
another approval. Managed To/Roll remains separate and keeps its agreed
continuation. When neither a saved next action nor a NOW item exists, say that
no task is selected rather than manufacturing one. Existing project restrictions
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
records for unresolved decisions, owed work and restrictions. Keep these in the
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

### Load Conductor before the dashboard

Before rendering the dashboard, load the sibling [Conductor](../../conductor/SKILL.md) in
this session using the host's skill mechanism, with an explicit instruction:
“Switch In: open a session on the restored position and authority already in
context; compose the arrival decision in the dashboard and wait.” Resolve the sibling from this Switch
distribution, not another cached version. If native skill invocation is
unavailable, read its SKILL.md directly; if neither route works, disclose that
Conductor was not loaded. Do not claim successful loading merely because its
name appears in the dashboard.

Carry the restored project, selected work (or none), agreement and restrictions,
pending decision and next action forward in context; don't create another record
or re-read the pickup set. Conductor's In paragraph is the full rule for choosing
the bounded next action and composing the one decision before rendering,
including pending-question, explicit-continuation and no-task cases. Do not
append a second report or approval after the dashboard. Managed
To/Roll is the exception and keeps its agreed continuation.

If collaboration is already established, restore it too. Resolve the local
pairing directory with `git rev-parse --git-path kerd-agent/partners` in the
current project; if it exists, read its binding metadata, not request archives
or transcripts. Use only bindings for this project; malformed or conflicting
metadata is unresolved, not a reason to guess a peer. The directory is local to
this Git worktree, not shared with linked worktrees or transferred by Git.
With an existing binding, retain the sibling [Agent](../../agent/SKILL.md) as
the route for later contributions; load its full instructions when a contribution
is requested, not merely to display a pairing. Retain the exact
provider, alias, session ID and recorded ongoing role privately in context.
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
selects only an unambiguous partner, never by title or recency. Show a compact TEAM line in
the status grid: `Claude (role) + Codex (role)`. Use brief faithful role labels,
not new assignments; a missing role stays unassigned. IDs and routine notice status
remain in Agent details, not the dashboard or project records. Surface a routing
problem in ATTENTION only when it affects the next action. A failed notice does not make restored memory incomplete.

### Welcome back: the screen summary

After restoration, orient before detail. Four short blocks, worded for the project:

- **Now:** work within the selected continuation and its necessary completion
  steps, not a copy of the project's wider `## Now`. Conductor restores that
  selection before composing; the rest stays behind the documents link.
- **Last session:** the main achievement or change.
- **This session:** the next agreed work and why. If none is agreed, say so; a
  suggestion stays a suggestion. Describe this action's scope, not the next
  roadmap item: “No build, deploy or push” states a limit without promising
  that a separate build follows. Name other work only if it affects this action.
- **Where we are:** position in the wider work, in the project's own stage names,
  not the stage of the pickup itself.

Close with the document links; the task list carries the label **Open work**
and points at the existing work/status page — HTML where one exists, otherwise
the Markdown record or task list. Resolve a real
target; don't invent a page or build one during In. The backlog and audit evidence
live behind that link. This replaces an exhaustive switch-in report and adds no
record field. Being short does not suspend the rules above: a contradiction,
failed synchronization or restriction still appears on screen.

An **Insight** is optional: one source-grounded learning, implication or tradeoff
in its own callout — never compulsory, never a hidden question.
A log preserves a reported claim; it does not prove someone observed the event.
Missing logs do not make verification impossible, and reconstructing a log does
not resolve conflicting claims. Keep the uncertainty visible or omit the Insight.

```text
★ Insight ─────────────────────────────────────────
The draft is ready, but its benefit is not measured.
A first-reader check can test whether the instructions
actually help someone get started.
───────────────────────────────────────────────────
```

A fictional example. Rewrap to width, use ASCII rules where the star renders
poorly, and omit the callout when there is nothing useful to say.

Render it with the packaged renderer, [scripts/where_we_are.py](../scripts/where_we_are.py),
resolved relative to this skill so it travels with the package:

Finish composing and checking the summary **before** this call. For each NOW
item, keep it only if it is the current action or necessary follow-through on
that action's result. A separately scoped later build does not qualify merely
because it is tagged “needs approval”; the current proposed action may still
await its own approval. Move checking procedures to the linked
task detail; keep only the action/outcome and immediate permission limits here.
Put dependencies in the action text, not in the owner label.

```sh
printf '%s' "$summary" | python3 "$SKILL_DIR/scripts/where_we_are.py" --summary - --markdown
```

The complete stdout from this call **is the final assistant message**. Return
it unchanged: no paraphrasing, expanded checklist, reworded warning, added intro
or second question. Rendering is the last step of In, not material for another
writing pass. If content needs correcting, change the summary and render again;
use that latest complete output. If the tool output is truncated, retrieve the
complete result rather than reconstructing missing text. A genuinely unavailable
renderer uses the disclosed plain-text fallback below, not a claimed renderer result.
The client may style numbered lists as letters; do not rewrite content to undo
client styling. This instruction governs the assistant's text, not client pixels.

Use `--markdown` in assistant chat. Start with the explicit completion heading
and a Markdown grid: PROJECT / PHASE / STATE / TEAM. Then three separated bullets:
LAST SESSION, THIS SESSION and NOW, with owner-labelled numbered actions nested
under NOW. Keep each session summary to one high-level sentence. Follow with
essential ATTENTION, document links, optional Insight, source footer and
**END OF PICKUP · SESSION READY**. No arrival boxes or fenced tables; let the
client render the grid. Grid appearance and wrapping depend on that client.

NOW answers who can move the work forward in this sitting, and what they should
do next. Number the immediate actions in priority order; include necessary
follow-through after their results, with that dependency explicit. Do not fill
the list with later projects, future-event checks or evidence bookkeeping.
“At the next live event” stays behind Open work until that event is available;
an unrelated build awaiting separate approval does not become NOW just because
it follows in the roadmap. Keep a consequential blocker or restriction visible
in ATTENTION, or an actionable step to resolve it in NOW.
Not shown is not dropped: omitting other open items from this screen changes
neither the saved priority nor their status. Keep them behind Open work, not
in ATTENTION merely because they remain owed. ATTENTION covers material limits
on the selected action or safe restoration: for example failed synchronization,
a consequential contradiction or a falsely recorded decision. A later question
can stay off-screen while a false claim that it was answered remains visible.
Also retain risks the restored record itself flags as urgent or imminent, even
outside this action, unless already resolved by available evidence. Keep each
brief and distinguish the dated saved observation from a fresh check; this is
not permission to relabel every owed item urgent or re-audit them at pickup.

Each item identifies the owner, action and target/outcome. Before rendering,
remove the **how** (clicks, restart sequences, navigation) and the **pass criteria**
(expected colours, values or states), even when they fit in one short sentence.
Point to their existing task/spec or saved account; do not claim a link contains
steps that were never recorded there. Keep details needed to identify the right
target, distinguish the scope, or avoid an immediate safety/permission mistake
in the item or THIS SESSION. Combine related recording
into one follow-through action; do not silently change saved priority or retire
work merely to shorten the display. There is no fixed item count to fill.
Do not relocate the removed procedure or checklist into another dashboard
section or the final question. An Insight may explain what the check can or
cannot establish; it is not another home for the test instructions.

Use `**Owner:** action` inside the existing string, for example:

1. `**Anthony:** Check the installed stats panel on either TV against the linked device-pass task.`
2. `**Claude:** After your report, record the result and identify any correction needed.`

For example, “Quit and reopen the app, open the match, check the bar is green
and the count is zero” is procedure plus pass criteria, not a tighter version
of item 1. Keep it behind the task link. THIS SESSION can say “Proposed: your
device check, then recording the result; no build, deploy or push.” This selects
the current work without retiring or rescheduling anything in the saved plan.

Only use established owners; otherwise say owner unassigned. This explicit
notation distinguishes owners from ordinary colon prose. The renderer preserves
bold labels in chat and strips emphasis in terminal output; it neither assigns
owners nor chooses priorities. Completed observations belong in LAST SESSION or
status, not NOW. A displayed recommendation is not permission to execute it.

The single immediate question comes first after END, as a bold speech-bubble
blockquote: `> 💬 **Can you run these checks on Master now?**`.
Recommend one action; no “or later?”, alternative task, reply menu or duplicate
question. A factual clarification asks for the fact, not approval; a yes to
doing a check is not its result. With no answer needed, stop at END. The renderer
places the question; do not append it yourself.

The end line ends restoration, not the session, and starts no work. Partial or
unknown restoration gets an incomplete or unconfirmed ending instead. Keep
header values and summaries brief; the renderer wraps rather than truncates.
Terminal mode uses colour when supported and puts the question after END too;
`--question-below` remains a compatibility flag. `--color` forces ANSI,
`--no-color` or `NO_COLOR` disables it. Markdown never emits ANSI. Plain terminal
output is the fallback when Markdown is unavailable. These are presentation
choices, not new state, memory reads or permission to continue work.

`$summary` is the shape below, filled from what pickup already read. **Copy it
from here; do not open the script to work out the keys.** The example is one
coherent sitting — a task is selected, so the session names it; a decision is
genuinely open, so `question` is filled. Use `null` or `[]` for anything the work
has nothing for.

```json
{
  "project": "Kerd",
  "phase": "Design needed — freshness alert",
  "task": null,
  "task_reason": null,
  "state": "Awaiting your approval",
  "state_reason": null,
  "team": [
    {"provider": "claude", "id": "11111111-1111-4111-8111-111111111111", "role": "current session", "self": true, "status": "identity verified"},
    {"provider": "codex", "id": "22222222-2222-4222-8222-222222222222", "role": "Implementation partner", "status": "submitted-unconfirmed"}
  ],
  "now": [
    "**Claude:** Design the freshness alert after approval; no implementation or deployment.",
    "**Anthony:** Review the design when it is ready."
  ],
  "last_session": "Diagnosed the pipeline outage. No alert has been built.",
  "this_session": "Proposed: design the alert. Implementation and deployment are not included in this approval.",
  "question": {
    "text": "Starting on the alert design — approve?",
    "proposed": null
  },
  "documents": [
    ["Open work", "docs/work/model-ready-work/consolidation.md"],
    ["Design", "docs/work/model-ready-work/design.md"]
  ],
  "warnings": ["Publisher health is a saved observation, not rechecked during pickup."],
  "insight": "A freshness check makes an otherwise silent stop visible.",
  "source": "CONTEXT.md, TODO.md, the newest session log",
  "updated": "2026-09-10 17:34 EDT",
  "base": ".",
  "restored": "yes",
  "restore_note": null
}
```

New chat summaries put the task in NOW, leaving `task` null to avoid repeating
it in the orientation grid. Older inputs retain a task unless a NOW action
matches it exactly (apart from its explicit owner label). The retained task
appears as Focus under NOW; any `task_reason` appears there as task context.
Neither fallback invents an owner or additional numbered action.
Terminal output retains its existing labelled rows as the plain-text fallback.

`project` is the project already restored, never inferred from the renderer's
installation path. `documents` are `[label, path]` pairs resolved against `base`; a path that does
not exist is reported as a warning rather than offered as a link. `task_reason`
and `state_reason` carry the sentence after an explicit "none". `restored` is
`"yes"`, `"partial"`, `"no"`, or omitted when no pickup claim is being made;
`restore_note` says what is missing when it is not `"yes"`.

`question.text` supplies the one question. New callers leave `proposed` null:
put scope in NOW or THIS SESSION. For older callers, a nonempty `proposed` still
renders below NOW as scope/recommendation, preserving paragraphs and complete
limits rather than silently losing them when YOU disappears. Legacy `reply`
is tolerated but not displayed; it must not carry necessary facts.

`team` uses the Agent arrival result's array; the fictional IDs above illustrate
its input shape only. A caller may shorten a role's wording faithfully for
display, without modifying its private binding or assigning new responsibility.
The renderer groups identical identities and displays providers and roles only.
IDs, receipt status, errors and other helper metadata remain available in Agent.
Use `[]` for no established pairing and `null` for unread/unresolved state.
A consequential routing problem belongs in `warnings`; routine unconfirmed
notice delivery is not a blocker or an availability claim. No pairing means no
notice or setup question.

`updated` is the selected source's recorded update time, not the current time,
an estimated close time or a guessed aggregate across files. If no applicable
source time is known, use `null`. The renderer supplies `rendered` from its clock;
do not hand-type that footer. Reversed displayed times in the renderer's
`YYYY-MM-DD HH:MM ZONE` format with identical zone labels produce an attention
warning, leaving both values intact. Other formats and differing or absent zones
are not compared; no timezone conversion or clock-cause diagnosis is implied.

**What the caller should supply, and what the renderer checks — they are not the
same thing.** Given a correctly shaped JSON object, fields are not required: a
missing, misspelled or null one degrades quietly, so a typo costs you a blank
line rather than an error. That tolerance is about *fields*, not about input —
malformed JSON exits 2 with a message, and a top-level value that is not an
object (an array, say) exits 1 on an unhandled error. `PROJECT`, `PHASE`, `STATE`, `NOW`, `LAST SESSION` and `THIS SESSION` **always render**, falling back to "not recorded" or a plain sentence
when they have nothing — they are the frame, and a gap in them is information.
Compose `now` using the immediate-action guidance above, from the saved plan.
This changes the display, not the saved list. The backlog is not supplied here.
TEAM always renders (unknown versus no established pairing stay distinct).
Only the attention panel, `DOCUMENTS` and the `★` insight line are **omitted
entirely** when empty. Always supply `source`: it names what the pickup actually
read, and it is the one field nothing else can stand in for.

It reads stdin, so nothing is written to disk. Do not re-read files to fill it,
and do not stop for approval before showing it. Only if rendering fails or the
renderer is unavailable, disclose that failure and present the restored facts
and single question as plain text. A successful complete render uses the unchanged
stdout rule above; this fallback is not permission to restyle or paraphrase it.

`restored` states whether the necessary context was recovered. Which presentation
ran is a separate fact: an older Switch producing the long report is not an
incomplete restore, and belongs in the attention lines if it matters at all.
Use `yes` when the necessary position, authority and next action were recovered,
even with a dirty tree, unpushed commits, pending approval or a missing log whose
necessary content was recovered elsewhere. Those facts may still need attention.
Use `partial` or `no` only for a material context gap, and name it in `restore_note`.
Missing session paperwork alone is not a failed restoration. Never turn a
reconstructed claim into verified evidence merely to make the banner complete.

## Out

Read the active state and inspect what actually changed. Preserve the current
agreement, decisions, exact next action, unresolved jobs and important findings.
After the contribution checkpoint below, append an evidence-backed session
account to the existing history; read the clock
for dates/times written now. Unknown start time stays unknown. Do not retain the
whole native conversation or private session IDs as project history.

When collaboration matters to the next pickup, retain a short provider,
contribution and evidenced result, plus the relevant next-action/work-record
link in that existing account. Do not copy private pairing IDs or aliases into
Git history. This is project memory, not a session registry or proof that a
particular partner has read it; Agent resolves live identities separately.

### One coordinated closeout

The owner is the session the person asked to run Out. If another Out owner is
already known, return this session's account to that owner instead of rewriting
shared pointers. If both sessions were asked to own the closeout, the person
names one before either writes. Before editing the handoff, check the owner's
existing pairing-role continuity using Agent's
[Out ownership check](../../agent/references/session-succession.md#out-designate-this-roles-continuation).
Reuse an explicit replacement choice already given; Out alone grants no role.
No binding means no setup stop. Unresolved routing does not prevent a safe memory
save, but its continuation limit must remain visible.

**Contribution checkpoint — before drafting or editing closeout records.**
Identify the known sessions that contributed to this sitting, including the
owner. Compare their necessary decisions, authority, results, limits and unfinished
work with the accounts already available. Returned subagent results and adequate
work records count; do not request ceremonial acknowledgements or fresh accounts
for material already captured. If a necessary delta remains with a participant,
request it directly through Agent and retrieve the response before drafting the
combined closeout. Submission or timeout is not receipt. The owner drives this
collection; the person must not have to ask each agent or relay their accounts.
A known pending job is covered when its owner, current state and result-retrieval
location are captured. Its unfinished result is not itself missing memory; carry
the wait/retrieval step forward instead of waiting merely to finish Out or
claiming the job done.

Show the checkpoint in one short line, for example: “Contributions captured:
Claude (review) + Codex (implementation); missing: none.” Name actual contributors
and roles, not private IDs; this is an accountable coverage statement, not a
machine proof. An unavailable participant is not itself missing necessary memory:
if other evidence restores the scope, authority, known outcomes, limits and next
action, record any residual gap and why it does not prevent safe continuation.
Never turn an unresolved observation into a verified result. If necessary memory
is unavailable, explicitly report incomplete coverage, the missing contribution
and the recovery step before writing a partial account.
Preserve known memory, but set `handoff_ready: false` and do not offer to clear
or designate a ready successor. Do not wait indefinitely or invent completeness.
Only after coverage is complete—or its specific gap is explicitly reported as
incomplete—draft the closeout. A material contribution arriving during drafting
reopens the checkpoint; incorporate its delta before finalizing, not in a late
repair after claiming completion. Reuse one account, not duplicate session logs.
If a necessary delta arrives after saving, reopen the account and correct the
completion claim. Save the amendment within existing authority, then re-designate
after any pointer change; if saving is not authorized, report the pending amendment
instead of claiming the old handoff includes it.

During Out, the owner alone writes the shared pointer, active list,
session account and any work record it is reconciling. Contributors write only
an already-owned record no other session is editing; otherwise they return their
account to the owner. Re-read affected records from disk after a contributor
finishes editing, before reconciling them. Contributors retain decisions, scope/authority,
findings, verification limits and unfinished work in their existing work record
as contributions finish. A read-only contributor returns that account for the
owner to record, rather than gaining write permission.

Use the sibling [Agent](../../agent/SKILL.md) for missing accounts and own their
retrieval. No all-session sweep, whole-transcript read or new inbox. The reply
does not grant approval, prove a claimed observation or settle a contradiction.
Discovery lists sessions, not what they hold; unknown standalone contributions
are not covered by a known-partner check. If there is concrete uncertainty about
who holds necessary work, ask the person to identify the contributor. Do not
make every ordinary Out repeat a session census or assume an unseen session
has nothing relevant.

The owner reconciles the contributions into the existing account, work record
and lean start point; other sessions do not run competing shared-file closeouts.
Link the detailed contribution instead of copying it into every file. Work on
another branch or worktree is named by branch, record and saved location in the
start point, with local-only/uncommitted limits carried; retain the necessary
account in the handoff if its record is not reachable there. Out does not merge,
push an additional branch or sweep another session's edits into this save.
Check that a fresh reader can recover the agreement, restrictions, evidence
limits, unresolved work and next action without either old conversation open.
Before finalizing, verify the checkpoint's captured contributions are actually
represented in that reading set, rather than only in the owner's native context.
A pending job keeps its actual owner/status; do not stop it or call it finished
to close the record. If a peer is unavailable, preserve known work and name the
specific missing context and recovery step. Do not claim the handoff ready or
advise clearing context while necessary detail is still unsaved.

Reconcile active work against evidence. Remove completed tasks from active lists
while retaining their completion record. Retire redundant work only with a known
reason. Keep independent sub-findings and migration-sensitive work open. Archive
historical detail with reachable links; age alone doesn't retire a decision,
dependency or risk. For an initial legacy reorganization, keep a recoverable
original. Do not rewrite dated history or maintain duplicate living plans.

### Save the selected continuation

Update the next session's lean start point with what is true and what to do next.
After reconciling contributions and active work, leave one concise continuation
in the existing pointer's current section, or a directly linked current work
record included in the pickup reading set. Save the choice the sitting reached,
not only its collection of open tasks:

- the selected next action and owner, with agreed/proposed/awaiting-approval status;
- the completion steps within that scope and where it stops, including exclusions;
- its pending question, if any, distinguished from other open questions.

Use existing prose or headings; these are meanings to preserve, not three new
required fields. If the selection already exists clearly, reconcile it in place
rather than copy it to several living records. Keep the session log as the dated
account and the broader TODO list as open work; link instead of duplicating them.
Do not turn a proposed next step into agreement. Where the person has not selected
work, retain a grounded recommendation as proposed or a genuine unresolved choice;
Out does not need a ceremonial approval just to save that uncertainty.

For example: “Pending approval: Claude builds main, installs it on Master,
verifies and records the installation; stop before playback. Question: may I
build and install on Master?” is one scope. A later playback check can remain
in the wider plan without becoming part of that approval. If no action is
selected and none can be grounded, say so. Never change a user's priority to
make the handoff neater.

Before saving, check that the pointer/current record and the log's next-action
account agree on that scope and stopping point; a fresh reader should not have
to assemble them from competing lists. Include this selection in the measured
reading set and carry it into the closing box's existing `next` text. In restores
the meaning even when an older handoff has no named fields; it does not declare
the selection missing merely because it was written as a sentence. New user
direction can supersede it. Changed evidence can make it stale; Conductor
explains that and proposes a replacement, never calls that replacement agreed.

Historical decisions needed by a future feature remain discoverable by subject;
the active memory must include constraints that affect the next work. Be explicit
about unreconciled historical sections rather than calling the migration lossless.

Alongside the next action, name the small reading set that supports it: actual
files or complete sections, why they matter, and where deeper history lives.
Use the existing handoff/work record; do not add a parallel manifest or duplicate
source text. This lets the next pickup reuse the outgoing session's knowledge
of the work instead of rediscovering the entire repository. Preserve unresolved
decisions and authority even when the next action looks simple.

### Leave a lean start point

The next pickup pays for every byte the start point carries, so Out ends by
making it small on purpose, not by reading less next time. Four moves, in this
order, each leaving a reachable link behind:

1. **Rulings stay, cases move.** The loaded pointer keeps each standing decision
   as its ruling — the bold sentence and its date — only for decisions that
   govern the next work or a constraint the next sitting must honour. The full
   entry (the case, the evidence, the argument) lives in a living decisions
   record (`docs/decisions.md` by convention), newest first with an index of
   rulings so history is discoverable by subject. Superseded decisions are
   marked there, never deleted. A ruling without its case is a link, not a loss.
2. **Closed work leaves the active list with its reason.** The closure review
   already gives every open row a verdict; rows judged done or dead move to a
   backlog archive (`docs/backlog-archive.md` by convention) with the verdict,
   the evidence and the date. Open and unsure rows stay. Age alone closes
   nothing.
3. **Name the reading set in the start point** as exact files and complete
   sections, in the pointer's current-state section, with why each matters.
   The default set is the pointer, the active list's `## Now`, and the newest
   session log; add a work record section only when the next action needs it.
4. **Measure it and record the reading.** Run the helper's `measure` on that
   set and write the result beside the reading set:

   ```sh
   python3 /path/to/switch/scripts/handoff.py --project /path/to/project measure \
     --record CONTEXT.md --section TODO.md '## Now' --file kivna/sessions/<date>.md
   ```

   It counts bytes exactly and estimates tokens at four bytes each, labelled as
   an estimate; the target is the trial's 8,000 unless the work agreement sets
   another (`--target`). Over target is information: prune further under the
   rules above, or record why the set must stay larger. It never blocks a save.

   Save the returned `read_args` array beside that measurement in the existing
   start point. It is the exact selection to reuse at In, not another manifest.
   For the example above it is:
   `["--record", "CONTEXT.md", "--file", "kivna/sessions/<date>.md", "--section", "TODO.md", "## Now"]`.
   Measure and prepare resolve these arguments through the same selector. Never
   measure an excerpt then hand off its containing file or section. Each source
   reports its byte count and `reaches_eof`. Complete files always reach EOF;
   for a section, true means no later same-level or higher-level heading ends
   the selection: a lone `## Now` includes the entire remainder, not just the
   first task. If that is too broad, give the intended
   block a real heading boundary (preserving the history), select it and measure
   again; do not substitute a smaller estimate or silently truncate the read.
   Re-measure changed selections or source content; a previous reading is not a
   size guarantee for edited files. Keep findings archives available on demand.

The first run on a legacy pointer is a migration: keep a recoverable original
(the move itself, in Git, plus a dated note in the session log), reconcile any
conflicting current claims, and say what was not reconciled. Do not apply the
migration to an unrelated live project.

The living handoff describes the sitting that is ending, not the moment it was
written. A record states the revision observed while writing, so a boundary
commit made afterwards leaves it naming an ancestor with a next action already
done. Keep those apart: label the observed revision as the position before the
save, and let the next action be what remains after it. Never write the
resulting commit ID into a file inside that commit; name the boundary by branch
and record, and let `git log`/`git show` supply the ID. When the save completes
work the record still lists as pending, correct that record in the same
boundary. Say plainly which the handoff reached — prepared locally, committed,
or verified at the remote; a local memory save is neither of the last two.

Record the scope rule and where the boundary is, not an exhaustive file list.
`git show --name-only <commit>` reproduces that inventory on demand, so a copied
path list costs every later pickup and proves nothing Git does not already hold.
Existing manifests stay as reachable history, not required pickup reading.

Inspect pending jobs before ending a sitting. A running job is not saved merely
because its task name appears in a file. Respect existing direction on whether
it continues; a genuine unresolved ownership issue needs a decision.

Under the agreed Git authority, commit the relevant work/session files by name
and push to the intended branch. A save commits only the named files. Exact paths
the project has already decided to keep locally — a scratch patch, a stray build
artifact — are acknowledged with `--preserve`: they stay untouched and are reported
as local only, not saved. Keep that acknowledgement in the project's existing
memory as exact paths; it is not a pattern, an ignore entry or a new config file,
and it never deletes or stashes. New or unacknowledged work still needs resolution,
not blanket staging. Show locally saved vs committed vs remotely verified. A failed
push leaves useful local work recoverable; do not call that a cross-device handoff.

### Close with the saved-place box

End Out on one box that says how far the save reached, rendered with the same
packaged renderer:

```sh
printf '%s' "$closing" | python3 "$SKILL_DIR/scripts/where_we_are.py" --closing - --markdown
```

Use the same chat-versus-terminal presentation choice as In above. In chat,
show the Markdown directly: the emphasized save verdict is the completion
signal, not a claim that a green theme colour proves a successful push. Out's
presentation is unchanged by the compact In layout.

`$closing` is filled from the helper's save result and what Out just wrote.
**Copy the shape from here; do not open the script for the keys.** `saved` is
one of `remote-verified` (the helper's `saved_to_remote`), `committed` (a local
commit, push not verified) or `not-saved`; the banner and its words follow it.
An absent or unrecognised `saved` renders SAVE STATUS NOT RECORDED, never
"nothing committed": unknown is not evidence. The free-context hint follows
only a remote-verified or committed save **and** `handoff_ready: true` after
the coordinated-closeout check. This boolean is the owner's memory-coverage
assessment, not something a Git push or renderer can prove. False or omitted
keeps the session open; omitted means readiness unassessed, not context missing.
False also names the missing detail/recovery action in
`next`. The MEMORY row distinguishes readiness from the SAVED Git verdict.
`local_only` is the helper's
`preserved_local_only`. `tree` is what remains in
the working tree after the save, in words. `next` is the exact next action the
start point names, `reading_set` the files and sections it names, `measured`
the helper's `measure` reading. Use `null` or `[]` for anything Out has nothing
for; a missing field renders as "not recorded", never as a claim.

After the final save, if this session has an established role and the handoff is
ready, prepare the role verified by the pre-save check under the
[succession guide](../../agent/references/session-succession.md) before showing
the closing box. Do not create a role or transfer another session's role here.
Failure affects automatic pairing recovery, not the Git save verdict; name it
in the closing next action. Use the existing `next` text for successful designation
or not applicable too, keeping the saved next action intact; no new JSON field.
Do not include private IDs or claim memory completeness from routing. No session is
ended by preparing its handoff.

```json
{
  "project": "Kerd",
  "branch": "main",
  "saved": "remote-verified",
  "handoff_ready": true,
  "commit": "2e59ab7",
  "files": 15,
  "remote": "origin/main",
  "local_only": ["kerd-laptop-result.patch"],
  "tree": "clean",
  "closed": "2026-09-12 12:40 EDT",
  "next": "Run one real Conductor session on 0.112.0 and confirm a Claude player is a native subagent.",
  "reading_set": ["CONTEXT.md", "TODO.md ## Now", "kivna/sessions/2026-09-12.md"],
  "measured": "23,482 bytes, about 5,871 tokens estimated at four bytes each, within the 8,000 target",
  "log": "kivna/sessions/2026-09-12.md"
}
```

The box distinguishes saved locally, committed and remote-verified in words,
names local-only leftovers and an unclean tree rather than hiding them, and
ends by saying the session is still open with the free-context hint. It never
says the session exited or the context was cleared: a save is a Git fact, and
starting fresh context is a separate action in the person's client. If the renderer cannot
run, say the same things as plain text.

## Default verified save when pushing is authorized

For an authorized commit-and-push Out, use `handoff.py save ... --push` by default.
Its successful remote check is the evidence for saying the save reached GitHub;
an attempted push or stale local tracking ref is not. Local-only Out remains a
valid choice and does not require GitHub access or new push permission.

If the helper cannot support the agreed workflow, explain the limitation. A
manual route must retain explicit file selection, existing-index protection and
verification that the intended remote branch contains the exact saved tip before
claiming remote success. Report use of that fallback. Do not sweep unrelated
changes into a commit or replace an unsafe checkout to make the helper pass.

Resolve `scripts/handoff.py` from the skill directory. Example shapes, not literal
commands to run against a guessed project/branch:

```sh
python3 /path/to/switch/scripts/handoff.py --project /path/to/project save \
  --branch trial-branch --file CONTEXT.md --file TODO.md \
  --file path/to/session-log.md --message "Save the working place" --push
python3 /path/to/switch/scripts/handoff.py --project /path/to/project pickup \
  --branch trial-branch --record CONTEXT.md --sync
python3 /path/to/switch/scripts/handoff.py --project /path/to/project prepare \
  --branch trial-branch --record CONTEXT.md --section TODO.md '## Now'
```

List actual changed files, including any archive files; the helper refuses unassigned
changes or an existing staged index. It won't check out a different branch for you.
The loaded record is only the entrypoint: follow its relevant context links and
verify the next action. It is not a parser-based declaration of complete memory.

`prepare` is an optional caller convenience: it returns local Git identity and
raw, source-labelled records together for a fresh reader. Repeat `--file` for
complete files or `--section FILE '## Exact heading'` for complete Markdown ATX
sections, including child sections. Prepared sources must be Git-tracked UTF-8
text; their line endings are preserved. Missing, empty or ambiguous selections fail;
it does not guess replacements. Conductor chooses from the project's actual
memory structure. The helper does not select relevant sources, write a second
memory file, start a session or grant permission. Without `--sync` it is local-only.
