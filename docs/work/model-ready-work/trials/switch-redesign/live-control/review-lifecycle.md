# Independent lifecycle review

Read-only review by a separate agent of the live command channel, owned Codex
adapter, Roll lifecycle and managed Git handoff. Isolated fixture tests were
permitted; no live project, native session or Git change was performed by reviewer.

Four concrete findings were returned and corrected:

1. Cancellation/EOF could queue during publication without preventing successful
   source release. A shared stop event is now checked before dispatch, publication,
   release and destination preparation, including inside the commit verifier.
2. Committed state was trusted until destination pickup. The actual committed
   checkpoint and protected agreement are now compared before pushing; evidence
   paths must exist in that commit. Working-tree-only verification is insufficient.
3. Cancellation during preparation could still return success. It is checked again
   after preparation and before the successful handoff response.
4. A failed held save recorded `blocked`, which ordinary Roll could dispatch from
   after owner loss. It now records `uncertain`, requiring inspected recovery.

Final independent recheck: no remaining supported blockers in this bounded scope.
The reviewer's previous cancellation reproduction now raises instead of returning
success. This is lifecycle assessment, not an assertion that the artifact or the
whole Switch product is accepted.
