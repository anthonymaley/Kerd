# Kerd Modes: Design

Session configurations that prime the right tools for a type of work. Modes don't call other skills directly. They set up the session, present a customizable flow, and guide you through it.

## Concept

A mode is a session configuration. When invoked, Kerd:

1. Loads the mode definition (a markdown file with YAML frontmatter)
2. Checks which core skills are installed
3. Auto-discovers extra skills from installed plugins using keywords
4. Presents the flow as an editable checklist
5. Lets the user customize (skip steps, reorder, add custom steps)
6. Tracks progress through the flow during the session

Modes are the orchestration layer across Kerd, GSD, Superpowers, and any other installed plugins.

## Invocation

```
/kerd:mode                    list all available modes by category
/kerd:mode greenfield         load and start the greenfield flow
/kerd:mode maintain           load and start the maintenance flow
```

## File structure

```
modes/
  greenfield.md
  quickfix.md
  deepwork.md
  maintain.md
  strategy.md
  writing.md
  research.md
  legal.md
  sales.md
```

One file per mode. Contributors PR a single file to add a mode. No manifest updates needed. Kerd auto-discovers mode files from the `modes/` directory.

## Mode file format

```markdown
---
name: greenfield
description: "Build a new feature from scratch using spec-driven development"
category: development
core_skills:
  - gsd:new-project
  - gsd:discuss-phase
  - gsd:plan-phase
  - gsd:execute-phase
  - gsd:verify-work
  - superpowers:brainstorming
  - superpowers:test-driven-development
  - superpowers:verification-before-completion
  - superpowers:requesting-code-review
  - kerd:switch
  - kerd:slainte
discover_keywords:
  - "feature"
  - "implementation"
  - "testing"
  - "code review"
  - "deployment"
---

# Greenfield: Build a New Feature

## Setup
- [ ] `/kerd:switch in` — pull, get context
- [ ] Confirm: what are we building?

## Spec
- [ ] `/gsd:new-project` — questions, research, requirements, roadmap
- [ ] Review and approve roadmap

## Build (repeat per phase)
- [ ] `/gsd:discuss-phase N` — capture decisions
- [ ] `/gsd:plan-phase N` — research + task plans
- [ ] `/gsd:execute-phase N` — parallel execution
- [ ] `/gsd:verify-work N` — confirm it works

## Close
- [ ] `/kerd:slainte docs` — health check
- [ ] `/kerd:switch out` — commit, push, vault update
```

### Frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Mode identifier (lowercase, single word or hyphenated) |
| `description` | yes | One-line description shown in mode listing |
| `category` | yes | Grouping: `development`, `business`, `maintenance`, `creative` |
| `core_skills` | yes | Skills this mode depends on (checked on load) |
| `discover_keywords` | no | Keywords for auto-discovering extra skills from installed plugins |

### Body

The markdown body is the flow. Uses standard checkbox format (`- [ ]`). Sections group related steps. The body is displayed to the user and used for progress tracking.

## The mode skill mechanic

### 1. Load

Read `modes/<name>.md`. Parse frontmatter and body. If mode not found, list available modes.

### 2. Check core skills

For each skill in `core_skills`, check if the plugin is installed (scan `~/.claude/plugins/`). Report status:

```
Core skills:
  ✓ gsd:new-project
  ✓ superpowers:brainstorming
  ✗ superpowers:test-driven-development (not installed)
```

Missing core skills are a warning, not a blocker.

### 3. Auto-discover extras

Scan installed plugins for skills whose descriptions match `discover_keywords`. Show matches not already in the core list:

```
Discovered extras:
  + superpowers:using-git-worktrees — isolate feature work
  + pr-review-toolkit:review-pr — comprehensive PR review
```

Suggestions only. Displayed once.

### 4. Present and customize

Display the flow as a numbered checklist. All steps enabled by default. Ask the user to customize:

```
Greenfield flow:

  [x] 1. /kerd:switch in — pull, get context
  [x] 2. Confirm: what are we building?
  [x] 3. /gsd:new-project — questions, research, requirements
  [x] 4. /gsd:discuss-phase N — capture decisions
  [x] 5. /gsd:plan-phase N — research + task plans
  [x] 6. /gsd:execute-phase N — parallel execution
  [x] 7. /gsd:verify-work N — confirm it works
  [x] 8. /kerd:slainte docs — health check
  [x] 9. /kerd:switch out — commit, push, vault

Edit the flow? (skip steps, reorder, add custom steps, or 'go' to start)
```

User can:
- Skip steps: "skip 4 and 8"
- Add steps: "add 'run migrations' after step 6"
- Reorder: "move 8 before 7"
- Start: "go"

Once the user says go, the flow is locked and progress tracking begins.

### 5. Track progress

Store active mode state in `kivna/.active-modes` (same file dian uses). After each step completes, check it off and remind the user what's next. If the user goes off-script, don't block them. Note where they are when they come back.

### 6. Complete

When all steps are checked off (or the user says done), clear the mode from `.active-modes`.

## Starter modes

### Development
- **greenfield** — new feature, full spec-driven flow (GSD + Superpowers + Kerd)
- **quickfix** — bug fix or small change (Superpowers debugging/TDD + Kerd light)
- **deepwork** — existing feature, no GSD, dian-driven (Kerd dian + Superpowers)
- **maintain** — health loop: tend, slainte, lorg, skriv audit

### Business
- **strategy** — positioning, go-to-market, competitive analysis (skriv + brainstorming + sales skills)
- **writing** — prose creation: blog posts, docs, investor updates (skriv + brainstorming)
- **research** — investigation, due diligence, market analysis (brainstorming + firecrawl)

### Operations
- **legal** — contract review, compliance, policy drafting (skriv + relevant legal skills)
- **sales** — pipeline review, call prep, outreach (sales plugin skills)

## Community contribution

To add a mode:
1. Create `modes/<name>.md` following the format above
2. PR to the Kerd repo
3. Mode is available to all users on next plugin update

No manifest changes needed. Kerd auto-discovers modes from the `modes/` directory.

## What modes don't do

- **Don't call skills directly.** Modes set context and guide. The user invokes each tool.
- **Don't enforce order.** The flow is a recommendation. Users can skip around.
- **Don't require all core skills.** Missing skills are warnings. The mode adapts.
- **Don't replace dian.** Dian is session discipline within a mode. A mode can include dian as a step.

## Implementation notes

- New skill: `skills/mode/SKILL.md`
- New directory: `modes/` at repo root
- Mode state: reuse `kivna/.active-modes` format
- Auto-discover: scan `~/.claude/plugins/cache/` for installed skill descriptions
- No new dependencies. Pure markdown and file reads.
