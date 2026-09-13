# Compact arrival and coordinated closeout

## Now

Outcome: a recognizable Switch In dashboard and a handoff that preserves
collaborating sessions' necessary context without duplicate shared-file saves.

Stage: 0.119.0 released 14:40 by Codex (TEAM, arrival notice, YOU recommendation;
record `docs/work/switch-arrival-team/work.md`), after 0.118.0 (13:03) and
0.117.0 (12:40). Rows 3 and 4 carry results from this sitting; rows 1 and 2
carry the 0.118.0 arrival observation, with Anthony's assessment given through
Codex rather than as a reply.
Current activity: Out saved by the Claude session holding `kerd-b5-review`,
which designates its successor after the save.
Pending question: none.
Next action: a fresh Claude session verifies it loaded 0.119.0 (Anthony restarts
Claude), runs Switch In with the planned adoption and its first live arrival
notice, and shows the 0.119.0 arrival for Anthony's assessment; results on rows
1, 2 and 4. Unplanned recovery is observed only if a role-holding session is
actually lost later. Consumer pickups stay deferred until items 1–5 carry
evidence of the fixes working. No installation is authorized.

Source boundary: branch `main`, subject `Release Kerd 0.119.0: visible team and recommended next action`;
this Out's rows and account are saved in the boundary commit that follows it.

Agreement: Anthony approved the compact example: completion box with PROJECT,
PHASE, TASK, STATE; LAST/THIS SESSION; NOW; essential attention; separate YOU;
document links; END OF PICKUP · SESSION READY. Colour is optional. He then
approved one coordinated Out, with contributors' decisions, evidence limits and
unfinished work preserved without either old conversation remaining open. His
final instruction was to obtain Claude's review, especially of Out, implement
and release. No installation refresh or consumer-project edits are authorized.
Anthony then added defining and retaining ongoing roles during Agent. These use
the existing private pairing records, not a tracked session-ID roster.

Earlier 0.115.0 boundary: branch main, subject
`Release Kerd 0.115.0: compact arrival and coordinated closeout`.
That save preceded the 0.116.0 work above; resolve its revision with Git.

## Targeted verification of reported failures (2026-09-13)

Anthony, 10:41–10:50 EDT: "no point picking up projects when Kerd isn't working
as it should, prove that first." Codex's account of the reported failures (from
Anthony's supplied outputs, not watched terminals) and its three corrections to
Claude's plan are accepted: the consumer-pickup question is deferred, not pending;
existing ordinary-use evidence is the baseline, not repeated; a build delegates
when useful and never manufactures subagent work. Agreed division: Claude owns
arrival and closeout checks; Codex verifies the installed Codex version, checks
pairing state and sends the successor a real request. Before any clear, both
contributions are preserved and the handoff confirmed ready. Fixtures passing and
0.116.0 shipping establish none of this. One list, one owner, evidence and the
remaining gap per item; results are appended here by the owner.

