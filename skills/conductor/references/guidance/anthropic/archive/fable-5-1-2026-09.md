---
profile:
  provider: anthropic
  family: fable-5-1
  version: 2026-09
  applicable_models: [claude-fable-5-1, claude-mythos-5-1]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
      retrieved: 2026-09-04
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-09-04
  last_evaluated: null
  supersedes: null
---

# Claude Fable 5.1 profile

```yaml
- id: all-efforts-eligible
  applies_when: every new task class
  guidance: Start at high, then include medium and low in the task eval; use xhigh or max only where the task needs the headroom. Effort labels are not assumed equivalent to earlier families.
  basis: provider-guidance
  source: official_sources[1]
  evaluation: pending
  review_trigger: matched effort sweep or source change
- id: finish-long-task
  applies_when: asynchronous or explicitly autonomous multi-step work
  guidance: State that already-authorized next steps should be completed without asking again; do not apply this clause to live pair work.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: premature-stop comparison or source change
- id: low-effort-search-trigger
  applies_when: effort is low and the task depends on current or unfamiliar facts
  guidance: Explicitly require retrieval of named fast-moving facts rather than relying on model memory.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: low-effort research comparison or source change
- id: targeted-edits
  applies_when: a small part of an existing file changes
  guidance: Prefer a surgical edit when it preserves the result; do not rewrite the whole file merely for convenience.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: edit-size comparison or source change
- id: append-only-history
  applies_when: the harness replays thinking blocks or relies on prompt caching
  guidance: Keep conversation history append-only and record compaction as a new state rather than editing earlier turns.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: harness state handling changes or source change
```

Kerd-owned example delta:

```xml
<execution_mode>Autonomous batch. Complete the authorized task and its stated
checks. Ask only if a missing producer-owned decision would materially change
the result.</execution_mode>
<edit_scope>Make targeted changes to the named sections. Report unrelated
defects separately.</edit_scope>
```

