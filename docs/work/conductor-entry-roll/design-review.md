# Entry and Roll: review brief

Established Claude partner; keep native model, effort and permissions. Use the
existing Opus 5 scope-boundary guidance; effort unverified. Read-only review,
no edits, installs, consumer probes, lifecycle actions or new model jobs.

<objective>
Anthony approved “make the conductor ask in normal path first then add rolling
switch”. He requires automatic low-context session continuation without user
input. Codex implements and owns this tree; no release has been requested.
</objective>

<sources>
docs/work/conductor-entry-roll/work.md holds the agreement and measured baseline.
Read current skills/conductor/SKILL.md, references/execution.md; Switch SKILL.md,
references/in-out.md entry section, references/to-roll.md and scripts/roll.py.
Inspect codex_roll.py only where needed to assess its existing context route.
</sources>

<contribution>
Review two boundaries while Codex edits ordinary entry: (1) keep Conductor's
arrival composition, but explicitly ask “Start/Resume Conductor on X?” for
agent-owned work; on affirmative action approval invoke the skill again for
execution with the actual scope and authority, skip intake. Human checks/facts
stay their own questions. (2) make rolling Out/checkpoint and rolling In/resume
explicit within the existing managed Roll route, never normal In's approval.
Identify any concrete missing mechanics, especially contributor capture,
outer-controller exhaustion versus worker exhaustion, and Claude support.
Recommend the smallest honest implementation boundary. Do not call documentation
a whole-session rollover implementation. Return consequential findings with
source locations and any current native evidence you already hold; no new live
probes required. Codex will retrieve this reply and ask you to review the diff.
</contribution>
