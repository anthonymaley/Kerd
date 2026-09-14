# Conductor restoration compared with v0.105.0

## Evidence boundary

Historical source is `54c28cd:skills/conductor/SKILL.md`, the v0.105.0 four-role
contract. Current source is this uncommitted integrated candidate. Two fresh
Sol/medium interpreters received the same six raw scenarios in
[composer-restoration-fixtures.md](composer-restoration-fixtures.md), one source
variant each, without this comparison or its expected verdicts. These are
source-guided interpretations, not installed-version performance. Requested
settings are recorded; effective runtime settings were not independently observed.

Claude separately reported native dispatch counts: on 09-01/02 under the old
four-role design, composer calls and explicitly sized players were frequent; on
09-11..14 after the rewrite, composer calls, player count and explicit sizing
dropped sharply. Those counts motivated this work but were not independently
recounted by Codex and are not normalized for work volume or evidence of quality.

## Source contract

| Contract | v0.105.0 | Integrated candidate | Verdict |
| --- | --- | --- | --- |
| Four owners | Named producer/composer/conductor/players at historical lines 18–34 | Capability-based owners in `orchestration.md` “Compose a score…” | Restored; provider branding removed |
| Composer | Top-tier call, not a mode; two bounded passes at lines 226–249 | Two-pass bounded composer at `orchestration.md` lines 59–84 | Restored; fallback judged to same bar rather than presumed inferior |
| Cold-readable score | Spec body, then tag, exact terrain/why/verify at lines 217–224 | Complete step before assignment at `orchestration.md` lines 86–103 | Restored and broadened beyond code |
| Delegation bias | Mostly delegate with seam review at lines 220–223 | Bias for well-factored work; no ratio/quota; collateral review explicit | Adapted to retain judgment and permission checks |
| Model/effort | Fixed named ladder and session advice down/up at lines 101–114, 223 | Task-based capability mapping and supported effort, advice down/up | Restored without frozen provider tiers or mandatory confirmation |
| Worker brief | Spec slice sent to player at lines 263–266 | Complete score step reused; only missing transport facts added | Restored with less duplicate briefing |
| Controller collateral gate | Every task reads the actual diff; bulk/pattern changes always get this check at historical lines 268–282 | Every returned Player edit is checked against owned paths/hunks; bulk deletions, renames and pattern edits require the full diff at `execution.md` “Review every returned edit…” | Restored after Claude caught its omission from the first score |
| Evidence honesty | Verification and strong-language gates distinguish checked results and require naming how self-corrections were caught at historical lines 268–301 | Returned is not checked; settings evidence stays qualified; every caught defect, including Conductor's own, names its detection path | Restored and adapted to current evidence states |
| Failure ownership | Re-dispatch, never re-specify; three failures declared score wrong | Sound failure preserves semantics; known defect returns immediately; three attempts are a ceiling, not proof | Restored and corrected |
| Managed continuation | No current managed schema/routing in the historical source | Existing immutable agreement and `blocked` action retained; repair occurs after verified stop | Modern safeguard preserved |
| Named partner review | No persistent Agent binding route in historical source | Exact established partner through Agent; no silent fresh substitute | Modern safeguard preserved |
| Switch entry | Historical mode assumes older pickup/approval machinery | Generic offer opens direction-setting; task authority stays distinct | Current interactive-orientation agreement preserved |

Intentionally not restored: provider-brand defaults, command-only delegation
eligibility, a fixed number of `[keep]` steps, compulsory model confirmation,
legacy mode-marker/state writes, automatic closeout/commits, assumed composer
superiority, the historical plan gate where the producer approved the spec,
tags and sizing together before execution, or historical lifecycle actions.

## Same-scenario interpretation

| Scenario | v0.105.0 result | Integrated candidate result | Assessment |
| --- | --- | --- | --- |
| Two independent surfaces, shared seam | Two-pass composer; two delegated implementations; retained seam review | Same split, with explicit controller integration, route evidence and no action before score | Core behavior restored |
| Tiny spelling edit on highest/high | Inline; advised a historically named cheap pair and described an old settings gate | Inline; recommends a lower supported pair for comparable work without delaying or auto-changing this edit | Down-sizing retained, friction reduced |
| Narrow check passes, adjacent helper deleted | Rejects return at diff-review gate; re-dispatches same slice | Same; the source now mandates reading every returned edit's actual diff, and the fixture rejects the narrow pass | Restored after peer review exposed the first score's omission |
| Player error vs impossible score premise | Re-dispatches player error; returns impossible premise to composer; after three failures asserts score wrong | Same first two choices; after three, stops before fourth and reassesses without claiming cause | Restored with false inference removed |
| Generic offer, human check blocked, independent design available | Keeps direction on missing human report and asks for it | Keeps report unknown but proposes independent design with its own approval | Current orientation fix adds useful direction |
| Managed score defect and named Claude review | Correctly identifies score defect but has no managed handoff or partner route | Returns existing `blocked`, preserves passage/evidence, waits for verified stop; routes review to exact established Claude partner | Current safeguards fill historical gaps |

## Cold-player execution

A fresh Terra/medium player received only the completed `normalize_status` score
slice and the three-file scratch project at
`/private/tmp/kerd-cold-player.Dn4eUh`. It edited only `api.py`, returned its diff
and passed two tests. The controller independently reran both tests, inspected
the exact diff, and confirmed `test_api.py` and `sentinel.txt` had no tracked diff.
The public `format_label` neighbor was unchanged. This demonstrates one score
slice was playable cold; it does not prove general prompt efficiency, installed
Conductor behavior or composer quality.

## Present verdict

The candidate restores the v0.105.0 mechanisms hypothesized to explain bounded
composition, finished specs, predominantly delegated well-factored work,
per-contribution sizing and controller-held evidence judgment. It deliberately
keeps newer authority, model-evidence, Agent and managed-run safeguards. The
controller assessed the current interpretation as equal or stronger in the four
like-for-like cases. Scenarios 5–6 are not like-for-like: they exercise current
interactive-orientation, managed-run and Agent capabilities absent from the
historical source. In scenario 5, current Conductor can recommend independent
eligible work after the generic offer instead of treating a missing human report
as a project-wide hold.

This verdict is source and synthetic-execution evidence. It is not ordinary-use
acceptance or proof of lower tokens, cost or elapsed time.

## Future real-build observations

### Build 1 — not yet observed

Record actual installed revision, outcome/authority, composer scoping and terrain,
score/playability, assignments and requested/observed settings, returns, repairs,
review, human intervention and final evidence. Compare decisions with v0.105.0;
do not infer efficiency from counts alone.

### Build 2 — not yet observed

Use the same evidence shape. After both builds, mark each contract met, unmet or
unassessed and name any correction. These slots do not block the source release.
