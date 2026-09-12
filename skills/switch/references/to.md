# To: continue on another device

Do not run Out's backlog cleanup or replan the task at a mid-work boundary.
Save the agreed outcome and success measures, active step, useful decisions and
findings, current artifacts, pending question with shown answer, exact next action,
failure counts, optional resource limits and unresolved job state. No transcript
transfer, hidden-reasoning preservation or native process migration is claimed.

## To: one device releases; the other continues

Start from the person's intent and the current session, not a guessed mechanism.
Use answers already recorded; ask one focused question only if the route is unclear.

| What the person means | What Switch does |
|---|---|
| Reconnect to the same running SSH/tmux session from another console | Keep that session and work running. Use the known connection; no Git handoff or source exit is needed just to change consoles. |
| Move active work owned by a live local controller to a fresh session | Use that owning controller's [managed To path](to-roll.md#managed-source-save-and-recovery). It saves, verifies and releases its actual source before destination work. |
| Move work from an ordinary interactive session | Save the precise working place under existing Git authority. If host exit is unsupported, show “saved; source exit still needed” and stop short of destination execution. |

A running marker, process ID, tmux environment variable or saved transport record
alone is not a live controller handle. Do not start a new worker and call its exit
the exit of the person's original session. Don't kill a pane, send exit keystrokes
to a guessed target or introduce a background service to bridge this gap.
For the managed route, use the already-owning controller through its available
connection; a separate invocation cannot reconstruct its live Python object.
If no such connection is available, report that specific limitation, not success.

Show a compact journey line and the saved-place link as work proceeds:
`Save → source release → destination pickup → continue`, marking only observed
steps complete. At a stop, name the unfinished step and what can actually resolve
it. Same-session console use instead shows “Same session continues; no handoff”.
Don't add an interview, replan, full Out cleanup or routine “shall I continue?”.

Resolve the source repo/branch and intended destination.
For destination startup, provide one self-contained pickup instruction carrying
the repo, branch, exact saved revision, record path, source-release evidence and
authority—not a trial nickname alone. Keep private session IDs and credentials
out of the portable instruction. The
destination must find that record before using generic project memory. A wrong
checkout or absent record stops the attempt; do not replace it with local readiness
checks. This instruction must travel with the handoff because the destination may
not have this skill installed.
If the person must carry the instruction, put it in one copyable plain-text code
block after the short status summary. Link the saved record for detail rather than
repeating its whole narrative in the user-facing response.

When the helper is available, use `handoff.py prepare` with `--branch`,
`--record`, `--commit FULL_SAVED_COMMIT` and `--sync`, adding only the current sources
needed for the next action. It checks the fetched revision before updating the
checkout. Fetch can update Git metadata even when pickup refuses; working files
and HEAD are not advanced to a mismatched handoff. A newer tip needs reconciliation,
not silent adoption or reset to an older commit. Ordinary latest-state In can omit
`--commit`. This uses the existing Git revision, not a new seal or approval scheme.
Complete command shape for the caller, not parameters the person must invent:

```sh
python3 /path/to/switch/scripts/handoff.py --project /path/to/destination prepare \
  --branch SAVED_BRANCH --record SAVED_RECORD --commit FULL_SAVED_COMMIT --sync
```

Without the helper, carry the same checks explicitly in the destination instruction.
Loading files is not evidence that the source stopped: without release evidence,
restoration may be inspected read-only, but active work must not start there.

Preserve relevant edits and publish the precise handoff through the agreed GitHub
route; use the [verified save helper](in-out.md#default-verified-save-when-pushing-is-authorized)
by default when its workflow applies, preserving the same checks for a disclosed fallback. Verify the saved remote revision
before relinquishing the source. Failed save: retain control and name recovery.

The user requires the source to end control and exit, not keep writing alongside
the destination. Account for running children: finish safely or resolve their
status under standing authority, never blindly duplicate or kill them. An unknown
job is not a clean handoff. On the destination, safely synchronize the intended
repo revision and restore this precise place—not a generic next-sitting summary.

Source exit requires control of the actual source session. Issuing `exit` in a
child shell does not exit the model host. The current Git helper explicitly reports
that it has NOT exited the source. With no supported host lifecycle route, report
“saved, source exit unproved” and the exact needed transition. Do not count a manual
exit as automatic To support. Arbitrary interactive-host exit is not implemented
by this candidate. Normal SSH/tmux console use needs no migration at all.
