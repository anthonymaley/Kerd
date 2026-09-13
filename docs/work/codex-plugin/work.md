# Kerd core on Codex

## Now

Outcome: installable Codex packaging for Conductor, Switch, Visuals and Agent,
using the same maintained skills as Claude, with honest host-specific behavior.

Stage: Implementation and independent review complete. Release boundary:
`main`, subject `Release Kerd 0.113.0: Codex core and reliable pickup`.
Resolve its saved revision and remote state with Git; this record is prepared
before that save. Fresh-session checks remain pending.

Agreement: Anthony asked whether to package Kerd as a Codex plugin, agreed to
the four-core-skill scope, then said "okay lets make a plan and execute".
Anthony subsequently answered "yes" to installing into the user-level Codex setup.
After the combined review and corrections, Anthony said "okay lets release",
authorizing the 0.113.0 commit and publication. This does not refresh installations.

Scope: local implementation, generated artifacts, isolated tests and the approved
user-level Codex installation, followed by the authorized release. No consumer
projects are changed. The existing Claude partner supplied review and closeout;
no fresh model session was launched. Eight legacy skills and Claude hooks remain outside the Codex core
artifact. The full Claude distribution remains twelve skills with its hooks.

Plan: extend the existing packager; derive the version from the source release;
include Agent and its dependency declaration; document installation/update/use;
correct host assumptions; test the relocated package and save/pickup round trip.

Current activity: release boundary prepared after verification. The installed
snapshot is unchanged; ordinary-use checks remain after publication.

## Implementation

The existing `docs/work/model-ready-work/packaging/build.py` now packages four
skills. `--codex-marketplace` emits a fresh catalog with `plugins/kerd/` and a
native `.codex-plugin/plugin.json`, plus a local catalog entry. It never installs
or overwrites output. Manifest templates inherit the root release version.
The generated copy is not a second maintained implementation.

The package keeps references and helpers together, includes the explicitly
allowlisted Agent requirements file, excludes legacy skills/hooks and private
history, and reports a runtime-independent path for development evidence.
Conductor's native-job rule now checks host/model availability rather than
assuming a Claude-native subagent is available inside Codex. The Out completion
hint uses client-neutral wording and retains the confirmed-save requirement.

The preceding reading-set fix remains in this same release preparation. It
returns reusable selection arguments, uses one selector for measurement and
preparation, and labels selections reaching EOF. It does not freeze content or
prove a later edited source still has its previous size.

## Evidence and limits

Packaging tests cover exact shared-source copies, four-skill scope, current
manifest versions, optional dependency inclusion, safe destinations, relative
links, catalog resolution, Agent help without provider tools, and a packaged
Switch save followed by a separate-process pickup in a temporary Git repo.
The round trip preserves the authority text and compares measured bytes with
restored content, while leaving the unselected historical tail on disk.

Results: packaging 9; Switch full suite 298 before the additional host-neutral
hint test, renderer suite 90 afterward; Agent 117; Conductor 37; hook checks 21;
gate selftest 57 and root resolution 7. Release check clean; audit clean with
the existing requirements trace-gap finding. Skill and Codex manifest validation
pass. Agent tests emitted SQLite ResourceWarnings; shellcheck was unavailable.
No claim that those warnings or the existing audit finding were corrected.

Artifact: `output/kerd-codex-0.113.0`, a generated, ignored catalog. After approval,
`codex plugin marketplace add` registered this catalog as `kerd-core`, then
`codex plugin add kerd@kerd-core --json` installed version 0.113.0. A subsequent
`codex plugin list --marketplace kerd-core --json` reports installed and enabled.
The installed cache and generated package compare identical with `diff -qr`;
the cache contains only agent, conductor, switch and visuals. Claude's install
was not changed. Retain this local catalog while it is the registered source;
it is not a published Git marketplace and will not track source edits automatically.

Fresh-session skill discovery, an actual Codex conversation through Conductor and
Visuals, live bidirectional pairing and token savings are not established by
those tests or installation. No such model jobs were launched here. The user
guide lists the fresh-session live check separately.

