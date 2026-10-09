import { describe, expect, mock, test } from 'claude-code/testing'
import type { AgentInfo, On, SessionUsage } from 'claude-code'

import type { OvertonePlan, OvertoneWorkers } from '../types'

const T0 = new Date(2026, 9, 2, 12).getTime()

type World = {
  usage: SessionUsage
  agents: AgentInfo[]
  failList: boolean
  now: number
  sessionModel: string
  answeredBy: string | undefined
  steps: unknown[]
  measured: unknown[]
  stepUsage: Record<string, number> | undefined
  writes: { path: string; text: string }[]
  runs: string[][]
  git: () => { exitCode: number; stdout: string; stderr: string }
  files: Record<string, { text: string; mtimeMs: number }>
  submitted: { text: string; context?: readonly string[] }[]
}

// The engine beneath the plugin, answered from memory.
function world(on: On, opts: { mockClock?: boolean } = {}): World {
  const w: World = {
    usage: { startedAt: 0, context: { window: 1_000_000 }, rateLimits: [] },
    agents: [],
    failList: false,
    now: T0,
    sessionModel: 'claude-sonnet-5-5',
    answeredBy: 'claude-sonnet-5-5',
    steps: [],
    measured: [],
    stepUsage: undefined,
    writes: [],
    runs: [],
    git: () => ({ exitCode: 128, stdout: '', stderr: 'fatal: not a git repository' }),
    files: {},
    submitted: [],
  }
  if (!opts.mockClock) on('clock.now', () => ({ value: w.now }))
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('session.id', () => ({ value: 'sess-1' }))
  on('session.root', () => ({ value: '/w' }))
  on('env.get', ($, e) => ({ value: e.name === 'HOME' ? '/home/t' : undefined }))
  on('fs.write', ($, e) => {
    w.writes.push({ path: e.path, text: e.text })
    return { value: undefined }
  })
  // Kerd Agent's records, from memory: w.files by absolute path.
  on('fs.exists', ($, e) => ({ value: Object.keys(w.files).some(p => p === e.path || p.startsWith(`${e.path}/`)) }))
  on('fs.list', ($, e) => ({
    value: Object.entries(w.files)
      .filter(([p]) => p.startsWith(`${e.path}/`) && !p.slice(e.path.length + 1).includes('/'))
      .map(([p, f]) => ({ name: p.slice(e.path.length + 1), kind: 'file', size: f.text.length, mtimeMs: f.mtimeMs, isLink: false })),
  }) as never)
  on('fs.read', ($, e) => {
    const f = w.files[e.path]
    if (!f) throw new Error('ENOENT')
    return { value: f.text } as never
  })
  on('process.run', ($, e) => {
    w.runs.push([...e.argv])
    const out = e.argv[0] === 'git' ? w.git() : { exitCode: 0, stdout: '', stderr: '' }
    return { value: { ...out, isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('prompt.submit', ($, e) => {
    w.submitted.push({ text: e.text, context: e.context })
    return { text: e.text, context: e.context }
  })
  on('session.usage', () => ({ value: w.usage }))
  on('session.model', () => ({ value: w.sessionModel }))
  on('agent.list', () => {
    if (w.failList) throw new Error('list down')
    return { value: w.agents }
  })
  on('command.register', ($, e) => ({ value: { command: e.name } }))
  on('session.measure', ($, e) => {
    w.measured.push(e)
    return { changed: e.changed }
  })
  on('turn.step', async function* ($, e) {
    w.steps.push(e)
    return {
      turnId: e.turnId,
      index: e.index,
      answer: 'ok',
      toolUses: [],
      stopReason: 'end_turn',
      usage: w.answeredBy === undefined ? null : { model: w.answeredBy, ...(w.stepUsage ?? {}) },
    } as never
  })
  // The engine draws nothing of its own above the prompt; an empty Box stands
  // for that here.
  on('ui.render', ($, e) => $.ui.resolve(e).Box({}))
  return w
}

const PROPS = {
  hasSurvey: false,
  isWorking: false,
  maxRows: 20,
  bodyColumns: 120,
  scroll: { offset: 0, bodyRows: 19 },
  view: {},
}

const SURFACES = ['terminal', 'desktop'] as const

type T = Parameters<Parameters<typeof test>[1]>[0]

async function measure($: T, w: World) {
  return $.session.measure({ context: w.usage.context, rateLimits: w.usage.rateLimits, changed: ['context'] })
}

const step = (extra: Record<string, unknown> = {}) =>
  ({ turnId: 't1', index: 0, model: 'claude-sonnet-5-5', effort: 'high', messageCount: 3, ...extra }) as never

async function drain(stream: AsyncGenerator<unknown, unknown>): Promise<unknown> {
  for (;;) {
    const r = await stream.next()
    if (r.done) return r.value
  }
}

// Opens the dashboard with a press, then mounts it afresh for reading.
async function expanded($: T, props: Record<string, unknown> = {}, surface: 'terminal' | 'desktop' = 'terminal') {
  const first = await $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: { ...PROPS, ...props } as never })
  await first.press({ key: 'usage' })
  await first.unmount()
  return $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: { ...PROPS, ...props } as never })
}

const H = 3_600_000
const iso = (ms: number) => new Date(ms).toISOString()
const LINE = /^ {2}ctx/
const ROW = (name: string) => new RegExp(`^▸ ${name} `)
const squash = (t: string | undefined) => (t ?? '').trim().replace(/ {2,}/g, ' | ')

// The terminal draws the band's bars (and the plan card's marks and bars) as
// Raster; elsewhere they are text. `walk` flattens a node to text with each
// Raster as ▰ per column; `lineOf` is the band line either way.
type N = { type: string; props: Record<string, unknown>; text?: string; children?: (N | string)[] }
const walk = (n: N | string): string =>
  typeof n === 'string' ? n : n.type === 'Raster' ? '▰'.repeat(Number(n.props.columns)) : (n.children ?? []).map(walk).join('')
