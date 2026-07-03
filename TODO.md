# TODO

## Current Session

**⚗ TEST 2 IN FLIGHT — lean handoff.** This handoff was hand-written in the context/history-split shape (`docs/plans/2026-07-03-context-history-split.md`; skill unchanged). **At switch-in, read ONLY: `CONTEXT.md` + this file + `kivna/sessions/2026-07-03.md`. Skip vault Status.md, the MOC, and older-log skims.** Then Tony judges: does it still feel like the same session?

- **Next: Test 2 verdict** → pass = build the split as a conductor session (3 slices, plan in the design doc); fail = the miss names what to pull back into the lean set.
- **Then: dogfood sherpa on `~/Bree`** — happens in that repo, fresh session there (decide first: mid-lifecycle pickup vs fresh feature).
- Mode reconciliation deferred until the dogfood; clean krutho-strategy's stray `sessions-of-record/` (tend detects it).

### Context

Moved to `CONTEXT.md` (Test 2 — see above). Standing decisions, open questions, and the active-mode snapshot live there now.

## Backlog

- skriv voice profile: wiring held pending non-founder-genre samples (see CONTEXT.md)
- Decide whether switch should commit the vault repo (contract vs behavior disagree — see CONTEXT.md)
- slainte auto-trigger idea: fold a light slainte pass into switch-in
- kivna/vault-spec question: is the human-first structure optimized for the cold-LLM-read consumer? (partly answered by the 2026-07-03 split design: Status.md becomes write-only, human-only)
- First interactive smoke test of /kerd:interrogate (meta path or real path)
- Path B (paused): Stop + PostToolUse hooks — ship only if Path A reframe doesn't shift behavior measurably
- Spike mode v1 retro — pending after measurable-baseline test
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults
- PPS marketplace.json fix from prior session — still unpushed/unregistered
- Hook version staleness check in /kerd:tend (pinning is a recurring manual burden)
- Stale Kerd.md MOC version field (says 0.31.0 vs actual) — update per release or remove (lean remove)
- Solicit community mode contributions
