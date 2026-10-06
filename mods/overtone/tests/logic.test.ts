import { describe, expect, test } from 'claude-code/testing'

import type { OvertoneModel, OvertoneWorkers } from '../types'
import {
  EMPTY_WORKERS,
  INFERRED,
  QUIET_AFTER_MS,
  bandState,
  bandText,
  compareModels,
  composeBand,
  fmtDuration,
  foldWorkers,
  isQuiet,
  needsBand,
  noteAsk,
  noteEnd,
  noteList,
  noteListError,
  noteSpawn,
  noteStepEnd,
  noteStepStart,
  noteToolEnd,
  noteToolStart,
  quietCount,
  readContext,
  rowText,
  showModel,
  summarizeTool,
  tierFor,
} from '../hooks/logic'
import type { Band, BandInput, Row } from '../hooks/logic'

const T0 = new Date(2026, 9, 2, 12).getTime()
const MIN = 60_000

const calm = { tokens: 119_000, window: 1_000_000, percent: 12 }
const hot = { tokens: 164_000, window: 200_000 } // 82%, derived: an estimate
const matched: OvertoneModel = { asked: 'claude-sonnet-5-5', seen: 'claude-sonnet-5-5', effort: 'high', steps: 3 }
const mismatched: OvertoneModel = { asked: 'claude-opus-4-7', seen: 'claude-sonnet-5-5', steps: 2 }

const texts = (b: Band | undefined): string[] => (b ? b.rows.map(rowText) : [])
const toned = (r: Row | undefined) => (r ? r.segs.filter(s => s.tone === 'warning' || s.tone === 'error') : [])

function running(n: number): OvertoneWorkers {
  let w: OvertoneWorkers = EMPTY_WORKERS
  for (let i = 0; i < n; i++) {
    w = noteSpawn(w, { id: `a${i}`, description: `Worker ${i}`, type: 'Explore', nowMs: T0 + i * MIN })
  }
  return w
}

function blockedOne(base: OvertoneWorkers, id: string, at: number): OvertoneWorkers {
  let w = noteToolStart(base, { agentId: id, toolUseId: `u-${id}`, summary: 'Bash git push', nowMs: at })
  w = noteAsk(w, { toolUseId: `u-${id}`, nowMs: at })
  return w
}

describe('context row', () => {
  test('state at the thresholds (the old rule, unchanged)', () => {
    expect(bandState(199_000, 59)).toBe('keep working')
    expect(bandState(200_000, 20)).toBe('switch at a break')
    expect(bandState(120_000, 60)).toBe('switch at a break')
    expect(bandState(160_000, 80)).toBe('switch now')
  })

  test('engine percent is a fact, a derived one an estimate', () => {
    expect(readContext(calm)).toEqual({ tokens: 119_000, percent: 12, isEstimate: false, state: 'keep working', crossedBy: undefined })
    expect(readContext(hot)).toMatchObject({ percent: 82, isEstimate: true, state: 'switch now', crossedBy: 'percent' })
    expect(readContext({ tokens: 341_000 })).toMatchObject({ percent: undefined, state: 'switch at a break', crossedBy: 'tokens' })
    expect(readContext({ tokens: 150_000 })).toMatchObject({ state: undefined })
    expect(readContext(null)).toBeUndefined()
    expect(readContext({ window: 200_000 })).toBeUndefined()
  })

  test('crossed: the number is coloured, the remedy named', () => {
    const b = composeBand({ reading: hot, model: null, workers: null, nowMs: T0 }, 120)
    expect(b?.tier).toBe('wide')
    const ctx = b?.rows[0]
    expect(rowText(ctx as Row)).toBe('ctx 164k · ≈82% of window used · switch now')
    expect(ctx?.dim).toBe(false)
    expect(toned(ctx)).toEqual([{ text: '≈82%', tone: 'error', bold: true }])
  })

  test('200k rule with no window: the token count is what crossed', () => {
    const b = composeBand({ reading: { tokens: 341_000 }, model: null, workers: null, nowMs: T0 }, 120)
    expect(texts(b)[0]).toBe('ctx 341k · window not reported · switch at a break')
    expect(toned(b?.rows[0])).toEqual([{ text: 'ctx 341k', tone: 'warning', bold: true }])
  })
})

