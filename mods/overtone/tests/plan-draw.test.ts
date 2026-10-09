import { describe, expect, test } from 'claude-code/testing'

import type { OvertoneWorker } from '../types'
import type { PlanRow, PlanView } from '../hooks/plan-logic'
import {
  HEX,
  barCells,
  barPixels,
  cardRow,
  cells,
  fit,
  isAnimating,
  BAND_TITLE_MAX,
  bandLabel,
  planBand,
  planCard,
  planLayout,
  rowSegs,
  squareCells,
  squarePixels,
  squeeze,
  textBar,
} from '../hooks/plan-draw'

const bytes = (b64: string): number[] => [...atob(b64)].map(c => c.charCodeAt(0))
const firstWord = (b64: string): number => {
  const b = bytes(b64)
  return (b[0]! | (b[1]! << 8) | (b[2]! << 16) | (b[3]! << 24)) >>> 0
}
const hex = (s: string): number => parseInt(s.slice(1), 16)
const GREEN = hex(HEX.done)
const YELLOW = hex(HEX.running)
const RED = hex(HEX.needs)
const GREY = hex(HEX.todo)

const worker = (over: Partial<OvertoneWorker> = {}): OvertoneWorker => ({
  id: 'w1',
  label: 'agent w1',
  type: 'agent',
  status: 'running',
  firstSeenMs: 0,
  fromSpawn: true,
  tools: 0,
  pending: {},
  ...over,
})

const row = (over: Partial<PlanRow> & { state: PlanRow['state'] }): PlanRow => ({
  key: 't-1',
  kind: 'task',
  n: 1,
  title: 'Plan state',
  ...over,
})

const view = (rows: PlanRow[], accepted = 0): PlanView => ({ accepted, total: rows.filter(r => r.kind === 'task').length, rows })

describe('cell encoding', () => {
  test('a solid pixel pair is one full block, little-endian u32 triplet', () => {
    expect(cells([[0xff8800], [0xff8800]], 1, 1)).toBe('iCUAAACI/wAAAAAB')
  })
  test('two colours make an upper half block, foreground over background', () => {
    expect(cells([[0x5cc5a3], [0x1c2622]], 1, 1)).toBe('gCUAAKPFXAAiJhwA')
  })
  test('no pixels is a blank cell in the default colours', () => {
    expect(cells([[null], [null]], 1, 1)).toBe('IAAAAAAAAAEAAAAB')
  })
  test('a lower pixel alone is a lower half block', () => {
    const words = firstWord
    expect(words(cells([[null], [GREEN]], 1, 1))).toBe(0x2584)
    expect(words(cells([[GREEN], [null]], 1, 1))).toBe(0x2580)
  })
})

describe('the segment bar', () => {
  test('one empty column between segments, none after the last', () => {
    const px = barPixels(14, ['done', 'running', 'todo', 'todo', 'todo', 'todo', 'todo'], 0)[0]!
    expect(px.length).toBe(14)
    // 7 segments in 14 columns: a block and a gap each
    const gaps = px.map((p, i) => (p === null ? i : -1)).filter(i => i >= 0)
    expect(gaps.length).toBe(6)
    expect(px[13]).not.toBe(null)
  })
  test('both pixel rows match, so the bar is full blocks', () => {
    const [top, bot] = barPixels(24, ['done', 'running', 'todo'], 0)
    expect(top).toEqual(bot)
  })
  test('colours follow the state: green done, yellow running, red needs, grey todo', () => {
    const px = barPixels(8, ['done', 'running', 'needs', 'todo'], 0)[0]!
    expect(px[0]).toBe(GREEN)
    expect(px[2]).toBe(YELLOW)
    expect(px[4]).toBe(RED)
    expect(px[6]).toBe(GREY)
  })
  test('the last column of a running or needs segment flashes on odd frames only', () => {
    const even = barPixels(8, ['running', 'needs'], 0)[0]!
    const odd = barPixels(8, ['running', 'needs'], 1)[0]!
    expect(even.filter(p => p !== null)).not.toEqual(odd.filter(p => p !== null))
    expect(odd.filter(p => p === YELLOW).length).toBe(even.filter(p => p === YELLOW).length - 1)
    expect(odd.filter(p => p === RED).length).toBe(even.filter(p => p === RED).length - 1)
  })
  test('a failed segment is red like needs', () => {
    expect(barPixels(2, ['failed'], 0)[0]).toEqual([RED, RED])
  })
  test('a bar too narrow for gaps runs the segments together', () => {
    const px = barPixels(4, ['done', 'todo', 'done', 'todo', 'done'], 0)[0]!
    expect(px.every(p => p !== null)).toBe(true)
  })
  test('more segments than columns are squeezed, the urgent one kept', () => {
    expect(squeeze(['done', 'done', 'needs', 'todo'], 2)).toEqual(['done', 'needs'])
    expect(squeeze(['done'], 4)).toEqual(['done'])
  })
  test('the encoded bar is columns x 1 cells', () => {
    expect(bytes(barCells(24, ['done', 'todo'], 0)).length).toBe(24 * 12)
  })
})

