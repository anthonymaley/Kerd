import { describe, expect, test } from 'claude-code/testing'

import type { OvertonePlan, OvertoneWorkers } from '../types'
import { EMPTY_WORKERS, noteAsk, noteEnd, noteList, noteSpawn, noteToolStart } from '../hooks/logic'
import {
  EMPTY_PLAN,
  PLAN_CAP,
  PLAN_SPEC,
  PLAN_TOOL,
  STEP_MAX,
  SUBJECT_MAX,
  STEP_SPEC,
  STEP_TOOL,
  normTask,
  notePlanCall,
  notePlanTool,
  planAnswer,
  readPlan,
  noteStep,
  planRows,
  planTotals,
  planView,
  readStep,
} from '../hooks/plan-logic'
import { shownText as _shownText } from '../hooks/plan-logic'
import { noteAsked, noteWorkerModel, noteWorkerSeen } from '../hooks/usage-logic'

const T0 = new Date(2026, 9, 8, 12).getTime()
const MIN = 60_000

const ok = (result: unknown) => ({ ref: 1, result, text: 'ok' })
const create = (p: OvertonePlan, id: string, subject: string, nowMs = T0, activeForm?: string) =>
  notePlanCall(p, {
    tool: 'TaskCreate',
    input: { tool: 'TaskCreate', subject, description: 'd', ...(activeForm ? { activeForm } : {}) },
    ran: ok({ task: { id, subject } }),
    nowMs,
  })
const setStatus = (p: OvertonePlan, taskId: string, status: string, nowMs = T0) =>
  notePlanCall(p, {
    tool: 'TaskUpdate',
    input: { tool: 'TaskUpdate', taskId, status },
    ran: ok({ success: true, taskId, updatedFields: ['status'] }),
    nowMs,
  })
const todo = (p: OvertonePlan, todos: { content: string; status: string; activeForm?: string }[], nowMs = T0, newTodos: unknown = todos) =>
  notePlanCall(p, { tool: 'TodoWrite', input: { tool: 'TodoWrite', todos }, ran: ok({ oldTodos: [], newTodos }), nowMs })

function threeTasks(): OvertonePlan {
  let p = create(EMPTY_PLAN, '1', 'Build the plan state')
  p = create(p, '2', 'Write the tests', T0 + MIN, 'Writing the tests')
  p = create(p, '3', 'Validate the mod', T0 + 2 * MIN)
  return p
}

