---
name: kivna
description: "Use when the user says 'kivna', 'vault', 'save context', 'save', 'scaffold', 'import', 'export context', or needs to manage project knowledge in the Obsidian vault: updating project status, importing external files, exporting session context, or setting up the vault."
---

# Kivna (Knowledge Management)

From Gaelic "cuimhne" (memory), respelled phonetically.

Single owner of the project's knowledge layer. The vault is a human knowledge base. Every file answers a question someone would actually ask. Files are living, updated in place, not appended to.

## Vault Discovery

Every kivna command starts here. Resolve the vault location before doing anything else.

1. **Check `kivna/vault.json`.** If it exists, read `vault`, `folder`, and `name`. Expand `~` to the user's home directory.

2. **Convention fallback.** If no `vault.json`, check for `~/Obsidian/`:
   - If `~/Obsidian/` exists, use it as the vault root.
   - Folder: lowercase repo directory name (e.g., repo at `~/Kerd` → folder `kerd`)
   - Display name: title-case the folder name (e.g., `kerd` → `Kerd`)
   - Check if `~/Obsidian/[folder]/` exists on disk.

3. **No vault found.** If neither `vault.json` exists nor `~/Obsidian/` exists on disk, ask:
   > Where is your Obsidian vault? (default: `~/Obsidian/`)

   If the user provides a path, use it. If they accept the default, create `~/Obsidian/` and proceed. Then run the scaffold mechanic to set up the project folder within it.

## Folder Convention

- `kivna/vault.json` vault config (committed to git)
- `kivna/sessions/` session logs written by switch (committed)
- `kivna/.active-modes` ephemeral mode state (not committed)
- `kivna/input/` drop files here for import (gitignored, transit folder)
- `kivna/output/` exports land here (gitignored, transit folder)

## Commands

### `/kerd:kivna save` (Save to Vault)

Update the vault to reflect the current session state. Use it at natural breakpoints: after finishing a task, before context gets long, when switching topics, or when something important was decided.

#### The mechanic

1. **Discover vault.** Follow the vault discovery steps above. Stop if no vault is found and user declines scaffold.

2. **Update `[Name] Status.md`.** Read the current `[Name] Status.md` from the vault folder. Draft an updated version reflecting the current session state. Show the user a diff or summary of what changed. Ask for approval before overwriting. If the file doesn't exist, create it (still ask approval for the content).

   Status.md format:

   ```markdown
   # [Name] Status

   ## Where We Are
   [Current state: what's working, what was just completed]

   ## What's Open
   [Open questions, blockers, unresolved items]

   ## What's Next
   [Prioritized next steps]
   ```

3. **Distribute new knowledge.** Review the session for new knowledge that belongs in other vault files. For each piece of knowledge, identify the target file (Architecture Decisions, Playbook, Positioning Contract, etc.), show the proposed addition, and ask for approval. Create the file if it doesn't exist (with user approval). Skip if no new knowledge surfaced.

4. **Update MOC.** If new vault files were created this session, read `[Name].md` and add links for the new files. Don't scan repo files or manage symlinks.

5. **Confirm.** One-line summary:
   > Saved to vault: Status updated, N files updated, MOC refreshed.

### `/kerd:kivna in` (Import External Knowledge)

Read files from `kivna/input/`, extract what's relevant, write it into the project, delete the originals.

1. **List the inbox.** `ls kivna/input/`. Show the user what's there. If empty, say so and stop.

2. **Read each file.** Supported formats:
   - `.pdf`: read with the Read tool (supports PDF)
   - `.md`, `.txt`: read directly
   - `.json`, `.jsonl`: read as structured data (likely LLM session exports)
   - `.html`: read and extract text content
   - Other formats: tell the user you can't process them, skip

3. **Summarize what you found.** For each file, tell the user:
   - What it contains (1-2 sentences)
   - What's relevant to this project
   - Where you'd put it (existing doc to update, new file to create, or discard)

4. **Wait for approval.** Do not write anything until the user confirms.

5. **Integrate.** For each approved item:
   - If updating an existing doc, use Edit to add the relevant content
   - If creating a new doc, prefer putting it in the project's natural doc structure
   - If the content is a session transcript from another LLM, extract decisions, insights, and action items. Do not copy the raw transcript
   - Write in the project's voice

6. **Flag vault knowledge.** If import surfaces knowledge that belongs in a vault file, note it for the user. They can update the vault with `/kerd:kivna save` later.

7. **Clean up.** Delete the processed files from `kivna/input/`. Leave any files the user said to skip.

8. **Report.** Tell the user what was imported and where it went.

### `/kerd:kivna out` (Export Session Context)

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
# Session Export: [Project Name], [Date]

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
[Brief description of the project, its structure, and conventions (enough for a cold start in another tool)]
```

4. **Confirm.** Show the user the export path and a summary of what's in it.

### `/kerd:kivna scaffold` (Vault Scaffold)

Set up the Obsidian vault folder for this project. Also triggered automatically when vault discovery fails and the user says yes.

#### The mechanic

1. **Create the vault folder.** `~/Obsidian/[folder]/`.

2. **Create `[Name].md`** (MOC). Links to `[Name] Status.md` only (nothing else exists yet). Under 40 lines.

3. **Create `[Name] Status.md`.** Seed from repo state: read git log, TODO.md, CLAUDE.md, README.md. Write in human form: a summary someone could read cold. Show the user the draft and ask for approval before writing.

4. **Write `kivna/vault.json`** in the repo:

```json
{
  "vault": "~/Obsidian",
  "folder": "[folder]",
  "name": "[Name]"
}
```

5. **Suggest optional files.** Based on what the project looks like, suggest vault files the user might want later. Examples:
   - "This looks like a code plugin. Consider `[Name] Architecture Decisions.md` and `[Name] Usage Guide.md`."
   - "This has a company/product. Consider `[Company] Playbook.md` and `[Company] Company.md`."

   Do NOT create these files. Just suggest. They get added as knowledge accumulates.

6. **Confirm.** Report vault path, files created, suggestions made.

## Notes

- The vault spec at `docs/vault-spec.md` defines what belongs in the vault and what doesn't. Kivna implements the mechanics; the spec defines the philosophy.
- Status.md is overwritten, not appended to. Always show the user what's changing and get approval before overwriting.
- Vault files use self-identifying names (`[Project] Status.md`, not `Status.md`). This prevents collisions in Obsidian's quick switcher across vaults.
- No symlinks to repo files. The vault contains knowledge written in human form, not mirrors of machine-readable repo files.
- `kivna/input/` and `kivna/output/` should be in `.gitignore`. They're transit folders, not project content.
- Exports are written in plain markdown so any LLM can read them.
- When importing LLM session transcripts, be aggressive about filtering. Most of a chat session is noise. Extract the signal: decisions, code patterns, insights, action items.
- When importing PDFs or reports, focus on what's actionable for THIS project.
- Kivna adds `[[wikilinks]]` in vault files when referencing people (`[[people/Name]]`) or other projects (`[[project-name/file]]`). Kivna does NOT create people files, just links.
- On cold start, read vault `[Name] Status.md` and scan the MOC to discover other relevant vault files.
