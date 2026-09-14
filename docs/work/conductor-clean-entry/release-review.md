# Integrated 0.124.0 release review

<objective>
Anthony authorized this combined release after we agree. Codex owns the single
commit/push and CI check. Review read-only; no edits, installs, commits, pushes,
dispatch, bindings or lifecycle changes from you. Source held stable for review.
</objective>

<clarified_direction>
Anthony corrected the proposed explicit-only trigger: substantial build/design/
workflow requests should OFFER Conductor whether new or existing work/repos.
Small fixes can stay ordinary. Explicit requests open it, and established guided
work doesn't repeat the offer. This is now in SKILL.md, orchestration.md and
README, with no native invocation-policy metadata added. The earlier design
request's “not merely build an app” explicit-only wording is superseded.
</clarified_direction>

<sources>
Review git diff and the untracked skills/conductor/references/orchestration.md.
Main paths: switch SKILL.md/in-out.md, conductor SKILL.md and references
execution.md, understanding.md, journey.md, model-jobs.md, orchestration.md,
README.md, both manifests. Version 0.124.0 in three fields; capability strings
updated together. Prior reviewed clean-entry changes remain in this same diff.
Work evidence: docs/work/conductor-clean-entry/work.md, orchestration-brief.md,
scenarios.md. Development briefs in that directory ship as records, not runtime.
kerd-laptop-result.patch stays untracked and excluded.
</sources>

<review>
Check latest all-task model/composer/worker contract, definite assignment rather
than retrospective consideration, prompt-guidance/retention before dispatch,
settings evidence and unavailable controls, startup visibility even without a
worker, and absence of repeated staffing ceremony or mandatory worker count.
Check the offer/entry/ordinary-small-fix distinction and established-work evidence.
Your six design concerns should be addressed: definitions, current-pair limits,
and no interactive startup routine in managed decisions. Check the release
surfaces and any consequential contradiction in the prior clean-entry changes.
Return numbered blockers with path/line and minimal fix, or readiness to release
with evidence limits. Tests running: Switch full, Conductor transport, packaging,
Agent, hooks and CI gate commands; final results will be retained before commit.
No installed or natural consumer-compliance claim from these source checks.
</review>
