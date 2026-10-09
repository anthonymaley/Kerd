// overtone's plan view, drawn: pure builders, no `$`, no state, nothing
// mutable at module level. usage.tsx lays these out with Raster (terminal)
// or plain Text (every other surface, or a terminal without Raster).
//
// Raster cells are half-block pixels in true colour: each cell holds two
// vertical pixels as ▀ / ▄ / █ (code point, foreground, background), packed
// as little-endian u32 triplets in base64. The shapes follow the settled
// prototype (raster-proto-register.tsx in the overtone-savvy work folder).

import type { PlanRow, PlanRowState, PlanView } from './plan-logic'
import { compareModels, shownText } from './logic'
import { prettyModel } from './usage-logic'

// ---------------------------------------------------------------------------
// Colours
// ---------------------------------------------------------------------------

export const HEX = {
  done: '#5CC5A3',
  running: '#E3B341',
  returned: '#E3B341',
  needs: '#D64545',
  failed: '#D64545',
  todo: '#3A4A43',
  track: '#1C2622',
} as const

const hex = (s: string): number => parseInt(s.slice(1), 16)
const GREEN = hex(HEX.done)
const YELLOW = hex(HEX.running)
const RED = hex(HEX.needs)
const GREY = hex(HEX.todo)
const TRACK = hex(HEX.track)

// The terminal's own colour (bit 24 alone).
const DEF = 0x01000000

export const stateHex = (s: PlanRowState): string => HEX[s]
const stateRgb = (s: PlanRowState): number => hex(HEX[s])

export const blend = (a: number, b: number, t: number): number => {
  const ch = (sh: number) => Math.round(((a >> sh) & 255) * (1 - t) + ((b >> sh) & 255) * t)
  return (ch(16) << 16) | (ch(8) << 8) | ch(0)
}

// ---------------------------------------------------------------------------
// Cells
// ---------------------------------------------------------------------------

// A pixel: a 0xRRGGBB colour, or null for none (the terminal's default shows).
export type Px = number | null

const B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

export function toB64(bytes: Uint8Array): string {
  let out = ''
  for (let i = 0; i < bytes.length; i += 3) {
    const a = bytes[i] ?? 0
    const b = bytes[i + 1] ?? 0
    const c = bytes[i + 2] ?? 0
    const n = (a << 16) | (b << 8) | c
    out += B64[(n >> 18) & 63]! + B64[(n >> 12) & 63]!
    out += i + 1 < bytes.length ? B64[(n >> 6) & 63]! : '='
    out += i + 2 < bytes.length ? B64[n & 63]! : '='
  }
  return out
}

// `px` rows of pixels (two per cell row) packed as Raster's `cells`: `cols`
// by `rows` cells, row-major, [code point, foreground, background] each.
export function cells(px: Px[][], cols: number, rows: number): string {
  const words = new Uint32Array(cols * rows * 3)
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const top = px[r * 2]?.[c] ?? null
      const bot = px[r * 2 + 1]?.[c] ?? null
      let ch = 0x20
      let fg = DEF
      let bg = DEF
      if (top !== null && top === bot) [ch, fg] = [0x2588, top]
      else if (top !== null && bot !== null) [ch, fg, bg] = [0x2580, top, bot]
      else if (top !== null) [ch, fg] = [0x2580, top]
      else if (bot !== null) [ch, fg] = [0x2584, bot]
      const i = (r * cols + c) * 3
      words[i] = ch
      words[i + 1] = fg
      words[i + 2] = bg
    }
  }
  // Little-endian whatever the host: write the bytes by hand.
  const bytes = new Uint8Array(words.length * 4)
  words.forEach((w, i) => {
    bytes[i * 4] = w & 255
    bytes[i * 4 + 1] = (w >>> 8) & 255
    bytes[i * 4 + 2] = (w >>> 16) & 255
    bytes[i * 4 + 3] = (w >>> 24) & 255
  })
  return toB64(bytes)
}