describe('quiet by default', () => {
  test('calm context alone: the context row always shows, dim, then the model row; no workers row', () => {
    const i: BandInput = { reading: calm, model: matched, workers: running(0), nowMs: T0 }
    expect(needsBand(i)).toBe(false)
    const b = composeBand(i, 120)
    expect(texts(b)).toEqual([
      'ctx 119k · 12% of window used · keep working',
      'model  sonnet-5.5 asked · sonnet-5.5 seen · effort high asked, seen unavailable',
    ])
    expect(b?.rows.every(r => r.dim)).toBe(true)
    expect(b?.rows.flatMap(toned)).toEqual([])
    const est = composeBand({ reading: { tokens: 119_000, window: 1_000_000 }, model: null, workers: null, nowMs: T0 }, 120)
    expect(texts(est)[0]).toBe('ctx 119k · ≈12% of window used · keep working')
    expect(texts(est)[1]).toBe('model  — (not seen yet)')
  })

  test('the slot goes back only when even the context is unreadable', () => {
    expect(composeBand({ reading: null, model: null, workers: null, nowMs: T0 }, 120)).toBeUndefined()
    expect(composeBand({ reading: { window: 200_000 }, model: matched, workers: null, nowMs: T0 }, 120)).toBeUndefined()
    // Something that needs you still shows without a reading, the context honest.
    const b = composeBand({ reading: null, model: mismatched, workers: null, nowMs: T0 }, 120)
    expect(texts(b)[0]).toBe('ctx — (no reading yet)')
  })

  test('calm with a worker: every row dim, nothing coloured', () => {
    const b = composeBand({ reading: calm, model: matched, workers: running(1), nowMs: T0 + 2 * MIN }, 120)
    expect(texts(b)).toEqual([
      'ctx 119k · 12% of window used · keep working',
      'model  sonnet-5.5 asked · sonnet-5.5 seen · effort high asked, seen unavailable',
      'workers  1 running',
      '▸ Worker 0',
      '    2m · 0 tool calls',
    ])
    expect(b?.rows.every(r => r.dim)).toBe(true)
    expect(b?.rows.flatMap(r => toned(r))).toEqual([])
  })

  test('no ANSI escape in any row', () => {
    const b = composeBand({ reading: hot, model: mismatched, workers: blockedOne(running(2), 'a0', T0), nowMs: T0 }, 120)
    for (const t of texts(b)) expect(t).not.toMatch(/\u001b/)
  })
})

