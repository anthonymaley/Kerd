// overtone 0.4's usage logic: pure, no `$`, nothing mutable at module level.
// The usage band (usage.tsx), register.tsx and the tests import from here.
//
// Only what drives a decision is kept (dashboard-v3): context tokens and the
// switch rule, the 5-hour and weekly windows with their projections, a row
// per job (workers and Kerd Agent partner requests), and the cache only when
// it went cold or is about to. Every figure is Claude Code's own, or worked
// out from it (marked ≈); partner rows come from Kerd Agent's request
// records. No session-log scan, no dollars.

import type {
  OvertoneCounts,
  OvertoneLimit,
  OvertoneModel,
  OvertonePartnerRow,
  OvertonePartners,
  OvertoneReading,
  OvertoneSteps,
  OvertoneUsage,
  OvertoneView,
  OvertoneWorker,
  OvertoneWorkers,
} from '../types'
import { EMPTY_MODEL, EMPTY_WORKERS, compareModels, isActive, normModel, readContext } from './logic'
import type { BandState } from './logic'

// ---------------------------------------------------------------------------
// Segments: what the hook draws, as plain data
// ---------------------------------------------------------------------------

// `success`, `warning`, `error` are the host's theme keys (colour follows
// light and dark); `dim` and `plain` carry no colour.
export type UTone = 'dim' | 'plain' | 'success' | 'warning' | 'error'
export type USeg = { text: string; tone?: UTone; bold?: boolean }
export type ULine = USeg[]

const sg = (text: string, tone?: UTone, bold?: boolean): USeg =>
  bold ? { text, tone, bold } : tone ? { text, tone } : { text }

export const lineText = (l: ULine): string => l.map(s => s.text).join('')
export const lineWidth = (l: ULine): number => [...lineText(l)].length

// ---------------------------------------------------------------------------
// Empty values, key and expand state
// ---------------------------------------------------------------------------

export const EMPTY_STEPS: OvertoneSteps = { requests: 0, trend: [] }
export const EMPTY_VIEW: OvertoneView = { expanded: false }
export const TREND_KEEP = 24

// The band Button's engine action: its chord presses the band from the
// prompt. `app:cycleDiffBase` is bound by default to `ctrl+x b` in the
// DiffPanel context only, so from the prompt that chord is otherwise unused;
// while the diff panel is open its own handler is mounted and the chord
// cycles the diff base there instead. The API exposes no way to read the
// person's bindings, so a rebinding is not reflected in the hint.
export const BAND_ACTION = 'app:cycleDiffBase'
export const BAND_CHORD = 'ctrl+x b'

export const toggleView = (v: OvertoneView | null | undefined): OvertoneView => ({ expanded: !(v?.expanded ?? false) })

// ---------------------------------------------------------------------------
// Formatting
// ---------------------------------------------------------------------------

const isNum = (n: unknown): n is number => typeof n === 'number' && Number.isFinite(n)

export function fmtTok(n: number): string {
  if (!isNum(n) || n < 0) return '—'
  if (n < 1000) return String(Math.round(n))
  if (n < 100_000) return `${(n / 1000).toFixed(1).replace(/\.0$/, '')}k`
  if (n < 1_000_000) return `${Math.round(n / 1000)}k`
  return `${(n / 1e6).toFixed(1).replace(/\.0$/, '')}M`
}