describe('plan: TaskCreate and TaskUpdate', () => {
  test('creates in order, numbered from 1, pending, with their creation time', () => {
    const p = threeTasks()
    expect(p.source).toBe('task')
    expect(p.tasks.map(t => [t.id, t.n, t.subject, t.status])).toEqual([
      ['1', 1, 'Build the plan state', 'pending'],
      ['2', 2, 'Write the tests', 'pending'],
      ['3', 3, 'Validate the mod', 'pending'],
    ])
    expect(p.tasks[1]).toMatchObject({ activeForm: 'Writing the tests', createdMs: T0 + MIN })
    expect(p.nextN).toBe(4)
  })

  test('in_progress starts the clock once; completed finishes it; reopened loses the finish', () => {
    let p = threeTasks()
    p = setStatus(p, '1', 'in_progress', T0 + 5 * MIN)
    expect(p.tasks[0]).toMatchObject({ status: 'in_progress', startedMs: T0 + 5 * MIN })
    expect(p.tasks[0]?.finishedMs).toBeUndefined()
    p = setStatus(p, '1', 'completed', T0 + 9 * MIN)
    expect(p.tasks[0]).toMatchObject({ status: 'completed', startedMs: T0 + 5 * MIN, finishedMs: T0 + 9 * MIN })
    p = setStatus(p, '1', 'in_progress', T0 + 12 * MIN)
    expect(p.tasks[0]).toMatchObject({ status: 'in_progress', startedMs: T0 + 5 * MIN })
    expect(p.tasks[0]?.finishedMs).toBeUndefined()
  })

  test('subject and activeForm updates; deleted stays in state but is not drawn or counted', () => {
    let p = threeTasks()
    p = notePlanCall(p, {
      tool: 'TaskUpdate',
      input: { tool: 'TaskUpdate', taskId: '3', subject: 'Validate and commit', activeForm: 'Validating' },
      ran: ok({ success: true, taskId: '3', updatedFields: ['subject', 'activeForm'] }),
      nowMs: T0,
    })
    expect(p.tasks[2]).toMatchObject({ subject: 'Validate and commit', activeForm: 'Validating' })
    p = setStatus(p, '2', 'deleted', T0 + MIN)
    expect(p.tasks[1]).toMatchObject({ status: 'deleted', finishedMs: T0 + MIN })
    p = setStatus(p, '1', 'completed')
    expect(planTotals(p)).toEqual({ accepted: 1, total: 2 })
    expect(planRows(p, EMPTY_WORKERS, T0).map(r => [r.n, r.taskId, r.state])).toEqual([
      [1, '1', 'done'],
      [2, '3', 'todo'],
    ])
  })

  test('a deny, an errored call, a refused update or an unknown task changes nothing', () => {
    const p = threeTasks()
    const deny = notePlanCall(p, { tool: 'TaskCreate', input: { subject: 'x' }, ran: { deny: 'no' }, nowMs: T0 })
    expect(deny).toBe(p)
    const errored = notePlanCall(p, { tool: 'TaskCreate', input: { subject: 'x' }, ran: { isError: true, text: 'boom' }, nowMs: T0 })
    expect(errored).toBe(p)
    const refused = notePlanCall(p, {
      tool: 'TaskUpdate',
      input: { taskId: '1', status: 'completed' },
      ran: ok({ success: false, taskId: '1', updatedFields: [], error: 'Task not found' }),
      nowMs: T0,
    })
    expect(refused).toBe(p)
    expect(setStatus(p, '99', 'completed')).toBe(p)
    expect(notePlanCall(p, { tool: 'TaskUpdate', input: { taskId: '1', status: 'bogus' }, ran: ok({ success: true }), nowMs: T0 })).toBe(p)
    // a create whose result carries no task id is no task
    expect(notePlanCall(p, { tool: 'TaskCreate', input: { subject: 'x' }, ran: ok({}), nowMs: T0 })).toBe(p)
    // any other tool
    expect(notePlanCall(p, { tool: 'Read', input: { file_path: '/a' }, ran: ok('x'), nowMs: T0 })).toBe(p)
  })

  test('past the cap the oldest finished tasks go; numbers never move', () => {
    let p = EMPTY_PLAN
    for (let i = 1; i <= PLAN_CAP + 3; i++) {
      p = create(p, String(i), `Task ${i}`)
      if (i <= 5) p = setStatus(p, String(i), 'completed')
    }
    expect(p.tasks.length).toBe(PLAN_CAP)
    expect(p.tasks[0]).toMatchObject({ id: '4', n: 4 })
    expect(p.nextN).toBe(PLAN_CAP + 4)
  })
})

describe('plan: TodoWrite', () => {
  test('replaces the list; a todo kept by its text keeps its number and start; new ones get the next number', () => {
    let p = todo(EMPTY_PLAN, [
      { content: 'Read the code', status: 'in_progress', activeForm: 'Reading the code' },
      { content: 'Write it', status: 'pending', activeForm: 'Writing it' },
    ])
    expect(p.source).toBe('todo')
    expect(p.tasks.map(t => [t.id, t.n, t.status, t.startedMs])).toEqual([
      ['todo-1', 1, 'in_progress', T0],
      ['todo-2', 2, 'pending', undefined],
    ])
    p = todo(
      p,
      [
        { content: 'Read the code', status: 'completed', activeForm: 'Reading the code' },
        { content: 'Write it', status: 'in_progress', activeForm: 'Writing it' },
        { content: 'Test it', status: 'pending', activeForm: 'Testing it' },
      ],
      T0 + 3 * MIN,
    )
    expect(p.tasks.map(t => [t.id, t.n, t.status, t.startedMs, t.finishedMs])).toEqual([
      ['todo-1', 1, 'completed', T0, T0 + 3 * MIN],
      ['todo-2', 2, 'in_progress', T0 + 3 * MIN, undefined],
      ['todo-3', 3, 'pending', undefined, undefined],
    ])
    // a todo that went is dropped
    p = todo(p, [{ content: 'Test it', status: 'pending', activeForm: 'Testing it' }], T0 + 4 * MIN)
    expect(p.tasks.map(t => t.id)).toEqual(['todo-3'])
  })

  test('an empty newTodos beside an all-completed input keeps the finished list', () => {
    const done = [{ content: 'Only step', status: 'completed', activeForm: 'Doing it' }]
    const p = todo(EMPTY_PLAN, done, T0, [])
    expect(planTotals(p)).toEqual({ accepted: 1, total: 1 })
  })

  test('the source that writes last wins: a todo list gives way to a task list and back', () => {
    let p = todo(EMPTY_PLAN, [{ content: 'A', status: 'pending', activeForm: 'A-ing' }])
    p = create(p, '1', 'Task one')
    expect(p.source).toBe('task')
    expect(p.tasks.map(t => [t.id, t.n])).toEqual([['1', 1]])
    p = todo(p, [{ content: 'B', status: 'pending', activeForm: 'B-ing' }])
    expect(p.source).toBe('todo')
    expect(p.tasks.map(t => [t.id, t.n])).toEqual([['todo-1', 1]])
    // a TaskUpdate while the plan is a todo list changes nothing
    expect(setStatus(p, '1', 'completed')).toBe(p)
  })

  test('an errored TodoWrite changes nothing', () => {
    const p = todo(EMPTY_PLAN, [{ content: 'A', status: 'pending' }])
    expect(notePlanCall(p, { tool: 'TodoWrite', input: { todos: [] }, ran: { isError: true, text: 'bad' }, nowMs: T0 })).toBe(p)
  })
})

