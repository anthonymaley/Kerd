# Deep review — Conductor, Switch and Visuals together

## Requested outcome

Give an independent assessment of whether this candidate is a sound replacement
for everyday Kerd use, what would prevent adoption, and what we should remove or
simplify before adopting it. Review the actual skills and supporting code, not
just the proposal or the builder's summary. This is a review, not authorization
to install the candidate or implement your recommendations.

The user requested the existing Claude Kerd session for this review. Use its
actual available model and appropriate supported effort; report the identity and
effort if observable, otherwise say unknown. No particular model name is assumed.

## Authority and working state

Keep any existing Conductor session parked; do not advance its marker, invoke
installed Switch, or start a new guided interview. Read relevant project files
and perform safe local diagnostic checks. Tests and visual renders may use an
isolated temporary output directory. Do not change tracked or untracked project
content, install tools, commit, push, deploy, contact other projects, or terminate
existing sessions. Existing uncommitted work belongs to the user.

Return the review in the conversation. Do not edit a verdict into the work record.
If your available tools cannot run a check or render a view, disclose the missing
evidence; do not treat reading source as observing runtime or visual behavior.

## The product intention

Kerd should help anyone doing repo-based work—not only developers—describe an
outcome, agree success and boundaries, and get a complete, independently assessed
work package. Conductor guides Understand → Shape → Agree → Deliver → Complete.
During authorized delivery it continues without routine "next" prompts. It
answers routine decisions from facts and agreement, not invented facts, and asks
the user when the basis is missing or the impact is significant.

The model and effort should fit the work. Prompt preparation should give that
model the outcome, necessary context, evidence and authority, with freedom over
method. Lower cost is not permission to assign an inadequate model. Resource
limits are optional. Cross-model contributions are bounded jobs, not a debate
or a documentation factory.

The user rejected complex rung gates, seals, requirement fingerprints and CI or
custom-hook dependencies for using Kerd. Strong understanding, clear agreement,
honest evidence and trustworthy continuation remain important. Evaluate whether
the simpler approach achieves those aims. If it cannot, explain the concrete
failure and tradeoff; do not preserve old machinery merely because it exists.

## Start with the current candidate

Paths below are relative to this repository. The pack is
`docs/work/model-ready-work/`.

Read first:

1. `docs/work/model-ready-work/consolidation.md`
2. `docs/work/model-ready-work/candidate-entry.md`
3. `docs/work/model-ready-work/skills/conductor/SKILL.md`
4. `docs/work/model-ready-work/skills/switch/SKILL.md`
5. `docs/work/model-ready-work/skills/visuals/SKILL.md`
6. `docs/work/model-ready-work/trials/switch-redesign/completion.md`

Then follow the relevant references and implementations in those three skill
directories. Examine the interview/journey, delivery, model-job and work-record
guides; the actual request runner; Switch's In/Out and To/Roll guides and helpers;
and Visuals' patterns, sources and example asset. Inspect tests where needed.
Use the local `guidance/` sources to check how model-specific preparation is
actually supported, rather than treating provider advice as proof of performance.

Inspect the rendered views when tooling permits:

- `docs/work/model-ready-work/diagrams/working-loop.html`
- `docs/work/model-ready-work/trials/switch-redesign/direction.html`
- `docs/work/model-ready-work/skills/visuals/assets/review-flow.html`

Compare against the intended experience in
`docs/work/model-ready-work/experience-refresh.md`. Trace relevant claims back
through original trial evidence and failures, particularly
`trials/switch-redesign/pickup-budget/comparison/results.md` and its linked reviews,
`trials/switch-redesign/device-build/results.md`, and
`trials/switch-redesign/review-continuity-completion.md` within the pack.

The candidate is not installed. Switch has producer acceptance for tested paths
with explicit limits, not a universal preservation or automatic handoff claim.
The refreshed full conversation still lacks a complete real-person usability
validation. Test counts in summaries are reported evidence until reproduced;
they do not prove usability or prevent all model deviations.

Older proposals, trial states and the old `review-brief.md` contain superseded
claims. Use history to understand decisions, not as current execution authority.
For adoption conflicts, inspect affected live `skills/`, plugin configuration,
hooks and project instructions selectively. Do not read all session history by
default or silently reconcile conflicting instructions yourself.

## Questions the review must answer

- **Conductor:** Are all-project questions, source-backed proposed answers,
  success measures, confirmation and material decisions clear without exhausting
  the user? Are questions visually distinct, progress intelligible and diagrams
  introduced when useful? Does authorized work really continue, including after
  interruptions, failed reviews and brief user confirmations?
- **Model work:** Does the chosen model actually receive the right information,
  tools and authority? Where do context loss, unsupported assumptions, misleading
  effort claims, failure accounting or repeated reviews threaten the result?
  Separate demonstrated behavior from instruction-only promises.
- **Switch:** Do In, Out, To and Roll preserve the decisions, unfinished work,
  constraints, next action and Git authority needed to continue? Is cleanup
  recoverable and justified? Examine source release, destination identity,
  failed saves, concurrent work and session ownership where implemented. Are
  user-opened destinations and managed-worker limitations clearly communicated?
  Does the context-saving evidence support its actual claim without hiding lost
  meaning, preparation cost or unmeasured whole-pickup cost?
- **Visuals:** Do pictures explain the user's product or work, not just our
  process? Are relationships, uncertainty and consequential boundaries accurate?
  Check readability, narrow layouts, accessible descriptions and agreement flow.
  Are diagram-design and Archify capabilities and limitations represented honestly?
- **Together:** Can a new user and a returning user find the current question,
  work position and next action? Do the three skills share one coherent agreement
  and saved state, or create competing records? Are required references actually
  loaded at the moment needed? Could completion be mistaken for publication or
  permission to install? What breaks when used beside existing Kerd instructions?
- **Simplicity:** What can be deleted, merged or deferred without weakening the
  outcome? Where has trial machinery leaked into the everyday product? What is
  the smallest useful adoption step, and which remaining uncertainty genuinely
  needs a person rather than another model review?

## Return a decision, not a new rulebook

Lead with a verdict: ready for controlled adoption, revise first, or rethink.
Give a short assessment of Conductor, Switch, Visuals and their integration.

Prioritize consequential findings. For each, include the observed file/line or
runtime evidence, the concrete user failure, the smallest correction, and its
cost or tradeoff. Distinguish observed defects, plausible risks and untested
claims. Disclosed limitations are not automatically defects: say whether they
block the proposed use and why. Challenge prior acceptance if evidence warrants
it, but do not rewrite that acceptance or silently widen what it covered.

Finish with what to keep, remove and defer; a short adoption sequence with a
recoverable previous setup; and checks actually performed versus evidence still
missing. Recommend no new framework, mandatory gate, hook or CI requirement
without showing why a smaller process or implementation change cannot suffice.
Do not manufacture a minimum number of findings or turn rare edge cases into
an endless pre-adoption checklist.
