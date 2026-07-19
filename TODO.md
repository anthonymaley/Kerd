# TODO

## Now

- **Update installed plugin cache to 0.65.0** (`claude plugins install kerd`) so conductor's gate-message rule takes effect in other repos. (The 0.64.0 cache update happened — this session's skills loaded from the 0.64.0 cache path.)
- **Dogfood sherpa on `~/Bree`** — in that repo, fresh session, after the cache update above. Decide first: mid-lifecycle pickup vs fresh feature (open question in CONTEXT.md).

## Backlog

- Sweep stale version-pinned Kerd hooks in other repos (krutho-strategy, leru, obair — check each `.claude/settings.local.json`); rewire dead cache-version paths to the current version. `~/3of3` was fixed 2026-07-11 (was pinned to GC'd `0.41.0`) but is now pinned to `0.63.0` — still in cache, one GC away from breaking again. Also migrate each repo's `kivna/.focus → kivna/.pair` during the sweep: 3of3 still has `.focus`, so the partner-mode hook (which reads `.pair`) is silently off there. Overlaps the tend category-9 staleness item below — do manually now or wait for the automated check.
- Mode reconciliation deferred until the sherpa dogfood; clean krutho-strategy's stray `sessions-of-record/` (tend detects it)
- skriv voice profile: wiring held pending non-founder-genre samples (see CONTEXT.md)
- Decide whether switch should commit the vault repo (contract vs behavior disagree — see CONTEXT.md)
- Guard switch-in step 3 smoke test against context bloat: delegate build/test to a subagent (or tail/grep output); switch-in absorbs a pass/fail verdict, never a full build log. Low-severity; bites only on build-heavy repos (e.g. ~/3of3). Fold in next time the skill is touched.
- Run /kerd:tend on krutho-founders, krutho-strategy, obair to migrate vaults (now also migrates them to the CONTEXT.md split via first switch-out)
- Hook version staleness check in /kerd:tend (pinning is a recurring manual burden — 3of3 just proved it: cache GC breaks wired paths silently)
- Stale Kerd.md MOC version field (says 0.31.0 vs actual) — update per release or remove (lean remove)
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md` — replace the hard multiple-choice ban in the Question-formation gate with a quality bar. Exact phrase ready to drop:
  > Default to one open question. Offer options only when they *clarify* a real choice that's yours to make — a genuine, near-complete set of 2-4 distinct alternatives, each stated in a few crisp words. Not allowed: lazy binaries that offload a call you should make, vague or verbose options, or a menu that forecloses answers the user would otherwise give. If the options would pre-narrow an open space, ask open.
