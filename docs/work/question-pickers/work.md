# The question form gains pickers, and Agent gains a role selector

## Now

Owner: the Claude session holding `kerd-b5-review` (Conductor controller, Kerd).
Stage: Complete. **Released as 0.131.0**, commit `6610f60`, pushed to `main`
2026-09-15 21:09, CI `entry-gate` green on that SHA. Anthony approved the release at
21:02 and reconfirmed at 21:04.

**Scope agreed, Anthony, 2026-09-15 20:06** ("yes" to taking the question-form
correction and Agent's role selector as the next release, with visual communication
following separately as its own release —
`docs/work/visual-communication/work.md`).

**Wording agreed, Anthony, 2026-09-15 20:29** ("thats a yes"), relayed as five rules:

- Context and recommendation come first.
- The speech bubble is always the last prose line and contains the single question.
- A native single- or multi-select picker may follow for faster answering.
- The picker must represent that same question, include Other/free-form input, and
  never narrow an intentionally open question.
- Without picker support, the person answers the bubble normally.
- "Including for an approval" is acceptable, provided the picker does not broaden
  what the question authorizes.

This builds on the 19:50/19:51 ruling correction already recorded in `CONTEXT.md` and
`docs/decisions.md`: the 0.129.0 "no boxed cards or native pickers" wording was
Claude's over-reach, not Anthony's instruction.

## Terrain, as checked 2026-09-15 20:2x

The withdrawn rule has a smaller blast radius than `TODO.md` recorded:

- `skills/conductor/references/journey.md:79-80` — "no native picker or multi-select
  control replaces the bubble". The only prose instance.
- `skills/conductor/references/journey.md:65` — "It is the last thing in the message",
  which contradicts a picker following the bubble and becomes "the last prose line".
- `skills/conductor/scripts/tests/test_question_form.py:44` — asserts *journey.md*
  contains "no native picker". `TODO.md` recorded this as asserting every entry point;
  it does not, and the entry-point lines never carried the phrase.
