# Roll first proof — real results, bounded scope

The user approved the integrated direction with “perfect”. This is the first
implementation slice, not the whole Switch redesign or a passed Seinn handoff.

## What is being exercised

Build a usable standard-library handoff-report CLI in three bounded pieces:
implementation, tests, then documentation and supported corrections. Deliberate
piece boundaries force two fresh-context transitions. A different actual native
session must be observed for each run. Only the agreement, saved place and task
artifacts bridge those runs; no resume/latest or native transcript transfer.

The saved-place fixture starts with a clearly seeded failure count of one, so
the test can detect lost accounting. That seed is not an actual build failure.
The helper returns review-ready, not independently accepted, when the worker says
its pieces are done. The controller runs the tests and an independent reviewer
assesses results. Deliberately placed boundaries do not prove automatic detection
of imminent context exhaustion or takeover of an existing interactive session.

## Jobs and guidance

- Codex build: gpt-5.6-sol, high effort. Appropriate coding/reasoning route with
  workspace-write tools; local GPT-5.6 profile 2026-09-05 and shared guidance used
  for outcome-first prompts and native effort. Not selected as a cost shortcut.
- Claude build: claude-opus-5, high effort, using local Opus/shared 2026-09 guidance.
  Clear bounded task with agreement/saved-place boundaries. The existing bridge
  gives file tools, not shell/delegation; main runs the resulting tests.
- Independent native safety review of the helper: current inherited model,
  separate agent, isolated fake-transport tests and raw source/design. No live jobs
  or remote writes by that reviewer.

The existing bridge owns provider execution and private session/event evidence.
Roll adds fresh aliases, saved-place read-back, task progress checks and a local
exclusive owner. Worker edits remain prompt-bounded within the project; this is
not a new OS sandbox or a claim that prompt instructions enforce file isolation.

Local trial root: /tmp/kerd-roll-proof.QujmIu. Model prompts and raw native session
IDs stay in each trial repo's Git metadata. Publish only sanitized observations
and reviewed deliverables here. No credentials or native transcript archive goes
into the shared work pack.

## Results

| Check | Observed result |
|---|---|
| Codex real build | Three fresh native sessions; two automatic transitions; status review |
| Claude real build | Three fresh native sessions; two automatic transitions; status review |
| Codex artifact tests | Controller independently ran 13 tests; all passed |
| Claude artifact tests | Controller independently ran 34 tests; all passed |
| Saved accounting | Seeded failure count 1 retained by both; cumulative artifact paths retained |
| Corrected helper safety tests | 21 Roll tests and 16 Git handoff tests; 37 passed |
| Skill validation | Candidate Switch passes skill-creator quick_validate |
| Independent artifact assessment | Claude reviewed the Codex result; no blocking finding in inspected scope |

Each provider returned continue, continue, review. Native session identity was
distinct within each three-run build; requests used fresh aliases, not resume.
The sequence needed no human “next” messages. This is actual useful artifact work,
not just a message echo. Codex was requested as gpt-5.6-sol/high; the bridge's
returned model field was unavailable. Claude reported claude-opus-5. Do not turn
requested identity into an independently observed model version.

Claude's route did not have shell tools and correctly disclosed that its tests
had not run. The controller ran them afterward. The Codex example is preserved
in [roll-example](roll-example/USAGE.md). The independent review and its limitations
are in [returned review](roll-artifact-review.md), with the
[actual review prompt](review-roll-output.md). Test-quality and hardening observations
remain visible; this review is not a claim that every invalid input was exercised.

The live builds exercised the initial helper revision. Independent review then
exposed ways to disguise no progress with evidence aliases, fresh helper instances,
or a return to baseline. The corrected helper seeds and retains artifact snapshots
and rejects duplicate/protected evidence paths; all 37 tests passed after correction.
The live successes were not rerun under that corrected revision. Artifact changes
still do not prove meaningful progress or truthful worker reporting.

## What this does not establish

- Automatic detection of context exhaustion or prevention of native compaction
  inside a long piece. The boundaries were deliberately specified in the fixture.
- Replacing or exiting an arbitrary existing interactive app/TUI session.
- A two-device move or exclusive ownership across two machines. The helper's
  owner lock is local; Git alone does not establish cross-device source release.
- The agreed low-context budget. Prompt byte sizes and cumulative input/cache
  billing usage were observed, but neither is current context occupancy. No
  token-cost pass, speed improvement, cost saving or universal lossless recall
  is claimed from these runs.
- Final acceptance. `review` means independent assessment is due, not that a
  worker can grant producer acceptance.
