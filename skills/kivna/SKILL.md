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

2. **Convention fallback.** If no `vault.json`, check for `~/eolas/vault/`:
   - If `~/eolas/vault/` exists, use it as the vault root.
   - Folder: lowercase repo directory name (e.g., repo at `~/Kerd` → folder `kerd`)
   - Display name: title-case the folder name (e.g., `kerd` → `Kerd`)
   - Check if `~/eolas/vault/[folder]/` exists on disk.

3. **No vault found.** If neither `vault.json` exists nor `~/eolas/vault/` exists on disk, ask:
   > Where is your Obsidian vault? (default: `~/eolas/vault/`)

   If the user provides a path, use it. If they accept the default, create `~/eolas/vault/` and proceed. Then run the scaffold mechanic to set up the project folder within it.

## Folder Convention

- `kivna/vault.json` vault config (committed to git)
- `kivna/sessions/` session logs written by switch (committed)
- `kivna/.active-modes` ephemeral mode state (not committed)
- `kivna/input/` drop files here for import (gitignored, transit folder)
- `kivna/output/` exports land here (gitignored, transit folder)

## Commands

### `/kerd:kivna save` (Save to Vault)

Update the vault to reflect the current session state. Use it at natural breakpoints: after finishing a task, before context gets long, when switching topics, or when something important was decided.

Save is deliberate and on-demand — switch no longer calls it at the session boundary as of v0.83.0, so a vault is exactly as fresh as its last save.

#### The mechanic

1. **Discover vault.** Follow the vault discovery steps above. Stop if no vault is found and user declines scaffold.

2. **Update `[Name] Status.md`.** Read the current `[Name] Status.md` from the vault folder. Draft an updated version reflecting the current session state. Show the user a short summary of what changed and overwrite — **no approval prompt** (v0.60.0: save writes directly; the do-not-save markers in step 6 remain the privacy control). If the file doesn't exist, create it.

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

3. **Update `[Name] Weekly.md`.** Track achievements and risks on a rolling weekly basis for quick status report generation.

   - Find or create the current week's section using the Monday date as anchor: `## Week of YYYY-MM-DD`
   - Under `### Achievements`, add bullet points for notable work completed this session. Match vocabulary to the work — features shipped or bugs fixed for code, drafts published or revisions accepted for writing, accounts opened or calls booked for sales, frameworks decided or positions taken for strategy, sources reviewed or findings logged for research. Be specific and concise — these feed into status reports.
   - Under `### Risks`, add any new risks surfaced this session. Each risk gets a status marker: `[open]` or `[mitigated]`. When a previously open risk is resolved, update its marker to `[mitigated]` with a brief note.
   - If the current week section already exists (from an earlier session this week), append new items to the existing lists. Don't duplicate.
   - Weeks are in reverse chronological order (newest first).
   - Show the user what's being added as part of the save report — no approval prompt.
   - If no achievements or risks surfaced this session, skip this step silently. Do not invent achievements to fill the section. "I don't know if anything this session counts as an achievement" is a valid reason to skip.

   Format:

   ```markdown
   # [Name] Weekly

   ## Week of 2026-03-17

   ### Achievements
   - Shipped weekly tracker feature in Kivna (v0.14.0)
   - Resolved vault path migration to ~/eolas/vault

   ### Risks
   - [open] No playbook yet — /kerd:tend to create one
   - [mitigated] Vault path hardcoded in old sessions → fixed in v0.12.1

   ## Week of 2026-03-10

   ### Achievements
   - ...
   ```

4. **Distribute new knowledge.** Review the session for new knowledge that belongs in other vault files. For each piece of knowledge, identify the target file (Architecture Decisions, Playbook, Positioning Contract, etc.), show the addition, and write it — no approval prompt. Create the file if it doesn't exist. Skip if no new knowledge surfaced.

5. **Update MOC.** If new vault files were created this session (including `[Name] Weekly.md` on first creation), read `[Name].md` and add links for the new files. Don't scan repo files or manage symlinks.

6. **Respect do-not-save markers.** If the user said "don't save this to vault", "this is private", "off the record", or similar during the session, exclude that content from all vault writes. Track these markers in conversation context only — they do not persist to disk (no `.private` file, no frontmatter flag). When proposing vault updates, skip any knowledge the user marked as private. If unsure whether something was marked, ask.

7. **Confirm.** One-line summary:
   > Saved to vault: Status updated, N files updated, MOC refreshed.

### `/kerd:kivna in` (Import External Knowledge)

Read files from `kivna/input/`, extract what's relevant, write it into the project, delete the originals.

1. **List the inbox.** `ls kivna/input/`. Show the user what's there. If empty, say so and stop.

2. **Read each file.** Supported formats:
   - `.kif.json`: Kerd Interchange Format (structured import, see below)
   - `.kif.toon`: inform user this is the LLM-readable companion — use the `.kif.json` file instead. Skip.
   - `.pdf`: read with the Read tool (supports PDF)
   - `.md`, `.txt`: read directly
   - `.json`, `.jsonl`: read as structured data (likely LLM session exports)
   - `.html`: read and extract text content
   - Other formats: tell the user you can't process them, skip

