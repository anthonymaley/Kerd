# Kerd

"Ceird" means skill in Gaelic. Respelled.

Twelve workflow skills plus community-contributed modes for Claude Code. Skills handle the operational side of working across sessions and machines: when to pull, what to commit, where to put notes, how to audit for drift, how to maintain structural health. Modes orchestrate skills from Kerd, Superpowers, and other plugins into guided flows for different types of work. They keep the plumbing clean so you can focus on the work.

## Install

```
claude plugins add-marketplace anthonymaley/Kerd
claude plugins install kerd
```

## What's New (v0.45.0)

### v0.45.0

**Tend now detects vault spine drift.** `/kerd:tend` Category 3 (vault integration) previously checked only for the MOC and Status.md. It now verifies the full spine (MOC + Status + **Weekly**), flags any vault-side `sessions/`-style folder (session history belongs in the repo, not the vault), and exempts Weekly.md from the append-only false-positive (its `## Week of` headers are by design). Detect-only — the fix points back at `kivna scaffold`, which owns vault writes. This completes the spine rollout from `docs/vault-spec.md` (kivna builds it, tend guards it). Second slice from dogfooding the `jit` mode.

### v0.44.0

**Kivna scaffold now builds the full spine + runs an intake interview.** `/kerd:kivna scaffold` previously created only a MOC and Status.md from repo state. It now creates the complete spine — MOC + Status + **Weekly.md** — seeded from a short *batched* intake interview (≤5 open questions in one round, reflect-back before writing). The MOC seeds purpose/success/constraints from the answers and links Weekly; Weekly is seeded with a ready skeleton, no invented content. This wires the spine convention from `docs/vault-spec.md` into the skill (drift detection in `tend` is the remaining step). Built by dogfooding the new `jit` mode.

### v0.43.0

**JIT mode + capturerequirements; GSD removed.** New `jit` mode for just-in-time MVP development: lock requirements by interview, write a thin spec, build the smallest valuable slice, show it, learn, revise — build what you need, not what you think you need. The new `/kerd:capturerequirements` skill is its front door: a fast one-question-at-a-time interview that locks MVP must-haves and defers the rest, lighter than interrogate's exhaustive readiness sweep. Separately, **GSD is fully removed** — `greenfield` now sequences Superpowers (`writing-plans`/`executing-plans`/TDD/verification/code-review) for spec-driven building instead, and GSD references are gone from mode/SKILL.md, state-contract.md, README, and the playbook.

### v0.42.0

**Focus** — New skill: `/kerd:focus on|off`. A per-repo toggle (default off) for a rapid, conversational working style — Claude keeps its reasoning to itself unless it changes your decision or it's stuck, asks short speech-bubble questions, and interrupts early instead of working alone then dumping. Off is the resting state so you keep seeing how the work gets made; flip it on to move fast. Enforced by a fourth opt-in hook (`UserPromptSubmit` → `hooks/focus.sh`) that injects the partner-mode reminder every prompt while focus is on, reading the repo's `kivna/.focus` flag. Five new harness tests; hooks now total 26.

> **Editorial note (2026-04-25):** The v0.34.0-v0.38.0 sequence below responded to a calibration failure observed in real-world spike work. A subsequent sensei review of the underlying A3 caught the critical limitation: **these releases ship better text rules + measurement infrastructure (genuine improvement at the existing granularity), not a fix to the granularity problem itself (the diagnosed root cause).** All the new rules live in markdown files read at turn-start — the same granularity the A3 identified as broken. The granularity gap remains open; closing it requires harness-level mechanisms (post-response hooks, output-format requirements) unavailable to skill files alone. See the vault `Kerd Skill Lessons.md` for the full recursive-trap analysis. Reading the entries below: take them as "more specific text rules + measurable baseline," not as a calibration fix.

### v0.40.0

**Switch** — Reframed around session handoff as the primary use: wrap up, commit, exit, and pick up cold in a fresh session with full context restored from disk. Moving between machines is the same mechanism, now the secondary case. Behavior unchanged; framing and triggers now match how switch is actually used day to day.