// A span: `14m`, `2h 14m`, `3d 6h`; under a minute `<1m`.
export function fmtSpan(ms: number): string {
  const m = Math.floor(Math.max(0, ms) / 60_000)
  if (m < 1) return '<1m'
  if (m < 60) return `${m}m`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}h ${m % 60}m`
  return `${Math.floor(h / 24)}d ${h % 24}h`
}

// A job's elapsed time to the second under an hour: `2m 14s`, `45s`, `1h 05m`.
export function fmtElapsed(ms: number): string {
  const s = Math.floor(Math.max(0, ms) / 1000)
  if (s < 60) return `${s}s`
  if (s < 3600) return `${Math.floor(s / 60)}m ${String(s % 60).padStart(2, '0')}s`
  return `${Math.floor(s / 3600)}h ${String(Math.floor(s / 60) % 60).padStart(2, '0')}m`
}

// Seconds under two minutes (`50s`), else as a span.
export const fmtLeft = (ms: number): string => (ms < 120_000 ? `${Math.max(0, Math.round(ms / 1000))}s` : fmtSpan(ms))

// Local wall-clock time from epoch ms and the machine's UTC offset (minutes).
const local = (ms: number, offsetMin: number): Date => new Date(ms + offsetMin * 60_000)
const pad2 = (n: number): string => String(n).padStart(2, '0')
export const fmtClock = (ms: number, offsetMin: number): string => {
  const d = local(ms, offsetMin)
  return `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`
}
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
export const dayKey = (ms: number, offsetMin: number): string => local(ms, offsetMin).toISOString().slice(0, 10)
export const fmtDayClock = (ms: number, offsetMin: number): string =>
  `${DAYS[local(ms, offsetMin).getUTCDay()]} ${fmtClock(ms, offsetMin)}`
// A time today reads as `14:02`, another day as `Tue 14:02`.
export function fmtWhen(ms: number, nowMs: number, offsetMin: number): string {
  return dayKey(ms, offsetMin) === dayKey(nowMs, offsetMin) ? fmtClock(ms, offsetMin) : fmtDayClock(ms, offsetMin)
}

// A model for people: `claude-sonnet-5-5` -> `Sonnet 5.5`, `opus` -> `Opus`.
export function prettyModel(raw: string | undefined): string {
  if (!raw) return '—'
  const n = normModel(raw)
  if (n === '') return raw
  const m = /^([a-z]+)(?:-(\d+))?(?:-(\d+))?(.*)$/.exec(n)
  if (!m) return n
  const family = (m[1] as string).charAt(0).toUpperCase() + (m[1] as string).slice(1)
  const version = m[2] === undefined ? '' : ` ${m[2]}${m[3] === undefined ? '' : `.${m[3]}`}`
  return `${family}${version}${m[4] ?? ''}`
}

// The family alone, for the short alert: `sonnet`.
export const familyOf = (raw: string | undefined): string => (raw ? (normModel(raw).split('-')[0] ?? raw) : '—')

// A gauge: filled cells and the rest, `width` cells in all.
export function gauge(percent: number, width: number): { fill: string; rest: string } {
  const w = Math.max(1, Math.floor(width))
  const p = Math.max(0, Math.min(100, isNum(percent) ? percent : 0))
  const n = Math.round((p / 100) * w)
  return { fill: '█'.repeat(n), rest: '░'.repeat(w - n) }
}

const pct = (n: number): string => `${Math.round(n * 10) / 10}%`.replace(/\.0%$/, '%')

const clip = (text: string, max: number): string => {
  const t = text.replace(/\s+/g, ' ').trim()
  return t.length <= max ? t : `${t.slice(0, Math.max(1, max - 1))}…`
}

// ---------------------------------------------------------------------------
// Rate-limit windows: pace and the even-pace projection
// ---------------------------------------------------------------------------

export const FIVE_HOUR_MS = 5 * 3_600_000
export const SEVEN_DAY_MS = 7 * 86_400_000

export type Pace = {
  percent: number
  resetsMs?: number
  openedMs?: number
  // Share of the window gone, 0..100: where an even pace would be.
  evenPct?: number
  // ≈ Where the window lands at reset at the pace so far (window average).
  projectedPct?: number
  // ≈ When that pace reaches 100%, only when that is before the reset.
  runOutMs?: number
  // ≈ How long before the reset it runs out.
  earlyMs?: number
  isOut: boolean
}

export const limitOf = (u: OvertoneUsage | null | undefined, kind: string): OvertoneLimit | undefined =>
  u?.rateLimits.find(l => l.kind === kind && isNum(l.percentUsed))

// The projection is the window's average pace carried to its reset: too
// early in a window (under 5% of it, or 10 minutes) it says nothing.
export function pace(limit: OvertoneLimit | undefined, nowMs: number, windowMs: number): Pace | undefined {
  if (!limit) return undefined
  const percent = limit.percentUsed
  const resetsMs = limit.resetsAt ? Date.parse(limit.resetsAt) : Number.NaN
  const out: Pace = { percent, isOut: percent >= 100 }
  if (!isNum(resetsMs)) return out
  const openedMs = resetsMs - windowMs
  const elapsed = Math.max(0, Math.min(windowMs, nowMs - openedMs))
  out.resetsMs = resetsMs
  out.openedMs = openedMs
  out.evenPct = Math.round((elapsed / windowMs) * 100)
  const minElapsed = Math.max(10 * 60_000, windowMs * 0.05)
  if (elapsed >= minElapsed && percent > 0 && !out.isOut) {
    out.projectedPct = Math.round((percent * windowMs) / elapsed)
    const runOut = openedMs + (100 * elapsed) / percent
    if (runOut < resetsMs) {
      out.runOutMs = runOut
      out.earlyMs = resetsMs - runOut
    }
  }
  return out
}

// red when out or 95%+; amber when projected to run out or 80%+; else green.
export function paceTone(p: Pace | undefined): UTone {
  if (!p) return 'dim'
  if (p.isOut || p.percent >= 95) return 'error'
  if (p.runOutMs !== undefined || p.percent >= 80) return 'warning'
  return 'success'
}

// The weekly figure that drives the week's choices: where it lands at reset.
export const landsTone = (p: Pace | undefined): UTone =>
  !p?.projectedPct ? 'dim' : p.projectedPct >= 100 ? 'error' : p.projectedPct >= 80 ? 'warning' : 'success'

export const ctxTone = (state: BandState | undefined): UTone =>
  state === 'switch now' ? 'error' : state === 'switch at a break' ? 'warning' : state === 'keep working' ? 'success' : 'dim'

// ---------------------------------------------------------------------------
// The cache: per main request (turn.step), and when it needs saying
// ---------------------------------------------------------------------------

export type StepUsage = {
  input_tokens: number
  output_tokens: number
  cache_read_input_tokens: number
  cache_creation_input_tokens: number
  model?: string
}

const num = (n: unknown): number => (isNum(n) && n >= 0 ? n : 0)

export const toCounts = (u: StepUsage): OvertoneCounts => ({
  input: num(u.input_tokens),
  output: num(u.output_tokens),
  cacheRead: num(u.cache_read_input_tokens),
  cacheWrite: num(u.cache_creation_input_tokens),
})

// The prompt side of one request: what the cache served of all of it.
export function hitPct(c: OvertoneCounts): number | undefined {
  const prompt = c.input + c.cacheRead + c.cacheWrite
  return prompt > 0 ? Math.round((c.cacheRead * 100) / prompt) : undefined
}

// The hit's colour: green from 80%, amber from 50%, red below.
export const hitTone = (h: number): UTone => (h >= 80 ? 'success' : h >= 50 ? 'warning' : 'error')

// Tokens the request sent without the cache: uncached plus written anew.
export const resent = (c: OvertoneCounts): number => c.input + c.cacheWrite

// One main-loop response came back (`startMs` when its request was sent).
export function noteMainStep(s: OvertoneSteps | null | undefined, u: StepUsage, startMs: number, nowMs: number): OvertoneSteps {
  const prev = s ?? EMPTY_STEPS
  const c = toCounts(u)
  const next: OvertoneSteps = {
    requests: prev.requests + 1,
    last: { ...c, startMs, atMs: nowMs, ...(u.model ? { model: u.model } : {}) },
    trend: prev.trend,
  }
  if (prev.last) {
    const h = hitPct(prev.last)
    if (h !== undefined) next.prevHit = h
    next.gapMs = Math.max(0, startMs - prev.last.atMs)
    if (prev.last.model && u.model && normModel(prev.last.model) !== normModel(u.model)) next.modelChanged = true
  }
  const h = hitPct(c)
  if (h !== undefined) next.trend = [...prev.trend, h].slice(-TREND_KEEP)
  // cold prompts in a row since the cache was last warm (a session that
  // starts cold has none until it has been warm once)
  if (h !== undefined && h < HIT_ALERT_BELOW && next.prevHit !== undefined) {
    if (next.prevHit >= HIT_ALERT_BELOW) next.coldStreak = 1
    else if ((prev.coldStreak ?? 0) >= 1) next.coldStreak = (prev.coldStreak ?? 0) + 1
  }
  // What this cold run has said: the first alert needs a re-send of
  // MIN_RESENT or more (a small one is suppressed and the next larger one is
  // then the first); after it, "remains cold" once; then quiet.
  if (next.coldStreak !== undefined) {
    const phase = next.coldStreak === 1 ? 0 : (prev.coldPhase ?? 0)
    if (phase === 0 && resent(c) >= MIN_RESENT) {
      next.coldAlert = 'first'
      next.coldPhase = 1
    } else if (phase === 1) {
      next.coldAlert = 'remains'
      next.coldPhase = 2
    } else next.coldPhase = phase
  }
  return next
}

// The prompt cache's life. Claude Code reports it (`cache_ttl`) only on a
// model switch and when a resume restores the model (classic
// PostModelSwitch); otherwise 1 hour is assumed, what Claude Code uses on a
// subscription. The expiry warning covers the last 5 minutes of an hour's
// life, the last minute of a 5-minute one.
export const DEFAULT_TTL_MS = 3_600_000
export const HIT_ALERT_BELOW = 80
export const MIN_RESENT = 10_000
export const EXPIRY_MIN_CONTEXT = 50_000

export type CacheLife = { ms: number; label: string; reported: boolean; warnMs: number }

export function cacheLife(reported: '5m' | '1h' | undefined): CacheLife {
  if (reported === '5m') return { ms: 300_000, label: '5m cache', reported: true, warnMs: 60_000 }
  if (reported === '1h') return { ms: 3_600_000, label: '1h cache', reported: true, warnMs: 300_000 }
  return { ms: DEFAULT_TTL_MS, label: '1h cache assumed', reported: false, warnMs: 300_000 }
}

export type CacheCase = 'idle' | 'model switched' | 'unknown'

export type CacheAlert = {
  // The last prompt went (partly) cold: hit under 80% after one at 80% or
  // more (the crossing); `remains` on the next cold prompt, said once.
  cold?: { hit: number; was?: number; resent: number; case: CacheCase; gapMs?: number; remains?: true }
  // ≈ Idle with a big context and the cache about to lapse.
  expiresInMs?: number
  untilMs?: number
}

export function cacheAlert(
  steps: OvertoneSteps | null | undefined,
  contextTokens: number | undefined,
  isWorking: boolean,
  nowMs: number,
  life: CacheLife = cacheLife(undefined),
): CacheAlert | undefined {
  const s = steps ?? EMPTY_STEPS
  if (!s.last) return undefined
  const out: CacheAlert = {}
  const hit = hitPct(s.last)
  const sent = resent(s.last)
  // Only the cold run's first alert, then "remains cold" once (noteMainStep).
  if (hit !== undefined && s.coldAlert) {
    const kase: CacheCase = s.modelChanged ? 'model switched' : (s.gapMs ?? 0) >= life.ms ? 'idle' : 'unknown'
    out.cold = { hit, was: s.prevHit, resent: sent, case: kase, ...(s.gapMs !== undefined ? { gapMs: s.gapMs } : {}) }
    if (s.coldAlert === 'remains') out.cold.remains = true
  }
  // the cache's life counts from when the last request was sent
  const until = s.last.startMs + life.ms
  const left = until - nowMs
  if (!isWorking && left > 0 && left <= life.warnMs && (contextTokens ?? 0) >= EXPIRY_MIN_CONTEXT) {
    out.expiresInMs = left
    out.untilMs = until
  }
  return out.cold || out.expiresInMs !== undefined ? out : undefined
}

// ---------------------------------------------------------------------------
// Jobs: workers (subagents) and Kerd Agent partner requests
// ---------------------------------------------------------------------------

// What a kerd:<model>-<effort> agent type names (kerd:sonnet-high, kerd:haiku).
export function kerdAsk(type: string | undefined): { model?: string; effort?: string } {
  const m = /^kerd:(opus|sonnet|haiku|fable)(?:-(low|medium|high|xhigh|max))?$/.exec(type ?? '')
  return m ? { model: m[1], ...(m[2] ? { effort: m[2] } : {}) } : {}
}

// The spawn asked: the Agent call's own model, else the one the type names.
export function noteAsked(
  w: OvertoneWorkers | null | undefined,
  id: string,
  ask: { model?: string; type?: string },
): OvertoneWorkers {
  const prev = w ?? EMPTY_WORKERS
  const old = prev.byId[id]
  if (!old) return prev
  const k = kerdAsk(ask.type)
  const next: OvertoneWorker = { ...old }
  const model = ask.model || k.model
  if (model) next.asked = model
  if (k.effort) next.askedEffort = k.effort
  return { ...prev, byId: { ...prev.byId, [id]: next } }
}

// A worker's own request (before it is sent): the model and effort sent.
export function noteWorkerModel(
  w: OvertoneWorkers | null | undefined,
  id: string,
  model: string,
  effort: string | number | undefined,
): OvertoneWorkers {
  const prev = w ?? EMPTY_WORKERS
  const old = prev.byId[id]
  if (!old) return prev
  const next: OvertoneWorker = { ...old, model }
  if (effort === undefined) delete next.effort
  else next.effort = effort
  return { ...prev, byId: { ...prev.byId, [id]: next } }
}

// Its response: the model the API reported answering.
export function noteWorkerSeen(w: OvertoneWorkers | null | undefined, id: string, seen: string | undefined): OvertoneWorkers {
  const prev = w ?? EMPTY_WORKERS
  const old = prev.byId[id]
  if (!old || !seen) return prev
  return { ...prev, byId: { ...prev.byId, [id]: { ...old, seen } } }
}

export type JobState =
  | 'running'
  | 'matches'
  | 'wrong model'
  | 'waiting on you'
  | 'returned, not yet checked'
  | 'failed, not yet checked'
  | 'waiting on a reply'
  | 'delivery uncertain'
  | 'reply received'

export type JobRow = {
  key: string
  kind: 'worker' | 'partner'
  job: string
  doing: string
  asked: string
  saw: string
  elapsed: string
  state: JobState
  // What the worker's requests sent where it differs from what was asked.
  sent?: string
  // Waiting time of a partner request, for the over-ten-minutes alert.
  waitMs?: number
}

export const stateTone = (s: JobState): UTone =>
  s === 'matches' || s === 'reply received'
    ? 'success'
    : s === 'wrong model' || s === 'failed, not yet checked'
      ? 'error'
      : s === 'running'
        ? 'dim'
        : 'warning'

export const stateLabel = (s: JobState): string =>
  s === 'matches' ? '✓ matches' : s === 'wrong model' ? `▼ ${s}` : s

const FAILED = new Set(['failed', 'killed', 'error', 'cancelled'])

// "asked" is the requested pair, kept intact: the spawn's model (the Agent
// call's, or the one a kerd:<model>-<effort> type names) and the effort that
// type names. What the worker's requests actually sent is never merged into
// it: where it differs it is a separate note ("sent low").
const askedModel = (x: OvertoneWorker): string | undefined => x.asked
const askedEffort = (x: OvertoneWorker): string | undefined => x.askedEffort

export function sentNote(x: OvertoneWorker): string | undefined {
  const parts: string[] = []
  const asked = askedModel(x)
  if (x.model && (!asked || compareModels(asked, x.model) === 'mismatch')) parts.push(prettyModel(x.model))
  if (x.effort !== undefined && (parts.length > 0 || String(x.effort) !== askedEffort(x))) parts.push(String(x.effort))
  return parts.length > 0 ? `sent ${parts.join(' · ')}` : undefined
}

// "saw" is only ever the model the API reported answering: until a response
// comes back the worker is `running` and saw is `—`. With nothing asked there
// is nothing to match.
function workerState(x: OvertoneWorker): JobState {
  if (!isActive(x)) return FAILED.has(x.status) ? 'failed, not yet checked' : 'returned, not yet checked'
  if (x.blocked) return 'waiting on you'
  if (!x.seen || !askedModel(x)) return 'running'
  const m = compareModels(askedModel(x), x.seen)
  return m === 'mismatch' ? 'wrong model' : m === 'match' ? 'matches' : 'running'
}

const withEffort = (model: string | undefined, effort: string | number | undefined): string =>
  model ? `${prettyModel(model)}${effort === undefined ? '' : ` · ${effort}`}` : '—'

// Active workers, and those that returned since the main loop last stepped
// (it has not read them yet).
export function workerJobs(w: OvertoneWorkers | null | undefined, lastMainStartMs: number | undefined, nowMs: number): JobRow[] {
  const all = Object.values((w ?? EMPTY_WORKERS).byId)
  const shown = all.filter(x => isActive(x) || (x.endedMs !== undefined && x.endedMs > (lastMainStartMs ?? 0)))
  shown.sort((a, b) => a.firstSeenMs - b.firstSeenMs)
  return shown.map(x => {
    const state = workerState(x)
    const end = isActive(x) ? nowMs : (x.endedMs ?? nowMs)
    const sent = sentNote(x)
    return {
      ...(sent ? { sent } : {}),
      key: `w-${x.id}`,
      kind: 'worker',
      job: x.label,
      doing: x.blocked ? x.blocked.what : !isActive(x) ? 'returned' : (x.activity ?? 'started'),
      asked: withEffort(askedModel(x), askedEffort(x)),
      saw: x.seen ? prettyModel(x.seen) : '—',
      elapsed: `${x.fromSpawn ? '' : '≥'}${fmtElapsed(end - x.firstSeenMs)}`,
      state,
    }
  })
}

// Kerd Agent requests: waiting ones up to three hours old, replies for
// fifteen minutes after they came back.
export const PARTNER_WAIT_KEEP_MS = 3 * 3_600_000
export const PARTNER_REPLY_KEEP_MS = 15 * 60_000
export const PARTNER_ALERT_MS = 10 * 60_000

export type RequestRecord = {
  request_id?: unknown
  provider?: unknown
  session?: unknown
  project?: unknown
  role?: unknown
  status?: unknown
  created_at?: unknown
  received_at?: unknown
  kind?: unknown
  reply_expected?: unknown
}

const WAITING = new Set(['submitted-unconfirmed', 'launched-unconfirmed'])
const UNCERTAIN = new Set(['delivery-uncertain', 'start-uncertain'])

// One request record, read: undefined when it is not this project's, not a
// request that expects a reply, or too old to matter.
export function partnerRow(
  r: RequestRecord,
  project: string,
  aliases: Readonly<Record<string, string>>,
  nowMs: number,
): OvertonePartnerRow | undefined {
  if (typeof r.request_id !== 'string' || typeof r.status !== 'string' || !isNum(r.created_at)) return undefined
  if (r.kind === 'arrival-notice' || r.reply_expected === false) return undefined
  const trim = (p: string) => p.replace(/\/+$/, '')
  if (typeof r.project !== 'string' || trim(r.project) !== trim(project)) return undefined
  const createdMs = r.created_at * 1000
  const provider = typeof r.provider === 'string' ? r.provider : 'partner'
  const session = typeof r.session === 'string' ? r.session : ''
  const alias = aliases[`${provider}:${session}`] ?? `${provider} ${session.slice(0, 8)}`.trim()
  const doing = clip(typeof r.role === 'string' && r.role.trim() !== '' ? r.role : 'a request', 60)
  if (r.status === 'reply-received') {
    const receivedMs = isNum(r.received_at) ? r.received_at * 1000 : undefined
    if (receivedMs === undefined || nowMs - receivedMs > PARTNER_REPLY_KEEP_MS) return undefined
    return { id: r.request_id, alias, provider, doing, createdMs, receivedMs, state: 'received' }
  }
  if (nowMs - createdMs > PARTNER_WAIT_KEEP_MS) return undefined
  if (WAITING.has(r.status)) return { id: r.request_id, alias, provider, doing, createdMs, state: 'waiting' }
  if (UNCERTAIN.has(r.status)) return { id: r.request_id, alias, provider, doing, createdMs, state: 'uncertain' }
  return undefined
}

// partners/<alias>.json: { alias, provider, id } -> `${provider}:${id}` -> alias.
export function aliasMap(records: readonly unknown[]): Record<string, string> {
  const out: Record<string, string> = {}
  for (const r of records) {
    if (!r || typeof r !== 'object') continue
    const p = r as Record<string, unknown>
    if (typeof p.alias === 'string' && typeof p.provider === 'string' && typeof p.id === 'string') out[`${p.provider}:${p.id}`] = p.alias
  }
  return out
}

export function partnerJobs(p: OvertonePartners | null | undefined, nowMs: number): JobRow[] {
  return (p?.rows ?? [])
    .slice()
    .sort((a, b) => a.createdMs - b.createdMs)
    .map(r => {
      const state: JobState = r.state === 'received' ? 'reply received' : r.state === 'uncertain' ? 'delivery uncertain' : 'waiting on a reply'
      const age = (r.receivedMs ?? nowMs) - r.createdMs
      return {
        key: `p-${r.id}`,
        kind: 'partner',
        job: r.alias,
        doing: r.doing,
        asked: r.provider === 'codex' ? 'Codex session' : r.provider === 'claude' ? 'Claude session' : 'partner session',
        saw: '—',
        elapsed: fmtSpan(age),
        state,
        ...(r.state === 'received' ? {} : { waitMs: nowMs - r.createdMs }),
      }
    })
}

// ---------------------------------------------------------------------------
// The snapshot every view draws from
// ---------------------------------------------------------------------------

export type Snapshot = {
  nowMs: number
  // Local UTC offset in minutes.
  offsetMin: number
  isWorking: boolean
  reading: OvertoneReading | null | undefined
  model: OvertoneModel | null | undefined
  usage: OvertoneUsage | null | undefined
  steps: OvertoneSteps | null | undefined
  workers: OvertoneWorkers | null | undefined
  partners: OvertonePartners | null | undefined
  // The prompt-cache TTL Claude Code last reported; absent, 1h is assumed.
  cacheTtl?: '5m' | '1h'
}

export const lifeOf = (s: Snapshot): CacheLife => cacheLife(s.cacheTtl)

// Before a context reading or a rate-limit window the band hands its slot
// back, as the old status line printed nothing.
export const hasFigures = (s: Snapshot): boolean =>
  readContext(s.reading) !== undefined || (s.usage?.rateLimits.length ?? 0) > 0

export const jobsOf = (s: Snapshot): JobRow[] => [
  ...workerJobs(s.workers, s.steps?.last?.startMs, s.nowMs),
  ...partnerJobs(s.partners, s.nowMs),
]

// ---------------------------------------------------------------------------
// Alerts: red, appended to the line only while they fire
// ---------------------------------------------------------------------------

export type Alert = { key: string; text: string; short: string; note: string }

export function alertsOf(s: Snapshot): Alert[] {
  const out: Alert[] = []
  const c = readContext(s.reading)
  const cache = cacheAlert(s.steps, c?.tokens, s.isWorking, s.nowMs, lifeOf(s))
  if (cache?.cold?.remains) {
    out.push({ key: 'cache', text: `cache remains cold (${cache.cold.hit}%)`, short: 'cache cold', note: `cache remains cold (${cache.cold.hit}% hit)` })
  } else if (cache?.cold) {
    out.push({
      key: 'cache',
      text: `cache ${cache.cold.hit}% ▼ re-sent ${fmtTok(cache.cold.resent)}`,
      short: `cache ${cache.cold.hit}% ▼`,
      note: `cache ${cache.cold.hit}% hit (was ${cache.cold.was}%), re-sent ${fmtTok(cache.cold.resent)} (case: ${cache.cold.case})`,
    })
  }
  const jobs = jobsOf(s)
  const wrong = jobs.filter(j => j.kind === 'worker' && j.state === 'wrong model')
  if (wrong.length === 1) {
    const x = Object.values(s.workers?.byId ?? {}).find(w => `w-${w.id}` === wrong[0]?.key)
    const asked = x ? askedModel(x) : undefined
    out.push({
      key: 'worker',
      text: `worker on ${familyOf(x?.seen)}, asked ${familyOf(asked)}`,
      short: 'wrong model',
      note: `worker ${wrong[0]?.job} on ${prettyModel(x?.seen)}, asked ${prettyModel(asked)}`,
    })
  } else if (wrong.length > 1) {
    out.push({ key: 'worker', text: `${wrong.length} workers on the wrong model`, short: 'wrong model', note: `${wrong.length} workers on the wrong model` })
  }
  const late = jobs.filter(j => j.kind === 'partner' && j.waitMs !== undefined && j.waitMs >= PARTNER_ALERT_MS)
  if (late[0]) {
    const first = late[0]
    out.push({
      key: 'partner',
      text: `${first.job} waiting ${fmtSpan(first.waitMs ?? 0)}${late.length > 1 ? ` +${late.length - 1}` : ''}`,
      short: `${first.job} ${fmtSpan(first.waitMs ?? 0)}`,
      note: `${first.job} reply pending ${fmtSpan(first.waitMs ?? 0)}${late.length > 1 ? ` (+${late.length - 1} more)` : ''}`,
    })
  }
  return out
}

// ---------------------------------------------------------------------------
// The next line: what needs him, worst first, at most two joined
// ---------------------------------------------------------------------------

export type Next = { lead: string; rest: string; tone: UTone }

type Part = { lead: string; rest: string; tone: UTone; second: string }

export function nextNote(s: Snapshot): Next | undefined {
  const c = readContext(s.reading)
  const five = pace(limitOf(s.usage, 'five_hour'), s.nowMs, FIVE_HOUR_MS)
  const seven = pace(limitOf(s.usage, 'seven_day'), s.nowMs, SEVEN_DAY_MS)
  const parts: Part[] = []
  const ctxFig = c ? fmtTok(c.tokens) : ''
  if (c?.state === 'switch now') {
    parts.push({ lead: `Context ${ctxFig}`, rest: 'switch now; Switch Out saves your place', tone: 'error', second: `context ${ctxFig}, switch now` })
  }
  if (five?.isOut) {
    const r = five.resetsMs === undefined ? '' : `resets ${fmtClock(five.resetsMs, s.offsetMin)}`
    parts.push({ lead: '5-hour window used up', rest: r, tone: 'error', second: '5-hour window used up' })
  } else if (five?.runOutMs !== undefined) {
    const at = fmtClock(five.runOutMs, s.offsetMin)
    parts.push({ lead: `5-hour runs out ≈ ${at}`, rest: 'hold big jobs; a good point to Switch Out', tone: 'warning', second: `5-hour runs out ≈ ${at}` })
  }
  if (c?.state === 'switch at a break') {
    parts.push({ lead: `Context ${ctxFig}`, rest: 'switch at a break', tone: 'warning', second: `context ${ctxFig}, switch at a break` })
  }
  if (seven?.isOut) parts.push({ lead: 'Weekly window used up', rest: '', tone: 'error', second: 'weekly window used up' })
  else if ((seven?.projectedPct ?? 0) >= 100) {
    const l = `Weekly lands ≈${seven?.projectedPct}%`
    parts.push({ lead: l, rest: 'save headroom: lighter models, lower effort', tone: 'warning', second: `weekly lands ≈${seven?.projectedPct}%` })
  }
  const jobs = jobsOf(s)
  for (const j of jobs.filter(j => j.state === 'wrong model')) {
    const t = `the ${j.job} is on the ${j.state}`
    parts.push({ lead: `The ${j.job}`, rest: `is on the ${j.state}`, tone: 'error', second: t })
  }
  const cache = cacheAlert(s.steps, c?.tokens, s.isWorking, s.nowMs, lifeOf(s))
  if (cache?.expiresInMs !== undefined) {
    const l = `cache expires in ≈${fmtLeft(cache.expiresInMs)}`
    parts.push({ lead: l, rest: 'send the next prompt now, or Switch Out', tone: 'warning', second: l })
  } else if (cache?.cold?.case === 'idle' && !cache.cold.remains) {
    parts.push({ lead: 'The cache went cold', rest: 'at a break, Switch Out rather than continue a big context', tone: 'error', second: 'the cache went cold' })
  }
  for (const j of jobs.filter(j => j.state === 'waiting on you')) {
    parts.push({ lead: `The ${j.job}`, rest: 'waits on a permission prompt', tone: 'warning', second: `the ${j.job} waits on a permission prompt` })
  }
  for (const j of jobs.filter(j => (j.waitMs ?? 0) >= PARTNER_ALERT_MS)) {
    parts.push({ lead: j.job, rest: `reply pending ${j.elapsed}`, tone: 'warning', second: `${j.job} reply pending ${j.elapsed}` })
  }
  const first = parts[0]
  if (!first) return undefined
  const rest = [first.rest, parts[1]?.second ?? ''].filter(Boolean).join('; ')
  return { lead: first.lead, rest, tone: first.tone }
}

export const nextText = (n: Next): string => (n.rest ? `${n.lead} — ${n.rest}` : n.lead)

// ---------------------------------------------------------------------------
// The collapsed line: one row of bars, shrunk as the columns shrink
// ---------------------------------------------------------------------------

// `ctx ■■■■■■■■■■  │  5h ■■■■■■■■■■  │  7d ■■■■■■■■■■  │  cache 98%` (the
// used part of each bar dim), then
// any firing alert. Each bar is what is LEFT: the context window free, the
// 5-hour and weekly allowance left. Its colour is the tone the figure has
// everywhere else: ctx the switch state (so a mostly-free bar can be amber
// past 200k), 5h its pace, 7d the worse of its pace and where it lands at
// reset. The figures themselves (tokens, state words, run-out, lands,
// resets) live in the expanded dashboard and Claude's `usage:` line.
export const SEP = '  │  '
const DOT = ' · '

export const BAR_CELLS = [10, 6, 4] as const

type Cells = {
  bar: number
  cache: boolean
  five: boolean
  seven: boolean
  alertsShort: boolean
  alertsMark: boolean
  ctxLabel: boolean
  ctx: boolean
}

// Lowest priority first: the bars shrink (10 → 6 → 4 cells), then the cache
// cell, the alerts' long wording, the weekly bar, the 5-hour bar; then the
// alerts fold into one red `⚠ N` (the expanded view still lists them), the
// ctx label goes, then the ctx bar. Every firing alert stays represented:
// `⚠ N` is the last thing to go and never goes (see collapsedLine).
const REDUCE: ((c: Cells) => void)[] = [
  c => (c.bar = BAR_CELLS[1]),
  c => (c.bar = BAR_CELLS[2]),
  c => (c.cache = false),
  c => (c.alertsShort = true),
  c => (c.seven = false),
  c => (c.five = false),
  c => (c.alertsMark = true),
  c => (c.ctxLabel = false),
  c => (c.ctx = false),
]

// The alerts folded to one mark when even their short wording has no room.
export const alertMark = (n: number): string => `⚠ ${n}`

const TONE_RANK: Record<UTone, number> = { dim: 0, plain: 0, success: 1, warning: 2, error: 3 }
const worse = (a: UTone, b: UTone): UTone => (TONE_RANK[b] > TONE_RANK[a] ? b : a)

// The weekly bar's tone: the week's most decisive figure, as the line had
// it: where it lands at reset (landsTone), or the used figure's own tone
// (paceTone) when that is worse or there is no landing yet.
export const sevenTone = (p: Pace | undefined): UTone => worse(paceTone(p), landsTone(p))

// One bar group: dim label, then `free`% of `width` blocks in `tone`, the
// rest dim. Blocks (`◼`, a medium square: `■` ran solid in his font), not a solid run, so each cell reads on its own,
// as the band-bars mock drew them; no reading, a dim `—`.
export const BLOCK = '◼'
function barGroup(label: string, free: number | undefined, tone: UTone, width: number): ULine {
  const g: ULine = label ? [sg(`${label} `, 'dim')] : []
  if (free === undefined) return [...g, sg('—', 'dim')]
  const b = gauge(free, width)
  if (b.fill) g.push(sg(BLOCK.repeat(b.fill.length), tone))
  if (b.rest) g.push(sg(BLOCK.repeat(b.rest.length), 'dim'))
  return g
}

function buildCollapsed(s: Snapshot, cells: Cells): ULine {
  const groups: ULine[] = []
  const c = readContext(s.reading)
  if (cells.ctx) groups.push(barGroup(cells.ctxLabel ? 'ctx' : '', c?.percent === undefined ? undefined : 100 - c.percent, ctxTone(c?.state), cells.bar))
  const five = pace(limitOf(s.usage, 'five_hour'), s.nowMs, FIVE_HOUR_MS)
  if (cells.five) groups.push(barGroup('5h', five ? 100 - five.percent : undefined, paceTone(five), cells.bar))
  const seven = pace(limitOf(s.usage, 'seven_day'), s.nowMs, SEVEN_DAY_MS)
  if (cells.seven) groups.push(barGroup('7d', seven ? 100 - seven.percent : undefined, sevenTone(seven), cells.bar))
  // The last prompt's cache hit, always (a cache alert, when one fires, says it instead).
  const alerts = alertsOf(s)
  if (cells.cache && !alerts.some(a => a.key === 'cache')) {
    const h = s.steps?.last ? hitPct(s.steps.last) : undefined
    groups.push(h === undefined ? [sg('cache ', 'dim'), sg('—', 'dim')] : [sg('cache ', 'dim'), sg(`${h}%`, hitTone(h), true)])
  }
  if (cells.alertsMark && alerts.length) groups.push([sg(alertMark(alerts.length), 'error', true)])
  else for (const a of alerts) groups.push([sg(cells.alertsShort ? a.short : a.text, 'error', true)])
  const out: ULine = []
  groups.forEach((g, i) => {
    if (i > 0) out.push(sg(SEP, 'dim'))
    out.push(...g)
  })
  return out
}

// The terminal draws a Button as `[ label ]`, then a two-space gap; the
// engine draws its own `[-]` at the row's right end, which is kept free.
export const COLLAPSED_LABEL = '▸ usage'
export const EXPANDED_LABEL = '▾ usage'
export const BUTTON_ROOM = [...COLLAPSED_LABEL].length + 4 + 2 + 4

// The line never passes `room`, with one documented exception: while alerts
// fire, `⚠ N` alone is the floor and is returned even when `room` is
// narrower, so an alert is never hidden by the host's truncation while a
// shorter form exists. With no alerts and no room even for a bare bar, the
// line is empty.
export function collapsedLine(s: Snapshot, columns: number): ULine {
  const room = Math.max(0, (isNum(columns) ? columns : 200) - BUTTON_ROOM)
  const cells: Cells = {
    bar: BAR_CELLS[0],
    cache: true,
    five: true,
    seven: true,
    alertsShort: false,
    alertsMark: false,
    ctxLabel: true,
    ctx: true,
  }
  let line = buildCollapsed(s, cells)
  for (const step of REDUCE) {
    if (lineWidth(line) <= room) return line
    step(cells)
    line = buildCollapsed(s, cells)
  }
  // Every step taken: `⚠ N` alone while alerts fire (the floor), else nothing.
  return lineWidth(line) <= room || alertsOf(s).length ? line : []
}

// ---------------------------------------------------------------------------
// The expanded dashboard, as plain data
// ---------------------------------------------------------------------------

export type Panel = { key: string; title: ULine; right: ULine; lines: ULine[]; tone?: UTone }

// The even-pace mark under a gauge: `╵` where an even pace would be, its
// caption after it, or before it when there is no room after.
export function paceMark(evenPct: number, gaugeWidth: number, width: number): ULine {
  const at = Math.min(gaugeWidth - 1, Math.max(0, Math.round((evenPct / 100) * gaugeWidth)))
  const texts = [`even pace ${evenPct}%`, `${evenPct}%`]
  for (const text of texts) {
    if (at + 2 + text.length <= width) return [sg(`${' '.repeat(at)}╵ `, 'dim'), sg(text, 'dim')]
    if (at >= text.length + 1) return [sg(`${' '.repeat(at - text.length - 1)}${text} ╵`, 'dim')]
  }
  return [sg(`${' '.repeat(at)}╵`, 'dim')]
}

function gaugeLine(percent: number, label: string, tone: UTone, width: number): { line: ULine; gw: number } {
  const gw = Math.max(6, width - label.length - 1)
  const g = gauge(percent, gw)
  return { line: [sg(g.fill, tone), sg(g.rest, 'dim'), sg(` ${label}`, tone, true)], gw }
}

function contextPanel(s: Snapshot, width: number): Panel {
  const c = readContext(s.reading)
  const win = s.reading?.window
  const right: ULine = c ? [sg(`${fmtTok(c.tokens)}${win ? ` / ${fmtTok(win)}` : ''}`)] : []
  const title: ULine = [sg('Context', 'plain', true)]
  if (!c) return { key: 'context', title, right, lines: [[sg('— no reading yet (after the first reply)', 'dim')]] }
  const tone = ctxTone(c.state)
  const lines: ULine[] = []
  if (c.percent !== undefined) lines.push(gaugeLine(c.percent, `${c.isEstimate ? '≈' : ''}${c.percent}%`, tone, width).line)
  else lines.push([sg('window size not reported', 'dim')])
  const ladder: ULine = []
  const states: BandState[] = ['keep working', 'switch at a break', 'switch now']
  states.forEach((st, i) => {
    if (i > 0) ladder.push(sg(DOT, 'dim'))
    const label = st === 'keep working' ? 'keep' : st
    ladder.push(c.state === st ? sg(`▸ ${label}`, tone, true) : sg(label, 'dim'))
  })
  lines.push(ladder)
  lines.push([sg('break: from 200k or 60% · now: from 80%', 'dim')])
  lines.push([sg(fmtTok(c.tokens), 'plain', true), sg(' tokens re-sent on every call', 'dim')])
  return { key: 'context', title, right, lines, ...(tone === 'warning' || tone === 'error' ? { tone } : {}) }
}

function noWindow(key: string, title: ULine): Panel {
  return { key, title, right: [], lines: [[sg('— not reported yet', 'dim')], [sg('(subscription windows only)', 'dim')]] }
}

function fivePanel(s: Snapshot, width: number): Panel {
  const title: ULine = [sg('5-hour', 'plain', true)]
  const p = pace(limitOf(s.usage, 'five_hour'), s.nowMs, FIVE_HOUR_MS)
  if (!p) return noWindow('five', title)
  const tone = paceTone(p)
  const { line, gw } = gaugeLine(p.percent, pct(p.percent), tone, width)
  const lines: ULine[] = [line]
  if (p.evenPct !== undefined) lines.push(paceMark(p.evenPct, gw, width))
  const resets = p.resetsMs === undefined ? '' : `resets ${fmtClock(p.resetsMs, s.offsetMin)}`
  if (p.isOut) {
    lines.push([sg('✕ used up', 'error', true)])
    lines.push([sg(resets, 'dim')])
  } else if (p.runOutMs !== undefined) {
    lines.push([sg(`▲ runs out ≈ ${fmtClock(p.runOutMs, s.offsetMin)}`, 'warning', true), sg(`, ${fmtSpan(p.earlyMs ?? 0)} early`, 'warning')])
    lines.push([sg(`${resets} · hold big jobs until then`, 'dim')])
  } else if (p.projectedPct !== undefined) {
    lines.push([sg('✓ no ▲ run-out', 'success', true), sg(' before the reset', 'dim')])
    lines.push([sg(`${resets}${p.projectedPct < 70 ? ' · room to fan out' : ''}`, 'dim')])
  } else {
    lines.push([sg('too early in the window to project', 'dim')])
    lines.push([sg(resets, 'dim')])
  }
  const right: ULine = p.resetsMs === undefined ? [] : [sg(`resets in ${fmtSpan(p.resetsMs - s.nowMs)}`, 'dim')]
  return { key: 'five', title, right, lines, ...(tone === 'warning' || tone === 'error' ? { tone } : {}) }
}

function weekPanel(s: Snapshot, width: number): Panel {
  const title: ULine = [sg('Weekly', 'plain', true), sg(' (7 days)', 'dim')]
  const p = pace(limitOf(s.usage, 'seven_day'), s.nowMs, SEVEN_DAY_MS)
  if (!p) return noWindow('seven', title)
  const tone = paceTone(p)
  const { line, gw } = gaugeLine(p.percent, pct(p.percent), tone, width)
  const lines: ULine[] = [line]
  if (p.evenPct !== undefined) lines.push(paceMark(p.evenPct, gw, width))
  if (p.isOut) lines.push([sg('✕ used up', 'error', true)])
  else if (p.runOutMs !== undefined) {
    lines.push([sg(`▲ lands past the limit: out ≈ ${fmtWhen(p.runOutMs, s.nowMs, s.offsetMin)}`, 'error', true)])
  } else if (p.projectedPct !== undefined) lines.push([sg(`lands ≈${p.projectedPct}% at reset`, landsTone(p), true)])
  else lines.push([sg('too early in the week to project', 'dim')])
  const head = p.projectedPct !== undefined ? `headroom left: ≈${Math.max(0, 100 - p.projectedPct)}% of the week` : `headroom left: ${pct(Math.max(0, 100 - p.percent))} now`
  lines.push([sg(head, 'dim')])
  const right: ULine = p.resetsMs === undefined ? [] : [sg(`resets in ${fmtSpan(p.resetsMs - s.nowMs)}`, 'dim')]
  const t = landsTone(p) === 'error' ? 'error' : tone
  return { key: 'seven', title, right, lines, ...(t === 'warning' || t === 'error' ? { tone: t } : {}) }
}

export type CacheCard = { right: ULine; lines: ULine[] }

function cacheCard(s: Snapshot): CacheCard | undefined {
  const c = readContext(s.reading)
  const a = cacheAlert(s.steps, c?.tokens, s.isWorking, s.nowMs, lifeOf(s))
  if (!a) return undefined
  const lines: ULine[] = []
  let right: ULine = []
  if (a.cold?.remains) {
    lines.push([sg('The cache remains cold', 'warning', true), sg(` (${a.cold.hit}% hit, re-sent ${fmtTok(a.cold.resent)}); said once, quiet until it is warm again.`)])
    right = [sg('▼ remains cold', 'warning', true)]
  } else if (a.cold) {
    lines.push([
      sg(`Last prompt re-sent ${fmtTok(a.cold.resent)} tokens without the cache`, 'error', true),
      sg(` (${a.cold.hit}% hit${a.cold.was === undefined ? '' : `, was ${a.cold.was}%`}).`),
    ])
    const idle = a.cold.case === 'idle'
    const changed = a.cold.case === 'model switched'
    const idleFor = a.cold.gapMs === undefined ? '' : ` (${fmtSpan(a.cold.gapMs)} idle)`
    lines.push([
      sg(idle ? '▸ ' : '  ', idle ? 'warning' : 'dim'),
      sg(`Idle past the cache's life${idle ? idleFor : ''}`, idle ? 'warning' : 'dim', idle),
      sg(' → every next prompt starts cold: at a break, Switch Out rather than continue a big context.', idle ? undefined : 'dim'),
    ])
    lines.push([
      sg(changed ? '▸ ' : '  ', changed ? 'warning' : 'dim'),
      sg(changed ? 'The model switched' : 'Instructions, tools or the model changed mid-session', changed ? 'warning' : 'dim', changed),
      sg(' → a one-off; carry on.', changed ? undefined : 'dim'),
    ])
    right = [sg(a.cold.case === 'unknown' ? '▼ cause unknown' : `▼ case: ${a.cold.case}`, 'error', true)]
  }
  if (a.expiresInMs !== undefined && a.untilMs !== undefined) {
    lines.push([
      sg(`≈ ${fmtLeft(a.expiresInMs)} until the cache expires`, 'warning', true),
      sg(' — send the next prompt now, or Switch Out.'),
      sg(` (at ${fmtClock(a.untilMs, s.offsetMin)}; ${lifeOf(s).label})`, 'dim'),
    ])
    if (!a.cold) right = [sg('▼ about to expire', 'warning', true)]
  }
  return { right, lines }
}

