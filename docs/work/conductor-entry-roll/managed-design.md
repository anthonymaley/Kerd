# Managed Conductor: implementation brief

## Authority and scope

Anthony approved managed Conductor sessions, with the current chat as control
surface, after the ordinary start/resume entry change. Implement locally; no
publication, installs, consumer changes or takeover of an existing TUI.

## Design for review

One local Python driver owns the existing `.git/roll/owner.lock` and run.json.
It launches a **read-only Conductor decision session**, not an implementation
worker renamed Conductor. That session reads the agreed work, compact saved
place, Conductor guidance and the latest worker/reviewer contribution. It
returns a saved place plus one next decision: scoped implementation job,
independent review job, checkpoint, complete, or a genuine user/blocker stop.
The driver persists the decision before dispatch. Jobs cannot dispatch jobs.
Only one child runs at a time. Each decision session is fresh; context pressure
also steers it to return a checkpoint rather than exhausting the window. The
driver saves/read-backs the checkpoint and verifies source shutdown before the
successor. No ordinary In dashboard, approval or repeated intake between them.

Use the existing Codex app-server stdio adapter for Conductor decisions, with a
caller-specific checkpoint instruction (legacy worker instruction unchanged).
Codex is the first supported managed **coordinator**; either host chat can own
the process handle. No implicit substitution if the user named Claude as the
coordinator: its pressure-aware adapter is not implemented. Implementation uses
the same pressure-aware Codex adapter and existing worker checkpoint contract;
review uses a distinct fresh read-only Codex or Claude job through ask.py.
Claude review's existing route has file-inspection tools, no Bash; disclose that
limit. Choose available models/efforts explicitly at launch, never silently
change them. Save every prompt before dispatch and report real transitions.

Agreement is immutable during the run. Saved place retains cumulative evidence,
failure counts and useful memory. Keep all contributor receipts durably in the
private run ledger; give the next Conductor the latest result and references to
older receipts, not a growing transcript. Conductor must disposition the latest
result in its checkpoint before the driver allows another job. Pending jobs
never roll across an unverified ownership boundary. Read-only Conductor and
review jobs must not alter project files. Scoped implementation has no commit,
push, install, network or detached-job authority. These are prompt boundaries
inside native sandbox permissions, not a claim of arbitrary path enforcement.

Completion requires a successful independent review after the most recent
implementation, a recorded Conductor disposition and no pending jobs; a review
receipt is evidence of review, not machine proof of semantic acceptance.
Repeated checkpoint-only no-progress turns and repeated failed corrections stop
for reassessment. User/product decisions stop with the exact question; automatic
roll does not approve new scope. A run limit is a safe pause, not completion.

Uncertain exit, malformed result, missing usage, surviving child, changed
agreement/place, reused identity or interrupted pending job latches uncertainty;
no automatic redispatch. Existing worker Roll and new managed Conductor refuse
each other's retained records. Crash recovery is an explicit inspected follow-up,
not a promise this first driver survives loss of its host process.

## Tests and evidence

Fake-transport integration: implementation -> review finding -> correction ->
review -> Conductor complete without another control-chat turn; forced context
checkpoint -> new coordinator with retained findings; no second dispatch before
source cleanup; malformed/foreign/reused results; limits, ownership collision,
agreement mutation, no unreviewed completion, explicit provider configuration.
Keep legacy Roll tests green. Separately report native model/protocol evidence;
fixtures do not prove real context pressure or model compliance.

## Review request

Established Claude partner: read-only design review before lifecycle edits.
Find concrete holes in the above design and propose the smallest correction.
Especially: is this genuinely rolling the Conductor decision/review loop, and
does the durable result/ack boundary avoid lost or duplicated contributions?
Do not edit, dispatch, install, change bindings, commit or publish. Scope is
this design plus relevant existing roll.py, codex_roll.py and ask.py interfaces.
