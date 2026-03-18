# TODO

## Current Session
(no active session, last completed 2026-03-18)

### Done this session
- [x] Added weekly tracker to Kivna save (v0.14.0) — new `[Name] Weekly.md` vault file for achievements/risks
- [x] Renamed shakh back to switch — no superpowers collision existed, confirmed by scanning plugin cache
- [x] Removed deprecated `.sotu` config, created `.slainte` with expanded targets
- [x] Ran first slainte audit — found and fixed stale refs (sotu in lorg, missing kerd: prefixes in switch/skriv)
- [x] Added tend Category 8 (Skill hygiene) to catch prefix and stale name issues automatically
- [x] Updated vault-spec.md with Weekly file type
- [x] Fixed version in TODO context (was 0.13.0, now 0.14.0)

## Backlog
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults
- Update vault.json in other repos to point to ~/eolas/vault/
- Re-open Obsidian vault in app pointing to ~/eolas/vault/ (manual step)
- Test slainte playbook audit on a project with a playbook
- Adopt third-person description format for skill triggers (low priority)
- Description optimization for skill triggers (low priority, eval harness limitations)

### Context
- Version is 0.14.0
- Vault path is now ~/eolas/vault/ (changed from ~/Obsidian/)
- Switch skill restored to plain English name (was shakh, then seach, originally switch)
- Plugin update command is `claude plugin update kerd@kerd-marketplace`
- marketplace.json URL uses ssh format (git@github.com:), intentional
- Tend now has Category 8 (Skill hygiene) to catch missing kerd: prefixes and stale skill names
