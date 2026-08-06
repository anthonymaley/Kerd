---
route: new
stage: contracted
---

# Release-closeout — slice 1 build spec (v0.85.0)

Contract for the release-closeout slice-1 build: slainte becomes the
release close-out pass — triggered by conductor at version bumps, fixing
drift with reported restraint — and the `.slainte` config dies. Authority:
`docs/design/release-closeout.md` (the 21-edit map and its six stage-1
measurements are binding); frame: `docs/product/release-closeout.md`;
GO record `docs/gates/2026-08-06-release-closeout-design.md`.
All paths relative to `/Users/anthonymaley/Kerd` (call it `$BASE`).
Subagent cwd resets between calls — every command uses absolute paths.
Fenced blocks below quote headings and checkboxes safely — the gate and
progress parsers are fence-aware since v0.83.1.

Fixture-asserted strings — these appear VERBATIM in the files and in
this spec; any paraphrase is a build failure:

- restraint discipline (slainte identity + description): `reports what it deliberately left`
- CI-owns pointer (slainte charter): `CI owns the mechanical layer (release rules R1–R3, audit rules AU1–6)`
- skriv wire (slainte fix discipline): `passes ` `` `/kerd:skriv` `` `'s one-shot audit`
- tend deprecated row: `` `.slainte`: removed in v0.85.0 — targets derive from the repo; offer deletion ``
- kerd-map one-liner first line: `release close-out pass: triggered`

