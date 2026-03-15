# TODO

## Current Session
(no active session)

### Done This Session
- [x] Added tend skill (v0.8.0) — structural health check replacing startup
- [x] Added discover skill (v0.9.0) — skill gap analysis with three tiers
- [x] Renamed vault path ~/ObsidianLLM → ~/Obsidian (v0.9.1)
- [x] Updated tend Category 3 with vault advisory for unconfigured projects
- [x] Updated kivna scaffold to ask for vault location instead of assuming
- [x] Created .gitignore (was on backlog)
- [x] Ran tend on Kerd repo — fixed 8 missing symlinks, removed commands/, deleted stray screenshots/DS_Store
- [x] Designed discover skill through full brainstorming process

## Backlog
- Restart Claude Code and test /kerd:tend and /kerd:discover live (new skills need restart)
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate them to vault
- Re-open Obsidian vault pointing to ~/Obsidian/ (manual step)
- Test sotu playbook audit on a project with a playbook
- Implement discover skill (design complete, not yet tested live)
- Adopt third-person description format for skill triggers (low priority)
- Description optimization for skill triggers (low priority — eval harness limitations)

### Context
- Version is now 0.9.1
- Plugin update command is `claude plugin update kerd@kerd-marketplace`
- marketplace.json URL uses ssh format (git@github.com:) — intentional
- discover-sources.json seeded in vault with 2 repos and 1 URL
- Vault renamed from ~/ObsidianLLM to ~/Obsidian — need to re-open in Obsidian app
