# conductor-revision-out

First-user round 6, sitting 2 (batch-1114, first-user-6.md): the person brings the
product team's answers, and Conductor revises a launch brief that was already
delivered and accepted. In round 6, 0 of 4 such revisions ran Switch Out afterwards.
The case checks that Conductor makes the change, starts `/kerd:switch out` itself in
the same turn, and that Out then stops to ask before saving the person's own file.

- `scaffold.sh` rebuilds round 6's project as it stood after sitting 1, with the same
  commit IDs and no Git remote.
- `prompt.md` is the handoff Conductor received in rerun `r3`, word for word. It still
  says "Edit launch-brief.md only", so the case also checks that a limit on which
  files the work edits never limits Out.
- The case is one turn. The eval format adds a second turn only by resuming a recorded
  session (`context.history_file`), so the case ends at Out's save question and does
  not grade the closing box.

## How it is graded

Every grader except `reply-not-empty` is a model-judged rubric (`type: llm`). Three
review rounds on regex graders each found another wording or command shape the
patterns got wrong, so judging meaning moved to rubrics. `reply-not-empty` stays a
trivial length check.

The tests in `skills/switch/scripts/tests/test_round6_revision_finish.py` can only
check that each rubric states its criteria. They do not show that the judge applies
those criteria correctly. Only a real `claude plugin eval` run of this case can show
how the judge behaves, and none has been recorded yet. Each run pays for eight judge
calls, four of which read the whole trace.
