---
name: slainte
description: "Use when the user says 'slainte', 'audit', 'health check', 'check staleness', or needs to audit project health across docs, code, site, or dependencies. Read-only audit that reports issues without fixing them."
---

# Slainte (Project Health)

From Irish "slàinte" (health). Pronounced "SLAHN-chuh".

Read-only audit of project health. Reports issues with severity grades. Does not fix anything. That's the user's call.

## Config

Slainte uses a `.slainte` config file at the project root to know what to audit. If no config exists on first run, prompt the user to register targets.

### Config format (`.slainte`):

```
# Slainte Audit Targets

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

## playbook
- docs/playbook.md
```

## Commands

### `/kerd:slainte` (no args)

Show the current `.slainte` config: what's registered under each area. If no config exists, say so and offer to create one.

### `/kerd:slainte add <area> <path>`

Register a file or directory under an area. Create `.slainte` if it doesn't exist. Valid areas: `docs`, `code`, `site`, `deps`, `playbook`.

Example: `/kerd:slainte add docs README.md`

### `/kerd:slainte <area>`

Run the audit for the specified area. Valid areas: `docs`, `code`, `site`, `deps`, `playbook`, `all`.

#### docs

For each target registered under `## docs`:

1. **Doc inventory**: if CLAUDE.md has a docs table, cross-reference: every file listed should exist, every doc file should be listed
2. **Name consistency**: search for old or stale names across all docs. Check CLAUDE.md or README for the canonical project name.
3. **Path consistency**: search for broken internal links and old paths
4. **Internal links**: check markdown links between docs resolve to real files
5. **Stats drift**: check test counts, package counts, and other metrics against actual values
6. **TODO.md accuracy**: are "done" items actually done? Are "blocked" items still blocked?
7. **README vs CLAUDE.md**: do they agree on structure, counts, and key details?

#### code

For each target registered under `## code`:

1. **Test suite**: run all tests, report failures
2. **Build check**: run the project's build command, report errors
3. **Unused exports**: spot-check main entry points against actual usage
4. **Lock file consistency**: lock files match manifests
5. **CI config**: if `.github/workflows/` exists, check it references correct versions and commands

#### site

For each target registered under `## site`:

1. **Build check**: run the site build command, must pass clean
2. **Content sync**: if docs are synced from a source directory, check for drift
3. **Navigation completeness**: every doc should appear in sidebar/nav config
4. **Asset check**: referenced assets should exist
5. **Broken links**: scan for references to deleted files

#### deps

For each target registered under `## deps`:

1. **Dependency freshness**: run package manager outdated commands (npm outdated, pip list --outdated, cargo outdated, etc.)
2. **Lock file consistency**: lock files match manifests
3. **Security vulnerabilities**: run `npm audit`, `pip audit`, or equivalent if available

#### playbook

For each target registered under `## playbook`:

1. **Existence**: does `docs/playbook.md` exist? If not, high severity ("No playbook found. Run `/kerd:tend` to create one from the skeleton.")
2. **Current Status accuracy**: compare the "Current Status" section against actual project state (working build, test results, deployed state if detectable)
3. **Tech stack drift**: are the tools/frameworks listed in the playbook still in `package.json` / `pyproject.toml` / equivalent? Flag removed or added deps not reflected in playbook
4. **Setup steps validity**: do the setup commands reference files and scripts that still exist?
5. **Freshness**: when was playbook last modified relative to recent commits? If 10+ commits have landed since the last playbook update, flag as medium
6. **Section completeness**: are any major sections empty or still showing skeleton placeholder text?

#### release

Kerd-specific release audit. Checks the release checklist rules from CLAUDE.md automatically. Only runs when slainte detects `.claude-plugin/plugin.json` (i.e., in the Kerd repo itself or a Kerd-like plugin repo).

1. **Version sync**: compare version strings across `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` `metadata.version`, and `.claude-plugin/marketplace.json` `plugins[0].version`. All three must match. Any mismatch is high severity.
2. **Description sync**: compare `description` in `plugin.json` with `plugins[0].description` in `marketplace.json`. They must match. Mismatch is medium severity.
3. **Skill count consistency**: count `skills/*/SKILL.md` files and compare against claims in `README.md` (e.g., "Nine workflow skills") and `docs/playbook.md`. Mismatches are high severity.
4. **Mode count consistency**: count `modes/*.md` files and compare against claims in `README.md` mode table rows. Mismatch is medium severity.
5. **SKILL frontmatter drift**: for each `skills/*/SKILL.md`, verify the `name` field matches the directory name. Flag mismatches as high.
6. **Namespace sweep**: scan all `skills/*/SKILL.md` files for slash-command references missing the `kerd:` prefix (e.g., `/conductor` instead of `/kerd:conductor`). Skip README.md (allowed shorthand). Each hit is medium severity.
7. **Marketplace URL**: verify `.claude-plugin/marketplace.json` `plugins[0].source.url` points to the canonical repo (not a fork). Mismatch is high severity.
8. **Cross-doc claim verification**: verify that claims made in docs match the code and each other:
   - README "What's New" version numbers match the actual current version in plugin.json. If the latest What's New entry references a version that doesn't match the current version, flag as medium.
   - README skill descriptions match SKILL.md behavior. For each skill section in README, spot-check 2-3 specific claims (e.g., "conductor does not write session logs") against the actual SKILL.md. Flag contradictions as high.
   - `docs/playbook.md` "Working" list matches actual skill set and feature claims. Flag stale claims as medium.
   - `docs/state-contract.md` ownership table matches actual skill behavior. For each W (write) entry, verify the skill actually writes to that file. For each `-` (no interaction), verify the skill doesn't reference that file. Flag contradictions as high.
   - Vault Status.md version matches plugin.json version. Mismatch is low (vault is updated by kivna save, may lag by a session).
9. **Hook template currency**: verify `hooks/hooks.template.json` exists, is valid JSON, and references hook scripts that exist in `hooks/`. Flag missing scripts as high. Verify the template is not named `hooks.json` (would auto-load). Flag as high if found.

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

### Evidence specification

Each finding must include an **Evidence** column entry — the specific check that detected it: file:line reference, command run with output, grep result, version comparison, or doc citation. "References old project name" without a line number or grep result is unverifiable; "References old project name (grep 'OldName' → 3 hits at lines 12, 47, 89)" is reproducible. This applies to ALL severity levels — even `low` findings get a citation, because a finding without evidence is a claim without a source.

If a finding cannot be cited (e.g. cross-doc drift detected through reading rather than a specific command), record the comparison method explicitly: "compared README.md `## Skills` count to `skills/` directory count: README says 9, directory has 10."

### Severity guide:
- **high**: factually wrong, broken build, missing file, security vulnerability
- **medium**: stale but not misleading, cosmetic inconsistency
- **low**: nitpick, style drift, minor staleness