| # | Reported failure | Check on 0.116.0, in Kerd | Owner | Evidence baseline | Remaining gap |
|---|---|---|---|---|---|
| 1 | Arrival reply bound to the wrong thing: Leru 0.112.0 In promised design would start on a yes/no; Kerd 0.115.0 In (09:40) said "naming the project is what starts it" | Fresh Claude session after a clear; first verify which skill path and version actually loaded (0.116.0 is in the cache on disk, `plugin.json` 0.116.0; presence does not establish what loads). Switch In, then reply "not now" to its one pending question: nothing starts, nothing shown as owed. The project-name and factual Yes/No/Not sure replies each need their own genuine pending question; Kerd's arrival carries neither, so they stay with the deferred Codex pickup and the clarification scenario in `docs/work/codex-plugin/work.md`. | Claude (fresh session) | Anthony's supplied Leru and Kerd outputs, held by Codex | Needs Anthony to clear and open the session; he reads one reply. Only the "not now" case is exercised here. **Result 2026-09-13 13:52, Claude (0.118.0 cache, base path and `plugin.json` read 0.118.0):** fresh Claude session after a restart; Switch In asked once, after END OF PICKUP, "Can you assess this 0.118.0 arrival now?", with a REPLY line "Your verdict / Not now". Anthony did not answer that question in the Claude window; nothing started on the unanswered question, and the session did only peer-requested read-only reviews until his 14:31 release direction. His assessment reached Claude through Codex instead (numbered NOW and the question after END visible; pairing buried in ATTENTION), leading to 0.119.0. The "not now" reply itself remains unexercised; record it when a real reply occurs, don't stage one |
| 2 | Human-owned check presented as agent work: Seinn 0.115.0 In asked "Starting on the couch verdict — approve?" | The same fresh In: the saved next action includes Anthony's own assessment of the arrival, so TASK/STATE name him as actor and YOU asks whether he can give it, not "Starting on X" | Claude (fresh session) | Anthony's supplied Seinn output | Kerd has no device; the assessment stands in for the couch verdict. **Result 2026-09-13 13:52, Claude:** the Kerd 0.118.0 arrival named Anthony as actor (TASK "Anthony assesses this 0.118.0 arrival", STATE "Awaiting Anthony's assessment") and asked whether he could assess it, not "Starting on X" (observed in the rendered output). Anthony's verdict on that framing was not given directly; his Seinn 0.118.0 YOU box, supplied to Codex, was too dense with a confusing REPLY menu, leading to 0.119.0's one recommended action and one direct question. The next check is his assessment of a 0.119.0 arrival |
| 3 | Coordinated Out lost a contributor: Leru Out/In had no Codex log and conflicting TV claims, reconstructed not resolved | This session runs Out as owner: loaded skill is the 0.115.0 cache, guide followed is the released 0.116.0 `in-out.md` from the repository (a disclosed test route, not an installed-0.116.0 result); Codex's returned account captured once; MEMORY row shown; the fresh In (item 1) recovers both accounts without either old conversation | Claude (this session, owner); Codex returns its account | `kivna/sessions/2026-09-13.md` (one contributor, already saved) | Unresolved facts stay unresolved in the record, never reconstructed into proof. **Result 2026-09-13 15:31, Claude as Out owner on the installed 0.118.0 cache:** the role-ownership check matched (this session's verified ID is the `kerd-b5-review` binding); the contribution checkpoint requested Codex's delta since the 14:40 release through Agent and retrieved "none", with Codex's release account already in `docs/work/switch-arrival-team/work.md`. First run of both on an installed release. The fresh In recovering both accounts without either old conversation is still to be observed |
| 4 | Role not recoverable when the session ID changes (pairing showed a stale title; ordinary `pair` refused a new ID) | After the Out save, this session (bound as `kerd-b5-review`, which has no `partner_role`, no ownership flag and no `handoff`; role preservation cannot be claimed for a field that is absent) runs `handoff --record CONTEXT.md` with the released helper `skills/agent/scripts/agent.py`, not the 0.115.0 cache helper, which lacks the command; the designation is verified against the final saved pointer before Anthony clears; the new session's In records the actual identity before and after, then `adopt --expected-session <old> --record CONTEXT.md`; Codex checks the binding and sends the successor one real request that arrives | Claude designates and adopts; Codex verifies and routes | Fixture tests and one native self-ID read (Agent 135) | Compare the actual identity before and after the clear; never infer it. A safe refusal on unknown or conflicting identity is a successful safety observation, not successful role continuation. **Result 2026-09-13, Claude:** planned adoption met on 0.118.0: at 13:52 `identity` matched this session, `adopt --expected-session <bound ID> --record CONTEXT.md` consumed the 12:43 designation against the unchanged saved record, kept the role and wrote a recovery receipt retiring the predecessor. Messaging proof met: seven real Codex requests (13:58–14:40) targeted the adopted binding's ID and all replies were retrieved (request records, `reply-received`); Codex reports resolving the established alias to the new binding. Unplanned restart recovery remains unobserved |
| 5 | Installed Codex snapshot reported stale since 2026-09-12 | Read the installed version before any Codex-side result is counted | Codex | Earlier 2026-09-13 read found installed/enabled 0.113.0, corroborated by its cache manifest; no update at that check | **Update 2026-09-13, Codex:** Anthony subsequently authorized the user-level update (“lets do that too”). Built `output/kerd-codex-0.116.0`, repointed only `kerd-core` via the CLI and reinstalled Kerd. `codex plugin list --marketplace kerd-core --json` now reports installed/enabled 0.116.0; the cached manifest agrees and all four core skill entries exist. Old 0.113.0 catalog retained. Installed-version check met; a fresh session loading it and its behavior remain unverified. No consumer pickup started. **13:05, Codex, for 0.118.0:** Anthony's "ask codex to do plugin on codex too" was relayed by Claude's Agent request; Codex held it pending his direct confirmation in its own window (the earlier authorization covered 0.116.0). Read-only: CLI and cached manifest report 0.116.0 installed and enabled; marketplace still points at the 0.116.0 build; nothing changed. **Then, Codex (reported 13:30):** after Anthony's direct "go ahead" in its window, built `output/kerd-codex-0.118.0` from the release commit and re-registered only `kerd-core`; `codex plugin list --marketplace kerd-core --json` reports installed/enabled 0.118.0, the cached manifest agrees and generated and cached skills match. 0.116.0 build retained. Installed-version check met for 0.118.0; a fresh Codex session loading it remains unverified |
| 6 | Implementation never delegated (Anthony: not seen in a long time; Codex: reviews only, today) | Judged at the next real build where a split is useful; the check is the decision and visible ownership, including an inline choice with its reason. Not a prerequisite for items 1–5. The Backlog's Agent four-limits work is a candidate, and a separate scope decision for Anthony | Claude (Conductor) when a build runs | Four hypothetical choices reviewed 2026-09-13 | No real build in this verification |
| 7 | Consumer pickups (Codex in a work project; Seinn, Leru) | Deferred until items 1–5 carry evidence of the fixes working, not merely a recorded outcome; failed or unresolved checks stay visible here and keep the hold | — | — | Anthony's instruction, 10:41 |

