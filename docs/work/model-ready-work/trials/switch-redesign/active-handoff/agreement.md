# Prepared pickup preview

Outcome: let a person see what a prepared pickup will load, without reading a
JSON packet or exposing the private memory body on screen.

Deliver `pickup_preview.py`, `test_pickup_preview.py` and `USAGE.md` in this project.
Python standard library only. CLI accepts one packet JSON file. Importable
`summarize(packet)` returns display text; invalid input raises ValueError. CLI
errors go to stderr with a nonzero exit, not a traceback.

Success measures:
- M1: show the recorded branch/revision and each selected file/section, counts
  and text size. Count UTF-8 bytes honestly, not tokens. Input follows the existing
  packet shape: status pickup_prepared, branch, commit, clean_at_check,
  synchronized, sources [{file, selection, content}], and optional note.
- M2: identify local-only versus synchronized status; say prepared does not mean
  restored or accepted. Missing/invalid fields cannot look successful.
- M3: never display the source content, private session IDs, or unknown extra
  fields. Neutralize control characters from labels to protect terminal output.
- M4: tests cover realistic/Unicode input, multiple/empty/malformed sources,
  wrong booleans, privacy, terminal controls and CLI success/failure.
- M5: usage describes actual invocation, output and limits. Preserve the supplied
  real example unchanged, and do not rewrite this agreement.

Use useful judgment about implementation details. No approvals, fingerprinting,
CI or hooks are part of the product. No Git writes, network, background processes,
other agents, native session history or files outside this checkout. Only change
the three deliverables. Do not write handoff.json; the controller saves your reply.

Return JSON with status continue/review/blocked, next_action, memory, evidence
(cumulative relative file paths), failures (counts by measure), pending_jobs.
Ready for independent review is not user acceptance. Preserve existing failure
counts; they are historical trial state, not something to reset or fabricate.
