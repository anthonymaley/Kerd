import { describe, expect, test } from 'claude-code/testing'

import type { OvertonePartners, OvertoneSteps, OvertoneWorker, OvertoneWorkers } from '../types'
import {
  BAND_ACTION,
  BAND_CHORD,
  BUTTON_ROOM,
  EMPTY_STEPS,
  alertsOf,
  aliasMap,
  cacheAlert,
  cacheLife,
  collapsedLine,
  sevenTone,
  alertMark,
  contextSummary,
  dashboard,
  dashboardRows,
  fmtElapsed,
  fmtSpan,
  fmtTok,
  gauge,
  sentNote,
  hasFigures,
  jobColumns,
  cell,
  hitPct,
  jobsOf,
  kerdAsk,
  lineText,
  lineWidth,
  nextNote,
  nextText,
  noteAsked,
  noteMainStep,
  noteWorkerModel,
  noteWorkerSeen,
  pace,
  paceMark,
  partnerRow,
  perRowFor,
  prettyModel,
  snapshotJson,
  toggleView,
  usageText,
} from '../hooks/usage-logic'
import type { Snapshot } from '../hooks/usage-logic'

// Noon UTC; every view below is drawn at UTC (offset 0) so times are fixed.
const T0 = Date.UTC(2026, 9, 3, 12, 0)
const M = 60_000
const H = 3_600_000
const iso = (ms: number) => new Date(ms).toISOString()
const PROJECT = '/Users/a/dev/kerd'

const step = (input: number, cacheRead: number, cacheWrite: number, output = 100, model = 'claude-opus-5-5') => ({
  input_tokens: input,
  output_tokens: output,
  cache_read_input_tokens: cacheRead,
  cache_creation_input_tokens: cacheWrite,
  model,
})

// A warm main request answered at T0 - 69m, then (optionally) one after
// `gapMin` idle minutes.
function steps(second?: { gapMin: number; u: ReturnType<typeof step> }): OvertoneSteps {
  let s = noteMainStep(EMPTY_STEPS, step(2_000, 196_000, 2_000), T0 - 70 * M, T0 - 69 * M)
  if (second) s = noteMainStep(s, second.u, T0 - 69 * M + second.gapMin * M, T0 - 69 * M + second.gapMin * M + 30_000)
  return s
}

function worker(over: Partial<OvertoneWorker> & { id: string }): OvertoneWorker {
  return { label: over.id, type: 'agent', status: 'running', firstSeenMs: T0 - 134_000, fromSpawn: true, tools: 0, pending: {}, ...over }
}

function snap(over: Partial<Snapshot> = {}): Snapshot {
  return {
    nowMs: T0,
    offsetMin: 0,
    isWorking: false,
    reading: { tokens: 212_000, window: 1_000_000, percent: 21 },
    model: { asked: 'Opus 5.5', seen: 'claude-opus-5-5', effort: 'xhigh', steps: 3 },
    usage: {
      rateLimits: [
        // opened 08:55, resets 13:55: 62% of the window gone at noon
        { kind: 'five_hour', percentUsed: 15, resetsAt: iso(T0 + 115 * M) },
        // resets in 6h 15m: 96% of the week gone
        { kind: 'seven_day', percentUsed: 85, resetsAt: iso(T0 + 375 * M) },
      ],
      measuredMs: T0,
    },
    steps: steps(),
    workers: { byId: {} },
    partners: null,
    ...over,
  }
}

// idle past the assumed 1-hour life
const COLD = steps({ gapMin: 61, u: step(1_000, 100_000, 125_000) })

describe('pace and the even-pace projection', () => {
  test('ahead of pace: runs out before the reset, how early, where it would land', () => {
    const p = pace({ kind: 'five_hour', percentUsed: 60, resetsAt: iso(T0 + 3 * H) }, T0, 5 * H)
    expect(p?.evenPct).toBe(40)
    expect(p?.projectedPct).toBe(150)
    expect(p?.runOutMs).toBe(T0 + 80 * M)
    expect(p?.earlyMs).toBe(100 * M)
  })

  test('the picture: 5h on pace, the week landing at 88%', () => {
    const five = pace({ kind: 'five_hour', percentUsed: 15, resetsAt: iso(T0 + 115 * M) }, T0, 5 * H)
    expect([five?.evenPct, five?.projectedPct, five?.runOutMs]).toEqual([62, 24, undefined])
    const week = pace({ kind: 'seven_day', percentUsed: 85, resetsAt: iso(T0 + 375 * M) }, T0, 7 * 24 * H)
    expect([week?.evenPct, week?.projectedPct, week?.runOutMs]).toEqual([96, 88, undefined])
  })

  test('too early, no reset time, or used up: no projection', () => {
    expect(pace({ kind: 'five_hour', percentUsed: 20, resetsAt: iso(T0 + 5 * H - 5 * M) }, T0, 5 * H)?.projectedPct).toBeUndefined()
    expect(pace({ kind: 'five_hour', percentUsed: 20 }, T0, 5 * H)).toEqual({ percent: 20, isOut: false })
    expect(pace({ kind: 'five_hour', percentUsed: 100, resetsAt: iso(T0 + H) }, T0, 5 * H)?.isOut).toBe(true)
  })
})

// A bar as the collapsed line draws it: `n` filled cells of `w`.
const B = (n: number, w = 10) => '◼'.repeat(w)

