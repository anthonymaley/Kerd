# Run Conductor in managed contexts

Use for an authorized sustained **local** build that must carry its Conductor
decisions, implementation and review/correction loop through fresh context
without routine user input. Start it at delivery entry, not when the existing
chat has already exhausted its memory. The chat remains the control surface;
the managed decision sessions own the continuing work. Small work still belongs
inline when a managed loop would add needless cost. Do not silently substitute
this route for a named provider, existing partner, or an incompatible authority.

## Prepare once

Use the actual approved work record as the immutable agreement. It must name
the outcome, required proof, scope/owned files, decisions, current authority and
stopping condition. Capture all necessary contributor accounts before launch;
reconcile pending jobs before handing over exclusive editing. Write the small
Roll saved-place JSON beside the work (the schema in the Switch Roll guide),
with concrete next action, compact memory, cumulative evidence and failures.
These two files must be distinct and inside the project. The driver alone writes
the place while running; do not edit either from the control chat.

Prepare any needed execution score outside the driver before launch. Include its
applicable content or a resolvable reference in the immutable agreement's existing
narrative; this adds no required agreement or Roll field. Each managed decision
selects work within those finished steps and retains the current passage identity,
evidence and cumulative unsuccessful-attempt count in existing place memory and
failures. It may clarify transport, but cannot edit or re-specify the score
(whoever wrote it), launch a Composer or turn the score itself into new authority.

Read model-jobs.md and the applicable model profiles. Choose explicit available
coordinator, implementation and review models/efforts for this task; reuse a
sound existing choice. Save a safe launch brief and selection rationale beside
the work, including relevant profile/version or the disclosed fallback. Full
generated prompts and replies are saved privately before each dispatch, not
copied blindly into public records. The decision contract is intentionally
narrow; it does not load the entire interactive Conductor skill per decision.

Show the delegation grid: Conductor decisions (Codex, read-only), implementation
(Codex, local writable), and independent review (fresh Codex or Claude, read-only),
with actual requested models/efforts and a Fit line for each. The managed route's
forced review after every implementation takes precedence over an established
partner's recorded review cadence; the cadence neither relaxes nor replaces it. This serial route owns one child at a time,
not parallel editors. It chooses a scoped implementation contribution and judges
results; it does not hand the entire interactive interview to a worker.

Launch the sibling `switch/scripts/conductor_roll.py`, resolving the installed
package path. Below are shell placeholders for choices already made, not values
for the user to memorize or an invitation to use a default model:

```sh
python3 "$switch_scripts/conductor_roll.py" --project "$project" \
  --agreement "$agreement" --place "$place" \
  --coordinator-model "$coordinator_model" --coordinator-effort "$coordinator_effort" \
  --worker-model "$worker_model" --worker-effort "$worker_effort" \
  --review-provider "$review_provider" --review-model "$review_model" --review-effort "$review_effort"
```

Use the host's managed background command for a long run; retain its output and
exit status. Do not use a short foreground timeout and assume surviving work is
owned. `--timeout` is an optional per-child limit; `--max-cycles` is an optional
number of decision cycles, ending at a safe pause rather than completion. Neither
is a context-pressure detector. Do not add limits the person did not request
except a disclosed bounded trial. Capture emitted dispatch/return/rolling events
in the live work view; they carry requested model, effort and prompt size. An
event is actual driver activity, not a claim of semantic success.

## What continues automatically

The Python driver holds the existing `.git/roll/owner.lock`. Its read-only
Conductor session selects implementation, review, a memory checkpoint, completion
or a real blocker. Every decision is a fresh managed context. The Codex adapter
also observes context usage and steers to a checkpoint at its existing reserve
threshold. A checkpoint does not return to ordinary Switch In or ask approval.

Before releasing a Codex source, the adapter saves and reads back its full reply
in the native request record. After verified shutdown, the driver validates and
promotes that reply to the working saved place. Only then can a successor start.
Request IDs are persisted before dispatch. Contributions remain in their exact
result files; dispositions cite those IDs. Open review findings are carried into
every new decision and correction job until review of the changed tree clears
them, or Conductor explicitly rejects each named finding with reason/evidence.
A contradictory passing review on the unchanged tree does not clear them.
Malformed results remain linked as unvalidated contributions for inspection.
Failure counts
cannot decrease. Review and read-only decision jobs are checked against a tree
fingerprint; completion requires passing review of the current tree, not an old
one. This is a mechanical precondition, not proof of the model's judgment.

