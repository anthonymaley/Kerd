---
name: kivna
description: "Use when the user says 'kivna', 'import', 'export context', 'save memory', 'remember this', 'checkpoint', 'save context', 'snapshot', or needs to manage project knowledge — importing external files, exporting session context, saving quick notes, or checkpointing working context mid-session."
---

# Kivna — Knowledge Management

From Gaelic "cuimhne" (memory), respelled phonetically.

Single owner of the project's knowledge layer. Sessions, memories, imports, exports all live under `kivna/`.

## Folder Convention

- `kivna/context.md` — living working context, overwritten each checkpoint (committed to git)
- `kivna/checkpoints/` — daily archives of previous context versions (committed to git)
- `kivna/sessions/` — full session logs written by switch (committed to git)
- `kivna/memories/` — quick notes captured mid-session (committed to git)
- `kivna/input/` — drop files here for import (should be gitignored, transit folder)
- `kivna/output/` — exports land here (should be gitignored, transit folder)

## Commands

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

6. **Clean up.** Delete the processed files from `kivna/input/`. Leave any files the user said to skip.

7. **Report.** Tell the user what was imported and where it went.

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

### `/kivna memory` — Quick Save

Save a note mid-session without ceremony.

- Takes freeform text as the argument: `/kivna memory decided to use PostgreSQL over SQLite for concurrency reasons`
- Append a timestamped entry to `kivna/memories/YYYY-MM-DD.md`
- One file per day, multiple entries with timestamps
- Create the file and `kivna/memories/` directory if they don't exist
- Quick confirmation only — no approval flow

Format in the memories file:

```
## HH:MM

[note text]
```

### `/kivna checkpoint` — Context Snapshot

Capture the current working context to `kivna/context.md`. This is the anti-context-rot mechanism — write frequently at natural breakpoints so compaction or session boundaries don't lose the thinking.

1. **Archive the current context.** If `kivna/context.md` exists and has content beyond the skeleton, append its content to `kivna/checkpoints/YYYY-MM-DD.md` with a `## HH:MM` timestamp header and a `---` separator. Create the file and directory if they don't exist.

2. **Write the new context.** Overwrite `kivna/context.md` with the current working state:

```markdown
# Context — [Project Name]

## Current Focus
[What we're actively working on. The task, the approach, where we are in it.]

## Mental Model
[The high-level understanding of how things fit together right now. Not architecture docs — the working theory that guides decisions.]

## Decisions
[Each decision with full reasoning. What was considered, what was rejected, why the chosen approach won.]

## Rejected Approaches
[Things we tried or considered and ruled out. With reasons. Prevents re-exploring dead ends.]

## Working Assumptions
[Things established as true that aren't written anywhere else. Constraints discovered, behaviors observed, limits hit.]

## Active Threads
[Partial work, what's in progress, what's blocking, what's queued next.]

## Open Questions
[Unresolved things that need input or investigation.]
```

3. **Quick confirmation.** No approval flow — same as `/kivna memory`. Just confirm what was written.

Triggered automatically by `/kerd:dian` at task boundaries and close-out. Also available manually anytime.

## Notes

- `kivna/input/` and `kivna/output/` should be in `.gitignore` — they're transit folders, not project content.
- `kivna/sessions/` and `kivna/memories/` should be committed to git — they're permanent history.
- Exports are written in plain markdown so any LLM can read them.
- When importing LLM session transcripts, be aggressive about filtering. Most of a chat session is noise. Extract the signal: decisions, code patterns, insights, action items.
- When importing PDFs or reports, focus on what's actionable for THIS project.
- `kivna/context.md` and `kivna/checkpoints/` should be committed to git — they're the session's working memory.
- Context checkpoints are cumulative, not incremental. Each checkpoint captures the full working state, not just deltas.
- On cold start, read `kivna/context.md` alone. The archive in `kivna/checkpoints/` is for tracing decisions back, not for restore.
