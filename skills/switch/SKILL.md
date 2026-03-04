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

### 3. Ensure context is current

If `kivna/context.md` exists and a `/kerd:dian` session was active, close-out should have already updated it — verify it's current and move on. If no `/kerd:dian` session was running (quick switch without formal session), write a checkpoint now using the `/kerd:kivna checkpoint` mechanic.

### 4. Update progress tracking

If progress tracking exists (check for `docs/project/progress.md`, `progress.md`, or similar), update it.

### 5. Stage and commit

Stage all work including the session log and doc updates. Use a descriptive commit message.

### 6. Push

Push to remote. Verify the push succeeds.

### 7. Verify

Run `git status` and confirm the working tree is clean and nothing remains uncommitted. If uncommitted changes remain, go back to step 5 — do not proceed to the confirm step until the tree is clean.

### 8. Confirm

Print a short summary: what was pushed, what the next session should start with.

## Switch In — Arriving on This Machine

Pick up where the other machine left off.

### 1. Pull

`git pull`. If there are conflicts, resolve them before proceeding.

### 2. Read TODO.md

Focus on the `## Current Session` block. This is where the last session left off.

### 3. Read working context

If `kivna/context.md` exists, read it. This has the decisions, reasoning, active threads, and assumptions from the last session. It's the richest source for picking up where things left off.

### 4. Check session logs

Read the latest file(s) in `kivna/sessions/` for detailed context on what happened recently.

### 5. Read progress tracking

If progress tracking exists, read it.

### 6. Summarize

Tell the user:
- What was done last session
- What's in progress or queued next
- Any open questions or decisions from the previous session
- Suggest what to work on

### 7. Offer dian

Ask: "Start a `/kerd:dian` session?" If yes, flow into `/kerd:dian` orient. If no, stop — user wants to do something quick without full session discipline.

## Fallback Behavior

If no TODO.md or session logs exist (fresh repo), say so cleanly:

"Fresh repo — no previous session state found. No TODO.md, no session logs in kivna/sessions/. Ready to start from scratch."

Do not fail silently or produce errors for missing files.
