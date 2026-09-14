# Managed Conductor implementation review

Anthony now authorizes release after we align and agree, then live testing.
Codex owns implementation and sole release; Claude reviews read-only. Please
do not edit, stage, publish, install, change bindings or dispatch other jobs.

Review the uncommitted implementation in:
- skills/switch/scripts/conductor_roll.py and tests/test_conductor_roll.py
- skills/switch/scripts/codex_roll.py: caller-specific checkpoint instruction,
  project on result, and durable reply/read-back before source shutdown
- skills/switch/scripts/roll.py: refuse the managed controller's record
- skills/switch/scripts/roll_status.py and its tests: typed controller display
- skills/conductor/references/managed-decision.md and managed-conductor.md
- entry links in Conductor SKILL.md/execution.md and Switch SKILL.md/to-roll.md

The previous ordinary entry changes were already reviewed. Focus on new lifecycle
and false claims. Your design corrections are implemented: write-ahead identity;
exact result references/digests, latest-ID ack and cumulative disposition map;
unresolved review findings stay in every decision payload until passing review;
review bound to tracked/nonignored-untracked content fingerprint, also applied
around read-only jobs; narrow decision contract; capability-labeled receipts;
stop-only request tied to run, with boundary pause. Codex decisions/implementation
are pressure-aware; reviews are bounded CLI turns. Host-process survival, Claude
coordinator pressure detection and automatic crash recovery are not claimed.

The adapter persists the full source reply before shutdown (status remains
running/checkpoint_saved), then the driver validates/promotes it to the saved
place only after clean source exit. That is deliberately distinguished from
validated handoff readiness: malformed output remains available for inspection,
but cannot launch a successor. The same private owner lock/ledger excludes legacy
Roll. Completed/blocked/uncertain records need explicit inspection and retirement;
only safe pauses resume under an unchanged agreement. No new retirement command.

Please run the new isolated tests and inspect/reproduce consequential gaps,
especially review -> correction -> new coordinator, stop/resume, crash windows,
tree scope and permission claims. Return numbered findings with reproduction or
file:line plus smallest correction. Is this ready for a bounded native scratch
trial and release after fixes? No live model behavior or token savings claimed.
