# TODO

## Current Session
(no active session, last completed 2026-03-17)

### Done this session
- [x] Updated skriv rule: ban all dashes as punctuation (em, en, double hyphens), not just em dashes
- [x] Cleaned all em dashes from every living file in the project (14 files, 295 replacements)
- [x] Bumped version to 0.10.1
- [x] Committed and pushed

## Backlog
- Restart Claude Code and test /kerd:tend and /kerd:discover live (v0.10.0 needs restart)
- Run /kerd:tend on krutho-founders, krutho-strategy, obair. Will flag old symlinks and Context.md/Log.md for removal
- Build out Kerd vault files: Playbook, Usage Guide, Architecture Decisions, Install Guide
- Re-open Obsidian vault pointing to ~/Obsidian/ (manual step)
- Clean old vault files from ~/Obsidian/kerd/ (symlinks, Context.md, Log.md, Decisions.md). Tend will flag these
- Test sotu playbook audit on a project with a playbook
- Adopt third-person description format for skill triggers (low priority)
- Description optimization for skill triggers (low priority, eval harness limitations)

### Context
- Version is now 0.10.1
- Plugin update command is `claude plugin update kerd@kerd-marketplace`
- marketplace.json URL uses ssh format (git@github.com:), intentional
- discover-sources.json in vault with 9 repos and 6 URLs
- Vault redesign shipped: no symlinks, living Status.md, approval-gated overwrites, vault spec at docs/vault-spec.md
- Old vault files (Context.md, Log.md, Decisions.md) still exist in ~/Obsidian/kerd/. Need cleanup via /kerd:tend
- Cache still shows v0.9.2. Restart needed to pick up v0.10.0