**Dian** — Slimmed to the disciplined middle of a session. Orient is now conditional: the warm path (after switch-in) re-reads nothing, the cold path does a light TODO + vault read. Close-out hands the boundary to switch — dian no longer calls `/kerd:kivna save`, updates the playbook, or runs diff review (switch owns the session log, vault save, and commit). Its unique core stays: task-framing, plan-approval, 3-fix limit, scope-creep stop, step-marker cadence. The execute-phase Claim Discipline gates are now self-contained (no longer assume a global CLAUDE.md). State-contract updated so switch is the sole caller of kivna save.

### v0.39.0

**Interrogate** — New skill: `/kerd:interrogate`. Produces a co-signed plan-readiness document by interviewing the user across every viability axis of a plan or idea (technical, business, legal, operational). Designed to prevent the convergence pull in normal brainstorming — verbose framing, premature multiple-choice, unilateral declarations of "done." Discipline anchored in user-veto on stop, mandatory frontmatter session state for deterministic resume, and a structural document check before recitation gate. Output lives at `docs/interrogations/YYYY-MM-DD-<topic>.md`. Does NOT produce the implementation plan itself — produces readiness; transition to `superpowers:writing-plans` after sign-off. Design at `docs/plans/2026-05-02-interrogate-design.md`.

### v0.38.0

**Slainte + tend** — Evidence-pointer discipline for audit findings. Each slainte finding now requires an `Evidence` column entry citing the specific check (file:line, command run with output, grep result, doc reference). Each tend failing/warning finding's "Why" cell must reference which check detected it AND include a verification step the user can run after the fix lands. Same shape as the global Claim Discipline "verified by [URL]" tag, applied to audit-shaped output. A finding without evidence is a claim without a source.

### v0.37.0

**Dian** — Five claim-discipline additions across all four phases. **Step-boundary markers** (`[dian: execute step N/M]`) fire 5-30 times per session within execute, where claim-level failures actually happen — phase markers alone fire 3-4 times, too coarse. **Pre-flight inventory** in orient asks for credentials/inputs/scope upfront so they don't trickle in mid-execute (5-10x friction multiplier). **Plan-step prediction citations** — predictions like "this will fix X" must cite a source or downgrade to "expected outcome — to be verified". **Strong-language gate during execute** sits in front of the existing verification gate; mid-step claims need evidence in the same loop iteration, not deferred to end-of-step. **Close-out summary discipline** applies the global Claim Discipline to TODO summary text. All five implement sensei's "discipline at the granularity of the failure" insight at every dian phase, not just at task completion.

**Global CLAUDE.md Claim Discipline section** (~/.claude/CLAUDE.md) — Five gates at claim-formation: strong-language vocabulary (downgrade absent ≥3 obs or citation), doc-fetch for external facts, verification-after-change, negative-result-to-systemic-cause, provisional-tagging default. Applies to all sessions, not just Kerd. Sourced from the parallel sensei A3; converged with spike v1.1's structural rules from a different methodology. Both interventions are hypotheses awaiting empirical measurement against the 33-42% confident-wrong baseline.

**Spike v1.2** — Three additions imported from a parallel TPS-A3 investigation (Toyota sensei skill ran the same retro on the same calibration failure and converged on the same fix shape). Strong-language gate adds an explicit downgrade vocabulary list — "verified", "definitively", "impossible", "always", "never", "private mechanism", "service-policy", "closed", "decline" — that requires ≥3 confirming observations OR a documented citation, otherwise downgrades to "tested but not yet verified". Tripwires fire mid-flow (not at close-out) when "✓ verified" is about to be written without retest, when strong-language vocabulary is used without citation, or when an architectural claim comes from 1-2 negative observations. Self-audit at close-out counts strong-language claims vs. citations against a measurable baseline (33-42% confident-wrong rate from the 3of3 spike) so we can tell whether the gates actually grip across sessions.

