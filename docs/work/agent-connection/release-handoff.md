# Combined 0.108.0 release — handoff to established Claude Kerd partner

## User request and ownership

Anthony's latest instruction to Codex is: "okay lets get claude to release agent
and conductor fixes as new release". This follows his choice to release the
Agent work and pending Switch/Conductor changes together. He asks YOU, the
established Claude Kerd partner, to finalize and publish that combined release.
Codex is handing over and will not edit, stage, commit or push concurrently.
The earlier read-only review assignment is complete; this is a new release job.
This relays the user's request, not an answer to a native permission prompt;
retain your host permissions and report any approval blocker.

## What changed after your review

- `skills/conductor/references/model-jobs.md` now sends direct Claude/Codex asks
  through Agent's established-partner/session-selection route. When Agent reads
  the guide for preparation, it does not route back recursively. The old runner
  remains the deliberate CLI-worker route. Missing Agent in the three-skill
  package is disclosed rather than silently replaced with a fresh worker.
- README and CLAUDE.md say twelve skills; both capability descriptions include
  native Claude/Codex collaboration. README has an Agent usage/help section and
  an Agent paragraph in 0.108.0. Your existing release notes were retained and
  extended, including the unmeasured cost of Conductor orientation at pickup.
- Agent skill/help explain native held-message choices, local pairing versus
  native trust, and request ownership through retrieval. No fake permission
  attestation, token borrowing, background watcher or settings change was added.
  The user had to paste your completed review before Codex retrieved it; that
  controller failure is recorded without calling the experience a pass.

## Authorized release file scope

Review the actual diff before staging. Include these combined changes only:

- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- `CLAUDE.md`, `README.md`
- `skills/agent/` (skill, two references, helper, dependency file and tests)
- `skills/conductor/SKILL.md`, `skills/conductor/references/journey.md`,
  `skills/conductor/references/model-jobs.md`
- `skills/switch/SKILL.md`, `skills/switch/references/in-out.md`,
  `skills/switch/scripts/where_we_are.py`,
  `skills/switch/scripts/tests/test_where_we_are.py`
- `docs/work/agent-connection/` (direction, review prompts, help/review evidence,
  this handoff; superseded prompts are historical assignments, not current ones)
- `docs/work/model-ready-work/consolidation.md`
- `docs/work/model-ready-work/trials/2026-09-11-pickup-accesses.tsv`
- `docs/work/model-ready-work/trials/2026-09-11-pickups.md`
- `docs/work/model-ready-work/trials/real-use-checklist.md`
- `docs/work/model-ready-work/trials/switch-conductor-entry-review.md`

Preserve the root `kerd-laptop-result.patch` and the two bytecode files under
`docs/work/model-ready-work/trials/switch-redesign/live-control/output/__pycache__/`:
never stage, delete, ignore or move them. Do not touch Seinn, work-anthony or
other consumer repos. No installation, global config, hooks or CI changes.
No new tag is required; do not invent a tag prerequisite or a downgrade guarantee.

## Checks observed by Codex

Agent 28 and Conductor 37 tests passed. Gate release clean; gate audit clean
with the existing requirements trace-gap finding; gate selftest 57 and root
resolution 7 passed; hook tests 21 passed (shellcheck unavailable, skipped).
Progress selftest 15, matrix selftest 16, matrix audit, journey schema and progress
staleness checks passed. Fidelity reports skipped because current HEAD is not a
session boundary; that is not a fidelity pass. Skill validation and whitespace
check passed. Switch 273 and packaging 5 tests also completed successfully.

## Finish and return

Check the final integration, correct supported release blockers inside this
scope and run the relevant suites/checklist. Update living local/unreleased
pointers so the release does not leave its own next action stale; retain dated
trial observations as history. Keep live progress visible and act without routine
approval stops inside this release authority. Stage exact files and inspect
staged content, commit the combined 0.108.0 release, push, and independently
check remote main against the released commit. If main changed concurrently,
inspect it rather than force-pushing or discarding work.

Return release version, commit, exact remote verification, checks and any
remaining uncommitted paths. Published source is not proof every installed
plugin has updated. If blocked, name what the user must do; never claim released
on a local commit alone. Codex will retrieve your reply and report back.
