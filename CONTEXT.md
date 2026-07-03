# Context

> Test 2 artifact (2026-07-03): hand-written in the shape the context/history-split
> design proposes (`docs/plans/2026-07-03-context-history-split.md`). If the split
> is built, switch owns this file. If Test 2 fails, delete it.

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills plus community modes. Core skills: switch (session handoff/boundary), conductor (session discipline), sherpa (idea lifecycle PM), kivna (vault/knowledge), tend, trim, slainte, skriv, lorg, interrogate, focus, capturerequirements. Currently v0.59.0.

## Where We Are

Two live threads:

1. **Context/history split (this week's work).** Design co-signed and committed: state (CONTEXT.md, overwritten) / work (TODO.md, lean) / history (kivna/sessions/, immutable) — one kind of information per file; switch-in reads state + work + latest log only (~4.3k → ~2.3k tokens, zero fidelity loss). **Test 1 (A/B cold-pickup quiz) PASSED** 2026-07-03. **Test 2 is in flight right now**: this very handoff was written in the lean shape by hand (skill unchanged) — the next switch-in reads only CONTEXT.md + TODO.md + the latest session log, and Tony judges whether it still feels like the same session. Pass → build (3 slices, plan in the design doc).
2. **Sherpa dogfood (carried).** The full sherpa Explore→Validate→Plan→Build→Launch lifecycle is functional (v0.46.0–v0.49.0) and `dian` was renamed `conductor` (v0.59.0), but the stages have never run live. Dogfood target: `~/Bree` (personal-health-OS app, mid-Build) — happens in that repo, in a fresh session there, after Tony updates the stale plugin cache (was 0.45.0).

## Key Decisions

- **State/work/history are different things — one file each** (2026-07-03). Completeness comes from full-fidelity session logs + git history of CONTEXT.md (pruned content is never lost); efficiency comes from reading less, not storing less. The sharp edge: CONTEXT.md must never become a diary — the session log is the diary.
- **RDF rejected** for document/data holding and handoff (2026-07-03): an LLM has no query engine at load time — it pays per token of serialized text; triples run ~2× the tokens of prose for the same decision and drop the causal "why". Prose is the compressed format for the LLM reader.
- **Vault Status.md: written at switch-out, never read at switch-in.** The vault stays human-first; it contains nothing the log + CONTEXT.md don't.
- **Older session logs are archive, never per-session load.** Safe because forward-only discipline carries live items and the playbook is the durable gotcha net — switch-out will verify gotcha mirroring before commit (design hardening after Test 1 found a five-day-old unmirrored gotcha).
- **conductor (session) + sherpa (lifecycle), split by timespan** — sherpa guides the multi-session climb, conductor keeps one session in tempo. "coach" rejected (too sporty); "sensei" rejected (collides with the sensei plugin, oversells).
- **A mode is a right-sizing contract, not an orchestration checklist**; skills are everyday tools. Kerd owns its modes — not a router over external skills (GSD removed v0.43.0; Superpowers distrusted as waterfall).
- **sherpa = one skill; Kerd stays one plugin.** Durable state in committed `kivna/sherpa.md` (one repo = one idea); `.active-modes` holds only a session pointer (session-ephemeral).
- **Validate is risk-driven, not menu-driven** — find the killer assumption, run the cheapest test of it, clear only the fatal risks. Design: `docs/plans/2026-06-29-validate-methods-toolkit.md`.
- **jit + spike stay standalone modes** (Tony needs jit for the dogfood); folding/retiring the rest of the prune list is deferred until the dogfood teaches us what the stages need.
- **Memory tools (claude-mem/mem0/mempalace/beads/agentmemory): adopt none** — they break git-portable handoff and human-first, and solve a retrieval problem Kerd doesn't have.
- **skriv voice profile: HELD** — don't wire until non-founder-genre samples exist (n=1: profile at `~/eolas/vault/people/Anthony Maley Voice.md`).
- **TODO is forward-only**; session history stays repo-side (`kivna/sessions/`), never the vault.

## Open Questions

- **Test 2 verdict** — does the lean pickup feel like the same session? (Decides the split build.)
- Dogfood shape: pick up Bree mid-lifecycle (past Explore) or take a fresh feature through the full climb?
- Should switch commit the vault repo? (`~/eolas/vault` is a separate git repo, ~20 uncommitted files; skill contract claims all git boundary ops, behavior doesn't commit it — contract and behavior disagree.)
- At build time: does conductor's close-out need its own line in the lean-TODO contract? Should tend gain a CONTEXT.md drift check (lean yes)?

## Active Mode

- **focus: on** in this repo — partner-mode working agreement: rapid back-and-forth, reasoning internal unless it changes Tony's decision, ONE speech-bubble question (no X/Y binaries), interrupt early, eyeball-gated slices. Enforced by a UserPromptSubmit hook; persisted user-global in `~/.claude`.
