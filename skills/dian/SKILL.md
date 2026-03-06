---
name: dian
description: "Use when starting a work session, when you need structured session discipline, or when the user says 'dian', 'session', 'let's get structured', or wants to plan and track a focused work block. Provides orient-plan-execute-close protocol."
---

# Dian — Session Discipline

From Irish/Scottish Gaelic "dian" — intense, rigorous. Pronounced "DEE-an".

A protocol for staying focused within a session. Dian does not touch git boundaries (pull/push) — that's switch's job. Dian keeps you on track once you're working.

## Mode Markers

Dian is a modal skill — it runs across multiple responses. Announce the current phase so the user always knows what's active.

**On every phase transition**, output a marker on its own line at the top of your response:

- `[dian: orient]` — reading context, summarizing state
- `[dian: plan]` — proposing session plan
- `[dian: execute]` — working through tasks
- `[dian: close-out]` — updating docs, running checks
- `[dian: closed]` — session complete (final marker, then done)

**State file:** When entering a phase, write the current phase to `kivna/.active-modes`. When closing out, remove the dian line from the file (or delete the file if it's the only entry). This lets `/kerd:switch in` report active modes.

Format of `kivna/.active-modes` (one skill per line):
```
dian: execute
```

## The Protocol

### 1. Orient

Output `[dian: orient]` at the top of your response.

Read these files if they exist (skip any that don't):

1. `TODO.md` — current session plan, roadmap, task queue
2. `CLAUDE.md` — project conventions and structure
3. `kivna/context.md` — working context from the last checkpoint (decisions, reasoning, active threads, assumptions)
4. Progress tracking — check `docs/project/progress.md`, `progress.md`, or `CHANGELOG.md`
5. Decision log — check `docs/project/decisions.md` or `decisions.md` if the work involves architecture choices
6. `docs/playbook.md` — project playbook (how to rebuild this project from scratch)

Summarize the current state for the user.

### 2. Plan

Output `[dian: plan]` at the top of your response.

Propose a session plan to the user:
- What we'll do (numbered steps)
- What files we'll touch
- What docs need updating

Write this as a `## Current Session` block in TODO.md with today's date. Wait for user approval before executing.

### 3. Execute

Output `[dian: execute]` at the top of your response when entering this phase.

Do the work. Commit incrementally if it makes sense. Stay focused on the plan — if scope creep appears, flag it and add it to TODO.md for later rather than chasing it now.

**Auto-save:** After completing each task in the plan, update `kivna/context.md` with the current working context using the `/kerd:kivna save` mechanic (archive previous version, write new one). This ensures context survives compaction mid-session.

### 4. Close Out

Output `[dian: close-out]` at the top of your response.

Before ending the session:

1. **Update TODO.md** — check off completed tasks, add new ones discovered during work, update roadmap statuses, clear the `## Current Session` block.
2. **Doc impact assessment** — if the project has a Doc Impact Table in CLAUDE.md, check it. Update ALL affected docs.
3. **Finalize context** — update `kivna/context.md` with end-of-session state. Mark "Current Focus" as completed or paused. Update "Active Threads" to reflect what's done and what carries over. This becomes the cold-start document for the next session.
4. **Update playbook** — if `docs/playbook.md` exists, update it with anything learned this session: new setup steps, new integrations, gotchas discovered, tech stack changes, updated Current Status section. If it doesn't exist, create it from the skeleton:

```markdown
# Playbook — [Project Name]

How to rebuild this project from scratch.

## Tech Stack
[What tools/frameworks and why they were chosen]

## Setup
[Steps to get the project running locally]

## Architecture
[Key structural decisions and why]

## Integrations
[External services, APIs, config needed]

## Deployment
[How to deploy, environment variables needed]

## Gotchas
[Things that broke, non-obvious behavior, workarounds]

## Current Status
[What's working, what's in progress, what's next]
```

5. **Staleness sweep** — search for any renamed or changed concepts across `docs/`, `README.md`, and other documentation.
6. **Run checks** — run the project's build/test command if one exists. Do not close out with failing tests.
7. **Clear mode marker** — remove the dian line from `kivna/.active-modes`. Output `[dian: closed]` as the final marker.

## Principles

- **No git boundary ops.** No `git pull`, no `git push`. Use `/kerd:switch` for that.
- **Flag scope creep.** If something comes up that isn't in the plan, add it to TODO.md and stay on track.
- **Incremental commits.** Commit working states, not big bangs.
- **Docs travel with code.** If you change behavior, update the docs in the same commit.
