# TODO

## Now

- **Start the DESIGN rung — 4 functions, beginning with `Shape the solution`.** PRODUCT is complete (5 walked, 1 cut, 1 added). Walk state: `docs/plans/2026-08-03-requirements-walk.md`. Interview data is `DETAIL` in `tools/diagram/gen_functions.py`; each walked function gets a stage flow from its own generator in `tools/diagram/`. See `kivna/sessions/2026-08-03.md`.
- `Shape the solution` is served today by **superpowers brainstorming**, marked `PARTIAL` — it gives the capability, then captures the plan phase, routes to `writing-plans`, and never returns. That behaviour is the thing to interview against.
- **Debt from PRODUCT:** the route-specific acceptance checklists for `Frame the intent` (idea brief vs problem statement) are named but not written.
- **Still open — `reachable`.** Naming solves findability, not reachability. Partly answered by *What we ruled out* being read in grounding; not settled generally.
- **Still open — accepted risks age and nothing brings them back.** Temporary countermeasures are self-expiring, so that class is answered. Accepted unknowns and low-likelihood fatals are not.
- **Do NOT use `/kerd:capturerequirements`** — Tony's standing instruction; its dated-snapshot output is the shape under suspicion.
- **Nothing gets ripped until the design is approved** — including the `docs/plans/` rename implied by the naming rule.
- **v0.66–v0.68 are installed and have still never run.** Out of Fable credits, so the first run exercises the unavailable-orchestrator fallback.

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **CI on `~/3of3`** — high consequence AND high value, alone in that. `/loop` cannot run where nothing can refuse, so this gates a capability rather than guarding one. 0 workflows, 0 pre-commit hooks, every repo.
- Repin `leru`, `krutho-strategy`, `krutho-founders` off `kerd/0.65.0` — high consequence, **no value**: pure hygiene, one cache GC from silent breakage. `obair` has no pin at all (deliberate, or drift — unchecked).

**Medium**
- **The SPIKE** — route ONE dead skill cheaply and watch whether it gets used. Highest value in this band: one cheap test settles the fate of four dead skills. Candidate: `capturerequirements`.
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
- Dogfood sherpa on `~/Bree` — sherpa may be routed, reshaped or ripped by the design pass.
- Mode reconciliation, and clean krutho-strategy's stray `sessions-of-record/` — same decision.
- skriv voice profile wiring — needs non-founder-genre samples.
