---
route: problem
stage: framed
---

# Inline work gets a composer call — the score it currently skips

## Value

Tony's requirement, in his words (2026-08-13 evening, stated after a session
proposed hand-writing four retroactive gate records for two features that had
already shipped):

> yes this is an issue as many enhancements, changes or ideas come inline.
> composer is where the value is

and, asked whether the score should replace the design and contract records or
whether inline work should gain a call it does not make today:

> inline work should get a composer call it currently skips entirely

Conductor today routes small work *away* from the composer by rule. Its
lean/inline path says "No composer call, no spec file", and the composer
section closes with "Skip the composer call entirely for lean/inline tasks — if
there's no score to write, there's no one to summon." The premise is false.
There is a score to write; the work simply proceeds without one, and the
reasoning that would have gone into it is spent once in conversation and then
lost.

The measure of winning: **an inline enhancement leaves a score on disk** — one
artifact, written by the model that is good at writing scores, precise enough
that the build can be checked against it afterwards. Today the count of scores
left by inline work is zero, and it is zero by rule rather than by accident.
The two most recent shipped features — `model-effort-advisory` (v0.98.0) and
`hooks-autoload` (v0.96.0) — were both built this way and both left none.

The value is the score itself, not the paperwork around it. This item does not
buy a design doc, a GO record, or a board position; it buys the one artifact
that carries the reasoning.

## Grounding

- skills/conductor/SKILL.md — the lean/inline path (line 214) and the skip rule (line 247), the two sites that route inline work away from the composer; also the existing composer-unavailable fallback this item depends on.
- docs/design/conductor-role.md — the four-role seating and the composer's cost model: top tier bought per-call rather than per-session, which is what makes a call affordable on small work.
- docs/product/model-effort-advisory.md — a proportional-middle build that shipped at v0.98.0 and left no score; the first of the two measured instances.
- docs/product/hooks-autoload.md — the second instance, same shape, shipped at v0.96.0.
- tools/gates/README.md — the rung ladder and what each rung demands, which is what makes a missing score visible downstream.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| A composer call on every small task becomes ceremony, so users abandon conductor for inline work and it leaves fewer artifacts than it does today | yes | worse than the status quo: today inline work leaves no score but still runs under conductor's verification gate; an abandoned conductor loses the gate too | high without the countermeasure — the lean/inline path exists precisely because the full delegated path felt too heavy, and the last two features both took the proportional route by explicit producer call | measured: conductor's own text created the lean path for this reason; v0.96.0 and v0.98.0 both chose it | countermeasure - permanent | The score is sized to the work like every other call: a short score for a small change, not a twelve-step spec. The call is one brief and one score, and it replaces the conversation's lost reasoning rather than adding a stage | |
| Top-tier capacity runs out, so inline work blocks on an unavailable composer | no | inline work stalls, or silently degrades to a worse score without the producer knowing | medium — capacity limits are real and already documented as a failure mode | conductor already specifies the fallback: write the score as conductor and say so explicitly at the gate | countermeasure - permanent | Reuse the existing composer-unavailable rule unchanged — conductor writes the score and names it as the lesser one at the approval gate | |
| The score satisfies the contract rung but not the design rung, so inline work still cannot reach goal and the board still misreports it | no | a composer call is paid for and the board is unchanged — the visible symptom that motivated the investigation survives | certain as the gates stand today | measured this session: `gate.py route model-effort-advisory` reports every frame/viability/slice/design input present and still demands `docs/design/<slug>.md` plus a design GO record before contract | countermeasure - temporary | Slice 1 deliberately does not claim the board fix; whether one score can satisfy both rungs, or whether a proportional route legitimately skips design, is the central question of this item's design rung | Fires at the design rung — the decision must be taken there, not deferred again |
| The score is written but nothing checks it was written, so the rule decays into advice | no | inline work drifts back to no score, invisibly | medium — this repo's standing finding is that skill text cannot enforce on itself | `OPS-001`, and the measured history of prompt-layer gates in this repo | countermeasure - temporary | Slice 1 ships the rule at the prompt layer and names it as unenforced; a refuser is a later slice once the artifact's shape is settled | Fires when slice 1 has run on real inline work and the score's shape is known |

## Release slice

Rigor level: mvp

Slice 1 — inline work gains the call:

- `skills/conductor/SKILL.md` line 214: the lean/inline path stops saying "no
  composer call, no spec file" and gains a sized composer call that writes a
  short score.
- `skills/conductor/SKILL.md` line 247: the skip rule is removed, and the
  premise it rests on ("if there's no score to write") is named as false.
- The score's location and shape for inline work — where it lands and how it
  differs from a delegated spec, which is the part that must not simply
  reproduce the twelve-step contract at small scale.
- The composer-unavailable fallback is stated as applying here too.

Deliberately excluded, each for a reason:

- **Any change to `tools/gates/`.** Whether a score can satisfy the design rung
  is this item's design question, not a frame-time assumption — see risk 3.
- **Closing `model-effort-advisory` and `hooks-autoload` on the ladder.** They
  are the evidence that motivated this item, not its scope; they close through
  whatever this produces, in their own sitting.
- **A refuser that checks the score exists.** Named as unenforced in slice 1
  rather than pretended otherwise — see risk 4.
- **Any change to the delegated path**, which works and is not the problem.