export type Dashboard = {
  header: ULine
  hint: string
  jobs: JobRow[]
  // Jobs left out to fit the band ("+K more"); the worst are kept.
  jobsHidden: number
  // Why the job list may be incomplete (the last worker list read failed, or
  // the partner records could not be read).
  jobsNote?: string
  // A band shorter still: the jobs card drops its column-header row, and
  // "+K more" and the note go into its title row.
  jobsCompact?: boolean
  panels: Panel[]
  perRow: number
  panelWidth: number
  cache?: CacheCard
  next?: Next
  // On a band short of rows the outer frame goes first; the card frames
  // only when nothing else will make the whole fit.
  outerBorder: boolean
  panelBorder: boolean
}

// Panels three across from 124 columns, two from 80, else one.
export function perRowFor(columns: number): number {
  const inner = (isNum(columns) ? columns : 200) - 4
  return inner >= 120 ? 3 : inner >= 76 ? 2 : 1
}

export function dashboardRows(
  d: Pick<Dashboard, 'jobs' | 'jobsHidden' | 'jobsNote' | 'jobsCompact' | 'panels' | 'perRow' | 'cache' | 'next' | 'outerBorder' | 'panelBorder'>,
): number {
  const frame = d.panelBorder ? 2 : 0
  const jobs =
    d.jobs.length === 0
      ? 1
      : d.jobsCompact
        ? frame + 1 + d.jobs.length
        : frame + 2 + d.jobs.length + (d.jobsHidden > 0 ? 1 : 0) + (d.jobsNote ? 1 : 0)
  // The context, 5-hour and weekly panels are not drawn in the band (the
  // line carries them as bars); /overtone prints them.
  const cache = d.cache ? frame + 1 + d.cache.lines.length : 0
  return (d.outerBorder ? 2 : 0) + 1 + jobs + cache + (d.next ? 1 : 0)
}

