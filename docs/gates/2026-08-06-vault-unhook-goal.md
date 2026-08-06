---
route: new
stage: done
---

# Goal record — vault-unhook slice 1 (the vault becomes opt-in everywhere), 2026-08-06

Both keys given: cold eyes (opus reviewer, work order + change only,
verdict could block — its fourth run, and its best catch yet) and the
expert-user pass, which for this feature IS the 2026-08-06 day-sitting
boundary: the first real switch-out run on the shipped v0.83.0
contract, observed live, with Tony at the keyboard end of it. The
blocks raised at layers 1/3/4 were resolved by amendment (33656f3)
before this record.

## Done condition

Assembled from upstream declarations, every item a conformance check:

- **Met the contract** — 12/12 Pieces landed, every step verified
  first-run (`docs/plans/2026-08-06-vault-unhook-spec.md`; commits
  4aa301b · d89f1e5 · 33656f3), six players dispatched off the 12-step
  score.
- **Met the design** — the coverage table named every vault artifact's
  fate (duplicated-in-repo · vault-only-kept-via-on-demand; `people/`
  the genuine residue, kept), and the three proof obligations came back
  exact: automatic boundary writes 1 → 0 by grep, kivna's edit
  `2 0` by numstat (two lines added, zero removed), Switch In
  byte-identical before/after.
- **Proof layers pass** — all seven CI steps green on every ship SHA
  (4aa301b, d89f1e5, 33656f3), headSha-verified.
- **Product measurements met** — the boundary's automatic vault write
  is gone (observed at the first post-ship switch-out: no vault
  written, the banner named the change); `/kerd:kivna save` performs
  the full write on demand, untouched; the killer feature — fresh
  session, switch in, one second ago — unchanged byte-for-byte.

## The blocks, and their resolution

Cold eyes blocked at layers 1, 3 and 4 — the fourth run, and the first
to catch the *design itself* rather than wording: the edit map missed
the two documents that actually route the boundary behaviour —
`skills/conductor/SKILL.md` (four boundary-vault claims) and
`docs/state-contract.md` (four rows) — plus six lesser declared-truth
sites still asserting the automatic write. All amended in one sitting
(33656f3), CI green. A standing rule was born from the block: **any
slice touching system-wide behaviour owes a cross-cutting `grep -rn`
sweep at design time** — the playbook's oldest gotcha, promoted to a
design-rung obligation.

A note for the record: writing this record was itself refused once.
The spec's own quoted blocks (a deleted SKILL.md section, the README
What's New insert) tripped a fence-blind step parser, and the build
rung derived `need 2` over a verified, CI-green build — the record
would have contradicted the board. The parser went fence-aware first
(v0.83.1, 2a0ea4a, fixtures T25/T26), the board flipped to
build/goal pass, and only then was this record written. Derived truth
holds rank over the record that cites it.

## The expert-user pass

The pass and the shipped behaviour are the same event: the 2026-08-06
day-sitting switch-out ran the boundary on the freshly shipped
contract — no vault write occurred, and the completion banner carried
the line naming the change (vault not written, on-demand since
v0.83.0). The observation and the record are one act; nothing was
staged for the demo. Honesty note carried from the session log: the
running session's injected skill text was still the 0.79.0 cache, so
the boundary honored the shipped contract deliberately rather than by
skill-text default — the next fresh session picks up the 0.83.x text.
No finding raised beyond the interview's own side-products, which were
already in Backlog before the build started (boundary-cycle,
auto-sizing, stop-hook, kivna verdict, trim-cut).

## Hands to

LOOP — nothing further for this slice: the deleted step cannot run,
so the opt-in behaviour guards every future boundary by construction.
The vault stays fully writable on demand; nothing in any vault was
deleted. The kivna verdict (import/export/scaffold archaeology) and
boundary auto-sizing stay deliberately unqueued behind their Backlog
rows.
