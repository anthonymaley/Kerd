// overtone's plan: pure logic, no `$`, no state, nothing mutable at module
// level. register.tsx folds the main loop's task-list calls (TaskCreate,
// TaskUpdate, TodoWrite) and its own `plan` tool calls (Kerd Conductor's
// score) into OvertonePlan, and records a worker's own `step` reports; the
// plan view (plan-draw.ts) reads planView(). Whichever source wrote last
// owns the plan.
//
// Matching: a worker belongs to a task when its normalized Agent description
// equals the task's normalized subject or activeForm. Each worker serves at
// most one task; workers no task claims and still running follow the tasks.

import type { OvertonePlan, OvertoneStep, OvertoneTask, OvertoneTaskStatus, OvertoneWorker, OvertoneWorkers } from '../types'
import { EMPTY_WORKERS, isActive, isRunning } from './logic'

export const EMPTY_PLAN: OvertonePlan = { source: 'none', tasks: [], nextN: 1 }

// Tasks kept at most; past it the oldest finished (completed or deleted) go.
export const PLAN_CAP = 100

// The worker step tool: registered as `step`, which the model calls as
// `mcp__overtone__step` (`mcp__<plugin>__<name>`, plugin.json's name).
export const STEP_NAME = 'step'
export const STEP_TOOL = 'mcp__overtone__step'
export const STEP_SPEC = {
  name: STEP_NAME,
  description:
    'For a subagent only: report your own progress through your assigned job, in one cheap call. ' +
    'Call it when you finish a step: `done` steps finished so far of `total` steps you expect, ' +
    'with an optional short `note` (a few words on the step just finished). It changes nothing ' +
    'and returns at once; the person sees it beside your job. The main conversation should not call it.',
  inputSchema: {
    type: 'object',
    properties: {
      done: { type: 'integer', minimum: 0, description: 'Steps finished so far.' },
      total: { type: 'integer', minimum: 1, description: 'Steps you expect in all.' },
      note: { type: 'string', maxLength: 80, description: 'A few words on the step just finished.' },
    },
    required: ['done', 'total'],
    additionalProperties: false,
  },
  isDeferred: false,
} as const

export const TASK_TOOLS: ReadonlySet<string> = new Set(['TaskCreate', 'TaskUpdate', 'TodoWrite'])

// The plan tool: registered as `plan`, called as `mcp__overtone__plan`. Kerd
// Conductor reports its score through it where the task tools are not given
// to the model. Its description sits in every session's context: short.
export const PLAN_NAME = 'plan'
export const PLAN_TOOL = 'mcp__overtone__plan'
export const PLAN_SPEC = {
  name: PLAN_NAME,
  description:
    "For Kerd Conductor: report the score to overtone's plan view. At the go send title and tasks (the full list, in order); " +
    'after each accepted task send accepted; at the end send finished: true. Each task subject must equal the Agent ' +
    'description that task is dispatched with, so its worker matches. Fields left out keep their values.',
  inputSchema: {
    type: 'object',
    properties: {
      title: { type: 'string', maxLength: 80, description: 'The plan in a few words.' },
      tasks: {
        type: 'array',
        description: 'The full ordered task list; replaces it, keeping the status of subjects that stay.',
        items: { type: 'object', properties: { subject: { type: 'string' } }, required: ['subject'] },
      },
      accepted: {
        description: 'Subjects accepted, or how many of the first tasks are.',
        anyOf: [{ type: 'array', items: { type: 'string' } }, { type: 'integer', minimum: 0 }],
      },
      running: { type: 'array', items: { type: 'string' }, description: 'Subjects in progress now.' },
      finished: { type: 'boolean', description: 'true closes the plan.' },
    },
    additionalProperties: false,
  },
  isDeferred: false,
} as const

const STATUSES: ReadonlySet<string> = new Set(['pending', 'in_progress', 'completed', 'deleted'])
const FAILED: ReadonlySet<string> = new Set(['failed', 'killed', 'error', 'cancelled'])

const rec = (x: unknown): Record<string, unknown> => (x && typeof x === 'object' ? (x as Record<string, unknown>) : {})
const str = (x: unknown): string | undefined => (typeof x === 'string' && x.trim() !== '' ? x.trim() : undefined)
const statusOf = (x: unknown): OvertoneTaskStatus | undefined =>
  typeof x === 'string' && STATUSES.has(x) ? (x as OvertoneTaskStatus) : undefined