describe('worker steps', () => {
  test('the step tool: its full name and schema', () => {
    expect(STEP_TOOL).toBe('mcp__overtone__step')
    expect(STEP_SPEC.name).toBe('step')
    expect(STEP_SPEC.inputSchema.required).toEqual(['done', 'total'])
    expect(STEP_SPEC.description).toMatch(/subagent/)
  })

  test('readStep: integers, done held at total, note trimmed and cut', () => {
    expect(readStep({ done: 2, total: 5 })).toEqual({ done: 2, total: 5 })
    expect(readStep({ done: 7, total: 5, note: '  wrote   the tests ' })).toEqual({ done: 5, total: 5, note: 'wrote the tests' })
    expect(readStep({ done: 1, total: 3, note: 'x'.repeat(200) })?.note?.length).toBe(80)
    expect(readStep({ done: 1.5, total: 3 })).toBeUndefined()
    expect(readStep({ done: -1, total: 3 })).toBeUndefined()
    expect(readStep({ done: 0, total: 0 })).toBeUndefined()
    expect(readStep({ done: '1', total: 3 })).toBeUndefined()
    expect(readStep(undefined)).toBeUndefined()
  })

  test('noteStep records on the worker, adds one not yet known, and leaves an ended one alone', () => {
    let w = noteSpawn(EMPTY_WORKERS, { id: 'a1', description: 'Write the tests', type: 'kerd:sonnet-high', nowMs: T0 })
    w = noteStep(w, { agentId: 'a1', step: { done: 2, total: 4, note: 'folding' }, nowMs: T0 + MIN })
    expect(w.byId.a1?.steps).toEqual({ done: 2, total: 4, note: 'folding', atMs: T0 + MIN })
    w = noteStep(w, { agentId: 'zz', step: { done: 1, total: 2 }, nowMs: T0 })
    expect(w.byId.zz).toMatchObject({ status: 'running', fromSpawn: false, steps: { done: 1, total: 2, atMs: T0 } })
    const ended = noteEnd(w, { agentId: 'a1', failed: false, nowMs: T0 + 2 * MIN })
    expect(noteStep(ended, { agentId: 'a1', step: { done: 4, total: 4 }, nowMs: T0 + 3 * MIN })).toBe(ended)
  })
})

