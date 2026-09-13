# Grid presentation review request

Profile: existing Claude partner; Opus 5 2026-09 local guidance (scope-boundary,
clear outcome and evidence). Keep native model and permissions unchanged; no
effort override, applied effort unknown. Reviewer edits nothing.

<objective>
Anthony approved both presentation changes: the live Conductor delegation grid
and Switch In using the same grid style for orientation, followed by three
bullets LAST SESSION / THIS SESSION / NOW. His final instruction: “lets do both
changes”. Implementation only; no release, installation or consumer-project work.
</objective>

<agreement>
Switch: PROJECT / PHASE / STATE / TEAM grid, no arrival boxes; nested numbered
known-owner actions under NOW; detailed checks and later/event-dependent work
behind links; immediate limits visible; explicit completion and END retained;
one bold speech-bubble question immediately after END. No new pickup work.
Conductor: task / route / model requested / effort / status grid; real updates
for applicable guidance, actual prompts saved, dispatch and checked results.
Never invent effort or counts, label native subagents as `kerd:agent`, or confuse
queued with running. No fixed staffing quota or prompt template requirement.
</agreement>

<sources>
Read the current diff: skills/switch/scripts/where_we_are.py and its tests,
skills/switch/{SKILL.md,references/in-out.md},
skills/conductor/{SKILL.md,references/journey.md,references/execution.md},
skills/agent/references/session-succession.md and README.md current usage.
The earlier uncommitted NOW tightening is included, authorized separately.
The work record may be updated by Codex during review; source edits paused.
</sources>

<contribution>
Review consequential behavior/guidance contradictions. Run the focused renderer
tests and try the documented JSON in Markdown and plain terminal. Check real
table cells cannot be injected by pipes/newlines/backticks, three nested sections,
full scope retention, no-question/partial-restoration, unchanged Out. The grid
does not carry TASK: old task values absent from NOW/THIS are preserved as Focus
under NOW; task_reason always survives. New guide uses null task and names it in
NOW. Terminal is the existing labelled fallback, not the chat grid.
For delegation, verify the described transitions stay tied to actual work and
the distinction between requested/observed settings and native versus Kerd
routes. Report numbered findings with evidence and minimal changes, or ready for
local implementation. This is not an experience acceptance or publication review.
</contribution>

<boundaries>
Read-only shared tree. Temporary scratch fixtures allowed. No edits, commits,
pushes, installs, bindings, session changes, model dispatch or consumer access.
No shared verification-record update. Return once through Agent's markers.
</boundaries>
