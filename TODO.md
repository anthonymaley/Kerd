# TODO

## Current Session
(2026-06-06, in progress)

### Done this session
- [x] Started a `/kerd:switch in` and pivoted into a full skill architecture audit triggered by dian's prompt verbosity and multiple-choice patterns surfacing as Question-formation gate (#7) violations.
- [x] Ran a 5-question survey across ~30 skills (Kerd + Superpowers + adjacent plugins). Surfaced 6 patterns, the biggest being "sequential chains aren't named — each skill is an island."
- [x] **Load-bearing reframe:** initial diagnosis of #1 was wrong-shaped (cross-references between skills); user pushed back — that's mode's job. Adopted **three-layer model**: skills atomic, modes orchestrators, discipline gates universal. One narrow exception: structural primitives (e.g., switch → kivna save).
- [x] **Plugin split (provisionally locked):** Kerd plugin = modes only. 9 skills (switch, dian, kivna, interrogate, skriv, tend, slainte, trim, lorg) move to a separate `kerd-skills` plugin. Gated by M12 (verify cross-plugin skill invocation works in Claude Code). May bundle some back if OOB UX requires.
- [x] **Mode set rewritten from 10 → 16:** 4 retired (deepwork, greenfield, quickfix, legal), 6 kept with rewrite (research, spike, strategy, writing, sales, maintain), 10 new (new idea, plan, interrogate, product design, adversarial review, problem analysis, execute, peer review reception, call transcript analysis, project-manage).
- [x] **Mode file format locked:** capability-first frontmatter (`capabilities: [id + description]`), per-step blocks (Goal / Do / Don't / Exit when / Produces), follow_on field with rationale. Steps reference capability id OR are inline actions.
- [x] **Critical correction mid-design:** initially named recommended skills in capability entries. User pushed back — defer skill naming entirely until mode design completes. Rewrote all 16 briefs to description-only capabilities. Skill mapping becomes its own deferred layer (capability id → skill, defined post-mode-design).
- [x] **Mode briefs (all 16) and full specs (modes 1 + 3) written** in design doc at `docs/plans/2026-05-04-skill-architecture-review.md`. Capability inventory aggregated across modes (~35 capabilities, 12+ recurring).
- [x] New skill identified: `email-writer` (domain-agnostic email iteration + paste-ready formatting). Capability gaps surfaced for skill assessment phase: persona work, project state retrieval, action item extraction.
- [x] Rename plan (R1–R4) absorbed into plugin-split migration as combined v1.0.0 effort. Gaelic names (dian, kivna, skriv, slainte, lorg) → English (session, vault, write, audit, discover) AND move to `kerd-skills` plugin.

### Context
- **No commits made this session.** All work in design doc — single untracked file: `docs/plans/2026-05-04-skill-architecture-review.md`.
- **Mode design ~30% complete by spec.** Briefs done for all 16 (capability-first, description-only). Full specs done for mode 1 (new idea, 11 steps / 5 phases) and mode 3 (interrogate, 7 steps / 4 phases). 14 modes still need full per-step expansion.
- **Suggested mode-by-mode sequence:** mode 4 (spike) next — tests how already-rich existing content reformats. Then maintain, project-manage (different shapes), then plan (heavily-referenced by follow_ons), then remaining 10.
- **Skill assessment phase is deferred** — does not start until all 16 modes are fully spec'd. At that point: match each capability description to a skill, name gaps, decide which Kerd skills update/drop/move.
- **Capability inventory is the load-bearing artifact** of this session. ~35 distinct capabilities aggregated from briefs, with `[recurring]` markers on those needed by 2+ modes. Recurring capabilities (session boundary, vault capture, idea exploration, web research, doc drafting, goal/decision framing, synthesis, persona work, response drafting, action item extraction, next-step decision) are where skill investment has highest leverage.
- **Open architectural question:** project-state file structure (TODO.md, sessions/, .active-modes) may need rethinking under new architecture. Captured as deferred — not in mode design scope.
- **Carryover from 2026-05-04:** interrogate smoke test on 3of3 still mid-stream (`3of3/docs/interrogations/2026-05-02-integration-spike.md`). New gates from 2026-05-04 not exercised in this session — full design focus instead.

## Backlog
- **First interactive smoke test of `/kerd:interrogate`** — meta path (interrogate the design doc) or real path (next upcoming idea). Watch for: declaring done before user-veto, response verbosity, multiple-choice slips, sliding sideways instead of drilling.
- **Path B (paused) — Stop hook + PostToolUse hook at genuinely different granularity.** Decision rule unchanged: ship only if Path A reframe + interrogate's structural anchors don't shift behavior measurably. User-pushback rate is the externally-anchored truth signal.
- **Spike mode v1 retro** — pending after measurable-baseline test. Watch: does N+1 batching produce useful additions or noise? Does wins+losses recording complement TODO? Does commit-graduation help mid-flight?
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults.
- PPS marketplace.json fix from prior session — still unpushed/unregistered.
- Hook version pinning is a recurring manual burden. Consider adding hook version staleness check to /kerd:tend.
- Stale `Kerd.md` MOC version field (says 0.31.0 vs actual 0.39.0) — either update on every release or remove entirely (lean remove).
- Solicit community mode contributions.
