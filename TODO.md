# TODO

## Now

- **Continue the walk — SESSION rung next (4 functions: open/close · route to the altitude · drive to done · keep context optimal), then CROSS-CUTTING (5 open).** The spine (PRODUCT → DESIGN → CONTRACT → BUILD) is complete and reviewed. Same interview loop; expect consolidation — every drafted rung has shrunk under interview.
- **Standing constraints:** no `/kerd:capturerequirements`; nothing gets ripped until the design is approved; no skill names in candidate views — requirements and outcomes only.
- **Debt carried:** route-specific acceptance checklists for `Frame the intent`; the `reachable` clause; accepted risks age with nothing to bring them back.

Standing constraints: no `/kerd:capturerequirements`; nothing ripped until the design is approved; no skill names in candidate views. Debt carried: `Frame the intent` acceptance checklists; `reachable`; accepted risks age.

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
