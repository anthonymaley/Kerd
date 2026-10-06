// overtone's $.state contract: the plain values the band draws from.
// Every field is plain data; nothing here is persisted ($.state is the
// session's and survives a reload, not a restart).

// The last context reading. `tokens` is absent until the first response of
// the live window.
export type OvertoneReading = {
  tokens?: number
  window?: number
  percent?: number
}

// The main loop's model, as the band last saw it. Subagent requests never
// write here.
export type OvertoneModel = {
  // What was asked: the session's model as /model shows it, else the model
  // the request named. Absent until the first main request.
  asked?: string
  // The model that answered, by the id the API reported on the last main
  // response that carried usage.
  seen?: string
  // The effort the last main request asked for; absent when the request
  // carried none. The API reports no served effort.
  effort?: string | number
  // How many main requests the band has seen.
  steps: number
}

// One worker (a subagent or teammate) as the band knows it.
export type OvertoneWorker = {
  id: string
  label: string
  type: string
  // The engine's task status (`running`, `completed`, `failed`, `killed`, ...),
  // or overtone's own `completed`/`failed` once the worker's turn ended.
  status: string
  // When overtone first saw it; `fromSpawn` says whether that was its spawn
  // (so the elapsed time is exact) or later (a lower bound).
  firstSeenMs: number
  fromSpawn: boolean
  endedMs?: number
  // The agent whose loop spawned it, when known: from agent.spawn's
  // parentAgentId or $.agent.list()'s parentId; absent for the main loop's.
  parentId?: string
  // When it last started a tool call (absent until its first).
  lastToolMs?: number
  // Whether the latest good $.agent.list() read named it.
  listed?: boolean
  // The last tool call it made, summarised, and how many it made.
  activity?: string
  tools: number
  // tool_use_id -> summary, for calls still running.
  pending: Record<string, string>
  // Set while one of its calls sits at a permission ask.
  blocked?: { what: string; sinceMs: number; toolUseId: string }
  // What the spawn asked for: the Agent call's model (an alias or an id), or
  // the one a kerd:<model>-<effort> agent type names, and that type's effort.
  asked?: string
  askedEffort?: string
  // Its own requests (turn.step): the model and effort sent, and the model
  // the API reported answering.
  model?: string
  effort?: string | number
  seen?: string
}

export type OvertoneWorkers = {
  byId: Record<string, OvertoneWorker>
  // Why the last $.agent.list() read failed; cleared by the next good read.
  error?: string
}

// One rate-limit window as Claude Code reported it (exact).
export type OvertoneLimit = { kind: string; percentUsed: number; resetsAt?: string }

// The rate-limit windows $.session.usage() / session.measure carry, as last read.
export type OvertoneUsage = {
  rateLimits: OvertoneLimit[]
  sessionId?: string
  measuredMs: number
}

// The four token counts of ModelUsage for one request.
export type OvertoneCounts = { input: number; output: number; cacheRead: number; cacheWrite: number }

// The main loop's requests as turn.step saw them (exact counts).
export type OvertoneSteps = {
  requests: number
  // The last main request: its counts, when it was sent and answered, the
  // model that answered.
  last?: OvertoneCounts & { startMs: number; atMs: number; model?: string }
  // The cache hit % of the main request before it.
  prevHit?: number
  // Time between the response before and the last request: idle time.
  gapMs?: number
  // Whether the last request's answering model differs from the one before.
  modelChanged?: boolean
  // Cold main requests in a row since the cache was last warm (80%+ hit).
  coldStreak?: number
  // What this cold run has said so far (0 nothing, 1 the first alert,
  // 2 "remains cold"), and what the last request says.
  coldPhase?: number
  coldAlert?: 'first' | 'remains'

  // Cache hit % of recent main requests, oldest first.
  trend: number[]
}

// A Kerd Agent partner request of this project, read from its record.
export type OvertonePartnerRow = {
  id: string
  alias: string
  provider: string
  doing: string
  createdMs: number
  receivedMs?: number
  state: 'waiting' | 'uncertain' | 'received'
}

export type OvertonePartners = {
  polledMs: number
  rows: OvertonePartnerRow[]
  // Why no rows could be read (no git repo, no Kerd Agent records, a failure).
  note?: string
}

// The prompt-cache TTL Claude Code reported (classic PostModelSwitch, raised
// on a model switch and when a resume restores the model).
export type OvertoneCacheTtl = { ttl: '5m' | '1h'; atMs: number }

// The band's own view state: collapsed (one line) or expanded (dashboard).
export type OvertoneView = { expanded: boolean }

declare module 'claude-code' {
  interface PluginState {
    overtone: {
      reading: OvertoneReading | null
      model: OvertoneModel
      workers: OvertoneWorkers
      usage: OvertoneUsage | null
      steps: OvertoneSteps
      partners: OvertonePartners | null
      cacheTtl: OvertoneCacheTtl | null
      view: OvertoneView
      // The time of the last tick (every 15 s), so countdowns redraw while idle.
      tick: number
    }
  }
}
