# Live connection: local handoff proved

Conductor sent To through the actual running Roll command, recovered an injected
save failure through the same channel, and continued the work in a fresh destination
without another user turn. No observer called the internal handoff class in place
of the product route. This closes the local live-controller connection gap, not
the entire Switch redesign.

[Updated process view](../direction.html) · [Method and scope](method.md) ·
[Observed results](observed.json) · [Original agreement](agreement.md)

## What happened

| Observed point · 2026-09-07 UTC | Result |
|---|---|
| 17:13:01 · source started | gpt-5.6-sol/high; actual Roll CLI with open control channel |
| During work · To received | Same active turn accepted a safe-checkpoint request |
| 17:15:24 · source held | Unfinished patch attempt recorded honestly; no code change claimed |
| 17:15:25 · injected push failed | Same owner retained its source; destination remained at initial revision |
| 17:16:16 · retry completed | Only local push address repaired; remote verified, owned source and children exited |
| 17:16:28 · fresh destination started | Exact saved revision and unchanged agreement; no user “next” |
| 17:20:14 · work reached review | New JSON preview, tests and usage delivered; no pending jobs |

Saved handoff revision: `d2c2e019223d9d82c5bb789f7f708da7f8b0f56e`.
One source worker and one different destination worker. Seeded M3=1 history
survived. Native identifiers remain private; the collector verifies their
distinctness and owned-process cleanup without publishing them.

The source's combined patch failed on a USAGE context mismatch and applied no
changes. Its analysis and exact next action were what moved. This is a useful
unfinished-work transfer, not a claim of transferring partially edited code.
The earlier [failed-save trial](../failed-save/results.md) covers that case.

## The actual prompts and deliverable

- [Source prompt](source-1-prompt.md): outcome, proof and boundaries, native high effort.
- [Fresh destination prompt](destination-1-prompt.md): same agreement plus the actual checkpoint.
- [Claude review request](review-request.md), [returned assessment](review-artifact.md),
  and [narrow evidence follow-up request](review-followup-request.md).
- [Preview implementation](output/pickup_preview.py), [tests](output/test_pickup_preview.py),
  [usage](output/USAGE.md), [example](output/example.json).

The feature adds `--format json` to the existing text preview. It returns only
validated metadata, keeps original labels through JSON decoding, counts UTF-8
source bytes and never emits source bodies or extra fields. Text remains default.
No library was installed and the feature remains a trial artifact.

## Assessment and follow-up

Claude Opus 5/high independently found no blocking defect against M1–M4. It did
not execute tests. Its returned assessment remains unchanged, including its
unverified cross-parser speculation; that speculation is not a product fact.

The controller then closed supported test/doc gaps without changing product code:

- **M1:** the unchanged earlier 13-test suite passes against the new module AND
  CLI using [the transparent loader](check_legacy.py). The current suite also passes.
- **M2:** tests cover byte counts and original branch, revision, file and selection
  labels. Documentation makes the Python-only parser trial explicit. Lone-surrogate
  labels remain preserved, not normalized; universal parser compatibility is unassessed.
- **M3:** malformed-packet cases now exercise both renderers; syntax errors and
  missing files exercise both CLI formats, with no successful stdout payload.
- **M4:** explicit text, default text, JSON and invalid-format routes pass. Usage
  now distinguishes the tested Python 3.14 runtime from its untested 3.10 floor,
  and explains that metadata alone proves neither acceptance nor execution authority.

19 current artifact tests pass after these follow-ups; the test count is unchanged
because existing methods gained additional cases. The new implementation was not
modified after independent review. Additional test/doc edits were made by the
controller, not attributed to the destination worker.
Claude's [follow-up assessment](review-followup.md) closed E1/M1: the original
assertions were retained or strengthened, the unchanged-test loader targets the
new library and CLI, and no contradiction was found. It distinguishes its static
assessment from tests actually executed by the controller.

[Independent lifecycle review](review-lifecycle.md) identified four concrete
controller issues, all corrected and independently rechecked. The final scoped
review found no remaining supported blocker. 186 Switch regressions pass in both
the pack and isolated candidate; the Conductor transport's 34 tests also pass.
Both skill validations pass in both locations. No CI was required to use this.

The raw handoff receipt in observed.json retains its original generic Git note
alongside `source_session_exited: true`. The controller's separate release proof
establishes the actual exit. After the run, the receipt's display note was clarified
in ManagedTo; this wording correction does not rewrite the captured observation.

## What this does not prove

No automatic remote launch, Studio-to-laptop active-build transfer, takeover of an
already-open user session, crash survival, universal compaction prevention, full
pickup-cost measurement or optimal speed/model/effort comparison. The live caller
must keep its existing channel open. A cancellation during synchronization can
leave updated destination files but cannot be treated as permission to execute.

The process diagram was rendered and inspected at desktop and narrow widths;
its sequences reflow without observed clipping. Only the isolated candidate
mirror was synchronized. Installed Kerd, live Seinn, root TODO changes, GitHub,
global configuration and the person's current session were untouched.

Next proof boundary: a real active-build device handoff needs the actual destination
available and its explicit project/session entry. Do not substitute another
read-only laptop pickup or pretend a local clone exercised remote session startup.
