// overtone guard (idea 5): before Claude runs a Bash command that stages,
// commits or pushes a private path toward a public repo, show the evidence
// and ask. The decision is the engine's own dialog ($.ui.ask: it takes the
// keyboard at any width, in tmux too); the evidence is a pane where one is
// placed, else the band above the prompt.
//
// Contract:
// - Observe, then ask. A command with no private path passes untouched,
//   `next(e)`, the same object.
// - Fail OPEN on the guard's own detection: a reader bug or git failing must
//   not block git work. It is logged to the debug log and counted in
//   $.store `guard-failures`, never toasted. A command the reader cannot
//   READ (a shell expansion in a path, an unreadable push target) is not a
//   bug: it asks.
// - Fail CLOSED on the decision: dismissal, no answer in 30 s, an error in
//   the dialog, or an interrupt refuses, and the deny tells Claude what to do.
//   Plugins have no call that closes a `$.ui.ask`, so after a timeout the
//   dialog may stay on screen; its late answer is ignored and runs nothing.
// - `next(e)` is called in one place, once, after every check. A failure
//   before it is the guard's; once it is entered, `.catch` never calls it
//   again (the call's own result or rejection stands).
// - `$` never goes into a closure: the timer's callback and every render
//   hook use their own.
// - The private-path list is GUARD, at the top of guard-logic.ts.
//
// Module state: `holds` (the evidence on screen), `asking` (commands
// waiting on the dialog or its decision), `entered` (calls whose `next`
// was entered and did not settle cleanly) and `seen` (what GitHub said about
// each remote URL, and when). A reload drops them; a wait in flight
// still ends in its own hook.

import type { Elements, EngineInterface, Register, RenderSurface } from 'claude-code'

import {
  GH_WAIT_MS,
  GUARD,
  PUSH_DST,
  aliasKey,
  destinationBase,
  liveCheck,
  liveRange,
  refSetStaleWhy,
  HEADER,
  LATE_NOTE,
  RUN,
  SAFE,
  assess,
  decide,
  denyMessage,
  evidence,
  ghFailure,
  githubRepo,
  needsPushConfig,
  parseGitOps,
  pushPlan,
  pushRemoteName,
  publicRemotes,
  question,
  stagesIgnored,
  workNotesInVault,
  expandHome,
  readVault,
  vaultFrom,
  type GitOp,
  type Spec,
  type VaultFacts,
  type VaultRead,
  type Aliases,
  type Evidence,
  type Finding,
  type Outcome,
  type PushConfig,
  type PushPlan,
  type LiveRead,
  type RepoFacts,
  type Visibility,
} from './guard-logic'

const PANE_ID = 'overtone-guard'
const FAILURES_KEY = 'guard-failures'
const MAX_ROWS = 6
// A ref-set push (--all, --mirror, --tags): at most this many tips have
// their kivna/vault.json read; more asks.
const MAX_TIPS = 64

type Hold = Evidence & { where: 'pane' | 'band' }
const holds = new Map<string, Hold>()
const asking = new Set<string>()
const entered = new Set<string>()
// Definite answers only: a failed ask is asked again next time. 'public' is
// kept for the session (it only ever asks more). 'private' is kept for
// PRIVATE_MS, so a repo made public mid-session is guarded again within
// five minutes. Accepted residual: for up to those five minutes such a repo
// passes as private and can take private paths unguarded.
const seen = new Map<string, { said: 'public' | 'private'; at: number }>()
const PRIVATE_MS = 5 * 60_000

const firstHold = (): Hold | undefined => holds.values().next().value

const WORK_ROOT = GUARD.newWorkFolders.root
// `git ls-tree -z` output: NUL-separated, so a name git would quote
// (`docs/work/é`) comes through as written.
const slugsFrom = (lsTree: string): string[] =>
  lsTree
    .split('\0')
    .filter(Boolean)
    .map(p => p.slice(WORK_ROOT.length).split('/')[0] ?? '')

// `gh` may not be on the hook's PATH: the usual installs, in order.
const GH = ['gh', '/opt/homebrew/bin/gh', '/usr/local/bin/gh']

