# Independent review of pending 0.113.0

## Outcome and authority

Anthony wants the combined changes reviewed with the established Claude Kerd
partner before release. This is the actual review request, not an acknowledgement
note. Codex holds edits while you review. Review the uncommitted diff against
75f97e5 plus this work directory. Read-only repository; temporary isolated test
fixtures are allowed. No edits, staging, commits, pushes, installations, settings,
consumer-project access, live queue probes or additional model jobs. Keep your
existing model, effort and permissions. Return findings, do not implement them.

## Agreed scope

1. Switch should measure and restore the same named selections, not describe a
   tiny excerpt while reading a huge findings/history tail. Preserve archives;
   return reusable read arguments and flag sections reaching EOF. No new gate
   or manifest protocol, no claim those arguments freeze subsequently edited data.
2. Package the four core skills (Conductor, Switch, Visuals, Agent) for Codex
   from one maintained source. No legacy skills or Claude hooks in the core
   artifact; full Claude distribution remains intact. Build and install are
   distinct. A previously approved local installation exists as an older
   generated snapshot; it is not proof of delivery of today's changes.
3. Factual clarification does not authorize next proposed work. Ask once, in
   YOU or below the frame where required. Logs preserve claims, not evidence
   that an event was observed. Fix shared behavior, not the project that exposed it.

## Sources and checks

Inspect `git diff`, `docs/work/codex-plugin/work.md`, the modified helpers and
their tests, packaging START.md, both manifests and README 0.113.0. Exclude the
preserved untracked root patch. Relevant implementations:

- skills/switch/scripts/handoff.py: reading_picks, selected_source, measure,
  prepare; reusable read_args and EOF labeling.
- skills/switch/scripts/where_we_are.py: --question-below, default/alternate
  presentation, unchanged save-state guard with host-neutral success hint.
- docs/work/model-ready-work/packaging/build.py and test_build.py: four-core
  selection, canonical copies, version derivation, allowlisted requirements,
  fresh catalog generation, relocation and standalone save/pickup tests.
- Conductor SKILL.md, execution.md and model-jobs.md; Switch SKILL.md and
  in-out.md: authority semantics, native-host capability, single question,
  bounded reads, claim/evidence distinction.

Builder results, not evidence to accept on trust: Switch 304 (renderer 95),
Conductor 37, packaging 9; release check clean; audit carries its known trace
gap. Try bounded reproductions where useful. Separate behavioral model
compliance and fresh-session user experience (unobserved) from renderer/fixture
results. Review behavior and consequences, not opportunities for more protocol.

## Return

Numbered consequential findings, each with path/line, reproduction or concrete
counterexample, and smallest suggested correction. Check tests bind to behavior
instead of agreeing lists; package paths/links work away from the source; guides
do not promote measurements, installation or authority beyond evidence. Include
release-surface omissions or contradictions introduced by this diff. Distinguish
what you ran from what you read. End with ready/not ready for release review
closeout and remaining live checks. That verdict does not authorize publication.

This is the established partner, not a freshly independent conversation.
No matching local Fable profile is assumed; use a clear outcome-first brief and
your existing settings, not invented model tuning. Return one complete answer
using Agent's supplied reply markers. Codex will retrieve it; no reciprocal wait.
