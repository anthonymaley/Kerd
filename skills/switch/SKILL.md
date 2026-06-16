---
name: switch
description: "Use when the user says 'switch', 'wrapping up', 'picking up', 'save context', 'handoff', or 'switching machines', or needs to cleanly end a work session and resume it later with full context. The primary use is session handoff: wrap up, commit, exit, and pick up cold in a fresh session. The same mechanism carries across machines as the secondary case. Handles all git boundary operations (pull, push, commit of session state). Supports 'light' modifier to skip vault and reflection, or 'low' modifier for minimum viable handoff on tight token budgets."
---

# Switch (Session Handoff)

Clean handoff between work sessions. The primary use: wrap up a session, commit and push, exit, then pick up cold in a fresh session with full context restored from disk. The same mechanism handles moving between machines, that's just the secondary case. Switch owns all git boundary operations: pull, push, commit of session state. No other skill should do these things.

## Usage

`/kerd:switch out` wrapping up a session (full)
`/kerd:switch out light` wrapping up a session (skip vault, reflection, progress tracking)
`/kerd:switch out low` wrapping up a session (minimum viable handoff, tight token budget)
`/kerd:switch in` picking up a session (full)
`/kerd:switch in light` picking up a session (skip vault, smoke test)
`/kerd:switch in low` picking up a session (minimum viable pickup, tight token budget)

The same path serves a fresh session on this machine (the common case) and a move to another machine (the same git boundary operations either way).

If no argument is given, check for uncommitted changes. If changes exist, assume `out`. If clean, assume `in`.

### Modifier progression

| | Full | Light | Low |
|---|---|---|---|
| TODO.md update | Full session block | Full session block | Brief: 3-5 lines max |
| Session log | Full template (all sections) | Full template | Skeleton: What Was Done + What's Next only |
| Vault update | Yes (kivna save) | Skip | Skip |
| Reflection/gotchas | Yes | Skip | Skip (unless something critical) |
| Progress tracking | Yes | Skip | Skip |
| Untracked file triage | Yes | Yes | Skip (unless obviously risky files like .env) |
| Pre-commit summary | Full with evidence | Full with evidence | One-line: "Committing N files: [list]" |
| Trim suggestion | Yes | No | No |
| Final confirmation | Evidence-cited | Evidence-cited | One-line: commit hash + push target |
| **Switch-in** | | | |
| Pull | Yes | Yes | Yes |
| Handoff verification | Yes | Yes | Skip |
| Smoke test | Yes | Skip | Skip |
| Read TODO.md | Full | Full | Current Session block only |
| Read vault | Yes | Skip | Skip |
| Read session logs | Newest full, older skimmed | Newest full, older skimmed | Latest What's Next only |
| Read progress | Yes | Skip | Skip |
| Check active modes | Yes | Yes | Yes |
| Offer dian | Yes | Yes | Skip |

## Switch Out (Wrapping Up a Session)

Wrap up everything so the next session can pick up cold, whether that's a fresh session on this machine or another.

### 1. Write session state to TODO.md

Create TODO.md if it doesn't exist. **Overwrite** the `## Current Session` block — replace it in place with the current forward-looking state. `TODO.md` is forward-only: it holds what still needs doing, not a record of what's done. Never rename the block to `## Previous Session` to keep history — the completed record is written to the session log in step 2.

**Full/light:** Write what's in progress, what's next, and any unresolved context that would be lost (open decisions, things tried, open questions). Do **not** keep a list of completed items in the block — those belong in the session log. The Current Session block describes the project's forward state, not this session's diary.

**Low:** Keep it to 3-5 lines max, forward-only: what's next plus any critical open context. Skip the done-items list — the session log holds it.

**Mode snapshot:** If `kivna/.active-modes` contains a mode block, snapshot the mode state into the `### Context` section of TODO.md so cross-machine handoff works without the ephemeral file. Include: mode name, current step number and total, session instruction (if any), and the full steps list with status markers. Example:

```
### Context
- Mode active: greenfield (step 4 of 9)
  Instruction: focus on pricing strategy only
  Steps: 1 done, 2 done, 3 done, 4 current, 5-9 pending
```

### 1b. Heal accumulated history

`TODO.md` is forward-only, so it must contain no `## Previous Session` or `## Older Session` blocks. Scan for them (drift from before this rule, or a slip). For each block found:

1. Read its date from the heading, or from any explicit `kivna/sessions/<date>.md` reference inside the block. If neither yields a date, treat the block as **undated**.
2. If `kivna/sessions/<date>.md` already exists for that date → the block is already archived; remove it from `TODO.md`.
3. If no log exists for that date → **rescue first**: create `kivna/sessions/<date>.md` from the block's content (or append under a `---` separator if a same-day file already exists), then remove the block. For an **undated** block, rescue it to a new `kivna/sessions/undated-<slug>.md` (slug from the heading text) instead, then remove.
4. Never delete a block when its content is not first preserved in a session log — rescue is mandatory before removal, dated or not.

Report: "Healed TODO: N session block(s) archived (M rescued)." If none exist, skip silently. This runs in all modes (full/light/low) — it is cheap and is the backstop that prevents unbounded TODO growth.

### 2. Write session log

Create `kivna/sessions/YYYY-MM-DD.md` (or append if one already exists for today).

If appending to an existing file for today (multiple sessions), add a `---` separator and a new section with a time or sequence number.

The session log captures what happened in this session for the next session to pick up cold. Two sections are **required**: `## What Was Done` and `## What's Next`. Four sections are **optional**: `## Key Decisions`, `## Commits`, `## Gotchas`, `## Insights`. Read the rules below before writing.

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

### 3. Update the vault

**Skip this step if `light` or `low` modifier is set.**

Call `/kerd:kivna save`. Switch owns the vault save now; dian no longer touches the vault. This updates Status.md and proposes updates to other vault files, each with user approval. (If a kivna save already ran earlier this session, it will just surface a near-empty diff.)

### 4. Update progress tracking

**Skip this step if `light` or `low` modifier is set.**

If progress tracking exists (check for `docs/project/progress.md`, `progress.md`, or similar), update it.

### 5. Reflect and capture learnings

**Skip this step if `light` or `low` modifier is set** — with one exception: if something genuinely critical broke or a dangerous gotcha was discovered during the session, capture it even in low mode. One line in the session log is enough. The bar for "critical" in low mode is: would the next person waste significant time without this information?

Before committing, reflect on the session:

- **What broke unexpectedly?** Any gotchas, edge cases, or non-obvious behavior discovered? These go in the session log `## Gotchas` section AND in `docs/playbook.md` Gotchas section (so they survive beyond session logs).
- **What patterns emerged?** Any recurring problems, useful approaches, or workflow improvements worth codifying?
- **What should be remembered?** Best practices discovered, conventions that worked well or didn't.
- **What would make the next session better?** Anything about the project, tooling, or workflow that should be adjusted.