export function dashboard(s: Snapshot, columns: number, maxRows: number = Infinity): Dashboard {
  const perRow = perRowFor(columns)
  const inner = (isNum(columns) ? columns : 200) - 4
  const panelWidth = Math.max(24, Math.floor((inner - (perRow - 1)) / perRow))
  const textWidth = panelWidth - 4
  const m = s.model ?? EMPTY_MODEL
  const shown = m.seen ?? m.asked
  const header: ULine = [sg(shown ? ` · ${prettyModel(shown)}` : '', 'dim')]
  if (m.effort !== undefined) header.push(sg(` · ${m.effort}`, 'dim'))
  if (compareModels(m.asked, m.seen) === 'mismatch') header.push(sg(` · asked ${prettyModel(m.asked)} ≠ seen`, 'error', true))
  const d: Dashboard = {
    header,
    hint: `click or ${BAND_CHORD} collapses`,
    jobs: jobsOf(s),
    jobsHidden: 0,
    panels: [contextPanel(s, textWidth), fivePanel(s, textWidth), weekPanel(s, textWidth)],
    perRow,
    panelWidth,
    outerBorder: true,
    panelBorder: true,
  }
  const notes = [
    s.workers?.error !== undefined ? `worker status unavailable · ${s.workers.error}` : '',
    s.partners?.note?.startsWith('partner records unreadable') ? s.partners.note : '',
  ].filter(Boolean)
  if (notes.length > 0) d.jobsNote = notes.join(' · ')
  const cache = cacheCard(s)
  if (cache) d.cache = cache
  const n = nextNote(s)
  if (n) d.next = n
  // Workers come first: on a band short of rows the outer frame goes, then
  // the cache card shrinks to its first line and then goes (the line still
  // shows the cache in red), then the next line; only then do jobs fold, and
  // the card frames go last.
  if (dashboardRows(d) > maxRows) d.outerBorder = false
  if (dashboardRows(d) > maxRows && d.cache && d.cache.lines.length > 1) d.cache = { ...d.cache, lines: d.cache.lines.slice(0, 1) }
  if (dashboardRows(d) > maxRows) delete d.cache
  if (dashboardRows(d) > maxRows) delete d.next
  // Still too tall: the jobs the band cannot show fold into "+K more", the
  // worst kept (wrong model, waiting on you, failed, late replies first).
  const allJobs = d.jobs
  foldJobs(d, maxRows)
  if (dashboardRows(d) > maxRows) d.panelBorder = false
  // Shorter still: the jobs card sheds its column-header row and folds
  // "+K more" and the note into its title row, then folds again from every
  // job. From three rows up the band never runs past what it is given.
  if (dashboardRows(d) > maxRows && d.jobs.length > 0) {
    d.jobsCompact = true
    d.jobs = allJobs
    d.jobsHidden = 0
    foldJobs(d, maxRows)
  }
  return d
}

