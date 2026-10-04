import { describe, expect, mock, test } from 'claude-code/testing'
import type { AgentInfo, On, SessionUsage } from 'claude-code'

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

describe('band', () => {
  test('calm: one line above the prompt, bars of what is left, no key hint', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    for (const surface of SURFACES) {
      const ui = await $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: PROPS })
      expect((await ui.find({ type: 'Text', text: LINE }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h —  │  7d —  │  cache —')
      expect((await ui.find({ type: 'Button' }))?.props).toMatchObject({ label: '▸ usage', action: 'app:cycleDiffBase' })
      const coloured = (await ui.findAll({ type: 'Text' })).filter(t => t.props.color !== undefined)
      expect(coloured.map(t => [t.text, t.props.color])).toEqual([['◼◼◼◼◼◼◼◼◼', 'success']])
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
      expect((await ui.find({ type: 'Text', text: LINE }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h —  │  7d —  │  cache —')
      const coloured = (await ui.findAll({ type: 'Text' })).filter(t => t.props.color !== undefined)
      expect(coloured.map(t => [t.text, t.props.color])).toEqual([
        ['◼◼', 'error'],
      ])
      await ui.unmount()
    }
  })

  test('a click (or the chord) opens the dashboard in place; again closes it; the state is kept', async ($, on) => {
    const w = world(on)
    w.usage = { startedAt: 0, context: { tokens: 119_000, window: 1_000_000, percent: 12 }, rateLimits: [] }
    await measure($, w)
    for (const surface of SURFACES) {
      const ui = await expanded($, {}, surface)
      expect(await ui.find({ type: 'Text', text: 'Context' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: '5-hour' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'Weekly' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /Monthly|Today|This session/ })).toBeUndefined()
      expect((await ui.find({ type: 'Button' }))?.props).toMatchObject({ label: '▾ usage', action: 'app:cycleDiffBase' })
      expect((await ui.find({ type: 'Text', text: /collapses$/ }))?.text).toBe('click or ctrl+x b collapses')
      expect(await ui.find({ type: 'Text', text: '▸ Workers · no jobs running' })).toBeDefined()
      // nothing needs him: no next line, no cache card
      expect(await ui.find({ type: 'Text', text: /^next/ })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: 'Cache' })).toBeUndefined()
      expect(await ui.find({ type: 'Text', text: LINE })).toBeUndefined()
      await ui.press({ key: 'usage' })
      await ui.unmount()
      const closed = await $.ui.mount({ plugin: 'overtone', surface, component: 'AbovePrompt', props: PROPS })
      expect(await closed.find({ type: 'Text', text: LINE })).toBeDefined()
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
    expect((await ui.find({ type: 'Text', text: LINE }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h ◼◼◼◼◼◼◼◼◼◼  │  7d ◼◼◼◼◼◼◼◼◼◼  │  cache —')
    const hot = (await ui.findAll({ type: 'Text' })).filter(t => t.props.color === 'warning').map(t => t.text)
    expect(hot).toEqual(['◼◼', '◼◼◼◼◼'])
    await ui.unmount()
    const big = await expanded($, { bodyColumns: 150 })
    expect((await big.find({ type: 'Text', text: /^next ▸/ }))?.text).toMatch(/^next ▸ 5-hour runs out ≈ \d\d:\d\d — hold big jobs; a good point to Switch Out$/)
    expect((await big.find({ type: 'Text', text: /^▲ runs out/ }))?.text).toMatch(/^▲ runs out ≈ \d\d:\d\d, 2h 33m early$/)
    expect(await big.find({ type: 'Text', text: 'lands ≈88% at reset' })).toBeDefined()
    expect(await big.find({ type: 'Text', text: 'headroom left: ≈12% of the week' })).toBeDefined()
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
    expect((await ui.find({ type: 'Text', text: LINE }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h —  │  7d —  │  cache 44% ▼ re-sent 126k')
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
  test('main steps: asked vs seen; a mismatch shows in the dashboard header', async ($, on) => {
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
    expect((await open.find({ type: 'Text', text: /^ · Sonnet/ }))?.text).toBe(' · Sonnet 5.5 · high · asked Opus 4.7 ≠ seen')
    const coloured = (await open.findAll({ type: 'Text' })).filter(t => t.props.color !== undefined)
    expect(coloured.map(t => [t.text, t.props.color])).toContainEqual([' · asked Opus 4.7 ≠ seen', 'error'])
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
      expect((await ui.find({ type: 'Text', text: /^Workers/ }))?.text).toBe('Workers running now, what each is doing, asked vs saw')
      expect(squash((await ui.find({ type: 'Text', text: /^ {2}job/ }))?.text)).toBe('job | doing | asked | saw | elapsed | state')
      expect(squash((await ui.find({ type: 'Text', text: ROW('Reviewer') }))?.text)).toBe('▸ Reviewer | started | — | — | ≥2m 00s | running')
      expect(squash((await ui.find({ type: 'Text', text: ROW('Scout') }))?.text)).toBe('▸ Scout | returned | — | — | ≥0s | returned, not yet checked')
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
      seenWhileWaiting = (await ui.findAll({ type: 'Text' })).map(t => squash(t.text))
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
    expect(seenWhileWaiting).toContain('▸ Reviewer | wants to run Read h… Sonnet · high | Sonnet 5.5 | 0s | waiting on you')
    expect(seenWhileWaiting).toContain('next ▸ The Reviewer — waits on a permission prompt')
    const ui = await $.ui.mount({ plugin: 'overtone', surface: 'terminal', component: 'AbovePrompt', props: PROPS })
    expect(squash((await ui.find({ type: 'Text', text: ROW('Reviewer') }))?.text)).toBe(
      '▸ Reviewer | Read hooks.ts | Sonnet · high | Sonnet 5.5 | 0s | ✓ matches',
    )
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
    expect((await ui.find({ type: 'Text', text: LINE }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h —  │  7d —  │  cache —  │  worker on sonnet, asked opus')
    await ui.unmount()
    const open = await expanded($)
    expect(squash((await open.find({ type: 'Text', text: ROW('Builder') }))?.text)).toBe('▸ Builder | started | Opus | Sonnet 5.5 | 0s | ▼ wrong model · sent Sonnet 5.5 · high')
    const red = (await open.findAll({ type: 'Text' })).filter(t => t.props.color === 'error').map(t => t.text.trim())
    expect(red).toEqual(expect.arrayContaining(['Sonnet 5.5', '▼ wrong model']))
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
    const lines = (await ui.findAll({ type: 'Text', text: LINE })).map(t => t.text)
    expect(lines).toEqual(['  ctx ◼◼◼◼  │  5h ◼◼◼◼'])
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
    expect((await ui.find({ type: 'Text', text: LINE }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h —  │  7d —  │  cache —  │  codex-partner waiting 14m')
    await ui.unmount()
    const open = await expanded($, { bodyColumns: 150 })
    expect(squash((await open.find({ type: 'Text', text: /^▸ codex-partner .*review/ }))?.text)).toBe(
      '▸ codex-partner | review of overtone 0.3.1 | Codex session | — | 14m | waiting on a reply',
    )
    expect(squash((await open.find({ type: 'Text', text: /^▸ codex-partner .*guard/ }))?.text)).toBe(
      '▸ codex-partner | guard re-check | Codex session | — | 13m | reply received',
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
