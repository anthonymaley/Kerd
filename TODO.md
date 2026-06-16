# TODO

## Current Session
(2026-06-16 — forward-only handoff; tree clean, all work pushed)

### What's next
- **Heavier phase — wire the spine into the skills.** Wire full-spine creation (MOC + Status + Weekly) + the intake interview into `kivna scaffold`, and spine-drift detection into `tend`. Currently kivna seeds MOC + Status only; `docs/vault-spec.md` documents the target convention and carries a rollout note tracking the gap. Skill behavior change → full release checklist + version bump when done.
- **Clean krutho-strategy's stray `sessions-of-record/`.** `~/eolas/vault/krutho-strategy/sessions-of-record/` is legacy drift — session history is repo-side now. Remove or grandfather it so the reference vault stops modeling the wrong thing.
- Architecture / skill-review threads remain open (see Backlog): spike mode, interrogate smoke test, Path B, skriv voice profile.

### Context
- **TODO is now forward-only (v0.41.0).** This block is overwritten each switch-out; completed work lives in `kivna/sessions/`. No `## Previous Session` accumulation — switch out self-heals any that appear (rescue-before-delete).
- Decision this session: **session history stays repo-side (`kivna/sessions/`), never the vault.**
- Architecture design (2026-06-06) still in-progress: mode redesign ~30% (briefs 16/16, full specs 2/16); next mode is spike. Detail in `docs/plans/2026-05-04-skill-architecture-review.md` + the 2026-06-06 session log.

## Backlog
- **skriv voice profile (parked — needs user input).** Build Approach A: a persisted voice profile derived from the user's real writing, stored user-global at `~/eolas/vault/people/Anthony Maley Voice.md`, applied on top of skriv's existing anti-AI rules. Selective Strunk borrowing only — take concreteness/strength rules, reject topic-sentence and uniform-sentence rules (they flatten voice). **Blocked on:** user to provide writing samples. Goal: content sounds like the user AND avoids the AI feel, for public use.
- **slainte auto-trigger idea.** Fold a light slainte pass into switch-in so drift gets caught without manual invocation. Under-use is the problem, not capability (the stale MOC version is the kind of thing it'd catch).
- **kivna / vault-spec question.** User says the vault is "mostly for LLM to read context" — its primary consumer is the cold-LLM-read at session start, not human Obsidian browsing. Revisit whether the human-first Status/Weekly/MOC structure is optimized for the right reader. (Partly addressed by the 2026-06-16 spine fold; the reader-optimization question remains.)
- **First interactive smoke test of `/kerd:interrogate`** — meta path (interrogate the design doc) or real path (next upcoming idea). Watch for: declaring done before user-veto, response verbosity, multiple-choice slips, sliding sideways instead of drilling.
- **Path B (paused) — Stop hook + PostToolUse hook at genuinely different granularity.** Decision rule unchanged: ship only if Path A reframe + interrogate's structural anchors don't shift behavior measurably. User-pushback rate is the externally-anchored truth signal.
- **Spike mode v1 retro** — pending after measurable-baseline test. Watch: does N+1 batching produce useful additions or noise? Does wins+losses recording complement TODO? Does commit-graduation help mid-flight?
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults.
- PPS marketplace.json fix from prior session — still unpushed/unregistered.
- Hook version pinning is a recurring manual burden. Consider adding hook version staleness check to /kerd:tend.
- Stale `Kerd.md` MOC version field (says 0.31.0 vs actual 0.41.0) — either update on every release or remove entirely (lean remove).
- Solicit community mode contributions.