// Folds the fewest jobs that fit `maxRows` into the hidden count, the worst
// kept; at least one stays.
function foldJobs(d: Dashboard, maxRows: number): void {
  if (dashboardRows(d) <= maxRows || d.jobs.length <= 1) return
  const ranked = d.jobs.map((j, i) => ({ j, i })).sort((a, b) => jobRank(a.j) - jobRank(b.j) || a.i - b.i)
  const all = d.jobs
  const hidden = d.jobsHidden
  for (let keep = all.length - 1; keep >= 1; keep--) {
    const kept = new Set(ranked.slice(0, keep).map(r => r.i))
    d.jobs = all.filter((_, i) => kept.has(i))
    d.jobsHidden = hidden + all.length - keep
    if (dashboardRows(d) <= maxRows) return
  }
}

const RANK: Record<JobState, number> = {
  'wrong model': 0,
  'waiting on you': 1,
  'failed, not yet checked': 2,
  'waiting on a reply': 3,
  'delivery uncertain': 4,
  'returned, not yet checked': 5,
  'reply received': 6,
  running: 7,
  matches: 8,
}
const jobRank = (j: JobRow): number => (j.waitMs !== undefined && j.waitMs >= PARTNER_ALERT_MS ? 2.5 : RANK[j.state])

// The jobs table's columns, sized to the band: job, doing, asked, saw,
// elapsed, state. `doing` takes what is left.
export function jobColumns(columns: number): { job: number; doing: number; asked: number; saw: number; elapsed: number } {
  const inner = Math.max(40, (isNum(columns) ? columns : 200) - 8)
  const fixed = { job: inner >= 130 ? 22 : 14, asked: 20, saw: 20, elapsed: 9 }
  const state = 26
  const doing = Math.max(10, inner - fixed.job - fixed.asked - fixed.saw - fixed.elapsed - state - 2)
  return { ...fixed, doing }
}

