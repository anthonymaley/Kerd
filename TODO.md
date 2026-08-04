# TODO

## Now

- **Continue the walk — CONTRACT rung next: `Write the contract · Size and assign` (function 10).** DESIGN is complete: collapsed 4→1 into `Design the solution`, interviewed and reviewed both-keys 2026-08-03. Walk state: `docs/plans/2026-08-03-requirements-walk.md`. Note for the interview: this function is served by conductor v0.66–0.68 — its session protocol ran live for the first time on 2026-08-03 (lean/inline path), but the orchestrator call and sized players have still never fired.
- **Standing constraints:** no `/kerd:capturerequirements`; nothing gets ripped until the design is approved; **no skill names in candidate views during the requirements walk** — requirements and outcomes only (Tony, 2026-08-03).
- **Debt carried:** route-specific acceptance checklists for `Frame the intent`; the `reachable` clause; accepted risks age with nothing to bring them back.

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **CI on `~/3of3`** — high consequence AND high value, alone in that. `/loop` cannot run where nothing can refuse, so this gates a capability rather than guarding one. 0 workflows, 0 pre-commit hooks, every repo.
- Repin `leru`, `krutho-strategy`, `krutho-founders` off `kerd/0.65.0` — high consequence, **no value**: pure hygiene, one cache GC from silent breakage. `obair` has no pin at all (deliberate, or drift — unchecked).

**Medium**
- **The SPIKE** — route ONE dead skill cheaply and watch whether it gets used. Highest value in this band: one cheap test settles the fate of four dead skills. Candidate: `capturerequirements`.
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Settle the `reachable` clause (also in Now — it blocks every artifact from being useful rather than merely stored).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).

**Low — genuinely ignorable, and you can see what ignoring costs**
- Decide whether switch should commit the vault repo (contract vs behaviour disagree).
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Surface model-tiered delegation in the two plugin capability-list descriptions. Open since v0.64.0.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- Mode reconciliation, and clean krutho-strategy's stray `sessions-of-record/` — same decision.
- skriv voice profile wiring — needs non-founder-genre samples.
