# Switch in / out / to redesign

## Direction

The user selected “switch in/out/to redesign” as the next real build trial of
the refreshed Conductor experience. This names the work, not a complete outcome
agreement. Keep this package within the existing model-ready-work pack.

### Outcome clarified by the user

“yes this is new, i want to be able to switch my session to another device, so
move it to my laptop so i can take it with me, or return it to the studio to work
while im out”

`To` means a device handoff: take the current work to the laptop, or return it to
the Studio so work can continue there while the person is away. The desired
continuity is established; the mechanics are not. Whether this requires moving
a native conversation, restoring project context, remote access or handing over
execution is still to be investigated, not assumed supported.

The user answered the follow-up about checking in from the laptop: “yes but via
tmux ssh”. Once work is on the Studio, the intended interaction is SSH with tmux,
not a new remote-control interface. This settles the outcome follow-up, not the
mechanics or feasibility of moving a native model session between devices.
Topic 1 is confirmed by these two substantive answers; no repeat confirmation
is needed. Source and destination execution, running-job handling and transfer
contents remain questions for later understanding and technical investigation.

### Device continuity clarified — current direction

The user clarified: the Studio normally hosts sessions because it has more
memory; the laptop is a console through SSH/tmux. Alternatively, the user starts
a fresh local session in iTerm in the laptop's repo directory. Switch-in should
bring in the latest GitHub repo state, then load the saved memory. The user said
“we dont need to sync the sessoons other than github repo” and “we can trial in
that mode”.

This resolves the earlier native-session-transfer uncertainty: continuity travels
through the repo and saved memory, not synchronized provider conversations or
migrated running processes. Test the fresh-local-session pickup path. The Studio
remote-console workflow remains usable without building a new remote interface.
Do not assume a Git push transfers, stops or starts a running agent. Handling
unfinished work safely is still relevant; a process-migration system is not.

## Audience — confirmed

People using Kerd for repo-based work, including people continuing across their
own devices. Begin the device trial with the user's laptop and Studio; do not
hard-code the skill to them. SSH and tmux are the user's chosen way to interact
with work on the Studio, not a universal requirement for local save/resume.
The user confirmed the audience with “yes” and supplied the normal and alternative
device workflows above. Shared-team handoffs and a new remote UI are not
established requirements.

## Starting evidence

- [Current Switch](../../../../../skills/switch/SKILL.md): the inspected usage
  section names in and out, with the same boundary flow for same-machine pickup
  and moving machines. No `to` usage was found in the inspected material.
- [Candidate Switch](../../skills/switch/SKILL.md): saves/restores a work record
  and handoff pointer without automatically committing, pushing or pulling.
  It explicitly disclaims automatic native-session transfer and backup.
- These are design inputs, not decisions to preserve every current behavior.
  The device meaning of `to` is now clarified above; its implementation is open.

### Starting point and preservation — user input

The user clarified that in/out themselves are central to the redesign, not just
the new device handoff. Switch-in should read the session and repo's current
position, recover what happened last session and what should happen this session,
and be fully context-aware, with “no compacting”. Switch-out should save the
session and context, commit files and prepare the next session. Existing GitHub
interaction and memory saving are valuable responsibilities to preserve while
making the process more efficient.

The inspected current Switch supports this description: it owns boundary Git
operations and maintains state, work and append-only history. The lighter
candidate's no-automatic-Git behavior is therefore not the agreed replacement
for this redesign. Do not silently remove these responsibilities for efficiency.
Exact Git behavior, failure handling and authority will be settled in this work;
this discussion is not a request to commit, push, pull or end the session now.

The user rejected verbatim conversation retention: “no, thats overkill, how does
switch do it now?” After an explanation of state + next work + durable session
history, the user agreed to optimize that approach. No transcript capture or
control over native host compaction is requested. Preserve useful working context
and decision history, not every utterance.

### Outgoing cleanup and focused pickup — agreed direction

The user requested removal of done tasks, archival of old work during switch-out,
and better selection of what switch-in reads so context is not bloated before new
work begins. Topic 3's starting point and desired improvement are established by
these substantive answers; no additional confirmation of them is needed.

Design implications to work through, not an implemented archive scheme:

- Move evidenced completions out of the active task list while retaining a
  reachable completion record; an uncertain task is not automatically done.
