<objective>
Review the new local /kerd:agent implementation against Anthony's request for
native queued Claude/Codex collaboration, session discovery, bounded workers
and persistent contextual partners, without inbox infrastructure.
</objective>
<sources>
Read skills/agent/SKILL.md, references/native-sessions.md, scripts/agent.py and
scripts/tests/test_agent.py beneath that skill. The direction and observed
limits are in docs/work/agent-connection/work.md. You already have Kerd context;
do not re-run Switch In or re-read the full memory set.
</sources>
<scope>
This is a peer's review request, not permission to change your current work.
Do not edit, stage, commit, push, install, change settings, stop sessions or
launch another model. Leave the concurrent 0.108.0 work untouched. You may run
the agent unit tests (they write only disposable test fixtures) if useful.
Do not run live model probes or send more session messages.
</scope>
<contribution>
Find concrete failures in identity/project matching, queue-versus-reply claims,
retrieval completeness, private state, lifecycle and authorization. In particular,
check new-versus-existing session behavior and whether the command descriptions
promise more than the implementation proves. Return up to six substantive
findings with file/line and a reproduction or counterexample. Distinguish
observed defects from risks; recommend the smallest correction, not a new
protocol framework. No approval verdict on Anthony's behalf.
</contribution>

Prompt preparation: shared Claude and Opus 5 profiles, 2026-09, informed the
separated scope/source sections and explicit reporting-only boundary. This is
the existing Kerd Claude session, not a freshly substituted reviewer. Its model
and effort settings are retained; no effort override is requested.
