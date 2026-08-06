---
route: new
stage: done
---

# Goal record — conductor-boundary slice 1 (the close-out runs the boundary), 2026-08-06

Both keys given: cold eyes (opus reviewer, work order + change only,
verdict could block — five layer-4 blocks, all amended before this
record) and the expert-user pass, which for this feature was the
2026-08-06 late-evening close itself: the first one-act boundary, run
live with Tony watching — close-out invoked `/kerd:switch out` as its
final act, no handoff ask, and the banner ended with the next pick and
the `/clear` ritual. No finding was raised; the composer's next word
was "keep going", aimed at the next pick the banner had just named —
the feature's intended loop, observed working on its first run.

## Done condition

Assembled from upstream declarations, every item a conformance check:

- **Met the contract** — 11/11 Pieces landed, every step verified
  first-run (`docs/plans/2026-08-06-conductor-boundary-spec.md`;
  commits b8140a7 · ed34392 · 6b5d218); six players (2 sonnet,
  4 haiku) off the 11-step score, 7 delegate / 4 keep.
- **Met the design** — the 17-edit map landed whole; the
  single-definition law holds beyond the spec's own greps (the
  reviewer's independent sweep of conductor for switch-out step
  vocabulary returned zero hits — one instruction to invoke, zero
  descriptions); Switch In and Switch Out steps 1–6 byte-identical to
  parent; both flagged beyond-map additions applied as flagged.
- **Proof layers pass** — all six local gate commands green at the
  build tip and re-verified by the reviewer; `stale` green after the
  render commit. CI note, honest: the amendment and boundary tips'
  first runs died in GitHub's own job setup ("Service Unavailable"
  resolving actions — infrastructure, not a gate; no gate step
  executed), re-runs requested the same sitting. Every earlier tip of
  the feature (b3b919f/e81e45e frame, 2d63926/ff7e7b0 design,
  b8140a7/ed34392 build) is CI-green headSha-verified.
- **Product measurements met** — boundary acts per conductor session
  2 → 1 (observed: the close ran as one act); the no-decision handoff
  ask is gone (grep 0, and none was asked at the live close); the
  close named the next pick from TODO (observed in the banner); the
  ritual line appeared (observed); standalone `/kerd:switch out`
  intact (byte-proven, and exercised standalone earlier the same
  evening at the post-vault-unhook boundary).

## The blocks, and their resolution

Cold eyes blocked five declared-truth gaps at layer 4 (layers 1–3
passed without reservation — five-for-five blocking on that layer
across the goal gate's history): README's conductor-opening still said
"hand the boundary to switch" while the mapped edit fixed only its
sibling sentence one paragraph away; README's switch section carried
the byte-twin of the ownership sentence the design deleted from the
skill file; conductor's own opening line kept the unqualified "never
commits session state" against its amended principles bullet;
conductor-role.md's never-becomes list read as a prohibition v0.84.0
now crosses as a caller; and CONTEXT.md's v0.67.0 standing decision
needed its supersession clause. All amended 6b5d218 (the CONTEXT
clause riding the boundary commit 08a15b4, as session state must).
The catch class evolved again: two gaps were same-section TWINS of
correctly-mapped edits — the design-time sweep grepped by phrase and
missed sibling wordings. Standing consequence, mirrored to the
playbook: **the edit-map sweep greps by concept, not by phrase, and
reads each surviving section whole.**

Two reviewer observations became Backlog rows rather than night
patches: a CI rule to machine-enforce the single-definition law
(nothing refuses a future re-description today — a named limit), and
the close-out double-write wart (step 1 writes CONTEXT/TODO, the
invoked flow overwrites both — pre-existing, now visible in one act).

## The expert-user pass

The pass and the shipped behaviour were the same event, the second
time in one day this repo has closed a feature by using it: the
build's own session ended through the new close-out. The running
session's cached skill text was 0.79.0 — the shipped v0.84.0 contract
was honored deliberately, per the vault-unhook precedent; the first
cache-native run arrives with the next fresh session. The invoke
mechanism itself was proven in both directions inside one session:
switch-in chained into conductor at open, conductor chained into
switch out at close.

## Hands to

LOOP — the close-out cannot end a conducted session any other way
now; every future conductor session exercises the one-act boundary by
construction, and every close names the next pick. The in-half of the
ritual (automating `/clear` + switch-in) stays in Backlog with its
confirmed wall; the CI rule for the single-definition law and the
double-write wart sit behind their Backlog rows.
