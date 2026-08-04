# Annotation log

Annotations are a **queue, not an archive**. Tony writes on the canvas, the
comment is captured to `<diagram>-tony.json`, it gets acted on, and then it is
**deleted** — the substance now lives in the diagram, the generator, or a
decision record.

This file is the disposition trail, so a comment never disappears with nothing
to show for it. Append-only; it is a record of events, so entries are dated and
never rewritten.

Deleting them also fixes a real defect: preserved annotations kept absolute
position but not attachment, so a comment drifted away from what it annotated
whenever the layout reflowed. A comment that lives one cycle cannot drift.

---

## 2026-08-03 — `2026-08-03-frame-the-intent-flow`

**"Its extensively tested in ~/toyota-sensei and other projects though"**
Placed on the sensei bet at step 5.
→ **Dealt with.** The bet was wrong as written. Sensei is not untested — it is
proven elsewhere and has simply never run inside Kerd, so the bet narrowed to
*transfer, not the method*. Changed in the step 5 note and in the tooling
catalogue (`gen_functions.py` → `TOOLING`). Commit `a976e11`.

**"Green is collaboration Foudner > Claude"**
Placed top-left, as a grammar addition.
→ **Dealt with.** `GREEN` added to `kit.py`. First applied wrongly — I read it
as *steps where both of us act* and coloured capture and the two-key approval;
Tony's rule is **his input into the work**. Reverted the steps, kept the colour,
and it is now in the flow legend. Commit `a976e11`.

---

## 2026-08-03 — `2026-08-02-product-to-build` (backlog: six pre-queue comments)

These six predate the queue policy — captured 2026-08-02, preserved and
re-merged on every regeneration since. One had drifted onto movement-4 text
(the exact defect the queue dissolves). All six were acted on long before the
policy existed; dispositions recorded now, file deleted.

**"we need an actual measurement that we can use to know when we have achieved
or to show the gap"**
→ **Dealt with.** Became the EVIDENCE column of the function map — the
`gen_functions.py` header quotes it verbatim. Every row states what you could
point at.

**"super important, MVP vs someday"**
→ **Dealt with.** Movement 7 — the build sequence with MVP / SPIKE / v1 /
SOMEDAY bands. Tony's call on the ordering.

**"diagram to show gap/change/impact"**
→ **Dealt with.** The story-format MUST in *How we talk to each other*
(compare/contrast: current → new → what changes) and v0.68's now / the change /
what it means shape.

**"Where doest TDD and testing live"**
→ **Dealt with.** Settled today: testing strategy is part of the *Design the
solution* package (test bias per layer, contract seams named), proof layers are
BUILD's verify functions.

**"Leverage Sensei Story formats for diagrams (see examples)"**
→ **Dealt with.** The pick-a-story-format MUST, and sensei's TOOLING row
(proven elsewhere; the bet is transfer).

**"Could be a spike too."**
→ **Dealt with.** The SPIKE band exists — "SPIKE — not a decision", routing
bet tested rather than decided.

## 2026-08-03 — `2026-08-03-frame-the-intent-flow` (file cleanup)

Both comments were dispositioned above (commit `a976e11`) but the capture file
lingered — deleting a dealt-with file is part of the queue policy. Deleted.