export const cell = (text: string, width: number): string => {
  const t = clip(text, width - 1)
  return t + ' '.repeat(Math.max(1, width - [...t].length))
}

// ---------------------------------------------------------------------------
// Text forms: Claude's context line, /overtone, and the $.store snapshot
// ---------------------------------------------------------------------------

// One short line for the model on each prompt, alerts and a next line only
// when they fire. Undefined when there is nothing to say yet.
export function contextSummary(s: Snapshot): string | undefined {
  if (!hasFigures(s)) return undefined
  const parts: string[] = []
  const c = readContext(s.reading)
  if (c) {
    const win = s.reading?.window ? `/${fmtTok(s.reading.window)}` : ''
    const p = c.percent === undefined ? '' : ` (${c.isEstimate ? '≈' : ''}${c.percent}%)`
    parts.push(`ctx ${fmtTok(c.tokens)}${win}${p}${c.state ? `, ${c.state}` : ''}`)
  }
  const five = pace(limitOf(s.usage, 'five_hour'), s.nowMs, FIVE_HOUR_MS)
  if (five) {
    let t = `5h ${pct(five.percent)}`
    if (five.resetsMs !== undefined) t += ` resets ${fmtClock(five.resetsMs, s.offsetMin)}`
    if (five.runOutMs !== undefined) t += `, runs out ≈${fmtClock(five.runOutMs, s.offsetMin)}`
    parts.push(t)
  }
  const seven = pace(limitOf(s.usage, 'seven_day'), s.nowMs, SEVEN_DAY_MS)
  if (seven) {
    let t = `7d ${pct(seven.percent)}`
    if (seven.projectedPct !== undefined) t += `, lands ≈${seven.projectedPct}% at reset`
    if (seven.resetsMs !== undefined) t += `, resets ${fmtWhen(seven.resetsMs, s.nowMs, s.offsetMin)}`
    parts.push(t)
  }
  // the cache hit, unless a cache alert below says it
  const alerts = alertsOf(s)
  const h = s.steps?.last ? hitPct(s.steps.last) : undefined
  if (h !== undefined && !alerts.some(a => a.key === 'cache')) parts.push(`cache ${h}%`)
  const lines = [`usage: ${parts.join(' · ')}`]
  if (alerts.length > 0) lines[0] += ` · alerts: ${alerts.map(a => a.note).join('; ')}`
  const n = nextNote(s)
  if (n) lines.push(`usage next: ${nextText(n)}`)
  return lines.join('\n')
}

