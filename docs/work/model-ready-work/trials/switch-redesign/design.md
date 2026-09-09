# Switch: keep your place, leave room to work

Status: direction agreed; candidate build and trials in progress, not accepted or installed.
[Open the connected view](direction.html) · [User decisions and current place](work.md)

## Four actions, one memory of the work

| Action | Purpose | What happens next |
|---|---|---|
| In | Restore the repo and useful working context | Continue the exact authorized action, including an active Conductor build |
| Out | End the sitting well | Record history, tidy active work, commit/push relevant files and prepare next time |
| To | Move the precise working position to another device | Save through GitHub, end source control and exit; destination restores that position |
| Roll | Give the same build a fresh context window | Freeze useful state, start a fresh run, thaw and continue automatically |

To and Roll do not run Out's backlog cleanup or replan the work. In recognizes
whether it is restoring a prepared sitting or a precise mid-work handoff.
GitHub moves repository files, not native conversations or running processes.
Normal SSH/tmux use remains unchanged.

For a source started by the local controller, To now separates paused work from
source exit. The same source stays open while the controller saves. A failed save
returns control for an authorized repair; it cannot start the destination. Verified
remote save → verified source cleanup → exact-revision destination pickup is the
successful path. [The local failed-push trial](failed-save/results.md) exercised
this with real work and fresh native sessions. The controller must remain alive;
this is not crash survival or takeover of an existing user session.

At entry, distinguish changing consoles for the same SSH/tmux session from moving
work to a fresh local session. The former needs no handoff. A normal interactive
source without host control can save its place but cannot claim automatic exit.
For a precise destination pickup, the saved Git revision is checked before updating
working files; a newer branch tip is not silently treated as the same handoff.
[Entry behavior and regression evidence](to-entry/results.md) are separate from
the [live controller connection](live-control/method.md). Conductor starts managed
Codex Roll with an open input/output channel, retains its execution handle and
sends To to that same owner. A safe checkpoint request reaches the current turn;
no new worker impersonates the source. Failed saves wait for an inspected retry
or explicit abandonment. A verified handoff returns its exact destination to
Conductor, which starts the fresh worker without another routine user turn.
The first connection uses existing separate local clones; remote session startup
is not implemented. Ordinary interactive sessions still need supported host control.

For a named handoff, first locate the specified repo/branch/record. If it cannot
be found, stop instead of substituting ordinary project pickup or readiness work.
Carry that instruction and the task authority in destination startup; do not
assume the destination already has the candidate installed. This targeted rule
comes from the [wrong-checkout trial and forward test](pickup-correction.md).

## The memory we carry

Keep current project context, active work and durable history, but give them
different reading roles. A small start page locates the current work and the
necessary project rules. The work's saved place carries the agreement, exact
next action, current artifacts/evidence, unresolved decisions, review findings,
failed attempts and relevant running-job status. Link historical detail instead
of copying the same narrative into every record.

The start page is a pointer, not another brief or dashboard. Existing suitable
files can fill these roles; do not create parallel CONTEXT/TODO systems. Exact
file placement will follow the trial repo's existing structure.

On In, load the complete selected working set, then retrieve specific history
when a decision needs it. Do not read the entire archive by ritual or silently
truncate something claimed as read. Still-applicable decisions remain available
regardless of the age of the task that introduced them.

For a fresh reader, Conductor can prepare that working set once: choose the
existing current records → gather their complete text with source labels → give
it to the reader → check that decisions, owed work and restrictions survived.
The optional `handoff.py prepare` command handles gathering, not choosing or
summarizing. Named sections include their children; missing or ambiguous sources
are reported, never replaced by guesses. No new persistent memory file is needed.
The source-selection work still costs resources outside the fresh reader.

On Out, remove evidenced completions from active lists and retain their completion
record. Retire redundant tasks only with an established reason; uncertainty is
not permission to delete. Archive old work without rewriting dated history or
breaking useful links. Show what changed. This deliberately replaces the legacy
rule tying all pruning to acceptance records and the mandatory full daily-log
pickup; those old instructions must not remain active beside the new behavior.

## Roll without magic