Write actionable learnings to the appropriate place:
- **Gotchas** → add to `docs/playbook.md` Gotchas section (duplicates what's in the session log, but the playbook is the living reference; session logs are archives)
- **Project conventions and enforcement rules** → add to `CLAUDE.md` (so they're enforced in future sessions)
- **Conventions and patterns** → flag for the appropriate vault file (Architecture Decisions, Positioning Contract, etc.), these get proposed during the `/kerd:kivna save` step

Skip this step if the session was trivial (quick fix, single file change). But for any session with meaningful work, take the time. Compounding small improvements across sessions is how projects stay healthy.

### 6. Triage, commit, and push

Before staging anything, run `git status` to see the actual state of the working tree. Classify every changed or untracked file into two buckets:

- **Session files** — files this session created or modified (TODO.md, session log, playbook updates, vault files, etc.). These are auto-committed without asking.
- **Unexpected files** — untracked files that existed before switch-out started, or modifications the session didn't make. These need a decision.

#### Normal path (no unexpected files)

Stage session files by name, commit with a descriptive message, and push. No confirmation prompt. Then show the completion banner (step 7).

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

### 7. Completion banner

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

Pick up where the last session left off.

### 1. Pull

`git pull`. If there are conflicts, resolve them before proceeding.

### 2. Handoff contract verification

**Skip this step if `low` modifier is set.**

After pulling, verify the outgoing machine completed its handoff. Check:

- Does `TODO.md` exist and have a `## Current Session` block?
- Does the latest file in `kivna/sessions/` have a `## What's Next` section?

If both are present, proceed normally. If either is missing, flag it explicitly:

```
⚠ Partial handoff detected:
  - TODO.md missing ## Current Session block
  - Latest session log missing ## What's Next
  
  Proceeding with available context. Some state may be missing.
```

Do not pretend the pickup is clean when the handoff was incomplete.

### 3. Smoke test

**Skip this step if `light` or `low` modifier is set.**

If the project has a test command (check `package.json` scripts, `Makefile`, `pyproject.toml`, or similar), run it. If tests fail, report the failures in the summary. The user should know the state of the codebase before planning new work. If no test command exists, skip this step.

### 4. Read TODO.md

Focus on the `## Current Session` block. This is where the last session left off.

**Low:** Read only the `## Current Session` block. Do not read the Backlog or any other sections.

### 5. Read vault

**Skip this step if `light` or `low` modifier is set.**

Discover the vault path using `kivna/vault.json` or convention (see `/kerd:kivna` vault discovery). Read `[Name] Status.md` for where the project stands. Read the MOC (`[Name].md`) to discover what other vault files exist and read any that are relevant (Architecture Decisions, Playbook, etc.).

### 6. Check session logs

**Full/light:** Read the most recent file in `kivna/sessions/` in full. For older session logs (if any exist), skim only the `## What's Next`, `## Key Decisions`, and `## Gotchas` sections to find the pickup point and any unresolved issues. Do not read older logs in full unless the user asks.

**Low:** Read only the `## What's Next` section of the latest session log. Skip everything else.

### 7. Read progress tracking

**Skip this step if `light` or `low` modifier is set.**

If progress tracking exists, read it.

### 8. Check active modes

Check two sources for mode state:

1. **`kivna/.active-modes`** (same-machine resume): if it exists and is non-empty, read it and report active modes.
2. **`TODO.md` Context block** (cross-machine handoff): if `.active-modes` doesn't exist or is empty, check TODO.md's `### Context` section for a mode snapshot. If found, report it and offer to restore it to `.active-modes`.

Report any active modes in the summary (e.g., "**Active modes:** `greenfield (step 4 of 9)`"). If neither source has mode state, skip this. Don't mention modes.

### 9. Summarize

Tell the user:
- What was done last session
- What's in progress or queued next
- Any open questions or decisions from the previous session
- Any test failures from the smoke test (if applicable, full mode only)
- Any handoff issues detected in step 2
- Suggest what to work on

If `light` modifier was used, note: "Light pickup: vault and smoke test skipped. Run `/kerd:switch in` for full context."

**Low:** Compress the summary to 2-3 lines: what was done last, what's next, active mode if any. Skip suggestions, skip open questions. Example:

```
Last session: fixed hook paths in krutho-founders and krutho-strategy (v0.29.1)
Next: tend on other repos, community mode contributions
```

### 10. Offer dian

**Skip this step if `low` modifier is set.**

Ask: "Start a `/kerd:dian` session?" If yes, flow into `/kerd:dian` orient. If no, stop. The user wants to do something quick without full session discipline.

## Fallback Behavior

If no TODO.md or session logs exist (fresh repo), say so cleanly:

"Fresh repo. No previous session state found. No TODO.md, no session logs in kivna/sessions/. Ready to start from scratch."

If no vault is found (no `kivna/vault.json` and no vault folder at `~/eolas/vault/[folder]/`), report this gracefully. Suggest running `/kerd:kivna scaffold` to set up the vault.

Do not fail silently or produce errors for missing files.