type Found = { findAll(q: { type: string }): Promise<N[]>; find(q: { type: string; text?: string | RegExp }): Promise<N | undefined> }
const boxKeyed = async (ui: Found, key: string) => (await ui.findAll({ type: 'Box' })).find(b => b.props.key === key)
const lineOf = async (ui: Found): Promise<string | undefined> => {
  const r = await boxKeyed(ui, 'c-r')
  return r ? walk(r) : (await ui.find({ type: 'Text', text: LINE }))?.text
}
// A bar of `w` cells (10 full): Raster 8 columns on the terminal, text elsewhere.
const bar = (surface: string, w = 10) => (surface === 'terminal' ? '▰'.repeat(w === 10 ? 8 : w) : '◼'.repeat(w))
// A worker's one-line plan row, squashed.
const rowOf = async (ui: Found, id: string): Promise<string | undefined> => {
  const b = await boxKeyed(ui, `w-${id}`)
  return b ? walk(b).trim().replace(/ +/g, ' ') : undefined
}
// The foreground colour of a Raster's first cell.
const fgOf = (cells: unknown): number => {
  const b = atob(String(cells))
  return b.charCodeAt(4) | (b.charCodeAt(5) << 8) | (b.charCodeAt(6) << 16)
}
const lineRasterFgs = async (ui: Found): Promise<number[]> => {
  const r = await boxKeyed(ui, 'c-r')
  return ((r?.children ?? []) as (N | string)[]).filter((c): c is N => typeof c !== 'string' && c.type === 'Raster').map(c => fgOf(c.props.cells))
}
const C = { green: 0x5cc5a3, yellow: 0xe3b341, red: 0xd64545 }

describe('band', () => {
  test('calm: one line above the prompt, bars of what is left, no key hint', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    for (const surface of SURFACES) {
      const ui = await $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: PROPS })
      expect(await lineOf(ui)).toBe(`  ctx ${bar(surface)}  │  5h —  │  7d —  │  cache —`)
      expect((await ui.find({ type: 'Button' }))?.props).toMatchObject({ label: 'expand ▾', action: 'app:cycleDiffBase' })
      if (surface === 'terminal') expect(await lineRasterFgs(ui)).toEqual([C.green])
      else {
        const coloured = (await ui.findAll({ type: 'Text' })).filter(t => t.props.color !== undefined)
        expect(coloured.map(t => [t.text, t.props.color])).toEqual([['◼◼◼◼◼◼◼◼◼', 'success']])
      }
      await ui.unmount()
    }
  })

  test('no context reading: the band hands the slot back', async ($, on) => {
    world(on)
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await ui.find({ type: 'Text' })).toBeUndefined()
    await ui.unmount()
  })

  test('a crossed threshold: the context bar in a theme colour', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 820_000, window: 1_000_000, percent: 82 }, rateLimits: [] }
    await measure($, w)
    for (const surface of SURFACES) {
      const ui = await $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: PROPS })
      expect(await lineOf(ui)).toBe(`  ctx ${bar(surface)}  │  5h —  │  7d —  │  cache —`)
      if (surface === 'terminal') expect(await lineRasterFgs(ui)).toEqual([C.red])
      else {
        const coloured = (await ui.findAll({ type: 'Text' })).filter(t => t.props.color !== undefined)
        expect(coloured.map(t => [t.text, t.props.color])).toEqual([['◼◼', 'error']])
      }
      await ui.unmount()
    }
  })

  test('a click (or the chord) opens the dashboard in place; again closes it; the state is kept', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    for (const surface of SURFACES) {
      const ui = await expanded($, {}, surface)
      // the line carries context, 5-hour and weekly; the band shows workers and cache
      expect(await ui.find({ type: 'Text', text: 'Context' })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: '5-hour' })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: 'Weekly' })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: /Monthly|Today|This session/ })).toBeUndefined()
      expect((await ui.find({ type: 'Button' }))?.props).toMatchObject({ label: 'collapse ▴', action: 'app:cycleDiffBase' })
      // no old header row: no hint, no model line, no outer frame
      expect(await ui.find({ type: 'Text', text: /collapses$/ })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: '▸ Workers · no jobs running' })).toBeDefined()
      // nothing needs him: no next line, no cache card
      expect(await ui.find({ type: 'Text', text: /^next/ })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: 'Cache' })).toBeUndefined()
      // the opened view starts with the same band line as the folded one
      expect(await lineOf(ui)).toBeDefined()
      await ui.press({ key: 'usage' })
      await ui.unmount()
      const closed = await $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: PROPS })
      expect(await lineOf(closed)).toBeDefined()
      await closed.unmount()
    }
  })

  test('rate limits: the 5h bar amber on a run-out, the 7d bar amber where the week lands; the next line in the dashboard', async ($, on) => {
    const w = world(on)
    w.usage = {
      startedAt: 0,
      context: { tokens: 119_000, window: 1_000_000, percent: 12 },
      rateLimits: [
        { kind: 'five_hour', percentUsed: 82, resetsAt: iso(T0 + 3 * H) },
        { kind: 'seven_day', percentUsed: 47, resetsAt: iso(T0 + 78 * H) },
      ],
    }
    await measure($, w)
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: { ...PROPS, bodyColumns: 200 } })
    expect(await lineOf(ui)).toBe(`  ctx ${bar('terminal')}  │  5h ${bar('terminal')}  │  7d ${bar('terminal')}  │  cache —`)
    expect(await lineRasterFgs(ui)).toEqual([C.green, C.yellow, C.yellow])
    await ui.unmount()
    const big = await expanded($, { bodyColumns: 150 })
    expect((await big.find({ type: 'Text', text: /^next ▸/ }))?.text).toMatch(/^next ▸ 5-hour runs out ≈ \d\d:\d\d — hold big jobs; a good point to Switch Out$/)
    expect(await big.find({ type: 'Text', text: 'lands ≈88% at reset' })).toBeUndefined()
    await big.unmount()
  })

  test('a reported 5-minute cache life (PostModelSwitch): six idle minutes is the idle case', async ($, on) => {
    const w = world(on)
    const stored: Record<string, unknown> = {}
    on('store.set', ($, e) => {
      stored[e.key] = e.value
      return { value: undefined }
    })
    // the settings hooks beneath: none configured, nothing to say
    let reached = 0
    on('classic.PostModelSwitch', () => {
      reached++
      return {}
    })
    w.usage = { startedAt: 0, context: { tokens: 212_000, window: 1_000_000, percent: 21 }, rateLimits: [] }
    const passed = await $.classic.PostModelSwitch({
      from_model: 'claude-opus-5-5',
      to_model: 'claude-opus-5-5',
      requested_model: null,
      source: 'resume',
      context_tokens: 212_000,
      prompt_cache_warm: true,
      cache_ttl: '5m',
      estimated_cache_write_usd: 0,
      pricing: 'catalog',
    } as never)
    expect(passed).toEqual({})
    expect(reached).toBe(1)
    w.stepUsage = { input_tokens: 2_000, output_tokens: 100, cache_read_input_tokens: 196_000, cache_creation_input_tokens: 2_000 }
    await drain($.turn.step(step()))
    w.now = T0 + 6 * 60_000
    w.stepUsage = { input_tokens: 1_000, output_tokens: 100, cache_read_input_tokens: 100_000, cache_creation_input_tokens: 125_000 }
    await drain($.turn.step(step()))
    await measure($, w)
    const open = await expanded($, { bodyColumns: 150, maxRows: 30 })
    expect(await open.find({ type: 'Text', text: '▼ case: idle' })).toBeDefined()
    await open.unmount()
    expect((stored.snapshot as { estimates: { cacheTtl: string } }).estimates.cacheTtl).toBe('5m')
  })

  test('the cache went cold: a red alert on the line, the cache card in the dashboard', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 212_000, window: 1_000_000, percent: 21 }, rateLimits: [] }
    w.stepUsage = { input_tokens: 2_000, output_tokens: 100, cache_read_input_tokens: 196_000, cache_creation_input_tokens: 2_000 }
    await drain($.turn.step(step()))
    // past the assumed 1-hour cache life
    w.now = T0 + 61 * 60_000
    w.stepUsage = { input_tokens: 1_000, output_tokens: 100, cache_read_input_tokens: 100_000, cache_creation_input_tokens: 125_000 }
    await drain($.turn.step(step()))
    await measure($, w)
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await lineOf(ui)).toBe(`  ctx ${bar('terminal')}  │  5h —  │  7d —  │  cache 44% ▼ re-sent 126k`)
    expect((await ui.findAll({ type: 'Text' })).filter(t => t.props.color === 'error').map(t => t.text)).toEqual(['cache 44% ▼ re-sent 126k'])
    await ui.unmount()
    const open = await expanded($, { bodyColumns: 150, maxRows: 30 })
    expect((await open.find({ type: 'Text', text: /^Last prompt/ }))?.text).toBe('Last prompt re-sent 126k tokens without the cache (44% hit, was 98%).')
    expect(await open.find({ type: 'Text', text: '▼ case: idle' })).toBeDefined()
    expect((await open.find({ type: 'Text', text: /^next ▸/ }))?.text).toBe('next ▸ Context 212k — switch at a break; the cache went cold')
    await open.unmount()
  })

  test('the measure event passes on unchanged', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 10_000, window: 200_000, percent: 5 }, rateLimits: [] }
    const e = { context: w.usage.context, rateLimits: [], changed: ['context' as const] }
    const result = await $.session.measure(e)
    expect(w.measured[0]).toEqual(JSON.parse(JSON.stringify(e)))
    expect(result).toEqual({ changed: ['context'] })
  })
})