A model cannot reliably promise to clear and restart the host containing it.
Candidate implementation: a small local helper outside the model's context window
starts a run through the existing CLI, waits for a safe saved handoff, verifies
the next run can find it, then starts a fresh run from that state. It does not
resume the entire old conversation. No CI, custom hooks or hosted service.

The helper coordinates lifecycle; Conductor still directs the build. The job
agreement, permissions, failure counters and optional resource limits persist.
Only the conversational working space is renewed. Progress stays visible:
working → saving place → starting fresh → restored → continuing.

The managed Codex route now observes latest-request context usage, asks for a
safe checkpoint, verifies saved work and ends its owned worker before starting
the next. Its default reserve is 65% of the reported usable window; lower trial
triggers are explicitly labelled tests. It handles its own surviving children,
not arbitrary live app sessions. Claude remains on the bounded-piece route.
See [implementation and live evidence](conductor-roll-proof.md) for the successful
clean transition, earlier failures and the remaining product boundaries.

This first implementation proves a helper-managed build loop. It must not claim
it can take over or terminate arbitrary already-open Codex/Claude app or terminal
sessions. Entering an existing interactive session into that loop needs an honest
supported transition. Investigate this boundary before implementation; if it
changes the agreed experience, bring that change back to the user.

The helper stops on completion or a genuine unresolved blocker. Before another
run it checks actual progress so repeated identical failures cannot spin forever.
Jobs still writing must finish safely or be explicitly reconciled before handoff;
do not blindly relaunch an uncertain job. Source release and destination start
must not create two owners of the same work. A failed save leaves the source
available for recovery, rather than exiting and losing the place.

## Low-context pickup: agreed trial target

For the representative Seinn trial, the agreed target is **at most 8,000 additional input
tokens for pickup, and at most 5% of the host's usable context window when that
capacity is observable**. Count Switch instructions, selected memory and pickup
tool output through the point it is ready to do the next task. Separate existing
host overhead. This is an agreed product budget, not a vendor recommendation or
an observed result. The [local measurement](pickup-budget/results.md) now records
actual native readings, including failed discovery runs and a smaller prepared
input. This does not establish whole-workflow cost or automatic source selection.

File bytes and billing totals are not interchangeable with context occupancy.
Use available per-request usage and a disclosed tokenizer/estimator as appropriate;
if the measurement cannot establish the target, report it unassessed. A task
needing unusually large essential context is disclosed, not silently trimmed.
Compare against current Switch on the same work and report time too. Passing the
budget is insufficient unless independent restoration checks pass as well.

## Build and proof sequence

1. **Prove the risky connection first.** In an isolated workspace, have a small
   real build cross two fresh runs automatically, with saved state as the only
   task-history bridge. Verify fresh sessions and no resumed transcript; inspect
   the artifacts and preserved constraints. Exercise both supported providers.
2. **Implement In and Out.** Use a separate Seinn clone; inspect its actual state
   and history, design the lean read set, preserve decisions, tidy active work,
   and demonstrate correct pickup with measured input. Do not alter its live
   checkout or main. Baseline files measured 430,854 bytes including the newest
   daily log; actual token cost is still unmeasured.
3. **Implement To and join Roll.** Use an unused dedicated Seinn trial branch.
   Verify GitHub save, destination freshness, source release and exact next-step
   restoration. A two-clone local test is preliminary, not a device handoff pass.
   Select actual destination access before connecting; no guessed SSH targets.
4. **Independent assessment and demonstration.** Check continuity, footprint,
   cleanup and honest failure behavior against the user's measures. Correct
   supported findings within the agreed bounds. Show actual results for final
   user review; no automatic live installation.

No deadline or trial spending cap was requested. Use existing access, appropriate
models and efficient work; do not buy capacity, change accounts or bypass host
permissions. A helper-managed proof or manual workaround must not be reported as
universal interactive-session restart support.

## Direction decision

The product behavior comes from the confirmed interview. The implementation
proposal adds the small local helper and a concrete pickup budget. Agreement to
this design authorizes the scoped build and tests, not a claim that the unknown
host behavior already works. Source facts and official CLI references are kept
in the work record; no copied vendor manual is needed in the pickup prompt.
