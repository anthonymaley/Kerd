---
name: dian
description: "Use when starting a work session, when you need structured session discipline, or when the user says 'dian', 'session', 'let's get structured', or wants to plan and track a focused work block. Provides orient-plan-execute-close protocol."
---

# Dian (Session Discipline)

From Irish/Scottish Gaelic "dian," intense, rigorous. Pronounced "DEE-an".

A protocol for staying focused within a session. Dian does not touch git boundaries (pull/push). That's switch's job. Dian keeps you on track once you're working.

## Mode Markers

Dian is a modal skill. It runs across multiple responses. Announce the current phase so the user always knows what's active.

**On every phase transition**, output a marker on its own line at the top of your response:

- `[dian: orient]` reading context, summarizing state
- `[dian: plan]` proposing session plan
- `[dian: execute]` working through tasks
- `[dian: close-out]` updating docs, running checks
- `[dian: closed]` session complete (final marker, then done)

**State file:** When entering a phase, write the current phase to `kivna/.active-modes`. When closing out, remove the dian line from the file (or delete the file if it's the only entry). This lets `/kerd:switch in` report active modes.

Format of `kivna/.active-modes` (one skill per line):
```
dian: execute
```

## The Protocol

### 1. Orient

Output `[dian: orient]` at the top of your response.

Read these files if they exist (skip any that don't):

1. `TODO.md`: current session plan, roadmap, task queue
2. `CLAUDE.md`: project conventions and structure
3. Vault: discover the vault path using `kivna/vault.json` or convention (see `/kerd:kivna` vault discovery). Read `[Name] Status.md` for where the project stands. Read the MOC (`[Name].md`) to discover what other vault files exist (Architecture Decisions, Playbook, etc.) and read any that are relevant to the planned work.
4. Progress tracking: check `docs/project/progress.md`, `progress.md`, or `CHANGELOG.md`
5. `docs/playbook.md`: project playbook (how to rebuild this project from scratch)

**Consistency sniff test:** After reading, do a quick cross-check. Does CLAUDE.md reference files or conventions that don't match the codebase? Does the playbook's tech stack or architecture still match reality? Does the vault Status mention things that have since changed? Flag any contradictions to the user before planning. Don't build on stale assumptions.

Summarize the current state for the user, including any inconsistencies found.

### 2. Plan

Output `[dian: plan]` at the top of your response.

Propose a session plan to the user:
- What we'll do (numbered steps)
- What files we'll touch
- What docs need updating
- How we'll verify each task worked (what does "done" look like?)

**Before writing the plan, interrogate the task.** Ask clarifying questions about anything ambiguous. Push back on things that don't make sense or seem underspecified. Do not guess or infer context. If you're unsure about something, ask. It's cheaper to spend two minutes clarifying than to build the wrong thing and rework it.

**Specifically, challenge yourself on:**
- Do I actually understand what the user wants, or am I filling in gaps with assumptions?
- Are there dependencies between tasks that affect the order?
- Is anything in the plan vague enough that I might interpret it differently than the user intended?
- What could go wrong, and how will I catch it?

Write this as a `## Current Session` block in TODO.md with today's date. Wait for user approval before executing. Do not proceed until the user confirms the plan. A good plan prevents rework.

### 3. Execute

Output `[dian: execute]` at the top of your response when entering this phase.

Do the work. Commit incrementally if it makes sense. Stay focused on the plan. If scope creep appears, flag it and add it to TODO.md for later rather than chasing it now.

**Verify after each task.** Before moving to the next task, confirm the work actually does what was intended. Run tests if they exist, re-read the changed files, check for obvious issues. If something isn't right, fix it now. Don't accumulate problems for close-out to discover.

**Record decisions immediately.** When a significant decision is made during execution (architecture choice, rejected approach, key trade-off), record it in the session log (`kivna/sessions/`) and in TODO.md context. Don't defer decision recording to close-out. Decisions lose their reasoning if you wait. The vault gets updated once at close-out via `/kerd:kivna save`.

**Docs travel with code, enforced.** If a task changes behavior, update the affected docs (README, playbook, CLAUDE.md) in the same commit. Don't defer doc updates to close-out. The principle is: no commit should leave docs inconsistent with code.

**No mid-session vault writes.** Work accumulates in repo-side files (session log, TODO.md) during execution. The vault gets one clean update at close-out. This keeps the vault lean and searchable: one session, one update.

### 4. Close Out

Output `[dian: close-out]` at the top of your response.

Before ending the session:

1. **Update TODO.md**: check off completed tasks, add new ones discovered during work, update roadmap statuses, clear the `## Current Session` block.
2. **Doc impact assessment**: if the project has a Doc Impact Table in CLAUDE.md, check it. Update ALL affected docs.
3. **Update the vault**: call `/kerd:kivna save` once. This updates vault `[Name] Status.md` (with approval) and proposes updates to any other vault files where new knowledge belongs. This is the single vault write for the session.
4. **Update playbook**: if `docs/playbook.md` exists, update it with anything learned this session: new setup steps, new integrations, gotchas discovered, tech stack changes, updated Current Status section. If it doesn't exist, create it from the skeleton:

```markdown
# Playbook: [Project Name]

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

5. **Diff review**: run `git diff` (or `git diff --cached` if staged) to review everything changed this session. Look for accidental changes, forgotten files, inconsistencies between code and docs, anything that doesn't match the plan. Fix issues before proceeding.
6. **Staleness sweep**: search for any renamed or changed concepts across `docs/`, `README.md`, and other documentation.
7. **Run checks**: run the project's build/test command if one exists. Do not close out with failing tests.
8. **Clear mode marker**: remove the dian line from `kivna/.active-modes`. Output `[dian: closed]` as the final marker.

## Principles

- **No git boundary ops.** No `git pull`, no `git push`. Use `/kerd:switch` for that.
- **Flag scope creep.** If something comes up that isn't in the plan, add it to TODO.md and stay on track.
- **Incremental commits.** Commit working states, not big bangs.
- **Docs travel with code.** If you change behavior, update the docs in the same commit.