describe('model row', () => {
  test('main steps: asked vs seen; a mismatch is no longer drawn in the opened view (no header row)', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    await measure($, w)
    w.sessionModel = 'Opus 4.7'
    w.answeredBy = 'claude-sonnet-5-5'
    const e = step()
    const before = JSON.parse(JSON.stringify(e))
    const result = await drain($.turn.step(e))
    expect(w.steps[0]).toEqual(before)
    expect(result).toMatchObject({ answer: 'ok', usage: { model: 'claude-sonnet-5-5' } })
    const open = await expanded($)
    expect(await open.find({ type: 'Text', text: /^ · Sonnet/ })).toBeUndefined()
    await open.unmount()
  })

  test('subagent steps are excluded: they name their own model', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    await measure($, w)
    await drain($.turn.step(step()))
    w.answeredBy = 'claude-haiku-4-5'
    await drain($.turn.step(step({ agentId: 'sub1', model: 'claude-haiku-4-5', effort: 'low' })))
    expect(w.steps).toHaveLength(2)
    const out = await $.command.run({
      command: 'overtone',
      args: '',
      origin: { kind: 'composer' },
      presentation: { isFullscreen: false, columns: 100 },
    })
    expect(out.text).toContain('model  sonnet-5.5 asked · sonnet-5.5 seen · effort high asked, seen unavailable')
    expect(out.text).not.toContain('haiku')
  })
})

