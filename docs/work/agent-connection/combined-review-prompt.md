<scope_update>
Anthony corrected the release split: "no, lets do it all together or hold off
until we are ready?" We will hold publishing until the combined work is ready,
then publish one v0.108.0 release. This supersedes my previous Agent-only
v0.109.0 proposal. Nothing has been committed or pushed.
</scope_update>
<review>
Please extend your pending review to the complete intended release: Agent skill
and help, Switch In's status-only behavior and Conductor orientation, dashboard
input/example and tests, and the related README/manifests/trial evidence.
Inspect git diff and new skills/agent/ plus the new trial records named in git
status under docs/work/model-ready-work/trials/. The root patch and preserved
bytecode are excluded. Check integration rather than repeating already-completed
review work. In particular, a direct "ask Claude" must reach the existing
partner route rather than Conductor's older fresh-worker-only path; ordinary
Switch In must not execute work, while later approval continues under Conductor.
Report actionable release blockers and disclosed limits separately. Do not
award producer acceptance for user-visible experience or token savings.
</review>
<authority>
Still read-only: no edits, stage, commits, push, installations, settings changes,
stopping sessions or other model jobs. Relevant local fixture tests are allowed.
I will handle integration changes and all publishing. Please leave shared release
files untouched while I work. No new protocol design; smallest supported fixes.
</authority>

Same existing Claude partner and retained model/effort. Shared Claude/Opus 5
profiles (2026-09) used for the separated scope and source material.
