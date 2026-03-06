# Kerd

Claude Code plugin: six workflow skills for session discipline, machine handoff, knowledge management, project audits, human writing voice, and project scaffolding.

## Commit Rules

- **Always push after committing.** Every commit goes to remote immediately.
- **Always run the release checklist before committing.** Version bumps, README updates, and description updates happen before the commit, not after.

## Release Checklist

Every change to a skill (new skill, modified behavior, renamed command, changed output) requires ALL of the following before commit:

1. **Bump version** in all three locations (keep them in sync):
   - `.claude-plugin/plugin.json` → `version`
   - `.claude-plugin/marketplace.json` → `metadata.version`
   - `.claude-plugin/marketplace.json` → `plugins[0].version`

2. **Update README.md** — if the skill's behavior, usage, or output changed, update its section in the README. If a new skill was added, add a new section following the existing pattern.

3. **Update plugin descriptions** — if the change affects what Kerd does at a high level, update:
   - `.claude-plugin/plugin.json` → `description`
   - `.claude-plugin/marketplace.json` → `metadata.description`
   - `.claude-plugin/marketplace.json` → `plugins[0].description`

4. **Update skill trigger description** — the `description` field in the skill's SKILL.md frontmatter controls when Claude invokes it. If behavior changed, update the trigger description to match.

5. **Namespace references** — all slash-command references in docs and skills must use the `kerd:` prefix (e.g., `/kerd:startup`, `/kerd:dian`). The only exception is within README.md examples showing shorthand usage, which may omit the prefix for readability.

## Version Strategy

Use semver: `MAJOR.MINOR.PATCH`
- **PATCH** — bug fixes, wording tweaks, internal refactors with no behavior change
- **MINOR** — new skill, new feature within a skill, changed behavior
- **MAJOR** — breaking changes to skill interfaces or directory conventions

## Project Structure

```
skills/           # skill definitions (each skill in its own folder with SKILL.md)
commands/         # command definitions (markdown, one per command)
docs/plans/       # design docs and implementation plans
docs/playbook.md  # living project guide, updated by dian close-out
kivna/context.md  # living working context, overwritten each checkpoint
kivna/checkpoints/ # daily archives of previous context versions
kivna/sessions/   # session logs from switch (committed)
kivna/memories/   # quick notes from kivna memory (committed)
kivna/input/      # drop files here for kivna import (gitignored)
kivna/output/     # kivna exports land here (gitignored)
.claude-plugin/   # plugin.json and marketplace.json
```

## Conventions

- Skill names are lowercase, single-word, Gaelic-inspired where it adds character
- Skills define behavior. Commands are thin wrappers that invoke skills.
- SKILL.md frontmatter `name` field is the local name only (no `kerd:` prefix — the plugin system adds it)
- All cross-skill references use `/kerd:<skill>` format
