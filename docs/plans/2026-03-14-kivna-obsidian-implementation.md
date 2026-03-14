# Kivna Obsidian Integration — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the Obsidian vault the single source of truth for context, decisions, and activity logging. Kivna becomes the read/write interface to the vault.

**Architecture:** Kivna discovers the vault via `kivna/vault.json` (or convention fallback), reads/writes `[Project] Context.md`, `[Project] Log.md`, and `Decisions.md` in the vault. Repo keeps ephemeral state (TODO.md, sessions, mode markers). Dian and switch update their read/write targets to use the vault through kivna's mechanic.

**Tech Stack:** Pure markdown. No runtime. No dependencies.

---

### Task 1: Create kivna/vault.json for Kerd

Kerd's own vault config. This is the reference example for other projects.

**Files:**
- Create: `kivna/vault.json`

**Step 1: Write the config file**

```json
{
  "vault": "~/ObsidianLLM",
  "folder": "kerd",
  "name": "Kerd"
}
```

**Step 2: Verify**

Read back `kivna/vault.json` and confirm it parses as valid JSON with all three fields.

**Step 3: Commit**

```bash
git add kivna/vault.json
git commit -m "feat: add vault.json for Obsidian integration"
```

---

### Task 2: Rewrite kivna SKILL.md — vault discovery and save mechanic

The biggest change. Rewrite the entire SKILL.md to use the vault as the knowledge layer.

**Files:**
- Modify: `skills/kivna/SKILL.md` (full rewrite)

**Step 1: Write the new SKILL.md**

Replace the entire file. Key sections:

**Intro** — update the one-liner. Kivna owns the project's knowledge layer, stored in the Obsidian vault at `~/ObsidianLLM/[folder]/`.

**Vault Discovery** — new section:
1. Check `kivna/vault.json` — read `vault`, `folder`, `name`
2. Convention fallback — repo dir name → vault folder, title-case for display name
3. No vault found → prompt user to scaffold
4. Expand `~` to home directory in vault path

**Folder Convention** — update to reflect new layout:
- `kivna/vault.json` — vault config (committed)
- `kivna/sessions/` — session logs written by switch (committed, symlinked to vault)
- `kivna/.active-modes` — ephemeral mode state (not committed)
- `kivna/input/` — import inbox (gitignored)
- `kivna/output/` — export outbox (gitignored)
- Remove references to: `kivna/context.md`, `kivna/checkpoints/`, `kivna/memories/`

**`/kivna save` — Save to Vault** — rewrite the mechanic:

1. Discover vault (vault discovery steps above)
2. Prepend new dated section to `[Project] Context.md`:
   ```markdown
   ## YYYY-MM-DD HH:MM

   ### Where We Are
   [current focus]

   ### Active Work
   [specific tasks in progress]

   ### Key Relationships
   [[[people/Name]] wikilinks — only if relevant. Skip section if none.]

   ### Blocked / Waiting
   [skip section if nothing]

   ### Open Questions
   [skip section if none]
   ```
   Insert after the file header (first `---` separator) and before existing sections. The header is the `# [Project] — Context` line and the tagline.

3. Prepend one-liners to `[Project] Log.md`. Insert after the file header and `---` separator, before existing entries. Format: `YYYY-MM-DD — did the thing`

4. Flag decisions — if new decisions were made since last save, show them to user:
   > "New decisions to add to Decisions.md:
   > - **X over Y** — reasoning
   >
   > Add these?"
   User approves → append to `Decisions.md`. User edits or skips → respect that.

5. Confirm — one-line: "Saved to vault: Context updated, N log entries, M decisions flagged."

Note: the save mechanic no longer has a "note" variant. The note concept is replaced by log entries.

**`/kivna in` — Import** — keep existing mechanic. Add: if import surfaces decisions, flag them for Decisions.md approval.

**`/kivna out` — Export** — keep existing mechanic unchanged.

**`/kivna scaffold` — Vault Scaffold** — new command (also triggered automatically when vault not found):

1. Create `~/ObsidianLLM/[folder]/` and subdirectories mirroring repo .md file structure
2. Symlink all `.md` files from repo with `ln -sf`, preserving subfolder structure
3. Create vault-native files:
   - `[Project].md` — MOC linking every symlinked file, grouped by category
   - `[Project] Context.md` — seeded with one section from current state
   - `[Project] Log.md` — seeded from recent git history
   - `Decisions.md` — seeded from CLAUDE.md rules and any decisions in existing context
4. Write `kivna/vault.json`
5. Offer to remove deprecated files (with confirmation): `kivna/context.md`, `kivna/checkpoints/`, `kivna/memories/`
6. Confirm what was created

**Notes section** — update:
- Remove references to checkpoints, memories, context.md
- Add: vault files (`[Project] Context.md`, `[Project] Log.md`, `Decisions.md`) are vault-native, not committed to the repo
- Add: `[Project] Context.md` is append-only — old sections are never deleted
- Add: Decisions.md requires user approval before kivna writes to it
- Keep: import/export notes unchanged

