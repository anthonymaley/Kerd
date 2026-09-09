# Agreed integration trial: a readable Roll status command

Conductor selected this bounded deliverable within the user's approved Roll
integration trial. It is useful candidate work, not a new Seinn product feature.
The user authorized building and independently reviewing a real task on the
Studio, in isolation, without routine next/permission prompts. No resource cap
was requested. No publishing, installations, account changes or live-project edits.

## Outcome

Build a small Python-standard-library command that tells a person where a managed
Roll is, what happened last and what happens next. Existing helper output is raw
JSON; people need a readable, truthful status without exposing native session IDs.
Deliver roll_status.py, test_roll_status.py and USAGE.md in this project root.
Choose the implementation method and work sequence. No preset number of pieces.

## Success and evidence

- M1: `python3 roll_status.py --project REPO` is strictly read-only. Resolve the
  actual Git root and its private directory through Git so ordinary clones and
  worktrees work. Never fetch, checkout, merge, stage, run project scripts or write
  a fallback record. Tests must cover clone-style .git and worktree-style .git file.
- M2: read .git/roll/run.json through that resolved Git directory. Show friendly
  current status and exact next action for running, paused, continue, review,
  blocked, uncertain and failed. Review means awaiting independent assessment,
  not accepted. Unknown/missing/invalid records get a concise explanation and
  nonzero exit; never infer completion from file count or a successful command.
- M3: when history exists, show completed worker count, last returned status and
  whether context-triggered Roll was observed. Runtime ledger history entries
  contain status, context_trigger (null or object) and context_readings (optional
  list). Do not print raw history, native session_id/request_id or arbitrary
  private error content. last status is not proof of quality. Optional fields may
  be absent for older records; label unknown rather than inventing values.
- M4: safe terminal output: validate expected JSON types; suppress ANSI/control
  characters from displayed saved text; do not emit tracebacks on malformed input
  or read/Git errors. Normal output should be a small readable text panel, not
  an engineer-facing JSON dump. Exit 0 only for a valid readable known state;
  that exit means the status was read, not the work passed.
- M5: tests run with `python3 -m unittest -v test_roll_status.py` using temporary
  repos/fixtures only. Include negative cases, data untouched checks, no native-ID
  leakage and honest review/unknown states. USAGE explains invocation and limits.
  Every claim about tests needs an actual execution; a different model reviews
  these deliverables against this original agreement before handoff to the user.

## Runtime facts supplied by Conductor

The live helper's private ledger has status, next_action, history, agreement,
place, target, requested_model and requested_effort. Each history item may have
session_id, request_id, status, usage, model, prompt_bytes, estimated_cost_usd,
context_readings, context_trigger and route. Don't read this trial's actual
.git/roll or .git/cross-llm files to reconstruct your predecessor's conversation.
Use synthetic fixture values for these private fields in tests.

## Authority and continuity

Edit only the three deliverable files above. You may run local Python/Git tests
and use temporary test directories. No network, extra agents, background jobs,
commits, pushes, dependency install, arbitrary repo/archive reading or live work.
The caller owns agreement.md and place.json; do not edit either. They are passed
as context. Preserve all accumulated evidence and real failed-correction counts.
If the controller requests Roll, finish a safe local operation and return the
saved place without inventing completion. Otherwise work toward the whole outcome.
The controller, not this worker, arranges independent review after status review.