### Local arrival refinements after 0.116.0

Anthony requested the actual dashboard question as the first content after END,
and NOW as numbered next actions in priority order instead of a report of evidence
rows. Markdown now places the question below automatically; YOU retains scope,
proposal and reply guidance. No question means stop at END. Terminal output keeps
the explicit question-below option. Both modes enumerate supplied NOW order;
the composing skill selects actionable priority from the saved plan, not the
renderer. Completed observations and deferred work are not next actions.

Tests first failed on the old placement and bullets, then the renderer suite
passed 116 tests, including complete values, no duplicate question, no-question
output and multi-digit numbering. Full Switch suite 325, packaging 9, both skill
validators and release gate passed. Local
changes only: no new version, commit, publication or installed-plugin update.

Codex checked the successor binding: previous ID matches the outgoing Claude,
role retained, designation consumed. The subsequent real review submission was
refused before delivery: exact bound session not reachable. Native discovery
lists a different, unpaired Claude session. No substitution, resume, role edit or
retry occurred. Row 4's messaging proof and independent review remain open;
the cause of the later identity difference is unverified. Review prompt and
routing metadata remain private.

Follow-up: Anthony explicitly selected the listed Claude session. Codex created
a separate contact alias without overwriting the designated role, sent the review
and retrieved its complete reply. Claude (observed `claude-opus-5`; native effort
unchanged/unobserved) ran renderer 116 and Switch 325 successfully, accepted the
renderer and found two live guidance contradictions about question placement
and status bullets in NOW. Those are corrected locally. This manually selected
contact is not a successful automatic-succession result.

### Lost successor and another restart

Anthony then explained: “i lost the claude session and had to restart”. The
binding shows the first adoption consumed its designation and retained the role;
the next native session had a different identity and nothing left to adopt.
That explains why a single Out/In fixture was insufficient. No claim is made
about what unsaved memory the lost session held.

