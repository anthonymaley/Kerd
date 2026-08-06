# TODO

## Now

**rigor-level: built and cold-eyes-amended — waiting on the morning keys.** v0.81.0 live (design GO 61d320b · build 6e65ff7/ee43b6c · goal amendments f671cdc, all CI-green). Cold eyes: layers 1–3 PASS, layer 4 blocked four declared-truth gaps, amended per precedent. **Morning: Tony's expert-user pass → goal record `docs/gates/` → loop rung.** Cold-eyes findings born tonight sit in Backlog Medium (derive-from-constant · gate.py root pin · fenced-block wart).

Working default: per-piece evidence check — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values); cache pinned at kerd/0.79.0, one version behind (repin when convenient; corrected 2026-08-05 — both skills verifiably loaded from 0.79.0 this session).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **CI on `~/3of3`** — *3of3 is its own project, not part of Kerd* (clarified 2026-08-04); a possible trial ground for the refusal pattern, taken up only if that project wants it. `/loop` still cannot run there until something refuses.
- Repin `leru`, `krutho-strategy`, `krutho-founders` off `kerd/0.65.0` — high consequence, **no value**: pure hygiene, one cache GC from silent breakage. `obair` has no pin at all (deliberate, or drift — unchecked).

**Medium**
- **Revisit the journey view when more data exists** (parked 2026-08-05, Tony's call, shape agreed on mock v4 — `docs/plans/2026-08-05-journey-view-mock.html`). Settled shape: one page per journey, the idea/problem as title; A3 Proposal head (current drawn · numbered pains · proposal drawn · targets in units · cost named) + measured-in-use strip; then the ladder as sections — steps with status + facts, "what we created" with links per rung; a front page above it: what's-cooking task cards (name · sentence · % · time-left · status word) + next-up queue. Revisit condition: more journeys walked through the gates. Prerequisite surfaced: progress % and time-left need declared on-disk homes before the real page can show them. progress-html stays held at proving meanwhile; the trio plumbing stays.
- Clean krutho-strategy's stray `sessions-of-record/` — unblocked by the mode cut (v0.75.0).
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork (`.Codex-plugin`, `/kerd:dian` references); its identity line was fixed locally in the cut, the rest of the drift stands.
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- PR-event edge in the stale CI step (goal-gate cold review find): on `pull_request` the merge ref carries base-branch trailers the branch never rendered — a converged branch could go red. Unexercised (no PR flow); scope the step to `push` or contract PR behaviour when PRs become real.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).
- Derive the rigor refusal messages (and their fixtures) from `RIGOR_LEVELS` via join — closes the goal gate's BLOCK 1 in code instead of by named risk (cold eyes 2026-08-06; doc amendment shipped meanwhile).
- `gate.py` CLI pins root to `kit.ROOT` — run from any other cwd it silently audits Kerd, not the cwd tree (cold-eyes trap 2026-08-06); consider a `--root` flag.
- A fenced code block containing a `Rigor level:` line inside a `## Release slice` section counts as a duplicate — the first product doc that documents the rule inside its own Release slice goes red (cold eyes 2026-08-06, robustness wart, nothing trips it today).
- Gate records can only say GO: a refused gate has no dated home — AU3 rejects any non-rung filename in docs/gates/ and a `*-goal.md` file would satisfy the route glob (found 2026-08-05 when progress-html's goal was refused; verdict lives in the product doc instead). Consider a refusal-record shape in the gates schema.

**Low — genuinely ignorable, and you can see what ignoring costs**
- README conductor section's closing line "Conductor doesn't touch git. No pulls, no pushes." contradicts the commits-its-own-work paragraph above it — stale since v0.67.0. One-line fix, next release that touches the section.
- Decide whether switch should commit the vault repo (contract vs behaviour disagree).
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Surface model-tiered delegation in the two plugin capability-list descriptions. Open since v0.64.0.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- skriv voice profile wiring — needs non-founder-genre samples.
