# Conductor restoration compared with v0.105.0

## Evidence boundary

Historical source is `54c28cd:skills/conductor/SKILL.md`, the v0.105.0 four-role
contract. The compared source is the 0.125.0 candidate as released at `ae2f17e`;
line and heading references below are to that commit. Two fresh
Sol/medium interpreters received the same six raw scenarios in
[composer-restoration-fixtures.md](composer-restoration-fixtures.md), one source
variant each, without this comparison or its expected verdicts. These are
source-guided interpretations, not installed-version performance. Requested
settings are recorded; effective runtime settings were not independently observed.

Claude separately reported native dispatch counts: on 09-01/02 under the old
four-role design, composer calls and explicitly sized players were frequent; on
09-11..14 after the rewrite, composer calls, player count and explicit sizing
dropped sharply. Those counts motivated this work but were not independently
recounted by Codex and are not normalized for work volume or evidence of quality.

## Source contract

| Contract | v0.105.0 | Integrated candidate | Verdict |
| --- | --- | --- | --- |
| Four owners | Named producer/composer/conductor/players at historical lines 18–34 | Capability-based owners in `ae2f17e:orchestration.md` “Compose a score…” | Restored; provider branding removed |
| Composer | Top-tier call, not a mode; two bounded passes at lines 226–249 | Two-pass bounded composer at `ae2f17e:orchestration.md` lines 59–84 | Restored; fallback judged to same bar rather than presumed inferior |
| Cold-readable score | Spec body, then tag, exact terrain/why/verify at lines 217–224 | Complete step before assignment at `ae2f17e:orchestration.md` lines 86–103 | Restored and broadened beyond code |
| Delegation bias | Mostly delegate with seam review at lines 220–223 | Bias for well-factored work; no ratio/quota; collateral review explicit | Adapted to retain judgment and permission checks |
| Model/effort | Fixed named ladder and session advice down/up at lines 101–114, 223 | Task-based capability mapping and supported effort, advice down/up | Restored without frozen provider tiers or mandatory confirmation |
| Worker brief | Spec slice sent to player at lines 263–266 | Complete score step reused; only missing transport facts added | Restored with less duplicate briefing |
| Controller collateral gate | Every task reads the actual diff; bulk/pattern changes always get this check at historical lines 268–282 | Every returned Player edit is checked against owned paths/hunks; bulk deletions, renames and pattern edits require the full diff at `execution.md` “Review every returned edit…” | Restored after Claude caught its omission from the first score |
| Evidence honesty | Verification and strong-language gates distinguish checked results and require naming how self-corrections were caught at historical lines 268–301 | Returned is not checked; settings evidence stays qualified; every caught defect, including Conductor's own, names its detection path | Restored and adapted to current evidence states |
| Failure ownership | Re-dispatch, never re-specify; three failures declared score wrong | Sound failure preserves semantics; known defect returns immediately; three attempts are a ceiling, not proof | Restored and corrected |
| Managed continuation | No current managed schema/routing in the historical source | Existing immutable agreement and `blocked` action retained; repair occurs after verified stop | Modern safeguard preserved |
| Named partner review | No persistent Agent binding route in historical source | Exact established partner through Agent; no silent fresh substitute | Modern safeguard preserved |
| Switch entry | Historical mode assumes older pickup/approval machinery | Generic offer opens direction-setting; task authority stays distinct | Current interactive-orientation agreement preserved |

Intentionally not restored: provider-brand defaults, command-only delegation
eligibility, a fixed number of `[keep]` steps, compulsory model confirmation,
legacy mode-marker/state writes, automatic closeout/commits, assumed composer
superiority, the historical plan gate where the producer approved the spec,
tags and sizing together before execution, or historical lifecycle actions.

## Same-scenario interpretation

