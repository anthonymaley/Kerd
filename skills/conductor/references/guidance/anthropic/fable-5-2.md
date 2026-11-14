---
profile:
  provider: anthropic
  family: fable-5-2
  version: 2026-11-12
  applicable_models: [claude-fable-5-2, claude-mythos-5-2]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
      retrieved: 2026-11-12
    - url: https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2
      retrieved: 2026-11-12
    - url: https://platform.claude.com/docs/en/models/fable-5-2/migration-guide
      retrieved: 2026-11-12
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-11-12
    - url: https://code.claude.com/docs/en/model-config
      retrieved: 2026-11-12
  last_evaluated: null
  supersedes: null
---

# Claude Fable 5.2 profile

Fable 5.2 (released 2026-11-09) is a new profile, not a revision of Fable 5.1's:
the provider's 5.2 guide is written from fresh testing and does not say 5.1
prompts carry over. Several 5.1 clauses point the opposite way on 5.2 (5.1 fixed
nearby code unasked; 5.2, told nothing about ownership, adds to the existing
structure and reports nearby problems instead). So nothing below is copied from
the [Fable 5.1 profile](fable-5-1.md); each clause rests on a 5.2 source. A 5.1
clause with no 5.2 source (quoted source text, the crop-and-zoom vision tip,
surgical edits) is left out, to be added back if a 5.2 job shows the same need.

The clauses cover two uses: a delegated Fable 5.2 job that Conductor briefs,
and a Fable 5.2 session that conducts. Kerd's native route is Claude Code,
which builds the requests itself, so the API-only clauses at the end change
nothing for a native player.

