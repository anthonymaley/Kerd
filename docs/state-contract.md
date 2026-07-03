# Shared State Contract

Kerd skills share state through a small set of files. This document defines who owns each file, who reads it, what format it uses, and what the rules are.

The design principle (v0.60.0, `docs/plans/2026-07-03-context-history-split.md`): **state, work, and history are three different things, one file each.** CONTEXT.md holds what's currently true (overwritten), TODO.md holds what's still to do (forward-only, lean), `kivna/sessions/` holds what happened (immutable, full fidelity). Switch-in reads exactly those three; everything else is on-demand reference.

## CONTEXT.md

**Owner:** switch (writes at out), conductor (records decisions during execution)
**Readers:** switch (in), conductor (cold orient), modes (setup steps)
**Committed:** yes

### Format

```markdown
# Context

## What This Is        — one paragraph, the project in brief
## Where We Are        — current working state, short, overwritten
## Key Decisions       — standing decisions + their why; pruned when superseded
## Open Questions      — genuinely unresolved; removed when answered
## Active Mode         — mode/sherpa/conductor snapshot for cross-machine handoff
```

### Rules

- **Never a diary.** Episodic content (what happened) belongs in the session log; CONTEXT.md holds only what is *currently true*. If it accumulates per-session narrative, it regrows the bloat the split removed.
- Overwritten in place; superseded decisions and answered questions are pruned. Git history archives every version — pruning loses nothing.
- Bare headers, omit-if-empty (same anti-padding discipline as session logs).
- `## Active Mode` replaces the old TODO.md `### Context` mode snapshot for cross-machine handoff.

## TODO.md

**Owner:** conductor (writes session plan into `## Now`), switch (writes wrap-up, runs closure inference)
**Readers:** switch (in), lorg (work signals), kivna out (backlog export)
**Committed:** yes

### Format

```markdown
# TODO

## Now
- current focus: pointers + deltas, a few lines, no re-narration

## Backlog
- queued items, one line each
- an uncertain item (done? — confirm)
```

### Rules

- **TODO.md is forward-only and lean.** `## Now` + `## Backlog` only — no session story, no `### Context` section (standing context lives in CONTEXT.md). The record of completed work is the `kivna/sessions/<date>.md` log — never a retained TODO entry.
- `## Now` is **overwritten in place** by conductor (plan phase) or switch (out) — never accumulated.
- **Anti-pattern — demote-and-keep.** `## Previous Session` / `## Older Session` blocks (and the pre-split `## Current Session` / `### Context` shapes) must not exist; `switch out` self-migrates any that appear (rescue-before-remove into CONTEXT.md and session logs).
- **Closure inference (switch out):** every open item gets a verdict — done (evidence required; removed, recorded in the session log), open (kept), or unsure (kept, tagged `(done? — confirm)`). The verdict list is shown to the user as information, never a prompt; switch-in asks one question about tagged items.
- `## Backlog` is append-only (items added, never silently removed outside closure inference). Completed items can also be cleaned by trim.
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
- Switch out snapshots mode state to CONTEXT.md `## Active Mode` before committing (cross-machine handoff).

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
- Switch is the sole creator. Conductor records decisions in CONTEXT.md during execution; switch captures them in the session log at the boundary.
- Session logs are immutable history: append-only within a day, never rewritten. Switch-in reads **only the newest file**; older logs are archive (grep/read on demand). This is the fidelity guarantee that lets CONTEXT.md stay lean.

## Vault Status.md

**Owner:** kivna save
**Readers:** the human (Obsidian), lorg (work signals), kivna out (status export) — **not switch, not conductor** (write-only from the session flow's perspective since v0.60.0)
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

- Overwritten each save, not appended to. Save shows what changed but does not prompt for approval (v0.60.0); do-not-save markers remain the privacy control.
- kivna save is the sole writer. One vault write per session (at close-out), not per-task.
- Switch out calls kivna save at session close. Conductor no longer calls it; switch owns the vault save.
- Never read at switch-in: it contains nothing CONTEXT.md + the latest session log don't. It exists for the human Obsidian reader.

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
| CONTEXT.md | W/R | W/R | R | - | - | - | R | - | - |
| TODO.md | W | W/R | - | - | R | - | R | R | - |
| .active-modes | W/R | R | W | W | - | - | - | - | R |
| sessions/ | - | W/R | - | - | R | - | - | R | R |
| vault Status | - | - | - | - | W | R | - | R | - |
| KIF exports | - | - | - | - | W | - | - | - | - |
| lorg-report | - | - | - | - | - | - | - | W | - |

W = writes, R = reads, - = no interaction

## Workflow Ownership

Which skill owns which responsibility. If two skills could do something, only one should.

| Responsibility | Owner | Others must NOT |
|----------------|-------|-----------------|
| Git pull/push/commit | **switch** | No other skill touches git boundaries |
| Session log creation | **switch** | Conductor records decisions in TODO.md, not session logs |
| Session plan (TODO.md `## Now`) | **conductor** (plan), **switch** (wrap-up) | Mode reads but doesn't write TODO.md |
| Standing state (CONTEXT.md) | **switch** (out), **conductor** (decisions during execute) | Other skills read but don't write |
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
