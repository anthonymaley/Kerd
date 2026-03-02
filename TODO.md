# TODO

## Current Session

**Date:** 2026-03-02
**Machine:** Mac.attlocal.net

### Done
- [x] Added verify step to switch skill — blocks handoff if uncommitted changes remain
- [x] Brainstormed and designed playbook integration, sotu playbook area, and startup skill
- [x] Updated dian skill — playbook in orient read list, create/update playbook in close-out
- [x] Updated sotu skill — new playbook audit area with 6 checks
- [x] Created startup skill — scaffolds new projects with Kerd conventions
- [x] Updated README with all new skills and features
- [x] Bumped plugin version to 0.2.0, pushed, and verified plugin update works

### In Progress
- Nothing in progress

### Next
- Test startup skill on a fresh repo
- Test dian's playbook creation on first close-out in a real project
- Test sotu playbook audit on a project with a playbook
- Consider adding version bumping to the switch out process (or a separate release skill)

### Context
- Playbook concept borrowed from ~/klar/ project — a living rebuild guide updated every session
- Plugin update command is `claude plugin update kerd@kerd-marketplace` (full qualified name required)
- marketplace.json URL uses ssh format (git@github.com:) — this is intentional, was resolved last session
