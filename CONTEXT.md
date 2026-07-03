# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills plus community modes. Core skills: switch (session handoff/boundary), conductor (session discipline), sherpa (idea lifecycle PM), kivna (vault/knowledge), tend, trim, slainte, skriv, lorg, interrogate, focus, capturerequirements. At v0.60.0 (context/history split).

## Where We Are

Two live threads:

1. **Context/history split — BUILT (2026-07-03).** Test 1 (A/B quiz) and Test 2 (manual lean cycle) both passed; the split shipped as v0.60.0: state (CONTEXT.md, overwritten) / work (TODO.md, `## Now` + `## Backlog`) / history (kivna/sessions/, immutable). Switch-in reads exactly those three files. Switch-out gained closure inference (done/open/unsure verdicts on open TODOs, informational list, unsure tagged `(done? — confirm)` for one switch-in question) and a prompt-free vault save. First switch-out on other repos self-migrates them. This file is now owned by switch.
2. **Sherpa dogfood (carried).** The full Explore→Validate→Plan→Build→Launch lifecycle is functional (v0.46.0–v0.49.0), `dian` renamed `conductor` (v0.59.0), but the stages have never run live. Dogfood target: `~/Bree` (personal-health-OS app, mid-Build) — in that repo, fresh session, after Tony updates the stale plugin cache (was 0.45.0).

## Key Decisions

- **State/work/history are different things — one file each** (2026-07-03). Completeness comes from full-fidelity session logs + git history of CONTEXT.md (pruned content is never lost); efficiency comes from reading less, not storing less. The sharp edge: CONTEXT.md must never become a diary — the session log is the diary.
- **Closure inference is a readable list, never a prompt** (2026-07-03): switch-out shows done/open/unsure verdicts; a "done" verdict requires session evidence (commit, file, log entry); only unsure items become a question, asked once at next switch-in.
- **kivna save writes without approval** (2026-07-03): switch-out is the single vault write path, so an approval gate was pure friction; do-not-save markers remain the privacy control. Scaffold keeps its approvals (it creates from an interview; save just reflects the session).
- **Conductor's decisions live in CONTEXT.md, its plan in TODO `## Now`** (2026-07-03) — settled the design doc's open contract question; no separate conductor line needed.
- **RDF rejected** for document/data holding and handoff (2026-07-03): an LLM has no query engine at load time — it pays per token of serialized text; triples run ~2× the tokens of prose for the same decision and drop the causal "why". Prose is the compressed format for the LLM reader.
- **Vault Status.md: written at switch-out, never read at switch-in.** The vault stays human-first; it contains nothing the log + CONTEXT.md don't. (This also answers the old vault-spec question about the cold-LLM-read consumer: the LLM reads CONTEXT.md, the human reads the vault.)
- **Older session logs are archive, never per-session load.** Safe because forward-only discipline carries live items and the playbook is the durable gotcha net — switch-out verifies gotcha mirroring before commit (hardening after Test 1 found a five-day-old unmirrored gotcha).
- **conductor (session) + sherpa (lifecycle), split by timespan** — sherpa guides the multi-session climb, conductor keeps one session in tempo. "coach" rejected (too sporty); "sensei" rejected (collides with the sensei plugin, oversells).
- **A mode is a right-sizing contract, not an orchestration checklist**; skills are everyday tools. Kerd owns its modes — not a router over external skills (GSD removed v0.43.0; Superpowers distrusted as waterfall).
- **sherpa = one skill; Kerd stays one plugin.** Durable state in committed `kivna/sherpa.md` (one repo = one idea); `.active-modes` holds only a session pointer (session-ephemeral).
- **Validate is risk-driven, not menu-driven** — find the killer assumption, run the cheapest test of it, clear only the fatal risks. Design: `docs/plans/2026-06-29-validate-methods-toolkit.md`.
- **jit + spike stay standalone modes** (Tony needs jit for the dogfood); folding/retiring the rest of the prune list is deferred until the dogfood teaches us what the stages need.
- **Memory tools (claude-mem/mem0/mempalace/beads/agentmemory): adopt none** — they break git-portable handoff and human-first, and solve a retrieval problem Kerd doesn't have.
- **skriv voice profile: HELD** — don't wire until non-founder-genre samples exist (n=1: profile at `~/eolas/vault/people/Anthony Maley Voice.md`).
- **TODO is forward-only**; session history stays repo-side (`kivna/sessions/`), never the vault.

## Open Questions

- Dogfood shape: pick up Bree mid-lifecycle (past Explore) or take a fresh feature through the full climb?
- Should switch commit the vault repo? (`~/eolas/vault` is a separate git repo, ~20 uncommitted files; skill contract claims all git boundary ops, behavior doesn't commit it — contract and behavior disagree.)

## Active Mode

- **focus: on** in this repo — partner-mode working agreement: rapid back-and-forth, reasoning internal unless it changes Tony's decision, ONE speech-bubble question (no X/Y binaries), interrupt early, eyeball-gated slices. Enforced by a UserPromptSubmit hook; persisted user-global in `~/.claude`.
