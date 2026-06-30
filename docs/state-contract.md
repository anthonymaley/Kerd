# Shared State Contract

Kerd skills share state through a small set of files. This document defines who owns each file, who reads it, what format it uses, and what the rules are.

## TODO.md

**Owner:** conductor (writes session plan), switch (writes session wrap-up)
**Readers:** switch (in), SessionStart hook, lorg (work signals), kivna out (backlog export)
**Committed:** yes

### Format

```markdown
# TODO

## Current Session
(completed YYYY-MM-DD)

### Done this session
- [x] completed items

### Context
- Mode active: <name> (step N of M)
  Instruction: <session instruction>
  Steps: N done, N current, N pending
- Other context that would be lost

## Backlog
- unchecked items
```

### Rules

- **TODO.md is forward-only.** It contains only `## Current Session` (forward-looking state) and `## Backlog`. The record of completed work is its `kivna/sessions/<date>.md` log — never a retained TODO entry.
- `## Current Session` is **overwritten in place** each session by conductor (plan phase) or switch (out): replaced with forward-looking state (in-progress, what's next, open decisions), never the prior session's content.
- **Anti-pattern — demote-and-keep.** Renaming `## Current Session` → `## Previous Session` (or `## Older Session`) and keeping it is forbidden. Such blocks must not exist in TODO.md; `switch out` heals any that appear by archiving them to `kivna/sessions/`.
- `### Context` within Current Session holds the mode snapshot for cross-machine handoff
- `## Backlog` is append-only (items added, never silently removed). Checked-off items can be cleaned by trim.
- conductor writes the plan, switch writes the wrap-up. They don't conflict because conductor runs within a session and switch runs at the boundary.

## kivna/.active-modes

**Owner:** each skill owns its own line(s)
**Readers:** switch (in), Stop hook, SessionStart hook, PostToolUse hook, mode skill
**Committed:** no (gitignored, ephemeral)

### Format

```
# One line per skill: <skill>: <state>
conductor: execute
skriv: active
mode: greenfield (step 3 of 9)
  instruction: focus on pricing strategy only
  steps:
    1: /kerd:switch in | open session, set context [done]
    2: /superpowers:brainstorming | explore the problem space [done]
    3: /superpowers:writing-plans | produce the implementation plan [current]
    4: /superpowers:executing-plans 1 | build phase 1 [pending]
    5: /kerd:switch out | close session [pending]
```

### Rules

- Each skill writes only its own line(s). Never touch another skill's entries.
- Removing a line means the skill is inactive. Don't write `skill: off`.
- Mode's `steps:` block uses format: `<id>: <skill> [<args>] | <label> [<status>]`
- Status markers: `[done]`, `[current]`, `[pending]`, `[skipped]`
- Step IDs are stable integers assigned at mode start.
- Hooks read this file but never write to it.
- PostToolUse hook receives a full envelope on stdin (confirmed 2026-04-04):
  `{session_id, cwd, hook_event_name, tool_name, tool_input: {skill, args}, tool_response: {success, commandName}, tool_use_id}`
  The hook checks `tool_response.success` before reporting progress and extracts `tool_input.skill` via sed.
- Switch out snapshots mode state to TODO.md Context block before committing (cross-machine handoff).

## kivna/sessions/YYYY-MM-DD.md

**Owner:** switch (creates on out)
**Readers:** switch (in), conductor (orient), lorg (work signals), kivna out (decisions export)
**Committed:** yes

### Format

```markdown
# Session — YYYY-MM-DD

**Machine:** [hostname]

## What Was Done
[concrete list]

## Key Decisions
[decisions with reasoning]

## Commits
[hash + message list]

## What's Next
[next session pickup]
```

### Rules

- One file per day. Multiple sessions append with `---` separator.
- Switch is the sole creator. Conductor records decisions in TODO.md during execution; switch captures them in the session log at the boundary.
- Session logs are append-only within a day, overwritten across days (each day starts fresh).

## Vault Status.md

**Owner:** kivna save
**Readers:** switch (in), conductor (orient), lorg (work signals), kivna out (status export)
**Committed:** no (lives in vault at `~/eolas/vault/[project]/`)

### Format

```markdown
# [Name] Status

## Where We Are
[current state]

## What's Open
[open questions, blockers]

## What's Next
[prioritized next steps]
```

### Rules

- Overwritten each save, not appended to. Always show diff and get approval.
- kivna save is the sole writer. One vault write per session (at close-out), not per-task.
- Switch out calls kivna save at session close. Conductor no longer calls it; switch owns the vault save.

## kivna/output/ (KIF exports)

**Owner:** kivna out
**Readers:** kivna in (on another project), external LLMs
**Committed:** no (gitignored)

### Format

Two files per export:
- `export-YYYY-MM-DD.kif.toon` — TOON format (LLM handoff, export only)
- `export-YYYY-MM-DD.kif.json` — JSON format (machine import)

### Rules

- Both files produced on every export. Overwrite previous exports for the same date.
- Import only reads `.kif.json`. TOON is for LLM consumption only.
- Exports are repo-grounded: artifacts first, conversation fills gaps.

## docs/lorg-report.md

**Owner:** lorg
**Readers:** lorg report (display), switch (in, mentioned in summary if relevant)
**Committed:** yes

### Rules

- Overwritten each scan. Not append-only.
- Duplicate copy written to vault (`[Name] Lorg Report.md`).
- Includes `Last scanned: YYYY-MM-DD` date line.

## Cross-Skill Interaction Summary

| File | conductor | switch | mode | skriv | kivna | slainte | tend | lorg | hooks |
|------|------|--------|------|-------|-------|---------|------|------|-------|
| TODO.md | W | W/R | - | - | R | - | - | R | R |
| .active-modes | W/R | R | W | W | - | - | - | - | R |
| sessions/ | - | W | - | - | R | - | - | R | - |
| vault Status | - | R | - | - | W | - | - | R | - |
| KIF exports | - | - | - | - | W | - | - | - | - |
| lorg-report | - | - | - | - | - | - | - | W | - |

W = writes, R = reads, - = no interaction

## Workflow Ownership

Which skill owns which responsibility. If two skills could do something, only one should.

| Responsibility | Owner | Others must NOT |
|----------------|-------|-----------------|
| Git pull/push/commit | **switch** | No other skill touches git boundaries |
| Session log creation | **switch** | Conductor records decisions in TODO.md, not session logs |
| Session plan (TODO.md Current Session) | **conductor** (plan), **switch** (wrap-up) | Mode reads but doesn't write TODO.md |
| Vault writes | **kivna** (save) | Switch calls kivna save, doesn't write vault directly |
| Mode state (.active-modes mode block) | **mode** | Conductor reads mode state but never writes the mode line |
| Conductor state (.active-modes conductor line) | **conductor** | Mode reads conductor state but never writes the conductor line |
| Skriv state (.active-modes skriv line) | **skriv** | Same rule — each skill owns only its own line |
| Structural audit and fix | **tend** | Slainte reports content issues but doesn't fix structure |
| Content audit (read-only) | **slainte** | Slainte never modifies files, only reports |
| Archiving completed docs | **trim** | Switch suggests trim but doesn't archive |
| Skill/plugin recommendations | **lorg** | Lorg recommends, never auto-installs |
| Workflow routing | **mode** | Mode guides, never calls skills directly |

### Conflict resolution

If a skill needs to do something owned by another skill, it calls that skill rather than doing it directly:
- Switch calls `/kerd:kivna save` at the boundary (switch owns the vault save; conductor no longer calls it)
- Switch suggests `/kerd:trim` but doesn't run trim's steps itself
- Mode presents steps for the user to invoke, never invokes skills programmatically
