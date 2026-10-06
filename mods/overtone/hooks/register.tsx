// overtone's workers, as 0.2 gathered them: spawns, their tool calls,
// permission asks and endings. Since 0.3 the usage band (usage.tsx) draws
// them, and also holds 0.2's session.start, session.measure and turn.step
// hooks (the context reading, the model asked vs seen): the engine takes one
// unmatched registration of an event per plugin, and `$` may only be handed
// to a function of the same file. This module only observes.
//
// Safety contract:
// - Observe only. Every hook passes its event on as it came, `next(e)`, the
//   same object, and returns what `next` resolved to; nothing is rewritten,
//   denied, appended or submitted; no process, file write or network call.
// - Fail open. Each hook's own work sits in try/catch, and each registration
//   has a `.catch`. The plain hooks' catch hands the event on only when the
//   hook never reached `next`; once it had (`next.called`), it returns
//   undefined and the engine keeps that call's own result. The streaming
//   `turn.step` catch always continues the stream with `next(e)`, which in a
//   `.catch` is replay-safe: after the hook's own call it gives back what that
//   call settled to, the hooks beneath not running again. Either way nothing
//   beneath runs twice. An error in overtone leaves the session as if
//   overtone were absent.
// - Reload safe. No module-level mutable state and no timers: everything the
//   band draws lives in $.state, so register() may run again.
// - `$` is used only as the hook's own argument, never handed to a closure
//   or helper. All formatting, tiers and folding live in logic.ts.

import { atom, update } from 'claude-code'
import type { AgentInfo, Register } from 'claude-code'

import type { OvertoneWorkers } from '../types'
import { EMPTY_WORKERS, noteAsk, noteEnd, noteList, noteSpawn, noteToolEnd, noteToolStart, summarizeTool } from './logic'
import { noteAsked } from './usage-logic'

const workers = atom({ plugin: 'overtone', key: 'workers' } as const, EMPTY_WORKERS)

export const register: Register = on => {
  // Rows 3+. A spawn: its label and type, timed from before it started.
  on('agent.spawn', async ($, e, next) => {
    let t0: number | undefined
    try {
      t0 = await $.clock.now()
    } catch {
      t0 = undefined
    }
    const result = await next(e)
    try {
      if (result.agentId !== undefined && t0 !== undefined) {
        const id = result.agentId
        const s = { id, description: e.description, name: e.name, type: e.subagentType, parentId: e.parentAgentId, nowMs: t0 }
        await update($, workers, (w: OvertoneWorkers) => noteSpawn(w, s))
        // what the spawn asked for: the Agent call's model, or a kerd:<model>-<effort> type
        await update($, workers, (w: OvertoneWorkers) => noteAsked(w, id, { model: e.model, type: e.subagentType }))
      }
    } catch {
      // fail open
    }
    return result
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // A worker's tool call: its activity now, and the pending call so a
  // permission ask on it can be told apart. Main-loop calls pass untouched.
  on('tool.call', async ($, e, next) => {
    if (e.agentId === undefined) return next(e)
    const agentId = e.agentId
    const toolUseId = e.tool_use_id
    try {
      const now = await $.clock.now()
      const summary = summarizeTool(String(e.tool), e)
      await update($, workers, (w: OvertoneWorkers) => noteToolStart(w, { agentId, toolUseId, summary, nowMs: now }))
    } catch {
      // fail open
    }
    const result = await next(e)
    try {
      await update($, workers, (w: OvertoneWorkers) => noteToolEnd(w, { agentId, toolUseId }))
    } catch {
      // fail open
    }
    return result
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // A permission ask on a worker's pending call marks that worker blocked
  // until the call settles. The verdict is passed on as it came.
  on('tool.check', async ($, e, next) => {
    const result = await next(e)
    try {
      const toolUseId = e.tool_use_id
      if (result.decision === 'ask' && toolUseId !== undefined) {
        const now = await $.clock.now()
        await update($, workers, (w: OvertoneWorkers) => noteAsk(w, { toolUseId, nowMs: now }))
      }
    } catch {
      // fail open
    }
    return result
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  // A turn ended. A worker's: finished, or failed on an error or abort, and
  // what it spawned ends with it, judged against a list read taken first. The
  // main loop's: just the list read, so rows whose ending never came are
  // reconciled even when no subagent ends.
  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    try {
      const now = await $.clock.now()
      let list: AgentInfo[] | undefined
      try {
        list = await $.agent.list()
      } catch {
        list = undefined
      }
      if (e.agentId !== undefined) {
        const agentId = e.agentId
        const failed = e.reason !== 'answer'
        await update($, workers, (w: OvertoneWorkers) => noteEnd(w, { agentId, failed, nowMs: now, listed: list }))
      }
      if (list !== undefined) {
        const read = list
        await update($, workers, (w: OvertoneWorkers) => noteList(w, read, now))
      }
    } catch {
      // fail open
    }
    return result
  }).catch(($, e, next) => (next.called ? undefined : next(e)))
}
