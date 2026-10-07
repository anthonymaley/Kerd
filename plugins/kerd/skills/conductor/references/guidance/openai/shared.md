---
profile:
  provider: openai
  family: shared-current-reasoning
  version: 2026-09
  applicable_models: [gpt-5.5, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna]
  official_sources:
    - url: https://developers.openai.com/api/docs/guides/latest-model
      retrieved: 2026-09-04
  last_evaluated: null
  supersedes: null
---

# Shared current-OpenAI reasoning guidance

This draft records candidate clauses for the pilot. Exact model availability
and identifiers must be confirmed in the execution environment before a family
profile is approved.

```yaml
- id: outcome-first
  applies_when: always
  guidance: Lead with expected outcome, measurable success, evidence, authority, guardrails, and stopping conditions.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first OpenAI pilot result or source change
- id: path-freedom
  applies_when: execution order is not itself required for correctness
  guidance: Omit detailed step-by-step method and allow the model to choose an efficient path.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: method-guidance ablation or source change
- id: native-contracts
  applies_when: tools or structured outputs are available through the harness
  guidance: Put tool behavior in tool descriptions and output shape in native structured-output mechanisms instead of repeating schemas in prompt prose.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: tool/schema integration changes or source change
- id: effort-from-evals
  applies_when: selecting reasoning effort
  guidance: Start at the family guidance's balanced point, then raise or lower effort only when matched evaluations justify the quality, latency, and cost trade.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: effort sweep or model-family change
```

## Kerd-owned example

```markdown
# Outcome
Identify why the gate is reading the wrong repository.

# Success and evidence
- S1: reproduce the root cause.
- S2: verify the correction in both root directions.
- Return command evidence mapped to S1 and S2.

# Authority and guardrails
- Choose the investigation path.
- Remain read-only until the cause is proven.
- Do not infer environment-variable availability.
- Stop on proof or an evidenced blocker.

# Context
Repository paths and retrieved files follow.
```