- Archive inactive/historical work without discarding it. Age alone does not
  establish that a decision, dependency, unfinished task or risk is irrelevant.
- Keep still-applicable decisions and constraints visible even when the work
  that introduced them is complete. Avoid copying the same narrative into several
  pickup files.
- Define a purposeful pickup set: current project position, standing constraints,
  active work, last-session handoff and next action, with specific historical
  detail retrieved when needed. This changes how context is organized, rather
  than silently truncating a file that the skill claims to have read fully.
- Explicitly reconcile the redesign with legacy event-restricted pruning and
  full-newest-daily-log reading; do not leave conflicting instructions or silently
  change the live rules during this trial.

Exact archive placement, read selection and Git operations remain design work.
No live TODO entries or history have been removed, moved, committed or pushed.

## Deliverables and scope — user-corrected direction

- Redesign in/out/to as one coherent Switch skill, with usable instructions and
  evidence from a repo-based handoff trial.
- Out: close and prepare the sitting. Commit relevant files, record work done,
  remove evidenced completions from TODO/backlog, retire demonstrably redundant
  tasks with reasons, archive historical detail, save session history and useful
  context, and line up the next session for quick, informed continuation.
- In: restore repo state and working context from the last session, including
  what happened and, crucially, exactly what to do now. Recognize an active
  Conductor build and continue its next authorized action automatically, without
  another start/continue ceremony. This is needed for the build loop. Preserve
  genuine unresolved questions, failed attempts and authority limits; pickup
  must not invent an approval or rerun an uncertain active job.
- To: save the specific mid-work position through GitHub for destination pickup,
  as close to continuing the same session as possible. This is NOT full switch-out:
  do not perform end-of-sitting task cleanup, archival or replanning as a substitute
  for saving the exact place. Capture the current work/step, relevant decisions,
  current artifacts and results, pending questions/jobs and exact next action.
  These details are a proposed means of fulfilling the user's continuity request,
  not a claim that native conversation or running-process state is transferable.
- Destination restoration must distinguish that precise mid-work handoff from
  the prepared-next-session handoff produced by Out. The destination invocation
  and storage details remain to be designed; no new mandatory command is assumed.
- Trial: save/push from the source, then use a fresh local session in the laptop's
  repo to pull/read and continue. Do not claim a two-device test from two local
  directories or a synthetic transcript.
- Outside this proposed build: copying native sessions, moving running processes,
  replacing SSH/tmux, a new remote-control UI, and live installation without
  separately established authority.

Correction provenance: the previous proposal made To “the same save/pickup flow”.
The user explicitly rejected that equivalence: “save to gihub but not a full
switch out” and “very specific state save and restore”. Shared Git plumbing is
possible; shared closeout behavior is not the requested experience. The user also
specified automatic continuation of an active Conductor build on In.

### Source control — user decision

The user answered: “now handoff: source ends control and exits session”. To is
therefore an exclusive handoff, not two sessions continuing the same work. This
describes the redesigned behavior, not an instruction to exit this interview.
Safe implementation must establish that the handoff is durably saved before
relinquishing the source; a failed save must not be presented as a successful move.
Git transfer and session exit do not by themselves prove child jobs stopped.
How to finish, pause or reconcile those jobs is still technical design work, not
permission to indiscriminately kill processes.

### Conductor fresh-context continuation — proposed addition

The user suggested a Conductor-specific action that “saves all that it neads and
clears context, restarts build as if nothing happended (with clear context window)”.
Desired outcome: continue the same agreed build in a fresh context window, without
re-interviewing, replanning or asking for another go-ahead merely because the
window changed. This is distinct from full closeout and from moving devices.

Recommendation: one Conductor-aware action within Switch, sharing the needed
save/restore behavior, rather than a second independently maintained boundary
skill. A command name has not been selected.

The saved build state must preserve the agreed outcome and measures, authority
and optional resource limits, current plan and active step, reviewed results,
unresolved findings, failed-attempt counts, pending jobs and exact next action.
Fresh context does not reset permissions, retry counts or resource accounting.
Persist task-relevant state and evidence, not hidden reasoning or a verbatim
conversation. Files must be verified before any destructive context reset.

