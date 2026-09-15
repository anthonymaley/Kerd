# Backlog archive

Backlog rows closed at Switch Out, each with its verdict, the evidence and the date; and
position paragraphs moved out of `CONTEXT.md` when they stopped being current. Nothing here
is edited after it lands. Started 2026-09-11 at the first run of the lean-start step (v0.111.0).

## Closed 2026-09-15

**Verdict: done — both real-build slots recorded 2026-09-14.** Builds 1 and 2 (a
consumer project on 0.126.0, non-code notes and a composer-route packaging build) are in
`docs/work/conductor-clean-entry/composer-restoration-comparison.md`. They are read from
source, reviewed by Codex, and assessed met, unmet or unassessed. The unmet findings
were fixed in 0.127.0.

- **Then: observe the next two real multi-step builds on 0.126.0** and fill the two
  slots in `composer-restoration-comparison.md`: the route Conductor chose, composer
  calls, delegation share and fan-out, returned-diff reads, failure routing, and a
  visible controller model/effort assessment.

**Verdict: done — released in 0.127.0 (2026-09-15).** Pairing asks once for role
and review cadence; Conductor plans review from it or offers once. Design, four Codex
before-push rounds and evidence: `docs/work/review-and-fit-corrections/`.

- **Proposed correction: Conductor offers reviews itself** (Anthony, 2026-09-14
  20:10 and 20:14): ask once how reviews run, store it with the pairing, plan from it.

**Verdict: done — released in 0.128.0 (2026-09-15).** Five `kerd:effort-<level>`
agents set a delegated Claude job's effort. `job_evidence.py` observes what ran. A probe
observed `kerd:effort-low` as Sonnet 5 at `low`. Record:
`docs/work/effort-sized-players/`.

- **Next release: effort-sized Claude players** (Anthony, 2026-09-14 23:55).

**Verdict: superseded — by bringing the plugins to 0.128.0 (current `TODO.md`).**
0.127.0 and 0.128.0 were released after this row.

- **First (proposed): bring the installed plugins to 0.126.0.**

**Verdict: superseded — the fit gap is fixed and the mangling is probably display
(one paste).** The grids in that 0.126.0 session were well-formed Markdown at source.
Anthony's pasted table was box-drawn by the client, which supports display or paste
as the cause, from one paste, not verified against the exact transcript Codex meant.
The missing controller fit assessment is addressed by 0.127.0's required Fit line.

- **Check the Conductor staffing grid in the original work-anthony transcript.**

## Closed 2026-09-14

**Verdict: done — observed 2026-09-13 16:08 EDT by the Claude session that adopted
`kerd-b5-review`.** That session's loaded skill path and `plugin.json` read 0.119.0;
`identity` matched, `adopt --expected-session … --record CONTEXT.md` consumed the
designation and wrote the recovery receipt against unchanged `CONTEXT.md` bytes;
`arrival` showed TEAM and returned the first live notice to `codex-tui` as
submitted-unconfirmed. The 0.119.0 layout it assessed was itself replaced the same
evening (0.120.0, no YOU box). Evidence: `kivna/sessions/2026-09-14.md`.

- **First: a fresh Claude In on 0.119.0** (rows 1, 2 and 4 of the shared
  verification list), with routing adoption and the first live arrival notice.

**Verdict: superseded — replaced by the two real-build observation slots in
`docs/work/conductor-clean-entry/composer-restoration-comparison.md`.** Delegation
was redesigned three times since (0.124.0 task assessment, 0.125.0 composer/score
restoration, 0.126.0 Conductor-written steps); observing "useful implementation
work with owners and edit boundaries" is now part of those slots.

- **Observe Conductor assigning useful implementation work with owners and edit
  boundaries at a real build (row 6).**

## Retained position, 2026-09-13 (moved from `CONTEXT.md` at the 2026-09-14 Out)

The 0.119.0 position paragraphs, no longer current: installed state and routing
sequence as they stood at the 2026-09-13 15:31 Out.

**Installed state, not to be overclaimed:** the 13:51 Claude session loaded the
0.118.0 cache (skill base path and `plugin.json`, observed once); no session has
been observed loading 0.119.0, and publication does not update a plugin cache.
Installed Codex Kerd is 0.118.0 (row 5, reported by Codex 13:30); no Codex
update to 0.119.0 is authorized. Verify the loaded skill path and version before
counting a result.

