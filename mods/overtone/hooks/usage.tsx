// overtone 0.4: the usage band (dashboard-v3). One line above the prompt
// (collapsed, the default): three bars of what is left (context window,
// 5-hour and weekly allowance, each in its usual tone), the cache hit, and
// red alerts only while they fire. A
// click on its `▸ usage` Button, or the chord of its engine action
// (BAND_ACTION, ctrl+x b), opens it in place: the jobs (workers and Kerd
// Agent partner requests) first, then Context, 5-hour and Weekly, a Cache
// card only when the cache went cold or is about to, and a next line only
// when something needs him.
//
// It also holds 0.2's session.start, session.measure and turn.step hooks
// (the context reading, the model asked vs seen): the engine takes one
// unmatched registration of an event per plugin, and `$` may only be handed
// to a function of the same file.
//
// Beyond drawing:
// - prompt.submit: one short line of the same figures (alerts and a next
//   line only when they fire) attached to the prompt's `context`. The
//   prompt's text is passed on as it came.
// - session.measure: the latest figures kept in $.store `snapshot` (no
//   plugin-managed file; $.store is host-managed). Claude gets the same
//   figures on every prompt (the context line above), which is what Switch
//   Out reads.
// - Partner rows: Kerd Agent's request records for this project, read-only
//   from `git rev-parse --git-path kerd-agent` (requests/*.json, aliases
//   from partners/*.json): at most every 30 s; of the records written in the
//   last three hours (each under 256 KB), newest first, at most 40 are read
//   and the first 12 that are this project's pending or just-answered
//   requests are kept (arrival notices and other projects never count). Nothing there is written, and the
//   helper's own `status` command (which takes a lock and may update the
//   record) is never run. Only alias, provider, role, status and times are
//   kept; prompt and reply text are not.
// - session.start also registers overtone's `step` tool (STEP_SPEC in
//   plan-logic.ts): a subagent reports its own done/total steps; and its
//   `plan` tool (PLAN_SPEC): Kerd Conductor reports its score. Matched hooks
//   in register.tsx answer both.
// - classic.PostModelSwitch: the prompt-cache TTL Claude Code reports there
//   (`cache_ttl`, on a model switch and when a resume restores the model);
//   without one the cache is assumed to live 1 hour.
// - Timers from session.start ($.clock.after, $.clock.every): the first
//   partner read 1.5 s after start, then a tick every 15 s that moves the
//   countdowns and re-reads partners when due. A hook's `$` ends with its
//   dispatch, so nothing is left running from any other hook.
//
// Safety contract: every hook passes its event on (`next`); only
// prompt.submit adds to it (context). Each hook's own work sits in try/catch
// and each registration has a `.catch` that calls `next` only when the hook
// never reached it.

import { atom, read, update } from 'claude-code'
import type { Elements, EngineInterface, Register } from 'claude-code'

import type {
  OvertoneModel,
  OvertonePartnerRow,
  OvertonePartners,
  OvertonePlan,
  OvertoneReading,
  OvertoneSteps,
  OvertoneUsage,
  OvertoneView,
  OvertoneWorkers,
} from '../types'
import { EMPTY_MODEL, EMPTY_WORKERS, bandText, noteList, noteListError, noteStepEnd, noteStepStart } from './logic'
import { EMPTY_PLAN, PLAN_SPEC, STEP_SPEC, planView } from './plan-logic'
import type { PlanView } from './plan-logic'
import { HEX, isAnimating, leftBarCells, planBand, planCard, toneRgb } from './plan-draw'
import type { CardRow, PSeg } from './plan-draw'
import {
  BAND_ACTION,
  BUTTON_ROOM,
  COLLAPSED_LABEL,
  EMPTY_STEPS,
  EMPTY_VIEW,
  EXPANDED_LABEL,
  SEP,
  aliasMap,
  cell,
  collapsedLine,
  contextSummary,
  dashboard,
  dashboardRows,
  hasFigures,
  jobColumns,
  jobTitle,
  lineWidth,
  workerPlanView,
  noteMainStep,
  noteWorkerModel,
  noteWorkerSeen,
  partnerRow,
  snapshotJson,
  stateLabel,
  stateTone,
  toggleView,
  usageText,
} from './usage-logic'
import type { JobRow, Snapshot, StepUsage, ULine, UTone } from './usage-logic'

