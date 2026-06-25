# TODO

## Current Session
(2026-06-25 — forward-only handoff; Kerd tree clean, session state pushed)

### What's next
- **skriv voice profile — decide wiring, then gather more samples.** First-pass profile captured at `~/eolas/vault/people/Anthony Maley Voice.md` (Approach A, n=1, founder-narrative genre), cross-linked from the person file. **Open decision the user did not resolve before wrapping:** wire skriv to load the profile (skill change → full release checklist + version bump) live now, OR hold until samples in non-founder genres (technical post, short update) generalize it. The profile is inert until skriv is wired — nothing reads it yet.
- **Heavier phase — wire the spine into the skills.** Wire full-spine creation (MOC + Status + Weekly) + the intake interview into `kivna scaffold`, and spine-drift detection into `tend`. Currently kivna seeds MOC + Status only; `docs/vault-spec.md` documents the target convention and carries a rollout note. Skill behavior change → full release checklist + version bump.
- **Clean krutho-strategy's stray `sessions-of-record/`.** Legacy drift — session history is repo-side now. Remove or grandfather it.
- Architecture / skill-review threads remain open (see Backlog): spike mode, interrogate smoke test, Path B.

### Context
- **TODO is forward-only (v0.41.0).** This block is overwritten each switch-out; completed work lives in `kivna/sessions/`. Switch out self-heals stray `## Previous Session` blocks (rescue-before-delete).
- **The vault (`~/eolas/vault`) is a separate git repo that switch-out does NOT commit.** It carries ~20 uncommitted files across many projects/activities (coaching notes, digests, idea captures, several `Status.md`). This session's two vault files (`people/Anthony Maley.md` + `people/Anthony Maley Voice.md`) are written-but-uncommitted among them. Open question tracked in Backlog: should switch own vault commits?
- **skriv voice-profile design decision:** "never read as AI-written" is the top priority; voice traits yield to anti-AI rules on collision. The one real collision is vague self-promotional superlatives → convert to a concrete fact.
- Decision (prior): session history stays repo-side (`kivna/sessions/`), never the vault.
- Architecture design (2026-06-06) still in-progress: mode redesign ~30% (briefs 16/16, full specs 2/16); next mode is spike. Detail in `docs/plans/2026-05-04-skill-architecture-review.md`.

## Backlog
- **skriv voice profile (first-pass built — needs wiring decision + more samples).** Approach A profile captured at `~/eolas/vault/people/Anthony Maley Voice.md` from one sample (Vouch/Krutho founder-origin draft), cross-linked from the person file. Decision locked: "never read as AI-written" wins all collisions; voice applies on top. Still open: (1) wire skriv to load the profile (skill change → release checklist + version bump) now vs hold; (2) more samples in non-founder genres (technical post, short update) to generalize past founder-narrative; (3) selective Strunk borrowing (concreteness/strength rules only) not yet applied. Goal unchanged: sounds like the user AND avoids the AI feel, for public use.
- **Decide whether switch should commit the vault repo.** The vault (`~/eolas/vault`) is a separate git repo carrying ~20 uncommitted files accumulating across sessions; switch-out writes to it (kivna save, person files) but never commits it, despite the skill claiming to "own all git boundary operations: pull, push, commit of session state." Either switch should stage+commit its own vault writes, or vault sync is intentionally manual and the skill's contract wording overreaches. Resolve which — don't leave the contract and the behavior disagreeing.
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
