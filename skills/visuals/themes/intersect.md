<!-- diagram-design-profile
name: Intersect
slug: intersect
source-url: none
created: 2026-10-15
updated: 2026-10-15
notes: Opt-in Kerd theme, shipped in kerd:visuals. A photocopied engineering schematic: off-white paper, toner ink, one red, capitals. Never a default unless the person makes it one.
-->
# Style Guide

**The single source of truth for colors, typography, and tokens.** Every diagram draws from this — not from hex values inlined in other reference files.

Skin: **the Intersect sheet**. A government engineering drawing photocopied once too often: warm off-white paper with a little grain, warm near-black ink, one hard red used on exactly one thing. Everything is capitals. Shapes carry the meaning, not colour: black pin tags, chevron banners, studded buses, dotted bead links, dashed orbit rings, a barber-pole title frame and blueprint dimension lines. The sheet itself (frame, title block, legend strip, grain) is required on every diagram: see The sheet below. Deliberate rules are listed under Intersect house rules at the end.

---

## Tokens

### Semantic roles

| Role | Purpose | Default (light) | Default (dark) |
|---|---|---|---|
| `paper` | Page background, default node fill | `#ECE9E1` (photocopy bond) | `#14171A` (lightbox off) |
| `paper-2` | Sheet frame fill, secondary fill | `#E3DFD5` | `#1C2024` |
| `ink` | Primary text, primary stroke, pin tags, banners | `#1F1B18` (toner black) | `#E6E2D8` |
| `muted` | Secondary text, default arrow stroke | `#4A443E` | `#A8A296` |
| `soft` | Sublabels, fine-print legends | `#6B645B` | `#8A857B` |
| `rule` | Hairline borders, grid | `#C9C3B6` | `#2C3136` |
| `rule-solid` | Sheet frame border, dimension lines | `#8F887C` | `#5A5F64` |
| `accent` | Exactly one thing per sheet: the focal change's border, else the binder edge | `#C4161C` | `#FF4A3D` |
| `accent-tint` | Fill for accent-bordered boxes | `#ECE9E1` (no tint: same as paper) | `#14171A` |
| `link` | External / interface arrows | `#1F1B18` (no second hue: same as ink) | `#E6E2D8` |

### Inversion rule (light → dark)

Dark is the same sheet on a lightbox: paper and ink swap, the red brightens slightly. Opacities stay the same.

### Series palette (multi-series chart types only)

Charts on an Intersect sheet are ink line plots with a hatched area fill (an ink line plot over a hatched area). Use one series in `ink`; the shipped series palette below is kept for schema completeness and should not normally appear.

| Token | Light | Dark | Notes |
|---|---|---|---|
| `series-1` | `#7c8f6f` (sage) | `#9caf8f` | Non-focal series |
| `series-2` | `#5e7a9b` (dusty-blue) | `#82a0c0` | Non-focal series |
| `series-3` | `#b8915a` (mustard) | `#d3ad7a` | Non-focal series |
| `series-4` | `#9c6b50` (rust-brown) | `#b88670` | Non-focal series |
| `series-5` | `#6e6479` (slate) | `#8d8298` | Non-focal series |

### Terminal skin (opt-in alternate)

Unchanged from the shipped skill; not used by this profile.

| Token | Hex | Purpose |
|---|---|---|
| `terminal-page` | `#0a0a0a` | Page background behind the window |
| `terminal-paper` | `#141414` | Window body, node fill |
| `terminal-bar` | `#1b1b1b` | Titlebar strip |
| `terminal-border` | `#2b2b2b` | Window border, hairlines |
| `terminal-ink` | `#f5f5f5` | Primary text, primary stroke |
| `terminal-muted` | `#9a9a9a` | Secondary text, sublabels, ring stroke |
| `terminal-soft` | `#5c5c5c` | Tertiary — inactive dots, spokes |
| `terminal-accent` | `#ff5a36` | The one accent |
| `terminal-accent-tint` | `rgba(255,90,54,0.12)` | Fill for accent-bordered boxes |