const isFinal = (t: OvertoneTask): boolean => t.status === 'completed' || t.status === 'deleted'

// For matching: case, punctuation and spacing do not count.
export function normTask(raw: string | undefined): string {
  return (raw ?? '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim()
}

// A status set at `nowMs`: the first in_progress starts the clock, completed
// or deleted stops it, and a task reopened loses its finish.
function withStatus(t: OvertoneTask, status: OvertoneTaskStatus, nowMs: number): OvertoneTask {
  if (status === t.status) return t
  const next: OvertoneTask = { ...t, status }
  if (status === 'in_progress' && next.startedMs === undefined) next.startedMs = nowMs
  if (status === 'completed' || status === 'deleted') next.finishedMs = nowMs
  else delete next.finishedMs
  return next
}

function capped(tasks: OvertoneTask[]): OvertoneTask[] {
  if (tasks.length <= PLAN_CAP) return tasks
  let drop = tasks.length - PLAN_CAP
  return tasks.filter(t => {
    if (drop > 0 && isFinal(t)) {
      drop--
      return false
    }
    return true
  })
}

// The tool's outcome as `tool.call` resolved: a deny, an errored call, or an
// answered one with its record in `result`.
export type PlanCall = { tool: string; input: unknown; ran: unknown; nowMs: number }

// One main-loop call folded into the plan. A deny, an error, a refused update
// (`success: false` or an `error`), an unknown task, or any other tool:
// the plan as it was.
export function notePlanCall(plan: OvertonePlan | null | undefined, call: PlanCall): OvertonePlan {
  const prev = plan ?? EMPTY_PLAN
  if (!TASK_TOOLS.has(call.tool)) return prev
  const ran = rec(call.ran)
  if (ran.deny !== undefined || ran.isError === true) return prev
  const input = rec(call.input)
  const result = rec(ran.result)
  if (call.tool === 'TaskCreate') return taskCreate(prev, input, result, call.nowMs)
  if (call.tool === 'TaskUpdate') return taskUpdate(prev, input, result, call.nowMs)
  return todoWrite(prev, input, result, call.nowMs)
}

function taskCreate(prev: OvertonePlan, input: Record<string, unknown>, result: Record<string, unknown>, nowMs: number): OvertonePlan {
  const made = rec(result.task)
  const id = typeof made.id === 'string' && made.id !== '' ? made.id : undefined
  const subject = str(made.subject) ?? str(input.subject)
  if (id === undefined || subject === undefined) return prev
  // A todo list gives way to a task list.
  const base = prev.source === 'task' ? prev : EMPTY_PLAN
  const kept = base.tasks.filter(t => t.id !== id)
  const task: OvertoneTask = { id, n: base.nextN, subject, status: 'pending', createdMs: nowMs }
  const activeForm = str(input.activeForm)
  if (activeForm) task.activeForm = activeForm
  return { source: 'task', tasks: capped([...kept, task]), nextN: base.nextN + 1, updatedMs: nowMs }
}

function taskUpdate(prev: OvertonePlan, input: Record<string, unknown>, result: Record<string, unknown>, nowMs: number): OvertonePlan {
  if (prev.source !== 'task') return prev
  if (result.success === false || result.error !== undefined) return prev
  const id = typeof input.taskId === 'string' ? input.taskId : typeof result.taskId === 'string' ? result.taskId : undefined
  if (id === undefined || !prev.tasks.some(t => t.id === id)) return prev
  const status = statusOf(input.status)
  const subject = str(input.subject)
  const activeForm = str(input.activeForm)
  if (status === undefined && subject === undefined && activeForm === undefined) return prev
  const tasks = prev.tasks.map(t => {
    if (t.id !== id) return t
    let next: OvertoneTask = { ...t }
    if (subject) next.subject = subject
    if (activeForm) next.activeForm = activeForm
    if (status) next = withStatus(next, status, nowMs)
    return next
  })
  return { ...prev, tasks, updatedMs: nowMs }
}

type Todo = { content: string; status: OvertoneTaskStatus; activeForm?: string }

function todosOf(x: unknown): Todo[] | undefined {
  if (!Array.isArray(x)) return undefined
  const out: Todo[] = []
  for (const raw of x) {
    const t = rec(raw)
    const content = str(t.content)
    if (!content) continue
    const status = statusOf(t.status) ?? 'pending'
    const activeForm = str(t.activeForm)
    out.push(activeForm ? { content, status, activeForm } : { content, status })
  }
  return out
}

// TodoWrite replaces the whole list. Items are kept by their text, so a todo
// that stays keeps its number and times; one that went is dropped. The
// result's newTodos is read first; an empty newTodos beside an input whose
// todos are all completed is taken as the list finished (the input), not
// cleared (not verified against the live tool).
function todoWrite(prev: OvertonePlan, input: Record<string, unknown>, result: Record<string, unknown>, nowMs: number): OvertonePlan {
  const fromResult = todosOf(result.newTodos)
  const fromInput = todosOf(input.todos)
  let todos = fromResult ?? fromInput
  if (todos === undefined) return prev
  if (todos.length === 0 && fromInput && fromInput.length > 0 && fromInput.every(t => t.status === 'completed')) todos = fromInput
  const base = prev.source === 'todo' ? prev : EMPTY_PLAN
  const left = [...base.tasks]
  let nextN = base.nextN
  const tasks = todos.map(td => {
    const at = left.findIndex(t => normTask(t.subject) === normTask(td.content))
    const old = at >= 0 ? left.splice(at, 1)[0] : undefined
    let task: OvertoneTask
    if (old) task = { ...old, subject: td.content }
    else {
      task = { id: `todo-${nextN}`, n: nextN, subject: td.content, status: 'pending', createdMs: nowMs }
      nextN++
    }
    if (td.activeForm) task.activeForm = td.activeForm
    else delete task.activeForm
    return withStatus(task, td.status, nowMs)
  })
  return { source: 'todo', tasks, nextN, updatedMs: nowMs }
}

// ---------------------------------------------------------------------------
// Worker steps
// ---------------------------------------------------------------------------

export type StepInput = { done: number; total: number; note?: string }

// The step tool's input, or undefined when it is not one: `done` an integer
// of at least 0, `total` an integer of at least 1. `done` past `total` is
// held at `total`; the note is cut to 80 characters.
export function readStep(input: unknown): StepInput | undefined {
  const i = rec(input)
  const { done, total } = i
  if (typeof done !== 'number' || !Number.isInteger(done) || done < 0) return undefined
  if (typeof total !== 'number' || !Number.isInteger(total) || total < 1) return undefined
  const note = str(i.note)?.replace(/\s+/g, ' ')
  const out: StepInput = { done: Math.min(done, total), total }
  if (note) out.note = note.length <= 80 ? note : `${note.slice(0, 79)}…`
  return out
}

// A worker's own step report. A worker not yet known is added (the step may
// be its first call overtone sees); one already over keeps what it had.
export function noteStep(
  w: OvertoneWorkers | null | undefined,
  s: { agentId: string; step: StepInput; nowMs: number },
): OvertoneWorkers {
  const prev = w ?? EMPTY_WORKERS
  const old: OvertoneWorker = prev.byId[s.agentId] ?? {
    id: s.agentId,
    label: `agent ${s.agentId.slice(0, 8)}`,
    type: 'agent',
    status: 'running',
    firstSeenMs: s.nowMs,
    fromSpawn: false,
    tools: 0,
    pending: {},
  }
  if (!isActive(old)) return prev
  const steps: OvertoneStep = { ...s.step, atMs: s.nowMs }
  return { ...prev, byId: { ...prev.byId, [s.agentId]: { ...old, steps } } }
}

// What the step tool answers.
export const STEP_MAIN_ANSWER = 'ignored: step is for subagents reporting their own progress; the main conversation keeps its plan in its task list'
export const STEP_BAD_ANSWER = 'ignored: done must be an integer of at least 0 and total an integer of at least 1'
export const stepAnswer = (s: StepInput): string => `recorded ${s.done}/${s.total}`

// ---------------------------------------------------------------------------
// Rows for the plan card
// ---------------------------------------------------------------------------

export type PlanRowState = 'done' | 'running' | 'needs' | 'todo' | 'failed'

export type PlanRow = {
  key: string
  // A task of the plan, or a running worker no task claims.
  kind: 'task' | 'worker'
  // A task row's place among the drawn tasks, 1..total (deleted tasks are not
  // drawn and take no number). Absent on a worker row.
  n?: number
  taskId?: string
  // The task's subject, or the unmatched worker's label.
  title: string
  activeForm?: string
  state: PlanRowState
  // The task's (a worker row: the worker's first sight and ending).
  startedMs?: number
  finishedMs?: number
  // The matched worker as the workers state holds it: asked/askedEffort (what
  // the spawn asked), model/effort (what its requests sent), seen (what
  // answered), blocked, status.
  worker?: OvertoneWorker
  // The worker's own step report, when it made one.
  steps?: OvertoneStep
}

export type PlanTotals = { accepted: number; total: number }

// `title`: the plan tool's title, when it gave one.
export type PlanView = PlanTotals & { title?: string; rows: PlanRow[] }

// accepted: tasks completed; total: tasks not deleted.
export function planTotals(plan: OvertonePlan | null | undefined): PlanTotals {
  const live = (plan ?? EMPTY_PLAN).tasks.filter(t => t.status !== 'deleted')
  return { accepted: live.filter(t => t.status === 'completed').length, total: live.length }
}

// Which candidate serves a task: blocked first, then running, then the
// newest seen.
function rank(x: OvertoneWorker, nowMs: number): number {
  if (isActive(x) && x.blocked) return 3
  if (isRunning(x, nowMs)) return 2
  if (isActive(x)) return 1
  return 0
}

function taskState(t: OvertoneTask, x: OvertoneWorker | undefined, nowMs: number): PlanRowState {
  if (t.status === 'completed') return 'done'
  if (x && isActive(x) && x.blocked) return 'needs'
  if (x && !isActive(x) && FAILED.has(x.status)) return 'failed'
  if (t.status === 'in_progress' || (x && isRunning(x, nowMs))) return 'running'
  return 'todo'
}

export function planRows(
  plan: OvertonePlan | null | undefined,
  workers: OvertoneWorkers | null | undefined,
  nowMs: number,
): PlanRow[] {
  // In the plan's own order (creation order for TaskCreate; the list's order
  // for TodoWrite and the plan tool).
  const tasks = (plan ?? EMPTY_PLAN).tasks.filter(t => t.status !== 'deleted')
  const all = Object.values((workers ?? EMPTY_WORKERS).byId)
  const claimed = new Set<string>()
  const rows: PlanRow[] = tasks.map((t, i) => {
    const keys = new Set([normTask(t.subject), normTask(t.activeForm)].filter(k => k !== ''))
    const x = all
      .filter(w => !claimed.has(w.id) && keys.has(normTask(w.description)))
      .sort((a, b) => rank(b, nowMs) - rank(a, nowMs) || b.firstSeenMs - a.firstSeenMs)[0]
    if (x) claimed.add(x.id)
    const row: PlanRow = { key: `t-${t.id}`, kind: 'task', n: i + 1, taskId: t.id, title: t.subject, state: taskState(t, x, nowMs) }
    if (t.activeForm) row.activeForm = t.activeForm
    if (t.startedMs !== undefined) row.startedMs = t.startedMs
    if (t.finishedMs !== undefined) row.finishedMs = t.finishedMs
    if (x) row.worker = x
    if (x?.steps) row.steps = x.steps
    return row
  })
  const loose = all.filter(w => !claimed.has(w.id) && isRunning(w, nowMs)).sort((a, b) => a.firstSeenMs - b.firstSeenMs)
  for (const x of loose) {
    const row: PlanRow = { key: `w-${x.id}`, kind: 'worker', title: x.label, state: x.blocked ? 'needs' : 'running', startedMs: x.firstSeenMs, worker: x }
    if (x.steps) row.steps = x.steps
    rows.push(row)
  }
  return rows
}

export function planView(
  plan: OvertonePlan | null | undefined,
  workers: OvertoneWorkers | null | undefined,
  nowMs: number,
): PlanView {
  // A plan the plan tool closed is drawn no more.
  if (!plan || plan.closed) return { accepted: 0, total: 0, rows: [] }
  const v: PlanView = { ...planTotals(plan), rows: planRows(plan, workers, nowMs) }
  if (plan.title) v.title = plan.title
  return v
}

// ---------------------------------------------------------------------------
// The plan tool (Kerd Conductor's score)
// ---------------------------------------------------------------------------

export type PlanInput = {
  title?: string
  tasks?: string[]
  accepted?: string[] | number
  running?: string[]
  finished?: boolean
}

const strList = (x: unknown): string[] | undefined =>
  Array.isArray(x) && x.every(v => typeof v === 'string') ? (x as string[]).map(v => v.trim()).filter(v => v !== '') : undefined

// The plan tool's input, or undefined when a field it gives is malformed.
// Fields left out stay out (they keep the plan's values).
export function readPlan(input: unknown): PlanInput | undefined {
  const i = rec(input)
  const out: PlanInput = {}
  if (i.title !== undefined) {
    if (typeof i.title !== 'string') return undefined
    out.title = i.title.replace(/\s+/g, ' ').trim().slice(0, 80)
  }
  if (i.tasks !== undefined) {
    if (!Array.isArray(i.tasks)) return undefined
    const subjects: string[] = []
    for (const t of i.tasks) {
      const subject = str(rec(t).subject)
      if (subject === undefined) return undefined
      subjects.push(subject)
    }
    out.tasks = subjects
  }
  if (i.accepted !== undefined) {
    if (typeof i.accepted === 'number') {
      if (!Number.isInteger(i.accepted) || i.accepted < 0) return undefined
      out.accepted = i.accepted
    } else {
      const list = strList(i.accepted)
      if (list === undefined) return undefined
      out.accepted = list
    }
  }
  if (i.running !== undefined) {
    const list = strList(i.running)
    if (list === undefined) return undefined
    out.running = list
  }
  if (i.finished !== undefined) {
    if (typeof i.finished !== 'boolean') return undefined
    out.finished = i.finished
  }
  return out
}

// One plan tool call folded in.
// - title: set (empty clears it).
// - tasks: the full ordered list; a subject that stays keeps its task (number,
//   status, times), a new one is pending, one left out goes.
// - running: the subjects in progress now; one no longer named that was
//   running goes back to pending (its start kept). A completed task stays so.
// - accepted: subjects, or the first N tasks, set completed. It only adds:
//   an earlier acceptance is never taken back.
// - finished: true closes the plan (planView draws nothing); false reopens.
// A call naming a title or tasks after the plan was closed, or while another
// source owned it, starts a fresh plan.
export function notePlanTool(plan: OvertonePlan | null | undefined, input: PlanInput, nowMs: number): OvertonePlan {
  const prev = plan ?? EMPTY_PLAN
  const fresh = prev.source !== 'tool' || (prev.closed === true && (input.title !== undefined || input.tasks !== undefined))
  let next: OvertonePlan = fresh ? { source: 'tool', tasks: [], nextN: 1 } : { ...prev }
  if (input.title !== undefined) {
    if (input.title === '') delete next.title
    else next.title = input.title
  }
  if (input.tasks !== undefined) {
    const left = [...next.tasks]
    let nextN = next.nextN
    next.tasks = input.tasks.map(subject => {
      const at = left.findIndex(t => normTask(t.subject) === normTask(subject))
      const old = at >= 0 ? left.splice(at, 1)[0] : undefined
      if (old) return { ...old, subject }
      const task: OvertoneTask = { id: `plan-${nextN}`, n: nextN, subject, status: 'pending', createdMs: nowMs }
      nextN++
      return task
    })
    next.nextN = nextN
  }
  if (input.running !== undefined) {
    const on = new Set(input.running.map(normTask))
    next.tasks = next.tasks.map(t => {
      if (t.status === 'completed' || t.status === 'deleted') return t
      if (on.has(normTask(t.subject))) return withStatus(t, 'in_progress', nowMs)
      return t.status === 'in_progress' ? withStatus(t, 'pending', nowMs) : t
    })
  }
  if (input.accepted !== undefined) {
    const acc = input.accepted
    const named = typeof acc === 'number' ? undefined : new Set(acc.map(normTask))
    next.tasks = next.tasks.map((t, i) => {
      const hit = named ? named.has(normTask(t.subject)) : i < (acc as number)
      return hit && t.status !== 'deleted' ? withStatus(t, 'completed', nowMs) : t
    })
  }
  if (input.finished === true) next.closed = true
  else if (input.finished === false || fresh) delete next.closed
  next = { ...next, updatedMs: nowMs }
  return next
}

// What the plan tool answers.
export const PLAN_SUB_ANSWER = "ignored: plan is for the main conversation's score; a subagent reports its own steps with step"
export const PLAN_BAD_ANSWER =
  'ignored: title must be a string, tasks a list of { subject }, accepted a list of subjects or a count, running a list of subjects, finished true or false'
export function planAnswer(p: OvertonePlan): string {
  if (p.closed) return 'plan closed'
  const t = planTotals(p)
  return `plan: ${t.accepted} of ${t.total} accepted`
}