// ---------------------------------------------------------------------------
// The segment bar
// ---------------------------------------------------------------------------

// Which state shows when several share one column.
const PRIORITY: Record<PlanRowState, number> = { needs: 4, failed: 4, running: 3, returned: 3, done: 2, todo: 1 }

// `segs` squeezed into at most `n` entries, the most urgent state per bucket.
export function squeeze(segs: readonly PlanRowState[], n: number): PlanRowState[] {
  if (n < 1) return []
  if (segs.length <= n) return [...segs]
  const out: PlanRowState[] = []
  for (let i = 0; i < n; i++) {
    const from = Math.floor((i * segs.length) / n)
    const to = Math.max(from + 1, Math.floor(((i + 1) * segs.length) / n))
    let pick = segs[from]!
    for (let k = from + 1; k < to; k++) if (PRIORITY[segs[k]!] > PRIORITY[pick]) pick = segs[k]!
    out.push(pick)
  }
  return out
}

// The pixel rows (both the same) of a `cols`-column bar of segments, each
// as wide as `cols` allows with one empty column between neighbours (the
// gap is dropped when the bar is too narrow for one per segment). A running
// segment is yellow, needs/failed red, done green, todo grey, returned yellow
// and steady; the last column of a running or needs/failed segment flashes on
// odd frames.
export function barPixels(cols: number, segs: readonly PlanRowState[], frame: number): Px[][] {
  const w = Math.max(0, Math.floor(cols))
  const list = squeeze(segs, w)
  const n = list.length
  const gaps = n > 1 && w >= 2 * n // each segment keeps a block and a gap
  const row: Px[] = []
  for (let x = 0; x < w; x++) {
    if (n === 0) {
      row.push(TRACK)
      continue
    }
    const i = Math.min(n - 1, Math.floor((x * n) / w))
    const last = Math.ceil(((i + 1) * w) / n) - 1
    const st = list[i]!
    const gap = gaps && i < n - 1
    if (gap && x === last) {
      row.push(null)
      continue
    }
    const flash = x === last - (gap ? 1 : 0) && frame % 2 === 1
    if (st === 'todo') row.push(GREY)
    else if (st === 'done') row.push(GREEN)
    else row.push(flash && st !== 'returned' ? blend(stateRgb(st), TRACK, 0.7) : stateRgb(st))
  }
  return [row, [...row]]
}

export const barCells = (cols: number, segs: readonly PlanRowState[], frame: number): string =>
  cells(barPixels(cols, segs, frame), Math.max(0, Math.floor(cols)), 1)

// A 2×2-pixel square: running, one bright pixel chases round a dim ring;
// needs/failed, all four blink red; done, solid green; returned, solid
// yellow (steady: it waits on acceptance, nothing moves); todo, dim grey.
const RING: [number, number][] = [[0, 0], [1, 0], [1, 1], [0, 1]]

export function squarePixels(state: PlanRowState, frame: number): Px[][] {
  const px: Px[][] = [[null, null], [null, null]]
  RING.forEach(([x, y], i) => {
    let p: number
    if (state === 'running') p = i === frame % 4 ? YELLOW : blend(YELLOW, TRACK, 0.6)
    else if (state === 'needs' || state === 'failed') p = frame % 2 === 1 ? blend(RED, TRACK, 0.6) : RED
    else if (state === 'done') p = GREEN
    else if (state === 'returned') p = YELLOW
    else p = GREY
    px[y]![x] = p
  })
  return px
}

export const squareCells = (state: PlanRowState, frame: number): string => cells(squarePixels(state, frame), 2, 1)

// ---------------------------------------------------------------------------
// Text forms (no Raster)
// ---------------------------------------------------------------------------

export type PSeg = { text: string; color?: string; dim?: boolean; bold?: boolean }

export const GLYPH: Record<PlanRowState, string> = { running: '●', returned: '◉', done: '✓', needs: '◆', failed: '◆', todo: '◷' }

