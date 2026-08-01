---
name: switch
description: "Use when the user says 'switch', 'wrapping up', 'picking up', 'save context', 'handoff', or 'switching machines', or needs to cleanly end a work session and resume it later with full context. The primary use is session handoff: wrap up, commit, exit, and pick up cold in a fresh session. The same mechanism carries across machines as the secondary case. Owns `git pull` and the session-state commit (CONTEXT.md, TODO.md, session log, vault); conductor commits its own work per verified task. Writes state to CONTEXT.md, work to TODO.md, history to kivna/sessions/; pickup reads only those three. Supports 'light' modifier to skip vault and reflection, or 'low' modifier for minimum viable handoff on tight token budgets."
---

# Switch (Session Handoff)

Clean handoff between work sessions. The primary use: wrap up a session, commit and push, exit, then pick up cold in a fresh session with full context restored from disk. The same mechanism handles moving between machines, that's just the secondary case.

**Switch owns `git pull` and the session-state commit.** Nothing else pulls. The session-state commit is CONTEXT.md, TODO.md, the session log, and vault files — written and committed once, here, at the boundary.

**Switch does not own every commit.** Conductor commits and pushes its own work — code plus the docs travelling with it — at each verified task boundary, staged by name (see `/kerd:conductor`). That is deliberate: holding work until the boundary piles a whole session's interleaved change into one diff, which is where collateral damage hides. So expect the tree at switch-out to hold mostly session state, with the session's actual work already pushed.

## State, Work, and History

Switch keeps three kinds of information in three files — one kind each, never smeared across files (design: `docs/plans/2026-07-03-context-history-split.md`):

| File | Kind | Discipline |
|---|---|---|
| `CONTEXT.md` (root) | **State** — what's currently true | Overwritten in place, bounded size |
| `TODO.md` (root) | **Work** — what's still to do | Forward-only, lean |
| `kivna/sessions/` | **History** — what happened | Immutable, append-forever, full fidelity |

Completeness comes from full-fidelity session logs plus git history of every pruned CONTEXT.md version — nothing is lost in storage. Efficiency comes from reading less, not storing less: switch-in reads only CONTEXT.md + TODO.md + the newest session log.

**The sharp edge: CONTEXT.md must never become a diary.** The session log is the diary. If a fact is episodic (what happened), it belongs in the log; if it's standing (a decision, a constraint, the current stage), it belongs in CONTEXT.md. Superseded content is pruned — git keeps it.

## Usage

`/kerd:switch out` wrapping up a session (full)
`/kerd:switch out light` wrapping up a session (skip vault, reflection, progress tracking)
`/kerd:switch out low` wrapping up a session (minimum viable handoff, tight token budget)
`/kerd:switch in` picking up a session (full)
`/kerd:switch in light` picking up a session (skip smoke test)
`/kerd:switch in low` picking up a session (minimum viable pickup, tight token budget)

The same path serves a fresh session on this machine (the common case) and a move to another machine (the same git boundary operations either way).

If no argument is given, check for uncommitted changes. If changes exist, assume `out`. If clean, assume `in`.

### Modifier progression

| | Full | Light | Low |
|---|---|---|---|
| CONTEXT.md update | Full (all sections) | Full | Where We Are + Active Mode only |
| TODO.md update | Lean (Now + Backlog) | Lean (Now + Backlog) | Now only, 3-5 lines max |
| Closure inference | Yes (verdict list) | Yes (verdict list) | Skip |
| Session log | Full template (all sections) | Full template | Skeleton: What Was Done + What's Next only |
| Vault update | Yes (kivna save, no approval) | Skip | Skip |
| Reflection/gotchas | Yes (+ playbook mirror check) | Skip | Skip (unless something critical) |
| Progress tracking | Yes | Skip | Skip |
| Untracked file triage | Yes | Yes | Skip (unless obviously risky files like .env) |
| Pre-commit summary | Full with evidence | Full with evidence | One-line: "Committing N files: [list]" |
| Trim suggestion | Yes | No | No |
| Final confirmation | Evidence-cited | Evidence-cited | One-line: commit hash + push target |
| **Switch-in** | | | |
| Pull | Yes | Yes | Yes |
| Handoff verification | Yes | Yes | Skip |
| Smoke test | Yes | Skip | Skip |
| Read CONTEXT.md | Full | Full | Where We Are only |
| Read TODO.md | Full | Full | Now only |
| Read session logs | Newest only, in full | Newest only, in full | Latest What's Next only |
| Confirm `(done? — confirm)` items | Yes | Yes | Skip |
| Read progress | Yes | Skip | Skip |
| Check active modes | Yes | Yes | Yes |
| Offer conductor | Yes | Yes | Skip |