describe('the square', () => {
  test('running: one bright pixel on a dim ring, moving with the frame', () => {
    const at = (f: number) => squarePixels('running', f).flat().indexOf(YELLOW)
    expect(squarePixels('running', 0).flat().filter(p => p === YELLOW).length).toBe(1)
    expect(at(0)).not.toBe(at(1))
    expect(at(0)).toBe(at(4))
  })
  test('needs blinks red, done is solid green, todo grey', () => {
    expect(squarePixels('needs', 0).flat()).toEqual([RED, RED, RED, RED])
    expect(squarePixels('needs', 1).flat()).not.toEqual([RED, RED, RED, RED])
    expect(squarePixels('done', 3).flat()).toEqual([GREEN, GREEN, GREEN, GREEN])
    expect(squarePixels('todo', 3).flat()).toEqual([GREY, GREY, GREY, GREY])
  })
  test('two cells wide', () => {
    expect(bytes(squareCells('done', 0)).length).toBe(2 * 12)
  })
})

describe('row segments', () => {
  test('steps give one block per step, done then the current one in the row state', () => {
    const r = row({ state: 'running', steps: { done: 2, total: 5, atMs: 0 } })
    expect(rowSegs(r)).toEqual(['done', 'done', 'running', 'todo', 'todo'])
    expect(rowSegs({ ...r, state: 'needs' })).toEqual(['done', 'done', 'needs', 'todo', 'todo'])
  })
  test('no steps is a solid bar in the row state', () => {
    expect(rowSegs(row({ state: 'done' }))).toEqual(['done'])
    expect(rowSegs(row({ state: 'todo' }))).toEqual(['todo'])
    expect(rowSegs(row({ state: 'running' }))).toEqual(['running'])
  })
  test('a huge step total never allocates past the bar: buckets of steps, the step under way in its bucket', () => {
    // review 2026-10-08 item 1: one entry per reported step, unbounded
    const r = row({ state: 'running', steps: { done: 500_000, total: 1_000_000, atMs: 0 } })
    const segs = rowSegs(r, 10)
    expect(segs.length).toBe(10)
    expect(segs).toEqual(['done', 'done', 'done', 'done', 'done', 'running', 'todo', 'todo', 'todo', 'todo'])
    expect(rowSegs(row({ state: 'done', steps: { done: 1, total: 1e9, atMs: 0 } }), 24).length).toBe(24)
    expect(rowSegs(r).length).toBe(50)
    // within the bar, one per step as before
    expect(rowSegs(row({ state: 'running', steps: { done: 2, total: 5, atMs: 0 } }), 24)).toEqual(['done', 'done', 'running', 'todo', 'todo'])
    // the card passes its bar width
    const c = cardRow(r, planLayout(120, true), false, 0)
    expect(c.bar.text!.length).toBeLessThanOrEqual(c.bar.cols)
  })
  test('a done row with steps is all done', () => {
    expect(rowSegs(row({ state: 'done', steps: { done: 1, total: 3, atMs: 0 } }))).toEqual(['done', 'done', 'done'])
  })
})

