# Kivna → Obsidian Integration Design

**Date:** 2026-03-13
**Status:** Approved
**Affects:** kivna, dian, switch

## Problem

Kerd's knowledge layer is split across two locations: repo-local files (`kivna/context.md`, `kivna/checkpoints/`, `kivna/memories/`) and the Obsidian vault (`~/ObsidianLLM/[project]/`). This causes duplication, drift, and misses the graph's cross-project linking.

## Decision

Make the Obsidian vault the single source of truth for all context, decisions, and activity logging. Kivna becomes the read/write interface to the vault. Repo keeps ephemeral working state (TODO.md, session scratchpad) and build docs (playbook, CLAUDE.md).

## Architecture

### Where Things Live

| File | Location | Why |
|------|----------|-----|
| `[Project] Context.md` | Vault | Durable, append-only, cross-linkable |
| `[Project] Log.md` | Vault | Scannable activity history |
| `Decisions.md` | Vault | Durable, cross-linkable, approval-gated |
| `[Project].md` (MOC) | Vault | Manual curation, graph entry point |
| `TODO.md` | Repo | Ephemeral session scratchpad |
| `docs/playbook.md` | Repo (symlinked to vault) | Build instructions, belongs with code |
| `CLAUDE.md` | Repo (symlinked to vault) | Claude Code enforcement rules |
| `kivna/sessions/` | Repo (symlinked to vault) | Git history, switch writes here |
| `kivna/.active-modes` | Repo | Ephemeral session state |
| `kivna/input/` | Repo | Transit folder, gitignored |
| `kivna/output/` | Repo | Transit folder, gitignored |

### Removed

| File | Replaced By |
|------|-------------|
| `kivna/context.md` | `[Project] Context.md` in vault |
| `kivna/checkpoints/` | Append-only sections in Context.md |
| `kivna/memories/` | Context sections + Log entries |

## Vault Discovery

1. **Check `kivna/vault.json`** — if it exists, read vault path, folder, and display name.
2. **Convention fallback** — repo directory name → vault folder. `~/Kerd` → `~/ObsidianLLM/kerd/`. Display name: title-case the folder name, or read from `# heading` in MOC file.
3. **No vault found** — prompt user: "No Obsidian vault found for this project at `~/ObsidianLLM/[folder]/`. Want me to set it up?" If yes, scaffold. If no, work repo-local (backwards compatible).

### vault.json

```json
{
  "vault": "~/ObsidianLLM",
  "folder": "kerd",
  "name": "Kerd"
}
```

Always created on scaffold. Committed to repo.

## Kivna Save Mechanic

Triggered manually (`/kivna save`) or automatically by dian (after each task, on close-out).

### Steps

1. **Discover vault.** Read `kivna/vault.json` or derive from repo name. No vault? Prompt to scaffold.

2. **Prepend to `[Project] Context.md`.** New dated section at the top (below the file header):

```markdown
## YYYY-MM-DD HH:MM

### Where We Are
[current focus]

### Active Work
[specific tasks in progress]

### Key Relationships
[[[people/Name]] wikilinks — only if relevant people came up. Skip if none.]

### Blocked / Waiting
[anything stalled — skip section if nothing]

### Open Questions
[unresolved items — skip section if none]
```

3. **Prepend to `[Project] Log.md`.** One-liners for what was just done. Format: `YYYY-MM-DD — did the thing`

4. **Flag decisions.** If new decisions were made since last save, show them to the user with reasoning. User approves → append to `Decisions.md`. User edits or skips → respect that. Kivna does NOT write to Decisions.md without approval.

5. **Confirm.** One-line summary: "Saved to vault: Context updated, 3 log entries, 1 decision flagged."

## Kivna Import (`/kivna in`)

No changes to import mechanic. Still reads from `kivna/input/`, integrates into project, cleans up. The only difference: if import surfaces decisions, they get flagged for Decisions.md approval.

## Kivna Export (`/kivna out`)

No changes to export mechanic. Still writes to `kivna/output/`.

## Vault Scaffold

When no vault exists and user approves setup:

1. **Create `~/ObsidianLLM/[folder]/`** and subdirectories mirroring repo .md file structure.
2. **Symlink all `.md` files** from repo with `ln -sf`, preserving subfolder structure.
3. **Create vault-native files:**
   - `[Project].md` — MOC linking every symlinked file, grouped by category
   - `[Project] Context.md` — seeded with one section from current project state
   - `[Project] Log.md` — seeded from recent git history
   - `Decisions.md` — seeded from CLAUDE.md rules and any decisions in existing context
4. **Write `kivna/vault.json`** with vault path, folder name, and display name.
5. **Remove deprecated files** (with user confirmation):
   - `kivna/context.md`
   - `kivna/checkpoints/`
   - `kivna/memories/`

## Dian Changes

Protocol unchanged (orient/plan/execute/close-out). Only the read/write targets move.

### Orient
- **Was:** read `kivna/context.md`
- **Now:** read latest section of `[Project] Context.md` from vault + `Decisions.md` from vault
- Everything else unchanged: TODO.md, CLAUDE.md, playbook from repo

### Execute
- **Auto-save after each task:** calls kivna save → writes to vault
- **Decision recording:** decisions go into Context.md section AND get flagged for Decisions.md approval
- **Docs-with-code enforcement:** unchanged (repo docs travel with repo code)

### Close-out
- **Was:** finalize `kivna/context.md`
- **Now:** write close-out section to vault `[Project] Context.md` with session-closed marker, prepend summary to `[Project] Log.md`
- TODO.md and playbook updates: unchanged (repo)
- Mode markers (`kivna/.active-modes`): unchanged (repo)

## Switch Changes

### Switch-in
- **Was:** read `kivna/context.md`
- **Now:** read vault `[Project] Context.md` (latest section) + `[Project] Log.md` for recent activity
- Everything else unchanged: TODO.md, session logs, smoke test

### Switch-out
- Session log still goes to `kivna/sessions/` in repo (git history)
- Reflection learnings: enforcement rules → CLAUDE.md (repo). Conventions and patterns → flag for vault Decisions.md (with approval).

## Cross-Project Linking

Kivna adds `[[wikilinks]]` in Context.md when referencing:
- People: `[[people/Name]]`
- Other projects: `[[project-name/file]]`

Kivna does NOT:
- Automatically chase inbound links from other projects
- Create people files (just links — user creates people files manually)
- Modify the MOC (user curates)

## Implementation Plan

Three files to modify:
1. `skills/kivna/SKILL.md` — rewrite save mechanic, add vault discovery + scaffold, remove checkpoints/memories references
2. `skills/dian/SKILL.md` — update orient reads, execute auto-save, close-out writes
3. `skills/switch/SKILL.md` — update in/out reads

Plus:
4. Add `kivna/vault.json` to Kerd repo (self-referential — Kerd's own vault config)
5. Bump version (minor — new feature, changed behavior)
6. Update README.md with vault integration docs
7. Update playbook with new architecture

## Backwards Compatibility

If no vault exists and user declines scaffold, kivna falls back to repo-local behavior. All existing commands still work. The vault is additive.
