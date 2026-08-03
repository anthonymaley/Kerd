# TODO

## Now

- **Continue the requirements walk — next is `Test viability`, function 2 of 5 in PRODUCT.** 1 of 25 functions interviewed. Walk state and verdicts: `docs/plans/2026-08-03-requirements-walk.md`. Interview data is `DETAIL` in `tools/diagram/gen_functions.py`; each walked function also gets a stage flow from `tools/diagram/gen_flow.py`. Order is top-of-board, function by function. See `kivna/sessions/2026-08-03.md`.
- **Debt carried from `Frame the intent`:** the route-specific acceptance checklists (idea brief vs problem statement) are named but not written.
- **Still open on `Where the work is written down`:** the *reachable* clause. Naming solves findability, not reachability — the 6 Jul design doc that held 1 Aug's answer was perfectly well named and went unread. Everything else in that requirement is agreed.
- **Do NOT use `/kerd:capturerequirements` for this** — Tony's explicit instruction. It's under review, and its dated-snapshot output shape is the thing we suspect is wrong.
- **Nothing gets ripped until the design is approved.** Includes the `docs/plans/` rename implied by the new naming rule.
- **v0.66–v0.68 are installed and still have never run.** First real conductor session should watch: does the orchestrator subagent reliably write-and-summarise; does after-the-body tagging shrink `[keep]`; does a `[keep]` diff-review catch collateral a verify command misses. Tony is out of Fable credits, so the first run exercises the unavailable-orchestrator fallback.

## Backlog

- **The SPIKE** (movement 7): route ONE dead skill cheaply and watch whether it gets used. Candidate: `capturerequirements`, cheapest to wire with the cleanest signal.
- **CI on `~/3of3`** — highest consequence on the board, least Kerd-shaped. 0 workflows, 0 pre-commit hooks, every repo.
- Repin remaining repos to the current cache version: `leru`, `krutho-strategy`, `krutho-founders` are still on `kerd/0.65.0`. `obair` has no Kerd pin at all (deliberate, or drift — unchecked).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).
- Decide whether switch should commit the vault repo (contract vs behaviour disagree — see CONTEXT.md).
- `CHANGELOG.md` is stale at 0.14.0 while the repo is at 0.68.0, and it's absent from the CLAUDE.md release checklist. Revive it or delete it.
- Surface model-tiered delegation in the two plugin capability-list descriptions, or leave "session discipline" to subsume it. Open since v0.64.0.
- Dogfood sherpa on `~/Bree` — contingent on the design pass, since sherpa may be routed, reshaped or ripped.
- Mode reconciliation deferred until that same decision; clean krutho-strategy's stray `sessions-of-record/`.
- skriv voice profile: wiring held pending non-founder-genre samples.
- Stale Kerd.md MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`. May be superseded by whatever the requirements agreement decides.
