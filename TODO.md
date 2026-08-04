# TODO

## Now

**Post-walk design: turn the six tooling decisions into specs** (`docs/plans/2026-08-04-post-walk-tooling.md`): the format library into How-we-talk · the approaches capability + evaluation matrix (design instrument) · interrogate → tiered risk ledger · conductor's split (driving role; pieces graduate to the functions) · the sherpa cut executed when rips are licensed. MVP sequence: entry gates (keystone) · CI/refusal · progress renderer. The nine review questions are all answered (`annotations/log.md`).

Standing constraints: nothing ripped until the design is approved. Debt carried: `Frame the intent` route-specific acceptance checklists; accepted risks age with nothing to bring them back; one `(?)` left on the board (Design: machine-checkable interface values).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **CI on `~/3of3`** — high consequence AND high value, alone in that. `/loop` cannot run where nothing can refuse, so this gates a capability rather than guarding one. 0 workflows, 0 pre-commit hooks, every repo.
- Repin `leru`, `krutho-strategy`, `krutho-founders` off `kerd/0.65.0` — high consequence, **no value**: pure hygiene, one cache GC from silent breakage. `obair` has no pin at all (deliberate, or drift — unchecked).

**Medium**
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
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
