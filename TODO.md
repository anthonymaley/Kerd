# TODO

## Now

**Three time-awareness follow-ups DONE — v0.89.0** (`ffa327e`, started 18:19 · landed 18:22): conductor's marker write moved out of Mode Markers into all four phase sections, close-out's no-execute-stamp consequence named, the `**Clock:**` line given its first write-side instruction, the hook fixture stamped and its assertion strengthened. Prompt-layer discipline placed at the drift's own granularity — **not a check**, and named as such in the skill, the README and the commit.

**The sitting-range unit got its live test this session.** The plugin cache is current (0.88.0 served at switch-in — the repin debt is closed), and the marker was written and restamped at every transition: orient 18:10 · plan 18:13 · execute 18:19 · close-out 18:28, each from a same-turn `date`. This sitting's log heading is the first with a derivable open time.

**CI honesty — still unverified, and not this session's fault**: GitHub's Actions incident has run all day (`major_outage`, confirmed live at 21:30Z). Every tip from `4889293` onward has no run; `ffa327e` did not even queue one. All seven gate steps plus the 26-test hook harness are green locally on every tip.

Next pick: Backlog High freshest — auto-sizing · stop-hook · boundary-cycle · release-closeout slice 2 (declared external surfaces).

Working default: per-piece evidence check — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **boundary-cycle, in-half** (Tony 2026-08-06; the out half and the next-pick suggestion SHIPPED as conductor-boundary v0.84.0 — close-out invokes switch out and names the pick, no loop): what remains is the reset ritual's automation — today it's the banner's two keystrokes (`/clear`, then switch in). **Killer feasibility question first, verified against harness docs at frame, never from memory**: a session cannot run `/clear` on itself (wall confirmed 2026-08-06); candidate mechanism is a marker file + SessionStart/UserPromptSubmit hooks. Used at every 50%-context reset. The wider loop question (auto-pick between boundaries) was resolved to suggestion-not-loop by Tony's key; the 2026-08-02 loop-guard flip (CI can refuse now) stays noted here if it's ever re-argued.
- **Boundary auto-sizing**: light/low have zero users ever (interview 2026-08-06) — kill them as user-facing modifiers; switch reads what the session changed and sizes its own boundary. Protect the three-file switch-in path absolutely.
- **Stop-hook over-prescription**: the hook nudges full switch-out when the honest need is a conductor work commit or a TODO touch — distinguish work-dirty from session-state-dirty at a real stopping point.

**Medium**
- **The refusal surface does not travel with the plugin** (found 2026-08-06 answering Tony's CI question): `.github/workflows/gate.yml` is Kerd's own build gate — three steps are self-tests, `release` checks Kerd's version fields, `stale` compares Kerd's board, and `tools/gates/kit.py:24` derives `ROOT` from the tool's own path, so a consuming project cannot audit itself even though the cache ships `tools/`. No skill invokes any tool (grep of `skills/`: zero hits). So in a project *using* Kerd, "a model choosing to comply is not a check" still holds in full — the gates are Kerd's development discipline, not something the plugin confers. Decide whether that's the intended contract (and say so in the README) or a gap worth closing (the `--root` flag row below is its cheapest first step).
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