Agreed work: recover established-role continuity after restart, without selecting
a teammate again or guessing from the only visible session. Codex implements;
the selected Claude partner reviews read-only. No release, install, lifecycle
operation or consumer-repo change is part of this correction. Recovery evidence
belongs in the existing private Agent binding, not a second Markdown roster.
Tests must cover a second restart, unchanged alias/role, stale expected IDs,
changed saved memory, a still-listed predecessor, unavailable native evidence,
revocation and no rerouting of old requests. Pairing recovery is not memory
completeness or authority to start work.

Implemented in the existing binding: record-based adoption consumes the one-use
designation but retains a restart receipt for the same saved path/digest and
holder. Claude recovery checks verified self, matching machine fingerprint,
unfiltered native listing with current present/predecessor absent, retired IDs
and the expected-old-ID lock. It retains the alias/role and old request targets.
New Out, cancellation or explicit replacement supersedes the receipt. Switch In
recognizes the receipt, shows pairing and exposes specific refusal reasons.
Codex new-ID unplanned recovery refuses because saved threads do not establish
terminal absence. Same-ID continuation and planned handoffs remain supported.

Claude design review caught cross-machine and resumed-predecessor risks; both
became guards and tests. Its suggested one-recovery cap was declined: repeatedly
asking for the same teammate after a restart recreates the reported failure.
Retired IDs prevent automatic reclaim across the recovery chain instead; Claude
accepted that disposition in implementation review. That review also reproduced
an unintended dependency of planned handoffs on the OS fingerprint. Fixed:
Out does not need it; designated adoption captures it best-effort, and only
unplanned recovery requires a valid match. Final read-only review returned ready
and reran the failing reproduction successfully.

Verification: Agent **143**, including **20** succession cases; Switch **325**;
packaging **9**; Agent/Switch/Conductor skill validators pass; release gate clean;
audit retains its pre-existing requirements trace finding; diff check clean.
In-memory mutations disabling predecessor, host, retired-ID and digest checks
each failed tests. Removing the planned-handoff fallback also failed its new
test. The native macOS fingerprint read succeeded without exposing its value.
Initial full Agent run exposed fixture ResourceWarnings for SQLite; the clean
rerun suppressed only that warning category, not errors. An initial packaging
command used a nonexistent root path; the actual packaging suite above was
then located and run. Reviews used observed `claude-opus-5`, native effort
unchanged/unobserved, profile `opus-5` version `2026-09`.

Limits: real restart recovery and the user's experience are unobserved, so row 4
is not closed. Native absence is observational; another same-machine session
restoring the identical account can be indistinguishable from the intended
successor. Guidance limits adoption to that role's pickup. Missing or changed
memory is never repaired by routing. Legacy consumed designations have no
receipt to reconstruct; explicit replacement remains necessary for those.
The reviewer noted a non-blocking extra host read while writing the recovery
receipt: a transient failure after the first successful check can disable the
next automatic recovery; the null host is explicit and fails closed.
No live binding changes, lifecycle operations, commit, release or installation
were performed for this correction. The earlier authorized Codex installation
result remains in row 5; it does not include these local changes.

### 0.117.0 release checks

Released 2026-09-13 after Anthony's 12:35 EDT "okay lets release and i'll try",
from the Claude reviewer session; the tree had been still since 11:44. Run
there before the save: Agent 143, Conductor 37, Switch 325, hooks 21; gate
selftest, audit (the pre-existing trace finding only), release, progress,
matrix, journey and stale checks all clean; diff check clean. The packaging
suite was not rerun there. CI had been red since the two session-close pushes
on `fidelity.py`: four new artifacts were named nowhere a pickup reads. This
release names them in `CONTEXT.md`. The legacy `kerd-b5-review` binding has no
restart receipt, so automatic recovery starts only after a new Out designation
and a record-based adoption. CI on the release commit succeeded (run 34769275129).

Before Out, at Codex's advice relayed by Anthony (12:42): the reviewer session
verified its identity and explicitly adopted `kerd-b5-review` with
`--confirm-replacement` against the lost successor's ID, using the repository's
0.117.0 helper. The role was kept and the lost session recorded as `previous`;
no receipt or designation was written, as expected for explicit replacement.
The contact alias `kerd-83-review` stays as it was. Out (12:43) then saves the
account and designates the successor against the final `CONTEXT.md`.

