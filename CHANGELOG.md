# Changelog

## 0.3.0

**Context checkpointing** — living `kivna/context.md` that captures working context (decisions, reasoning, rejected approaches, assumptions) and survives context compaction and session boundaries.

- Added `/kivna checkpoint` command — snapshots full working context to `kivna/context.md`, archives previous version to `kivna/checkpoints/YYYY-MM-DD.md`
- Updated dian: reads `kivna/context.md` in orient, auto-checkpoints at task boundaries during execute, finalizes context on close-out
- Updated switch: reads `kivna/context.md` on switch in, ensures it's current on switch out, offers to start a dian session on arrival
- Updated startup: scaffolds `kivna/context.md` skeleton and `kivna/checkpoints/` directory
- Added CHANGELOG.md

## 0.2.4

**SOTU audit fixes** — ran first full `/sotu all` audit and fixed all 11 findings.

- Normalized README slash-command prefixes to bare names throughout
- Added "project scaffolding" to plugin.json and marketplace.json descriptions
- Expanded CLAUDE.md Project Structure with full kivna layout
- Populated docs/playbook.md with real project content (was skeleton placeholders)

## 0.2.3

- Fixed missing command wrapper for startup skill
- Cache bust version bumps (0.2.1, 0.2.2)
- Fixed namespace prefix references in startup skill

## 0.2.0

**Playbook and startup** — three new features in one release.

- Added startup skill — one-time project scaffold for new repos
- Added playbook integration to dian — creates/updates `docs/playbook.md` on close-out
- Added playbook audit area to sotu — checks existence, accuracy, tech stack drift, setup validity, freshness, section completeness
- Updated README with all new skills and features

## 0.1.0

**Initial release** — five workflow skills.

- dian — session discipline (orient/plan/execute/close-out)
- switch — machine handoff (git pull on arrive, commit+push on leave)
- kivna — knowledge management (import, export, quick memory notes)
- sotu — project health audit (docs, code, site, deps)
- skriv — human writing voice enforcement (audit, fix, session mode)
- Plugin scaffolding and marketplace config
