# PROPOSED — acceptance record draft, rung-vocabulary slice 1

> **THIS IS A DRAFT AND IT IS NOT THE RECORD.** It sits in `docs/plans/`
> deliberately. `tools/gates/kit.py:789` globs `docs/gates/*-<slug>-acceptance.md`
> and qualifies any match carrying a `## Release condition` section — so the
> trip-wire is the glob, not the filename. A file with this content anywhere in
> `docs/gates/` would flip the router to `ready-to-release` before the producer
> had accepted anything, which is the one thing this gate exists to prevent.
>
> **On the producer's key**, this content moves to
> `docs/gates/2026-08-25-rung-vocabulary-acceptance.md` and
> `docs/product/rung-vocabulary.md`'s front matter goes
> `stage: designed` → `stage: ready-to-release` **in the same commit** — the
> producer-visible state change is atomic, so no audit can observe a half-state.
>
> **The second key is not given yet.** The expert-user pass below is written as
> what remains, not as something done.

**Clock:** drafted 2026-08-25 20:14 EDT

## Release condition

Assembled from upstream declarations. Every row is a conformance check against
something declared before the build, never authored here.

- **Met the contract** — 16/16 pieces landed, verified against the tree rather
  than read off the checklist. `docs/plans/2026-08-25-rung-vocabulary-spec.md`
  carries 16 `## Pieces` items, all checked; `cbf8458` carries 16 `Piece:`
  trailers, one-for-one with them; each piece was opened and confirmed present
  in the tree by an independent reviewer that never saw the build. Every one of
  the 16 steps carries a real `**Verify:**` block. Commits `cbf8458` (work,
  14:13) · `8ffd5a7` (render, 14:13) · `fb20eaf` (release close-out, 16:12) ·
  `64ff7cb` (cold-eyes amendments, 20:14).

- **Met the design** — the declared sweep in `docs/design/rung-vocabulary.md`
  landed whole in both directions: every declared site changed, and every
  changed-but-undeclared file is legitimate collateral of the fold rather than
  scope creep (`progress_kit.py`'s `goal_for` → `piece_strip_for` rename is the
  notable one — necessary, independently specced, and a gap in the design's own
  sweep table rather than a build defect). The build stayed inside
  `## Scope` and `## Deliberately not in this item`: no `docs/product` →
  `docs/work` migration, no `skills/drive/`, no `loop → learn`, no wholesale
  Stage-Gate vocabulary. The design GO record's appended amendment was
  re-verified and is accurate on all three of its corrections.

- **Proof layers pass** — nine of nine green at the tip, each run rather than
  assumed: `gate.py selftest` (45 cases) · `gate.py audit` (clean; 1
  pre-existing finding about the requirements register, unrelated) ·
  `gate.py release` (clean, three version fields synced at 0.100.0) ·
  `progress.py selftest` (15 ok) · `progress.py stale` (render current) ·
  `matrix.py selftest` (16 ok) · `matrix.py audit` (clean) ·
  `gen_journey.py check` (7 stages) · `tests/hooks_test.sh` (22/22). CI green
  on every commit of this item.

- **Product measurements met** — against `docs/design/rung-vocabulary.md`'s
  five declared stage-1 measurements. **Two are machine-verified:** route
  positions blurring machine work with producer approval, 2 → 0; execution
  mechanics exposed as producer-visible gates, 2 → 0. Both hold — `RUNGS`
  contains no `goal`, `build`, `verify` or `adjust`, and selftest asserts
  `enters_at` never returns them. **One is met under a stated qualification:**
  term-of-art collision, 7 of 8 → 7 of 7, met by the *"session handoff"* /
  *"work handoff"* rule rather than by `handoff` being unique — the producer's
  own ruling, and zero bare uses remain in ambiguous position. **Two are
  honestly declared unmeasurable** — cross-work readability and newcomer
  searchability — and were left as named gaps rather than given numbers
  invented after the fact. That is the gap `gate-visuals` left open at its own
  gate, deliberately not repeated here.

## Cold eyes — the block, and what it cost

Four blind reviewers over `cbf8458..fb20eaf`, none of which saw the session
narrative. **Layers 1 and 3 passed. Layers 4a and 4b blocked**, holding to the
pattern: the declared-truth layer has now blocked at every gate where it ran.

**The finding that changed the acceptance bar.** `gen_journey.py` keys steps by
section heading and looks them up by stage *label*. The fold renamed three
labels; `docs/design/funnel-steps.md` kept the old headings. Every journey page
went from 1 `Rungs not defined for this stage yet` block to **3** — a plausible
false claim printed over steps that existed four lines away. Every gate stayed
green and CI passed, because the two sides are a living interface joined only by
a string, and nothing tested it.

The producer's ruling: regenerating pages proves only that they match the
current source, so it would have preserved the same blank panels forever. The
countermeasure shipped in `64ff7cb` is a **check, not a rule** —
`check_stage_schema()` refuses in both directions, `stage_steps()` enforces it
so no render can emit a false blank, and CI runs it on every push. Proven by
reproducing the exact regression: the check exits 1 naming both halves, and the
render exits 1 rather than publishing.

**Eleven further declared-truth corrections**, each verified against `kit.py`
before the edit — the full list is in `64ff7cb`. The pattern across all of them
is the one this build already recorded: *an enumerated sweep is precise and
non-exhaustive*, and every gap was a site the enumeration did not name.

**Ruled out of scope, recorded rather than fixed.** Three stale sealed views
belong to other work items — `funnel-driver/why-an-umbrella.html` and
`funnel-driver/span-vs-slice.html` (both newly found here) and
`gate-visuals/visual-lifecycle.html` (already filed). Resealing another item's
view re-keys the evidence its producer is about to judge. They are that item's
business at that item's gate.

**One finding refuted.** The prose reviewer flagged conductor's *"work handoff"*
as an invented label; it is the producer's 2026-08-23 ruling verbatim, and the
non-compliant twin is `README.md:42`'s bare *"the design and handoff stages"*.
Recorded inverted, at low severity.

## The expert-user pass — NOT YET GIVEN

The second key is the producer using the output. Nothing below is claimed.

What it would exercise: run `gate.py route` on a live slug and read the rung
names back; open a journey page and check the stages say what they should;
frame something new and see whether the killer-risk floor asks the right
question at the right rung.

## The live test this record triggers

This is the first `*-acceptance.md` the repo will ever write. Conductor,
slainte and switch all moved their completion triggers to that glob on
2026-08-25, and **whether they actually fire has never been observed** — the
rename's own most dangerous defect class was a trigger going quiet while every
drawing and gate record still looked correct. When this record lands, close-out
should fire the release pass without being asked. If it stays silent, the
rename is broken in exactly the way the ruling was aimed at, and nothing on the
board would show it.

## Known limits of this record

- The proof layers prove reachability and conformance, never comprehension.
  A doc that names a file passes even if it misdescribes it.
- `## Grounding` resolves file paths and not symbols inside a line, so a
  grounding entry can still name a function that does not exist. Filed.
- The seven legacy `-goal.md` records remain, unrewritten and read-only. The
  filename check validates shape, not intent: a freshly written `-goal.md`
  would still pass it. The write discipline is prose, not machinery.
