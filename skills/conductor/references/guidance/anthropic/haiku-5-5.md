---
profile:
  provider: anthropic
  family: haiku-5-5
  version: 2026-10
  applicable_models: [claude-haiku-5-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5
      retrieved: 2026-10-09
    - url: https://platform.claude.com/docs/en/models/haiku-5-5/overview
      retrieved: 2026-10-09
    - url: https://platform.claude.com/docs/en/models/haiku-5-5/whats-new-haiku-5-5
      retrieved: 2026-10-09
    - url: https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
      retrieved: 2026-10-09
    - url: https://code.claude.com/docs/en/sub-agents
      retrieved: 2026-10-09
  last_evaluated: null
  supersedes: null
---

# Claude Haiku 5.5 profile

Short local interpretation of Anthropic's Haiku 5.5 pages, retrieved 2026-10-09.
It comes from Anthropic's docs only: there is no matched Kerd comparison for this
model yet, and every clause below is pending until a real brief uses it and its
result is assessed.

Haiku 5.5 is the first Haiku with effort levels. `model: haiku` resolves to the
newest Haiku, so Kerd routes it as `kerd:haiku-low`, `kerd:haiku-medium` or
`kerd:haiku-high`. Plain `kerd:haiku` sets no effort and stays only for sessions
that predate those agents; it runs at the host default. Haiku 4.5 is the previous
model and works differently (see [model choice](../model-choice.md)).

Left out because Kerd's native route sets none of them: `budget_tokens` (returns
400 on 5.5, adaptive thinking is on by default), and sampling parameters
(`temperature`, `top_p`, `top_k`).

```yaml
- id: fit
  applies_when: deciding whether a job suits claude-haiku-5-5
  guidance: Anthropic describes it as built for high-volume, latency-sensitive work such as classification, routing, extraction and subagent tasks. Suits scans, extraction, classification and other bounded subagent jobs; Opus 5.5 or Sonnet 5.5 stays the choice for open-ended or long-horizon work, and Anthropic advises also running evals on Sonnet 5.5 and comparing.
  basis: provider-guidance
  source: official_sources[0]; official_sources[1]
  evaluation: pending
  review_trigger: first matched Haiku 5.5 comparison on a Kerd job type, or source change
- id: effort-levels
  applies_when: choosing effort for a claude-haiku-5-5 job
  guidance: low for short, simple tool tasks and high-volume simple requests; medium is the default and the place to start, including agentic coding; high for long agent tasks, knowledge work and strict instruction following. xhigh and max only where evals justify them. Name the level through kerd:haiku-<effort>; do not assume the level of a worker routed as plain kerd:haiku.
  basis: provider-guidance
  source: official_sources[0]; official_sources[4]
  evaluation: pending
  review_trigger: first Haiku 5.5 effort comparison on a Kerd job type, or source change
- id: low-medium-risks-long-briefs
  applies_when: a long brief or a code-changing job goes to claude-haiku-5-5 at low or medium
  guidance: In long agent prompts at low it sometimes stops early and hands the task back (raising low to medium roughly halved this and more than doubled output tokens), and may skip a search or a check. At low and medium it sometimes reports a code change as done without running a check. A long or code-changing Haiku job's brief carries two lines. First, "Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step." Second, the guide's check paragraph: "When you change code that can be run, built, or type-checked, run a real check that exercises the change before reporting it done: the project's tests, type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to start, does not count." Its install sentence is left out: a brief names what the player may install. Conductor still opens the evidence before accepting.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Haiku 5.5 long-brief or code-changing job, or source change
- id: token-use
  applies_when: budgeting a claude-haiku-5-5 job
  guidance: The same text takes about 30% more tokens than on Haiku 4.5, so allow for that in context and output budgets. Context is 1M and max output 128K (Haiku 4.5: 200K and 64K).
  basis: provider-guidance
  source: official_sources[1]; official_sources[2]
  evaluation: pending
  review_trigger: source change
- id: migration
  applies_when: reusing a Haiku 4.5 brief on claude-haiku-5-5
  guidance: Anthropic says prompts written for Haiku 4.5 should perform well without changes. Reasoning-like text appears in replies more often at low or with thinking off, and new safety-classifier refusals can end a turn with stop_reason "refusal", with no server-side fallback.
  basis: provider-guidance
  source: official_sources[0]; official_sources[3]
  evaluation: pending
  review_trigger: source change
```
