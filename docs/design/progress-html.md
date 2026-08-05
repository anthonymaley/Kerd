# Progress HTML — design package

Living design doc. Owner: the `progress-html` work item
(`docs/product/progress-html.md`), slice 1. Parent:
`docs/design/progress-view.md`. Sibling it amends:
`docs/design/push-wiring.md` (the byte-compare set grows from a pair to
a trio — that doc's "both files" becomes "all three" when this ships).

## What it does

One committed, self-contained page — `docs/plans/progress.html` — that
answers "where are we?" on open: the board at a glance, every goal
strip, click any goal for its pieces and per-rung named have/need, and a
freshness line saying what state the picture reflects. Read-only, works
cold over `file://`, zero external requests. Guarded by the same
staleness check as the canvas pair: a lying page cannot sit at a pushed
tip unnoticed.

## The freshness anchor — and the self-reference catch

The product doc's third Value row wants the page to name what it was
rendered from. **It must NOT embed HEAD:** the commit that stores the
page moves HEAD, so the next fresh render would differ by exactly that
hash — permanent staleness, every ship deadlocked. Same killer class the
push-wiring probe answered (the render must not change what the next
render shows).

The anchor derives from the MODEL instead, so it converges by
construction — render-only commits do not change the model:

- **Freshness line:** the newest landed-piece commit across all goals
  (already in the derived model, trailer evidence), shown as short sha +
  subject; plus a **state fingerprint** — `md5` of the canonical model
  JSON — so two pages are comparable at a glance.
- Both values change exactly when the picture changes. Nothing else in
  the page may vary run-to-run (no timestamps, no HEAD, no randomness).

## Generation — one write path, grown

`progress_kit.write_pair(canvas, dir_path)` becomes
**`write_surfaces(model, canvas, dir_path)`** — the single serializer of
ALL committed view surfaces: the `.excalidraw`, the `.svg`, and now
`progress.html`. The render and `stale` both write through it, same as
today; the byte-compare set becomes the trio. The HTML needs data the
canvas doesn't carry, hence `model` joins the signature; per-slug named
have/need comes from the gates kit already loaded in-process
(`load_gates_kit()` exists in progress_kit).

**`FIX_LINE` grows** to add all three files. Fixture F12's spelled-out
literal must be updated to the new line — the spelled-literal rule
stands (asserting the constant against itself proves nothing).

## The page

Self-contained: inline CSS, inline vanilla JS, model + gate detail
inlined as a JSON `<script>` block at generation. System font stack, no
external anything.

- **Header:** title · the freshness line.
- **Board:** the rung × slug grid, same glyph vocabulary as the table
  (`#` built · `>` in flight · `·` missing with need-count · `G`
  agreed); colour grammar holds — red marks missing/cost, nothing else
  is red.
- **Goal strips:** one row per goal — bar of landed/in-flight/remaining,
  counts, drift flag if any.
- **Click a goal → detail panel:** its pieces (n, text, state, evidence
  sha where landed) and, per rung, the gate's named have/need lines
  verbatim.
- Read-only. No control mutates anything, nothing polls, nothing
  refreshes itself.

## Determinism

Same rules that made the byte-compare safe for the pair: iteration over
sorted structures, no time, no random, values derived only from the
model and the gate detail. Proof: two consecutive generations
byte-identical (a fixture asserts it).

## Staleness and CI

No new CI step. The existing seventh step covers the trio automatically
because `stale` compares whatever `write_surfaces` writes. A stale or
missing `progress.html` reds the tip naming it, message carrying the
grown fix line.

## Testing strategy

- **F14:** two consecutive `write_surfaces` runs byte-identical (html
  included).
- **F11–F13 amended:** the trio replaces the pair — converged → 0;
  drifted → 1 naming all three stale files with the NEW fix line as a
  spelled literal; missing → 1 naming all three.
- **At ship:** both-ways demonstration on the real tree (the 0.70.0
  pattern), then the expert-user pass — Tony opens the committed page
  cold over `file://` and answers "where are we?" without touching a
  terminal. That open IS the acceptance of the product's first Value
  row.

## Named answers — the stage-1 measurements

| Measurement (product doc, Value) | Target | Named answer |
|---|---|---|
| Actions to answer "where are we?" | open one file | `docs/plans/progress.html` is committed and self-contained; board + strips on open, detail one click deep. Measured by: the expert-user cold open at ship. |
| Detail on demand | in the page, zero terminal | Pieces and per-rung named have/need inlined at generation from the model + gate kit; expand on click. Measured by: the drill-down present for every slug in the fixture model. |
| Trust in what you're seeing | freshness named; stale page reds the tip | The freshness line (newest landed-piece sha + state fingerprint, both model-derived so the compare converges); the trio byte-compare in the existing CI step. Measured by: F11–F14 + the both-ways demonstration. |

## Out of scope, named (composer key on the frame)

Live refresh / watch mode · any server · any control that mutates ·
replacing the SVG or terminal surfaces. Each returns only through its
own frame.
