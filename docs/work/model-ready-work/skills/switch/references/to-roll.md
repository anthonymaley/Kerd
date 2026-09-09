# Managed To and Roll: fresh workers, same work

Do not run Out's backlog cleanup or replan the task at a mid-work boundary.
Save the agreed outcome and success measures, active step, useful decisions and
findings, current artifacts, pending question with shown answer, exact next action,
failure counts, optional resource limits and unresolved job state. No transcript
transfer, hidden-reasoning preservation or native process migration is claimed.

Read this guide for helper-managed builds, not ordinary device pickup. For a
managed To, also follow the [device-handoff rules](to.md); they own destination
identity, exact revision, source release and the portable pickup instruction.

## To: one device releases; the other continues

Everyday To is in [the shorter device guide](to.md). The implementation below
requires a live owning controller; it does not attach to arbitrary terminals.

### Managed-source save and recovery

For Conductor's running managed Codex job, the normal connection is the existing
command's input/output stream. Launch the Roll command below with
`--context-aware --control`, using a host execution tool that keeps stdin open
(for example its PTY option). Retain that tool's handle privately. Send one JSON
line through that same handle when the authorized destination is known:

```json
{"action":"to","branch":"work-branch","destination":"/existing/destination/clone","message":"Save current working place","files":["place.json","result.py","test_result.py"]}
```

The caller fills the real branch, destination and complete assigned output list;
the person should not have to compose this command. The destination must already
exist as a separate clean clone on the named branch with the same origin URL.
This first connection handles a local controller and reachable local clone, not
automatic SSH setup or a remote-session launcher.

For pickup in a fresh session on another device, add `"pickup":"on_destination"`
to that same To command. Supply the known absolute project path on that device.
The source does not resolve or probe that foreign path. It saves to the verified
remote and releases its worker, then returns `awaiting_destination` with the exact
revision, origin, agreement and place. This is not `destination_prepared` and
does not launch SSH or a remote model. Give the person one self-contained pickup
instruction carrying those facts and observed release evidence. Their fresh local
destination session performs the exact-revision checks above and continues under
the saved authority. Both released-source states prevent redispatch from the old
controller record; a new source run is not permission to duplicate the work.

`received` means queued, not moved. The adapter requests a safe checkpoint from
the same active native turn. The owner holds the source, commits assigned work,
checks the committed checkpoint and agreement, verifies the remote save, releases
its source, and prepares the exact destination. An explicit move may preserve an
unchanged working place; ordinary automatic looping still needs useful progress.
If the worker reaches review or a blocker first, the caller gets that result and
an explicit `handoff_not_performed`, not a fabricated destination launch.

On a failed save, inspect the reported cause and repair only within authority.
Send `{"action":"retry"}` to retry that same request with that same held source.
`{"action":"status"}` asks for status at a safe boundary; it is not a health probe.
`{"action":"abandon"}` explicitly ends this owned attempt, not successful To.
Closing the channel also abandons it; keep stdin open while expecting recovery.
Do not launch a replacement controller to retry a held source. A prior uncertain
record requires inspected recovery if its owner is lost.

On `handed_off`, Conductor uses the returned pickup and unchanged agreement to
start a fresh destination run immediately within authority. Source release and
destination preparation are observed separately from destination execution.
Cancellation during pickup may leave a synchronized checkout but must not launch
work. This is cooperative lifecycle control, not crash-proof process migration or
a security barrier against another writer changing the checkout concurrently.

For a source the local controller started itself, the Codex adapter supports
`run(..., hold=True)`. A completed turn returns with the same native thread and
process held open. Its transport remains running and its named-session lock stays
owned. The controller, not another model turn, then uses
[`ManagedTo`](../scripts/managed_to.py) with the branch, existing saved-place file,
previous state, explicit output files and protected input bytes.

`save_and_release()` validates the checkpoint, commits/pushes assigned files,
verifies the remote, and only then releases the owned source and verifies cleanup.
If saving fails, the exception returns to the still-running controller; it does
not close the source or start the destination. Diagnose the cause and repair only
what existing authority permits, then retry that method with the same held source.
Failed commits may leave an index needing inspection; don't reset it blindly.
`prepare_destination()` refuses without verified save and release and requires
the exact saved revision in a separate checkout. Conductor then dispatches the
fresh destination with the prepared records and unchanged agreement.

Use `inspect_held()` to check that the same source thread is loaded and idle,
without reading its turns. Unexpected activity or uncertain inspection is latched:
a later idle reading cannot make an old checkpoint trustworthy. Reassess rather
than retrying past that state. Explicit `release_held(abandon=True)` ends an owned
attempt as abandonment, never successful handoff. A cancellation request holds
the handoff for that disposition; it is not permission to start the destination.

The synchronous controller must remain alive and retain its bridge object until
release or explicit abandonment. There is no daemon, crash-survival guarantee,
automatic recovery after controller death, or control over arbitrary open user
sessions. Do not place unconditional source shutdown in a save-error `finally`.
Keep the failure and recovery visible. This managed route does not change ordinary
Roll's automatic shutdown after each completed worker.