const reading = atom({ plugin: 'overtone', key: 'reading' } as const, null)
const model = atom({ plugin: 'overtone', key: 'model' } as const, EMPTY_MODEL)
const workers = atom({ plugin: 'overtone', key: 'workers' } as const, EMPTY_WORKERS)
const usage = atom({ plugin: 'overtone', key: 'usage' } as const, null)
const steps = atom({ plugin: 'overtone', key: 'steps' } as const, EMPTY_STEPS)
const partners = atom({ plugin: 'overtone', key: 'partners' } as const, null)
const cacheTtl = atom({ plugin: 'overtone', key: 'cacheTtl' } as const, null)
const view = atom({ plugin: 'overtone', key: 'view' } as const, EMPTY_VIEW)
const plan = atom({ plugin: 'overtone', key: 'plan' } as const, EMPTY_PLAN)
// The plan drawing's animation frame; it moves only while a row runs or waits.
const anim = atom({ plugin: 'overtone', key: 'frame' } as const, 0)
const tick = atom({ plugin: 'overtone', key: 'tick' } as const, 0)

// Theme keys for the tones that carry colour.
const COLOR: Partial<Record<UTone, string>> = { success: 'success', warning: 'warning', error: 'error' }

const TICK_MS = 15_000
const FAST_MS = 500
const PARTNER_EVERY_MS = 30_000
const PARTNER_FILES = 12
const PARTNER_READS = 40
const PARTNER_WINDOW_MS = 3 * 3_600_000
const PARTNER_MAX_BYTES = 256 * 1024
const ALIAS_EVERY_MS = 5 * 60_000

// Module state: the timers, and the partner reader's caches. A reload starts
// them over (the old timers are cancelled with the old environment).
let ticker: { cancel: () => void } | undefined
let first: { cancel: () => void } | undefined
// The plan drawing's fast ticker, and a closure over session.start's `$` that
// starts or stops it (a render hook's `$` ends with its dispatch, so only
// session.start's may hold a timer).
let fast: { cancel: () => void } | undefined
let syncer: (() => Promise<void>) | undefined
let polling = false
let agentDir: { root: string; dir: string | null } | undefined
let aliases: { root: string; atMs: number; map: Record<string, string> } | undefined

const errText = (err: unknown): string => (err instanceof Error ? err.message : String(err))

type Context = { tokens?: number; window: number; percent?: number }

const toReading = (c: Context): OvertoneReading => ({
  tokens: c.tokens,
  window: c.window,
  percent: c.percent,
})

type Usage = Awaited<ReturnType<EngineInterface['session']['usage']>>

async function readUsage($: EngineInterface, u: Usage): Promise<OvertoneUsage> {
  let sessionId: string | undefined
  try {
    sessionId = await $.session.id()
  } catch {
    sessionId = undefined
  }
  const out: OvertoneUsage = {
    rateLimits: u.rateLimits.map(l => ({ kind: l.kind, percentUsed: l.percentUsed, resetsAt: l.resetsAt })),
    measuredMs: await $.clock.now(),
  }
  if (sessionId !== undefined) out.sessionId = sessionId
  return out
}

async function snapshotOf($: EngineInterface, isWorking: boolean): Promise<Snapshot> {
  const nowMs = await $.clock.now()
  const ttl = (await read($, cacheTtl))?.ttl
  return {
    ...(ttl ? { cacheTtl: ttl } : {}),
    nowMs,
    offsetMin: -new Date(nowMs).getTimezoneOffset(),
    isWorking,
    reading: await read($, reading),
    model: await read($, model),
    usage: await read($, usage),
    steps: await read($, steps),
    workers: await read($, workers),
    partners: await read($, partners),
    plan: await read($, plan),
  }
}

