---
profile:
  provider: anthropic
  family: opus-5
  version: 2026-09
  applicable_models: [claude-opus-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
      retrieved: 2026-09-04
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-09-04
  last_evaluated: null
  supersedes: null
---

# Claude Opus 5 profile

Local interpretation for pilot use:

```yaml
- id: effort-sweep
  applies_when: every new task class
  guidance: Start at high; test medium and low where latency or cost matters, and xhigh only for demanding agentic work. Preserve the lowest effort that holds outcome quality.
  basis: provider-guidance
  source: official_sources[1]
  evaluation: pending
  review_trigger: first matched effort sweep or source change
- id: remove-legacy-verification
  applies_when: machinery or the model already verifies the work
  guidance: Do not add generic final-verification or verifier-agent instructions; retain only verification that is a task obligation or repository invariant.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: verification ablation or source change
- id: scope-boundary
  applies_when: task scope is narrow or nearby work is visible
  guidance: State the exact requested scope and require reporting, not fixing, unrelated findings.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first scope-expansion failure or source change
- id: vision-tools-over-effort
  applies_when: diagrams, documents, charts, or UI images must be judged
  guidance: Give iterative view/crop/inspect tools before increasing effort solely for visual accuracy.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: visual-task comparison or source change
```

Kerd-owned example delta from the shared Claude rendering:

```xml
<scope>Correct only the sealed view and its living description. Record nearby
stale claims as follow-up findings; do not repair them in this task.</scope>
```

No generic "verify everything again" clause is added. The envelope's named
evidence and repository gate remain authoritative.

