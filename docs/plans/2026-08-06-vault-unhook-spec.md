---
route: new
stage: contracted
---

# Vault-unhook — slice 1 build spec (v0.83.0)

Contract for the vault-unhook slice-1 build: the vault becomes opt-in
everywhere. Authority: `docs/design/vault-unhook.md` (edit map wordings
binding where given); GO record `docs/gates/2026-08-06-vault-unhook-design.md`.
All paths relative to `/Users/anthonymaley/Kerd` (call it `$BASE`).
Subagent cwd resets between calls — every command uses absolute paths.

Fixture-asserted strings — these appear VERBATIM in the files and in
this spec; any paraphrase is a build failure:

- banner line: `vault not written (on-demand since v0.83.0) — /kerd:kivna save for the Obsidian export`
- tend info line: `no vault configured — opt-in via /kerd:kivna scaffold when this project wants a knowledge base`

Proof obligations (encoded as verifies below):

- `grep -c "kivna save" skills/switch/SKILL.md` = **2** exactly
  (terrain: 3 today — modifier-table row, step 4, reflection bullet;
  after build only the reflection re-point and the banner line remain).
- kivna SKILL.md diff = one added sentence, zero removals
  (`git diff --numstat` = `2 0`: the sentence + its blank separator).
- ZERO diff hunks inside `## Switch In (Picking Up a Session)` —
  byte-compared against HEAD; any hunk there is a build refusal.

R3: `skills/**` is in the release sweep's allowlist — every skill
reference written into skill text uses the `/kerd:` prefix. README may
keep its sanctioned shorthand (`/switch`, `/kivna save`).

Out of scope: light/low modifier changes beyond the vault row; the
cycle automation; kivna import/export/scaffold edits; anything in
`~/eolas/vault/`; `.github/workflows/`; capability-list wording; any
edit inside switch's `## Switch In` section.

## Pieces

- [x] Step 1 — skills/switch/SKILL.md: the 11-edit map
- [x] Step 2 — Diff-review switch SKILL.md (blast radius)
- [x] Step 3 — skills/kivna/SKILL.md: one sentence, zero removals
- [x] Step 4 — skills/tend/SKILL.md: opt-in info line + Category 2 drops
- [x] Step 5 — docs/vault-spec.md: Ownership opt-in sentence + rollout note
- [x] Step 6 — README.md: the three named re-wordings
- [x] Step 7 — README.md: consistency sweep + What's New v0.83.0
- [x] Step 8 — Version bump to 0.83.0 (three fields)
- [x] Step 9 — Proof-obligation sweep + collateral check
- [x] Step 10 — Full local suite (six gate.yml lines; stale deferred)
- [x] Step 11 — Work commit (one commit, all boxes checked, trailer)
- [x] Step 12 — Progress refresh, pure render commit, stale check, single push

### Step 1 — skills/switch/SKILL.md: the 11-edit map

`[delegate, model: sonnet, effort: high]` — file:
`/Users/anthonymaley/Kerd/skills/switch/SKILL.md`. Eleven edits, exact
old → new. Touch NOTHING inside the `## Switch In (Picking Up a Session)`
section (it ends at `## Fallback Behavior`) — edit 10 is *after* that
heading, in Fallback Behavior itself.

**(1) Frontmatter description** — two substring swaps inside the one-line
`description:` value:

old: `Owns \`git pull\` and the session-state commit (CONTEXT.md, TODO.md, session log, vault); conductor commits its own work per verified task.`
new: `Owns \`git pull\` and the session-state commit (CONTEXT.md, TODO.md, session log); conductor commits its own work per verified task.`

old: `Supports 'light' modifier to skip vault and reflection, or 'low' modifier for minimum viable handoff on tight token budgets.`
new: `Supports 'light' modifier to skip reflection, or 'low' modifier for minimum viable handoff on tight token budgets.`

**(2) Intro paragraph:**

old: `**Switch owns \`git pull\` and the session-state commit.** Nothing else pulls. The session-state commit is CONTEXT.md, TODO.md, the session log, and vault files — written and committed once, here, at the boundary.`
new: `**Switch owns \`git pull\` and the session-state commit.** Nothing else pulls. The session-state commit is CONTEXT.md, TODO.md, and the session log — written and committed once, here, at the boundary.`

