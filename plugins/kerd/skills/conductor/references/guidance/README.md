# Local model guidance

This directory gives Conductor quick, local instructions for preparing work for
each model family. A person using the process does not need to read these files
or know prompt engineering. Start with [model choice](model-choice.md) for the
capability shortlist, evidence and selection method; then read the applicable
prompt profile. Use local guidance first and refresh only relevant stale or
missing facts, not a vendor-documentation tour during every task.

Current model-specific files live directly under the provider folder. Files in
`archive/` preserve prior run guidance; don't load them for new work unless
reproducing that run. The GPT-5.6 profile's 2026-09-05 revision removes the older
“cheapest eligible tier” rule to match the user's quality-first model selection.
The Opus 5.5 profile's 2026-09-24 revision (prior version in `anthropic/archive/`)
loosens two clauses to match the provider's wording, scopes max_tokens to API
routes, and adds three pending clauses from the same guide.
The 2026-09-27 revisions fill the Fable 5.1 and Sonnet 5 profiles from full reads of
their current guides (prior versions in `anthropic/archive/`) and add two clauses to
Opus 5.5; the Opus clauses are additions only, so its archived 2026-09 version stays
the one it supersedes.
The Sonnet 5.5 profile's 2026-10-08 revision (prior version in `anthropic/archive/`) adds
one kerd-eval clause, grading readers at medium, from three Kerd effort checks.
The 2026-09-29 addition is a new Sonnet 5.5 profile (`anthropic/sonnet-5-5.md`), from a
full read of its prompting guide, beside the unchanged Sonnet 5 profile, because Claude
Code's `sonnet` alias moved to Sonnet 5.5 on 2026-09-28.
The 2026-10-09 addition is a Haiku 5.5 profile (`anthropic/haiku-5-5.md`), from Anthropic's
docs only, with no matched Kerd comparison yet.
No model default, pricing, native permission or account setting changed.

## What is stored

- Concise interpretations of official guidance relevant to Kerd's work.
- Model-family differences that affect prompt structure, effort, tool use,
  context, autonomy, verification, or output control.
- Kerd-authored examples showing how one work brief is prepared for the model
  family.
- Source URL, retrieval date, applicable model identifiers, evaluation state,
  and review trigger for every clause.

Full vendor pages are not mirrored. They are large, copyrighted, and become
stale without announcing it. The registry stores only the operational guidance
Kerd uses, in Kerd's words, with direct provenance back to the official page.

## Required profile header

```yaml
profile:
  provider: anthropic | openai
  family: <stable local family key>
  version: YYYY-MM
  applicable_models: [<exact tested or declared model IDs>]
  official_sources:
    - url: <official URL>
      retrieved: YYYY-MM-DD
  last_evaluated: null | YYYY-MM-DD
  supersedes: null | <profile@version>
```

Every individual instruction then carries:

```yaml
- id: <stable clause id>
  applies_when: <observable condition>
  guidance: <local operational interpretation>
  basis: provider-guidance | kerd-eval | invariant
  source: <source index or invariant ID>
  evaluation: pending | <eval result ID>
  review_trigger: <when this must be reconsidered>
```

## Precedence

Host instruction hierarchy and native permission/tool contracts remain binding.
Within them: repository and producer boundaries → agreed work brief → relevant
evaluated guidance → applicable provider guidance → unevaluated recommendation.
Provider guidance never expands authority or overrides the agreed quality bar.

A model profile may change presentation and useful support. It may not change
the outcome, success measures, proof obligations, decision rights, or
boundaries.

## Lifecycle

1. Read changed official guidance.
2. Amend the local interpretation and Kerd-owned examples.
3. Create a new dated profile version; never silently rewrite the basis of a
   past run.
4. Run the frozen evaluation set against old and new profiles.
5. Promote instructions that improve results; delete or leave pending those that do
   not.
6. Record the exact profile version and model ID in every run record.
