# Kerd Plugin Design

**Date:** 2026-02-27
**Status:** Approved

## Overview

Kerd ("skill" from Gaelic ceird) is a Claude Code plugin containing an opinionated workflow toolkit. It packages personal productivity skills as a single installable plugin distributed via its own GitHub marketplace.

## Distribution

The Kerd repo serves as both plugin source and marketplace. Users add it with:

```
claude plugins add-marketplace <github-user>/Kerd
```

## Plugin Structure

```
Kerd/
├── README.md
├── LICENSE
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── dian/
│   │   └── SKILL.md
│   ├── switch/
│   │   └── SKILL.md
│   ├── kivna/
│   │   └── SKILL.md
│   ├── sotu/
│   │   └── SKILL.md
│   └── skriv/
│       └── SKILL.md
├── commands/
│   ├── dian.md
│   ├── switch.md
│   ├── kivna.md
│   ├── sotu.md
│   └── skriv.md
├── marketplace.json
└── docs/
    └── plans/
```

## Skills

### Dian (session discipline)

From Irish/Scottish Gaelic "dian" — intense, rigorous, severe, ardent. Pronounced "DEE-an".

**Purpose:** Protocol for staying focused within a session. No git operations — those belong to switch.

**Scope:**
- **Orient** — read TODO.md, CLAUDE.md, progress tracking. Understand current state.
- **Plan** — propose numbered steps, write to TODO.md as `## Current Session`, get user approval.
- **Execute** — do the work, commit incrementally if it makes sense.
- **Close out** — update TODO.md (check off completed, add new tasks), doc impact assessment, staleness sweep, run build/tests.

**Does NOT do:** git pull, git push, session handoff. That's switch's job.

**Command:** `/dian`

---

### Switch (machine handoff)

**Purpose:** Clean handoff between machines. Owns all git boundary operations.

**Commands:**
- `/switch out` — leaving this machine
- `/switch in` — arriving on a new machine

**`switch out` flow:**
1. Write session state to TODO.md (`## Current Session` block): what was done, what's in progress, what's next, any context that would be lost.
2. Write session log to `kivna/sessions/YYYY-MM-DD.md` with: machine hostname, what was done, key decisions, commits, what's next.
3. Update progress tracking if it exists.
4. Stage and commit all work (including session log and doc updates).
5. Push. Verify success.
6. Confirm with summary.

**`switch in` flow:**
1. `git pull`. Resolve conflicts if any.
2. Read TODO.md — focus on `## Current Session`.
3. Read latest `kivna/sessions/` files for context.
4. Read progress tracking if it exists.
5. Summarize: what was done, what's next, open questions.
6. Ask: "Ready to continue, or do you want to change direction?"

**Fallback:** If no TODO.md or session logs exist (fresh repo), say so cleanly instead of failing silently.

**Auto-detection:** If no argument given, check for uncommitted changes. Changes exist = `out`. Clean = `in`.

---

### Kivna (knowledge management)

From Gaelic "cuimhne" (memory), respelled phonetically.

**Purpose:** Single owner of the project's knowledge layer — sessions, memories, imports, exports.

**Folder convention:**
- `kivna/sessions/` — full session logs written by switch (committed to git)
- `kivna/memories/` — quick notes captured mid-session (committed to git)
- `kivna/input/` — drop files for import (gitignored, transit folder)
- `kivna/output/` — exports land here (gitignored, transit folder)

**Commands:**

**`/kivna in` — import external knowledge:**
1. List `kivna/input/`. If empty, say so and stop.
2. Read each file (supports .pdf, .md, .txt, .json, .jsonl, .html).
3. Summarize what was found — what it contains, what's relevant, where it goes.
4. Wait for approval.
5. Integrate — edit existing docs or create new ones. Extract signal from LLM transcripts (decisions, insights, action items), not raw content.
6. Clean up — delete processed files from input folder.
7. Report what was imported and where.

**`/kivna out` — export session context:**
1. Gather context from current conversation: tasks, decisions, files changed, open questions.
2. Read TODO.md and progress tracking to fill gaps.
3. Write export to `kivna/output/export-YYYY-MM-DD.md` with: what happened, key decisions, files changed, current state, open questions, project context.
4. Confirm with path and summary.

