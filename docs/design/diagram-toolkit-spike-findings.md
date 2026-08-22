# Diagram toolkit spike — findings

Run 2026-08-22 against `cathrynlavery/diagram-design` (MIT), in a throwaway
directory, never installed into this repo. Frame and kill criteria:
`docs/product/diagram-toolkit.md`.

## Verdict against the four criteria, declared before the spike ran

| | Criterion | Result |
|---|---|---|
| 1 | Expresses containment without arrows | **PASS** — a dedicated `nested` type: *"hierarchy through containment… outer = broader, inner = more specific"*. The drawing that worked used zero arrows. |
| 2 | Works without the network | **PASS** — the font stacks already declare fallbacks (`'Geist', system-ui, sans-serif`). The CDN `<link>` can simply be left out; typography substitutes, the diagram renders. |
| 3 | Stable enough to live under CI | **FAIL** — see below. This is the structural finding. |
| 4 | Cheaper than the generator it replaces | **PASS** — ~90 lines of markup against 141 lines of Python for a comparable diagram. |

## The structural finding: there is no generator

**Every script in the repository is a verifier, a linter or a build helper.
None of them draws anything.** A diagram is produced by *the model writing SVG
from a template*, and the linters check the result afterwards.

So "deterministic", as its README uses the word, means **the templates carry no
layout engine and no randomisation** — not that two runs produce the same bytes.
Run it twice, get two different diagrams.

**Consequence, and it is permanent:** this cannot serve the progress board or
anything else derived from disk and byte-compared in CI. A renderer whose output
differs between runs turns the staleness refuser into a source of false alarms.
Job 2 is closed to it forever, not pending a fix.

**The other side of the same fact:** because generation is prompt-driven, the
5,961 lines across 27 bespoke generators are not replaced by other code. They
are replaced by a prompt and a lint pass.

## What the linters are worth

`lint-skin.py` rejected the first attempt with four accessibility defects — a
missing `<title>`, a missing `<desc>`, and accessible-name IDs that did not
match the file slug. Fixed as directed, second attempt clean.

That is a refusal from outside the model, which is the standard this repo holds
its own gates to. `lint-render.py` goes further and uses headless Chromium as
the oracle — screenshot as authored, screenshot with `overflow` released, diff
the two — to catch content clipped by the viewport.

## THE FINDING THAT MATTERS MOST, and it is about the operator

**Two diagrams were produced. The producer's verdict on the first: *"yes that
drawing is correct."* On the second: *"none of the diagrams make any sense…
was text on the screen with box that made no sense to the subject."***

The difference is not the toolkit. It is the same toolkit both times.

- **The first drawing used a type.** `nested`, whose rule is that containment
  means something: outer is broader, inner is more specific. The boxes *carried*
  the argument.
- **The second freelanced.** It ignored all 38 types and hand-rolled three bands
  of panels with paragraphs inside them. Its first band happened to be right —
  one requirement drawn inside the rule it qualifies — and the other two were
  **prose in rectangles**.

**The rule this produces, which is the spike's most useful output:** *a box must
mean something.* If a box is only a container for text, the result is a slide,
not a diagram. This is the standing decision — *"what fails the gate is prose"* —
reappearing one level down: prose does not stop being prose because a rectangle
is drawn around it.

**And the operating instruction that follows: pick a type and obey its layout
rules. Do not freelance.** The toolkit's value is 38 opinionated layouts; a
hand-rolled panel grid discards exactly the thing being adopted.

## A verification failure worth recording separately

Both diagrams were shipped to the producer **without ever being rendered**.
`lint-skin.py` reads source and passed; `lint-render.py`, which exists to catch
what a picture actually looks like, needs headless Chromium and was skipped.
This repo's own kit already carries `overflow_report`, `collision_report` and
`text_overlap_report` for the same reason, and neither was used.

"I built it" is not "it works", and for a *drawing* the only real check is
looking at it.

## Kept

- **The verdict:** adopted for job 3 — explaining a design. Closed for job 2.
  Job 1, the evaluation matrix, was never in scope.
- **Two rules worth taking regardless**, both now measured rather than assumed:
  **every coordinate divisible by 4** (verified on both drawings — 66 and 150
  coordinates, none off-grid) and **density 4/10, every node earns its place.**
- **The operator rule above**, which is the thing that decides whether any of
  this is worth anything.

## Not done

- No adoption shipped. A spike that ships is not a spike; whatever survives
  re-enters the ladder as normal work.
- `lint-render.py` never run — it needs a Playwright install this spike declined
  to make.
- The evaluation matrix spin-off stays framed and unbuilt.