// Starts the 500 ms frame ticker while some plan row is running or needs
// you, and cancels it when none is. Called when the drawing renders and by
// the ticker itself. Fail open.
async function syncFrame($: EngineInterface): Promise<void> {
  try {
    // the real plan when one is sent, else the workers drawn as one
    const s = await snapshotOf($, false)
    const real = planView(s.plan, s.workers, s.nowMs)
    const v = real.total > 0 ? real : workerPlanView(s)
    const on = v !== undefined && isAnimating(v)
    if (on && !fast) {
      fast = $.clock.every(FAST_MS, () => {
        void (async () => {
          try {
            await update($, anim, (n: number) => (n + 1) % 1_000_000)
            await syncFrame($)
          } catch {
            // fail open
          }
        })()
      })
    } else if (!on && fast) {
      fast.cancel()
      fast = undefined
    }
  } catch {
    // fail open
  }
}

// The latest figures in $.store `snapshot`. Best effort; no plugin-managed
// file ($.store is host-managed).
async function writeSnapshot($: EngineInterface): Promise<void> {
  const s = await snapshotOf($, false)
  await $.store.set('snapshot', snapshotJson(s, s.usage?.sessionId))
}

async function readJson($: EngineInterface, path: string): Promise<unknown> {
  try {
    return JSON.parse(await $.fs.read(path))
  } catch {
    return undefined
  }
}

// Kerd Agent's request records for this project, read-only, bounded.
async function pollPartners($: EngineInterface): Promise<void> {
  if (polling) return
  polling = true
  try {
    const now = await $.clock.now()
    const root = await $.session.root()
    if (agentDir?.root !== root) {
      const r = await $.process.run(['git', 'rev-parse', '--path-format=absolute', '--git-path', 'kerd-agent'], {
        cwd: root,
        timeoutMs: 5_000,
      })
      const dir = r.exitCode === 0 ? r.stdout.trim() : ''
      agentDir = { root, dir: dir !== '' ? dir : null }
    }
    const dir = agentDir.dir
    const none = async (note: string) => {
      await update($, partners, () => ({ polledMs: now, rows: [], note }) satisfies OvertonePartners)
    }
    if (dir === null) return await none('not in a git repository')
    if (!(await $.fs.exists(`${dir}/requests`))) return await none('no Kerd Agent requests in this project')
    if (!aliases || aliases.root !== root || now - aliases.atMs >= ALIAS_EVERY_MS) {
      const records: unknown[] = []
      if (await $.fs.exists(`${dir}/partners`)) {
        const list = await $.fs.list(`${dir}/partners`)
        for (const f of list.filter(x => x.kind === 'file' && x.name.endsWith('.json') && x.size <= PARTNER_MAX_BYTES).slice(0, 64)) {
          records.push(await readJson($, `${dir}/partners/${f.name}`))
        }
      }
      aliases = { root, atMs: now, map: aliasMap(records) }
    }
    // Newest first, within the window; each record read is checked (this
    // project, a request that expects a reply, a status that matters) before
    // it counts. At most PARTNER_READS reads, at most PARTNER_FILES rows.
    const recent = (await $.fs.list(`${dir}/requests`))
      .filter(x => x.kind === 'file' && x.name.endsWith('.json') && x.size <= PARTNER_MAX_BYTES && now - x.mtimeMs <= PARTNER_WINDOW_MS)
      .sort((a, b) => b.mtimeMs - a.mtimeMs)
      .slice(0, PARTNER_READS)
    const rows: OvertonePartnerRow[] = []
    for (const f of recent) {
      if (rows.length >= PARTNER_FILES) break
      const rec = await readJson($, `${dir}/requests/${f.name}`)
      const row = rec && typeof rec === 'object' ? partnerRow(rec, root, aliases.map, now) : undefined
      if (row) rows.push(row)
    }
    await update($, partners, () => ({ polledMs: now, rows }) satisfies OvertonePartners)
  } catch (err) {
    try {
      const now = await $.clock.now()
      await update($, partners, (p: OvertonePartners | null) => ({
        polledMs: now,
        rows: p?.rows ?? [],
        note: `partner records unreadable: ${errText(err).slice(0, 60)}`,
      }))
    } catch {
      // fail open
    }
  } finally {
    polling = false
  }
}

