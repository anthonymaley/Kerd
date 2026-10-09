// overtone's pure logic: no `$`, no state, nothing mutable at module level.
// The hooks module (register.tsx) and the tests both import from here.
//
// The band is one composed tree (the AbovePrompt slot is shared): row 1
// context (always, dim when calm), row 2 the model asked vs seen, rows 3+
// workers (only when there are workers). composeBand() returns its rows as
// plain segments, or undefined only when even the context is unreadable and
// nothing else needs saying, so the hook hands the slot back.

import type { OvertoneModel, OvertoneReading, OvertoneWorker, OvertoneWorkers } from '../types'

// ---------------------------------------------------------------------------
// Rows and segments: what the hook draws, as plain data
// ---------------------------------------------------------------------------

// A segment's tone. `warning` and `error` are the host's theme keys, so the
// colour follows light and dark; `dim` and `plain` carry no colour.
export type Tone = 'dim' | 'plain' | 'warning' | 'error'
export type Seg = { text: string; tone?: Tone; bold?: boolean }
// `dim` is the row's own tone: true when nothing on it crossed a threshold.
export type Row = { key: string; segs: Seg[]; dim: boolean }
export type Tier = 'wide' | 'mid' | 'narrow'

export const WIDE_AT = 100
export const MID_AT = 50
export const ROW_CAP = 3
export const RUNNING_CAP = 2

export const rowText = (row: Row): string => row.segs.map(s => s.text).join('')

// The form from the band's width: wide shows full rows with their tail,
// about 60 columns drops the optional tail, narrow is one line.
export function tierFor(bodyColumns: number): Tier {
  if (!Number.isFinite(bodyColumns) || bodyColumns >= WIDE_AT) return 'wide'
  if (bodyColumns >= MID_AT) return 'mid'
  return 'narrow'
}

const SEP = ' · '
const seg = (text: string, tone?: Tone, bold?: boolean): Seg =>
  bold ? { text, tone, bold } : tone ? { text, tone } : { text }

function joinSegs(parts: Seg[][]): Seg[] {
  const out: Seg[] = []
  parts.forEach((p, i) => {
    if (i > 0) out.push(seg(SEP))
    out.push(...p)
  })
  return out
}

function clip(text: string, max: number): string {
  const t = text.replace(/\s+/g, ' ').trim()
  return t.length <= max ? t : `${t.slice(0, max - 1)}…`
}

// ---------------------------------------------------------------------------
// Row 1: context (the rule the old ctx line used)
// ---------------------------------------------------------------------------

export type BandState = 'keep working' | 'switch at a break' | 'switch now'

// The same rule as ~/.claude/statusline-command.sh:
//   switch now         80%+ of the window used
//   switch at a break  200k+ tokens or 60%+ used
//   keep working       otherwise (under 200k and under 60%)
export function bandState(tokens: number, percent: number): BandState {
  if (percent >= 80) return 'switch now'
  if (tokens >= 200_000 || percent >= 60) return 'switch at a break'
  return 'keep working'
}

const isCount = (n: unknown): n is number => typeof n === 'number' && Number.isFinite(n) && n >= 0

export type Context = {
  tokens: number
  // The engine's percent, or tokens / window when it gave none (an estimate).
  percent?: number
  isEstimate: boolean
  // Undefined when no rule decides one (under 200k tokens with no percent).
  state?: BandState
  // Which number crossed: the percent, or the token count (the 200k rule).
  crossedBy?: 'percent' | 'tokens'
}

// Undefined before the first reading. A window is never assumed. With no
// percent the 200k rule still decides "switch at a break"; under 200k
// nothing decides a state.
export function readContext(reading: OvertoneReading | null | undefined): Context | undefined {
  if (!reading || !isCount(reading.tokens)) return undefined
  const tokens = reading.tokens
  const hasWindow = isCount(reading.window) && reading.window > 0
  const isEstimate = !isCount(reading.percent) && hasWindow
  const percent = isCount(reading.percent)
    ? reading.percent
    : hasWindow
      ? Math.round((tokens * 100) / (reading.window as number))
      : undefined
  let state: BandState | undefined
  if (percent !== undefined) state = bandState(tokens, percent)
  else if (tokens >= 200_000) state = 'switch at a break'
  let crossedBy: Context['crossedBy']
  if (state !== undefined && state !== 'keep working') {
    crossedBy = percent !== undefined && percent >= 60 ? 'percent' : 'tokens'
  }
  return { tokens, percent, isEstimate, state, crossedBy }
}

