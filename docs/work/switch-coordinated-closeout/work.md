# Compact arrival and coordinated closeout

## Now

Outcome: a recognizable Switch In dashboard and a handoff that preserves
collaborating sessions' necessary context without duplicate shared-file saves.

Stage: 0.116.0 release contents tested and reviewed; publication authorized.
Current activity: no implementation in flight. Publication authorized by Anthony's
“lets releaese”; resolve its state from the source boundary below.
Pending question: none.
Next action: the shared verification list below (`## Targeted verification of
reported failures`), item by item, owners as named. Consumer pickups stay deferred
until items 1–5 carry evidence of the fixes working. No consumer installation is part of this source release.

Source boundary: branch `main`, subject `Release Kerd 0.116.0: role continuity and implementation delegation`.
This record is saved with the release; its resulting hash and remote/CI result
are checked after saving, not pre-asserted inside it. Prior local-only statements
below describe the earlier reviews; publication was subsequently authorized.

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
| 1 | Arrival reply bound to the wrong thing: Leru 0.112.0 In promised design would start on a yes/no; Kerd 0.115.0 In (09:40) said "naming the project is what starts it" | Fresh Claude session after a clear; first verify which skill path and version actually loaded (0.116.0 is in the cache on disk, `plugin.json` 0.116.0; presence does not establish what loads). Switch In, then reply "not now" to its one pending question: nothing starts, nothing shown as owed. The project-name and factual Yes/No/Not sure replies each need their own genuine pending question; Kerd's arrival carries neither, so they stay with the deferred Codex pickup and the clarification scenario in `docs/work/codex-plugin/work.md`. | Claude (fresh session) | Anthony's supplied Leru and Kerd outputs, held by Codex | Needs Anthony to clear and open the session; he reads one reply. Only the "not now" case is exercised here |
| 2 | Human-owned check presented as agent work: Seinn 0.115.0 In asked "Starting on the couch verdict — approve?" | The same fresh In: the saved next action includes Anthony's own assessment of the arrival, so TASK/STATE name him as actor and YOU asks whether he can give it, not "Starting on X" | Claude (fresh session) | Anthony's supplied Seinn output | Kerd has no device; the assessment stands in for the couch verdict |
| 3 | Coordinated Out lost a contributor: Leru Out/In had no Codex log and conflicting TV claims, reconstructed not resolved | This session runs Out as owner: loaded skill is the 0.115.0 cache, guide followed is the released 0.116.0 `in-out.md` from the repository (a disclosed test route, not an installed-0.116.0 result); Codex's returned account captured once; MEMORY row shown; the fresh In (item 1) recovers both accounts without either old conversation | Claude (this session, owner); Codex returns its account | `kivna/sessions/2026-09-13.md` (one contributor, already saved) | Unresolved facts stay unresolved in the record, never reconstructed into proof |
| 4 | Role not recoverable when the session ID changes (pairing showed a stale title; ordinary `pair` refused a new ID) | After the Out save, this session (bound as `kerd-b5-review`, which has no `partner_role`, no ownership flag and no `handoff`; role preservation cannot be claimed for a field that is absent) runs `handoff --record CONTEXT.md` with the released helper `skills/agent/scripts/agent.py`, not the 0.115.0 cache helper, which lacks the command; the designation is verified against the final saved pointer before Anthony clears; the new session's In records the actual identity before and after, then `adopt --expected-session <old> --record CONTEXT.md`; Codex checks the binding and sends the successor one real request that arrives | Claude designates and adopts; Codex verifies and routes | Fixture tests and one native self-ID read (Agent 135) | Compare the actual identity before and after the clear; never infer it. A safe refusal on unknown or conflicting identity is a successful safety observation, not successful role continuation |
| 5 | Installed Codex snapshot reported stale since 2026-09-12 | Read the installed version before any Codex-side result is counted | Codex | Not rechecked at the 0.116.0 release | **Result 2026-09-13 ~11:00, Codex:** `codex plugin list --marketplace kerd-core --json` reports kerd@kerd-core installed, enabled, version 0.113.0, and the cached manifest agrees. Stale installed version confirmed; not 0.116.0 readiness. Nothing updated |
| 6 | Implementation never delegated (Anthony: not seen in a long time; Codex: reviews only, today) | Judged at the next real build where a split is useful; the check is the decision and visible ownership, including an inline choice with its reason. Not a prerequisite for items 1–5. The Backlog's Agent four-limits work is a candidate, and a separate scope decision for Anthony | Claude (Conductor) when a build runs | Four hypothetical choices reviewed 2026-09-13 | No real build in this verification |
| 7 | Consumer pickups (Codex in a work project; Seinn, Leru) | Deferred until items 1–5 carry evidence of the fixes working, not merely a recorded outcome; failed or unresolved checks stay visible here and keep the hold | — | — | Anthony's instruction, 10:41 |

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
