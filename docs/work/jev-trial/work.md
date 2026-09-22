# Work: is Jev worth trying inside Kerd?

## Direction

Anthony, 2026-09-21 23:43: "honestly just looking for use cases for this to see if its worth
trying." Jev is TypeSafe AI's System One model: state plus typed questions in, typed answers
with probabilities and confidence out, no generated text. Early access since 2026-09-15.
Agreed ("sure", 23:45): a one-off trial outside Kerd, no skill changed, on the graded claims
from the front-page check. README text only, which is public. Write up and stop.

## What was run (2026-09-21, late evening)

`run_trial.py` against `dataset.json`, model `jev-latest` (answered as `jev-1.13.0`), one
request per item, 118 requests, 0 errors, 48,108 input tokens (about $0.002 at the listed
$42 per billion), median 292 ms. Answers in `results.json`. Key read from the repo's `.env`,
never printed; checked absent from every file here.

Labels: the 55 claims and their verdicts come from the claim-reading agent's report of
2026-09-20 (22 proved, 21 never run, 7 not checkable as written, 5 wrong). Row 19 corrected to
proved (F5 of front-page-claims) and left out of condition B, because its evidence note
predates the proof. The nine overstatement sentences are the ones Codex blocked or Claude
withdrew, each paired with its corrected version; those labels are this session's.

## Results

**A · claim alone: "could any check show this true or false?"** Failed. It never said no:
all seven uncheckable claims scored 0.55 to 0.76 (at the 0.5 line, every one called
checkable), and five checkable ones scored below 0.5. Values sat in a narrow 0.39 to 0.95
band with no separation.

**B · claim plus the reviewer's evidence note: choose proved / not yet run / wrong / not
checkable.** 40 of 54 agree with the recorded verdict (74%). It caught all five wrong claims,
but also called eight others wrong, mostly proved claims whose notes carry a caveat.
Confidence did track correctness: median 0.85 when right, 0.545 when wrong.
- Acting only at confidence ≥ 0.7: 30 decided, 28 agree, 24 sent to a reviewer.
- At ≥ 0.9: 18 decided, 17 agree. The one exception (0.93, "the picture exists and renders")
  is arguably a bad label: the note says rendering was left to another job.
Caveat: the notes were written by the same agent that set the labels, and several contain
the verdict in words ("already established"). This tests turning written evidence into a
verdict, not finding evidence.

**C · sentence plus evidence: "does the sentence claim more than the evidence?"** Every one
of the five overclaims (0.66 to 0.87) scored above every one of the four accurate versions
(0.10 to 0.51). Nine items, and a thin margin: two accurate sentences sat at 0.51, so a 0.5
threshold would flag them. Tested once, not verified.

## What it means for Kerd

Jev does not find evidence; it grades evidence already written, fast and cheaply, and its
confidence is a usable routing signal on a verdict choice. In Kerd the expensive part is the
finding (reading the repo, running the install, a browser pass), and the grading is already
done inside a session that holds the context. So it saves little at Kerd's volume.

Where it could earn a place: a cheap screen before independent review. Grade every
evidence-backed sentence of a docs change, accept the confident ones, and send the rest, plus
every "wrong", to Codex. Condition C is the promising half and the least tested.

Not tried: Score questions, putting several questions in one call, a larger or independently
labelled set, and any comparison against an LLM doing the same grading on the same inputs.

## Now

Complete. Nothing committed. Open for Anthony: whether anything here is worth more than this
trial. Found on the way: `.env` at the repo root is not in `.gitignore`.

## Viability tests, proposed not agreed (2026-09-22 00:00)

Pass lines set before running, so a result cannot move them. Picture: `tests.html` / `.png`.
1. Backlog triage: the 73 judged rows in
   `docs/work/model-ready-work/trials/2026-09-12-conductor-session-closure-review.md`
   (3 done, 8 dead, 60 open, 2 unsure). Pass: at confidence ≥ 0.7, 9 in 10 agree, at least
   half decided, and no open row called done or dead. Data on disk.
2. Concert returns: real returns with their score steps, plus copies with planted faults.
   Pass: 9 in 10 faults caught, no more than 1 in 5 clean returns flagged. Needs building.
3. Hook checks: latency from a real hook, and voice scores on before/after rewrites from Git.
   Pass: 95% under one second, rewrite scores better 8 in 10. Needs building.
4. Pre-Codex screen: 170 past review requests with replies (in `.git/kerd-agent/requests/`,
   local only). Pass: flags most blocked reviews, clears half the cleared. Expected to fail.
Labels are earlier Opus or Codex judgments, so a pass means agreement with those judges.

## Viability results, tests 1 and 4 (2026-09-22, just after midnight)

Agreed ("y", 23:56). 158 more requests, 0 errors, median about 300 ms.

**Test 1 · Backlog triage: fails its pass line.** `run_backlog.py`, answers in
`backlog_results.json`. 58 of 73 agree with the 2026-09-12 review. At confidence ≥ 0.7 it
decides 42 (more than half) and 37 agree, 88% against the 90% line, and it calls 4 open rows
dead or done, against a line of none. At ≥ 0.9: 22 decided, 20 agree, 1 open row closed. Of 9
open rows it called dead or done at any confidence, the four confident ones (rows 3, 17, 36,
49) were all closed as dead a week later, when the ladder was retired on 2026-09-19. That is
a pattern worth knowing, not a pass: the reason they died did not exist on 2026-09-12. It
got 7 of 8 dead rows, but only 1 of 3 done rows.

**Test 4 · Screening before review: meets the line only at a threshold picked afterwards,
and a one-line rule does as well.** `run_reviews.py`, scores in `review_results.json` (request
ids and roles only; the requests themselves stay in `.git/kerd-agent/`, local). 114 replies
read and marked by hand: 58 blocked, 27 cleared, 29 excluded as not verdicts. Jev saw only the
request. It separates them somewhat (AUC 0.70; blocked median 0.62, cleared 0.55). At 0.5 it
flags 56 of 58 blocked but clears only 8 of 27; at 0.6, 37 of 58 and 19 of 27, which meets the
line; at 0.7, 17 and 24. The pass line named no threshold, so 0.6 was chosen after seeing the
scores. A rule with no model, "flag unless the request says recheck, final, confirm or
correction", flags 46 of 58 and clears 16 of 27. Within first rounds and within follow-up
rounds, Jev still ranks somewhat (AUC 0.69 and 0.66), so it reads something beyond the round.
As a screen it would skip review on requests that would have been blocked: at 0.6, 21 of 58.

**Both are tested once, not verified.** Every mark is an earlier Opus or Codex verdict, and
test 4's marks are this session's reading of them.

## Now

Tests 1 and 4 done; neither shows Jev earning a place. Tests 2 and 3 not built, by the
agreement (only if test 1 passed). Nothing committed. `review_results.json` carries local
review roles and should stay out of Git unless Anthony decides otherwise.

## Other projects surveyed (2026-09-22, 00:05)

Candidates found, none tested: 3of3's Archie hard tail (its spec asks for a model "constrained
to emit validated corpus IDs", NONE first-class; unbuilt), Bree's converse lane (Sonnet under a
40-a-day cap, mostly choosing; idle since July), Obair's `rank.py` keyword categories (blocked:
`Connections.csv` not on disk). No need found in Seinn, Leru, MusicTUI, Apple Music, Krutho,
Aran, Eolas or weefish. Anthony declined the Archie test ("no", 00:08).
