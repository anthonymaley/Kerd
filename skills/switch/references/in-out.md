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

Resolve the current project and branch. Before any fast-forward or work proposal,
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
With no record, add no discovery or setup step. Do not infer completion merely
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
"Leave a lean start point" below).
When the handoff includes the helper's `read_args`, use those exact file/heading
selections, not a broader paraphrase. They are arguments to `prepare` (with the
current project and branch supplied), or the boundaries for reading normally.
Read those first, in full. They are a saved navigation aid, not a ban on further
reading: also cover the pointer-designated active list and child sections, its
explicitly current linked work records, governing current decisions, standing
constraints and known risks; check linked detail when a
contradiction, orientation gap or recommendation requires it. Where the host can
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
list (with child sections) and any [saved selection](#save-the-selected-continuation)
as candidates. For each, ask: does it move the product or the person's work
forward, and why would it come before the others? Current user direction takes
precedence; recorded priority, dependency and authority inform the order. A saved
selection is one candidate with its recorded reasons, not the answer. Work that
only proves the project's own mechanics (a self-check, a record tidy, evidence
bookkeeping) does not lead unless it blocks the product work or the person asked
for it. If evidence shows the saved selection stale or completed, say so plainly.

**Open work** lists the items that move the work, one plain line each, in
recommended order, with no file names, line numbers or internal labels unless the
person needs them to recognize the item. Keep a human-owned check or a pending
decision in the list as what it is; do not dress it as agent work. Items
omitted from the screen stay open behind the documents link; omission changes
neither their status nor the saved priority.

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

- **Chooses work** (“yes”, the recommendation's picker option, “the migration
  sign-off”, or new work in their own words): invoke `/kerd:conductor` through the host's skill
  mechanism at Understand/Shape for that work. Naming or accepting the work
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
a one-row grid, then the text:

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
it unchanged: no paraphrasing, added intro or second question. Rendering is the
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
follow the rendered output with exactly two options: **“Yes — <the recommended
work>”**, naming the work it opens, and **“Something else”**, which opens
Conductor to ask what; the host's free-form route stays open. Where the picker
carries a description, Yes's says it opens Conductor at Shape for that work and
approves none of its operations, so an action-worded recommendation (“Release
0.137.0”) is never read as approval. The picker never
replaces or precedes the bubble. Without picker support, the bubble is answered
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
reading set and carry it into the closing box's `next`, with its reason in
`why`. Save why it matters to the product, not only what it is: the next In weighs it against
the other open work and shows only a reason a person can check. Work that only
proves the project's own mechanics is saved as open work, not as the selection,
unless it blocks product work or the person chose it. In restores
the meaning even when an older handoff has no named fields; it does not declare
the selection missing merely because it was written as a sentence. New user
direction can supersede it. Changed evidence can make it stale; Switch
explains that and proposes a replacement, never calls that replacement agreed.

Alongside that selection, keep each known, unresolved risk the active records
flag as urgent or imminent **inside the pickup reading set**, even when it does
not affect the selected action. A concise line in the pointer's current section
can carry the risk, its recorded observation date and source, clearly labelled
saved or freshly checked; otherwise include the relevant source section in
`read_args`. Unknown dates stay unknown. A link to an unread section is not
coverage. Reconcile an existing risk line rather than adding a second stale copy.
If the risk is only a bullet inside a large Backlog, prefer the concise carried
line rather than loading that whole section; the existing heading-boundary rule
also allows a narrow source selection. When the source section is selected,
the pointer can identify the risk and source without repeating its figures.
This carries recorded urgency, not a fresh operational verdict or authority to
investigate; routine owed work does not become urgent to justify inclusion.

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
   The default set is the pointer, its designated complete active list (including
   child sections), explicitly current linked work records, and the newest session
   log; add source sections for governing current decisions, standing constraints
   or known risks when they are not already covered. Before measuring or claiming
   memory ready, compare those active records used for this closeout with the
   actual selected text, including unresolved urgent/imminent flags in their
   Backlog sections. Carry any missing risk, constraint or decision into that
   text or select its source section. Do not search the whole archive or recheck
   live systems to perform this coverage check. An unresolved gap stays disclosed,
   not a complete handoff claim. Size targets never justify dropping material
   active-work context or an urgent risk; re-measure after changing the set.
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

End Out on one box, rendered with the same packaged renderer:

```sh
printf '%s' "$closing" | python3 "$SKILL_DIR/scripts/where_we_are.py" --closing - --markdown
```

Use the same chat-versus-terminal presentation choice as In above. The box
mirrors the arrival, in plain product English: a one-row grid (PROJECT, SAVED,
PHASE, NEXT), **This session** with what changed for the person one line each,
**Next time** with the next step and its **Why**, then one closing line. Save
mechanics (commit, file count, remote, reading set, measurement, log path) stay
in the records the next Switch In reads, not on the screen. A save problem
appears under **ATTENTION**, only when it is true.

`$closing` is filled from the helper's save result and what Out just wrote.
**Copy the shape from here; do not open the script for the keys.** `saved` is
one of `remote-verified` (the helper's `saved_to_remote`), `committed` (a local
commit, push not verified) or `not-saved`; the banner, the SAVED cell and any
attention line follow it. An absent or unrecognised `saved` renders SAVE STATUS
NOT RECORDED, never "nothing committed": unknown is not evidence.
`handoff_ready` is the owner's memory-coverage assessment after the coordinated
closeout check, not something a Git push or renderer can prove: `false` or
omitted adds an attention line, and `false` also names the missing detail or
recovery action in `next`. `phase` is where the wider work stands, in the
project's own terms. `this_session` is what changed, in product language, not
the files touched. `next` is the exact next action the start point names; `why`
is the reason it comes first. `tree` is what remains in the working tree, in
words: exactly `clean` when nothing is left; anything else is shown under attention. Files the project
keeps out of Git by decision are expected and not shown. `warnings` carries any
other problem, such as a failed role designation. `host` is `claude` or `codex`:
it chooses the closing line; only `claude` (or an unrecorded host) gets `/clear`. Use `null` or `[]` for anything Out has nothing
for; a missing field renders as "not recorded", never as a claim.

The closing line offers a restart only after a remote-verified or committed save
**and** `handoff_ready: true`: under Claude, "Exit and restart or /clear and
/kerd:switch in to pick up from here."; under Codex, "Exit and restart, then
switch in to pick up from here." Otherwise it asks to keep the session open and
resolve the save or the missing handoff first, because clearing context then
would lose the very work that is unsaved. It never says the session exited or
the context was cleared: a save is a Git fact, and restarting is the person's
action.

After the final save, if this session has an established role and the handoff is
ready, prepare the role verified by the pre-save check under the
[succession guide](../../agent/references/session-succession.md) before showing
the closing box. Do not create a role or transfer another session's role here.
Failure affects automatic pairing recovery, not the Git save verdict; name it
in `warnings`. Do not include private IDs or claim memory completeness from
routing. No session is ended by preparing its handoff.

```json
{
  "project": "Kerd",
  "branch": "main",
  "saved": "remote-verified",
  "handoff_ready": true,
  "phase": "Launch: 2 of 5 done",
  "this_session": [
    "The risk-rating change was accepted: launch step 1 done.",
    "Conductor now checks where your work stands in your own project: launch step 2 done."
  ],
  "next": "Start the diagnostic pilot.",
  "why": "It is the first real work item driven in someone else's project, and the only way to see Kerd work for a real user.",
  "tree": "clean",
  "warnings": [],
  "host": "claude"
}
```

If the renderer cannot run, say the same things as plain text.

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
