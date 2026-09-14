# Focused re-review: composer restoration corrections

<objective>
Recheck only the five findings from Agent request e0191009 after correction.
Return remaining consequential defects or a release-readiness verdict. Read-only.
</objective>

<corrections>
1. The GPT-6 Astra/high Composer repaired the defective score passage first.
   Step 2 now requires controller inspection of every returned Player edit's
   actual diff against owned boundaries; bulk deletions, renames and pattern edits
   always receive the full diff; every defect names how it was caught.
2. The original Sol/medium Step 2 owner implemented that repaired passage in
   execution.md under “Review every returned edit before accepting it”.
3. The original Terra/medium Step 1 owner qualified inline briefing cost: a
   finished score step's transport supplement is not itself a keep reason.
4. orchestration.md now says a complete score step plus identified transport
   supplement is the saved brief; a separate brief is prepared only without a
   score step.
5. composer-restoration-comparison.md now adds independent collateral and evidence-
   honesty rows; says the mechanisms are hypothesized to explain the old behavior;
   labels the controller's assessment; marks scenarios 5–6 non-like-for-like; and
   names the historical spec/tag/sizing plan gate as deliberately not restored.
</corrections>

<sources>
Read the changed passages in composer-restoration-spec.md, orchestration.md,
execution.md and composer-restoration-comparison.md plus your prior reply retained
by Agent. Read adjacent text only to check consistency. The exact hand-back and
player correction prompts are in composer-restoration-corrections.md and
composer-restoration-correction-player.md.
</sources>

<evidence>
Owners ran their scoped diff checks and inspected their hunks. Root updated the
comparison and will rerun affected/full checks after review. No installed behavior
or efficiency claim was added. The first review's tests remain separate evidence.
</evidence>

<boundaries>
No edits, consumer/transcript access, dispatch, commit, push, install, settings,
binding, lifecycle or live probe. Do not reopen settled style. Identify any
remaining finding with path:line and minimal correction; otherwise state ready
for the one authorized release. Reply once through Agent.
</boundaries>