describe('collapsed line', () => {
  test('the picture: three bars of what is left, then the cache hit', () => {
    // 21% of the window used, 5h 15% used, 7d 85% used
    expect(lineText(collapsedLine(snap(), 220))).toBe(`ctx ${B(8)}  │  5h ${B(9)}  │  7d ${B(2)}  │  cache 98%`)
  })

  test('colours: filled cells in the tone, the rest dim; ctx amber past 200k, 5h green, 7d amber; no dollars', () => {
    const line = collapsedLine(snap(), 220)
    const toned = line.filter(s => s.tone && s.tone !== 'dim').map(s => [s.text, s.tone])
    expect(toned).toEqual([
      [B(8, 8), 'warning'],
      [B(9, 9), 'success'],
      [B(2, 2), 'warning'],
      ['98%', 'success'],
    ])
    expect(line.filter(s => s.tone === 'dim' && s.text.startsWith('◼')).length).toBe(3)
    expect(lineText(line)).not.toMatch(/\$/)
  })

  test('the text moved out: no tokens, state words, run-out, lands, resets or key hint', () => {
    const run = snap({ usage: { rateLimits: [{ kind: 'five_hour', percentUsed: 82, resetsAt: iso(T0 + 3 * H) }, { kind: 'seven_day', percentUsed: 85, resetsAt: iso(T0 + 375 * M) }], measuredMs: T0 } })
    for (const s of [snap(), run]) {
      const text = lineText(collapsedLine(s, 400))
      expect(text).not.toMatch(/212k|switch|keep working|out ~|▲|lands|resets|click or|ctrl\+x b/)
    }
  })

  test('ctx amber while mostly free: 316k of 1M leaves 68%, past 200k is switch at a break', () => {
    const line = collapsedLine(snap({ reading: { tokens: 316_000, window: 1_000_000, percent: 32 } }), 220)
    expect(lineText(line).startsWith(`ctx ${B(7)}  │`)).toBe(true)
    expect(line[1]).toEqual({ text: B(7, 7), tone: 'warning' })
    // red at 80%+ (switch now), green while keep working
    expect(collapsedLine(snap({ reading: { tokens: 820_000, window: 1_000_000, percent: 82 } }), 220)[1]).toEqual({ text: B(2, 2), tone: 'error' })
    expect(collapsedLine(snap({ reading: { tokens: 119_000, window: 1_000_000, percent: 12 } }), 220)[1]).toEqual({ text: B(9, 9), tone: 'success' })
  })

  test('the 5-hour bar keeps its pace tone: amber on a projected run-out, red at 95%+', () => {
    const fiveAt = (percentUsed: number) => {
      const line = collapsedLine(snap({ usage: { rateLimits: [{ kind: 'five_hour', percentUsed, resetsAt: iso(T0 + 3 * H) }], measuredMs: T0 } }), 220)
      const i = line.findIndex(s => s.text === '5h ')
      return line[i + 1]
    }
    expect(fiveAt(82)).toEqual({ text: B(2, 2), tone: 'warning' })
    expect(fiveAt(95)).toEqual({ text: B(1, 1), tone: 'error' })
  })

  test('the weekly bar: the worse of its used tone and where it lands at reset', () => {
    const sevenAt = (percentUsed: number, resetsInMs: number) => {
      const line = collapsedLine(snap({ usage: { rateLimits: [{ kind: 'seven_day', percentUsed, resetsAt: iso(T0 + resetsInMs) }], measuredMs: T0 } }), 220)
      const i = line.findIndex(s => s.text === '7d ')
      return line[i + 1]
    }
    // half the week gone, 60% used: lands ≈120%, red though half is left
    expect(sevenAt(60, 84 * H)).toEqual({ text: B(4, 4), tone: 'error' })
    // just reset: no landing yet, the used figure's green
    expect(sevenAt(0, 7 * 24 * H - M)).toEqual({ text: B(10, 10), tone: 'success' })
    expect(sevenTone(undefined)).toBe('dim')
  })

  test('no reading: the label and a dim dash, as the cache cell has', () => {
    const line = collapsedLine(snap({ reading: null, usage: null, steps: EMPTY_STEPS }), 220)
    expect(lineText(line)).toBe('ctx —  │  5h —  │  7d —  │  cache —')
    expect(line.every(s => s.tone === 'dim')).toBe(true)
  })

  test('the cache hit, always: green from 80%, amber from 50%, red below, — before a reading', () => {
    const at = (cacheRead: number, cacheWrite: number) =>
      collapsedLine(snap({ steps: noteMainStep(EMPTY_STEPS, step(1_000, cacheRead, cacheWrite), T0 - 2 * M, T0 - M) }), 220).find(sg => sg.bold && /^\d+%$/.test(sg.text))
    expect(at(97_000, 2_000)).toEqual({ text: '97%', tone: 'success', bold: true })
    expect(at(60_000, 39_000)).toEqual({ text: '60%', tone: 'warning', bold: true })
    expect(at(30_000, 69_000)).toEqual({ text: '30%', tone: 'error', bold: true })
    expect(lineText(collapsedLine(snap({ steps: EMPTY_STEPS }), 220))).toMatch(/│ {2}cache —$/)
    // the warm-to-cold alert says it instead; so does "remains cold"
    expect(lineText(collapsedLine(snap({ steps: COLD }), 400)).match(/cache/g)).toHaveLength(1)
    const remains = noteMainStep(COLD, step(1_000, 100_000, 125_000), T0 - 6 * M, T0 - 5 * M)
    expect(lineText(collapsedLine(snap({ steps: remains }), 400)).match(/cache/g)).toHaveLength(1)
  })

  test('red alerts are appended only while they fire', () => {
    const w: OvertoneWorkers = { byId: { b: worker({ id: 'b', label: 'Builder', asked: 'opus', seen: 'claude-sonnet-5-5' }) } }
    const p: OvertonePartners = {
      polledMs: T0,
      rows: [{ id: 'r1', alias: 'codex-partner', provider: 'codex', doing: 'review', createdMs: T0 - 14 * M, state: 'waiting' }],
    }
    const line = collapsedLine(snap({ steps: COLD, workers: w, partners: p }), 400)
    expect(lineText(line)).toBe(
      `ctx ${B(8)}  │  5h ${B(9)}  │  7d ${B(2)}  │  cache 44% ▼ re-sent 126k  │  worker on sonnet, asked opus  │  codex-partner waiting 14m`,
    )
    expect(line.filter(s => s.tone === 'error').map(s => s.text)).toEqual(['cache 44% ▼ re-sent 126k', 'worker on sonnet, asked opus', 'codex-partner waiting 14m'])
    expect(lineText(collapsedLine(snap(), 400))).not.toMatch(/▼|worker|waiting/)
  })

  test('narrow: bars shrink 10 → 6 → 4 before any group goes; never past its room; ctx stays', () => {
    const at = (cols: number) => lineText(collapsedLine(snap(), cols))
    for (let cols = 200; cols >= 25; cols--) expect(lineWidth(collapsedLine(snap(), cols))).toBeLessThanOrEqual(cols - BUTTON_ROOM)
    expect(at(81)).toBe(`ctx ${B(8)}  │  5h ${B(9)}  │  7d ${B(2)}  │  cache 98%`)
    expect(at(80)).toBe(`ctx ${B(5, 6)}  │  5h ${B(5, 6)}  │  7d ${B(1, 6)}  │  cache 98%`)
    expect(at(68)).toBe(`ctx ${B(3, 4)}  │  5h ${B(3, 4)}  │  7d ${B(1, 4)}  │  cache 98%`)
    expect(at(62)).toBe(`ctx ${B(3, 4)}  │  5h ${B(3, 4)}  │  7d ${B(1, 4)}`)
    expect(at(48)).toBe(`ctx ${B(3, 4)}  │  5h ${B(3, 4)}`)
    expect(at(36)).toBe(`ctx ${B(3, 4)}`)
    // an alert stays: short wording while it fits, else folded into ⚠ N
    expect(lineText(collapsedLine(snap({ steps: COLD }), 41))).toBe(`ctx ${B(3, 4)}  │  cache 44% ▼`)
    expect(lineText(collapsedLine(snap({ steps: COLD }), 40))).toBe(`ctx ${B(3, 4)}  │  ⚠ 1`)
  })

  // Three alerts firing: the cold cache, a worker on the wrong model, a partner waiting.
  const ALERTS3 = snap({
    steps: COLD,
    workers: { byId: { b: worker({ id: 'b', label: 'Builder', asked: 'opus', seen: 'claude-sonnet-5-5' }) } },
    partners: { polledMs: T0, rows: [{ id: 'r1', alias: 'codex-partner', provider: 'codex', doing: 'review', createdMs: T0 - 14 * M, state: 'waiting' }] },
  })

  test('alerts never hidden: short wording, then one red ⚠ N, then the ctx label and bar go; ⚠ N is the floor', () => {
    const at = (cols: number) => lineText(collapsedLine(ALERTS3, cols))
    expect(alertsOf(ALERTS3).map(a => a.short)).toEqual(['cache 44% ▼', 'wrong model', 'codex-partner 14m'])
    // 40 columns: the short wording has no room, so ⚠ 3 stands for all three
    expect(at(40)).toBe(`ctx ${B(3, 4)}  │  ⚠ 3`)
    expect(collapsedLine(ALERTS3, 40).at(-1)).toEqual({ text: alertMark(3), tone: 'error', bold: true })
    expect(at(29)).toBe(`${B(3, 4)}  │  ⚠ 3`)
    expect(at(20)).toBe('⚠ 3')
    // below the floor: ⚠ 3 still, the one documented case past the room
    expect(at(8)).toBe('⚠ 3')
    expect(at(0)).toBe('⚠ 3')
  })

  test('tiny widths: never past the room, with and without alerts, but for the documented ⚠ N floor', () => {
    const shorts = alertsOf(ALERTS3).map(a => a.short)
    for (const cols of [40, 30, 20, 10, 5, 0]) {
      const room = Math.max(0, cols - BUTTON_ROOM)
      const fired = collapsedLine(ALERTS3, cols)
      const text = lineText(fired)
      // every alert represented: by its wording or by the mark
      expect(text.includes(alertMark(3)) || shorts.every(t => text.includes(t))).toBe(true)
      if (text !== alertMark(3)) expect(lineWidth(fired)).toBeLessThanOrEqual(room)
      expect(lineWidth(collapsedLine(snap(), cols))).toBeLessThanOrEqual(room)
    }
  })

  test('no alerts at tiny widths: the ctx bar alone, then the bare bar, then an empty line', () => {
    const at = (cols: number) => lineText(collapsedLine(snap(), cols))
    expect(at(25)).toBe(`ctx ${B(3, 4)}`)
    expect(at(21)).toBe(B(3, 4))
    expect(collapsedLine(snap(), 20)).toEqual([])
    expect(collapsedLine(snap(), 0)).toEqual([])
  })

  test('the band toggles; the key is an engine action whose chord is ctrl+x b', () => {
    expect(toggleView(undefined)).toEqual({ expanded: true })
    expect(toggleView({ expanded: true })).toEqual({ expanded: false })
    expect([BAND_ACTION, BAND_CHORD]).toEqual(['app:cycleDiffBase', 'ctrl+x b'])
  })
})