// What GitHub says about each URL, from `seen` or `gh repo view`. A URL gh
// could not answer for (none installed, offline, not signed in, a cut or
// unreadable answer) is left out: the guard could not confirm it private.
// One GitHub did not answer in time reads 'slow' (unconfirmed, never kept),
// so the words can say why.
// The host is named (`github.com/o/r`) so GH_HOST cannot send the question
// elsewhere, and an answer counts only when its url is that repo's.
async function askGithub($: EngineInterface, urls: readonly string[]): Promise<Visibility> {
  const now = await $.clock.now()
  const slow = new Set<string>()
  for (const url of urls) {
    const repo = githubRepo(url)
    const known = seen.get(url)
    if (known && (known.said === 'public' || now - known.at < PRIVATE_MS)) continue
    seen.delete(url) // an expired 'private' is unconfirmed until gh answers again
    if (repo === null) continue
    for (const gh of GH) {
      let r: Awaited<ReturnType<EngineInterface['process']['run']>>
      const asked = await $.clock.now()
      try {
        r = await $.process.run([gh, 'repo', 'view', `github.com/${repo}`, '--json', 'isPrivate,url'], {
          timeoutMs: GH_WAIT_MS,
        })
      } catch (err) {
        const why = ghFailure(err instanceof Error ? err.message : String(err), (await $.clock.now()) - asked)
        if (why === 'absent') continue // not at this path: try the next
        if (why === 'timeout') slow.add(url)
        break // gh ran: another path is the same gh, so stop, unconfirmed
      }
      if (r.exitCode === 127) continue // a shell's "command not found": try the next
      try {
        const answer: unknown = r.exitCode === 0 && !r.isStdoutTruncated ? JSON.parse(r.stdout) : undefined
        const { isPrivate, url: said } = (answer ?? {}) as { isPrivate?: unknown; url?: unknown }
        const same = typeof said === 'string' && said.toLowerCase() === `https://github.com/${repo}`.toLowerCase()
        if (same && typeof isPrivate === 'boolean') seen.set(url, { said: isPrivate ? 'private' : 'public', at: now })
      } catch {
        // unreadable: unconfirmed
      }
      break
    }
  }
  return new Map<string, 'public' | 'private' | 'slow'>([
    ...[...seen].map(([url, v]) => [url, v.said] as const),
    ...[...slow].map(url => [url, 'slow'] as const),
  ])
}

// The vault as kivna/vault.json and the person's vault_path setting say,
// plus where each path really lands when it is a link (a vault reached by its
// link and by its target is one vault).
async function resolveVault(
  $: EngineInterface,
  reads: readonly VaultRead[],
  own: string,
  home: string | undefined,
): Promise<VaultFacts> {
  const facts = vaultFrom(reads, own)
  const landed = async (list: readonly string[]) => {
    const out = [...list]
    for (const p of list) {
      try {
        const real = (await $.fs.stat(expandHome(p, home), { resolve: true }))?.realPath
        if (real && !out.includes(real)) out.push(real)
      } catch {
        // not there, or no file access: the path as written still counts
      }
    }
    return out
  }
  return { ...facts, paths: await landed(facts.paths), own: await landed(facts.own) }
}

// Each pathspec with where it lands when a folder on its way is a link, so a
// vault named by its target still catches a path spelled through the link.
// Only when there is a vault to compare with.
async function landSpecs($: EngineInterface, op: GitOp, vault: VaultFacts): Promise<GitOp> {
  if (!vault.paths.length && !vault.own.length) return op
  const specs: Spec[] = []
  for (const s of op.specs) {
    if (s.unreadable || s.raw.startsWith(GUARD.notesPrefix) || !s.abs.startsWith('/')) {
      specs.push(s)
      continue
    }
    const cut = s.abs.lastIndexOf('/')
    const dir = cut <= 0 ? '/' : s.abs.slice(0, cut)
    try {
      const real = (await $.fs.stat(dir, { resolve: true }))?.realPath
      const landed = real ? `${real.replace(/\/$/, '')}/${s.abs.slice(cut + 1)}` : undefined
      specs.push(landed && landed !== s.abs ? { ...s, real: landed } : s)
    } catch {
      specs.push(s)
    }
  }
  return { ...op, specs }
}

// What a kivna/vault.json file says; missing or unreadable as a file: null
// (no vault rule from it).
async function readVaultFile($: EngineInterface, path: string): Promise<VaultRead> {
  try {
    return readVault(await $.fs.read(path))
  } catch {
    return null
  }
}

// The git ops in a command, with its git aliases read (`git config --get
// alias.<name>` where git runs): parse, read the aliases it names, parse
// again, a few rounds for an alias of an alias. An alias whose read fails
// (thrown, or an answer git gives for neither set nor unset) stays unread,
// and its op asks as it stands.
async function readOps($: EngineInterface, command: string, cwd: string, home: string | undefined): Promise<GitOp[]> {
  const aliases = new Map<string, string | null>()
  const tried = new Set<string>()
  let ops = parseGitOps(command, cwd, home, aliases)
  for (let round = 0; round < 4; round++) {
    const want = ops.filter(o => o.alias !== undefined && !tried.has(aliasKey(o.cwd, o.alias)))
    if (!want.length) break
    for (const o of want) {
      const key = aliasKey(o.cwd, o.alias!)
      if (tried.has(key)) continue
      tried.add(key)
      try {
        const r = await $.process.run(['git', 'config', '--get', `alias.${o.alias}`], { cwd: o.cwd, timeoutMs: 10_000 })
        if (r.exitCode === 0 && !r.isStdoutTruncated) aliases.set(key, r.stdout.trim())
        else if (r.exitCode === 1) aliases.set(key, null)
      } catch {
        // unread: the op asks
      }
    }
    ops = parseGitOps(command, cwd, home, aliases as Aliases)
  }
  return ops
}

const REFUSED_IN_CATCH =
  'overtone guard: did not run this command: the guard failed while waiting on the person. ' +
  'It stages, commits or pushes a private path toward a public repo. Stage files by name, never the private path, ' +
  'and ask the person how they want it done.'

