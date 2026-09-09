# Active work moved between local checkouts

Status: **successful local handoff and continuation observed**. The destination
finished the preview tool, all 10 artifact tests pass independently, and Claude
found no blocking artifact issue. This is a local rehearsal, not automatic device To.

The source built the pickup preview implementation and saved a real unfinished
place: tests and usage remained. The destination received that place, the original
agreement and the same commit, then continued without a new user instruction.

Observed 2026-09-07, UTC:

| Event | Time | Observation |
|---|---|---|
| Unfinished checkpoint ready | 14:55:26.837 | Source parent still alive |
| Local remote save verified | 14:55:27.323 | Source parent still alive |
| Source shutdown confirmed | 14:55:27.418 | Owned children and group checked gone |
| Destination started | 14:55:28.067 | Exact saved revision loaded |
| Destination ready for review | 14:59:26.965 | Fresh worker finished, owned children stopped |

Saved revision: `7fc468abbdc511cce47a436e4cadb554e8aa48de`, on the disposable
`active-handoff-trial` branch. The remote is a local bare repository, not GitHub.
This is one controller-owned sequence, not a distributed lock against arbitrary
sessions on other machines. Source worker start to destination cleanup took about
5 minutes 31 seconds. That includes useful implementation and tests; it is not
handoff overhead, a pickup-budget result or a speed comparison. Both workers used
gpt-5.6-sol/high, and M3's explicitly seeded count remained 1 across the transition.

## Evidence and deliverable

- [Observed events](events.json), [source result](source-result.json),
  [destination result](destination-result.json): sanitized actual readings, no
  private session IDs. Distinct native session identity was checked by the driver.
- [Source prompt](source-prompt.json), [destination prompt](destination-prompt.json)
  and [agreement](agreement.md): the destination got the saved work, not a transcript.
- [Preview tool and usage](output/USAGE.md): lists chosen records, recorded state
  and UTF-8 sizes without printing their memory bodies. Worker output is retained
  unchanged, not installed. Labels and the optional note must be display-safe
  material; this is not a general secret redactor.
- [Artifact review](review-artifact.md): no blocking findings, with minor display
  limits and controller-tested dispositions. All 10 artifact tests pass in both
  destination and copied output. Ten additional local checks pass: eight driver
  admission/preservation cases and two supplemental artifact checks.
- [Driver review and disposition](review-runner.md): the actual run used
  [run-observed.py](run-observed.py). Later [run.py](run.py) adds history and saved-
  place checks, Python-cache exclusion and destination candidate validation.
  Those later corrections are unit-tested, not claimed as another live replay.

Controller also checked the original clone revision against the saved commit's
parent, the absence of extra source commits, unchanged destination HEAD, and
unchanged handoff/agreement/example against Git. No unsupported global
single-writer or all-host-compatibility guarantee follows from this one sequence.

## Product boundary uncovered

The existing Roll adapter stops its worker after a completed turn, before the
caller can publish a Git handoff. The trial-only observer performs the save while
that turn is complete but the parent still exists. Actual shutdown then precedes
destination dispatch. No installed adapter or live session was modified.

To make this a product route, completion of a worker's turn must be separable from
release of its session: a failed save must keep the source available for recovery,
with destination dispatch stopped. Today the adapter's cleanup still exits the
worker on save failure. Keeping the outer controller and files recoverable is
useful but is not the promised retained source session. That requirement stays
open; this rehearsal does not quietly weaken it.

No live Seinn edits, GitHub writes, installation, source user-session exit or new
device check occurred. The only commits/pushes are inside disposable local repos.
