# TODO

## Now

**Next: grounding-was-read** — the remaining design-layer build (gates check the groundwork was actually read; spec A8 sketches the landing site — a `grounding` slot per rung + read-receipts on the `mark_reviewed` precedent). Working default: per-piece evidence check — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values); cache pinned at kerd/0.77.0, two versions behind (repin when convenient).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **Rigor level as a forcing function** (framed with Tony 2026-08-05, post-boundary): the level (spike / MVP / production-v1 / …) is **declared in the Release slice definition** — machine-checked legal values, gate-refused when absent. Declaring a level expands into named rigor classes (security · performance · logic coverage · data integrity · …), each forced into exactly one state: measured-with-target · waived-by-name (accepted risk + review trigger) · n/a-with-reason. DONE then assembles the rigor checks by construction — silence becomes structurally impossible; a spike stays cheap because its classes land in waived-by-name. Reuses the ledger's state pattern; generalizes `route: spike` into a rigor axis; level climbs per slice. Gap it closes: today an undeclared rigor class fails nothing — it's just never checked.
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