**Step 2: Verify**

Read back the full SKILL.md. Check:
- No references to `kivna/context.md`, `kivna/checkpoints/`, or `kivna/memories/` remain (except in scaffold cleanup step)
- Vault discovery section is present and complete
- Save mechanic writes to three vault files
- Scaffold section covers all vault-native files
- Import still works from `kivna/input/`
- Export still works to `kivna/output/`

**Step 3: Commit**

```bash
git add skills/kivna/SKILL.md
git commit -m "feat: rewrite kivna to use Obsidian vault as knowledge layer"
```

---

### Task 3: Update dian SKILL.md — vault reads and writes

Update dian to read from vault on orient and write through kivna save on execute/close-out.

**Files:**
- Modify: `skills/dian/SKILL.md`

**Step 1: Update Orient (section 1)**

Change item 3 in the orient read list:
- **Was:** `kivna/context.md` — working context from the last checkpoint
- **Now:** Vault `[Project] Context.md` (latest section) — working context from last session. Discover vault path using `kivna/vault.json` or convention. Also read vault `Decisions.md` for project rules and conventions.

Change item 5 in the orient read list:
- **Was:** Decision log — check `docs/project/decisions.md` or `decisions.md`
- **Now:** Vault `Decisions.md` — already read above, remove this as a separate item

Update consistency sniff test text — change "Does context.md mention things" to "Does vault Context mention things".

**Step 2: Update Execute (section 3)**

Change decision recording paragraph:
- **Was:** write to `kivna/context.md` right then
- **Now:** decisions go into the vault Context.md section (via kivna save) AND get flagged for Decisions.md approval

Change auto-save paragraph:
- **Was:** update `kivna/context.md` using the `/kerd:kivna save` mechanic (archive previous version, write new one)
- **Now:** save to the Obsidian vault using the `/kerd:kivna save` mechanic (prepend to vault Context.md, update Log.md, flag decisions)

**Step 3: Update Close Out (section 4)**

Change item 3 (Finalize context):
- **Was:** update `kivna/context.md` with end-of-session state
- **Now:** write close-out section to vault `[Project] Context.md` via `/kerd:kivna save`. Include a "session closed" note in the Where We Are section. Prepend session summary to vault `[Project] Log.md`.

**Step 4: Verify**

Read back the full SKILL.md. Check:
- No references to `kivna/context.md` remain
- Orient reads from vault Context.md and Decisions.md
- Execute auto-save goes through kivna save to vault
- Close-out writes to vault
- TODO.md, playbook, CLAUDE.md references unchanged (still repo)
- Mode markers unchanged (still `kivna/.active-modes` in repo)

**Step 5: Commit**

```bash
git add skills/dian/SKILL.md
git commit -m "feat: update dian to read/write Obsidian vault via kivna"
```

---

### Task 4: Update switch SKILL.md — vault reads and reflection

Update switch to read vault on switch-in and flag decisions on switch-out.

**Files:**
- Modify: `skills/switch/SKILL.md`

**Step 1: Update Switch Out**

Change step 3 (Ensure context is current):
- **Was:** verify `kivna/context.md` is current, or save using kivna save mechanic
- **Now:** verify vault `[Project] Context.md` is current (latest section reflects this session). If not, run `/kerd:kivna save` to write to vault. Discover vault using `kivna/vault.json` or convention.

Change step 5 (Reflect and capture learnings):
- **Was:** write to CLAUDE.md, memory files, playbook
- **Now:** enforcement rules → CLAUDE.md (repo). Conventions and patterns → flag for vault Decisions.md with approval. Project gotchas → playbook (repo). Remove reference to "Claude Code memory files" — the vault replaces that.

**Step 2: Update Switch In**

Change step 4 (Read working context):
- **Was:** read `kivna/context.md`
- **Now:** read vault `[Project] Context.md` (latest section). Discover vault using `kivna/vault.json` or convention. Also read vault `[Project] Log.md` for recent activity at a glance.

Add after step 4, new step 5: Read vault `Decisions.md` for project conventions and rules.

Renumber remaining steps (old 5→6, 6→7, 7→8, 8→9, 9→10).

Update Fallback Behavior — add: if no vault found, fall back to reading `kivna/context.md` if it exists. Mention this gracefully.

**Step 3: Verify**

Read back the full SKILL.md. Check:
- Switch-in reads from vault Context.md, Log.md, Decisions.md
- Switch-out writes through kivna save to vault
- Switch-out reflection flags decisions for vault Decisions.md
- Session logs still go to `kivna/sessions/` in repo
- TODO.md still read/written from repo
- Fallback behavior handles missing vault gracefully

**Step 4: Commit**

```bash
git add skills/switch/SKILL.md
git commit -m "feat: update switch to read/write Obsidian vault via kivna"
```

---

### Task 5: Version bump and description updates

Minor version bump — new feature, changed behavior.

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Bump version to 0.7.0 in all three locations**