// The dashboard as plain text, for /overtone.
export function usageText(s: Snapshot): string {
  const d = dashboard(s, 200)
  const out: string[] = [`usage${lineText(d.header)}`]
  if (d.jobsNote) out.push(`Workers · ${d.jobsNote}`)
  if (d.jobs.length === 0) out.push('Workers · no jobs running')
  else {
    out.push(`Workers — ${d.jobs.length}`)
    for (const j of d.jobs) {
      out.push(`  ▸ ${j.job} · ${j.doing} · asked ${j.asked} · saw ${j.saw} · ${j.elapsed} · ${stateLabel(j.state)}${j.sent ? ` · ${j.sent}` : ''}`)
    }
    if (d.jobsHidden > 0) out.push(`  +${d.jobsHidden} more`)
  }
  for (const p of d.panels) {
    const right = lineText(p.right)
    out.push(`${lineText(p.title)}${right ? ` — ${right}` : ''}`)
    for (const l of p.lines) out.push(`  ${lineText(l).trimEnd()}`)
  }
  if (d.cache) {
    out.push(`Cache — ${lineText(d.cache.right)}`)
    for (const l of d.cache.lines) out.push(`  ${lineText(l).trim()}`)
  }
  for (const a of alertsOf(s)) out.push(`alert: ${a.note}`)
  if (d.next) out.push(`next ▸ ${nextText(d.next)}`)
  return out.join('\n')
}

