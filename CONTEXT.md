# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills plus community modes. Core skills: switch (session handoff/boundary), conductor (session discipline), sherpa (idea lifecycle PM), kivna (vault/knowledge), tend, trim, slainte, skriv, lorg, interrogate, pair, capturerequirements. At v0.60.0 (context/history split).

## Where We Are

Two live threads:

1. **Kerd core stable at v0.64.0.** The context/history split (v0.60) is shipped and in daily use — state=CONTEXT.md / work=TODO.md / history=kivna/sessions/, switch-in reads exactly those three. Conductor's model-tiered delegation is now shaped as a **model-advisory gate** (v0.64): it advises the driving model the task needs, gates on the user confirming/switching, then right-sizes `[delegate]` steps with a sized `model`+`effort` tag. This superseded the v0.62 `fable on|off` toggle and v0.63 effort-hint (git + session logs hold that history). Same release renamed `focus` → `pair` (the Claude Code harness has its own native focus mode). **Cache caveat:** `/kerd:pair` and the new conductor behavior only take effect once the installed plugin cache updates to 0.64.0 — the dev repo is the source, the cache lags.
2. **Sherpa dogfood (carried).** The full Explore→Validate→Plan→Build→Launch lifecycle is functional (v0.46.0–v0.49.0), `dian` renamed `conductor` (v0.59.0), but the stages have never run live. Dogfood target: `~/Bree` (personal-health-OS app, mid-Build) — in that repo, fresh session, after Tony updates the stale plugin cache.

## Key Decisions

- **Conductor: model advisory replaces the `fable` toggle** (2026-07-11, v0.64.0): the `/kerd:conductor fable on|off` toggle is **removed**. A skill can't read or set its own model, so conductor doesn't detect or assert it — right after orient it sizes the task, **advises the driving model** the work needs (mechanical → current model fine; hard/architectural/judgment-heavy → top-tier Opus/Fable), and **gates**: user switches to it or confirms before planning. Delegation is then conductor's default right-sizing, not an opt-in: if the task has mechanical bulk it writes a spec file; steps are tagged `[keep]` (driving model does inline; was `[fable]`) or `[delegate]`, and each `[delegate]` step carries a **sized model + effort in the tag** (`[delegate, model: haiku, effort: low]` … `[delegate, model: sonnet, effort: high]`) approved at the plan gate. Small/all-judgment tasks skip the spec and run lean inline. Supersedes the v0.62.0 explicit-toggle decision and the v0.63.0 effort-hint (effort now lives in the sized tag alongside model). **The spec is the contract** stays — a vague `[delegate]` step yields a confidently-wrong build; spec quality is the safety mechanism. Provenance of the tiering idea: a friend's Fable workflow; its compact/checkpoint ideas were **rejected** — switch owns boundaries, conductor never manages context or compacts.
- **Multiple-choice questions are a quality bar, not a ban** (2026-07-06): offer options only when they *clarify* a real choice that's the user's to make (2-4 crisp, distinct options) — never a lazy binary that offloads a call Claude should make, never vague or verbose. Lives in the pair hook now; a ready-to-drop phrase for promoting it to global `~/.claude/CLAUDE.md` sits in the backlog.
- **Switch-in Summarize ends with a numbered pick-list** (2026-07-06): the full `## Now` + `## Backlog`, one terse line each, so the user picks by number or steers. No truncation (TODO is lean by design), no reply-hint.
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
- Surface model-tiered delegation in the top-level plugin capability list (plugin.json / marketplace.json `description`), or leave "session discipline" to subsume it? Still unsurfaced as of v0.64.0 pending a call.

## Active Mode

- **pair: on** in this repo — partner-mode working agreement: rapid back-and-forth, reasoning internal unless it changes Tony's decision, ONE speech-bubble question (no X/Y binaries), interrupt early, eyeball-gated slices. Enforced by a UserPromptSubmit hook (`hooks/pair.sh`, reading `kivna/.pair`); persisted user-global in `~/.claude`. (Renamed from `focus` in v0.64.0.)
