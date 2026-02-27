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

## What's Next
[What the next session should pick up]
```

If appending to an existing file for today (multiple sessions), add a `---` separator and a new section with a time or sequence number.

### 3. Update progress tracking

If progress tracking exists (check for `docs/project/progress.md`, `progress.md`, or similar), update it.

### 4. Stage and commit

Stage all work including the session log and doc updates. Use a descriptive commit message.

### 5. Push

Push to remote. Verify the push succeeds.

### 6. Confirm

Print a short summary: what was pushed, what the next session should start with.

## Switch In — Arriving on This Machine

Pick up where the other machine left off.

### 1. Pull

`git pull`. If there are conflicts, resolve them before proceeding.

### 2. Read TODO.md

Focus on the `## Current Session` block. This is where the last session left off.

### 3. Check session logs

Read the latest file(s) in `kivna/sessions/` for detailed context on what happened recently.

### 4. Read progress tracking

If progress tracking exists, read it.

### 5. Summarize

Tell the user:
- What was done last session
- What's in progress or queued next
- Any open questions or decisions from the previous session
- Suggest what to work on

### 6. Ask

"Ready to continue, or do you want to change direction?"

## Fallback Behavior

If no TODO.md or session logs exist (fresh repo), say so cleanly:

"Fresh repo — no previous session state found. No TODO.md, no session logs in kivna/sessions/. Ready to start from scratch."

Do not fail silently or produce errors for missing files.
