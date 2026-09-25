# Shared State Contract

Kerd skills share state through a small set of files. This document defines who owns each file, who reads it, what format it uses, and what the rules are.

The design principle (v0.60.0, `docs/plans/2026-07-03-context-history-split.md`): **state, work, and history are three different things, one file each.** CONTEXT.md holds what's currently true (overwritten), TODO.md holds what's still to do (forward-only, lean), `kivna/sessions/` holds what happened (immutable, full fidelity). Switch-in reads the pickup set the last Out named — by default exactly those three; everything else is on-demand reference.

## The same-turn rule (time)

**One definition, here.** Every skill that writes a wall-clock time points at this section; nothing restates it.

A time is written into an artifact only when a machine produced it in the same turn as the write. Two sources, no third: `date` was run in this turn and its output read, or the time was copied from a machine-written record read in this turn — a git commit timestamp. (The `conductor: <phase> @ ...` marker was a third source until v0.107.0; Conductor no longer writes it, so read the clock instead.) A time the model remembers, infers from the conversation, or estimates from how long the work felt is never written.

Formats: `YYYY-MM-DD HH:MM TZ` for a full stamp (marker lines, gate-record `**Clock:**` lines), `HH:MM TZ` where the date is already established (session-log headings, the switch-out banner), `HH:MM–HH:MM TZ` for a range. Produce them with `date '+%Y-%m-%d %H:%M %Z'` and `date '+%H:%M %Z'`.

**The machine layer checks presence and format only.** A grep can see that a stamp is there and well-shaped; nothing on disk distinguishes a real `date` output from a plausible invention. Time honesty is this frame's declared limit — the retrieval-not-comprehension class. It is held by the write discipline above, not by a checker, and a wrong time is a failure of the discipline rather than of a missing validator.

## CONTEXT.md

**Owner:** the Switch Out flow, run explicitly
**Readers:** switch (in)
**Committed:** yes

### Format

```markdown
# Context

## What This Is        — one paragraph, the project in brief
## Where We Are        — current working state, short, overwritten
## Key Decisions       — rulings only (bold sentence + date) for decisions that govern the next work; the full case lives in docs/decisions.md
## Open Questions      — genuinely unresolved; removed when answered
## Active Mode         — legacy: the conductor snapshot of the retired modes system; nothing writes it
```

### Rules

- **Never a diary.** Episodic content (what happened) belongs in the session log; CONTEXT.md holds only what is *currently true*. If it accumulates per-session narrative, it regrows the bloat the split removed.
- Overwritten in place; superseded decisions and answered questions are pruned. Git history archives every version — pruning loses nothing.
- **Rulings stay, cases move (Switch Out, from v0.111.0).** `## Key Decisions` holds a ruling only while it governs the next work or a constraint the next sitting must honour; every full entry lives in `docs/decisions.md`, newest first with a ruling index, superseded entries marked rather than deleted. Out names the pickup reading set in `## Where We Are` and records the helper's `measure` reading beside it.
- Bare headers, omit-if-empty (same anti-padding discipline as session logs).
- `## Active Mode` carried the retired modes system's snapshot across machines. Nothing has written it since v0.75.0; a section found there is history.

## TODO.md

**Owner:** the Switch Out flow, run explicitly (writes wrap-up, runs closure inference)
**Readers:** switch (in), kivna out (backlog export)
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

- **TODO.md is forward-only and lean.** `## Now` + `## Backlog` only — no session story, no `### Context` section (standing context lives in CONTEXT.md). The record of completed work is the `kivna/sessions/<date>.md` log and, from v0.111.0, the closed row itself in `docs/backlog-archive.md` — never a retained TODO entry.
- `## Now` is **overwritten in place** by switch (out) — never accumulated.
- **Anti-pattern — demote-and-keep.** `## Previous Session` / `## Older Session` blocks (and the pre-split `## Current Session` / `### Context` shapes) must not exist; they are migrated explicitly (rescue-before-remove into CONTEXT.md and session logs); `/kerd:tend` detects them, and no skill heals them automatically as of v0.107.0.
- **Closure inference (switch out):** every open item gets a verdict — done (evidence required; removed, recorded in the session log and the archive), dead (undone, its reason gone or its subject removed; archived with that reason), open (kept), or unsure (kept, tagged `(done? — confirm)`). The verdict list is shown to the user as information, never a prompt; switch-in asks one question about tagged items.
- `## Backlog` is append-only (items added, never silently removed outside closure inference).
- **Closed rows leave with their reason (Switch Out, from v0.111.0).** Rows the closure review judges done or dead move to `docs/backlog-archive.md` with verdict, evidence and date; open and unsure rows stay. Age alone closes nothing.
- conductor writes the plan, switch writes the wrap-up. They don't conflict because conductor runs within a session and switch runs at the boundary.

## kivna/.active-modes

**Owner:** Skriv, for its own `skriv:` line, and nothing else. The modes system that
gave this file its name was cut in v0.75.0, so there is no `conductor:` line or `mode:`
block any more and nothing writes one.
**Readers:** `hooks/session-start.sh` and `hooks/skill-complete.sh` still grep `^mode:`,
which no current skill writes; a file carrying one is leftover state from before v0.75.0.
**Committed:** no (gitignored, ephemeral).