Host support for clearing/restarting a context window and automatically resuming
must be investigated for each supported host. Writing a handoff is not proof
that a skill can restart its own host. No such capability is claimed yet.
The user confirmed autonomous initiation as the desired outcome: at the Conductor
build loop there may be more work than one context window can hold, so save the
position ("freeze"), resume in a new context window ("thaw") and continue toward
build completion without making the user unblock routine continuation. This
settles the scope follow-up; it is not evidence of host support. No context
threshold or new spending permission is assumed.

## Experience — established through the user's answers

Standard topic: What should the experience of using the result be like?

The user wants continuity: In knows precisely what to do now and continues an
authorized Conductor build without ceremony. To ends source control and restores
the precise place on the destination. Freeze/thaw keeps a long build moving across
fresh context windows without repeated input or manual restart prompts.
These direct answers settle the desired experience; do not ask the user to
confirm the same automatic-continuation preference again. The earlier visual-UX
direction still applies: show current work, a brief truthful transition update
and resumed position. Do not fake invisible background execution.

Automatic continuation does not remove genuine stops for missing authority,
material outcome changes, failed recovery or an unresolved consequential decision.
Those existing protections are not routine context-change approval ceremonies.

## Success and proof — agreed direction

Standard topic: What does success look like, and how will we prove it?

The user answered “yes” to the displayed success examples, then added “also
switch in does not consume significnt context”. The tests below are agreed
direction, not achieved results. The added small-footprint requirement still
needs an operational threshold during design; no numerical target was supplied.

- A real build continues through at least two fresh-context transitions and
  reaches its agreed result without the user supplying routine next/go commands.
  Independent review checks retained decisions, next actions, measures, failures,
  authority and resource accounting; no repeated or skipped completed work.
- A precise GitHub-backed device handoff saves the work, ends source control and
  restores the same active step in a fresh destination session without a full
  closeout. A same-machine fixture is not presented as two-device evidence.
- Out removes evidenced completions and demonstrably redundant tasks from active
  lists while preserving reachable history and still-applicable decisions. In
  restores what happened and what to do next from the resulting records.
- Compare pickup time and loaded context against current Switch on the same
  representative work. Improvement must retain all decision-relevant context;
  no arbitrary percentage target, silent truncation or fabricated token count.
- Switch-in must not consume a significant part of a fresh context window.
  Merely using less than the legacy baseline is insufficient. Measure actual
  pickup context, including skill/reference instructions, loaded records and
  relevant tool output, not just visible response length. Distinguish existing
  host overhead from Switch-added input and disclose unavailable measurements.
  During design propose a concrete small-footprint target using observed data
  and available context; establish it before claiming the requirement met.
  Smaller pickup must still pass context-restoration checks, not hide omissions.
- A failed save or restore never triggers blind continuation or a false success
  report. Host limitations remain visible; a manual fallback does not prove the
  automatic build-continuity measure passed.

These examples make continuity, safety and efficiency observable. Desired
benefit: long work reaches completion with less supervision and less context
wasted on stale material, not merely more successful file writes.

## Trial limits — confirmed

The user answered topic 7: “yeah no limits lets just get it done as quick as
possible and prove it out”. No time, token or spending cap was requested for
this trial. Prioritize efficient implementation and real proof, not extra
ceremony or speculative breadth. This does not authorize new purchases, paid
overages, weakened success criteria or unbounded unrelated work. The small
Switch-in context footprint remains a product success requirement.

## Authority — confirmed boundary

The user answered “yeah” to the displayed candidate/isolated-test boundary.

Implement the redesigned candidate and its supporting files in the existing
work pack/isolated candidate, run local build and behavioral checks in isolated
test repos, and obtain bounded independent review against the agreed measures.
Use existing available model access; do not change accounts or buy capacity.

Protect installed Kerd, unrelated changes, live sessions and existing GitHub
branches. Do not actually clear or exit the user's live session during development.
Exercise session exit/restart in designated test sessions. A real GitHub-backed
handoff needs an identified test repo/branch and destination; those targets are
still to be established before external writes. Ask only for consequential
choices or missing authority, not routine implementation methods.

## Dependencies and unknowns — initial read-only discovery

Standard topic: What dependencies or important unknowns could affect the work?

Observed locally: Codex CLI 0.153.4, Claude Code 2.1.263, Git and tmux executables
are available. Availability is not proof of successful model authentication or
destination-machine readiness. No live model job was launched in this check.