describe('layout', () => {
  test('wide: name 28, bar 24, model 12, effort 8, detail takes the rest', () => {
    const l = planLayout(120, true)
    expect(l).toMatchObject({ mark: 2, name: 28, bar: 24, model: 12, effort: 8 })
    expect(l.detail).toBe(120 - (2 + 28 + 24 + 12 + 8 + 5))
  })
  test('narrower: the name then the bar shrink, then effort and model go', () => {
    const w = (n: number) => planLayout(n, true)
    expect(w(85).name).toBeLessThan(28)
    expect(w(85).bar).toBe(24)
    expect(w(75).bar).toBeLessThan(24)
    expect(w(60).effort).toBe(0)
    expect(w(60).model).toBe(12)
    expect(w(50).model).toBe(0)
    expect(w(50).detail).toBeGreaterThanOrEqual(10)
  })
  test('the layout never needs more columns than it was given', () => {
    for (let n = 30; n <= 200; n++) {
      const l = planLayout(n, true)
      const cols = [l.mark, l.name, l.bar, l.model, l.effort, l.detail].filter(c => c > 0)
      expect(cols.reduce((a, b) => a + b, 0) + cols.length - 1).toBeLessThanOrEqual(n)
    }
  })
  test('text mode marks are one column', () => {
    expect(planLayout(120, false).mark).toBe(1)
  })
  test('fit pads or cuts to the width', () => {
    expect(fit('abc', 6)).toBe('abc   ')
    expect(fit('abcdefghij', 6)).toBe('abcde…')
    expect(fit('abcdef', 6)).toBe('abcdef')
  })
  test('rows align: name, model and effort are the same width on every row', () => {
    const lay = planLayout(120, true)
    const a = cardRow(row({ state: 'running', title: 'Short', worker: worker({ seen: 'claude-sonnet-5-5', effort: 'medium' }) }), lay, true, 0)
    const b = cardRow(
      row({ key: 't-2', n: 2, state: 'todo', title: 'A much longer task title that will not fit the column at all' }),
      lay,
      true,
      0,
    )
    expect([...a.name].length).toBe(lay.name)
    expect([...b.name].length).toBe(lay.name)
    expect(b.name.endsWith('…')).toBe(true)
    expect([...a.model!.text].length).toBe(lay.model)
    expect([...b.model!.text].length).toBe(lay.model)
    expect([...a.effort!.text].length).toBe(lay.effort)
    expect(a.bar.cols).toBe(b.bar.cols)
  })
})

describe('card rows', () => {
  const lay = planLayout(120, true)
  test('model and effort show what was seen; a different ask shows red', () => {
    const ok = cardRow(
      row({ state: 'running', worker: worker({ asked: 'sonnet', seen: 'claude-sonnet-5-5', askedEffort: 'medium', effort: 'medium' }) }),
      lay,
      true,
      0,
    )
    expect(ok.model!.text.trim()).toBe('Sonnet 5.5')
    expect(ok.model!.color).toBeUndefined()
    const bad = cardRow(
      row({ state: 'running', worker: worker({ asked: 'opus', seen: 'claude-sonnet-5-5', askedEffort: 'high', effort: 'low' }) }),
      lay,
      true,
      0,
    )
    expect(bad.model!.color).toBe(HEX.needs)
    expect(bad.effort!.color).toBe(HEX.needs)
    expect(bad.effort!.text.trim()).toBe('low')
  })
  test('detail: note when running, accepted, to come, the blocked call or asks you in red, failed in red', () => {
    const d = (r: PlanRow) => cardRow(r, lay, true, 0).detail!
    expect(d(row({ state: 'running', steps: { done: 1, total: 4, note: 'adding the atom', atMs: 0 } })).text).toBe('adding the atom')
    expect(d(row({ state: 'done' })).text).toBe('accepted')
    expect(d(row({ state: 'todo' })).text).toBe('to come')
    const needs = d(row({ state: 'needs', worker: worker({ blocked: { what: 'wants to run git push', sinceMs: 0, toolUseId: 'x' } }) }))
    expect(needs).toMatchObject({ text: 'git push', color: HEX.needs })
    expect(d(row({ state: 'needs' }))).toMatchObject({ text: 'asks you', color: HEX.needs })
    expect(d(row({ state: 'failed' }))).toMatchObject({ text: 'failed', color: HEX.failed })
  })
  test('a worker row has no number', () => {
    const r = cardRow(row({ kind: 'worker', n: undefined, key: 'w-1', title: 'loose worker', state: 'running' }), lay, true, 0)
    expect(r.name.startsWith('loose worker')).toBe(true)
  })
  test('without Raster the mark is a glyph in the state colour and the bar is text', () => {
    const l = planLayout(120, false)
    const g = (s: PlanRow['state']) => cardRow(row({ state: s }), l, false, 0).mark.glyph!
    expect(g('running')).toEqual({ text: '●', color: HEX.running })
    expect(g('done')).toEqual({ text: '✓', color: HEX.done })
    expect(g('needs')).toEqual({ text: '◆', color: HEX.needs })
    expect(g('todo')).toEqual({ text: '◷', color: HEX.todo })
    const r = cardRow(row({ state: 'running', steps: { done: 1, total: 3, atMs: 0 } }), l, false, 0)
    expect(r.mark.cells).toBeUndefined()
    expect(r.bar.text!.map(s => s.text).join('')).toBe('██░'.padEnd(l.bar - 0 > 3 ? 3 : l.bar) + ' '.repeat(l.bar - 3))
  })
  test('text bar: solid fills the width; todo is ░', () => {
    expect(textBar(4, ['done']).map(s => s.text).join('')).toBe('████')
    expect(textBar(4, ['todo']).map(s => s.text).join('')).toBe('░░░░')
  })
})