// What `git ls-remote <url> <patterns>` says now, by ref name; undefined when
// the read failed, timed out, threw or was cut (never a partial answer).
async function liveRefs(
  $: EngineInterface,
  root: string,
  url: string,
  patterns: readonly string[],
): Promise<Map<string, string> | undefined> {
  try {
    const ls = await $.process.run(['git', 'ls-remote', url, ...patterns], { cwd: root, timeoutMs: 10_000 })
    if (ls.exitCode !== 0 || ls.isStdoutTruncated) return undefined
    const said = new Map<string, string>()
    for (const line of ls.stdout.split('\n')) {
      const [oid, ref] = line.split('\t')
      if (oid && ref) said.set(ref.trim(), oid.trim())
    }
    return said
  } catch {
    return undefined
  }
}

// Which of these reads' live commits this clone has (`here`), and which
// checks threw or timed out (`unchecked`), for liveCheck.
async function liveHere($: EngineInterface, root: string, reads: readonly LiveRead[]) {
  const here = new Set<string>()
  const unchecked = new Set<string>()
  for (const r of reads) {
    for (const oid of r.live) {
      if (typeof oid !== 'string' || oid === r.tracking || here.has(oid) || unchecked.has(oid)) continue
      try {
        const has = await $.process.run(['git', 'cat-file', '-e', `${oid}^{commit}`], { cwd: root, timeoutMs: 10_000 })
        if (has.exitCode === 0) here.add(oid)
      } catch {
        unchecked.add(oid)
      }
    }
  }
  return { here, unchecked }
}

// A ref-set push excludes (`--not --remotes=<remote>`) every commit any of the
// remote's tracking refs holds. Each of those refs, read live: null when the
// remote still has exactly what they say, else why the guard cannot trust them
// (an ask). `urls`: every guarded push URL of the remote.
async function trackingStale(
  $: EngineInterface,
  root: string,
  remote: string,
  urls: readonly string[],
): Promise<string | null> {
  const prefix = `refs/remotes/${remote}/`
  const unlisted = "the guard could not list this clone's tracking refs for the remote, so it cannot tell what the push republishes"
  let list: Awaited<ReturnType<EngineInterface['process']['run']>>
  try {
    list = await $.process.run(['git', 'for-each-ref', '--format=%(refname) %(objectname) %(symref)', prefix], {
      cwd: root,
      timeoutMs: 10_000,
    })
  } catch {
    return unlisted
  }
  if (list.exitCode !== 0 || list.isStdoutTruncated) return unlisted
  const reads: LiveRead[] = []
  for (const line of list.stdout.split('\n')) {
    if (line.trim() === '') continue
    const [ref, oid, symref] = line.trim().split(' ')
    if (!ref || !oid || !ref.startsWith(prefix)) return unlisted
    // `origin/HEAD` and the like: the ref it points at is read as itself.
    if (symref) {
      if (symref.startsWith(prefix)) continue
      return `the tracking ref ${ref.slice('refs/remotes/'.length)} points outside the remote, so the guard cannot tell what the push republishes`
    }
    reads.push({ base: ref, tracking: oid, live: [] })
  }
  // No tracking refs: nothing is excluded, so nothing is trusted.
  if (!reads.length) return null
  for (const url of urls) {
    const said = await liveRefs($, root, url, ['refs/heads/*'])
    reads.forEach(r => r.live.push(said === undefined ? undefined : said.get(`refs/heads/${r.base.slice(prefix.length)}`) ?? null))
  }
  const { here, unchecked } = await liveHere($, root, reads)
  const checked = liveCheck(reads, here, unchecked)
  if ('why' in checked) return checked.why
  return refSetStaleWhy(checked.stale)
}