Three review failures or three consecutive checkpoint-only decisions stop for
reassessment. Missing usage, malformed output, changed protected files, ambiguous
ownership or surviving children stop automatic continuation. A real permission
or product question stops with that question; an answer must become an explicitly
approved new agreement/run, not a message injected as authority into this loop.
Three unsuccessful Player attempts against the same score step and measure also
stop for reassessment/hand-back, with no reset for a renamed task, changed route
or repaired passage. This ceiling does not prove a score defect. A known defect,
contradiction, missing consequential decision or impossible premise in a score
passage stops immediately instead of consuming more Player attempts.

## Observe, stop, close

A premature complete from an otherwise valid, clean read-only decision is not
uncertain ownership. The driver retains the refused decision, does not promote
its place, and sends explicit review-gate feedback to a fresh coordinator.
Three refused completion decisions without changed implementation content or an
explicit evidenced finding rejection stop for reassessment. Re-review of the
unchanged tree does not reset that counter. They never bypass the completion gate.

Finding-rejection evidence paths are checked for existence, not relevance.
A changed tree plus passing review is not mechanical proof that a specific
finding was corrected: reviewer and Conductor still own that judgment against
the exact findings supplied. These checks prevent silent omissions, not bad
reasoning or unsupported evidence claims.

`switch/scripts/roll_status.py --project "$project"` reads the recorded phase;
it is not a live probe. A control chat, including a replacement chat, can request
a stop with `conductor_roll.py --project "$project" --stop`. This records a
stop-only request tied to the current run. Decision/implementation jobs checkpoint;
a review finishes its bounded turn. Wait for **paused** and confirmed process
exit before editing or starting anything else. A written stop request is not
delivery or shutdown proof. Resuming a user-stopped run requires their direction;
the same launch command can resume a safe pause under the unchanged agreement.

If a stop arrives after a decision but before dispatch, no job starts. On resume
the fresh coordinator re-derives that next job from the saved place and receipts.

Unknown/running/uncertain records must be inspected, never deleted to force a
retry. Completed or blocked runs also require explicit inspection and retirement
of their retained record before a new agreement/run. There is no automatic
crash-recovery or record-retirement command in this first version; for a
finished worker Roll record, see the retirement paragraph in
`skills/switch/references/to-roll.md`. Retain receipts,
verify no owned job remains, and reconcile the saved place; never replay an
uncertain request under a fresh ID. Legacy worker Roll refuses this controller's
record, and this controller refuses a legacy worker record.

For a defective score passage, the managed decision uses the existing `blocked`
action and records the exact passage, discrepancy evidence and needed repair in
the existing place fields. It neither composes a correction nor edits the live
agreement. The control owner inspects that result and verifies the managed owner
has stopped before any change. The passage's author, a Composer or the
controlling Conductor for a step it wrote, may then repair only the affected
passage under the existing agreement and run-replacement authority, preserving
prior requirements and explaining consequential changes. Any new outcome,
quality, scope or authority choice returns to the Producer. Follow the existing
inspection and replacement boundary: never edit a live agreement, auto-retire
the run or invent a driver action for composition.

On return, the control chat reports the actual outcome, review evidence and any
limits; it does not repeat the build. At ordinary Out, the run is a contributor:
capture its outcome/unfinished work once, reference evidence, and leave the
selected continuation. Do not close as complete while the driver still owns jobs.

## Capability and evidence limits

- First pressure-aware coordinator and implementation adapter: **Codex only**.
  Either Claude or Codex may be the control chat. Claude can review, but this is
  not pressure-aware Claude coordination or automatic replacement of its TUI.
  Worker Roll (`roll.py --target claude --context-aware`) does have an observed
  Claude route; it is not yet wired into this managed decision loop.
- Reviews use a bounded fresh CLI turn, not pressure-aware Roll. Claude's review
  route has file-inspection tools, no Bash. Both review routes are instructed
  not to run write-producing tests. Required test evidence must be supplied by
  implementation; missing evidence remains a blocker, never invented execution.
- The native sandbox and prompt limits forbid expanded authority. The driver
  detects content/history changes; it is not a security monitor for every possible
  ignored file, external effect or project-specific tool. No commits, publication,
  installation, network, background children or nested model dispatch are granted.
- The Python host process and its execution handle are not rolled. A control-chat
  replacement can observe and request a stop, but host-process survival depends
  on that host's actual background mechanism. Do not claim survival without a
  test. Real provider/model usage and natural context pressure need separate
  evidence from lifecycle fixtures; no latency/token savings are established.
