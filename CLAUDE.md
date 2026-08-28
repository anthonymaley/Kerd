# Kerd

Claude Code plugin: ten workflow skills for driving a work item from idea to acceptance, session discipline, risk qualification, session and machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, and conversational pair mode.

## Commit Rules

- **Always push after committing.** Every commit goes to remote immediately.
- **Always run the release checklist before committing.** Version bumps, README updates, and description updates happen before the commit, not after.

## Release Checklist

Every change to a skill (new skill, modified behavior, renamed command, changed output) requires ALL of the following before commit:

1. **Bump version** in all three locations (keep them in sync):
   - `.claude-plugin/plugin.json` → `version`
   - `.claude-plugin/marketplace.json` → `metadata.version`
   - `.claude-plugin/marketplace.json` → `plugins[0].version`

2. **Update README.md**. If the skill's behavior, usage, or output changed, update its section in the README. If a new skill was added, add a new section following the existing pattern.

3. **Update plugin descriptions**: if the change affects what Kerd does at a high level, update both *capability-list* locations and keep them byte-identical:
   - `.claude-plugin/plugin.json` → `description` (capability list)
   - `.claude-plugin/marketplace.json` → `plugins[0].description` (capability list — same string as plugin.json above)

   The `metadata.description` field in `marketplace.json` is intentionally a different shape — a marketplace one-liner ("Kerd: opinionated workflow skills…"), not the capability list. Don't homogenize them. Update `metadata.description` only when the marketplace summary itself needs to change (rebrand, scope shift), as a separate decision.

4. **Update skill trigger description**: the `description` field in the skill's SKILL.md frontmatter controls when Claude invokes it. If behavior changed, update the trigger description to match.

5. **Namespace references**: all slash-command references in docs and skills must use the `kerd:` prefix (e.g., `/kerd:tend`, `/kerd:conductor`). The only exception is within README.md examples showing shorthand usage, which may omit the prefix for readability.

CI enforces the mechanical subset of this checklist on every push: `python3 tools/gates/gate.py release` refuses version drift (item 1), capability-list drift (item 3), and bare slash references (item 5).

## Version Strategy

Use semver: `MAJOR.MINOR.PATCH`
- **PATCH**: bug fixes, wording tweaks, internal refactors with no behavior change
- **MINOR**: new skill, new feature within a skill, changed behavior
- **MAJOR**: breaking changes to skill interfaces or directory conventions

## Project Structure

```
skills/           # skill definitions (each skill in its own folder with SKILL.md)
tools/gates/      # entry-gate ladder + release/audit/fidelity checks (gate.py, kit.py, fidelity.py)
tools/diagram/    # progress board and journey renders
tools/design/     # the evaluation-matrix checker
docs/product/     # the funnel board — one <slug>.md per work item, written at the frame stage
docs/work/question-sets/ # seed question sets, one <work-type>.md, copied into a work record at intake
docs/design/      # living design docs (undated filenames — CI-enforced)
docs/gates/       # dated gate records, immutable
docs/plans/       # dated contract specs and generated progress renders
docs/playbook.md  # living project guide, updated by conductor close-out
docs/state-contract.md # who owns and reads CONTEXT.md, TODO.md, kivna/sessions/
CONTEXT.md        # current state, overwritten each session
TODO.md           # open work (## Now + ## Backlog)
hooks/            # session hooks (statusline, pair toggle, session-start/stop, skill-complete)
tests/            # hooks_test.sh
kivna/vault.json  # Obsidian vault config
kivna/sessions/   # session logs from switch (committed)
.claude-plugin/   # plugin.json and marketplace.json
.github/workflows/gate.yml # the entry-gate workflow
```

## Conventions

- Skill names are lowercase, single-word, Gaelic-inspired where it adds character
- Skills define behavior. The plugin system loads them directly via the `kerd:` prefix.
- SKILL.md frontmatter `name` field is the local name only (no `kerd:` prefix, the plugin system adds it)
- All cross-skill references use `/kerd:<skill>` format