Next action: verify this boundary's Git/remote state before any retry of publication.
After the intended build is installed with applicable setup authority,
open a fresh Codex session in a work project and run Switch In; identify the
actual installed snapshot. The independent combined review and correction check
are complete. This record does not claim CI or remote verification before saving.

Documents: [installation and update guide](../model-ready-work/packaging/START.md),
[packager](../model-ready-work/packaging/build.py),
[package tests](../model-ready-work/packaging/test_build.py).

## Shared pickup corrections after installation

Anthony approved product-level fixes, not edits to the project that supplied
the example: factual clarification does not approve subsequent work; the
arrival question appears once; logs preserve claims rather than prove events.
Conductor handles reply meaning; Switch explains the evidence limit and offers
`--question-below` without adding summary fields. The remaining host-specific
delegation paragraph now points to the shared model-job route.

Five new renderer tests use a generic conflicting-preview scenario, cover both
CLI inputs and question placements, preserve complete qualifications, and check
widths 50/78/100. They first failed on the absent flag, then all 95 renderer tests
passed. These checks prove presentation, not model interpretation of authority.

Behavioral regression to observe in ordinary use (not yet run): the work notes
say a preview was seen, the delivery checklist says it was not opened, and the
next design has no approval. In should show the uncertainty and one factual
question without starting work. A reply of Yes or No settles only the reported
observation; Not sure leaves it unresolved. None grants design approval.
An independent already-authorized task may proceed if it does not depend on
that fact. A reconstructed log must not be presented as observation evidence.

The paired Claude release session acknowledged coordination and holds edits.
It owns no overlapping uncommitted changes; its later Switch Out remains owed.
It also flagged the old release-111-followup pointer for later closeout repair;
that unrelated record was not changed in this pass. No new installation,
commit, push or consumer-repository change is part of these corrections.

Post-correction checks: Switch 304, including renderer 95; Conductor 37;
packaging 9; release clean; audit clean with its existing trace-gap finding;
Switch and Conductor skill validation and `git diff --check` pass.

## Independent combined review

The established Claude partner (observed Fable 5.1, native settings unchanged)
reviewed the combined uncommitted diff against 75f97e5. This was a substantive
read-only review, not the earlier acknowledgement. Its brief is
[review-prompt.md](review-prompt.md). The matching local Fable 5.1 and shared
Claude profiles exist at version 2026-09; the controller read them only after
dispatch, so this run does not establish profile-led prompt preparation.

Claude reported passing Switch, Conductor, Agent, packaging and hook suites,
release/audit checks, relocated package links and question-placement probes.
It found no code defect. It requested an explicit native-subagent default and
named CLI exceptions in execution.md; that wording is now restored without
assuming a Codex host can spawn Claude natively. Its low-priority EOF-label
clarification is also made: complete files always reach EOF, while a section's
flag concerns its terminating heading. The Codex catalog schema was not
independently verified by Claude; prior local installation remains the evidence.

The missing Kerd pickup pointer is assigned to Claude's already-owed Switch Out
for CONTEXT.md, TODO.md and today's log, subject to its existing authority and
without overlapping this pending tree. The pointer must distinguish the older
installed snapshot from current source and retain the fresh-session/live checks.
That closeout is still outstanding, not performed by this review. No release,
commit, publication or installation approval is inferred from the review.

Claude subsequently read both corrected paragraphs and marked them ready, with
no blocking wording issue; it acknowledged the future Out ownership explicitly.
Post-wording checks: packaging 9, both skill validators, release check and
`git diff --check` pass. This is review completion, not release completion.

Release validation: Switch 304, Agent 117, packaging 9, hooks 21, gate selftest
57/root 7, progress 15, matrix 16, matrix audit, stage schema and render-current
checks pass. Agent still emits its previously disclosed SQLite ResourceWarnings;
shellcheck is unavailable. Conductor's first release run errored in
`test_uncatchable_runner_death_blocks_session_reuse_and_close` on `os.killpg(group, 0)`
with PermissionError; an isolated complete rerun passed 37/37. No code or test
was weakened, and the intermittent process-check error is not diagnosed or
claimed fixed. Release and audit checks retain the known audit trace gap.
