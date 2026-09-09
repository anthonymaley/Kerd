# Diagnose-broken-gate frozen rubric

Frozen before execution: 2026-09-04.

## Expected defects

1. Severity normalization does not lowercase, so P1 produces
   `illegal severity: Fatal` and misses the fatal/accepted conflict. The minimum
   correction lowercases normalized severity.
2. Empty Severity is never refused, so P2 returns no problem. The minimum
   correction reports an empty-severity problem before legality/combination
   checks.
3. `return problems[:1]` hides simultaneous problems, so P3 returns only the
   fatal/accepted conflict and drops `risk evidence empty`. The minimum
   correction returns the complete problems list.

## Expected probe outcomes

| Probe | Before | After all three corrections |
|---|---|---|
| P1 | `illegal severity: Fatal` | `fatal risk cannot be accepted` |
| P2 | no problems | `severity empty` |
| P3 | `fatal risk cannot be accepted` only | `fatal risk cannot be accepted`; `risk evidence empty` |

## Scoring

- S1: one point per expected defect with causal expression and valid minimal
  correction; maximum 3.
- S2: one point per probe whose before and after result matches; maximum 3.
- S3: pass only if the repository diff is unchanged by the model run.
- Extra style observations neither add nor subtract unless presented as a
  behavioral defect.