describe('model row', () => {
  test('names compare across their spellings', () => {
    expect(showModel('claude-opus-4-7')).toBe('opus-4.7')
    expect(showModel('claude-sonnet-4-5-20250929')).toBe('sonnet-4.5')
    expect(compareModels('Opus 5.5 (1M context)', 'claude-opus-5-5')).toBe('match')
    expect(compareModels('claude-opus-5-5[1m]', 'claude-opus-5-5')).toBe('match')
    expect(compareModels('opus', 'claude-opus-5-5')).toBe('match')
    expect(compareModels('opus', 'claude-sonnet-5-5')).toBe('mismatch')
    expect(compareModels('claude-opus-4-7', 'claude-sonnet-5-5')).toBe('mismatch')
    expect(compareModels('default', 'claude-sonnet-5-5')).toBe('unknown')
    expect(compareModels('opusplan', 'claude-sonnet-5-5')).toBe('unknown')
    expect(compareModels(undefined, 'claude-sonnet-5-5')).toBe('unknown')
    expect(compareModels('claude-opus-5-5', undefined)).toBe('unknown')
  })

  test('steps: asked from the session, else the request; seen kept when no usage came', () => {
    let m = noteStepStart(null, { sessionModel: 'opus', stepModel: 'claude-opus-5-5', effort: 'xhigh' })
    expect(m).toEqual({ asked: 'opus', effort: 'xhigh', steps: 1 })
    m = noteStepEnd(m, 'claude-opus-5-5')
    m = noteStepStart(m, { stepModel: 'claude-opus-5-5' })
    expect(m).toEqual({ asked: 'claude-opus-5-5', seen: 'claude-opus-5-5', steps: 2 })
    expect(noteStepEnd(m, undefined)).toBe(m)
  })

  test('mismatch is coloured and said in words', () => {
    const b = composeBand({ reading: calm, model: mismatched, workers: null, nowMs: T0 }, 120)
    expect(texts(b)[1]).toBe('model  opus-4.7 asked · sonnet-5.5 seen · mismatch · effort — (none on the request)')
    expect(toned(b?.rows[1])).toEqual([{ text: 'sonnet-5.5 seen · mismatch', tone: 'warning', bold: true }])
    expect(b?.rows[0]?.dim).toBe(true)
  })

  test('not seen yet: an honest dash, never a guess', () => {
    const b = composeBand({ reading: hot, model: { steps: 0 }, workers: null, nowMs: T0 }, 120)
    expect(texts(b)[1]).toBe('model  — (not seen yet)')
    const s = composeBand({ reading: hot, model: { asked: 'claude-opus-5-5', steps: 1 }, workers: null, nowMs: T0 }, 120)
    expect(texts(s)[1]).toBe('model  opus-5.5 asked · seen — · effort — (none on the request)')
  })
})

