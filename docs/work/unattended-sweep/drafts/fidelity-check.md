# The fidelity check: proposal

*Draft for Anthony, 2026-09-25. Proposal only; nothing built.*

## The gap

Switch Out names a reading set (by default CONTEXT.md, TODO.md `## Now` and the newest
session log), measures its size and saves the `read_args`. Switch In reads those files. So
we know the files are reachable and small enough. Nothing asks whether the findings Out
meant to hand on are inside that text. The newest log drops out at the next dated log, and
a sketchbook marked "(local)" is untracked, so a finding recorded only there disappears
while every check stays green. A live example: the 2026-09-25 threshold check found that
the automatic chat roll's no-progress check never catches thrash. That finding is in the
2026-09-25 log and in `docs/work/rolling-session/threshold.md`, which is untracked. It is
not in CONTEXT.md or TODO.md. Tomorrow's In reads a new log and will not see it, and
nothing will say so.

A related defect found while checking this: `measure` accepts an untracked file (I ran it
on `threshold.md`; it measured it), while `prepare` refuses any file Git does not track.
Out can record a reading set that In's own helper will not assemble, and that another
machine does not have.

## Recommendation

Give `measure` two reports, and add one Out step.

1. Out writes the few findings that must survive (three to five, one line each) as
   `--carry "<phrase>"` arguments to the `measure` call it already runs.
2. `measure` reports, for each phrase, which selected source contains it, or "not in the
   reading set". It also marks each source as tracked or local only.
3. Out fixes any miss the usual way: write the finding into CONTEXT.md or TODO.md, or add
   its source section to the set. Then measure again.

Like the size reading, this never blocks a save. It reports; Out acts on the report.
That keeps it inside the 2026-09-19 ruling that retired the old refusing fidelity check.

**Hypothesis.** I believe naming the must-survive findings at Out and checking them
against the exact bytes In will read will stop findings from dying with the session log
or a local sketchbook, because the failure happens at Out and nobody names the finding at
that moment today.

**How we'd know.** Run it on the next five Outs. It worked if each miss it reports is a
real finding that would have been lost (the thrash finding should be the first), and if a
week later a spot check of each carried phrase finds it in the reading set of that day's
In.

## Cost

About 30 lines in `handoff.py` plus tests, one paragraph in `in-out.md` step 4, and a
patch release. At each Out: writing three to five phrases, about a minute. At In:
nothing.

## What it would not catch

- A finding Out never thought to name. The check is only as good as the list.
- Understanding. A phrase present in the text proves it can be read, not that In weighed
  it or put it in the arrival. That is the retrieval versus comprehension limit
  `docs/state-contract.md` already declares.
- Rewording. Exact text matching will miss a finding Out paraphrased when it moved it.
- Anything outside the repo: memory, the host's settings, the other provider's context.

Default: Out names the findings itself at every close, asking you nothing.

> 💬 **Is one minute of naming must-survive findings at every Switch Out worth it to you?**
