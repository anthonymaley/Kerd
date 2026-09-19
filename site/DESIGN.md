# The Kerd look

One page. Everything the site, the pictures and any later page needs in order to
match `site/index.html` without asking. The single source is `site/assets/kerd.css`;
this page explains what is in it and why.

The idea in one line: Kerd is a made thing, so the design is drawn rather than
decorated. One hue, one grid, one family, one curve.

## The wordmark

`site/assets/wordmark.svg`. The four letters are built from two parts and nothing
else: one stroke of constant width, and one circle. The bowl of the **e** and the
bowl of the **d** are the same circle at the same size; the **r** shoulder is a
quarter of it; the **K** is the stroke alone. Kerd is *ceird*, skill — a mark drawn
with a compass and a rule says that better than a symbol would.

- Draw it in `currentColor` when it sits in a page, so it follows the theme. The
  standalone file carries its own light and dark colours.
- Smallest size: 70px wide. Below that the counters close up.
- Never stretch it, never outline it, never put it in a box, never set "Kerd" in
  live text and call it the wordmark.
- The tab icon is the same two parts on their own — the circle and the stroke — as an
  inline data URI in the page head. Copy that line from `index.html`; do not draw a
  new one.

## Colour

One hue — a deep spruce — at six values, plus one accent. That is the whole palette.

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--paper` | `#EDF0EE` | `#0B1310` | the page |
| `--surface` | `#F7F9F7` | `#121B17` | picture frames, code blocks |
| `--ink` | `#0B1512` | `#E5EBE7` | all text that carries meaning |
| `--ink-soft` | `#4E5D58` | `#93A29B` | captions, small print, table right column |
| `--rule` | `#D5DCD7` | `#223029` | every hairline and border |
| `--grid-line` | `#DFE5E0` | `#1B2823` | the drawing grid inside an empty frame |
| `--accent` | `#0B5E4A` | `#5CC5A3` | links, the one button, the skill line |

Dark comes from `prefers-color-scheme`. `data-theme="dark"` or `"light"` on `<html>`
forces one, which is how you check a page without changing your machine.

The accent appears at most three times on a screen. It is never a background fill
behind text except on the one button.

## Type

`-apple-system, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Inter, system-ui,
"Segoe UI", Roboto, sans-serif`. No web font: the page has nothing to wait for, and
on the machines Kerd runs on the system face is the better-drawn one. Weight does the
work that a second family would do — 600 for anything that states something, 400 for
everything else.

| Token | Size | Line | Tracking | Role |
|---|---|---|---|---|
| `--t-1` | 40 → 84px | 1.02 | −0.035em | the one sentence a page opens with |
| `--t-2` | 33 → 54px | 1.08 | −0.026em | a section's statement |
| `--t-3` | 24 → 32px | 1.16 | −0.02em | a title inside a section |
| `--t-lead` | 19 → 23px | 1.45 | −0.012em | the paragraph under an opening sentence |
| `--t-body` | 17px | 1.62 | — | body |
| `--t-small` | 15px | — | — | captions, small print, navigation |
| `--t-micro` | 13px | — | — | last resort |

Measure: body stays under 34rem, a lead under 30rem. Headings take a full stop,
because they are sentences. Sentence case everywhere.

## Grid

12 columns, gutter `clamp(16px, 2.2vw, 32px)`, page margin `clamp(20px, 5vw, 72px)`,
content capped at 1280px. `.wrap` sets the margins, `.grid` sets the columns.

One rule governs every section, and it never flips:

```
| 1  2  3  4  5 | 6 | 7  8  9  10 11 12 |
|  what you say |   |  what proves it   |
```

`.col-say` / `.piece__say` is columns 1–5. `.col-show` / `.piece__show` is 7–12.
Column 6 is the seam, and it stays empty. Alternating left and right down a page is
the thing that makes a page feel like a template; holding still is what makes it feel
made. Under 900px everything becomes one column in source order.

Vertical rhythm: `.band` sections, `padding-block: clamp(72px, 10vw, 152px)`, with a
single hairline between consecutive bands. Spacing steps are `--s1`…`--s10`
(4, 8, 12, 16, 24, 32, 48, 64, 96, 144).

## Pictures

Every picture lives at `docs/pictures/<name>.svg` and a page points at it from a
frame:

```html
<figure class="piece__show">
  <div class="frame"><img src="../docs/pictures/rehearsal.svg" alt="What the picture shows."></div>
  <figcaption class="caption">One line saying what the picture shows.</figcaption>
</figure>
```

The frame draws itself: a hairline border, a faint 40px drawing grid, and the picture
laid over it as an `<img>` with alt text. Until a picture exists, leave the frame empty
(`<div class="frame"></div>`): an empty drawing area, never a broken image. *(Changed
2026-09-19: the first version carried the path in a `--pic` custom property, which
Chrome resolves against the stylesheet, not the page, so no picture ever appeared.)* `.frame` is
16:9; `.frame--wide` is 2.5:1 and is for a picture that reads left to right across a
whole day.

Rules for the pictures themselves:

1. Draw on the same 40px module as the frame grid, with hairlines of the same weight
   as `--rule`.
2. Use only the seven tokens above. Accent exactly one thing per picture — the thing
   the picture is about.
3. Carry both themes inside the file. A picture is loaded as an image, so it cannot
   inherit the page's colours; put a `<style>` block in the SVG with the light values
   and a `@media (prefers-color-scheme: dark)` block with the dark ones, as
   `wordmark.svg` does.
4. Set type in the picture in the same stack, sentence case, never below 13px at the
   size it will be seen.
5. Give the SVG no background fill. The frame supplies `--surface` beneath it.
6. Fit the picture to 16:9 unless it is the day-long one, which is 2.5:1.

## A page, put together

```html
<header class="masthead"><div class="wrap masthead__inner"> wordmark + nav </div></header>
<main>
  <section class="wrap grid band">
    <div class="col-say"><h2 class="statement">One idea.</h2></div>
    <div class="col-show"> what proves it </div>
  </section>
</main>
<footer class="wrap grid colophon"> … </footer>
```

Classes that already exist, so nothing needs inventing: `display`, `statement`,
`title`, `lead`, `prose`, `soft`, `small`, `micro`, `band`, `frame`, `caption`,
`button`, `link-plain`, `does` / `does__row`, `steps` / `step`, `colophon`.

## Three things never to do

1. **Never add a colour.** No second accent, no gradient, no coloured word inside a
   heading, no red or green status tint. If something needs to stand apart, give it
   air or a hairline, not a hue.
2. **Never mirror the grid.** The statement is always on the left, what proves it is
   always on the right, on every page and every section.
3. **Never dress a box.** No drop shadows, no rounded content panels, no capitalised
   labels above headings, no arrows glued to link text. The button's pill is the only
   curve on a page, and it is there because the wordmark is built from a circle.
