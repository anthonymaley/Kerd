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
# Machine-readable pickup preview

Improve the existing privacy-conscious pickup preview so a caller can use its
summary without scraping terminal text. This is real candidate work, tested in
disposable repositories; it is not installed product functionality.

Deliver `pickup_preview.py`, tests, and updated `USAGE.md`. Add `--format json`
alongside the existing default text output. JSON must contain validated branch,
revision, clean/synchronized flags, selected-source file/selection/UTF-8 byte
counts, and total bytes. It must never include source contents or unknown fields.
Keep existing text output and invalid-input behaviour compatible. Choose clear
field names and document them. Do not embed terminal-escaped labels in JSON data:
JSON escaping must preserve the original string when parsed.

Success measures:
- M1: existing text behaviour and all existing tests remain passing.
- M2: JSON parses into the documented metadata, counts non-ASCII bytes correctly,
  and preserves original labels including controls/backslashes after JSON decoding.
- M3: source contents and extra input fields remain absent; malformed packets
  fail with exit 2 and no successful stdout payload in either format.
- M4: tests and usage prove the new CLI route, including default text, JSON,
  invalid input and invalid format. Report only checks actually run.

Authority: edit only pickup_preview.py, test_pickup_preview.py and USAGE.md.
Use the existing Python standard library and local tests. No network, packages,
other agents, live projects, Git commits or pushes by the worker. Do not change
agreement.md, example.json, .gitignore or place.json. The controller owns saves
and an already-authorized local-only handoff, not publication to GitHub.

Continue until the result is ready for independent assessment; no routine user
confirmation. On a controller checkpoint request finish the current safe operation
and return the precise unfinished place without inventing progress. Review is not
acceptance. No time or spending cap is set. Preserve the seeded M3=1 history;
three failed corrections require reassessment. Leave no background jobs.

# Saved place
{
  "status": "continue",
  "next_action": "Add and prove the machine-readable pickup preview",
  "memory": "Existing privacy-conscious text preview has 13 tests. M3=1 is seeded history, not a new failure.",
  "evidence": [
    "pickup_preview.py",
    "test_pickup_preview.py",
    "USAGE.md"
  ],
  "failures": {
    "M3": 1
  },
  "pending_jobs": []
}