---

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | IBM Plex Mono | 36px | 500, CAPITALS, tracking 0.04em | Sheet title, top right, two or three stacked lines ("INTERSECT / STORAGE / CAPACITY") |
| `node-name` | Open Sans | 16px | 700, CAPITALS, tracking 0.06em | Panel and cluster names ("EPPROM CLUSTER", "DISPLAY MATRIX") |
| `sublabel` | IBM Plex Mono | 13px | 400 | Part codes, captions in lower or mixed case, keeping names and codes as written (iPhone, plan A, TV); texture-only fine print (legend lists, sheet codes) may drop to 12px |
| `eyebrow` | IBM Plex Mono | 13px | 600, CAPITALS, tracking 0.12em | Pin-tag numbers, type tags, dimension figures |
| `arrow-label` | IBM Plex Mono | 13px | 500, CAPITALS | Labels on buses and links |
| `callout` | Open Sans | 20px | 700, CAPITALS | An optional subtitle line inside the barber-pole title frame, under the title |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Open+Sans:wght@700&display=swap" rel="stylesheet">
```

```css
/* titles, fine print, tags, labels: */
font-family: "IBM Plex Mono", "Letter Gothic Std", ui-monospace, Menlo, monospace;
/* panel names and the subtitle: */
font-family: "Open Sans", "Gill Sans", "Helvetica Neue", sans-serif;
```

**Load-bearing rule:** two families. The monospace is the engineer's typewriter (titles and every technical mark); the bold sans is the stencil on the panel. Never a serif.

---

## Stroke, radius, spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `1` | Fine print boxes, grid, dimension lines |
| `stroke-default` | `1.5` | Node outlines, links |
| `stroke-strong` | `2` | Sheet frame, core circle, panel outlines |
| `radius-sm` | `0` | Pin tags (pentagon, not rounded) |
| `radius-md` | `4` | Panel boxes |
| `radius-lg` | `12` | Rack/cabinet housings only |
| `grid` | `4` | Every coord, size, and gap is divisible by 4 (hard rule) |

---

## Node type → treatment

| Type | Fill | Stroke |
|---|---|---|
| `focal` (exactly one) | `paper` | `ink` stroke 2, wrapped in a dashed `ink` orbit ring (dash `6,6`); the barber-pole frame belongs to the title block, never the focal node |
| `backend` | `paper` | `ink` |
| `store` | `paper-2` | `muted` |
| `external` | `paper` | `rule-solid` |
| `input` | `paper` | `soft` |
| `optional` | `paper` | `muted` dashed `4,4` |
| `security` | `paper` | `ink` dashed `8,4` |

---

## The sheet (required on every Intersect diagram)

Recolouring a normal diagram is not this theme. Every diagram drawn with this guide is a whole **sheet**, and these are hard rules, not options:

1. **One SVG is the page, at full size.** The page body is `paper` with the SVG centred in it, drawn at its viewBox width (one SVG unit to one CSS pixel) and never scaled down; a narrower window scrolls sideways rather than shrinking labels under the 13px floor. Check the rendered text size. No HTML heading, eyebrow, paragraph or legend outside the SVG: the title, the subtitle and the notes go inside the sheet, with an SVG `<title>` and `<desc>` that explain the subject.
2. **Sheet frame:** a `rule-solid` stroke-2 rectangle inset 24 from the SVG edge. Everything else sits inside it.
3. **Title block, in the barber-pole frame:** at the top of the title column, inside the barber-pole frame (the sheet's one striped box, always `ink` stripes): first, as the first line of text in the render, Visuals' project line (`PROJECT: subject · kind · status`, in `eyebrow`, the name in capitals and a colon); then the title in `title` type, CAPITALS, stacked on two or three short lines, in a right-hand column about a quarter of the sheet wide; then one line of `sublabel` fine print ("plan view, sheet 1 of 1"). Notes go under the frame as a short list. A diagram too wide for a column puts the same framed block in the top-right corner of the sheet instead, never as a page heading. The stripes frame the title only; they never mark a next step or a takeaway.
4. **Legend strip:** a `rule` hairline across the bottom of the frame, then `LEGEND` in `eyebrow`, one sample of each primitive used with its meaning in fine print, and the sheet code right-aligned ("SHEET <PROJECT>-<NNNN> · <DATE>").
5. **Grain:** the `feTurbulence` grain rectangle over the whole sheet as the very last element.
6. **Fills:** `paper`, `paper-2` and solid `ink` only. Never `#FFFFFF`, never a tint.
7. **Primitives for what is there:** draw every primitive the content gives a reason for, using the mapping below: numbered or listed items get pin tags, a flow between groups gets the studded bus, groups get housings, the title block gets the barber-pole frame. Never invent structure, numbering or a flow the diagram does not have to fit a primitive in; a small diagram may need only the sheet and one or two.

### Mapping an ordinary diagram onto the sheet

The mapping gives shapes; Visuals' state rules decide their outlines. A housing, box or name for something proposed is dashed `ink` (`8,4`), what exists today is solid `ink`, and the focal change is the solid `accent` border. The frame, the title column, the legend strip and the grain are sheet furniture: they never carry a state.

