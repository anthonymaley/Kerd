# TODO

## Current Session
(2026-06-10, switching out)

### Done this session
- [x] Ran `/kerd:tend` — structure clean. Fixed vault MOC (added `Kerd Skill Lessons` link), removed 4 stray `.DS_Store`. Withdrew a false-positive after verifying: `discover-sources.json` is lorg-required at its exact vault path, not a stray file.
- [x] Started a **usage-driven skill review** — the deferred "skill assessment phase" from `docs/plans/2026-05-04-skill-architecture-review.md`, approached from how each skill is actually used rather than capability theory.
- [x] **switch → v0.40.0 (prose only, behavior unchanged):** reframed session-handoff-first, machine-swap secondary. Verified artifacts are identical across same-machine restart vs cross-machine, so no behavior change was needed. Title, intro, usage, section headers, frontmatter trigger (added `save context`), README, and capability list all session-first.
- [x] **dian → v0.40.0 (behavior change):** slimmed to "the disciplined middle." Orient now conditional (warm: confirm what switch-in loaded; cold: light TODO+Status). Close-out 9→5 steps — vault save, playbook update, diff review, staleness sweep handed to switch. Execute gates kept but made self-contained for users without a global CLAUDE.md. Ripple fixed: switch step 3 (sole kivna-save caller), state-contract ownership, slainte playbook hint, `modes/deepwork.md`, README.
- [x] **skriv reviewed, parked** pending writing samples (see Backlog).

### Context
- One continuous session: began 2026-06-06 (tend + switch-in onto the architecture thread), closed 2026-06-10.
- **Skill-review verdicts so far:** switch ✓ reframed · dian ✓ slimmed · skriv parked · tend = no change · kivna = plumbing (used via switch; open vault-spec question below) · slainte = under-used (idea below).
- dian slim is a deliberate **stepping-stone** to the design doc's eventual `plan`/`execute` modes; nothing here undoes that.
- **Calibration corrected mid-session:** dian's gate "duplication" is duplication only FOR THIS USER (has global CLAUDE.md gates); for strangers installing Kerd the gates are load-bearing — kept, made self-contained.
- Architecture design (2026-06-06) still in-progress: mode redesign ~30% (briefs 16/16, full specs 2/16); next mode is spike. Detail in the design doc + 2026-06-06 session log.
- `CHANGELOG.md` abandoned (last entry 0.14.0, repo at 0.40.0) — README "What's New" is the living changelog. Separate staleness finding.

## Backlog
- **skriv voice profile (parked — needs user input).** Build Approach A: a persisted voice profile derived from the user's real writing, stored user-global at `~/eolas/vault/people/Anthony Maley Voice.md`, applied on top of skriv's existing anti-AI rules. Selective Strunk borrowing only — take concreteness/strength rules, reject topic-sentence and uniform-sentence rules (they flatten voice). **Blocked on:** user to provide writing samples. Goal: content sounds like the user AND avoids the AI feel, for public use.
- **slainte auto-trigger idea.** Fold a light slainte pass into switch-in so drift gets caught without manual invocation. Under-use is the problem, not capability (the stale MOC version this session is the kind of thing it'd catch).
- **kivna / vault-spec question.** User says the vault is "mostly for LLM to read context" — its primary consumer is the cold-LLM-read at session start, not human Obsidian browsing. Revisit whether the human-first Status/Weekly/MOC structure is optimized for the right reader.
- **First interactive smoke test of `/kerd:interrogate`** — meta path (interrogate the design doc) or real path (next upcoming idea). Watch for: declaring done before user-veto, response verbosity, multiple-choice slips, sliding sideways instead of drilling.
- **Path B (paused) — Stop hook + PostToolUse hook at genuinely different granularity.** Decision rule unchanged: ship only if Path A reframe + interrogate's structural anchors don't shift behavior measurably. User-pushback rate is the externally-anchored truth signal.
- **Spike mode v1 retro** — pending after measurable-baseline test. Watch: does N+1 batching produce useful additions or noise? Does wins+losses recording complement TODO? Does commit-graduation help mid-flight?
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults.
- PPS marketplace.json fix from prior session — still unpushed/unregistered.
- Hook version pinning is a recurring manual burden. Consider adding hook version staleness check to /kerd:tend.
- Stale `Kerd.md` MOC version field (says 0.31.0 vs actual 0.39.0) — either update on every release or remove entirely (lean remove).
- Solicit community mode contributions.
