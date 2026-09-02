---
route: spike
stage: framed
---

# Question set derivation — can a rung's questions be reproduced from durable sources, or must each be researched fresh?

## Value

**Winning, in the producer's words (2026-09-02):** *"determining whether a
rung's question set can be reproduced from durable sources instead of
reinvented through model judgment each time."*

**The two shapes success may take, his words verbatim:**

> - A candidate viability set where every question traces to a machine-enforced
>   gate need or named standing decision and exposes the material viability
>   issues in representative passed items; or
> - A bounded finding that full derivation fails, identifying precisely which
>   necessary questions require fresh Law 4 research or unrecorded judgment.

**And the boundary, his words:** *"The deliverable is evidence and a scoped
verdict—not a shipped seed file or new machinery."*

**What is at stake, measured.** Drive drives **one gate of seven**. Its own text
says so: *"Viability, scope, design, work handoff, loop and acceptance have no
question set yet."* One set exists —
`docs/work/question-sets/software-change.md`, six questions, 24 lines, serving
the frame gate. Six rungs have none. If a set is derivable, the remaining six
are a bounded afternoon; if each needs fresh Law 4 research, they are six
research items and the umbrella stays one-seventh built for as long as that
takes. **That difference is the whole reason this is a spike and not a build.**

**The producer's stated fear, recorded 2026-09-01 and unresolved:** that each
rung needs fresh Law 4 research. This spike exists to test that fear against
evidence rather than settle it by assertion.

## The question

Can the questions a rung asks be **derived** from (a) what the gates already
machine-enforce at that rung and (b) standing decisions already
standards-anchored — or does some necessary question come only from fresh Law 4
research or from judgment nobody wrote down?

**The viability rung is the test case**, chosen because it is the next rung
after the one set that exists, so a derivation there is checkable against a
worked example rather than against nothing.

## What "derivable" is measured against

Stated before the derivation runs, so the verdict is read off rather than
argued afterwards.

**A question is DERIVED if it traces to one of exactly two sources:**

1. **A machine-enforced gate need** — a check in `tools/gates/kit.py` that
   refuses when the thing is absent. Cited by symbol and line.
2. **A named standing decision** — a bullet in `CONTEXT.md ## Key Decisions`,
   or a rule in a living design doc, that is already standards-anchored or
   already keyed by the producer. Cited by its dated headline.

**A question is NOT derived if** it comes from the model's sense of what a good
viability question is, from a standard nobody has read into this repo yet, or
from an unrecorded convention. Those are the interesting cases — the finding's
job is to name them precisely, not to hide them by writing a plausible question
anyway.

## Method

1. **Enumerate the viability rung's exit demands from the code**, not from
   memory. The structural rule this depends on is already ruled and is stated
   here because the whole derivation rests on it: *the check that guards rung
   N's exit lives in rung N+1's block* — `kit.py`'s frame-gate question-set
   check sits inside the viability block "because `frame` requires nothing to
   enter, so the frame gate's exit is the viability block" (the 2026-08-28
   code-location-versus-reader-name ruling). So viability's exit demands are
   what `check_rung(slug, "scope")` adds.

2. **Attempt the derivation.** For each demand, write the plainest question
   whose answer satisfies it, and record the citation. Where a demand yields no
   sensible question, or a necessary question has no demand behind it, record
   that instead of inventing.

3. **Test against representative items whose viability rung genuinely passed.**
   The test is not "does the question read well" — it is *would this question
   have surfaced the material viability issue that item actually hit?* An item's
   real issues are recoverable from its risk ledger, its CONTEXT.md decisions
   and its gate records.

4. **Read the verdict off the kill-or-keep below.** Do not argue it afterwards.

**Evidence tiering, stated because it bounds the finding.** A citation to a
line in `kit.py` is primary. A citation to a CONTEXT.md decision is primary for
*what was decided* and says nothing about whether it was right. A claim that no
source exists is the weakest kind and is reported as *searched X, Y; not found*
— never as *does not exist*.

## Kill-or-keep

Declared before the derivation runs.

**Full derivability is KILLED if any one of these holds:**

1. **A necessary question has no source.** If the derived set omits something
   the representative items show was materially load-bearing at viability, and
   no gate need or standing decision produces it, derivation is incomplete —
   and the finding names that question specifically.
2. **The gate demands are too thin to yield a set.** If viability's exit
   demands produce fewer questions than the rung needs to do its job, the
   remainder is judgment, and the shortfall is the finding.
3. **A derived question passes an item that should have been stopped.** A set
   that would have waved through a known-bad viability decision is worse than
   no set, and its failure is the result.

**Full derivability is KEPT if** every question in the candidate set carries a
citation of one of the two legal kinds, **and** the set surfaces the material
viability issues in the representative items tested.

**A third outcome is legal and is expected to be the honest one: PARTIAL.**
Some questions derive, some do not. The finding then states the split
precisely — which derived, which did not, and what the non-deriving ones would
need. **A partial result is a real answer, not a failure to reach one**, and it
still sizes the remaining six rungs: it says how much of each set is free and
how much is research.

## Deliberately not in this spike

- **Any gate machinery.** No `kit.py` edit, no new check, no AU rule.
- **`docs/work/question-sets/viability.md`.** The candidate set lives inside the
  finding as evidence. Writing it to the directory Drive reads at intake would
  ship it, and *a spike that ships is not a spike*
  (`docs/product/standards-grounding.md`).
- **The other five rungs.** Viability is the test case; the finding sizes the
  rest, it does not write them.
- **Whether the derived questions are well-worded.** Wording is the adoption
  item's problem. This spike tests derivability, not craft.
- **A verdict on the frame set that already exists.** It is the worked example
  the derivation is checked against, not a thing under review here.

## Grounding

- tools/gates/kit.py — the machine-enforced demands one of the two legal citation sources points at
- docs/work/question-sets/software-change.md — the one set that exists; the worked example the derivation is checked against
- CONTEXT.md — the standing decisions that are the second legal citation source
- docs/product/hooks-autoload.md — a live item sitting at viability, and its ledger is a representative test case
- docs/product/standards-grounding.md — the spike shape this frame follows, and the source of "a spike that ships is not a spike"
- skills/drive/SKILL.md — where a question set is consumed at intake, and the text recording that six rungs have none