describe('the band group', () => {
  const v = view([row({ state: 'done' }), row({ key: 't-2', n: 2, state: 'running' }), row({ key: 't-3', n: 3, state: 'todo' })], 1)
  test('no plan, nothing', () => {
    expect(planBand({ accepted: 0, total: 0, rows: [] }, 100, true, 0)).toBeUndefined()
  })
  test('a bar, at most 28 columns, and "N of M"', () => {
    const b = planBand(v, 200, true, 0)!
    expect(b.count).toBe('1 of 3')
    expect(b.bar.cols).toBe(12)
    const big = planBand(view(Array.from({ length: 12 }, (_, i) => row({ key: `t-${i}`, n: i + 1, state: 'todo' }))), 200, true, 0)!
    expect(big.bar.cols).toBe(28)
    expect(b.width).toBe(5 + 5 + 12 + 1 + 6)
  })
  test('shrinks to the room left, then goes', () => {
    const wide = planBand(v, 200, true, 0)!
    const less = planBand(v, wide.width - 4, true, 0)!
    expect(less.bar.cols).toBe(wide.bar.cols - 4)
    expect(less.width).toBeLessThanOrEqual(wide.width - 4)
    expect(planBand(v, 20, true, 0)).toBeUndefined()
  })
  test('never wider than the room it was given', () => {
    for (let room = 0; room < 80; room++) {
      const b = planBand(v, room, true, 0)
      if (b) expect(b.width).toBeLessThanOrEqual(room)
    }
  })
  test('the plan tool\'s title leads the bar, short; without one the label is "plan"', () => {
    expect(planBand(v, 200, true, 0)!.label).toBe('plan')
    const titled = planBand({ ...v, title: 'overtone plan view' }, 200, true, 0)!
    expect(titled.label).toBe('overtone plan view')
    expect(titled.width).toBe(5 + 'overtone plan view'.length + 1 + 12 + 1 + 6)
    const long = planBand({ ...v, title: 'a very long plan title that goes on' }, 200, true, 0)!
    expect(long.label.length).toBe(BAND_TITLE_MAX)
    expect(long.label.endsWith('…')).toBe(true)
    expect(bandLabel('  ')).toBe('plan')
  })
  test('short of room the title gives way to "plan" before the group goes', () => {
    const t = { ...v, title: 'overtone plan view' }
    const plain = planBand(v, 200, true, 0)!
    const b = planBand(t, plain.width, true, 0)!
    expect(b.label).toBe('plan')
    for (let room = 0; room < 80; room++) {
      const x = planBand(t, room, false, 0)
      if (x) expect(x.width).toBeLessThanOrEqual(room)
    }
  })
  test('a one-task plan shows in Raster too (4 columns, under the 6 minimum for longer plans)', () => {
    // review 2026-10-08 item 4
    const one = view([row({ state: 'running' })])
    const b = planBand(one, 200, true, 0)!
    expect(b).toBeDefined()
    expect(b.bar.cols).toBe(4)
    expect(planBand(one, b.width - 1, true, 0)).toBeUndefined()
  })
  test('without Raster the bar is text, one character per task', () => {
    const b = planBand(v, 200, false, 0)!
    expect(b.bar.cells).toBeUndefined()
    expect(b.bar.text!.map(s => s.text).join('')).toBe('██░')
  })
})