3. **KIF import path.** For `.kif.json` files, parse the structured sections and present each one:
   - `meta`: show project name, version, date — confirm this is the right export
   - `status`: show the status summary — offer to update vault Status.md
   - `backlog`: show items — offer to merge into TODO.md
   - `decisions`: show decisions — offer to note in session log or vault
   - `playbook`, `architecture`, `memory`, `mode`: (if present) show each and offer to integrate

   For each section, the user can: accept (integrate), skip, or modify. Do not write anything without approval.

4. **Standard import path.** For non-KIF files, summarize what you found:
   - What it contains (1-2 sentences)
   - What's relevant to this project
   - Where you'd put it (existing doc to update, new file to create, or discard)

5. **Wait for approval.** Do not write anything until the user confirms.

6. **Integrate.** For each approved item:
   - KIF backlog items: merge into TODO.md Backlog section (skip duplicates)
   - KIF decisions: append to the current session log in kivna/sessions/
   - KIF status: update vault Status.md (same mechanic as `/kerd:kivna save`; the import approval in step 5 already gated this)
   - Non-KIF: if updating an existing doc, use Edit. If creating new, prefer the project's natural doc structure. For LLM transcripts, extract signal only (decisions, insights, action items). Write in the project's voice.

7. **Flag vault knowledge.** If import surfaces knowledge that belongs in a vault file, note it for the user. They can update the vault with `/kerd:kivna save` later.

8. **Clean up.** Delete the processed files from `kivna/input/`. Leave any files the user said to skip.

9. **Report.** Tell the user what was imported and where it went.

### `/kerd:kivna out` (Export — Kerd Interchange Format)

Export project context in two formats: `.kif.toon` (token-efficient, for LLM handoff) and `.kif.json` (machine-parseable, for import). Both land in `kivna/output/`.

**Usage:**
- `/kerd:kivna out` — default sections (meta, status, backlog, decisions)
- `/kerd:kivna out --full` — all sections (adds playbook, architecture, memory, mode)

#### Source order (repo-grounded first)

Gather context from repo artifacts in this order. Only use conversation context to fill gaps that no artifact covers.

