<objective>
Anthony asks: "okay ask claude to review and when finalized make a new release?"
Review the Agent command and its latest help/session-selection behavior for
release. You are the established Kerd partner; retain your context. No Switch In.
</objective>
<agreement>
Short requests use the established partner for this project/provider by default.
When no partner is established or the target is ambiguous, show matching native
sessions so the person can choose; make the choice visible with useful metadata.
Explicit fresh/new requests select a new session. Never silently substitute for
an unavailable partner. Help must not start work. Keep the experience light.
</agreement>
<sources>
Read skills/agent/SKILL.md, references/user-guide.md, references/native-sessions.md,
scripts/agent.py and scripts/tests/test_agent.py under that skill. Your earlier
review and fixes are summarized in docs/work/agent-connection/work.md.
Check compatibility with committed HEAD's conductor/scripts/ask.py because this
release will exclude concurrent uncommitted Switch/Conductor changes.
</sources>
<scope>
Read-only review, no edits, staging, commit, push, installation, settings changes,
session lifecycle changes or model dispatch. Agent unit tests in disposable
fixtures are allowed. Report concrete defects, not a fresh protocol design.
I am preparing an Agent-only v0.109.0 release, leaving your pending 0.108.0
Switch/Conductor changes and trial records local and intact. Shared README and
manifest edits will be staged selectively. Please do not edit those surfaces
or publish concurrently while this release is prepared. Tell me if there is a
dependency or other conflict with that split; do not expand release scope.
</scope>
<return>
Report actionable findings with file/line, severity and a reproduction or
counterexample. Check whether the prose promises more than code supports,
whether a new user can actually use the help, and regressions in previous fixes.
Separate release blockers from disclosed limitations. No producer acceptance
verdict. Stop after the review and return your findings in the request markers.
</return>

Prompt uses shared Claude and Opus 5 profiles (2026-09) for separated material
and scope. Existing session model/effort retained; no effort override requested.
