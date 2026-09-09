# Build a small handoff report tool

Outcome: turn a saved work record into a clear, read-only terminal handoff so a
person knows what is finished, what is blocked, and exactly what comes next.

Deliver handoff_report.py (Python standard library), test_handoff_report.py
(unittest), and USAGE.md. No dependencies, network, background work or Git changes.
You may edit only those three files. Do not edit agreement.md or place.json.

Input is a JSON object: project (nonempty string), stage (nonempty string),
next_action (nonempty string), tasks (list of objects with nonempty unique id,
nonempty title, status exactly done/active/blocked/queued). Preserve order within
groups. Output readable Markdown grouped Done, Active, Blocked, Queued, omitting
empty groups, followed by the explicit Next action. Never infer that work is
complete from a task count. Treat titles as plain single-line text; reject embedded
newlines in any string. Error messages go to stderr and exit 2; no traceback on
invalid input. Accept one CLI path argument; no writes to the input file.

Evidence: unittest coverage of all four groups, no empty headings, valid empty
tasks, duplicate IDs, invalid statuses, missing/blank strings, wrong data types,
embedded newlines, malformed JSON and CLI failure exit. Tests must be executable
with python3 -m unittest -v. Expose render_report(data) for tests. Documentation
includes a clearly fictional sample and realistic limitations, no fake claims.

This is a controlled Roll proof using real deliverables. Work in THREE bounded
pieces, saving after each: first implement the report tool; next add the tests;
finally inspect both, correct any supported issues, and write usage instructions.
Return continue after the first two pieces and review after the third. Do not
complete later pieces early: fresh-run continuity is part of this experiment.
If your tools cannot execute tests, report tests as not run; the controller will
execute them. Keep failures counter continuity-check: 1 unchanged unless an
additional failure of that measure actually occurs. This seeded count is part
of the fixture, not a failure attributed to this build.

Success requires independent assessment after the files are ready. Do not label
the work accepted. Retain meaningful evidence and exact next action across rolls.
