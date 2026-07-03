---
name: tend
description: "Use when the user says 'tend', 'check structure', 'fix drift', 'structural health check', 'set up this project', 'initialize kerd', 'scaffold', or needs to audit or converge repo structure to current Kerd conventions. Works on new repos (full setup) and existing repos (detect drift, fix gaps)."
---

# Tend (Structural Health & Convergence)

Audits repo infrastructure against current Kerd conventions. Shows a visual report of current vs expected state. Fixes with approval.

Run it on a new repo to set up everything. Run it on an existing repo to catch drift. Run it after a Kerd version bump to pick up new conventions. Safe to run anytime. It converges, never destroys.

## Usage

`/kerd:tend`: run in the root of a git repo

## Boundary with Slainte

- **tend**: structure and plumbing (dirs, vault, config files, naming, stray files, deprecated patterns).
- **slainte**: content (doc accuracy, staleness, consistency, CLAUDE.md sections).

## The Process

### 1. Verify git

Confirm `.git` exists. If not, stop: "No git repo found. Initialize a repo and set up a remote first, then run `/kerd:tend` again."

### 2. Infer project identity

Resolve the project name without asking questions:

1. Check `kivna/vault.json` → `name` field
2. Check `README.md` → first `# heading`
3. Fall back to the directory name, title-cased

Only ask for project name and one-line description if this is a brand new repo (no README.md, no CLAUDE.md, no docs/).

### 3. Run all checks

Run each category below. Collect results into three buckets:
- `✓` passing: no action needed
- `✗` failing: needs creation or structural fix
- `⚠` warning: needs cleanup or migration

#### Category 1: Directory structure

Check required dirs exist:
- `kivna/`
- `kivna/sessions/`
- `docs/`

#### Category 2: Required files

Check these files exist:
- `README.md`
- `CLAUDE.md`
- `CONTEXT.md`
- `TODO.md`
- `docs/playbook.md`
- `.slainte`
- `kivna/vault.json`

**TODO shape check (drift detection):** TODO.md must be lean — `## Now` + `## Backlog` only. Flag `⚠` if it contains a `## Current Session` block, a `### Context` section, or any `## Previous/Older Session` blocks (pre-split shape, v0.60.0). The fix is the next `/kerd:switch out`, which self-migrates; tend detects, switch heals. Same for a missing CONTEXT.md when TODO.md exists — flag as pre-split, don't create it here.

For brand new repos (user provided project name), create missing files using these templates:

**README.md:**
```
# [Project Name]

[One-line description]
```

**TODO.md:**
```
# TODO

## Now

## Backlog
```

**CONTEXT.md:**
```
# Context

## What This Is
[One paragraph: the project in brief]

## Where We Are
[Current working state]
```

**CLAUDE.md:**
```
# [Project Name]

## Session Workflow

When wrapping up a session (`/kerd:switch out` or `/kerd:conductor`):
1. Update `TODO.md`: check off completed items, add new ones.
2. Update `docs/playbook.md`: if any new steps, tools, or config were added during the session, add them to the playbook. Always update the "Current Status" section.

## Doc Impact Table

| Doc | Update When |
|-----|-------------|
| README.md | Project description, setup steps, or structure changes |
| docs/playbook.md | New setup steps, integrations, gotchas, tech stack changes, or status changes |
| TODO.md | Every session close-out |
```

**docs/playbook.md:**
```
# Playbook: [Project Name]

How to rebuild this project from scratch.

## Tech Stack
[What tools/frameworks and why they were chosen]

## Setup
[Steps to get the project running locally]

## Architecture
[Key structural decisions and why]

## Integrations
[External services, APIs, config needed]

## Deployment
[How to deploy, environment variables needed]

## Gotchas
[Things that broke, non-obvious behavior, workarounds]

## Current Status
[What's working, what's in progress, what's next]
```

**.slainte:**
```
# Slainte Audit Targets

## docs
- README.md
- docs/

## playbook
- docs/playbook.md
```

**kivna/vault.json:**
```json
{
  "vault": "~/eolas/vault",
  "folder": "[project-name-lowercase]",
  "name": "[Project Name]"
}
```

