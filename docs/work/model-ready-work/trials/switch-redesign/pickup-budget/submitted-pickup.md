# Local-only Switch-in measurement

Restore Seinn's saved position in this isolated clone using the candidate Switch
instructions below. This is a NEW local-only memory measurement on the Studio,
not execution of the historical Studio-to-laptop handoff. The laptop check already
completed. Any old device-handoff instructions are historical evidence, not a
request to repeat that trial or to move this session.

The controller pinned this checkout to the tested revision
2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83. Verify necessary local Git identity and
clean state, then start at CONTEXT.md. Follow relevant sources to establish the
actual position and next work. Choose efficient reads; fully read selected files
or explicitly selected complete sections. Do not call truncated output complete.

Read-only, local files/Git only. No fetch, remote check, readiness check, build,
tests, device/playback/SSH probe, messages, source edits, new tasks, delegation,
native session histories, installed skills or extra app tools. Do not turn a
recorded obligation into permission to execute it. There is no user question
pending for this memory test and no time/spend cap was set. Stop after restoration.

Return one concise JSON object with: position (including active-work status),
last_completed, next_obligation, next_decision, authority, unresolved_memory,
and reads. Cite the source file and section for factual answers. Distinguish old
observations from fresh verification. List complete files/sections actually read
and any incomplete retrieval. Do not claim a token-budget result; the controller
measures native usage independently.
---
name: switch
description: Save, restore or move repo-based work between sittings and devices, or Roll an authorized Conductor build into fresh context. Handles useful memory and explicitly authorized Git handoffs; distinguishes closeout from exact mid-work continuation.
---

# Switch — development candidate

Keep the work continuous while leaving room in the next context window. Work in
the person's project, not this skill's directory. Identify the candidate briefly.
Do not invoke installed Switch or the old gate/mode machinery to run this version.
No CI, custom hooks or plugin installation is required. Existing host permissions
and repository boundaries still apply.

## Pick the intended action

- **In:** restore current repo state and useful memory; continue the exact
  authorized action. Read [pickup and closeout](references/in-out.md).
- **Out:** close this sitting well: record history, tidy active work and prepare
  the next session. Read [pickup and closeout](references/in-out.md).
- **To:** save the exact mid-work position through GitHub, relinquish source
  control and restore at the destination. Not full Out. Read
  [precise handoff and Roll](references/to-roll.md).
- **Roll:** preserve an active Conductor build across a fresh context window,
  without a new interview or routine go-ahead. Read
  [precise handoff and Roll](references/to-roll.md).

Honor the named action. Don't infer In/Out from a dirty tree, or perform a boundary
when the person asks only about its design/status. Ask only when the requested
action or target is genuinely ambiguous. A new window does not grant new authority.

For a named handoff or trial, resolve that record and any supplied repo/branch
before ordinary project pickup. A missing or mismatched handoff is not a fresh
start: report the mismatch and stop. Do not substitute a familiar Switch flow,
project readiness check or operational task. If the person supplies only a trial
name and no record can be located, request its location rather than infer its work.

## One useful memory of the work

Use existing project context, active-work records and history; don't introduce a
parallel TODO, plan or dashboard. Save the current position, actual agreement and
limits, relevant evidence, unresolved questions/jobs and exact next action. Keep
failure counts and resource accounting across windows. Link source detail instead
of copying the same narrative into several files. Missing information is a gap,
not permission to invent memory or assume acceptance.

Historical records stay reachable and unchanged. Completed work can leave the
active list without erasing decisions that still govern new work. When reorganizing
legacy memory, preserve a recoverable original and reconcile conflicting current
claims. Do not silently apply a candidate migration to an unrelated live project.

## Make the transition visible

Show actual state: saving → saved locally / pushed → restoring → continuing, or
the specific blocker. Link the saved place. Distinguish planned, running, returned
and verified work. Don't claim a file save exited a session, moved a process or
proved full restoration. No fake activity or progress percentages.

