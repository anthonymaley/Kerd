---
profile:
  provider: anthropic
  family: sonnet-5
  version: 2026-09
  applicable_models: [claude-sonnet-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
      retrieved: 2026-09-04
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
      retrieved: 2026-09-04
  last_evaluated: null
  supersedes: null
---

# Claude Sonnet 5 profile

This profile is intentionally thin until Kerd reads and evaluates the complete
model-specific page. The official index identifies the dimensions to test:
response length, effort/thinking calibration, tool triggering, literal
instruction following, and design/frontend defaults.

```yaml
- id: literal-instruction-audit
  applies_when: the compiled prompt contains overlapping or exceptional rules
  guidance: Remove conflicts and state the intended exception next to the rule it narrows; do not rely on implied precedence.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: full source review, first Sonnet pilot, or source change
- id: tool-trigger-test
  applies_when: task success requires a tool call
  guidance: Make the required evidence explicit, then test whether the model selects the tool without a universal must-call rule.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first tool-required pilot or source change
```

