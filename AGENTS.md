# Kerd model-profile catalogue

This branch (`catalogue`) holds the model-profile catalogue that Kerd's Conductor reads.
It is an orphan branch: it shares no history with `main`. Profiles are
`guidance/<provider>/<model>.md`, with provider-wide notes in `guidance/<provider>/shared.md`
and superseded versions in `guidance/<provider>/archive/`. The copies shipped inside the Kerd
plugin are the fallback when this branch can't be read. `guidance/README.md` defines the format.

A profile starts with a YAML header: `provider`, `family`, `version` (YYYY-MM),
`applicable_models` (exact model IDs), `official_sources` (each a `url` and a `retrieved`
date, YYYY-MM-DD), `last_evaluated` and `supersedes`. Each clause in the profile's YAML block
carries `id`, `applies_when`, `guidance`, `basis` (provider-guidance, kerd-eval or invariant),
`source` (an `official_sources[n]` index, or the evaluation or invariant it rests on),
`evaluation` and `review_trigger`.

`retry.md` lists work cut back for a model's capability, one line each.

## Code Review Rules

- Every added or changed clause cites an official page (its `source` resolves to an
  `official_sources` entry with a `url`) and a `retrieved` date for that page.
- The clause's `guidance` must match what the cited page says. If the page does not support
  the claim, flag it as P1.
- Nothing outside `guidance/` and `retry.md` may change. Any other changed file is P1.
- A model added or retired is named in the PR description. A retired profile moves to
  `archive/` with its prior version intact.
- Dates and model IDs are exact: `retrieved` and `last_evaluated` are real YYYY-MM-DD dates,
  `version` is YYYY-MM, and each model ID in `applicable_models` appears on a cited page.
- No promotional wording: clauses state operational guidance in plain terms.