**(3) Usage line:**

old: `` `/kerd:switch out light` wrapping up a session (skip vault, reflection, progress tracking)``
new: `` `/kerd:switch out light` wrapping up a session (skip reflection, progress tracking)``

**(4) Modifier table** — delete this entire row (one line):

`| Vault update | Yes (kivna save, no approval) | Skip | Skip |`

**(5) Under-table note** — full replacement (design wording binding):

old: `The vault is never read at switch-in in any mode — Status.md is write-only from switch's perspective; it exists for the human Obsidian reader and contains nothing CONTEXT.md + the latest log don't.`
new: `The vault is neither read nor written by switch in any mode — it is kivna's, on demand.`

**(6) Delete step 4 "Update the vault"; renumber 5–8 → 4–7.** Delete
this whole block (heading through paragraph, leaving exactly one blank
line between step 3's end and the next heading):

```
### 4. Update the vault

**Skip this step if `light` or `low` modifier is set.**

Call `/kerd:kivna save`. Switch owns the vault save; conductor no longer touches the vault. This updates Status.md and the relevant domain files **directly, without an approval prompt** — report what was written. The vault stays human-first: Status.md is written here but never read at switch-in.
```

Then renumber the remaining Switch Out headings:
`### 5. Update progress tracking` → `### 4. Update progress tracking`
`### 6. Reflect and capture learnings` → `### 5. Reflect and capture learnings`
`### 7. Triage, commit, and push` → `### 6. Triage, commit, and push`
`### 8. Completion banner` → `### 7. Completion banner`

And the one internal cross-reference (in the normal-path paragraph):
old: `Stage session files by name, commit with a descriptive message, and push. No confirmation prompt. Then show the completion banner (step 8).`
new: `Stage session files by name, commit with a descriptive message, and push. No confirmation prompt. Then show the completion banner (step 7).`

WHY delete-and-renumber (not tombstone): living docs describe what is;
git history archives what was — the design's marks table decided this.

**(7) Reflection re-point** (in the now-step-5 learnings list):

old: `- **Conventions and patterns** → flag for the appropriate vault file (Architecture Decisions, Positioning Contract, etc.), written during the \`/kerd:kivna save\` step`
new: `- **Conventions and patterns** → record in CONTEXT.md Key Decisions; a project that keeps a vault updates it on demand via \`/kerd:kivna save\``

**(8) Triage session-files list:**

old: `- **Session files** — files this session created or modified (CONTEXT.md, TODO.md, session log, playbook updates, vault files, etc.). These are auto-committed without asking.`
new: `- **Session files** — files this session created or modified (CONTEXT.md, TODO.md, session log, playbook updates, etc.). These are auto-committed without asking.`

**(9) Completion banner conditional line** — insert a new paragraph
immediately after the closing ``` ``` ``` of the completion-banner
template and before the `If the tree is not clean` paragraph:

`If \`kivna/vault.json\` exists, append one line inside the banner: \`vault not written (on-demand since v0.83.0) — /kerd:kivna save for the Obsidian export\`.`

WHY conditional-on-config and permanent: it is the risk ledger's
third-row countermeasure — the banner names the change; harmless to keep.

**(10) Fallback Behavior** — delete this paragraph (and its trailing
blank line, so one blank line remains between neighbors):

`If no vault is found at switch-out (no \`kivna/vault.json\` and no vault folder at \`~/eolas/vault/[folder]/\`), report this gracefully. Suggest running \`/kerd:kivna scaffold\` to set up the vault.`

WHY: absence is now legitimate, not a gap — no nag toward scaffold.

**(11) Light-mode note** (in the now-step-7 banner section):

old: `If \`light\` modifier was used, note: "Light handoff: vault and reflection skipped."`
new: `If \`light\` modifier was used, note: "Light handoff: reflection skipped."`

**Verify:** `grep -c "kivna save" /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints exactly `2`, and `awk '/^## Switch Out/,/^## Switch In/' /Users/anthonymaley/Kerd/skills/switch/SKILL.md | grep '^### '` prints exactly these 8 lines in order: `### 1. Update CONTEXT.md (state)` / `### 2. Update TODO.md (work)` / `### 2b. Heal and self-migrate` / `### 3. Write session log (history)` / `### 4. Update progress tracking` / `### 5. Reflect and capture learnings` / `### 6. Triage, commit, and push` / `### 7. Completion banner`.

### Step 2 — Diff-review switch SKILL.md (blast radius)

`[keep]` — review `git -C /Users/anthonymaley/Kerd diff skills/switch/SKILL.md`
in full. The review must specifically catch:

1. **ZERO hunks inside `## Switch In`** — run the byte-compare:
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/switch/SKILL.md | sed -n '/^## Switch In (Picking Up a Session)$/,/^## Fallback Behavior$/p') <(sed -n '/^## Switch In (Picking Up a Session)$/,/^## Fallback Behavior$/p' /Users/anthonymaley/Kerd/skills/switch/SKILL.md)`
   — must exit 0 with no output. Any difference is a build refusal:
   revert the file and re-dispatch Step 1.
2. **Step-number cross-references reconciled** — run
   `grep -n 'step [0-9]' /Users/anthonymaley/Kerd/skills/switch/SKILL.md`
   and confirm exactly three hits: `completion banner (step 7)` (Switch
   Out normal path), `(step 2b)` and `step 2` (both inside Switch In —
   they reference unrenumbered steps and must be untouched). Any
   surviving `(step 8)` or dangling `step 4`/`step 5` reference to the
   old numbering is a refusal.
3. No hunk outside the eleven edits: frontmatter description, intro,
   usage line, modifier-table row, under-table note, the step-4 block
   deletion + four heading renumbers + one cross-ref, reflection bullet,
   triage list, banner paragraph insert, fallback paragraph deletion,
   light note. In particular `### 2b`, the session-log templates, and
   the low-mode texts are byte-identical.