describe('workers', () => {
  test('a row per job while it runs; returned jobs stay until the main loop moves on', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    w.agents = [
      { id: 'a1', description: 'Reviewer', type: 'Explore', status: 'running' },
      { id: 'a2', description: 'Scout', type: 'Explore', status: 'completed' },
    ]
    await measure($, w)
    w.now = T0 + 2 * 60_000
    for (const surface of SURFACES) {
      const ui = await expanded($, {}, surface)
      expect((await ui.find({ type: 'Text', text: /^Workers/ }))?.text).toBe('Workers  1 of 2 returned')
      expect(await rowOf(ui, 'a1')).toMatch(/1\. Reviewer\s.*— —$/)
      expect(await rowOf(ui, 'a2')).toMatch(/2\. Scout\s.*— — returned$/)
      await ui.press({ key: 'usage' })
      await ui.unmount()
    }
    w.agents = [{ id: 'a1', description: 'Reviewer', type: 'Explore', status: 'completed' }]
    await measure($, w)
    w.now = T0 + 3 * 60_000
    await drain($.turn.step(step()))
    const ui = await expanded($)
    expect(await ui.find({ type: 'Text', text: /^Workers/ })).toBeUndefined()
    expect(await ui.find({ type: 'Text', text: '▸ Workers · no jobs running' })).toBeDefined()
    await ui.unmount()
  })

  test('workers with no plan sent: the card draws them as plan rows, numbered in start order, colour by state', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    w.agents = [
      { id: 'a1', description: 'Reviewer', type: 'Explore', status: 'running' },
      { id: 'a2', description: 'Scout', type: 'Explore', status: 'completed' },
    ]
    await measure($, w)
    const band = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    // no plan was sent: no plan bar on the collapsed band
    expect(await band.find({ type: 'Text', text: / of 2$/ })).toBeUndefined()
    expect(await band.find({ type: 'Text', text: /^(plan|workers) $/ })).toBeUndefined()
    await band.unmount()
    const ui = await expanded($)
    expect((await ui.find({ type: 'Text', text: /^Workers/ }))?.text).toBe('Workers  1 of 2 returned')
    const scout = await boxKeyed(ui, 'w-a2')
    const marks = ((scout?.children ?? []) as (N | string)[]).filter((c): c is N => typeof c !== 'string' && c.type === 'Raster')
    // the returned worker's square is solid green
    expect(fgOf(marks[0]?.props.cells)).toBe(C.green)
    await ui.unmount()
  })

  test('workers with no plan on a two-row band: the card keeps its count-only header, no worker row past the budget', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    w.agents = [
      { id: 'a1', description: 'Reviewer', type: 'Explore', status: 'running' },
      { id: 'a2', description: 'Scout', type: 'Explore', status: 'running' },
    ]
    await measure($, w)
    const ui = await expanded($, { maxRows: 2 })
    const rowBoxes = (await ui.findAll({ type: 'Box' })).filter(b => String(b.props.key).startsWith('w-'))
    expect(rowBoxes).toHaveLength(0)
    expect(await ui.find({ type: 'Text', text: /^Workers/ })).toBeDefined()
    await ui.unmount()
  })

  test('workers with no plan animate: the frame ticker runs for the synthetic view too', async ($, on) => {
    const w = world(on, { mockClock: true })
    const clock = mock.clock(on, { now: T0 })
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    w.agents = [{ id: 'a1', description: 'Reviewer', type: 'Explore', status: 'running' }]
    await $.session.start({ cwd: '/w', surface: 'terminal', isInteractive: true })
    await measure($, w)
    const barOf = async (ui: Found) =>
      (((await boxKeyed(ui, 'w-a1'))?.children ?? []) as (N | string)[]).filter((c): c is N => typeof c !== 'string' && c.type === 'Raster').map(c => String(c.props.cells))
    const first = await expanded($)
    const before = await barOf(first)
    await first.unmount()
    await clock.advance(2_100)
    await clock.settle()
    const again = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS as never })
    const after = await barOf(again)
    expect(before).toHaveLength(2)
    expect(after).not.toEqual(before)
    await again.unmount()
  })

  test('a spawn and its requests: asked vs saw, activity; a permission ask holds it', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    on('agent.spawn', () => ({ model: 'claude-sonnet-5-5', agentId: 's1' }))
    let ask: unknown
    on('tool.check', () => ({ decision: 'ask' }) as never)
    // The engine's own check, raised from the test's `$` while the call waits.
    on('tool.call', async (_inner, e) => {
      ask = await $.tool.check({ tool: e.tool, input: {}, tool_use_id: e.tool_use_id } as never)
      const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
      seenWhileWaiting = [...(await ui.findAll({ type: 'Text' })).map(t => squash(t.text)), (await rowOf(ui, 's1')) ?? '']
      await ui.unmount()
      return { result: 'ok' } as never
    })
    let seenWhileWaiting: string[] = []
    await measure($, w)
    const open = await expanded($)
    await open.unmount()
    const spawned = await $.agent.spawn({ prompt: 'Review it.', description: 'Reviewer', subagentType: 'kerd:sonnet-high' } as never)
    expect(spawned).toMatchObject({ agentId: 's1' })
    await drain($.turn.step(step({ agentId: 's1', model: 'claude-sonnet-5-5', effort: 'high' })))
    const call = await $.tool.call({ tool: 'Read', file_path: '/a/b/hooks.ts', agentId: 's1', tool_use_id: 'u1' } as never)
    expect(call).toMatchObject({ result: 'ok' })
    expect(ask).toMatchObject({ decision: 'ask' })
    expect(seenWhileWaiting).toContain('▰▰1. Reviewer ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰Sonnet 5.5 high Read hooks.ts')
    expect(seenWhileWaiting).toContain('next ▸ The Reviewer — waits on a permission prompt')
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await rowOf(ui, 's1')).toMatch(/^▰*1\. Reviewer\b/)
    await ui.unmount()
  })

  test('a nested helper the list names under a parent ends with that parent; a main-loop turn reconciles the rest', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    on('agent.spawn', (_$, e) => ({ model: 'claude-sonnet-5-5', agentId: e.description === 'Child' ? 'c1' : 'p1' }))
    on('turn.complete', () => ({ text: 'ok' }))
    on('tool.call', () => ({ result: 'ok' }) as never)
    const done = (extra: Record<string, unknown> = {}) =>
      ({ answer: 'done', durationMs: 1, isAborted: false, turnId: 't1', reason: 'answer', ...extra }) as never
    await measure($, w)
    await $.agent.spawn({ prompt: 'Go.', description: 'Parent', subagentType: 'Explore' } as never)
    await $.agent.spawn({ prompt: 'Go.', description: 'Child', subagentType: 'Explore', parentAgentId: 'p1' } as never)
    // two helpers overtone never saw spawn: one the list ties to the parent, one it stops naming
    await $.tool.call({ tool: 'Read', file_path: '/a/b.ts', agentId: 'h1', tool_use_id: 'u1' } as never)
    await $.tool.call({ tool: 'Read', file_path: '/a/c.ts', agentId: 'h2', tool_use_id: 'u2' } as never)
    w.agents = [
      { id: 'p1', description: 'Parent', type: 'Explore', status: 'running' },
      { id: 'h1', description: 'Helper', type: 'Explore', status: 'running', parentId: 'p1' },
    ]
    await measure($, w)
    const rows = async () => {
      const ui = await expanded($)
      const texts = (await ui.findAll({ type: 'Box' }))
        .filter(b => String(b.props.key).startsWith('w-'))
        .map(b => walk(b).trim().replace(/ +/g, ' '))
      await ui.press({ key: 'usage' })
      await ui.unmount()
      return texts
    }
    const names = (rs: string[]) => rs.map(t => /^▰*(\d+\. (?:agent h\d|\w+))/.exec(t)?.[1])
    expect(names(await rows())).toEqual(['1. Parent', '2. Child', '3. agent h1', '4. agent h2'])
    // the parent returns; the list (read first) no longer shows its helper as alive
    w.agents = [
      { id: 'p1', description: 'Parent', type: 'Explore', status: 'completed' },
      { id: 'h1', description: 'Helper', type: 'Explore', status: 'completed', parentId: 'p1' },
    ]
    await $.turn.complete(done({ agentId: 'p1' }))
    // h2 is a main-loop leftover: the list no longer has it, and a main turn reads the list
    w.agents = [{ id: 'h2', description: 'Other', type: 'Explore', status: 'completed' }]
    await $.turn.complete(done())
    // the ones the list says returned show so (until the main loop steps); the child inferred over is
    // not claimed as returned; none is running
    const after = await rows()
    expect(names(after)).toEqual(['1. Parent', '2. agent h1', '3. agent h2'])
    expect(after.every(t => t.endsWith('returned'))).toBe(true)
  })

  test('a worker the list does not name goes quiet after ten minutes: counted apart, not running, not done', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    on('tool.call', () => ({ result: 'ok' }) as never)
    await measure($, w)
    await $.tool.call({ tool: 'Read', file_path: '/a/b.ts', agentId: 'h9', tool_use_id: 'u1' } as never)
    // a good list read that leaves it out is what lets it go quiet
    await measure($, w)
    w.now = T0 + 9 * 60_000
    let ui = await expanded($)
    expect(await rowOf(ui, 'h9')).toMatch(/^▰*1\. agent h9\b/)
    await ui.press({ key: 'usage' })
    await ui.unmount()
    w.now = T0 + 11 * 60_000
    ui = await expanded($)
    const texts = (await ui.findAll({ type: 'Text' })).map(t => squash(t.text))
    expect(texts).toContain('▸ Workers · no jobs running · 1 quiet')
    expect(texts.some(t => /agent h9|returned/.test(t))).toBe(false)
    await ui.press({ key: 'usage' })
    await ui.unmount()
    await $.tool.call({ tool: 'Read', file_path: '/a/c.ts', agentId: 'h9', tool_use_id: 'u2' } as never)
    ui = await expanded($)
    expect(await rowOf(ui, 'h9')).toMatch(/^▰*1\. agent h9\b/)
    await ui.press({ key: 'usage' })
    await ui.unmount()
  })

  test('a worker on another model than asked: red on the line and in its row', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    on('agent.spawn', () => ({ model: 'claude-sonnet-5-5', agentId: 'b1' }))
    await measure($, w)
    await $.agent.spawn({ prompt: 'Build.', description: 'Builder', subagentType: 'general-purpose', model: 'opus' } as never)
    await drain($.turn.step(step({ agentId: 'b1', model: 'claude-sonnet-5-5', effort: 'high' })))
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await lineOf(ui)).toBe(`  ctx ${bar('terminal')}  │  5h —  │  7d —  │  cache —  │  worker on sonnet, asked opus`)
    await ui.unmount()
    const open = await expanded($)
    expect(await rowOf(open, 'b1')).toMatch(/^▰*▼ 1\. Builder\b.*Sonnet 5\.5 high wrong model · asked Opus$/)
    // the model the worker is not meant to be on shows red in its row
    const red = (await open.findAll({ type: 'Text' })).filter(t => t.props.color === '#D64545').map(t => t.text.trim())
    expect(red).toEqual(expect.arrayContaining(['Sonnet 5.5']))
    expect((await open.find({ type: 'Text', text: /^next ▸/ }))?.text).toBe('next ▸ The Builder — is on the wrong model')
    await open.unmount()
  })

  test('a failed list read: "status unavailable" in the dashboard, and the chain goes on', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    w.failList = true
    const result = await measure($, w)
    expect(result).toEqual({ changed: ['context'] })
    const ui = await expanded($)
    // The engine words the failure itself; the band shows it, cut short.
    const warned = (await ui.findAll({ type: 'Text' })).filter(t => t.props.color === 'warning').map(t => t.text)
    expect(warned).toEqual([expect.stringMatching(/^ · worker status unavailable · .+/)])
    await ui.unmount()
  })

  test('a rejection beneath a worker tool call or a spawn: each runs once, never replayed', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    let calls = 0
    let spawns = 0
    on('tool.call', () => {
      calls++
      throw new Error('the tool beneath failed')
    })
    on('agent.spawn', () => {
      spawns++
      throw new Error('the spawn beneath failed')
    })
    await measure($, w)
    const call = await $.tool.call({ tool: 'Read', file_path: '/a/b.ts', agentId: 's1', tool_use_id: 'u9' } as never).then(
      () => 'resolved',
      () => 'rejected',
    )
    const spawn = await $.agent
      .spawn({ prompt: 'x', description: 'Reviewer', subagentType: 'Explore' } as never)
      .then(
        () => 'resolved',
        () => 'rejected',
      )
    expect(calls).toBe(1)
    expect(spawns).toBe(1)
    expect(call).toBe('rejected')
    expect(spawn).toBe('rejected')
  })

  test('narrow: still one line, bars shrunk and lower cells dropped', async ($, on) => {
    const w = world(on)
    w.usage = {
      startedAt: 0,
      context: { tokens: 50_000, window: 1_000_000, percent: 5 },
      rateLimits: [{ kind: 'five_hour', percentUsed: 30, resetsAt: iso(T0 + 3 * H) }],
    }
    w.agents = [{ id: 'a1', description: 'Reviewer', type: 'Explore', status: 'running' }]
    await measure($, w)
    await drain($.turn.step(step()))
    const ui = await $.ui.mount({
      plugin: 'overtone',
      surface: 'terminal',
      component: 'AbovePrompt',
      props: { ...PROPS, bodyColumns: 40 },
    })
    expect(await lineOf(ui)).toBe('  ctx ▰▰▰▰  │  5h ▰▰▰▰')
    await ui.unmount()
  })

  test('a survey holds the band: overtone yields', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 900_000, window: 1_000_000, percent: 90 }, rateLimits: [] }
    await measure($, w)
    const ui = await $.ui.mount({
      plugin: 'overtone',
      surface: 'terminal',
      component: 'AbovePrompt',
      props: { ...PROPS, hasSurvey: true },
    })
    expect(await ui.find({ type: 'Text', text: /^ctx/ })).toBeUndefined()
    await ui.unmount()
  })
})

