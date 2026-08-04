# Contributing to Kerd

Kerd accepts contributions for new skills, skill improvements, and bug fixes. This doc sets expectations for PRs.

## Skills

Skill PRs change behavior. They require scrutiny.

**Before opening a PR:**
1. Fork and branch from `main`
2. One skill per PR. Don't bundle unrelated changes.
3. Run `/kerd:slainte release` against your branch. Fix any findings before opening.

**Your PR must include:**
- `skills/<name>/SKILL.md` with valid frontmatter (`name`, `description`)
- Updated `README.md` section for the skill
- Updated `docs/playbook.md` skill list and working/recent-changes sections
- Version bump in all 3 locations (see below). New skill = minor bump.
- Updated plugin descriptions in `plugin.json` and `marketplace.json` if the high-level scope changed

**Your PR must NOT include:**
- Changes to files unrelated to the skill (`.gitattributes`, CI config, line-ending normalization)
- Version bumps that skip numbers (bump from the current version on `main`, not from your fork's version)
- Marketplace URL changes (must always point to `anthonymaley/Kerd`)
- Plan or design docs in `docs/plans/` (keep those in your fork; the skill itself is the deliverable)

## Version bumps

Three files, always in sync:
- `.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → `metadata.version`
- `.claude-plugin/marketplace.json` → `plugins[0].version`

Semver: PATCH for bug fixes, MINOR for new skills or behavior changes, MAJOR for breaking changes.

## Review process

1. Open a PR against `main`
2. Maintainer reviews for: skill quality, doc completeness, version correctness, no scope creep
3. If the PR branch drifts too far from `main`, the maintainer may cherry-pick the skill content rather than merge. Contributor credit is preserved via `Co-Authored-By`.
4. Merged or cherry-picked work is published immediately (push after commit).

## What makes a good skill

- **Single responsibility.** One skill does one thing. If you need "and" to describe it, it might be two skills.
- **User confirmation before destructive actions.** Archive, delete, overwrite — always ask first.
- **No external dependencies.** Kerd is pure markdown + JSON + bash. No npm, no pip, no build step.
- **Concrete, not vague.** "Scan `docs/` for files with 'spec' in the filename" beats "look for relevant documents."
- **Boundary-aware.** Know what your skill owns and what belongs to other skills. Check `docs/state-contract.md`.

## What NOT to PR

- Skills that duplicate existing skill behavior (check the README first)
- Skills that require API keys or external services
- Skills tightly coupled to a specific plugin (e.g., hardcoding `superpowers:brainstorming` as a required step)
- Repo-wide configuration changes (discuss in an issue first)
