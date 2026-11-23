---
profile:
  provider: openai
  family: gpt-6
  version: 2026-11-23
  applicable_models: [gpt-6.2-astra, gpt-6.2-sol, gpt-6-astra, gpt-6-sol, gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna]
  official_sources:
    - url: https://developers.openai.com/api/docs/guides/latest-model
      retrieved: 2026-11-23
    - url: https://developers.openai.com/api/docs/models
      retrieved: 2026-11-23
    - url: https://learn.chatgpt.com/docs/models
      retrieved: 2026-11-03
    - url: https://developers.openai.com/api/docs/guides/model-selection
      retrieved: 2026-11-23
  last_evaluated: null
  supersedes: gpt-6@2026-11-03
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

The 2026-11-23 revision adds `gpt-6.2-astra` and `gpt-6.2-sol`, which the models page and the API guide now list. It rewrites `tier-roles`, `effort-levels-by-tier`, `astra-asks-before-assuming` and `name-the-report-shape`, replaces `skip-tests-for-reversible-low-impact-changes` with `tests-only-when-wanted`, removes `instructions-outrank-skill-framing` (the current guide has no skill-precedence text), and adds `keep-prefix-unchanged` and `unsupported-parameters`. The prior version is preserved in `archive/gpt-6-2026-11-03.md`.

Clauses already covered by `openai/gpt-5-6.md` or `openai/shared.md` and not
contradicted by what the fetched pages say — model suitability over cost,
using native tool/schema mechanisms instead of prompt-prose schemas, and
cache-prefix shaping — are not repeated here. This file holds only what
changes for a GPT-6 job versus a GPT-5.6 one.

```yaml
- id: tier-roles
  applies_when: choosing among gpt-6.2-astra, gpt-6.2-sol, gpt-6.1-terra and gpt-6-luna for a GPT-6 job
  guidance: As of 2026-11-23 the models page lists four flagship models. gpt-6.2-astra is the most capable, for the hardest projects. gpt-6.2-sol is the page's go-to model for everyday work. gpt-6.1-terra is the model for visual reasoning. gpt-6-luna is the fastest and most cost-effective, for focused, high-volume tasks. The model-selection page starts most API workflows at gpt-6.2-sol with medium reasoning effort, uses gpt-6.2-astra for demanding engineering or analysis, gpt-6-luna for small repeatable tasks and gpt-6.1-terra for interpreting charts and screenshots, and says to compare models on the same inputs and keep the lightest setting that meets the quality bar. gpt-6-astra, gpt-6-sol and gpt-6.1-sol are no longer in the models page's flagship list; the Codex models page of 2026-11-03 (official_sources[2]) still listed gpt-6-astra and gpt-6.1-sol.
  basis: provider-guidance
  source: official_sources[1]; official_sources[3]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: effort-levels-by-tier
  applies_when: setting reasoning effort for a GPT-6 model through the API
  guidance: As of 2026-11-23 the models page lists reasoning levels low, medium, high, xhigh and max for gpt-6.2-astra and gpt-6.2-sol, and none, low, medium, high, xhigh and max for gpt-6.1-terra and gpt-6-luna. The migration guide starts new GPT-6.2 integrations at medium and says to change none or minimal to low; the results should be compared rather than assuming minimal maps onto low. The page gives no level list for gpt-6-astra, gpt-6-sol or gpt-6.1-sol, so check the models page at dispatch for those. The effort parameter is reasoning.effort in the Responses API and reasoning_effort in Chat Completions.
  basis: provider-guidance
  source: official_sources[1]; official_sources[0]
  evaluation: pending
  review_trigger: effort sweep or source change
- id: codex-effort-naming-is-separate
  applies_when: briefing a Codex CLI job (a kerd:agent Codex partner) rather than a direct API call
  guidance: Codex's own reasoning-effort names (Low, Medium, High, Extra High, Max, and Ultra for automatic subagent delegation) come from a different product surface than the API's none/low/medium/high scale, and are not the same scale. State which surface (API or Codex) a brief's effort setting refers to, and do not map Codex effort names onto the API's effort names or onto Claude's effort levels — they are not equivalent.
  basis: provider-guidance
  source: official_sources[2]
  evaluation: pending
  review_trigger: Codex model/effort naming change or source change
- id: astra-asks-before-assuming
  applies_when: briefing a gpt-6.2-astra job, especially an unattended one
  guidance: The guide says that when intent is unclear Astra may propose a next step and wait for confirmation, and that for longer tasks the prompt should allow reasonable assumptions and continued work. For unattended work, put the facts it would otherwise ask about into the brief, and state which gaps it may resolve itself and which must come back. The guide's recommended text has it stop only for significant scope changes, concrete blockers, user-level decisions, or irreversible or destructive actions, and flag its assumptions. That text never expands Kerd's authority; keep stop conditions and approval boundaries literal.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: tests-only-when-wanted
  applies_when: the brief covers a coding change
  guidance: The guide's recommended coding-style text says to skip new tests unless they are requested, required by the repo, or needed to catch a specific regression existing tests would miss. Do not copy that line into a Kerd brief whose agreed quality bar wants tests; where tests are wanted, say which ones. The same text says to reuse existing repo logic and preserve behavior callers rely on, and the guide says to describe project conventions explicitly.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: name-the-report-shape
  applies_when: the deliverable is prose or a report, not code
  guidance: The guide says Astra is more concise and direct by default than earlier models, and to revisit instructions such as "be concise" when migrating. State the report shape Kerd wants, including length and whether formatting is welcome, as an explicit instruction in the brief. The guide's writing text asks for the user's and sources' terminology, active voice, key points first, and final answers that stand on their own without reasoning shorthand.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first GPT-6 pilot or source change
- id: keep-prefix-unchanged
  applies_when: a gpt-6.2-astra or gpt-6.2-sol job runs over several Responses API turns, or its history, model or end user may change between turns
  guidance: The guide says that from GPT-6.2 the Responses API drops reasoning items after mid-conversation edits to history, certain model changes (including downgrades), or changes to the end user or organization, which can reduce answer quality and increase token use. Keep the prefix unchanged between responses. Put reusable instructions in a developer message as the first item in input; top-level instructions are appended after input for GPT-6.2 and later, so use them only for guidance that applies to the current request.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first multi-turn GPT-6.2 API run or source change
- id: unsupported-parameters
  applies_when: building an API request for gpt-6.2-astra or gpt-6.2-sol
  guidance: The guide says to omit temperature, top_p and logprobs-related parameters. In Chat Completions omit temperature, top_p, logprobs and top_logprobs; in Responses omit temperature, top_p and top_logprobs, and remove message.output_text.logprobs from include. Neither model supports Flex (service_tier flex).
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: source change
```

The pilot must test these as hypotheses against real GPT-6 runs before any
clause is promoted past `pending`; none of them is evaluated yet.