Official OpenAI documentation and local `codex exec --help` describe fresh
non-interactive runs and a distinct resume path. Official Claude CLI guidance
and local help describe non-interactive `claude -p` runs and separate continuation
options. This supports investigating a small launcher that starts fresh runs from
saved state; it does not prove a skill can clear/restart its own interactive host
or avoid auto-compaction mid-job. No hooks, CI or global changes introduced.

Sources inspected for this scoped feasibility check:
- [OpenAI non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [OpenAI CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Claude CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Claude commands](https://code.claude.com/docs/en/commands)

Still to prove: safe run boundaries before context exhaustion, actual restoration
quality/footprint, honest usage accounting, job reconciliation and automatic
continuation with existing permissions. A manually restarted session does not
satisfy the autonomous-continuation criterion.

### Trial project selected: Seinn

The user selected “one of my projects, seinn”. Read-only checks located
`/Users/anthonymaley/development/product/seinn`, with origin
`git@github.com:anthonymaley/seinn.git`. The working tree was clean on main;
local HEAD and a fresh remote main lookup both returned
`19b7a98a778b88dedab52c91bd662e6ac4b7843d`. This is a point-in-time observation,
not authority to change main. No AGENTS.md or CLAUDE.md was found inside this repo
by the instruction-file search; task-relevant project records still need reading.

The measured current CONTEXT.md is 388,097 bytes and TODO.md 30,465 bytes: 418,562
bytes together before the newest daily session log. These are file sizes, not
token counts or an observed fresh-session context reading. Use them as a baseline
lead, not proof of actual pickup cost or successful reduction.

Use a separate clone and dedicated trial branch of Seinn; preserve its working
checkout, main and existing work. Selection authorizes this project as the test
target within the agreed isolated-test boundary, not arbitrary production writes.
Before a remote test branch is created/pushed, resolve its exact unused name and
recheck remote state. Destination checkout/access remains to be established for
the actual device test; do not invent an SSH host or claim local simulations prove
two-device continuity. No clone, branch or remote change was made in discovery.

Dependency treatment: investigate automatic host continuation and context-cost
measurement during design, then prove them in the trial. Neither tool availability
nor agreement to investigate is a successful test result.

## Completion and handoff — confirmed

Standard topic: What does finished mean, and who receives the result?

Deliver the redesigned Switch candidate and any minimal supporting launcher,
the user-friendly flow and usage instructions, and evidence against the agreed
continuity, cleanup and low-context criteria in this same work package. Include
independent assessment and the Seinn trial results with unsupported host/device
paths explicitly identified. No unsupported path is silently counted as passing.

The user receives a ready-to-use candidate and a concise demonstration of out,
in, to and Conductor Roll (freeze/thaw). Final user review is required before calling
the package complete. Replacing installed Kerd is a separate adoption decision,
not part of the isolated trial. A spec or manual restart workaround alone does
not meet the automatic-continuation outcome.

The user confirmed the finish line: “yeah we can call freeze/thaw 'Roll'”.
Use **Roll** as the product/action name from here; freeze and thaw describe its
save and restore behavior. This completes the ten-topic understanding, not the
implementation or agreement to unseen implementation choices.

## Integrated direction — agreed

The user answered “perfect” to the connected design, local Roll helper and
proposed 8,000-token / 5%-of-observable-usable-context pickup budget. This authorizes
the scoped build and proof sequence. It is not a passing result for any measure.

[Connected product view](direction.html) · [Design and build outline](design.md)

The direction preserves the four distinct actions and proposes a small local
helper for automatic Roll, outside the agent's context window. It introduces no
CI, custom hooks or hosted service. Initial proof is a helper-managed loop;
transition from arbitrary existing interactive sessions is still unproved and
must not be quietly substituted away.

Agreed pickup target: no more than 8,000 Switch-added input tokens and no more
than 5% of usable context when that capacity can be observed. Count instructions,
selected memory and pickup tool output separately from existing host overhead.
These numbers are now agreed trial targets, not vendor guidance or observed results.
Correct restoration remains required regardless of input size.

Build first proves fresh-run continuity, then lean In/Out on an isolated Seinn
clone, To/Roll integration and independent assessment. All artifacts remain here;
installed Kerd and Seinn's live checkout/main remain untouched.

Visual check: rendered the direction locally in isolated headless Chrome profiles
at 1280px and 700px widths. Inspected the complete desktop view and the reflowed
action sequences at narrow width; the narrow screenshot did not include the full
page below the proof heading. No diagram-label collisions were observed in the
inspected regions. This is visual QA, not functional proof or user agreement.

## Boundaries and agreement

Direction is agreed and candidate implementation is in progress. No installed skill,
global configuration, existing session marker or legacy boundary has been changed.
Reading Switch is reference inspection, not invocation of switch in/out.
Build direction, authority and the Seinn trial target are captured above.
Completion, implementation direction and numeric pickup budget are agreed.
Technical unknowns remain to be proved.
Trial resource limits are explicitly unset.
Voice remains parked outside the current candidate work.

## Now

Stage: Complete — producer accepted the supported candidate with stated limits.
The user selected this existing Switch work as the real-work Conductor trial.
All ten topics and the agreed direction carry forward; no new interview.

Completed: independent Roll continuity and cleanup assessment; returned laptop
artifact assessment; matched local pickup comparison; source-preserving
restoration correction and independent review. Final prepared local pickup used
5,518 estimated added input tokens, 3.15% context and 93 seconds, versus the old
local strategy's 32,825, 13.50% and 213 seconds. Both controls match; retained
meaning passes when display, annex and original authority prompt stay together.

Remaining limit: automated source discovery and whole synchronized-Git pickup
cost are unassessed. Source reading selections were prepared beforehand. No
universal history-recall, native-conversation transfer or arbitrary-host-exit
claim. The user opens the remote destination session.

The user answered “yes” to accepting this candidate with the stated limits.
[Acceptance and scope](completion.md#producer-acceptance) are recorded.
No question or build action remains within this accepted package. The broader
whole-pickup cost measure remains unassessed. Installation is a separate decision.

Read on pickup: this Now section; [four-action result and limits](completion.md);
[pickup evidence](pickup-budget/comparison/results.md). Read the agreement's
Success, Authority, Completion and Integrated direction above if a decision
needs its original wording. Prior observations and raw trials are supporting
history, not pending jobs.

No jobs remain active. Native comparison/repeat/control workers completed with
owned cleanup; Claude's review returned and its alias is closed. Raw private
records stay in /tmp/kerd-pickup-comparison.93NoWK/project Git metadata; useful
sanitized results/prompts are retained in the pack. Do not rerun the laptop trial.
Installed Kerd, live Seinn, global instructions, unrelated TODO edits and dated
history remain untouched. No commits, pushes or installations this continuation.

## Prior implementation observations

The observations below describe successive completed slices, not simultaneous
current blockers. For the active continuation use the Now section above.

Immediate position: **laptop artifacts assessed; focused Markdown correction
independently reviewed**. The actual submitted patch passed 31 tests but exposed
automatic URL/email links in supposedly inert cells. The corrected artifact passes
33 current tests and all 19 original tests; independent review found no remaining
M1–M4 blocker. [Artifact review and retained result](device-build/artifact-review.md).
Installed `kerd:switch` was loaded during pickup. The user confirmed that skill use
is appropriate: candidate-only version attribution is qualified, not a failed handoff.
The Studio worker saved to the dedicated Seinn trial branch at
6393778c4993405ffec17616ab3950821e9d7795 and exited with its owned children.
Only docs/work/switch-trial/device-build/ changed. The laptop was reported clean
at the preceding 2302c2a checkpoint. [Exact pickup and current proof](device-build/results.md).
The original patch is preserved. The corrected result is in this pack only;
neither the laptop nor released source branch was advanced. Laptop execution is
reported; the returned artifact and correction were independently tested on Studio.
Current candidate
Switch tests: 190 in both pack and isolated mirror; bounded lifecycle review passed.
This closes the pending artifact review for the active-work trial. Automatic remote
startup/result transport and pickup context cost remain unproved. No routine user
action is pending; live rollout is separate from this bounded trial.

Stage: Deliver — managed Roll and Seinn memory/Git trials produced real results.
Latest: the actual live Conductor command connection completed a local To trial,
including failed-save recovery and immediate fresh-destination continuation.
The resulting machine-readable preview has 19 passing artifact tests.
Claude independently found no blockers and closed its original-test evidence gap
after a focused follow-up. The unchanged earlier 13 tests also pass against the
new result. The actual source/destination prompts and both reviews are retained.
[Live connection evidence and prompts](live-control/results.md).
Confirmed topics: all ten, including Completion and the name Roll.
Success qualification: agreed pickup target is 8,000 additional tokens and 5% of
observable usable context; exact measurement must be disclosed, not invented.
Current result: prepared local pickup passed the scoped check on the pinned Seinn
trial snapshot. Its final native reader used an estimated 5,249 added input tokens
and 3.38% context; independent Claude assessment found no blocking restoration
issue. Earlier discovery runs missed, and two short answers
omitted useful constraints. All variants remain in [pickup results](pickup-budget/results.md).
The managed Codex Roll proof is complete. Full Switch remains in Deliver,
not accepted/installed. Latest result: [active local handoff](active-handoff/results.md)
saved unfinished work before owned-source shutdown, then a distinct fresh worker
finished the preview tool in the destination checkout. Ten artifact tests pass;
independent Claude artifact review found no blocker. Driver-review limits and
later unit-tested corrections are recorded separately. No GitHub/device or
interactive-host exit was performed. The subsequent [failed-save trial](failed-save/results.md)
now proves a deliberately failed local push keeps the same managed source alive,
blocks the destination, then recovers and finishes in a fresh destination.
Claude artifact review found no blockers; 13 tests pass after its small test/doc
gap was corrected. No routine user action is pending for these bounded checks.
Pending user action: none for the bounded laptop pickup; its result was supplied
2026-09-07 and supports successful second-device memory restoration. Do not
repeat that check or connect to guessed hosts.
Current results: two real builds (Codex and Claude), each across three fresh
sessions without human next messages; 13 and 34 artifact tests passed respectively.
Independent Claude review found no blocker in the inspected Codex deliverable.
Those earlier success runs used preset piece boundaries and predate subsequent
lifecycle corrections. They are not proof of observed context-pressure Roll.
Current build and regression evidence: [Conductor + Roll](conductor-roll-proof.md).

Seinn trial: source cleanup independently reviewed; twelve selected restoration
answers matched the source check. Five named memory files committed/pushed only
to kerd-switch-trial-20260906 (ef4dc42f13630c76da2ad2c1eaf43509e210e862). A second
local clone fetched that GitHub branch and restored identical current files.
Live Seinn/main and installed Kerd remain untouched. Candidate Switch was updated
in the work pack and synchronized only to the isolated candidate clone.

Evidence: [Roll proof](roll-proof.md), [artifact review](roll-artifact-review.md),
[Seinn proof and limits](seinn-proof.md). Current context entrypoint is 7,156 bytes,
not a measured token-cost pass. Final source corrections postdate the selected
fresh-reader run; this was not a whole-history preservation audit.

Implemented and locally proved: turn completion is separate from managed-source
release. The reusable held-source adapter and ManagedTo helper preserve the source
across a failed save; recovery of the same checkpoint then admits a fresh destination.
Independent lifecycle review found two issues, both corrected and rechecked.
The first native attempt failed on malformed JSON and remains recorded, not hidden.
Latest slice: [To entry and exact pickup](to-entry/results.md) distinguishes a
same-session console change, a live managed source and an ordinary interactive
source. Three independent disposable behavior checks matched those boundaries.
Destination pickup now checks the supplied saved Git revision before updating
working files; a regression reproduced and corrected the previous late refusal.
The live managed connection is now built: Conductor retains the running command's
input/output handle and sends To/retry to that same owner. The native source
checkpoints, remains held through failed publication, then exits only after save
verification. Conductor starts the prepared destination without another user turn.
Independent lifecycle review returned four findings, all corrected and rechecked.
An existing interactive-host takeover, remote destination startup and an
end-to-end active-build two-device run remain unproved. Whole-pickup cost beyond a
caller-prepared reader also remains open. The supplied laptop result establishes bounded
memory restoration, not automatic source release or active-build transfer.
No guessed SSH targets or automatic exit of a live user session. A managed Codex
context-observation route now completed a useful build through two fresh workers
and one automatic continuation, with no manual cleanup in the final run. Both
context-triggered saves and owned-process shutdowns succeeded. All 13 output
tests passed; independent Claude assessment found no blockers. Candidate Switch
has 186 passing tests in both the pack and synchronized isolated candidate mirror.
Both skill validations pass. The reviewed
readable status tool and optional source-assembly helper are included.
Earlier failed attempts remain in the proof record. This does not prove two
pressure-driven transitions, prevention of every native compaction, or takeover
of an existing interactive host. The local prepared-reader measurement excludes
Conductor's source-selection cost; automatic discovery and a full GitHub pickup
are not certified by its numerical result.
No further laptop action or generic permission prompt is needed for this proof.
Do not replay settled experience, success or resource-limit answers.

Latest visual QA: the live connection and its retry/continuation flow were rendered
at 1280×3900 and 700×7800 and inspected. The narrow view stacks the sequences;
no overlapping boxes or clipped labels were observed. This is static rendering,
not a mobile-device interaction trial.

Previous visual QA: the entry choices, then-current integration gap and existing flows
were rendered at 1280×3400 and 700×7000 and visually inspected. The narrow layout
stacks the cards and sequences without observed clipping or overlapping labels.

Previous visual QA: the updated failed-save recovery flow and truthful managed-source
limits were rendered at 1280×3200 and 700×6600 and visually inspected. The narrow
flow stacks vertically; no clipped boxes or overlapping labels were observed.
This is static browser rendering, not an interactive device trial.

Previous visual QA: the Deliver-stage view, including the prepared-pickup flow,
active local handoff result and explicit failed-save limitation, was rendered
at 1280×2600 and 700×5700. Both full-page
renders were inspected; the narrow flow reflows vertically, and no clipping or
label collisions were observed. This is visual inspection, not an interactive
mobile-device test. The isolated headless browsers were stopped after rendering.

## Studio → laptop preparation — 2026-09-06 23:13 UTC

User agreed to Studio → laptop. Local machine identification returned Anthony’s
Mac Studio. The dedicated Seinn trial clone was clean and its only recorded model
job was completed. Added only docs/work/switch-trial/device-handoff.md, committed
as 1d382a4f268ee21e994b05a94cbbbcc08c9a33c7 and verified the GitHub branch at that
revision. No source-session exit occurred; the Studio trial branch is now paused
pending the laptop result. Installed Kerd, live Seinn and main remain untouched.

The laptop uses a fresh local model session and a new isolated clone, not SSH/tmux
executing on Studio. It reads the saved handoff and current context, checks actual
machine/revision, and reports the restored place within read-only authority. No
new product task, deployment, message or boundary is authorized. The expected
deliverable is the pickup result, not another question about starting the trial.

[Published laptop handoff](https://github.com/anthonymaley/seinn/blob/1d382a4f268ee21e994b05a94cbbbcc08c9a33c7/docs/work/switch-trial/device-handoff.md).
Automatic source exit, active-work transfer and low-context measurement remain
open; a user-operated second-device check will not silently pass those measures.

## Reported laptop attempt and correction

The laptop session reported local 19b7a98, found no trial record, substituted
legacy readiness checks and builds, then claimed a handoff pass. The intended
trial was not entered. Operational findings remain user-reported, not validated
by this Kerd session. No new Switch or automatic To pass is recorded.

Following the user's acknowledgement, the candidate was narrowly corrected:
resolve an explicitly named handoff before ordinary pickup; missing/wrong means
stop, not fallback. Destination startup carries the location and read-only scope.
Helper tests now total 39 passing. An independent missing-record forward test
stopped without running the available fixture readiness script or changing files.
See [correction evidence](pickup-correction.md). Installed Kerd remains unchanged.
The retry handoff is published and remote-verified at
2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83 on the same dedicated trial branch.
Studio trial writes pause again pending the laptop result; source exit remains false.

## Laptop retry returned — recorded 2026-09-07 12:01 UTC

The supplied result reports local MacBook Pro execution, the intended isolated
checkout /Users/anthonymaley/seinn-test, trial branch and exact prepared revision
2302c2a, clean state and matching live remote. It restored the saved position,
unresolved decision and permissions correctly, with no reported operational probes
or builds. Bounded second-device memory restoration is supported by this evidence;
this controller did not independently inspect the laptop's commands.

The source session remained open, no active Seinn build existed to move, and the
model correctly reported token budget unassessed. Those separate measures remain
open. Setup's .remember/ exclusion question was unnecessary and based on an
initially incorrect claim, later corrected; no exclusion change was reported.
Do not repeat this read-only trial. [Detailed result and limits](seinn-proof.md).
