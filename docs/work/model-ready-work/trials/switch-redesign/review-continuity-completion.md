# Independent retained-evidence assessment

The independent reviewer inspected the original Codex and Claude Roll metadata,
all six request/result pairs, native tool events, complete agreements and final
saved-place files under the original isolated trial root
`/tmp/kerd-roll-proof.QujmIu`. No work was reenacted, no private reasoning was
read, and raw native identities are not published here.

## Findings

- Each provider used three distinct native sessions: two fresh transitions.
  Both sequences were continue → continue → review. Completed requests did not
  overlap, and no human next/go message appeared between pieces.
- Every prompt contained the exact full agreement, unchanged model/effort request
  and authority. Every next saved-place input exactly matched the previous reply;
  final place matched the final reply.
- Implementation decisions, next actions and evidence grew through implementation,
  tests, then inspection/documentation. Tool events did not show completed pieces
  being restarted or skipped. Final Claude corrections were explicitly assigned
  inspection work, not repeated completed pieces.
- The seeded continuity-check count of 1 survived every boundary. Claude's
  self-caught writing issues remained in working memory without being falsely
  reported as executed test failures.
- All six usage records matched provider results and remained accumulated.
  Unavailable Codex cost stayed null. No resource cap existed, so behavior at a
  cap was not tested. No permission or accounting reset is implied.
- Both returned review-ready, not self-accepted. Codex tool output showed 13
  passing tests; Claude consistently disclosed its inability to execute tests.

This closes the missing independent continuity assessment for the original
bounded two-transition builds. Those runs used deliberately prescribed piece
boundaries and an earlier helper revision. They do not by themselves verify
current runtime code, pressure-triggered behavior or termination of every child.
Later lifecycle and observed-context trials provide separate, scoped evidence.

One historical scope deviation remains explicit: Codex's first smoke check wrote
two temporary diagnostic files outside the agreement's literal three deliverables.
The authority text stayed unchanged across Roll; this is not evidence of authority
being expanded by a fresh window. Do not claim perfect historical file isolation.

## Cleanup

The reviewer also inspected the Seinn TODO diff. Seven removed narratives were
resolved, absorbed or superseded; independent unfinished findings stayed open.
Both retained original archives matched their baseline Git blobs by SHA-256.
The changes record retained reasons, applicable decisions and retrieval routes.
Selected restoration results support useful pickup. This meets the scoped cleanup
evidence need, not a promise to recall every possible historical fact.

## Still open

The matched pickup comparison and complete pickup footprint require their own
results. Final user review remains required. No live installation is implied.