### Rules

- Skriv adds `skriv: active` when session mode turns on and removes the line when it
  turns off, deleting the file if that was its only entry.
- No skill touches another skill's line, and hooks never write to this file.

## kivna/sessions/YYYY-MM-DD.md

**Owner:** the Switch Out flow (creates on out, run explicitly)
**Readers:** switch (in), kivna out (decisions export)
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
**Readers:** the human (Obsidian), kivna out (status export) — **not switch, not conductor** (write-only from the session flow's perspective since v0.60.0)
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

## Vault `work/<work>/work.md` (private working notes)

**Owner:** conductor (writes the sketchbook, its diagrams, evidence and drafts)
**Readers:** conductor, switch (in/out) — same as `docs/work/<work>/work.md`, its default home
**Committed:** yes, but in the vault's own git repo (shared with other vault content), not the project's

### Format

Same as [the work record](../skills/conductor/references/work-record.md); the
only change is where it lives.

### Rules

- Opt-in per project: only when `kivna/vault.json` sets `"work_notes": "vault"`.
  Without that key, the sketchbook stays at `docs/work/<work>/work.md` and is
  committed with the project, unchanged from before this section existed.
- Notes root: `<vault>/<folder>/work`, the `work/` folder inside the vault's
  existing private git repo — shared with the rest of the vault's content, not
  a separate repo of its own. Kivna recognizes the key; it does not create or
  maintain this folder.
- Records point at a moved sketchbook as `notes:<work>/work.md`. Switch In
  reads a `notes:<path>` reading-set entry from the notes root.
- Switch Out saves and pushes the vault repo the same way it saves the
  project, at the same session boundary; the `boundary` check covers both
  repos. This is not a second closeout — one sitting, two repos saved.

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

## docs/decisions.md

**Owner:** the Switch Out flow (moves each decision's full entry here; marks superseded entries)
**Readers:** conductor and slainte on demand, by ruling; never part of the default pickup set
**Committed:** yes

Living, newest first, with an index of rulings. Entries are never deleted; a superseded one is marked. Started 2026-09-11 (v0.111.0) from the whole of CONTEXT.md `## Key Decisions`.

## docs/backlog-archive.md

**Owner:** the Switch Out flow (appends closed rows with verdict, evidence and date)
**Readers:** slainte on demand; never part of the default pickup set
**Committed:** yes

Append-only. Nothing here is edited after it lands.

## Cross-Skill Interaction Summary

| File | conductor | switch | skriv | kivna | slainte | tend | hooks |
|------|------|--------|-------|-------|---------|------|-------|
| CONTEXT.md | W/R | W/R | - | - | - | R | - |
| TODO.md | W/R | W/R | - | W/R | R | R | - |
| sessions/ | - | W/R | - | W/R | - | - | R |
| vault Status | - | - | - | W/R | R | - | - |
| vault work/ | W/R | W/R | - | - | - | - | - |
| KIF exports | - | - | - | W | - | - | - |
| docs/decisions.md | R | W/R | - | - | R | - | - |
| docs/backlog-archive.md | - | W | - | - | R | - | - |

W = writes, R = reads, - = no interaction

## Workflow Ownership

Which skill owns which responsibility. If two skills could do something, only one should.

| Responsibility | Owner | Others must NOT |
|----------------|-------|-----------------|
| Git pull | **switch-in** | Nothing else pulls, ever — pulling mid-session changes files under in-flight work |
| Session-state commit + push | **the Switch Out flow**, run explicitly | No other skill commits CONTEXT.md, TODO.md, or session logs |
| Work commits + push | **conductor** (per verified task, since v0.67.0) | Session-state files never ride along in a work commit |
| Session log creation | **switch** | Conductor records decisions in TODO.md, not session logs |
| Session plan (TODO.md `## Now`) | **conductor** (plan), **switch** (wrap-up) | Other skills don't write `## Now`; kivna import may merge approved KIF items into `## Backlog` |
| Standing state (CONTEXT.md) | **switch** (out), **conductor** (decisions during execute) | Other skills read but don't write |
| Vault writes | **kivna** (save, on demand — v0.83.0) | No skill calls kivna save automatically |
| Vault `work/` writes | **conductor** (the sketchbook, opt-in via `work_notes`) | Kivna does not write it; it only recognizes the key |
| Vault `work/` save + push | **the Switch Out flow**, alongside the project | No other skill commits or pushes the vault repo |
| Structural audit and fix | **tend** | Tend keeps structure; slainte fixes *content* drift under the caller's gate |
| Content audit and fix | **slainte** — triggered by conductor at releases and feature closes, on demand otherwise | No other skill edits docs to fix content drift; slainte's own fixes land only under the caller's verification gate, restraint reported |

### Conflict resolution

If a skill needs to do something owned by another skill, it calls that skill rather than doing it directly:
- Nothing calls `/kerd:kivna save` automatically (v0.83.0) — the user invokes it when they want the vault current