describe('workers', () => {
  test('a worker is timed from its spawn; one seen later is a lower bound', () => {
    let w = noteToolStart(EMPTY_WORKERS, { agentId: 'x', toolUseId: 'u1', summary: 'Read a.ts', nowMs: T0 + 5 * MIN })
    expect(w.byId.x).toMatchObject({ fromSpawn: false, tools: 1, activity: 'Read a.ts', label: 'agent x' })
    w = noteSpawn(w, { id: 'x', description: 'Reviewer', type: 'Explore', nowMs: T0 })
    expect(w.byId.x).toMatchObject({ fromSpawn: true, firstSeenMs: T0, label: 'Reviewer', tools: 1 })
    const late = noteList(EMPTY_WORKERS, [{ id: 'y', description: 'Builder', type: 'general-purpose', status: 'running' }], T0)
    const b = composeBand({ reading: calm, model: null, workers: late, nowMs: T0 + 3 * MIN }, 120)
    expect(texts(b)).toContain('    ≥3m · 0 tool calls')
  })

  test('a permission ask blocks its worker until the call settles', () => {
    let w = running(1)
    w = noteToolStart(w, { agentId: 'a0', toolUseId: 'u9', summary: 'Bash git push origin main', nowMs: T0 })
    expect(noteAsk(w, { toolUseId: 'other', nowMs: T0 })).toBe(w)
    w = noteAsk(w, { toolUseId: 'u9', nowMs: T0 })
    expect(w.byId.a0?.blocked).toEqual({ what: 'wants to run Bash git push origin main', sinceMs: T0, toolUseId: 'u9' })
    w = noteToolEnd(w, { agentId: 'a0', toolUseId: 'u9' })
    expect(w.byId.a0?.blocked).toBeUndefined()
    expect(w.byId.a0?.pending).toEqual({})
  })

  test('blocked first, two lines a row, the second dim, the count coloured', () => {
    const w = blockedOne(running(2), 'a0', T0 + 2 * MIN)
    const b = composeBand({ reading: calm, model: matched, workers: w, nowMs: T0 + 6 * MIN }, 120)
    const t = texts(b)
    expect(t.slice(2)).toEqual([
      'workers  1 blocked · 1 running',
      '■ Worker 0  blocked: wants to run Bash git push',
      '    waiting 4m · answer the permission prompt',
      '▸ Worker 1',
      '    5m · 0 tool calls',
    ])
    expect(toned(b?.rows[2])).toEqual([{ text: '1 blocked', tone: 'warning', bold: true }])
    expect(b?.rows[3]?.dim).toBe(false)
    expect(b?.rows[4]?.dim).toBe(true)
  })

  test('fold: two newest running, +N more, a blocked one never folded', () => {
    expect(foldWorkers(running(5)).shown.map(x => x.id)).toEqual(['a4', 'a3'])
    expect(foldWorkers(running(5)).hidden).toBe(3)
    let w = running(3)
    for (const id of ['a0', 'a1', 'a2']) w = blockedOne(w, id, T0)
    w = noteSpawn(w, { id: 'z', description: 'Late', type: 'Explore', nowMs: T0 + 9 * MIN })
    w = blockedOne(w, 'z', T0 + 9 * MIN)
    w = noteSpawn(w, { id: 'r', description: 'Runner', type: 'Explore', nowMs: T0 })
    const f = foldWorkers(w)
    expect(f.blocked).toHaveLength(4)
    expect(f.shown.map(x => x.id)).toEqual(['a0', 'a1', 'a2', 'z'])
    expect(f.hidden).toBe(1)
    const b = composeBand({ reading: calm, model: null, workers: w, nowMs: T0 + 10 * MIN }, 120)
    expect(texts(b)).toContain('    +1 more running')
  })

  test('finished as ✓ Type ×N, failed as ✕; shown beside active ones only', () => {
    let w = running(4)
    w = noteEnd(w, { agentId: 'a0', failed: false, nowMs: T0 })
    w = noteEnd(w, { agentId: 'a1', failed: false, nowMs: T0 })
    w = noteEnd(w, { agentId: 'a2', failed: true, nowMs: T0 })
    const b = composeBand({ reading: calm, model: null, workers: w, nowMs: T0 + 4 * MIN }, 120)
    expect(texts(b)[2]).toBe('workers  1 running · ✓ Explore ×2 · ✕ Explore ×1')
    const done = noteEnd(w, { agentId: 'a3', failed: false, nowMs: T0 })
    // None active: no workers rows; the context and model rows stay.
    expect(texts(composeBand({ reading: calm, model: null, workers: done, nowMs: T0 }, 120))).toEqual([
      'ctx 119k · 12% of window used · keep working',
      'model  — (not seen yet)',
    ])
  })

  test('the list never undoes an ending overtone saw; a list read clears an error', () => {
    let w = noteEnd(running(1), { agentId: 'a0', failed: false, nowMs: T0 })
    w = noteList(w, [{ id: 'a0', description: 'x', type: 'Explore', status: 'running' }], T0)
    expect(w.byId.a0?.status).toBe('completed')
    w = noteListError(w, 'list timed out')
    expect(w.error).toBe('list timed out')
    expect(noteList(w, [], T0).error).toBeUndefined()
  })

  test('a failed read says "status unavailable", never an empty fleet', () => {
    const w = noteListError(EMPTY_WORKERS, 'boom')
    const b = composeBand({ reading: calm, model: null, workers: w, nowMs: T0 }, 120)
    expect(texts(b)[2]).toBe('workers  0 running · status unavailable · boom')
    expect(b?.rows[2]?.dim).toBe(false)
  })

  test('tool summaries: short, first line, the file not the path', () => {
    expect(summarizeTool('Bash', { command: 'git push origin main\necho done' })).toBe('Bash git push origin main')
    expect(summarizeTool('Edit', { file_path: '/a/b/hooks.ts' })).toBe('Edit hooks.ts')
    expect(summarizeTool('Grep', { pattern: 'TODO' })).toBe('Grep TODO')
    expect(summarizeTool('mcp__srv__lookup', {})).toBe('lookup')
    expect(summarizeTool('Bash', { command: 'x'.repeat(200) }).length).toBe(48)
  })

  test('durations', () => {
    expect(fmtDuration(42_000)).toBe('42s')
    expect(fmtDuration(4 * MIN)).toBe('4m')
    expect(fmtDuration(125 * MIN)).toBe('2h05m')
    expect(fmtDuration(-5)).toBe('0s')
  })
})

