# Failed save recovery — local managed-source pass

2026-09-07. The source stayed alive after a deliberately failed push. The same
process and loaded idle thread were inspected again; destination preparation was
refused. The controller repaired only the injected local push URL, retried the
same checkpoint, verified the remote, released the source with confirmed cleanup,
then started a distinct fresh destination that finished the work.

| Observed event (UTC) | Result |
|---|---|
| 15:57:41.432 | Source begins the agreed label improvement |
| 15:58:37.479 | Source held open; same loaded idle thread |
| 15:58:37.671 | Local push fails; source remains alive and idle |
| 15:58:37.672 | Destination preparation refuses; no destination worker |
| 15:58:37.701 | Same process/thread confirmed before retry |
| 15:58:37.947 | Remote save verified and source cleanup confirmed |
| 15:58:38.209 | Fresh destination starts from exact saved revision |
| 16:00:44.244 | Destination returns ready for independent review |

Both workers used gpt-5.6-sol/high. Saved commit:
`446654a647a8346bcfcbbeed0077fe860beee889`. Retry created no new work commit or source
model turn. Historical M3 failure count survived; protected inputs and saved-place
bytes remained unchanged. Roughly three minutes includes actual implementation,
tests and documentation, not pure transition overhead.

The disposable project is `/tmp/kerd-held-save.F1SdHU`; two clones and a local bare
remote. GitHub, devices, installed Kerd and live Seinn were not touched. No routine
user go-ahead was needed between source, recovery and destination.

## Proof and assessment

- [Observed events](events.json), [source result](source-result.json),
  [destination result](destination-result.json); native IDs remain private.
- Exact [source prompt](source-prompt.json) and [destination prompt](destination-prompt.json).
- [Method](method.md), [agreement](agreement.md), [runnable trial](run.py).
- [Output](output/USAGE.md): 12 model-produced artifact tests passed; 13 pass after
  the controller added the independent review's small surrogate-label regression.
- Candidate Switch regression suite: 163 tests pass. Existing 145 tests stayed
  green before adding the 18 new cases. The isolated candidate mirror also passes
  163 tests; both skill structure validations pass. Installed skills are unchanged.
- [Independent lifecycle review](review-lifecycle.md): two reproduced issues
  corrected and rechecked. [Claude artifact assessment](review-artifact.md) found
  no blockers; its small test/documentation gap was corrected and retested.
- [Attempt 1](attempt-1.md) failed on invalid reply JSON before the push-failure
  proof; its explicit teardown is not counted as successful recovery.

## What this does not prove

Only the deliberately failed push was exercised with real native sessions. Other
save and lifecycle failures have isolated regression evidence, not equivalent live
proof. The caller must keep the synchronous controller alive; host/controller
crash survival, automatic restart after its death, and arbitrary interactive-host
takeover are not implemented. Semantic uncertainty remains held for reassessment,
not automatic retry. A real device handoff and whole-pickup context cost remain
open. Review-ready work is not producer acceptance or installation.

The escaping improvement is retained as trial output, not silently adopted as a
new installed product feature. The reusable lifecycle implementation is in the
candidate Switch adapter and managed To helper, not in a one-off event observer.
The [updated process view](../direction.html) includes the failure/recovery path;
desktop and narrow static renders were visually inspected without clipping.
