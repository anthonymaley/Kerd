---
name: kivna
description: "Use when the user says 'kivna', 'vault', 'save context', 'save', 'scaffold', 'import', 'export context', or needs to manage project knowledge in the Obsidian vault: updating project status, importing external files, exporting session context, or setting up the vault."
---

# Kivna (Knowledge Management)

**Asking the person:** every question is one speech-bubble line, the last prose line of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it; never ask whether the person is confused: answer what they asked, with one recommendation; a genuine question is open (“What should it show?”), never “X, or Y?”; a check the person runs, its expected result already written above, asks whether that result happened (“Did the import finish and say how many were saved?”), never an open recall question (“What does the finished line say?”); when options are in hand (open work, known routes, candidates), list them above the question with one recommendation; a question that chooses among them (which work, which route) asks about that recommendation (“Start with the export fix?”), never an open question that ignores the list, while a missing fact, a pick-several choice and Switch In’s fixed arrival question keep their own question; ask with no list only when none are in hand; where the host offers one, a native picker may follow the bubble carrying those same options and always leaving a free-form answer open, never replacing or preceding it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Putting a decision to the person:** a consequential question — its answer commits to work, spends real effort, releases or deletes something, or reverses a ruling — comes after a decision block: Problem, Facts (with how we know the problem is real and how strong that evidence is), Known options (or “needs study”), Recommendation, Why, Cost, What we lose, Input (who else checked it, or nobody yet). Its bubble is the Recommendation sentence ending “— approve?”, every operation included, or one genuine question the recommendation depends on; never a smaller or softer question than the real decision, and never without the block. A factual question or a small, easily undone step stays one line — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Showing the person:** when they ask to see something, and whenever a proposal carries two or more connected parts, a branch, an ownership boundary or a before → after change, the answer carries a saved, rendered view drawn with diagram-design or Archify — never hand-rolled ASCII in a code fence, never an offer question, no quota; only a single action or a factual answer stays text, and being easy to describe in words does not make it one — see [showing the work](../conductor/references/journey.md#visuals-belong-throughout).

From Gaelic "cuimhne" (memory), respelled phonetically.

Single owner of the project's knowledge layer. The vault is a human knowledge base. Every file answers a question someone would actually ask. Files are living, updated in place, not appended to.

## Write Safety

One rule covers every write Kivna makes (save, import, export, scaffold). An update needs a successful read of the target first. A create needs confirmed absence ("no such file", not a permission error or an unclear result). Inspect the target again immediately before writing. On an error, or if the target changed since it was read or checked (a file appeared, or its content differs), stop and say so; keep what is there and do not overwrite it.

## Vault Discovery

Every kivna command starts here. Resolve the vault location before doing anything else.

1. **Check `kivna/vault.json`.** If it exists, read `vault`, `folder`, and `name`. Expand `~` to the user's home directory. If it also sets `"work_notes": "vault"`, the project keeps its working notes private: the notes root is `<vault>/<folder>/work`, the `work/` folder inside the vault's existing private git repo (shared with the rest of the vault's content, not a repo of its own, and separate from this project's repo), and Conductor writes each piece of work's sketchbook there instead of `docs/work/`. Kivna does not create or maintain this folder; it only recognizes the key.

   Absence must be confirmed: "no such file" counts, but a permission error, an unreadable folder or any check that does not give a clear answer does not. If the check fails, stop and say what could not be inspected; do not continue as if the file were absent.

   If `kivna/vault.json` exists but cannot be read, is not valid JSON, or lacks `vault`, `folder` or `name`, it is not "absent". Stop, say what is wrong with it, and say how to repair it (fix the JSON or the missing field by hand, or delete the file to start over). Do not ask for a vault path, do not scaffold, and do not write over it.

2. **No `vault.json` at all: find or ask.** Kerd assumes no vault location as a default. The project folder is the lowercase repo directory name (e.g., repo at `~/Kerd` → folder `kerd`) and the display name is that folder title-cased (`kerd` → `Kerd`).

   - **A vault already on this machine.** If `~/eolas/vault/` is confirmed present, offer it as a location found, not as a default, so projects set up before `vault.json` existed keep working. Ask "Use the vault found at `~/eolas/vault/`?" and write `kivna/vault.json` only after the person confirms. If that check errors, stop and say what could not be inspected. If the folder is confirmed absent, say nothing about it: a newcomer sees no such path.
   - **Otherwise ask**, with no default path, and use what they say (expand `~`):

   > 💬 **Where is your Obsidian vault?**

   Once the path is known, look in it for an existing project folder and spine (`[Name].md`, `[Name] Status.md`, `[Name] Weekly.md`). An error opening the vault folder or reading its contents is a stop: say what could not be inspected, and do not treat it as "no folder yet". If any spine file exists, keep it as it is and write only `kivna/vault.json`; run scaffold for the missing spine files only on the person's explicit approval, and never overwrite an existing vault file. The question is asked once per project because `vault.json` is then written.

   **If the vault folder they name is confirmed absent** ("no such file"), offer to create it and do so only after they confirm, checking again just before creating; then run the scaffold mechanic on the new folder. A permission error or any other failure to inspect it is a stop, not an offer to create. If they have no vault and do not want one, stop: a vault is optional, and nothing else in Kerd needs it.

## Folder Convention

- `kivna/vault.json` vault config (committed to git)
- `kivna/sessions/` session logs written by switch (committed)
- `kivna/input/` drop files here for import (gitignored, transit folder)
- `kivna/output/` exports land here (gitignored, transit folder)

With `work_notes` set, the vault also holds `<folder>/work/`: the home of this
project's private working notes (sketchbooks, diagrams, evidence, drafts), one
`<work>/work.md` per piece of work. Conductor writes it; Switch Out saves and
pushes it, alongside the project, at the session boundary. See Kerd's own
`../../docs/vault-spec.md` and `../../docs/state-contract.md`, resolved from this skill's folder
(not the project's `docs/`).

## Commands

### `/kerd:kivna save` (Save to Vault)

Update the vault to reflect the current session state. Use it at natural breakpoints: after finishing a task, before context gets long, when switching topics, or when something important was decided.

Every write below follows Write Safety (top of this file): read before updating, confirm absence before creating, check again just before writing.

Save is deliberate and on-demand — switch no longer calls it at the session boundary as of v0.83.0, so a vault is exactly as fresh as its last save.

#### The mechanic

1. **Discover vault.** Follow the vault discovery steps above. Stop if no vault is found and user declines scaffold.

2. **Update `[Name] Status.md`.** Read the current `[Name] Status.md` from the vault folder. Draft an updated version reflecting the current session state. Show the user a short summary of what changed and overwrite — **no approval prompt** (v0.60.0: save writes directly; the do-not-save markers in step 6 remain the privacy control). If the file is confirmed absent (not merely unreadable), create it; if it cannot be inspected, stop and say so. (Write Safety applies.)

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
   - Moved the vault to a new path

   ### Risks
   - [open] No playbook yet — optional; write `docs/playbook.md` by hand, or copy and adapt the skeleton Tend shows in its Category 2 by hand (Tend reports a missing playbook; it does not create it)
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

6. **Integrate.** Each write follows Write Safety (top of this file). For each approved item:
   - KIF backlog items: merge into TODO.md Backlog section (skip duplicates)
   - KIF decisions: append to the current session log in kivna/sessions/
   - KIF status: update vault Status.md (same mechanic as `/kerd:kivna save`; the import approval in step 5 already gated this)
   - Non-KIF: if updating an existing doc, use Edit. If creating new, prefer the project's natural doc structure. For LLM transcripts, extract signal only (decisions, insights, action items). Write in the project's voice.

7. **Flag vault knowledge.** If import surfaces knowledge that belongs in a vault file, note it for the user. They can update the vault with `/kerd:kivna save` later.

8. **Clean up.** Delete the processed files from `kivna/input/`. Leave any files the user said to skip.

9. **Report.** Tell the user what was imported and where it went.

### `/kerd:kivna out` (Export — Kerd Interchange Format)

Export project context in two formats: `.kif.toon` (token-efficient, for LLM session handoff) and `.kif.json` (machine-parseable, for import). Both land in `kivna/output/`.

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

#### Write the TOON export

Write Safety applies to both export files: an existing export is read and replaced only knowingly, a new one needs confirmed absence, and the target is checked again just before the write.

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
  repo: github.com/example/Kerd

status:
  phase: active development
  summary: Hooks and KIF shipped in v0.19.0

backlog[3]{id,item,priority}:
  1,Merge trim PR after Kwan approves,high
  2,Lorg ranking rules,medium
  3,Shared state contract doc,low

decisions[2]{date,decision,reasoning}:
  2026-04-04,Weekly sections are updated in place,Keeps the file short
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
    "repo": "github.com/example/Kerd"
  },
  "status": {
    "phase": "active development",
    "summary": "Hooks and KIF shipped in v0.19.0"
  },
  "backlog": [
    {"id": 1, "item": "Merge trim PR after Kwan approves", "priority": "high"}
  ],
  "decisions": [
    {"date": "2026-04-04", "decision": "Weekly sections are updated in place", "reasoning": "Keeps the file short"}
  ]
}
```

#### Confirm

Show the user both export paths and a one-line summary of what's included (section count, item counts).

### `/kerd:kivna scaffold` (Vault Scaffold)

Set up the Obsidian vault folder for this project. Also triggered automatically when vault discovery fails and the user says yes.

Scaffold creates the **spine** (MOC + Status + Weekly) and nothing else, seeded from a short intake interview. The spine is the canonical convention in Kerd's `../../docs/vault-spec.md` (resolved from this skill's folder, not the project's `docs/`) — that doc is the source of truth; this section is how the skill executes it.

#### The mechanic

1. **Create the vault folder.** `[vault]/[folder]/`, where `[vault]` is the path from discovery. Write Safety applies to every create below (folder, MOC, Status, Weekly, `vault.json`): each needs confirmed absence and a fresh check immediately before its write, and a file that appeared meanwhile is kept, never overwritten.

2. **Run the per-project intake.** A short, batched interview that seeds the spine — this replaces "blank folder, figure it out later." It is *batched*, not drilled: ask everything in one round (≤5 prompts). Show the prompts as labelled fields, not questions, then close with one speech-bubble question. (Intake is *seeding*, not *deciding*, so it batches rather than drilling one question at a time.)

   Rules: open-ended and consequential only (every answer must change what gets written, no yes/no); skip and pre-fill anything the repo README, folder, or conversation already answers; reflect understanding back in 2–3 lines and let the user correct before writing; if the user gives a one-line brain-dump that covers it, skip straight to reflect-back. The interview is a floor, not a gate.

   The fields (adapt wording, drop any already answered):
   1. **Purpose:** what the project is, in a line or two, and why it exists. → MOC opening + purpose.
   2. **Success:** what "done" or "working well" looks like. → success criteria in the MOC.
   3. **Current state:** where it stands today, what's already true. → Status.md.
   4. **Constraints:** hard limits or non-negotiables. → constraints in the MOC.
   5. **Exclusions:** what's explicitly out of scope, or unwanted. → scope ceiling, prevents over-production.

   Optional 6th, only if material clearly exists: **Sources:** existing docs, repos or references to read in first. → suggest a Sources slot + `/kerd:kivna in` import rather than asking content questions a source already answers.

   Close with one bubble covering the batch, for example `> 💬 **What would you put in each of these?**`.

3. **Create `[Name].md`** (MOC). Seed the opening, purpose, success criteria, and constraints from the intake answers (1, 2, 4). Links to `[Name] Status.md` and `[Name] Weekly.md` (the spine). Under 40 lines. Show the draft and get approval before writing.

4. **Create `[Name] Status.md`.** Seed from the intake "where it stands" answer (3), cross-checked against repo state (git log, TODO.md, CLAUDE.md, README.md). Write in human form: a summary someone could read cold. Show the draft and get approval before writing.

5. **Create `[Name] Weekly.md`.** Seed with the title and the current week's skeleton, ready for the first `/kerd:kivna save` to fill — do not invent achievements at scaffold time. The current week anchors to this week's Monday date.

   ```markdown
   # [Name] Weekly

   ## Week of YYYY-MM-DD

   ### Achievements

   ### Risks
   ```

6. **Write `kivna/vault.json`** in the repo, only when its absence is confirmed, checked again immediately before the write. If one already exists, keep it exactly as it is (it may hold `work_notes` or other keys) and do not rewrite it; if it cannot be inspected, stop and say so. For a new file:

```json
{
  "vault": "[vault path from discovery]",
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

- The vault spec at Kerd's `../../docs/vault-spec.md` (from this skill's folder) defines what belongs in the vault and what doesn't. Kivna implements the mechanics; the spec defines the philosophy.
- Status.md is overwritten, not appended to. Save reports what changed but does not ask for approval (v0.60.0); do-not-save markers are the privacy control. Scaffold still gets approval — it creates files from an interview, save just reflects the session.
- Weekly.md is the one file with dated, append-only sections. Each week's section is updated in place during the week, and new weeks are prepended. Old weeks stay for history. (Decisions, when it exists, also grows rather than being overwritten, but as one running document, not dated sections.)
- Vault files use self-identifying names (`[Project] Status.md`, not `Status.md`). This prevents collisions in Obsidian's quick switcher across vaults.
- No symlinks to repo files. The vault contains knowledge written in human form, not mirrors of machine-readable repo files.
- `kivna/input/` and `kivna/output/` should be in `.gitignore`. They're transit folders, not project content.
- Exports produce `.kif.toon` (token-efficient, LLM-readable) and `.kif.json` (machine-parseable). Both are human-readable.
- When importing LLM session transcripts, be aggressive about filtering. Most of a chat session is noise. Extract the signal: decisions, code patterns, insights, action items.
- When importing PDFs or reports, focus on what's actionable for THIS project.
- Kivna adds `[[wikilinks]]` in vault files when referencing people (`[[people/Name]]`) or other projects (`[[project-name/file]]`). Kivna does NOT create people files, just links.
- On cold start, read vault `[Name] Status.md` and scan the MOC to discover other relevant vault files.
