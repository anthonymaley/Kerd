---
name: switch
description: "Save, restore or move repo work between sittings and devices, or Roll an authorized Conductor build into fresh context. In restores memory and pairing, weighs every open item, shows a plain-English arrival headed by the Kerd version it loaded: a project/phase/next/team grid, where things stand, open work, one recommendation with why, ending on “Start a Conductor session?” with a picker of up to four (the recommendation, up to two other open items, Something else), without loading Conductor; choosing work opens Conductor at Shape, never approving its operations. Out checks role ownership, contributor coverage and urgent risks, adds what settled to the sketchbook, saves the next action and approval boundary, and ends on a plain-English box: what changed, next step and why, and up to two other items Switch In will offer, marked proposed. Managed Roll continues without arrival approval; a tmux Conductor chat rolls itself into a fresh session (`/kerd:switch roll`) at its saved next step."
---

# Switch

**Asking the person:** every question is one speech-bubble line, the last prose line of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it; a genuine question is open (“What should it show?”), never “X, or Y?”; when options are in hand (open work, known routes, candidates), list them above the question with one recommendation, even for an open question, and ask bare only when none are in hand; where the host offers one, a native picker may follow the bubble carrying those same options and always leaving a free-form answer open, never replacing or preceding it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Putting a decision to the person:** a consequential question — its answer commits to work, spends real effort, releases or deletes something, or reverses a ruling — comes after a decision block: Problem, Facts (with how we know the problem is real and how strong that evidence is), Known options (or “needs study”), Recommendation, Why, Cost, What we lose, Input (who else checked it, or nobody yet). Its bubble is the Recommendation sentence ending “— approve?”, every operation included, or one genuine question the recommendation depends on; never a smaller or softer question than the real decision, and never without the block. A factual question or a small, easily undone step stays one line — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Showing the person:** when they ask to see something, and whenever a proposal carries two or more connected parts, a branch, an ownership boundary or a before → after change, the answer carries a saved, rendered view drawn with diagram-design or Archify — never hand-rolled ASCII in a code fence, never an offer question, no quota; only a single action or a factual answer stays text, and being easy to describe in words does not make it one — see [showing the work](../conductor/references/journey.md#visuals-belong-throughout).

Keep the work continuous while leaving room in the next context window. Work in
the person's project, not this skill's directory. Do not invoke the old gate/mode
machinery to run this skill. No CI, custom hooks or plugin installation is required. Existing host permissions
and repository boundaries still apply.

## Must hold

A run of each action does not skip these steps or break these prohibitions. Each
item names the guide section with its detail: open that section before the step.

### In

- A named handoff or trial resolves its own record, repo and branch first; missing
  or mismatched stops, never a fresh start ([In](references/in.md#in)).
- Before any fast-forward or work proposal, check `git rev-parse --git-path roll/run.json`;
  a recorded managed run is inspected read-only with `roll_status.py`: never adopted,
  its checkout unchanged, no competing work proposed, unknown state never read as no
  run; an unclaimed `roll/chat.json` is shown in ATTENTION, never acted on by
  ordinary In ([In](references/in.md#in)).
- An explicitly requested Git-backed pickup syncs under the agreed Git authority:
  local changes preserved, fast-forward only when safe, no auto-stash, force-reset or
  guessed conflict resolution; a failed sync is shown, never claimed current; paths
  the project deliberately keeps out of Git are named with `--preserve`
  ([In](references/in.md#in)).
- The read set: the saved `read_args` selections, read first and in full, through
  `prepare` (with `--notes-commit` when the start point records one), or by hand where
  `prepare` cannot run or the caller already supplied the records; plus the complete
  active list with child sections, explicitly current linked work records, governing
  decisions, constraints and risks; every `notes:` entry is read from the notes root,
  and unsaved vault notes or a vault missing the recorded commit are refused
  ([In](references/in.md#in)).
- Team: with a binding for this project, compare this session's ID, follow the
  [succession guide](../agent/references/session-succession.md) when an ID matches or
  continuity evidence exists, then, after identity and any required adoption, send its arrival notice to established partners
  (or, when none is named, the helper's unambiguous default); TEAM shows provider and
  role only; no binding, no setup question ([Restore the existing team](references/in.md#restore-the-existing-team)).
- Weigh every open item, the saved one included, and recommend exactly one with its
  Why, or say nothing is actionable rather than invent work, without loading
  Conductor ([Compose the arrival](references/in.md#compose-the-arrival-in-switch)).
- Renderer: copy the `$summary` shape from the guide, never from the script, and run
  `where_we_are.py --summary - --markdown`; only if it fails or is unavailable, say so
  and give the restored facts and the question as plain text ([Welcome back](references/in.md#welcome-back-the-screen-summary)).
- The screen is pasted as reply text, unchanged, before any picker in the same message;
  output left in a tool result has not been shown.
- One question: `> 💬 **Start a Conductor session?**`, placed by the renderer, is the
  last line of the message. Only the host's native picker may follow it (up to four
  options); without one, nothing follows: never a written list of options. In does
  not execute the restored plan or other project work (no drafted replies, reviews, repairs or
  backlog investigation); requested safe Git sync and private Agent succession and
  arrival upkeep are permitted. An answer that chooses work opens Conductor at Shape
  without approving its operations; only approval and exclusions the person states
  are carried ([Enter Conductor from the answer](references/in.md#enter-conductor-from-the-answer)).

### Out

- The session asked to run Out owns it: if another owner is already known, return
  this account to it; if both were asked, the person names one. Check the owner's
  pairing-role continuity with Agent's Out ownership check before editing the
  handoff; no binding, no setup stop ([One coordinated closeout](references/out.md#one-coordinated-closeout)).
- Contribution checkpoint before drafting closeout records, shown in one line
  (“Contributions captured: …; missing: …”). A residual gap is recorded with why it
  is safe when other evidence restores scope, authority, known outcomes, limits and
  next action; only unavailable necessary memory is reported as incomplete coverage,
  with its recovery step, and sets `handoff_ready: false` ([One coordinated closeout](references/out.md#one-coordinated-closeout)).
- Add what the sitting settled and the record is missing to each moved piece of
  work's sketchbook (a small fix needs none), nothing invented, asking the person
  nothing ([Add to Conductor's sketchbook](references/out.md#add-to-conductors-sketchbook));
  with `work_notes`, keep `notes:outside-the-repo.md` ([the list](references/out.md#keep-the-outside-the-repo-list)).
- Save the selected continuation: next action and owner with its status, where it
  stops, its pending question, its why, up to two other items as proposed, or, when
  none can be grounded, say so; and every unresolved risk the active records flag
  urgent or imminent, inside the reading set ([Save the selected continuation](references/out.md#save-the-selected-continuation)).
- A lean, measured start point: rulings stay and cases move, closed rows leave with
  their reason, the reading set is named, `handoff.py measure` runs with `--carry-file`
  (never a phrase as a bare argument), and its reading and `read_args` are saved beside
  the set ([Leave a lean start point](references/out.md#leave-a-lean-start-point)).
- Save named files only, under the agreed Git authority; on a concert branch, stop if
  the checked-out branch is not its sketchbook's; acknowledged local paths are passed
  with `--preserve`; with `work_notes`, the vault repo is saved the same way;
  `save … --push` when pushing is authorized ([Default verified save](references/out.md#default-verified-save-when-pushing-is-authorized)).
- With `work_notes`, save the vault first and write its commit into the start point
  before the project's last commit. After the last commit and before the box, run the
  `boundary` check on every repo committed to, repeating `--preserve <path>`; only
  `passed` earns the ✓ (a local-only Out says so instead), and nothing is written
  after it
  ([Leave a lean start point](references/out.md#leave-a-lean-start-point)).
- End on the saved-place box from `where_we_are.py --closing - --markdown`, its shape
  copied from the guide; nothing follows its closing line; if the renderer cannot
  run, say the same as plain text
  ([Close with the saved-place box](references/out.md#close-with-the-saved-place-box)).
- The restart line appears only after a remote-verified or committed save,
  `handoff_ready: true` and `boundary: "passed"`; never claim the session exited or
  the context was cleared.

### To

- Start from the person's intent: the same SSH/tmux session needs no handoff; a live
  controller's work takes its managed To path; an ordinary session saves its precise
  place under existing Git authority ([device handoff](references/to-roll.md#to-one-device-releases-the-other-continues)).
- No Out backlog cleanup or replanning at a mid-work boundary; save the agreed outcome
  and success measures, active step, useful decisions and findings, current artifacts,
  pending question with shown answer, exact next action, failure counts, optional
  resource limits and unresolved jobs ([To and Roll](references/to-roll.md)).
- Verify the saved remote revision before relinquishing the source; a failed save keeps
  control and names recovery.
- The destination gets one self-contained pickup instruction (repo, branch, exact saved
  revision, record path, source-release evidence, authority; no private IDs or
  credentials) and, with the helper, runs `prepare … --commit FULL_SAVED_COMMIT --sync`;
  without it, the instruction carries the same checks explicitly.
- Never kill a pane, send exit keystrokes to a guessed target or call a new worker's
  exit the source's exit (the one exception is the Conductor chat roll restarting its
  own recorded pane); without release evidence the destination only inspects
  read-only, and an unproved exit is reported as “saved, source exit unproved”.

### Roll

- Only for a build its controller already owns under agreed authority: no new
  interview or routine go-ahead, and a new window grants no new authority
  ([Roll](references/to-roll.md#roll-fresh-window-same-authorized-build)).
- Rolling In starts only after the checkpoint is saved and read back and the source's
  release is verified; review and genuine blockers return to Conductor.
- The chat roll is a Claude Conductor chat only, at a batch boundary or after a
  delivery job returns, owning nothing outstanding (unknown counts as outstanding),
  past 50% of the host-declared window (none declared, no roll); nothing is typed into
  Claude and no shell variables go in the command ([the chat roll](references/to-roll.md#roll-the-conductor-chat-tmux)).
- `/kerd:switch roll in` claims the marker or refuses; a refusal stops and says why and
  never becomes ordinary In; every abandoned roll revokes the prepared role with
  Agent's `handoff --cancel` before the old session does any more work.
- A finished worker Roll record (`review` or `blocked`, no pending job, owner lock
  free) is inspected, reconciled and retired with `roll_retire.py` before a different
  agreement runs, never deleted or moved by hand; a `running`, `uncertain` or `failed`
  record goes through recovery, and a blocked or uncertain outcome needs diagnosis
  before any retry ([Run the existing managed loop](references/to-roll.md#run-the-existing-managed-loop)).

## Pick the intended action

- **In:** restore useful memory, the wider active-work picture and the saved
  plan; weigh every open item, the saved one included, and compose one
  plain-English arrival without loading Conductor: a project/phase/next/team
  grid, where things stand in product terms, the open work one line each, one
  recommendation and why, ending on the one question
  **“Start a Conductor session?”**. A saved next
  step is a candidate, never repeated just because it was saved. Return the renderer's complete
  Markdown as the final message unchanged, then wait; do not rewrite its prose. Read
  [pickup](references/in.md).
- **Out:** close this sitting well: record history, tidy active work, leave a
  lean, measured start point with the selected continuation, its approval
  boundary, recorded urgent risks and, with vault notes, the private list of
  live links outside the repo — rulings kept, cases and closed rows moved to
  reachable records, the reading set named — and end on the saved-place box:
  a project/saved/phase/released grid, what changed this session in product terms,
  what Switch In will offer (the next step and why, plus up to two other open
  items each with its reason, marked proposed, never agreed), save problems
  under attention, and one restart line
  only after a confirmed save. Read
  [closeout](references/out.md).
- **To:** save the exact mid-work position through GitHub, relinquish source
  control and restore at the destination. Not full Out. Read
  [device handoff](references/to-roll.md#to-one-device-releases-the-other-continues). Load managed detail only for an owned build.
- **Roll:** preserve an active Conductor build across a fresh context window,
  without a new interview or routine go-ahead. Read
  [managed handoff and Roll](references/to-roll.md). For the continuing decision
  and review loop as well as workers, use sibling Conductor's
  [managed controller](../conductor/references/managed-conductor.md).
  Conductor rolls its own chat with `/kerd:switch roll`: save, restart its tmux
  pane into a fresh `claude`, and `/kerd:switch roll in` picks up the saved next
  step; outside tmux it saves and shows one line to run. `roll --cancel` withdraws
  an unclaimed roll. Read [the chat roll](references/to-roll.md#roll-the-conductor-chat-tmux).

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

For In, use the guide's [welcome-back summary](references/in.md#welcome-back-the-screen-summary):
explicit completion heading naming the Kerd version it loaded, the PROJECT · PHASE · NEXT · TEAM grid, Where
things stand, Last session, Open work, Recommended with its Why, attention and a
real link to the open-work page, all in plain product English. No footer or end
marker. The single question ends the screen as a bold speech-bubble blockquote.
The screen is reply text: paste the rendered output into the message itself, before the picker in the same message; output left in a tool result has not been shown, since the host folds it away.
Where the host has a native picker it follows with up to four options: “Yes — <the
recommended work>”, up to two other open items each with a one-line why, and
“Something else”, free text always open; a plain yes still means the
recommendation, and the recommendation stays one item.
Retain the terminal output when appropriate.
An evidence-grounded Insight is optional, never an entry requirement.

Ordinary In restores the current work picture without executing it. Switch owns
the [arrival decision](references/in.md#compose-the-arrival-in-switch): use
the restored context, not a Conductor invocation or another intake. An answer to
**“Start a Conductor session?”** that chooses work, a plain yes or another
offered item included, opens
Conductor at Shape for that work, and “Something else” opens it for
direction-setting; choosing work never
approves its operations. An explicitly selected and authorized task, direct
workflow request or action approval invokes Conductor through the host skill
mechanism as the guide's
[work handover](references/in.md#enter-conductor-from-the-answer)
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
permission to omit other active work. Assemble the reading set with the helper's
`prepare` on those saved `read_args`, passing the saved notes commit as
`--notes-commit` when the start point records one (`--sync` when this vault may
be behind it). Where `prepare` cannot run, or the caller already supplied the
records, read the same set by hand, every `notes:` entry from the notes root
included; an entry is never skipped because it lives outside the repo. Retrieve
a bounded complete relevant entry when a gap affects orientation or a
recommendation; do not sweep the archive.
Don't silently truncate records or claim that small output means low input.
Measure instructions, memory and tool output when testing context cost; disclose
unavailable readings.

## Implementation boundary

[Git helper](scripts/handoff.py) supplies explicit-file save, safe fast-forward
pickup, optional assembly of caller-selected current records, and a `measure`
of the reading set's size against the pickup target (bytes exact, tokens
estimated; never blocking; warns rather than refuses a file Git does not
track — `prepare` refuses an untracked source and a `notes:` source must be
tracked in the vault, while pickup can still read a project record the project
deliberately keeps out of Git, named with `--preserve`), and the `boundary`
check Out must pass before its ✓
(fetch now, HEAD on a remote branch, clean tree; stashes counted, not refused).
When a project keeps its working notes in the vault (`kivna/vault.json`'s
`work_notes`), Out saves and pushes that vault repo the same way and the
boundary check covers both repos.
It does not choose what is done, select relevant memory, grant authority or control sessions.
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
