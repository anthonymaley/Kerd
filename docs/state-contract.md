# Shared State Contract

Kerd skills share state through a small set of files. This document defines who owns each file, who reads it, what format it uses, and what the rules are.

The design principle (v0.60.0, `docs/plans/2026-07-03-context-history-split.md`): **state, work, and history are three different things, one file each.** CONTEXT.md holds what's currently true (overwritten), TODO.md holds what's still to do (forward-only, lean), `kivna/sessions/` holds what happened (immutable, full fidelity). Switch-in reads exactly those three; everything else is on-demand reference.

## The same-turn rule (time)

**One definition, here.** Every skill that writes a wall-clock time points at this section; nothing restates it.

A time is written into an artifact only when a machine produced it in the same turn as the write. Two sources, no third: `date` was run in this turn and its output read, or the time was copied from a machine-written record read in this turn — a `conductor: <phase> @ ...` marker stamp, a git commit timestamp. A time the model remembers, infers from the conversation, or estimates from how long the work felt is never written.

Formats: `YYYY-MM-DD HH:MM TZ` for a full stamp (marker lines, gate-record `**Clock:**` lines), `HH:MM TZ` where the date is already established (session-log headings, the switch-out banner), `HH:MM–HH:MM TZ` for a range. Produce them with `date '+%Y-%m-%d %H:%M %Z'` and `date '+%H:%M %Z'`.

**The machine layer checks presence and format only.** A grep can see that a stamp is there and well-shaped; nothing on disk distinguishes a real `date` output from a plausible invention. Time honesty is this frame's declared limit — the retrieval-not-comprehension class. It is held by the write discipline above, not by a checker, and a wrong time is a failure of the discipline rather than of a missing validator.

## CONTEXT.md

**Owner:** the Switch Out flow (standalone, or invoked by conductor close-out), conductor (records decisions during execution)
**Readers:** switch (in), conductor (cold orient)
**Committed:** yes

### Format

```markdown
# Context

## What This Is        — one paragraph, the project in brief
## Where We Are        — current working state, short, overwritten
## Key Decisions       — standing decisions + their why; pruned when superseded
## Open Questions      — genuinely unresolved; removed when answered
## Active Mode         — conductor snapshot for cross-machine handoff
```

### Rules

- **Never a diary.** Episodic content (what happened) belongs in the session log; CONTEXT.md holds only what is *currently true*. If it accumulates per-session narrative, it regrows the bloat the split removed.
- Overwritten in place; superseded decisions and answered questions are pruned. Git history archives every version — pruning loses nothing.
- Bare headers, omit-if-empty (same anti-padding discipline as session logs).
- `## Active Mode` replaces the old TODO.md `### Context` mode snapshot for cross-machine handoff.

## TODO.md

**Owner:** conductor (writes session plan into `## Now`), the Switch Out flow (writes wrap-up, runs closure inference — standalone, or invoked by conductor close-out)
**Readers:** switch (in), conductor (cold orient), lorg (work signals), kivna out (backlog export)
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
- `## Backlog` is append-only (items added, never silently removed outside closure inference).
- conductor writes the plan, switch writes the wrap-up. They don't conflict because conductor runs within a session and switch runs at the boundary.

## kivna/.active-modes

**Owner:** each skill owns its own line(s)
**Readers:** switch (in), Stop hook, SessionStart hook, PostToolUse hook
**Committed:** no (gitignored, ephemeral)

### Format

```
# One line per skill: <skill>: <state>
conductor: execute @ 2026-08-06 15:17 EDT
skriv: active
```

### Rules

- Each skill writes only its own line(s). Never touch another skill's entries.
- Removing a line means the skill is inactive. Don't write `skill: off`.
- Hooks read this file but never write to it.
- Conductor's line carries an `@ YYYY-MM-DD HH:MM TZ` stamp (the same-turn rule above). The three hook readers grep by prefix (`^conductor:` in `hooks/stop.sh`; `^mode:` in `session-start.sh` and `skill-complete.sh`), so the suffix is inert to them; `hooks/stop.sh` echoes the whole line, which is how the stamp reaches the human for free. Switch reads the line whole and carries the stamp into CONTEXT.md `## Active Mode`.
- PostToolUse hook receives a full envelope on stdin (confirmed 2026-04-04):
  `{session_id, cwd, hook_event_name, tool_name, tool_input: {skill, args}, tool_response: {success, commandName}, tool_use_id}`
  The hook checks `tool_response.success` before reporting progress and extracts `tool_input.skill` via sed.