describe('the cache', () => {
  test('per main request: hit, the one before, idle time, a model switch', () => {
    const s = COLD
    expect(s.requests).toBe(2)
    expect(s.prevHit).toBe(98)
    expect(s.gapMs).toBe(61 * M)
    expect(hitPct(s.last as never)).toBe(44)
    expect(s.trend).toEqual([98, 44])
    const switched = noteMainStep(steps(), step(1_000, 0, 200_000, 100, 'claude-sonnet-5-5'), T0 - 68 * M, T0 - 67 * M)
    expect(switched.modelChanged).toBe(true)
  })

  test('the cache life: 1 hour assumed; what Claude Code reports, when it does', () => {
    expect(cacheLife(undefined)).toEqual({ ms: H, label: '1h cache assumed', reported: false, warnMs: 5 * M })
    expect(cacheLife('1h')).toEqual({ ms: H, label: '1h cache', reported: true, warnMs: 5 * M })
    expect(cacheLife('5m')).toEqual({ ms: 5 * M, label: '5m cache', reported: true, warnMs: M })
  })

  test('cold: hit under 80% after a warmer prompt; idle when the gap passed the cache life', () => {
    expect(cacheAlert(COLD, 212_000, true, T0)?.cold).toEqual({ hit: 44, was: 98, resent: 126_000, case: 'idle', gapMs: 61 * M })
    // six idle minutes: past a reported 5-minute life, within the assumed hour
    const six = steps({ gapMin: 6, u: step(1_000, 100_000, 125_000) })
    expect(cacheAlert(six, 212_000, true, T0)?.cold?.case).toBe('unknown')
    expect(cacheAlert(six, 212_000, true, T0, cacheLife('5m'))?.cold?.case).toBe('idle')
    expect(cacheAlert(COLD, 212_000, true, T0, cacheLife('1h'))?.cold?.case).toBe('idle')
    const switched = noteMainStep(steps(), step(1_000, 0, 200_000, 100, 'claude-sonnet-5-5'), T0 - 68 * M, T0 - 67 * M)
    expect(cacheAlert(switched, 212_000, true, T0)?.cold?.case).toBe('model switched')
  })

  test('only the warm-to-cold crossing alerts; the next cold prompt says once it remains cold; then quiet', () => {
    const second = noteMainStep(COLD, step(1_000, 100_000, 125_000), T0 - 6 * M, T0 - 5 * M)
    expect(second.coldStreak).toBe(2)
    expect(cacheAlert(second, 212_000, true, T0)?.cold).toMatchObject({ hit: 44, remains: true })
    expect(alertsOf(snap({ steps: second })).map(a => a.text)).toEqual(['cache remains cold (44%)'])
    expect(dashboard(snap({ steps: second }), 150).cache?.lines.map(lineText)).toEqual([
      'The cache remains cold (44% hit, re-sent 126k); said once, quiet until it is warm again.',
    ])
    const third = noteMainStep(second, step(1_000, 100_000, 125_000), T0 - 4 * M, T0 - 3 * M)
    expect(third.coldStreak).toBe(3)
    expect(cacheAlert(third, 212_000, true, T0)).toBeUndefined()
    // warm again, then cold: a new crossing alerts again
    const warm = noteMainStep(third, step(2_000, 196_000, 2_000), T0 - 2 * M, T0 - 110_000)
    expect(warm.coldStreak).toBeUndefined()
    const again = noteMainStep(warm, step(1_000, 100_000, 125_000), T0 - M, T0 - 50_000)
    expect(cacheAlert(again, 212_000, true, T0)?.cold?.remains).toBeUndefined()
    // a session that starts cold and stays cold never crossed: no alert
    const coldStart = noteMainStep(noteMainStep(EMPTY_STEPS, step(1_000, 0, 200_000), T0 - 3 * M, T0 - 2 * M), step(1_000, 50_000, 150_000), T0 - M, T0 - 50_000)
    expect(cacheAlert(coldStart, 212_000, true, T0)).toBeUndefined()
  })

  test('a crossing suppressed for a small re-send: the next larger cold prompt is the first alert', () => {
    const small = steps({ gapMin: 61, u: step(1_000, 2_000, 5_000) })
    expect([small.coldStreak, small.coldPhase, small.coldAlert]).toEqual([1, 0, undefined])
    expect(cacheAlert(small, 212_000, true, T0)).toBeUndefined()
    const large = noteMainStep(small, step(1_000, 100_000, 125_000), T0 - 6 * M, T0 - 5 * M)
    expect([large.coldStreak, large.coldAlert]).toEqual([2, 'first'])
    expect(cacheAlert(large, 212_000, true, T0)?.cold?.remains).toBeUndefined()
    expect(alertsOf(snap({ steps: large })).map(a => a.text)).toEqual(['cache 44% ▼ re-sent 126k'])
    const next = noteMainStep(large, step(1_000, 100_000, 125_000), T0 - 4 * M, T0 - 3 * M)
    expect(next.coldAlert).toBe('remains')
    const after = noteMainStep(next, step(1_000, 100_000, 125_000), T0 - 2 * M, T0 - M)
    expect(after.coldAlert).toBeUndefined()
  })

  test('quiet: a warm cache, the first prompt of a session, or a small re-send', () => {
    expect(cacheAlert(steps(), 212_000, true, T0)).toBeUndefined()
    const firstOnly = noteMainStep(EMPTY_STEPS, step(1_000, 0, 200_000), T0 - 2 * M, T0 - M)
    expect(cacheAlert(firstOnly, 212_000, true, T0)).toBeUndefined()
    const small = steps({ gapMin: 6, u: step(1_000, 2_000, 5_000) })
    expect(cacheAlert(small, 212_000, true, T0)).toBeUndefined()
  })

  test('about to expire: idle, a big context, the last 5 minutes of the assumed hour, counted from the request', () => {
    // sent 56m ago (answered 55m10s ago): 4m of the hour left
    const s = noteMainStep(EMPTY_STEPS, step(2_000, 196_000, 2_000), T0 - 56 * M, T0 - 55 * M - 10_000)
    expect(cacheAlert(s, 212_000, false, T0)).toEqual({ expiresInMs: 240_000, untilMs: T0 + 240_000 })
    // a long request: its life began when it was sent, so it already lapsed
    const long = noteMainStep(EMPTY_STEPS, step(2_000, 196_000, 2_000), T0 - 62 * M, T0 - 56 * M)
    expect(cacheAlert(long, 212_000, false, T0)).toBeUndefined()
    expect(cacheAlert(s, 212_000, true, T0)).toBeUndefined()
    expect(cacheAlert(s, 20_000, false, T0)).toBeUndefined()
    expect(cacheAlert(s, 212_000, false, T0 - 2 * M)).toBeUndefined()
    expect(cacheAlert(s, 212_000, false, T0 + 5 * M)).toBeUndefined()
    // a reported 5-minute life: its last minute
    const short = noteMainStep(EMPTY_STEPS, step(2_000, 196_000, 2_000), T0 - 4 * M - 10_000, T0 - 4 * M)
    expect(cacheAlert(short, 212_000, false, T0, cacheLife('5m'))).toEqual({ expiresInMs: 50_000, untilMs: T0 + 50_000 })
    expect(cacheAlert(short, 212_000, false, T0)).toBeUndefined()
  })
})