```yaml
- id: effort-start-high-then-sweep
  applies_when: 'choosing effort for any new Fable 5.2 task class'
  guidance: 'Start at high (the API default and where most of the gain is). Move to medium where the task is interactive or everyday and the result holds; use low for well-specified, fast subagent work, where 5.2 at low scored close to 5.1 at higher effort on coding. Use xhigh only for the hardest long-running coding or agentic work with a measured gain (it raised coding scores slightly for many more tokens), and max only to find the ceiling or for open-ended problems where time and tokens do not matter. Never carry over an effort tuned on Fable 5.1 or Opus 5.5; the levels rank the same across models but the thinking at each differs. On the native route the level is the `kerd:fable-<effort>` agent.'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[3]'
  evaluation: pending
  review_trigger: 'first matched Kerd effort comparison on Fable 5.2, or source change'
- id: effort-not-reply-length
  applies_when: 'a brief wants shorter or longer replies, or less thinking'
  guidance: 'Effort barely changes reply length, and a line such as "answer directly without deliberating" does not stop 5.2 from thinking at medium and above (5.1 usually obeyed it). Set length and tone in the brief''s words; to cut thinking, lower the effort. Remove any don''t-think wording a brief inherited.'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[2]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 job that is slow or costly on easy turns, or source change'
- id: finish-the-whole-task
  applies_when: 'an autonomous or long multistep job runs at low or medium effort'
  guidance: '5.2 can end a turn early by listing what is left, offering to continue, or stopping at an ordinary obstacle, more often at low and medium. Tell the job not to stop while it owes work the brief asked for; to carry on with work that does not depend on an open question; to diagnose ordinary obstacles (errors, timeouts, locked files, empty results, failing tools) and work through them with the access it has; and to leave a deliberate blocker (a file marked not to touch, withheld access, a guardrail) alone, say plainly what it found and look for another safe route. This never lifts the brief''s confirmation steps for risky or irreversible actions. The provider measured about half as many unfinished sessions and about 30 percent more output tokens; endings that list what remains and then stop were not removed, so Conductor still checks each return against its part of the score.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 player that returns with owed work undone, or source change'
- id: approvals-name-the-action
  applies_when: 'a brief lists actions that need approval, or a go is relayed to a Fable 5.2 job or session'
  guidance: 'Name the exact actions that need approval ("ask before pushing to main", "ask before deleting files"), never a broad category; in the provider''s test a rule naming "sending messages to people outside this conversation" made the model hold back about half of its routine requests. A go relayed to the job says exactly what is approved ("yes, run the migration on staging"), not a bare "continue".'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 job that holds routine work for approval, or source change'
- id: say-who-owns-the-code
  applies_when: 'a Fable 5.2 player changes code or documents in the person''s repository'
  guidance: 'Ownership wording changes the result. With nothing said, or with the code presented as someone else''s, 5.2 adds to the existing structure (even duplicating code) and reports nearby problems instead of fixing them; that is the right default for Kerd players, where the person owns the code, so leave the provider''s ownership sentence out. Add "You are the owner and long-term maintainer of this codebase, and its design is up to you" only when the agreed work is restructuring with that latitude; it then consolidated duplicates in about 75 percent of runs against under 10 percent, but output rose 70 to 80 percent, unrequested tests and documentation appeared, and some runs changed existing behaviour. A scope limit in the same brief does not cancel it. When consolidation is wanted without that latitude, ask for that one change in the brief.'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[1]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 player diff that duplicates code the brief wanted shared, or that restructures unasked, or source change'
- id: check-the-diff-not-the-summary
  applies_when: 'a Fable 5.2 player returns code changes'
  guidance: 'Its closing summary often leaves out small changes. Conductor''s return check reads the diff itself against the player''s part of the score, and lists any change the summary did not mention.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first return where diff and summary disagree, or source change'
- id: no-verification-reminders
  applies_when: 'writing any Fable 5.2 brief'
  guidance: 'Lead with the outcome and hand ambiguous problems (root causes, architecture choices) whole, leaving the path to the job where the agreement does not fix it; it checks its own work with less prompting. This never drops a step, boundary or check the agreement or score requires. Leave out generic "remember to test" reminders, but keep the brief''s named checks: they are the agreed proof obligations, not reminders, and provider guidance never lowers the quality bar.'
  basis: provider-guidance
  source: 'official_sources[4]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 player that skips a check the brief named, or source change'
- id: no-token-budget-in-brief
  applies_when: 'the work has a token or cost limit'
  guidance: 'The size of a budget shown in the prompt changes how much 5.2 spends; removing a large one cut cost with equal results on the provider''s coding tasks at high and xhigh, and the provider advises testing without it. Keep a large controller budget in the sketchbook and the grid rather than the brief, but state any limit the player must observe. Leaving it out is an experiment to measure on Kerd jobs, not a settled rule.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 brief that carries a budget, or source change'
- id: subagents-cost
  applies_when: 'a Fable 5.2 job or session can start subagents'
  guidance: '5.2 delegates readily in a harness whose prompts invite it, and at xhigh and max it was seen starting subagents to review its own work; subagents can be a large share of a session''s cost. A player brief says whether the job may start subagents (by default no: the score already split the work and review belongs to the reviewer). When a Fable 5.2 session conducts, Conductor''s fan-out rule is itself a standing instruction to delegate: every dispatch still goes through the grid with its model named, so count what it starts.'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[2]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 job that starts subagents unasked, or a Fable-conducted concert whose dispatch count exceeds the score, or source change'
- id: rules-with-scope-not-never
  applies_when: 'a Fable 5.2 session conducts, or a brief carries standing rules, cautions or memory'
  guidance: '5.2 follows instructions closely and treats a rule containing "never" as absolute; cautions piled up in memory, notes and instruction files made agents ask for approvals they did not need, mostly when several agents worked together. In a brief, write each rule with its scope and reason ("ask before deleting files" rather than "never delete files"), list the routine steps that need no approval, narrow stop conditions such as "stop at the first error", and leave out cautions whose reason no longer holds. Kerd''s own guides use many absolute "never" rules; this is known, not yet tested on a Fable 5.2 conductor.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 session or job that asks for approval of routine work, or source change'
- id: keep-re-examining
  applies_when: 'a Fable 5.2 job answers follow-ups, or a reviewer runs a second round'
  guidance: 'Do not carry over Opus 5.5''s "treat that earlier answer as done" lines; on 5.2 they cut thinking on follow-ups and made it far less likely to point out mistakes in its earlier answers. A re-review brief asks the job to recheck its earlier findings, not only the new change.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 re-review that misses a fault in its own earlier answer, or source change'
- id: style-rules-only-as-needed
  applies_when: 'a brief carries writing-style rules (house style, Skriv, length limits)'
  guidance: '5.2 follows style rules closely, so a hard limit such as "one instruction per sentence, in 20 words or fewer" makes its prose choppy. Before briefing, remove style rules the deliverable no longer needs, and check any hard sentence-length limit that remains.'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[1]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 deliverable that reads choppy, or source change'
- id: report-for-a-low-context-reader
  applies_when: 'a Fable 5.2 job writes a final report, handoff or any message the person reads cold'
  guidance: 'Its writing rated above 5.1''s and close to Opus 5.5''s, but the reader has not seen its tool calls or files. Tell it to write for an intelligent reader with no context; key points first; no term or abbreviation it made up during the work; plain full sentences, one idea each, active voice, the same word for the same thing; prose where ideas connect and bullets only for separate items; and only the details the reader needs. This sits under Kerd''s report shape (Found, Needs you, Unsure first), not in place of it.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 report the person could not follow without the files, or source change'
- id: findings-not-reasoning
  applies_when: 'a brief asks a job to explain how it reached a result'
  guidance: 'Asking the model to reproduce its internal reasoning in the reply can be refused (`reasoning_extraction`, which no fallback retries). Ask for the findings, the evidence and the steps it took, never "write out your thinking".'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[1]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 refusal on a Kerd brief, or source change'
- id: classifier-refusals-and-fallback
  applies_when: 'a coding, security-review or biology-adjacent job runs on Fable 5.2'
  guidance: 'Safety classifiers can decline benign security and life-sciences work (`cyber`, `bio`). In Claude Code a flagged request can rerun on another model (cyber on Opus 4.8, biology on Opus 5), unless the fallback model is blocked; with `switchModelsOnFlag` set to ask, a player subagent fails instead of switching. A separate chain covers an overloaded model, and an allowlist or alias override can also change the model. Record the observed model with `job_evidence.py` and check the fallback notice and its timing before naming a cause: a job that fell back ran partly or wholly off Fable 5.2, and its turns after the switch work without 5.2''s earlier reasoning. A refusal on a benign job is a cue to rephrase, not a finding about the code.'
  basis: provider-guidance
  source: 'official_sources[0], official_sources[1], official_sources[4]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 refusal or fallback on a Kerd job, or source change'
- id: progress-in-long-turns
  applies_when: 'a Fable 5.2 session works interactively with the person (conducting)'
  guidance: '5.2 can run long stretches of tool calls with nothing for the reader, and can start without saying what it is about to do. Say in a line what is about to happen before the first tool call, give a one-line update every few tool calls, and close with a recap that stands alone. Background players need none of this; the final report is what counts there.'
  basis: provider-guidance
  source: 'official_sources[0]'
  evaluation: pending
  review_trigger: 'first Fable 5.2 conducting session the person found silent, or source change'
- id: api-routes-append-only
  applies_when: 'API or custom-harness routes that replay Fable 5.2 thinking blocks; not a native Kerd player, where Claude Code builds the requests'
  guidance: 'The prefix check applies to every account on 5.2: changing `system`, `tools` or an earlier message invalidates later thinking blocks: by default the Messages API rejects the request with a 400 and the Message Batches API drops those blocks (`drop_block` makes the Messages API drop them too). Keep history append-only, put changed instructions in the newest turn, start new conversations for changed system text, shorten history only with compaction or context editing, and treat `drop_block` as a stopgap. Only Fable 5.2 and Mythos 5.2 read 5.2''s thinking blocks, so a router or fallback that moves a conversation off 5.2 loses that reasoning. At high and above set a large `max_tokens` (thinking and reply share it). Forced tool use (`tool_choice` any or tool) and `temperature`, `top_p`, `top_k` return 400s.'
  basis: provider-guidance
  source: 'official_sources[1], official_sources[2], official_sources[3]'
  evaluation: pending
  review_trigger: 'a Kerd route that builds its own requests, or source change'
```

Kerd-owned example delta, for an autonomous player at medium on code the person owns:

```xml
<execution_mode>Autonomous batch. Finish everything this brief asks before you
stop. Work through ordinary errors, timeouts and failing tools; leave anything
marked do-not-touch alone and say what you found. Ask before pushing, deleting
files or installing anything; the other steps here need no approval.</execution_mode>
<edit_scope>The person owns this code. Change what the brief names; report other
problems you see as follow-ups. Do not start subagents.</edit_scope>
<report>Only your final message reaches the caller, and they have not seen your
tool calls. Put the key points first, in plain full sentences: what you found,
what you changed (every file), and what is still open.</report>
```