// The latest snapshot, kept in $.store `snapshot` (no plugin-managed file;
// $.store is host-managed); Claude gets the same figures on every prompt via
// the context line.
// Counts, states and times only; no prompt, reply or role text.
export function snapshotJson(s: Snapshot, sessionId: string | undefined): Record<string, unknown> {
  const c = readContext(s.reading)
  const five = pace(limitOf(s.usage, 'five_hour'), s.nowMs, FIVE_HOUR_MS)
  const seven = pace(limitOf(s.usage, 'seven_day'), s.nowMs, SEVEN_DAY_MS)
  const iso = (ms: number | undefined) => (ms === undefined ? undefined : new Date(ms).toISOString())
  // What Claude Code reported, apart from what overtone works out from it.
  const lim = (p: Pace | undefined) => p && { percent: p.percent, resetsAt: iso(p.resetsMs) }
  const projection = (p: Pace | undefined) =>
    p && { evenPacePercent: p.evenPct, projectedAtResetPercent: p.projectedPct, runsOutAt: iso(p.runOutMs) }
  const last = s.steps?.last
  const cache = cacheAlert(s.steps, c?.tokens, s.isWorking, s.nowMs, lifeOf(s))
  return {
    v: 2,
    source: 'overtone 0.4.1',
    writtenAt: new Date(s.nowMs).toISOString(),
    sessionId,
    summary: contextSummary(s),
    exact: {
      context: c ? { tokens: c.tokens, window: s.reading?.window, percent: c.percent, state: c.state } : null,
      fiveHour: lim(five) ?? null,
      sevenDay: lim(seven) ?? null,
      cacheLastPrompt: last ? { hitPercent: hitPct(last), resent: resent(last), read: last.cacheRead } : null,
    },
    estimates: {
      note: `projections and the cache expiry (${lifeOf(s).label}) are estimates`,
      cacheTtl: lifeOf(s).reported ? s.cacheTtl : null,
      fiveHour: projection(five) ?? null,
      sevenDay: projection(seven) ?? null,
      weeklyHeadroomPercent: seven?.projectedPct === undefined ? null : Math.max(0, 100 - seven.projectedPct),
      cacheExpiresAt: last ? iso(last.startMs + lifeOf(s).ms) : null,
      cacheCase: cache?.cold?.case ?? null,
    },
    jobs: jobsOf(s).map(j => ({ kind: j.kind, job: j.job, asked: j.asked, saw: j.saw, state: j.state, ...(j.sent ? { sent: j.sent } : {}) })),
    alerts: alertsOf(s).map(a => a.note),
    next: nextNoteText(s),
  }
}

const nextNoteText = (s: Snapshot): string | null => {
  const n = nextNote(s)
  return n ? nextText(n) : null
}