export const glyphSeg = (s: PlanRowState): PSeg => ({ text: GLYPH[s], color: HEX[s] })

// █ in the state's colour for work begun or done, ░ in grey for what is to
// come; `cols` characters wide (padded with spaces).
export function textBar(cols: number, segs: readonly PlanRowState[], pad = true): PSeg[] {
  const w = Math.max(0, Math.floor(cols))
  const list = segs.length === 1 ? Array<PlanRowState>(w).fill(segs[0]!) : squeeze(segs, w)
  const out: PSeg[] = list.map(s => (s === 'todo' ? { text: '░', color: HEX.todo } : { text: '█', color: HEX[s] }))
  if (pad && list.length < w) out.push({ text: ' '.repeat(w - list.length) })
  return out
}

// ---------------------------------------------------------------------------
// The collapsed band's plan group
// ---------------------------------------------------------------------------

export const BAND_BAR_MAX = 28
export const BAND_BAR_MIN = 6
// The plan tool's title before the bar, cut to this many columns.
export const BAND_TITLE_MAX = 20
// `  │  ` before the group, a space after the label, a space before the count.
const BAND_FIXED = 5 + 1 + 1

export type PlanBand = {
  // Columns the whole group takes, separator included.
  width: number
  // Before the bar: the plan's title, short, or `plan`.
  label: string
  count: string
  bar: { cols: number; cells?: string; text?: PSeg[] }
}

export const taskStates = (v: PlanView): PlanRowState[] => v.rows.filter(r => r.kind === 'task').map(r => r.state)

// The title in at most BAND_TITLE_MAX columns, `plan` without one.
export function bandLabel(title: string | undefined): string {
  const t = (title ?? '').replace(/\s+/g, ' ').trim()
  if (t === '') return 'plan'
  return t.length <= BAND_TITLE_MAX ? t : `${t.slice(0, BAND_TITLE_MAX - 1).trimEnd()}…`
}

// The plan bar and its "N of M" in at most `room` columns, or undefined when
// there is no plan or no room (the bar shrinks first, a title gives way to
// `plan`, then the group goes).
export function planBand(v: PlanView, room: number, raster: boolean, frame: number): PlanBand | undefined {
  if (v.total <= 0) return undefined
  const segs = taskStates(v)
  if (segs.length === 0) return undefined
  const count = `${v.accepted} of ${v.total}`
  const titled = bandLabel(v.title)
  for (const label of titled === 'plan' ? ['plan'] : [titled, 'plan']) {
    const fixed = BAND_FIXED + label.length + count.length
    const avail = Math.floor(room) - fixed
    if (raster) {
      const cols = Math.min(BAND_BAR_MAX, segs.length * 4, avail)
      // A plan of one task (4 columns) is shown too; the minimum is for longer ones.
      if (cols < Math.min(BAND_BAR_MIN, segs.length * 4)) continue
      return { width: fixed + cols, label, count, bar: { cols, cells: barCells(cols, segs, frame) } }
    }
    const cols = Math.min(BAND_BAR_MAX, segs.length)
    if (avail < Math.min(cols, BAND_BAR_MIN)) continue
    const w = Math.min(cols, avail)
    return { width: fixed + w, label, count, bar: { cols: w, text: textBar(w, segs, false) } }
  }
  return undefined
}

// ---------------------------------------------------------------------------
// The expanded card
// ---------------------------------------------------------------------------

export type PlanLayout = {
  // The mark: 2 columns for a Raster square, 1 for a glyph.
  mark: number
  name: number
  bar: number
  // 0: column dropped.
  model: number
  effort: number
  // 0: no detail column.
  detail: number
}

const MIN_DETAIL = 10

const widthOf = (mark: number, name: number, bar: number, model: number, effort: number, detail: number): number => {
  const cols = [mark, name, bar, model, effort, detail].filter(c => c > 0)
  return cols.reduce((a, b) => a + b, 0) + Math.max(0, cols.length - 1)
}

