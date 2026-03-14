# Playbook — Kerd

How to rebuild this project from scratch.

## Tech Stack

Pure markdown and JSON. No runtime dependencies, no build step, no package manager.

- **Claude Code plugin system** — skills (SKILL.md), commands (markdown wrappers), plugin manifest (plugin.json/marketplace.json)
- **Markdown** — all skill definitions, docs, session logs, and the playbook itself
- **JSON** — plugin.json and marketplace.json in `.claude-plugin/`
- **Git** — version control and the distribution mechanism (plugins install from the git repo)

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

**Skills define behavior. Commands are thin wrappers that invoke skills.**

Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`) and the full protocol in markdown. The `description` field controls when Claude auto-invokes the skill.

Each command lives in `commands/<name>.md` and simply tells Claude to invoke the corresponding skill. One command per skill, one-to-one mapping.

The plugin manifest (`.claude-plugin/plugin.json`) declares the plugin name, version, and description. The marketplace manifest (`.claude-plugin/marketplace.json`) wraps that for the Claude Code marketplace.

**Directory layout:**
```
skills/           # SKILL.md per skill (dian, kivna, skriv, sotu, startup, switch)
commands/         # one .md per command (thin wrappers)
docs/plans/       # historical design docs
docs/playbook.md  # this file
kivna/vault.json  # Obsidian vault config
kivna/sessions/   # session logs written by switch
kivna/.active-modes # ephemeral mode state
.claude-plugin/   # plugin.json + marketplace.json
```

The project's durable knowledge layer lives in the Obsidian vault at `~/ObsidianLLM/kerd/`. Kivna reads and writes vault files (`Kerd Context.md`, `Kerd Log.md`, `Decisions.md`). The vault config is at `kivna/vault.json`. See `/kerd:kivna` for details.

**Six skills, each with a single responsibility:**
- **dian** — session discipline (orient/plan/execute/close-out protocol)
- **switch** — git boundary operations (pull on arrive, commit+push on leave)
- **kivna** — knowledge management (Obsidian vault integration: context, decisions, activity log, import/export)
- **sotu** — project health audits (docs, code, site, deps, playbook)
- **skriv** — human writing voice enforcement (audit, fix, session mode)
- **startup** — one-time project scaffold for new repos

## Integrations

No external services or APIs. Kerd operates entirely within the local filesystem and git.

The only integration point is the **Claude Code plugin system** — Kerd registers as a plugin and its skills become available as slash commands (`/kerd:dian`, `/kerd:switch`, etc.).

Session logs written by switch go to `kivna/sessions/` and are committed to git, making them available across machines.

## Deployment

Kerd is distributed as a Claude Code marketplace plugin.

**To publish an update:**
1. Make changes to skills/commands/docs
2. Bump the version in all three locations per the release checklist in CLAUDE.md:
   - `.claude-plugin/plugin.json` → `version`
   - `.claude-plugin/marketplace.json` → `metadata.version`
   - `.claude-plugin/marketplace.json` → `plugins[0].version`
3. Commit and push to `main`
4. Users get the update on next `claude plugins install kerd`

No CI/CD pipeline, no build artifacts, no environment variables.

## Gotchas

- **Version sync** — the version must be identical in three places (plugin.json version, marketplace.json metadata.version, marketplace.json plugins[0].version). Easy to update one and forget the others. The release checklist in CLAUDE.md exists because this happened.
- **Cache busting** — after publishing, Claude Code may cache the old plugin version. Bumping a patch version forces a re-fetch. This is why you see "cache bust" commits in the history.
- **Namespace prefix** — skill SKILL.md frontmatter uses bare names (`name: dian`), but all references in docs and skills must use `kerd:` prefix (`/kerd:dian`). The plugin system adds the prefix automatically. README examples are exempt for readability.
- **No .gitignore** — the project doesn't have one yet. The `kivna/input/` and `kivna/output/` directories are described as gitignored in the README, but that applies to projects that *use* Kerd, not to the Kerd repo itself.
- **Command wrappers removed** — the plugin system now loads skills directly from SKILL.md via the `kerd:` prefix (e.g., `/kerd:dian`). Legacy command wrappers in `commands/` were removed in v0.7.0.

## Current Status

**Version:** 0.7.0

**Working:**
- All six skills functional: dian, switch, kivna, sotu, skriv, startup
- Plugin installs from marketplace
- Session logs, playbook creation, and health audits all operational
- Obsidian vault integration — kivna reads/writes vault for context, decisions, and activity log
- Startup scaffold verified — produces correct directory structure and files
- Dian playbook creation verified — skeleton matches startup's template
- Mode markers on dian and skriv — visible phase/state announcements with `.active-modes` state file
- Dian rigorous planning (interrogate tasks, push back, no guessing) and execute verification (check each task, record decisions immediately, docs with code)
- Switch-out reflection — captures learnings to CLAUDE.md and memory files
- Switch-in smoke test — runs project tests if they exist

**Recent changes (as of 2026-03-14):**
- v0.7.0: Obsidian vault integration — kivna now reads/writes context, decisions, and activity log from `~/ObsidianLLM/kerd/` vault instead of local `kivna/context.md` and checkpoints
- v0.6.0: Strengthened dian (consistency check in orient, rigorous planning, verify-as-you-go in execute, diff review in close-out) and switch (reflection step on out, smoke test on in)
- v0.5.0: Mode markers for dian and skriv, `.active-modes` state file, switch-in reports active modes

**Next:**
- Test sotu playbook audit on a project with a playbook
- Consider adding version bumping to the switch-out process
- Adopt third-person description format for skill triggers (low priority)