describe('plan rows: matching tasks and workers', () => {
  function spawned(id: string, description: string, at = T0): (w: OvertoneWorkers) => OvertoneWorkers {
    return w => noteSpawn(w, { id, description, type: 'kerd:sonnet-high', nowMs: at })
  }

  test('normTask ignores case, punctuation and spacing', () => {
    expect(normTask('  Write the TESTS. ')).toBe('write the tests')
    expect(normTask('write-the  tests')).toBe('write the tests')
    expect(normTask(undefined)).toBe('')
  })

  test('a worker matches by subject or activeForm; model asked vs seen and steps ride the row', () => {
    let p = threeTasks()
    p = setStatus(p, '1', 'completed', T0 + MIN)
    let w = EMPTY_WORKERS
    w = spawned('a2', 'writing the tests', T0 + MIN)(w) // activeForm of task 2, spawned once it existed
    w = noteAsked(w, 'a2', { type: 'kerd:sonnet-high' })
    w = noteWorkerModel(w, 'a2', 'claude-sonnet-5-5', 'high')
    w = noteWorkerSeen(w, 'a2', 'claude-sonnet-5-5')
    w = noteStep(w, { agentId: 'a2', step: { done: 1, total: 3, note: 'cases' }, nowMs: T0 + 2 * MIN })
    const v = planView(p, w, T0 + 3 * MIN)
    expect(v.accepted).toBe(1)
    expect(v.total).toBe(3)
    expect(v.rows.map(r => [r.kind, r.n, r.title, r.state])).toEqual([
      ['task', 1, 'Build the plan state', 'done'],
      ['task', 2, 'Write the tests', 'running'],
      ['task', 3, 'Validate the mod', 'todo'],
    ])
    const row = v.rows[1]
    expect(row?.worker).toMatchObject({ id: 'a2', asked: 'sonnet', askedEffort: 'high', model: 'claude-sonnet-5-5', effort: 'high', seen: 'claude-sonnet-5-5' })
    expect(row?.steps).toEqual({ done: 1, total: 3, note: 'cases', atMs: T0 + 2 * MIN })
  })

  test('a blocked worker makes its task "needs"; a failed one "failed"; a completed task stays done', () => {
    let p = threeTasks()
    p = setStatus(p, '3', 'completed', T0 + 4 * MIN)
    let w = EMPTY_WORKERS
    w = spawned('b1', 'Build the plan state', T0 + 2 * MIN)(w)
    w = noteToolStart(w, { agentId: 'b1', toolUseId: 'u1', summary: 'Bash git push', nowMs: T0 + 2 * MIN })
    w = noteAsk(w, { toolUseId: 'u1', nowMs: T0 + 2 * MIN })
    w = spawned('f2', 'Write the tests', T0 + 2 * MIN)(w)
    w = noteEnd(w, { agentId: 'f2', failed: true, nowMs: T0 + 3 * MIN })
    w = spawned('f3', 'Validate the mod', T0 + 2 * MIN)(w)
    w = noteEnd(w, { agentId: 'f3', failed: true, nowMs: T0 + 3 * MIN })
    expect(planRows(p, w, T0 + 5 * MIN).map(r => [r.n, r.state, r.worker?.id])).toEqual([
      [1, 'needs', 'b1'],
      [2, 'failed', 'f2'],
      [3, 'done', 'f3'],
    ])
  })

  test('an in_progress task with no worker is running; one worker serves one task; the live one is preferred', () => {
    let p = create(EMPTY_PLAN, '1', 'Review')
    p = create(p, '2', 'Review')
    p = setStatus(p, '1', 'in_progress')
    let w = EMPTY_WORKERS
    w = spawned('old', 'Review', T0)(w)
    w = noteEnd(w, { agentId: 'old', failed: false, nowMs: T0 + MIN })
    w = spawned('new', 'Review', T0 + 2 * MIN)(w)
    const rows = planRows(p, w, T0 + 3 * MIN)
    expect(rows.map(r => [r.n, r.state, r.worker?.id])).toEqual([
      [1, 'running', 'new'],
      [2, 'returned', 'old'],
    ])
  })

  test('unmatched running workers follow the tasks, oldest first; ended or claimed ones do not', () => {
    const p = threeTasks()
    let w = EMPTY_WORKERS
    w = spawned('m1', 'Build the plan state')(w)
    w = spawned('u2', 'Explore the repo', T0 + 2 * MIN)(w)
    w = spawned('u1', 'Look up the types', T0 + MIN)(w)
    w = noteToolStart(w, { agentId: 'u1', toolUseId: 'q', summary: 'Bash rm', nowMs: T0 + MIN })
    w = noteAsk(w, { toolUseId: 'q', nowMs: T0 + MIN })
    w = spawned('gone', 'Something finished')(w)
    w = noteEnd(w, { agentId: 'gone', failed: false, nowMs: T0 + MIN })
    w = noteStep(w, { agentId: 'u2', step: { done: 3, total: 4 }, nowMs: T0 + 3 * MIN })
    const rows = planRows(p, w, T0 + 4 * MIN)
    expect(rows.map(r => [r.kind, r.n, r.title, r.state])).toEqual([
      ['task', 1, 'Build the plan state', 'running'],
      ['task', 2, 'Write the tests', 'todo'],
      ['task', 3, 'Validate the mod', 'todo'],
      ['worker', undefined, 'Look up the types', 'needs'],
      ['worker', undefined, 'Explore the repo', 'running'],
    ])
    expect(rows[4]).toMatchObject({ key: 'w-u2', startedMs: T0 + 2 * MIN, steps: { done: 3, total: 4 } })
  })

  test('a worker only a list read named matches by the description the list gave', () => {
    const p = create(EMPTY_PLAN, '1', 'Audit the docs')
    const w = noteList(EMPTY_WORKERS, [{ id: 'l1', description: 'Audit the docs', type: 'Explore', status: 'running' }], T0)
    expect(planRows(p, w, T0).map(r => [r.state, r.worker?.id])).toEqual([['running', 'l1']])
  })

  test('a long description still matches (the label is cut, the description is not)', () => {
    const long = 'Build the plan state for overtone from TaskCreate, TaskUpdate and TodoWrite results, with tests'
    const p = create(EMPTY_PLAN, '1', long)
    const w = spawned('x', long)(EMPTY_WORKERS)
    expect(w.byId.x?.label.length).toBeLessThan(long.length)
    expect(planRows(p, w, T0)[0]?.worker?.id).toBe('x')
  })

  test('no plan, no workers: no rows, 0 of 0', () => {
    expect(planView(null, null, T0)).toEqual({ accepted: 0, total: 0, rows: [] })
  })
})