**Where the sequence stands at this save:** the 13:51 session adopted
`kerd-b5-review` at 13:52 from the 12:43 Out's designation against the unchanged
saved record (row 4's planned adoption), then took seven real requests from Codex
on that binding, all answered (row 4's messaging proof). It ran this Out on the
0.118.0 cache: the ownership check matched, and the contribution checkpoint
requested Codex's delta since the release, which returned "none". After the save
it designates its successor against this file with
`skills/agent/scripts/agent.py handoff --record CONTEXT.md`. Anthony then
restarts Claude so the plugin can load 0.119.0 (`/clear` is not assumed to
update it). The fresh session: verify the loaded skill path reads 0.119.0; Switch
In's routing runs `identity`, then `adopt --expected-session <the currently bound
ID> --record CONTEXT.md`, then 0.119.0's `arrival --provider claude --self-alias
kerd-b5-review` (its default recipient on Kerd is `codex-tui`, by a metadata-only
check); the arrival shows TEAM and the notice outcome for Anthony's assessment.
Receipts and the designation stop matching when this file's bytes change.


## Closed 2026-09-11

**Verdict: dead — the step it describes no longer exists.** Conductor has had no close-out
since 0.107.0 replaced it (`grep -rniE "close-out|closeout" skills/conductor` is empty; the
2026-09-11 Fable review, finding 1, and README's rewritten "How They Fit Together").

- **Close-out double-write** — conductor step 1 writes CONTEXT/TODO, step 6's
  invoked flow overwrites both.

**Verdict: superseded — the producer took option (c) on 2026-09-11** ("switch out should
clean up todos/backlogs/docs/etc and set next session start to make switch in faster/cheaper"),
before the row's own return condition fired (CONTEXT.md was 216 KB against the 250 KB
trigger). Built as Switch Out's lean-start step in v0.111.0: ruling in the loaded file, case
in `docs/decisions.md`. The row's measurements and its named risk (a reachable record can
sit unread) stand and are the reason the reading set is measured at every Out.

- **Switch-in costs ~17% of the context window — measured, diagnosed, and
  DEFERRED by the producer 2026-09-01.** *"Do nothing for now"* — this repo is
  complex, mid-planning, and losing context is the more expensive error. The
  measurement is recorded here so no later session re-derives it, and **the row
  as first filed blamed the wrong lever (pruning); that framing is superseded by
  what follows.**
  **Where the cost is:** the read set is 250KB — `CONTEXT.md` 177KB (70.7%, so
  **12 of the 17 points**) · the day's session log 37KB (2.5 pts) · `TODO.md`
  36KB (2.5 pts). `## Key Decisions` alone is **97.9%** of CONTEXT.md; every
  other section totals 3.8KB.
  **Growth is two multipliers, and pruning only reaches one.** Bullets went 17
  (2026-07-06) -> 48 -> 74 -> 101 -> **131** today, while the MEAN bullet went
  232B -> 676 -> 919 -> 1,239 -> **1,352B**. Count 7.7x, size 5.8x.
  **The decisive measurement: old bullets do not accrete.** Of the 48 standing on
  2026-08-04, **44 survive and grew 1.01x** (29,376B -> 29,593B) with 4 removed;
  the **87 added since average 1,696B — 2.5x the survivors' 672B — and are 147KB,
  83% of the whole section.** So deleting every pre-August decision recovers 29KB
  (16%) and touches none of the growth. **Pruning is aimed at the wrong
  variable**, which is why two licensed prune events both ended with the file
  bigger.
  **Rate: linear, not compounding.** ~30 new bullets per window, per-window mean
  1,297B -> 2,117B -> 1,695B (inflated once in mid-August, then plateaued). ~5.3
  KB/day, projecting ~250KB in two weeks (~22% of a pickup) and ~320KB in four
  (~26%).
  **Two options were priced and neither taken.** (a) A size budget per decision —
  **refused on the producer's own reasoning**, the argument that got to a ruling
  is the thing the boundary exists to preserve. (b) Tiered loading, his idea:
  deferring the whole Backlog buys **2.2 pts**, and rank-and-read-High-only buys
  **0.5 pts** because High is already 76% of the Backlog — both aimed at the
  2.5-point file. (c) Named but untested: split CONTEXT.md the way 2026-07-03
  split state/work/history, keeping the **ruling** in the loaded file and moving
  the **case** to a reachable record — a full read of a smaller file rather than
  a reduced mode, which `skills/switch/SKILL.md` forbids outright. **Its risk is
  the one this repo has already paid:** `docs/design/conductor-role.md` was
  reachable by name and sat unbuilt for three days, which is why `fidelity.py`
  exists.
  **Return condition:** CONTEXT.md passes **250KB**, or a pickup passes **25%**,
  or the per-window bullet mean resumes climbing — whichever comes first. Until
  one fires, this is an accepted cost, not an open task.

## Closed 2026-09-12

Verdicts from the closure review a native Opus 5 subagent returned on 2026-09-12
(the first real Conductor session on 0.111.0; full table at
`docs/work/model-ready-work/trials/2026-09-12-conductor-session-closure-review.md`).
Three done, eight dead; the sixty open and two unsure rows stay in TODO.md. The
hooks-verification row's open sub-finding was kept in TODO as its own row.

**Verdict: done.** `71391f8` exists; `docs/product/gate-visuals.md:8,12` carry the resealed fingerprints the row names.

- ~~**THREE sealed views are factually stale.**~~ **CLOSED 2026-08-29.**
  `funnel-driver`'s two were resealed 2026-08-28 (`71391f8`); `gate-visuals`'
  `visual-lifecycle.html` was corrected and resealed at its own acceptance gate
  on 2026-08-29 (`fp:3ef85a6441d5` -> `fp:c4f3e8949191`, producer's eye), and
  `design-gate-check.html` was found stale by cold eyes at the same gate and
  resealed with it (`fp:ccbac6efdb93` -> `fp:d210312a9bec`). The rule the row
  existed to enforce held throughout: each was redrawn at ITS OWN gate, never
  from another slug's slice.

**Verdict: done.** `hooks/hooks.json` present; `hooks/session-start.sh` builds the string; the row's three observations stand. Its open sub-finding stays in TODO as its own row.

- ~~**Verify hooks auto-load fires on this machine.**~~ **CLOSED 2026-08-13
  ~16:40**, at this sitting's switch-in. Three confirming observations: the
  cache carries 0.96.0 with `hooks/hooks.json`; neither `.claude/settings.local.json`
  nor `~/.claude/settings.json` holds any Kerd hook wiring; and `📋 Last session:
  2026-08-13` appeared at session start — a string built only by
  `hooks/session-start.sh` (lines 39, 58, 63). Auto-load works and
  `${CLAUDE_PLUGIN_ROOT}` resolves at runtime with zero per-repo wiring.
  **Note for `docs/product/hooks-autoload.md`:** its risk ledger still calls
  this open, and its acceptance test quotes the rendered string `Last session`
  when the source literal is lowercase — a grep for the documented string
  returns nothing and reads as "the hook didn't fire".

**Verdict: done.** `find ~/development/work/krutho-strategy -maxdepth 4 -name 'sessions-of-record*'` returns nothing; the directory is gone.

- Clean krutho-strategy's stray `sessions-of-record/`.

**Verdict: dead.** The composer was removed at 0.107.0 (`21e6779`; `grep -rni composer skills/` is empty). Artifact half verified fixed: 0 absolute home paths, 21 `rev-parse --show-toplevel` in the 2026-09-01 spec.

- **The composer emits hard-coded absolute repository paths, and a cold review
  pass does not catch them** (measured 2026-09-01 on the
  `requirements-success-measurement` spec). Pass 1 produced 24 of them
  (`/Users/anthonymaley/development/product/Kerd`), the dedicated cold-review
  pass read the whole spec and missed every one, and the amendment inherited
  them and added two more — 26 at review. **This is the same defect handed back
  to the composer on 2026-08-28**, when a reviewer's host had the repo at
  `~/Kerd` and the score assumed this one; it is therefore reproduced, not
  new. A player on another machine, or in a git worktree, follows the score to
  the wrong tree. Fixed in place this time on the producer's call (mechanical,
  no judgment): every block now derives `repo_root=$(git rev-parse
  --show-toplevel)`. **The countermeasure is a brief clause, not a fix:** the
  composer dispatch should forbid absolute paths outright, and the cold-review
  brief should name them as a hunt target. Neither is written down anywhere
  today, which is why the same defect arrived twice.

**Verdict: dead.** Same composer removal (`21e6779`). Artifact half fixed: the spec's verify chain uses `test … -eq 0`.

- **`grep -c` in a fail-fast verify chain fails exactly when it should pass**
  (found 2026-09-01, second instance). The spec's final step ended
  `&& grep -c "^- \[ \] " <spec>` to prove zero unchecked boxes — and `grep -c`
  exits 1 on zero matches, so the `&&` chain aborted on the desired answer.
  Corrected to an exit-safe count (`awk` then `test -eq 0`), tested both ways.
  **Also handed back on 2026-08-28** as one of the same three sibling score
  defects. Two of those three have now recurred, which says the 2026-08-28
  findings were fixed in the artifact and never in the process that produces it.

**Verdict: dead.** Same composer removal (`21e6779`). Artifact half fixed by `528ca88`; cross-step invalidation marked in the spec.

- **A spec writes the CONSEQUENCE of an open question as settled fact, so
  answering the question falsifies prose elsewhere in the document** (measured
  2026-09-01, twice in one sitting, on the
  `requirements-success-measurement` spec). Step 5's `categories.md` rewrite was
  written assuming `MSC` would be another requirement category, and ruling 1
  falsified it — its own override clause covers only item 1, so items 2 and 3
  stand as written and contradict the ruling. Step 4 stated that a machine
  comparison was *"feasible only under Step 2's ruling (a)"*, and ruling 2 took
  (b) — but the premise was already wrong on its own terms: `kit.py:892` globs
  and parses acceptance records today, so the option was **relocated, not
  eliminated**, and would have been silently dropped by anyone reading the spec
  literally. **Same family as the hard-coded-path and `grep -c` rows above: a
  countermeasure that is a brief clause nobody has written down.** The clause:
  a spec whose steps depend on an unanswered gate must mark those cross-step
  dependencies explicitly, so keying a gate names what it invalidates instead of
  leaving it to be found one gate at a time. Not fixed here — carried into the
  composer hand-back for this item, which is not the same as fixing the process.

**Verdict: dead.** Its named home, Conductor's "Calling the composer" section, no longer exists; the intent survives at `skills/conductor/references/execution.md` ("Finish the outcome").

- **The three composer-brief clauses need a DURABLE home in
  `skills/conductor/SKILL.md` — the producer's ruling, 2026-09-01: two places at
  two times.** *Now* they are explicit acceptance conditions in tonight's
  composer brief (done — dispatched this sitting). *Later*, as **its own scoped
  skill-behaviour change — not inside `requirements-success-measurement`** — they
  land in the composer-brief section (`skills/conductor/SKILL.md:226-249`,
  "Calling the composer" / what the brief carries), **with verification that a
  future score actually carries all three.** The three, as he worded them: every
  repository path derives from `git rev-parse --show-toplevel` · zero-match
  checks remain successful when zero is the expected result · consequences of
  unresolved producer gates are expressed as dependencies or branches, never as
  settled facts.
  **Why this is High and not Medium: it is the generator fix for the three rows
  above, and the defect has now survived being fixed twice.** Two of the three
  sibling score defects handed back on 2026-08-28 came back on 2026-09-01,
  because the correction was written into the artifact and never into the thing
  that produces artifacts. The session log's own insight states the mechanism —
  *a finding fixed in the artifact and not in the generator is a finding that
  will arrive again* — and this is its measured proof. **Verified 2026-09-01:**
  `grep -rn "absolute path\|hard-coded path\|rev-parse --show-toplevel" skills/`
  returns **zero**, so nothing in any skill forbids absolute paths, names them as
  a cold-review hunt target, or requires cross-step dependencies to be marked.
  **Sizing note:** this is a real skill-behaviour change, so it carries the full
  release checklist (version in three locations, README, trigger description) —
  which is exactly why the producer refused to fold it into tonight's sitting,
  per the 2026-08-27 ruling that bumps are not for corrections inside one
  unfinished item. **Cold-review brief is a second surface** and may need the
  same clause: the dedicated cold-review pass read the whole spec on 2026-09-01
  and missed all 24 hard-coded paths — *a reviewer hunting meaning does not see
  form*, which argues the two hunts are separate briefs.

**Verdict: dead.** The marker was removed at 0.107.0 (`21e6779`); `docs/state-contract.md:11` records the removal.

- **The conductor marker cannot carry a sitting's open time, and 2026-08-23 is
  the second and worse instance — the diagnosis is now broader than "planning
  twice".** First bite (2026-08-22): re-entering `plan` overwrote the `execute`
  stamp. Second bite (2026-08-23): the session ran ~08:44–12:17 almost entirely
  in `plan` — a design conversation carried by drawings — so `execute` stamped
  at **12:17**, fourteen minutes before close. Handing that over as the sitting's
  open time would have labelled a four-hour session as fourteen minutes. **The
  real defect: the marker holds one line, so it can only ever report the LAST
  phase, while the open time is a property of the FIRST.** Any design-heavy
  session reproduces this, planning once or twice. Two candidate fixes, neither
  chosen: keep a separate never-overwritten `opened` stamp, or have the boundary
  derive the open side from the session's first machine-written timestamp rather
  than from the marker at all. Owner: conductor's mode-marker section + switch's
  sitting-heading rule. **SIXTH instance 2026-08-25 at ~14 minutes, the smallest yet** (switch-in
  12:13, `execute` stamped 12:27). **FIFTH instance 2026-08-25, ~26
  minutes** (switch-in 07:46, `execute` stamped 08:12) — small because execute
  was reached early. The measured spread is now 14 min · 26 min · 66 min · 157
  min, which shows the defect scales with how long the planning phase runs, not
  with anything random. **SEVENTH instance 2026-09-09, and a new failure mode:
  six DAYS, not minutes.** No conductor ran that session at all, yet
  `kivna/.active-modes` still held `conductor: plan @ 2026-09-03 23:59 EDT` — the
  parked schema-split marker — so switch-out's fallback ("use the stamp on the
  `conductor:` line still in `.active-modes`, if one is there") pointed at a
  marker from a previous *session*, not a previous phase. The boundary wrote
  `closed HH:MM` instead. **This widens the diagnosis a second time:** the marker
  cannot report the first phase (the 2026-08-23 finding), and it cannot report
  *whether it belongs to this sitting at all*. A staleness guard is needed
  regardless of which of the two candidate fixes is chosen.

**Verdict: dead.** `hooks/stop.sh` was cut at v0.96.0 (`2146925`, "Ship hooks via plugin auto-load; cut stop.sh").

- **Stop-hook over-prescription**: distinguish work-dirty from
  session-state-dirty at a real stopping point.

**Verdict: dead.** Its reason is gone: `skills/tend/SKILL.md:207` says the hook path never version-rots (v0.96.0, `2146925`).

- Hook version staleness check in `/kerd:tend`.

**Verdict: dead.** Switch was replaced at 0.107.0 (`21e6779`); the numbered steps and the smoke test no longer exist.

- Guard switch-in step 3 smoke test against context bloat.

## Retained position, 2026-09-03

Moved verbatim from `CONTEXT.md` `## Where We Are` on 2026-09-11; it was a position
paragraph, not a decision, and TODO.md's "Earlier launch sequence" carries the live
version of the same items.

### Previous installed-Kerd position — retained, not freshly revalidated

**2026-09-03, three sittings (08:38–09:16 · 10:40–14:03 · 14:09–23:18 EDT) —
the schema migration SHIPPED.** Kerd at **v0.106.0**; CI green at the tip
(`f098ae5`).

- **`risk-state-split` is at ACCEPTANCE** — all 14 pieces landed. The whole
  ladder walked in one sitting: design package with three sealed views and a
  GO record (`1008a43`), a 14-step work specification, and the migration
  itself as **one atomic commit** (`e15a0f0`). The ledger's `State` column is
  now **Severity** (`fatal` | `non-fatal`) + **Treatment** (the four values);
  `Evidence` renamed `Risk evidence`; **`Treatment evidence`** is new, in
  three machine-distinguished forms — empty · `planned — <what will exist> ·
  <expected location>` · a resolving citation. 21 records, 84 rows migrated;
  selftest 51 → **57**. Next: the evidence-backed acceptance record.
- **`gate-reachability` still REFUSES at viability, on row 2** — and that is
  the intended outcome, not a regression. Row 1 parses clean (fatal +
  permanent + planned evidence): the new mechanism working on real data. Row 2
  is fatal with an `accepted unknown` treatment and empty evidence, so it
  refuses independently. **The migration clarified the blocker; it did not
  unblock the item.** Its narrow `${CLAUDE_PLUGIN_ROOT}` measurement must
  resolve before it advances.
- **Four fatal/accepted-family risks are newly VISIBLE and refusing** —
  `funnel-driver` row 4 · `gate-reachability` row 2 · `gate-visuals` row 1 ·
  `switch-fidelity` row 4. Each was carried as *accepted* while being fatal,
  a contradiction the one-column schema could not express. Remediation
  belongs to each owning item, never to the migration (the producer's ruling).
- **The migration-map view was RESEALED** (`fp:aef214c7ae05` →
  `fp:3b7b1c17243a`) after the producer's row-2 key superseded the
  design-time prediction that gate-reachability would unblock. Downgrade →
  correct → re-render → his eye → reseal, in that order; the dated GO record
  stands untouched and the supersession lives in
  `docs/plans/2026-09-03-risk-state-split-reseal.md`.
- **The launch plan is ON DISK** (`8b08ad1`) — five outcomes, the 8-step
  critical path, the binding rules. **Launch: 0 of 5 outcomes.**
- **v0.105.0 (morning): the Status Report talk format** — status speaks Work
  item · Stage · Issue · Resolution path, one final question.