**Spike v1.1** — Six structural additions after first real-world dogfood. Setup gains pre-flight inventory (collect accounts/inputs/scope upfront — prevents trickle-in friction that compounds 5-10x mid-spike) and empirical-primitive-first (run the cheap ground-truth probe across the entire surface before guessing — AASA fetch for tvOS deep-links, curl for APIs, etc). Try gains per-variant verify (test-then-tag in the same loop iteration; no batched verification at close-out), provisional-decline zone (closure claims stay provisional until they survive a configuration change OR an explicit user push-back round, with required "what would change my mind" + "what I haven't yet tried" enumeration), WebFetch-fail-3-alternates (no general-knowledge guessing about external systems; each external claim carries a "verified by [URL]" tag), and matrix trimming (graduate-and-remove without prompting). All changes are structural — required artifacts and gates, not prose reminders.

**Spike** — New mode for high-uncertainty exploration. Directional but exploratory — no plan, no decomposition. Captures both wins AND losses with evidence in a per-topic spec file. Batch-hard for hardware/long-loop tests (default N+1 variants over what was asked). Commit graduation at close-out: each output classified as `keep-as-is`, `extract-and-promote`, or `discard` so working solutions are extractable for the real build. Includes a Removed-from-backlog log for disproven hypotheses.

**Dian** — Task framing before planning: decompose requests into scoped tasks with acceptance criteria and verification, approve boundaries, then plan implementation. Hard verification gate, 3-fix escalation limit, scope-creep stop, mode-aware orient and close-out. Default one task per session, fresh-session retry when framing was wrong.

**Switch** — Auto-commit session files without confirmation prompts. Only interrupts with a visible `⚠ INPUT REQUIRED` banner when unexpected files need a decision. Pre-commit summary with untracked file triage, handoff contract verification on arrival, evidence-cited completion banner. Three-level modifier: `full` → `light` → `low`.

