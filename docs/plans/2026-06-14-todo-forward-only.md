# TODO-is-forward-only Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `TODO.md` forward-only — `switch` overwrites the Current Session block, self-heals accumulated `## Previous Session` blocks into `kivna/sessions/`, and the state contract names the demote-and-keep anti-pattern.

**Architecture:** Prose-only changes to three Kerd skill/contract files plus release housekeeping. The fix is a *mechanism* (switch self-heal) backing a *rule* (forward-only), because the rule alone already existed in `state-contract.md` and the model drifted anyway. No code, no new artifacts — `kivna/sessions/` is already the archive.

**Tech Stack:** Markdown skill definitions. No build, no test runner in this repo — verification is `grep`/read-back assertions and a fixture simulation where a fresh agent executes the new switch prose against a synthetic bloated TODO.

**Spec:** `docs/plans/2026-06-14-todo-forward-only-design.md`

**Working location:** `main` working tree. NOT a worktree — the tree already holds uncommitted v0.40.0 work that must land first (Task 1). Do not create a worktree.

**Commit strategy (Kerd convention overrides "frequent commits"):** Kerd requires the release checklist (version bump ×3 + README + descriptions) *before* any skill-change commit, so v0.41.0 edits land as ONE release-checklisted commit (Task 8), not per-task. Task 1 is a separate prerequisite commit for the pending v0.40.0 work.

---

### Task 1: Land the pending v0.40.0 work (prerequisite)

The working tree holds the aborted 2026-06-10 switch-out (v0.40.0). It must land as its own commit so v0.41.0 is clean. **This pushes to origin — confirm with the user before running step 3.**

**Files:**
- Stage by name (v0.40.0 only): `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `README.md`, `TODO.md`, `docs/state-contract.md`, `modes/deepwork.md`, `skills/dian/SKILL.md`, `skills/slainte/SKILL.md`, `skills/switch/SKILL.md`, `kivna/sessions/2026-06-10.md`
- **Exclude:** `docs/plans/2026-06-14-todo-forward-only-design.md` and `docs/plans/2026-06-14-todo-forward-only.md` (those are v0.41.0).

- [ ] **Step 1: Confirm the tree matches expectation**

Run: `git status --short`
Expected: the 9 modified files above + untracked `kivna/sessions/2026-06-10.md` + the two untracked `docs/plans/2026-06-14-todo-forward-only*.md`. Nothing else.

- [ ] **Step 2: Stage v0.40.0 files by name (NOT the 2026-06-14 docs)**

```bash
git add .claude-plugin/marketplace.json .claude-plugin/plugin.json README.md TODO.md \
  docs/state-contract.md modes/deepwork.md skills/dian/SKILL.md skills/slainte/SKILL.md \
  skills/switch/SKILL.md kivna/sessions/2026-06-10.md
git status --short
```
Expected: the 10 files staged (`M`/`A`), the two `docs/plans/2026-06-14-*` still untracked (`??`).

- [ ] **Step 3: Commit and push (after user confirmation)**

```bash
git commit -m "feat(switch,dian): session-first reframe + dian slim (v0.40.0)"
git push origin main
```
Expected: commit created, push succeeds. Run `git log --oneline -1` to confirm the hash.

---

### Task 2: Codify forward-only in the state contract

**Files:**
- Modify: `docs/state-contract.md` (the `### Rules` block under the TODO.md section, ~line 32-37)

- [ ] **Step 1: Replace the Rules list**

Find:
```markdown
### Rules

- `## Current Session` is overwritten each session by dian (plan phase) or switch (out)
- `### Context` within Current Session holds the mode snapshot for cross-machine handoff
- `## Backlog` is append-only (items added, never silently removed). Checked-off items can be cleaned by trim.
- dian writes the plan, switch writes the wrap-up. They don't conflict because dian runs within a session and switch runs at the boundary.
```

Replace with:
```markdown
### Rules