// Columns for `inner` terminal columns: the full set (name 28, bar 24,
// model 12, effort 8, detail takes the rest) when it fits; otherwise the
// name and the bar shrink, then effort and model go, then the detail.
export function planLayout(inner: number, raster: boolean): PlanLayout {
  const mark = raster ? 2 : 1
  const room = Number.isFinite(inner) ? Math.floor(inner) : 200
  const tries: [number, number, number, number][] = [
    [28, 24, 12, 8],
    [20, 24, 12, 8],
    [20, 16, 12, 8],
    [14, 16, 12, 8],
    [14, 12, 12, 0],
    [14, 12, 0, 0],
  ]
  for (const [name, bar, model, effort] of tries) {
    const detail = room - widthOf(mark, name, bar, model, effort, 1) + 1
    if (detail >= MIN_DETAIL) return { mark, name, bar, model, effort, detail }
  }
  // No room for a detail: what is left goes to the name, then the bar.
  const bar = Math.max(4, Math.min(12, room - mark - 12 - 2))
  const name = Math.max(6, Math.min(28, room - mark - bar - 2))
  return { mark, name, bar, model: 0, effort: 0, detail: 0 }
}

const clip = (text: string, max: number): string => {
  const t = text.replace(/\s+/g, ' ').trim()
  const chars = [...t]
  return chars.length <= max ? t : `${chars.slice(0, Math.max(1, max - 1)).join('')}…`
}

// `text` cut to `width - 1` (with …) and padded to `width`; no gap column left
// when the cut leaves none.
export function fit(text: string, width: number): string {
  if (width <= 0) return ''
  const t = clip(text, width)
  const n = [...t].length
  return n >= width ? t : t + ' '.repeat(width - n)
}

export type CardRow = {
  key: string
  state: PlanRowState
  // Raster square cells, or (no Raster) the glyph.
  mark: { cells?: string; glyph?: PSeg }
  // Padded to the layout's name width.
  name: string
  bar: { cols: number; cells?: string; text?: PSeg[] }
  model?: PSeg
  effort?: PSeg
  detail?: PSeg
}

// The row's bar segments: one per reported step, or, past `max` (the bar's
// columns), `max` buckets of steps each. Never more than `max` entries
// whatever total a step report carries.
export function rowSegs(row: PlanRow, max = 50): PlanRowState[] {
  const s = row.steps
  const cap = Math.max(1, Math.floor(max))
  if (s && s.total > 0 && Number.isFinite(s.total)) {
    const total = Math.floor(s.total)
    const n = Math.min(total, cap)
    if (row.state === 'done' || row.state === 'returned') return Array<PlanRowState>(n).fill(row.state)
    if (row.state === 'running' || row.state === 'needs' || row.state === 'failed') {
      const done = Math.max(0, Math.min(s.done, total))
      // bucket i covers steps [lo, hi): done when all of them are, the row's
      // state when the step under way falls in it, else to come
      return Array.from({ length: n }, (_, i): PlanRowState => {
        const lo = Math.floor((i * total) / n)
        const hi = Math.floor(((i + 1) * total) / n)
        return hi <= done ? 'done' : lo <= done && done < hi ? row.state : 'todo'
      })
    }
  }
  return [row.state]
}

function modelCol(row: PlanRow, width: number): PSeg | undefined {
  if (width <= 0) return undefined
  const w = row.worker
  if (!w) return { text: fit('', width) }
  const shown = w.seen ?? w.model ?? w.asked
  const bad = w.seen !== undefined && w.asked !== undefined && compareModels(w.asked, w.seen) === 'mismatch'
  const seg: PSeg = { text: fit(shown ? prettyModel(shown) : '—', width) }
  if (bad) {
    seg.color = HEX.needs
    seg.bold = true
  } else seg.dim = true
  return seg
}

