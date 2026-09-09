# Independent review job

## Status supplied to the reviewer

**Current review target:** [Rework Conductor, keep Kerd](kerd-conductor-rework.md),
[its process drawing](diagrams/kerd-conductor-rework.html), and
[its implementation specification](conductor-rework-spec.md). Read those first;
load supporting material only for a specific question. The older standalone-first
implementation sequence is superseded. No live skill changes have been made.

The user has explicitly chosen a strong guided process without complex rung
gates, seals, requirement fingerprints, mandatory schemas or CI/hook usage
dependencies. Review the adequacy of the simpler process, not its conformity to
the old machinery. Identify legacy instructions that must be removed; do not
require their preservation just because they were once approved.

Challenge whether agreement and outcome validation are clear enough, whether
the first slice is small enough, and whether hidden infrastructure requirements
remain. If a protection is missing, name the concrete failure and the smallest
remedy. Do not assume a new gate or hook is the answer.

This is an expanded working design, not an approved or shipped product. Three
earlier diagrams were reviewed before the guided interview, multi-feature
handling, work levels, visual depths, and cross-model job design were added.
Those additions remain unapproved hypotheses.

The existing demonstration proves only deterministic prompt preparation,
local model profiles, coverage reporting, 20 test cases, and one matched
diagnostic run. The interview, readiness engine, feature map, context freshness,
work view, cross-model runner, recovery, and full evaluation runner are planned
but not implemented.

## Review job

```yaml
objective: >
  Find the smallest set of defects that would prevent Model-ready work from
  being easy, fast, trustworthy, and effective.

review_questions:
  - Can a product-minded person use it without learning prompt engineering?
  - Does the design genuinely work for product, project, executive, research,
    operational, creative, and software work—or merely rename a coding process?
  - Does the interview gather enough information without becoming exhausting?
  - Does bounded model freedom still prevent drift?
  - Does Conductor choose sufficient depth without burdening the user with levels?
  - Can progressive disclosure hide a consequential fact?
  - Will cross-model jobs improve outcomes rather than create noise?
  - Does the design contain duplicate truths or unnecessary machinery?
  - Which current Kerd behaviors conflict with this design?
  - What is the smallest viable implementation and trial?

do_not:
  - Rewrite the entire design.
  - Produce an exhaustive edge-case catalogue.
  - Add features without naming the failure they solve.
  - Treat provider guidance as proof.
  - Judge prose style unless it affects usability.
  - Reintroduce the retired machinery under new names.
  - Treat prompt-layer behavior as unbypassable enforcement.

return:
  - Five highest-consequence findings maximum.
  - Evidence for each finding.
  - Proposed correction and what becomes worse if corrected.
  - Verdict: ready for trial, revise first, or fundamentally unsound.
```

## Reviewer A — product and usability

Recommended: capable Claude model. Focus on interview burden, clarity,
progressive disclosure, product drift, decision ownership, visual usability,
and whether an ordinary product user can operate the system.

## Reviewer B — system and evaluation

Recommended: capable OpenAI reasoning model. Focus on duplicate truth, state
derivation, coverage limits, context freshness, evaluation validity, failure
classification, cross-model jobs, and the smallest viable implementation.

The reviews are independent bounded jobs. Reviewers do not see or debate each
other's output. Conductor reconciles findings against the fixed questions.