describe('width tiers', () => {
  test('cut points', () => {
    expect(tierFor(140)).toBe('wide')
    expect(tierFor(100)).toBe('wide')
    expect(tierFor(99)).toBe('mid')
    expect(tierFor(60)).toBe('mid')
    expect(tierFor(50)).toBe('mid')
    expect(tierFor(49)).toBe('narrow')
  })

  test('about 60 columns: the optional tail drops first', () => {
    const calmBand = composeBand({ reading: calm, model: matched, workers: running(1), nowMs: T0 + 2 * MIN }, 60)
    expect(texts(calmBand)).toEqual(['ctx 119k · 12% used', 'model sonnet-5.5 ✓ seen', 'workers 1 running', '▸ Worker 0 · 2m'])
    const w = blockedOne(running(2), 'a0', T0)
    const hotBand = composeBand({ reading: hot, model: mismatched, workers: w, nowMs: T0 }, 60)
    expect(texts(hotBand)).toEqual([
      'ctx 164k · ≈82% used · switch now',
      'model opus-4.7 asked, sonnet-5.5 seen ≠',
      'workers 1 blocked · 1 running',
      '■ Worker 0 · blocked: wants to run Bash git push',
      '▸ Worker 1 · 0s',
    ])
  })

  test('narrow: one line, worst first when anything needs you', () => {
    const calmLine = composeBand({ reading: calm, model: matched, workers: running(1), nowMs: T0 }, 40)
    expect(calmLine?.tier).toBe('narrow')
    expect(texts(calmLine)).toEqual(['ctx 119k · 12% · sonnet-5.5 ✓ · 1 worker'])
    const hotLine = composeBand({ reading: hot, model: mismatched, workers: blockedOne(running(2), 'a0', T0), nowMs: T0 }, 40)
    expect(texts(hotLine)).toEqual(['1 blocked · model ≠ · ctx ≈82%'])
    expect(hotLine?.rows[0]?.dim).toBe(false)
  })

  test('too few rows for the full band: the one line instead', () => {
    const b = composeBand({ reading: calm, model: matched, workers: running(1), nowMs: T0 }, 120, 3)
    expect(b?.tier).toBe('narrow')
  })
})

describe('/overtone text', () => {
  test('the wide band, or the calm context and model rows when the band is quiet', () => {
    expect(bandText({ reading: calm, model: matched, workers: null, nowMs: T0 }).split('\n')).toEqual([
      'ctx 119k · 12% of window used · keep working',
      'model  sonnet-5.5 asked · sonnet-5.5 seen · effort high asked, seen unavailable',
    ])
    expect(bandText({ reading: hot, model: null, workers: null, nowMs: T0 }).split('\n')[0]).toBe(
      'ctx 164k · ≈82% of window used · switch now',
    )
  })
})