describe('what Claude and Switch Out see', () => {
  test('each prompt carries one short context line of the same figures; the text is unchanged', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 200_000, percent: 60 }, rateLimits: [] }
    await measure($, w)
    const r = await $.prompt.submit({ text: 'finish the dashboard', wait: false, origin: { kind: 'composer' } })
    expect(w.submitted).toHaveLength(1)
    expect(w.submitted[0]?.text).toBe('finish the dashboard')
    expect(w.submitted[0]?.context).toEqual(['usage: ctx 119k/200k (60%), switch at a break\nusage next: Context 119k — switch at a break'])
    expect(r.text).toBe('finish the dashboard')
  })

  test('no figures yet: the prompt passes untouched', async ($, on) => {
    const w = world(on)
    await $.prompt.submit({ text: 'hi', wait: false, origin: { kind: 'composer' } })
    expect(w.submitted[0]?.context).toBeUndefined()
  })

  test('after a turn: the snapshot in $.store only (host-managed); no plugin-managed file, no host command', async ($, on) => {
    const w = world(on)
    const stored: Record<string, unknown> = {}
    on('store.set', ($, e) => {
      stored[e.key] = e.value
      return { value: undefined }
    })
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 200_000, percent: 60 }, rateLimits: [] }
    await measure($, w)
    expect(w.writes).toEqual([])
    expect(w.runs).toEqual([])
    const snap = stored.snapshot as Record<string, unknown>
    expect(snap.source).toBe('overtone 0.4.1')
    expect(snap.summary).toBe('usage: ctx 119k/200k (60%), switch at a break\nusage next: Context 119k — switch at a break')
    expect(JSON.stringify(snap)).not.toMatch(/costUsd|today|last30Days/)
  })

  test('the tick manages no file either: only the countdowns and partner reads', async ($, on) => {
    const w = world(on, { mockClock: true })
    const clock = mock.clock(on, { now: T0 })
    mock.store(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 200_000, percent: 60 }, rateLimits: [] }
    await $.session.start({ cwd: '/w', surface: 'terminal', isInteractive: true })
    await measure($, w)
    await clock.advance(24 * H)
    await clock.settle()
    expect(w.writes).toEqual([])
    expect(w.runs.filter(r => r[0] !== 'git')).toEqual([])
  })

  test('partner requests: read from Kerd Agent records on the timers, a row each, a red alert past ten minutes', async ($, on) => {
    const w = world(on, { mockClock: true })
    const clock = mock.clock(on, { now: T0 })
    const dir = '/w/.git/kerd-agent'
    w.git = () => ({ exitCode: 0, stdout: `${dir}\n`, stderr: '' })
    const rec = (id: string, over: Record<string, unknown>) =>
      JSON.stringify({ request_id: id, provider: 'codex', session: 'sess-c', project: '/w', role: 'review of overtone 0.3.1', prompt: 'PROMPT TEXT', created_at: (T0 - 14 * 60_000) / 1000, ...over })
    w.files = {
      [`${dir}/partners/codex-partner.json`]: { text: JSON.stringify({ alias: 'codex-partner', provider: 'codex', id: 'sess-c', project: '/w' }), mtimeMs: T0 - 99 * H },
      [`${dir}/requests/r1.json`]: { text: rec('r1', { status: 'submitted-unconfirmed' }), mtimeMs: T0 - 14 * 60_000 },
      [`${dir}/requests/r2.json`]: { text: rec('r2', { status: 'reply-received', received_at: (T0 - 60_000) / 1000, role: 'guard re-check' }), mtimeMs: T0 - 60_000 },
      [`${dir}/requests/r3.json`]: { text: rec('r3', { status: 'submitted-unconfirmed', project: '/elsewhere' }), mtimeMs: T0 - 60_000 },
      [`${dir}/requests/old.json`]: { text: rec('old', { status: 'submitted-unconfirmed' }), mtimeMs: T0 - 5 * H },
      [`${dir}/requests/r1.lock`]: { text: '', mtimeMs: T0 },
    }
    // newer records that never count (arrival notices, another project) do not crowd out the rows
    for (let i = 0; i < 13; i++) {
      w.files[`${dir}/requests/n${i}.json`] = { text: rec(`n${i}`, { status: 'submitted-unconfirmed', kind: i % 2 ? 'arrival-notice' : undefined, project: i % 2 ? '/w' : '/other' }), mtimeMs: T0 - 1_000 }
    }
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    await $.session.start({ cwd: '/w', surface: 'terminal', isInteractive: true })
    await measure($, w)
    expect(w.runs.filter(r => r[0] === 'git')).toEqual([])
    await clock.advance(1_500)
    await clock.settle()
    expect(w.runs.filter(r => r[0] === 'git')).toEqual([['git', 'rev-parse', '--path-format=absolute', '--git-path', 'kerd-agent']])
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await lineOf(ui)).toBe(`  ctx ${bar('terminal')}  │  5h —  │  7d —  │  cache —  │  codex-partner waiting 14m`)
    await ui.unmount()
    const open = await expanded($, { bodyColumns: 150 })
    expect(squash((await open.find({ type: 'Text', text: /^▸ codex-partner .*review/ }))?.text)).toBe(
      '▸ codex-partner · review of overtone 0.3.1 | Codex session | — | 14m | waiting on a reply',
    )
    expect(squash((await open.find({ type: 'Text', text: /^▸ codex-partner .*guard/ }))?.text)).toBe(
      '▸ codex-partner · guard re-check | Codex session | — | 13m | reply received',
    )
    expect(await open.find({ type: 'Text', text: /elsewhere|PROMPT/ })).toBeUndefined()
    expect((await open.findAll({ type: 'Text', text: /^▸ codex-partner/ })).length).toBe(2)
    await open.unmount()
    // the prompt context names the alert; partner prompt text never leaves the record
    await $.prompt.submit({ text: 'go', wait: false, origin: { kind: 'composer' } })
    expect(w.submitted[0]?.context?.[0]).toContain('alerts: codex-partner reply pending 14m')
    expect(JSON.stringify(w.writes)).not.toContain('PROMPT TEXT')
    // re-read on the tick at most every 30 s; git asked once per root
    await clock.advance(30_000)
    await clock.settle()
    expect(w.runs.filter(r => r[0] === 'git')).toHaveLength(1)
  })

  test('no Kerd Agent records, or no repository: no partner rows, nothing else changes', async ($, on) => {
    const w = world(on, { mockClock: true })
    const clock = mock.clock(on, { now: T0 })
    w.usage = { startedAt: 0, context: { tokens: 50_000, window: 1_000_000, percent: 5 }, rateLimits: [] }
    await $.session.start({ cwd: '/w', surface: 'terminal', isInteractive: true })
    await measure($, w)
    await clock.advance(1_500)
    await clock.settle()
    const ui = await expanded($)
    expect(await ui.find({ type: 'Text', text: '▸ Workers · no jobs running' })).toBeDefined()
    await ui.unmount()
  })

  test('/overtone prints the figures as text', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 200_000, percent: 60 }, rateLimits: [] }
    const out = await $.command.run({
      command: 'overtone',
      args: '',
      origin: { kind: 'composer' },
      presentation: { isFullscreen: false, columns: 100 },
    })
    expect(out.text).toMatch(/^overtone\nusage\nWorkers · no jobs running\nContext — 119k \/ 200k\n/)
    expect(out.text).toContain('5-hour\n  — not reported yet')
    expect(out.text).toContain('next ▸ Context 119k — switch at a break')
    expect(out.text).not.toMatch(/Monthly|Today|This session|\$/)
    expect(out.text).toContain('ctx 119k · 60% of window used · switch at a break')
  })
})

