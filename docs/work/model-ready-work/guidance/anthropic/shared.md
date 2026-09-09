---
profile:
  provider: anthropic
  family: shared-current-claude
  version: 2026-09
  applicable_models: [claude-fable-5, claude-fable-5-1, claude-sonnet-5, claude-opus-5, claude-opus-4-8]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
      retrieved: 2026-09-04
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-09-04
  last_evaluated: null
  supersedes: null
---

# Shared current-Claude guidance

This draft records candidate clauses for the pilot. None is proven for Kerd
until evaluated.

```yaml
- id: clear-direct
  applies_when: always
  guidance: State the requested outcome and constraints plainly; explain why a non-obvious constraint matters.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Claude pilot result or source change
- id: xml-mixed-material
  applies_when: instructions, context, examples, and variable input coexist
  guidance: Separate those materials with descriptive XML tags; do not add XML to a simple prompt merely for style.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first complex-prompt ablation or source change
- id: examples-for-demonstrated-format-gap
  applies_when: baseline runs miss a required output pattern
  guidance: Add 3–5 relevant and diverse Kerd-owned examples, clearly separated from instructions; do not add examples before a failure demonstrates the need.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: example ablation or source change
- id: general-reasoning-over-script
  applies_when: reasoning method is not itself a requirement
  guidance: Ask for careful reasoning at the selected effort and let the model choose the decomposition; avoid prescribing a human chain of thought.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: reasoning-quality ablation or source change
```

## Kerd-owned example

```xml
<objective>Identify why the gate is reading the wrong repository.</objective>
<success_criteria>
  <criterion id="S1">The root cause is reproduced.</criterion>
  <criterion id="S2">The proposed correction is verified in both root directions.</criterion>
</success_criteria>
<guardrails>Read-only until the cause is proven. Do not infer environment-variable availability.</guardrails>
<context>Repository paths and retrieved files are supplied here.</context>
<task>Choose the investigation path. Return observed evidence against S1 and S2, or stop with an evidenced blocker.</task>
```
