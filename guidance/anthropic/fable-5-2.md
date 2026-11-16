---
profile:
  provider: anthropic
  family: fable-5-2
  version: 2026-11-16
  applicable_models: [claude-fable-5-2, claude-mythos-5-2]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
      retrieved: 2026-11-16
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-11-16
    - url: https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2
      retrieved: 2026-11-16
    - url: https://platform.claude.com/docs/en/models/fable-5-2/overview
      retrieved: 2026-11-16
    - url: https://code.claude.com/docs/en/model-config
      retrieved: 2026-11-16
  last_evaluated: null
  supersedes: null
---

# Claude Fable 5.2 profile

Fable 5.2 (`claude-fable-5-2`, released 2026-11-09) is a new family. It does not
supersede `anthropic/fable-5-1.md`: Fable 5.1 is still listed on the models
overview. Mythos 5.2 (`claude-mythos-5-2`) has the same capabilities and is open
only to organizations verified through Anthropic's programs. Every clause below
is from the five pages above and is unevaluated.

```yaml
- id: effort-start-high-and-resweep
  applies_when: choosing effort for a new fable-5-2 job class
  guidance: The API default is high, and the provider says to start there and run evals at medium and xhigh as well; most of the capability gain is already present at high. Do not carry over an effort setting tuned on Fable 5.1 or Opus 5.5, because the amount of thinking at each level can differ. xhigh is for the hardest long-running coding and agentic work where a gain was measured; max is for measuring the ceiling. The Claude Code model-config page lists medium as the default effort for Fable 5.2 in Claude Code, so a Claude Code session that sets no effort runs at medium, not the API's high; set the level explicitly and report the active level as unverified unless it was read from the session.
  basis: provider-guidance
  source: official_sources[0]; official_sources[1]; official_sources[4]
  evaluation: pending
  review_trigger: matched effort sweep or source change
- id: low-effort-stops-early
  applies_when: agentic multistep work at low or medium effort
  guidance: The model sometimes ends a turn before the work is done, by listing what remains, offering to continue, or stopping at an ordinary obstacle such as a timeout, more often at low and medium. For such jobs the brief should say not to stop while owed work remains, to carry on with work that does not depend on an open question, and to diagnose errors, timeouts and failing tools and work through them unless the blocker is deliberate (a file marked untouchable, withheld access, a safety guardrail), in which case it reports it plainly. The provider's test of such text at medium roughly halved sessions ending with continuable work and raised output tokens about 30 percent. This never overrides confirmation for risky or destructive actions, which the brief keeps.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 job at low or medium that stops early, or source change
- id: approvals-name-the-action
  applies_when: a brief or reply authorizes the job to continue, or carries approval rules
  guidance: Say exactly what is approved rather than sending a bare continue. List the specific actions that need approval; a broad rule such as sending messages to people outside the conversation made the model hold back about half of its routine requests to colleagues in the provider's simulated tasks. Write ask-for-approval-before for an action Kerd wants kept under the job's responsibility instead of never, because the model treats never as absolute.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 job that holds routine work for approval, or source change
- id: say-who-owns-the-code
  applies_when: a fable-5-2 player changes existing code
  guidance: With no statement about ownership, or with the code presented as someone else's, the model tends to add to the existing structure and to report nearby problems rather than fix them. Telling it that it owns and maintains the codebase made it consolidate duplicated code in about 75 percent of small-task runs against under 10 percent without, but output tokens rose 70 to 80 percent, with unrequested tests, documentation and sometimes changed behaviour, and its closing summary often omitted small changes. Leave the ownership sentence out where the user owns the code and wants minimal change; a scope-limiting rule did not cancel it. Where it is used, review the diff, not only the summary.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 player diff, or source change
- id: updates-and-standalone-report
  applies_when: a person reads a fable-5-2 job's progress or final message
  guidance: The model can write little user-facing text during long tool runs and may make its first tool call without saying what it will do. Where a human is in the loop, ask in the brief for a line before starting, brief updates while working, and a closing recap that stands alone (what was found, done and next); the provider measured about 20 percent more output tokens from this. For final reports and handoffs, the reader has not seen the tool calls, so the report must make sense alone, lead with the key points and avoid terms the job invented. On API routes, progress updates arrive as thinking blocks that are empty at the default thinking.display of omitted. For long asynchronous jobs where nobody needs updates, the provider recommends the model without this text.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first silent long fable-5-2 turn or unclear report, or source change
- id: subagent-use-and-cost
  applies_when: a fable-5-2 session orchestrates or may start subagents
  guidance: How much it delegates depends on the harness - it rarely started subagents with a minimal tool on short tasks and delegated readily where prompts invite it, and at xhigh and max it used subagents to review its own work. Subagents can be a large share of session cost, so check which model they default to. Review standing lines that tell the model to delegate before carrying them over; if it starts more subagents than the task needs, state what a subagent costs, when delegation is worth it and how to brief one.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2-led fan-out, or source change
- id: carry-over-lines-to-review
  applies_when: a brief, skill or memory carried over from Fable 5.1 or Opus 5.5 is reused for fable-5-2
  guidance: Remove an answer-directly-without-deliberating line; it did not stop the model from thinking at medium and above, so lower the effort for easy turns instead. Do not show the job a token budget in the prompt without testing, since removing a large one lowered cost at equal performance on the provider's coding tasks at high and xhigh. Drop the Opus 5.5 treat-that-answer-as-done chat lines where the model should keep re-examining earlier answers. Remove hard style limits such as one instruction per sentence in 20 words or fewer, which make prose choppy. Delete stale never and stop-at-first-error cautions that no longer hold, since the model follows them closely.
  basis: provider-guidance
  source: official_sources[0]; official_sources[2]
  evaluation: pending
  review_trigger: first carried-over brief on fable-5-2, or source change
- id: append-only-history-prefix-check
  applies_when: API or custom-harness routes that build their own requests; it does not change a native Kerd player brief, where Claude Code owns the conversation
  guidance: A request that changes the system prompt, tools or an earlier message before a stored thinking block fails the prefix check with a 400 error, so keep the history append-only and put changed instructions in the newest turn; thinking blocks are read only by Fable 5.2 and Mythos 5.2 and are dropped when the conversation moves to another model. Claude Code, claude.ai, Managed Agents and the Agent SDK build their own requests and are unaffected.
  basis: provider-guidance
  source: official_sources[2]; official_sources[0]
  evaluation: pending
  review_trigger: harness state handling change or source change
- id: api-request-limits
  applies_when: a direct API call or custom harness targets fable-5-2
  guidance: Adaptive thinking is always on, and thinking disabled or enabled with budget_tokens returns a 400 error. Forced tool use (tool_choice any or tool) returns a 400; use auto with strict tool use or JSON outputs for schema-valid output. Omit temperature, top_p and top_k. The computer_20251124 tool returns a 400 except on Amazon Bedrock; use computer_toolset_20260801. A Fable 5.2 executor in the advisor tool accepts only Fable 5.2 or Mythos 5.2 as advisor. The model needs 30-day data retention and is not available under zero data retention unless Anthropic expressly authorizes it.
  basis: provider-guidance
  source: official_sources[2]; official_sources[3]
  evaluation: pending
  review_trigger: source change
- id: refusals-are-not-findings
  applies_when: a fable-5-2 job returns stop_reason refusal or declines benign security or life-science work
  guidance: The model runs safety classifiers (categories cyber, bio, frontier_llm, reasoning_extraction, general_harms). Benign cybersecurity and life-sciences work can trigger the cyber and bio classifiers, so treat a refusal as a routing signal, not a finding about the work. Remove any instruction that asks the job to write out its reasoning in the reply, which the reasoning_extraction category covers. Permitted fallback targets are Claude Opus 4.8 and Claude Opus 5, which do not read its thinking blocks.
  basis: provider-guidance
  source: official_sources[0]; official_sources[2]
  evaluation: pending
  review_trigger: first refusal on a benign Kerd job, or source change
```