describe('jobs', () => {
  test('asked vs saw: matches, wrong model, no response yet, waiting on you, returned not yet checked; effort only as sent', () => {
    let w: OvertoneWorkers = {
      byId: {
        r: worker({ id: 'r', label: 'Reviewer', activity: 'checking the diff', firstSeenMs: T0 - 134_000 }),
        b: worker({ id: 'b', label: 'Builder', activity: 'writing dashboard.py', firstSeenMs: T0 - 401_000 }),
        x: worker({ id: 'x', label: 'Explorer', status: 'completed', firstSeenMs: T0 - 300_000, endedMs: T0 - 118_000 }),
        e: worker({ id: 'e', label: 'Effort', firstSeenMs: T0 - 60_000 }),
        q: worker({ id: 'q', label: 'Asker', firstSeenMs: T0 - 30_000, blocked: { what: 'wants to run Bash ls', sinceMs: T0, toolUseId: 'u' } }),
        old: worker({ id: 'old', label: 'Old', status: 'completed', firstSeenMs: T0 - 3 * H, endedMs: T0 - 2 * H }),
      },
    }
    w = noteAsked(w, 'r', { type: 'kerd:sonnet-high' })
    w = noteWorkerModel(w, 'r', 'claude-sonnet-5-5', 'high')
    w = noteWorkerSeen(w, 'r', 'claude-sonnet-5-5')
    w = noteAsked(w, 'b', { model: 'opus', type: 'general-purpose' })
    w = noteWorkerModel(w, 'b', 'claude-opus-5-5', 'xhigh')
    w = noteWorkerSeen(w, 'b', 'claude-sonnet-5-5')
    w = noteAsked(w, 'e', { type: 'kerd:haiku' })
    w = noteAsked(w, 'e', { type: 'kerd:opus-high' })
    w = noteWorkerModel(w, 'e', 'claude-opus-5-5', 'low')
    // the main loop last stepped 10 minutes ago: Explorer returned since, Old before
    const rows = jobsOf(snap({ workers: w, steps: noteMainStep(EMPTY_STEPS, step(1, 1, 1), T0 - 10 * M, T0 - 9 * M) }))
    // asked is the requested pair, intact; saw only the answering model; what
    // was sent, where it differs from the ask, is a separate note
    expect(rows.map(r => [r.job, r.doing, r.asked, r.saw, r.elapsed, r.state, r.sent])).toEqual([
      ['Builder', 'writing dashboard.py', 'Opus', 'Sonnet 5.5', '6m 41s', 'wrong model', 'sent xhigh'],
      ['Explorer', 'returned', '—', '—', '3m 02s', 'returned, not yet checked', undefined],
      ['Reviewer', 'checking the diff', 'Sonnet · high', 'Sonnet 5.5', '2m 14s', 'matches', undefined],
      ['Effort', 'started', 'Opus · high', '—', '1m 00s', 'running', 'sent low'],
      ['Asker', 'wants to run Bash ls', '—', '—', '30s', 'waiting on you', undefined],
    ])
  })

  test('the sent note: only what differs from the ask, never merged into it', () => {
    const base = worker({ id: 'a' })
    expect(sentNote({ ...base, asked: 'opus', askedEffort: 'high', model: 'claude-opus-5-5', effort: 'high' })).toBeUndefined()
    expect(sentNote({ ...base, asked: 'opus', askedEffort: 'high', model: 'claude-opus-5-5', effort: 'low' })).toBe('sent low')
    expect(sentNote({ ...base, asked: 'opus', askedEffort: 'high', model: 'claude-sonnet-5-5', effort: 'high' })).toBe('sent Sonnet 5.5 · high')
    expect(sentNote({ ...base, model: 'claude-opus-5-5' })).toBe('sent Opus 5.5')
    expect(sentNote(base)).toBeUndefined()
  })

  test('no response yet: running, saw —, never "matches" before the API answers', () => {
    let w: OvertoneWorkers = { byId: { a: worker({ id: 'a', label: 'A' }) } }
    w = noteAsked(w, 'a', { type: 'kerd:sonnet-high' })
    w = noteWorkerModel(w, 'a', 'claude-sonnet-5-5', 'high')
    const before = jobsOf(snap({ workers: w }))[0]
    expect([before?.asked, before?.saw, before?.state]).toEqual(['Sonnet · high', '—', 'running'])
    const after = jobsOf(snap({ workers: noteWorkerSeen(w, 'a', 'claude-sonnet-5-5') }))[0]
    expect([after?.saw, after?.state]).toEqual(['Sonnet 5.5', 'matches'])
    // nothing asked (no model on the call, not a kerd type): nothing to match;
    // what was sent shows as a note beside what answered
    const sent = noteWorkerSeen(noteWorkerModel({ byId: { b: worker({ id: 'b', label: 'B' }) } }, 'b', 'claude-opus-5-5', undefined), 'b', 'claude-sonnet-5-5')
    const row = jobsOf(snap({ workers: sent }))[0]
    expect([row?.asked, row?.saw, row?.state, row?.sent]).toEqual(['—', 'Sonnet 5.5', 'running', 'sent Opus 5.5'])
  })

  test('kerd agent types name their model and effort', () => {
    expect(kerdAsk('kerd:sonnet-high')).toEqual({ model: 'sonnet', effort: 'high' })
    expect(kerdAsk('kerd:haiku')).toEqual({ model: 'haiku' })
    expect(kerdAsk('kerd:effort-high')).toEqual({})
    expect(kerdAsk('Explore')).toEqual({})
    expect(prettyModel('claude-sonnet-5-5')).toBe('Sonnet 5.5')
    expect(prettyModel('Opus 5.5 (1M context)')).toBe('Opus 5.5')
    expect(prettyModel('haiku')).toBe('Haiku')
  })

  test('partner requests: this project, waiting up to 3h, replies for 15 minutes', () => {
    const aliases = aliasMap([
      { alias: 'codex-partner', provider: 'codex', id: 'sess-c', project: PROJECT },
      { junk: true },
      null,
    ])
    expect(aliases).toEqual({ 'codex:sess-c': 'codex-partner' })
    const rec = (over: Record<string, unknown>) => ({
      request_id: 'r1',
      provider: 'codex',
      session: 'sess-c',
      project: PROJECT,
      role: 'review of overtone 0.3.1',
      status: 'submitted-unconfirmed',
      created_at: (T0 - 14 * M) / 1000,
      prompt: 'SECRET PROMPT TEXT',
      ...over,
    })
    const waiting = partnerRow(rec({}), `${PROJECT}/`, aliases, T0)
    expect(waiting).toEqual({ id: 'r1', alias: 'codex-partner', provider: 'codex', doing: 'review of overtone 0.3.1', createdMs: T0 - 14 * M, state: 'waiting' })
    expect(JSON.stringify(waiting)).not.toContain('SECRET')
    expect(partnerRow(rec({ status: 'reply-received', received_at: (T0 - 5 * M) / 1000 }), PROJECT, aliases, T0)?.state).toBe('received')
    expect(partnerRow(rec({ status: 'reply-received', received_at: (T0 - 20 * M) / 1000 }), PROJECT, aliases, T0)).toBeUndefined()
    expect(partnerRow(rec({ project: '/elsewhere' }), PROJECT, aliases, T0)).toBeUndefined()
    expect(partnerRow(rec({ created_at: (T0 - 4 * H) / 1000 }), PROJECT, aliases, T0)).toBeUndefined()
    expect(partnerRow(rec({ kind: 'arrival-notice' }), PROJECT, aliases, T0)).toBeUndefined()
    expect(partnerRow(rec({ reply_expected: false }), PROJECT, aliases, T0)).toBeUndefined()
    expect(partnerRow(rec({ status: 'delivery-uncertain' }), PROJECT, aliases, T0)?.state).toBe('uncertain')
    expect(partnerRow(rec({ session: 'other-session-id', role: '' }), PROJECT, aliases, T0)?.alias).toBe('codex other-se')
    expect(partnerRow(rec({ session: 'other-session-id', role: '' }), PROJECT, aliases, T0)?.doing).toBe('a request')
    const p: OvertonePartners = { polledMs: T0, rows: [waiting as never] }
    expect(jobsOf(snap({ partners: p })).map(r => [r.job, r.doing, r.asked, r.saw, r.elapsed, r.state])).toEqual([
      ['codex-partner', 'review of overtone 0.3.1', 'Codex session', '—', '14m', 'waiting on a reply'],
    ])
  })
})