### Out pre-save role ownership check — local, unreleased

On Anthony's "do we need to add this to switch out?" and "lets add that" (as
reported by Codex), Codex added a pre-save check to Out: verify this owner's
identity against the intended existing role before editing the pointer; same ID
keeps it; an explicit replacement choice already given is reused; Out alone
grants no role; no binding means no setup stop; designation follows the final
save and is reported separately from Git and memory. Files: `README.md`,
`skills/agent/references/session-succession.md`, `skills/switch/SKILL.md`,
`skills/switch/references/in-out.md`, one sequence test in
`skills/agent/scripts/tests/test_agent.py`; no runtime script. Codex reports
succession 21, packaging 9, skill validator and release gate passing. Claude's
read-only review (12:47, Agent suite run) returned ready with two wording fixes:
the unresolved-role question goes in the closing next action after the save, not
as a stop before it; the closing JSON has no designation field, so say it goes in
`next` or add one. Codex made both by 12:50 (safe memory saving proceeds with
the unresolved pairing choice in the closing next action; designation status
goes in the existing `next` text, no new field), confirmed by Claude's reading;
Codex reports Agent 144, packaging 9, Switch validator, release gate and diff
check passing; its full Switch regression later finished at 325.

Then, on Anthony's "i had to ask you both if it happended" and "lets add it and
do it so we can actually test this" (as quoted by Codex), Codex added a
**contribution checkpoint** to Out in the same local files (`in-out.md`, Switch
`SKILL.md` description, `README.md`): the owner identifies contributors, reuses
captured accounts, requests only a missing delta through Agent and retrieves it
before drafting; a known pending job is covered by its owner, state and result
location; an unavailable participant is a recorded residual gap when other
evidence restores the rest; a necessary delta after saving reopens the account
and needs re-designation. Codex reports renderer 116, packaging 9, Switch
validator, release gate and diff check passing. First real use, this Out,
12:53–12:56: collection ran before drafting and requested one delta; result
"missing: none", with the lost 11:11 session carried as a non-blocking gap
(session log, newest sitting). Tests cover mechanics and the example, not model
compliance; one observed run is not acceptance. Also observed: a
contributor's uncommitted edits during a
coordinated Out block `handoff.py save`, leaving only the manual fallback.
Both changes released together in 0.118.0 on Anthony's 13:00 "yes". Checks run
by Claude before that save: Agent 144, Conductor 37, Switch 325, packaging 9
(`docs/work/model-ready-work/packaging/test_build.py`), hooks 21, every CI gate
step clean except `fidelity.py`, which found `skills/conductor/references/journey.md`
(changed in 0.117.0) unnamed; the release names it in `CONTEXT.md`. Anthony also
asked for Codex's plugin to be updated ("ask codex to do plugin on codex too");
requested from Codex by Agent after the save, result on row 5.

## Implementation and checks

Switch's existing renderer uses the approved compact chat shape. Optional
`project` identifies the already-restored project; unknown stays not recorded.
Values wrap rather than truncate; brief summaries are composed from context
already loaded. Completion follows `restored`, not the absence of warnings.
Partial and unknown restoration end explicitly incomplete or unconfirmed. The
one plain question can follow the marker only when the host requires it outside
YOU. Out's existing presentation is otherwise retained.

The Out owner reuses saved contributions, requests only material missing detail
through Agent, and preserves its scope and evidence limits. Other contributors
do not rewrite the shared handoff. No new inbox, tracker or session sweep.
`handoff_ready` is the owner's boolean memory-coverage assessment, distinct from
the helper's Git result; missing/false does not offer to clear context, and a
true value still requires a confirmed save. This is not machine proof that a
model preserved every fact.

Renderer suite: 112 tests pass at draft stage. Updated tests check the new
layout rather than retaining the superseded loose Markdown expectations. New
checks cover box width/order, warning-independent completion, safe fences and
the cross-product of save states and memory readiness. No end-user appearance
or token-savings acceptance is claimed.

## Independent review

