---
profile:
  provider: anthropic
  family: opus-5-5
  version: 2026-09-24
  applicable_models: [claude-opus-5-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
      retrieved: 2026-09-24
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-09-24
    - url: https://platform.claude.com/docs/en/models/opus-5-5/overview
      retrieved: 2026-09-24
    - url: https://code.claude.com/docs/en/model-config
      retrieved: 2026-09-24
  last_evaluated: null
  supersedes: opus-5-5@2026-09
---

# Claude Opus 5.5 profile

Local interpretation for pilot use. Opus 5 keeps its own profile (`opus-5.md`);
this file records only what differs for 5.5, not a restatement of clauses that
still hold unchanged.

```yaml
- id: effort-default-medium
  applies_when: briefing any claude-opus-5-5 job
  guidance: Default effort is medium, one level below Opus 5's high default. Start every opus-5-5 brief there and set it explicitly; don't carry over an opus-5 effort setting, because effort names don't line up between the two models (medium on 5.5 matched or beat opus-5 at high on coding and knowledge work in Anthropic's testing, and low came close on several coding evaluations). Trying other levels, lower as well as higher, is allowed and encouraged; adopt a setting for a job type from those trials' results. In Claude Code, medium is what a 5.5 session gets unless an explicit choice or applicable settings override it, so report the active level as unverified unless it was read from the session.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first opus-5-5 effort sweep or source change
- id: effort-raise-on-evidence
  applies_when: a job's evals show medium falls short, or the job is long-running agentic or coding work
  guidance: Reserve xhigh and max for job types where Kerd has measured a quality gain. Don't raise by default for "demanding" work the way the opus-5 profile does; at a given level 5.5 already thinks more per turn than opus-5. Observed once (2026-09-24, one pair, not a frozen eval): a five-bug code review found all five at both medium and high, medium with about a quarter fewer output tokens.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first xhigh/max comparison on a Kerd job or source change
- id: thinking-always-on
  applies_when: writing a brief or harness instruction for claude-opus-5-5
  guidance: Adaptive thinking cannot be turned off at any effort level (opus-5 allowed disabling it at high and below). Drop any "disable thinking" or "skip reasoning" instruction inherited from an opus-5 brief; effort, not a thinking toggle, is the only lever for how much it reasons.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first opus-5-5 job carrying an inherited opus-5 thinking instruction, or source change
- id: max-tokens-headroom
  applies_when: setting an output/token ceiling for a claude-opus-5-5 job, especially at higher effort
  guidance: API routes only. Size the ceiling for thinking plus reply, not reply alone — thinking tokens count against it even when not shown back. A ceiling sized for an opus-5 brief can truncate a 5.5 reply; 128,000 (the model's max) has worked for long agentic-coding turns. Kerd's native Claude Code route (kerd:<model>-<effort> agents) sets no max_tokens, so this clause does not apply there.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first truncated opus-5-5 reply or source change
- id: text-only-end-not-done
  applies_when: reading back a delegated claude-opus-5-5 job's result, particularly an unattended or multi-step one
  guidance: A turn that ends with summary text and no tool call is a progress report, not proof the job is finished. Check the job's own checklist or score state before recording it done; don't accept the text alone as the returned change set. If the job started a background command or subagent that is still running, wait for it and read its output before recording the job done. Observed 2026-09-25 (two runs, one fan-out scenario): both leads ended turns with text while their background subagents still ran, so reading the first result alone would have recorded the job done too early.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first premature "done" recorded from an opus-5-5 text-only stop, or source change
- id: visual-density-tools
  applies_when: the job requires judging dense charts, diagrams, screenshots, or documents
  guidance: 5.5 reads visual material more accurately than opus-5 without extra tooling, so re-test whether scaffolding built for opus-5 is still needed before keeping it; don't drop it untested. For the densest inputs, such as technical drawings, higher-resolution images and a crop/zoom tool still add accuracy, and the model uses those tools better at higher effort. Without tools, raising effort helps drawings but does little for charts.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first dense-visual job on opus-5-5 or source change
- id: frontend-defaults-name-avoids
  applies_when: briefing an HTML or frontend build with no design direction supplied
  guidance: Without direction, 5.5 falls back to a few default styles, and a generic "avoid a generic AI look" instruction mostly swaps one default for another. Name the specific patterns to avoid (background treatment, label style, button shape, and so on), check the first result against that list and extend it. Giving a positive design direction as well is recommended. Observed once (2026-09-24, one pair): the generic instruction produced a cream background, an italic accent word, 01–04 section labels, monospace labels and pill badges; the named list removed them and produced a dark default page with the same hero-and-card layout instead.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first opus-5-5 frontend brief or source change
- id: unattended-premature-stop
  applies_when: an unattended claude-opus-5-5 run is observed ending a turn with text that announces a next step while its checklist still has open items and it names no blocker
  guidance: Confirm the stop is premature against the job's own checklist first. A controller-requested checkpoint, a pending approval, a genuine blocker or a bounded piece of work finishing is not a premature stop. For a confirmed one, continue with a short message naming the open items, and stop after two or three such nudges on the same task so a stuck run ends and is reviewed. The limit belongs in the harness; prompt wording cannot enforce it. The provider's standing no-early-stop instruction is for fully unattended runs only, never an interactive or human-in-the-loop session. Kerd builds none of this until a Kerd route shows the failure. Observed 2026-09-25 (two runs per variant, no run past about 3 minutes): 0 of 4 runs stopped early, with or without the standing instruction; long unattended runs, where the provider says early stops appear, were not tried.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first observed premature stop in a Kerd unattended opus-5-5 run, or source change
- id: fan-out-time-budget
  applies_when: a lead claude-opus-5-5 session is about to fan out several independent jobs and can estimate how long the work should take
  guidance: Observed 2026-09-25 (two scenarios, two runs per variant in each, stated budget only, no run past about 3 minutes): 2.2 to 2.6 times faster with the same recall on planted bugs. The lead did less verification and chose lower-effort foreground subagents. It did not fan out wider. The provider found a time budget with elapsed time shown on every message made agent teams finish sooner through more parallel work. Claude Code cannot append elapsed time to each subagent message, so Kerd could only state a budget in the brief up front. The budget is advisory: keep a real timeout where one is needed, and check quality and which effort the lead chose for its subagents, since under time pressure the model may search and verify a little less.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fan-out that states a budget, or source change
- id: explore-before-acting
  applies_when: briefing a claude-opus-5-5 job that is loosely specified and draws on several sources outside the files it will change (other repos, docs, tickets, mail) that the brief does not all name
  guidance: 5.5 tends to get to work quickly. Add one sentence telling it to look through the relevant sources, including ones the brief doesn't name, before it changes anything. Keep untrusted content out of what it searches, since the instruction tells it to act on what it finds. Observed 2026-09-25 (two runs per variant, one small repo): both runs without the sentence read the unnamed sources before their first edit, as did both runs with it, so its effect there was not shown.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first loosely specified multi-source opus-5-5 job, or source change
```

Kerd-owned example delta from the opus-5 rendering:

```yaml
model: claude-opus-5-5
effort: medium   # not opus-5's high default; raise only on measured evidence
```

Read-back on a returned job: treat a text-only end of turn as a progress
report, not a finished job. Confirm against the job's own checklist or score
before recording it done — do not add a generic "verify everything again"
instruction on top of that check.

