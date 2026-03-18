# Changelog

## 0.14.0

**Weekly tracker and switch rename.**

Weekly tracker: Kivna save now updates a `[Name] Weekly.md` file in the vault, tracking achievements and risks by week. Reverse chronological, `[open]`/`[mitigated]` risk markers.

Switch renamed back from shakh. No actual superpowers collision existed. Slainte and lorg stay Gaelic.

- Added step 3 to Kivna save mechanic: update Weekly.md
- Added Weekly file type to vault spec
- Renamed skill shakh → switch (directory, SKILL.md, all cross-references)
- Updated README, CLAUDE.md, playbook, tend, dian, kivna

## 0.11.0

**Skill rename.** Three skills renamed to Gaelic to avoid collisions with superpowers plugin.

- Renamed sotu → slainte (from Irish "slàinte," health)
- Renamed switch → seach → shakh (from Gaelic "seachad," to hand over. Respelled for voice tools)
- Renamed discover → lorg (from Gaelic "lorg," to seek)
- Config file `.sotu` renamed to `.slainte`
- Old `.sotu` added to tend's deprecated patterns

## 0.10.1

**Skriv dash rule.** Expanded to ban all dashes as punctuation (em, en, double hyphens), then applied across every living file.

## 0.10.0

**Vault redesign.** Human knowledge base, not machine sync layer.

- Rewrote kivna: scaffold creates MOC + Status.md only (no symlinks, no Context.md/Log.md/Decisions.md), save overwrites Status.md with approval and proposes updates to domain files
- Updated dian: orient reads Status.md + MOC, execute has no vault writes, close-out calls `/kerd:kivna save` once
- Updated switch: in reads Status.md + MOC, out delegates vault writes to `/kerd:kivna save`
- Updated tend: vault audit flags symlinks and generic filenames as violations, checks MOC link resolution, detects append-only remnants
- Added vault spec at `docs/vault-spec.md`, the canonical reference for vault philosophy and file types
- Added vault redesign design doc at `docs/plans/2026-03-15-vault-redesign.md`

## 0.9.2

- Kivna save now refreshes the vault MOC (`[Name].md`). Updates version, skill table, symlinks, and section links so the MOC never drifts

## 0.9.1

- Changed default vault path from `~/ObsidianLLM/` to `~/Obsidian/`, later to `~/eolas/vault/`
- Updated kivna scaffold to ask for vault location if `~/eolas/vault/` doesn't exist
- Added vault advisory to tend Category 3. Explains what the vault is and how to set it up
- Updated all skill references, README, and playbook

## 0.9.0

**Discover.** Skill gap analysis for projects.

- Added discover skill. Scans project signals (tech stack + work themes) and recommends skills/plugins across three tiers: installed but unused here, available in marketplace/curated sources, trending on GitHub/web
- Rich card report format with descriptions, relevance, and actionable prompts per item
- Curated source list in Obsidian vault (`discover-sources.json`) syncs between machines

## 0.8.0

**Tend replaces startup.** Structural health check and convergence.

- Added tend skill. Audits repo structure against current Kerd conventions, reports visually with current-vs-proposed tables, fixes with approval
- Removed startup skill. Tend covers both initial setup and ongoing drift detection
- Seven audit categories: directory structure, required files, vault integration, deprecated patterns, naming consistency, stray/stale files, .gitignore hygiene

## 0.7.0

**Obsidian vault integration.** Kivna now reads and writes the Obsidian vault as the single source of truth for context, decisions, and activity logging.

- Rewrote kivna: vault discovery (`kivna/vault.json`), `/kivna save` writes to vault `Context.md`, `Log.md`, and flags decisions for `Decisions.md` approval
- Added `/kivna scaffold`. Sets up the Obsidian vault folder with symlinks, MOC, Context, Log, and Decisions files
- Updated dian: orient reads vault Context.md and Decisions.md, execute/close-out save to vault
- Updated switch: in reads vault, out reflection flags decisions for vault Decisions.md
- Updated startup: scaffolds `kivna/vault.json` and triggers `/kerd:kivna scaffold` instead of creating `kivna/context.md`
- Removed `kivna/context.md`, `kivna/checkpoints/`, `kivna/memories/` (replaced by vault files)
- Removed legacy command wrappers in `commands/` (plugin system loads skills directly via `kerd:` prefix)

