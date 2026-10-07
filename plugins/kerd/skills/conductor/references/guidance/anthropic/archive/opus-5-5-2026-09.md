---
profile:
  provider: anthropic
  family: opus-5-5
  version: 2026-09
  applicable_models: [claude-opus-5-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
      retrieved: 2026-09-23
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-09-23
    - url: https://platform.claude.com/docs/en/about-claude/models/overview
      retrieved: 2026-09-23
  last_evaluated: null
  supersedes: null
---

# Claude Opus 5.5 profile

Local interpretation for pilot use. Opus 5 keeps its own profile (`opus-5.md`);
this file records only what differs for 5.5, not a restatement of clauses that
still hold unchanged.

```yaml
- id: effort-default-medium
  applies_when: briefing any claude-opus-5-5 job
  guidance: Default effort is medium, one level below Opus 5's high default. Start every opus-5-5 brief there and change it only after Kerd's own evals show a gap — don't carry over an opus-5 effort setting. Effort names don't line up between the two models; medium on 5.5 already matched or beat opus-5 at high on coding and knowledge work in Anthropic's own testing.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first opus-5-5 effort sweep or source change
- id: effort-raise-on-evidence
  applies_when: a job's evals show medium falls short, or the job is long-running agentic or coding work
  guidance: Raise to xhigh or max only where Kerd has measured a quality gain for that job type. Don't raise by default for "demanding" work the way the opus-5 profile does — 5.5 sustains long unattended runs and multi-hour audits better at its own default effort.
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
  guidance: Size the ceiling for thinking plus reply, not reply alone — thinking tokens count against it even when not shown back. A ceiling sized for an opus-5 brief can truncate a 5.5 reply; 128,000 (the model's max) has worked for long agentic-coding turns.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first truncated opus-5-5 reply or source change
- id: text-only-end-not-done
  applies_when: reading back a delegated claude-opus-5-5 job's result, particularly an unattended or multi-step one
  guidance: A turn that ends with summary text and no tool call is a progress report, not proof the job is finished. Check the job's own checklist or score state before recording it done; don't accept the text alone as the returned change set.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first premature "done" recorded from an opus-5-5 text-only stop, or source change
- id: visual-density-tools
  applies_when: the job requires judging dense charts, diagrams, screenshots, or documents
  guidance: 5.5 reads visual material more accurately than opus-5 without extra tooling, so drop scaffolding built for opus-5 by default. Keep an image-inspection tool (crop/zoom) only for the densest inputs, such as technical drawings, where it still adds accuracy — raising effort alone helps drawings but does little for charts.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first dense-visual job on opus-5-5 or source change
- id: frontend-defaults-name-avoids
  applies_when: briefing an HTML or frontend build with no design direction supplied
  guidance: Without direction, 5.5 falls back to a few default styles, and a generic "avoid a generic AI look" instruction just swaps one default for another. Name the specific patterns to avoid (background treatment, label style, button shape, and so on) instead, and check the first result against that list.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first opus-5-5 frontend brief or source change
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