| Part of the diagram | Draw it as |
|---|---|
| A numbered step, item or member | A box or name with a **pin tag** carrying its two-digit number; the name in `node-name`, its detail in lower-case `sublabel` under it |
| The main flow or sequence between groups | A **studded bus** from the item the relationship actually leaves to the item it actually reaches (in a plain sequence of groups, the last item of one and the first of the next): out from under its source, along the gap between the groups, and down into its target, with rounded bends (radius 16) and a large solid arrowhead. Never a short straight drop between housings, and never moved to a different endpoint for the look |
| A short hop inside a group | An `ink` 1.5 line with a small solid arrowhead |
| A secondary link, a check, "then", "depends on" | A **bead link** |
| A group, row, lane or stage | A `paper` housing (radius 12, stroke 2, outline by its state) with its name as rotated `node-name` text on a narrow side panel (56 wide) at its left edge |
| The one interface, exit or outcome leaving the sheet | A **chevron banner** |
| The project and title | The **barber-pole frame** around the title block (above) |
| The point the reader should take away | A short note under the title frame, in fine print; never a second striped box |
| A size, a count, an extent | A **dimension line** beside what it measures |
| The recommended or changed thing | Visuals' focal treatment: solid `accent` border at 2.5; then nothing else is red and there is no binder edge |
| A diagram with no focal change | The **binder edge** spends the red |

### Sheet skeleton (copy, then draw inside the frame)

```html
<style>
:root{--paper:#ECE9E1;--paper-2:#E3DFD5;--ink:#1F1B18;--muted:#4A443E;--soft:#6B645B;--rule:#C9C3B6;--rule-solid:#8F887C;--accent:#C4161C}
@media (prefers-color-scheme: dark){:root{--paper:#14171A;--paper-2:#1C2024;--ink:#E6E2D8;--muted:#A8A296;--soft:#8A857B;--rule:#2C3136;--rule-solid:#5A5F64;--accent:#FF4A3D}}
body{margin:0;background:var(--paper);overflow-x:auto;padding:24px}
svg{display:block;width:1440px;height:auto;margin:0 auto}
.title{font:500 36px "IBM Plex Mono",monospace;letter-spacing:.04em;fill:var(--ink)}
.name{font:700 16px "Open Sans",sans-serif;letter-spacing:.06em;fill:var(--ink)}
.fine{font:400 13px "IBM Plex Mono",monospace;fill:var(--soft)}
.tagn{font:600 13px "IBM Plex Mono",monospace;fill:var(--paper);text-anchor:middle}
.eyebrow{font:600 13px "IBM Plex Mono",monospace;letter-spacing:.12em;fill:var(--muted)}
</style>
<svg viewBox="0 0 1440 900" role="img" aria-labelledby="sheet-title sheet-desc" xmlns="http://www.w3.org/2000/svg">
<title id="sheet-title">PROJECT: subject</title>
<desc id="sheet-desc">What the diagram shows, in one or two sentences.</desc>
<defs>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 0.07"/></feComponentTransfer></filter>
<pattern id="pole" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="12" fill="var(--paper)"/><rect width="6" height="12" fill="var(--ink)"/></pattern>
</defs>
<rect width="1440" height="900" fill="var(--paper)"/>
<rect x="24" y="24" width="1392" height="852" fill="none" stroke="var(--rule-solid)" stroke-width="2"/>
<rect x="1040" y="48" width="336" height="224" fill="url(#pole)"/>
<rect x="1052" y="60" width="312" height="200" fill="var(--paper)"/>
<text x="1072" y="92" class="eyebrow">PROJECT: subject ·</text>
<text x="1072" y="112" class="eyebrow">kind · status</text>
<text x="1072" y="160" class="title">FIRST LINE</text>
<text x="1072" y="204" class="title">SECOND LINE</text>
<text x="1072" y="240" class="fine">plan view, sheet 1 of 1</text>
<!-- the drawing goes in x 48 to 1020, the title column in x 1040 to 1376 -->
<!-- legend strip -->
<line x1="48" y1="812" x2="1376" y2="812" stroke="var(--rule)" stroke-width="1"/>
<text x="48" y="848" class="eyebrow">LEGEND</text>
<text x="1376" y="848" class="fine" text-anchor="end">SHEET XX-0001 · YYYY-MM-DD</text>
<rect width="1440" height="900" filter="url(#grain)" pointer-events="none"/>
</svg>
```

Size the viewBox to the content and set the SVG width to the viewBox width (keep the 24 inset and every coordinate on the 4 grid); keep the title column unless the drawing needs the full width.