- Switch out snapshots `.active-modes` state to CONTEXT.md `## Active Mode` before committing (cross-machine handoff); switch in restores that snapshot back into `.active-modes` when the file is absent or empty, with the user's assent. The restore rehydrates a whole file — it never edits a line that is already there.

## kivna/sessions/YYYY-MM-DD.md

**Owner:** the Switch Out flow (creates on out — standalone, or invoked by conductor close-out)
**Readers:** switch (in), lorg (work signals), kivna out (decisions export)
**Committed:** yes

### Format

```markdown
# Session YYYY-MM-DD (<sitting label>, HH:MM–HH:MM TZ)

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
- The heading carries the sitting label and a real `HH:MM–HH:MM TZ` range; with no conductor stamp to open it, `(<label>, closed HH:MM TZ)` instead. The rule is defined in `skills/switch/SKILL.md` step 3 (single-definition law), under the same-turn rule above.
- The Switch Out flow is the sole creator (either caller). Conductor records decisions in CONTEXT.md during execution; the Switch Out flow captures them in the session log at the boundary.
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
- kivna save is the sole session-flow writer, and it runs on demand only (v0.83.0) — no skill calls it automatically. A vault is exactly as fresh as its last deliberate save.
- Neither switch nor conductor writes or triggers a vault write. The vault is opt-in per project; absence is legitimate.
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
**Readers:** lorg (report display, and each scan to preserve unscanned tier sections)
**Committed:** yes

### Rules

- Overwritten each scan. Not append-only.
- Duplicate copy written to vault (`[Name] Lorg Report.md`).
- Includes `Last scanned: YYYY-MM-DD` date line.

## Cross-Skill Interaction Summary

| File | conductor | switch | skriv | kivna | slainte | tend | lorg | hooks |
|------|------|--------|-------|-------|---------|------|------|-------|
| CONTEXT.md | W/R | W/R | - | - | - | R | - | - |
| TODO.md | W/R | W/R | - | W/R | R | R | R | - |
| .active-modes | W/R | W/R | W | R | - | - | - | R |
| sessions/ | - | W/R | - | W/R | - | - | R | R |
| vault Status | - | - | - | W/R | R | - | R | - |
| KIF exports | - | - | - | W | - | - | - | - |
| lorg-report | - | - | - | - | - | - | W/R | - |

W = writes, R = reads, - = no interaction

## Workflow Ownership

Which skill owns which responsibility. If two skills could do something, only one should.

| Responsibility | Owner | Others must NOT |
|----------------|-------|-----------------|
| Git pull | **switch-in** | Nothing else pulls, ever — pulling mid-session changes files under in-flight work |
| Session-state commit + push | **the Switch Out flow** (standalone, or invoked by conductor close-out) | No other skill commits CONTEXT.md, TODO.md, or session logs |
| Work commits + push | **conductor** (per verified task, since v0.67.0) | Session-state files never ride along in a work commit |
| Session log creation | **switch** | Conductor records decisions in TODO.md, not session logs |
| Session plan (TODO.md `## Now`) | **conductor** (plan), **switch** (wrap-up) | Other skills don't write `## Now`; kivna import may merge approved KIF items into `## Backlog` |
| Standing state (CONTEXT.md) | **switch** (out), **conductor** (decisions during execute) | Other skills read but don't write |
| Vault writes | **kivna** (save, on demand — v0.83.0) | No skill calls kivna save automatically; lorg's report copy is the one automatic exception |
| Conductor state (.active-modes conductor line) | **conductor** | Other skills read conductor state but never write the conductor line |
| Skriv state (.active-modes skriv line) | **skriv** | Same rule — each skill owns only its own line |
| Structural audit and fix | **tend** | Tend keeps structure; slainte fixes *content* drift under the caller's gate |
| Content audit and fix | **slainte** — triggered by conductor at releases and feature closes, on demand otherwise | No other skill edits docs to fix content drift; slainte's own fixes land only under the caller's verification gate, restraint reported |
| Skill/plugin recommendations | **lorg** | Lorg recommends, never auto-installs |

### Conflict resolution

If a skill needs to do something owned by another skill, it calls that skill rather than doing it directly:
- Nothing calls `/kerd:kivna save` automatically (v0.83.0) — the user invokes it when they want the vault current