describe('the plan tool (Kerd Conductor\'s score)', () => {
  const go = (p: OvertonePlan | null, subjects: string[], title?: string, at = T0) =>
    notePlanTool(p, { ...(title !== undefined ? { title } : {}), tasks: subjects }, at)

  test('its full name and schema; a short description that names Conductor and the matching rule', () => {
    expect(PLAN_TOOL).toBe('mcp__overtone__plan')
    expect(PLAN_SPEC.name).toBe('plan')
    expect(Object.keys(PLAN_SPEC.inputSchema.properties)).toEqual(['title', 'tasks', 'accepted', 'running', 'finished'])
    expect(PLAN_SPEC.description).toMatch(/Kerd Conductor/)
    expect(PLAN_SPEC.description).toMatch(/Agent description/)
    expect(PLAN_SPEC.description.length).toBeLessThan(400)
  })

  test('readPlan: fields left out stay out; a malformed field refuses the call', () => {
    expect(readPlan({})).toEqual({ input: {} })
    expect(readPlan({ title: '  The   plan ', tasks: [{ subject: ' A ' }, { subject: 'B' }], accepted: 1, running: ['B'], finished: false })).toEqual({
      input: {
        title: 'The plan',
        tasks: ['A', 'B'],
        accepted: 1,
        running: ['B'],
        finished: false,
      },
    })
    expect(readPlan({ accepted: ['A'] })).toEqual({ input: { accepted: ['A'] } })
    for (const bad of [
      { tasks: [{ subject: '' }] },
      { tasks: 'A' },
      { accepted: -1 },
      { accepted: 1.5 },
      { accepted: [1] },
      { running: 'A' },
      { finished: 'yes' },
      { title: 3 },
    ]) {
      expect(readPlan(bad).refused).toMatch(/^ignored/)
    }
  })

  test('the go: title and tasks in order, pending, numbered 1..n', () => {
    const p = go(EMPTY_PLAN, ['Build state', 'Draw it', 'Wire Conductor'], 'Plan view')
    expect(p).toMatchObject({ source: 'tool', title: 'Plan view', nextN: 4, updatedMs: T0 })
    expect(p.tasks.map(t => [t.id, t.n, t.subject, t.status])).toEqual([
      ['plan-1', 1, 'Build state', 'pending'],
      ['plan-2', 2, 'Draw it', 'pending'],
      ['plan-3', 3, 'Wire Conductor', 'pending'],
    ])
    expect(planAnswer(p)).toBe('plan: 0 of 3 accepted')
  })

  test('a new list keeps the status of subjects that stay, adds new ones pending, drops the rest; rows follow its order', () => {
    let p = go(EMPTY_PLAN, ['A', 'B', 'C'], 'T')
    p = notePlanTool(p, { running: ['A'], accepted: ['B'] }, T0 + MIN)
    p = go(p, ['b', 'New', 'A'], undefined, T0 + 2 * MIN)
    expect(p.title).toBe('T')
    expect(p.tasks.map(t => [t.n, t.subject, t.status])).toEqual([
      [2, 'b', 'completed'],
      [4, 'New', 'pending'],
      [1, 'A', 'in_progress'],
    ])
    expect(planRows(p, EMPTY_WORKERS, T0).map(r => [r.n, r.title])).toEqual([
      [1, 'b'],
      [2, 'New'],
      [3, 'A'],
    ])
  })

  test('running is the set in progress now; accepted only adds, by subject or by count', () => {
    let p = go(EMPTY_PLAN, ['A', 'B', 'C'])
    p = notePlanTool(p, { running: ['A', 'B'] }, T0 + MIN)
    p = notePlanTool(p, { running: ['B'] }, T0 + 2 * MIN)
    expect(p.tasks.map(t => [t.status, t.startedMs])).toEqual([
      ['pending', T0 + MIN],
      ['in_progress', T0 + MIN],
      ['pending', undefined],
    ])
    p = notePlanTool(p, { accepted: ['b', 'unknown'] }, T0 + 3 * MIN)
    expect(p.tasks.map(t => t.status)).toEqual(['pending', 'completed', 'pending'])
    p = notePlanTool(p, { accepted: 1 }, T0 + 4 * MIN)
    expect(p.tasks.map(t => t.status)).toEqual(['completed', 'completed', 'pending'])
    // accepted never takes an acceptance back; running never reopens a completed task
    p = notePlanTool(p, { accepted: [], running: ['A'] }, T0 + 5 * MIN)
    expect(planTotals(p)).toEqual({ accepted: 2, total: 3 })
  })

  test('the title rides the view; finished closes the plan and the view draws nothing', () => {
    let p = go(EMPTY_PLAN, ['A'], 'Plan view')
    expect(planView(p, EMPTY_WORKERS, T0)).toMatchObject({ title: 'Plan view', accepted: 0, total: 1 })
    p = notePlanTool(p, { accepted: 1, finished: true }, T0 + MIN)
    expect(p.closed).toBe(true)
    expect(planAnswer(p)).toBe('plan closed')
    expect(planView(p, EMPTY_WORKERS, T0)).toEqual({ accepted: 0, total: 0, rows: [] })
    // a later go starts a fresh plan
    p = go(p, ['Next'], 'Second')
    expect(p.closed).toBeUndefined()
    expect(p.tasks.map(t => [t.n, t.subject, t.status])).toEqual([[1, 'Next', 'pending']])
    // an empty title clears it
    expect(notePlanTool(p, { title: '' }, T0).title).toBeUndefined()
  })

  test('whichever source wrote last owns the plan', () => {
    let p = create(EMPTY_PLAN, '1', 'Task one')
    p = go(p, ['Score A'], 'Score')
    expect(p.source).toBe('tool')
    expect(p.tasks.map(t => t.subject)).toEqual(['Score A'])
    // the task tools then take it back; a TaskUpdate on a tool plan changes nothing
    expect(setStatus(p, 'plan-1', 'completed')).toBe(p)
    p = create(p, '7', 'Task seven')
    expect(p.source).toBe('task')
    expect(p.title).toBeUndefined()
    // an accepted-only call on another source's plan starts an empty tool plan
    const q = notePlanTool(p, { accepted: 1 }, T0)
    expect(q.source).toBe('tool')
    expect(q.tasks).toEqual([])
  })

  test('workers match tool-plan tasks by their Agent description', () => {
    const p = go(EMPTY_PLAN, ['Build state', 'Draw it'], 'Plan')
    const w = noteSpawn(EMPTY_WORKERS, { id: 'a1', description: 'Draw it', type: 'kerd:sonnet-high', nowMs: T0 })
    expect(planRows(p, w, T0).map(r => [r.title, r.state, r.worker?.id])).toEqual([
      ['Build state', 'todo', undefined],
      ['Draw it', 'running', 'a1'],
    ])
  })
})

