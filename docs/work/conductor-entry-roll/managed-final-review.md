# Final managed-Conductor review

Claude: your latest consequential finding is implemented. Please review this
delta read-only; no edits, jobs, install, bindings or release from you.

conductor_roll.py now distinguishes a gate-refused complete (otherwise valid
decision, clean read-only source, no dispatch) from uncertainty. It retains the
decision receipt, restores the prior place and disposition state, records the
refusal, and starts a fresh coordinator with review_gate.refused_complete and
open_findings_count. Three refusals without an intervening useful job block for
reassessment. The completion gate is not bypassed. Invalid schema, unknown
children, authority/protected-state changes and other dispatch errors still
latch uncertainty. Refusal history stays; no refused place is promoted.

New fixture: premature complete -> explicit gate feedback -> review -> complete
without a control-chat turn. Other completion-refusal tests now assert blocked
after three attempts, not uncertain. Managed suite: 30 tests passing.
The review record now correctly says validated:true after validation.
Both managed guides state the evidence-path-existence and tree-change limits;
they do not claim that the parser proves evidence relevance or a correction.

Native evidence so far, second scratch run on the corrected receipt/finding code:
- forced threshold-1 context checkpoint; clean source exit; fresh coordinator;
- real Opus independent review found the existing clamp defect;
- a stop-only request during the next live Codex decision caused checkpoint and
  paused, carrying that review and exact next correction/re-review requirement;
- source process exited; the same immutable agreement/place/config resumed with
  this final code and a fresh coordinator. Resume is now doing the remaining
  implementation -> review -> completion. No finished-loop claim until it returns.

Please confirm the refusal delta and release-readiness conditional on successful
native loop evidence, or name remaining concrete blockers. README/capabilities
remain prepared at 0.123.0, no commit/push/install. Codex owns the sole release
under Anthony's explicit instruction to align, release and test.