**Verify:** the byte-compare in (1) exits 0 with no output, and the grep in (2) prints exactly three lines.

### Step 3 — skills/kivna/SKILL.md: one sentence, zero removals

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/skills/kivna/SKILL.md`. ONE insertion, ZERO
removals. Immediately after the save-command intro paragraph
(`Update the vault to reflect the current session state. Use it at natural breakpoints: after finishing a task, before context gets long, when switching topics, or when something important was decided.`)
and its blank line, before `#### The mechanic`, insert this new
paragraph followed by one blank line:

`Save is deliberate and on-demand — switch no longer calls it at the session boundary as of v0.83.0, so a vault is exactly as fresh as its last save.`

WHY minimal: the design keeps kivna deliberately untouched beyond this
sentence so review meets an unmodified surface; invoking kivna IS the
opt-in.

**Verify:** `git -C /Users/anthonymaley/Kerd diff --numstat -- skills/kivna/SKILL.md` prints exactly `2	0	skills/kivna/SKILL.md`, and `grep -c 'as of v0.83.0' /Users/anthonymaley/Kerd/skills/kivna/SKILL.md` prints `1`.

### Step 4 — skills/tend/SKILL.md: opt-in info line + Category 2 drops

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/skills/tend/SKILL.md`. Four edits. Category
3's present-vault checks (spine, symlinks, banned files, naming, MOC
links, session-history ban, append-only scan) are untouched.

**(a) Category 2 required-files list** — delete the line
`` - `kivna/vault.json` `` from the "Check these files exist:" list
(the list then ends at `` - `.slainte` ``).

**(b) Category 2 template block** — delete this whole block (leaving
one blank line between the `.slainte` template and the "For existing
repos" paragraph):

````
**kivna/vault.json:**
```json
{
  "vault": "~/eolas/vault",
  "folder": "[project-name-lowercase]",
  "name": "[Project Name]"
}
```
````

WHY (consistency edit, beyond the named map): with vault.json out of
the required list, a creation template would still auto-create a vault
config on every brand-new repo — the exact opt-out violation this slice
removes ("every nag toward creating one"). Scaffold remains the one
deliberate creator of vault.json.

**(c) Category 3 missing-vault path** — replace the entire block from
the line `If \`kivna/vault.json\` does not exist, report with context:`
through the closing ``` ``` ``` of its ⚠ report (the block ending
`It will ask where your vault lives (or create one).`) with:

````
If `kivna/vault.json` does not exist, the vault is simply not opted in — this is not a finding. Report one info line, never a ⚠ or ✗ state, and count the category as passing:

```
ℹ Vault integration: no vault configured — opt-in via /kerd:kivna scaffold when this project wants a knowledge base
```
````

The line after the block (`If vault needs full setup, the fix is to run
the \`/kerd:kivna scaffold\` mechanic...`) stays — it is the
present-vault path.

