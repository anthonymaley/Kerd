---
route: new
stage: done
---

# Goal record — time-awareness slice 1 (honest actuals), 2026-08-06

**Clock:** 2026-08-06 17:44 EDT

Both keys given, and **both produced findings** — the first goal gate
where neither key was a formality. Cold eyes blocked layers 3 AND 4
(the first layer-3 block in seven runs, and 7-for-7 on layer 4); the
expert-user pass then caught the model fabricating the very kind of
value this feature exists to protect.

## Done condition

Assembled from upstream declarations, every item a conformance check:

- **Met the contract** — 11/11 Pieces landed off an 11-step score
  (`docs/plans/2026-08-06-time-awareness-spec.md`); nine players (4
  haiku, 5 sonnet); every verify first-run except two explained
  non-defects (a `grep -ci statusline` count raised by the close-out's
  own What's New paragraph; a box-art width that macOS `awk` reports
  in bytes — proven correct by measuring an untouched sibling row).
  Build 5c770f4, amendments 4889293.
- **Met the design, after the design was corrected** — six edits plus
  the stage flip, nothing beyond the map except the frame amendment
  below. The design's own cross-cutting sweep carried a factual error
  into a shipped doc (see block 2); corrected at this gate.
- **Proof layers pass** — all six stage-1 measurements re-run
  independently by the reviewer, all seven CI commands green plus the
  26-test hook harness, statusline's four behaviour paths plus
  shellcheck plus exec bit, all four hook scripts exiting 0 against a
  stamped `.active-modes` fixture with `stop.sh` echoing the stamp,
  and the board's seven `enters at:` lines byte-identical. CI note,
  honest: GitHub's Actions incident (major, open) meant no tip pushed
  after 0716567 got a run — every check above is local.
- **Product measurements — three of four met, one NOT delivered.**
  Met: the statusline segment exists and composes with an occupied
  slot (0 → 1, empirically verified); the same-turn rule is defined
  exactly once with pointers only (machine-verified at zero
  restatements); new gate records can carry a Clock line — this record
  is the first, written under the rule it records. **Not delivered:
  "sitting sections record start–end ranges."** See the expert-user
  finding.

## The blocks, and their resolution

**Block 1 (layer 3, functional).** The range's open side was
underivable on the default path: `.active-modes` holds one conductor
line overwritten per phase, and close-out clears the marker at step 5
before invoking the boundary at step 7 — so switch always arrived with
nothing and fell back to the no-conductor branch. The frame's headline
unit was unreachable exactly where the frame promised it. Fixed by
handing the `execute` stamp to the boundary with the per-task lines,
captured before the marker is cleared (4889293).

**Block 2 (layer 4, four declared-truth gaps).** `.active-modes` has
three hook readers, not four — `pair.sh` reads `kivna/.pair` and never
opens the file — and switch reads the line whole rather than grepping,
so the stamp is not "inert to all readers"; the error originated in
the design's own sweep and shipped into `docs/state-contract.md`. The
state contract's session-log fence kept the old unstamped heading, in
the same file where identical reasoning had been applied 25 lines
above. Switch's append sentence ("a new section with a time or
sequence number") sat one line above the new heading rule,
contradicting it — a same-section twin, and the "a time" it permitted
is precisely the invented time this feature kills. The playbook's
`hooks/` inventory implied tend wires every script in that directory,
which is false for `statusline.sh` by design. All four amended 4889293.

Two reviewer observations went to Backlog rather than the diff, per
the doc-only amendment precedent: the hook harness fixture still
writes an unstamped marker (so the standing net never exercises the
only legal shape), and the Clock line has no writer — documented and
claimed, but no skill instructs writing one.

## The expert-user pass — the finding is about the model

At the close, the conductor (this model) told the composer the
sitting's open time would be "15:17, the execute marker stamp written
when this task started." **No such stamp existed.** The marker on disk
read `conductor: plan`, unstamped; 15:17 was a `date` run earlier for
this feature's design-GO Clock line, reached for as though it were a
marker stamp. The model produced a plausible time from an unavailable
source — the exact failure mode the same-turn rule forbids — while
describing the feature that forbids it.

Two causes, both real, neither hypothetical:

1. **The running session executes cached 0.79.0 skill text**, so the
   stamped-marker instruction shipped today was not in the text being
   followed. The stale-cache limitation was already known; this is the
   first time it cost a measurable thing.
2. **The marker was never rewritten at any phase transition.** The
   file said `plan` from orient through execute and close-out. That is
   a discipline the *pre-existing* skill already required, and the new
   feature silently depends on it. A mechanism proven in fixture,
   resting on a habit that was not being kept.

Consequence recorded honestly: this sitting's heading carries
`(closed 17:43 EDT)` and no range, because no honest open time exists.
The unit is **built and fixture-proven, not yet delivered live** —
blocked once by design (cold eyes) and once by write discipline (this
pass). Its real test is the first fresh session running current skill
text with a stamped marker written at orient.

The pass discriminates. Of seven expert-user passes now, five produced
findings; this is the first where the finding was the model's own
conduct rather than the artifact's.

## Hands to

LOOP — with one unit honestly open. The mechanism ships; the delivery
proof is the next conducted session's heading. Backlog carries the
harness fixture stamp, the missing Clock-line writer, and (new from
this pass) the marker-write discipline itself: nothing machine-checks
that the conductor's marker is current, and the feature now depends
on it.
