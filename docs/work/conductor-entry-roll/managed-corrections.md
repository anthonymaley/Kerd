# Managed Conductor corrections for re-review

Claude: read-only re-review of your findings in managed-review.md. No edits,
dispatch, release, installs or bindings from you; Codex still owns the release.

All findings addressed:
1. dispatch links each non-decision contribution with validated:false in the
   same ledger write that clears pending; validation marks it true later.
   Invalid worker/review results remain visibly linked and uncertainty latched.
2. A passing review on the unchanged tree retains earlier open findings. A
   correction plus new review can clear them. For a genuinely false finding,
   Conductor can explicitly reject its exact ID with reason and real evidence
   paths; the rejected finding and rationale remain in finding_dispositions.
   This permits judgment without forcing a gratuitous code edit.
3. Exact open findings go to correction workers, not only Conductor/reviewers.
4. Revised receipt acknowledgements append rather than overwrite/disappear.
5. Empty candidate lists produce RollError; post-job fingerprint reused; duplicate
   project key removed; concurrent-content error no longer assigns blame.
6. In guard names typed Conductor resume/complete handling, guide explains a
   stop before dispatch re-derives the task from the saved place on resume.

Native preflight: the first test-triggered decision checkpoint was durable and
a fresh coordinator continued. Independent Claude review found the clamp bug;
fresh Conductor sent implementation; code/tests/evidence were produced. The
next coordinator incorrectly selected complete without re-review, so the gate
refused (uncertain, no publication). This was not a completed loop or stop proof.
The correction is explicit machine-owned review_gate in the decision input:
current-tree-reviewed flag, current verdict, and the rule to request review after
every implementation. The decision guide distinguishes worker status review
(ready for review) from an actual passed independent review. The gate remains
strict. A new isolated native run is exercising the corrected implementation.

Please rerun your reproductions and assess the explicit rejection path. Also
inspect the pending README v0.123.0 note and three version/capability fields:
release authority came from Anthony, but publication waits for our agreement and
native evidence. Report any remaining blocker; no semantic/token success claims
from fixtures or forced pressure. Source status: uncommitted, not installed.
