# Kerd Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Kerd plugin with 5 skills (dian, switch, kivna, sotu, skriv) packaged as a Claude Code plugin distributed via its own marketplace.

**Architecture:** Single plugin repo that doubles as marketplace. Skills in `skills/<name>/SKILL.md`, commands in `commands/<name>.md` as thin wrappers. Marketplace config in `.claude-plugin/marketplace.json` pointing to self.

**Tech Stack:** Claude Code plugin system (markdown skills, markdown commands, JSON config)

---

### Task 1: Plugin scaffolding

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Modify: `README.md`

**Step 1: Create plugin.json**

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "kerd",
  "description": "Opinionated workflow toolkit — session discipline, machine handoff, knowledge management, project audits, and human writing voice",
  "version": "0.1.0",
  "author": {
    "name": "Anthony Maley"
  },
  "homepage": "https://github.com/anthonymaley/Kerd",
  "repository": "https://github.com/anthonymaley/Kerd",
  "license": "MIT",
  "keywords": ["skills", "workflow", "session-management", "writing", "audit"]
}
```

**Step 2: Create marketplace.json**

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "kerd-marketplace",
  "owner": {
    "name": "Anthony Maley"
  },
  "metadata": {
    "description": "Kerd — opinionated workflow skills for Claude Code",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "kerd",
      "source": {
        "source": "url",
        "url": "https://github.com/anthonymaley/Kerd.git"
      },
      "description": "Opinionated workflow toolkit — session discipline, machine handoff, knowledge management, project audits, and human writing voice",
      "version": "0.1.0",
      "strict": true
    }
  ]
}
```

**Step 3: Update README.md**

Replace the current README with a proper plugin README:

```markdown
# Kerd

"Ceird" means skill in Gaelic. Respelled.

An opinionated workflow toolkit for Claude Code. Session discipline, machine handoff, knowledge management, project audits, and human writing voice.

## Install

```
claude plugins add-marketplace anthonymaley/Kerd
claude plugins install kerd
```

## Skills

| Name | What it does |
|------|-------------|
| **dian** | Session discipline — orient, plan, execute, close out |
| **switch** | Machine handoff — clean wrap-up and pick-up across machines |
| **kivna** | Knowledge management — import, export, session logs, quick memories |
| **sotu** | Project health audit — registered targets, severity-graded reports |
| **skriv** | Writing voice — audit, fix, and enforce human writing standards |

## Commands

| Command | Usage |
|---------|-------|
| `/dian` | Start a structured session |
| `/switch in\|out` | Arrive on or leave a machine |
| `/kivna in\|out\|memory <note>` | Import, export, or save a memory |
| `/sotu [area]\|add <area> <path>` | Run audit or register targets |
| `/skriv [file]\|fix <file>\|on\|off` | Audit, fix, or toggle session mode |

## Naming

Gaelic-inspired where it adds character:
- **Kerd** — skill (ceird)
- **Kivna** — memory (cuimhne)
- **Dian** — intense, rigorous
- **Skriv** — the act of writing (scríobh)
```

**Step 4: Create LICENSE**

Create a standard MIT LICENSE file.

**Step 5: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json README.md LICENSE
git commit -m "feat: add plugin scaffolding and marketplace config"
```

---

### Task 2: Dian skill (session discipline)

**Files:**
- Create: `skills/dian/SKILL.md`
- Create: `commands/dian.md`

**Step 1: Create the skill**

Create `skills/dian/SKILL.md`:

```markdown
---
name: dian
description: "Use when starting a work session, when you need structured session discipline, or when the user says 'dian', 'session', 'let's get structured', or wants to plan and track a focused work block. Provides orient-plan-execute-close protocol."
---

# Dian — Session Discipline

From Irish/Scottish Gaelic "dian" — intense, rigorous. Pronounced "DEE-an".

A protocol for staying focused within a session. Dian does not touch git boundaries (pull/push) — that's switch's job. Dian keeps you on track once you're working.

## The Protocol

### 1. Orient

