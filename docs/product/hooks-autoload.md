---
route: problem
stage: scoped
---

# Hooks auto-load — the plugin ships its own hooks, so they never break on update

## Value

Tony's requirement, in his words (2026-08-13, stated live after finding Kerd
hooks silently dead across eleven repos because each was wired to a plugin-cache
version that had since been garbage-collected):

> we need to fix this in the standard way to do it so that 1. it never breaks
> 2. when users update kerd skill it doesnt break, 3. standard mechanism that
> skills should use and users expect

The measure of winning: a user installs or updates Kerd and its hooks work with
zero per-repo wiring, and a Kerd version bump never leaves a stale path behind.

## Grounding

- docs/playbook.md — the GC-pin-rot gotcha (2026-07-11): Claude Code garbage-collects old cache versions, so a repo pinned to a pruned version's hook path breaks silently, even in repos never touched. The exact failure being fixed.
- skills/tend/SKILL.md — Category 9, the current wiring mechanism (manual, version-pinned absolute paths in each repo's settings.local.json) that this replaces.

(External: Claude Code plugin docs at code.claude.com/docs/en/plugins-reference.md, verified live 2026-08-13 via claude-code-guide — a plugin's hooks/hooks.json is auto-registered on enable, and ${CLAUDE_PLUGIN_ROOT} expands there but NOT in user settings.local.json. Recorded in the risk-ledger evidence below.)

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
|---|---|---|---|---|---|---|---|---|---|
| Auto-load doesn't actually fire on this machine — the docs are right in principle but the harness build here behaves differently | yes | the whole fix is inert: hooks silently absent everywhere instead of silently broken | unknown until tested | claude-code-guide confirmed from live docs but flagged "tested but not yet verified" empirically; no fresh-session observation yet | fatal | countermeasure - permanent | Empirical fresh-session check before the task is called done: a repo with no manual entries must see pair/session-start fire from the plugin alone |  | Fires if a future harness update stops auto-loading plugin hooks |
| Stripping a consumer repo's manual entries before its cache repins to the version shipping hooks.json leaves that repo with no hooks in the gap | no | brief window with no Kerd hooks in that repo — identical to today, where the pinned path is already dead | certain but harmless | the eleven repos already point at pruned versions, so their manual hooks are already non-functional; stripping loses nothing working | non-fatal | countermeasure - permanent | Strip is safe regardless of repin order because broken == absent; auto-load activates on repin |  |  |
| Cutting stop.sh removes the only live surfacing of the conductor phase-stamp to the human at turn-end | no | the stamp is still written to the marker and read into CONTEXT.md; only the free turn-end echo is lost | certain | `state-contract.md:89`, `time-awareness.md:28` — stop.sh echoes the whole conductor line | non-fatal | accepted |  |  | Fires if the turn-end stamp surfacing is missed enough to want a replacement |
## Scope

Rigor level: mvp

The whole fix, shipped as one proportional build (design settled in conversation
2026-08-13, so no separate design/contract rung):

- `hooks/hooks.json` created (pair, session-start, skill-complete — `${CLAUDE_PLUGIN_ROOT}` paths), auto-loaded by the harness on enable.
- `hooks/stop.sh` cut; `hooks/hooks.template.json` retired (superseded by the real auto-loaded file).
- `skills/tend/SKILL.md` Category 9 rewritten: no manual version-pinned wiring; instead confirm the plugin auto-provides hooks and offer to strip stale manual entries.
- Living docs de-referenced (README, state-contract, time-awareness, playbook, the test harness). Immutable records untouched.
- The eleven consumer repos migrated off their dead pinned paths.
- Version 0.95.0 → 0.96.0; release checklist run.

Deliberately excluded: any automated cross-repo repin mechanism (the cache still
updates through the normal plugin-update path); the statusline segment (separate,
not a hook).