The established Claude partner reviewed through Agent with source edits held.
Profile: Claude Fable 5.1, version 2026-09; retained native settings, observed
claude-fable-5-1, effort unobserved. Four guidance findings were addressed:
person-designated ownership (including two Out requests), exclusive shared-file
writes, branch/worktree contributions and unknown standalone contributors.
Readiness unassessed no longer claims context missing. The reviewer verified
the corrections and found no remaining consequential Out defect. Its final
fresh-disk-read reminder was also added.

Two synthetic scenarios were walked, not executed as live closeouts. A complete
read-only review account with an unresolved device claim can yield ready memory
once the claim, limits, branch location and next action are preserved. Two Out
owners with a conversation-only decision must resolve ownership before shared
writes, and cannot mark memory ready while that necessary decision is unsaved.
This is reasoning evidence, not proof that every host follows the skill.

Full Switch 321 and renderer 112 pass. Packaging 9 and skill validation pass;
release check clean, audit retains the existing requirements trace finding.
Final release checks also pass: Conductor 37, hooks 21 (shellcheck unavailable),
gate selftest 57/root resolution 7, progress selftest/current render, matrix
selftest/audit and journey schema. Source publication, not installation, is
authorized. Git and CI results are checked after saving this named boundary.

## Ongoing Agent roles

`pair` and `start --kind partner` accept `--partner-role`, separate from the
existing per-job `--role`. An explicit update changes only that role on the same
alias/provider/ID; omission preserves it. It remains in private Git metadata,
including uncertain launches, and is returned by session discovery. No native
role setting, permission change, dispatch-on-pair, public roster or automatic
Out ownership. An unavailable target cannot be re-paired just to change its role.

Agent 123 tests pass, including three new cases for private persistence/update,
invalid/worker role refusal before effects and uncertain-launch retention. The
successful Claude launch test also proves persistent role versus first-job role
separation. Existing SQLite ResourceWarnings remain. Claude independently
reviewed every private-binding write and ran the Agent suite: release-ready,
no consequential defect. Optional role null versus absent was noted as a
cosmetic difference; both mean not defined. No live pairing or launch was
performed for the tests, and no role-based routing beyond the recorded alias
is claimed. Both review replies were retrieved and assessed by Codex.

## 0.115.0 ordinary-use follow-up (2026-09-13)

Anthony approved the narrow follow-up after two Claude arrivals, then asked
whether established Agent pairing could continue through In. The source release
above is complete; this follow-up is local and uncommitted, not a new release.

Conductor now binds an answer to the question actually asked. A target name
alone supplies a fact; a deferral starts nothing; an explicit scoped instruction
can supply both target and approval without another stop. Human-owned checks
name the human actor and specific check, retaining per-occasion permission
without presenting the check as an agent operation.

Switch In reads existing current-project binding metadata from Git's own
resolved private path and retains Agent as the route for later contributions.
The full skill is loaded on contribution, not every pickup. No peer probe,
dispatch, resume, replacement, transcript read or setup question on an unpaired
project. Saved availability stays unknown; multiple bindings do not silently
choose a partner. Roles are not modes or authorization. No new store or schema.

Clipping diagnosis: inspected only the two relevant native session logs, outside
the consumer worktrees. Kerd's renderer result and final assistant event both
contain the complete snapshot warning, parked-marker warning, Insight and source
line; Seinn's also retain the long NOW item, playback restriction and source line.
The pasted reports lose fragments present in both stages. The loss is downstream
of the stored final text; client rendering versus copying remains unestablished.
No renderer source fix is supported. A CLI regression checks complete long
values at widths 40, 64 and 100. Switch suite: 322 passed; release gate clean;
Switch and Conductor skill validators passed. Conductor 37 and packaging 9
passed; audit retains its pre-existing requirements trace finding. The first
packaging invocation named a nonexistent tests subdirectory; rerunning from
the actual packaging directory passed. No token or visual UX pass claimed.