For existing repos, only report missing files. Don't create them with templates. The user may have a reason for their absence, or may want to create them with project-specific content.

#### Category 3: Vault integration

Check:
- `kivna/vault.json` exists and is valid JSON with `vault`, `folder`, `name` fields
- The vault folder at the resolved path exists on disk
- **Spine complete**: the spine is `[Name].md` (MOC) + `[Name] Status.md` + `[Name] Weekly.md`. Flag any missing spine file. The fix for a missing spine file is `/kerd:kivna scaffold` (which is idempotent — it fills gaps without clobbering existing files); kivna owns vault writes, tend only detects. (Spine convention: `docs/vault-spec.md`.)
- **No vault-side session history**: flag a `sessions/`, `sessions-of-record/`, or similar dated-log folder inside the vault folder. Session history lives in the repo (`kivna/sessions/`), never in the vault. The fix is to remove it from the vault (the repo is the system of record).
- **No symlinks**: scan the vault folder for symlinks pointing to the repo. Each symlink is a violation.
- **No banned files**: check for files that don't belong in the vault: `CLAUDE.md`, `README.md`, `TODO.md`, `Context.md`, `[Name] Context.md`, `[Name] Log.md`, `Log.md`, session export files, any file whose name doesn't start with the project/company name (generic names like `Decisions.md`, `Notes.md`)
- **Self-identifying filenames**: every file in the vault folder (except the MOC) should start with the project or company name. Flag files that would collide across vaults in Obsidian's quick switcher.
- **MOC links resolve**: every `[[wikilink]]` in the MOC should point to a file that exists in the vault folder.
- **No append-only patterns**: flag files with multiple dated `## YYYY-MM-DD` section headers (remnants of old pattern). Exempt `[Name] Weekly.md` — it is the one sanctioned append-style spine file, and its `## Week of YYYY-MM-DD` sections are by design.

If `kivna/vault.json` does not exist, report with context:

```
⚠ Vault integration
  ┌──────────────────┬───────────────┬─────────────────────────────┐
  │ Item             │ Current       │ Proposed                    │
  ├──────────────────┼───────────────┼─────────────────────────────┤
  │ vault.json       │ not configured│ run /kerd:kivna scaffold    │
  └──────────────────┴───────────────┴─────────────────────────────┘
  Kerd stores project context, decisions, and activity logs
  in an Obsidian vault. This works as plain markdown files
  even without Obsidian installed, but Obsidian adds graph
  view, search, and cross-project linking.

  To set up: /kerd:kivna scaffold
  It will ask where your vault lives (or create one).
```

If vault needs full setup, the fix is to run the `/kerd:kivna scaffold` mechanic (not to reimplement it here; kivna owns vault operations).

#### Category 4: Deprecated patterns

Detect files/dirs from older Kerd versions:
- `kivna/context.md`: replaced by vault Status.md in v0.10.0 (was vault Context.md in v0.7.0)
- `kivna/checkpoints/`: replaced by vault Status.md in v0.10.0 (was vault Context.md in v0.7.0)
- `kivna/memories/`: replaced by vault in v0.7.0
- `commands/`: removed in v0.7.0, plugin system loads skills directly
- `.sotu`: renamed to `.slainte` in v0.11.0
- `skills/shakh/`: renamed back to `skills/switch/` in v0.14.0
- `skills/seach/`: intermediate name, renamed to `skills/switch/` in v0.14.0

#### Category 5: Naming consistency

Scan committed files (not gitignored) for:
- Mixed case patterns in the same directory (e.g., `Setup.md` alongside `config.md`)
- Inconsistent separators within a directory (kebab-case mixed with snake_case mixed with spaces)
- Detect the project's dominant naming convention per directory and flag outliers

Skip `skills/` (SKILL.md is a Kerd convention), `docs/plans/` (dated prefixes are intentional), and vault-native files.

#### Category 6: Stray & stale files

Scan for:
- Screenshots (`*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.webp`) in repo root or committed dirs
- Temp files (`*.tmp`, `*.log`, `*.bak`, `*.swp`, `*~`)
- `.DS_Store` anywhere in the repo
- Files with no git commits touching them in 60+ days that aren't documentation (`.md`), config (`.json`, `.yaml`, `.toml`, `.slainte`), or gitignore. Use `git log -1 --format=%at -- <file>` to check the most recent commit touching the file.
- Orphaned files not referenced by any other file in the repo (check with grep for the filename across all files). Only check for files in the repo root (subdirectory files are more likely intentional).

