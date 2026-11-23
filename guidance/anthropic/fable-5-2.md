---
profile:
  provider: anthropic
  family: fable-5-2
  version: 2026-11-23
  applicable_models: [claude-fable-5-2, claude-mythos-5-2]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
      retrieved: 2026-11-23
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-11-23
    - url: https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2
      retrieved: 2026-11-23
    - url: https://platform.claude.com/docs/en/models/overview
      retrieved: 2026-11-23
    - url: https://code.claude.com/docs/en/model-config
      retrieved: 2026-11-23
  last_evaluated: null
  supersedes: null
---

# Claude Fable 5.2 profile

Local interpretation for pilot use, from Anthropic's Fable 5.2 prompting guide,
what's-new page, effort page, models overview and Claude Code model page, all
read on 2026-11-23. Fable 5.2 was released on 2026-11-09. Fable 5.1 keeps its
own profile (`fable-5-1.md`); this file does not restate it, and a clause
there is not assumed to hold here. The clauses record only what changes how
Kerd briefs a delegated Fable 5.2 or Mythos 5.2 job. Every clause is pending
until a real brief uses it and its result is assessed.

Left out because they matter only to someone building an API harness and
Kerd's native route (Claude Code) sets them itself: forced tool use returning
a 400, `thinking` field values, sampling parameters, the computer-use toolset
change, advisor-model pairing, and the 30-day data-retention requirement.