Review exercises returned and retrieved: independent replies to a project
name, “not now”, and explicit scoped installation/pickup approval; human device
check availability versus agreement; paired and unpaired pickup followed by a
read-only contribution request. Judge the response and intended actions, not a
wording-match test. These are synthetic model exercises, not live installs or
consumer session changes. Anthony selected the new live Claude after the old
partner was no longer listed. A new private review alias was created without
rewriting the old binding. Claude Fable 5.1 (observed; native effort retained,
unobserved; profile 2026-09) reviewed read-only and ran Switch 322, Conductor 37
and Agent 123, all passing. It found no blocking code defect and recommended
deferring Agent's 8,074-byte skill load until a contribution is requested;
that correction is applied. Its Git-worktree scope and Switch body reminders
are also applied. Its simulated deferral left STATE awaiting; the instruction
now explicitly removes the implication that an answer is owed now.

### Session identity succession — proposed, not built

Anthony agreed to compare actual IDs, not infer identity from clearing or
restarting the terminal. Claude can read `CLAUDE_CODE_SESSION_ID` in a current
Bash tool call, and the reviewer verified it against native discovery. Codex's
`CODEX_THREAD_ID` was present here and matched a current-project native store
row; this is local evidence, not a universal host guarantee. Claude's
[environment documentation](https://code.claude.com/docs/en/env-vars) explicitly
says its tool-process session ID updates on `/clear`; retained MCP process IDs
can be stale. No real session was cleared or restarted for these checks.

Proposed shape: keep the existing private alias/role stable; Out records the
verified current owner and named handoff, never a guessed future ID. In keeps
an unchanged ID or binds a verified successor only with role-takeover authority.
Same project, title or latest activity is not that authority. Ambiguity asks a
real choice, not a guess. Prefer one atomic binding update conditional on the
expected old ID over accumulating aliases and a two-file successor chain.
Retain prior identity for recovery, preserve the role, never copy owned-launch
privileges to an external successor, and leave old request destinations/replies
unchanged. No Markdown ID roster, new inbox, hooks or automatic peer launch.
This differs from Claude's first new-alias suggestion and is sent for a narrow
design reassessment before any ID-replacement implementation.

Reassessment returned and retrieved: Claude verified the local correction set
with no remaining consequential finding and agreed that a single locked,
atomic binding replacement is smaller than its proposed two-alias chain.
Required implementation checks: same-ID byte-preserving no-op; stale expected
old ID refusal; exactly one winning concurrent replacement; wrong provider,
wrong project and uncorroborated self-ID refusal; preserved role unless explicitly
changed; old request/reply destinations unchanged. Existing owned-launch partners
are excluded from external replacement rather than inheriting launch privileges.
Codex validation must use its actual native-store/TUI rules, not claim every
eligible thread is live-listed or attended. Unknown self-ID is unresolved, not
permission to choose the latest session. No automatic new binding on discovery.

A new ID requires a designated role handoff or the person's explicit selection.
Out must not declare the process exited; a fresh same-project session alone is
not its successor. The stable role's private handoff can carry prior designation
so ordinary authorized continuation does not ask again. Both reviewers distinguish
verified identity from authority to take over. This remains design evidence,
not a tested replacement implementation. The earlier local arrival changes are
reviewed and ready to include in a later authorized release; versions untouched.

### Implementation commissioned

Anthony said “lets do it” after the reviewed succession design. The existing
Agent helper now has `identity`, `handoff` and `adopt`. `identity` corroborates
the actual host ID without writing; `handoff` prepares or cancels only the
currently bound session's continuation after its final record is saved;
`adopt` is a same-ID no-op or a locked expected-old-ID replacement. Automatic
adoption binds the relative handoff path and its saved bytes; changed content
refuses. Explicit user selection is a separate flag, never inferred authority.
One previous identity is retained in the binding, without an alias chain or
launch settings; owned partners cannot be externally replaced.

Switch links one short conditional succession guide. Its private routing update
is explicitly separate from project work at In. The full Agent skill remains
deferred until a contribution. No private handoff was prepared and no real ID
was replaced during implementation. A read-only Codex identity command matched
this host's native project record; simulated identity tests cover both providers.
Existing SQLite fixture ResourceWarnings remain; the repeat suite run filters
those warnings only, not test failures.

Claude independently reran all 135 Agent tests and read the implementation.
No code defect found; corrected the guide's intended-pickup enforcement claim,
same-ID outstanding designation handling, conditional guide loading, saved
pointer convention and unsupported Codex-host limit. Claude's follow-up reran
135 tests and returned ready for local handoff, no consequential finding.
Claude also corroborated its own native identity read-only. Neither provider's
live binding was replaced. A real clear/restart and role continuation is still
unobserved; tests are not that experience verdict.

Codex strengthened the racing test after an in-memory mutation exposed a weak
fixture: consuming the prepared designation could refuse the loser even without
the expected-ID check. Both competitors now use explicit selection, isolating
the expected-ID guard. Removing that guard fails one test; removing the handoff
match guard fails one test. Restored production passes all 12 succession tests
and all 135 Agent tests. Earlier full checks: Switch 322, Conductor 37,
packaging 9, skill validators; release gate and diff whitespace check clean
after corrections. Versions remain unchanged and nothing is committed here.

### Separate delivery-delegation observation

Anthony reports not seeing Conductor delegate work in a long time. This build
used Claude for independent reviews, not implementation. Reading execution.md
shows that routing, briefs and review are defined, but the decision to split
implementation between controller and workers is not prompted before inline
execution. Claude agrees with that distinction. Recommended separate correction:
at delivery start consider bounded independent implementation contributions,
delegate when useful and permitted, keep tightly coupled small work inline,
and show actual assignments and returned evidence. No compulsory worker quota
or ceremonial delegation. Anthony then approved “lets fix that now.”

The delivery guide now makes the implementation split explicit before inline
execution, with bounded contribution, context/latency/token cost and authority
as criteria. It names ownership, disjoint edits, controller integration and
complementary work. Small coupled edits stay inline with a brief reason; no
staffing approval loop or new tracker. The entrypoint points to this decision.
Codex makes this small instruction edit inline; Claude reviews it, rather than
manufacturing an implementation worker for an already-bounded paragraph edit.

Review brief: inspect the two new delivery paragraphs and entrypoint reference
for consequential routing/authority conflicts; apply them without dispatch to
a one-word fix, independent UI/export work, a delegation-prohibited host, and
two jobs editing the same dependent function. Existing Claude partner, observed
model `claude-fable-5-1`, retained effort unobserved; profile Fable 5.1 version
2026-09, scoped XML brief. Claude returned ready with two wording corrections:
include the established implementation partner in the candidate set and keep
independent review explicit beside controller integration. Both applied; resumed
builds also reuse settled assignments. The hypothetical choices were inline,
split with disjoint owners, inline without bypass, and one shared-function owner.
This is model scenario evidence, not an observed delegated implementation or
measured token/latency benefit. No mandatory wording-matching test was added.

Local checks: Conductor 37 tests, packaging 9, skill validation, release gate and
diff whitespace check pass. No runtime, manifest, installation or release change.

### 0.116.0 release checks

Anthony authorized the reviewed bundle's publication. Re-ran Agent 135, Switch
322, Conductor 37 and packaging 9 tests; hooks 21 passed (shellcheck unavailable).
Gate selftest 57 and root resolution 7 passed; release clean, audit clean with
the pre-existing requirements trace finding. Progress 15, matrix 16, matrix audit,
stage-schema check, render freshness and the three skill validators passed.
A fresh temporary Codex catalog built 54 files with manifest version 0.116.0;
the new succession guide shipped and the packaged adopt help ran. Not installed.

Claude's final read-only release-surface review checked manifests, descriptions,
README, links and living pointers, and ran the release gate. Ready for release;
its stale earlier-boundary label finding is corrected above. No session log or
dated decisions were rewritten. Remote commit and CI are verified after saving.

## Sources

- [Switch guide](../../../skills/switch/references/in-out.md)
- [Renderer](../../../skills/switch/scripts/where_we_are.py)
- [Renderer tests](../../../skills/switch/scripts/tests/test_where_we_are.py)
- [Agent](../../../skills/agent/SKILL.md)
- [Conversation presentation](../../../skills/conductor/references/journey.md)

No session lifecycle action, installation, deployment or peer-owned file change.
The root `kerd-laptop-result.patch` stays local-only and untouched.
