---
name: sotu
description: "Use when the user says 'sotu', 'audit', 'health check', 'check staleness', 'state of the union', or needs to audit project health across docs, code, site, or dependencies. Read-only audit that reports issues without fixing them."
---

# SOTU (State of the Union)

Read-only audit of project health. Reports issues with severity grades. Does not fix anything. That's the user's call.

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

## playbook
- docs/playbook.md
```

## Commands

### `/sotu` (no args)

Show the current `.sotu` config: what's registered under each area. If no config exists, say so and offer to create one.

### `/sotu add <area> <path>`

Register a file or directory under an area. Create `.sotu` if it doesn't exist. Valid areas: `docs`, `code`, `site`, `deps`, `playbook`.

Example: `/sotu add docs README.md`

### `/sotu <area>`

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

1. **Existence**: does `docs/playbook.md` exist? If not, high severity ("No playbook found. Run a dian session to create one.")
2. **Current Status accuracy**: compare the "Current Status" section against actual project state (working build, test results, deployed state if detectable)
3. **Tech stack drift**: are the tools/frameworks listed in the playbook still in `package.json` / `pyproject.toml` / equivalent? Flag removed or added deps not reflected in playbook
4. **Setup steps validity**: do the setup commands reference files and scripts that still exist?
5. **Freshness**: when was playbook last modified relative to recent commits? If 10+ commits have landed since the last playbook update, flag as medium
6. **Section completeness**: are any major sections empty or still showing skeleton placeholder text?

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
- **high**: factually wrong, broken build, missing file, security vulnerability
- **medium**: stale but not misleading, cosmetic inconsistency
- **low**: nitpick, style drift, minor staleness
