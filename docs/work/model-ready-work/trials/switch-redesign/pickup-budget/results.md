# A smaller pickup must still remember the work

Local Seinn trial, 2026-09-07: **the corrected prepared reader passed this scoped
check**. It fits both numerical targets, and independent Claude assessment found
no blocking restoration issue. This does not mean all of Switch is finished.

## What we tried

All runs used fresh Codex gpt-5.6-sol sessions, high effort, the same pinned Seinn
snapshot, full candidate instructions and read-only authority. Success required
both small context use and correct restoration. Prior failures remain visible.

| Approach | Added input estimate | Added context | Reader time | Finding |
|---|---:|---:|---:|---|
| Reader discovers the sources | 17,097 | 7.59% | 171 s | Missed both limits |
| More selective-reading instructions | 20,424 | 8.86% | 185 s | Still missed; read more history |
| Complete current records supplied | 4,761 | 2.24% | 41 s | Small enough, but omitted decisions and a prohibition |
| Helper gathers records; reader checks retained meaning | 5,151 | 2.66% | 65 s | Small enough; still omitted scoped restrictions |
| Same records; preserve restrictions with their scope | 5,249 | 3.38% | 119 s | Both numerical limits met; independent restoration review passed |

Targets: no more than 8,000 additional input tokens and 5% added context.
The last row used zero additional tools. All bracketing controls reported the same
13,026 input tokens. Its peak input was 18,275; peak total was 21,769, against an
observed window of 258,400. Added total context is conservatively estimated at
8,743 tokens, including the answer. These are matched-run differences, not exact
attribution. The short control instruction itself is subtracted too; its small
bias is not separately quantified. See [method](method.md) and
[latest readings](preserved-observation.json), [post-control](preserved-post-control.json).

## What changes in the product

Conductor chooses the relevant existing records. A small optional helper gathers
their complete contents and source labels. The fresh reader uses them directly,
then checks that open decisions, owed work and prohibitions survived. Supporting
history stays available when something genuinely needs resolving.

The helper is not an intelligent memory selector. It neither summarizes nor
writes another context file. It does not start sessions, grant permissions, or
require CI or hooks. Its 32 Git/handoff tests and the full 145-test Switch suite
pass; skill validation passes. These are controller-executed checks, not a peer's
claim to have run tests. Skill Creator influenced the implementation by keeping
this reusable assembly in the existing script and mode-specific guidance in the
In/Out reference, rather than adding universal instructions or a new subsystem.

## Proof and limits

- [First independent review and disposition](review-first.md): numerical success
  alone was rejected because useful memory was missing.
- [Second restoration review](review-assembled.md) kept the scope-loss failure
  visible instead of accepting a numerical pass.
- [Final independent assessment](review-final.md): no blocking findings. The
  full linked TV-decision entry is still needed before acting on that decision;
  the report-only trial did not require it. Both controls were checked by the
  controller; the peer explicitly limits its own pre-control verification.
- [Actual revised prompt](submitted-pickup-preserved.md) and
  [helper output](prepared-packet.json): full CONTEXT and the complete TODO Now
  section, including Owed children. No expected answers were inserted.
- [Earlier observations](observations.json), [earlier metrics](metrics.json) and
  [assembled metrics](assembled-metrics.json) and [latest metrics](preserved-metrics.json)
  retain all tested variants.
- [Helper review](review-helper.md) and [recheck](review-helper-recheck.md): text
  handling, tracked sources and changed-state checks were corrected and tested.

This measures one fresh reader consuming caller-prepared current records, not the
controller's source-selection effort, an end-to-end GitHub pickup, an active build
handoff, or every project/model. It is not a matched comparison with old Switch.
No complete archive-preservation claim is made. General discovery still missed
the target here; a different or larger necessary working set needs its own check.

The isolated Seinn checkout remained clean at 2302c2a. No live Seinn changes,
installation, commit, push, operational probes or source-session exit occurred.
Candidate Switch files match the isolated candidate mirror; all 145 tests pass
there too. No live skill was changed. The actual prompt snapshots are retained:
the tested final behavior is in submitted-pickup-preserved.md, not reconstructed
from a later version of the instructions.

The [connected diagram](../direction.html) now shows the prepared-pickup flow and
this result. Full desktop (1280×2600) and narrow (700×5700) renders were visually
inspected without observed clipping or label collisions. No interactive device
test is implied. Temporary headless browser processes were stopped afterward.