A pin tag: `<polygon points="800,230 808,220 840,220 840,240 808,240" fill="var(--ink)"/><text x="824" y="235" class="tagn">01</text>`. The binder edge, only when there is no focal change: `<rect x="1396" y="24" width="20" height="852" fill="var(--accent)"/>`.

### Before delivering, check the sheet

Frame present; the project line first and the title inside the barber-pole frame, not above the sheet; no other striped box; every line in the frame fits inside its paper box at its stated size (wrap a long project line or title onto another line; never shrink it or drop part of it); the bus between groups takes the long route between its real endpoints; SVG title and description present; drawn at full size, labels at 13px or more as rendered; legend strip and sheet code present; grain is the last element; no `#FFFFFF` or tinted fill anywhere; every part the mapping covers drawn as its primitive, nothing invented; outlines follow Visuals' states; names and codes keep their case; exactly one red thing. A sheet that fails any of these is redrawn, not delivered.

## Intersect primitives

These are what make a sheet read as the Intersect. The sheet is always present (above); draw each primitive the content gives a reason for, never all of them for their own sake.

- **Pin tag.** A solid `ink` pentagon (rectangle with a pointed end, 36×20, point 8 wide) with a `paper`-coloured two-digit number in `eyebrow` (so it inverts correctly in dark) ("01"–"07"), attached by a 1.5 stroke to a panel. Stack them 28 apart down one side of a cluster box; the cluster name runs vertically beside them only as rotated text on a side panel, never `writing-mode`.
- **Chevron banner.** A solid `ink` bar 44 high with a pointed right end, text in `paper`, `node-name` at 20px. Marks an interface or the direction work leaves the sheet. At most one per sheet.
- **Studded bus.** The main flow: an `ink` path 12 wide with a `paper` path 4 wide on top, dashed `4,8`, so it reads as a toothed conduit. Between groups it takes the long route between its real endpoints (out from under its source, along the gap, down into its target, rounded bends), never a short stub. Ends in a large solid arrowhead. One or two per sheet.
- **Bead link.** Secondary connection: round-capped dots, `ink` stroke 4, dash `0.1,12`, `stroke-linecap: round`.
- **Orbit ring.** Dashed `ink` circle (dash `6,6`) 24 outside the core circle; a short beaded spine may drop from the core.
- **Diamond junction.** A 20×20 `ink` square rotated 45°, where links meet.
- **Barber-pole frame.** The title block's frame, one per sheet: a 12-wide border filled with a 45° stripe pattern of `ink` and `paper`, around a `paper` box holding the project line and the title. Always `ink` stripes, never `accent`; never used for a next step or a takeaway.
- **Dimension line.** A `rule-solid` line with tick marks every 24 and end bars, a figure in `eyebrow` at its middle; frames a panel like a blueprint.
- **Sheet frame.** A `rule-solid` 2 border inset 24 from the edge, with the sheet code and date at the right end of the legend strip ("CLASSIFIED" is not used). Required: see The sheet.
- **Binder edge.** The `accent` may appear as a 16-wide red bar down one side of the sheet. When it does, nothing else is red.

---

## Intersect house rules

- **One red thing.** `accent` marks exactly one element. When the sheet shows a change (a Kerd proposal, a before → after), that element is the focal change: `paper` fill, solid `accent` border at stroke 2.5, heavier than the rest. Only a sheet with no focal change may spend the red, on the binder edge. Never two.
- **Capitals everywhere** except fine print (part legends, plan-view captions), which stays lower or mixed case like the originals; never lower-case a name or code (iPhone, plan A, TV stay as written). Titles, names and banners are full capitals, names included (IPAD, not iPAD).
- **Shapes, not colours.** Distinguish kinds by pin tags, banners, dashing and hatching. No fills other than `paper`, `paper-2` and solid `ink`.
- **Grain, lightly.** Every sheet carries a faint photocopy grain (`feTurbulence`, alpha ~7%) laid over everything as the last element, so label masks never show as patches against it.
- **Orthogonal connectors.** The shipped connector rules hold, except that the studded bus may sweep in a single large arc (radius ≥ 48) around a core, as the originals do.
- **13px floor at reading size** for every label a reader needs: names, tags, arrow labels, captions. Only texture-only fine print (legend lists, sheet codes) may drop to 12px, and nothing a reader needs may live only there.
- **States stay distinct inside Kerd's Visuals.** What exists today: solid `ink` outline. What is proposed: dashed `ink` outline (`8,4`). The change the view is about: solid `accent` border, heavier, no tinted fill. This theme overrides only the look (paper, ink, type, capitals and the primitives above); it never overrides Visuals' rules for states, the focal change or the project leading the top heading.
- **Carry both themes** with a `@media (prefers-color-scheme: dark)` block.