export const register: Register = (on, options) => {
  // The person's own vault (the vault_path setting): guarded in every repo.
  const own = typeof options?.vault_path === 'string' ? options.vault_path : ''
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const command = typeof e.command === 'string' ? e.command : ''
    const id = e.tool_use_id
    let deny: string | undefined

    // Every command goes to the reader: a text test for "git" would be
    // stricter than it (`gi\t add`, `"$G" add`, `xargs git` fed a verb).
    // A command it finds no git add, commit or push in reads nothing.
    if (command.trim() !== '') {
      // ---- observe: fail open -------------------------------------------
      let findings: Finding[] = []
      try {
        const cwd = await $.session.cwd()
        const home = await $.env.get('HOME')
        const ops = await readOps($, command, cwd, home)
        const cache = new Map<string, RepoFacts | 'none' | null>()
        let textVault: VaultFacts | undefined
        for (const op of ops) {
          // Git runs in a repository the guard cannot name (find -execdir,
          // `git -C {}`): no read of this one says where it goes. It asks.
          if (op.unknownRepo) {
            findings.push(assess(op, null, home))
            continue
          }
          // A push's facts depend on its target, and a forced add's on its
          // pathspecs (the ignored files), so each of those reads its own.
          const key = `${op.kind}\0${op.cwd}\0${op.kind === 'push' || stagesIgnored(op) ? op.text : ''}`
          if (!cache.has(key)) {
            // The facts this op needs, by plain git reads. 'none': not a git
            // repo (the command cannot stage anything). `$.process.run` is
            // spelled at each call, as the host reads it from source.
            let facts: RepoFacts | 'none' | null
            try {
              const T = 10_000
              const top = await $.process.run(['git', 'rev-parse', '--show-toplevel'], { cwd: op.cwd, timeoutMs: T })
              if (top.exitCode !== 0) facts = 'none'
              else {
                const root = top.stdout.trim()
                // On a push, every git read below fails closed: a throw or
                // timeout makes the plan opaque or the fact unknown (asks),
                // never the text-only pass. `unread` names the first such
                // read that decides where or what the push sends.
                let unread: string | null = null
                let remotes = ''
                // A cut read is not a read, nor is a failed one: on a push,
                // only exit 0 with every byte counts.
                const fullRead = (r: { exitCode: number; isStdoutTruncated: boolean }) =>
                  r.exitCode === 0 && !r.isStdoutTruncated
                try {
                  const rv = await $.process.run(['git', 'remote', '-v'], { cwd: root, timeoutMs: T })
                  if (op.push && !fullRead(rv)) unread = "the guard could not read the repo's remotes"
                  else remotes = rv.stdout
                } catch (err) {
                  if (!op.push) throw err
                  unread = "the guard could not read the repo's remotes"
                }
                // Is each GitHub remote (and a push's URL as written) private?
                const target = op.push?.remote
                const visibility = await askGithub($, [
                  ...publicRemotes(remotes),
                  ...(target && githubRepo(target) ? [target] : []),
                ])
                let status: string | null = null
                let ignored: string | null | undefined
                let pushPaths: string[] | null = null
                let plan: PushPlan | null = null
                // push: the current branch's ref (refs/heads/<name>), null when detached.
                let headRef: string | null = null
                // The base trees for the new-folder rule: HEAD for stage and
                // commit; for a push, what each destination branch has on that
                // remote. A push destination with no readable base leaves the
                // new-folder judgement unknown, which assess asks about.
                let workBaseUnknown = false
                const bases: string[] = op.push ? [] : ['HEAD']
                if (op.push) {
                  try {
                    // Exit 1: a detached HEAD (no current branch). Any other
                    // failure, or a cut answer, is unread.
                    const head = await $.process.run(['git', 'symbolic-ref', '-q', 'HEAD'], { cwd: root, timeoutMs: T })
                    if (fullRead(head)) headRef = head.stdout.trim() || null
                    else if (head.exitCode !== 1 || head.isStdoutTruncated) {
                      unread ??= 'the guard could not read the current branch'
                    }
                  } catch {
                    unread ??= 'the guard could not read the current branch'
                  }
                  // Where a bare push goes from this branch, as git names it.
                  let defaultRemote: string | null = null
                  if (op.push.remote === null && headRef !== null) {
                    try {
                      const name = await $.process.run(['git', 'for-each-ref', '--format=%(push:remotename)', headRef], {
                        cwd: root,
                        timeoutMs: T,
                      })
                      // Empty: no push remote configured (then `origin`).
                      if (fullRead(name)) defaultRemote = name.stdout.trim() || null
                      else unread ??= 'the guard could not read which remote this branch pushes to'
                    } catch {
                      unread ??= 'the guard could not read which remote this branch pushes to'
                    }
                  }
                  // No refspec and no ref set: git config decides what goes
                  // (remote.<name>.mirror, remote.<name>.push, push.default).
                  // Unset reads exit 1; any other failure (a value git cannot
                  // read as a bool exits 128) leaves it null, which asks.
                  let config: PushConfig | null = null
                  if (needsPushConfig(op.push)) {
                    try {
                      const name = pushRemoteName(op.push, defaultRemote)
                      const rp = await $.process.run(['git', 'config', '--get-all', `remote.${name}.push`], {
                        cwd: root,
                        timeoutMs: T,
                      })
                      const pd = await $.process.run(['git', 'config', '--get', 'push.default'], { cwd: root, timeoutMs: T })
                      // --type=bool: git reads its own bool forms (yes, on, 1,
                      // a bare key) and prints true or false.
                      const mi = await $.process.run(['git', 'config', '--type=bool', '--get', `remote.${name}.mirror`], {
                        cwd: root,
                        timeoutMs: T,
                      })
                      // A cut read is not a read: unreadable, which asks.
                      const read = (r: { exitCode: number; isStdoutTruncated: boolean }) =>
                        (r.exitCode === 0 || r.exitCode === 1) && !r.isStdoutTruncated
                      if (read(rp) && read(pd) && read(mi)) {
                        config = {
                          remotePush: rp.exitCode === 0 ? rp.stdout.split('\n').map(l => l.trim()).filter(Boolean) : [],
                          pushDefault: pd.exitCode === 0 ? pd.stdout.trim() || null : null,
                          mirror: mi.exitCode === 0 && mi.stdout.trim() === 'true',
                        }
                      }
                    } catch {
                      config = null
                    }
                  }
                  plan = pushPlan(op.push, remotes, defaultRemote, config, visibility)
                  // Each destination branch's remote-tracking ref
                  // (refs/remotes/<remote>/<branch>), never another branch.
                  const tracked: string[] = []
                  if (plan.kind === 'revs') {
                    if (plan.dsts === null) workBaseUnknown = true
                    for (const dst of plan.dsts ?? []) {
                      let b = destinationBase(plan.remote, dst, headRef)
                      if (dst === PUSH_DST && headRef !== null) {
                        // A bare push: git names the branch it updates.
                        try {
                          const at = await $.process.run(['git', 'for-each-ref', '--format=%(push)', headRef], {
                            cwd: root,
                            timeoutMs: T,
                          })
                          // Empty: git names none, so no base (unknown).
                          if (fullRead(at)) {
                            const ref = at.stdout.trim()
                            b = ref.startsWith(`refs/remotes/${plan.remote}/`) ? ref : null
                          } else unread ??= 'the guard could not read which branch this push updates'
                        } catch {
                          unread ??= 'the guard could not read which branch this push updates'
                        }
                      }
                      if (b === null) workBaseUnknown = true
                      else if (!tracked.includes(b)) tracked.push(b)
                    }
                  }
                  // A read that decides where or what the push sends failed:
                  // ask. Only a push to a named remote that is not public
                  // (or a delete) still passes, as the head reads do not
                  // change it.
                  if (unread !== null && !(plan.kind === 'none' && op.push.remote !== null && remotes !== '')) {
                    plan = {
                      kind: 'opaque',
                      why: `${unread}, so it cannot tell where or what this push sends`,
                      ...(plan.kind === 'none' || !plan.urls ? {} : { urls: plan.urls }),
                    }
                  }
                  if (plan.kind === 'revs') {
                    // Tracking refs can be stale (the remote rewound since the
                    // last fetch). What each guarded push URL has now, live;
                    // a failed, timed-out or cut read leaves it undefined.
                    let revs = plan.revs
                    if (tracked.length) {
                      const prefix = `refs/remotes/${plan.remote}/`
                      const heads = tracked.map(b => `refs/heads/${b.slice(prefix.length)}`)
                      const reads: LiveRead[] = []
                      // Every read here fails closed: a throw or timeout leaves
                      // it unavailable, which liveCheck turns into an ask.
                      for (const b of tracked) {
                        let tracking: string | null | undefined
                        try {
                          const tr = await $.process.run(['git', 'rev-parse', '-q', '--verify', `${b}^{commit}`], {
                            cwd: root,
                            timeoutMs: T,
                          })
                          tracking = tr.exitCode === 0 ? tr.stdout.trim() || null : null
                        } catch {
                          tracking = undefined
                        }
                        reads.push({ base: b, tracking, live: [] })
                      }
                      for (const url of plan.urls) {
                        const said = await liveRefs($, root, url, heads)
                        reads.forEach((r, i) => r.live.push(said === undefined ? undefined : said.get(heads[i]!) ?? null))
                      }
                      // Which live commits this clone has.
                      const { here, unchecked } = await liveHere($, root, reads)
                      const checked = liveCheck(reads, here, unchecked)
                      if ('why' in checked) {
                        plan = { kind: 'opaque', why: checked.why, urls: plan.urls }
                      } else {
                        revs = liveRange(plan, checked.stale)
                        // A stale destination's base is its live commit; one
                        // gone there has no base.
                        for (const b of tracked) {
                          const st = checked.stale.find(x => x.base === b)
                          if (st === undefined) bases.push(b)
                          else if (st.oid !== null) bases.push(st.oid)
                          else workBaseUnknown = true
                        }
                      }
                    }
                    if (plan.kind === 'revs' && op.push.sets.length) {
                      // A ref set (--all, --branches, --mirror, --tags) is
                      // measured against every tracking ref of the remote
                      // (`--remotes=<remote>`), not a named destination, so
                      // each of those is read live too: any that is not what
                      // the remote has now asks.
                      const why = await trackingStale($, root, plan.remote, plan.urls)
                      if (why !== null) plan = { kind: 'opaque', why, urls: plan.urls }
                    }
                    if (plan.kind === 'revs') {
                      // What this push publishes: its source refs, less every
                      // commit THAT remote has. A failed, cut, thrown or
                      // timed-out list stays null: assess asks. -z: names
                      // as written, never git's C-quoting (`"\303\251.png"`).
                      // --diff-merges=separate: a merge lists what it changes
                      // against each parent, so a file only a merge brings (a
                      // conflict resolution) is listed too.
                      try {
                        const log = await $.process.run(
                          ['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', ...revs, '--'],
                          { cwd: root, timeoutMs: T },
                        )
                        pushPaths =
                          log.exitCode === 0 && !log.isStdoutTruncated
                            ? [...new Set(log.stdout.split('\0').filter(Boolean))]
                            : null
                      } catch {
                        pushPaths = null
                      }
                    }
                  }
                } else {
                  const st = await $.process.run(['git', 'status', '--porcelain=v1', '-z', '--untracked-files=all'], {
                    cwd: root,
                    timeoutMs: T,
                  })
                  status = st.exitCode === 0 ? st.stdout : null
                  if (stagesIgnored(op)) {
                    // -f stages ignored files too, which status does not
                    // list. git matches the pathspecs as `git add` would, from
                    // where it runs; a sweep with none lists the whole repo.
                    // A failed or cut listing stays null: assess asks.
                    ignored = null
                    try {
                      const specs = op.specs.filter(s => !s.unreadable && !s.raw.startsWith(GUARD.notesPrefix))
                      const whole = op.isOpaque || specs.length === 0
                      const ls = await $.process.run(
                        [
                          'git', 'ls-files', '-z', '--others', '--ignored', '--exclude-standard', '--full-name',
                          ...(whole ? [] : ['--', ...specs.map(s => (s.raw.startsWith('~') ? s.abs : s.raw))]),
                        ],
                        { cwd: whole ? root : op.cwd, timeoutMs: T },
                      )
                      if (ls.exitCode === 0 && !ls.isStdoutTruncated) ignored = ls.stdout
                    } catch {
                      ignored = null
                    }
                  }
                }
                // Known slugs: those every base tree has (new to any one is
                // new). The new-work-folder rule: only where the repo keeps
                // its working notes in the vault, as a base tree's committed
                // file OR the working tree's says. The same change cannot
                // switch it off: a deleted or broken working copy leaves a
                // committed "vault" standing. Missing or unreadable: no.
                let knownWorkSlugs: string[] | null = null
                let vaultWorkNotes = false
                // Where the private vault is: what every copy of the file
                // read here says (base trees and the working tree).
                const vaultReads: VaultRead[] = []
                // A push also reads HEAD's committed copy and each pushed
                // revision's: add-only (never a base, never a slug), so a
                // first push of a new branch keeps what the branch itself
                // commits when the working copy is deleted or broken.
                if (op.push && plan?.kind === 'revs') {
                  const at = plan.revs.indexOf('--not')
                  const pushed = (at < 0 ? plan.revs : plan.revs.slice(0, at)).filter(r => !r.startsWith('-'))
                  // A ref set (--all/--branches, --mirror, --tags) sends every
                  // tip it names, each with its own committed copy: read them
                  // all. A listing that fails or runs past MAX_TIPS, or a tip
                  // whose copy cannot be read, asks.
                  const tips = new Set<string>()
                  let setWhy: string | null = null
                  if (op.push.sets.length) {
                    const patterns = [
                      ...new Set(op.push.sets.map(s => (s === '--branches' ? 'refs/heads/' : s === '--tags' ? 'refs/tags/' : 'refs/'))),
                    ]
                    try {
                      const list = await $.process.run(['git', 'for-each-ref', '--format=%(objectname)', ...patterns], {
                        cwd: root,
                        timeoutMs: T,
                      })
                      if (!fullRead(list)) setWhy = 'the guard could not list the refs this push sends'
                      else {
                        const oids = [...new Set(list.stdout.split('\n').map(l => l.trim()).filter(Boolean))]
                        if (oids.length > MAX_TIPS) {
                          setWhy = `this push sends ${oids.length} ref tips, more than the ${MAX_TIPS} whose ${GUARD.newWorkFolders.file} the guard reads`
                        } else for (const oid of oids) tips.add(oid)
                      }
                    } catch {
                      setWhy = 'the guard could not list the refs this push sends'
                    }
                  }
                  for (const rev of [...new Set(['HEAD', ...pushed, ...tips])]) {
                    if (setWhy !== null) break
                    if (bases.includes(rev)) continue
                    try {
                      const copy = await $.process.run(['git', 'show', `${rev}:${GUARD.newWorkFolders.file}`], {
                        cwd: root,
                        timeoutMs: T,
                      })
                      if (copy.exitCode === 0 && !copy.isStdoutTruncated) {
                        vaultWorkNotes ||= workNotesInVault(copy.stdout)
                        vaultReads.push(readVault(copy.stdout))
                      } else if (copy.exitCode === 0) {
                        // cut: as a base read; on a ref-set tip, it asks
                        workBaseUnknown = true
                        if (tips.has(rev)) setWhy = `the guard could not read ${GUARD.newWorkFolders.file} at a ref this push sends`
                      } else if (tips.has(rev)) {
                        // A ref-set tip whose copy git would not show: absent
                        // only when that tip's tree has no such path; any
                        // other failure asks, as a cut or thrown read does.
                        const has = await $.process.run(
                          ['git', 'ls-tree', '--full-tree', rev, '--', GUARD.newWorkFolders.file],
                          { cwd: root, timeoutMs: T },
                        )
                        if (has.exitCode !== 0 || has.isStdoutTruncated || has.stdout.trim() !== '') {
                          workBaseUnknown = true
                          setWhy = `the guard could not read ${GUARD.newWorkFolders.file} at a ref this push sends`
                        }
                      }
                    } catch {
                      // Thrown or timed out: as a thrown base read, the
                      // work-folder judgement is unknown (asks on one); on a
                      // ref-set tip, it asks.
                      workBaseUnknown = true
                      if (tips.has(rev)) setWhy = `the guard could not read ${GUARD.newWorkFolders.file} at a ref this push sends`
                    }
                  }
                  if (setWhy !== null) {
                    plan = { kind: 'opaque', why: `${setWhy}, so it cannot tell which paths each keeps private`, urls: plan.urls }
                  }
                }
                // On a push a thrown or timed-out read leaves the base unknown
                // (assess asks on work folders); stage and commit keep their
                // text-only fallback.
                for (const b of bases) {
                  let tree: Awaited<ReturnType<EngineInterface['process']['run']>>
                  try {
                    tree = await $.process.run(['git', 'ls-tree', '-d', '--name-only', '-z', b, WORK_ROOT], {
                      cwd: root,
                      timeoutMs: T,
                    })
                  } catch (err) {
                    if (!op.push) throw err
                    workBaseUnknown = true
                    continue
                  }
                  if (tree.exitCode !== 0) {
                    if (op.push) workBaseUnknown = true
                    continue
                  }
                  const slugs = slugsFrom(tree.stdout)
                  knownWorkSlugs = knownWorkSlugs === null ? slugs : knownWorkSlugs.filter(x => slugs.includes(x))
                  // Every base's copy: its private_paths and vault add up.
                  try {
                    const committed = await $.process.run(['git', 'show', `${b}:${GUARD.newWorkFolders.file}`], {
                      cwd: root,
                      timeoutMs: T,
                    })
                    if (committed.exitCode === 0 && !committed.isStdoutTruncated) {
                      vaultWorkNotes ||= workNotesInVault(committed.stdout)
                      vaultReads.push(readVault(committed.stdout))
                    }
                  } catch (err) {
                    if (!op.push) throw err
                    workBaseUnknown = true
                  }
                }
                try {
                  const text = await $.fs.read(`${root}/${GUARD.newWorkFolders.file}`)
                  vaultWorkNotes ||= workNotesInVault(text)
                  vaultReads.push(readVault(text))
                } catch {
                  // missing or unreadable as a file: nothing from it
                }
                const vault = await resolveVault($, vaultReads, own, home)
                facts = {
                  root,
                  remotes,
                  status,
                  ignored,
                  pushPaths,
                  knownWorkSlugs,
                  vaultWorkNotes,
                  vault,
                  visibility,
                  pushPlan: plan,
                  ...(workBaseUnknown ? { workBaseUnknown } : {}),
                }
              }
            } catch (err) {
              // No process access (tests, a host without it) or git would not
              // start: judge from the command text and the path list alone.
              facts = null
              $.ui.log(`overtone guard: git facts unavailable, text only (${String(err).slice(0, 120)})`, { to: 'debug' })
            }
            cache.set(key, facts)
          }
          const facts = cache.get(key)
          if (facts === 'none') continue
          // An alias the guard could not read, with no git to say whether the
          // repo has a public remote: not asked about (text mode passes
          // what it cannot place).
          if (!facts && op.alias !== undefined) continue
          // Text mode: the session project's kivna/vault.json says where the
          // vault is.
          if (!facts) textVault ??= await resolveVault($, [await readVaultFile($, `${cwd}/${GUARD.newWorkFolders.file}`)], own, home)
          const vault = facts ? facts.vault : textVault
          findings.push(assess(vault ? await landSpecs($, op, vault) : op, facts ?? null, home, undefined, textVault))
        }
      } catch (err) {
        findings = []
        $.ui.log(`overtone guard: detection failed, command passed (${String(err).slice(0, 160)})`, { to: 'debug' })
        try {
          const n = Number(await $.store.get(FAILURES_KEY)) || 0
          await $.store.set(FAILURES_KEY, n + 1)
        } catch {
          // the count is a nicety
        }
      }

      if (findings.some(f => f.verdict === 'ask')) {
        // ---- ask: fail closed -------------------------------------------
        // `asking` stays set until the decision is made, so a failure
        // anywhere in here reaches `.catch` as a refusal.
        const key = id ?? command
        asking.add(key)
        let outcome: Outcome = { kind: 'error' }
        try {
          const ev = evidence(command, findings)
          holds.set(key, { ...ev, where: 'band' })
          try {
            const opened = await $.ui.open({
              id: PANE_ID,
              title: 'overtone guard',
              rows: Math.min(MAX_ROWS, ev.rows.length) + 6,
            })
            if (opened.isPlaced) holds.set(key, { ...ev, where: 'pane' })
          } catch {
            // no pane: the band draws it
          }
          $.ui.invalidate('ui.render')

          let timer: { cancel: () => void } | undefined
          const timeout = new Promise<Outcome>(resolve => {
            timer = $.clock.after(GUARD.timeoutMs, () => resolve({ kind: 'timeout' }))
          })
          const startedAt = await $.clock.now()
          // `settled`: the race is over. An answer after that (the dialog
          // can outlive the timeout; nothing closes it) is dropped here.
          let settled = false
          const asked = $.ui
            .ask(question(command, findings), { header: HEADER, options: [SAFE, RUN] })
            .then(
              (answer): Outcome => (settled ? { kind: 'timeout' } : { kind: 'answer', answer, elapsedMs: 0 }),
              (): Outcome => ({ kind: 'dismissed' }),
            )
          outcome = await Promise.race([asked, timeout])
          settled = true
          timer?.cancel()
          if (outcome.kind === 'answer') outcome = { ...outcome, elapsedMs: (await $.clock.now()) - startedAt }
        } catch {
          outcome = { kind: 'error' }
        } finally {
          holds.delete(key)
          try {
            if (!holds.size) await $.ui.close({ id: PANE_ID })
            $.ui.invalidate('ui.render')
          } catch {
            // drawing is not the decision
          }
        }

        const decision = decide(outcome)
        if (!decision.run) {
          const late = outcome.kind === 'timeout'
          deny = denyMessage(command, findings, decision.why, late ? LATE_NOTE : undefined)
          if (late) {
            try {
              $.ui.log(`overtone guard: refused after ${Math.round(GUARD.timeoutMs / 1000)} s. ${LATE_NOTE}`)
            } catch {
              // the deny carries the note too
            }
          }
        }
        asking.delete(key)
      }
    }

    if (deny !== undefined) return { deny }
    // ---- pass: the one call of next(e) --------------------------------------
    // Marked before it starts; a rejection beneath leaves the mark for
    // `.catch`, which then never calls it again.
    if (id !== undefined) entered.add(id)
    const result = await next(e)
    if (id !== undefined) entered.delete(id)
    return result
  }).catch(($, e, next) => {
    const id = e.tool_use_id
    const key = id ?? (typeof e.command === 'string' ? e.command : '')
    const wasEntered = next.called || (id !== undefined && entered.has(id))
    if (id !== undefined) entered.delete(id)
    // The command already went beneath: its own result (or rejection)
    // stands. Undefined is "this hook absent", which the engine settles with
    // the hook's last `next` result; it never runs the command again.
    if (wasEntered) return undefined
    // The failure came before `next`. Mid-decision: refuse.
    if (asking.has(key)) {
      asking.delete(key)
      holds.delete(key)
      return { deny: REFUSED_IN_CATCH }
    }
    // Otherwise the failure was the guard's own detection: pass, once.
    return next(e)
  })


  // ---- the evidence: one drawing for the pane and the band ----------------
  const draw = (
    { Box, Text }: Pick<Elements[RenderSurface], 'Box' | 'Text'>,
    hold: Hold,
    columns: number,
  ) => {
    const shown = hold.rows.slice(0, MAX_ROWS)
    const more = hold.rows.length - shown.length
    const width = Math.max(30, columns - 2)
    return (
      <Box key="guard" flexDirection="column" width={width}>
        <Text key="head" bold color="warning" wrap="truncate-end">
          ⚠ overtone guard · Claude is waiting on your answer in the dialog
        </Text>
        <Text key="cmd" wrap="truncate-end">
          <Text dimColor>Command </Text>
          <Text bold>{hold.command.split('\n')[0]}</Text>
        </Text>
        <Text key="would" wrap="truncate-end">
          <Text dimColor>Would   </Text>
          <Text bold color="error">
            {hold.verb} {hold.rows.length === 1 ? 'a private path' : `${hold.rows.length} private paths`} toward{' '}
            {hold.unresolved
              ? 'a destination the guard could not resolve'
              : hold.unconfirmed
                ? `${hold.remote} (could not confirm it is private)`
                : `public ${hold.remote}`}
          </Text>
        </Text>
        {shown.map((hit, i) => (
          <Text key={`row:${i}`} wrap="truncate-end">
            {'  '}
            {hit.path}
            <Text dimColor> · {hit.reason}</Text>
          </Text>
        ))}
        {more > 0 ? (
          <Text key="more" dimColor>
            {'  '}+{more} more
          </Text>
        ) : null}
        <Text key="foot" dimColor wrap="truncate-end">
          {hold.mode === 'text' ? 'Read from the command text (git was not reachable). ' : ''}
          {hold.incomplete ? `Careful: ${hold.incomplete}. ` : ''}
          {`"${SAFE}" is the default; no answer in ${Math.round(GUARD.timeoutMs / 1000)} s counts as no.`}
        </Text>
      </Box>
    )
  }

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    const hold = firstHold()
    if (e.requestId !== PANE_ID || !hold) return next(e)
    try {
      const { Box, Text } = $.ui.resolve(e)
      return draw({ Box, Text }, hold, e.props.bodyColumns ?? 80)
    } catch {
      return next(e)
    }
  }).catch(($, e, next) => (next.called ? undefined : next(e)))

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const hold = firstHold()
    if (!hold || hold.where !== 'band' || e.props.hasSurvey) return next(e)
    try {
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box flexDirection="column">
          {draw({ Box, Text }, hold, e.props.bodyColumns ?? 80)}
          {await next(e)}
        </Box>
      )
    } catch {
      return next(e)
    }
  }).catch(($, e, next) => (next.called ? undefined : next(e)))
}