#### Category 7: .gitignore hygiene

Check:
- `.gitignore` exists
- Contains entries for: `kivna/input/`, `kivna/output/`, `.DS_Store`
- Untracked files (from `git status`) that suggest a missing ignore rule: group by pattern and suggest rules

#### Category 8: Skill hygiene

Scan all `skills/*/SKILL.md` files and key docs (`CLAUDE.md`, `README.md`, `docs/playbook.md`) for:
- **Missing `kerd:` prefix**: any slash-command reference like `/conductor`, `/switch`, `/skriv` etc. that should be `/kerd:conductor`, `/kerd:switch`, `/kerd:skriv`. Check inside backtick-quoted commands and prose references. Skip README.md (allowed to use shorthand per CLAUDE.md convention).
- **Stale skill names**: references to deprecated skill names (`sotu`, `seach`, `shakh`) in active/instructional context (not CHANGELOG, session logs, or deprecated patterns lists). Each hit is a rename that was missed.
- **Frontmatter drift**: the `name` field in SKILL.md should match its parent directory name. The `description` field should not reference deprecated skill names.

#### Category 9: Hook hygiene

Check whether Kerd hooks are registered in the project's `.claude/settings.local.json`. This is collaborator-local (each developer opts in independently).

Check:
- `.claude/settings.local.json` exists
- It contains hook entries for Kerd's Stop, SessionStart, and PostToolUse events pointing to `${CLAUDE_PLUGIN_ROOT}/hooks/`

If hooks are not registered:

```
⚠ Hook hygiene
  ┌──────────────────┬───────────────┬─────────────────────────────────┐
  │ Item             │ Current       │ Proposed                        │
  ├──────────────────┼───────────────┼─────────────────────────────────┤
  │ Stop hook        │ not registered│ remind about uncommitted changes │
  │ SessionStart     │ not registered│ surface stale state on resume    │
  │ PostToolUse      │ not registered│ mode progress after skill runs   │
  └──────────────────┴───────────────┴─────────────────────────────────┘
  Why: Kerd hooks provide session boundary reminders and mode
       progress tracking. They are read-only and non-blocking.
  Fix: merge hook entries into .claude/settings.local.json
```

When fixing, read existing `.claude/settings.local.json` (create if missing), merge the hook entries from `hooks/hooks.template.json` (relative to the Kerd plugin root) into the settings without overwriting existing hook entries. Preserve any existing permissions or other settings.

**Critical: resolve absolute paths.** `${CLAUDE_PLUGIN_ROOT}` does NOT expand in `settings.local.json`. It only works inside the plugin's own `hooks.json`. When writing hook commands to settings.local.json, resolve the absolute path at wiring time:
- For the installed plugin: find the cache path at `~/.claude/plugins/cache/kerd-marketplace/kerd/<version>/hooks/`
- For local dev (the Kerd repo itself): use the repo path directly (e.g., `/Users/<name>/Kerd/hooks/`)

The hook command must use the resolved absolute path, e.g.: `bash /Users/anthonymaley/.claude/plugins/cache/kerd-marketplace/kerd/0.29.0/hooks/stop.sh`

