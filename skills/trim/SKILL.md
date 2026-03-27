---
name: trim
description: "Use when the user says 'trim', '/trim', 'token trim', or 'feature complete cleanup'. Archives completed feature docs, prunes stale CLAUDE.md content, cleans stale memory entries, and trims completed TODO items. Run this after every feature is shipped."
---

# Trim (Token Optimization — Light Pass)

A quick cleanup to run after each feature ships. Keeps active context lean without touching anything you still need.

## Steps

Work through each step in order. Confirm with the user before removing anything.

### 1. Archive completed feature docs

Scan for spec, plan, and design docs in these locations:
- `docs/` — files with "spec", "plan", or "design" in the filename, and anything under `docs/plans/`
- Project root — same naming patterns

**Archive criteria:** A doc is archivable if its feature is merged to main AND documented as complete in `docs/playbook.md` Current Status section. Do not archive docs for work-in-progress features or features awaiting code review.

For each archivable doc, **before moving it**, run the forward-looking content rescue (see step 1a below). Then:
- Create `docs/archive/` if it doesn't exist
- Move it to `docs/archive/`
- Skip anything still referenced in active backlog items in `TODO.md`

### 1a. Rescue forward-looking content

Before archiving any doc, scan it for content that is still relevant to the project's future even though the feature is complete. This includes:

- **Deferred tasks** — items explicitly marked as deferred, out-of-scope, or "later"
- **Future phase notes** — design decisions, constraints, or options noted for an upcoming phase
- **Known limitations** — documented gaps or tradeoffs that future work will need to address
- **Pending architectural decisions** — open questions or to-be-decided items
- **Cross-cutting concerns** — notes that will affect future features (e.g. "when we add X, remember Y")

For each piece of rescued content:
1. Append it to `docs/deferred.md` under a heading matching the source doc's feature name:
   ```
   ## <Feature Name> (from <source-doc-filename>)
   <rescued content, preserved verbatim or lightly summarized>
   ```
   Create `docs/deferred.md` with this header if it doesn't exist:
   ```
   # Deferred & Future Context

   Forward-looking notes rescued during trim passes. Check this file when starting
   new features — items here may affect design or unblock work.
   ```
2. Do **not** archive the doc until the rescue is complete.
3. If `docs/deferred.md` does not already appear in `CLAUDE.md`, append this line to the bottom of `CLAUDE.md` (under a `## Living Docs` section, creating it if needed):
   ```
   See `docs/deferred.md` for deferred tasks and forward-looking context from past features.
   ```

Present rescued items to the user before writing them, so they can discard anything that is truly dead.

### 2. Update archive index

After archiving, append a line to `docs/archive/INDEX.md` for each archived doc:
```
- <feature-name>: <relative path>
```
Create the file if it doesn't exist, with this header:
```
# Archive Index
```

### 3. Prune CLAUDE.md

Scan `CLAUDE.md` for feature-specific guidance blocks — instructions that described how to handle a feature that is now permanently in the codebase and no longer needs a reminder. Present each candidate to the user and remove only with their confirmation.

Do not remove:
- Design constraints
- Code conventions
- Doc impact table
- Token efficiency rules
- Session workflow

### 4. Clean memory files

Scan the project's `memory/` directory (typically at `~/.claude/projects/<project-id>/memory/`) for `project_*.md` entries. For each one, check whether the stated purpose is still relevant. Flag entries where:
- The feature described has shipped and the entry is no longer actionable
- A decision described has been reversed or superseded

Present each candidate to the user. Remove only with their confirmation. Never remove `feedback_*.md` or `user_*.md` entries — those are permanent.

### 5. Trim TODO.md

Review `TODO.md`. Present checked-off items under completed session headers to the user and confirm they are safe to remove. Do not touch:
- Backlog items (checked or unchecked)
- Items in the current or next session

### 6. Safety gate

Dispatch a subagent (haiku model) with the following task:

> Read the current state of CLAUDE.md, the memory MEMORY.md index, TODO.md, docs/archive/INDEX.md, docs/deferred.md (if present), and docs/. Verify that /kerd:switch in would still have all context needed: project state, active feature, session notes, key decisions, architecture constraints. Check that any deferred/future-phase content from archived docs appears in docs/deferred.md and that CLAUDE.md references it. Also scan vault session logs from the last 3 months for any inline references to docs that were just archived — flag any that now point to archived locations. Report: CONTEXT INTACT or GAPS FOUND with specifics.

If the subagent reports GAPS FOUND, surface the issues to the user before finalizing any changes. Do not commit until the user confirms.

## After trim

Report a concise summary:
- N docs archived → listed by feature name
- N forward-looking items rescued → written to `docs/deferred.md`
- N CLAUDE.md blocks removed
- N memory entries removed
- N TODO items removed
- Safety gate result
