---
route: new
stage: contracted
---

# The mode cut — spec

Kerd's third rip, the last graveyard verdict. `skills/mode/` and all eleven `modes/` files are deleted whole. Evidence licensed the cut: never used in five months; the routing job died with the entry gates (`gate.py route` routes by construction — the menus never got to); its phase menus violate the talk rules; its step tracker is self-reported position, which progress-derives-from-disk forbids. `spike.md`'s unique method content — empirical-primitive-first, the provisional-loss survival gate, commit graduation, the self-audit baseline — goes to git history at this cut's commit. **No relocation of any mode content anywhere.**

**Return condition** (recorded in the What's New entry): the first real spike run that wants method guidance brings spike.md's content back. The spike ROUTE stays alive in the gate vocabulary (`route: spike` is the one licensed ladder bypass).

Version: 0.74.0 → **0.75.0** (MINOR — the v0.73.0 and v0.74.0 cut precedents).

**Composer amendment governs every rewritten passage**: a wrong line does not survive; the no-touch protection is for correct content only. Every replacement below is exact text, validated against disk at spec-writing time. If a step's verify does not produce its expected output, or an old string does not match the file, the player STOPS and hands back to the orchestrator. No improvisation.

## The two Elevens — distinct counts, never merged

"Eleven" appears in two different counts. They move independently:

1. **Skills count** — `skills/` holds 11 directories today (conductor, interrogate, kivna, lorg, mode, pair, skriv, slainte, switch, tend, trim); after this cut, 10. README line 5 ("Eleven workflow skills"), CLAUDE.md line 3 ("eleven workflow skills"), and the playbook line 61 ("Eleven skills") all go **Ten**. AGENTS.md says "eight" — never right; it is replaced wholesale by the agreed identity line (step 4).
2. **Starter-modes count** — README line 304 ("Eleven starter modes") counts `modes/*.md` files. It dies with the section it lives in. It is never edited to "Ten".

Applying the skills edit mechanically to line 304, or vice versa, is the failure this section exists to prevent.

## Surface

The diff may touch ONLY these files (plus this spec file itself):

- `skills/mode/SKILL.md` (deleted — the directory's only file)
- `modes/deepwork.md`, `modes/greenfield.md`, `modes/jit.md`, `modes/legal.md`, `modes/maintain.md`, `modes/quickfix.md`, `modes/research.md`, `modes/sales.md`, `modes/spike.md`, `modes/strategy.md`, `modes/writing.md` (all deleted)
- `scripts/demo-mode.sh` (deleted — step 9 hand-back ruling: an asciinema recording cheat-sheet whose entire subject is the dead skill; its steps say run `/kerd:mode strategy` and walk the phase menus, which can never happen again; the `docs/demo-mode.cast` it records to was never committed. A living helper, not a record — its subject died, it dies, content archived in git history at this commit. The `scripts/` directory held only this file and disappears with it.)
- `hooks/skill-complete.sh` (one comment line — step 9 hand-back ruling; behavior untouched)
- `README.md`
- `CONTRIBUTING.md`
- `CLAUDE.md`
- `AGENTS.md` (GITIGNORED — `.gitignore` line 7; the edit is machine-local by declaration and is never staged or shipped)
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `skills/slainte/SKILL.md`
- `skills/switch/SKILL.md` (two lines — a template comment and an illustrative example that name the dead skill)
- `docs/playbook.md`
- `docs/state-contract.md`

**Deliberately not touched — each is a decision, not an oversight:**

- **`skills/kivna/SKILL.md` and README line 229** (`/kivna out --full` … "adds playbook, architecture, memory, mode"): kivna's `mode` export section reads `kivna/.active-modes` — the pair/conductor state concept, NOT the mode skill. Both stay exactly as they are. A player or reviewer who "fixes" them has broken this spec.
- **The `.active-modes` machinery**: `hooks/stop.sh`, `hooks/session-start.sh`, `hooks/skill-completion.sh`, `tests/hooks_test.sh`, conductor's mode-awareness sections (`skills/conductor/SKILL.md` orient/plan/close-out), switch's Mode-snapshot step (line 90) and section 9 (active-modes check/restore, including its `greenfield (step 4 of 9)` legacy-state illustration), the playbook's `kivna/.active-modes` layout line (55) and hook descriptions (74–78), README's hook descriptions ("active mode", "interrupted mode", "When a mode is active"). Conductor/switch/pair use this file; readers that tolerate or report leftover state stay. Only the dead skill's WRITER-side references go.
- **The pair skill**: "Partner Mode" naming stays throughout.
- **R3 allowlist glob**: `tools/gates/kit.py` line 661 docstring and `tools/gates/README.md` line 169 mention `modes/**` in the R3 allowlist. A glob over a deleted directory matches nothing — CI unaffected — and the allowlist mirrors the gate spec in dated `docs/gates/` records, which are never edited. Editing the mirror alone would create spec drift. Both stay.
- **`CHANGELOG.md`**: abandoned at 0.14.0, not part of the release flow. No entry.
- **`docs/lorg-report.md`**: generated point-in-time scan output; regenerated on next lorg run.
- **README line 166** (conductor "mode-aware" paragraph): describes conductor's surviving `.active-modes` awareness — machinery, untouched.
- **Playbook line 172** (`**Version:** 0.60.0`), line 185 ("Mode markers on conductor and skriv" — the phase-marker concept), and the Recent-changes history block (197–226): stale-version drift is pre-existing and a separate decision; phase markers are a different "mode"; history is a record.
- **AGENTS.md's remaining drift** (Codex-era release checklist, `.Codex-plugin` paths, `/kerd:dian`): pre-existing, flagged to the composer, not this cut's to fix. Only the identity line and the structure block's modes/ line change. **AGENTS.md is gitignored** (`.gitignore` line 7): the edit keeps the local Codex fork in agreement on this machine, ships nothing, never appears in `git status`, and must never be `git add`ed (git refuses ignored paths without `-f`; forcing it would un-ignore by accident).
- **`hooks/skill-complete.sh` behavior**: the hook stays whitelisted machinery — it reads `.active-modes` mode blocks (legacy tolerance) and `tests/hooks_test.sh` pins its behavior. Only its line-4 comment changes (Edit P): a comment naming the dead skill as a live actor is writer-side vocabulary, the class step 8 removes everywhere else, and a comment-only change is behavior-neutral.

**Records — never edited**: `kivna/sessions/`, dated `docs/plans/` files (this spec included), `docs/gates/`, the annotations log, README What's New history entries, playbook Recent-changes entries (mode records at 211/212/214/222/223/224), `Sensei Input/`. **Session state — not spec steps**: `CONTEXT.md` and `TODO.md` name mode as the pending graveyard verdict; they are the conductor's own close-out updates, excluded from this spec and its surface.

## Pieces

- [ ] 1. Rip skills/mode and modes/
- [ ] 2. README: identity, section out, fit-together rewrite, What's New 0.75.0
- [ ] 3. CONTRIBUTING: modes path out, skills become the door
- [ ] 4. CLAUDE.md + AGENTS.md: identity and structure lines
- [ ] 5. Manifests: capability lists + marketplace one-liner + triple bump
- [ ] 6. slainte: mode-count rule out, renumber
- [ ] 7. playbook: roster, layout, composition section, Working list
- [ ] 8. state-contract + switch: dead-skill references out
- [ ] 9. Collateral diff review + mode sweep
- [ ] 10. Ship

## Steps

All commands run from `/Users/anthonymaley/Kerd`.

### Step 1 — Rip skills/mode and modes/ [delegate, model: haiku, effort: low]

First confirm the contents:

```
ls skills/mode/
ls modes/ | wc -l
```

Expected: exactly `SKILL.md`; exactly `11`. Anything else ⇒ STOP, hand back. Then:

```
git rm -r skills/mode modes
```

This commit-to-be IS the archive for spike.md's method content — no copy is made anywhere.

**Verify:**

```
test -e skills/mode && echo STILL-THERE || echo GONE
test -e modes && echo STILL-THERE || echo GONE
git status --short | grep -c '^D '
```

Expected: `GONE`, `GONE`, `12` (1 skill file + 11 mode files, all staged as deletions).

**Addendum (step 9 hand-back ruling — HIT 1):** also delete the mode demo recording cheat-sheet; `git rm` stages this deletion too, and `scripts/` (which holds only this file) disappears with it:

```
git rm scripts/demo-mode.sh
```

**Verify (addendum):**

```
test -e scripts/demo-mode.sh && echo STILL-THERE || echo GONE
git status --short | grep -c '^D '
```

Expected: `GONE`, `13`.

### Step 2 — README: identity, section out, fit-together rewrite, What's New 0.75.0 [delegate, model: sonnet, effort: medium]

Seven edits, A–G. Anchor on the exact strings, not line numbers (earlier edits shift later lines).

Edit A — line 5, the identity paragraph. The "Eleven" here is the SKILLS count (see the two-Elevens section). Old:

```
Eleven workflow skills plus community-contributed modes for Claude Code. Skills handle the operational side of working across sessions and machines: when to pull, what to commit, where to put notes, how to audit for drift, how to maintain structural health. Modes orchestrate skills from Kerd, Superpowers, and other plugins into guided flows for different types of work. They keep the plumbing clean so you can focus on the work.
```

New:

```
Ten workflow skills for Claude Code. Skills handle the operational side of working across sessions and machines: when to pull, what to commit, where to put notes, how to audit for drift, how to maintain structural health. They keep the plumbing clean so you can focus on the work.
```

Edit B — What's New. Change `## What's New (v0.74.0)` to `## What's New (v0.75.0)`, then insert immediately after it (before `### v0.74.0`):

```

### v0.75.0

**mode is cut — a capability you had yesterday is gone, and so are its eleven flows.** Yesterday, `/kerd:mode` listed guided workflows by category and walked you through one — phase menus, a step tracker, a session instruction resurfaced at each step — and anyone could add a flow by PRing a single markdown file into `modes/`. Today nothing answers that phrase. The losses, named: **the community-contribution path via `modes/` dies un-exercised** — zero community modes arrived in four and a half months (the one community contribution in that window, trim, came as a skill); **eight flows disappear with no direct replacement** — spike, deepwork, maintain, strategy, writing, research, legal, and sales; **the skill count goes Eleven → Ten**. What replaces the rest: the three code-building flows (greenfield, jit, quickfix) hand their job to the ladder — the entry gates route each piece of work to its rung by construction (`python3 tools/gates/gate.py route <slug>`), which is the routing the menus promised, and the progress view derives position from disk — which is exactly why the step tracker had to go: it was self-reported position, and position is derived, never asserted. spike.md's method content — empirical-primitive-first, the provisional-loss survival gate, commit graduation, the self-audit baseline — lives in git history at this cut's commit; the spike ROUTE stays alive in the gate vocabulary (`route: spike` is the one licensed ladder bypass). Return condition: the first real spike run that wants method guidance brings that content back.
```

The existing `### v0.74.0` entry and everything below it (including every historical mode record) is untouched.

Edit C — the slainte section sentence. Old:

```
Release (Kerd-specific) catches version sync drift, description mismatches, skill/mode count claims, namespace prefix issues, and marketplace URL changes.
```

New:

```
Release (Kerd-specific) catches version sync drift, description mismatches, skill count claims, namespace prefix issues, and marketplace URL changes.
```

Edit D — delete the whole `### mode (Workflow Routing)` section: the heading, its three paragraphs (the last containing "Eleven starter modes ship with Kerd" — the OTHER Eleven, which dies here and is never rewritten as "Ten"), the category table, the code fence containing `/mode`, and the trailing blank line — so exactly one blank line remains between trim's closing code fence (the one containing `/trim`) and `### pair (Partner Mode)`. Pre-check the bounds:

```
sed -n '296p;298p;318p' README.md
```

Expected: a bare ` ``` ` fence line, `### mode (Workflow Routing)`, `### pair (Partner Mode)`. Any mismatch ⇒ STOP, hand back.

Edit E — the Skill completion hook line. Old:

```
**Skill completion hook:** When a mode is active and you complete the current step's skill, shows your progress and what's next. Read-only — the mode skill handles state transitions.
```

New:

```
**Skill completion hook:** When a mode is active and you complete the current step's skill, shows your progress and what's next. Read-only — it never writes `.active-modes`.
```

(The hook itself is untouched machinery; only the clause naming the dead skill changes.)

Edit F — in `## How They Fit Together`, delete the entire `**Picking a workflow:**` paragraph and its trailing blank line (the paragraph starting `**Picking a workflow:** Before diving in, run `/mode`` and ending `resurfaces your instructions at each step.`), so exactly one blank line separates the `**Starting a project:**` paragraph from the `**Day to day:**` paragraph.

Edit G — two sentence-level fixes in the same section. First, in the `**Day to day:**` paragraph, old:

```
(what happened last time). If a mode was active when you left, switch tells you where you were in the flow. Then it offers
```

New:

```
(what happened last time). Then it offers
```

Second, the `**The layers:**` paragraph. Old:

```
**The layers:** Switch owns the session boundary — pull, and the session-state commit. Conductor owns session discipline, and commits its own work as it verifies. Kivna owns the knowledge vault. Mode sits above all of them, routing you to the right combination based on what you're doing. You can use any skill standalone, but mode ties them into a coherent flow.
```

New:

```
**The layers:** Switch owns the session boundary — pull, and the session-state commit. Conductor owns session discipline, and commits its own work as it verifies. Kivna owns the knowledge vault. Routing sits above all of them in the entry gates: `python3 tools/gates/gate.py route <slug>` reads what is on disk and names the rung where the work enters. Every skill works standalone.
```

Deliberately NOT edited in README: line 229 (`adds playbook, architecture, memory, mode` — kivna's `.active-modes` export, see Surface), line 166 (conductor mode-awareness — machinery), the Stop/SessionStart hook lines ("active mode" / "interrupted mode" — `.active-modes` vocabulary), and all What's New history.

**Verify:**

```
sed -n '5p' README.md | cut -c1-3
grep -n "What's New (v0.75.0)" README.md
grep -c '### mode' README.md
grep -c 'Workflow Routing' README.md
grep -c 'Picking a workflow' README.md
grep -c 'starter modes' README.md
grep -n 'kerd:mode' README.md
grep -n 'memory, mode' README.md
```

Expected: `Ten`; a hit at line 14; `0` (grep -c exits 1 at zero — that exit is the pass); `0`; `0`; `0`; exactly ONE hit, inside the new `### v0.75.0` entry; exactly ONE hit (the kivna fence line, ~229 — it MUST still be there).

### Step 3 — CONTRIBUTING: modes path out, skills become the door [delegate, model: haiku, effort: low]

Three edits.

Edit A — line 3. Old:

```
Kerd accepts contributions for new modes, skill improvements, and bug fixes. This doc sets expectations for PRs.
```

New:

```
Kerd accepts contributions for new skills, skill improvements, and bug fixes. This doc sets expectations for PRs.
```

Edit B — delete the whole `## Modes (easiest contribution)` section: the heading through `- Test by running `/kerd:mode your-mode` in a real project` plus the blank line after it, so line 3's paragraph is followed by one blank line and then `## Skills` as the first section.

Edit C — the Skills section opener (its "more" compared against the now-dead modes path). Old:

```
Skill PRs change behavior. They require more scrutiny.
```

New:

```
Skill PRs change behavior. They require scrutiny.
```

**Verify:**

```
grep -c -i 'mode' CONTRIBUTING.md
sed -n '3p;5p' CONTRIBUTING.md
```

Expected: `0` (exit 1); line 3 is the new sentence, line 5 is `## Skills`.

### Step 4 — CLAUDE.md + AGENTS.md: identity and structure lines [delegate, model: haiku, effort: low]

Four edits. The two files' identity lines end byte-identical except for the first word pair (`Claude Code plugin:` vs `Codex plugin:`).

Edit A — CLAUDE.md line 3. Old:

```
Claude Code plugin: eleven workflow skills plus community-contributed modes for session discipline, risk qualification, machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, conversational pair mode, and workflow routing.
```

New:

```
Claude Code plugin: ten workflow skills for session discipline, risk qualification, machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, and conversational pair mode.
```

Edit B — CLAUDE.md Project Structure: delete the line

```
modes/            # workflow mode definitions (one .md per mode, community-contributed)
```

Edit C — AGENTS.md line 3 (stale at "eight" — replaced wholesale per the composer amendment; the rest of AGENTS.md's Codex-era drift stays, flagged separately). Old:

```
Codex plugin: eight workflow skills plus community-contributed modes for session discipline, machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, and workflow routing.
```

New:

```
Codex plugin: ten workflow skills for session discipline, risk qualification, machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, and conversational pair mode.
```

Edit D — AGENTS.md Project Structure: delete its modes/ line (identical string to Edit B's).

**AGENTS.md is gitignored** (`.gitignore` line 7). Edits C-D are machine-local by declaration: they keep the local Codex fork in agreement, ship nothing, and the file never appears in `git status`. Do NOT `git add` it at any step.

**Verify:**

```
grep -c 'modes/' CLAUDE.md AGENTS.md
grep -n 'ten workflow skills' CLAUDE.md AGENTS.md
grep -c 'workflow routing' CLAUDE.md AGENTS.md
```

Expected: `0` and `0` (exit 1); a hit at line 3 in each; `0` and `0` (exit 1).

### Step 5 — Manifests: capability lists + marketplace one-liner + triple bump [delegate, model: haiku, effort: low]

Both capability lists lose `with community-contributed modes` and `, and workflow routing`, and stay byte-identical. The one replacement string, used verbatim in BOTH `.claude-plugin/plugin.json` → `description` AND `.claude-plugin/marketplace.json` → `plugins[0].description`:

```
Opinionated workflow toolkit: session discipline, session and machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, risk qualification, and conversational pair mode
```

`metadata.description` in marketplace.json is intentionally a different shape and is normally untouched — but the standing carve-out is "update it only when the marketplace summary itself needs to change," and it NAMES modes, so this once it changes. Old:

```
Kerd: opinionated workflow skills and community-contributed modes for Claude Code
```

New:

```
Kerd: opinionated workflow skills for Claude Code
```

Version bump `0.74.0` → `0.75.0` in all three places: `plugin.json` → `version`; `marketplace.json` → `metadata.version`; `marketplace.json` → `plugins[0].version`.

**Verify:**

```
python3 -c "
import json
a=json.load(open('.claude-plugin/plugin.json')); b=json.load(open('.claude-plugin/marketplace.json'))
print(a['description']==b['plugins'][0]['description'])
print(a['version'], b['metadata']['version'], b['plugins'][0]['version'])
print(any('mode' in s for s in (a['description'], b['plugins'][0]['description'], b['metadata']['description'])))"
```

Expected (`conversational pair mode` is gone from nothing — note the third line checks the WORD `mode`, and `pair mode` contains it, so):

```
True
0.75.0 0.75.0 0.75.0
True
```

The `True` on line 3 is `conversational pair mode` only — confirm with `python3 -c "import json; d=json.load(open('.claude-plugin/plugin.json'))['description']; print('community-contributed' in d, 'workflow routing' in d)"` → `False False`.

### Step 6 — slainte: mode-count rule out, renumber [delegate, model: haiku, effort: low]

In `skills/slainte/SKILL.md`, the `#### release` area. Delete rule 4 entirely:

```
4. **Mode count consistency**: count `modes/*.md` files and compare against claims in `README.md` mode table rows. Mismatch is medium severity.
```

Then renumber the five rules after it (the file has no other reference to release rules by number — verified at spec-writing time):

- `5. **SKILL frontmatter drift**` → `4. **SKILL frontmatter drift**`
- `6. **Namespace sweep**` → `5. **Namespace sweep**`
- `7. **Marketplace URL**` → `6. **Marketplace URL**`
- `8. **Cross-doc claim verification**` → `7. **Cross-doc claim verification**`
- `9. **Hook template currency**` → `8. **Hook template currency**`

Rule 3's illustrative `(e.g., "Nine workflow skills")` stays — it is an example, not a count claim.

**Verify:**

```
grep -c 'Mode count' skills/slainte/SKILL.md
awk '/#### release/,/#### all/' skills/slainte/SKILL.md | grep -o '^[0-9]*\.' | tr -d '.\n'; echo
```

Expected: `0` (exit 1); `12345678`.

### Step 7 — playbook: roster, layout, composition section, Working list [delegate, model: sonnet, effort: medium]

Eleven edits, A–K, in `docs/playbook.md`. Recent-changes history (mode records in the `v0.29.0`/`v0.28.0`/`v0.26.0`/`v0.19.0`/`v0.17.x` entries) is a record — untouched.

Edit A — directory layout skills line (roster already omitted interrogate/trim/pair — pre-existing; only the dead name is removed). Old:

```
skills/           # SKILL.md per skill (conductor, lorg, kivna, mode, skriv, slainte, tend, switch)
```

New:

```
skills/           # SKILL.md per skill (conductor, lorg, kivna, skriv, slainte, tend, switch)
```

Edit B — delete the layout line:

```
modes/            # workflow mode definitions (one .md per mode, community-contributed)
```

(The `kivna/.active-modes` layout line stays — machinery.)

Edit C — the skills-count line (the SKILLS Eleven). Old:

```
**Eleven skills, each with a single responsibility, plus four opt-in hooks:**
```

New:

```
**Ten skills, each with a single responsibility, plus four opt-in hooks:**
```

Edit D — delete the roster bullet:

```
- **mode**: workflow routing (orchestrates Kerd, Superpowers, and other plugins into guided flows)
```

Edit E — delete the whole `## Mode-to-Skill Composition` section: the heading, its intro line ("Rules for how modes and skills interact:"), and all seven rule bullets, through the blank line before `## Integrations` — so exactly one blank line separates the hooks list from `## Integrations`.

Edit F — the cross-cutting gotcha's sweep list (living guidance; the sweep must match the tree). Old (within the line starting `- **Cross-cutting changes need a final grep across ALL files`):

```
sweep skills/, modes/, docs/, hooks/, tests/, README, and the manifests before calling a shape change done.
```

New:

```
sweep skills/, docs/, hooks/, tests/, README, and the manifests before calling a shape change done.
```

Edit G — Current Status Working list, first line (wrong twice: names the dead skill, omits pair; composer amendment applies — ten names, now exact). Old:

```
- All ten skills functional: conductor, lorg, switch, kivna, slainte, skriv, tend, trim, mode, interrogate
```

New:

```
- All ten skills functional: conductor, interrogate, lorg, switch, kivna, slainte, skriv, tend, trim, pair
```

Edit H — Old:

```
- Slainte release audit catches version sync, description sync, skill/mode count drift, namespace issues
```

New:

```
- Slainte release audit catches version sync, description sync, skill count drift, namespace issues
```

Edit I — Old:

```
- Unified `.active-modes` schema shared by conductor, skriv, mode, and switch
```

New:

```
- Unified `.active-modes` schema shared by conductor, skriv, and switch
```

Edit J — delete the Working line:

```
- Mode tracks progress with structured steps format (stable IDs, concrete args, status markers)
```

Edit K — delete the Working line:

```
- Mode skill for workflow routing with 10 community-contributed starter modes (added `spike` for high-uncertainty exploration)
```

Untouched by declaration: `**Version:** 0.60.0` (pre-existing staleness, separate decision), "Switch snapshots active mode state…" (machinery), "Mode markers on conductor and skriv…" (phase-marker concept), both hook description lines, all Recent-changes entries.

**Verify:**

```
grep -c 'Mode-to-Skill' docs/playbook.md
grep -n 'Ten skills' docs/playbook.md
grep -n 'workflow routing\|Mode skill\|modes/' docs/playbook.md
```

Expected: `0` (exit 1); a hit at ~59; every remaining hit at a line number INSIDE the `**Recent changes` block (all ≥ its heading line, currently 197) — zero hits above it.

### Step 8 — state-contract + switch: dead-skill references out [delegate, model: sonnet, effort: medium]

Sixteen edits: twelve in `docs/state-contract.md` (A–L), three in `skills/switch/SKILL.md` (M–O), one in `hooks/skill-complete.sh` (P). The `.active-modes` FILE section survives — conductor, skriv, switch, and the hooks still use it; only the dead skill's writer-side content goes.

Edit A — CONTEXT.md readers. Old:

```
**Readers:** switch (in), conductor (cold orient), modes (setup steps)
```

New:

```
**Readers:** switch (in), conductor (cold orient)
```

Edit B — CONTEXT.md format comment (spacing before the em-dash preserved exactly). Old:

```
## Active Mode         — mode/conductor snapshot for cross-machine handoff
```

New:

```
## Active Mode         — conductor snapshot for cross-machine handoff
```

Edit C — .active-modes readers. Old:

```
**Readers:** switch (in), Stop hook, SessionStart hook, PostToolUse hook, mode skill
```

New:

```
**Readers:** switch (in), Stop hook, SessionStart hook, PostToolUse hook
```

Edit D — .active-modes format fence: remove the mode block (nothing writes it anymore; hooks tolerating leftover blocks is undocumented legacy tolerance). Old fence body:

```
# One line per skill: <skill>: <state>
conductor: execute
skriv: active
mode: greenfield (step 3 of 9)
  instruction: focus on pricing strategy only
  steps:
    1: /kerd:switch in | open session, set context [done]
    2: /superpowers:brainstorming | explore the problem space [done]
    3: /superpowers:writing-plans | produce the implementation plan [current]
    4: /superpowers:executing-plans 1 | build phase 1 [pending]
    5: /kerd:switch out | close session [pending]
```

New fence body:

```
# One line per skill: <skill>: <state>
conductor: execute
skriv: active
```

Edit E — delete the three mode-format rules (three consecutive bullets):

```
- Mode's `steps:` block uses format: `<id>: <skill> [<args>] | <label> [<status>]`
- Status markers: `[done]`, `[current]`, `[pending]`, `[skipped]`
- Step IDs are stable integers assigned at mode start.
```

Edit F — the snapshot rule keeps its meaning, loses the dead vocabulary. Old:

```
- Switch out snapshots mode state to CONTEXT.md `## Active Mode` before committing (cross-machine handoff).
```

New:

```
- Switch out snapshots `.active-modes` state to CONTEXT.md `## Active Mode` before committing (cross-machine handoff).
```

Edit G — Cross-Skill Interaction Summary: remove the `mode` column. Replace the whole table. Old:

```
| File | conductor | switch | mode | skriv | kivna | slainte | tend | lorg | hooks |
|------|------|--------|------|-------|-------|---------|------|------|-------|
| CONTEXT.md | W/R | W/R | R | - | - | - | R | - | - |
| TODO.md | W | W/R | - | - | R | - | R | R | - |
| .active-modes | W/R | R | W | W | - | - | - | - | R |
| sessions/ | - | W/R | - | - | R | - | - | R | R |
| vault Status | - | - | - | - | W | R | - | R | - |
| KIF exports | - | - | - | - | W | - | - | - | - |
| lorg-report | - | - | - | - | - | - | - | W | - |
```

New:

```
| File | conductor | switch | skriv | kivna | slainte | tend | lorg | hooks |
|------|------|--------|-------|-------|---------|------|------|-------|
| CONTEXT.md | W/R | W/R | - | - | - | R | - | - |
| TODO.md | W | W/R | - | R | - | R | R | - |
| .active-modes | W/R | R | W | - | - | - | - | R |
| sessions/ | - | W/R | - | R | - | - | R | R |
| vault Status | - | - | - | W | R | - | R | - |
| KIF exports | - | - | - | W | - | - | - | - |
| lorg-report | - | - | - | - | - | - | W | - |
```

Edit H — Workflow Ownership row cell. Old:

```
| Session plan (TODO.md `## Now`) | **conductor** (plan), **switch** (wrap-up) | Mode reads but doesn't write TODO.md |
```

New:

```
| Session plan (TODO.md `## Now`) | **conductor** (plan), **switch** (wrap-up) | Other skills read but don't write TODO.md |
```

Edit I — delete the row:

```
| Mode state (.active-modes mode block) | **mode** | Conductor reads mode state but never writes the mode line |
```

Edit J — Old:

```
| Conductor state (.active-modes conductor line) | **conductor** | Mode reads conductor state but never writes the conductor line |
```

New:

```
| Conductor state (.active-modes conductor line) | **conductor** | Other skills read conductor state but never write the conductor line |
```

Edit K — delete the row:

```
| Workflow routing | **mode** | Mode guides, never calls skills directly |
```

Edit L — delete the conflict-resolution bullet:

```
- Mode presents steps for the user to invoke, never invokes skills programmatically
```

Edit M — `skills/switch/SKILL.md` line 85, same fix as Edit B (spacing preserved exactly). Old:

```
## Active Mode         — mode/conductor snapshot for cross-machine handoff
```

New:

```
## Active Mode         — conductor snapshot for cross-machine handoff
```

Edit N — `skills/switch/SKILL.md` line 118, an illustrative closure-inference example naming the dead contribution path (same indent and column shape; it is illustrative text — use this replacement):

Old:

```
  · open   — "solicit community mode contributions" (untouched)
```

New:

```
  · open   — "wire the progress render into CI" (untouched)
```

Edit O — `skills/switch/SKILL.md` line 384, inside the Switch-In low-mode example fence: a second illustrative line naming the dead contribution path (same class as Edit N — illustrative text; the replacement keeps the example's two-item shape and matches N's phrase):

Old:

```
Next: tend on other repos, community mode contributions
```

New:

```
Next: tend on other repos, wire the progress render into CI
```

The preceding example line (`Last session: fixed hook paths in krutho-founders and krutho-strategy (v0.29.1)`) is untouched.

Edit P — `hooks/skill-complete.sh` line 4 (step 9 hand-back ruling — HIT 2): the comment names the dead skill as a live actor. Comment-only, behavior-neutral — the hook's bash semantics are untouched and `tests/hooks_test.sh` pins behavior, not comments. Old:

```
# Does NOT mutate .active-modes. The mode skill handles state transitions.
```

New:

```
# Does NOT mutate .active-modes. A mode block found there is legacy state.
```

Lines 3 and 5 ("reminds about mode progress", "no mode is active") stay — `.active-modes` machinery vocabulary.

Untouched in switch by declaration: the Mode-snapshot step (line 90) and section 9's active-modes check/restore including its `greenfield (step 4 of 9)` illustration — that machinery is exactly what still tolerates a leftover mode block from a pre-cut session.

**Verify:**

```
grep -c 'mode skill\|Mode state\|Workflow routing\|mode: greenfield\|modes (setup steps)' docs/state-contract.md
grep -n 'conductor snapshot' docs/state-contract.md skills/switch/SKILL.md
grep -c 'community mode' skills/switch/SKILL.md
grep -c '| mode |' docs/state-contract.md
grep -c 'mode skill' hooks/skill-complete.sh
```

Expected: `0` (exit 1); a hit at ~22 and ~85; `0` (exit 1); `0` (exit 1); `0` (exit 1).

### Step 9 — Collateral diff review + mode sweep [keep]

Deletion blast radius check. Three parts, all must pass.

Part A — the diff touches nothing outside the surface:

```
git add -A -n; git status --short
```

Expected changed paths, exactly and only: `skills/mode/SKILL.md` (D), the eleven `modes/*.md` (D), `scripts/demo-mode.sh` (D), `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/slainte/SKILL.md`, `skills/switch/SKILL.md`, `hooks/skill-complete.sh`, `docs/playbook.md`, `docs/state-contract.md`, this spec file (`docs/plans/2026-08-04-mode-cut-spec.md`, new) — plus possibly `CONTEXT.md`/`TODO.md` if the conductor has begun close-out (session state, never staged with this commit). **AGENTS.md never appears here — it is gitignored**; confirm its local edit exists by content instead: `grep -c 'ten workflow skills' AGENTS.md` → `1`. Any other path ⇒ FAIL, hand back.

Part B — no live doc still points at the dead skill or the dead directory:

```
grep -rn 'kerd:mode' . --exclude-dir=.git
grep -rni 'workflow routing\|community-contributed modes\|starter modes\|mode skill' . --exclude-dir=.git
grep -rn 'modes/' . --exclude-dir=.git | grep -v '\.active-modes'
```

PASS iff every remaining hit is one of:
- records: `kivna/sessions/`, dated `docs/plans/` files (this spec included), `docs/gates/`, `docs/plans/annotations`, `Sensei Input/`, README What's New entries, playbook Recent-changes entries;
- generated report: `docs/lorg-report.md`;
- the R3 allowlist glob, deliberately kept: `tools/gates/kit.py` (docstring, ~661) and `tools/gates/README.md` (~169);
- machinery: `tests/hooks_test.sh`, `hooks/*.sh`, conductor/switch/kivna `.active-modes` text, state-contract machinery lines;
- session state: `CONTEXT.md`/`TODO.md` (conductor's close-out cleans these).

Resolved by the step 9 hand-back (a deterministic re-run finds neither): `scripts/demo-mode.sh` is deleted (step 1 addendum — `scripts/` no longer exists) and `hooks/skill-complete.sh` line 4 no longer names the dead skill (step 8 Edit P). Switch's `docs/demo-mode.gif`/`.mp4` untracked-triage examples match none of the sweep patterns and need no entry.

Any hit in living skill/doc text that names the mode SKILL or the `modes/` DIRECTORY as alive ⇒ FAIL: hand the hit back to the orchestrator — do not improvise a fix. In particular confirm `skills/kivna/SKILL.md` and README line 229 still carry their `mode` export references UNCHANGED (removing them would be collateral damage, not compliance).

Part C — counts and identity:

```
ls skills/ | wc -l
test -e modes && echo STILL-THERE || echo GONE
sed -n '5p' README.md | cut -c1-3
grep -n 'ten workflow skills' CLAUDE.md AGENTS.md
grep -n 'Ten skills' docs/playbook.md
python3 -c "import json; a=json.load(open('.claude-plugin/plugin.json')); b=json.load(open('.claude-plugin/marketplace.json')); print(a['description']==b['plugins'][0]['description'])"
```

Expected: `10`; `GONE`; `Ten`; hits at line 3 in both; a hit at ~59; `True`.

### Step 10 — Ship [keep]

1. Run the full local gate — the same four checks CI enforces. All must exit 0; any failure ⇒ hand back, do not ship:

```
python3 tools/gates/gate.py selftest
python3 tools/gates/gate.py audit
python3 tools/gates/gate.py release
python3 tools/diagram/progress.py selftest
```

2. Stage by name. The `skills/mode`, `modes/`, and `scripts/demo-mode.sh` deletions are ALREADY STAGED by step 1's `git rm` — do NOT `git add` the deleted paths (they no longer exist on disk; adding them would error with "pathspec did not match"). **AGENTS.md is gitignored and is NOT in this list** — `git add AGENTS.md` refuses an ignored path and would fail the step; its edit stays local by declaration:

```
git add README.md CONTRIBUTING.md CLAUDE.md .claude-plugin/plugin.json .claude-plugin/marketplace.json skills/slainte/SKILL.md skills/switch/SKILL.md hooks/skill-complete.sh docs/playbook.md docs/state-contract.md docs/plans/2026-08-04-mode-cut-spec.md
```

3. Commit with piece trailers (conductor appends its own session trailer per its conventions). Trailers cover pieces 1–9 only: a commit cannot witness its own landing, so `Piece: mode-cut/10` is explicitly assigned to the follow-up render-refresh commit (the progress-view re-render that follows the ship — both previous cuts did exactly this):

```
Cut mode: routing belongs to the gates (v0.75.0)

The mode skill and all eleven modes/ files are deleted whole — the
third rip, the last graveyard verdict. Never used in five months; the
entry gates route by construction, the phase menus violated the talk
rules, and the step tracker was self-reported position, which
derived-from-disk forbids. Losses named in What's New: the modes/
contribution path dies un-exercised, eight flows disappear,
the skill count goes Eleven to Ten. spike.md's method content lives in
git history at this commit; return condition: the first real spike run
that wants method guidance. README, CONTRIBUTING, CLAUDE.md, both
capability lists, the marketplace one-liner, slainte, switch, the
skill-complete hook comment, playbook and state-contract re-point; the
mode demo recording script dies with its subject.

Piece: mode-cut/1
Piece: mode-cut/2
Piece: mode-cut/3
Piece: mode-cut/4
Piece: mode-cut/5
Piece: mode-cut/6
Piece: mode-cut/7
Piece: mode-cut/8
Piece: mode-cut/9
```

4. Push, then verify CI on the RIGHT SHA — `gh run list` right after a push can return the previous run (playbook gotcha), so match `headSha` explicitly:

```
git push
git rev-parse HEAD
gh run list --limit 3 --json headSha,status,conclusion,workflowName
```

Re-poll until a run whose `headSha` equals the pushed SHA reports `completed`/`success` for the entry-gate workflow. A green run on any other SHA proves nothing.

**Verify:** all four gate commands exit 0 locally; after commit, `git status --short` shows nothing staged and no surface file modified (only `CONTEXT.md`/`TODO.md` may remain dirty — session state, committed later by switch); push accepted; the CI run on the pushed SHA (headSha-matched) completes green.