**(d) Display-report example** — in the `✓ Required files` example line,
old: `  README.md  CLAUDE.md  CONTEXT.md  TODO.md  docs/playbook.md  .slainte  vault.json`
new: `  README.md  CLAUDE.md  CONTEXT.md  TODO.md  docs/playbook.md  .slainte`
(consistency: the example must not display a file the check no longer requires).

**Verify:** `grep -c 'no vault configured — opt-in via /kerd:kivna scaffold when this project wants a knowledge base' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `1`; `grep -c 'not configured' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `0`; `grep -c 'vault.json' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `3` (identity inference, Category 3 present-vault check, the new info-path sentence).

### Step 5 — docs/vault-spec.md: Ownership opt-in sentence + rollout note

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/vault-spec.md`. Two edits in the
`## Ownership` section.

**(a)** Insert a new paragraph after the `tend` bullet
(`- **\`tend\`** detects spine drift in existing projects (missing spine file, non-canonical slot name, a \`sessions/\` folder that belongs in the repo) and converges them.`)
and before the italic rollout line:

`The vault is opt-in per project (v0.83.0): a project without a vault is not in violation, and \`tend\` flags drift only where a vault exists. \`/kerd:kivna scaffold\` is the opt-in; \`/kerd:kivna save\` is the only writer, on demand — switch no longer writes the vault at the session boundary.`

**(b)** Rollout note, old:

`*Rollout: complete. \`kivna scaffold\` builds the full spine (MOC + Status + Weekly) and runs the batched intake interview; \`tend\` (Category 3) detects spine drift in existing projects — missing spine file, vault-side session-history folder, non-canonical slot names — and points the fix back at \`kivna scaffold\`.*`

new:

`*Rollout: complete. \`kivna scaffold\` builds the full spine (MOC + Status + Weekly) and runs the batched intake interview; \`tend\` (Category 3) detects spine drift in existing projects — missing spine file, vault-side session-history folder, non-canonical slot names — and points the fix back at \`kivna scaffold\`. Since v0.83.0 the vault is opt-in everywhere: an absent vault is reported by \`tend\` as one info line, never a warning, and the session boundary makes no automatic save.*`

**Verify:** `grep -c 'not in violation' /Users/anthonymaley/Kerd/docs/vault-spec.md` prints `1`, and `grep -c 'Since v0.83.0' /Users/anthonymaley/Kerd/docs/vault-spec.md` prints `1`.

### Step 6 — README.md: the three named re-wordings

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. README shorthand (`/switch`,
`/kivna save`) is sanctioned here — keep it.

**(a) switch section** — two substring swaps:

old: `Switch owns \`git pull\` and the session-state commit — CONTEXT.md, TODO.md, the session log, and vault files, committed once at the boundary.`
new: `Switch owns \`git pull\` and the session-state commit — CONTEXT.md, TODO.md, and the session log, committed once at the boundary.`

old: `reflects on the session (capturing gotchas and learnings, with a check that every gotcha reached the playbook), saves the vault without an approval prompt, then shows a pre-commit summary of what's about to ship.`
new: `reflects on the session (capturing gotchas and learnings, with a check that every gotcha reached the playbook), then shows a pre-commit summary of what's about to ship.`

**(b) kivna section:**

old: `This is the same save mechanic switch uses at the session boundary.`
new: `Save is deliberate and on-demand — switch no longer calls it at the session boundary (v0.83.0); a vault is exactly as fresh as its last save.`

**(c) How They Fit, day-to-day paragraph:**

old: `Then \`/switch out\` updates CONTEXT.md and TODO.md (closing done TODO items against session evidence), writes the session log, calls \`/kivna save\` to update the vault (one clean write, no prompt), commits, and pushes.`
new: `Then \`/switch out\` updates CONTEXT.md and TODO.md (closing done TODO items against session evidence), writes the session log, commits, and pushes. The Obsidian vault refreshes only when you ask — \`/kivna save\`, on demand, whenever you want the export current.`