describe('plan state and the step tool', () => {
  // The test's own `$` reads no plugin state: an inline plugin's `Peek` tool
  // answers it from its own `$`.
  const peekPlugin = {
    name: 'peek',
    register: ((on: On) => {
      on('tool.call', { tool: 'Peek' as never }, async $ => ({
        result: {
          plan: (await $.state.get({ plugin: 'overtone', key: 'plan' })).value,
          workers: (await $.state.get({ plugin: 'overtone', key: 'workers' })).value,
        },
      }) as never)
    }) as never,
  }
  const PEEK = { plugins: [peekPlugin] }
  const peek = async ($: T) => ((await $.tool.call({ tool: 'Peek', tool_use_id: 'peek' } as never)) as { result: { plan: OvertonePlan; workers: OvertoneWorkers } }).result

  test('a plan is drawn: a plan bar on the band, one line per row in the card; text where there is no Raster; no plan, no change', async ($, on) => {
    const w = world(on)
    let nextId = 0
    on('tool.call', (_$, e) => {
      if (e.tool === 'TaskCreate') return { result: { task: { id: String(++nextId), subject: e.subject } } } as never
      return { result: { success: true, taskId: e.taskId } } as never
    })
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    const bare = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await bare.find({ type: 'Text', text: 'plan ' })).toBeUndefined()
    await bare.unmount()
    await $.tool.call({ tool: 'TaskCreate', subject: 'Build it', description: 'd', tool_use_id: 'c1' } as never)
    await $.tool.call({ tool: 'TaskCreate', subject: 'Test it', description: 'd', tool_use_id: 'c2' } as never)
    await $.tool.call({ tool: 'TaskUpdate', taskId: '1', status: 'completed', tool_use_id: 'c3' } as never)
    const band = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(await band.find({ type: 'Text', text: 'plan ' })).toBeDefined()
    expect(await band.find({ type: 'Text', text: ' 1 of 2' })).toBeDefined()
    expect(await band.find({ type: 'Raster' })).toBeDefined()
    expect(await lineOf(band)).toBeDefined()
    await band.unmount()
    for (const surface of SURFACES) {
      const ui = await expanded($, {}, surface)
      expect(await ui.find({ type: 'Text', text: /1 of 2 accepted/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /^1\. Build it/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /^2\. Test it/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'accepted' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'to come' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: '▸ Workers · no jobs running' })).toBeUndefined()
      await ui.press({ key: 'usage' })
      await ui.unmount()
    }
  })

  test('the band: the plain button is last, folded and opened; the plan group has a green dot and a bold name; opened has one Workers box and no outer frame or header', async ($, on) => {
    const w = world(on)
    let nextId = 0
    on('tool.call', (_$, e) => {
      if (e.tool === 'TaskCreate') return { result: { task: { id: String(++nextId), subject: e.subject } } } as never
      return { result: { success: true, taskId: e.taskId } } as never
    })
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    await $.tool.call({ tool: 'TaskCreate', subject: 'Build it', description: 'd', tool_use_id: 'c1' } as never)
    await $.tool.call({ tool: 'TaskCreate', subject: 'Test it', description: 'd', tool_use_id: 'c2' } as never)
    const lastOf = async (ui: Found) => {
      const band = await boxKeyed(ui, 'band')
      return (band?.children ?? []).filter((c): c is N => typeof c !== 'string').at(-1)
    }
    const folded = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    const fb = await lastOf(folded)
    expect(fb?.type).toBe('Button')
    expect(fb?.props).toMatchObject({ label: 'expand ▾', plain: true, action: 'app:cycleDiffBase' })
    expect(fb?.props.variant).toBeUndefined()
    // the plan group: separator, green dot, bold name, bar, bold count
    const dot = await folded.find({ type: 'Text', text: '● ' })
    expect(dot?.props.color).toBe('#5CC5A3')
    const name = await folded.find({ type: 'Text', text: 'plan ' })
    expect(name?.props.bold).toBe(true)
    expect(name?.props.dimColor).toBeUndefined()
    // with no plan the button follows the usage line
    await folded.press({ key: 'usage' })
    await folded.unmount()
    const open = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    const ob = await lastOf(open)
    expect(ob?.type).toBe('Button')
    expect(ob?.props).toMatchObject({ label: 'collapse ▴', plain: true })
    expect(ob?.props.variant).toBeUndefined()
    // the same band line on top, no old header, one rounded box (Workers) and no other frame
    expect(await lineOf(open)).toBeDefined()
    expect(await open.find({ type: 'Text', text: /collapses$/ })).toBeUndefined()
    const framed = (await open.findAll({ type: 'Box' })).filter(b => b.props.borderStyle !== undefined)
    expect(framed.map(b => [b.props.key, b.props.borderStyle])).toEqual([['p-jobs', 'round']])
    await open.press({ key: 'usage' })
    await open.unmount()
  })

  test('the band keeps one row at any height: opened with 1, 2, 3 rows the band line stays and the Workers box degrades', async ($, on) => {
    const w = world(on)
    let nextId = 0
    on('tool.call', (_$, e) => {
      if (e.tool === 'TaskCreate') return { result: { task: { id: String(++nextId), subject: e.subject } } } as never
      return { result: { success: true, taskId: e.taskId } } as never
    })
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    await $.tool.call({ tool: 'TaskCreate', subject: 'Build it', description: 'd', tool_use_id: 'c1' } as never)
    for (const maxRows of [1, 2, 3, 20]) {
      const ui = await expanded($, { maxRows })
      expect(await boxKeyed(ui, 'band')).toBeDefined()
      expect((await ui.findAll({ type: 'Button' })).length).toBe(1)
      const boxes = (await ui.findAll({ type: 'Box' })).filter(b => b.props.key === 'p-jobs')
      expect(boxes.length).toBeLessThanOrEqual(1)
      if (maxRows === 20) expect(boxes.length).toBe(1)
      await ui.press({ key: 'usage' })
      await ui.unmount()
    }
  })

  test('main-loop TaskCreate / TaskUpdate results fold into the plan; the call passes on as it came', PEEK, async ($, on) => {
    const w = world(on)
    let nextId = 0
    const seen: unknown[] = []
    on('tool.call', (_$, e) => {
      seen.push(e)
      if (e.tool === 'TaskCreate') return { result: { task: { id: String(++nextId), subject: e.subject } } } as never
      if (e.tool === 'TaskUpdate') return { result: { success: true, taskId: e.taskId, updatedFields: ['status'] } } as never
      return { result: 'ok' } as never
    })
    const made = await $.tool.call({ tool: 'TaskCreate', subject: 'Build it', description: 'd', tool_use_id: 'c1' } as never)
    expect(made).toMatchObject({ result: { task: { id: '1', subject: 'Build it' } } })
    await $.tool.call({ tool: 'TaskCreate', subject: 'Test it', description: 'd', tool_use_id: 'c2' } as never)
    w.now = T0 + 60_000
    await $.tool.call({ tool: 'TaskUpdate', taskId: '1', status: 'in_progress', tool_use_id: 'c3' } as never)
    expect(seen.map(e => (e as { tool: string }).tool)).toEqual(['TaskCreate', 'TaskCreate', 'TaskUpdate'])
    const p = (await peek($)).plan
    expect(p.tasks.map(t => [t.id, t.n, t.subject, t.status, t.startedMs])).toEqual([
      ['1', 1, 'Build it', 'in_progress', T0 + 60_000],
      ['2', 2, 'Test it', 'pending', undefined],
    ])
  })

  test('a denied or errored task call changes nothing; a subagent task call is not the plan', PEEK, async ($, on) => {
    world(on)
    on('tool.call', (_$, e) => {
      if (e.tool === 'TaskCreate' && e.subject === 'Denied') return { deny: 'no tasks today' } as never
      if (e.tool === 'TaskCreate' && e.subject === 'Broken') throw new Error('tool failed')
      return { result: { task: { id: '9', subject: String(e.subject) } } } as never
    })
    const denied = await $.tool.call({ tool: 'TaskCreate', subject: 'Denied', description: 'd', tool_use_id: 'c1' } as never)
    expect(denied).toMatchObject({ deny: 'no tasks today' })
    await $.tool.call({ tool: 'TaskCreate', subject: 'Broken', description: 'd', tool_use_id: 'c2' } as never).then(
      () => undefined,
      () => undefined,
    )
    await $.tool.call({ tool: 'TaskCreate', subject: 'Theirs', description: 'd', agentId: 's1', tool_use_id: 'c3' } as never)
    expect((await peek($)).plan.tasks).toEqual([])
  })

  test('a main-loop TodoWrite becomes the plan', PEEK, async ($, on) => {
    world(on)
    on('tool.call', (_$, e) => ({ result: { oldTodos: [], newTodos: (e as { todos: unknown }).todos } }) as never)
    const todos = [
      { content: 'One', status: 'completed', activeForm: 'Doing one' },
      { content: 'Two', status: 'in_progress', activeForm: 'Doing two' },
    ]
    await $.tool.call({ tool: 'TodoWrite', todos, tool_use_id: 't1' } as never)
    const p = (await peek($)).plan
    expect(p.source).toBe('todo')
    expect(p.tasks.map(t => [t.n, t.subject, t.status])).toEqual([
      [1, 'One', 'completed'],
      [2, 'Two', 'in_progress'],
    ])
  })

  test('session.start registers the step tool; a worker step is recorded, a main-loop one ignored', PEEK, async ($, on) => {
    world(on)
    const registered: Record<string, unknown>[] = []
    on('tool.register', (_$, e) => {
      registered.push(e as Record<string, unknown>)
      return { value: { tool: `mcp__overtone__${e.name}` } }
    })
    on('agent.spawn', () => ({ model: 'claude-sonnet-5-5', agentId: 's1' }))
    let beneath = 0
    on('tool.call', () => {
      beneath++
      return { result: 'beneath' } as never
    })
    await $.session.start({ cwd: '/w', surface: 'terminal', isInteractive: true })
    expect(registered.map(r => [r.name, r.isDeferred])).toEqual([
      ['step', false],
      ['plan', false],
    ])
    await $.agent.spawn({ prompt: 'Go.', description: 'Write the tests', subagentType: 'kerd:sonnet-high' } as never)
    const worker = await $.tool.call({ tool: 'mcp__overtone__step', done: 2, total: 5, note: 'cases', agentId: 's1', tool_use_id: 'k1' } as never)
    expect(worker).toMatchObject({ result: 'recorded 2/5' })
    expect((await peek($)).workers.byId.s1?.steps).toEqual({ done: 2, total: 5, note: 'cases', atMs: T0 })
    const main = await $.tool.call({ tool: 'mcp__overtone__step', done: 1, total: 2, tool_use_id: 'k2' } as never)
    expect(main).toMatchObject({ result: expect.stringMatching(/^ignored/) })
    const bad = await $.tool.call({ tool: 'mcp__overtone__step', done: 1, total: 0, agentId: 's1', tool_use_id: 'k3' } as never)
    expect(bad).toMatchObject({ result: expect.stringMatching(/^ignored/) })
    // answered by overtone: nothing beneath ran, and the worker's activity is not "step"
    expect(beneath).toBe(0)
    expect((await peek($)).workers.byId.s1?.activity).toBeUndefined()
  })

  test('the plan tool: the main loop writes the plan (title, tasks, running, accepted, finished); a subagent is ignored', PEEK, async ($, on) => {
    const w = world(on)
    let beneath = 0
    on('tool.call', () => {
      beneath++
      return { result: 'beneath' } as never
    })
    const call = (input: Record<string, unknown>) => $.tool.call({ tool: 'mcp__overtone__plan', tool_use_id: 'p', ...input } as never)
    const go = await call({ title: 'overtone plan view', tasks: [{ subject: 'Build state' }, { subject: 'Draw it' }, { subject: 'Wire Conductor' }] })
    expect(go).toMatchObject({ result: 'plan: 0 of 3 accepted' })
    w.now = T0 + 60_000
    await call({ running: ['Build state', 'Draw it'] })
    w.now = T0 + 120_000
    expect(await call({ accepted: ['Build state'] })).toMatchObject({ result: 'plan: 1 of 3 accepted' })
    let p = (await peek($)).plan
    expect(p.source).toBe('tool')
    expect(p.title).toBe('overtone plan view')
    expect(p.tasks.map(t => [t.subject, t.status, t.startedMs, t.finishedMs])).toEqual([
      ['Build state', 'completed', T0 + 60_000, T0 + 120_000],
      ['Draw it', 'in_progress', T0 + 60_000, undefined],
      ['Wire Conductor', 'pending', undefined, undefined],
    ])
    expect(await call({ title: 'theirs', agentId: 's1' })).toMatchObject({ result: expect.stringMatching(/^ignored/) })
    expect(await call({ tasks: 'nope' })).toMatchObject({ result: expect.stringMatching(/^ignored/) })
    // review 2026-10-08 item 5: oversized input is refused with a clear answer, the plan unchanged
    const huge = Array.from({ length: 101 }, (_, i) => ({ subject: `T${i}` }))
    expect(await call({ tasks: huge })).toMatchObject({ result: expect.stringMatching(/at most 100 tasks/) })
    expect((await peek($)).plan.tasks.length).toBe(3)
    // review 2026-10-08 item 1: a step total past 50 is refused
    expect(await $.tool.call({ tool: 'mcp__overtone__step', done: 1, total: 1_000_000, agentId: 's9', tool_use_id: 'k' } as never)).toMatchObject({
      result: expect.stringMatching(/from 1 to 50/),
    })
    expect((await peek($)).plan.title).toBe('overtone plan view')
    expect(await call({ accepted: 3, finished: true })).toMatchObject({ result: 'plan closed' })
    p = (await peek($)).plan
    expect(p.closed).toBe(true)
    expect(p.tasks.every(t => t.status === 'completed')).toBe(true)
    expect(beneath).toBe(0)
  })
})