describe('workers that never reported an ending', () => {
  const listed = (id: string, status: string, parentId?: string) => ({ id, status, ...(parentId ? { parentId } : {}) })

  test('a parent that ends takes its unseen descendants with it, against a list read', () => {
    let w = noteSpawn(EMPTY_WORKERS, { id: 'p', description: 'Parent', type: 'Explore', nowMs: T0 })
    // the child is known by its parentAgentId on the spawn, the grandchild by the list
    w = noteSpawn(w, { id: 'c', description: 'Child', type: 'Explore', parentId: 'p', nowMs: T0 })
    w = noteToolStart(w, { agentId: 'g', toolUseId: 'u1', summary: 'Read a.ts', nowMs: T0 + MIN })
    w = noteToolEnd(w, { agentId: 'g', toolUseId: 'u1', nowMs: T0 + MIN })
    w = noteList(w, [listed('p', 'running'), listed('c', 'running', 'p'), listed('g', 'running', 'c')], T0 + MIN)
    expect(w.byId.c?.parentId).toBe('p')
    expect(w.byId.g?.parentId).toBe('c')
    w = noteEnd(w, { agentId: 'p', failed: false, nowMs: T0 + 5 * MIN, listed: [listed('p', 'idle')] })
    expect(w.byId.p).toMatchObject({ status: 'completed', endedMs: T0 + 5 * MIN })
    expect(w.byId.c).toMatchObject({ status: INFERRED, endedMs: T0 + 5 * MIN, pending: {} })
    expect(w.byId.g).toMatchObject({ status: INFERRED, endedMs: T0 + 5 * MIN })
    expect(foldWorkers(w).running).toEqual([])
  })

  test('with no good list the parent still ends and nothing under it is guessed at', () => {
    let w = noteSpawn(EMPTY_WORKERS, { id: 'p', description: 'Parent', type: 'Explore', nowMs: T0 })
    w = noteSpawn(w, { id: 'c', description: 'Child', type: 'Explore', parentId: 'p', nowMs: T0 })
    w = noteEnd(w, { agentId: 'p', failed: false, nowMs: T0 + MIN })
    expect(w.byId.p?.status).toBe('completed')
    expect(w.byId.c?.status).toBe('running')
    // the next good read settles it
    w = noteList(w, [listed('p', 'idle'), listed('c', 'completed', 'p')], T0 + 2 * MIN)
    expect(w.byId.c?.status).toBe('completed')
  })

  test('a list that marks a worker final ends its descendants the list does not name as alive', () => {
    let w = noteList(EMPTY_WORKERS, [listed('p', 'running'), listed('c', 'running', 'p'), listed('k', 'running', 'p')], T0)
    w = noteList(w, [listed('p', 'completed'), listed('k', 'running', 'p')], T0 + 3 * MIN)
    expect(w.byId.p).toMatchObject({ status: 'completed', endedMs: T0 + 3 * MIN })
    // c dropped off the list: ended; k still running per the list: kept
    expect(w.byId.c).toMatchObject({ status: INFERRED, endedMs: T0 + 3 * MIN })
    expect(w.byId.k?.status).toBe('running')
    expect(w.byId.k?.endedMs).toBeUndefined()
  })

  test('a worker the list reports running, pending or waiting is never ended', () => {
    for (const status of ['running', 'pending', 'waiting']) {
      let w = noteList(EMPTY_WORKERS, [listed('p', 'running'), listed('c', status, 'p')], T0)
      w = noteEnd(w, { agentId: 'p', failed: false, nowMs: T0 + MIN, listed: [listed('p', 'completed'), listed('c', status, 'p')] })
      expect(w.byId.c?.status).toBe(status)
      w = noteList(w, [listed('p', 'completed'), listed('c', status, 'p')], T0 + 2 * MIN)
      expect(w.byId.c?.status).toBe(status)
      expect(w.byId.c?.endedMs).toBeUndefined()
    }
  })

  test('a parent loop in the records cannot hang the cascade', () => {
    let w = noteList(EMPTY_WORKERS, [listed('a', 'completed', 'b'), listed('b', 'running', 'a')], T0)
    w = noteList(w, [listed('a', 'completed', 'b')], T0 + MIN)
    expect(w.byId.b?.status).toBe(INFERRED)
  })

  test('quiet: an unspawned worker the list does not name, after QUIET_AFTER_MS without a tool call', () => {
    let w = noteToolStart(EMPTY_WORKERS, { agentId: 'x', toolUseId: 'u1', summary: 'Read a.ts', nowMs: T0 })
    w = noteToolEnd(w, { agentId: 'x', toolUseId: 'u1' })
    // never quiet before a good list read has left it out; a failed read proves nothing
    expect(isQuiet(w.byId.x as never, T0 + 60 * MIN)).toBe(false)
    w = noteListError(w, 'list timed out')
    expect(isQuiet(w.byId.x as never, T0 + 60 * MIN)).toBe(false)
    w = noteList(w, [], T0 + 1000)
    const x = () => w.byId.x as NonNullable<(typeof w.byId)[string]>
    expect(isQuiet(x(), T0 + QUIET_AFTER_MS - 1)).toBe(false)
    expect(isQuiet(x(), T0 + QUIET_AFTER_MS)).toBe(true)
    const late = T0 + QUIET_AFTER_MS + MIN
    // not running, not done: still active, counted apart
    expect(foldWorkers(w, late).running).toEqual([])
    expect(foldWorkers(w, late).quiet.map(q => q.id)).toEqual(['x'])
    expect(quietCount(w, late)).toBe(1)
    expect(x().status).toBe('running')
    expect(needsBand({ reading: calm, model: matched, workers: w, nowMs: late })).toBe(false)
    expect(texts(composeBand({ reading: calm, model: matched, workers: w, nowMs: late }, 120))[2]).toBe('workers  0 running · 1 quiet')
    // a later tool call makes it running again
    w = noteToolStart(w, { agentId: 'x', toolUseId: 'u2', summary: 'Read b.ts', nowMs: late })
    expect(isQuiet(x(), late + MIN)).toBe(false)
    expect(foldWorkers(w, late + MIN).running.map(r => r.id)).toEqual(['x'])
    expect(quietCount(w, late + MIN)).toBe(0)
  })

  test('quiet never applies to a spawned worker, one the list names, one mid-call or blocked', () => {
    const late = T0 + 3 * 60 * MIN
    const spawned = noteSpawn(EMPTY_WORKERS, { id: 's', description: 'Spawned', type: 'Explore', nowMs: T0 })
    expect(quietCount(spawned, late)).toBe(0)
    expect(foldWorkers(spawned, late).running.map(r => r.id)).toEqual(['s'])
    const named = noteList(EMPTY_WORKERS, [{ id: 'n', status: 'running' }], T0)
    expect(quietCount(named, late)).toBe(0)
    // once a later read stops naming it, the clock counts
    expect(quietCount(noteList(named, [], T0 + MIN), late)).toBe(1)
    const midCall = noteList(noteToolStart(EMPTY_WORKERS, { agentId: 'm', toolUseId: 'u1', summary: 'Bash make', nowMs: T0 }), [], T0 + 1000)
    expect(quietCount(midCall, late)).toBe(0)
    expect(quietCount(noteList(blockedOne(EMPTY_WORKERS, 'b', T0), [], T0 + 1000), late)).toBe(0)
  })

  test('the cascade stops below a live child: its descendants are kept, even at a permission ask', () => {
    let w = noteList(EMPTY_WORKERS, [listed('p', 'running'), listed('c', 'running', 'p'), listed('g', 'running', 'c')], T0)
    w = noteToolStart(w, { agentId: 'g', toolUseId: 'u1', summary: 'Bash git push', nowMs: T0 + MIN })
    w = noteAsk(w, { toolUseId: 'u1', nowMs: T0 + MIN })
    // the list names p (now over) and c as running, but omits g
    const read = [listed('p', 'completed'), listed('c', 'running', 'p')]
    const ended = noteEnd(w, { agentId: 'p', failed: false, nowMs: T0 + 2 * MIN, listed: read })
    expect(ended.byId.c?.status).toBe('running')
    expect(ended.byId.g?.status).toBe('running')
    expect(ended.byId.g?.blocked).toBeDefined()
    const reread = noteList(w, read, T0 + 2 * MIN)
    expect(reread.byId.g?.status).toBe('running')
    // without the permission ask or the live child, a worker with a call pending is still kept
    const pending = noteToolStart(noteList(EMPTY_WORKERS, [listed('p', 'running'), listed('g', 'running', 'p')], T0), { agentId: 'g', toolUseId: 'u2', summary: 'Bash make', nowMs: T0 })
    expect(noteList(pending, [listed('p', 'completed')], T0 + MIN).byId.g?.status).toBe('running')
  })

  test('an inferred ending claims no success and is undone by a later list or tool call', () => {
    const base = noteList(EMPTY_WORKERS, [listed('p', 'running'), listed('g', 'running', 'p')], T0)
    // the parent FAILED: the descendant is not reported as completed, and not as a ✓ either
    const failedParent = noteEnd(base, { agentId: 'p', failed: true, nowMs: T0 + MIN, listed: [listed('p', 'failed')] })
    expect(failedParent.byId.p?.status).toBe('failed')
    expect(failedParent.byId.g?.status).toBe(INFERRED)
    const b = composeBand({ reading: calm, model: null, workers: failedParent, nowMs: T0 + 2 * MIN }, 120)
    expect(texts(b).join('\n')).not.toMatch(/Explore|✓/)
    expect(texts(b)).toHaveLength(2)
    // a later list naming it running revives it
    const byList = noteList(failedParent, [listed('p', 'failed'), listed('g', 'running', 'p')], T0 + 3 * MIN)
    expect(byList.byId.g?.status).toBe('running')
    expect(byList.byId.g?.endedMs).toBeUndefined()
    // so does a tool call, and the next list that omits it does not end it again
    const byCall = noteToolStart(failedParent, { agentId: 'g', toolUseId: 'u9', summary: 'Read a.ts', nowMs: T0 + 3 * MIN })
    expect(byCall.byId.g?.status).toBe('running')
    expect(byCall.byId.g?.endedMs).toBeUndefined()
    const settled = noteToolEnd(byCall, { agentId: 'g', toolUseId: 'u9', nowMs: T0 + 3 * MIN })
    expect(noteList(settled, [listed('p', 'failed')], T0 + 4 * MIN).byId.g?.status).toBe('running')
    // its own turn.complete later is a confirmed ending
    expect(noteEnd(failedParent, { agentId: 'g', failed: false, nowMs: T0 + 5 * MIN }).byId.g?.status).toBe('completed')
    // and a list that reports it final confirms the ending as the list says
    expect(noteList(failedParent, [listed('p', 'failed'), listed('g', 'killed', 'p')], T0 + 3 * MIN).byId.g?.status).toBe('killed')
  })

  test('a tool call that ran past the quiet time is not quiet the moment it returns', () => {
    let w = noteToolStart(EMPTY_WORKERS, { agentId: 'x', toolUseId: 'u1', summary: 'Bash make', nowMs: T0 })
    w = noteList(w, [], T0 + 1000)
    const back = T0 + QUIET_AFTER_MS + 5 * MIN
    expect(quietCount(w, back)).toBe(0)
    w = noteToolEnd(w, { agentId: 'x', toolUseId: 'u1', nowMs: back })
    expect(quietCount(w, back)).toBe(0)
    expect(quietCount(w, back + QUIET_AFTER_MS)).toBe(1)
  })

  test('a long chain of finished roots resolves in one pass', () => {
    const list = [listed('r0', 'completed')]
    for (let i = 1; i < 40; i++) list.push(listed(`r${i}`, i % 2 ? 'completed' : 'running', `r${i - 1}`))
    const w = noteList(EMPTY_WORKERS, list, T0)
    expect(Object.values(w.byId).filter(x => x.status === INFERRED)).toHaveLength(0)
    const gone = noteList(w, list.filter(a => a.id === 'r0'), T0 + MIN)
    expect(Object.values(gone.byId).every(x => x.status !== 'running')).toBe(true)
  })
})