describe('the dashboard', () => {
  test('panels in order: Context, 5-hour, Weekly, as pictured', () => {
    const d = dashboard(snap(), 150)
    expect(d.perRow).toBe(3)
    expect(d.panels.map(p => p.key)).toEqual(['context', 'five', 'seven'])
    expect(lineText(d.header)).toBe(' · Opus 5.5 · xhigh')
    expect(d.hint).toBe('click or ctrl+x b collapses')
    const [ctx, five, week] = d.panels
    expect(lineText(ctx?.right ?? [])).toBe('212k / 1M')
    expect(ctx?.lines.map(lineText).slice(1)).toEqual([
      'keep · ▸ switch at a break · switch now',
      'break: from 200k or 60% · now: from 80%',
      '212k tokens re-sent on every call',
    ])
    expect(ctx?.tone).toBe('warning')
    expect(lineText(five?.right ?? [])).toBe('resets in 1h 55m')
    expect(five?.lines.map(lineText).slice(2)).toEqual(['✓ no ▲ run-out before the reset', 'resets 13:55 · room to fan out'])
    expect(lineText(week?.title ?? [])).toBe('Weekly (7 days)')
    expect(week?.lines.map(lineText).slice(2)).toEqual(['lands ≈88% at reset', 'headroom left: ≈12% of the week'])
    expect(lineText(five?.lines[1] ?? [])).toMatch(/╵ even pace 62%$/)
    expect(lineText(week?.lines[1] ?? [])).toMatch(/even pace 96% ╵$/)
  })

  test('no jobs, a calm cache, nothing due: no jobs card, no cache card, no next line', () => {
    const calm = snap({ reading: { tokens: 50_000, window: 1_000_000, percent: 5 } })
    const d = dashboard(calm, 150)
    expect(d.jobs).toEqual([])
    expect(d.cache).toBeUndefined()
    expect(d.next).toBeUndefined()
  })

  test('the cache card in plain words: what was re-sent, the case, what to do', () => {
    const d = dashboard(snap({ steps: COLD }), 150)
    expect(lineText(d.cache?.right ?? [])).toBe('▼ case: idle')
    expect(d.cache?.lines.map(lineText)).toEqual([
      'Last prompt re-sent 126k tokens without the cache (44% hit, was 98%).',
      "▸ Idle past the cache's life (1h 1m idle) → every next prompt starts cold: at a break, Switch Out rather than continue a big context.",
      '  Instructions, tools or the model changed mid-session → a one-off; carry on.',
    ])
    const unknown = dashboard(snap({ steps: steps({ gapMin: 2, u: step(1_000, 100_000, 125_000) }) }), 150)
    expect(lineText(unknown.cache?.right ?? [])).toBe('▼ cause unknown')
    const expiring = noteMainStep(EMPTY_STEPS, step(2_000, 196_000, 2_000), T0 - 56 * M, T0 - 55 * M - 10_000)
    const e = dashboard(snap({ steps: expiring }), 150)
    expect(e.cache?.lines.map(lineText)).toEqual(['≈ 4m until the cache expires — send the next prompt now, or Switch Out. (at 12:04; 1h cache assumed)'])
    // where Claude Code reported the life, it is named without "assumed"
    const short = noteMainStep(EMPTY_STEPS, step(2_000, 196_000, 2_000), T0 - 4 * M - 10_000, T0 - 4 * M)
    const r = dashboard(snap({ steps: short, cacheTtl: '5m' }), 150)
    expect(r.cache?.lines.map(lineText)).toEqual(['≈ 50s until the cache expires — send the next prompt now, or Switch Out. (at 12:00; 5m cache)'])
  })

  test('next: worst first, two joined', () => {
    const w: OvertoneWorkers = { byId: { b: worker({ id: 'b', label: 'Builder', asked: 'opus', seen: 'claude-sonnet-5-5' }) } }
    expect(nextText(nextNote(snap({ workers: w })) as never)).toBe('Context 212k — switch at a break; the Builder is on the wrong model')
    expect(nextNote(snap({ reading: { tokens: 850_000, window: 1_000_000, percent: 85 } }))?.lead).toBe('Context 850k')
    const run = snap({ usage: { rateLimits: [{ kind: 'five_hour', percentUsed: 82, resetsAt: iso(T0 + 3 * H) }], measuredMs: T0 } })
    expect(nextText(nextNote(run) as never)).toBe('5-hour runs out ≈ 12:26 — hold big jobs; a good point to Switch Out; context 212k, switch at a break')
  })

  test('a short band keeps workers first: outer frame, then cache, then next; card frames last', () => {
    const w = { byId: { a: worker({ id: 'a', label: 'A' }) } }
    const s = snap({ steps: COLD, workers: w })
    const tall = dashboard(s, 150)
    // outer 2 + header 1 + jobs card (2 frame + title + columns + 1 job) 5 + cache (2 + title + 3) 6 + next 1
    expect([tall.outerBorder, tall.panelBorder, dashboardRows(tall)]).toEqual([true, true, 15])
    const noOuter = dashboard(s, 150, 13)
    expect([noOuter.outerBorder, noOuter.cache?.lines.length, dashboardRows(noOuter)]).toEqual([false, 3, 13])
    const shrunk = dashboard(s, 150, 11)
    expect([shrunk.cache?.lines.length, dashboardRows(shrunk)]).toEqual([1, 11])
    const noCache = dashboard(s, 150, 6)
    expect([noCache.cache, noCache.next, noCache.panelBorder, noCache.jobs.length]).toEqual([undefined, undefined, true, 1])
    const tiny = dashboard(s, 150, 5)
    expect(tiny.panelBorder).toBe(false)
    // /overtone still prints the context, 5-hour and weekly panels
    expect(usageText(s)).toMatch(/^Context — /m)
    expect(perRowFor(124)).toBe(3)
    expect(perRowFor(80)).toBe(2)
    expect(perRowFor(79)).toBe(1)
  })

  test('jobs beyond the rows the band offers fold into "+K more", the worst kept', () => {
    const byId: Record<string, OvertoneWorker> = {}
    for (let i = 0; i < 8; i++) byId[`w${i}`] = worker({ id: `w${i}`, label: `Job ${i}`, firstSeenMs: T0 - (10 - i) * M })
    byId.w6 = { ...(byId.w6 as OvertoneWorker), asked: 'opus', seen: 'claude-sonnet-5-5' }
    const s = snap({ workers: { byId } })
    const all = dashboard(s, 150)
    expect([all.jobs.length, all.jobsHidden]).toEqual([8, 0])
    const short = dashboard(s, 150, 8)
    expect(short.panelBorder).toBe(true)
    expect(dashboardRows(short)).toBeLessThanOrEqual(8)
    expect(short.jobsHidden).toBe(8 - short.jobs.length)
    expect(short.jobs.map(j => j.job)).toContain('Job 6')
    expect(usageText(s).includes('+')).toBe(false)
    // A hard cap from three rows up, with the worker-list note too: the jobs
    // card sheds its column-header row and folds "+K more" and the note into
    // its title row; the worst job stays.
    const noted = snap({ workers: { byId, error: 'read failed' } })
    for (const snapshot of [s, noted]) {
      for (let rows = 3; rows <= 16; rows++) {
        const d = dashboard(snapshot, 150, rows)
        expect([rows, dashboardRows(d) <= rows]).toEqual([rows, true])
        expect([rows, d.jobs.length + d.jobsHidden, d.jobs.map(j => j.job).includes('Job 6')]).toEqual([rows, 8, true])
      }
    }
    const five = dashboard(noted, 150, 5)
    expect([five.jobsCompact, five.jobsNote, dashboardRows(five)]).toEqual([true, 'worker status unavailable · read failed', 5])
  })

  test('the even-pace mark: caption after it, or before it when there is no room', () => {
    expect(lineText(paceMark(20, 30, 44))).toBe('      ╵ even pace 20%')
    expect(lineText(paceMark(96, 30, 40))).toBe('               even pace 96% ╵')
  })
})

