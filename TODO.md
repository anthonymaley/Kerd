# TODO

## Now

- **Verify delegated conductor live** — new in v0.62.0, written-but-not-run-live. On Fable: `/kerd:conductor fable on`, produce the spec file, dispatch a `[delegate]` step to a Sonnet subagent, confirm the review-evidence flow fires as written (and `.active-modes` carries the `[fable]` toggle). See kivna/sessions/2026-07-07.md.
- **Dogfood sherpa on `~/Bree`** — in that repo, fresh session, after updating the plugin cache to 0.62.0 (`claude plugins install kerd`). Decide first: mid-lifecycle pickup vs fresh feature (open question in CONTEXT.md).

## Backlog

- **Conductor: add reasoning-effort as a per-step lever** (next conductor iteration, *after* v0.62.0 delegation is verified live). Alongside the `[fable]`/`[delegate]` tag, let a step carry an effort hint — high/xhigh for the spec, low for mechanical delegated steps, high + Opus for core-but-delegatable work (effort × tier, not just tier; the Agent tool already has an `effort` param). Provenance: a friend's Fable-delegation workflow. The rest of that workflow (compact/checkpoint at ~200k, decision-brief-then-compact) was **rejected** — switch owns boundaries and gives lossless cold pickup; conductor never manages context or compacts.
- Mode reconciliation deferred until the sherpa dogfood; clean krutho-strategy's stray `sessions-of-record/` (tend detects it)
- skriv voice profile: wiring held pending non-founder-genre samples (see CONTEXT.md)
- Decide whether switch should commit the vault repo (contract vs behavior disagree — see CONTEXT.md)
- Guard switch-in step 3 smoke test against context bloat: delegate build/test to a subagent (or tail/grep output); switch-in absorbs a pass/fail verdict, never a full build log. Low-severity; bites only on build-heavy repos (e.g. ~/3of3). Fold in next time the skill is touched.
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults (now also migrates them to the CONTEXT.md split via first switch-out)
- Hook version staleness check in /kerd:tend (pinning is a recurring manual burden)
- Stale Kerd.md MOC version field (says 0.31.0 vs actual) — update per release or remove (lean remove)
- Consider promoting the refined question-formation rule from the focus hook into global `~/.claude/CLAUDE.md` — replace the hard multiple-choice ban in the Question-formation gate with a quality bar. Exact phrase ready to drop:
  > Default to one open question. Offer options only when they *clarify* a real choice that's yours to make — a genuine, near-complete set of 2-4 distinct alternatives, each stated in a few crisp words. Not allowed: lazy binaries that offload a call you should make, vague or verbose options, or a menu that forecloses answers the user would otherwise give. If the options would pre-narrow an open space, ask open.