describe('shownText', () => {
  test('drops escape sequences, control, bidi and format characters', () => {
    expect(_shownText('\u001b[2J\u001b]0;pwned\u0007Plan\u202e one\u200b\n two')).toBe('[2J ]0;pwned Plan one two')
    expect(_shownText('\u009b31mred')).toBe('31mred')
    expect(_shownText('plain task')).toBe('plain task')
  })
})

describe('review 2026-10-08', () => {
  test('item 1: a step total is 1..STEP_MAX in the schema and the parser', () => {
    expect(STEP_SPEC.inputSchema.properties.total.maximum).toBe(STEP_MAX)
    expect(readStep({ done: 1, total: STEP_MAX })).toEqual({ done: 1, total: STEP_MAX })
    expect(readStep({ done: 1, total: STEP_MAX + 1 })).toBeUndefined()
    expect(readStep({ done: 1, total: 1e12 })).toBeUndefined()
  })

  test('item 2: a completed task never claims a worker seen after its finish; that worker keeps its own row', () => {
    let p = create(EMPTY_PLAN, '1', 'Review', T0)
    p = setStatus(p, '1', 'completed', T0 + MIN)
    let w = noteSpawn(EMPTY_WORKERS, { id: 'late', description: 'Review', type: 'Explore', nowMs: T0 + 2 * MIN })
    w = noteToolStart(w, { agentId: 'late', toolUseId: 'u', summary: 'Bash git push', nowMs: T0 + 2 * MIN })
    w = noteAsk(w, { toolUseId: 'u', nowMs: T0 + 2 * MIN })
    const rows = planRows(p, w, T0 + 3 * MIN)
    expect(rows.map(r => [r.kind, r.state, r.worker?.id])).toEqual([
      ['task', 'done', undefined],
      ['worker', 'needs', 'late'],
    ])
    // one seen by its finish, and over, still serves it
    const early = noteEnd(noteSpawn(EMPTY_WORKERS, { id: 'early', description: 'Review', type: 'Explore', nowMs: T0 + 30_000 }), {
      agentId: 'early',
      failed: false,
      nowMs: T0 + 50_000,
    })
    expect(planRows(p, early, T0 + 3 * MIN)[0]?.worker?.id).toBe('early')
  })

  test('item 2: a new plan never inherits an older plan\'s failed worker', () => {
    let w = noteSpawn(EMPTY_WORKERS, { id: 'old', description: 'Build it', type: 'Explore', nowMs: T0 })
    w = noteEnd(w, { agentId: 'old', failed: true, nowMs: T0 + MIN })
    const p = notePlanTool(EMPTY_PLAN, { title: 'Second', tasks: ['Build it'] }, T0 + 5 * MIN)
    expect(p.bornMs).toBe(T0 + 5 * MIN)
    expect(planRows(p, w, T0 + 6 * MIN).map(r => [r.state, r.worker?.id])).toEqual([['todo', undefined]])
    // the same goes for the task tools and TodoWrite
    expect(create(EMPTY_PLAN, '1', 'Build it', T0 + 5 * MIN).bornMs).toBe(T0 + 5 * MIN)
    expect(todo(EMPTY_PLAN, [{ content: 'Build it', status: 'pending' }], T0 + 5 * MIN).bornMs).toBe(T0 + 5 * MIN)
    expect(planRows(create(EMPTY_PLAN, '1', 'Build it', T0 + 5 * MIN), w, T0 + 6 * MIN)[0]?.state).toBe('todo')
  })

  test('item 3: a worker that came back, task not yet accepted, is "returned", not counted accepted', () => {
    let p = create(EMPTY_PLAN, '1', 'Draw it', T0)
    p = setStatus(p, '1', 'in_progress', T0)
    let w = noteSpawn(EMPTY_WORKERS, { id: 'a', description: 'Draw it', type: 'Explore', nowMs: T0 })
    w = noteEnd(w, { agentId: 'a', failed: false, nowMs: T0 + MIN })
    const v = planView(p, w, T0 + 2 * MIN)
    expect(v.rows.map(r => r.state)).toEqual(['returned'])
    expect(v.accepted).toBe(0)
    // accepted, it is done
    expect(planView(setStatus(p, '1', 'completed', T0 + 3 * MIN), w, T0 + 4 * MIN).rows.map(r => r.state)).toEqual(['done'])
  })

  test('item 5: TaskCreate past the cap with nothing finished keeps the first PLAN_CAP and counts the rest', () => {
    let p = EMPTY_PLAN
    for (let i = 1; i <= PLAN_CAP + 5; i++) p = create(p, String(i), `Task ${i}`)
    expect(p.tasks.length).toBe(PLAN_CAP)
    expect(p.tasks[0]?.id).toBe('1')
    expect(p.overflow).toBe(5)
    expect(planView(p, EMPTY_WORKERS, T0).overflow).toBe(5)
  })

  test('item 5: TodoWrite past the cap keeps PLAN_CAP and counts the rest; subjects are cut', () => {
    const many = Array.from({ length: PLAN_CAP + 7 }, (_, i) => ({ content: `Todo ${i} ${'x'.repeat(i === 0 ? 500 : 0)}`, status: 'pending' }))
    const p = todo(EMPTY_PLAN, many)
    expect(p.tasks.length).toBe(PLAN_CAP)
    expect(p.overflow).toBe(7)
    expect(p.tasks[0]?.subject.length).toBe(SUBJECT_MAX)
    // a list back under the cap clears the count
    expect(todo(p, many.slice(0, 3)).overflow).toBeUndefined()
  })

  test('item 5: TaskCreate and TaskUpdate subjects are cut to SUBJECT_MAX', () => {
    let p = create(EMPTY_PLAN, '1', 'y'.repeat(1000))
    expect(p.tasks[0]?.subject.length).toBe(SUBJECT_MAX)
    p = notePlanCall(p, { tool: 'TaskUpdate', input: { taskId: '1', subject: 'z'.repeat(1000) }, ran: ok({ success: true }), nowMs: T0 })
    expect(p.tasks[0]?.subject.length).toBe(SUBJECT_MAX)
  })

  test('item 5: the plan tool refuses oversized input with a clear answer, changing nothing', () => {
    expect(PLAN_SPEC.inputSchema.properties.tasks.maxItems).toBe(PLAN_CAP)
    expect(PLAN_SPEC.inputSchema.properties.tasks.items.properties.subject.maxLength).toBe(SUBJECT_MAX)
    const many = Array.from({ length: PLAN_CAP + 1 }, (_, i) => ({ subject: `T${i}` }))
    expect(readPlan({ tasks: many }).refused).toMatch(/at most 100 tasks/)
    expect(readPlan({ tasks: [{ subject: 'x'.repeat(SUBJECT_MAX + 1) }] }).refused).toMatch(/at most 200 characters/)
    expect(readPlan({ running: many.map(t => t.subject) }).refused).toMatch(/at most 100/)
    expect(readPlan({ accepted: many.map(t => t.subject) }).refused).toMatch(/at most 100/)
    expect(readPlan({ tasks: many.slice(0, PLAN_CAP) }).input?.tasks?.length).toBe(PLAN_CAP)
  })
})

