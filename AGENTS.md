# Kerd model-profile catalogue

This branch (`catalogue`) holds the model-profile catalogue that Kerd's Conductor reads.
It is an orphan branch: it shares no history with `main`. Profiles are
`guidance/<provider>/<model>.md`, with provider-wide notes in `guidance/<provider>/shared.md`
and superseded versions in `guidance/<provider>/archive/`. The copies shipped inside the Kerd
plugin are the fallback when this branch can't be read. `guidance/README.md` defines the format.

A profile starts with a YAML header: `provider`, `family`, `version` (the date of the edit, YYYY-MM-DD; seed profiles from before the catalogue may carry YYYY-MM),
`applicable_models` (exact model IDs), `official_sources` (each a `url` and a `retrieved`
date, YYYY-MM-DD), `last_evaluated` (`null` until Kerd evaluates it) and `supersedes` (`<family>@<previous version>`, or `null`). Each clause in the profile's YAML block
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
  `archive/<model>-<its version>.md`, content unchanged.
- A revised profile gets a new `version` equal to the edit date (YYYY-MM-DD), different from
  every earlier version of that family; its `supersedes` names the previous version
  (`<family>@<previous version>`); and the previous file is copied to
  `archive/<model>-<previous version>.md` exactly as it was. Existing files in `archive/` are
  never modified or deleted. A violation is P1.
- Only `basis: provider-guidance` clauses are rewritten from vendor pages, and the citation
  rules above apply to those. A PR that changes or removes a `basis: kerd-eval` or
  `basis: invariant` clause is P1.
- Dates and model IDs are exact: `retrieved` and `last_evaluated` are real YYYY-MM-DD dates,
  `last_evaluated` may be `null`, `version` is a real date as above, and each model ID in `applicable_models` appears on a cited page.
- No promotional wording: clauses state operational guidance in plain terms.
