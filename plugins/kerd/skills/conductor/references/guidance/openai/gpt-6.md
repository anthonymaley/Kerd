---
profile:
  provider: openai
  family: gpt-6
  version: 2026-09
  applicable_models: [gpt-6-astra, gpt-6-sol, gpt-6-luna]
  official_sources:
    - url: https://developers.openai.com/api/docs/guides/latest-model
      retrieved: 2026-09-23
    - url: https://developers.openai.com/api/docs/models
      retrieved: 2026-09-23
    - url: https://learn.chatgpt.com/docs/models
      retrieved: 2026-09-23
  last_evaluated: null
  supersedes: null
---

# OpenAI GPT-6 family profile

GPT-5.6 stays as its own profile (`openai/gpt-5-6.md`); this file does not
supersede it. GPT-6 is a separate current family — brief the two differently
when a job names one specifically, and do not assume a clause here applies to
a GPT-5.6 job or vice versa.

The third source above, `https://learn.chatgpt.com/docs/models`, is where
`https://developers.openai.com/codex/models` redirected (308 Permanent
Redirect) on 2026-09-23. It is the Codex CLI's own model/effort reference and
is distinct from the API guide at `official_sources[0]`.

Clauses already covered by `openai/gpt-5-6.md` or `openai/shared.md` and not
contradicted by what the fetched pages say — model suitability over cost,
using native tool/schema mechanisms instead of prompt-prose schemas, and
cache-prefix shaping — are not repeated here. This file holds only what
changes for a GPT-6 job versus a GPT-5.6 one.

```yaml
- id: tier-roles
  applies_when: choosing Astra, Sol, or Luna for a GPT-6 job
  guidance: Astra is positioned as the most capable model, for the hardest end-to-end work; Sol for complex coding and agentic workflows; Luna as the most efficient tier for focused, high-volume work (summarization, extraction, focused coding). This replaces the GPT-5.6 Sol/Terra/Luna positioning Kerd used before, and there is no GPT-6 Terra — do not carry the Terra role over.
  basis: provider-guidance
  source: official_sources[1]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: effort-levels-by-tier
  applies_when: setting reasoning effort for gpt-6-astra, gpt-6-sol, or gpt-6-luna through the API
  guidance: Astra has no none setting; where a brief used none, use low. Sol and Luna support none. For each tier's upper levels, check the models page at dispatch rather than assuming a fixed ladder; two fetches on 2026-09-23 summarized them differently. A brief carried over from a GPT-5.6 job that used a minimal-equivalent effort should start at low on GPT-6 and compare results on representative tasks, rather than assume minimal maps onto low.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: effort sweep or source change
- id: codex-effort-naming-is-separate
  applies_when: briefing a Codex CLI job (a kerd:agent Codex partner) rather than a direct API call
  guidance: Codex's own reasoning-effort names (Low, Medium, High, Extra High, Max, and Ultra for automatic subagent delegation) come from a different product surface than the API's none/low/medium/high scale, and are not the same scale. State which surface (API or Codex) a brief's effort setting refers to, and do not map Codex effort names onto the API's effort names or onto Claude's effort levels — they are not equivalent.
  basis: provider-guidance
  source: official_sources[2]
  evaluation: pending
  review_trigger: Codex model/effort naming change or source change
- id: instructions-outrank-skill-framing
  applies_when: a GPT-6 brief carries Kerd guardrails, authority, or stop conditions
  guidance: The guide's recommended prompt text tells GPT-6 that the user's instructions take precedence over guidance provided in a skill. Present Kerd's guardrails and stop conditions as the operator's direct instructions in the brief text itself, not as advisory background attributed to an embedded skill, so GPT-6 does not rank them below the task instructions.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: astra-asks-before-assuming
  applies_when: briefing a gpt-6-astra job, especially an unattended one
  guidance: Astra is more likely than earlier models to stop and ask for clarification where they would have assumed. Autonomous continuation is something a prompt can ask for, not its default. For unattended work, put the facts it would otherwise ask about into the brief, and state which gaps it may resolve itself and which must come back. Provider guidance that asks it to act without pausing never expands Kerd's authority; keep stop conditions and approval boundaries literal.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: skip-tests-for-reversible-low-impact-changes
  applies_when: the brief covers a reversible, low-impact change
  guidance: The guide's recommended prompt text tells GPT-6 not to write tests for reversible, low-impact changes that mirror the implementation. Do not copy that line into a Kerd brief whose agreed quality bar wants tests; where tests are wanted, say which ones.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: name-the-report-shape
  applies_when: the deliverable is prose or a report, not code
  guidance: Astra tends toward detailed, formatted answers (lists, tables, Markdown) and can repeat phrases across sessions. State the report shape Kerd wants, including length and whether formatting is welcome, as an explicit instruction in the brief rather than relying on its default.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
```

The pilot must test these as hypotheses against real GPT-6 runs before any
clause is promoted past `pending`; none of them is evaluated yet.