Read these files if they exist (skip any that don't):

1. `TODO.md` — current session plan, roadmap, task queue
2. `CLAUDE.md` — project conventions and structure
3. Progress tracking — check `docs/project/progress.md`, `progress.md`, or `CHANGELOG.md`
4. Decision log — check `docs/project/decisions.md` or `decisions.md` if the work involves architecture choices

Summarize the current state for the user.

### 2. Plan

Propose a session plan to the user:
- What we'll do (numbered steps)
- What files we'll touch
- What docs need updating

Write this as a `## Current Session` block in TODO.md with today's date. Wait for user approval before executing.

### 3. Execute

Do the work. Commit incrementally if it makes sense. Stay focused on the plan — if scope creep appears, flag it and add it to TODO.md for later rather than chasing it now.

### 4. Close Out

Before ending the session:

1. **Update TODO.md** — check off completed tasks, add new ones discovered during work, update roadmap statuses, clear the `## Current Session` block.
2. **Doc impact assessment** — if the project has a Doc Impact Table in CLAUDE.md, check it. Update ALL affected docs.
3. **Staleness sweep** — search for any renamed or changed concepts across `docs/`, `README.md`, and other documentation.
4. **Run checks** — run the project's build/test command if one exists. Do not close out with failing tests.

## Principles

- **No git boundary ops.** No `git pull`, no `git push`. Use `/switch` for that.
- **Flag scope creep.** If something comes up that isn't in the plan, add it to TODO.md and stay on track.
- **Incremental commits.** Commit working states, not big bangs.
- **Docs travel with code.** If you change behavior, update the docs in the same commit.
```

**Step 2: Create the command**

Create `commands/dian.md`:

```markdown
---
description: "Start a structured work session — orient, plan, execute, close out"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
---

Invoke the kerd:dian skill and follow it exactly as presented to you.
```

**Step 3: Commit**

```bash
git add skills/dian/SKILL.md commands/dian.md
git commit -m "feat: add dian skill — session discipline protocol"
```

---

### Task 3: Switch skill (machine handoff)

**Files:**
- Create: `skills/switch/SKILL.md`
- Create: `commands/switch.md`

**Step 1: Create the skill**

Create `skills/switch/SKILL.md`:

```markdown
---
name: switch
description: "Use when the user says 'switch', 'switching machines', 'wrapping up', 'picking up', 'handoff', or needs to cleanly leave or arrive on a machine. Handles all git boundary operations (pull, push, commit of session state)."
---

# Switch — Machine Handoff

Clean handoff between machines. Switch owns all git boundary operations — pull, push, commit of session state. No other skill should do these things.

## Usage

`/switch out` — leaving this machine
`/switch in` — arriving on a new machine

If no argument is given, check for uncommitted changes. If changes exist, assume `out`. If clean, assume `in`.

## Switch Out — Leaving This Machine

Wrap up everything so the next machine can pick up cold.

### 1. Write session state to TODO.md

Create TODO.md if it doesn't exist. Update the `## Current Session` block with:
- What was done (check off completed items)
- What's in progress (mark clearly)
- What's next (so the next session knows where to start)
- Any context that would be lost (decisions made in conversation, things tried that didn't work, open questions)

### 2. Write session log

Create `kivna/sessions/YYYY-MM-DD.md` (or append if one already exists for today) with:

```
# Session — YYYY-MM-DD

**Machine:** [hostname from `hostname`]

## What Was Done
[Concrete list of what was accomplished. Be specific: files created, features built, bugs fixed, decisions made.]

## Key Decisions
[Any decisions made during the session with brief reasoning. Skip if none.]

## Commits
[List commit hashes and messages from this session]

## What's Next
[What the next session should pick up]
```

If appending to an existing file for today (multiple sessions), add a `---` separator and a new section with a time or sequence number.

### 3. Update progress tracking

If progress tracking exists (check for `docs/project/progress.md`, `progress.md`, or similar), update it.

### 4. Stage and commit

Stage all work including the session log and doc updates. Use a descriptive commit message.

### 5. Push

Push to remote. Verify the push succeeds.

### 6. Confirm

Print a short summary: what was pushed, what the next session should start with.

## Switch In — Arriving on This Machine

Pick up where the other machine left off.

### 1. Pull

`git pull`. If there are conflicts, resolve them before proceeding.

### 2. Read TODO.md

Focus on the `## Current Session` block. This is where the last session left off.

### 3. Check session logs

Read the latest file(s) in `kivna/sessions/` for detailed context on what happened recently.

### 4. Read progress tracking

If progress tracking exists, read it.

### 5. Summarize

Tell the user:
- What was done last session
- What's in progress or queued next
- Any open questions or decisions from the previous session
- Suggest what to work on

### 6. Ask

"Ready to continue, or do you want to change direction?"

## Fallback Behavior

If no TODO.md or session logs exist (fresh repo), say so cleanly:

"Fresh repo — no previous session state found. No TODO.md, no session logs in kivna/sessions/. Ready to start from scratch."

Do not fail silently or produce errors for missing files.
```

**Step 2: Create the command**

Create `commands/switch.md`:

```markdown
---
description: "Seamless machine switch — wraps up current session or picks up from another machine"
argument-hint: "<direction: out|in>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

The user's argument is: $ARGUMENTS

Invoke the kerd:switch skill and follow it exactly as presented to you.
```

**Step 3: Commit**

```bash
git add skills/switch/SKILL.md commands/switch.md
git commit -m "feat: add switch skill — machine handoff protocol"
```

---

### Task 4: Kivna skill (knowledge management)

**Files:**
- Create: `skills/kivna/SKILL.md`
- Create: `commands/kivna.md`

**Step 1: Create the skill**

Create `skills/kivna/SKILL.md`:

```markdown
---
name: kivna
description: "Use when the user says 'kivna', 'import', 'export context', 'save memory', 'remember this', or needs to manage project knowledge — importing external files, exporting session context, or saving quick notes mid-session."
---

# Kivna — Knowledge Management

From Gaelic "cuimhne" (memory), respelled phonetically.

Single owner of the project's knowledge layer. Sessions, memories, imports, exports all live under `kivna/`.

## Folder Convention

- `kivna/sessions/` — full session logs written by switch (committed to git)
- `kivna/memories/` — quick notes captured mid-session (committed to git)
- `kivna/input/` — drop files here for import (should be gitignored, transit folder)
- `kivna/output/` — exports land here (should be gitignored, transit folder)

## Commands

### `/kivna in` — Import External Knowledge

Read files from `kivna/input/`, extract what's relevant, write it into the project, delete the originals.

1. **List the inbox.** `ls kivna/input/` — show the user what's there. If empty, say so and stop.

2. **Read each file.** Supported formats:
   - `.pdf` — read with the Read tool (supports PDF)
   - `.md`, `.txt` — read directly
   - `.json`, `.jsonl` — read as structured data (likely LLM session exports)
   - `.html` — read and extract text content
   - Other formats — tell the user you can't process them, skip

3. **Summarize what you found.** For each file, tell the user:
   - What it contains (1-2 sentences)
   - What's relevant to this project
   - Where you'd put it (existing doc to update, new file to create, or discard)

4. **Wait for approval.** Do not write anything until the user confirms.

5. **Integrate.** For each approved item:
   - If updating an existing doc, use Edit to add the relevant content
   - If creating a new doc, prefer putting it in the project's natural doc structure
   - If the content is a session transcript from another LLM, extract decisions, insights, and action items — do not copy the raw transcript
   - Write in the project's voice

6. **Clean up.** Delete the processed files from `kivna/input/`. Leave any files the user said to skip.

7. **Report.** Tell the user what was imported and where it went.

### `/kivna out` — Export Session Context

Package the current session's work into a portable file another LLM can use as input.

1. **Gather context.** From the current conversation, collect:
   - What was done this session (tasks completed, decisions made)
   - Key files created or modified (with brief descriptions)
   - Architecture decisions and their reasoning
   - Open questions or unresolved items
   - Current project state (what's working, what's blocked)

2. **Read TODO.md and any progress tracking** to fill gaps.

3. **Write the export.** Create `kivna/output/export-YYYY-MM-DD.md` with this structure:

```
# Session Export — [Project Name] — [Date]

## What Happened
[Plain prose summary of the session. What was built, fixed, or decided.]

## Key Decisions
[Each decision with its reasoning. Another LLM needs to understand WHY, not just WHAT.]

## Files Changed
[List of files with one-line descriptions of what changed and why]

## Current State
[What works, what's blocked, what's next]

## Open Questions
[Anything unresolved that needs input]

## Project Context
[Brief description of the project, its structure, and conventions — enough for a cold start in another tool]
```

4. **Confirm.** Show the user the export path and a summary of what's in it.

### `/kivna memory` — Quick Save

Save a note mid-session without ceremony.

- Takes freeform text as the argument: `/kivna memory decided to use PostgreSQL over SQLite for concurrency reasons`
- Append a timestamped entry to `kivna/memories/YYYY-MM-DD.md`
- One file per day, multiple entries with timestamps
- Create the file and `kivna/memories/` directory if they don't exist
- Quick confirmation only — no approval flow

Format in the memories file:

```
## HH:MM

[note text]
```

## Notes

- `kivna/input/` and `kivna/output/` should be in `.gitignore` — they're transit folders, not project content.
- `kivna/sessions/` and `kivna/memories/` should be committed to git — they're permanent history.
- Exports are written in plain markdown so any LLM can read them.
- When importing LLM session transcripts, be aggressive about filtering. Most of a chat session is noise. Extract the signal: decisions, code patterns, insights, action items.
- When importing PDFs or reports, focus on what's actionable for THIS project.
```

**Step 2: Create the command**

Create `commands/kivna.md`:

```markdown
---
description: "Import external knowledge, export session context, or save a quick memory"
argument-hint: "<direction: in|out|memory <note>>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

The user's argument is: $ARGUMENTS

If no argument is given, check if `kivna/input/` has files. If yes, assume `in`. If empty or missing, assume `out`.

Invoke the kerd:kivna skill and follow it exactly as presented to you.
```

**Step 3: Commit**

```bash
git add skills/kivna/SKILL.md commands/kivna.md
git commit -m "feat: add kivna skill — knowledge management"
```

---

### Task 5: SOTU skill (project health audit)

**Files:**
- Create: `skills/sotu/SKILL.md`
- Create: `commands/sotu.md`

**Step 1: Create the skill**

Create `skills/sotu/SKILL.md`:

```markdown
---
name: sotu
description: "Use when the user says 'sotu', 'audit', 'health check', 'check staleness', 'state of the union', or needs to audit project health across docs, code, site, or dependencies. Read-only audit that reports issues without fixing them."
---

# SOTU — State of the Union

Read-only audit of project health. Reports issues with severity grades. Does not fix anything — that's the user's call.

## Config

SOTU uses a `.sotu` config file at the project root to know what to audit. If no config exists on first run, prompt the user to register targets.

### Config format (`.sotu`):

```
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

## Commands

### `/sotu` (no args)

Show the current `.sotu` config — what's registered under each area. If no config exists, say so and offer to create one.

### `/sotu add <area> <path>`

Register a file or directory under an area. Create `.sotu` if it doesn't exist. Valid areas: `docs`, `code`, `site`, `deps`.

Example: `/sotu add docs README.md`

### `/sotu <area>`

Run the audit for the specified area. Valid areas: `docs`, `code`, `site`, `deps`, `all`.

#### docs

For each target registered under `## docs`:

1. **Doc inventory** — if CLAUDE.md has a docs table, cross-reference: every file listed should exist, every doc file should be listed
2. **Name consistency** — search for old or stale names across all docs. Check CLAUDE.md or README for the canonical project name.
3. **Path consistency** — search for broken internal links and old paths
4. **Internal links** — check markdown links between docs resolve to real files
5. **Stats drift** — check test counts, package counts, and other metrics against actual values
6. **TODO.md accuracy** — are "done" items actually done? Are "blocked" items still blocked?
7. **README vs CLAUDE.md** — do they agree on structure, counts, and key details?

#### code

For each target registered under `## code`:

1. **Test suite** — run all tests, report failures
2. **Build check** — run the project's build command, report errors
3. **Unused exports** — spot-check main entry points against actual usage
4. **Lock file consistency** — lock files match manifests
5. **CI config** — if `.github/workflows/` exists, check it references correct versions and commands

#### site

For each target registered under `## site`:

1. **Build check** — run the site build command, must pass clean
2. **Content sync** — if docs are synced from a source directory, check for drift
3. **Navigation completeness** — every doc should appear in sidebar/nav config
4. **Asset check** — referenced assets should exist
5. **Broken links** — scan for references to deleted files

#### deps

For each target registered under `## deps`:

1. **Dependency freshness** — run package manager outdated commands (npm outdated, pip list --outdated, cargo outdated, etc.)
2. **Lock file consistency** — lock files match manifests
3. **Security vulnerabilities** — run `npm audit`, `pip audit`, or equivalent if available

#### all

Run all areas. Use parallel agents where possible for speed.

## Output Format

Start with a summary line:

```
SOTU: X high, Y medium, Z low
```

Then a severity table per area:

| Severity | File | Issue |
|----------|------|-------|
| high | `docs/whitepaper.md` | References old project name |
| medium | `CLAUDE.md` | Test count says 145, actual is 148 |
| low | `README.md` | Minor formatting inconsistency |

### Severity guide:
- **high** — factually wrong, broken build, missing file, security vulnerability
- **medium** — stale but not misleading, cosmetic inconsistency
- **low** — nitpick, style drift, minor staleness
```

**Step 2: Create the command**

Create `commands/sotu.md`:

```markdown
---
description: "State of the Union — audit project health for drift, staleness, and issues"
argument-hint: "[area: docs|code|site|deps|all] or [add <area> <path>]"
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit, Task]
---

The user's argument is: $ARGUMENTS

If no argument is given, show the current .sotu config.

Invoke the kerd:sotu skill and follow it exactly as presented to you.
```

**Step 3: Commit**

```bash
git add skills/sotu/SKILL.md commands/sotu.md
git commit -m "feat: add sotu skill — project health audit"
```

---

### Task 6: Skriv skill (writing voice)

**Files:**
- Create: `skills/skriv/SKILL.md`
- Create: `commands/skriv.md`

**Step 1: Create the skill**

Create `skills/skriv/SKILL.md`:

```markdown
---
name: skriv
description: "Use when the user says 'skriv', 'human draft', 'write like a human', 'check my writing', 'fix the tone', or needs to audit, fix, or write prose with human voice. Also activates when referenced inline in a prompt (e.g. 'write this using skriv'). Applies to prose only — never code, commits, or technical discussion."
---

# Skriv — Writing Voice

From Gaelic "scríobh" (the act of writing), respelled. The physical act of putting words down, not generating them.

## Modes

### Audit: `/skriv <file>`

Review the file against the rules below. Report violations with line numbers and suggestions. Do not modify the file.

Output format:
```
Line 12: "leverage" — kill list word. Try: "use" or "build on"
Line 28: em dash found — use comma, period, or parentheses
Line 45-52: five-paragraph essay structure — rewrite as direct prose
```

### Fix: `/skriv fix <file>`

Apply the rules directly. Rewrite the file in place. Then cut 20% — remove any sentence that restates a point already made, remove any paragraph that exists only to transition.

### Session mode: `/skriv on` / `/skriv off`

When on, apply rules to all prose output for the rest of the session. Only applies to prose — never code, commits, or technical discussion. Off by default.

### Inline reference

When mentioned in a prompt ("write this blog post using /skriv", "review this content against /skriv"), the rules apply to that specific output only.

---

## The Rules

### Core

- No em dashes. Use commas, periods, or parentheses instead.
- No bullet points or tables unless the content is genuinely a list of items. Prose by default.
- No markdown formatting (bold, headers, tables) in the output unless explicitly asked. Write in plain paragraphs.
- Allow uneven sections, abrupt pivots, and slight redundancy.
- Mix short fragments with longer, winding sentences. Some sentences should be four words. Some should run long enough that a copyeditor would flag them.
- Use plain language. Technical terms only when necessary and grounded in reality.
- Do not write in five-paragraph essay structure. No intro, no three supporting paragraphs, no conclusion. Just write.
- Do not write in an educational or instructional tone. You are a peer sharing an opinion, not teaching a class.
- Never sound like a framework, manifesto, or platform pitch.

### Vocabulary Kill List

Never use these words or phrases: straightforward, comprehensive, robust, nuanced, leverage, facilitate, delve, realm, landscape, tapestry, multifaceted, it's worth noting, that said, generally speaking, in many cases, certainly, absolutely, I'd be happy to, let me, here's what, notably, ultimately, essentially, at its core, in terms of, strikes a balance, crucial, pivotal, groundbreaking, unleash, harness, navigate (metaphorical), game-changer, revolutionize, cutting-edge, dynamic, innovative, holistic, seamless, transformative, impactful, actionable, meticulous, proactive, intricate, underscore, foster, testament, enhance, captivate, watershed moment, deeply rooted, steadfast, breathtaking, stunning, enduring legacy, lasting legacy, rich cultural heritage, rich history, profound.

Never use these phrase patterns:
- "stands as a..." / "serves as a testament to..."
- "plays a vital/significant/crucial role"
- "leaves a lasting impact"
- "continues to captivate/inspire"
- "it's important to note/remember/consider"
- "no discussion would be complete without"
- "in this article" / "in this piece"
- "on the other hand" / "in addition" / "in contrast"
- "Overall," or "In conclusion" to begin a closing sentence

### Structure

- No "acknowledge then answer" pattern. Do not compliment the question or restate it before answering.
- No "First... Second... Third..." enumeration in prose.
- No formal transition words between paragraphs. No "However," "Furthermore," "Additionally," "Moreover," "That said." Start the next thought directly. "But" and "And" at sentence starts are fine.
- Do not end with a question back to the reader or an offer to help further. End when the last point is made.
- Do not open by restating what the piece is about. Start with the first actual point.
- Do not close by summarizing what was just said. No "Key Takeaways" sections.
- No rule of three. Do not default to triplets in lists or adjective chains ("convenient, efficient, and innovative"). Vary list lengths: sometimes two, sometimes four, sometimes one.
- No "It's not X, it's Y" negative parallelism constructions.
- No false ranges ("From X to Y") that imply a spectrum without actual progression.
- No -ing words as hollow commentary (ensuring, highlighting, emphasizing, reflecting, underscoring). If you need to explain why something matters, actually explain it.
- No weasel attribution. Do not write "some critics argue," "industry experts suggest," "observers have noted" without naming the source. Either cite someone specific or state the claim directly.
- No promotional inflation. Do not overstate significance. If something is good, say how. Do not call it a "key turning point" or say it "solidified its place."
- No bold-term-then-definition structure in running prose. That is a glossary, not writing.

### Confidence

State things directly. Do not hedge claims you're confident about. "This doesn't work" is better than "In many cases, this may not produce optimal results." If genuinely uncertain, say "I don't know" rather than softening with qualifiers. Take a position.

### Human Texture

If a specific memory or detail would naturally support a point, include it. Do not manufacture anecdotes. Leaving a claim unsupported is better than faking a story. Use imperfect metaphors. The writing should feel learned, not declared.

### Tone

Calm, confident, slightly stubborn. No hype. Assume the reader is smart and a little skeptical. Write like you've been in the room when things went wrong. Contractions are good. It is okay to be blunt.

### After Drafting

Cut 20%. Remove any sentence that restates a point already made. Remove any paragraph that exists only to transition. If the piece reads fine without a sentence, delete it. One pass of cuts, then stop.

### Goal

The output should feel like a first or second draft by an experienced human. Slightly messy, specific, and defensible. Something a peer would believe you actually wrote.
```

**Step 2: Create the command**

Create `commands/skriv.md`:

```markdown
---
description: "Enforce human writing voice — audit files, fix prose, or toggle session mode"
argument-hint: "<file>|fix <file>|on|off"
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

The user's argument is: $ARGUMENTS

If no argument is given, tell the user the available modes:
- `/skriv <file>` — audit a file against the rules
- `/skriv fix <file>` — rewrite a file applying the rules
- `/skriv on` / `/skriv off` — toggle session mode for all prose output

Invoke the kerd:skriv skill and follow it exactly as presented to you.
```

**Step 3: Commit**

```bash
git add skills/skriv/SKILL.md commands/skriv.md
git commit -m "feat: add skriv skill — human writing voice"
```

---

### Task 7: Final cleanup and verification

**Files:**
- Modify: `README.md` (verify accuracy)

**Step 1: Verify all files exist**

Run:
```bash
find . -name "SKILL.md" -o -name "plugin.json" -o -name "marketplace.json" | sort
```

Expected:
```
./.claude-plugin/marketplace.json
./.claude-plugin/plugin.json
./skills/dian/SKILL.md
./skills/kivna/SKILL.md
./skills/skriv/SKILL.md
./skills/sotu/SKILL.md
./skills/switch/SKILL.md
```

**Step 2: Verify all commands exist**

Run:
```bash
ls commands/
```

Expected: `dian.md  kivna.md  skriv.md  sotu.md  switch.md`

**Step 3: Verify README matches actual structure**

Read README.md and confirm all skill names, commands, and descriptions match what was built.

**Step 4: Final commit if any corrections needed**

```bash
git add -A
git commit -m "chore: final cleanup and verification"
```
