---
name: kivna
description: "Use when the user says 'kivna', 'vault', 'save context', 'save', 'snapshot', 'scaffold', 'import', 'export context', or needs to manage project knowledge in the Obsidian vault — saving working context, importing external files, exporting session context, or setting up the vault."
---

# Kivna — Knowledge Management

From Gaelic "cuimhne" (memory), respelled phonetically.

Single owner of the project's knowledge layer. All durable context, decisions, and activity logs live in the Obsidian vault. Kivna is the read/write interface between Claude Code sessions and the vault.

## Vault Discovery

Every kivna command starts here. Resolve the vault location before doing anything else.

1. **Check `kivna/vault.json`.** If it exists, read `vault`, `folder`, and `name`. Expand `~` to the user's home directory.

2. **Convention fallback.** If no `vault.json`, derive from the repo directory name:
   - Vault path: `~/ObsidianLLM/`
   - Folder: lowercase repo directory name (e.g., repo at `~/Kerd` → folder `kerd`)
   - Display name: title-case the folder name (e.g., `kerd` → `Kerd`)
   - Check if `~/ObsidianLLM/[folder]/` exists on disk.

3. **No vault found.** If neither `vault.json` exists nor the convention folder exists on disk, prompt:
   > No Obsidian vault folder found for this project at `~/ObsidianLLM/[folder]/`. Want me to set it up?

   If yes → run the scaffold mechanic. If no → stop and tell the user kivna requires a vault.

## Folder Convention

- `kivna/vault.json` — vault config (committed to git)
- `kivna/sessions/` — session logs written by switch (committed, symlinked to vault)
- `kivna/.active-modes` — ephemeral mode state (not committed)
- `kivna/input/` — drop files here for import (gitignored, transit folder)
- `kivna/output/` — exports land here (gitignored, transit folder)

## Commands

### `/kivna save` — Save to Vault

Snapshot the current working context into the Obsidian vault. This is the same mechanic that `/kerd:dian` triggers at task boundaries — but available manually anytime.

Use it at natural breakpoints: after finishing a task, before context gets long, when switching topics, or when something important was decided.

#### The mechanic

1. **Discover vault.** Follow the vault discovery steps above. Stop if no vault is found and user declines scaffold.

2. **Prepend to `[Name] Context.md`.** Insert a new dated section after the file's `# heading` line and `---` separator, before any existing sections. `[Name]` is the display name from vault discovery. If the file doesn't exist, create it with a `# [Name] Context` heading, a `---` separator, then the section.

```markdown
## YYYY-MM-DD HH:MM

### Where We Are
[current focus — what we're actively working on and where we are in it]

### Active Work
[specific tasks in progress, with enough detail for a cold-start reader]

### Key Relationships
[[[people/Name]] wikilinks for people involved — skip this section entirely if none]

### Blocked / Waiting
[anything stalled or waiting on input — skip this section entirely if nothing]

### Open Questions
[unresolved items that need investigation or input — skip this section entirely if none]
```

3. **Prepend to `[Name] Log.md`.** Insert one-liners after the file's `# heading` and `---` separator, before existing entries. Each line: `YYYY-MM-DD — did the thing`. If the file doesn't exist, create it with a `# [Name] Log` heading and a `---` separator, then the entries.

4. **Flag decisions.** If new decisions were made since the last save, show each one to the user with its reasoning. Wait for approval before writing anything to `Decisions.md`. User can approve, edit, or skip each decision. Kivna does NOT write to `Decisions.md` without explicit approval.

5. **Confirm.** One-line summary:
   > Saved to vault: Context updated, N log entries, M decisions flagged.

### `/kivna in` — Import External Knowledge

Read files from `kivna/input/`, extract what's relevant, write it into the project, delete the originals.

1. **List the inbox.** `ls kivna/input/` — show the user what's there. If empty, say so and stop.

2. **Read each file.** Supported formats:
   - `.pdf` — read with the Read tool (supports PDF)
   - `.md`, `.txt` — read directly
   - `.json`, `.jsonl` — read as structured data (likely LLM session exports)
   - `.html` — read and extract text content
   - Other formats — tell the user you can't process them, skip

3. **Summarize what you found.** For each file, tell the user:
   - What it contains (1-2 sentences)
   - What's relevant to this project
   - Where you'd put it (existing doc to update, new file to create, or discard)

4. **Wait for approval.** Do not write anything until the user confirms.

5. **Integrate.** For each approved item:
   - If updating an existing doc, use Edit to add the relevant content
   - If creating a new doc, prefer putting it in the project's natural doc structure
   - If the content is a session transcript from another LLM, extract decisions, insights, and action items — do not copy the raw transcript
   - Write in the project's voice

