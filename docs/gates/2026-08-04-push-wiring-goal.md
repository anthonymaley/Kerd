---
route: new
stage: done
---

# Goal record — push-wiring slice 1 (the staleness refuser), 2026-08-04

The ladder's first goal gate. Both keys given: cold eyes (opus reviewer,
work order + change only, verdict could block) and the expert-user pass
(Tony). One BLOCK raised and resolved by composer-keyed amendment before
this record.

## Done condition

Assembled from upstream declarations, every item a conformance check:

- **Met the contract** — 4/4 Pieces landed, 6/6 steps verified
  (`docs/plans/2026-08-04-push-wiring-spec.md`; commits 4a0f45f ·
  1f7f570 · bc0c07e · 8c0a838).
- **Met the design** — cold-eyes layers 1–4 all PASS: code verbatim to
  Part B, no constructible false-zero, single-serializer holds
  (`write_pair` is the only pair-writer in `tools/`), shipped behavior
  matches `docs/design/push-wiring.md` item by item.
- **Proof layers pass** — `selftest: 13 ok` locally and in CI; all seven
  CI steps green on both ship SHAs (1f7f570, 8c0a838), headSha-verified;
  Mac↔Linux byte-identity proven by both runs.
- **Product measurements met as amended** — staleness at a pushed tip:
  ≤ one CI run, never silent (both-ways demonstration + green history);
  remember-steps: 0 silent (fixture asserts the fix-line message
  verbatim; session evidence: five pushes shipped with zero render
  obligations held in anyone's head).

## The block, and its resolution

Cold-eyes layer 5 (product measurements) BLOCKED: CI on a direct push
runs after the ref moves — the build delivers detection at the tip, not
refusal before landing, while design and product declared prevention.
Composer chose amendment over enforcement (protecting main would kill
the direct-push working style): declarations restated as
detection-at-tip in 821f475 (CI green), true prevention recorded on the
product ledger as an accepted unknown with a named return condition.
Two declared-truth contradictions fixed in the same commit (at-HEAD vs
disk; spec stage lag); the latent PR-event edge is backlogged.

## The expert-user pass

Tony used the output cold. Verdict: the slice's value stands — nothing
about the render can now be silently stale. Finding: the human pull
surface is insufficient — a static SVG and a terminal table are hard to
consume quickly; the expert user wants an interactive HTML view. That
finding is the Value line of the next piece (merging the already-named
"gate.py rendering through the progress view" slice), to be framed
through the gates as the ladder's next passenger — not built on impulse.

## Hands to

LOOP — nothing further for this slice; the next piece enters at frame.