**Trim** — New skill (community contribution from [Kwanwoo Lee](https://github.com/KwanwooLee63)). Post-feature cleanup: archive completed docs with forward-looking content rescue, prune stale CLAUDE.md blocks, clean memory, trim TODO.md. Safety-gated by haiku subagent.

**Lorg** — Tiered subcommands: `/lorg` defaults to Tier 1 (installed but unused), `/lorg available` for marketplace, `/lorg explore` for web, `/lorg all` for full scan. Per-tier freshness dates, incremental saves, cross-tier dedupe, signal-grounded explanations.

**Slainte** — Cross-doc claim verification: README descriptions vs SKILL.md behavior, playbook vs actual features, state-contract ownership table vs reality, hook template currency.

**Mode** — Resume/recovery protocol for stale or compacted context. Verifies coherence against git/session evidence before continuing.

**Kivna** — Do-not-save markers for private session content. Conversation-only, excluded from all vault writes.

**Infrastructure** — CONTRIBUTING.md contributor quality gate, mode-to-skill composition conventions, workflow ownership table in state-contract.md, opt-in hooks with absolute path resolution.

## Skills

### dian (Session Discipline)

Dian gives an open session structure. It runs *after* switch-in has loaded context (switch-in is the session-opener; dian is the disciplined middle), and walks through: orient (warm path — confirm the state switch-in just loaded; cold path — a light TODO + vault read if dian was invoked without switch-in), plan (decompose the request into scoped tasks with acceptance criteria, approve boundaries, then write concrete implementation steps), execute (do the work, verify each task with evidence before claiming done, escalate after 3 failed fixes), close out (update TODO, confirm docs are current, run checks, clear the session block, hand the boundary to switch). It writes the session plan to TODO.md and enforces scope: out-of-plan work goes to backlog immediately, no tangents. Default one task per session.

The project playbook (`docs/playbook.md`) — a living guide for rebuilding the project from scratch: tech stack, setup, architecture, integrations, gotchas, status — is updated as behavior changes (docs travel with code during execute), and switch captures session gotchas into it at the boundary. It grows with the project, session by session.

During execution, decisions accumulate in TODO.md. Dian doesn't touch the vault or write session logs — those are boundary operations switch owns. At close-out dian updates TODO.md and hands off; switch then writes the session log and calls `/kivna save` once to update the vault, one clean write per session, not ten incremental dumps.

Dian is mode-aware: if a mode is active, orient reports the mode context and instruction, the plan respects the mode's scope, and close-out doesn't claim the session is done when running as part of a larger mode flow.

Dian announces its current phase with a mode marker (`[dian: orient]`, `[dian: execute]`, etc.) so you always know what's active. When the session closes, it outputs `[dian: closed]` so there's no ambiguity.

Dian doesn't touch git. No pulls, no pushes. That's switch's job.

```
/dian
```

### interrogate (Plan Readiness)

Interrogate produces a co-signed plan-readiness document by interviewing you across every viability axis of a plan or idea: technical, business, legal, operational. It's built to resist the convergence pull in normal brainstorming — verbose framing that buries the question, premature multiple-choice that narrows the answer space, unilateral declarations of "done" before you've signed off. Discipline is anchored in three places: user-veto on stop (only you can end the interview), mandatory frontmatter session state so a fresh session can resume deterministically, and a structural document check before recitation so the model can't claim coverage that isn't on the page.

Run it with no argument for a zero-path interview (start from an idea), or pass a plan reference to interrogate an existing draft. Output lives at `docs/interrogations/YYYY-MM-DD-<topic>.md`. Interrogate does not produce the implementation plan itself — it produces readiness. After sign-off, transition to `superpowers:writing-plans` to draft the plan.

Design at `docs/plans/2026-05-02-interrogate-design.md`.

```
/kerd:interrogate              # zero-path: interview from an idea
/kerd:interrogate <plan-ref>   # interrogate an existing plan draft
```

### capturerequirements (Requirements Capture)

Capturerequirements is the fast, interview-based front door to building — the Reqs step of the jit mode. It interviews you one question at a time to lock the MVP must-haves, names what's explicitly *not* now, and stops as soon as the first slice is clear. It is deliberately lighter than interrogate: where interrogate exhaustively stress-tests viability across every axis and co-signs a readiness document, this just gets you moving. The principle is build-what-you-need: anything you can't tie to the core outcome goes to **Later**, not into the build. Output is a short note at `docs/requirements/YYYY-MM-DD-<topic>.md` that the jit loop revises as you learn — a starting point, not a contract.

Use interrogate when the cost of being wrong is high; use capturerequirements when the cost of not starting is high.

```
/kerd:capturerequirements      # interview to lock MVP must-haves
```

### switch (Session Handoff)

Switch owns git boundary operations. All of them. The primary use is session handoff: you wrap up at a clean point, exit, and start fresh later with full context restored from disk. The same operations carry across machines as the secondary case. When you wrap up a session, it reflects on the session (capturing gotchas and learnings), writes session state to TODO.md, creates a session log in `kivna/sessions/` with branch metadata, then shows a pre-commit summary of what's about to ship. Untracked files get triaged (commit, gitignore, or leave) so nothing drifts silently. The final confirmation cites evidence: commit hash, push target, clean tree status. When you pick up a session, it pulls, verifies the handoff was complete (checks TODO.md and session log for expected sections, flags partial handoffs), runs a smoke test if tests exist, reads the most recent session log in full (older logs get skimmed for key decisions and gotchas), and tells you where you left off. It also reads vault Status.md and reports any active modes left from a previous session. Switch keeps `TODO.md` forward-only: at switch-out it overwrites the Current Session block (completed work lives in the dated `kivna/sessions/` log, not TODO) and self-heals any accumulated `## Previous Session` blocks by archiving them to the session logs.

If you run it without arguments, it checks for uncommitted changes. Changes present means you're leaving. Clean repo means you're arriving. Add `light` to skip vault operations, reflection, and smoke tests for a faster handoff with lower token cost.

```
/switch out          # full wrap-up (vault, reflection, commit, push)
/switch out light    # quick wrap-up (TODO + session log, commit, push)
/switch out low      # minimum viable handoff (brief TODO, skeleton log, push)
/switch in           # full pickup (pull, vault, smoke test, session logs)
/switch in light     # quick pickup (pull, TODO, session log)
/switch in low       # minimum viable pickup (pull, TODO current session, what's next)
```

### kivna (Knowledge Management)

Kivna owns the project's knowledge layer, stored in an Obsidian vault at `~/eolas/vault/[project]/`. The vault is a human knowledge base. Every file answers a question someone would actually ask. No symlinks, no append-only logs, no session dumps. Files are living, updated in place with approval.

Save (`/kivna save`) updates the vault's Status.md, updates the Weekly tracker (achievements and risks by week for quick status report generation), and proposes updates to other vault files (Architecture Decisions, Playbook, etc.), each change shown and approved before writing. This is the same save mechanic switch uses at the session boundary. Scaffold (`/kivna scaffold`) creates the vault folder and the spine — MOC, Status.md, and Weekly.md — seeded from a short batched intake interview (≤5 open questions, one round), then suggests what other files might fit the project. Import (`/kivna in`) reads files from `kivna/input/` and integrates relevant knowledge, including structured `.kif.json` imports. Export (`/kivna out`) produces two files: `.kif.toon` (token-efficient for LLM handoff) and `.kif.json` (machine-parseable for cross-project import). Exports are repo-grounded: TODO.md, session logs, playbook, and vault status are read first, with conversation context filling gaps.

The folder structure:

```
kivna/
  vault.json   # vault config (points to ~/eolas/vault/[project]/)
  sessions/    # session logs from switch (committed)
  input/       # drop files here for import (gitignored)
  output/      # exports land here (gitignored)
```

```
/kivna in                                          # import from inbox (.kif.json, .md, .pdf, etc.)
/kivna out                                         # export as .kif.toon + .kif.json
/kivna out --full                                  # export all sections (adds playbook, architecture, memory, mode)
/kivna save                                        # update vault
/kivna scaffold                                    # set up Obsidian vault
```

### slainte (Project Health)

Slainte audits project health across six areas: docs, code, site, deps, playbook, and release. It reads a `.slainte` config file at the project root to know what to check. Each area has specific checks. Docs gets cross-referenced against CLAUDE.md, scanned for stale names and broken links. Code runs tests and the build. Deps checks for outdated packages and security issues. Playbook checks whether `docs/playbook.md` exists, whether its Current Status is accurate, whether the tech stack listed still matches reality, and whether setup steps still point to files that exist. Release (Kerd-specific) catches version sync drift, description mismatches, skill/mode count claims, namespace prefix issues, and marketplace URL changes.

Everything gets a severity grade: high (factually wrong, broken build, security vulnerability), medium (stale but not misleading), low (nitpick). Slainte reports problems. It doesn't fix them.

```
/slainte              # show current config
/slainte add docs README.md   # register a target
/slainte docs         # audit docs area
/slainte playbook     # audit the playbook
/slainte release      # audit version sync, counts, namespaces (Kerd repos)
/slainte all          # audit everything
```

### skriv (Writing Voice)

Skriv enforces a human writing voice. It has a kill list of words no one actually uses in conversation (leverage, facilitate, delve, holistic, the whole lot), bans all dashes as punctuation (em, en, and double hyphens) along with five-paragraph essay structure, catches synonym cycling and chatbot residue, and runs a self-audit ("what still sounds machine-made?") before cutting 20%. The goal is prose that reads like a first draft by someone who's been in the room, not something generated.

Three modes. Audit reviews a file and reports violations with line numbers. Fix rewrites the file in place. Session mode applies the rules to everything you write for the rest of the conversation. When session mode is on, skriv shows `[skriv: active]` at the top of responses and `[skriv: off]` when it ends.

```
/skriv README.md       # audit against the rules
/skriv fix README.md   # rewrite applying the rules
/skriv on              # session mode on
```

### tend (Structural Health)

Tend audits repo infrastructure against current Kerd conventions and fixes what's drifted. Run it on a new repo to set up everything from scratch, or on an existing repo to catch drift after a Kerd update. It checks nine categories: directory structure, required files, vault integration, deprecated patterns, naming consistency, stray/stale files, .gitignore hygiene, skill hygiene, and hook hygiene.

The report shows each category as passing (✓), failing (✗), or warning (⚠). Failing and warning items get a current-vs-proposed table with reasons. After the report, choose to fix all, pick individually, or skip. Tend makes changes but never commits. Switch owns that boundary.

```
/tend
```

### lorg (Skill Gap Analysis)

Lorg scans the current project and recommends skills or plugins you should be using but aren't. It works in three tiers, each runnable independently. Tier 1 checks what's already installed but underused (not invoked in the last 30 days). Tier 2 searches the Claude Code marketplace and a curated list of repos you maintain for plugins that fit your project's tech and themes. Tier 3 goes wider: GitHub and web search for trending or new plugins you haven't heard of yet.

The default (`/lorg`) runs Tier 1 only: fast, cheap, no web dependency, most actionable. Use subcommands for wider search. Each tier tracks its own freshness date, and running one tier preserves the others in the report.

The recommendations aren't just based on file types. Lorg reads your README, playbook, TODO, session logs, and vault decisions to extract work themes (fundraising, compliance, content creation, whatever keeps coming up). Results are ranked by relevance (theme match + tech match + recency boost - install friction) so the strongest matches appear first. Weak matches below a threshold are dropped.

The report is saved to `docs/lorg-report.md` (committed) and the Obsidian vault (searchable). Updates are incremental: only scanned tiers get overwritten.

```
/lorg                # Tier 1 only (installed but unused)
/lorg installed      # same as default
/lorg available      # Tier 2 (marketplace + curated sources)
/lorg explore        # Tier 3 (GitHub + web). Opt-in research.
/lorg all            # full scan across all tiers
/lorg report         # show last saved report
```

### trim (Token Optimization)

Trim keeps active context lean. Run it after every feature ships. It archives completed spec and plan docs, prunes stale CLAUDE.md guidance blocks, cleans up project memory entries that are no longer actionable, and removes checked-off TODO items. Before archiving any doc, trim rescues forward-looking content — deferred tasks, future phase notes, known limitations, and cross-cutting concerns — into `docs/deferred.md` so nothing project-relevant gets buried. A safety gate (haiku subagent) verifies that `/switch in` would still have all the context it needs before anything is finalized.

```
/trim
```

### mode (Workflow Routing)

Mode routes you to the right tools for the type of work you're doing. Each mode is a session configuration: it checks which skills are installed, auto-discovers extras from your plugins, and presents a customizable flow grouped by phase. You enable or disable steps interactively, add session instructions (narrow scope, set constraints, output preference), then the mode tracks your progress and resurfaces your instructions at each step.

Modes orchestrate across toolkits. A greenfield mode sequences Superpowers for spec-driven building, TDD, and code review, and Kerd for session boundaries. A jit mode locks requirements by interview, then loops smallest-slice builds. A strategy mode loads skriv for writing voice and brainstorming for exploration. Modes don't call skills directly. They guide you through the flow and remind you what's next.

Eleven starter modes ship with Kerd. Community members can contribute new modes by PRing a single markdown file to the `modes/` directory.

| Category | Modes |
|----------|-------|
| Development | `greenfield`, `jit`, `quickfix`, `spike`, `deepwork`, `maintain` |
| Business | `strategy`, `writing`, `research` |
| Operations | `legal`, `sales` |

```
/mode                # list all modes by category
/mode greenfield     # start the greenfield flow
/mode maintain       # start the maintenance flow
```

### focus (Partner Mode)

Focus toggles how you and Claude work together. Off by default — the full, show-your-reasoning style stays the resting state so you keep learning. Turn it on to move fast: Claude keeps its thinking internal (surfacing it only when it changes your decision, it's stuck, or you ask), asks one clear speech-bubble question at a time, interrupts early to flag or check in, and works like someone sitting beside you rather than narrating every step. It's per-repo state (`kivna/.focus`), enforced by an opt-in `UserPromptSubmit` hook that re-injects the partner-mode reminder each prompt while on. Focus governs interaction style only — your `CLAUDE.md` thinking discipline applies either way.

```
/focus on            # rapid partner mode
/focus off           # back to full reasoning
/focus               # show current state
```

## Hooks

Kerd ships four opt-in hooks that provide session boundary awareness and the focus toggle. They are not active by default. Run `/tend` to register them in your local settings.

**Stop hook:** When a session ends with uncommitted changes or an active mode, prints a one-line reminder to run `/switch out`. Silent when the repo is clean.

**SessionStart hook:** On same-machine resume, checks if the local branch is behind remote, reads the last session date from TODO.md, and reports any interrupted mode. Suggests `/switch in` when there's stale state. Silent on a fresh start.

**Skill completion hook:** When a mode is active and you complete the current step's skill, shows your progress and what's next. Read-only — the mode skill handles state transitions.

**Focus hook (`UserPromptSubmit`):** While focus is on for the repo (`kivna/.focus` = `on`), injects the partner-mode reminder into every prompt. Silent when focus is off or absent. See the focus skill above.

```
/tend                # registers hooks in .claude/settings.local.json
```

The four hooks are covered by a bash test harness, `tests/hooks_test.sh` (26 tests: path resolution under unset/empty `CLAUDE_PROJECT_DIR`, missing-file branches, behind-remote detection, the SessionStart staleness report, and the focus toggle's on/off/absent branches). Run `bash tests/hooks_test.sh` — it shellcheck-lints the hooks as part of the run.

## How They Fit Together

**Starting a project:** Create a repo, clone it, run `/tend`. It checks what's missing, shows you the plan, and sets up the full structure with your approval. Run `/lorg` to find plugins that fit your stack. Then `/dian` to start your first session.

**Picking a workflow:** Before diving in, run `/mode` to see what's available. If you're building something new, `/mode greenfield` sequences you through spec writing, planning, execution, and review. Fixing a bug? `/mode quickfix` strips the ceremony down to the essentials. Writing a blog post or strategy doc? `/mode writing` or `/mode strategy` loads the right tools (skriv for voice, brainstorming for exploration). The mode presents each phase as an interactive selection where you enable or disable steps, then asks for session instructions (narrow the scope, set constraints, pick an output format). Once you confirm, it tracks progress and resurfaces your instructions at each step.

**Day to day:** You sit down at your laptop and run `/switch in`. It pulls, reads the session logs, tells you what happened last time. It reads vault Status.md (where the project stands and what's next) plus any other vault files relevant to the work. If a mode was active when you left, switch tells you where you were in the flow. Then it offers to start a dian session. You run `/dian` to plan the session. Work happens, decisions get recorded in session logs and TODO.md. When the work is done, dian's close-out updates TODO.md and hands the boundary back to switch. You run `/slainte docs` to check nothing drifted. Then `/switch out` writes the session log, calls `/kivna save` to update the vault (one clean write with approval), commits, and pushes. Next session, same state, whether you pick up in a fresh session on this machine or on another. Periodically run `/lorg` to check if new skills have emerged that would help with the project.

**Quick sessions:** Use the `light` modifier when token cost matters. `/switch in light` skips vault reads and smoke tests, `/switch out light` skips vault saves and reflection. You still get TODO.md, session logs, and git operations. Full context when you need it, lightweight handoff when you don't.

**The layers:** Switch owns git boundaries. Dian owns session discipline. Kivna owns the knowledge vault. Mode sits above all of them, routing you to the right combination based on what you're doing. You can use any skill standalone, but mode ties them into a coherent flow.

## Naming

Gaelic-inspired where it adds character:
- **Kerd**: skill (ceird)
- **Kivna**: memory (cuimhne)
- **Dian**: intense, rigorous
- **Skriv**: the act of writing (scríobh)
- **Switch**: session handoff
- **Slainte**: health (slàinte)
- **Tend**: from English "to tend" (care for, maintain)
- **Lorg**: to seek, track down
- **Trim**: from English "to trim" (cut away excess)

## License

MIT
