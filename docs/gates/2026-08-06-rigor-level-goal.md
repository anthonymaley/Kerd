---
route: new
stage: done
---

# Goal record — rigor-level slice 1 (the declared level + the refusal), 2026-08-06

Both keys given: cold eyes (opus reviewer, work order + change only,
verdict could block; died once mid-review on an API error and was
resumed from transcript with its partial verification intact) and the
expert-user pass (Tony, morning after the night run). Four BLOCKs
raised at layer 4 and resolved by amendment before this record.

## Done condition

Assembled from upstream declarations, every item a conformance check:

- **Met the contract** — 12/12 Pieces landed, every step verified
  first-run including the DESIGNED intermediate red at step 2
  (`docs/plans/2026-08-05-rigor-level-spec.md`; commits 6e65ff7 ·
  bf8c76c · ee43b6c · f671cdc).
- **Met the design** — cold-eyes layers 1–3 all PASS without
  reservation: the six kit.py edits byte-match the spec's blocks at the
  contracted insertion points, the spec carries the design's semantics
  exactly (single-parser rule verified by grep: two call sites, no
  third parse in `tools/`), and the built slice delivers the frame's
  amended promise with nothing from slices 2/3 leaked in. The reviewer
  independently reproduced the route byte-compare via `git archive` of
  the parent tree.
- **Proof layers pass** — `selftest: 24 cases passed` locally and in
  CI; all seven CI steps green on every ship SHA (ee43b6c, f671cdc,
  b60376e), headSha-verified.
- **Product measurements met** — a Release slice without a declared,
  legal rigor level is a named refusal at the tip within one CI run
  (AU6, both-ways demonstrated twice: once in the build's step 11, once
  by Tony's own hands at the expert-user pass); the three done
  journeys' route output byte-identical before/after the rule landed
  (the honest-retrofit guarantee, demonstrated, reproduced
  independently by the reviewer); every malformed shape named verbatim
  (fixtures T20–T23).

## The blocks, and their resolution

Cold-eyes layer 4 BLOCKED four declared-truth gaps (layers 1–3 clean —
the build was faithful; the words overclaimed): the "legal set lives in
one declared place" claim was false at three altitudes — the set
repeats as literal text in the refusal messages, the fixtures that pin
them, and the standard, and nothing machine-checks those literals
against `RIGOR_LEVELS` (the fixture suite cements drift rather than
catching it); the frame's Value parenthetical named the design gate as
the delivering mechanism when AU6-at-every-push is what makes the
target "uniform"; the gate table's design row omitted the
none-elsewhere clause the rung actually enforces; and the CI prose said
"three things can fail the build" over a 3-step snippet in the very
paragraph the build had edited (seven steps; AU1's file count was also
stale at six-for-ten). All amended honestly f671cdc, CI green — the
conductor also caught and corrected an overclaim in its own first
amendment text ("the fixture suite will refuse a partial edit" — it
will not; that was the reviewer's point). The code-level closure
(derive the messages and fixtures from the constant) is a named Backlog
item, not a night patch. Inherited-drift fixes (the CI numbers, the
snippet) rode the amendment commit because they sat in the file being
amended; the reviewer's two robustness warts (the `gate.py` root pin;
a fenced example line counting as a duplicate) are Backlog rows.

A note for the record: the staleness refuser fired mid-ship on the
contract's own commit vehicle (spec box-checks riding the render commit
move the derived model) — its fifth genuine catch, against its author's
explicit reasoning.

## The expert-user pass

Tony ran the audit himself against a planted missing-line state: the
refusal named the file and the fix verbatim; restore came back clean —
"came backl clean", then "good to go". No finding raised: after two
goal gates that each produced a re-scoping insight, this pass produced
none — the feature's human surface is one red light with the fix
named, and it read clearly on first contact. The author question that
grounding's pass surfaced answers itself here: the four retrofit lines
were written by the machine per the contract; the composer's key
touched only the level's value. The catalog (slice 2) inherits that
seating by design: pre-filled by the system, human key on deviations
only.

## Hands to

LOOP — nothing further for this slice; AU6 now guards every push.
Slices 2 (catalog + disposition table, carrying the hollow-waiving
countermeasure and per-level floors) and 3 (measured classes as CI
checks) stay deliberately unqueued behind their ledger rows.
