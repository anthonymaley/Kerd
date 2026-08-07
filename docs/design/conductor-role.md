# The conductor role — what remains, and the graduation map

Living design doc. Source: post-walk decision 6 — conductor's protocol is
a seedbed; the pieces graduate out to the system's functions as each
instrument proves. What remains is the DRIVING ROLE.

## Vocabulary — out of scope for the funnel rename

**Added 2026-08-07.** A cross-cutting rename is queued: the machine's `rung`
becomes a **stage** of a **funnel**, per Tony's call that the work flow is a
funnel with stages and steps inside them. **That sweep must not touch this
file.** Here "rung" and "ladder" name *authority* — who may decide what, and
who hears a blocker — not a position in the work flow. Renaming them would
convert the role ladder into a role funnel by accident and change the seat
diagram's meaning without anyone deciding to.

## The seat

Rung two of the role ladder:

```
Tony (the last rung — never asked a fact, never guessed a position)
  ↑
intent-holder — an agent holding the composed intent, with DECLARED
  adjustment power; may reshape within it, escalates beyond it
  ↑
CONDUCTOR — the driving role (this spec)
  ↑
players and tools — sized per piece, bounded per invocation
```

## What the driving role owns

- **Dispatch** — next unblocked piece from the work order; which player,
  which tools (tools staffed like players: bounded contract in, result to
  the caller, KILL authority over rogue tasks).
- **Judgment of returned evidence** — against the piece's own check plus
  everything its change touches; re-dispatch, never re-specify.
- **Park vs stop** when a question waits on the human — nothing is built
  that the pending answer could invalidate; which of the two is the
  conductor's call.
- **Work commits** — each verified piece committed and pushed, staged by
  name; the liveness strip ticks on these.
- **Two tempos, one role**: INTERACTIVE (the human present — today's
  protocol, unchanged) and UNATTENDED (the loop's driver — enterable only
  through the loop's gate: a live refusal instance). The human's presence
  always overrides: interactive is never removed.

## The graduation map

Each protocol piece leaves for its function ONLY when the replacement
proves — an instance passing its own acceptance. No-rip: conductor sheds,
never breaks.

| Protocol piece (today) | Graduates to | Trigger |
|---|---|---|
| Pre-flight inventory | **Entry gates** | fired at v0.69.0; **shed at v0.91.0** — the inventory runs `gate.py route <slug> --json` first and asks the human only for what the gates cannot know (`skills/conductor/SKILL.md`) |
| Model advisory + sized tags | **Size work to a model** | sizing declarations ride the work order (the contract carries tier + effort + why per piece) |
| Spec-file machinery | **Write the contract** | work orders with per-piece checks + two-tier access exist as the contract instrument — **⚠ untestable as written: "two-tier access" appears in no other file in the repo and has no acceptance criterion derivable from disk. A trigger nobody can test never fires. Define the term or strike it before this row can be acted on (2026-08-07)** |
| Plan-gate approval | **Design GO + contract measurability** | the design package GO (two keys) + machine-measurable pieces remove the per-spec human gate |
| Verification gate + collateral check | **Build a piece · Prove it** | checks refuse from outside the model (CI instance) — behaviour unchanged, ownership moves |
| 3-fix + composer hand-back | **The role ladder** | the intent-holder exists as an agent with declared adjustment power |
| Close-out doc updates | **Byproduct capture** | dissolves — anything worth keeping is written the moment it exists (the state-in-artifacts property; the close-out-deferred loss window closes) |
| Scope-creep hard stop | **The work order** | out-of-plan work becomes a work-order change request riding the ladder |
| Decision recording | already byproduct | done — records at the moment of decision today |

## What conductor never was, and never becomes

The session boundary (switch's — conductor calls it at close-out since
v0.84.0, but never re-describes or owns it), the vault (kivna's, on
demand), context management (dissolved by construction — exact slice
per piece, free restarts between pieces).

## Transition rules

1. **No-rip** — a piece graduates only when its replacement passes its own
   acceptance in real use.
2. **One piece at a time** — each graduation is a normal work item through
   the gates, with its own check.
3. **Interactive tempo is permanent** — unattended is an addition behind
   its gate, never a replacement.
4. Until the graduations land, today's conductor skill runs unchanged —
   it is the living seedbed, and breaking it breaks the only working
   instance of half the system's functions.