// From the session.start hook, after `next`: the exact figures, the first
// partner read and the tick.
async function usageOnStart($: EngineInterface): Promise<void> {
  try {
    const u = await $.session.usage()
    const value = await readUsage($, u)
    await update($, usage, () => value)
  } catch {
    // fail open
  }
  try {
    // Work that outlives a dispatch runs on the session's timers.
    syncer = () => syncFrame($)
    fast?.cancel()
    fast = undefined
    ticker?.cancel()
    first?.cancel()
    first = $.clock.after(1_500, () => {
      void pollPartners($).catch(() => undefined)
    })
    ticker = $.clock.every(TICK_MS, () => {
      void (async () => {
        try {
          const now = await $.clock.now()
          await update($, tick, () => now)
          const p = await read($, partners)
          if (!p || now - p.polledMs >= PARTNER_EVERY_MS) await pollPartners($)
        } catch {
          // fail open
        }
      })()
    })
  } catch {
    ticker = undefined
    first = undefined
  }
  void syncFrame($)
}

export const register: Register = on => {
  // Registers /overtone and takes what a resumed or reloaded session already
  // has. `session.start` fires once per process (and again on a reload), not
  // after /clear; a registered command stays for the session.
  on('session.start', async ($, e, next) => {
    try {
      await $.command.register({
        name: 'overtone',
        description: 'The overtone usage band as text: jobs, context, 5-hour, weekly, cache alerts.',
      })
    } catch {
      // fail open
    }
    try {
      // The worker step tool, mcp__overtone__step; register.tsx answers it.
      // Awaited before `next`, so it is listed by turn one.
      await $.tool.register({ ...STEP_SPEC, inputSchema: { ...STEP_SPEC.inputSchema } })
    } catch {
      // fail open: no step tool, workers just report nothing
    }
    try {
      // The plan tool, mcp__overtone__plan, for Kerd Conductor's score.
      await $.tool.register({ ...PLAN_SPEC, inputSchema: { ...PLAN_SPEC.inputSchema } })
    } catch {
      // fail open: no plan tool, the plan comes from the task tools alone
    }
    try {
      const u = await $.session.usage()
      if (u.context.tokens !== undefined) await update($, reading, () => toReading(u.context))
    } catch {
      // fail open
    }
    try {
      const list = await $.agent.list()
      const now = await $.clock.now()
      await update($, workers, w => noteList(w, list, now))
    } catch {
      // fail open: no workers known yet is not a failed read worth showing
    }
    const started = await next(e)
    await usageOnStart($)
    return started
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // After each main-thread turn: the context reading, a fresh read of the
  // workers, the windows; then the snapshot in $.store (host-managed).
  on('session.measure', async ($, e, next) => {
    try {
      const u = await $.session.usage()
      await update($, reading, () => toReading(u.context))
      const value = await readUsage($, { ...u, rateLimits: e.rateLimits })
      await update($, usage, () => value)
    } catch {
      // fail open
    }
    try {
      const list = await $.agent.list()
      const now = await $.clock.now()
      await update($, workers, w => noteList(w, list, now))
    } catch (err) {
      try {
        await update($, workers, w => noteListError(w, errText(err)))
      } catch {
        // fail open
      }
    }
    const measured = await next(e)
    try {
      await writeSnapshot($)
    } catch {
      // fail open: the band does not depend on the file
    }
    return measured
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // Every model request. The main loop's: the model asked (the session's as
  // /model shows it, else the request's) and seen, the effort asked, and its
  // ModelUsage for the cache. A worker's: the model and effort it sent and
  // the model that answered (asked vs saw).
  on('turn.step', async function* ($, e, next) {
    const agentId = e.agentId
    if (agentId !== undefined) {
      try {
        await update($, workers, (w: OvertoneWorkers) => noteWorkerModel(w, agentId, e.model, e.effort))
      } catch {
        // fail open
      }
      const sub = yield* next(e)
      try {
        const seen = sub.usage?.model
        await update($, workers, (w: OvertoneWorkers) => noteWorkerSeen(w, agentId, seen))
      } catch {
        // fail open
      }
      return sub
    }
    let startMs = 0
    try {
      startMs = await $.clock.now()
      let sessionModel: string | undefined
      try {
        sessionModel = await $.session.model()
      } catch {
        sessionModel = undefined
      }
      await update($, model, (m: OvertoneModel) =>
        noteStepStart(m, { sessionModel, stepModel: e.model, effort: e.effort }),
      )
    } catch {
      // fail open
    }
    const result = yield* next(e)
    try {
      await update($, model, (m: OvertoneModel) => noteStepEnd(m, result.usage?.model))
      const u: StepUsage | null = result.usage
      if (u) {
        const now = await $.clock.now()
        await update($, steps, (s: OvertoneSteps) => noteMainStep(s, u, startMs || now, now))
      }
    } catch {
      // fail open
    }
    return result
  }).catch(async function* ($, e, next) {
    return yield* next(e)
  })

  // The prompt-cache TTL, where Claude Code reports it: after a model switch
  // and when a resume restores the model. Observed only; passed on as it came.
  on('classic.PostModelSwitch', async ($, e, next) => {
    try {
      const ttl = e.cache_ttl
      if (ttl === '5m' || ttl === '1h') {
        const now = await $.clock.now()
        await update($, cacheTtl, () => ({ ttl, atMs: now }))
      }
    } catch {
      // fail open
    }
    return next(e)
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // Claude sees the same figures: one short line beside the prompt.
  on('prompt.submit', async ($, e, next) => {
    let line: string | undefined
    try {
      // the person is prompting: no "send the next prompt" expiry note
      line = contextSummary(await snapshotOf($, true))
    } catch {
      line = undefined
    }
    if (line === undefined) return next(e)
    return next({ ...e, context: [...(e.context ?? []), line] })
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    let s: Snapshot
    let expanded: boolean
    try {
      await read($, tick)
      s = await snapshotOf($, e.props.isWorking)
      expanded = (await read($, view)).expanded
    } catch {
      return next(e)
    }
    if (!hasFigures(s)) return next(e)
    const ui = $.ui.resolve(e)
    const { Box, Text, Button } = ui
    // Raster is the terminal's alone; elsewhere (or without it) the plan is text.
    const Raster = e.surface === 'terminal' && 'Raster' in ui ? (ui as Elements['terminal']).Raster : undefined
    let pv: PlanView | undefined
    let fr = 0
    try {
      if (s.plan) {
        const v = planView(s.plan, s.workers, s.nowMs)
        if (v.total > 0) {
          pv = v
          fr = await read($, anim)
          void syncer?.()
        }
      }
    } catch {
      pv = undefined
    }
    // No plan sent: the workers are drawn as a plan of their own (the same
    // rows), never on the collapsed band.
    let wv: PlanView | undefined
    if (!pv) {
      try {
        wv = workerPlanView(s)
        if (wv && isAnimating(wv)) {
          fr = await read($, anim)
          void syncer?.()
        }
      } catch {
        wv = undefined
      }
    }
    const toggle = () => {
      void update($, view, (v: OvertoneView) => toggleView(v))
    }
    const segs = (line: ULine, key: string) =>
      line.map((sg, i) =>
        sg.tone === undefined ? (
          sg.text
        ) : (
          <Text key={`${key}-${i}`} color={COLOR[sg.tone]} bold={sg.bold} dimColor={sg.tone === 'dim' ? true : undefined}>
            {sg.text}
          </Text>
        ),
      )
    // The band line with Raster bars: one element per segment in a row.
    const rasterLine = (line: ULine, key: string) => (
      <Box key={`${key}-r`} flexDirection="row">
        <Text key={`${key}-pad`}>{'  '}</Text>
        {line.map((sg, i) =>
          sg.bar && Raster ? (
            <Raster key={`${key}-${i}`} columns={sg.text.length} rows={1} cells={leftBarCells(sg.text.length, sg.bar.left / 100, toneRgb(sg.tone))} />
          ) : (
            <Text
              key={`${key}-${i}`}
              color={sg.tone ? COLOR[sg.tone] : undefined}
              bold={sg.bold}
              dimColor={sg.tone === 'dim' ? true : undefined}
              wrap="truncate-end"
            >
              {sg.text}
            </Text>
          ),
        )}
      </Box>
    )
    const pseg = (list: PSeg[], key: string) =>
      list.map((p, i) => (
        <Text key={`${key}-${i}`} color={p.color} bold={p.bold ? true : undefined} dimColor={p.dim ? true : undefined}>
          {p.text}
        </Text>
      ))
    const beneath = await next(e)
    const cols = e.props.bodyColumns
    // The band line, the same folded and opened but for the button's label:
    // usage bars, the plan group, then the plain button last.
    const bandLine = (label: string) => {
      // The plan takes what the usage figures leave; it shrinks, then goes.
      const line = collapsedLine(s, cols, Raster !== undefined)
      const drawn = Raster !== undefined && line.some(sg => sg.bar)
      const band = pv
        ? planBand(pv, (Number.isFinite(cols) ? cols : 200) - BUTTON_ROOM - lineWidth(line), Raster !== undefined, fr)
        : undefined
      return (
        <Box key="band" flexDirection="row">
          {drawn ? (
            rasterLine(line, 'c')
          ) : (
            <Text key="line" wrap="truncate-end">
              {'  '}
              {segs(line, 'c')}
            </Text>
          )}
          {band ? (
            <Box key="plan" flexDirection="row">
              <Text key="plan-sep" dimColor>
                {SEP}
              </Text>
              <Text key="plan-dot" color={HEX.done}>
                {'● '}
              </Text>
              <Text key="plan-label" bold>
                {`${band.label} `}
              </Text>
              {band.bar.cells && Raster ? (
                <Raster key="plan-bar" columns={band.bar.cols} rows={1} cells={band.bar.cells} />
              ) : (
                <Text key="plan-bar">{pseg(band.bar.text ?? [], 'plan-bar')}</Text>
              )}
              <Text key="plan-count" bold>
                {` ${band.count}`}
              </Text>
            </Box>
          ) : (
            ''
          )}
          <Text key="btn-gap">{'  '}</Text>
          <Button key="usage" label={label} plain action={BAND_ACTION} onPress={toggle} />
        </Box>
      )
    }
    if (!expanded) {
      return (
        <Box flexDirection="column">
          <Text key="space"> </Text>
          {bandLine(COLLAPSED_LABEL)}
          {beneath}
        </Box>
      )
    }
    const d = dashboard(s, cols, e.props.maxRows)
    const frame = (key: string, tone?: UTone) => ({
      key,
      flexDirection: 'column' as const,
      borderStyle: d.panelBorder ? 'round' : undefined,
      borderColor: d.panelBorder && tone ? COLOR[tone] : undefined,
      borderDimColor: d.panelBorder && !tone ? true : undefined,
      paddingX: 1,
    })
    const titleRow = (key: string, left: ULine, right: ULine) => (
      <Box key={`${key}-head`} flexDirection="row" justifyContent="space-between">
        <Text key="t" wrap="truncate-end">
          {segs(left, `${key}-t`)}
        </Text>
        <Text key="r" wrap="truncate-end">
          {segs(right, `${key}-r`)}
        </Text>
      </Box>
    )
    const col = jobColumns(cols)
    const jobRow = (j: JobRow) => {
      const bad = j.state === 'wrong model'
      return (
        <Text key={j.key} wrap="truncate-end">
          <Text dimColor>{'▸ '}</Text>
          <Text bold>{cell(jobTitle(j, col.job), col.job)}</Text>
          {cell(j.asked, col.asked)}
          <Text color={bad ? 'error' : undefined} bold={bad ? true : undefined}>
            {cell(j.saw, col.saw)}
          </Text>
          {cell(j.elapsed, col.elapsed)}
          <Text color={COLOR[stateTone(j.state)]} dimColor={stateTone(j.state) === 'dim' ? true : undefined} bold={bad ? true : undefined}>
            {stateLabel(j.state)}
          </Text>
          {j.sent ? <Text color="warning">{` · ${j.sent}`}</Text> : ''}
        </Text>
      )
    }
    const planRow = (r: CardRow) => (
      <Box key={r.key} flexDirection="row" gap={1}>
        {r.mark.cells && Raster ? (
          <Raster key={`m-${r.key}`} columns={2} rows={1} cells={r.mark.cells} />
        ) : (
          <Text key={`m-${r.key}`} color={r.mark.glyph?.color}>
            {r.mark.glyph?.text ?? ' '}
          </Text>
        )}
        <Text
          key={`n-${r.key}`}
          bold={r.state !== 'todo' ? true : undefined}
          dimColor={r.state === 'todo' ? true : undefined}
          color={r.wrong ? HEX.needs : undefined}
        >
          {r.name}
        </Text>
        {r.bar.cells && Raster ? (
          <Raster key={`b-${r.key}`} columns={r.bar.cols} rows={1} cells={r.bar.cells} />
        ) : (
          <Text key={`b-${r.key}`}>{pseg(r.bar.text ?? [], `b-${r.key}`)}</Text>
        )}
        {r.model ? <Text key={`o-${r.key}`}>{pseg([r.model], `o-${r.key}`)}</Text> : ''}
        {r.effort ? <Text key={`e-${r.key}`}>{pseg([r.effort], `e-${r.key}`)}</Text> : ''}
        {r.detail ? (
          <Text key={`d-${r.key}`} wrap="truncate-end">
            {pseg([r.detail], `d-${r.key}`)}
          </Text>
        ) : (
          ''
        )}
      </Box>
    )
    // With a plan the Workers card is one line per plan row; Kerd Agent
    // partner requests keep their own lines beneath. The quiet count and the
    // note stay.
    let planCardEl: unknown = ''
    const cardView = pv ?? wv
    if (cardView && !d.jobsOff) {
      const partnerJobs = d.jobs.filter(j => j.kind === 'partner')
      const inner = Math.max(30, (Number.isFinite(cols) ? cols : 200) - (d.panelBorder ? 4 : 0))
      const room =
        e.props.maxRows - dashboardRows({ ...d, jobsOff: true }) - (d.panelBorder ? 2 : 0) - 1 - partnerJobs.length
      const card = planCard(cardView, inner, Raster !== undefined, fr, Math.max(0, room))
      planCardEl = (
        <Box {...frame('p-jobs')}>
          {titleRow(
            'jobs',
            [
              { text: 'Workers', tone: 'plain', bold: true },
              { text: `  ${card.header}`, tone: 'dim' },
            ],
            [
              ...(d.jobsQuiet ? [{ text: `${d.jobsQuiet} quiet`, tone: 'dim' as const }] : []),
              ...(d.jobsNote ? [{ text: `${d.jobsQuiet ? ' · ' : ''}${d.jobsNote}`, tone: 'warning' as const }] : []),
            ],
          )}
          {card.rows.map(planRow)}
          {partnerJobs.map(jobRow)}
        </Box>
      )
    }
    return (
      <Box flexDirection="column">
        <Box flexDirection="column">
          {bandLine(EXPANDED_LABEL)}
          {d.jobsOff ? (
            ''
          ) : cardView ? (
            planCardEl
          ) : d.jobs.length === 0 && d.jobsHidden === 0 ? (
            <Text key="no-jobs" wrap="truncate-end">
              <Text dimColor>{`▸ Workers · no jobs running${d.jobsQuiet ? ` · ${d.jobsQuiet} quiet` : ''}`}</Text>
              {d.jobsNote ? <Text color="warning">{` · ${d.jobsNote}`}</Text> : ''}
            </Text>
          ) : (
            <Box {...frame('p-jobs')}>
              {d.jobsCompact
                ? titleRow(
                    'jobs',
                    [{ text: 'Workers', tone: 'plain', bold: true }],
                    [
                      { text: String(d.jobs.length + d.jobsHidden) },
                      ...(d.jobsQuiet ? [{ text: ` · ${d.jobsQuiet} quiet`, tone: 'dim' as const }] : []),
                      ...(d.jobsHidden > 0 && d.jobs.length > 0 ? [{ text: ` · +${d.jobsHidden} more`, tone: 'dim' as const }] : []),
                      ...(d.jobsNote ? [{ text: ` · ${d.jobsNote}`, tone: 'warning' as const }] : []),
                    ],
                  )
                : titleRow('jobs', [{ text: 'Workers', tone: 'plain', bold: true }, { text: ' running now, asked vs saw', tone: 'dim' }], [{ text: String(d.jobs.length) }, ...(d.jobsQuiet ? [{ text: ` · ${d.jobsQuiet} quiet`, tone: 'dim' as const }] : [])])}
              {d.jobsCompact ? (
                ''
              ) : (
                <Text key="jobs-cols" dimColor wrap="truncate-end">
                  {`  ${cell('job', col.job)}${cell('asked', col.asked)}${cell('saw', col.saw)}${cell('elapsed', col.elapsed)}state`}
                </Text>
              )}
              {d.jobs.map(jobRow)}
              {!d.jobsCompact && d.jobsHidden > 0 ? (
                <Text key="jobs-more" dimColor>
                  {`  +${d.jobsHidden} more`}
                </Text>
              ) : (
                ''
              )}
              {!d.jobsCompact && d.jobsNote ? (
                <Text key="jobs-note" color="warning" wrap="truncate-end">
                  {d.jobsNote}
                </Text>
              ) : (
                ''
              )}
            </Box>
          )}
          {d.cache ? (
            <Box {...frame('p-cache', 'error')}>
              {titleRow('cache', [{ text: 'Cache', tone: 'plain', bold: true }, { text: ' shown only when it fires: hit under 80%, or about to expire', tone: 'dim' }], d.cache.right)}
              {d.cache.lines.map((l, i) => (
                <Text key={`cache-${i}`} wrap="truncate-end">
                  {segs(l, `cache-${i}`)}
                </Text>
              ))}
            </Box>
          ) : (
            ''
          )}
          {d.next ? (
            <Text key="next" wrap="truncate-end">
              <Text dimColor>next ▸ </Text>
              <Text color={COLOR[d.next.tone]} bold>
                {d.next.lead}
              </Text>
              {d.next.rest ? ` — ${d.next.rest}` : ''}
            </Text>
          ) : (
            ''
          )}
        </Box>
        {beneath}
      </Box>
    )
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // /overtone: the dashboard as text, then 0.2's context, model and workers rows.
  on('command.run', { command: 'overtone' }, async $ => {
    try {
      try {
        const u = await $.session.usage()
        const value = await readUsage($, u)
        await update($, usage, () => value)
        if (u.context.tokens !== undefined) await update($, reading, () => toReading(u.context))
      } catch {
        // the last reading stands
      }
      const s = await snapshotOf($, false)
      const rows = bandText({ reading: s.reading, model: s.model, workers: s.workers, nowMs: s.nowMs })
      return { text: `overtone\n${usageText(s)}\n\n${rows}` }
    } catch {
      return { text: 'overtone: the figures could not be read.' }
    }
  })
}
