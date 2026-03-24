# TODO

## Current Session
(no active session, last completed 2026-03-24)

### Done this session
- [x] Ran `/kerd:kivna save` — updated vault Status.md, created first Weekly.md, MOC link
- [x] Added `/kerd:lorg report` subcommand (v0.15.0)
- [x] Added `light` modifier to switch for lower-token handoffs (v0.16.0)
- [x] Updated README, playbook, vault Usage Guide for v0.15.0 and v0.16.0
- [x] Reviewed GSD (get-shit-done) and Hail repos, wrote landscape analysis
- [x] Designed workflow routing table (Kerd + GSD + Superpowers)
- [x] Designed modes feature: session configurations with customizable flows
- [x] Built mode skill and 9 starter modes (v0.17.0)
- [x] Updated all docs: README, CLAUDE.md, playbook, vault MOC, vault Status, vault Usage Guide, vault Workflow Routing

## Backlog
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults
- Update vault.json in other repos to point to ~/eolas/vault/
- Re-open Obsidian vault in app pointing to ~/eolas/vault/ (manual step)
- Test slainte playbook audit on a project with a playbook
- Test /kerd:mode greenfield in a real build session
- Solicit community mode contributions
- Adopt third-person description format for skill triggers (low priority)

### Context
- Version is 0.17.0
- Vault path is now ~/eolas/vault/ (changed from ~/Obsidian/)
- Mode skill orchestrates across Kerd, GSD, Superpowers, and other plugins
- 9 starter modes: greenfield, quickfix, deepwork, maintain, strategy, writing, research, legal, sales
- Modes are community-contributed: PR a single .md to modes/
- Switch light modifier: /switch out light and /switch in light skip vault, reflection, smoke test
- Lorg report subcommand: /lorg report shows last saved report
- Plugin update command is `claude plugin update kerd@kerd-marketplace`
- marketplace.json URL uses ssh format (git@github.com:), intentional
- Tend now has Category 8 (Skill hygiene) to catch missing kerd: prefixes and stale skill names
