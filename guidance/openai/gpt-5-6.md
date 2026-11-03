---
profile:
  provider: openai
  family: gpt-5-6
  version: 2026-09-05
  applicable_models: [gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna]
  official_sources:
    - url: https://developers.openai.com/api/docs/guides/latest-model
      retrieved: 2026-09-04
    - url: https://developers.openai.com/api/docs/models
      retrieved: 2026-09-04
  last_evaluated: null
  supersedes: gpt-5-6@2026-09
---

# OpenAI GPT-5.6 family profile

Choose among available models for the actual job, required tools, consequence
and available task evidence. Model names are not staffing roles, quality proofs
or a reason to choose the lowest price. The user's Kerd direction is explicit:
preserve the agreed quality; if resource constraints conflict with it, surface
the scope/effort tradeoff rather than quietly sending sub-par work to a model.
This is a Kerd policy correction, not a new claim about vendor model capability.
The previous profile is preserved in archive/gpt-5-6-2026-09.md for past runs.

```yaml
- id: outcome-first
  applies_when: always
  guidance: Compile objective, success, evidence, guardrails, authority, and stop conditions; omit process detail unless the path is required.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-5.6 pilot or source change
- id: suitability-before-cost
  applies_when: choosing Sol, Terra, or Luna
  guidance: Choose a model appropriate to the required outcome and tools. Use recorded task results where available; otherwise disclose the basis and uncertainty. Cost alone must not lower the agreed quality. Resolve a real resource/scope conflict with the user.
  basis: invariant
  source: producer direction on model suitability; conductor-rework-spec.md step 2
  evaluation: pending
  review_trigger: model-tier sweep, task-class change, or source change
- id: effort-native
  applies_when: selecting deliberation depth
  guidance: Set reasoning effort in native model configuration; do not simulate it with a long reasoning script. Choose a supported setting appropriate to the job, use task evidence where available and evaluate changes without claiming an unmeasured gain.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: effort sweep or source change
- id: native-tools-and-schema
  applies_when: tools or structured output are available
  guidance: Use native Responses tools, tool descriptions, and Structured Outputs. Keep only cross-tool policy and task evidence in prompt prose.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: platform integration changes or source change
- id: cache-shape
  applies_when: repeated prompts share a stable prefix
  guidance: Keep stable instructions before dynamic task context and record cached-input tokens separately.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: cache telemetry comparison or source change
```

Kerd-owned selection example (not a routing formula):

```yaml
job: review the evidence supporting a proposed change
selection_basis: appropriate analysis capability, usable read-only tools, and prior task results if available
model: an available model supported by that basis
effort: a supported setting appropriate to this review
uncertainty: record untested assumptions; do not call them proven efficiency
```

The pilot must test selection hypotheses; Conductor never treats model names
as the answer without considering the work.
