---
name: switch
description: Save, restore or move repo-based work between sittings and devices, or Roll an authorized Conductor build into fresh context. In loads Conductor, restores existing Agent pairing and designated role continuity, notifies established partners without requesting work or a reply, and returns the rendered status grid unchanged with provider/role TEAM, LAST/THIS/NOW sections and one question callout after END. Out checks existing role ownership and collects necessary contributor accounts before drafting one resumable handoff, with memory readiness distinct from Git save status. Distinguishes closeout from exact mid-work continuation.
---

# Switch

Keep the work continuous while leaving room in the next context window. Work in
the person's project, not this skill's directory. Do not invoke the old gate/mode
machinery to run this skill. No CI, custom hooks or plugin installation is required. Existing host permissions
and repository boundaries still apply.

## Pick the intended action

- **In:** restore useful memory, current status and the saved plan; load Conductor
  to compose one welcome-back dashboard with owner-labelled NOW actions and
  one question callout after the end marker. Return the renderer's complete
  Markdown as the final message unchanged, then wait; do not rewrite its prose. Read
  [pickup and closeout](references/in-out.md).
- **Out:** close this sitting well: record history, tidy active work, leave a
  lean, measured start point — rulings kept, cases and closed rows moved to
  reachable records, the reading set named — and end on the saved-place box
  that says how far the save reached. Read
  [pickup and closeout](references/in-out.md).
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
Now, Last session, This session, Where we are, and a real link to task detail.
Use its compact chat layout: explicit completion heading and a status grid with
provider/role TEAM, then LAST / THIS / NOW bullets with numbered owner-labelled
actions nested under NOW, links and an end-of-pickup marker.
The single question follows as a bold speech-bubble blockquote; no YOU box.
Retain the terminal output when appropriate.
An evidence-grounded Insight is optional, never an entry requirement.

Ordinary In restores an active build's place without executing it. Before
rendering the dashboard, load the sibling [Conductor](../conductor/SKILL.md) on
that place as the guide's [handover](references/in-out.md#load-conductor-before-the-dashboard)
describes. Conductor composes the dashboard's one decision and waits; its
SKILL.md In paragraph is the full rule. The approval, or an explicit request to continue, is what starts work;
managed To/Roll keeps its agreed continuation. Loading is not build authorization.
Retain existing local Agent pairing context as that guide describes; load Agent
when a contribution is requested. The short succession guide permits verifying
this session's ID and adopting its designated role in private metadata, plus a
deduplicated no-reply arrival notice to restored partners, not starting project
work at In. Eligible restart recovery
may check native identity/absence through that helper, preserving the role rather
than asking the person to select an established teammate again.

Keep pickup selective and explicit: fully read the chosen current working set,
then relevant historical entries as needed. Don't silently truncate records or
claim that small output means low input. Measure instructions, memory and tool
output when testing context cost; disclose unavailable readings.

## Implementation boundary

[Git helper](scripts/handoff.py) supplies explicit-file save, safe fast-forward
pickup, optional assembly of caller-selected current records, and a `measure`
of the reading set's size against the pickup target (bytes exact, tokens
estimated; never blocking). It does not
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