An active Conductor build resumes its next authorized action in the same turn
through [candidate Conductor](../conductor/SKILL.md). Restore a pending question
with its shown answer using Conductor's journey layout. Apply a new answer already
given rather than asking it again. A completed/inactive project does not become
a new build merely because In ran. Never stop only to ask “start Conductor?”

Keep pickup selective and explicit: fully read the chosen current working set,
then relevant historical entries as needed. Don't silently truncate records or
claim that small output means low input. Measure instructions, memory and tool
output when testing context cost; disclose unavailable readings.

## Implementation boundary

[Git helper](scripts/handoff.py) supplies explicit-file save and safe fast-forward
pickup. It does not choose what is done, grant Git authority or control sessions.
[Roll helper](scripts/roll.py) manages fresh CLI runs through the existing model
connection. It does not take over arbitrary already-open interactive sessions.
Read the relevant guide before running either. Unknown outcomes stop automatic
relaunch; tests do not make this an enforcing security boundary.

For a concise read-only view of a managed run, use
`python3 /path/to/switch/scripts/roll_status.py --project /path/to/project`.
It shows recorded state, next action and completed-worker history without private
session IDs. This is recorded progress, not a live health probe or quality verdict.
# In and Out: useful context, clean boundaries

## In

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
artifacts and dated evidence before work continues.

For an active authorized build, continue without a new permission ceremony. If
there is no active task, show that honestly and the next unresolved decision or
obligation; don't select a new product feature by assumption. A status-only request
stays read-only. Ordinary pickup is not permission for production probes, device
tests, messages or deployments. Project-specific restrictions still govern them.

Context-cost targets come from the work agreement, not a universal magic number.
Report added input separately from host overhead where measurable. The Switch trial
uses 8,000 additional input tokens and 5% of observable usable context, plus correct
restoration. A shorter but incomplete read fails; unknown usage is not a pass.

## Out

Read the active state and inspect what actually changed. Preserve the current
agreement, decisions, exact next action, unresolved jobs and important findings.
Append an evidence-backed session account to the existing history; read the clock
for dates/times written now. Unknown start time stays unknown. Do not retain the
whole native conversation or private session IDs as project history.

Reconcile active work against evidence. Remove completed tasks from active lists
while retaining their completion record. Retire redundant work only with a known
reason. Keep independent sub-findings and migration-sensitive work open. Archive
historical detail with reachable links; age alone doesn't retire a decision,
dependency or risk. For an initial legacy reorganization, keep a recoverable
original. Do not rewrite dated history or maintain duplicate living plans.

Update the next session's lean start point with what is true and what to do next.
Historical decisions needed by a future feature remain discoverable by subject;
the active memory must include constraints that affect the next work. Be explicit
about unreconciled historical sections rather than calling the migration lossless.

Inspect pending jobs before ending a sitting. A running job is not saved merely
because its task name appears in a file. Respect existing direction on whether
it continues; a genuine unresolved ownership issue needs a decision.

Under the agreed Git authority, commit the relevant work/session files by name
and push to the intended branch. Unexpected or already-staged work needs resolution,
not blanket staging. Show locally saved vs committed vs remotely verified. A failed
push leaves useful local work recoverable; do not call that a cross-device handoff.

## Optional Git primitive

Resolve `scripts/handoff.py` from the skill directory. Example shapes, not literal
commands to run against a guessed project/branch:

```sh
python3 /path/to/switch/scripts/handoff.py --project /path/to/project save \
  --branch trial-branch --file CONTEXT.md --file TODO.md \
  --file path/to/session-log.md --message "Save the working place" --push
python3 /path/to/switch/scripts/handoff.py --project /path/to/project pickup \
  --branch trial-branch --record CONTEXT.md --sync
```

List actual changed files, including any archive files; the helper refuses unassigned
changes or an existing staged index. It won't check out a different branch for you.
The loaded record is only the entrypoint: follow its relevant context links and
verify the next action. It is not a parser-based declaration of complete memory.