6. **Flag decisions.** If import surfaces any decisions, flag them for `Decisions.md` approval using the same mechanic as `/kivna save` step 4.

7. **Clean up.** Delete the processed files from `kivna/input/`. Leave any files the user said to skip.

8. **Report.** Tell the user what was imported and where it went.

### `/kivna out` — Export Session Context

Package the current session's work into a portable file another LLM can use as input.

1. **Gather context.** From the current conversation, collect:
   - What was done this session (tasks completed, decisions made)
   - Key files created or modified (with brief descriptions)
   - Architecture decisions and their reasoning
   - Open questions or unresolved items
   - Current project state (what's working, what's blocked)

2. **Read TODO.md and any progress tracking** to fill gaps.

3. **Write the export.** Create `kivna/output/export-YYYY-MM-DD.md` with this structure:

```
# Session Export — [Project Name] — [Date]

## What Happened
[Plain prose summary of the session. What was built, fixed, or decided.]

## Key Decisions
[Each decision with its reasoning. Another LLM needs to understand WHY, not just WHAT.]

## Files Changed
[List of files with one-line descriptions of what changed and why]

## Current State
[What works, what's blocked, what's next]

## Open Questions
[Anything unresolved that needs input]

## Project Context
[Brief description of the project, its structure, and conventions — enough for a cold start in another tool]
```

4. **Confirm.** Show the user the export path and a summary of what's in it.

### `/kivna scaffold` — Vault Scaffold

Set up the Obsidian vault folder for this project. Also triggered automatically when vault discovery fails and the user says yes.

#### The mechanic

1. **Create the vault folder.** `~/ObsidianLLM/[folder]/` and subdirectories that mirror the repo's `.md` file structure. For example, if the repo has `docs/plans/`, create `~/ObsidianLLM/[folder]/docs/plans/`.

2. **Symlink all `.md` files** from the repo into the vault folder using `ln -sf`, preserving subfolder structure. This makes repo docs visible in Obsidian's graph without duplication.

3. **Symlink `kivna/sessions/`** into the vault folder so session logs appear in Obsidian.

4. **Create vault-native files** (these are NOT symlinks — they live only in the vault):

   - **`[Name].md`** — Map of Content (MOC). Links every symlinked file, grouped by category (skills, docs, config, etc.). This is the graph entry point.
   - **`[Name] Context.md`** — Seeded with one section from the current project state, using the format from `/kivna save`.
   - **`[Name] Log.md`** — Seeded with entries from recent git history (`git log --oneline -20`), formatted as `YYYY-MM-DD — commit message`.
   - **`Decisions.md`** — Seeded from rules in `CLAUDE.md` and any decisions found in existing project context. Each entry gets a date and reasoning.

5. **Write `kivna/vault.json`** in the repo:

```json
{
  "vault": "~/ObsidianLLM",
  "folder": "[folder]",
  "name": "[Name]"
}
```

6. **Offer deprecated file cleanup.** If any of the following exist, ask the user for confirmation before removing them:
   - `kivna/context.md`
   - `kivna/checkpoints/`
   - `kivna/memories/`

   Tell the user these are replaced by the vault's `Context.md` (append-only) and `Log.md`. Only delete with explicit confirmation.

7. **Confirm.** Report what was created: vault path, number of symlinks, vault-native files created, and whether deprecated files were cleaned up.

## Notes

- `kivna/input/` and `kivna/output/` should be in `.gitignore` — they're transit folders, not project content.
- `kivna/sessions/` should be committed to git — they're permanent history, symlinked into the vault.
- Vault-native files (`Context.md`, `Log.md`, `Decisions.md`, MOC) live only in the vault and are NOT committed to the repo.
- `Context.md` is append-only — old sections are never deleted. New sections are always prepended after the header. This replaces the old checkpoint mechanic.
- `Decisions.md` requires user approval before every write. Kivna flags decisions; the user decides what gets recorded.
- Exports are written in plain markdown so any LLM can read them.
- When importing LLM session transcripts, be aggressive about filtering. Most of a chat session is noise. Extract the signal: decisions, code patterns, insights, action items.
- When importing PDFs or reports, focus on what's actionable for THIS project.
- Kivna adds `[[wikilinks]]` in Context.md when referencing people (`[[people/Name]]`) or other projects (`[[project-name/file]]`). Kivna does NOT create people files — just links.
- On cold start, read the latest section of `[Name] Context.md` from the vault. The older sections are for tracing decisions back, not for full restore.
