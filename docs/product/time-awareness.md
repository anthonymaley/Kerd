---
route: new
stage: done
---

# Time-awareness — the machine consults a clock, and effort becomes data

## Value

Born from Tony naming it live (2026-08-06, ~12:30 EDT): the model
wrote "late-evening sitting" at midday, then dated a TODO item
"midnight" without checking — the model cannot tell time and
misjudges elapsed effort. Two wrong-by-hours labels in one day; every
honest time label so far exists because a hand ran `date`. Meanwhile
git already timestamps every commit exactly — rung *landings* are
boundable today; what's missing is start times, in-session moments,
the human's clock, and the model consulting one while writing. The
aim behind the capture (Tony's framing at approval): task start and
end give duration; accumulated durations are the base that makes
effort estimates for future tasks accurate instead of guessed.

Value, in units:

- **Wrong-by-hours labels in new artifacts: 2 observed → 0.** A time
  may be written only when a machine produced it in the same turn — a
  `date` run, or a machine-written record read this turn (the
  same-turn rule, amended at contract time; definition in
  `docs/state-contract.md`).
- **Human clock: statusline segments 0 → 1.** A date-driven statusline
  segment renders the time on every update — opt-in, wired like the
  hooks.
- **Effort actuals per conducted task: 0 → captured.** Task start
  stamps ride the `.active-modes` phase-marker write at plan approval;
  task end is the work commit's git timestamp, already exact and free.
  Sitting sections record start–end ranges at the boundary. The
  actuals are the calibration base for estimating future tasks —
  estimates themselves stay a later slice.
- **Duration-per-rung: underivable → derivable for new gate records.**
  New records carry a `**Clock:**` line; with git commit times, rung
  durations get bounded at both ends. First on-disk home for the
  parked journey view's time data (its named prerequisite).

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| The model writes a plausible time instead of running `date` — the birth failure | yes | false times land in immutable records (worse than no time) and poison the calibration base | medium — it happened twice on the birth day | the "midnight" self-date; the "late-evening" heading written at midday (kivna/sessions/2026-08-06.md, correction note) | countermeasure - permanent | the same-turn rule: a time is written only when a machine produced it in the same turn — a `date` run, or a machine-written record read that turn (marker stamp, git timestamp); the machine layer checks presence/format only — time *honesty* is a declared limit, same class as retrieval-not-comprehension | |
| Retrofitted timestamps manufacture history | no | false records at any depth, silently plausible | low once named | the grounding precedent: declaring is opting in; a reconstructed value cannot be honest | countermeasure - permanent | new records only; nothing backfills a time into an existing artifact | |
| The statusline renders for the human only — the model never sees it | no | the model stays clock-blind in prose unless it runs `date` itself | certain — a named limit, not a defect | Tony's own framing: "the model doesn't see the statusline" | accepted | | a harness change ever exposes statusline content to the model |
| Clock-line presence unenforced in new records | no | a new gate record ships without its Clock line, silently | medium | AU rules check shape, not a record's birth date — old records legitimately lack the line | accepted | | first observed missing Clock line in a new record: graduate a dated-cutoff presence check into AU |

## Release slice

Rigor level: mvp

Slice 1 — **honest actuals, no estimates**: `hooks/statusline.sh`, a
date-driven statusline segment for the human (opt-in, wired with
resolved absolute paths per the hook-path gotcha, wiring documented
with the other hooks); the same-turn `date` rule written into switch
(sitting headers and banners) and conductor (phase-marker writes gain
a timestamp; close-out records each task's start–end range from the
marker stamp plus the work commit's git time); the gate-record schema
gains an optional `**Clock:**` line for new records (tools/gates
README — goal records first).

Deliberately excluded, named:

- **Per-step spec timestamps** — noise; per-task is the unit effort
  estimation needs.
- **Retrofits of any existing record** — manufactured history.
- **Estimates and derived duration views** — the parked journey
  view's slice when it wakes; slice 1 only builds the actuals base.
- **CI enforcement of Clock presence** — sits behind the accepted
  risk's review trigger, not built here.

## Grounding

- TODO.md — the birth item and its evidence (Tony 2026-08-06)
- kivna/sessions/2026-08-06.md — the mislabeled sitting and its correction note, the live evidence
- skills/switch/SKILL.md — sitting headers and banners, two of the write moments
- skills/conductor/SKILL.md — phase-marker writes and close-out, the task start/end moments
- tools/gates/README.md — the gate-record schema the Clock line joins
- hooks/ — the opt-in wiring pattern statusline.sh follows
