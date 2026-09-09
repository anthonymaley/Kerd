# Work: a "Where we are" view for one active Kerd work item

Run through the candidate Conductor at `docs/work/model-ready-work/skills/conductor/SKILL.md`.
Installed Kerd, Drive, gate tools and session markers are not used or changed.

## Direction

For the producer, at a glance, in the terminal where the work is happening.
Shows one active Kerd work item: its outcome and journey stage; completed,
active, next and blocked work separated; which model is doing each job; any
decision the person owes, unmistakably; and links to the actual result and
evidence. Source is the existing work record — not a second tracker.

User-stated, 2026-09-09: keep the first version to one work item; the
many-project dashboard waits. Saved status and live activity must be
distinguishable; an old snapshot must never read as "running now".

## Success and proof

Two checks the producer stated:

1. Can they tell what is happening, and whether they are needed, without
   reading a report?
2. After agreeing the direction, does the work reach a verified result without
   them typing "next"?

Proposed by Conductor, not yet agreed: the view renders from a record it did not
help write; every field it cannot find reads as "not recorded" rather than being
guessed; and an independent review checks the saved-versus-live labelling against
a record whose state has moved on.

## Boundaries and decisions

In: one work item, one view, reading records that already exist.
Out: many-item overview, a web dashboard, live process probing, any new tracker
file, changes to installed Kerd, hooks, CI or the parked schema-split session.

Must: no invented liveness; no new file the person has to maintain.
Prefer: readable in a terminal over tmux/SSH; evidence reachable by path.
Open (delegated within scope): exact layout, glyphs, parser shape.

Time/resources: none stated. Stopping point: a working view over one real Kerd
work item, independently reviewed and corrected, committed and pushed.

## Agreement

Agreed 2026-09-09, in the producer's words: "With those adjustments, direction
approved. Build, independently review, correct and verify within the proposed
scope. Keep progress visible and continue without routine approval stops."

The adjustments, all binding on the build:
1. Show one work item — this one. Do not mix adoption milestones or evaluation
   gaps into its jobs. An untested visibility outcome is not blocked work.
2. Read existing headings where their meaning is explicit. Label missing or
   ambiguous information; never turn prose interpretation into confident status.
3. Separate "rendered at" from "record updated at". No timestamp means unknown.
4. Never infer running activity from an assigned model.
5. Keep the decision, its proposed answer and the easy response inside a fully
   bounded box.

## Decisions and changes

- 2026-09-09, producer: this work item, over another invented trial.
- 2026-09-09, producer: Conductor shows a proposed view, takes agreement on the
  experience, then builds, reviews and corrects without routine stops.
- 2026-09-09, Conductor: this session's host exposes no native task-list tool
  (checked, not assumed), so journey.md's compact refreshed list is the fallback.

## Jobs

- [done] Direction agreed · producer — five corrections, then approval → work.md
- [done] Build the terminal view · Claude Opus 5 — 23 checks → where_we_are.py
- [done] Independent review · Claude Sonnet 5 (requested; not observed) — 8 findings
- [done] Correct the 7 confirmed findings · Claude Opus 5 — each retested
- [done] Save the boundary · Claude Opus 5 — pushed, verified at origin/main
- [next] Your judgement · producer — do the two checks pass?

## Now

Record updated: 2026-09-09 12:37 EDT
Stage: Deliver
Current activity: none. The build is reviewed, corrected, pushed and verified;
the work now waits on the producer's assessment of the two checks.
Analysis so far: the candidate's work records are prose under a writing aid that
explicitly is not a parser contract. So the source rule is the real design
decision: read the conventional headings and degrade honestly, add a labelled
block to records (a tracker the producer ruled out), or have a model read the
record each time (not reproducible, and it blurs saved versus live).
Recommendation: read the conventional headings; show anything missing as "not
recorded". A record that cannot say what is happening should show that.
Open issues: none blocking. Whether the two producer checks actually pass is
tested after the build, not assumed by it.
Pending question: Do the two checks pass — could you see what was happening and
whether you were needed, and did this reach a verified result without you typing
"next"?
Proposed answer: check 2 has an answer in the record; check 1 is yours alone.
Reply with: Passed / Not passed — say which one failed
Next action: the producer answers the two checks. The boundary is the commit
"A 'Where we are' view that refuses to interpret" on `main`, verified at origin;
its ID is in `git log`, not written into the record it saves.

## Results and evidence

`where_we_are.py` renders one record; `test_where_we_are.py` holds 22 checks, all
passing. Run it with `--record <path>` and an optional `--width`.

Found by running the build before any review, and fixed: an explicit
"Pending question: none" rendered as a decision box containing "none"; the YOU
line quoted Agreement prose as if it summarised it; lines overflowed at 80 and at
60 columns. A fourth was my own measurement — macOS awk counted bytes, making a
79-column line look like 81.

Independent review (Claude Sonnet 5 requested, identity not observed) returned
eight findings. Seven were reproduced against the code before being fixed, and
each now has a check that fails if the defect returns:

1. A second `## Now` section silently discarded the first one's pending question,
   then stated no decision was pending. Repeated sections are now labelled and
   not read from at all.
2. Headings inside fenced code were parsed as record state, so a quoted example
   could fabricate a question and a stage. Fenced content is now dropped entirely.
3. A field stated twice is now labelled and not read, rather than resolved by
   position. The reviewer also proposed judging whether a field sits under
   narrative prose; that is declined — deciding which `Stage:` line "really means
   it" is the prose interpretation this view exists to refuse. Repetition is
   checkable; tone is not.
4. `·`, `—` and `→` inside a title were torn out as fields, inventing an actor
   that was never recorded. Separators now require surrounding spaces.
5. A word longer than the box broke its border. Over-long words are now split.
6. Wide characters overflowed the box while the code's own `len()` metric read as
   aligned. Padding now counts terminal columns, and the checks measure columns
   independently rather than reusing the module's metric — the reviewer's point
   that a test sharing the implementation's blind spot proves nothing.
7. `Record updated` fell back to a `## Direction` timestamp, presenting an
   unrelated date as the status's currency. It now reads only the status section.

Finding 8, accepted as a limit rather than fixed: nothing stops unrelated content
being pasted into a record's `## Jobs`. The renderer has one file and no basis to
judge relevance; inventing that policy would be the interpretation this view
refuses. It stays an authoring discipline.

Correcting the review's own findings also introduced a bug that the new checks
caught: fenced lines were excluded from heading detection but still landed in the
section body, so the field appeared twice.

Verified against a record the view did not help write — `consolidation.md`, which
uses no `Stage:`, no `## Jobs` and contains fenced shell examples. Every field
reads "not recorded" or "unknown" rather than a guess, and the fences do not
corrupt it.

Two further defects surfaced after the first boundary, both by rendering this
record and reading the result:

- The view showed a pending question written across three lines as its first line
  only — a silent truncation that presented half a question as the whole one. A
  field value now runs on until a blank line or the next field, with a check.
- The record itself was wrong: an earlier edit to the job list silently did
  nothing, because the replacement was made without asserting that its target
  matched, and it was committed that way. The view exposed it by showing four
  jobs as still to do that were already done. Subsequent edits assert their
  target. The `Record updated` line was also written ahead of the clock and is
  now read from `date` rather than assumed.

That is the same failure this whole sitting opened with — a record outliving its
own next action — caught this time by the thing built to catch it.

Not established: whether the two producer checks pass. Only the producer can say
whether they can see what is happening, and whether the work reached a verified
result without them typing "next".