**Verify:** `grep -c 'same save mechanic' /Users/anthonymaley/Kerd/README.md` prints `0`, `grep -c 'saves the vault' /Users/anthonymaley/Kerd/README.md` prints `0`, and `grep -c 'and vault files, committed once' /Users/anthonymaley/Kerd/README.md` prints `0`.

### Step 7 — README.md: consistency sweep + What's New v0.83.0

`[delegate, model: sonnet, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. This step goes beyond the design's
three named README edits; each item below is a claim that becomes FALSE
at v0.83.0 (release-checklist rule: the README must not describe
behavior that no longer exists). The gate may strike this step whole —
none of the proof obligations depend on it.

**(a) conductor section:**
old: `switch then writes the session log, calls \`/kivna save\` once, and makes the session-state commit — one clean write per session, not ten incremental dumps.`
new: `switch then writes the session log and makes the session-state commit.`

**(b) switch section, light sentence:**
old: `Add \`light\` to skip vault operations, reflection, and smoke tests for a faster handoff with lower token cost.`
new: `Add \`light\` to skip reflection and smoke tests for a faster handoff with lower token cost.`

**(c) switch usage comment:**
old: `/switch out          # full wrap-up (closure inference, vault, reflection, commit, push)`
new: `/switch out          # full wrap-up (closure inference, reflection, commit, push)`

**(d) Quick sessions paragraph:**
old: `\`/switch in light\` skips the smoke test, \`/switch out light\` skips vault saves and reflection.`
new: `\`/switch in light\` skips the smoke test, \`/switch out light\` skips reflection.`

**(e) What's New** — heading `## What's New (v0.82.0)` →
`## What's New (v0.83.0)`. Insert this block immediately before
`### v0.82.0`:

```
### v0.83.0

**The vault becomes opt-in everywhere.** Switch-out no longer writes the Obsidian vault at the session boundary — `/kivna save` is the one writer, invoked on purpose, and a vault is exactly as fresh as its last save. When a vault exists, the switch-out banner says so (vault not written, on-demand). tend stops nagging vault-less projects: an absent vault is a legitimate opt-out, one info line, never a warning. Switch-in is untouched byte-for-byte — same three files, same pickup. Nothing in any existing vault is deleted; the automatic writer stops, the files stay.
```

Then delete the entire `### v0.78.0` block (heading + its paragraph) to
keep five versions, and update the trailing line:
old: `*Release notes for v0.77.0 and earlier live in git history — \`git log --follow README.md\`.*`
new: `*Release notes for v0.78.0 and earlier live in git history — \`git log --follow README.md\`.*`

**Verify:** `grep -c '### v0.83.0' /Users/anthonymaley/Kerd/README.md` prints `1`; `grep -c '### v0.78.0' /Users/anthonymaley/Kerd/README.md` prints `0`; `grep -c 'skips vault saves\|skip vault operations\|calls \`/kivna save\` once' /Users/anthonymaley/Kerd/README.md` prints `0`.

### Step 8 — Version bump to 0.83.0 (three fields)

`[delegate, model: haiku, effort: low]` — replace `"version": "0.82.0"`
with `"version": "0.83.0"` in:

- `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (one occurrence)
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (BOTH
  occurrences: `metadata.version` and `plugins[0].version`)

Both `description` fields untouched — capability lists stay
byte-identical ("knowledge management" remains true, on demand).
MINOR bump: changed behavior.

**Verify:** `grep -c '"version": "0.83.0"' /Users/anthonymaley/Kerd/.claude-plugin/plugin.json` prints `1` and `grep -c '"version": "0.83.0"' /Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` prints `2`.

### Step 9 — Proof-obligation sweep + collateral check

`[keep]` — run all three proof obligations on the final tree, then the
collateral check. All from `$BASE`:

1. `grep -c "kivna save" /Users/anthonymaley/Kerd/skills/switch/SKILL.md` → exactly `2`.
2. `git -C /Users/anthonymaley/Kerd diff --numstat -- skills/kivna/SKILL.md` → exactly `2	0	skills/kivna/SKILL.md`.
3. The Switch In byte-compare from Step 2 (same command) → exit 0, no output.
4. Collateral: `git -C /Users/anthonymaley/Kerd status --porcelain` lists EXACTLY these eight paths and nothing else:

```
 M .claude-plugin/marketplace.json
 M .claude-plugin/plugin.json
 M README.md
 M docs/vault-spec.md
 M skills/kivna/SKILL.md
 M skills/switch/SKILL.md
 M skills/tend/SKILL.md
