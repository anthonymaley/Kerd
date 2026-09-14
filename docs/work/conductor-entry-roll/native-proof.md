# Managed Conductor native proof — 2026-09-14

## Verdict and scope

One bounded source-level loop completed through fresh managed contexts. This is
not installed-plugin acceptance, natural context-pressure evidence, host-crash
survival, pressure-aware Claude coordination or a token-efficiency comparison.
The prior failed trial is recorded in work.md, not overwritten by this result.

Scratch project: `/tmp/kerd-managed-proof.GyXOzn`. No consumer project, install,
commit or publication occurred in the trial. Raw private request/result files
and source identities remain in that scratch project's `.git/cross-llm`; its
run ledger is `.git/roll/run.json`. Scratch files are local, not a permanent
portable archive. This sanitized account contains no private native IDs.

Agreement: review an existing incorrect clamp(value) first, correct real
findings, test below-zero/zero/interior/ten/above-ten behavior, record actual
test evidence and independently review the changed result before completion.
Allowed edits: clamp.py, test_clamp.py, evidence.md. No network, installs,
commits, publication, background tasks or nested model calls. The agreed outcome
was deliberately tiny to bound the lifecycle trial, not because it merits a
managed workflow in ordinary use.

Coordinator/implementer: requested and observed gpt-5.6-sol; requested high.
Reviewer: requested and observed claude-opus-5; requested high, file-inspection
route. Profiles: GPT-5.6 2026-09-05 and Opus 5 2026-09. Effort is recorded as
requested, not inferred from model identity. CLI: codex-cli 0.154.0.

## Observed sequence

| Step | Actual result |
| --- | --- |
| Fresh Conductor 1 | Forced threshold 1 observed usage 14,966 against a reported 258,400 context window; returned a durable checkpoint, source exited |
| Fresh Conductor 2 | Requested independent review of the existing code |
| Claude review 1 | Returned actual clamp defects and required tests/evidence |
| Fresh Conductor 3 | Received a real stop-only request while running; checkpointed the findings and exact correction/re-review next action |
| Driver stop | Returned paused and process exited; one contribution retained, no correction launched |
| Explicit trial resume | Same agreement, place and configuration, fresh host process and native coordinator |
| Fresh Conductor 4 | Requested the correction, carrying the exact open findings |
| Codex implementation | Corrected clamp.py, wrote five tests and recorded the actual successful command/result |
| Fresh Conductor 5 | Requested a NEW independent review of the changed tree |
| Claude review 2 | Passed against agreement, code, tests and recorded evidence |
| Fresh Conductor 6 | Acknowledged the result; completed with no open findings or pending jobs |

Nine distinct native sessions: six decisions, one implementation, two reviews.
All three contributions are linked and validated. Failure history retains
independent_review: 1. The final review is pass, with the current-tree gate met.
All Codex results report owned children gone; all nine requests completed and
the driver checked their process groups before proceeding. The explicit stop is
a test-control action, not a routine approval required at context rollover.

The trial ran once up to pause, then resumed once. It did not replay an uncertain
request. A tiny pressure trigger was applied only to the first coordinator;
remaining turns used the normal adapter reserve. It does not test a naturally
near-full 258,400-token context or provider behavior at that load.

The resumed source included the completion-refusal retry change. The subsequent
same-tree-review oscillation counter correction was fixture-tested; that branch
was not reached by this successful native sequence (no completion refusals).

## Independent artifact check by the control session

Read all three output artifacts. Ran, independently of the worker:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_clamp.py
test_above_ten ... ok
test_below_zero ... ok
test_interior ... ok
test_ten ... ok
test_zero ... ok
Ran 5 tests in 0.000s
OK
```

Result implements clamp with comparisons below 0 and above 10, returning the
input otherwise. The tests exercise -1, 0, 5, 10 and 11. No broader numeric-domain
acceptance or production usability claim follows from those five cases.

Prompt byte sizes, in session order: 6,031; 6,398; 2,626; 10,556; 11,514;
6,798; 9,759; 5,143; 9,510. These exclude native instructions/tool schemas and
are not token counts. Native usage counters are retained separately; this
intentionally elaborate lifecycle trial is not an efficiency benchmark.

Summed native usage across the completed requests (not simultaneous context):
Codex input 300,043, including 215,552 cached; output 7,397. Claude reports input
10, cache creation 20,944, cache reads 47,062 and output 2,180 separately. Do not
turn those request totals into a context-window percentage or treat differently
reported provider counters as a matched cost comparison. Fresh decision sessions
have real briefing overhead; use this route for sustained work, not tiny edits.
