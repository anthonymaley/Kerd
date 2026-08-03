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
