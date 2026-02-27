---
name: dian
description: "Use when starting a work session, when you need structured session discipline, or when the user says 'dian', 'session', 'let's get structured', or wants to plan and track a focused work block. Provides orient-plan-execute-close protocol."
---

# Dian — Session Discipline

From Irish/Scottish Gaelic "dian" — intense, rigorous. Pronounced "DEE-an".

A protocol for staying focused within a session. Dian does not touch git boundaries (pull/push) — that's switch's job. Dian keeps you on track once you're working.

## The Protocol

### 1. Orient

Read these files if they exist (skip any that don't):

1. `TODO.md` — current session plan, roadmap, task queue
2. `CLAUDE.md` — project conventions and structure
3. Progress tracking — check `docs/project/progress.md`, `progress.md`, or `CHANGELOG.md`
4. Decision log — check `docs/project/decisions.md` or `decisions.md` if the work involves architecture choices

Summarize the current state for the user.

### 2. Plan

Propose a session plan to the user:
- What we'll do (numbered steps)
- What files we'll touch
- What docs need updating

Write this as a `## Current Session` block in TODO.md with today's date. Wait for user approval before executing.

### 3. Execute

Do the work. Commit incrementally if it makes sense. Stay focused on the plan — if scope creep appears, flag it and add it to TODO.md for later rather than chasing it now.

### 4. Close Out

Before ending the session:

1. **Update TODO.md** — check off completed tasks, add new ones discovered during work, update roadmap statuses, clear the `## Current Session` block.
2. **Doc impact assessment** — if the project has a Doc Impact Table in CLAUDE.md, check it. Update ALL affected docs.
3. **Staleness sweep** — search for any renamed or changed concepts across `docs/`, `README.md`, and other documentation.
4. **Run checks** — run the project's build/test command if one exists. Do not close out with failing tests.

## Principles

- **No git boundary ops.** No `git pull`, no `git push`. Use `/switch` for that.
- **Flag scope creep.** If something comes up that isn't in the plan, add it to TODO.md and stay on track.
- **Incremental commits.** Commit working states, not big bangs.
- **Docs travel with code.** If you change behavior, update the docs in the same commit.
