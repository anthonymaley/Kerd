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

Skin: **the Intersect sheet**. A government engineering drawing photocopied once too often: warm off-white paper with a little grain, warm near-black ink, one hard red used on exactly one thing. Everything is capitals. Shapes carry the meaning, not colour: black pin tags, chevron banners, studded buses, dotted bead links, dashed orbit rings, barber-pole callouts and blueprint dimension lines. Deliberate rules are listed under Intersect house rules at the end.

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
| `sublabel` | IBM Plex Mono | 13px | 400 | Part codes, captions in lower case; texture-only fine print (legend lists, sheet codes) may drop to 12px |
| `eyebrow` | IBM Plex Mono | 13px | 600, CAPITALS, tracking 0.12em | Pin-tag numbers, type tags, dimension figures |
| `arrow-label` | IBM Plex Mono | 13px | 500, CAPITALS | Labels on buses and links |
| `callout` | Open Sans | 20px | 700, CAPITALS | The one barber-pole callout ("SINGLE MULTI-PLEXER / FOR INTERSECT CORE") |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Open+Sans:wght@700&display=swap" rel="stylesheet">
```

```css
/* titles, fine print, tags, labels: */
font-family: "IBM Plex Mono", "Letter Gothic Std", ui-monospace, Menlo, monospace;
/* panel names and the callout: */
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
| `focal` (exactly one) | `paper` | `ink` stroke 2, wrapped in a dashed `ink` orbit ring (dash `6,6`), or a barber-pole `accent` frame for a callout |
| `backend` | `paper` | `ink` |
| `store` | `paper-2` | `muted` |
| `external` | `paper` | `rule-solid` |
| `input` | `paper` | `soft` |
| `optional` | `paper` | `muted` dashed `4,4` |
| `security` | `paper` | `ink` dashed `8,4` |

---

## Intersect primitives

These are what make a sheet read as the Intersect. Use three to five on any one sheet, never all of them.

- **Pin tag.** A solid `ink` pentagon (rectangle with a pointed end, 36×20, point 8 wide) with a `paper`-coloured two-digit number in `eyebrow` (so it inverts correctly in dark) ("01"–"07"), attached by a 1.5 stroke to a panel. Stack them 28 apart down one side of a cluster box; the cluster name runs vertically beside them only as rotated text on a side panel, never `writing-mode`.
- **Chevron banner.** A solid `ink` bar 44 high with a pointed right end, text in `paper`, `node-name` at 20px. Marks an interface or the direction work leaves the sheet. At most one per sheet.
- **Studded bus.** The main flow: an `ink` path 12 wide with a `paper` path 4 wide on top, dashed `4,8`, so it reads as a toothed conduit. Ends in a large solid arrowhead. One or two per sheet.
- **Bead link.** Secondary connection: round-capped dots, `ink` stroke 4, dash `0.1,12`, `stroke-linecap: round`.
- **Orbit ring.** Dashed `ink` circle (dash `6,6`) 24 outside the core circle; a short beaded spine may drop from the core.
- **Diamond junction.** A 20×20 `ink` square rotated 45°, where links meet.
- **Barber-pole frame.** The one callout: a 12-wide border filled with a 45° stripe pattern of `ink` and `paper`, around a `paper` box with the callout text. It may use `accent` stripes instead of `ink` when it is the sheet's focal thing.
- **Dimension line.** A `rule-solid` line with tick marks every 24 and end bars, a figure in `eyebrow` at its middle; frames a panel like a blueprint.
- **Sheet frame.** A `rule-solid` 2 border inset 24 from the edge, with a title block of fine print in the bottom-right corner (sheet code, date, "CLASSIFIED" is not used).
- **Binder edge.** The `accent` may appear as a 16-wide red bar down one side of the sheet. When it does, nothing else is red.

---

## Intersect house rules

- **One red thing.** `accent` marks exactly one element. When the sheet shows a change (a Kerd proposal, a before → after), that element is the focal change: `paper` fill, solid `accent` border at stroke 2.5, heavier than the rest. Only a sheet with no focal change may spend the red on the binder edge or the callout's stripes. Never two.
- **Capitals everywhere** except fine print (part legends, plan-view captions), which stays lower or mixed case like the originals.
- **Shapes, not colours.** Distinguish kinds by pin tags, banners, dashing and hatching. No fills other than `paper`, `paper-2` and solid `ink`.
- **Grain, lightly.** The sheet may carry a faint photocopy grain (`feTurbulence`, alpha ~7%) laid over everything as the last element, so label masks never show as patches against it.
- **Orthogonal connectors.** The shipped connector rules hold, except that the studded bus may sweep in a single large arc (radius ≥ 48) around a core, as the originals do.
- **13px floor at reading size** for every label a reader needs: names, tags, arrow labels, captions. Only texture-only fine print (legend lists, sheet codes) may drop to 12px, and nothing a reader needs may live only there.
- **States stay distinct inside Kerd's Visuals.** What exists today: solid `ink` outline. What is proposed: dashed `ink` outline (`8,4`). The change the view is about: solid `accent` border, heavier, no tinted fill. This theme overrides only the look (paper, ink, type, capitals and the primitives above); it never overrides Visuals' rules for states, the focal change or the project leading the top heading.
- **Carry both themes** with a `@media (prefers-color-scheme: dark)` block.