const isCrossed = (c: Context | undefined): boolean => c?.state === 'switch at a break' || c?.state === 'switch now'
const ctxTone = (c: Context): Tone | undefined =>
  c.state === 'switch now' ? 'error' : c.state === 'switch at a break' ? 'warning' : undefined

function contextRow(c: Context | undefined, tier: Exclude<Tier, 'narrow'>): Row {
  if (!c) return { key: 'ctx', segs: [seg('ctx — (no reading yet)')], dim: true }
  const tone = ctxTone(c)
  const crossed = isCrossed(c)
  const size = `ctx ${Math.floor(c.tokens / 1000)}k`
  const pct = c.percent === undefined ? undefined : `${c.isEstimate ? '≈' : ''}${c.percent}%`
  const parts: Seg[][] = [[crossed && c.crossedBy === 'tokens' ? seg(size, tone, true) : seg(size)]]
  const pctSegs = (tail: string): Seg[] =>
    crossed && c.crossedBy === 'percent' ? [seg(pct as string, tone, true), seg(tail)] : [seg(`${pct}${tail}`)]
  if (tier === 'wide') {
    parts.push(pct === undefined ? [seg('window not reported')] : pctSegs(' of window used'))
    if (c.state !== undefined) parts.push([seg(c.state)])
  } else {
    parts.push(pct === undefined ? [seg('window —')] : pctSegs(' used'))
    if (crossed) parts.push([seg(c.state as string)])
  }
  return { key: 'ctx', segs: joinSegs(parts), dim: !crossed }
}

// ---------------------------------------------------------------------------
// Row 2: model asked vs seen, and effort
// ---------------------------------------------------------------------------

