# TODO

## Current Session
(no active session, last completed 2026-03-17)

### Done this session
- [x] Updated skriv rule: ban all dashes as punctuation (em, en, double hyphens)
- [x] Cleaned all em dashes from every living file (14 files, 295 replacements), v0.10.1
- [x] Renamed sotu→slainte, switch→seach, discover→lorg to avoid superpowers collisions, v0.11.0
- [x] Updated all cross-references, manifests, vault files, CHANGELOG
- [x] Committed and pushed

## Backlog
- Restart Claude Code to pick up v0.11.0
- Run /kerd:tend on krutho-founders, krutho-strategy, obair. Will flag old symlinks and Context.md/Log.md for removal
- Build out Kerd vault files: Playbook, Usage Guide, Architecture Decisions, Install Guide
- Re-open Obsidian vault pointing to ~/Obsidian/ (manual step)
- Clean old vault files from ~/Obsidian/kerd/ (symlinks, Context.md, Log.md, Decisions.md). Tend will flag these
- Test slainte playbook audit on a project with a playbook
- Adopt third-person description format for skill triggers (low priority)
- Description optimization for skill triggers (low priority, eval harness limitations)

### Context
- Version is now 0.11.0
- Skills renamed: sotu→slainte, switch→seach, discover→lorg
- Config file .sotu renamed to .slainte, old .sotu in tend's deprecated patterns
- Plugin update command is `claude plugin update kerd@kerd-marketplace`
- marketplace.json URL uses ssh format (git@github.com:), intentional
- discover-sources.json in vault with 9 repos and 6 URLs (filename NOT renamed)
- Vault redesign shipped: no symlinks, living Status.md, approval-gated overwrites, vault spec at docs/vault-spec.md
- Old vault files (Context.md, Log.md, Decisions.md) still exist in ~/Obsidian/kerd/. Need cleanup via /kerd:tend