1. `TODO.md` — backlog items (unchecked), current session context
2. `kivna/sessions/` — key decisions from the 3 most recent session logs
3. `docs/playbook.md` — tech stack, architecture, current status (--full only)
4. Vault `[Name] Status.md` — where the project stands
5. Vault architecture/decision files — (--full only)
6. `~/.claude/projects/*/memory/project_*.md` — project memory entries (--full only)
7. `kivna/.active-modes` — active mode state (--full only)
8. Current conversation — fill any remaining gaps (what happened this session that isn't yet in artifacts)

#### Sections

| Section | Default | `--full` | Source |
|---------|---------|----------|--------|
| `meta` | yes | yes | repo name, git remote, plugin version, today's date |
| `status` | yes | yes | vault Status.md |
| `backlog` | yes | yes | TODO.md unchecked items |
| `decisions` | yes | yes | last 3 session logs in kivna/sessions/ |
| `playbook` | no | yes | docs/playbook.md (tech stack, setup, architecture) |
| `architecture` | no | yes | vault architecture decisions file |
| `memory` | no | yes | project-type memory entries |
| `mode` | no | yes | kivna/.active-modes |

#### Write the TOON export

Create `kivna/output/export-YYYY-MM-DD.kif.toon`. TOON format rules:

- Nested objects use YAML-style indentation (key: value, indented children)
- Uniform arrays use CSV-style tabular layout: `name[count]{field1,field2,...}:` followed by indented comma-delimited rows
- No quotes around string values unless they contain commas
- Arrays of non-uniform objects fall back to nested notation

Example:

```toon
meta:
  project: Kerd
  exported: 2026-04-04
  version: 0.19.0
  repo: github.com/anthonymaley/Kerd

status:
  phase: active development
  summary: Hooks and KIF shipped in v0.19.0

backlog[3]{id,item,priority}:
  1,Merge trim PR after Kwan approves,high
  2,Lorg ranking rules,medium
  3,Shared state contract doc,low

decisions[2]{date,decision,reasoning}:
  2026-04-04,Hooks are opt-in via tend,Non-invasive for existing users
  2026-04-04,TOON export + JSON import,Avoids TOON parser dependency
```

Reference: https://github.com/toon-format/toon

#### Write the JSON export

Create `kivna/output/export-YYYY-MM-DD.kif.json` alongside the TOON file. Same data, standard JSON:

```json
{
  "kif_version": "1.0",
  "meta": {
    "project": "Kerd",
    "exported": "2026-04-04",
    "version": "0.19.0",
    "repo": "github.com/anthonymaley/Kerd"
  },
  "status": {
    "phase": "active development",
    "summary": "Hooks and KIF shipped in v0.19.0"
  },
  "backlog": [
    {"id": 1, "item": "Merge trim PR after Kwan approves", "priority": "high"}
  ],
  "decisions": [
    {"date": "2026-04-04", "decision": "Hooks are opt-in via tend", "reasoning": "Non-invasive for existing users"}
  ]
}
```

#### Confirm

Show the user both export paths and a one-line summary of what's included (section count, item counts).

### `/kerd:kivna scaffold` (Vault Scaffold)

Set up the Obsidian vault folder for this project. Also triggered automatically when vault discovery fails and the user says yes.

Scaffold creates the **spine** (MOC + Status + Weekly) and nothing else, seeded from a short intake interview. The spine is the canonical convention in `docs/vault-spec.md` — that doc is the source of truth; this section is how the skill executes it.

#### The mechanic

1. **Create the vault folder.** `~/eolas/vault/[folder]/`.

2. **Run the per-project intake.** A short, batched interview that seeds the spine — this replaces "blank folder, figure it out later." It is *batched*, not drilled: ask everything in one round (≤5 questions), the way conductor's pre-flight inventory does. (Intake is *seeding*, not *deciding*, so it batches rather than drilling one question at a time.)

   Rules: open-ended and consequential only (every answer must change what gets written, no yes/no); skip and pre-fill anything the repo README, folder, or conversation already answers; reflect understanding back in 2–3 lines and let the user correct before writing; if the user gives a one-line brain-dump that covers it, skip straight to reflect-back. The interview is a floor, not a gate.

   The questions (adapt wording, drop any already answered):
   1. **What is this project, in a line or two — and why does it exist?** → MOC opening + purpose.
   2. **What does "done" or "working well" look like?** → success criteria in the MOC.
   3. **Where does it stand today — what's already true?** → Status.md.
   4. **What are the hard constraints or non-negotiables?** → constraints in the MOC.
   5. **What's explicitly *out* of scope, or what do you not want?** → scope ceiling, prevents over-production.

   Optional 6th, only if material clearly exists: **Any existing docs, repos, or references I should read in first?** → suggest a Sources slot + `/kerd:kivna in` import rather than asking content questions a source already answers.

3. **Create `[Name].md`** (MOC). Seed the opening, purpose, success criteria, and constraints from the intake answers (1, 2, 4). Links to `[Name] Status.md` and `[Name] Weekly.md` (the spine). Under 40 lines. Show the draft and get approval before writing.

4. **Create `[Name] Status.md`.** Seed from the intake "where it stands" answer (3), cross-checked against repo state (git log, TODO.md, CLAUDE.md, README.md). Write in human form: a summary someone could read cold. Show the draft and get approval before writing.

5. **Create `[Name] Weekly.md`.** Seed with the title and the current week's skeleton, ready for the first `/kerd:kivna save` to fill — do not invent achievements at scaffold time. The current week anchors to this week's Monday date.

   ```markdown
   # [Name] Weekly

   ## Week of YYYY-MM-DD

   ### Achievements

   ### Risks
   ```

6. **Write `kivna/vault.json`** in the repo:

```json
{
  "vault": "~/eolas/vault",
  "folder": "[folder]",
  "name": "[Name]"
}
```

7. **Suggest optional slots.** Based on what the project looks like, suggest vault files the user might want later. Examples:
   - "This looks like a code plugin. Consider `[Name] Architecture Decisions.md` and `[Name] Usage Guide.md`."
   - "This has a company/product. Consider `[Company] Playbook.md` and `[Company] Company.md`."

   Do NOT create these files. Just suggest — they get added the moment they have something to hold. (If the intake's optional 6th question surfaced sources, suggest a `[Name] Sources.md` slot and offer to import.)

8. **Confirm.** Report vault path, spine files created (MOC + Status + Weekly), and suggestions made.

## Notes

- The vault spec at `docs/vault-spec.md` defines what belongs in the vault and what doesn't. Kivna implements the mechanics; the spec defines the philosophy.
- Status.md is overwritten, not appended to. Save reports what changed but does not ask for approval (v0.60.0); do-not-save markers are the privacy control. Scaffold still gets approval — it creates files from an interview, save just reflects the session.
- Weekly.md is the one append-style vault file. Each week's section is updated in place during the week, and new weeks are prepended. Old weeks stay for history.
- Vault files use self-identifying names (`[Project] Status.md`, not `Status.md`). This prevents collisions in Obsidian's quick switcher across vaults.
- No symlinks to repo files. The vault contains knowledge written in human form, not mirrors of machine-readable repo files.
- `kivna/input/` and `kivna/output/` should be in `.gitignore`. They're transit folders, not project content.
- Exports produce `.kif.toon` (token-efficient, LLM-readable) and `.kif.json` (machine-parseable). Both are human-readable.
- When importing LLM session transcripts, be aggressive about filtering. Most of a chat session is noise. Extract the signal: decisions, code patterns, insights, action items.
- When importing PDFs or reports, focus on what's actionable for THIS project.
- Kivna adds `[[wikilinks]]` in vault files when referencing people (`[[people/Name]]`) or other projects (`[[project-name/file]]`). Kivna does NOT create people files, just links.
- On cold start, read vault `[Name] Status.md` and scan the MOC to discover other relevant vault files.