The vault is never read at switch-in in any mode — Status.md is write-only from switch's perspective; it exists for the human Obsidian reader and contains nothing CONTEXT.md + the latest log don't.

## Switch Out (Wrapping Up a Session)

Wrap up everything so the next session can pick up cold, whether that's a fresh session on this machine or another.

### 1. Update CONTEXT.md (state)

Create `CONTEXT.md` at the repo root if it doesn't exist. **Overwrite in place** — it holds what is *currently true*, not what happened. Sections (bare headers, omit any that would be empty — same anti-padding discipline as session logs):

```
# Context

## What This Is        — one paragraph, the project in brief
## Where We Are        — current working state, a short paragraph, overwritten
## Key Decisions       — standing decisions + their why; prune when superseded
## Open Questions      — genuinely unresolved; remove when answered
## Active Mode         — mode/sherpa/conductor snapshot for cross-machine handoff
```

- Prune superseded decisions and answered questions — git history archives every version, so pruning loses nothing.
- **Not a copy of the session narrative.** If it's in the session log and episodic, it does not belong here.
- **Mode snapshot:** if `kivna/.active-modes` contains mode state, snapshot it into `## Active Mode` so cross-machine handoff works without the ephemeral file. Include: mode name, current step number and total, session instruction (if any), and the steps list with status markers.

**Low:** update only `## Where We Are` (a few lines) and `## Active Mode` if a mode is active. Leave the rest untouched.

### 2. Update TODO.md (work)

Create TODO.md if it doesn't exist. Shape:

```
# TODO

## Now       — current focus: pointers + deltas, a few lines, no re-narration
## Backlog   — queued items, one line each
```

TODO.md is **forward-only and lean**: what still needs doing, nothing else. No session story — the latest session log carries "what happened"; point (`see kivna/sessions/<date>.md`) instead of re-telling. No `### Context` section — standing context lives in CONTEXT.md.

**Closure inference.** Before writing the new TODO, review every open item (Now and Backlog) against what actually happened this session — files changed, commits made, work discussed and finished. Give each item a verdict:

- **done** — session evidence shows it's complete → remove it from TODO and record the closure in the session log's What Was Done
- **open** — untouched or still in progress → keep as-is
- **unsure** — evidence suggests it may be done but isn't conclusive → keep it, tagged `(done? — confirm)`

Show the verdicts as a readable list — **informational only, never a prompt; do not wait for input**:

```
TODO closure review:
  ✓ done   — "PPS marketplace.json fix" (pushed in a1b2c3)
  · open   — "solicit community mode contributions" (untouched)
  ? unsure — "hook staleness check in tend" (discussed; unclear if the edit shipped) → tagged
```

A "done" verdict requires pointing at session evidence (a commit, a file, a log entry). When in doubt, the verdict is open or unsure — never silently close an item you can't evidence. Switch-in asks about tagged items; that's the only place a question happens.

**Low:** keep `## Now` to 3-5 lines max; skip closure inference.

### 2b. Heal and self-migrate

TODO.md must contain no legacy shapes: no `## Current Session` block, no `### Context` section, no `## Previous Session` / `## Older Session` blocks. Scan for them (drift from before the split, or a slip). For each found:

1. **`### Context` section** → move standing content (decisions, open questions, mode snapshot) into the matching CONTEXT.md sections, then remove it from TODO.
2. **`## Current Session` block** → carry forward-looking items into `## Now`; episodic narrative goes to today's session log; then remove the block.
3. **`## Previous Session` / `## Older Session` blocks** → read the date from the heading or any `kivna/sessions/<date>.md` reference inside. If a log already exists for that date, the block is archived — remove it. If not, **rescue first**: create the log from the block's content (or append under a `---` separator), then remove. Undated blocks rescue to `kivna/sessions/undated-<slug>.md`.
4. Never delete a block whose content is not first preserved in CONTEXT.md or a session log — rescue is mandatory before removal.

