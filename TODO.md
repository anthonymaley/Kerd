# TODO

## Now

- **Install 0.66.0 and run the re-seated conductor live** (`claude plugins install kerd`). v0.66 is written but has never executed — only the write-to-disk mechanic is tested (one trial). What to watch on the first real run: does the orchestrator subagent reliably write the spec and return a summary rather than dumping it back as text; does the after-the-body tagging rule actually shrink `[keep]` (the prediction is mostly-delegate with one or two review steps at the seams); and does a `[keep]` diff-review step catch collateral damage a verify command misses.
- **Capture a baseline from the current shape while it's still installed** — the keep/delegate split and how much score-writing happens in-session, so v0.66 has something to be compared against. `~/3of3` and `~/dinner-tonight` both had live delegated sessions on 2026-07-31/08-01.
- **Dogfood sherpa on `~/Bree`** — in that repo, fresh session. Decide first: mid-lifecycle pickup vs fresh feature (open question in CONTEXT.md).

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
