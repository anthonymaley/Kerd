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