// A model name reduced for comparing and showing: lower case, no provider
// prefix, no `claude-`, no `[1m]` or `(1M context)` tail, no date or version
// suffix, dots as dashes. `Opus 5.5 (1M context)` and `claude-opus-5-5`
// both become `opus-5-5`.
export function normModel(raw: string): string {
  return raw
    .toLowerCase()
    .replace(/\[[^\]]*\]|\([^)]*\)/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/^.*anthropic\./, '')
    .replace(/^claude-/, '')
    .replace(/-v\d+(?::\d+)?$/, '')
    .replace(/-\d{8}$/, '')
    .replace(/\./g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

// For the band: `opus-5-5` -> `opus-5.5`.
// Text the model wrote (a title, a task, a step note) reaches the terminal:
// control characters (C0, DEL, C1, so ESC and every escape sequence's
// introducer), and invisible format and bidi characters are dropped;
// whitespace runs fold to one space.
export const shownText = (s: string): string =>
  s
    .replace(/[\u0000-\u001f\u007f-\u009f\u00ad\u061c\u180e\u200b-\u200f\u2028-\u202e\u2060-\u206f\ufeff\ufff9-\ufffb]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()

export function showModel(rawIn: string): string {
  const raw = shownText(rawIn)
  const n = normModel(raw)
  return (n === '' ? raw : n).replace(/-(\d+)-(\d+)$/, '-$1.$2')
}

// Aliases with no fixed model behind them: no mismatch is ever claimed.
const OPEN_ALIASES = new Set(['default', 'opusplan', 'best', 'inherit'])

export type ModelMatch = 'match' | 'mismatch' | 'unknown'

// Unknown unless both sides are known. An alias (`opus`, no version) matches
// any seen model of its family.
export function compareModels(asked: string | undefined, seen: string | undefined): ModelMatch {
  if (asked === undefined || seen === undefined) return 'unknown'
  const a = normModel(asked)
  const s = normModel(seen)
  if (a === '' || s === '') return 'unknown'
  if (a === s) return 'match'
  if (!/\d/.test(a)) {
    if (OPEN_ALIASES.has(a)) return 'unknown'
    return s === a || s.startsWith(`${a}-`) ? 'match' : 'mismatch'
  }
  return 'mismatch'
}

export const EMPTY_MODEL: OvertoneModel = { steps: 0 }

// One main-loop request about to be sent. Subagent requests never come here.
export function noteStepStart(
  m: OvertoneModel | null | undefined,
  step: { sessionModel?: string; stepModel: string; effort?: string | number },
): OvertoneModel {
  const prev = m ?? EMPTY_MODEL
  const next: OvertoneModel = { ...prev, asked: step.sessionModel || step.stepModel, steps: prev.steps + 1 }
  if (step.effort === undefined) delete next.effort
  else next.effort = step.effort
  return next
}

// Its response arrived; `seen` is the API's model id, absent when no usage came.
export function noteStepEnd(m: OvertoneModel | null | undefined, seen: string | undefined): OvertoneModel {
  const prev = m ?? EMPTY_MODEL
  return seen ? { ...prev, seen } : prev
}

function modelRow(m: OvertoneModel, tier: Exclude<Tier, 'narrow'>): Row {
  if (m.steps === 0) return { key: 'model', segs: [seg(tier === 'wide' ? 'model  — (not seen yet)' : 'model —')], dim: true }
  const match = compareModels(m.asked, m.seen)
  const asked = m.asked ? showModel(m.asked) : '—'
  const seen = m.seen ? showModel(m.seen) : undefined
  const bad = match === 'mismatch'
  if (tier === 'wide') {
    const seenSegs = bad
      ? [seg(`${seen} seen · mismatch`, 'warning', true)]
      : [seg(seen ? `${seen} seen` : 'seen —')]
    const effort =
      m.effort === undefined ? 'effort — (none on the request)' : `effort ${shownText(String(m.effort))} asked, seen unavailable`
    return { key: 'model', segs: joinSegs([[seg(`model  ${asked} asked`)], seenSegs, [seg(effort)]]), dim: !bad }
  }
  if (match === 'match') return { key: 'model', segs: [seg(`model ${seen} ✓ seen`)], dim: true }
  if (bad) return { key: 'model', segs: [seg(`model ${asked} asked, ${seen} seen `), seg('≠', 'warning', true)], dim: false }
  return { key: 'model', segs: [seg(`model ${asked} asked, ${seen ?? '—'} seen`)], dim: true }
}

// ---------------------------------------------------------------------------
// Rows 3+: workers
// ---------------------------------------------------------------------------

export const EMPTY_WORKERS: OvertoneWorkers = { byId: {} }
// `unconfirmed` is overtone's own: a worker inferred over because the agent
// above it ended, never seen to end itself. It is final for counting, but it
// claims neither success nor failure, and fresh evidence of life reverses it.
export const INFERRED = 'unconfirmed'
const FINAL = new Set(['completed', 'failed', 'killed', 'error', 'cancelled', 'stopped', INFERRED])
const FAILED = new Set(['failed', 'killed', 'error', 'cancelled'])
export const isActive = (w: OvertoneWorker): boolean => !FINAL.has(w.status)
export const KEEP_FINISHED = 50

// How long a worker overtone never saw spawn may go without a tool call, with
// the latest good list read having left it out (`listed === false`: a failed
// read proves no absence), before it is called quiet rather than
// running. Ten minutes: far longer than the gap between a working subagent's
// calls (a single long call is exempt while it runs, and its end counts as activity), short enough that a
// row whose ending never reached overtone stops reading as work within one
// sitting. Quiet is only a doubt, never an ending: the row is not counted as
// running, never shown as done, and a later tool call makes it running again.
export const QUIET_AFTER_MS = 10 * 60_000

export function isQuiet(w: OvertoneWorker, nowMs: number | undefined): boolean {
  if (nowMs === undefined || !isActive(w) || w.fromSpawn || w.listed !== false || w.blocked) return false
  if (Object.keys(w.pending).length > 0) return false
  return nowMs - (w.lastToolMs ?? w.firstSeenMs) >= QUIET_AFTER_MS
}

// Active and not quiet: what the band counts as running.
export const isRunning = (w: OvertoneWorker, nowMs: number | undefined): boolean => isActive(w) && !isQuiet(w, nowMs)

export const quietCount = (w: OvertoneWorkers | null | undefined, nowMs: number | undefined): number =>
  Object.values((w ?? EMPTY_WORKERS).byId).filter(x => isQuiet(x, nowMs)).length

// A tool call in a line: the tool and what it touches, never more than a
// short line. Only the first line of a command is kept.
export function summarizeTool(tool: string, input: unknown): string {
  const i = (input ?? {}) as Record<string, unknown>
  const str = (k: string): string | undefined => (typeof i[k] === 'string' ? (i[k] as string) : undefined)
  const base = (p: string): string => p.split('/').filter(Boolean).pop() ?? p
  const name = tool.startsWith('mcp__') ? (tool.split('__').pop() ?? tool) : tool
  let what: string | undefined
  if (tool === 'Bash') what = str('command')?.split('\n')[0]
  else if (str('file_path')) what = base(str('file_path') as string)
  else if (str('notebook_path')) what = base(str('notebook_path') as string)
  else if (str('pattern')) what = str('pattern')
  else if (str('url')) what = str('url')?.replace(/^https?:\/\//, '').split('/')[0]
  else if (str('description')) what = str('description')
  return clip(what ? `${name} ${what}` : name, 48)
}

function prune(byId: Record<string, OvertoneWorker>): Record<string, OvertoneWorker> {
  const done = Object.values(byId)
    .filter(w => !isActive(w))
    .sort((a, b) => (b.endedMs ?? b.firstSeenMs) - (a.endedMs ?? a.firstSeenMs))
  if (done.length <= KEEP_FINISHED) return byId
  const out = { ...byId }
  for (const w of done.slice(KEEP_FINISHED)) delete out[w.id]
  return out
}

function blank(id: string, nowMs: number, fromSpawn: boolean): OvertoneWorker {
  return { id, label: `agent ${id.slice(0, 8)}`, type: 'agent', status: 'running', firstSeenMs: nowMs, fromSpawn, tools: 0, pending: {} }
}

const ws = (w: OvertoneWorkers | null | undefined): OvertoneWorkers => w ?? EMPTY_WORKERS

// What a list read says is still alive: a status that is not final. A
// worker it names this way is never ended on a guess.
const liveIds = (list: readonly ListedAgent[]): Set<string> =>
  new Set(list.filter(a => a && typeof a.id === 'string' && !FINAL.has(a.status ?? '')).map(a => a.id))

// The agents under `roots`, which are over, are inferred over too (`unconfirmed`,
// not `completed`: absence is no evidence of success), unless something shows
// them alive: the list names them, a call is pending or waits on a permission,
// or they made a call after their root ended. Such a worker is kept, and so is
// everything below it. One pass over a parent -> children map built once.
function endUnder(
  byId: Record<string, OvertoneWorker>,
  roots: readonly string[],
  live: ReadonlySet<string>,
  nowMs: number,
): Record<string, OvertoneWorker> {
  const kids = new Map<string, string[]>()
  for (const x of Object.values(byId)) {
    if (x.parentId === undefined) continue
    const l = kids.get(x.parentId)
    if (l) l.push(x.id)
    else kids.set(x.parentId, [x.id])
  }
  const out = { ...byId }
  const seen = new Set(roots)
  const queue = roots.map(id => ({ id, at: byId[id]?.endedMs ?? nowMs }))
  for (let i = 0; i < queue.length; i++) {
    const { id, at } = queue[i] as { id: string; at: number }
    for (const c of kids.get(id) ?? []) {
      if (seen.has(c)) continue
      seen.add(c)
      const x = out[c]
      if (!x) continue
      if (isActive(x)) {
        if (live.has(c) || x.blocked || Object.keys(x.pending).length > 0 || (x.lastToolMs ?? -Infinity) > at) continue
        const next: OvertoneWorker = { ...x, status: INFERRED, endedMs: nowMs, pending: {} }
        delete next.blocked
        out[c] = next
      }
      queue.push({ id: c, at })
    }
  }
  return out
}

export function noteSpawn(
  w: OvertoneWorkers | null | undefined,
  s: { id: string; description?: string; name?: string; type?: string; parentId?: string; nowMs: number },
): OvertoneWorkers {
  const prev = ws(w)
  const old = prev.byId[s.id]
  const worker: OvertoneWorker = {
    ...(old ?? blank(s.id, s.nowMs, true)),
    label: clip(s.description || s.name || s.type || old?.label || s.id, 56),
    type: s.type || old?.type || 'agent',
    // `nowMs` is taken before the spawn ran: the earliest sign of the worker.
    firstSeenMs: Math.min(old?.firstSeenMs ?? s.nowMs, s.nowMs),
    fromSpawn: true,
    ...(s.parentId ? { parentId: s.parentId } : {}),
    // the description as given, for matching a plan task (the label is cut)
    ...(s.description ? { description: s.description.slice(0, 300) } : {}),
  }
  return { ...prev, byId: prune({ ...prev.byId, [s.id]: worker }) }
}

export type ListedAgent = { id: string; description?: string; type?: string; status?: string; name?: string; parentId?: string }

// A good $.agent.list() read. A worker overtone saw end keeps its own ending
// even when the list still says running; one the list no longer names keeps
// what overtone last knew. It also records each worker's parent, notes who
// the list named (for the quiet rule), and ends what is left under a worker
// that is over: its descendants the list does not name as alive.
export function noteList(w: OvertoneWorkers | null | undefined, list: readonly ListedAgent[], nowMs: number): OvertoneWorkers {
  const prev = ws(w)
  let byId = { ...prev.byId }
  const named = new Set(list.filter(a => a && typeof a.id === 'string').map(a => a.id))
  for (const id of Object.keys(byId)) byId[id] = { ...(byId[id] as OvertoneWorker), listed: named.has(id) }
  for (const a of list) {
    if (!a || typeof a.id !== 'string') continue
    const old = byId[a.id] ?? blank(a.id, nowMs, false)
    const listed = typeof a.status === 'string' && a.status !== '' ? a.status : old.status
    // An ending overtone saw stands; an inferred one gives way to the list.
    const status = old.endedMs !== undefined && old.status !== INFERRED ? old.status : listed
    // A guessed ending time is replaced by the time the list confirmed it.
    const ended = FINAL.has(status) ? ((old.status === INFERRED ? undefined : old.endedMs) ?? nowMs) : undefined
    const label = byId[a.id] ? old.label : clip(a.description || a.name || a.type || old.label, 56)
    const next: OvertoneWorker = { ...old, label, type: a.type || old.type, status, listed: true }
    if (next.description === undefined && typeof a.description === 'string' && a.description !== '') next.description = a.description.slice(0, 300)
    if (typeof a.parentId === 'string' && a.parentId !== '') next.parentId = a.parentId
    if (ended === undefined) delete next.endedMs
    else {
      next.endedMs = ended
      delete next.blocked
      next.pending = {}
    }
    byId[a.id] = next
  }
  // Roots are confirmed endings only: an inferred one carries its root's time,
  // so the cutoff for "made a call after it ended" never moves later.
  byId = endUnder(byId, Object.values(byId).filter(x => !isActive(x) && x.status !== INFERRED).map(x => x.id), liveIds(list), nowMs)
  return { byId: prune(byId) }
}

export function noteListError(w: OvertoneWorkers | null | undefined, reason: string): OvertoneWorkers {
  return { ...ws(w), error: clip(reason || 'read failed', 60) }
}

export function noteToolStart(
  w: OvertoneWorkers | null | undefined,
  t: { agentId: string; toolUseId?: string; summary: string; nowMs: number },
): OvertoneWorkers {
  const prev = ws(w)
  let old = prev.byId[t.agentId] ?? blank(t.agentId, t.nowMs, false)
  if (old.status === INFERRED) {
    // a call is fresh evidence of life: the inferred ending is undone
    old = { ...old, status: 'running' }
    delete old.endedMs
  } else if (!isActive(old)) return prev
  const pending = t.toolUseId ? { ...old.pending, [t.toolUseId]: t.summary } : old.pending
  return { ...prev, byId: { ...prev.byId, [t.agentId]: { ...old, activity: t.summary, tools: old.tools + 1, pending, lastToolMs: t.nowMs } } }
}

// `nowMs`, when given, is activity too: a call that ran long is not quiet the
// moment it returns.
export function noteToolEnd(
  w: OvertoneWorkers | null | undefined,
  t: { agentId: string; toolUseId?: string; nowMs?: number },
): OvertoneWorkers {
  const prev = ws(w)
  const old = prev.byId[t.agentId]
  if (!old) return prev
  const pending = { ...old.pending }
  if (t.toolUseId) delete pending[t.toolUseId]
  const next: OvertoneWorker = { ...old, pending }
  if (t.nowMs !== undefined && isActive(old)) next.lastToolMs = t.nowMs
  if (old.blocked && old.blocked.toolUseId === t.toolUseId) delete next.blocked
  return { ...prev, byId: { ...prev.byId, [t.agentId]: next } }
}

// A permission ask on a call a worker is making: that worker is blocked
// until the call settles. Calls no worker made change nothing.
export function noteAsk(w: OvertoneWorkers | null | undefined, a: { toolUseId: string; nowMs: number }): OvertoneWorkers {
  const prev = ws(w)
  const owner = Object.values(prev.byId).find(x => isActive(x) && x.pending[a.toolUseId] !== undefined)
  if (!owner) return prev
  const blocked = { what: `wants to run ${owner.pending[a.toolUseId]}`, sinceMs: a.nowMs, toolUseId: a.toolUseId }
  return { ...prev, byId: { ...prev.byId, [owner.id]: { ...owner, blocked } } }
}

export function noteEnd(
  w: OvertoneWorkers | null | undefined,
  e: { agentId: string; failed: boolean; nowMs: number; listed?: readonly ListedAgent[] },
): OvertoneWorkers {
  const prev = ws(w)
  const old = prev.byId[e.agentId]
  if (!old) return prev
  const next: OvertoneWorker = { ...old, status: e.failed ? 'failed' : 'completed', endedMs: e.nowMs, pending: {} }
  delete next.blocked
  let byId = { ...prev.byId, [e.agentId]: next }
  // Its descendants end with it, but only against a good list read: with none,
  // the next read (noteList) does it, so nothing running is ended on a guess.
  if (e.listed) byId = endUnder(byId, [e.agentId], liveIds(e.listed), e.nowMs)
  return { ...prev, byId: prune(byId) }
}

export function fmtDuration(ms: number): string {
  const s = Math.max(0, Math.floor(ms / 1000))
  if (s < 60) return `${s}s`
  const m = Math.floor(s / 60)
  if (m < 60) return `${m}m`
  return `${Math.floor(m / 60)}h${String(m % 60).padStart(2, '0')}m`
}

export type Fold = { blocked: OvertoneWorker[]; running: OvertoneWorker[]; quiet: OvertoneWorker[]; shown: OvertoneWorker[]; hidden: number }

// Blocked first (longest waiting first), never folded away; then the newest
// running, at most RUNNING_CAP of them and no more than ROW_CAP rows in all
// unless blocked ones alone take more. The rest fold into `+N more`. With
// `nowMs`, quiet workers are set apart: not running, not drawn as rows.
export function foldWorkers(w: OvertoneWorkers | null | undefined, nowMs?: number): Fold {
  const all = Object.values(ws(w).byId).filter(isActive)
  const quiet = all.filter(x => isQuiet(x, nowMs))
  const active = all.filter(x => !isQuiet(x, nowMs))
  const blocked = active
    .filter(x => x.blocked)
    .sort((a, b) => (a.blocked as { sinceMs: number }).sinceMs - (b.blocked as { sinceMs: number }).sinceMs)
  const running = active.filter(x => !x.blocked).sort((a, b) => b.firstSeenMs - a.firstSeenMs)
  const room = Math.max(0, Math.min(RUNNING_CAP, ROW_CAP - blocked.length))
  const shownRunning = running.slice(0, room)
  return { blocked, running, quiet, shown: [...blocked, ...shownRunning], hidden: running.length - shownRunning.length }
}

// Finished workers grouped by type, most first: `✓ Explore ×3`.
export function finishedGroups(w: OvertoneWorkers | null | undefined): { ok: [string, number][]; failed: [string, number][] } {
  const ok = new Map<string, number>()
  const failed = new Map<string, number>()
  for (const x of Object.values(ws(w).byId)) {
    if (isActive(x) || x.status === INFERRED) continue
    const m = FAILED.has(x.status) ? failed : ok
    const type = shownText(x.type)
    m.set(type, (m.get(type) ?? 0) + 1)
  }
  const sort = (m: Map<string, number>) => [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  return { ok: sort(ok), failed: sort(failed) }
}

function workerRows(w: OvertoneWorkers, nowMs: number, tier: Exclude<Tier, 'narrow'>): Row[] {
  const f = foldWorkers(w, nowMs)
  const nBlocked = f.blocked.length
  const nRunning = f.running.length
  const lead = tier === 'wide' ? 'workers  ' : 'workers '
  const head: Seg[][] = []
  if (nBlocked > 0) head.push([seg(`${nBlocked} blocked`, 'warning', true)])
  if (nRunning > 0 || nBlocked === 0) head.push([seg(`${nRunning} running`)])
  if (f.quiet.length > 0) head.push([seg(`${f.quiet.length} quiet`)])
  if (tier === 'wide') {
    const g = finishedGroups(w)
    for (const [type, n] of g.ok.slice(0, 2)) head.push([seg(`✓ ${type} ×${n}`)])
    for (const [type, n] of g.failed.slice(0, 1)) head.push([seg(`✕ ${type} ×${n}`)])
  }
  if (w.error !== undefined) {
    head.push([seg(tier === 'wide' ? `status unavailable · ${shownText(w.error)}` : 'status unavailable', 'warning', true)])
  }
  const rows: Row[] = [{ key: 'workers', segs: [seg(lead), ...joinSegs(head)], dim: nBlocked === 0 && w.error === undefined }]
  const since = (x: OvertoneWorker, from: number) => `${x.fromSpawn ? '' : '≥'}${fmtDuration(nowMs - from)}`
  for (const x of f.shown) {
    // A long task takes the room only on a wide running row; a blocked row keeps
    // room for what it waits on, a short row for its time.
    const label = clip(shownText(x.label), x.blocked ? 24 : tier === 'wide' ? 56 : 32)
    if (x.blocked) {
      const waited = fmtDuration(nowMs - x.blocked.sinceMs)
      if (tier === 'wide') {
        rows.push({ key: `w-${x.id}`, segs: [seg(`■ ${label}`, 'plain', true), seg(`  blocked: ${shownText(x.blocked.what)}`)], dim: false })
        rows.push({ key: `w-${x.id}-2`, segs: [seg(`    waiting ${waited} · answer the permission prompt`)], dim: true })
      } else {
        rows.push({ key: `w-${x.id}`, segs: [seg(`■ ${label}`, 'plain', true), seg(` · blocked: ${shownText(x.blocked.what)}`)], dim: false })
      }
      continue
    }
    if (tier === 'wide') {
      const calls = `${x.tools} tool call${x.tools === 1 ? '' : 's'}`
      rows.push({ key: `w-${x.id}`, segs: [seg(`▸ ${label}`)], dim: true })
      rows.push({ key: `w-${x.id}-2`, segs: [seg(`    ${since(x, x.firstSeenMs)} · ${calls}`)], dim: true })
    } else {
      rows.push({ key: `w-${x.id}`, segs: [seg(`▸ ${label} · ${since(x, x.firstSeenMs)}`)], dim: true })
    }
  }
  if (f.hidden > 0) rows.push({ key: 'w-more', segs: [seg(`${tier === 'wide' ? '    ' : ''}+${f.hidden} more running`)], dim: true })
  return rows
}

// ---------------------------------------------------------------------------
// The composed band
// ---------------------------------------------------------------------------

export type BandInput = {
  reading: OvertoneReading | null | undefined
  model: OvertoneModel | null | undefined
  workers: OvertoneWorkers | null | undefined
  nowMs: number
}

export type Band = { tier: Tier; rows: Row[] }

// What needs saying beyond a calm context reading: a context threshold
// crossed, a model mismatch, a worker running or blocked, or a worker read
// that failed. These decide colour and emphasis, not whether the band shows:
// a readable context always draws the band (calm = dim).
export function needsBand(i: BandInput): boolean {
  const w = ws(i.workers)
  return (
    isCrossed(readContext(i.reading)) ||
    compareModels(i.model?.asked, i.model?.seen) === 'mismatch' ||
    Object.values(w.byId).some(x => isRunning(x, i.nowMs)) ||
    w.error !== undefined
  )
}

// The one line: alerts first (blocked, model, context) when any; else the
// calm summary.
function narrowRow(i: BandInput): Row {
  const c = readContext(i.reading)
  const m = i.model ?? EMPTY_MODEL
  const w = ws(i.workers)
  const f = foldWorkers(w, i.nowMs)
  const match = compareModels(m.asked, m.seen)
  const alerts: Seg[][] = []
  if (f.blocked.length > 0) alerts.push([seg(`${f.blocked.length} blocked`, 'warning', true)])
  if (w.error !== undefined) alerts.push([seg('workers unavailable', 'warning', true)])
  if (match === 'mismatch') alerts.push([seg('model '), seg('≠', 'warning', true)])
  if (c && isCrossed(c)) {
    const n = c.crossedBy === 'percent' ? `${c.isEstimate ? '≈' : ''}${c.percent}%` : `${Math.floor(c.tokens / 1000)}k`
    alerts.push([seg('ctx '), seg(n, ctxTone(c), true)])
  }
  if (alerts.length > 0) return { key: 'narrow', segs: joinSegs(alerts), dim: false }
  const calm: Seg[][] = []
  if (c) {
    const pct = c.percent === undefined ? '' : `${SEP}${c.isEstimate ? '≈' : ''}${c.percent}%`
    calm.push([seg(`ctx ${Math.floor(c.tokens / 1000)}k${pct}`)])
  } else calm.push([seg('ctx —')])
  if (m.seen) calm.push([seg(`${showModel(m.seen)}${match === 'match' ? ' ✓' : ''}`)])
  const n = f.running.length
  if (n > 0) calm.push([seg(`${n} worker${n === 1 ? '' : 's'}`)])
  return { key: 'narrow', segs: joinSegs(calm), dim: true }
}

// The band: the context row always, then the model row, then workers rows
// when there are workers. Undefined (the slot goes back) only when the
// context is unreadable and nothing else needs saying.
export function composeBand(i: BandInput, bodyColumns: number, maxRows: number = Infinity): Band | undefined {
  if (readContext(i.reading) === undefined && !needsBand(i)) return undefined
  const tier = tierFor(bodyColumns)
  if (tier !== 'narrow') {
    const rows = [contextRow(readContext(i.reading), tier), modelRow(i.model ?? EMPTY_MODEL, tier), ...workerRowsIf(i, tier)]
    if (!(rows.length > maxRows)) return { tier, rows }
  }
  return { tier: 'narrow', rows: [narrowRow(i)] }
}

function workerRowsIf(i: BandInput, tier: Exclude<Tier, 'narrow'>): Row[] {
  const w = ws(i.workers)
  return Object.values(w.byId).some(isActive) || w.error !== undefined ? workerRows(w, i.nowMs, tier) : []
}

// The band as plain text, for /overtone: always the wide form, and the
// context and model rows even before a context reading arrives.
export function bandText(i: BandInput): string {
  const band = composeBand(i, WIDE_AT)
  if (band) return band.rows.map(rowText).join('\n')
  return [contextRow(readContext(i.reading), 'wide'), modelRow(i.model ?? EMPTY_MODEL, 'wide')].map(rowText).join('\n')
}