- `test_question_form.py:21` — `LEGACY` bans the literal string
  "multi-select question control" anywhere under `skills/`. Under the corrected ruling
  a multi-select picker may follow the bubble, for exactly the pick-several case
  journey.md names (Agent's review cadence), so that ban is retired and replaced with
  "no native picker" so the withdrawn rule cannot creep back.
- The shared "Asking the person:" line in all 12 `skills/*/SKILL.md` entry points
  gains the picker clause.
- `skills/agent/SKILL.md:66-73` — ask-once for role and cadence gains the selector.

## Work split

Two parallel players, no file overlap, change-read baselines `qp-s1` and `qp-s2`.

- **S1** — `journey.md`, `test_question_form.py`, and the eleven non-Agent entry points.
- **S2** — `skills/agent/SKILL.md` whole: its line 8 entry-point line plus the role
  selector paragraph.
- **Conductor (inline)** — release checklist: version bump in the three locations,
  README, plugin descriptions if the capability list changes, trigger descriptions.

Review: Codex `codex-tui` at its recorded cadence — checkpoint after the returns,
then before push.

## Built, 2026-09-15 20:30 - 20:45

**S1** (Opus 5 via `kerd:effort-high`, observed `claude-opus-5`/`high`, 38 records, no
gaps; baseline `qp-s1`): journey.md, the guard test and the eleven non-Agent entry
points. Change read clean both rounds - exactly its 13 owned paths, HEAD unmoved,
nothing unexpected. It mutation-tested three assertions, honestly flagged the fourth
(`"picker may follow it"`) as too generic, and that defect was returned to it; the
tightened `"native single- or multi-select picker may follow it"` was then
mutation-tested and bites. It also found and resolved the Correct / Change tension:
a stock menu stays banned *because* it carries none of the question's own options.

**S2** (Opus 5 via `kerd:effort-high`, observed `claude-opus-5`/`high`, 38 records, no
gaps; baseline `qp-s2`): `skills/agent/SKILL.md` whole. Change read clean. Three
judgment calls, all accepted: `on-request` stands alone (grounded in
`validate_review_cadence`, `agent.py:91`, and `user-guide.md:77` - without it the
guidance would have told a model to offer a multi-select the validator rejects);
"never re-asking a recorded role **or a recorded cadence**"; frontmatter description
left unchanged, since checklist item 4 binds *when* Claude reaches for the skill and
that has not changed. Its reason for not listing the five role shortcuts in the
description is the sharper one: it would present them as a permitted enum, which the
ruling denies.

**S3, inline (Conductor):** the arrival picker. Scope added by Anthony, 20:39 ("sure"),
after S1 surfaced the tension at `journey.md:58`. `journey.md`, `in-out.md` and
`skills/switch/SKILL.md` now allow a Yes / Not now / Other picker after the rendered
arrival output, on the argument that a picker is a separate surface rather than
appended text, so Switch's return-the-output-unchanged contract survives. Guarded by a
new test and mutation-checked. Done inline because it was two sentences in two files.

**Release checklist (Conductor):** 0.131.0 in the three locations; README What's New
added and the stale v0.129.0 clause pointed at the withdrawal; capability list
deliberately unchanged (a picker is presentation, not a high-level capability);
trigger descriptions deliberately unchanged in Agent and Switch, for the reason above.

**Verification:** 96 conductor + 182 agent + 443 switch tests OK;
`tools/gates/gate.py release` clean; five mutation tests, each reverted and
re-confirmed. Note for future sessions: `python3 -m unittest discover -s <dir> -t .`
fails on these suites (no `__init__.py`); root discovery at the tests directory.

## Codex checkpoint review, 20:44 (request `9f003152`)

Verdict: not ready for before-push review; four medium findings. The brief told Codex
that it had itself hardened the withdrawn ban at 0.129.0's before-push review, and
asked it to judge the correction on its merits rather than for consistency with that.

1. **Role picker had five options including a named "Other"** — duplication on hosts
   that supply Other automatically, and one over the 2-4 that `skills/pair/SKILL.md:16`
   sets. Verified and sharper than reported: Claude Code's picker supplies Other
   automatically and its tool spec says not to add one. Routed to S2, with the shared
   line's "and an Other" becoming "and always leaving a free-form answer open" across
   all twelve, and the arrival picker cut to Yes / Not now plus the host's free-form
   route. Conductor applied the `journey.md` and `in-out.md` half.
2. **`skills/pair/SKILL.md:16` still said the bubble goes "as the last line"** - a live
   contradiction with the new rule. Verified. Routed to S1.
3. **The guard omitted both safety bounds, and `"no native picker"` as a LEGACY
   fragment would reject legitimate future wording** such as "where no native picker is
   available". Both verified. Routed to S1, with whitespace normalization so a harmless
   rewrap stops reading as a rule violation - which also retires the brittleness note
   S1 and Conductor had both flagged.
4. **The separate-surface argument for Switch's arrival was argued, not observed.**
   Correct. A proper trial is circular right now: it needs 0.131.0 loaded, and the
   plugin cache does not yet carry 0.130.0, so "before release" means paying for a
   fresh-worker scenario against the working tree.

**Anthony's ruling, 20:5x, answering a bubble followed by a native picker** (the
release's own mechanism, used to ask about itself): release, and verify at the next
real Switch In here. The change is wording-only with no code path, and the next pickup
exercises it for free - consistent with the standing rule against manufacturing a
build to observe something.

**Correction, after Codex's before-push review:** the framing Anthony decided on
called the failure mode "a presentation regression rather than lost work". That
understated it. One of the untested behaviours is whether a picker Yes opens
direction-setting without approving saved work - an authority question. If a Yes
were read as approving the saved task, it could start work that was only meant to
be discussed. The risk is bounded - the bubble prose still states the mapping, and
the first real Switch In exercises it - but it is not cosmetic, and Anthony was
told it was cosmetic when he made the call. Put back to him at 21:02 with the corrected
characterisation; he reconfirmed the release unchanged ("no", his call on the
risk was not changed by it). The countermeasure that followed is the visible
label: the arrival picker's option reads “Yes — open direction-setting”, never a
bare Yes, and the guard asserts that exact label rather than the prose claiming
one exists — Codex's re-review caught that the first attempt only claimed it.

**Observed in that exchange:** the picker followed the bubble as a separate surface and
the prose above it was unchanged. That is the mechanical half of the separate-surface
claim observed once. Still untested: the renderer's byte-identity through
`where_we_are.py` with a picker attached, and that a picker Yes opens direction-setting
without approving saved work. Both are to be recorded at the next real Switch In.

## Next

Nothing owed on this release. Two deferred observations are recorded for the first
real Switch In on 0.131.0, and belong in that sitting's account, not here:

1. whether the renderer returns byte-identical Markdown with a picker attached;
2. whether a picked "Yes - open direction-setting" opens direction-setting without
   approving the saved task - the authority half, and the reason the label exists.

Neither is a build. Record what the next pickup actually shows; do not manufacture a
run to see it.

The visual-communication release (`docs/work/visual-communication/work.md`) is the
next one, still at Shape, with Archify's install needing Anthony's approval.