## 0.6.0

**Strengthened dian and switch.** Rigorous planning, verify-as-you-go execution, and session reflection.

- Dian orient: consistency sniff test across CLAUDE.md, playbook, and context
- Dian plan: interrogate tasks, push back on ambiguity, don't infer
- Dian execute: verify each task before moving on, record decisions immediately, docs travel with code
- Dian close-out: diff review of all session changes
- Switch out: reflection step captures learnings to CLAUDE.md, memory, and playbook
- Switch in: smoke test runs project tests if they exist

## 0.5.0

**Mode markers.** Visible phase/state announcements for modal skills.

- Dian announces current phase (`[dian: orient]`, `[dian: execute]`, etc.)
- Skriv announces session mode (`[skriv: active]`, `[skriv: off]`)
- Added `kivna/.active-modes` state file for cross-skill mode tracking
- Switch in reads and reports active modes

## 0.4.0

**Simplified kivna commands.** Merged `/kivna checkpoint` and `/kivna memory` into a single `/kivna save` command.

- `/kivna save` snapshots full working context to `kivna/context.md` (same mechanic dian uses at task boundaries)
- `/kivna save <note>` does the snapshot plus appends the note to `kivna/memories/YYYY-MM-DD.md`
- Removed `/kivna checkpoint` and `/kivna memory` as separate commands
- Updated dian and switch to reference `/kivna save` instead of `/kivna checkpoint`

## 0.3.1

**Switch session log template.** Added `## Insights` section between Key Decisions and What's Next.

## 0.3.0

**Context checkpointing.** Living `kivna/context.md` that captures working context (decisions, reasoning, rejected approaches, assumptions) and survives context compaction and session boundaries.

- Added `/kivna checkpoint` command. Snapshots full working context to `kivna/context.md`, archives previous version to `kivna/checkpoints/YYYY-MM-DD.md`
- Updated dian: reads `kivna/context.md` in orient, auto-checkpoints at task boundaries during execute, finalizes context on close-out
- Updated switch: reads `kivna/context.md` on switch in, ensures it's current on switch out, offers to start a dian session on arrival
- Updated startup: scaffolds `kivna/context.md` skeleton and `kivna/checkpoints/` directory
- Added CHANGELOG.md

## 0.2.4

**SOTU audit fixes.** Ran first full `/sotu all` audit and fixed all 11 findings.

- Normalized README slash-command prefixes to bare names throughout
- Added "project scaffolding" to plugin.json and marketplace.json descriptions
- Expanded CLAUDE.md Project Structure with full kivna layout
- Populated docs/playbook.md with real project content (was skeleton placeholders)

## 0.2.3

- Fixed missing command wrapper for startup skill
- Cache bust version bumps (0.2.1, 0.2.2)
- Fixed namespace prefix references in startup skill

## 0.2.0

**Playbook and startup.** Three new features in one release.

- Added startup skill for one-time project scaffold for new repos
- Added playbook integration to dian. Creates/updates `docs/playbook.md` on close-out
- Added playbook audit area to sotu. Checks existence, accuracy, tech stack drift, setup validity, freshness, section completeness
- Updated README with all new skills and features

## 0.1.0

**Initial release.** Five workflow skills.

- dian: session discipline (orient/plan/execute/close-out)
- switch: machine handoff (git pull on arrive, commit+push on leave)
- kivna: knowledge management (import, export, quick memory notes)
- sotu: project health audit (docs, code, site, deps)
- skriv: human writing voice enforcement (audit, fix, session mode)
- Plugin scaffolding and marketplace config
