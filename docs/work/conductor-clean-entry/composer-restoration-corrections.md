# Composer restoration — review corrections

Claude review request `e0191009` returned one score defect and three implementation/
record corrections. The review was read-only and retrieved through Agent. Claude
ran Conductor tests, release gate and whitespace check; it did not inspect
consumer repositories or transcripts. Observed reviewer model: claude-opus-5;
effort retained/unverified.

## Composer hand-back — exact message

Same composer and requested GPT-6 Astra/high controls; no matching Astra profile,
so the original disclosed outcome-contract fallback remains.

```text
Claude's integrated review found one defect in your execution score. Repair only the affected passage in /Users/anthonymaley/development/product/Kerd/docs/work/conductor-clean-entry/composer-restoration-spec.md using apply_patch; edit no other file. Defect: v0.105.0's controller-side collateral gate was weakened into an optional composer-authored field/review. The score must require Conductor to inspect every returned Player edit's actual diff against the score step's owned boundaries, not only verification output; bulk deletions, renames and pattern-driven edits always receive that diff read. It must also state how any defect—including one caught by the controller in its own work—was caught. Preserve the existing independent/seam-review rule; this controller check is additional and cannot depend on the Composer anticipating a specific damage mode. Update the affected Step 2 implementation requirement and its verification trace, and Step 5 comparison criteria if needed, without changing other agreed semantics or release/future observation boundaries. Return the repaired passage summary and whether the change is consequential to already-implemented execution.md. No implementation, release, commit, push, install, consumer access, model dispatch or lifecycle action. This is the score hand-back required by the current contract; requested native controls remain GPT-6 Astra/high, effective runtime unverified.
```

Pending after score repair:

- Step 1 owner: qualify briefing cost so a finished score step's small transport
  supplement is not itself an inline reason; reconcile unconditional saved-brief
  wording with score-step reuse.
- Step 2 owner: implement the repaired mandatory controller collateral gate.
- Controller: add the missing collateral/evidence-honesty comparison rows, remove
  causal language, label assessment, mark scenarios 5–6 non-like-for-like, and
  name the old plan gate as deliberately not restored.

## Step 1 implementation correction — exact message

```text
Claude's integrated review found two implementation gaps in your owned orchestration.md. Correct only skills/conductor/references/orchestration.md using apply_patch, preserving every existing orientation and score-contract change. (1) The inline-reason list still says 'briefing cost' without qualification. A finished score step is already the brief, so its remaining transport supplement is not by itself a reason to keep it. Qualify briefing cost to cases where no complete score step exists, while retaining genuine coordination/context-transfer reasons. (2) The later unconditional 'Prepare the real prompt... Save a safe shareable brief' paragraph contradicts score reuse. Make it explicit that a reused complete score step plus its identified transport supplement is the saved brief; only when no score step applies is a separate brief prepared. Do not change the score's semantics, other files or release surfaces. Run the owned diff check and inspect the complete resulting hunk. No commit, push, release, install, consumer access, dispatch, settings/binding or lifecycle action. Requested controls remain Terra/medium; effective runtime unverified.
```
