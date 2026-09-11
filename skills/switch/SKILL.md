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

- **In:** restore useful memory, current status and the saved plan; show the
  welcome-back dashboard, open a Conductor session on that place and stop at one
  approval line. Read [pickup and closeout](references/in-out.md).
- **Out:** close this sitting well: record history, tidy active work and prepare
  the next session. Read [pickup and closeout](references/in-out.md).
- **To:** save the exact mid-work position through GitHub, relinquish source
  control and restore at the destination. Not full Out. Read
  [device handoff](references/to.md). Load managed detail only for an owned build.
- **Roll:** preserve an active Conductor build across a fresh context window,
  without a new interview or routine go-ahead. Read
  [managed handoff and Roll](references/to-roll.md).

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

For In, use the guide's [welcome-back summary](references/in-out.md#welcome-back-the-screen-summary):
Last session, This session, Where we are, You, and a real link to task detail.
An evidence-grounded Insight is optional, never an entry requirement.

Ordinary In restores an active build's place without executing it. Then open the
sibling [Conductor](../conductor/SKILL.md) on that place using the guide's
[open-and-stop handover](references/in-out.md#open-conductor-and-stop-at-the-approval):
Conductor shows its journey strip, brief and task list, then one line —
“Starting on X — approve?” — and waits. One proposal, never two options, never
an “or”. The approval, or an explicit request to continue, is what starts work;
managed To/Roll keeps its agreed continuation. Loading is not build authorization.

Keep pickup selective and explicit: fully read the chosen current working set,
then relevant historical entries as needed. Don't silently truncate records or
claim that small output means low input. Measure instructions, memory and tool
output when testing context cost; disclose unavailable readings.

## Implementation boundary

[Git helper](scripts/handoff.py) supplies explicit-file save, safe fast-forward
pickup and optional assembly of caller-selected current records. It does not
choose what is done, select relevant memory, grant authority or control sessions.
[Roll helper](scripts/roll.py) manages fresh CLI runs through the existing model
connection. It does not take over arbitrary already-open interactive sessions.
Read the relevant guide before running either. Unknown outcomes stop automatic
relaunch; tests do not make this an enforcing security boundary.
The [managed To helper](scripts/managed_to.py) can keep an owned Codex source open
while its controller repairs a failed save; its lifecycle and limits are in the
To/Roll guide. It does not take over an already-open user session.

For a concise read-only view of a managed run, use
`python3 /path/to/switch/scripts/roll_status.py --project /path/to/project`.
It shows recorded state, next action and completed-worker history without private
session IDs. This is recorded progress, not a live health probe or quality verdict.