- `.claude-plugin/plugin.json` → `"version": "0.7.0"`
- `.claude-plugin/marketplace.json` → `metadata.version`: `"0.7.0"`
- `.claude-plugin/marketplace.json` → `plugins[0].version`: `"0.7.0"`

**Step 2: Update descriptions if needed**

Check if the plugin description needs updating. Current: "Opinionated workflow toolkit — session discipline, machine handoff, knowledge management, project audits, human writing voice, and project scaffolding"

This still works — knowledge management covers the vault integration. No change needed unless the description feels stale.

**Step 3: Update kivna skill trigger description**

In `skills/kivna/SKILL.md` frontmatter, update the description to mention vault/Obsidian:
- **Was:** mentions "importing external files, exporting session context, or saving working context mid-session"
- **Now:** add "Obsidian vault" to the trigger words

**Step 4: Verify**

Read all three version locations and confirm they all say `0.7.0`.

**Step 5: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json skills/kivna/SKILL.md
git commit -m "feat: bump version to 0.7.0 for Obsidian vault integration"
```

---

### Task 6: Update README.md

Update the user-facing docs to reflect the vault integration.

**Files:**
- Modify: `README.md`

**Step 1: Update the kivna section**

Rewrite the kivna description to lead with the vault as the knowledge layer. Update the folder structure diagram to remove `context.md`, `checkpoints/`, `memories/` and add `vault.json`. Update the example commands — remove the note variant of save, add `/kivna scaffold`.

**Step 2: Update "How They Fit Together"**

Update the workflow narrative to mention the vault. Key changes:
- Save writes to vault Context.md instead of kivna/context.md
- Switch-in reads from vault
- Dian orient reads from vault

**Step 3: Verify**

Read back README.md. Check:
- No references to `kivna/context.md`, `kivna/checkpoints/`, or `kivna/memories/` remain
- Vault integration is mentioned in kivna section
- How They Fit Together narrative is consistent

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README for Obsidian vault integration"
```

---

### Task 7: Update playbook and CLAUDE.md

Update project docs to reflect new architecture.

**Files:**
- Modify: `docs/playbook.md`
- Modify: `CLAUDE.md`

**Step 1: Update playbook**

In Architecture section:
- Update directory layout to remove `context.md`, `checkpoints/`, `memories/` and add `vault.json`
- Add a note about the Obsidian vault at `~/ObsidianLLM/[project]/` as the knowledge layer
- Update Current Status to mention v0.7.0 and vault integration

In the six skills list:
- Update kivna description to mention vault

**Step 2: Update CLAUDE.md**

In Project Structure:
- Update the `kivna/` tree to remove `context.md`, `checkpoints/`, `memories/` lines
- Add `kivna/vault.json` line

**Step 3: Verify**

Read back both files. Check consistency with the new architecture.

**Step 4: Commit**

```bash
git add docs/playbook.md CLAUDE.md
git commit -m "docs: update playbook and CLAUDE.md for vault integration"
```

---

### Task 8: Clean up deprecated files from Kerd repo

Remove the files that are now replaced by the vault.

**Files:**
- Delete: `kivna/context.md`
- Delete: `kivna/checkpoints/` (directory and contents)
- Delete: `kivna/memories/` (directory and contents)

**Step 1: Verify vault has the data**

Read `~/ObsidianLLM/kerd/Kerd Context.md` and confirm it has the latest context. Read `~/ObsidianLLM/kerd/Decisions.md` and confirm it has the decisions.

**Step 2: Remove deprecated files**

```bash
git rm kivna/context.md
git rm -r kivna/checkpoints/
git rm -r kivna/memories/
```

**Step 3: Remove stale symlinks from vault**

Remove the symlinks in the vault that pointed to the now-deleted files:
```bash
rm ~/ObsidianLLM/kerd/kivna/context.md
rm -r ~/ObsidianLLM/kerd/kivna/checkpoints/
rm -r ~/ObsidianLLM/kerd/kivna/memories/
```

**Step 4: Commit**

```bash
git add -A kivna/context.md kivna/checkpoints/ kivna/memories/
git commit -m "chore: remove deprecated kivna files replaced by Obsidian vault"
```

---

### Task 9: Final verification

**Step 1: Cross-check all skills for stale references**

Search all SKILL.md files for any remaining references to:
- `kivna/context.md`
- `kivna/checkpoints`
- `kivna/memories`

These should only appear in the scaffold cleanup step of kivna (offering to remove them from OTHER projects that haven't migrated yet).

**Step 2: Cross-check docs**

Search README.md, CLAUDE.md, playbook for same stale references.

**Step 3: Version check**

Confirm all three version locations read `0.7.0`.

**Step 4: Vault consistency**

Confirm `~/ObsidianLLM/kerd/` has:
- `Kerd.md` (MOC)
- `Kerd Context.md` (with sections)
- `Kerd Log.md` (with entries)
- `Decisions.md` (with decisions)
- All repo symlinks still valid

**Step 5: Git status**

Run `git status` and confirm clean working tree (except for the pre-existing command deletions and .DS_Store files which are separate concerns).
