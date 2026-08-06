---
route: new
stage: done
---

# Goal record — release-closeout slice 1 (the repo-surface pass), 2026-08-06

Both keys given: cold eyes (opus reviewer, work order + change only,
verdict could block — sixth run, one block of a new class, amended
before this record) and the expert-user pass, which for this feature
was its own maiden run: the 2026-08-06 ~13:20 close bumped versions,
so close-out step 6 fired the release pass on the very release that
shipped it — tend clean, slainte found and fixed two medium drifts
(0bdd38f) and named three things it deliberately left untouched. The
restraint report — the killer risk's countermeasure — was observed
working on first fire.

## Done condition

Assembled from upstream declarations, every item a conformance check:

- **Met the contract** — 15/15 Pieces landed, every verify first-run
  (`docs/plans/2026-08-06-release-closeout-spec.md`; build 2b80dc6 ·
  render ea1a801); ten of fifteen steps delegated (9 haiku, 1 sonnet).
  One orchestrator callback: the score's ship lists missed its own
  step-10 file — caught by the conductor's collateral check, corrected
  by the score's author, who also fixed the conductor's wrong
  alphabetical-order callback instruction against git's actual sort.
- **Met the design** — one release definition (the version-field diff,
  CI's R1 set); the pass is two invokes and a charter (invoke pattern
  uses 3–4, skriv's one-shot audit on machine prose is use 5); the
  charter split holds: slainte's CI-duplicated rules pruned to a
  CI-owns pointer, rule 7's judgment family kept; `.slainte` deleted,
  targets derive from the repo; tend wired at its two moments
  (conductor's bare-repo orient offer, the release drift check);
  standalone `/kerd:slainte release` and `/kerd:tend` stay invocable.
- **Proof layers pass** — all seven local gate commands green at the
  build tip, the amendment tip, and this session's trigger-amendment
  tip (0716567). CI green headSha-verified on the feature's pushed
  tips: frame 07ade2c/a87a9b6, design GO 392d8b1/719905a, build
  2b80dc6/ea1a801, goal amendment a8ddc4d, maiden pass 0bdd38f. CI
  note, honest: the session-close tip b8b4c92 was cancelled in
  GitHub's own job setup (outage class, zero gate steps run) — rerun
  requested this session, in flight as this record is written; the
  trigger-amendment tip's first run is likewise pending at record
  time, its tree green on all seven steps locally.
- **Product measurements met** — doc-surface passes per release
  0 → 1 (observed: the maiden run fired at the shipping close, by
  contract not memory); slainte fixes instead of reporting (observed:
  two drift fixes shipped as a gated work commit, 0bdd38f — README's
  conductor walkthrough claimed a cold-path vault read false since
  v0.64 and omitted both new wires; the playbook tree comment listed
  7 of 10 skills); restraint reported (three left-untouched items
  named in the pass's report); the hand-kept target list is gone
  (`.slainte` deleted, targets derive from the repo).

## The block, and its resolution

Cold eyes' sixth run: layers 1–3 passed clean (slainte's shipped text
byte-identical to spec), one layer-4 block of a class not seen in the
five prior gates — **falsified-by-own-build**. playbook:178 credited
slainte with the three checks this very build moved to CI: the line
was accurate at v0.84.0 and made false by the commit under review.
The design-time concept sweep runs against the old tree, so a line
describing behaviour the build is about to move reads as accurate and
never enters the edit map. Amended a8ddc4d. Standing consequence,
mirrored to the playbook: the sweep needs a goal-time companion — and
the release pass this build shipped is exactly that companion, now
firing at every release.

## The expert-user pass

The pass and the shipped behaviour were the same event — the third
feature in one day to close by using itself (vault-unhook's pass was
its boundary, conductor-boundary's was its close, release-closeout's
was its own maiden run). Tony's observation carried one finding, and
it reshaped the trigger: the pass fired because that close bumped
versions, but his release model is **ladder completion** — the two
diverge exactly at goal-record sessions, where a feature closes as
complete with no bump and the pass would stay silent at the moment
the narrative surfaces most need checking. Cache honesty: the
session's skill text was 0.79.0 throughout; the shipped contract was
honored deliberately, per the vault-unhook precedent.

## The trigger amendment, keyed at this record

Tony's key at this record: the pass gains a second firing moment — a
session that lands a goal record (a new `docs/gates/*-goal.md`, a
feature closed as complete) fires the pass, bump or no bump. One
release definition stays (the version-field diff, R1); the completion
clause is a firing moment, not a second release heuristic. Amended at
all seven living trigger sites plus both canvases, shipped 0716567
(v0.86.0). This record's own landing is the amended clause's first
match: the close of the session that writes it fires the pass on the
new trigger — observation and record collapsing into one act, again.

## Hands to

LOOP — every version bump and every feature close now runs the pass
by construction; nothing waits to be remembered. Slice 2 (declared
external surfaces) sits in Backlog High; the CI graduation
(version-bump-without-What's-New refusal) stays behind the accepted
risk's review trigger; the state-contract warts named for the pass's
first self-test sit in Backlog Medium.
