# Codex review of the Switch Out saved-place box and the 0.112.0 diff — 2026-09-12

Requested by Anthony: Claude restored the Out completion box dropped at 0.107.0
and prepared 0.112.0; Codex (the paired TUI thread) reviewed the box and the
final diff before anything was committed. Two read-only rounds, retrieved by
marker from the Codex rollout through Agent.

## Round one: four findings, all fixed before commit

1. The failed-save box still recommended clearing context. **Fixed:** the
   free-context hint follows only a remote-verified or committed save; otherwise
   the box says to keep the session open and resolve the save. Tested for five
   states.
2. A missing save status rendered as "nothing committed". **Fixed:** absent or
   unrecognised `saved` renders SAVE STATUS NOT RECORDED with no completion claim
   and no clear-context hint; the guide says so.
3. The LOG row bypassed wrapping and broke the width at a long path. **Fixed:**
   LOG renders through the wrapped row; width regression test at 78 and 100.
4. The spec's living `## Now` still said the implementation review was waiting.
   **Fixed:** status and the review outcome reconciled in
   [spec.md](spec.md), the earlier wait kept as history.

Codex also noted, not as a blocker: a top-level JSON array exits 1 with an
`AttributeError` in both closing and summary modes, a pre-existing shared rough
edge.

## Round two

"Ready to commit and push from this review: all four corrections verified, 89
renderer tests pass, and `git diff --check` is clean; no remaining findings
within the requested scope."