Note: when the plugin is updated to a new version, the cache path changes. Hooks wired to the old version path will break. Tend should detect this (hook script file doesn't exist at the wired path) and offer to re-wire.

### 4. Display report

Format the report as a visual table. Show passing categories as one-liners. Show failing/warning categories with current vs proposed tables and a "Why" explanation.

**Evidence tracking for failing/warning findings:** the "Why" cell must reference the source of the finding — which check detected it (e.g. "Category 3 vault.json check: missing field `name`" / "Category 6 staleness scan: file not touched in 60+ days per `git log -1 --format=%at -- <path>`" / "Category 9: hook path resolves to nonexistent file at `<path>`"). When proposing fixes in the Proposed column, include the verification step the user can run after the fix lands (e.g. "verify with: `cat kivna/vault.json` shows the `name` field; `git log -1 -- <path>` shows recent activity"). Findings without a source-of-detection are unverifiable; the proposed fix becomes "trust me" rather than reproducible.

```
┌─────────────────────────────────────────────────┐
│  /kerd:tend: [project-name]                      │
└─────────────────────────────────────────────────┘

✓ Directory structure
  kivna/  kivna/sessions/  docs/

✓ Required files
  README.md  CLAUDE.md  CONTEXT.md  TODO.md  docs/playbook.md  .slainte  vault.json

✗ Vault integration
  ┌──────────────────┬───────────────┬─────────────────────────────┐
  │ Item             │ Current       │ Proposed                    │
  ├──────────────────┼───────────────┼─────────────────────────────┤
  │ symlinks         │ 8 found       │ remove all (vault spec      │
  │                  │               │ prohibits repo symlinks)    │
  │ Context.md       │ exists        │ remove (replaced by         │
  │                  │               │ Status.md)                  │
  │ Log.md           │ exists        │ remove (no replacement,     │
  │                  │               │ git log is authoritative)   │
  │ Decisions.md     │ generic name  │ rename to [Project]         │
  │                  │               │ Architecture Decisions.md   │
  └──────────────────┴───────────────┴─────────────────────────────┘
  Why: vault spec requires self-identifying filenames, no symlinks,
       no append-only files. See docs/vault-spec.md.

⚠ Deprecated patterns
  ┌──────────────────┬───────────────┬─────────────────────────────┐
  │ Item             │ Current       │ Proposed                    │
  ├──────────────────┼───────────────┼─────────────────────────────┤
  │ kivna/context.md │ exists        │ remove (replaced by vault   │
  │                  │               │ Status.md)                  │
  │ kivna/checkpoints│ 3 files       │ remove (replaced by vault   │
  │                  │               │ Status.md)                  │
  └──────────────────┴───────────────┴─────────────────────────────┘

⚠ Stray & stale files
  ┌──────────────────┬───────────────┬─────────────────────────────┐
  │ Item             │ Current       │ Proposed                    │
  ├──────────────────┼───────────────┼─────────────────────────────┤
  │ Screenshot*.png  │ 2 files in    │ delete or move to           │
  │                  │ repo root     │ kivna/input/                │
  │ .DS_Store        │ 3 locations   │ add to .gitignore, remove   │
  └──────────────────┴───────────────┴─────────────────────────────┘

✓ Naming consistency
✓ .gitignore hygiene
✓ Skill hygiene

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 4 passing  ·  2 warnings  ·  1 failing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fix all? [yes / pick individually / skip]
```

### 5. Fix flow

**"yes" / "fix all"**: Apply all proposed fixes:
- Create missing directories and files
- Run `/kerd:kivna scaffold` if vault needs setup
- Remove deprecated files (after confirmation for deletions)
- Add missing `.gitignore` entries
- Delete or move stray files as proposed
- Stage all changes

**"pick" / "pick individually"**: Show each `✗`/`⚠` item one at a time. Ask yes/no for each. Apply only approved fixes.

**"skip" / "no"**: Do nothing. The report is the value.

### 6. Summary

After fixes are applied, print what was changed. Do NOT commit. Switch owns git boundary operations.

If this is a brand new repo and all structure was just created, suggest: "Structure ready. Run `/kerd:conductor` to start your first session, or `/kerd:switch out` to commit and push."

## No Commit

Tend does NOT commit or push. It makes structural changes and stops. This keeps switch as the sole owner of git boundary operations (Kerd convention). The user commits via `/kerd:switch out` or manually.

## Notes

- Tend is idempotent. Running it twice produces the same result.
- Tend replaces the old startup skill entirely. It covers both new repo setup and existing repo convergence.
- For vault operations (scaffold, vault setup), tend delegates to `/kerd:kivna scaffold` rather than reimplementing vault logic.
- The vault spec at `docs/vault-spec.md` defines what belongs in the vault. Tend checks structure against this spec.
- Category checks are ordered so that earlier categories don't depend on later ones. Directory structure is checked before required files, vault before deprecated patterns.
- The stale file check (60 days) uses git history, not filesystem mtime. This is intentional: mtime changes when you pull.
