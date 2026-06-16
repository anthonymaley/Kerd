# Design: TODO is forward-only (v0.41.0)

**Date:** 2026-06-14
**Status:** Approved design — pending spec review, then implementation plan
**Scope:** `switch`, `dian`, `state-contract.md`, release housekeeping

## Problem

A Kerd user's `TODO.md` (project: Aubel) reached **378 kb / 2,781 lines**. The space
is ~45 accumulated `## Previous Session — <date> #N` blocks spanning 2026-05-05 →
2026-06-13. Each block is a full, rich session narrative — and each one **already
cites its own `kivna/sessions/<date>.md` log** (e.g. "session log
`kivna/sessions/2026-06-13.md` (#33)"). The TODO copies are pure duplication of an
archive that already exists.

### Root cause

`docs/state-contract.md:34` says the `## Current Session` block is "overwritten each
session." But the skill that actually runs at session close — `switch` — never says
"overwrite." Its instruction (`skills/switch/SKILL.md:53`) is:

> Create TODO.md if it doesn't exist. Update the `## Current Session` block.

…with full-mode guidance to "Include what was done (check off completed items)…".
"Update + include what was done" was interpreted — reasonably, to preserve switch-in
continuity — as **demote-and-keep**: rename `## Current Session` → `## Previous
Session #N`, prepend a fresh block. Over ~40 sessions that produced 378 kb. The
authoritative "overwrite" rule lived only in `state-contract.md` and `dian`
close-out, neither of which `switch` invokes or references.

**Prose alone already failed.** The contract said "overwritten" and the model drifted
anyway for 40 sessions. The fix cannot be only a stronger sentence — it needs a
mechanism that corrects drift when it occurs.

## Principle

**`TODO.md` is forward-only.** It holds only work that still needs doing:

- `## Current Session` — in-progress items, what's next, open decisions/context
- `## Backlog` — queued future work

The record of *completed* work is its `kivna/sessions/<date>.md` log, which is the
readable session history. The moment work is done, its record is the session log, not
a TODO entry. Continuity is preserved because **"what's next" is itself
forward-looking** — it stays in TODO; only the completed narrative leaves.

## Design

### 1. The contract — `docs/state-contract.md`

Codify forward-only explicitly and name the anti-pattern:

- `TODO.md` contains only `## Current Session` (forward-looking state) and
  `## Backlog`. Nothing else persists across sessions.
- Completed session narrative lives in `kivna/sessions/`, never retained in TODO.
- Demote-and-keep (renaming `## Current Session` → `## Previous Session` and keeping
  it) is a named anti-pattern. `## Previous Session` / `## Older Session` blocks must
  not exist in `TODO.md`.

### 2. Prevention — `switch` out, step 1

Rewrite "Write session state to TODO.md":

- **Overwrite** the `## Current Session` block with forward-only state: what's in
  progress, what's next, and any unresolved decisions/context that would otherwise be
  lost. (Mode snapshot behavior unchanged.)
- Do **not** list completed items in the Current Session block, and do **not** rename
  it to `## Previous Session`. The completed record is written to the session log in
  step 2.
- The low-mode "Brief: 3-5 lines" stays, reframed as forward-only.

Sequencing note: the session log (step 2) is the durable record of what was done, so
it must capture the session's completed work *before or as* the Current Session block
is reduced to forward-only. The "what was done" content is not lost — it moves to its
correct home.

### 3. Self-heal — `switch` out, new step 1b ("Heal accumulated history")

On every switch-out, after writing the session log, scan `TODO.md` for `## Previous
Session` and `## Older Session` blocks. If any exist (drift from before this fix, or a
slip):

For each such block (deterministic rule, no fuzzy "does the log capture it" judgment):
1. Determine its date/identifier from the heading (and trust any explicit
   `kivna/sessions/<date>.md` reference inside the block).
2. If a `kivna/sessions/<date>.md` log exists for that date → treat as archived,
   remove the block.
3. If no log exists for that date → **rescue first**: write the block's content to a
   new `kivna/sessions/<date>.md` (or append under a `---` separator if same-day),
   then remove the block.
4. Never delete a block when no session log for its date exists.

After healing, report: "Healed TODO: N session blocks archived to kivna/sessions/
(M rescued)." This makes the 378 kb file collapse on its next switch-out with no
separate tool, and the rescue gate makes it safe even when logs are missing.

Trigger is **header-presence** (`## Previous Session` / `## Older Session`) — the
exact drift signature. A file-size note can be added as a secondary hint but is not
the gate.

### 4. Ripple

- **`dian` close-out (`skills/dian/SKILL.md:155`).** Already says "clear the
  `## Current Session` block." Sync wording to "overwrite to forward-only state; never
  demote-and-keep" so `dian` and `switch` agree. `dian` keeps recording unresolved
  decisions in `### Context` (forward-looking); resolved decisions flow to the session
  log at the boundary, as today.
- **`switch` in.** No behavior change — step 6 already reads recent history from
  session logs, not TODO. (Optional, low-cost: step 2 handoff-verification may note an
  oversized TODO / presence of `## Previous Session` blocks as a drift signal, since
  switch-out self-heal will clear it. Include only if it adds no complexity.)
- **`trim`.** No change. Its manual "Trim TODO.md" step (step 5) still stands;
  self-heal in `switch` makes it non-load-bearing rather than the only line of defense.

### 5. Release housekeeping (Kerd checklist)

This is a behavior change → **MINOR → v0.41.0**.

- Version bump in all three locations: `plugin.json`, `marketplace.json`
  `metadata.version`, `marketplace.json` `plugins[0].version`.
- README: update the `switch` (and if needed `trim`) descriptions to state TODO is
  forward-only and switch self-heals accumulated history.
- Plugin capability descriptions: update both byte-identical capability-list locations
  only if the high-level capability wording changes; leave `metadata.description`
  (marketplace one-liner) unless the summary itself needs it.
- Skill trigger descriptions: update `switch` frontmatter `description` if triggering
  should mention TODO hygiene (likely a light touch, not a new trigger).

**Sequencing:** the working tree currently holds uncommitted **v0.40.0** work (the
session-first reframe + dian slim from the aborted 2026-06-10 switch-out). That lands
as its own commit **first**; this v0.41.0 work is a separate commit on top.

## Out of scope (YAGNI)

- No separate cleanup CLI/tool — self-heal in `switch` is the cleanup, run once.
- No `trim` changes — would duplicate self-heal.
- No backlog pruning — `## Backlog` is legitimately persistent; the reported bloat was
  session blocks, not backlog.
- No new archive artifact — `kivna/sessions/` already is the archive.

## Acceptance criteria

1. `state-contract.md` states TODO is forward-only and names the `## Previous Session`
   demote-and-keep anti-pattern.
2. `switch` out step 1 instructs overwrite (not update/demote) and routes completed
   detail to the session log.
3. `switch` out step 1b heals existing `## Previous Session` / `## Older Session`
   blocks, with a rescue-before-delete safety gate, and reports the count.
4. `dian` close-out wording matches `switch` (overwrite, never demote-and-keep).
5. Version is v0.41.0 across all three manifest locations; README + descriptions
   updated; trigger text reviewed.
6. Applied to a 378 kb-style TODO, one switch-out leaves only `## Current Session`
   (forward-only) + `## Backlog`, with every removed block confirmed present in a
   session log.