| Scenario | v0.105.0 result | Integrated candidate result | Assessment |
| --- | --- | --- | --- |
| Two independent surfaces, shared seam | Two-pass composer; two delegated implementations; retained seam review | Same split, with explicit controller integration, route evidence and no action before score | Core behavior restored |
| Tiny spelling edit on highest/high | Inline; advised a historically named cheap pair and described an old settings gate | Inline; recommends a lower supported pair for comparable work without delaying or auto-changing this edit | Down-sizing retained, friction reduced |
| Narrow check passes, adjacent helper deleted | Rejects return at diff-review gate; re-dispatches same slice | Same; the source now mandates reading every returned edit's actual diff, and the fixture rejects the narrow pass | Restored after peer review exposed the first score's omission |
| Player error vs impossible score premise | Re-dispatches player error; returns impossible premise to composer; after three failures asserts score wrong | Same first two choices; after three, stops before fourth and reassesses without claiming cause | Restored with false inference removed |
| Generic offer, human check blocked, independent design available | Keeps direction on missing human report and asks for it | Keeps report unknown but proposes independent design with its own approval | Current orientation fix adds useful direction |
| Managed score defect and named Claude review | Correctly identifies score defect but has no managed handoff or partner route | Returns existing `blocked`, preserves passage/evidence, waits for verified stop; routes review to exact established Claude partner | Current safeguards fill historical gaps |

## Cold-player execution

A fresh Terra/medium player received only the completed `normalize_status` score
slice and the three-file scratch project at
`/private/tmp/kerd-cold-player.Dn4eUh`. It edited only `api.py`, returned its diff
and passed two tests. The controller independently reran both tests, inspected
the exact diff, and confirmed `test_api.py` and `sentinel.txt` had no tracked diff.
The public `format_label` neighbor was unchanged. This demonstrates one score
slice was playable cold; it does not prove general prompt efficiency, installed
Conductor behavior or composer quality.

## Present verdict

The candidate restores the v0.105.0 mechanisms hypothesized to explain bounded
composition, finished specs, predominantly delegated well-factored work,
per-contribution sizing and controller-held evidence judgment. It deliberately
keeps newer authority, model-evidence, Agent and managed-run safeguards. The
controller assessed the current interpretation as equal or stronger in the four
like-for-like cases. Scenarios 5–6 are not like-for-like: they exercise current
interactive-orientation, managed-run and Agent capabilities absent from the
historical source. In scenario 5, current Conductor can recommend independent
eligible work after the generic offer instead of treating a missing human report
as a project-wide hold.

This verdict is source and synthetic-execution evidence. It is not ordinary-use
acceptance or proof of lower tokens, cost or elapsed time.

## Addendum, 2026-09-14 13:06 EDT: third delegation route (local, after 0.125.0)

Anthony asked for a route that delegates already-clear work without a composer
call. The local change after `ae2f17e` adds it in `orchestration.md` “Choose who
writes the steps”: Conductor writes clear steps and delegates them when the
contribution is worth its handoff cost; the composer is used when the spec needs
design or reasoning; tiny, coupled or judgment-bound work stays inline. A defect
returns to the step's author. Codex reviewed it read-only and found no managed
boundary issue. The verdict above assesses the released 0.125.0 contract only;
the third route has no fixture, synthetic or real-build evidence yet, and v0.105.0
had no equivalent route to compare against.

## Future real-build observations

### Build 1 — observed to its send, 2026-09-14 (consumer project, non-code work)

Record actual installed revision, outcome/authority, composer scoping and terrain,
score/playability, assignments and requested/observed settings, returns, repairs,
review, human intervention and final evidence. Compare decisions with v0.105.0;
do not infer efficiency from counts alone.