describe('what Claude and scripts read', () => {
  test('the context line: the trimmed figures; alerts and next only when they fire', () => {
    const calm = snap({ reading: { tokens: 50_000, window: 1_000_000, percent: 5 } })
    expect(contextSummary(calm)).toBe(
      'usage: ctx 50k/1M (5%), keep working · 5h 15% resets 13:55 · 7d 85%, lands ≈88% at reset, resets 18:15 · cache 98%',
    )
    const w: OvertoneWorkers = { byId: { b: worker({ id: 'b', label: 'Builder', asked: 'opus', seen: 'claude-sonnet-5-5' }) } }
    expect(contextSummary(snap({ steps: COLD, workers: w }))).toBe(
      'usage: ctx 212k/1M (21%), switch at a break · 5h 15% resets 13:55 · 7d 85%, lands ≈88% at reset, resets 18:15 · alerts: cache 44% hit (was 98%), re-sent 126k (case: idle); worker Builder on Sonnet 5.5, asked Opus\n' +
        'usage next: Context 212k — switch at a break; the Builder is on the wrong model',
    )
    expect(contextSummary(snap({ reading: null, usage: null }))).toBeUndefined()
    expect(hasFigures(snap({ reading: null, usage: null }))).toBe(false)
  })

  test('the snapshot: Claude Code figures under exact, projections under estimates; no dollars, no logs', () => {
    const j = snapshotJson(snap({ steps: COLD }), 's-1') as Record<string, Record<string, unknown>>
    expect(j.source as unknown).toBe('overtone 0.4.1')
    expect(j.exact?.fiveHour).toEqual({ percent: 15, resetsAt: iso(T0 + 115 * M) })
    expect(j.estimates?.sevenDay).toEqual({ evenPacePercent: 96, projectedAtResetPercent: 88 })
    expect(j.estimates?.weeklyHeadroomPercent).toBe(12)
    expect(j.estimates?.cacheCase).toBe('idle')
    expect(j.exact?.cacheLastPrompt).toEqual({ hitPercent: 44, resent: 126_000, read: 100_000 })
    expect(j.estimates?.note).toBe('projections and the cache expiry (1h cache assumed) are estimates')
    expect(j.estimates?.cacheTtl).toBeNull()
    // the cache's life from when the last request was sent
    expect(j.estimates?.cacheExpiresAt).toBe(iso(T0 - 69 * M + 61 * M + H))
    expect((snapshotJson(snap({ cacheTtl: '5m' }), 's-1') as Record<string, Record<string, unknown>>).estimates?.cacheTtl).toBe('5m')
    expect(j.alerts as unknown).toEqual(['cache 44% hit (was 98%), re-sent 126k (case: idle)'])
    expect(JSON.stringify(j)).not.toMatch(/costUsd|today|last30Days|turns|logs/)
  })

  test('/overtone text: jobs, panels, alerts, next', () => {
    const t = usageText(snap({ steps: COLD }))
    expect(t.split('\n').slice(0, 3)).toEqual(['usage · Opus 5.5 · xhigh', 'Workers · no jobs running', 'Context — 212k / 1M'])
    expect(t).toContain('5-hour — resets in 1h 55m')
    expect(t).toContain('Cache — ▼ case: idle')
    expect(t).toContain('alert: cache 44% hit (was 98%), re-sent 126k (case: idle)')
    expect(t).toContain('next ▸ Context 212k — switch at a break; the cache went cold')
  })

  test('alerts list', () => {
    expect(alertsOf(snap())).toEqual([])
    expect(alertsOf(snap({ steps: COLD })).map(a => a.text)).toEqual(['cache 44% ▼ re-sent 126k'])
  })
})

describe('the jobs table', () => {
  test('columns fit the band; the job name gets more room on a wide one', () => {
    expect(jobColumns(120)).toEqual({ job: 35, asked: 20, saw: 20, elapsed: 9 })
    expect(jobColumns(150)).toEqual({ job: 65, asked: 20, saw: 20, elapsed: 9 })
    expect(cell('a very long job description here', 14)).toBe('a very long … ')
  })
})

describe('formatting', () => {
  test('tokens, spans, elapsed, gauges', () => {
    expect([fmtTok(950), fmtTok(2_900), fmtTok(126_000), fmtTok(1_000_000)]).toEqual(['950', '2.9k', '126k', '1M'])
    expect([fmtSpan(30_000), fmtSpan(14 * M), fmtSpan(134 * M), fmtSpan(78 * H)]).toEqual(['<1m', '14m', '2h 14m', '3d 6h'])
    expect([fmtElapsed(45_000), fmtElapsed(134_000), fmtElapsed(H + 5 * M)]).toEqual(['45s', '2m 14s', '1h 05m'])
    expect(gauge(60, 5)).toEqual({ fill: '███', rest: '░░' })
  })
})
