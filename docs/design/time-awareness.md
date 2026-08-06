# Time-awareness — design

Slice 1 of `docs/product/time-awareness.md`: honest actuals, no
estimates. Canvas: `docs/design/time-awareness.excalidraw`
(generator: `tools/diagram/gen_time_awareness.py`).

## The mechanism

**The same-turn rule — one definition, in the state contract.** A
wall-clock time may be written into any artifact only when it came
from one of two sources read in the same turn: a `date` invocation, or
a machine-written record (a marker stamp, a git commit timestamp). A
time the model "remembers" or infers is never written. (Amended at
contract time, Tony's approval: the one-source form banned this
feature's own mechanism — the close-out ranges and per-task lines copy
git timestamps and marker stamps, neither of which comes from a
same-turn `date`. What the rule defends against is a fabricated time,
and both admitted sources are machine-produced.) The rule's single definition lives in
`docs/state-contract.md` (the cross-skill conventions file); switch
and conductor carry one-line pointers at their write moments, per the
single-definition law (v0.84.0 precedent). The machine layer checks
presence and format only — time *honesty* is the frame's declared
limit.

**The marker stamp — task start rides a write that already happens.**
Conductor's phase-marker writes become
`conductor: <phase> @ YYYY-MM-DD HH:MM TZ`. All four readers are
prefix-greps (`^conductor:`, `^mode:` in stop.sh, session-start.sh,
skill-complete.sh — swept, proven safe); stop.sh echoes the whole
line, so the stamp reaches the human for free. The `execute` marker's
stamp IS the task's start time.

**Task end is git's, already exact.** The work commit timestamp closes
the range; nothing new is written. At the boundary, the sitting
section records each conducted task as one line: `task — started
HH:MM (marker) · landed HH:MM (work commit)`. Sitting headings carry a
real `(HH:MM–HH:MM TZ)` range: open time from the session's earliest
marker stamp (omitted honestly if none), close time from `date` at the
boundary.

**The Clock line — new gate records only.** The gate-record schema
gains an optional `**Clock:** YYYY-MM-DD HH:MM TZ` line under the
title. Documented in `tools/gates/README.md`; deliberately NOT
validated (the accepted risk's review trigger holds the CI
graduation). Goal records first. No existing record is touched — a
backfilled time is manufactured history.

**hooks/statusline.sh — composes, never claims.** The statusline slot
on a machine may be occupied (this machine: scorched-earth's
burn-rate wrapper — the live example). The script prints `HH:MM`; with
an optional argument naming an existing statusline command it prints
`HH:MM · <that command's output>`, forwarding stdin (statusline
commands receive context JSON on stdin). Wiring is machine-local and
opt-in, documented beside the hooks with resolved absolute paths (the
hook-path gotcha): free slot → point `statusLine` at the script;
occupied slot → pass the current command as the argument. The model
never sees the statusline — the frame's accepted limit.

## Edit map

Design-time cross-cutting sweep run (`.active-modes` readers: 4 hook
scripts, all prefix-safe; no other living doc defines the marker
format; no existing time-format conventions collide):

1. `hooks/statusline.sh` — NEW: stdin-forwarding, chainable, `HH:MM`
   segment.
2. `skills/conductor/SKILL.md` — Mode Markers section: stamped format
   + same-turn pointer; close-out step 1: the per-task range line.
3. `skills/switch/SKILL.md` — step 3: sitting heading range rule +
   per-task lines; step 8: banner close time from `date`; same-turn
   pointers.
4. `docs/state-contract.md` — the same-turn rule's single definition
   (conventions section).
5. `tools/gates/README.md` — Clock line row: documented, optional,
   not validated, accepted-risk pointer.
6. `README.md` — statusline wiring paragraph beside the hooks
   section (free-slot and occupied-slot paths).

Untouched, named: `docs/gates/*` (no retrofits), AU rules (no new
validation), spec templates (per-step stamps excluded by the frame),
`hooks/hooks.template.json` (statusline is not a hook event — it
lives beside them, wired via `statusLine`, not `hooks`).

## Stage-1 measurements — named answers

1. Standalone segment: `echo '{}' | bash hooks/statusline.sh` matches
   `^[0-2][0-9]:[0-5][0-9]$` — exit 0.
2. Chained segment: with a stub command printing `STUB`,
   `echo '{}' | bash hooks/statusline.sh <stub>` prints
   `HH:MM · STUB`.
3. Marker stamp: after a stamped write,
   `grep -c '^conductor: execute @ ' kivna/.active-modes` = 1, and
   all four hook scripts run against the stamped file exit 0.
4. Single definition: `grep -c 'same-turn'` — exactly one definition
   block in state-contract; ≥1 pointer each in switch and conductor.
5. Clock row present in `tools/gates/README.md` — grep = 1; and
   `git diff --stat docs/gates/` empty at the build tip (no
   retrofit).
6. Board byte-compare: `gate.py route` output identical before/after
   for all existing slugs (the change adds no gate inputs).