The single-definition law (v0.84.0's, extended here): conductor's two
new wires are ONE instruction each — invoke `/kerd:tend`, invoke
`/kerd:slainte` — and ZERO descriptions of what either skill's checks
are. Tend and slainte stay the definitions of their own checks. Any
conductor edit that re-describes a tend or slainte check is a build
refusal.

Standing terrain note, observed at contract time: `TODO.md` is modified
in the working tree (mid-session brief capture by the running conductor).
It is session state — the boundary's to commit, never this build's.
Tolerate ` M TODO.md` in every porcelain check below; never stage it,
never revert it.

Out of scope: `skills/switch/SKILL.md` entirely (any hunk there is a
refusal — the pass runs before the boundary and the boundary contract
is v0.84.0's); `skills/skriv/SKILL.md` (verdict keep — it is called,
not changed); any CI graduation (What's-New-untouched refusal etc.);
external/declared surfaces (slice 2); the kivna scaffold verdict
(Backlog archaeology); `CHANGELOG.md` (historical record — its
`.slainte` line at line 23 stays as the record of the v0.11.0 rename);
`tools/diagram/gen_release_closeout.py` and the design's own
`release-closeout.{excalidraw,svg}` (the design diagram narrates this
very change — historical once shipped); the playbook `## Current Status`
block (stale wholesale at v0.60.0 — a standing bystander; this slice
edits only the role line, and sweeping Current Status is exactly the
shipped pass's future job, not this build's); both capability-list
`description` fields (checked at contract time: neither mentions
slainte's read-only-ness — "project audits" still describes the pass +
the on-demand audits; they stay byte-identical and untouched).

## Pieces

- [x] Step 1 — skills/slainte/SKILL.md: re-founded (full replacement)
- [x] Step 2 — skills/tend/SKILL.md: the 5 .slainte sites
- [x] Step 3 — skills/conductor/SKILL.md: the two trigger wires
- [x] Step 4 — skills/kivna/SKILL.md: one stale example line (flagged, beyond map)
- [x] Step 5 — Diff-review the four SKILL.md files (blast radius; switch untouched)
- [x] Step 6 — docs/state-contract.md: the two audit rows
- [x] Step 7 — docs/playbook.md: the slainte role line
- [x] Step 8 — README.md: slainte section rewrite
- [x] Step 9 — README.md: What's New v0.85.0, five-version cap
- [x] Step 10 — gen_kerd_map.py one-liner + regenerate the map pair
- [x] Step 11 — git rm .slainte
- [x] Step 12 — Version bump 0.84.0 → 0.85.0 (three fields) + product-doc stage
- [x] Step 13 — Proof obligations: the six measurement families + collateral
- [x] Step 14 — Full local suite (six gate.yml commands; stale deferred)
- [x] Step 15 — Ship: work commit with boxes checked, render refresh, stale, one push

### Step 1 — skills/slainte/SKILL.md: re-founded (full replacement)

`[delegate, model: sonnet, effort: medium]` — file:
`/Users/anthonymaley/Kerd/skills/slainte/SKILL.md`. Design edits 1–6,
executed as ONE full-file replacement (the restructure touches every
section; surgical edits would be more fragile than a rewrite). Replace
the entire file content with EXACTLY the block below — byte-faithful,
including the en-dashes in `R1–R3` / `AU1–6`. The five area check lists
(docs/code/site/deps/playbook), the Output Format table, the Evidence
specification, and the Severity guide are carried over verbatim from the
current file; only the registration lines above them changed to derived
targets.

**What** — the complete new file content:

````markdown
---
name: slainte
description: "Use when the user says 'slainte', 'audit', 'health check', 'check staleness', or needs to audit project health across docs, code, site, or dependencies — or when conductor's close-out fires the release close-out pass at a version bump. The pass fixes drift under the caller's verification gate and reports what it deliberately left; on-demand area audits report-only unless the caller asks for fixes."
---

# Slainte (Project Health)

From Irish "slàinte" (health). Pronounced "SLAHN-chuh".

Slainte is the release close-out pass, plus on-demand health audits. The pass fixes what is drift and reports what it deliberately left; the on-demand area audits report issues with severity grades and fix only when the caller asks.

## Targets

Targets derive from the repo — there is no config file. The narrative surface is `README.md` (skill sections + What's New), `CLAUDE.md`, `docs/playbook.md`, `docs/state-contract.md`, the capability lists in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, and any `docs/design/` living doc the release's diff touched. Each area audit below names how its own targets derive.

## The release pass

**Trigger: the version-field diff — CI's release definition, reused.** A work commit that changes the three `"version"` fields IS a release (release rule R1's set). The caller is conductor's close-out, which invokes this pass before running the boundary; standalone `/kerd:slainte release` runs the same judgment checks on demand.

**Charter: CI owns the mechanical layer (release rules R1–R3, audit rules AU1–6)** — version sync, capability-list sync, namespace prefixes, dated design filenames, gate-record shape, grounding references, rigor lines. The pass never re-checks any of those; anything newly machine-checkable belongs in CI (file a Backlog row), not here. The pass owns what no machine rule covers: the `release` area checks below, swept across the derived narrative surface.

**Fix discipline: fixes are work commits, and restraint is reported.** The pass edits what is drift, under the caller's verification gate — diff read in full, blast radius reviewed, staged by name — and any prose it writes passes `/kerd:skriv`'s one-shot audit before landing. Anything judged deliberate-not-drift is named in the report as left untouched, with the reason. Visible restraint is the countermeasure for an audit with hands: never fix silently, never leave silently.

**Output: the severity table, plus the left-untouched list** (see Output Format).

## Commands

### `/kerd:slainte <area>`

Run the audit for the specified area. Valid areas: `docs`, `code`, `site`, `deps`, `playbook`, `release`, `all`.

#### docs

Targets: the repo's committed markdown surface — README.md and CLAUDE.md first, then `docs/` (excluding dated historical records: `docs/plans/`, `docs/gates/`, session logs).

1. **Doc inventory**: if CLAUDE.md has a docs table, cross-reference: every file listed should exist, every doc file should be listed
2. **Name consistency**: search for old or stale names across all docs. Check CLAUDE.md or README for the canonical project name.
3. **Path consistency**: search for broken internal links and old paths
4. **Internal links**: check markdown links between docs resolve to real files
5. **Stats drift**: check test counts, package counts, and other metrics against actual values
6. **TODO.md accuracy**: are "done" items actually done? Are "blocked" items still blocked?
7. **README vs CLAUDE.md**: do they agree on structure, counts, and key details?

#### code

Targets: the source directories the repo actually carries (for Kerd: `skills/`, `tools/`, `hooks/`) plus any manifest present (`package.json`, `pyproject.toml`, or equivalent).

1. **Test suite**: run all tests, report failures
2. **Build check**: run the project's build command, report errors
3. **Unused exports**: spot-check main entry points against actual usage
4. **Lock file consistency**: lock files match manifests
5. **CI config**: if `.github/workflows/` exists, check it references correct versions and commands

#### site

Targets: the site build config and content directories where they exist (`public/`, `next.config.js`, or equivalent). Skip the area when none exist.

1. **Build check**: run the site build command, must pass clean
2. **Content sync**: if docs are synced from a source directory, check for drift
3. **Navigation completeness**: every doc should appear in sidebar/nav config
4. **Asset check**: referenced assets should exist
5. **Broken links**: scan for references to deleted files

#### deps

Targets: every dependency manifest and lock file present. Skip the area when none exist.

1. **Dependency freshness**: run package manager outdated commands (npm outdated, pip list --outdated, cargo outdated, etc.)
2. **Lock file consistency**: lock files match manifests
3. **Security vulnerabilities**: run `npm audit`, `pip audit`, or equivalent if available

#### playbook

Targets: `docs/playbook.md`.

1. **Existence**: does `docs/playbook.md` exist? If not, high severity ("No playbook found. Run `/kerd:tend` to create one from the skeleton.")
2. **Current Status accuracy**: compare the "Current Status" section against actual project state (working build, test results, deployed state if detectable)
3. **Tech stack drift**: are the tools/frameworks listed in the playbook still in `package.json` / `pyproject.toml` / equivalent? Flag removed or added deps not reflected in playbook
4. **Setup steps validity**: do the setup commands reference files and scripts that still exist?
5. **Freshness**: when was playbook last modified relative to recent commits? If 10+ commits have landed since the last playbook update, flag as medium
6. **Section completeness**: are any major sections empty or still showing skeleton placeholder text?

#### release

Kerd-specific release audit — the judgment layer of the release pass, also runnable on demand. Only runs when slainte detects `.claude-plugin/plugin.json` (i.e., in the Kerd repo itself or a Kerd-like plugin repo).

CI owns the mechanical checks that used to open this list (version sync, description sync, namespace sweep — release rules R1–R3); never re-check them here.

1. **Skill count consistency**: count `skills/*/SKILL.md` files and compare against claims in `README.md` (e.g., "Nine workflow skills") and `docs/playbook.md`. Mismatches are high severity.
2. **SKILL frontmatter drift**: for each `skills/*/SKILL.md`, verify the `name` field matches the directory name. Flag mismatches as high.
3. **Marketplace URL**: verify `.claude-plugin/marketplace.json` `plugins[0].source.url` points to the canonical repo (not a fork). Mismatch is high severity.
4. **Cross-doc claim verification**: verify that claims made in docs match the code and each other:
   - README "What's New" version numbers match the actual current version in plugin.json. If the latest What's New entry references a version that doesn't match the current version, flag as medium.
   - README skill descriptions match SKILL.md behavior. For each skill section in README, spot-check 2-3 specific claims (e.g., "conductor does not write session logs") against the actual SKILL.md. Flag contradictions as high.
   - `docs/playbook.md` "Working" list matches actual skill set and feature claims. Flag stale claims as medium.
   - `docs/state-contract.md` ownership table matches actual skill behavior. For each W (write) entry, verify the skill actually writes to that file. For each `-` (no interaction), verify the skill doesn't reference that file. Flag contradictions as high.
   - Vault Status.md version matches plugin.json version. Mismatch is informational only (v0.83.0: the vault is opt-in and refreshed solely by deliberate `/kerd:kivna save` — staleness of any depth is expected, never a finding).
5. **Hook template currency**: verify `hooks/hooks.template.json` exists, is valid JSON, and references hook scripts that exist in `hooks/`. Flag missing scripts as high. Verify the template is not named `hooks.json` (would auto-load). Flag as high if found.

#### all

Run all areas (including release if `.claude-plugin/plugin.json` exists). Use parallel agents where possible for speed.

## Output Format

Start with a summary line:

```
Slainte: X high, Y medium, Z low
```

Then a severity table per area:

| Severity | Location | Issue | Evidence |
|----------|----------|-------|----------|
| high | `docs/whitepaper.md:12` | References old project name | grep "OldName" → 3 hits at lines 12, 47, 89 |
| medium | `CLAUDE.md` § Tests | Test count says 145, actual is 148 | `find . -name "*.test.*" \| wc -l` → 148; CLAUDE.md line 67 says 145 |
| low | `README.md:23` | Minor formatting inconsistency | trailing whitespace per `git diff --check` |

In the release pass, the table is followed by a **Left untouched** list — one line per deliberate non-fix, naming the finding and why it was judged deliberate rather than drift.

### Evidence specification

Each finding must include an **Evidence** column entry — the specific check that detected it: file:line reference, command run with output, grep result, version comparison, or doc citation. "References old project name" without a line number or grep result is unverifiable; "References old project name (grep 'OldName' → 3 hits at lines 12, 47, 89)" is reproducible. This applies to ALL severity levels — even `low` findings get a citation, because a finding without evidence is a claim without a source.

If a finding cannot be cited (e.g. cross-doc drift detected through reading rather than a specific command), record the comparison method explicitly: "compared README.md `## Skills` count to `skills/` directory count: README says 9, directory has 10."

### Severity guide:
- **high**: factually wrong, broken build, missing file, security vulnerability
- **medium**: stale but not misleading, cosmetic inconsistency
- **low**: nitpick, style drift, minor staleness
````

**Why:** the re-founding is design edits 1–6 in one stroke — identity,
config death, derived targets, the pass charter, pruned release rules
(1, 2, 5 → the CI-owns pointer; 3, 4, 6, 7, 8 kept and renumbered
1–5 with rule 7's vault note intact), and derivation lines per area.

**Verify:** from `$BASE` (baselines at contract time in parens;
`grep -c` exits 1 when it prints `0` — the printed count is the check):
`grep -c '\.slainte' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `0` (was 4);
`grep -c 'Read-only audit\|Does not fix anything\|never modifies files, only reports' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `0` (was 2);
`grep -ci 'release close-out pass' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `2`;
`grep -c 'CI owns' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `2`;
`grep -c 'Version sync' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `0` (was 1 — case-sensitive; the lowercase pointer mentions survive);
`grep -c 'skriv' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `1` (was 0);
`grep -c 'reports what it deliberately left' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `2`;
`grep -c '^#### ' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `7` (docs, code, site, deps, playbook, release, all — unchanged census).

### Step 2 — skills/tend/SKILL.md: the 5 .slainte sites

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/skills/tend/SKILL.md`. Design edits 7–11,
exact old → new. Touch nothing else — Category 3's vault checks, the
`## Boundary with Slainte` section, and Category 9 are untouched.

**(7) Required-files list** — delete this one line from the "Check
these files exist:" list (the list then ends at `` - `docs/playbook.md` ``;
the TODO shape check paragraph below it is untouched):

```
- `.slainte`
```

**(8) Scaffold template block** — delete this whole block (from the
`**.slainte:**` label through its closing fence), leaving exactly one
blank line between the playbook template's closing fence and the "For
existing repos" paragraph:

````
**.slainte:**
```
# Slainte Audit Targets

## docs
- README.md
- docs/

## playbook
- docs/playbook.md
```
````

**(9) Deprecated-patterns list** — replace the `.sotu` row with two rows:

old:

```
- `.sotu`: renamed to `.slainte` in v0.11.0
```

new:

```
- `.sotu`: renamed to `.slainte` in v0.11.0 (both since removed)
- `.slainte`: removed in v0.85.0 — targets derive from the repo; offer deletion
```

**(10) Stale-file exception list** (Category 6):

old:

```
- Files with no git commits touching them in 60+ days that aren't documentation (`.md`), config (`.json`, `.yaml`, `.toml`, `.slainte`), or gitignore. Use `git log -1 --format=%at -- <file>` to check the most recent commit touching the file.
```

new:

```
- Files with no git commits touching them in 60+ days that aren't documentation (`.md`), config (`.json`, `.yaml`, `.toml`), or gitignore. Use `git log -1 --format=%at -- <file>` to check the most recent commit touching the file.
```

**(11) Example report's required-files line:**

old:

```
  README.md  CLAUDE.md  CONTEXT.md  TODO.md  docs/playbook.md  .slainte
```

new:

```
  README.md  CLAUDE.md  CONTEXT.md  TODO.md  docs/playbook.md
```

**Why:** tend stops requiring, creating, and exempting the config it
now offers to delete — the `.slainte` survivors are the two
deprecated-pattern rows only.

**Verify:** from `$BASE`:
`grep -c '\.slainte' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `2` (was 5 — the two deprecated rows);
`grep -c 'both since removed' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `1`;
`grep -c 'offer deletion' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `1`;
`grep -c 'docs/playbook.md  .slainte' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `0`;
`grep -c 'Slainte Audit Targets' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `0`.

### Step 3 — skills/conductor/SKILL.md: the two trigger wires

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/skills/conductor/SKILL.md`. Design edits
12–13, exact old → new. One instruction per wire, ZERO re-description
of tend's or slainte's checks (the single-definition law above). Touch
nothing else — frontmatter, Plan, Execute, and Principles are untouched.

**(12) Orient gains the bare-repo wire.** Insert a new paragraph (with
one blank line either side) between the cold-path paragraph and the
`**Mode awareness:**` paragraph:

old:

```
**Cold path (conductor invoked with no switch-in this session):** Do a light orient — read only `CONTEXT.md` (`## Where We Are`) and `TODO.md` (`## Now`). That's enough to plan. Don't sweep the playbook, session logs, and progress files; that's switch-in's read. If you need the full picture, run `/kerd:switch in` first.

**Mode awareness:**
```

new:

```
**Cold path (conductor invoked with no switch-in this session):** Do a light orient — read only `CONTEXT.md` (`## Where We Are`) and `TODO.md` (`## Now`). That's enough to plan. Don't sweep the playbook, session logs, and progress files; that's switch-in's read. If you need the full picture, run `/kerd:switch in` first.

**Bare repo (no Kerd structure detected — no CONTEXT.md, no TODO.md, no `kivna/`):** offer `/kerd:tend` to set the structure up before planning — one invoke; tend's own SKILL.md defines the setup. If declined, orient on what exists and continue.

**Mode awareness:**
```

**(13) Close-out gains the release wire as step 6; the boundary
renumbers 6 → 7.** The `[conductor: closed]` marker stays inside the
boundary step, after it — i.e., still the final act.

old (one line):

```
6. **Run the boundary**: invoke `/kerd:switch out` via the Skill tool — full mode, the standalone default. The flow is defined once, in `skills/switch/SKILL.md` Switch Out; do not re-describe its steps here or anywhere in this file. When it completes, output `[conductor: closed]` as the final marker.
```

new (two lines):

```
6. **Release close-out pass**: if this session's work commits changed the three plugin `"version"` fields (CI's release definition, rule R1), invoke `/kerd:tend` and then `/kerd:slainte` before the boundary — the structural drift check and the narrative pass with fixes, each defined in its own SKILL.md, not here. The pass's edits are work commits under the verification gate. No version change, no pass.
7. **Run the boundary**: invoke `/kerd:switch out` via the Skill tool — full mode, the standalone default. The flow is defined once, in `skills/switch/SKILL.md` Switch Out; do not re-describe its steps here or anywhere in this file. When it completes, output `[conductor: closed]` as the final marker.
```

**Why:** the trigger lives with the caller that owns close-out; two
wires, one instruction each, so slainte and tend stay the only
definitions of their own checks.

**Verify:** from `$BASE`:
`grep -ci 'release close-out pass' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1` (was 0);
`grep -c 'no Kerd structure' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1` (was 0);
`grep -c 'kerd:tend' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `2` (was 0);
`grep -c 'kerd:slainte' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `2` (was 1 — the orient sniff-test pointer survives);
`awk '/^### 4. Close Out/,/^## Principles/' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md | grep -c '^[0-9]\.'` prints `7` (was 6).

### Step 4 — skills/kivna/SKILL.md: one stale example line (flagged, beyond map)

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/skills/kivna/SKILL.md`. **FLAGGED: beyond the
design's 21-edit map.** The contract-time repo-wide `.slainte` sweep
(the playbook's cross-cutting-grep obligation) found one live reference
the map missed: a Weekly-template example risk that asserts "health
audits can't run" without the config — false doctrine at v0.85.0. Same
class as the routing lines the v0.83.0 map missed. The gate may strike
this step alone — no proof obligation depends on it (Step 13's family 1
notes the conditional).

One exact line replacement inside the Weekly example fence (preserve
the 3-space indentation):

old:

```
   - [open] No .slainte config — health audits can't run
```

new:

```
   - [open] No playbook yet — /kerd:tend to create one
```

**Why:** an example asserting the dead config blocks audits would
re-teach the config's existence from inside kivna.

**Verify:** from `$BASE`:
`grep -c '\.slainte' /Users/anthonymaley/Kerd/skills/kivna/SKILL.md` prints `0` (was 1);
`git -C /Users/anthonymaley/Kerd diff --numstat -- skills/kivna/SKILL.md` prints exactly `1	1	skills/kivna/SKILL.md`.

### Step 5 — Diff-review the four SKILL.md files (blast radius; switch untouched)

`[keep]` — read `git -C /Users/anthonymaley/Kerd diff skills/` in full.
The characteristic blast-radius failure is mechanical — an edit range
that swallows a neighbour — and passes every step-level grep. The review
must specifically catch:

1. **switch untouched entirely** (this slice's hard boundary):
   `git -C /Users/anthonymaley/Kerd diff --name-only -- skills/switch/SKILL.md`
   prints nothing, and `git -C /Users/anthonymaley/Kerd diff --stat`
   does not list `skills/switch/SKILL.md`. Any hunk there is a refusal.
2. **Conductor untouched outside the two wire regions** — three
   byte-compares, each exits 0 with no output:
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/conductor/SKILL.md | sed -n '1,/^### 1. Orient$/p') <(sed -n '1,/^### 1. Orient$/p' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md)`
   (frontmatter and everything above Orient);
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/conductor/SKILL.md | sed -n '/^#### Model advisory$/,/^### 4. Close Out$/p') <(sed -n '/^#### Model advisory$/,/^### 4. Close Out$/p' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md)`
   (Plan and Execute whole);
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/conductor/SKILL.md | sed -n '/^## Principles$/,$p') <(sed -n '/^## Principles$/,$p' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md)`
   (Principles whole).
3. **No tend/slainte check re-described in conductor** — the
   single-definition law: the diff's added conductor lines contain the
   two invoke instructions and nothing describing what either skill
   checks. Grep guard:
   `grep -c 'Skill count\|frontmatter drift\|Marketplace URL\|Cross-doc claim\|Hook template\|Version sync' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md`
   prints `0` (baseline 0 — must stay 0).
4. **Tend hunks land only at the five named sites** — Category 3 whole
   is byte-identical:
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/tend/SKILL.md | sed -n '/^#### Category 3/,/^#### Category 4/p') <(sed -n '/^#### Category 3/,/^#### Category 4/p' /Users/anthonymaley/Kerd/skills/tend/SKILL.md)`
   exits 0 with no output; the `## Boundary with Slainte` section and
   Category 9 carry no hunks.
5. **Slainte carried its keep-list over** — the rewrite is the named
   region (whole file), so the check is content survival, not hunk
   scope: `grep -c 'Cross-doc claim verification' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `1`;
   `grep -c 'informational only' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `1` (rule 7's v0.83.0 vault note survived);
   `grep -c 'Doc inventory' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `1`;
   `grep -c 'Severity guide' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `1`.
6. **Kivna diff is one line swapped** — the numstat from Step 4, and no
   hunk outside the Weekly example fence.

**Why:** a verify command tests presence of the intended change and is
silent about the absence of unintended ones; the byte-compares are that
absence, proven.

**Verify:** the four diff commands exit 0 with no output; the two greps
print `0` and the survival greps print `1` each; the hunk-scope read
(items 1, 4, 6) is affirmed in one line each.

### Step 6 — docs/state-contract.md: the two audit rows

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/state-contract.md`. Design edits 14–15,
two exact full-line replacements in the Workflow Ownership table.
Nothing else in the file changes. This file is in the release sweep's
namespace allowlist — the new text contains no bare slash skill
reference.

**(14) Structural-audit row:**

old:

```
| Structural audit and fix | **tend** | Slainte reports content issues but doesn't fix structure |
```

new:

```
| Structural audit and fix | **tend** | Tend keeps structure; slainte fixes *content* drift under the caller's gate |
```

**(15) Content-audit row:**

old:

```
| Content audit (read-only) | **slainte** | Slainte never modifies files, only reports |
```

new:

```
| Content audit and fix | **slainte** — triggered at release by conductor, on demand otherwise | Fixes drift under the caller's verification gate; reports what it leaves |
```

**Why:** the ownership rows are the contract other skills route by —
the v0.83.0 goal block proved stale rows here route behaviour.

**Verify:** from `$BASE`:
`grep -c 'Content audit and fix' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `1`;
`grep -c 'Content audit (read-only)' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `0`;
`grep -c 'Read-only audit\|Does not fix anything\|never modifies files, only reports' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `0` (was 1);
`git -C /Users/anthonymaley/Kerd diff --numstat -- docs/state-contract.md` prints exactly `2	2	docs/state-contract.md`.

### Step 7 — docs/playbook.md: the slainte role line

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/playbook.md`. Design edit 18, one exact
line replacement in the Architecture skills list. Nothing else — the
stale `## Current Status` block is a named bystander (see Out of scope).
This file is in the release sweep's namespace allowlist — no bare slash
references in the new text.

old:

```
- **slainte**: project health audits (docs, code, site, deps, playbook)
```

new:

```
- **slainte**: the release close-out pass (triggered by conductor at version bumps; fixes doc drift under the gate) + on-demand health audits
```

**Why:** the playbook's architecture list is a routing document; this
line is its copy of the identity this slice re-founds.

**Verify:** from `$BASE`:
`grep -c 'the release close-out pass (triggered by conductor at version bumps' /Users/anthonymaley/Kerd/docs/playbook.md` prints `1`;
`grep -c 'project health audits (docs, code, site, deps, playbook)' /Users/anthonymaley/Kerd/docs/playbook.md` prints `0`;
`git -C /Users/anthonymaley/Kerd diff --numstat -- docs/playbook.md` prints exactly `1	1	docs/playbook.md`.

### Step 8 — README.md: slainte section rewrite

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. Design edit 16 — replace the
slainte section's two paragraphs and its usage fence, exactly as below.
README shorthand (`/slainte`) is sanctioned here — keep it. The
`### slainte (Project Health)` heading and the sections either side are
untouched (the tend section carries no `.slainte` mention — checked at
contract time).

old (two paragraphs + fence):

````
Slainte audits project health across six areas: docs, code, site, deps, playbook, and release. It reads a `.slainte` config file at the project root to know what to check. Each area has specific checks. Docs gets cross-referenced against CLAUDE.md, scanned for stale names and broken links. Code runs tests and the build. Deps checks for outdated packages and security issues. Playbook checks whether `docs/playbook.md` exists, whether its Current Status is accurate, whether the tech stack listed still matches reality, and whether setup steps still point to files that exist. Release (Kerd-specific) catches version sync drift, description mismatches, skill count claims, namespace prefix issues, and marketplace URL changes.

Everything gets a severity grade: high (factually wrong, broken build, security vulnerability), medium (stale but not misleading), low (nitpick). Slainte reports problems. It doesn't fix them.

```
/slainte              # show current config
/slainte add docs README.md   # register a target
/slainte docs         # audit docs area
/slainte playbook     # audit the playbook
/slainte release      # audit version sync, counts, namespaces (Kerd repos)
/slainte all          # audit everything
```
````

new:

````
Slainte is the release close-out pass, plus on-demand health audits. When a conductor session ships a version bump, close-out triggers slainte before the boundary: it sweeps the repo's own narrative surfaces — README sections and What's New, the playbook, the state contract, the capability lists, any living design doc the release touched — fixes what is drift, and names in its report what it deliberately left untouched, so restraint is visible instead of assumed. Fixes land as normal work commits under the caller's verification gate, and prose it writes passes skriv's one-shot audit first. The mechanical layer stays CI's (version sync, capability lists, namespaces — R1–R3 and AU1–6); slainte owns the judgment layer: skill-count claims, frontmatter drift, marketplace URL, hook template currency, and cross-doc claim verification. There is no config file — targets derive from the repo.

The on-demand area audits (docs, code, site, deps, playbook, release) still run any time, report-only by default. Everything gets a severity grade: high (factually wrong, broken build, security vulnerability), medium (stale but not misleading), low (nitpick).

```
/slainte docs         # audit docs area
/slainte playbook     # audit the playbook
/slainte release      # the release pass's judgment checks, on demand
/slainte all          # audit everything
```
````

**Why:** the public page must describe the triggered pass, the
restraint report, and the config's death — the old section was the
README's copy of the read-only identity.

**Verify:** from `$BASE`:
`grep -c '\.slainte' /Users/anthonymaley/Kerd/README.md` prints `0` (was 1);
`grep -c "It doesn't fix them" /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -c 'show current config' /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -ci 'release close-out pass' /Users/anthonymaley/Kerd/README.md` prints `1`.

### Step 9 — README.md: What's New v0.85.0, five-version cap

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. Four exact edits.

**(a) Heading:** `## What's New (v0.84.0)` → `## What's New (v0.85.0)`

**(b) Insert** this block immediately before the `### v0.84.0` line
(blank line after the block, so `### v0.84.0` keeps one blank line
above it):

```
### v0.85.0

**Releases now check their own story.** Before, slainte was a read-only audit you had to remember to run — and nobody did: the mechanical checks moved into CI, and the judgment layer (does the README still describe what shipped? is What's New honest?) ran never. Now the release moment itself triggers it: when a conductor session's work bumps the plugin version, close-out runs tend's drift check and slainte's narrative pass before the boundary. Slainte fixes what drifted — as normal work commits under the verification gate, with skriv auditing any prose it writes — and its report names what it deliberately left alone, so restraint is visible instead of assumed. The hand-kept `.slainte` config file is gone; audit targets derive from the repo. What it means: the doc surface gets one honest pass per release instead of zero, CI keeps the mechanical layer, and `/slainte` still answers on demand.
```

**(c) Delete** the entire `### v0.80.0` block (heading + its one
paragraph), leaving exactly one blank line between the `### v0.81.0`
paragraph and the trailing italic line:

```
### v0.80.0

**A document's reading list becomes machine-checkable — "lost" is now a red light.** A product doc may declare its background reading in a `## Grounding` section (`- <ref> — <why>`); audit rule AU5 proves every declared reference still resolves on disk at every push. A doc that moves, renames, or vanishes turns the push red naming the exact broken reference — the failure that used to be invisible (the well-named design doc that held the answer and went unread). Declaring is opting in; retrofitted reading lists would be hollow, so nothing is retrofitted. Whether the reading *happened* (read-receipts) is the named next slice.
```

**(d) Trailing line:**

old:

```
*Release notes for v0.79.0 and earlier live in git history — `git log --follow README.md`.*
```

new:

```
*Release notes for v0.80.0 and earlier live in git history — `git log --follow README.md`.*
```

**Why:** release notes keep the last five versions here (v0.82.0
convention); the entry speaks Compare & Contrast — before / now / what
it means, in the user's terms.

**Note on (b):** the step-8 grep `'.slainte'` count moves from 0 to 1
here — the What's New entry legitimately names the dead config file in
backticks. Step 13 family 1 carries the final README expectation.

**Verify:** from `$BASE`:
`grep -c '### v0.85.0' /Users/anthonymaley/Kerd/README.md` prints `1`;
`grep -c '### v0.80.0' /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -c '^### v0\.' /Users/anthonymaley/Kerd/README.md` prints `5`;
`grep -c 'v0.80.0 and earlier' /Users/anthonymaley/Kerd/README.md` prints `1`;
`grep -c "What's New (v0.85.0)" /Users/anthonymaley/Kerd/README.md` prints `1`.

### Step 10 — gen_kerd_map.py one-liner + regenerate the map pair

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/tools/diagram/gen_kerd_map.py`, then the
regen. Design edit 19.

**(a) The slainte one-liner** — exact replacement:

old:

```
        ("slainte", "read-only health audit:\ndocs, code, deps staleness;\nreports, never fixes", INK),
```

new:

```
        ("slainte", "release close-out pass: triggered\nat version bumps, fixes doc drift,\nrestraint reported", INK),
```

**(b) Title version — FLAGGED: beyond the design's named edit.** The
map title pins `(v0.81.0)`; shipping a v0.85.0 release that edits this
very file while its title claims v0.81.0 is the drift class this slice
exists to kill. The gate may strike this item alone — no proof
obligation depends on it:

old: `c.txt("Kerd — the whole system, current state (v0.81.0)", X0, 80, 30)`
new: `c.txt("Kerd — the whole system, current state (v0.85.0)", X0, 80, 30)`

**(c) Regenerate the pair:**
`python3 /Users/anthonymaley/Kerd/tools/diagram/gen_kerd_map.py`
must print, in order:
`wrote /Users/anthonymaley/Kerd/docs/design/kerd-map.excalidraw | elements: 81`
(81 measured at contract time — text edits change no element census),
an `svg <W>x<H>` line (dims not pinned), then exactly these three lines:
`no bound-text overflows` / `no text/box collisions` /
`no text/text overlaps`. Any line starting `!!` is a refusal — STOP,
report the fault line to the conductor (the fix is re-wrapping the
one-liner's `\n` breaks, a score decision, not yours). Note: the
changed text elements may render blue in the map — that is
`mark_deltas` marking deltas against the reviewed baseline, by design,
not drift.

**Why:** the map is the README's hero image and the design names the
one-liner + regen as one edit — the pair must move in the same commit
as the code that describes it.

**Verify:** from `$BASE`:
`grep -c 'release close-out pass' /Users/anthonymaley/Kerd/tools/diagram/gen_kerd_map.py` prints `1` (was 0);
`grep -c 'reports, never fixes' /Users/anthonymaley/Kerd/tools/diagram/gen_kerd_map.py` prints `0` (was 1);
the regen output matches the block above;
`git -C /Users/anthonymaley/Kerd status --porcelain -- docs/design/kerd-map.excalidraw docs/design/kerd-map.svg` prints exactly two ` M ` lines.

### Step 11 — git rm .slainte

`[keep]` — one command; dispatch overhead exceeds the work, no judgment
claimed. Design edit 20 — nothing replaces the file:

`git -C /Users/anthonymaley/Kerd rm .slainte`

`git rm` STAGES the deletion (standing playbook gotcha) — the ship step
must never `git add .slainte` afterwards; the deletion rides the index.

**Why:** the config's grave — targets derive from the repo now.

**Verify:** `git -C /Users/anthonymaley/Kerd ls-files .slainte` prints
nothing (was `.slainte`); `test -f /Users/anthonymaley/Kerd/.slainte; echo $?`
prints `1`; `git -C /Users/anthonymaley/Kerd status --porcelain -- .slainte`
prints `D  .slainte`.

### Step 12 — Version bump 0.84.0 → 0.85.0 (three fields) + product-doc stage

`[delegate, model: haiku, effort: low]` — MINOR bump: changed behaviour
(the pass, the wires, the config death). Replace `"version": "0.84.0"`
with `"version": "0.85.0"` in:

- `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (one occurrence)
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (BOTH
  occurrences: `metadata.version` and `plugins[0].version`)

All three `description` fields untouched — checked at contract time:
neither capability list mentions slainte's read-only-ness, and "project
audits" still describes the pass + the on-demand audits (design edit 21
verdict: unchanged). The capability lists stay byte-identical between
plugin.json and marketplace.json plugins[0] (release rule R2), and
`metadata.description` keeps its distinct marketplace one-liner shape.

Plus one line in `/Users/anthonymaley/Kerd/docs/product/release-closeout.md`
frontmatter — the stage-discipline line the conductor-boundary contract
named up front after the vault-unhook amendment proved the map forgets
it:

old: `stage: framed`
new: `stage: building`

**Why:** three synced version fields are release rule R1; the stage
line keeps the product doc honest about where the slug stands.

**Verify:** from `$BASE`:
`grep -c '"version": "0.85.0"' /Users/anthonymaley/Kerd/.claude-plugin/plugin.json` prints `1`;
`grep -c '"version": "0.85.0"' /Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` prints `2`;
`git -C /Users/anthonymaley/Kerd diff -U0 -- .claude-plugin/ | grep -E '^[-+][^-+]' | grep -vc '"version"'` prints `0` (only version lines changed);
`grep -c 'stage: building' /Users/anthonymaley/Kerd/docs/product/release-closeout.md` prints `1`.

### Step 13 — Proof obligations: the six measurement families + collateral

`[keep]` — run the design's six stage-1 measurement families verbatim on
the final tree, then the collateral check. Expected values are empirical
(baselines measured at contract time), not predicted. `grep -c` exits 1
when it prints `0` — the printed count is the check, not the exit code.

1. **Config dead:**
   `git -C /Users/anthonymaley/Kerd ls-files .slainte` prints nothing;
   `grep -c '\.slainte' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `0` (was 4);
   `grep -c '\.slainte' /Users/anthonymaley/Kerd/skills/tend/SKILL.md` prints `2` (was 5 — deprecated-pattern rows only);
   `grep -c '\.slainte' /Users/anthonymaley/Kerd/skills/kivna/SKILL.md` prints `0` (was 1; prints `1` only if the gate struck Step 4);
   `grep -c '\.slainte' /Users/anthonymaley/Kerd/README.md` prints `1` (the What's New entry naming the removed config — legitimate history).
2. **Read-only identity dead:**
   `grep -c 'Read-only audit\|Does not fix anything\|never modifies files, only reports' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `0` (was 2);
   `grep -c 'Read-only audit\|Does not fix anything\|never modifies files, only reports' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `0` (was 1).
3. **The wires exist, once each; conductor re-describes nothing:**
   `grep -ci 'release close-out pass' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1` (was 0);
   `grep -c 'no Kerd structure' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1` (was 0);
   `grep -c 'Skill count\|frontmatter drift\|Marketplace URL\|Cross-doc claim\|Hook template\|Version sync' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0` (baseline 0).
4. **The charter split is written:**
   `grep -c 'CI owns' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `2` (was 0);
   `grep -c 'Version sync' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `0` (was 1 — no kept rule carries the pruned heading).
5. **skriv wire present:**
   `grep -c 'skriv' /Users/anthonymaley/Kerd/skills/slainte/SKILL.md` prints `1` (was 0 — design floor: ≥ 1).
6. **Map regenerated:**
   `grep -c 'release close-out pass' /Users/anthonymaley/Kerd/tools/diagram/gen_kerd_map.py` prints `1` (was 0);
   `git -C /Users/anthonymaley/Kerd status --porcelain -- docs/design/` prints exactly the two ` M ` lines for `kerd-map.excalidraw` and `kerd-map.svg` (the committed pair regenerates in the work commit, Step 15).

Collateral: `git -C /Users/anthonymaley/Kerd status --porcelain` lists
EXACTLY these paths and nothing else (` M TODO.md` is the tolerated
bystander — present unless the boundary committed it meanwhile; its
absence is not a failure):

```
 M .claude-plugin/marketplace.json
 M .claude-plugin/plugin.json
D  .slainte
 M README.md
 M TODO.md
 M docs/design/kerd-map.excalidraw
 M docs/design/kerd-map.svg
 M docs/playbook.md
 M docs/product/release-closeout.md
 M docs/state-contract.md
 M skills/conductor/SKILL.md
 M skills/kivna/SKILL.md
 M skills/slainte/SKILL.md
 M skills/tend/SKILL.md
 M tools/diagram/gen_kerd_map.py
?? docs/plans/2026-08-06-release-closeout-spec.md
```

Any extra path is unintended drift — a refusal, back to the offending
step.

**Why:** these six are the design's named answers; shipping without
them green is shipping an unmeasured contract.

**Verify:** all six families plus the collateral list pass exactly as
stated above.

### Step 14 — Full local suite (six gate.yml commands; stale deferred)

`[keep]` — run the `run:` lines from
`/Users/anthonymaley/Kerd/.github/workflows/gate.yml` locally from
`$BASE`, EXCEPT `python3 tools/diagram/progress.py stale` — stale's
natural green moment is after Step 15's render commit; it runs there.
The six, in gate.yml order, with expected outputs (measured at contract
time on the parent tree):

1. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest` → exit 0, `selftest: 26 cases passed`
2. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` → exit 0, `audit: clean`
3. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py release` → exit 0, `release: clean` (R1: three synced 0.85.0 fields; R2: byte-identical capability lists; R3: no bare skill references — Steps 1–4, 6, 7 all wrote into swept files)
4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py selftest` → exit 0, `selftest: 14 ok`
5. `python3 /Users/anthonymaley/Kerd/tools/design/matrix.py selftest` → exit 0, `selftest: 14 ok`
6. `python3 /Users/anthonymaley/Kerd/tools/design/matrix.py audit` → exit 0, `matrix audit: clean (0 matrices)`

**Why:** the local suite is CI run early — a red push is a refusal that
should have happened on this machine.

**Verify:** all six exit 0 with the named outputs.

### Step 15 — Ship: work commit with boxes checked, render refresh, stale, one push

`[keep]` — in order:

1. Set ALL fifteen Pieces boxes in THIS spec to `[x]`. Boxes are checked
   IN THE WORK COMMIT, never the render commit — the progress board
   derives from contract checklists, so a box checked after the render
   moves the board the render just drew and the stale gate refuses the
   push (the standing stale-refuser gotcha).
2. Stage by name exactly these fourteen paths — `TODO.md` is session
   state and MUST NOT be staged, and `.slainte` MUST NOT be re-added
   (its deletion is already staged by Step 11; `git add` on a deleted
   path fails with "pathspec did not match"):
   `.claude-plugin/marketplace.json` `.claude-plugin/plugin.json`
   `README.md` `docs/design/kerd-map.excalidraw`
   `docs/design/kerd-map.svg`
   `docs/plans/2026-08-06-release-closeout-spec.md`
   `docs/playbook.md` `docs/product/release-closeout.md`
   `docs/state-contract.md` `skills/conductor/SKILL.md`
   `skills/kivna/SKILL.md` `skills/slainte/SKILL.md`
   `skills/tend/SKILL.md` `tools/diagram/gen_kerd_map.py`
3. ONE work commit, message exactly:

```
release-closeout slice 1: slainte becomes the release close-out pass — triggered at version bumps, fixes with restraint, .slainte config gone (v0.85.0)

Claude-Session: https://claude.ai/code/session_01B7yNRTL9d6oJJQcpLVMaSq
```

4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py` (the
   refresh).
5. `git -C /Users/anthonymaley/Kerd status --porcelain` — must list ONLY
   progress-render outputs (`docs/plans/progress.excalidraw`,
   `docs/plans/progress.svg`, `docs/plans/progress.html`), plus at most
   the tolerated ` M TODO.md`. Any other path is a refusal: a render
   commit that carries anything else moves the page it just rendered.
6. Stage the three render files by name, commit
   `Refresh progress render` — no trailer, render files only. If the
   refresh produced no render changes, skip this commit.
7. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py stale` →
   exit 0, `render current`.
8. `git -C /Users/anthonymaley/Kerd push` — ONE push carrying both
   commits.

**Why:** work and render stay separate commits so the board's
derivation is provable; one push keeps the boundary discipline.

**Verify:** `git -C /Users/anthonymaley/Kerd status --porcelain` prints
nothing except possibly ` M TODO.md`;
`git -C /Users/anthonymaley/Kerd rev-list origin/main..HEAD --count` prints `0`;
`git -C /Users/anthonymaley/Kerd log -2 --format=%s` shows
`Refresh progress render` above the work-commit subject (or only the
work commit if step 6 was skipped);
`git -C /Users/anthonymaley/Kerd show --stat HEAD --format=` on the work
commit lists exactly fifteen paths (the fourteen staged + the
`.slainte` deletion);
`grep -c '^- \[x\]' /Users/anthonymaley/Kerd/docs/plans/2026-08-06-release-closeout-spec.md` prints `15`;
the work commit's `git log --format=%B` ends with the `Claude-Session:` trailer.