```yaml
- id: effort-start-high
  applies_when: every new task class run through the API, or a Claude Code session whose effort is set explicitly
  guidance: The API default is high. Start there, then sweep medium and xhigh; do not carry over a setting tuned on Fable 5.1 or Opus 5.5, because the amount of thinking at each level differs. Low suits quick back-and-forth, well-specified tasks and high-volume subagent work, where the provider reports Fable 5.2 at low scoring close to Fable 5.1 at higher effort on coding evaluations. Medium suits interactive coding and everyday knowledge work. Use xhigh only for the hardest long-running coding or agentic work where a gain has been measured, and max only to measure the ceiling or for a task where time and tokens do not matter.
  basis: provider-guidance
  source: official_sources[0]; official_sources[1]
  evaluation: pending
  review_trigger: first fable-5-2 effort sweep or source change
- id: claude-code-default-medium
  applies_when: reporting or choosing the effort of a Fable 5.2 job run through Claude Code
  guidance: The Claude Code page lists medium as the default effort for Fable 5.2 there, while the API default is high. Set the effort explicitly on the job and report the level from what ran, not from either default. The page also says no Fable model is the account-type default on any plan or provider, and that the fable alias resolves to Fable 5.2 unless ANTHROPIC_DEFAULT_FABLE_MODEL is set.
  basis: provider-guidance
  source: official_sources[4]; official_sources[3]
  evaluation: pending
  review_trigger: Claude Code default change or source change
- id: no-think-less-lines
  applies_when: an inherited brief or template tells the model to answer directly without deliberating
  guidance: On Fable 5.2 such a line does not stop thinking at medium and above, and at high and above the model thinks before almost every reply, even a greeting. Remove the line and lower the effort for easy turns instead. Effort changes reply length very little; ask for the length and tone wanted in the brief.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 trivial request billed at high effort, or source change
- id: finish-whole-task
  applies_when: an asynchronous multi-step agentic job runs at low or medium effort
  guidance: Fable 5.2 sometimes ends a turn early by listing what is left, offering to continue, or stopping at an ordinary obstacle such as a timeout, more often at low and medium. Add a short instruction not to stop while owed work remains, to diagnose errors, timeouts and empty results and work through the ones that are not real blockers, and to leave deliberate blockers (a file marked not to be touched, withheld access, a safety guardrail) alone and report them. The provider measured about half as many unfinished sessions at medium with this text and about 30 percent more output tokens, and the text does not override confirmation for risky or destructive actions. It is not for live pair work.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first low or medium fable-5-2 job that stops early, or source change
- id: specific-approvals
  applies_when: a brief names actions that need approval, or a job is told to continue
  guidance: Name the exact actions to double-check, and the routine steps that need no approval, rather than writing a broad category. The provider saw a rule listing messages to people outside the conversation make the model hold back about half its routine requests to colleagues. Write "ask before deleting files" rather than "never delete files", because the model treats "never" as absolute. When continuing a job, say what is approved, not a bare "continue".
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 job held up by an approval rule, or source change
- id: code-ownership-statement
  applies_when: a player edits an existing codebase
  guidance: Fable 5.2 follows what the prompt says about who owns the code. With no statement, or with the code framed as someone else's, it tends to add to the existing structure and to report nearby problems rather than fix them. A statement that the model owns and maintains the codebase made it consolidate duplicated code in about 75 percent of small-task runs against under 10 percent without it, with 70 to 80 percent more output tokens, unrequested tests and documentation, and sometimes changed behaviour of an existing feature. Where the user owns the code and wants minimal change, leave the ownership sentence out; a no-drive-by-refactors rule alone did not cancel it once it was present. Check the reported diff, because the closing summary often omitted small changes.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 player diff with unrequested changes or a summary missing changes, or source change
- id: progress-updates
  applies_when: a person is in the loop on a long fable-5-2 job
  guidance: The model may write little user-facing text during long runs of tool calls and may make its first tool call without saying what it will do. For live work, ask for a one-line statement of intent before the first tool call, brief updates while working, and a closing recap that stands on its own; the provider measured an opening message in every run and about 20 percent more output tokens. For unattended work do not ask for frequent updates; the provider recommends Fable 5.2 for long asynchronous work where nobody needs them. On the API, progress updates arrive as thinking blocks that are empty at the default display setting, so a client reading only text blocks can look silent.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first live fable-5-2 job reported as silent, or source change
- id: subagent-expectations
  applies_when: a fable-5-2 session leads and may dispatch subagents
  guidance: How much Fable 5.2 delegates depends on the harness; it delegated readily where prompts invite delegation, and at xhigh and max the provider saw it start subagents to review its own work. Subagents can be a large share of a session's cost, so check which model they use. If it starts more subagents than the task needs, say in the brief what a subagent adds to the cost and when delegation is and is not worth it, and how to brief one; the provider saw a longer description of that kind roughly halve subagent counts at high. Review standing lines that tell the model to delegate. Early testers reported good results with Fable 5.2 as planner and orchestrator for other models.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2-led fan-out cost or source change
- id: caution-pile-up
  applies_when: a brief inherits notes, memory, instruction files or validation steps written for earlier models or earlier runs
  guidance: Fable 5.2 follows cautions closely, and old ones such as "never retry" or "stop and review at the first error" can cause needless approval requests or block autonomous work. Remove cautions whose reason no longer holds, narrow stopping conditions, and give absolute rules their scope and reason. Keep a confirmation step for risky or irreversible actions. This removes stale rules only; it never widens what the brief authorizes.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 job blocked by an inherited rule, or source change
- id: earlier-model-lines
  applies_when: a brief or template written for Fable 5.1 or Opus 5.5 is reused
  guidance: Review before reuse. A token budget shown to the model in the prompt changes how much it spends, and removing a large one lowered cost with equivalent performance at high and xhigh in the provider's coding tests. The two chat-prompt sentences telling the model to treat an earlier answer as done reduced its thinking on follow-ups and made it far less likely to point out mistakes in that answer, so leave them out where re-examination is wanted. Hard style limits such as one instruction per sentence in 20 words or fewer can make its prose choppy.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 job on a reused brief or source change
- id: report-for-low-context-reader
  applies_when: the job's final report or handoff is read by someone who did not see the tool calls
  guidance: Ask for a report that stands on its own, with key points in the first sentences, plain words in full sentences, no terms the job invented during the work, prose where ideas connect and bullets only for separate items, and nothing the reader must dig elsewhere to understand. The provider reports this made final reports less dense with fewer semicolons, and says to add length or specific-detail instructions as the readers need. Tell the model which reader it writes for.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-2 report judged dense, or source change
- id: refusal-handling
  applies_when: a fable-5-2 job returns stop_reason refusal or stops on a benign cyber or life-sciences task
  guidance: Safety classifiers can decline a request; categories are cyber, bio, frontier_llm, reasoning_extraction, general_harms or none, and benign security or life-sciences work can trigger the first two. Remove any instruction that asks the model to write out its reasoning in the reply. A refusal is not a finding about the code. The permitted API fallback targets for Fable 5.2 are Opus 4.8 and Opus 5, and a thinking block from Fable 5.2 is dropped when another model reads the conversation; Mythos 5.2 reads it. Mythos 5.2 offers the same capabilities only to organizations verified through Anthropic's programs.
  basis: provider-guidance
  source: official_sources[0]; official_sources[2]
  evaluation: pending
  review_trigger: first refusal on a benign Kerd job, or source change
- id: append-only-history
  applies_when: API or custom-harness routes that replay thinking blocks; it does not change a native Kerd player brief, where Claude Code owns the stored conversation
  guidance: Keep the system prompt, tools and earlier messages unchanged between requests and add only to the end. On Fable 5.2 a request that changes anything before a thinking block returns a 400 error, and changing instructions partway through belongs in the newest turn. Shorten history only with context editing or compaction that keeps no earlier turns after the summary.
  basis: provider-guidance
  source: official_sources[0]; official_sources[2]
  evaluation: pending
  review_trigger: harness state handling changes or source change
```

Kerd-owned example delta:

```xml
<execution_mode>Autonomous batch. Complete the authorized task and its stated
checks. Work through ordinary errors and timeouts; ask only if a missing
producer-owned decision would materially change the result.</execution_mode>
<edit_scope>Make targeted changes to the named sections. Report unrelated
defects separately instead of fixing them. Add tests only where the brief asks
or the repository already keeps them for this kind of change.</edit_scope>
<report>Only your final message reaches the caller, who has not seen your tool
calls. Put the key points first, use plain words, and say what you found, what
you changed and what is still open, across the whole job.</report>
```
