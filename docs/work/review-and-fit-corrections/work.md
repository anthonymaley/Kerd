# Review cadence, visible fit and returned-edit reads

## Now

Owner: Claude (Conductor controller, Kerd).
Stage: Complete for release. 0.127.0 is released in the boundary commit that adds this
record; resolve the revision with `git log`. Codex's before-push review 4
(2026-09-15 00:41) found no remaining issues, and every suite and gate passed
(Agent 182, Conductor 70, Switch, hooks 21/21, gate selftest/audit/release, progress,
matrix, journey, fidelity).
Next action (proposed, not agreed): the real-use correction test below, on the next
real paired build running 0.127.0 installed. Then the next release: effort-sized
Claude players (`TODO.md` `## Now`).
Environment note: `/usr/bin/git` failed on an Xcode license prompt from 2026-09-15
00:27 until Anthony accepted it at 08:46. This build used
`DEVELOPER_DIR=/Library/Developer/CommandLineTools`, which is no longer needed.

## Agreement

- 2026-09-14 23:08 EDT, Anthony: "yes do all and add the pairing too?" in reply to
  shaping a four-part correction from the real-build observations, then "yes see it -
  lets do it" (23:09), answering "Shall I lift the no-release scope and start shaping
  that four-part correction?". Authorized by that yes: (a) the no-release hold is
  lifted for this correction, meaning a release is no longer ruled out in
  principle; (b) shaping the whole correction. **Not yet authorized:** build,
  commit, push and release. Each needs its own explicit approval, asked when
  reached. (Codex's recheck proposed recording "shaping only". Claude kept (a)
  because it is Anthony's actual answer, and clarified the wording instead.)
- Direction on reviews (2026-09-14 20:10 and 20:14): "it should offer the reviews or
  ask how i want reviews run through the project once"; "if we set a pair we should
  ask prefernce at that time or if we /agent we ask preferences - can be adjusted by
  telling ssession of course but we can ask user up front - maybe even a multiple
  picker".

## Evidence

[composer-restoration-comparison.md](../conductor-clean-entry/composer-restoration-comparison.md)
Builds 1 and 2 (0.126.0 in real use, a consumer project, reviewed by Codex), and the
proposed correction in `TODO.md` `## Now`.

## The four gaps

1. **Reviews not planned or offered.** Every Codex review in both builds followed
   Anthony's request. `orchestration.md` already says to consider independent
   review at startup; Agent step 3 stores a role but no review cadence.
2. **Controller model/effort fit not argued.** Grids label "Opus 5 (host-declared)"
   with effort "Unknown" and no task-based reason, in three sessions.
3. **Player sizing without reasoning.** Build 2: a model requested per step with
   no recorded suitability, and step 7 changed Sonnet 5 → Opus 5 unexplained.
4. **Returned edits not diff-read.** Build 2: the controller re-ran verification
   instead of reading returned changes; most output was new files, which plain
   `git diff` does not show.

## Surveys (Shape)

- [D1 brief](survey-d1-docs.md): every clause bearing on the four gaps, with
  conflicts.
- [D2 brief](survey-d2-code.md): where a review cadence would be stored, read,
  displayed and tested.

Both surveys returned 2026-09-14 23:12–23:15 and were spot-checked by Conductor:
D2 4 of 4 and D1 5 of 5 citations matched. Findings are used below by file:line.

## Design, revision 2 (proposed; Codex design review 2026-09-14 23:20 applied)

Revision 1 was reviewed read-only by Codex, the established Kerd pairing, and was
"not ready for build". Its findings 1–8 are applied here and noted as [R1]–[R8].
Codex rechecked revision 2 at 23:25. It found 2, 5, 6 and 8 resolved; the
baseline contents, same-gate invalidation, the CLI guide, the `partners` output
contract and authority wording still open. All are applied as [recheck], with the
authority wording clarified rather than narrowed (see Agreement). There is no
third recheck; Codex reviews the full change set before release.

### A. Review cadence, asked at pairing (gap 1)

**Contract.**
- A pairing stores how that exact partner reviews, next to its role. Agent asks
  once when it pairs or starts a persistent partner.
- Conductor plans review from the cadence visibly at startup, and offers once when
  the selected established partner has none.
- The person changes it by telling any session.
- The cadence schedules that partner **only inside an independently authorized
  task**. It grants no work, no contact beyond that task, and no commit, push or
  release authority [R4]. A peer still cannot authorize anything.
- Managed Conductor's forced review after every implementation
  (`managed-decision.md:47-51`) takes precedence inside managed runs and is stated
  as such [R7].

**Values** (multi-select; the labels are proposed and Anthony may reword them):
- `checkpoints`: review at the risk points Conductor names in the plan.
- `before-push`: review the full change before commit, push or release.
- `end`: one review when the work completes.
- `on-request`: do not schedule this partner automatically. It is exclusive of
  the others. It does not waive Conductor's independent-assessment duty
  (`execution.md` "Review, prove and improve") [R4].

**Coalescing [R4, recheck].** One accepted review satisfies coincident gates, for
example the last checkpoint, before-push and end, only while the reviewed tree
and evidence are unchanged. **Any change after a review, including a correction
the reviewer asked for, invalidates every gate that review satisfied.** That same
gate is repeated before its protected effect (the push, the completion). The only
exception is another coincident gate that necessarily runs first and reviews the
current tree and evidence.

**Several established partners [R5].** Cadence is stored per exact binding.
Conductor selects the reviewer by recorded role and task fit. If several
candidates remain materially plausible, it shows that choice once. It never
schedules every binding or guesses from recency.

**Agent code** (`skills/agent/scripts/agent.py`):
- One cadence validator, used for CLI input and the persisted-binding readers
  `notice_binding` and `partners`; `checked_binding` (used by handoff and adopt)
  tolerates it (repaired 23:50 to match score S1). The current
  `adopt` copy path does not re-validate (D2 item 1) [R2]. Malformed stored
  cadence (wrong type, unknown value, `on-request` mixed with others) is reported
  as unresolved for that binding, never passed to orchestration.
- `pair` and `start --kind partner` accept a repeatable `--review-cadence VALUE`.
  It is stored as `review_cadence: [...]` next to `partner_role` (in `pair` at
  `:822`/`:827`, in `start` at `:878`/`:883`). Re-pairing with the flag replaces
  the list; a role-only update keeps it. `start` refuses it for workers.
- **Carry-forward:** `adopt` (`:610-614`) copies `review_cadence` with
  `partner_role`. That covers a prepared handoff, restart recovery and explicit
  `--confirm-replacement`, since all use `adopt` [R5].
- **New read-only command** `partners` returns this project's bindings from
  private metadata only, with no native discovery, session probing or contact.
  Conductor consumes it and does not parse binding JSON [R2]. `sessions` output
  is unchanged.
- **Output contract [recheck]:** JSON `{"partners": [...]}`, ordered by alias.
  Each row has `alias`, `provider`, `kind`, `role` (or null), `review_cadence`
  (list or null) and `valid`.
  - An invalid row is kept, with `valid: false`, an `error` string and
    `review_cadence: null`.
  - A mix of valid and invalid rows exits 0, so one corrupt binding never hides
    usable partners.
  - A non-zero exit is reserved for store-level failure (unreadable directory,
    wrong project).
  - No session IDs are shown beyond what `sessions` already returns.

**Agent tests** (new, next to `test_agent.py:409-439` and `:84-129`):
- store, replace, and role-only update preserving the cadence;
- refuse unknown values, `on-request` with others, and a cadence on a worker;
- malformed stored cadence is reported by `partners` and `arrival`; `adopt` carries
  it unchanged rather than refusing handoff (repaired 23:50 to match score S1);
- the cadence survives handoff/adopt, a second restart and explicit replacement,
  and this test fails if the copy line is removed;
- `partners` with several bindings returns each exactly, in alias order, and
  probes nothing;
- `partners` with one malformed and one valid binding exits 0, keeps both rows
  and marks the bad one with `valid: false` and an `error`.

**Agent docs:**
- `SKILL.md` step 3 (`:55-63`): ask once for role and cadence together, using
  the host's multi-select control where one exists, otherwise one plain question
  listing the values. Record them with `--partner-role` and `--review-cadence`,
  and do not re-ask on later requests.
- `references/user-guide.md` `:18`, `:64-72`: explain the cadence, its authority
  limit and how to change it.
- `references/session-succession.md`: the cadence travels with the role through
  handoff, recovery and replacement [R7].
- `references/native-sessions.md` (`:30-45`, the detailed `pair`/`start` CLI
  guide): cadence syntax, replacement and role-only preservation, the authority
  limit, and the `partners` command [recheck].
- `SKILL.md` frontmatter description: pairing records role and review cadence [R7].

**Conductor docs:**
- `orchestration.md` "One visible startup view" (`:165-187`) and `:136-137`: read
  established partners through `agent.py partners`; select the reviewer as above;
  show planned review rows from its cadence; with no cadence, propose one grounded
  in the task's risk, ask once and record it through Agent; with `on-request`,
  plan no partner row and keep the own-review duty; apply coalescing.
- `journey.md:191-195`: the example grid shows a planned review row with its
  cadence.
- `managed-conductor.md`: forced review takes precedence over a stored cadence
  inside managed runs [R7].
- `work-record.md`: the record keeps the review plan (partner, cadence, gates) [R7].
- `SKILL.md` frontmatter description, if the startup behaviour line changes [R7].

**Switch docs:** `in-out.md:196-200` keeps the cadence privately with the role.
TEAM stays `provider (role)`.

### B. Visible fit (gaps 2 and 3)

**Contract.**
- Every startup view carries a **Fit** line immediately under the grid, never a
  grid column.
- There is one Fit line for the controller, and one for **every newly selected
  model job: composer, player and reviewer** [R6]. Identical jobs may share one.
- Another is written whenever a job's model, effort or route differs from its
  plan or changes on retry.

Shape: `Fit · <job> — needs <requirement>; <pair> because <reason>`, adding
`; consider <alternative>` **only when the pair materially exceeds or misses the
need** [R6], so no alternatives are manufactured. Settings keep their evidence
labels (`orchestration.md:25-31`). No model confirmation is required. A grid with
a model and no Fit line is incomplete.

**Edits:**
- `orchestration.md:175-180`: the example gains a Fit line.
- `journey.md:191-195`: the example gains Fit lines.
- `execution.md:212-215`: a supported change states its reason before
  re-dispatch.
- `model-jobs.md:21-27`: a job dispatched differently from its plan states why
  before sending.
- `guidance/model-choice.md:70-73`: "Show the person" names the Fit line.
- `work-record.md`: the Fit evidence is kept with the job note [R7].
- `README.md:728-742`: describes the Fit line.

### C. Returned-edit reads against a baseline (gap 4)

**Contract [R3].**
1. **Before dispatch**, Conductor records a **content** baseline for the step's
   owned paths [recheck]. Names alone cannot attribute a player's edit to an
   already-dirty file. The baseline holds:
   - the tracked patch against `HEAD`, staged and unstaged, per path;
   - for every untracked or ignored entry inside the owned paths (enumerated with
     `git status --porcelain=v1 --untracked-files=all --ignored -- <owned paths>`):
     type, symlink target, size and content hash.

   Declared generated trees may use their named manifest or check command instead
   of per-file hashes.
2. **After return**, it records the same snapshot and **compares contents, not
   just membership**, so the player's change set is exactly the difference:
   - tracked hunks, staged and unstaged, against `HEAD`, read in full;
   - every new or changed untracked file, read if it is text;
   - **binaries and symlinks** checked by type, target, size or hash, and a
     domain check;
   - **deletions and renames** read as part of the complete set.
3. **Generated or ignored output** must be declared in the score, for example an
   ignored `out/`. Declared generated trees are checked by a named manifest or
   command, not read line by line. **An undeclared ignored-path delta is a
   finding**, never silently treated as generated.
4. The work view records each return:
   `Change read · N tracked hunks, M new text files read, K binary/symlink
   checked, generated paths checked by <command>, unexpected: none|list`.

For clean owned paths, the baseline is an empty snapshot, which keeps small work
proportionate. The snapshot is working evidence, kept beside the step, not a new
tracker.

**Edits:**
- `execution.md:198-206`: the actual change set above replaces "reads the actual
  diff". New files, binaries, symlinks and ignored deltas join the always-complete
  list.
- `orchestration.md` "Make every score step independently executable": a step
  declares its generated and ignored output paths.
- `journey.md` delegation updates: the returned-to-checked transition shows
  `Change read`.
- `work-record.md`: keeps the per-return change-read evidence [R7].
- `README.md` Conductor section: one sentence.

### Release shape (each stage awaits its own approval)

- 0.127.0 (MINOR: changed behaviour).
- The full release checklist per `CLAUDE.md`:
  - the three version locations;
  - README sections for Agent and Conductor;
  - **both byte-identical capability descriptions**, because pairing now stores
    an orchestration preference [R7];
  - trigger descriptions for `agent` and `conductor`.
- Checks [R7]:
  - `python3 tools/gates/gate.py release` plus the repository's other gate and
    audit checks;
  - the Agent, Switch and Conductor/packaging test suites;
  - `tests/hooks_test.sh`.
- Proposed build route, decided at build approval:
  - A's code and tests: a Conductor-written step for a player (the spec is clear
    and checkable by tests).
  - The doc edits: Conductor-written steps with disjoint file ownership.
  - Codex reviews the full change set before release (cadence: `before-push`).

### Test of the correction

**Automated** (before release) [R8]:
- exclusivity and malformed stored metadata;
- explicit replacement and several bindings;
- managed forced-review precedence (a doc and grid check);
- change-set baselines with staged, untracked, ignored, binary and pre-dirty
  cases (fixture checks of the documented commands).

- Also: a pre-dirty file edited by a player is caught by the content comparison;
  and a correction after a before-push review repeats that gate before the push
  [recheck].

**Real use** (after release; a smoke test, not full acceptance) [R8]:
- One real sequence: pair with a cadence, then Switch Out handoff and In adopt,
  then Conductor start. The cadence survives and review is planned from it.
- In the next real paired build on 0.127.0:
  - Fit lines for the controller and every selected model job;
  - a `Change read` line on every return, including new files;
  - coincident gates on an unchanged tree reviewed once.

Recorded like Builds 1 and 2.