Report: "Healed TODO: N legacy block(s) migrated (M rescued)." If none exist, skip silently. This runs in all modes (full/light/low) — it is cheap, it is the backstop against unbounded TODO growth, and it makes the split **self-migrating**: the first switch-out on a pre-split repo converts it with no separate migration step.

### 3. Write session log (history)

Create `kivna/sessions/YYYY-MM-DD.md` (or append if one already exists for today).

If appending to an existing file for today (multiple sessions), add a `---` separator and a new section with a time or sequence number.

The session log captures what happened in this session for the next session to pick up cold. This is the canonical record and the fidelity guarantee — it is never compressed and never rewritten. Two sections are **required**: `## What Was Done` and `## What's Next`. Four sections are **optional**: `## Key Decisions`, `## Commits`, `## Gotchas`, `## Insights`. Read the rules below before writing.

**Anti-hallucination rule.** Include an optional section ONLY if you can point to specific moments in this session that produced its content. If a section would be empty, **omit the header entirely**. Empty headers are padding. Inventing content to fill structure is hallucination. Do not write "None" or "N/A" — omit the section.

**It is okay not to know.** If you're uncertain why something happened, what something means, or what should come next, say so explicitly. Write "Unclear why this fix worked — needs investigation" or "Don't know what should come next — needs decision" rather than constructing a plausible-sounding explanation. "I don't know" is a valid log entry and a starting point for the next session. Do not guess. Do not jump to conclusions.

**Match vocabulary to the work.** A code session references files, commits, tests. A writing session references drafts, edits, voice. A strategy session references frameworks, positioning, decisions. A sales session references calls, accounts, outreach. A research session references sources, findings, gaps. Use the language of the actual work — do not force code vocabulary onto non-code sessions.

**Commits section** applies only when commits were made in this session. For non-code sessions or sessions with no commits, omit it.

**Full/light template** (bare headers — fill with content from this session, omit any optional header that would be empty):

```
# Session YYYY-MM-DD

**Machine:** {hostname}
**Branch:** {current branch}
**Tracking:** {upstream status, e.g. origin/main (up to date)}

## What Was Done

## What's Next

## Key Decisions

## Commits

## Gotchas

## Insights
```

**Low template:** Two required sections only, no metadata headers, no optional sections. Use bullets, 3-5 items in What Was Done, 1-2 lines in What's Next.

```
# Session YYYY-MM-DD

## What Was Done

## What's Next
```

### 4. Update the vault

**Skip this step if `light` or `low` modifier is set.**

Call `/kerd:kivna save`. Switch owns the vault save; conductor no longer touches the vault. This updates Status.md and the relevant domain files **directly, without an approval prompt** — report what was written. The vault stays human-first: Status.md is written here but never read at switch-in.

### 5. Update progress tracking

**Skip this step if `light` or `low` modifier is set.**

If progress tracking exists (check for `docs/project/progress.md`, `progress.md`, or similar), update it.

### 6. Reflect and capture learnings

**Skip this step if `light` or `low` modifier is set** — with one exception: if something genuinely critical broke or a dangerous gotcha was discovered during the session, capture it even in low mode. One line in the session log is enough. The bar for "critical" in low mode is: would the next person waste significant time without this information?

Before committing, reflect on the session:

- **What broke unexpectedly?** Any gotchas, edge cases, or non-obvious behavior discovered? These go in the session log `## Gotchas` section AND in `docs/playbook.md` Gotchas section (so they survive beyond session logs).
- **What patterns emerged?** Any recurring problems, useful approaches, or workflow improvements worth codifying?
- **What should be remembered?** Best practices discovered, conventions that worked well or didn't.
- **What would make the next session better?** Anything about the project, tooling, or workflow that should be adjusted.

