Continue this agreed build from the saved place below. This is a fresh
context, not a new assignment. Continue useful work toward the agreed outcome. Choose the method.
The controller observes context usage and may ask you to Roll. On that
request, finish the current safe operation and return your saved place.
You may also return early at a genuine blocker or a useful safe boundary.
Do not manufacture pieces or extra work to force a transition. Do not replay completed work.
Use only the project files needed for that action; do not inspect native session
history, .git/cross-llm logs, or unrelated archives to reconstruct a transcript.
Do not modify the agreement or saved-place file; the caller saves your response.
Do not launch background processes, other agents, network calls, commits or pushes.
Preserve outstanding decisions, failure counts, constraints and cumulative evidence.
The agreement remains authoritative, including its limits and stopping condition.
Return ONLY a JSON object with these fields:
status: 'continue' for another useful piece, 'review' when ready for independent
assessment (not an assertion of acceptance), or 'blocked' for a genuine blocker;
next_action: the exact next action or review/blocker needed;
memory: concise useful working context, decisions and findings for the next run;
evidence: cumulative relative paths to actual result/evidence files;
failures: cumulative failed-correction counts by measure (preserve existing keys);
pending_jobs: [] only if no jobs remain. Any unresolved job means blocked.
Do not invent test results. Tools unavailable to this run are an explicit limit,
not a reason to declare an unchecked result verified.

# Agreed work
# Add a report-friendly pickup summary

This is isolated Switch trial work, not Seinn product work. Continue the existing
pickup preview with `--format markdown`, so its safe metadata can be included in
a work report without copying source bodies. Text and JSON remain unchanged.

Work only in `docs/work/switch-trial/device-build/`. Deliver the updated
pickup_preview.py, test_pickup_preview.py and USAGE.md there. Use a readable
Markdown heading, recorded branch/revision/state and a source table with file,
selection and UTF-8 byte counts. Show that prepared is not restored or accepted.
Labels containing Markdown pipes, backticks, HTML or newlines must remain data,
not create extra rows, markup or executable HTML. Choose a safe representation
and document it. No source contents, note prose, private IDs or extra fields.

Measures declared before the build:
- M1: all existing text/JSON tests keep passing and their behaviour is unchanged.
- M2: Markdown presents the required metadata and correct Unicode byte counts;
  tests prove labels with pipes, backticks, HTML and newlines cannot escape cells.
- M3: private bodies/unknown fields remain absent; invalid input exits 2 with
  no successful stdout, including the Markdown CLI route.
- M4: tests and usage demonstrate Markdown, existing formats and clear limits.

Authority: edit only the three deliverables above. Local Python tests for this
folder are authorized; no dependencies, network or background jobs. No Seinn
build, readiness check, device probe, production operation, installed Kerd skill,
product source edit, account change or message to others. Do not modify root
CONTEXT.md/TODO.md, history, agreement.md, place.json, example.json or pickup.md.
The Studio controller alone may commit/push this trial folder to the designated
kerd-switch-trial-20260906 branch. The laptop finishes locally and reports; it
does not commit/push, deploy or end somebody's interactive session.

On a controller checkpoint request, finish the current safe operation and return
the real unfinished place, including failures and the next action. The laptop
continues from it without another interview. Complete means ready for independent
assessment with evidence, not self-approved. No time/spending cap was set; use
existing tools. M3=1 is retained seeded history, not a new failed attempt. Three
failed corrections of a measure require reassessment. No unresolved background jobs.

# Saved place
{
  "status": "continue",
  "next_action": "Add the safe Markdown report format, tests and usage under the agreement",
  "memory": "Text and JSON preview already have 19 passing tests. Add Markdown without changing their behaviour. This is isolated trial work, not a Seinn task.",
  "evidence": [
    "docs/work/switch-trial/device-build/pickup_preview.py",
    "docs/work/switch-trial/device-build/test_pickup_preview.py",
    "docs/work/switch-trial/device-build/USAGE.md"
  ],
  "failures": {
    "M3": 1
  },
  "pending_jobs": []
}
