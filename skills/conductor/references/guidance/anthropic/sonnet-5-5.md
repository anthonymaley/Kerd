---
profile:
  provider: anthropic
  family: sonnet-5-5
  version: 2026-09-29
  applicable_models: [claude-sonnet-5-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
      retrieved: 2026-09-29
    - url: https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5
      retrieved: 2026-09-29
    - url: https://platform.claude.com/docs/en/models/sonnet-5-5/overview
      retrieved: 2026-09-29
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
      retrieved: 2026-09-29
    - url: https://code.claude.com/docs/en/model-config
      retrieved: 2026-09-29
  last_evaluated: null
  supersedes: null
---

# Claude Sonnet 5.5 profile

Local interpretation for pilot use, from a full read of Anthropic's Sonnet 5.5
prompting guide, its "What's new" page and its model overview on 2026-09-29.
It aims to carry every behaviour in that guide that changes what a Kerd brief
should say to a delegated Sonnet job (reader, reviewer, player or composer).
Every clause is pending until a real brief uses it and its result is assessed.

This is a new family, not a revision: `sonnet-5.md` stays the profile for
`claude-sonnet-5`. The 5.5 guide says Sonnet 5 prompts should still work and
the Sonnet 5 guide's patterns remain a reasonable starting point, so the Sonnet
5 clauses that 5.5 doesn't change are carried here, sourced to the Sonnet 5
guide (re-read the same day); where 5.5 changes one, the clause is reworded
from the 5.5 pages. Anthropic also says an Opus model is the better choice for
the hardest long-horizon work.

Which Sonnet a `kerd:sonnet-<effort>` job actually runs depends on the provider
and Claude Code version (see [model choice](../model-choice.md)); read this
profile only when the observed model is `claude-sonnet-5-5`.

Left out, because they only matter to someone building their own API harness
and Kerd's native route (`kerd:sonnet-<effort>` agents in Claude Code) sets
none of them: `max_tokens` sizing and streaming; the `between_tools` thinking
setting (the replacement for `disabled`, which now returns a 400) and its
effort limits, and `thinking.display` for progress-update blocks; per-message
effort changes and prompt-cache effects; forced `tool_choice` (`any`/`tool`
now return a 400); structured outputs and strict tool use; thinking blocks
bound to model, conversation and account, and append-only history; tolerant
handling of mis-cased tool names; harness-sent "you've gone quiet" reminders
and token or budget countdowns; server-side refusal fallback settings;
computer-use toolset versions, advisor-tool pairings, compaction on demand and
tools defined in a message; and sampling parameters (`temperature`, `top_p`,
`top_k` at non-default values return a 400). Claude Code also can't turn
thinking off on Sonnet 5.5, so no thinking toggle applies on Kerd's route.

```yaml
- id: effort-recalibrated
  applies_when: choosing effort for any claude-sonnet-5-5 job
  guidance: Effort levels are recalibrated, so a level doesn't give the same amount of thinking it did on Sonnet 5; don't carry a Sonnet 5 setting across. The API defaults to high, but Claude Code runs Sonnet 5.5 at medium unless an explicit choice or settings say otherwise, so always name the level through kerd:sonnet-<effort> and report the active level as unverified unless it was read from the job. Anthropic's starting points, in Kerd's terms, are a player on a well-specified step at medium, moving to high for harder or longer steps (and for bug fixes in existing code, where Claude Code recommends high because verification matters); a reviewer at high; a composer doing non-agentic design or reasoning at high; a short, tightly bounded reader at medium, or low only when Conductor checks the result. Raise effort when quality needs it. Reserve xhigh and max for job types where Kerd has measured a quality gain, since thinking and replies get much longer there.
  basis: provider-guidance
  source: official_sources[0]; official_sources[4]
  evaluation: pending
  review_trigger: first Sonnet 5.5 effort comparison on a Kerd job type, or source change
- id: thinking-on-by-default
  applies_when: writing a brief for claude-sonnet-5-5, especially one adapted from a Sonnet 5 brief
  guidance: Adaptive thinking is on by default, and from medium up the model thinks briefly before almost every reply. Asking it in the brief to think less doesn't reliably reduce its thinking, so drop Sonnet 5's "answer directly unless the step needs multistep reasoning" steer and any "don't think" wording; lower the effort instead. At low it skips thinking on most simple requests.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job carrying a think-less instruction, or source change
- id: carry-work-through
  applies_when: a claude-sonnet-5-5 player runs multistep coding or tool work at low or medium effort
  guidance: At low and medium the model sometimes stops before the work is done, to confirm a plan, ask a question it could answer itself, or ask whether to continue after one part of a multipart step. Try a higher effort first. To keep the level, tell it in the brief to keep working until everything the step asks for is done, and to stop early only when it can't go on without Conductor or the person, or before a risky step, saying exactly why. This makes low and medium jobs run longer and cost more, and it never replaces the brief's ownership and authority rules.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 player that returns a check-in instead of finished work, or source change
- id: stop-when-done-and-checked
  applies_when: briefing a claude-sonnet-5-5 player that changes code or files
  guidance: At every effort level, more so at higher ones, the model tends to add tests, docs and small supporting files that fit the repository's conventions, even unasked; the requested change itself stays close to the ask. Kerd players own only what the brief names, so say plainly that once the requested work is done and checked it stops and reports, adds no features, tests, files, docs or refactors that weren't asked for, and lists anything it thinks would help at the end of its report instead of doing it. At xhigh and max this wording also makes changes smaller overall.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 player that touches files outside its brief, or source change
- id: no-self-started-review
  applies_when: a claude-sonnet-5-5 job runs at xhigh or max effort
  guidance: At xhigh and max the model can start its own rounds of review and verification after finishing, sometimes by launching reviewer subagents, and can make related fixes it noticed along the way, which costs time and tokens. Run routine work at high or below, where this is rare. When a job does run at xhigh or max, and Conductor or a separate reviewer owns review, say that once the work is done and its checks pass it stops and reports, starts no extra review or hardening rounds, launches no reviewer subagents unless the brief asks for a review, and says at the end if it thinks a deeper review is worth doing. In Anthropic's testing at max this stopped reviewer subagents and cut cost by about a third with no quality change, but made the main agent's own review rounds rarer rather than absent.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job at xhigh or max, or source change
- id: ideas-means-ideas
  applies_when: a claude-sonnet-5-5 composer or reader is asked for ideas, options or a plan
  guidance: On an open-ended request the model can start building a report, presentation or other artefact when only ideas were wanted. Say in the brief that it gives the ideas, options or plan and stops, and builds or changes nothing until told to go ahead.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 options or plan job, or source change
- id: real-check-before-done
  applies_when: a claude-sonnet-5-5 player changes code that can be run, built or type-checked, especially at low effort
  guidance: The model usually checks its work before reporting a change done, but at low it sometimes reports done without a check that exercises the change, for example skipping tests because dependencies aren't installed. Tell it to run a real check before reporting done (the project's tests, type-checker or build, or the changed command itself); a syntax-only check, or a check command that failed to start, doesn't count; and if no real check can run, name the check it didn't run and why instead of reporting done. Anthropic's version also tells it to install missing declared dependencies with the project's own package manager and lockfile, never sudo or a system package manager; put that in a Kerd brief only when installing is inside the job's authority. In Anthropic's testing at low this made skipped or superficial checks rare with no quality change and slightly higher cost.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 player at low that reports done without check output, or source change
- id: no-hold-findings-wording
  applies_when: a brief for a claude-sonnet-5-5 job would say "hold all findings for the final response" or similar
  guidance: Remove it; the guide names it as an older instruction to drop, since the model writes short notes on what it found and what it does next between tool calls. Kerd still reads only the job's final report, so instead describe what that report must contain. If Kerd wants notes at set points (for example one line on what it's about to do before its first tool call and a short recap at the end), say so; the model follows that.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 brief that needed interim notes, or a final report missing findings, or source change
- id: no-tool-discouraging-wording
  applies_when: a claude-sonnet-5-5 job needs facts that may have changed since training, or depends on searching or reading rather than recall
  guidance: The model sometimes answers from training knowledge where a search would catch details that have changed, such as what is allowed, required or charged. Take out wording like "only use tools when strictly necessary" or "minimise tool calls". When the job has a search tool, tell it to check such specifics even when it feels confident, and for researched work (a report or comparison) to gather current sources rather than write from memory.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 research or fact-checking job, or source change
- id: tool-trigger-test
  applies_when: task success requires a tool call
  guidance: Forced tool use isn't available on Sonnet 5.5, so the way to make it call a tool rather than answer in text is to say in the brief when that tool applies. Name the evidence the job must gather and, where a particular tool matters, why and when to use it; test whether it picks the tool before adding any universal must-call rule.
  basis: provider-guidance
  source: official_sources[1]
  evaluation: pending
  review_trigger: first tool-required Sonnet 5.5 pilot, or source change
- id: no-reasoning-in-reply
  applies_when: a brief for claude-sonnet-5-5 would ask it to "write out your reasoning", "show your thinking" or include its reasoning in the reply
  guidance: Remove that wording. Asking the model to reproduce its internal reasoning in the reply invites a reasoning_extraction safeguard decline, which no automatic fallback retries. Ask instead for the conclusions and the evidence behind them (what it checked, file and line, command output).
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job that returns a reasoning_extraction decline, or source change
- id: safeguard-refusal-not-a-bug
  applies_when: a delegated claude-sonnet-5-5 job's result reports a decline or refusal instead of doing the work
  guidance: A decline can come from a safety classifier rather than a bug; its categories are cyber, bio, frontier_llm, reasoning_extraction and general_harms, and benign work can trigger general_harms. Finding vulnerabilities in source code is allowed. In Claude Code, a cyber-flagged Sonnet 5.5 request re-runs on Sonnet 5 (shown in the transcript), while a bio-flagged one ends in a refusal because Sonnet 5.5 has no biology fallback model; so a job may have run on a different model than planned, and its observed model must be reported.
  basis: provider-guidance
  source: official_sources[0]; official_sources[4]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job that returns a safeguard refusal or a fallback notice, or source change
- id: decline-goes-to-a-person
  applies_when: a delegated claude-sonnet-5-5 job declines or refuses the work
  guidance: Don't reword the same brief to get past the decline; surface it for a person to decide. This is Kerd policy, not provider guidance.
  basis: invariant
  source: Kerd authority rule (a decline is the person's to decide; Conductor's delegated-job rules)
  evaluation: pending
  review_trigger: a Kerd authority-rule change
- id: instructions-not-inside-tool-output
  applies_when: a brief or mid-task message to a claude-sonnet-5-5 job carries pasted tool output, or Conductor sends the running job a course correction
  guidance: Sonnet 5.5 is trained to resist prompt injection arriving through tool results, and sometimes misreads a genuine message as one when the message sits inside a tool result or arrives right after one; it may then ignore it, ask for confirmation, or say the tool output held text posing as a message from the user. The guide's fixes are for API harnesses (never put user text inside a tool result; send it as its own user turn after the last result; keep harness notices separate from the user's words). In Kerd's terms, keep every instruction outside pasted tool output, fence the pasted output clearly as data, and never phrase instructions so they look like part of it. If a job reports that an instruction looked like injected text, treat that as this misread and resend it as a plain message of its own rather than rewording it to sound more authoritative. How Claude Code places a mid-task message to a running subagent relative to its tool results is not stated on these pages.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job that ignores or questions a Kerd instruction as possible injection, or source change
- id: json-answer-think-first
  applies_when: a claude-sonnet-5-5 job must return a JSON answer to work that takes a few steps (totalling figures, applying a rule, ranking items)
  guidance: On these tasks the model often answers without thinking first, especially at low and medium, and accuracy drops. End the brief with "Think the problem through before you answer", or run it at xhigh; at high that line brings accuracy close to xhigh for a modest token increase. Kerd's native route asks for JSON in the prompt, so the model may work the problem out in text and put the JSON at the end, sometimes after a draft; whoever reads the reply should take the last complete JSON value, not everything from the first brace to the last, check it has the expected fields, and retry once if not.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job whose JSON reply Kerd parses, or source change
- id: dense-visual-tools
  applies_when: a claude-sonnet-5-5 job must read a dense chart, technical drawing or diagram image
  guidance: Tell the job to crop, zoom or run code on the image (Kerd jobs can do this with a script); with such tools it reads these inputs markedly more accurately. For charts the tools help at every effort level and beat raising effort (with tools at high it read charts better than at max without, at a fraction of the cost); for technical drawings they help only from high up, most at xhigh and max.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job judging a rendered diagram or chart, or source change
- id: findings-report-everything
  applies_when: any claude-sonnet-5-5 job that reports findings — code or document review, sweep, audit, or a reader grading evidence
  guidance: Don't write "only report high-severity issues", "be conservative" or "don't nitpick"; the model can obey such a bar closely and silently drop real findings below it. Ask for every finding, uncertain and low-severity ones included, each with a confidence and a severity, and let Conductor or a separate step filter; if the job must filter itself, give a concrete bar (for example "anything that could cause wrong behaviour, a failing test or a misleading result; omit only pure style or naming preferences").
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 review or sweep whose recall is checked against known issues, or source change
- id: literal-scope
  applies_when: a brief gives an instruction that should apply to more than the one item it names, or a job could drift beyond the item it names
  guidance: The Sonnet 5 guide found the model doesn't extend an instruction from one item to the next or infer a request that wasn't made, most of all at low and medium; the 5.5 guide adds that at higher effort or on open-ended requests it can do more than asked. State scope both ways in the brief ("every file in the set, not just the first"; "only these files"), and name every deliverable you expect back.
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 job that applies a rule across several items, or source change
- id: literal-instruction-audit
  applies_when: the compiled prompt contains overlapping or exceptional rules
  guidance: Remove conflicts and state the intended exception next to the rule it narrows; do not rely on implied precedence.
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 pilot with overlapping rules, or source change
- id: brief-complete-up-front
  applies_when: briefing any claude-sonnet-5-5 player or composer
  guidance: Put the task, its intent and its constraints in the single brief rather than feeding them in over later messages; Anthropic found a complete first turn keeps both quality and token use better than a vague one clarified piecemeal. Choose effort by effort-recalibrated, not by the Sonnet 5 advice to start coding at high or xhigh.
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 player that needed a mid-job correction, or source change
- id: report-length-and-shape
  applies_when: the job's reply has a length or shape Conductor depends on
  guidance: The model sizes its reply to how complex it judges the task, so short on lookups and long on open analysis. When Kerd needs a particular shape or length back, describe it in the brief, ideally with a short example of a good reply rather than a list of things not to do.
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 reply too long or too thin to use, or source change
- id: no-forced-progress-updates
  applies_when: a brief for a long claude-sonnet-5-5 job would ask for interim status messages
  guidance: Don't add "summarise progress every N tool calls" scaffolding; the model writes notes between tool calls on its own. If Kerd needs updates at particular points, name those points and what each should contain (see no-hold-findings-wording).
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first long Sonnet 5.5 job with unusable updates, or source change
- id: prose-voice-restate
  applies_when: a claude-sonnet-5-5 composer or player writes long-form prose in a set voice
  guidance: Don't assume a voice prompt tuned on another model still lands; state the voice in the brief (or point to kerd:skriv) and check the first draft against it. Ask for variety in words, since sampling settings still aren't available on Sonnet 5.5.
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 prose job checked against a voice, or source change
- id: frontend-defaults-concrete-spec
  applies_when: briefing an HTML, frontend or design build on claude-sonnet-5-5
  guidance: Found on Sonnet 5 and not restated for 5.5; without direction the model settled into one house style, and generic wording ("clean and minimal", "not that colour") only swapped it for another fixed palette. Give a concrete spec (palette, type, radius, layout, sections), or have the job propose a few distinct directions first and build only the one chosen.
  basis: provider-guidance
  source: official_sources[3]
  evaluation: pending
  review_trigger: first Sonnet 5.5 frontend brief, or source change
```