describe('review round 2 (2026-10-08)', () => {
  test('two "Review" tasks, both workers started before the first acceptance: the completed task never takes the blocked one', () => {
    let p = create(EMPTY_PLAN, '1', 'Review', T0)
    p = create(p, '2', 'Review', T0)
    let w = noteSpawn(EMPTY_WORKERS, { id: 'r1', description: 'Review', type: 'Explore', nowMs: T0 + MIN })
    w = noteSpawn(w, { id: 'r2', description: 'Review', type: 'Explore', nowMs: T0 + MIN })
    w = noteToolStart(w, { agentId: 'r2', toolUseId: 'u2', summary: 'Bash git push', nowMs: T0 + 2 * MIN })
    w = noteAsk(w, { toolUseId: 'u2', nowMs: T0 + 2 * MIN })
    w = noteEnd(w, { agentId: 'r1', failed: false, nowMs: T0 + 3 * MIN })
    p = setStatus(p, '1', 'completed', T0 + 4 * MIN)
    const rows = planRows(p, w, T0 + 5 * MIN)
    expect(rows.map(r => [r.kind, r.n, r.state, r.worker?.id])).toEqual([
      ['task', 1, 'done', 'r1'],
      ['task', 2, 'needs', 'r2'],
    ])
    // with both still active at the acceptance, neither hides under the done task
    let both = noteSpawn(EMPTY_WORKERS, { id: 'a1', description: 'Review', type: 'Explore', nowMs: T0 + MIN })
    both = noteSpawn(both, { id: 'a2', description: 'Review', type: 'Explore', nowMs: T0 + MIN })
    both = noteToolStart(both, { agentId: 'a2', toolUseId: 'v', summary: 'Bash rm', nowMs: T0 + 2 * MIN })
    both = noteAsk(both, { toolUseId: 'v', nowMs: T0 + 2 * MIN })
    const r2 = planRows(p, both, T0 + 5 * MIN)
    expect(r2[0]).toMatchObject({ n: 1, state: 'done' })
    expect(r2[0]?.worker).toBeUndefined()
    expect(r2.map(r => r.worker?.id).filter(Boolean).sort()).toEqual(['a1', 'a2'])
    expect(r2.some(r => r.state === 'needs' && r.worker?.id === 'a2')).toBe(true)
  })

  test('"Review" removed and re-added in an open plan does not inherit its earlier failed worker', () => {
    let p = notePlanTool(EMPTY_PLAN, { title: 'T', tasks: ['Build', 'Review'] }, T0)
    let w = noteSpawn(EMPTY_WORKERS, { id: 'f', description: 'Review', type: 'Explore', nowMs: T0 + MIN })
    w = noteEnd(w, { agentId: 'f', failed: true, nowMs: T0 + 2 * MIN })
    expect(planRows(p, w, T0 + 3 * MIN)[1]).toMatchObject({ state: 'failed' })
    p = notePlanTool(p, { tasks: ['Build'] }, T0 + 4 * MIN)
    p = notePlanTool(p, { tasks: ['Build', 'Review'] }, T0 + 5 * MIN)
    expect(p.tasks[1]?.createdMs).toBe(T0 + 5 * MIN)
    expect(planRows(p, w, T0 + 6 * MIN).map(r => [r.title, r.state, r.worker?.id])).toEqual([
      ['Build', 'todo', undefined],
      ['Review', 'todo', undefined],
    ])
    // a new worker for it does match
    const w2 = noteSpawn(w, { id: 'n', description: 'Review', type: 'Explore', nowMs: T0 + 6 * MIN })
    expect(planRows(p, w2, T0 + 7 * MIN)[1]).toMatchObject({ state: 'running', worker: { id: 'n' } })
  })
})