**Source and limits.** One Claude session in a consumer project, started 14:10
EDT, read from its native transcript only: no contact and no edits there. The
transcript locator stays out of Git. A Sonnet 5 player extracted cited facts from
lines 1–858 under [observation-build-1-extract.md](observation-build-1-extract.md).
Conductor (this Kerd session's Claude review role) spot-checked lines 184, 320 and
724 (3 of 3 matching), and later scanned lines 859–1004 for the close. Line
numbers cite that transcript. This is **non-code, multi-step work**: two drafted partner
notes and one shared model-document update, each reviewed before commit. It is
judgment-heavy, which shapes every route below. Business content is left out.

- **Installed revision:** only `kerd/0.126.0` paths (switch, conductor, agent).
- **Entry:** Switch In, then "Start a Conductor session?", then a plain "yes" loaded
  Conductor for direction-setting with "no task approved by implication". It
  showed `Conductor · Shape` at 14:14. The person approved a recommended draft
  ("yes", 14:21) and later a scoped delivery ("yes", 15:07), which showed
  `Conductor · Deliver`, owner, file boundary and stopping point (uncommitted
  diff). No labelled Agree banner; the approval did that job.
- **Route chosen and why:** mostly route 3, inline, with concrete reasons: Shape
  had no approved task; drafting was judgment about claims; the model-document
  edit was "one shared file whose wording has to match both notes sentence for
  sentence". Route 1 (Conductor-written executable steps delegated) and route 2
  (composer) were **not exercised**; no step needed a design spec.
- **Assignments and settings:** 1 native subagent (read-only claim trace against
  source; `general-purpose`, Opus requested, in background), resumed once through
  SendMessage for a scoped second pass. Its metadata recorded `model: opus` as
  requested. Then 1 review by the person's existing Codex session through
  `kerd:agent`, which the person asked for by name. No parallel fan-out. The 36
  edit/write calls were all the controller's.
- **Grids:** six Task/Route/Model/Effort/Status grids, all well-formed Markdown at
  source. Every one labels the controller "Opus 5 (host-declared)" with effort
  "Unknown" and **argues no task-based fit**. The controller model/effort
  assessment that 0.124.0+ asks for is not visible.
- **Returns and diff reads:** both returns were read-only findings, not edits, so
  the returned-edit diff gate had nothing to check. The controller ran
  `git status`/`git diff` at several points and read the full diff of the model
  document before asking to approve it (line 836), after a parse self-check with
  the project's own status tool (line 829).
- **Failures and repairs:** no rejected return, re-dispatch or step repair. Three
  incidental tool errors were fixed on the next call. Failure routing is
  unassessed.
- **Human intervention:** three approvals, one redirect to Codex review, and then
  "review with codex" and "then send" (lines 859–869).
- **Close (lines 910–995):** a second Codex review returned a send-after-changes
  verdict. The controller applied the changes and committed and pushed to the
  consumer repository (line 971). It reported both notes sent, with local HEAD
  matching the remote (line 995). The next human message (line 1000, 21:00)
  starts Build 2.
- **Final evidence:** the pushed commits and the remote match reported at
  line 995. No test suite applies to this work.

**Assessment against the contract (complete run):**
- Met: inline reasons concrete, not "faster myself"; independent verification
  delegated rather than self-reviewed; named partner routed exactly; diff read
  before approval; entry and authority boundaries held.
- Unmet: visible controller model/effort fit. The observing session's own startup
  grid (Kerd, 15:20) had the same gap, so this is a wording or placement problem
  in the contract's presentation, not one session's slip. That is an inference
  from two sessions, not proven.
- Unassessed: routes 1 and 2, composer quality, delegation share on code, failure
  routing. Review was proactive only in part: both Codex reviews followed the
  person's request.

A second observation should be a code build, where route 1 can actually occur.

### Build 2 — observed through push and CI, 2026-09-14 (consumer project, composer route)

**Source and limits.** This is the same consumer session as Build 1: its second
piece of work, a staged packaging build (Swift package plus CMake suites and CI),
at lines 1005–2237. A Sonnet 5 player extracted cited facts under
[observation-build-2-extract.md](observation-build-2-extract.md), including the
`.meta.json` files for all subagents and the composer's own transcript.
Conductor spot-checked lines 1270, 1299 and 2039 (all matched) and scanned every
Bash and Read call in range. Two extraction defects were caught by those checks
and corrected here: the player missed Anthony's Codex reminder (lines 1522/1529)
and the sequencing statement (line 1385). **Close top-up (Conductor, inline scan of lines 2238–2466, 2026-09-14 23:00 EDT):**
stage 1's final review, commit, push and CI are covered below. Anthony confirmed
stage 1 done and stage 2 not started. Stage 2 is outside this observation. Project and partner names
are left out.

- **Installed revision:** 0.126.0 throughout (Build 1's reading; no other path in
  range).
- **Entry and authority:** a plain "yes" to shape the build (line 1000), then
  `Conductor · Shape` with owner (line 1005). There were two parallel Sonnet
  surveys for orientation, Codex design input at Anthony's request, "agree" to
  the shape (line 1207), and "yes" to build stage 1 and push once green
  (line 1262). The agreement named three stop conditions (line 1325). None fired.
  The step-7 check failure was outside them and ruled on within authority.
- **Route chosen and why:** route 2 (composer). The controller first re-read a
  saved feedback memory (2026-09-01): "subagents sized per step (Fable included),
  composer always Fable" (line 1270). That memory fixes the composer's model, not
  whether to compose. No written reason for choosing route 2 over route 1 was
  found. Step 9 (evidence) and commit/push were kept by the controller: "The score
  has no commit or push steps. I commit and push after the checks pass, as you
  approved." (line 1325). Route 1 was not used.
- **Composer:** one Fable subagent over nine turns. Pass 1 requested the reading
  set (line 1299), pass 2 wrote a 712-line score beside the work (line 1340), and
  there were **seven repair passes**. Triggers: the controller's own read of the
  score against the agreement (1), player evidence of score defects (5), and Codex
  review findings (1). The final score was 771 lines. Through the step-8 return
  (line 2237), every score defect went back to its author, the composer. The one
  later exception is under Close.
- **Score and players:** 8 of 9 steps delegated, with a model requested per step:
  Sonnet 5 for steps 1, 3 and 8; Opus 5 for 2, 4, 5 and 6. Step 7 was planned as
  Sonnet 5 and dispatched as Opus 5, with no stated reason found. There were 13
  player dispatches including re-runs, all background native subagents. A literal
  `[delegate]`/`[keep]` table was not found in the transcript. The grids' Route
  column carries the same information; the score file itself was not read.
- **Sequencing:** "Since every step's verification reruns export.sh into the same
  out/ folder, I'll run the players sequentially rather than in parallel to avoid
  conflicts." (line 1385). One player at a time, a concrete shared-state reason.
  "In parallel" at line 1475 means step 3 was sent out while the composer repaired
  step-2 passages, not two players at once. Only the orientation surveys fanned out.
- **Returned-edit diff reads:** the controller **independently re-ran players'
  verification** after returns: `export.sh`, test-count greps, probe logs,
  `build-report.sh --self-test`, and `export.sh` plus verify before step 8.
  It did not read the players' actual diffs or changed files before relying on
  them. The Bash and Read calls in range show one `git diff --stat` (line 2160,
  prompted by an empty step-8 return) and one Read of `ci.sh`. Most output was new
  files under a new package directory, which plain `git diff` would not show.
  Grep-tool calls were not scanned. At commit the controller checked
  staged paths against the upstream boundary (line 2307). That is a path-level
  check once, not a per-return hunk read.
- **Defects and routing:**
  - Step 2: the player found four wrong expectations in the score, sent to the
    composer.
  - Step 4: evidence staled one passage, sent to the composer.
  - Step 5: the player caught non-reproducibility. After a composer repair, the
    same player was resumed, passing on attempt 2.
  - Codex review of steps 1–6: six findings, all confirmed by the controller
    against the tree and sent to the composer as one pass. Affected steps
    re-ran.
  - Re-runs: a player reported a `pip` grep that always matches `pipefail`
    "instead of loosening the check", sent to the composer.
  - Step 7: its own check stopped at 11 of 12. The controller ruled "keep the
    check strict", the composer amended, and the player was resumed, passing on
    attempt 2.
  - Step 8: the first return was empty. The controller checked the state itself,
    and the full return later matched.
  - No step reached the three-attempt ceiling. The earlier report of the stop
    "moving to step 6" was a composer repair inside the agreed stops, not a
    change of scope.
- **Codex pair review:** Anthony's reminder (line 1522): "alos use codex as pair
  to review as we go or at the end - your call on when". Conductor then chose
  checkpoints: "one review after step 6 covering steps 1 to 6 ... and a final
  review of the full [repo] diff plus local `ci.sh` evidence before the push.
  Not per step: players are serialised and the mechanical steps are settled by
  their evidence." (line 1542). It recorded Codex's partner role as a pair
  reviewer through `agent.py`. The mid-build review returned "proceed after
  changes". The final review returned before commit (see Close).
- **Controller model/effort:** fifteen well-formed grids label the controller
  "Opus 5 (host-declared)" with effort "Unknown", and none argues fit.
- **Human intervention:** approvals at the shape and build gates; two review
  requests ("ask codex for input on that too", the pair reminder); and three
  clarity questions late in the run: "not clear, did codex do final review or not
  yet?", "aso what do you need now?", and "still not clear, where do i find the
  actual questions for 1-5, can you guide me 1 by 1".
- **Close:**
  - Codex's final review returned "commit and push", with all six earlier
    findings confirmed closed in code and two follow-ups (line 2357).
  - The controller made both follow-ups inline (lines 2268–2296): four edits,
    including **one edit to the composer-written score** (line 2296). No reason
    was found for not returning that passage to the composer. It looks like a
    small conformance edit.
  - Then a clean local full run (line 2300) and an explicit-file staging with
    `git diff --cached --stat`, plus a check that no upstream paths were staged
    (line 2307).
  - Commit pushed and confirmed on the remote (line 2318).
  - The CI run passed all 11 jobs. The controller "read the new job's
    log rather than trusting its green status" (line 2466).

**Assessment against the contract (stage 1 complete; stage 2 not observed):**
- **Met:**
  - Bounded two-pass composer with the reading set requested first.
  - Score written beside the work before assignment.
  - Delegation by default (8 of 9 steps).
  - Sequencing justified by concrete shared state.
  - "Re-dispatch, never re-specify": score defects returned to the composer
    seven times, player failures resumed with evidence.
  - Attempt counts within the ceiling.
  - Returns checked by independent re-execution, not accepted as reported.
  - Stop conditions honoured.
  - Named partner routed exactly.
  - Final evidence read from the CI job log, not from its status.
- **Unmet:**
  - (1) Reading every returned player edit's actual diff against owned paths
    before relying on verification. Re-running checks is strong evidence, but
    `execution.md` says verification does not substitute for the diff read.
    A staged-path boundary check at commit is the nearest evidence. (Grep-tool
    calls unscanned.)
  - (2) A visible task-based controller model/effort assessment. That's three
    sessions now, counting Build 1 and this observer's own grid.
  - (3) Considering independent review at startup, which `orchestration.md`
    already requires. Review was planned only after Anthony's reminder. See the
    proposed correction in `TODO.md`.
- **Partly met:** an explicit model was requested for each player (Sonnet 5 or
  Opus 5), but no task-based suitability reasoning was found, and step 7's
  Sonnet-to-Opus change is unexplained.
- **Partly met:** "a defect returns to the step's author" held for all seven
  score repairs, but one late follow-up edit to the composer's score was made
  inline with no stated reason.
- **Unassessed:**
  - Route 1 in real use.
  - Why route 2 was preferred over route 1.
- **Presentation observation:** the person asked three times for clearer state
  (final-review status, what was needed, where questions were). The status tables
  were well-formed but did not answer those questions. Anthony's pasted table was
  box-drawn, as rendered by the client, while the transcript grids are Markdown
  pipe tables. That supports the display/paste explanation for the earlier
  "mangled grid" note, from one paste only.

**Review of these records:** Codex, the established Kerd pairing, read-only,
2026-09-14 23:05 EDT. It returned five findings: public-record privacy, Build 1's
unexamined lines 910–999, two Build 2 contradictions, over-awarded player sizing,
and a misdiagnosed TODO source gap. Conductor verified each against the files and
applied all five. Codex judged the diff-read, inline-score-edit and controller-fit
calls fair. It was not asked to re-review the corrections.

Use the same evidence shape. After both builds, mark each contract met, unmet or
unassessed and name any correction. These slots do not block the source release.
