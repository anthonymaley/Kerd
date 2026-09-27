---
profile:
  provider: anthropic
  family: sonnet-5
  version: 2026-09-27
  applicable_models: [claude-sonnet-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
      retrieved: 2026-09-27
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
      retrieved: 2026-09-04
    - url: https://platform.claude.com/docs/en/models/overview
      retrieved: 2026-09-27
  last_evaluated: null
  supersedes: sonnet-5@2026-09
---

# Claude Sonnet 5 profile

Local interpretation for pilot use, from a full read of Anthropic's Sonnet 5
prompting guide on 2026-09-27. It carries every behaviour in that guide that
changes what a Kerd brief should say to a delegated Sonnet job (reader,
reviewer, player or composer). Every clause is pending until a real brief
uses it and its result is assessed.

Left out, because they only matter to someone building their own API harness
and Kerd's native route (`kerd:sonnet-<effort>` agents in Claude Code) sets
none of them: `max_tokens` headroom and the new tokenizer's roughly 30% more
tokens; sampling parameters (`temperature`, `top_p`, `top_k` at non-default
values return a 400); manual extended thinking (`budget_tokens`, now a 400);
the `thinking: {type: "disabled"}` switch; and computer-use and browser-use
tool versions and screenshot resolutions.

```yaml
- id: effort-default-high-strict-low
  applies_when: choosing effort for any claude-sonnet-5 job
  guidance: Default effort is high; use xhigh for the hardest coding and agentic jobs, and keep low for short, tightly scoped work. Sonnet 5 keeps strictly to the level it is given, so at low and medium it does only what was asked and can under-think a moderately complex job; when a result shows shallow reasoning, rerun at high or xhigh instead of adding "think harder" wording to the brief. Don't carry effort names over from Sonnet 4.6 (Sonnet 5 at medium is roughly 4.6 at high).
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet job run at low or medium on multistep work, or source change
- id: thinking-on-by-default
  applies_when: writing a brief for claude-sonnet-5, especially one adapted from a Sonnet 4.6 brief
  guidance: Adaptive thinking is on by default. Drop any "don't think" or "answer immediately" wording inherited from a 4.6 brief and use effort as the lever for depth; if a long brief makes the job think more than the work needs, say plainly that it should answer directly unless the step needs multistep reasoning, and check the result.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet job with an inherited thinking instruction or visible over-thinking, or source change
- id: findings-report-everything
  applies_when: any claude-sonnet-5 job that reports findings — code or document review, sweep, audit, or a reader grading evidence
  guidance: Don't write "only report high-severity issues", "be conservative" or "don't nitpick"; Sonnet 5 obeys such a bar closely and silently drops real findings below it. Ask for every finding, uncertain and low-severity ones included, each with a confidence and a severity, and let Conductor or a separate step filter; if the job must filter itself, give a concrete bar (for example "anything that could cause wrong behaviour, a failing test or a misleading result; omit only pure style or naming preferences").
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet review or sweep whose recall is checked against known issues, or source change
- id: literal-scope
  applies_when: a brief gives an instruction that should apply to more than the one item it names
  guidance: Sonnet 5 does not extend an instruction from one item to the next or infer a request that wasn't made, and is most literal at low and medium effort. State the scope in the brief ("every file in the set, not just the first", "each section"), and name every deliverable you expect back.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet job that applies a rule across several items, or source change
- id: literal-instruction-audit
  applies_when: the compiled prompt contains overlapping or exceptional rules
  guidance: Remove conflicts and state the intended exception next to the rule it narrows; do not rely on implied precedence.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet pilot with overlapping rules, or source change
- id: brief-complete-up-front
  applies_when: briefing any claude-sonnet-5 player or composer
  guidance: Put the task, its intent and its constraints in the single brief rather than feeding them in over later messages; Anthropic finds a complete first turn keeps both quality and token use better than a vague one clarified piecemeal. For coding players, start at high or xhigh effort.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet player that needed a mid-job correction, or source change
- id: tool-trigger-test
  applies_when: task success requires a tool call
  guidance: Sonnet 5 reaches for tools and checks its own work more readily than 4.6, and more so at high or xhigh effort. Name the evidence the job must gather and, where a particular tool matters, why and when to use it; test whether it picks the tool before adding any universal must-call rule.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first tool-required Sonnet pilot or source change
- id: report-length-and-shape
  applies_when: the job's reply has a length or shape Conductor depends on
  guidance: Sonnet 5 sizes its reply to how complex it judges the task, so short on lookups and long on open analysis. When Kerd needs a particular shape or length back, describe it in the brief, ideally with a short example of a good reply rather than a list of things not to do.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet reply too long or too thin to use, or source change
- id: no-forced-progress-updates
  applies_when: a brief for a long claude-sonnet-5 job would ask for interim status messages
  guidance: Don't add "summarise progress every N tool calls" scaffolding; Sonnet 5 gives regular updates on its own. If its updates don't fit, describe what they should contain, with an example.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first long Sonnet job with unusable updates, or source change
- id: prose-voice-restate
  applies_when: a claude-sonnet-5 composer or player writes long-form prose in a set voice
  guidance: Its default prose style differs from earlier models, so don't assume a voice prompt tuned elsewhere still lands; state the voice in the brief (or point to kerd:skriv) and check the first draft against it. Ask for variety in words, since sampling settings aren't available.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet prose job checked against a voice, or source change
- id: frontend-defaults-concrete-spec
  applies_when: briefing an HTML, frontend or design build on claude-sonnet-5
  guidance: Without direction Sonnet 5 settles into one house style, and generic wording ("clean and minimal", "not that colour") only swaps it for another fixed palette. Give a concrete spec (palette, type, radius, layout, sections), or have the job propose a few distinct directions first and build only the one chosen.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet frontend brief or source change
```