function effortCol(row: PlanRow, width: number): PSeg | undefined {
  if (width <= 0) return undefined
  const w = row.worker
  if (!w) return { text: fit('', width) }
  // Haiku takes no effort setting: show none, whatever was reported
  const model = w.seen ?? w.model ?? w.asked
  if (model && /haiku/i.test(model)) return { text: fit('—', width), dim: true }
  const shown = w.effort ?? w.askedEffort
  const bad = w.effort !== undefined && w.askedEffort !== undefined && String(w.effort) !== w.askedEffort
  const seg: PSeg = { text: fit(shown === undefined ? '—' : shownText(String(shown)), width) }
  if (bad) {
    seg.color = HEX.needs
    seg.bold = true
  } else seg.dim = true
  return seg
}

function detailOf(row: PlanRow, width: number): PSeg | undefined {
  if (width <= 0) return undefined
  const w = row.worker
  switch (row.state) {
    case 'needs':
      return { text: clip(shownText(w?.blocked?.what ?? '').replace(/^wants to run /, '') || 'asks you', width), color: HEX.needs }
    case 'failed':
      return { text: 'failed', color: HEX.failed }
    case 'done':
      return { text: 'accepted', dim: true }
    case 'todo':
      return { text: 'to come', dim: true }
    case 'returned':
      return { text: clip('returned, awaiting acceptance', width), color: HEX.returned }
    default:
      return { text: clip(shownText(row.steps?.note ?? w?.activity ?? ''), width), dim: true }
  }
}

export function cardRow(row: PlanRow, lay: PlanLayout, raster: boolean, frame: number): CardRow {
  const title = row.n !== undefined ? `${row.n}. ${row.title}` : row.title
  const segs = rowSegs(row, lay.bar)
  const out: CardRow = {
    key: row.key,
    state: row.state,
    mark: raster ? { cells: squareCells(row.state, frame) } : { glyph: glyphSeg(row.state) },
    name: fit(title, lay.name),
    bar: raster
      ? { cols: lay.bar, cells: barCells(lay.bar, segs, frame) }
      : { cols: lay.bar, text: textBar(lay.bar, segs) },
  }
  const model = modelCol(row, lay.model)
  if (model) out.model = model
  const effort = effortCol(row, lay.effort)
  if (effort) out.effort = effort
  const detail = detailOf(row, lay.detail)
  if (detail) out.detail = detail
  return out
}

export type PlanCard = {
  header: string
  layout: PlanLayout
  rows: CardRow[]
  hidden: number
}

const URGENCY: Record<PlanRowState, number> = { needs: 0, failed: 0, running: 1, returned: 1, todo: 2, done: 3 }

// The card for `inner` columns and at most `maxRows` task lines: all of
// them, or (past that) the most urgent in plan order, the rest counted in
// the header.
export function planCard(v: PlanView, inner: number, raster: boolean, frame: number, maxRows = Infinity): PlanCard {
  const layout = planLayout(inner, raster)
  let keep = v.rows.map((_, i) => i)
  if (v.rows.length > maxRows) {
    const n = Math.max(1, Math.floor(maxRows))
    const ranked = keep.slice().sort((a, b) => URGENCY[v.rows[a]!.state] - URGENCY[v.rows[b]!.state] || a - b)
    const chosen = new Set(ranked.slice(0, n))
    keep = keep.filter(i => chosen.has(i))
  }
  const hidden = v.rows.length - keep.length
  return {
    header: `${v.accepted} of ${v.total} accepted${hidden > 0 ? ` · +${hidden} more` : ''}${v.overflow ? ` · ${v.overflow} over the cap not kept` : ''}`,
    layout,
    rows: keep.map(i => cardRow(v.rows[i]!, layout, raster, frame)),
    hidden,
  }
}

// Whether anything on the view moves: a running, needs or failed row (a
// returned one is steady).
export const isAnimating = (v: PlanView): boolean =>
  v.rows.some(r => r.state === 'running' || r.state === 'needs' || r.state === 'failed')
