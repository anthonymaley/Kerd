---
name: slainte
description: "Use when the user says 'slainte', 'audit', 'health check', 'check staleness', or needs to audit project health across docs, code, site, or dependencies — or when conductor's close-out fires the release close-out pass at a version bump or an acceptance-record landing. The pass fixes drift under the caller's verification gate and reports what it deliberately left; on-demand area audits report-only unless the caller asks for fixes."
---

# Slainte (Project Health)

From Irish "slàinte" (health). Pronounced "SLAHN-chuh".

Slainte is the release close-out pass, plus on-demand health audits. The pass fixes what is drift and reports what it deliberately left; the on-demand area audits report issues with severity grades and fix only when the caller asks.

## Targets

Targets derive from the repo — there is no config file. The narrative surface is `README.md` (skill sections + What's New), `CLAUDE.md`, `docs/playbook.md`, `docs/state-contract.md`, the capability lists in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, and any `docs/design/` living doc the release's diff touched. Each area audit below names how its own targets derive.

## The release pass

**Two triggers, either alone: the version-field diff — CI's release definition, reused (a work commit that changes the three `"version"` fields IS a release, rule R1's set) — or an acceptance-record landing (a new `docs/gates/*-acceptance.md` in the session's work commits: a feature accepted as ready for release).** The release definition stays single; the completion moment fires the same pass. The caller is conductor's close-out, which invokes this pass before running the boundary; standalone `/kerd:slainte release` runs the same judgment checks on demand.

**Charter: CI owns the mechanical layer (release rules R1–R3, audit rules AU1–8)** — version sync, capability-list sync, namespace prefixes, dated design filenames, gate-record shape, grounding references, rigor lines, the requirements register's schema and links. The pass never re-checks any of those; anything newly machine-checkable belongs in CI (file a Backlog row), not here. The pass owns what no machine rule covers: the `release` area checks below, swept across the derived narrative surface.

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
5. **Hook auto-load currency**: verify `hooks/hooks.json` exists, is valid JSON, and every `${CLAUDE_PLUGIN_ROOT}/hooks/*.sh` it references exists in `hooks/`. Flag a missing script as high — the harness auto-loads this file on enable, so a wrong path silently kills the hook. Verify the retired `hooks/hooks.template.json` is absent (its presence means the v0.96.0 auto-load migration is incomplete); flag as medium if found.

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
