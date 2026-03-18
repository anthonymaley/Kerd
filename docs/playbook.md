# Playbook: Kerd

How to rebuild this project from scratch.

## Tech Stack

Pure markdown and JSON. No runtime dependencies, no build step, no package manager.

- **Claude Code plugin system**: skills (SKILL.md), plugin manifest (plugin.json/marketplace.json)
- **Markdown**: all skill definitions, docs, session logs, and the playbook itself
- **JSON**: plugin.json and marketplace.json in `.claude-plugin/`
- **Git**: version control and the distribution mechanism (plugins install from the git repo)

There is no package.json, no node_modules, no compiled output. The plugin is consumed directly by Claude Code from the repo.

## Setup

1. Clone the repo:
   ```
   git clone git@github.com:anthonymaley/Kerd.git
   cd Kerd
   ```

2. That's it. There's no install step. The project is markdown and JSON files consumed by Claude Code's plugin system.

3. To test locally, install the plugin in Claude Code:
   ```
   claude plugins install /path/to/Kerd
   ```

4. To install from the marketplace (published version):
   ```
   claude plugins add-marketplace anthonymaley/Kerd
   claude plugins install kerd
   ```

## Architecture

**Skills define behavior.** The plugin system loads them directly via the `kerd:` prefix (e.g., `/kerd:dian`).

Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`) and the full protocol in markdown. The `description` field controls when Claude auto-invokes the skill.

The plugin manifest (`.claude-plugin/plugin.json`) declares the plugin name, version, and description. The marketplace manifest (`.claude-plugin/marketplace.json`) wraps that for the Claude Code marketplace.

**Directory layout:**
```
skills/           # SKILL.md per skill (dian, lorg, kivna, skriv, slainte, tend, seach)
docs/plans/       # historical design docs
docs/playbook.md  # this file
kivna/vault.json  # Obsidian vault config
kivna/sessions/   # session logs written by seach
kivna/.active-modes # ephemeral mode state
.claude-plugin/   # plugin.json + marketplace.json
```

The project's knowledge layer lives in the Obsidian vault at `~/eolas/vault/kerd/`. The vault is a human knowledge base, living files updated in place, not append-only dumps. Kivna reads and writes vault files (`Kerd Status.md`, plus optional domain files like Architecture Decisions). The vault spec at `docs/vault-spec.md` defines what belongs. The vault config is at `kivna/vault.json`. See `/kerd:kivna` for details.

**Seven skills, each with a single responsibility:**
- **dian**: session discipline (orient/plan/execute/close-out protocol)
- **lorg**: skill gap analysis (scan project signals, recommend skills/plugins across tiers)
- **seach**: git boundary operations (pull on arrive, commit+push on leave)
- **kivna**: knowledge management (Obsidian vault: living Status.md, domain knowledge files, import/export)
- **slainte**: project health audits (docs, code, site, deps, playbook)
- **skriv**: human writing voice enforcement (audit, fix, session mode)
- **tend**: structural health check and convergence

## Integrations

No external services or APIs. Kerd operates entirely within the local filesystem and git.

The only integration point is the **Claude Code plugin system**. Kerd registers as a plugin and its skills become available as slash commands (`/kerd:dian`, `/kerd:seach`, etc.).

Session logs written by seach go to `kivna/sessions/` and are committed to git, making them available across machines.

## Deployment

Kerd is distributed as a Claude Code marketplace plugin.

**To publish an update:**
1. Make changes to skills and docs
2. Bump the version in all three locations per the release checklist in CLAUDE.md:
   - `.claude-plugin/plugin.json` → `version`
   - `.claude-plugin/marketplace.json` → `metadata.version`
   - `.claude-plugin/marketplace.json` → `plugins[0].version`
3. Commit and push to `main`
4. Users get the update on next `claude plugins install kerd`

No CI/CD pipeline, no build artifacts, no environment variables.

## Gotchas

- **Version sync**: the version must be identical in three places (plugin.json version, marketplace.json metadata.version, marketplace.json plugins[0].version). Easy to update one and forget the others. The release checklist in CLAUDE.md exists because this happened.
- **Cache busting**: after publishing, Claude Code may cache the old plugin version. Bumping a patch version forces a re-fetch. This is why you see "cache bust" commits in the history.
- **Namespace prefix**: skill SKILL.md frontmatter uses bare names (`name: dian`), but all references in docs and skills must use `kerd:` prefix (`/kerd:dian`). The plugin system adds the prefix automatically. README examples are exempt for readability.
- **Vault path convention**: default vault path is `~/eolas/vault/`. Kivna scaffold asks for the location if it doesn't exist. All vault.json files point here. If you rename or move the vault folder, update vault.json in every repo.
- **Vault spec**: the vault spec at `docs/vault-spec.md` defines what belongs in the vault. No symlinks, no append-only files, no generic filenames. When in doubt, check the spec.
- **Cross-cutting changes**: when modifying a pattern used across multiple skills (like vault file references), grep all skill files for the old pattern after implementation. The plan will miss files. The v0.10.0 vault redesign missed `lorg/SKILL.md` entirely, caught only by final code review searching for stale references.
- **Agent verification**: when using parallel agents for cross-file changes, always run a grep verification sweep afterward. Agents can make incorrect inferences (e.g., renaming `discover-sources.json` to `lorg-sources.json` when only the skill name changed, not the vault filename).


## Current Status

**Version:** 0.11.0

**Working:**
- All seven skills functional: dian, lorg, seach, kivna, slainte, skriv, tend
- Plugin installs from marketplace
- Session logs, playbook creation, and health audits all operational
- Obsidian vault integration. Kivna reads/writes living vault files (Status.md, domain knowledge) with approval-gated overwrites
- Tend audit verified. Reports structural drift and fixes with approval
- Dian playbook creation verified. Skeleton matches expected template
- Mode markers on dian and skriv. Visible phase/state announcements with `.active-modes` state file
- Dian rigorous planning (interrogate tasks, push back, no guessing) and execute verification (check each task, record decisions immediately, docs with code)
- Seach-out reflection. Captures learnings to CLAUDE.md and memory files
- Seach-in smoke test. Runs project tests if they exist

**Recent changes (as of 2026-03-17):**
- v0.11.0: Renamed three skills to Gaelic to avoid collisions with superpowers plugin: sotu to slainte, switch to seach, discover to lorg. Config file `.sotu` renamed to `.slainte`.
- v0.10.1: Expanded skriv dash rule to ban all dashes as punctuation (em, en, double hyphens). Cleaned all living files.
- v0.10.0: Vault redesign. Living human-readable files replace append-only dumps, no symlinks, approval-gated Status.md overwrites, vault spec at docs/vault-spec.md
- v0.9.0: Lorg. Skill gap analysis, scans project signals and recommends skills/plugins across three tiers
- v0.8.0: Tend replaces startup. Structural health check and convergence for new and existing repos, seven audit categories, visual report with fix flow

**Next:**
- Run `/kerd:tend` on other projects to migrate vaults
- Test slainte playbook audit on a project with a playbook
- Consider adding version bumping to the seach-out process