?? docs/plans/2026-08-06-vault-unhook-spec.md
```

Any extra path is unintended drift — a refusal, back to the offending
step.

**Verify:** all four checks pass exactly as stated above.

### Step 10 — Full local suite (six gate.yml lines; stale deferred)

`[keep]` — run the seven `run:` lines from
`/Users/anthonymaley/Kerd/.github/workflows/gate.yml` locally from
`$BASE`, EXCEPT `python3 tools/diagram/progress.py stale` — stale's
natural green moment is after Step 12's render commit; it runs there.
The six, in gate.yml order, with expected results:

1. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest` → exit 0, `selftest: 24 cases passed`
2. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` → exit 0, `audit: clean`
3. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py release` → exit 0, `release: clean` (this is R1–R3: three synced version fields, byte-identical capability lists, no bare skill references in the allowlist sweep)
4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py selftest` → exit 0
5. `python3 /Users/anthonymaley/Kerd/tools/design/matrix.py selftest` → exit 0
6. `python3 /Users/anthonymaley/Kerd/tools/design/matrix.py audit` → exit 0

**Verify:** all six exit 0 with the named outputs where stated.

### Step 11 — Work commit (one commit, all boxes checked, trailer)

`[keep]` — in order:

1. Set ALL twelve Pieces boxes in THIS spec to `[x]`. The ship-step
   boxes (11, 12) are pre-checked in the work commit deliberately: the
   progress board derives from contract checklists, so any later
   box-check would change the board after its render — the stale-gate
   burn from the rigor-level build. The render commit must find the
   spec already final.
2. Stage by name exactly:
   `.claude-plugin/marketplace.json` `.claude-plugin/plugin.json`
   `README.md` `docs/vault-spec.md` `skills/kivna/SKILL.md`
   `skills/switch/SKILL.md` `skills/tend/SKILL.md`
   `docs/plans/2026-08-06-vault-unhook-spec.md`
3. ONE commit, message:

```
vault-unhook slice 1: the vault becomes opt-in everywhere — boundary write removed, /kerd:kivna save on demand (v0.83.0)

Claude-Session: https://claude.ai/code/session_01B7yNRTL9d6oJJQcpLVMaSq
```

Do NOT push — the push is Step 12's, single, after the render commit.

**Verify:** `git -C /Users/anthonymaley/Kerd show --stat HEAD` lists exactly the eight files above; `git -C /Users/anthonymaley/Kerd log -1 --format=%B` ends with the `Claude-Session:` trailer; `grep -c '\- \[x\]' /Users/anthonymaley/Kerd/docs/plans/2026-08-06-vault-unhook-spec.md` prints `12`.

### Step 12 — Progress refresh, pure render commit, stale check, single push

`[keep]` — in order:

1. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py` (the refresh).
2. `git -C /Users/anthonymaley/Kerd status --porcelain` — must list ONLY
   progress-render outputs (the board's Excalidraw/SVG/HTML trio). Any
   other path — the spec included — is a refusal: a render commit that
   changes anything else moves the page it just rendered and the stale
   gate fires. Stop and return to the orchestrator.
3. `git -C /Users/anthonymaley/Kerd add -A` then
   `git -C /Users/anthonymaley/Kerd commit -m "Refresh progress render"`
   — NO trailer, render files only. If the refresh produced no changes,
   skip this commit.
4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py stale` → exit 0.
5. `git -C /Users/anthonymaley/Kerd push` — ONE push carrying both commits.

**Verify:** `git -C /Users/anthonymaley/Kerd status --porcelain` prints nothing; `git -C /Users/anthonymaley/Kerd rev-list origin/main..HEAD --count` prints `0`; `git -C /Users/anthonymaley/Kerd log -2 --format=%s` shows `Refresh progress render` above the work-commit subject (or only the work commit if step 3 was skipped).