Write actionable learnings to the appropriate place:
- **Gotchas** → add to `docs/playbook.md` Gotchas section (duplicates what's in the session log, but the playbook is the living reference; session logs are archives)
- **Project conventions and enforcement rules** → add to `CLAUDE.md` (so they're enforced in future sessions)
- **Conventions and patterns** → flag for the appropriate vault file (Architecture Decisions, Positioning Contract, etc.), written during the `/kerd:kivna save` step

**Gotcha-mirror verification (all modes, before commit):** for every entry in this session's `## Gotchas`, verify `docs/playbook.md` contains a counterpart (cheap grep). If one is missing, add it now. Older session logs are never skimmed at switch-in, so the playbook — not the log tail — is the durable gotcha net; an unmirrored gotcha is effectively lost.

Skip the reflection (not the mirror check) if the session was trivial (quick fix, single file change). But for any session with meaningful work, take the time. Compounding small improvements across sessions is how projects stay healthy.

### 7. Triage, commit, and push

Before staging anything, run `git status` to see the actual state of the working tree. Classify every changed or untracked file into two buckets:

- **Session files** — files this session created or modified (CONTEXT.md, TODO.md, session log, playbook updates, vault files, etc.). These are auto-committed without asking.
- **Unexpected files** — untracked files that existed before switch-out started, or modifications the session didn't make. These need a decision.

#### Normal path (no unexpected files)

Stage session files by name, commit with a descriptive message, and push. No confirmation prompt. Then show the completion banner (step 8).

**Trim suggestion (full only):** If `docs/plans/` or `docs/` contains spec, plan, or design docs whose features are marked complete in TODO.md or playbook, append to the completion banner: "Completed plan docs detected. Consider `/kerd:trim` to archive them."

#### Exception path (unexpected files found)

If there are unexpected untracked or modified files, stop and show a decision banner before committing:

```
┌─────────────────────────────────────────────┐
│  ⚠ INPUT REQUIRED — unexpected files found  │
│                                             │
│  Session files (will auto-commit):          │
│    TODO.md, kivna/sessions/2026-04-05.md    │
│                                             │
│  Needs decision:                            │
│    docs/demo-mode.gif — commit / ignore / .gitignore?  │
│    docs/demo-mode.mp4 — commit / ignore / .gitignore?  │
└─────────────────────────────────────────────┘
```

Wait for the user to decide on each unexpected file. Then stage, commit, and push everything together.

**Low:** Skip triage entirely unless an obviously risky file is untracked (`.env`, credentials, secrets). Auto-commit session files without any banner.

### 8. Completion banner

Run `git status` and `git log --oneline -1` fresh. Read the output. Show a completion banner with evidence:

```
┌─────────────────────────────────────────────┐
│  ✓ Switch out complete                      │
│                                             │
│  Pushed: [hash] [message]                   │
│  → origin/[branch] ([N files])              │
│  Tree: clean                                │
│  Next: [what to pick up]                    │
└─────────────────────────────────────────────┘
```

If the tree is not clean, report what remains and why (e.g., "3 untracked files left per triage decision"). If the push failed, stop and surface the error.

If `light` modifier was used, note: "Light handoff: vault and reflection skipped."

**Low:** Compress to one line:

```
Pushed: [commit-hash] → origin/[branch]. Next: [what to pick up]
```

## Switch In (Picking Up a Session)

Pick up where the last session left off. The read set is three files: CONTEXT.md, TODO.md, the newest session log. Nothing else is loaded per-session — older logs, the playbook, and the vault are on-demand references.

### 1. Pull

`git pull`. If there are conflicts, resolve them before proceeding.

### 2. Handoff contract verification

**Skip this step if `low` modifier is set.**

After pulling, verify the outgoing machine completed its handoff. Check:

- Does `CONTEXT.md` exist?
- Does `TODO.md` exist?
- Does the latest file in `kivna/sessions/` have a `## What's Next` section?

If all are present, proceed normally. If any is missing, flag it explicitly:

```
⚠ Partial handoff detected:
  - CONTEXT.md missing
  - Latest session log missing ## What's Next

  Proceeding with available context. Some state may be missing.
```

If CONTEXT.md is missing but TODO.md has a `## Current Session` block or `### Context` section, this is a **pre-split repo**, not a broken handoff: read the legacy shape, note that the next switch-out will migrate it (step 2b), and proceed.

Do not pretend the pickup is clean when the handoff was incomplete.

### 3. Smoke test

**Skip this step if `light` or `low` modifier is set.**

If the project has a test command (check `package.json` scripts, `Makefile`, `pyproject.toml`, or similar), run it. If tests fail, report the failures in the summary. The user should know the state of the codebase before planning new work. If no test command exists, skip this step.

### 4. Read CONTEXT.md

The state file: what the project is, where it stands, standing decisions, open questions, active mode snapshot.

**Low:** Read only `## Where We Are`.

### 5. Read TODO.md

The work file: current focus (`## Now`) and queued items (`## Backlog`).

**Low:** Read only `## Now`.

### 6. Read the newest session log

Read the most recent file in `kivna/sessions/` in full. **Older logs are archive — do not skim or read them per-session.** Forward-only discipline guarantees anything still relevant was carried into CONTEXT.md, TODO.md, or the newest log's What's Next; gotchas live durably in `docs/playbook.md`. Grep or read older logs only when the user asks or a specific question needs history.

**Low:** Read only the `## What's Next` section of the latest log.

### 7. Confirm uncertain closures

**Skip this step if `low` modifier is set.**

If any TODO items carry a `(done? — confirm)` tag, collect them and ask the user **one** question: which of these are actually done? Remove the confirmed ones (recording the closure in the summary); untag the rest back to open. If no tags exist, skip silently.

### 8. Read progress tracking

**Skip this step if `light` or `low` modifier is set.**

If progress tracking exists, read it.

### 9. Check active modes

Check two sources for mode state:

1. **`kivna/.active-modes`** (same-machine resume): if it exists and is non-empty, read it and report active modes.
2. **CONTEXT.md `## Active Mode`** (cross-machine handoff): if `.active-modes` doesn't exist or is empty, check CONTEXT.md's `## Active Mode` section for a snapshot. If found, report it and offer to restore it to `.active-modes`.

Report any active modes in the summary (e.g., "**Active modes:** `greenfield (step 4 of 9)`"). If neither source has mode state, skip this. Don't mention modes.

### 10. Summarize

Tell the user:
- What was done last session
- Any open questions or decisions from the previous session
- Any test failures from the smoke test (if applicable, full mode only)
- Any handoff issues detected in step 2
- **A short-form "what's next" pick-list** — a numbered menu of every `## Now` and `## Backlog` item, one terse line each. TODO is forward-only and lean by design, so list it in full — don't truncate to "+N more". This is a compact menu, not a re-narration: title-only, no re-explaining what each item is, no reply-instructions (the user just types a number or says what they want).

The pick-list is the point of the summary — the user reads it to pick their next move. Draw it straight from TODO.md; don't editorialize. Number the items and tag each with `[Now]`/`[Backlog]`. Shape:

```
What's next:

  1. [Now]      Dogfood sherpa on ~/Bree — mid-lifecycle vs fresh feature
  2. [Backlog]  tend other repos onto the split
  3. [Backlog]  vault-repo-commit contract question
  4. [Backlog]  first /kerd:interrogate smoke test
  5. [Backlog]  guard switch-in smoke test against context bloat
  6. [Backlog]  slainte auto-trigger idea
  ...
```

A number-reply picks that item as the session's focus; any freeform reply steers elsewhere. Don't auto-start work on a picked item — surface it and let the next step (offer conductor) frame it.

If `light` modifier was used, note: "Light pickup: smoke test skipped. Run `/kerd:switch in` for full context."

**Low:** Compress the summary to 2-3 lines: what was done last, what's next, active mode if any. Skip suggestions, skip open questions. Example:

```
Last session: fixed hook paths in krutho-founders and krutho-strategy (v0.29.1)
Next: tend on other repos, community mode contributions
```

### 11. Offer conductor

**Skip this step if `low` modifier is set.**

Ask: "Start a `/kerd:conductor` session?" If yes, flow into `/kerd:conductor` orient. If no, stop. The user wants to do something quick without full session discipline.

## Fallback Behavior

If no CONTEXT.md, TODO.md, or session logs exist (fresh repo), say so cleanly:

"Fresh repo. No previous session state found. No CONTEXT.md, no TODO.md, no session logs in kivna/sessions/. Ready to start from scratch."

If no vault is found at switch-out (no `kivna/vault.json` and no vault folder at `~/eolas/vault/[folder]/`), report this gracefully. Suggest running `/kerd:kivna scaffold` to set up the vault.

Do not fail silently or produce errors for missing files.
