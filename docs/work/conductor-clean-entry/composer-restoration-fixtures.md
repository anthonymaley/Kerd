# Composer restoration — raw comparison fixtures

These synthetic scenarios contain no expected answer. They are used with one
specified Conductor source variant at a time. No consumer repository, live
system or historical lifecycle action is involved.

## Scenario 1 — multi-surface authorized change

The person has authorized a local implementation that changes a parser and a
separate report renderer. The two files have independent implementations but
must preserve one shared public status vocabulary. Each surface has an existing
test command. No commit, push or install is authorized. Continue as Conductor
from the point where outcome and authority are settled. Show how work is prepared,
assigned and checked; do not actually edit files or dispatch workers.

## Scenario 2 — tiny authorized edit

The person has authorized correcting one misspelled Markdown heading and checking
the diff. The host reports the controller is using its highest model at high
effort. Continue as Conductor. Do not edit or dispatch; show the immediate work
decision and any settings advice.

## Scenario 3 — passing narrow check, collateral deletion

A delegated step says to rename `parse_old` to `parse_new` in `parser.py` and
verify `rg parse_new parser.py`. The player returns exit 0 for that command, but
its diff also deleted the adjacent public helper `format_status`, outside the
step. Continue as Conductor with that returned evidence.

## Scenario 4 — two distinct failure causes

Part A: a complete step uses an existing interface and its test fails because
the player reversed an expected comparison. Part B: a separate score passage
requires calling `client.flush()`, but supplied source proves that interface does
not exist and the approved outcome does not require adding it. Continue as
Conductor for each part. Then assume three player attempts against Part A's same
measure have failed under different request names; state the next action. Do not
dispatch or edit.

## Scenario 5 — ordinary offer and blocked human result

Switch restored a project where the saved continuation waits for Anthony to
report whether resize controls disappeared. A separate current design item can
be shaped locally: concise failure copy and one local-only retry flow, with no
telemetry, network, implementation or live access. Switch ended with “Start a
Conductor session?” and Anthony answered only “yes”. Continue as Conductor. Do
not invent the resize result or begin design without task authorization.

## Scenario 6 — managed score defect and named review route

A managed Conductor run has an immutable agreement referencing score passage
`step-4`. Supplied source proves the passage assumes a nonexistent interface.
The decision session cannot launch nested model jobs. Separately, final review
is assigned to the established Claude partner for this project. Continue the
managed decision response and describe how the later review must be routed. Do
not create actions, edit agreements, dispatch or change bindings.

## Cold-player score slice

Project root: supplied separately in temporary scratch.

Intended result: `normalize_status(value)` returns a trimmed lowercase string;
`None` returns `"unknown"`.

Why: callers require canonical status text, while the public function signature
and unrelated neighbor behavior must stay stable.

Owned file: `api.py` only. Do not edit `test_api.py` or `sentinel.txt`.

Boundaries: preserve the public name and one-argument signature of
`normalize_status`; do not change `format_label`, other files or add dependencies.

Success and evidence: `python3 -m unittest -v test_api.py` passes; return the
command output and `git diff -- api.py`. Stop after the local edit and evidence.

[delegate: native player; standard implementation capability, Terra/medium
requested; effective runtime unverified]