## Roll: fresh window, same authorized build

Use the small local helper only for a designated managed build. It owns fresh
CLI runs outside the workers' context windows, through the existing Conductor
model connection. Model/effort are explicit and job-appropriate. Do not change
accounts, buy capacity or bypass permissions. No global hooks or service setup.

The current managed-run interface has an agreed-work Markdown file and a compact
saved-place JSON file. The latter carries status (continue/review/blocked),
next_action, memory, cumulative evidence paths, failure counts and pending jobs.
This narrow executable interface is not a new schema requirement for all projects.
Prepare it from the actual agreed work; never seed it with example approvals.

```sh
python3 /path/to/switch/scripts/roll.py --project /path/to/project \
  --agreement path/to/agreement.md --place path/to/place.json \
  --target codex --model VERIFIED_MODEL --effort SUPPORTED_EFFORT
```

Choose the provider and appropriate model from available evidence. The bridge's
Claude route has file tools, not shell or nested delegation. If a job requires
tools that route lacks, arrange a supported controller step; don't pretend tests
ran. No --max-runs or --timeout is required. Honor supplied optional limits, and
do not reset them or failed-correction counts when the context changes.

Each run completes a useful bounded piece, saves and verifies its working place,
and starts a genuinely fresh session—not resume/latest. Existing owner locks,
unfinished provider groups, repeated session identity, changed agreement, missing
evidence and uncertain outcomes stop automatic continuation. Three failed
corrections require Conductor reassessment. Artifact-change checks are not proof
of semantic progress; independent assessment still judges the result.

`review` means ready for independent assessment, not accepted or build complete.
Feed supported findings back through the same agreement and preserved counters.
A `blocked` or uncertain outcome needs actual diagnosis before any retry; don't
delete the helper's private Git metadata to bypass it. One managed Roll currently
owns a repo at a time; do not run competing builds in that same checkout.

## Observed context route — Codex candidate

For a managed Codex build, add `--context-aware` to the Roll command above. The
installed CLI must support app-server stdio, context-usage notifications and
turn steering. The helper starts only its own temporary CLI child; it installs
no daemon, opens no listener and does not connect to an existing app session.
It uses the existing CLI authentication and native project permissions.
This route is for file/CLI work: desktop computer control is disabled for its
owned child and thread. Some host versions still prewarm a desktop helper despite
that setting. After graceful EOF and an exit grace period, the adapter may send
TERM only to a still-matching child whose PID and start time it recorded while
owning the parent. It rechecks disappearance before continuation. Unknown or
uninspectable survivors remain a stop; no unrelated group or live app is killed.
No user-global setting changes. Choose another supported route for desktop work.

The helper observes the latest request's context usage and reported model window,
not summed billing tokens. At a conservative 65% threshold it requests a safe
saved place. `--context-fraction` can adjust that reserve; this is a context-safety
setting, not a mandatory user spending limit. A deliberately lower
`--test-roll-at-tokens` threshold is for exercising the mechanism and must be
disclosed as such. It is not evidence of surviving real near-exhaustion.

Missing usage, changed effective model/authority, a foreign turn, compaction,
unanswered host requests or uncertain cleanup prevents automatic continuation.
Reported usage arrives between model requests: a single unexpectedly large tool
result can still cross the reserve before steering. Do not promise universal
compaction prevention. Record what the actual run showed. Current usage includes
host input; it does not alone prove Switch-added input meets the pickup budget.

Conductor remains outside the workers and owns the next job, independent review
and evidence. A completed worker must return review or blocked, not invent extra
work to make a Roll happen. Claude still uses the existing bounded-piece route;
observed-pressure steering for Claude has not been implemented or proved.

### Recover an inspected failure

An uncertain run is a stop for Conductor to inspect, not a fresh user interview.
Read the retained error and artifacts, reconcile any jobs and verify source
processes have ended. The connection's `resolve` command can retire an interrupted
request only after its recorded group is gone; it cannot prove the work succeeded.
The observed-context route also requires verified shutdown of its owned children.
If their identities or state are missing, do not bypass the refusal.

Prepare a corrected saved-place file inside the project, keeping prior evidence
and failure counts. Then use the existing Roll command with
`--recover-state path/to/prepared-place.json --recovery-reason "Inspected cause and disposition"`.
This preserves the prior checkpoint and failure provenance, verifies the prepared
place and retires the old session identity. It does not dispatch work. Conductor
then continues the normal command in the same turn under existing authority.
Completed provider output can still need recovery if saving or validating its
checkpoint failed. A clean provider exit is not acceptance of its answer.

## Remaining boundaries

The first proof used explicit piece boundaries. A later managed Codex proof
completed one actual pressure-triggered fresh-worker transition and independent
artifact review. That does not guarantee no compaction inside a large operation.
Starting a managed loop from an arbitrary already-open interactive session and
automatically replacing that host remain unimplemented. Do not quietly redefine
the agreed experience to fit this partial mechanism. Keep those measures open.
