---
name: switch
description: "Use when the user says 'switch', 'switching machines', 'wrapping up', 'picking up', 'handoff', or needs to cleanly leave or arrive on a machine. Handles all git boundary operations (pull, push, commit of session state)."
---

# Switch — Machine Handoff

Clean handoff between machines. Switch owns all git boundary operations — pull, push, commit of session state. No other skill should do these things.

## Usage

`/switch out` — leaving this machine
`/switch in` — arriving on a new machine

If no argument is given, check for uncommitted changes. If changes exist, assume `out`. If clean, assume `in`.

## Switch Out — Leaving This Machine

Wrap up everything so the next machine can pick up cold.

### 1. Write session state to TODO.md

Create TODO.md if it doesn't exist. Update the `## Current Session` block with:
- What was done (check off completed items)
- What's in progress (mark clearly)
- What's next (so the next session knows where to start)
- Any context that would be lost (decisions made in conversation, things tried that didn't work, open questions)

### 2. Write session log

Create `kivna/sessions/YYYY-MM-DD.md` (or append if one already exists for today) with:

```
# Session — YYYY-MM-DD

**Machine:** [hostname from `hostname`]

## What Was Done
[Concrete list of what was accomplished. Be specific: files created, features built, bugs fixed, decisions made.]

## Key Decisions
[Any decisions made during the session with brief reasoning. Skip if none.]

## Commits
[List commit hashes and messages from this session]

## Insights
[Observations about the codebase, patterns discovered, things that surprised you. Skip if none.]

## What's Next
[What the next session should pick up]
```

If appending to an existing file for today (multiple sessions), add a `---` separator and a new section with a time or sequence number.

### 3. Update the vault

If a `/kerd:dian` session was active, close-out should have already called `/kerd:kivna save`. Verify vault `[Name] Status.md` reflects this session and move on. If no `/kerd:dian` session was running (quick switch without formal session), call `/kerd:kivna save` now — this updates Status.md and proposes updates to other vault files, each with user approval.

### 4. Update progress tracking

If progress tracking exists (check for `docs/project/progress.md`, `progress.md`, or similar), update it.

### 5. Reflect and capture learnings

Before committing, reflect on the session:

- **What patterns emerged?** Any recurring problems, useful approaches, or workflow improvements worth codifying?
- **What should be remembered?** Best practices discovered, gotchas encountered, conventions that worked well or didn't.
- **What would make the next session better?** Anything about the project, tooling, or workflow that should be adjusted.

Write actionable learnings to the appropriate place:
- **Project conventions and enforcement rules** → add to `CLAUDE.md` (so they're enforced in future sessions)
- **Conventions and patterns** → flag for the appropriate vault file (Architecture Decisions, Positioning Contract, etc.) — these get proposed during the `/kerd:kivna save` step
- **Project-specific gotchas** → add to `docs/playbook.md` Gotchas section

Skip this step if the session was trivial (quick fix, single file change). But for any session with meaningful work, take the time — compounding small improvements across sessions is how projects stay healthy.

### 6. Stage and commit

Stage all work including the session log and doc updates. Use a descriptive commit message.

### 7. Push

Push to remote. Verify the push succeeds.

### 8. Verify

Run `git status` and confirm the working tree is clean and nothing remains uncommitted. If uncommitted changes remain, go back to step 6 — do not proceed to the confirm step until the tree is clean.

### 9. Confirm

Print a short summary: what was pushed, what the next session should start with.

## Switch In — Arriving on This Machine

Pick up where the other machine left off.

### 1. Pull

`git pull`. If there are conflicts, resolve them before proceeding.

### 2. Smoke test

If the project has a test command (check `package.json` scripts, `Makefile`, `pyproject.toml`, or similar), run it. If tests fail, report the failures in the summary — the user should know the state of the codebase before planning new work. If no test command exists, skip this step.

### 3. Read TODO.md

Focus on the `## Current Session` block. This is where the last session left off.

### 4. Read vault

Discover the vault path using `kivna/vault.json` or convention (see `/kerd:kivna` vault discovery). Read `[Name] Status.md` for where the project stands. Read the MOC (`[Name].md`) to discover what other vault files exist and read any that are relevant (Architecture Decisions, Playbook, etc.).

### 5. Check session logs

Read the latest file(s) in `kivna/sessions/` for detailed context on what happened recently.

### 6. Read progress tracking

If progress tracking exists, read it.

### 7. Check active modes

If `kivna/.active-modes` exists and is non-empty, read it. Report any active modes in the summary (e.g., "**Active modes:** `dian: execute`"). If the file doesn't exist or is empty, skip this — don't mention modes.

### 8. Summarize

Tell the user:
- What was done last session
- What's in progress or queued next
- Any open questions or decisions from the previous session
- Any test failures from the smoke test (if applicable)
- Suggest what to work on

### 9. Offer dian

Ask: "Start a `/kerd:dian` session?" If yes, flow into `/kerd:dian` orient. If no, stop — user wants to do something quick without full session discipline.

## Fallback Behavior

If no TODO.md or session logs exist (fresh repo), say so cleanly:

"Fresh repo — no previous session state found. No TODO.md, no session logs in kivna/sessions/. Ready to start from scratch."

If no vault is found (no `kivna/vault.json` and no vault folder at `~/Obsidian/[folder]/`), report this gracefully — suggest running `/kerd:kivna scaffold` to set up the vault.

Do not fail silently or produce errors for missing files.