- **TODO.md is forward-only.** It contains only `## Current Session` (forward-looking state) and `## Backlog`. The record of completed work is its `kivna/sessions/<date>.md` log — never a retained TODO entry.
- `## Current Session` is **overwritten in place** each session by dian (plan phase) or switch (out): replaced with forward-looking state (in-progress, what's next, open decisions), never the prior session's content.
- **Anti-pattern — demote-and-keep.** Renaming `## Current Session` → `## Previous Session` (or `## Older Session`) and keeping it is forbidden. Such blocks must not exist in TODO.md; `switch out` heals any that appear by archiving them to `kivna/sessions/`.
- `### Context` within Current Session holds the mode snapshot for cross-machine handoff
- `## Backlog` is append-only (items added, never silently removed). Checked-off items can be cleaned by trim.
- dian writes the plan, switch writes the wrap-up. They don't conflict because dian runs within a session and switch runs at the boundary.
```

- [ ] **Step 2: Verify**

Run: `grep -n "forward-only\|demote-and-keep" docs/state-contract.md`
Expected: at least the two new bullets match.

---

### Task 3: Make `switch` out overwrite (prevention)

**Files:**
- Modify: `skills/switch/SKILL.md` step 1 (~lines 53-57)

- [ ] **Step 1: Replace the step-1 body (overwrite + forward-only)**

Find:
```markdown
Create TODO.md if it doesn't exist. Update the `## Current Session` block.

**Full/light:** Include what was done (check off completed items), what's in progress, what's next, and any context that would be lost (decisions, things tried, open questions).

**Low:** Keep it to 3-5 lines max. One line per: what was done, what's next, any critical context. Skip detailed item-by-item checkoffs.
```

Replace with:
```markdown
Create TODO.md if it doesn't exist. **Overwrite** the `## Current Session` block — replace it in place with the current forward-looking state. `TODO.md` is forward-only: it holds what still needs doing, not a record of what's done. Never rename the block to `## Previous Session` to keep history — the completed record is written to the session log in step 2.

**Full/light:** Write what's in progress, what's next, and any unresolved context that would be lost (open decisions, things tried, open questions). Do **not** keep a list of completed items in the block — those belong in the session log. The Current Session block describes the project's forward state, not this session's diary.

**Low:** Keep it to 3-5 lines max, forward-only: what's next plus any critical open context. Skip the done-items list — the session log holds it.
```

- [ ] **Step 2: Verify the old wording is gone**

Run: `grep -n "Update the \`## Current Session\`" skills/switch/SKILL.md`
Expected: no matches (the "Update" wording is replaced by "Overwrite").
Run: `grep -n "Overwrite\*\* the \`## Current Session\`\|forward-only" skills/switch/SKILL.md`
Expected: matches in step 1.

---

### Task 4: Add the `switch` out self-heal step (1b)

**Files:**
- Modify: `skills/switch/SKILL.md` — insert a new `### 1b.` section between the step-1 "Mode snapshot" code block and `### 2. Write session log` (~before line 68)

- [ ] **Step 1: Insert step 1b**

Insert this block immediately before the line `### 2. Write session log`:
```markdown
### 1b. Heal accumulated history

`TODO.md` is forward-only, so it must contain no `## Previous Session` or `## Older Session` blocks. Scan for them (drift from before this rule, or a slip). For each block found:

1. Read its date/identifier from the heading; trust any explicit `kivna/sessions/<date>.md` reference inside the block.
2. If `kivna/sessions/<date>.md` already exists for that date → the block is already archived; remove it from `TODO.md`.
3. If no log exists for that date → **rescue first**: create `kivna/sessions/<date>.md` from the block's content (or append under a `---` separator if a same-day file already exists), then remove the block.
4. Never delete a block when no session log for its date exists — rescue is mandatory before removal.

Report: "Healed TODO: N session block(s) archived (M rescued)." If none exist, skip silently. This runs in all modes (full/light/low) — it is cheap and is the backstop that prevents unbounded TODO growth.

```

- [ ] **Step 2: Verify placement and ordering**

Run: `grep -n "^### " skills/switch/SKILL.md | head -12`
Expected: `### 1. Write session state to TODO.md`, then `### 1b. Heal accumulated history`, then `### 2. Write session log` in that order.

---

### Task 5: Sync `dian` close-out wording

**Files:**
- Modify: `skills/dian/SKILL.md` close-out step 1 (~line 155)

- [ ] **Step 1: Replace "clear the block" with "overwrite, never demote-and-keep"**

Find:
```markdown
1. **Update TODO.md**: check off completed tasks, add new ones discovered during work, record any decisions in the `### Context` section, clear the `## Current Session` block. Apply Claim Discipline to summary text — don't claim "we verified X" unless we did; downgrade to "tested with Y; Z untried" when alternates exist; don't promote provisional findings to canonical without the survival test.
```

Replace with:
```markdown
1. **Update TODO.md**: check off completed tasks, add new ones discovered during work, record any *unresolved* decisions in the `### Context` section, then overwrite the `## Current Session` block to forward-only state (what's next + open context). Never demote-and-keep it as a `## Previous Session` block — the completed record is the session log switch writes at the boundary. Apply Claim Discipline to summary text — don't claim "we verified X" unless we did; downgrade to "tested with Y; Z untried" when alternates exist; don't promote provisional findings to canonical without the survival test.
```

- [ ] **Step 2: Verify**

Run: `grep -n "demote-and-keep\|forward-only state" skills/dian/SKILL.md`
Expected: one match in close-out step 1.

---

### Task 6: Release housekeeping (version, README, descriptions)

**Files:**
- Modify: `.claude-plugin/plugin.json` (`version`), `.claude-plugin/marketplace.json` (`metadata.version` and `plugins[0].version`)
- Modify: `README.md` (switch section)

- [ ] **Step 1: Bump version 0.40.0 → 0.41.0 in all three locations**

Edit each:
- `.claude-plugin/plugin.json`: `"version": "0.40.0"` → `"version": "0.41.0"`
- `.claude-plugin/marketplace.json` `metadata.version`: `"version": "0.40.0"` → `"version": "0.41.0"`
- `.claude-plugin/marketplace.json` `plugins[0].version`: `"version": "0.40.0"` → `"version": "0.41.0"`

- [ ] **Step 2: Verify all three are 0.41.0**

Run: `grep -rn '"version"' .claude-plugin/`
Expected: exactly three `0.41.0` lines (plugin.json ×1, marketplace.json ×2). No `0.40.0` remaining.

- [ ] **Step 3: Update README switch section**

Run: `grep -n -i "switch" README.md` to locate the switch subsection. Read that subsection. Add one sentence stating TODO is forward-only and switch self-heals accumulated history. Exact sentence to insert at the end of the switch description paragraph:

```markdown
Switch keeps `TODO.md` forward-only: at switch-out it overwrites the Current Session block (completed work lives in the dated `kivna/sessions/` log, not TODO) and self-heals any accumulated `## Previous Session` blocks by archiving them to the session logs.
```

- [ ] **Step 4: Confirm capability-list / trigger descriptions**

Triggering conditions for switch are unchanged (same invocation phrases), so the SKILL.md frontmatter `description` and the byte-identical capability lists in `plugin.json`/`marketplace.json` need **no** change. Confirm by reading the switch frontmatter `description` — if it already covers session/handoff, leave it. Note in the commit body that triggers were reviewed and unchanged.

Run: `grep -n "description" skills/switch/SKILL.md | head -1` and read it; confirm no edit needed.

---

### Task 7: Verify the self-heal behavior on a fixture

This is the core behavioral test: a fresh agent executing the *new* switch step 1b prose must heal a bloated TODO correctly — the exact failure mode (prose misread) we're fixing.

**Files:**
- Create (temp, outside repo): `/tmp/heal-fixture/TODO.md`, `/tmp/heal-fixture/kivna/sessions/2026-06-12.md`

- [ ] **Step 1: Build the fixture**

```bash
mkdir -p /tmp/heal-fixture/kivna/sessions
cat > /tmp/heal-fixture/TODO.md <<'EOF'
# TODO

## Current Session — 2026-06-14
- [ ] next: ship the thing

## Previous Session — 2026-06-12 (log EXISTS)
- [x] did A
- [x] did B

## Previous Session — 2026-06-11 (log MISSING — must be rescued)
- [x] did C

## Backlog
- [ ] someday item
EOF
printf '# Session 2026-06-12\n\n## What Was Done\n- did A, did B\n' > /tmp/heal-fixture/kivna/sessions/2026-06-12.md
```

- [ ] **Step 2: Dispatch a subagent to execute step 1b against the fixture**

Use the Task/Agent tool (general-purpose). Prompt: "Read `skills/switch/SKILL.md` step `### 1b. Heal accumulated history` from this repo. Apply EXACTLY those instructions to the TODO at `/tmp/heal-fixture/TODO.md`, treating `/tmp/heal-fixture/` as the project root (session logs at `/tmp/heal-fixture/kivna/sessions/`). Make the edits. Report what you did."

- [ ] **Step 3: Verify the result**

```bash
echo "=== TODO must have NO Previous Session blocks ==="; grep -c "## Previous Session" /tmp/heal-fixture/TODO.md
echo "=== Current Session + Backlog must survive ==="; grep -c "## Current Session\|## Backlog" /tmp/heal-fixture/TODO.md
echo "=== 2026-06-11 must have been rescued ==="; cat /tmp/heal-fixture/kivna/sessions/2026-06-11.md
echo "=== 2026-06-12 log untouched-or-intact ==="; cat /tmp/heal-fixture/kivna/sessions/2026-06-12.md
```
Expected: first count `0`; second count `2`; the 2026-06-11 log exists and contains "did C"; the 2026-06-12 log still contains "did A, did B".

- [ ] **Step 4: Clean up the fixture**

```bash
rm -rf /tmp/heal-fixture
```

If Step 3 fails, the step-1b prose is ambiguous — revise Task 4's wording and re-run Task 7 before proceeding.

---

### Task 8: Self-review, then the single v0.41.0 commit

**Files:**
- Stage: `docs/state-contract.md`, `skills/switch/SKILL.md`, `skills/dian/SKILL.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`, `docs/plans/2026-06-14-todo-forward-only-design.md`, `docs/plans/2026-06-14-todo-forward-only.md`

- [ ] **Step 1: Final consistency sweep**

```bash
echo "=== no stale 0.40.0 ==="; grep -rn "0.40.0" .claude-plugin/ || echo OK
echo "=== forward-only present in all three ==="; grep -ln "forward-only" docs/state-contract.md skills/switch/SKILL.md
echo "=== no lingering 'Update the ## Current Session' ==="; grep -rn "Update the \`## Current Session\`" skills/ || echo OK
echo "=== switch step order ==="; grep -n "^### 1\b\|^### 1b\|^### 2\b" skills/switch/SKILL.md
```
Expected: no 0.40.0 in manifests; forward-only in both contract and switch; no lingering "Update the Current Session"; step order 1 → 1b → 2.

- [ ] **Step 2: Confirm the tree (v0.40.0 already committed in Task 1)**

Run: `git status --short`
Expected: only the eight files listed above are modified/untracked. If `TODO.md` or other v0.40.0 files reappear, Task 1 was incomplete — stop and resolve.

- [ ] **Step 3: Stage and commit v0.41.0**

```bash
git add docs/state-contract.md skills/switch/SKILL.md skills/dian/SKILL.md \
  .claude-plugin/plugin.json .claude-plugin/marketplace.json README.md \
  docs/plans/2026-06-14-todo-forward-only-design.md docs/plans/2026-06-14-todo-forward-only.md
git commit -m "feat(switch,dian): TODO is forward-only + self-heal accumulated history (v0.41.0)

switch overwrites the Current Session block and heals stray ## Previous Session
blocks into kivna/sessions/; state-contract names the demote-and-keep anti-pattern;
dian close-out wording synced. Fixes unbounded TODO growth (a user hit 378kb).
Triggers reviewed, unchanged."
```

- [ ] **Step 4: Push**

```bash
git push origin main
git log --oneline -2
```
Expected: push succeeds; log shows the v0.41.0 commit on top of the v0.40.0 commit.

---

## Self-Review (plan vs. spec)

**Spec coverage:**
- Contract forward-only + anti-pattern → Task 2 ✓
- switch prevention (overwrite) → Task 3 ✓
- switch self-heal step 1b w/ rescue gate + report → Task 4 ✓; behavior tested → Task 7 ✓
- dian wording sync → Task 5 ✓
- switch-in unchanged → no task (correct; spec marked it optional/no-change) ✓
- trim unchanged → no task (correct) ✓
- Release: v0.41.0 ×3, README, descriptions/triggers → Task 6 ✓
- Sequencing after v0.40.0 → Task 1 + Task 8 ✓
- Acceptance criterion 6 (378kb-style file heals to Current+Backlog) → Task 7 fixture ✓

**Placeholder scan:** every edit shows exact find/replace text; README step provides the exact sentence; no TBD/"handle edge cases". ✓

**Type/name consistency:** "forward-only", "demote-and-keep", "`## Previous Session`/`## Older Session`", "step 1b", "Healed TODO: N…" are used identically across contract, switch, dian, and the verification greps. ✓
