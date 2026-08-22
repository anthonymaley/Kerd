---
route: spike
stage: framed
---

# Diagram toolkit — can someone else draw our pictures?

## Value

**A drawing costs us a Python file. A paragraph costs nothing. That is why
"design is agreed in diagrams" keeps losing to prose.**

Measured 2026-08-22: `tools/diagram/` holds **27 hand-written generators,
5,961 lines**, one per drawing — `gen_flow_design.py`, `gen_flow_contract.py`,
`gen_rigor_level.py`, and 24 more. Every new picture is a new program.

The standing decision this undermines is Tony's, 2026-08-02 and re-confirmed by
running it the next day: *"Design is agreed in diagrams, not prose. Tony thinks
in high-level diagrams; prose is the wrong review modality, which is what 'too
much noise' has meant every time."* The evidence for it was that **every
substantive correction on 2026-08-03 came from drawing it, not discussing it.**

So the rule is right and the cost is what breaks it.

**Candidate:** `cathrynlavery/diagram-design` (MIT) — a Claude Code skill
generating self-contained HTML + SVG, 39 diagram types, deterministic output,
brand extraction from a URL, draw.io and Mermaid import.

**Winning:** a picture costs a prompt instead of a program, and the drawings
look like they came from one hand.

## The three jobs, because this is not one decision

Tony, 2026-08-22: *"im not saying this is the ONLY tool for visualizing, the
eval matrix can be its own tool too… this tool COULD be the answer for current
state views, proposed process and tech designs etc, a toolkit for us to
visualize consitently."*

| Job | What it needs | Who serves it |
|---|---|---|
| **Decide between options** — the evaluation matrix | colour carries cost; ~150 cells | **ours**, `tools/design/` — 1,767 lines, own CLI, 14 fixtures, 2 CI steps |
| **Show where work stands** — the progress board | derived from disk, byte-compared in CI, ~200 cells | **ours** — nothing else does derived-from-disk |
| **Explain a design** — current state, proposed process, architecture | editorial, 7–12 nodes, no derived-from-disk requirement | **this spike** |

**This spike covers the third job only.** The first two are not in scope and
are not up for replacement.

**The colour objection dissolves on that split.** The toolkit's central rule is
*"colors carry strict semantic roles, not user choice"* with an accent capped at
two elements, which collides with our grammar of red-means-cost. But colour is
load-bearing **only in job 1**, which is not going near this tool. Tony,
2026-08-22: *"color also we can give a little on, where we really need it is the
eval."*

## The question

Can a third-party toolkit draw our job-3 diagrams well enough, and cheaply
enough, that we stop hand-writing a generator per picture?

## Method

Take **one existing bespoke generator**, redraw the same diagram with the
toolkit, and put the two side by side. One real drawing, not a toy.

Never installed into this repo's environment — a throwaway directory, exactly
as the StrictDoc spike was run.

## Kill-or-keep

Declared before it runs, so the answer is read off rather than argued
afterwards.

**KILLED if any one of these holds:**

1. **It cannot express containment without arrows.** Our grammar is
   *"containment rather than arrows"*, with arrows the one exception in stage
   flows. A toolkit that reaches for arrows first cannot draw what we draw.
2. **It needs the network to look right.** Its typography loads Google Fonts
   from a CDN via `<link>`. Our own evaluation criterion is *"no server needed
   to read it"*, and a diagram that degrades offline fails it. Killed unless
   fonts can be embedded or dropped without the result looking broken.
3. **The output is not stable enough to live under CI.** The board is
   byte-compared at every push. A renderer whose output drifts between runs
   would turn the staleness refuser into a source of false alarms.
4. **Redrawing costs more than the generator did.** Measured against the real
   file it replaces, in the producer's own standard — *"i just mind overhead and
   overwork"*.

**KEPT if** a real diagram comes out looking right, offline, reproducibly, for
less effort than the Python file it replaces. What is kept is **the finding and
the sample**, never a shipped adoption — whatever survives re-enters the ladder
as normal work.

**KEPT EITHER WAY — two rules worth stealing whatever the verdict:**

- **Every coordinate divisible by 4.** Claimed as what stops a diagram looking
  machine-made. Cheap to apply to our own generators.
- **Density target 4/10 — every node earns its place.** That is *"too much
  noise"* with a number attached.

Tony has already named the value of learning from a tool without adopting it:
*"superpowers does some great things… so we can learn from it."*

## Deliberately not in this spike

- **The evaluation matrix** and **the progress board**. Different jobs, both
  ours, neither up for replacement.
- **Spinning the matrix off as its own tool.** A real idea and a separate frame.
  Held until this verdict lands, because if the toolkit is adopted the packaging
  question for both tools becomes the same question.
- **Adopting anything.** A spike that ships is not a spike.
- **Where an evaluation's output lives.** Already settled by approved
  requirements: R-0038 — the tools work on the project you are in, not on where
  they were installed — and R-0036 — a project's own repository holds its
  information, not Kerd.