describe('the card', () => {
  const rows = [
    row({ state: 'done' }),
    row({ key: 't-2', n: 2, state: 'running' }),
    row({ key: 't-3', n: 3, state: 'needs' }),
    row({ key: 't-4', n: 4, state: 'todo' }),
    row({ key: 't-5', n: 5, state: 'todo' }),
  ]
  test('one line per plan row in order, header counts accepted', () => {
    const c = planCard(view(rows, 1), 120, true, 0)
    expect(c.rows.map(r => r.key)).toEqual(['t-1', 't-2', 't-3', 't-4', 't-5'])
    expect(c.header).toBe('1 of 5 accepted')
  })
  test('short of rows the urgent ones stay, in plan order, the rest counted', () => {
    const c = planCard(view(rows, 1), 120, true, 0, 2)
    expect(c.rows.map(r => r.key)).toEqual(['t-2', 't-3'])
    expect(c.header).toBe('1 of 5 accepted · +3 more')
  })
  test('animates while a row runs, needs you or failed (failed rows flash); a returned row is steady', () => {
    expect(isAnimating(view(rows))).toBe(true)
    expect(isAnimating(view([row({ state: 'done' }), row({ key: 't-2', state: 'todo' })]))).toBe(false)
    // review 2026-10-08 item 6: a failed-only view stopped the ticker its flash needs
    expect(isAnimating(view([row({ state: 'failed' })]))).toBe(true)
    expect(isAnimating(view([row({ state: 'returned' })]))).toBe(false)
  })
})

describe('a returned row (review 2026-10-08 item 3)', () => {
  test('yellow and steady: square solid, bar never flashes, glyph ◉, detail "returned, awaiting acceptance"', () => {
    expect(HEX.returned).toBe(HEX.running)
    expect(squarePixels('returned', 0)).toEqual(squarePixels('returned', 1))
    expect(new Set(squarePixels('returned', 1).flat()).size).toBe(1)
    expect(barPixels(8, ['returned'], 1)).toEqual(barPixels(8, ['returned'], 0))
    const c = cardRow(row({ state: 'returned', steps: { done: 3, total: 3, atMs: 0 } }), planLayout(120, false), false, 0)
    expect(c.mark.glyph?.text).toBe('◉')
    expect(c.detail?.text).toBe('returned, awaiting acceptance')
    expect(c.detail?.color).toBe(HEX.returned)
  })
})

describe('overflow (review 2026-10-08 item 5)', () => {
  test('tasks a host tool sent past the cap are named in the card header, not dropped silently', () => {
    const v = { ...view([row({ state: 'todo' })]), overflow: 3 }
    expect(planCard(v, 120, false, 0).header).toBe('0 of 1 accepted · 3 over the cap not kept')
  })
})

describe('worker text on the plan card', () => {
  const BAD = /[\u0000-\u001f\u007f-\u009f‪-‮]/
  const lay = planLayout(120, true)
  test('effort, the blocked call and the activity are drawn without escape or bidi characters', () => {
    const e = cardRow(row({ state: 'running', worker: worker({ effort: 'hi\u001b[31mgh‮' }) }), lay, true, 0)
    expect(BAD.test(e.effort!.text)).toBe(false)
    expect(e.effort!.text.startsWith('hi [31m')).toBe(true)
    const b = cardRow(
      row({ state: 'needs', worker: worker({ blocked: { what: 'wants to run \u001b[31mgit‮ push', sinceMs: 0, toolUseId: 'x' } }) }),
      lay,
      true,
      0,
    )
    expect(BAD.test(b.detail!.text)).toBe(false)
    expect(b.detail!.text).toBe('[31mgit push')
    const a = cardRow(row({ state: 'running', worker: worker({ activity: 'ran \u001b]0;t\u0007it‮' }) }), lay, true, 0)
    expect(BAD.test(a.detail!.text)).toBe(false)
  })
})
