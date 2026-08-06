# TODO

## Now

**time-awareness DONE — the eighth full ladder walk, closed 17:45 EDT** (frame 0684c11 · design GO 9e77999 · contract af00386 · build 5c770f4 v0.88.0 · goal amendments 4889293 · record 628281e · release pass 8ef9759). Both keys produced findings: cold eyes blocked layers 3 AND 4 (first layer-3 block in seven runs — the sitting range's open time was underivable on the default path), and the expert-user pass caught **the model fabricating a marker stamp that never existed** while describing the feature that forbids exactly that. One unit honestly open: "sitting sections record start–end ranges" is built and fixture-proven but **not yet delivered live** — its real test is the first fresh session running current skill text with a stamped marker written at orient. Earlier the same day: trim CUT (v0.87.0, fourth rip, nine skills), release-closeout closed (seventh walk), the goal-record trigger clause added (v0.86.0).

**CI honesty — verify next session**: GitHub Actions major incident all afternoon (status "Partial System Outage — Incident with Actions, investigating"). Only 0716567 got a run and is green headSha-verified; b8b4c92 went green on its third rerun; every tip after ae2a4db has no run at all. All seven gate steps plus the 26-test hook harness are green locally on every tip.

Next pick: Backlog High freshest — auto-sizing · stop-hook · boundary-cycle · release-closeout slice 2 (declared external surfaces).

Working default: per-piece evidence check — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values); the plugin cache still serves 0.79.0 skill text (observed again this session in all four skill loads) while the repo is at 0.88.0 — repin/update before relying on new skill behavior.

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **boundary-cycle, in-half** (Tony 2026-08-06; the out half and the next-pick suggestion SHIPPED as conductor-boundary v0.84.0 — close-out invokes switch out and names the pick, no loop): what remains is the reset ritual's automation — today it's the banner's two keystrokes (`/clear`, then switch in). **Killer feasibility question first, verified against harness docs at frame, never from memory**: a session cannot run `/clear` on itself (wall confirmed 2026-08-06); candidate mechanism is a marker file + SessionStart/UserPromptSubmit hooks. Used at every 50%-context reset. The wider loop question (auto-pick between boundaries) was resolved to suggestion-not-loop by Tony's key; the 2026-08-02 loop-guard flip (CI can refuse now) stays noted here if it's ever re-argued.
- **Boundary auto-sizing**: light/low have zero users ever (interview 2026-08-06) — kill them as user-facing modifiers; switch reads what the session changed and sizes its own boundary. Protect the three-file switch-in path absolutely.
- **Stop-hook over-prescription**: the hook nudges full switch-out when the honest need is a conductor work commit or a TODO touch — distinguish work-dirty from session-state-dirty at a real stopping point.

**Medium**
- **The conductor's marker is never current** (expert-user pass 2026-08-06, time-awareness goal gate — the pass's own finding): the marker sat at `plan` from orient through close-out while phases advanced, and the model then fabricated an `execute` stamp that never existed. Nothing machine-checks marker currency, and the sitting-range open time now depends on it. Candidate: a check at close-out that the marker's phase matches the phase being closed, or derive the open time from the first work commit instead.
- **Stamp the hook harness fixture** (cold eyes 2026-08-06, time-awareness goal gate): `tests/hooks_test.sh:310` writes an unstamped `conductor: orient`, so the standing four-file net never exercises the stamped shape that is now the only legal one — measurement 3 proved it once with a throwaway. Append `@ 2026-08-06 15:17 EDT` to that fixture line to convert a one-time proof into a standing one.
- **The Clock line has no writer** (same review): `tools/gates/README.md` documents it and the frame claims new records carry it, but no skill instructs writing one — the unenforcement is the accepted risk, the missing write-side instruction is a separate gap. Candidate: one line in conductor at the gate-record moments.
- **Revisit the journey view when more data exists** (parked 2026-08-05, Tony's call, shape agreed on mock v4 — `docs/plans/2026-08-05-journey-view-mock.html`). Settled shape: one page per journey, the idea/problem as title; A3 Proposal head (current drawn · numbered pains · proposal drawn · targets in units · cost named) + measured-in-use strip; then the ladder as sections — steps with status + facts, "what we created" with links per rung; a front page above it: what's-cooking task cards (name · sentence · % · time-left · status word) + next-up queue. Revisit condition: more journeys walked through the gates. Prerequisite surfaced: progress % and time-left need declared on-disk homes before the real page can show them. progress-html stays held at proving meanwhile; the trio plumbing stays.
- Clean krutho-strategy's stray `sessions-of-record/` — unblocked by the mode cut (v0.75.0).
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork (`.Codex-plugin`, `/kerd:dian` references, line 42 "updated by dian close-out" — re-spotted by cold eyes 2026-08-06); its identity line was fixed locally in the cut, the rest of the drift stands.
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- PR-event edge in the stale CI step (goal-gate cold review find): on `pull_request` the merge ref carries base-branch trailers the branch never rendered — a converged branch could go red. Unexercised (no PR flow); scope the step to `push` or contract PR behaviour when PRs become real.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).
- **lorg-cut candidate** (Tony's canvas comment 2026-08-06: "never used… Claude has plugin management now") — evidence check per the rip discipline before any license: usage archaeology (lorg artifacts anywhere?), overlap vs `claude plugin` CLI (management ≠ gap-discovery — name what dies), README/capability-list rows die with it. **Interrogate rides the same review**: the walk found it never-invoked; its everyday tier already works without invocation; the question is whether the large-bet co-signed session needs a *skill* or just the ledger standard in docs/design/.
- **kivna verdict** — the same zero-usage smell as the vault (interview 2026-08-06: no user opens Obsidian). Import/export CONFIRMED unused (Tony 2026-08-06); their original intent was **cross-agent handoff** (export for Codex, import its output back) — never exercised, and the state-in-artifacts boundary now covers agent handoff through the repo itself (any agent reading the three files picks up the session). Evidence-checked archaeology per piece (scaffold too) before any license; the vault-unhook coverage table is its input.
- **CI rule for the single-definition law** (cold eyes 2026-08-06 v0.84.0 observation): nothing machine-enforces "conductor never re-describes a Switch Out step" — a future edit passes all seven steps silently. Cheap mechanical candidate: refuse if `skills/conductor/SKILL.md` matches any Switch Out `### ` heading text.
- **Close-out double-write** (same review): conductor close-out step 1 writes CONTEXT/TODO, then step 6's invoked flow overwrites both in place — pre-existing shape, now visibly redundant inside one act. Reconcile (likely: step 1 shrinks to decision-recording only) before it becomes a who-wrote-what incident.
- Derive the rigor refusal messages (and their fixtures) from `RIGOR_LEVELS` via join — closes the goal gate's BLOCK 1 in code instead of by named risk (cold eyes 2026-08-06; doc amendment shipped meanwhile).
- `gate.py` CLI pins root to `kit.ROOT` — run from any other cwd it silently audits Kerd, not the cwd tree (cold-eyes trap 2026-08-06); consider a `--root` flag.
- Gate records can only say GO: a refused gate has no dated home — AU3 rejects any non-rung filename in docs/gates/ and a `*-goal.md` file would satisfy the route glob (found 2026-08-05 when progress-html's goal was refused; verdict lives in the product doc instead). Consider a refusal-record shape in the gates schema.

**Low — genuinely ignorable, and you can see what ignoring costs**
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- skriv voice profile wiring — needs non-founder-genre samples.