**`/kivna memory <note>` — quick save:**
- Append timestamped note to `kivna/memories/YYYY-MM-DD.md`.
- No approval flow. Instant save.
- One file per day, multiple entries with timestamps.

---

### SOTU (project health audit)

State of the Union. Read-only audit with severity-graded output.

**Purpose:** Audit registered project targets for drift, staleness, and issues.

**Config file:** `.sotu` at project root (committed to git):

```markdown
# SOTU Audit Targets

## docs
- README.md
- docs/

## code
- src/
- package.json
- tsconfig.json

## site
- public/
- next.config.js

## deps
- package.json
- package-lock.json
```

**Commands:**
- `/sotu add <area> <path>` — register a target
- `/sotu docs` — audit docs targets
- `/sotu code` — audit code targets
- `/sotu site` — audit site targets
- `/sotu deps` — audit dependency freshness
- `/sotu all` — run all areas (parallel agents where possible)
- `/sotu` (no args) — show registered targets

**Audit areas:**

**docs:** Doc inventory, name consistency, path consistency, internal links, stats drift, TODO.md accuracy, README vs CLAUDE.md agreement.

**code:** Test suite, build check, unused exports, lock file consistency, CI config.

**site:** Build check, content sync, navigation completeness, asset check, broken links.

**deps:** Package manager outdated commands, lock file consistency.

**Output format:**
- Summary line at top: "X high, Y medium, Z low"
- Severity table per area:

| Severity | File | Issue |
|----------|------|-------|
| high | factually wrong, broken build, missing file |
| medium | stale but not misleading, cosmetic inconsistency |
| low | nitpick, style drift, minor staleness |

**First run:** If no `.sotu` config exists, prompt user to register targets.

---

### Skriv (writing voice)

From Gaelic "scríobh" (the act of writing), respelled.

**Purpose:** Enforce human writing voice. Works as a pointed tool, not a persistent mode (unless opted in).

**Commands:**

**`/skriv <file>` — audit:**
Review file against rules. Report violations with line numbers and suggestions.

**`/skriv fix <file>` — rewrite:**
Apply rules directly, rewrite file in place.

**`/skriv on` / `/skriv off` — session mode:**
Applies rules to all prose output for the session. Opt-in for content-heavy sessions. Only applies to prose — never code, commits, or technical discussion.

**Inline reference:**
When mentioned in a prompt ("write this using /skriv"), rules apply to that output only.

**Rules (carried from current human-draft):**

Core rules:
- No em dashes — use commas, periods, or parentheses
- No bullet points or tables unless genuinely a list. Prose by default.
- No markdown formatting in output unless explicitly asked
- Allow uneven sections, abrupt pivots, slight redundancy
- Mix short fragments with longer sentences
- Plain language. Technical terms only when necessary.
- No five-paragraph essay structure
- No educational/instructional tone — peer sharing an opinion

Vocabulary kill list: comprehensive, robust, nuanced, leverage, facilitate, delve, realm, landscape, tapestry, multifaceted, etc. (full list in SKILL.md)

Structural rules: no acknowledge-then-answer pattern, no formal transitions, no closing summaries, no rule of three, no promotional inflation, etc. (full list in SKILL.md)

Confidence: state things directly. No hedging on confident claims.

Human texture: real details only, no manufactured anecdotes. Imperfect metaphors welcome.

Tone: calm, confident, slightly stubborn. No hype. Contractions good. Bluntness fine.

Post-draft: cut 20%. Remove restated points and transition-only paragraphs.

---

## Key Design Decisions

1. **Dian and switch are cleanly separated.** Dian owns session focus and discipline. Switch owns git boundary operations (pull, push, commit of session state). No overlap.

2. **Kivna is the single knowledge layer.** Sessions, memories, imports, exports all live under `kivna/`. Switch writes session logs there. The memory command enables quick-save without closing a session.

3. **SOTU uses committed config.** Audit targets are stored in `.sotu` at the project root so they're consistent across machines and team members.

4. **Skriv is a pointed tool by default.** Session mode is opt-in. Most usage is audit/fix on specific files or inline reference in prompts.

5. **One plugin, own marketplace.** All skills ship together. Users install once and use what they want. Distributed via the Kerd repo as a GitHub marketplace.

## Future Skills

Planned additions that will slot in as new `skills/` directories:
- HTML presentation generator from markdown
- Toyota problem-solving methodology skill
