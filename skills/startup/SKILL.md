---
name: startup
description: "Use when the user says 'startup', 'set up this project', 'initialize kerd', 'scaffold', or needs to set up a new project with Kerd conventions. One-time setup that creates directory structure, docs, and initial commit."
---

# Startup — Project Scaffold

One-time setup for a new project. Creates Kerd directory structure, initial docs, and pushes the scaffold. Assumes the git repo already exists with a remote configured.

## Usage

`/kerd:startup` — run in the root of a git repo

## The Process

### 1. Verify git

Confirm `.git` exists. If not, stop: "No git repo found. Initialize a repo and set up a remote first, then run `/kerd:startup` again."

### 2. Gather context

Ask the user two things:
- **Project name** — used in README and playbook headers
- **One-line description** — what this project does

### 3. Create directory structure

```
kivna/
kivna/sessions/
docs/
```

### 4. Create files

**`README.md`**

```markdown
# [Project Name]

[One-line description]
```

**`TODO.md`**

```markdown
# TODO

## Current Session

## Backlog
```

**`CLAUDE.md`**

```markdown
# [Project Name]

## Session Workflow

When wrapping up a session (`/kerd:switch out` or `/kerd:dian`):
1. Update `TODO.md` — check off completed items, add new ones
2. Update `docs/playbook.md` — if any new steps, tools, or config were added during the session, add them to the playbook. Always update the "Current Status" section.

## Doc Impact Table

| Doc | Update When |
|-----|-------------|
| README.md | Project description, setup steps, or structure changes |
| docs/playbook.md | New setup steps, integrations, gotchas, tech stack changes, or status changes |
| TODO.md | Every session close-out |
```

**`docs/playbook.md`**

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

**`.sotu`**

```
# SOTU Audit Targets

## docs
- README.md
- docs/

## playbook
- docs/playbook.md
```

**`kivna/vault.json`**

```json
{
  "vault": "~/ObsidianLLM",
  "folder": "[project-name-lowercase]",
  "name": "[Project Name]"
}
```

### 5. Set up Obsidian vault

Run the `/kerd:kivna scaffold` mechanic to create the vault folder at `~/ObsidianLLM/[folder]/` with symlinks, MOC, Context, Log, and Decisions files. Since this is a fresh project, seed the Context with a "project initialized" section and the Log with a single "project scaffolded" entry.

### 6. Commit

Stage all created files. Commit with message: "feat: initialize project with Kerd scaffold"

### 7. Push

Push to remote. Verify the push succeeds.

### 8. Confirm

Print what was created (list of files and vault folder) and suggest: "Scaffold ready. Run `/kerd:dian` to start your first session."

## What Startup Does NOT Do

- No `git init` or remote setup — repo must already exist
- No tech stack decisions — those happen in the first dian session
- No skill file copying — Kerd skills live in the Kerd repo, not in each project
- No `.gitignore` setup — user handles that based on their stack

## Idempotency

If files already exist (e.g., README.md was created during repo init), do not overwrite them. Skip existing files and note which were skipped. Only create files that don't exist yet.
