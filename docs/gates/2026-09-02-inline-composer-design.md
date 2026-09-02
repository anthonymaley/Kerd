---
route: problem
stage: designed
---

# Design GO — inline-composer

**Clock:** 12:05 EDT

## GO

Design approved: `docs/design/inline-composer.md`, with the sealed view
`docs/design/inline-composer/inline-routes.html` (`Tony, 2026-09-02 ·
fp:17d01f87d0e8`).

## The keyed design — the producer's words

> - Inline work produces one work-specification artifact, sized by content.
> - That file may provide distinct evidence at design and handoff; the producer
>   keys design judgment, while the machine checks build readiness.
> - A waiver is an exceptional, deliberate skip with visible debt — not the
>   inline default.
> - A legacy closure advances historical work past a routing gap while
>   explicitly preserving the missing-evidence gap.
> - A forgotten gate remains blocked.

## What this key does NOT cover

- **The machinery.** `tools/gates/` is untouched, per the frame's own exclusion.
  Nothing renders `design waived`, nothing carries a waiver forward as debt,
  and nothing recognises one file as evidence at two rungs. Later
  implementation work; the conceptual route was deliberately not shaped around
  today's globs.
- **`switch-fidelity`'s waiver** and **`model-effort-advisory`'s legacy
  closure.** Both are separate acts on separate items and are excluded from
  this commit by the producer's instruction.
- **Risk 4's refuser** — a check that a score was written. Unenforced in slice 1
  by design, named on every surface, review trigger standing.

## Review history

Revision 1 was **refused** 2026-09-02. Claim 1 held. Claim 2 was rejected on a
false argument — *a score cannot satisfy design because the composer is not the
producer* — which the producer refuted: authorship was never the test, the
producer's key is, and a model typed every design document in this repo. The
rejected shape also recreated the item's own killer risk by making a ten-field
waiver the inline default. Claim 3's wording overclaimed impossibility and was
corrected to *the process did not require or retain it*. The `view: n/a`
refusal was rejected and the drawing was made. The measurements were not targets
and now carry a number and a scope each. A final correction at the eye replaced
*"closes nothing"* with the routing-gap / evidence-gap distinction.

## Measurements keyed with this design

| Measure | Baseline | Target |
|---|---|---|
| Inline-routed work leaving a valid score | 0 | 100% of inline-routed items begun after release |
| Items stuck at a rung with no record of why | 3 (`model-effort-advisory`, `switch-fidelity`, `hooks-autoload`) | 0 |
| Waivers carrying all ten required fields | n/a | 100% — **unenforced**, producer-read |

**Producer key:** Tony, 2026-09-02
