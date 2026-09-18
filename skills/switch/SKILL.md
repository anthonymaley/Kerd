---
name: switch
description: Save, restore or move repo-based work between sittings and devices, or Roll an authorized Conductor build into fresh context. Ordinary In restores memory and pairing, weighs every open item (the saved next step is one candidate) and shows a plain-English arrival: a project/phase/next/team grid, where things stand in product terms, open work one line each, one recommendation with why, then ends on “Start a Conductor session?” with a Yes / Something else picker, without loading Conductor; choosing work opens Conductor at Shape for it, never approval of its operations. Returns the rendered arrival unchanged. Out checks role ownership, contributor coverage and urgent risks in the pickup set, saves the next action and approval boundary, and ends on a plain-English box: what changed, the next step and why. Managed Roll continues without normal arrival approval.
---

# Switch

**Asking the person:** every question is one speech-bubble line, the last prose line of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it; where the host offers one, a native picker may follow the bubble carrying those same options and always leaving a free-form answer open, never replacing or preceding it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Keeping the decision with the question:** immediately before a consequential bubble, put a self-contained capsule — the recommended concrete action, what it decides or changes, material cost or risk, and the stopping or authority boundary — so the bubble can be answered from that block alone, without reading upward. Restate the recommendation there even when it already appears earlier; the repetition costs less than the reader's search. Never point upward with “the steps above” or “as described”. Nothing unrelated comes between the capsule and the bubble; name the concrete action and target in the bubble; tiny or factual questions stay proportionate — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Showing the person:** when they ask to see something, and whenever a proposal carries two or more connected parts, a branch, an ownership boundary or a before → after change, the answer carries a saved, rendered view drawn with diagram-design or Archify — never hand-rolled ASCII in a code fence, never an offer question, no quota; only a single action or a factual answer stays text, and being easy to describe in words does not make it one — see [showing the work](../conductor/references/journey.md#visuals-belong-throughout).

Keep the work continuous while leaving room in the next context window. Work in
the person's project, not this skill's directory. Do not invoke the old gate/mode
machinery to run this skill. No CI, custom hooks or plugin installation is required. Existing host permissions
and repository boundaries still apply.

## Pick the intended action

- **In:** restore useful memory, the wider active-work picture and the saved
  plan; weigh every open item, the saved one included, and compose one
  plain-English arrival without loading Conductor: a project/phase/next/team
  grid, where things stand in product terms, the open work one line each, one
  recommendation and why, ending on the one question
  **“Start a Conductor session?”**. A saved next
  step is a candidate, never repeated just because it was saved. Return the renderer's complete
  Markdown as the final message unchanged, then wait; do not rewrite its prose. Read
  [pickup and closeout](references/in-out.md).
- **Out:** close this sitting well: record history, tidy active work, leave a
  lean, measured start point with the selected continuation, its approval
  boundary and recorded urgent risks — rulings kept, cases and closed rows moved to
  reachable records, the reading set named — and end on the saved-place box:
  a project/saved/phase/next grid, what changed this session in product terms,
  the next step and why, save problems under attention, and one restart line
  only after a confirmed save. Read
  [pickup and closeout](references/in-out.md).
- **To:** save the exact mid-work position through GitHub, relinquish source
  control and restore at the destination. Not full Out. Read
  [device handoff](references/to.md). Load managed detail only for an owned build.
- **Roll:** preserve an active Conductor build across a fresh context window,
  without a new interview or routine go-ahead. Read
  [managed handoff and Roll](references/to-roll.md). For the continuing decision
  and review loop as well as workers, use sibling Conductor's
  [managed controller](../conductor/references/managed-conductor.md).

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
explicit completion heading, the PROJECT · PHASE · NEXT · TEAM grid, Where
things stand, Last session, Open work, Recommended with its Why, attention and a
real link to the open-work page, all in plain product English. No footer or end
marker. The single question ends the screen as a bold speech-bubble blockquote.
Where the host has a native picker it follows with exactly “Yes — <the
recommended work>” and “Something else”.
Retain the terminal output when appropriate.
An evidence-grounded Insight is optional, never an entry requirement.

Ordinary In restores the current work picture without executing it. Switch owns
the [arrival decision](references/in-out.md#compose-the-arrival-in-switch): use
the restored context, not a Conductor invocation or another intake. An answer to
**“Start a Conductor session?”** that chooses work, a plain yes included, opens
Conductor at Shape for that work, and “Something else” opens it for
direction-setting; choosing work never
approves its operations. An explicitly selected and authorized task, direct
workflow request or action approval invokes Conductor through the host skill
mechanism as the guide's
[work handover](references/in-out.md#enter-conductor-from-the-answer)
describes. Carry the actual approval and exclusions; opening the workflow alone
does not approve operations. This is not a second approval; managed To/Roll
keeps its agreed continuation.
Retain existing local Agent pairing context as that guide describes; load Agent
when a contribution is requested. The short succession guide permits verifying
this session's ID and adopting its designated role in private metadata, plus a
deduplicated no-reply arrival notice to restored partners, not starting project
work at In. Eligible restart recovery
may check native identity/absence through that helper, preserving the role rather
than asking the person to select an established teammate again.

Keep pickup selective and explicit: fully read the chosen current working set
and the complete active task list, including child sections, then relevant
current decisions, constraints and risks. Saved `read_args` are navigation, not
permission to omit other active work. Retrieve a bounded complete relevant entry
when a gap affects orientation or a recommendation; do not sweep the archive.
Don't silently truncate records or claim that small output means low input.
Measure instructions, memory and tool output when testing context cost; disclose
unavailable readings.

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
