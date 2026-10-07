import { describe, expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

const KERD = '/Users/alex/code/Kerd'
const REMOTES = 'origin\tgit@github.com:alex/Kerd.git (fetch)\norigin\tgit@github.com:alex/Kerd.git (push)\n'
const STATUS = '?? kerd-laptop-result.patch\0 M README.md\0'
const VAULT_JSON = `${KERD}/kivna/vault.json`
const OID_TRACKED = 'a'.repeat(40)
const remotesOf = (url: string) => `origin\t${url} (fetch)\norigin\t${url} (push)\n`
// The repo's kivna/vault.json: the vault, where notes go, the repo's own private paths.
const VAULT_TEXT =
  JSON.stringify({ vault: '~/notes/vault', folder: 'kerd', work_notes: 'vault', private_paths: ['kerd-laptop-result.patch'] }) + '\n'
// What `gh repo view github.com/<repo> --json isPrivate,url` prints.
const ghSays = (repo: string, isPrivate: boolean): [string, number] => [
  `${JSON.stringify({ isPrivate, url: `https://github.com/${repo}` })}\n`,
  0,
]

type Answer = string | 'dismiss' | 'never'

// A path as git prints it without -z (core.quotePath on): any byte outside
// printable ASCII, a quote or a backslash, and the name is quoted, octal-escaped.
const cQuote = (p: string): string => {
  const bytes = [...new TextEncoder().encode(p)]
  if (!bytes.some(b => b < 0x20 || b >= 0x7f || b === 0x22 || b === 0x5c)) return p
  return `"${bytes.map(b => (b === 0x22 || b === 0x5c ? `\\${String.fromCharCode(b)}` : b < 0x20 || b >= 0x7f ? `\\${b.toString(8).padStart(3, '0')}` : String.fromCharCode(b))).join('')}"`
}

type World = {
  ran: string[]
  asked: string[]
  argv: string[][]
  answer: Answer
  answerAfterMs: number
  noProcess: boolean
  gitThrows: boolean
  logs: string[]
  remotes: string
  // What `git log` prints for the push's revision range.
  log: (args: string) => string
  // The Bash tool beneath rejects (a downstream failure).
  bashThrows: boolean
  // `git config` answers by key: [stdout, exitCode, truncated?]; a key not here is unset (exit 1).
  config: Record<string, [string, number] | [string, number, boolean]>
  // `git ls-files --ignored` output, or 'fail' (exit 128).
  ignored: string | 'fail'
  status: string
  // Where `gh` answers ('none': nowhere), and what it says per repository
  // argument (`github.com/o/r`): [stdout, exitCode]; one not here fails (exit 1).
  ghAt: string
  gh: Record<string, [string, number]>
  // gh paths that run but get no answer from GitHub in time: they reject
  // after `ghTakesMs` on the clock. A test's rejection reaches the plugin as
  // "no implementation for process.run", never in the engine's own words, so
  // the guard reads it by how long it took.
  ghHangsAt: string[]
  ghTakesMs: number
  // Files `$.fs.read` finds, by absolute path.
  files: Record<string, string>
  // What `git show <base>:kivna/vault.json` prints, at any base or per base;
  // null: absent.
  committed: string | null | ((base: string) => string | null)
  // Bases `git ls-tree` cannot read (a remote branch that does not exist):
  // no tracking ref here, and no such branch on the remote.
  missingBases: string[]
  // Refs outside refs/heads/ the remote has, for a `git ls-remote` glob such
  // as `refs/pull/*/head` (a custom fetch refspec's source).
  remoteRefs: string[]
  // The branches the remote has, by name; null: every tracking ref's name.
  remoteBranches: string[] | null
  // What `git ls-remote <url> <refs>` says per URL and ref (null: no such
  // ref), or 'fail' (exit 128) / 'cut' (truncated). Default: what the
  // tracking ref holds (OID_TRACKED), so nothing is stale.
  live: ((url: string, ref: string) => string | null) | 'fail' | 'cut'
  // The remote-tracking refs `git for-each-ref refs/remotes/origin/` lists
  // (ref -> what it holds; `symref:<target>` makes it a symbolic ref).
  // Default: one branch, at the commit the live remote has.
  tracking: Record<string, string>
  // Commits this clone has (`git cat-file -e`).
  commits: string[]
  // The folders under docs/work/ every base's tree has (`git ls-tree`).
  workTree: string[]
  // `git log` exit code and truncation.
  logExit: number
  logCut: boolean
  // Commands that throw, by the words after `git` they start with, as a
  // timeout or a failed start does.
  throws: string[]
  // Answers that override the world's, by the same prefix:
  // [stdout, exitCode, truncated].
  answers: Record<string, [string, number, boolean]>
}

// The engine beneath the plugin: git answered from memory, the Bash tool
// records what ran, the AskUserQuestion dialog answers as the test says.
function world(on: On, over: Partial<World> = {}) {
  const w: World = {
    ran: [],
    asked: [],
    argv: [],
    answer: 'Run it',
    answerAfterMs: 5_000,
    noProcess: false,
    gitThrows: false,
    logs: [],
    remotes: REMOTES,
    log: () => 'README.md\n',
    bashThrows: false,
    config: {},
    ignored: '',
    status: STATUS,
    ghAt: 'gh',
    ghHangsAt: [],
    ghTakesMs: 5_000,
    gh: {
      'github.com/alex/Kerd': ghSays('alex/Kerd', false),
      'github.com/alex/notes': ghSays('alex/notes', true),
      'github.com/someone/kerd-mirror': ghSays('someone/kerd-mirror', false),
    },
    files: { [VAULT_JSON]: VAULT_TEXT },
    committed: VAULT_TEXT,
    missingBases: [],
    remoteRefs: [],
    remoteBranches: null,
    live: (url, ref) => (w.missingBases.some(b => b.endsWith(`/${ref.slice('refs/heads/'.length)}`)) ? null : OID_TRACKED),
    tracking: { 'refs/remotes/origin/feature': OID_TRACKED },
    commits: [OID_TRACKED],
    workTree: ['docs/work/jev-trial', 'docs/work/question-sets'],
    logExit: 0,
    logCut: false,
    throws: [],
    answers: {},
    ...over,
  }
  const clock = mock.clock(on, { now: 1_000_000 })
  mock.env(on, { HOME: '/Users/alex' })
  mock.store(on)
  on('session.cwd', () => ({ value: KERD }))
  on('fs.read', ($, e) => {
    const text = w.files[e.path]
    if (text === undefined) throw new Error('ENOENT')
    return { value: text } as never
  })
  on('process.run', async ($, e) => {
    if (w.noProcess) throw new Error('no process access')
    w.argv.push([...e.argv])
    const a = e.argv.join(' ')
    if (w.gitThrows && a.includes('status')) throw new Error('boom')
    if (w.throws.some(t => a === `git ${t}` || a.startsWith(`git ${t} `))) throw new Error(`${a} timed out`)
    const out = (stdout: string, exitCode = 0, isStdoutTruncated = false) => ({
      value: { exitCode, stdout, stderr: '', isStdoutTruncated, isStderrTruncated: false },
    })
    const given = Object.entries(w.answers).find(([t]) => a === `git ${t}` || a.startsWith(`git ${t} `))
    if (given) return out(...given[1])
    if (a === 'git rev-parse --show-toplevel') return out(`${KERD}\n`)
    if (a === 'git remote -v') return out(w.remotes)
    if (a === 'git symbolic-ref -q HEAD') return out('refs/heads/feature\n')
    if (a.startsWith('git for-each-ref --format=%(push) ')) return out('refs/remotes/origin/feature\n')
    if (a.startsWith('git for-each-ref --format=%(refname) %(objectname) %(symref) ')) {
      return out(
        Object.entries(w.tracking)
          .map(([ref, v]) => (v.startsWith('symref:') ? `${ref} ${OID_TRACKED} ${v.slice(7)}\n` : `${ref} ${v} \n`))
          .join(''),
      )
    }
    if (a.startsWith('git for-each-ref')) return out('origin\n')
    if (a.startsWith('git status')) return out(w.status)
    if (e.argv[1] === 'repo' && e.argv[2] === 'view') {
      if (w.ghHangsAt.includes(e.argv[0]!)) {
        if (w.ghTakesMs) await clock.sleep(w.ghTakesMs)
        throw new Error('timed out')
      }
      if (e.argv[0] !== w.ghAt) throw new Error(`spawn ${e.argv[0]} ENOENT`)
      const [stdout, code] = w.gh[e.argv[3]!] ?? ['', 1]
      return out(stdout, code)
    }
    // Whether a tip's tree holds kivna/vault.json: as `committed` says.
    if (a.startsWith('git ls-tree --full-tree ') && a.endsWith(' -- kivna/vault.json')) {
      const base = e.argv[3]!
      const text = typeof w.committed === 'function' ? w.committed(base) : w.committed
      return out(text === null ? '' : `100644 blob ${'b'.repeat(40)}\tkivna/vault.json\n`)
    }
    if (a.startsWith('git ls-tree')) {
      const b = e.argv.filter(x => !x.startsWith('-'))[2]!
      if (w.missingBases.includes(b)) return out('', 128)
      const z = e.argv.includes('-z')
      return out(w.workTree.map(p => `${z ? p : cQuote(p)}${z ? '\0' : '\n'}`).join(''))
    }
    if (a.startsWith('git show') && a.endsWith(':kivna/vault.json')) {
      const base = e.argv[2]!.slice(0, -':kivna/vault.json'.length)
      const text = typeof w.committed === 'function' ? w.committed(base) : w.committed
      return text === null ? out('', 128) : out(text)
    }
    // `git log` prints names C-quoted, one a line; with -z as written, NUL-ended.
    if (a.startsWith('git log')) {
      const names = w.log(a).split('\n').filter(Boolean)
      const text = e.argv.includes('-z') ? names.map(n => `${n}\0`).join('') : names.map(n => `${cQuote(n)}\n`).join('')
      return out(text, w.logExit, w.logCut)
    }
    if (a.startsWith('git rev-parse -q --verify ')) {
      const base = e.argv[4]!.replace(/\^\{commit\}$/, '')
      return w.missingBases.includes(base) ? out('', 1) : out(`${OID_TRACKED}\n`)
    }
    if (e.argv[1] === 'ls-remote') {
      const live = w.live
      if (live === 'fail') return out('', 128)
      if (live === 'cut') return out('', 0, true)
      const url = e.argv[2]!
      // `refs/heads/*` is every branch the clone tracks, as the remote says.
      const asked = e.argv.slice(3).flatMap(ref =>
        ref === 'refs/heads/*'
          ? (w.remoteBranches ?? Object.keys(w.tracking)
              .filter(t => !w.tracking[t]!.startsWith('symref:'))
              .map(t => t.slice('refs/remotes/origin/'.length))).map(b => `refs/heads/${b}`)
          : ref.includes('*')
            ? w.remoteRefs.filter(r => new RegExp(`^${ref.split('*').map(p => p.replace(/[.+?^${}()|[\]\\]/g, '\\$&')).join('.+')}$`).test(r))
            : [ref],
      )
      const lines = asked.flatMap(ref => {
        const oid = live(url, ref)
        return oid === null ? [] : [`${oid}\t${ref}\n`]
      })
      return out(lines.join(''))
    }
    if (a.startsWith('git cat-file -e ')) return out('', w.commits.includes(e.argv[3]!.replace(/\^\{commit\}$/, '')) ? 0 : 1)
    if (a.startsWith('git config')) {
      const [stdout, code, cut] = w.config[e.argv[e.argv.length - 1]!] ?? ['', 1]
      return out(stdout, code, cut ?? false)
    }
    if (a.startsWith('git ls-files')) return w.ignored === 'fail' ? out('', 128) : out(w.ignored)
    return out('', 1)
  })
  on('ui.open', () => ({ value: { isPlaced: false, reason: 'unasked below 144 columns' } }) as never)
  on('ui.close', () => ({ value: undefined }))
  on('ui.log', ($, e) => {
    w.logs.push(e.text)
    return { value: undefined }
  })
  on('tool.call', { tool: 'AskUserQuestion' }, async ($, e) => {
    const q = (e.questions as { question: string }[])[0]!.question
    w.asked.push(q)
    if (w.answer === 'never') return new Promise(() => {}) as never
    await clock.sleep(w.answerAfterMs)
    if (w.answer === 'dismiss') return { deny: 'dismissed' }
    return { result: { questions: e.questions, answers: { [q]: w.answer } } } as never
  })
  on('tool.call', { tool: 'Bash' }, ($, e) => {
    w.ran.push(e.command)
    if (w.bashThrows) throw new Error('the tool beneath failed')
    return { result: { stdout: '', stderr: '', interrupted: false } } as never
  })
  on('ui.render', ($, e) => $.ui.resolve(e).Box({}))
  return { w, clock }
}

const bash = (command: string) => ({ tool: 'Bash' as const, command })

describe('guard', () => {
  test('a command with no git passes untouched, no git read', async ($, on) => {
    const { w } = world(on)
    await $.tool.call(bash('ls -la'))
    expect(w.ran).toEqual(['ls -la'])
    expect(w.argv).toEqual([])
    expect(w.asked).toEqual([])
  })

  test('staging by name passes without a dialog', async ($, on) => {
    const { w } = world(on)
    await $.tool.call(bash('git add README.md'))
    expect(w.ran).toEqual(['git add README.md'])
    expect(w.asked).toEqual([])
  })

  test('git add -A that sweeps a private file asks; "Run it" runs it', async ($, on) => {
    const { w, clock } = world(on)
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('kerd-laptop-result.patch')
    expect(w.ran).toEqual(['git add -A'])
  })

  test('"Don\'t run it" refuses with the instructions', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A && git commit -m wip'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('did not run')
    expect(r.deny).toContain('by name')
  })

  test('no answer in 30 s refuses', async ($, on) => {
    const { w, clock } = world(on, { answer: 'never' })
    const call = $.tool.call(bash('git add .'))
    await clock.advance(30_000)
    const r = (await call) as { deny?: string }
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('no answer in 30 s')
  })

  test('a dismissed dialog refuses', async ($, on) => {
    const { w, clock } = world(on, { answer: 'dismiss' })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('did not run')
  })

  test('a typed-ahead "Run it" inside a second refuses', async ($, on) => {
    const { w, clock } = world(on, { answerAfterMs: 100 })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(100)
    const r = (await call) as { deny?: string }
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('typed-ahead')
  })

  test('detection failure fails open and logs to debug, no toast', async ($, on) => {
    const { w } = world(on, { gitThrows: true })
    await $.tool.call(bash('git add -A'))
    expect(w.ran).toEqual(['git add -A'])
    expect(w.asked).toEqual([])
    expect(w.logs.some(l => l.includes('overtone guard: git facts unavailable'))).toBe(true)
  })

  test('no process access: a sweep passes, a named private path still asks', async ($, on) => {
    const { w, clock } = world(on, { noProcess: true, answer: "Don't run it" })
    await $.tool.call(bash('git add -A'))
    expect(w.ran).toEqual(['git add -A'])
    const call = $.tool.call(bash('git add -f .env'))
    await clock.advance(5_000)
    await call
    expect(w.ran).toEqual(['git add -A'])
    expect(w.asked).toHaveLength(1)
  })

  test('push: the target ref is compared with the target remote, not every remote', async ($, on) => {
    const remotes =
      REMOTES + 'vault\tgit@github.com:alex/notes.git (fetch)\nvault\tgit@github.com:alex/notes.git (push)\n'
    // The slipped commit is already on the private vault remote but not on
    // public origin: the old `--not --remotes` hid it.
    const log = (a: string) =>
      a.includes('--remotes=origin') && a.includes(' feature ') ? 'docs/work/backlog-sweep/work.md\n' : ''
    const { w, clock } = world(on, { remotes, log, answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'feature', '--not', '--remotes=origin', '--'])
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('docs/work/backlog-sweep/work.md')
    // The same ref to the private remote passes without a dialog: GitHub
    // says the vault's repo is private.
    expect(w.argv).toContainEqual(['gh', 'repo', 'view', 'github.com/alex/notes', '--json', 'isPrivate,url'])
    await $.tool.call(bash('git push vault feature'))
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git push vault feature'])
  })

  test('push: a bare push reads where git says the branch pushes', async ($, on) => {
    const { w } = world(on, { log: () => '' })
    await $.tool.call(bash('git push'))
    expect(w.argv).toContainEqual(['git', 'for-each-ref', '--format=%(push:remotename)', 'refs/heads/feature'])
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'HEAD', '--not', '--remotes=origin', '--'])
    expect(w.ran).toEqual(['git push'])
  })

  test('push: a bare push reads git\'s push settings; push.default=matching asks', async ($, on) => {
    const { w, clock } = world(on, { config: { 'push.default': ['matching\n', 0] }, answer: "Don't run it" })
    const call = $.tool.call(bash('git push'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv).toContainEqual(['git', 'config', '--get-all', 'remote.origin.push'])
    expect(w.argv).toContainEqual(['git', 'config', '--get', 'push.default'])
    expect(w.argv.some(a => a[1] === 'log')).toBe(false)
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('push.default=matching')
  })

  test('push: remote.origin.push stands in for the refspec', async ($, on) => {
    const { w } = world(on, { config: { 'remote.origin.push': ['refs/heads/release:refs/heads/release\n', 0] }, log: () => '' })
    await $.tool.call(bash('git push'))
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'refs/heads/release', '--not', '--remotes=origin', '--'])
    expect(w.ran).toEqual(['git push'])
  })

  test('push: push.default=simple keeps the HEAD plan; a push with a refspec reads no push settings', async ($, on) => {
    const { w } = world(on, { config: { 'push.default': ['simple\n', 0] }, log: () => '' })
    await $.tool.call(bash('git push'))
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'HEAD', '--not', '--remotes=origin', '--'])
    const before = w.argv.length
    await $.tool.call(bash('git push origin feature'))
    expect(w.argv.slice(before).some(a => a[1] === 'config')).toBe(false)
    expect(w.ran).toEqual(['git push', 'git push origin feature'])
  })

  test('push: a bare push to a mirror remote asks', async ($, on) => {
    const { w, clock } = world(on, { config: { 'remote.origin.mirror': ['true\n', 0] }, answer: "Don't run it" })
    const call = $.tool.call(bash('git push'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv).toContainEqual(['git', 'config', '--type=bool', '--get', 'remote.origin.mirror'])
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('this remote is a mirror')
  })

  test('push: mirror false, or tracking, keeps the HEAD plan', async ($, on) => {
    const config: Record<string, [string, number]> = {
      'remote.origin.mirror': ['false\n', 0],
      'push.default': ['tracking\n', 0],
    }
    const { w } = world(on, { config, log: () => '' })
    await $.tool.call(bash('git push'))
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'HEAD', '--not', '--remotes=origin', '--'])
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push'])
  })

  test('push: a mirror setting git cannot read as a bool asks', async ($, on) => {
    const { w, clock } = world(on, { config: { 'remote.origin.mirror': ['', 128] }, answer: "Don't run it" })
    const call = $.tool.call(bash('git push'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
  })

  test('push: a cut config read is unreadable and asks', async ($, on) => {
    const config: Record<string, [string, number, boolean]> = { 'remote.origin.push': ['refs/heads/release\n', 0, true] }
    const { w, clock } = world(on, { config, answer: "Don't run it" })
    const call = $.tool.call(bash('git push'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
    expect(r.deny).toContain("could not read git's push settings")
  })

  test('push: -c on a push asks without reading config', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    const call = $.tool.call(bash('git -c url.git@github.com:alex/Kerd.git.insteadOf=/srv/vault push origin'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('sets git config for this push only')
  })

  test('git add -f --pathspec-from-file: the ignored files are listed from the root and .env is named', async ($, on) => {
    const { w, clock } = world(on, { ignored: '.env\0', answer: "Don't run it" })
    const call = $.tool.call(bash('git add -f --pathspec-from-file=paths.txt'))
    await clock.advance(5_000)
    await call
    const ls = w.argv.find(a => a[1] === 'ls-files')
    expect(ls).toEqual(['git', 'ls-files', '-z', '--others', '--ignored', '--exclude-standard', '--full-name'])
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('.env')
    expect(w.ran).toEqual([])
  })

  test('push: git\'s push settings unreadable asks', async ($, on) => {
    const { w, clock } = world(on, { config: { 'push.default': ['', 3] }, answer: "Don't run it" })
    const call = $.tool.call(bash('git push'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
    expect(r.deny).toContain("could not read git's push settings")
  })

  for (const command of ['git add -f .', 'git add --force .']) {
    test(`${command}: the ignored .env is listed, named in the dialog, and refused`, async ($, on) => {
      const { w, clock } = world(on, { ignored: '.env\0', answer: "Don't run it" })
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.argv).toContainEqual([
        'git', 'ls-files', '-z', '--others', '--ignored', '--exclude-standard', '--full-name', '--', '.',
      ])
      expect(w.asked).toHaveLength(1)
      expect(w.asked[0]).toContain('.env')
      expect(r.deny).toContain('.env (kept out of Git by instruction)')
      expect(w.ran).toEqual([])
    })
  }

  test('add -f: a failed ignored listing asks and says the list may be incomplete', async ($, on) => {
    const { w, clock } = world(on, { ignored: 'fail', answer: 'never' })
    const call = $.tool.call(bash('git add -f README.md'))
    await clock.settle()
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('may be incomplete')
    const ui = await $.ui.mount({
      plugin: 'overtone',
      surface: 'terminal',
      component: 'AbovePrompt',
      props: { hasSurvey: false, isWorking: true, maxRows: 20, bodyColumns: 200 } as never,
    })
    expect(await ui.find({ type: 'Text', text: /may be incomplete/ })).toBeDefined()
    await ui.unmount()
    await clock.advance(30_000)
    await call
    expect(w.ran).toEqual([])
  })

  test('add -f by name with nothing ignored passes without a dialog', async ($, on) => {
    const { w } = world(on, { ignored: '' })
    await $.tool.call(bash('git add -f README.md'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git add -f README.md'])
  })

  test('push: a target the guard cannot read asks', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    const call = $.tool.call(bash('git push "$REMOTE" main'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
    expect(r.deny).toContain('shell expansion')
  })

  test('a shell expansion in a path asks: git add -f "$(printf .env)"', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    const call = $.tool.call(bash('git add -f "$(printf .env)"'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
  })

  test('timeout, then a late "Run it": refused, nothing runs, the deny says the dialog may linger', async ($, on) => {
    const { w, clock } = world(on, { answer: 'Run it', answerAfterMs: 45_000 })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(30_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('no answer in 30 s')
    expect(r.deny).toContain('no way to close it')
    expect(r.deny).toContain('runs nothing')
    expect(w.logs.some(l => l.includes('refused after 30 s'))).toBe(true)
    // The dialog answers late.
    await clock.advance(20_000)
    await clock.settle()
    expect(w.ran).toEqual([])
  })

  test('a downstream rejection after a pass: the command ran once, never replayed', async ($, on) => {
    const { w } = world(on, { bashThrows: true })
    const r = await $.tool.call(bash('git add README.md')).then(
      v => ({ v }),
      (err: unknown) => ({ err }),
    )
    expect(w.ran).toEqual(['git add README.md'])
    expect('err' in r).toBe(true)
  })

  test('a downstream rejection after "Run it": ran once, never replayed', async ($, on) => {
    const { w, clock } = world(on, { bashThrows: true })
    const call = $.tool.call(bash('git add -A')).then(
      v => ({ v }),
      (err: unknown) => ({ err }),
    )
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git add -A'])
  })

  test('a downstream rejection on a git command that stages nothing: ran once', async ($, on) => {
    const { w } = world(on, { bashThrows: true })
    await $.tool.call(bash('git status')).catch(() => undefined)
    expect(w.ran).toEqual(['git status'])
  })

  test('a downstream rejection on a command with no git: ran once', async ($, on) => {
    const { w } = world(on, { bashThrows: true })
    await $.tool.call(bash('ls')).catch(() => undefined)
    expect(w.ran).toEqual(['ls'])
  })

  // Each test below names its own repo: GitHub's answers are kept for the
  // session, so a repo another test asked about could already be known.
  const ghCalls = (w: World, repo: string) => w.argv.filter(a => a[1] === 'repo' && a[3] === `github.com/${repo}`)

  test('a private GitHub repo with a private path staged passes, no question', async ($, on) => {
    const url = 'git@github.com:alex/ledger.git'
    const gh = { 'github.com/alex/ledger': ghSays('alex/ledger', true) }
    // gh is not on the hook's PATH here: found under /opt/homebrew/bin.
    const { w } = world(on, { remotes: remotesOf(url), gh, ghAt: '/opt/homebrew/bin/gh' })
    await $.tool.call(bash('git add -A && git commit -m wip'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git add -A && git commit -m wip'])
    expect(ghCalls(w, 'alex/ledger').map(a => a[0])).toEqual(['gh', '/opt/homebrew/bin/gh'])
  })

  test('isPrivate false: asks as before, naming the repo public', async ($, on) => {
    const url = 'git@github.com:alex/open-one.git'
    const gh = { 'github.com/alex/open-one': ghSays('alex/open-one', false) }
    const { w, clock } = world(on, { remotes: remotesOf(url), gh, answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('toward public github.com/alex/open-one.')
    expect(w.ran).toEqual([])
  })

  test('gh fails: asks, saying it could not confirm the repo is private; a failure is asked again', async ($, on) => {
    const url = 'git@github.com:alex/unknown-one.git'
    const { w, clock } = world(on, { remotes: remotesOf(url), ghAt: 'none', answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(ghCalls(w, 'alex/unknown-one').map(a => a[0])).toEqual(['gh', '/opt/homebrew/bin/gh', '/usr/local/bin/gh'])
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('toward github.com/alex/unknown-one (the guard could not confirm it is private).')
    expect(w.asked[0]).not.toContain('public github.com')
    expect(r.deny).toContain('could not confirm it is private')
    expect(w.ran).toEqual([])
    // gh found but failing (not signed in): unconfirmed too, and not kept.
    w.ghAt = 'gh'
    const again = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    await again
    expect(ghCalls(w, 'alex/unknown-one')).toHaveLength(4)
    expect(w.asked).toHaveLength(2)
    expect(w.asked[1]).toContain('could not confirm it is private')
  })

  test('gh not at the first path: the next path is tried', async ($, on) => {
    const url = 'git@github.com:alex/found-later.git'
    const gh = { 'github.com/alex/found-later': ghSays('alex/found-later', true) }
    const { w } = world(on, { remotes: remotesOf(url), gh, ghAt: '/usr/local/bin/gh' })
    await $.tool.call(bash('git add -A'))
    expect(ghCalls(w, 'alex/found-later').map(a => a[0])).toEqual(['gh', '/opt/homebrew/bin/gh', '/usr/local/bin/gh'])
    expect(w.asked).toEqual([])
  })

  test('GitHub does not answer in time: no second path, and the words say why', async ($, on) => {
    const url = 'git@github.com:alex/notes-slow.git'
    const gh = { 'github.com/alex/notes-slow': ghSays('alex/notes-slow', true) }
    const { w, clock } = world(on, { remotes: remotesOf(url), gh, ghHangsAt: ['gh'], answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000) // gh gives up
    await clock.advance(5_000) // the person answers
    const r = (await call) as { deny?: string }
    // The same gh at /opt/homebrew/bin would only wait again: never tried.
    expect(ghCalls(w, 'alex/notes-slow').map(a => a[0])).toEqual(['gh'])
    const slow =
      'toward github.com/alex/notes-slow (GitHub did not answer within 5 s, so the guard could not confirm it is private)'
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain(slow)
    expect(r.deny).toContain(slow)
    expect(w.ran).toEqual([])
    // Not kept: GitHub is asked again next time, and its answer counts.
    w.ghHangsAt = []
    await $.tool.call(bash('git add -A'))
    expect(ghCalls(w, 'alex/notes-slow')).toHaveLength(2)
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git add -A'])
  })

  test('gh fails another way: old words, not the timeout ones', async ($, on) => {
    const url = 'git@github.com:alex/not-signed-in.git'
    // gh answers exit 1 (not signed in): the repo is not in the answers.
    const { w, clock } = world(on, { remotes: remotesOf(url), answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked[0]).toContain('toward github.com/alex/not-signed-in (the guard could not confirm it is private).')
    expect(w.asked[0]).not.toContain('did not answer')
    expect(r.deny).toContain('(the guard could not confirm it is private)')
    expect(r.deny).not.toContain('did not answer')
  })

  // A rejection that came back fast is a gh that is not there.
  test('a fast rejection reads as not there: the next path is tried', async ($, on) => {
    const url = 'git@github.com:alex/fast-fail.git'
    const gh = { 'github.com/alex/fast-fail': ghSays('alex/fast-fail', true) }
    const { w } = world(on, { remotes: remotesOf(url), gh, ghAt: '/usr/local/bin/gh', ghHangsAt: ['gh'], ghTakesMs: 0 })
    await $.tool.call(bash('git add -A'))
    expect(ghCalls(w, 'alex/fast-fail').map(a => a[0])).toEqual(['gh', '/opt/homebrew/bin/gh', '/usr/local/bin/gh'])
    expect(w.asked).toEqual([])
  })

  test("GitHub's answer is kept: gh is asked once per URL across two commands", async ($, on) => {
    const url = 'git@github.com:alex/cached-one.git'
    const gh = { 'github.com/alex/cached-one': ghSays('alex/cached-one', true) }
    const { w } = world(on, { remotes: remotesOf(url), gh })
    await $.tool.call(bash('git add -A && git commit -m one'))
    await $.tool.call(bash('git add -A && git commit -m two'))
    expect(ghCalls(w, 'alex/cached-one')).toHaveLength(1)
    expect(w.asked).toEqual([])
    expect(w.ran).toHaveLength(2)
  })

  test('GH_HOST or a moved repo: an answer for another url is not taken, and it asks', async ($, on) => {
    const url = 'git@github.com:alex/elsewhere.git'
    const gh = { 'github.com/alex/elsewhere': ['{"isPrivate":true,"url":"https://ghe.example.test/alex/elsewhere"}\n', 0] as [string, number] }
    const { w, clock } = world(on, { remotes: remotesOf(url), gh, answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    await call
    // The host is named in the question, not left to GH_HOST.
    expect(ghCalls(w, 'alex/elsewhere')).toEqual([
      ['gh', 'repo', 'view', 'github.com/alex/elsewhere', '--json', 'isPrivate,url'],
    ])
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('could not confirm it is private')
    expect(w.ran).toEqual([])
  })

  // A "github" URL the strict parser does not read: asks unconfirmed, and gh
  // is never asked (so never kept), even when it would say private.
  const loose: [string, string][] = [
    ['a host that only mentions github.com', 'https://example.test/github.com/alex/ledger'],
    ['ssh with a port', 'ssh://git@github.com:22/alex/ledger.git'],
    ['http://', 'http://github.com/alex/ledger.git'],
  ]
  for (const [what, url] of loose) {
    test(`${what}: asks, could not confirm it is private, gh never asked`, async ($, on) => {
      const gh = { 'github.com/alex/ledger': ghSays('alex/ledger', true) }
      const { w, clock } = world(on, { remotes: remotesOf(url), gh, answer: "Don't run it" })
      const call = $.tool.call(bash('git add -A'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.argv.some(a => a[1] === 'repo')).toBe(false)
      expect(w.asked).toHaveLength(1)
      expect(w.asked[0]).toContain(`toward ${url} (the guard could not confirm it is private).`)
      expect(r.deny).toContain('could not confirm it is private')
      expect(w.ran).toEqual([])
    })
  }

  test('a remote with no "github" in it passes as before, gh never asked', async ($, on) => {
    const { w } = world(on, { remotes: remotesOf('https://gitlab.example.test/o/r.git') })
    await $.tool.call(bash('git add -A'))
    expect(w.argv.some(a => a[1] === 'repo')).toBe(false)
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git add -A'])
  })

  test('a new docs/work/<slug>/ in a public repo without kivna/vault.json: no new-folder hit', async ($, on) => {
    const { w } = world(on, { status: '?? docs/work/fresh/work.md\0', files: {}, committed: null })
    await $.tool.call(bash('git add -A'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git add -A'])
  })

  const trees: [string, Record<string, string>][] = [
    ['deleted', {}],
    ['changed', { [VAULT_JSON]: '{"work_notes": "repo"}' }],
    ['broken', { [VAULT_JSON]: '{oops' }],
  ]
  for (const [how, files] of trees) {
    test(`kivna/vault.json ${how} in the working tree while HEAD declares it: the hit stands`, async ($, on) => {
      const { w, clock } = world(on, { status: '?? docs/work/fresh/work.md\0', files, answer: "Don't run it" })
      const call = $.tool.call(bash('git add -A'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.argv).toContainEqual(['git', 'show', 'HEAD:kivna/vault.json'])
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain('docs/work/fresh/work.md (new work folder docs/work/fresh/')
      expect(w.ran).toEqual([])
    })
  }

  test('only the working tree declares it (not yet committed): the hit stands', async ($, on) => {
    const { w, clock } = world(on, { status: '?? docs/work/fresh/work.md\0', committed: null, answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
  })

  test('with kivna/vault.json "work_notes": "vault": the new-folder hit as before', async ($, on) => {
    const { w, clock } = world(on, { status: '?? docs/work/fresh/work.md\0', answer: "Don't run it" })
    const call = $.tool.call(bash('git add -A'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('docs/work/fresh/work.md (new work folder docs/work/fresh/')
    expect(w.ran).toEqual([])
  })

  test('an invalid kivna/vault.json that speaks of work_notes: asks (fail closed)', async ($, on) => {
    const { w, clock } = world(on, {
      status: ' M README.md\0',
      files: { [VAULT_JSON]: '{"work_notes": "vault"' },
      committed: null,
      answer: "Don't run it",
    })
    const call = $.tool.call(bash('git add README.md'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('kivna/vault.json (the guard could not read where kivna/vault.json puts the private vault')
    expect(w.ran).toEqual([])
  })

  test('an invalid kivna/vault.json that says nothing of work_notes: no vault rule, no ask', async ($, on) => {
    const { w } = world(on, { status: '?? docs/work/fresh/work.md\0', files: { [VAULT_JSON]: '{oops' }, committed: null })
    await $.tool.call(bash('git add -A'))
    await $.tool.call(bash('git add ~/notes/vault/kerd/work/x.md'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git add -A', 'git add ~/notes/vault/kerd/work/x.md'])
  })

  test('the vault path kivna/vault.json names is guarded; the deny names where notes go', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    const call = $.tool.call(bash('git add ~/notes/vault/kerd/work/x.md'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('~/notes/vault/kerd/work/x.md (inside the private vault)')
    expect(r.deny).toContain('(notes:<work>/, under ~/notes/vault/kerd/work/)')
    expect(w.ran).toEqual([])
  })

  test('a vault elsewhere in kivna/vault.json: that path asks, the other passes', async ($, on) => {
    const text = '{"vault": "/srv/vault", "folder": "proj", "work_notes": "vault"}'
    const { w, clock } = world(on, { files: { [VAULT_JSON]: text }, committed: text, answer: "Don't run it" })
    await $.tool.call(bash('git add ~/notes/vault/kerd/work/x.md'))
    expect(w.asked).toEqual([])
    const call = $.tool.call(bash('git add /srv/vault/proj/work/a.md'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('under /srv/vault/proj/work/)')
    expect(w.ran).toEqual(['git add ~/notes/vault/kerd/work/x.md'])
  })

  test('no kivna/vault.json: no vault rule', async ($, on) => {
    const { w } = world(on, { files: {}, committed: null })
    await $.tool.call(bash('git add ~/notes/vault/kerd/work/x.md'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git add ~/notes/vault/kerd/work/x.md'])
  })

  test('the vault reached through its link target is the vault', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    on('fs.stat', ($, e) => {
      if (e.path !== '/Users/alex/notes/vault') throw new Error('ENOENT')
      return { value: { kind: 'dir', size: 0, mtimeMs: 0, isLink: true, realPath: '/Users/alex/code/notes/vault' } } as never
    })
    const call = $.tool.call(bash('git add /Users/alex/code/notes/vault/kerd/work/x.md'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
  })

  // The reviewer's bypass: a repo's own vault.json naming a vault that holds
  // the repo (or home, or a relative path) once turned every check off.
  for (const v of ['~', '/Users/alex', '/Users/alex/code', '.', '..']) {
    test(`kivna/vault.json "vault": "${v}": git add .env still asks`, async ($, on) => {
      const text = JSON.stringify({ vault: v, work_notes: 'vault' })
      const { w, clock } = world(on, { status: '?? .env\0', files: { [VAULT_JSON]: text }, committed: text, answer: "Don't run it" })
      const call = $.tool.call(bash('git add .env'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain('.env (kept out of Git by instruction)')
      expect(w.ran).toEqual([])
    })
  }

  test('kivna/vault.json private_paths: a listed path asks; deleting the list in the same change does not undo it', async ($, on) => {
    const { w, clock } = world(on, { status: '?? kerd-laptop-result.patch\0', files: {}, answer: "Don't run it" })
    const call = $.tool.call(bash('git add kerd-laptop-result.patch'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('kerd-laptop-result.patch (kept out of Git by instruction)')
  })

  test('without private_paths, a Kerd file name is an ordinary file', async ($, on) => {
    const text = '{"vault": "~/notes/vault"}'
    const { w } = world(on, { status: '?? kerd-laptop-result.patch\0', files: { [VAULT_JSON]: text }, committed: text })
    await $.tool.call(bash('git add kerd-laptop-result.patch'))
    expect(w.asked).toEqual([])
  })

  test('the vault_path setting: guarded in a repo with no kivna/vault.json', { options: { vault_path: '~/mine/vault' } }, async ($, on) => {
    const { w, clock } = world(on, { files: {}, committed: null, answer: "Don't run it" })
    const call = $.tool.call(bash('git add ~/mine/vault/x.md'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('~/mine/vault/x.md (inside the private vault)')
    expect(r.deny).toContain('under ~/mine/vault/)')
    await $.tool.call(bash('git add README.md'))
    expect(w.ran).toEqual(['git add README.md'])
  })

  test('the vault_path setting holds in text mode too', { options: { vault_path: '/srv/mine' } }, async ($, on) => {
    const { w, clock } = world(on, { noProcess: true, files: {}, answer: "Don't run it" })
    const call = $.tool.call(bash('git add /srv/mine/x.md'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
  })

  test('a vault named by its link target still catches a path spelled through the link', { options: { vault_path: '/Volumes/data/vault' } }, async ($, on) => {
    const { w, clock } = world(on, { files: {}, committed: null, answer: "Don't run it" })
    on('fs.stat', ($, e) => {
      if (e.path !== '/Users/alex/notes/vault/kerd') throw new Error('ENOENT')
      return { value: { kind: 'dir', size: 0, mtimeMs: 0, isLink: false, realPath: '/Volumes/data/vault/kerd' } } as never
    })
    const call = $.tool.call(bash('git add ~/notes/vault/kerd/x.md'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual([])
  })

  test("text mode (no process): the session project's kivna/vault.json names the vault", async ($, on) => {
    const { w, clock } = world(on, { noProcess: true, answer: "Don't run it" })
    const call = $.tool.call(bash('git add ~/notes/vault/kerd/work/x.md'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    w.files = {}
    await $.tool.call(bash('git add ~/notes/vault/kerd/work/y.md'))
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git add ~/notes/vault/kerd/work/y.md'])
  })

  test("GitHub's private answer expires after 5 minutes; a public one is kept", async ($, on) => {
    const url = 'git@github.com:alex/expiring.git'
    const open = 'git@github.com:alex/stays-open.git'
    const gh = {
      'github.com/alex/expiring': ghSays('alex/expiring', true),
      'github.com/alex/stays-open': ghSays('alex/stays-open', false),
    }
    const { w, clock } = world(on, { remotes: remotesOf(url) + `other\t${open} (push)\n`, gh, status: ' M README.md\0' })
    await $.tool.call(bash('git add README.md'))
    expect(ghCalls(w, 'alex/expiring')).toHaveLength(1)
    await clock.advance(4 * 60_000)
    await $.tool.call(bash('git add README.md'))
    expect(ghCalls(w, 'alex/expiring')).toHaveLength(1)
    await clock.advance(60_000)
    await $.tool.call(bash('git add README.md'))
    expect(ghCalls(w, 'alex/expiring')).toHaveLength(2)
    expect(ghCalls(w, 'alex/stays-open')).toHaveLength(1)
    expect(w.ran).toHaveLength(3)
  })

  // A mirror remote that GitHub says is public, beside Kerd's origin.
  const MIRROR = 'git@github.com:someone/kerd-mirror.git'
  const WITH_MIRROR = REMOTES + `mirror\t${MIRROR} (fetch)\nmirror\t${MIRROR} (push)\n`

  test("push mirror topic:release: release's own committed vault.json decides, not mirror/HEAD", async ($, on) => {
    // release declares vault notes; mirror's HEAD branch does not; the source
    // deletes kivna/vault.json and adds a new work folder.
    const committed = (base: string) => (base === 'refs/remotes/mirror/release' ? VAULT_TEXT : null)
    const log = () => 'docs/work/fresh/work.md\nkivna/vault.json\n'
    const { w, clock } = world(on, { remotes: WITH_MIRROR, committed, files: {}, log, answer: "Don't run it" })
    const call = $.tool.call(bash('git push mirror topic:release'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv).toContainEqual(['git', 'ls-tree', '-d', '--name-only', '-z', 'refs/remotes/mirror/release', 'docs/work/'])
    expect(w.argv).toContainEqual(['git', 'show', 'refs/remotes/mirror/release:kivna/vault.json'])
    expect(w.argv.some(a => a[1] === 'ls-tree' && a[5] !== 'refs/remotes/mirror/release')).toBe(false)
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('public github.com/someone/kerd-mirror')
    expect(r.deny).toContain('docs/work/fresh/work.md (new work folder docs/work/fresh/')
    expect(w.ran).toEqual([])
  })

  test('a destination with no readable base: a work folder it carries asks, nothing else does', async ($, on) => {
    const { w, clock } = world(on, {
      remotes: WITH_MIRROR,
      missingBases: ['refs/remotes/mirror/newbranch'],
      log: () => 'docs/work/fresh/work.md\n',
      answer: "Don't run it",
    })
    const call = $.tool.call(bash('git push mirror topic:newbranch'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('cannot tell whether this work folder is new')
    // No other branch stands in for it.
    expect(w.argv.some(a => a[1] === 'ls-tree' && /HEAD|@\{u\}/.test(a[5]!))).toBe(false)
    // The same push carrying no work folder passes.
    w.log = () => 'README.md\n'
    await $.tool.call(bash('git push mirror topic:newbranch'))
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git push mirror topic:newbranch'])
  })

  test('git push origin HEAD reads the current branch; main:HEAD has no base and asks on a work folder', async ($, on) => {
    const { w, clock } = world(on, { log: () => 'docs/work/fresh/work.md\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin HEAD'))
    await clock.advance(5_000)
    await call
    expect(w.argv).toContainEqual(['git', 'ls-tree', '-d', '--name-only', '-z', 'refs/remotes/origin/feature', 'docs/work/'])
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).not.toContain('cannot tell')
    const before = w.argv.length
    const again = $.tool.call(bash('git push origin main:HEAD'))
    await clock.advance(5_000)
    const r = (await again) as { deny?: string }
    expect(w.argv.slice(before).some(a => a[1] === 'ls-tree')).toBe(false)
    expect(w.asked).toHaveLength(2)
    expect(r.deny).toContain('cannot tell whether this work folder is new')
  })

  test('fetch private, pushurl public: asks, naming the push URL', async ($, on) => {
    const FETCH = 'git@github.com:alex/ledger.git'
    const PUSH = 'git@github.com:someone/open.git'
    const gh = {
      'github.com/alex/ledger': ghSays('alex/ledger', true),
      'github.com/someone/open': ghSays('someone/open', false),
    }
    const remotes = `origin\t${FETCH} (fetch)\norigin\t${PUSH} (push)\n`
    const { w, clock } = world(on, { remotes, gh, log: () => 'README.md\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv.some(a => a[1] === 'log')).toBe(false)
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('toward public github.com/someone/open.')
    expect(r.deny).toContain('not the repository it fetches from')
  })

  test('a force push with a work path asks; without one it passes', async ($, on) => {
    const { w, clock } = world(on, { log: () => 'docs/work/jev-trial/plan.md\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push --force-with-lease origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('docs/work/jev-trial/plan.md')
    w.log = () => 'README.md\n'
    await $.tool.call(bash('git push -f origin feature'))
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git push -f origin feature'])
  })

  test('git log failed or cut: a guarded push asks, saying it could not list the files', async ($, on) => {
    const { w, clock } = world(on, { logCut: true, log: () => 'README.md\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('could not list the files this push publishes')
    expect(r.deny).toContain('could not list the files this push publishes')
    w.logCut = false
    w.logExit = 128
    const again = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    await again
    expect(w.asked).toHaveLength(2)
    expect(w.ran).toEqual([])
  })

  test('live remote equals the tracking ref: the range is unchanged', async ($, on) => {
    const { w } = world(on, { log: () => 'README.md\n' })
    await $.tool.call(bash('git push origin feature'))
    expect(w.argv).toContainEqual(['git', 'ls-remote', 'git@github.com:alex/Kerd.git', 'refs/heads/feature'])
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'feature', '--not', '--remotes=origin', '--'])
    expect(w.argv.some(a => a[1] === 'cat-file')).toBe(false)
    expect(w.ran).toEqual(['git push origin feature'])
  })

  test('the remote was rewound to a commit here: the range uses the live commit and catches .env', async ($, on) => {
    const REWOUND = 'b'.repeat(40)
    // The tracking ref still holds the commit that added .env; the remote
    // no longer has it, so the push republishes it.
    const log = (a: string) => (a.includes(REWOUND) ? '.env\nREADME.md\n' : 'README.md\n')
    const { w, clock } = world(on, { live: () => REWOUND, commits: [OID_TRACKED, REWOUND], log, answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv).toContainEqual([
      'git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'feature', '--not', REWOUND, '--exclude=origin/feature', '--remotes=origin', '--',
    ])
    expect(w.argv).toContainEqual(['git', 'ls-tree', '-d', '--name-only', '-z', REWOUND, 'docs/work/'])
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('.env (kept out of Git by instruction)')
    expect(w.ran).toEqual([])
  })

  test('the remote moved to a commit this clone does not have: asks, reads no log', async ($, on) => {
    const { w, clock } = world(on, { live: () => 'c'.repeat(40), answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv.some(a => a[1] === 'log')).toBe(false)
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('toward public github.com/alex/Kerd.')
    expect(r.deny).toContain('which this clone does not have')
  })

  test('git ls-remote failed or cut: asks', async ($, on) => {
    const { w, clock } = world(on, { live: 'fail', answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('git ls-remote failed')
    w.live = 'cut'
    const again = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    await again
    expect(w.asked).toHaveLength(2)
    expect(w.ran).toEqual([])
  })

  // A throw or timeout in the live reads or the log fails closed: a plain
  // push asks, never falls to the text-only pass.
  const thrown: [string, Partial<World>, string][] = [
    ['rev-parse -q --verify', {}, "could not read this clone's tracking ref"],
    ['cat-file', { live: () => 'b'.repeat(40) }, 'could not check whether this clone has'],
    ['log', {}, 'could not list the files this push publishes'],
  ]
  for (const [sub, over, says] of thrown) {
    test(`a thrown git ${sub} on a plain push asks`, async ($, on) => {
      const { w, clock } = world(on, { ...over, throws: [sub], log: () => 'README.md\n', answer: "Don't run it" })
      const call = $.tool.call(bash('git push origin feature'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.logs.some(l => l.includes('text only'))).toBe(false)
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain(says)
      expect(w.ran).toEqual([])
    })
  }

  // Every other push-path read fails closed too. %(push:remotename) and
  // %(push) are read only for a bare push, so those two use `git push`.
  const pushReads: [string, string, string][] = [
    ['remote -v', 'git push origin feature', "could not read the repo's remotes"],
    ['symbolic-ref -q HEAD', 'git push origin feature', 'could not read the current branch'],
    ['for-each-ref --format=%(push:remotename)', 'git push', 'could not read which remote this branch pushes to'],
    ['for-each-ref --format=%(push)', 'git push', 'could not read which branch this push updates'],
  ]
  for (const [read, command, says] of pushReads) {
    test(`a thrown git ${read} on \`${command}\` asks`, async ($, on) => {
      const { w, clock } = world(on, { throws: [read], log: () => 'README.md\n', answer: "Don't run it" })
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.logs.some(l => l.includes('text only'))).toBe(false)
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain(says)
      expect(w.ran).toEqual([])
    })
  }

  // A failed or cut answer from a read that decides where the push goes is
  // not a read: asks. Exit 1 from symbolic-ref is a detached HEAD, and an
  // empty %(push:remotename) is no push remote configured: both as before.
  const badAnswers: [string, string, [string, number, boolean], string][] = [
    ['remote -v', 'git push origin feature', ['', 128, false], "could not read the repo's remotes"],
    ['remote -v', 'git push origin feature', [REMOTES, 0, true], "could not read the repo's remotes"],
    ['symbolic-ref -q HEAD', 'git push origin feature', ['', 128, false], 'could not read the current branch'],
    ['symbolic-ref -q HEAD', 'git push origin feature', ['refs/heads/fea', 0, true], 'could not read the current branch'],
    ['for-each-ref --format=%(push:remotename)', 'git push', ['', 128, false], 'could not read which remote this branch pushes to'],
    ['for-each-ref --format=%(push:remotename)', 'git push', ['ori', 0, true], 'could not read which remote this branch pushes to'],
    ['for-each-ref --format=%(push)', 'git push', ['', 128, false], 'could not read which branch this push updates'],
    ['for-each-ref --format=%(push)', 'git push', ['refs/remotes/or', 0, true], 'could not read which branch this push updates'],
  ]
  for (const [read, command, answer, says] of badAnswers) {
    test(`git ${read} exit ${answer[1]}${answer[2] ? ', cut' : ''} on \`${command}\` asks`, async ($, on) => {
      const { w, clock } = world(on, { answers: { [read]: answer }, log: () => 'README.md\n', answer: "Don't run it" })
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain(says)
      expect(w.ran).toEqual([])
    })
  }

  test('symbolic-ref exit 1 is a detached HEAD, and an empty push remote is none configured: both pass as before', async ($, on) => {
    const { w } = world(on, { answers: { 'symbolic-ref -q HEAD': ['', 1, false] }, log: () => 'README.md\n' })
    await $.tool.call(bash('git push origin feature'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push origin feature'])
    w.answers = { 'for-each-ref --format=%(push:remotename)': ['\n', 0, false] }
    await $.tool.call(bash('git push'))
    // No push remote named: `origin`, read as before.
    expect(w.argv).toContainEqual(['git', 'ls-remote', 'git@github.com:alex/Kerd.git', 'refs/heads/feature'])
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push origin feature', 'git push'])
  })

  // The base-tree reads leave the base unknown: a work folder the push
  // carries asks (even one the remote has); a push without one passes.
  for (const read of ['ls-tree', 'show']) {
    test(`a thrown git ${read} of the base on \`git push origin feature\`: unknown base, asks on a work folder`, async ($, on) => {
      const { w, clock } = world(on, { throws: [read], log: () => 'docs/work/jev-trial/plan.md\n', answer: "Don't run it" })
      const call = $.tool.call(bash('git push origin feature'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.logs.some(l => l.includes('text only'))).toBe(false)
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain('cannot tell whether this work folder is new')
      w.log = () => 'README.md\n'
      await $.tool.call(bash('git push origin feature'))
      expect(w.asked).toHaveLength(1)
      expect(w.ran).toEqual(['git push origin feature'])
    })
  }

  test('add and commit keep the text-only fallback when a base read throws', async ($, on) => {
    const { w } = world(on, { throws: ['ls-tree'] })
    await $.tool.call(bash('git add README.md'))
    expect(w.logs.some(l => l.includes('text only'))).toBe(true)
    expect(w.ran).toEqual(['git add README.md'])
  })

  test('the pushurl is read live, not the remote name or its fetch URL', async ($, on) => {
    const FETCH = 'git@github.com:alex/Kerd.git'
    const PUSH = 'https://github.com/alex/Kerd'
    const gh = { 'github.com/alex/Kerd': ghSays('alex/Kerd', false) }
    const remotes = `origin\t${FETCH} (fetch)\norigin\t${PUSH} (push)\n`
    const { w } = world(on, { remotes, gh, log: () => 'README.md\n' })
    await $.tool.call(bash('git push origin feature'))
    expect(w.argv.filter(a => a[1] === 'ls-remote').map(a => a[2])).toEqual([PUSH])
    expect(w.ran).toEqual(['git push origin feature'])
  })

  test('a tag push has no base: a work folder it carries asks', async ($, on) => {
    const { w, clock } = world(on, { remotes: WITH_MIRROR, log: () => 'docs/work/fresh/work.md\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push mirror tag v1.0'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv.some(a => a[1] === 'ls-tree')).toBe(false)
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('cannot tell whether this work folder is new')
  })

  test("a bare push reads the branch git says it updates (@{push})", async ($, on) => {
    const { w } = world(on, { log: () => '' })
    await $.tool.call(bash('git push'))
    expect(w.argv).toContainEqual(['git', 'for-each-ref', '--format=%(push)', 'refs/heads/feature'])
    expect(w.argv).toContainEqual(['git', 'ls-tree', '-d', '--name-only', '-z', 'refs/remotes/origin/feature', 'docs/work/'])
    expect(w.ran).toEqual(['git push'])
  })

  test("an opaque push to the mirror names mirror's URL, not origin's", async ($, on) => {
    const config: Record<string, [string, number]> = { 'remote.mirror.mirror': ['true\n', 0] }
    const { w, clock } = world(on, { remotes: WITH_MIRROR, config, answer: "Don't run it" })
    const call = $.tool.call(bash('git push mirror'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('toward public github.com/someone/kerd-mirror.')
    expect(w.asked[0]).not.toContain('alex/Kerd')
    expect(r.deny).toContain('this remote is a mirror')
  })

  test('a push target the guard cannot resolve names no remote', async ($, on) => {
    const { w, clock } = world(on, { remotes: WITH_MIRROR, answer: "Don't run it" })
    const call = $.tool.call(bash('git push "$R" main'))
    await clock.advance(5_000)
    await call
    expect(w.asked[0]).toContain('toward a destination the guard could not resolve.')
    expect(w.asked[0]).not.toContain('github.com/')
  })

  test('the evidence draws in the band while the dialog waits, no hotkeys', async ($, on) => {
    const { w, clock } = world(on, { answer: 'never' })
    const call = $.tool.call(bash('git add -A'))
    await clock.settle()
    for (const surface of ['terminal', 'desktop'] as const) {
      const ui = await $.ui.mount({
        plugin: 'overtone',
        surface,
        component: 'AbovePrompt',
        props: { hasSurvey: false, isWorking: true, maxRows: 20, bodyColumns: 120 } as never,
      })
      expect(await ui.find({ type: 'Text', text: /overtone guard/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /kerd-laptop-result\.patch/ })).toBeDefined()
      expect(await ui.find({ type: 'Button' })).toBeUndefined()
      await ui.unmount()
    }
    await clock.advance(30_000)
    await call
    expect(w.ran).toEqual([])
  })

  test('with the band showing its context row, the evidence still draws beside it', async ($, on) => {
    const { w, clock } = world(on, { answer: 'never' })
    const context = { tokens: 119_000, window: 1_000_000, percent: 12 }
    on('session.usage', () => ({ value: { startedAt: 0, context, rateLimits: [] } }) as never)
    on('agent.list', () => ({ value: [] }))
    on('session.measure', ($, e) => ({ changed: e.changed }))
    await $.session.measure({ context, rateLimits: [], changed: ['context'] } as never)
    const call = $.tool.call(bash('git add -A'))
    await clock.settle()
    const ui = await $.ui.mount({
      plugin: 'overtone',
      surface: 'terminal',
      component: 'AbovePrompt',
      props: { hasSurvey: false, isWorking: true, maxRows: 20, bodyColumns: 120 } as never,
    })
    expect((await ui.find({ type: 'Text', text: /^ {2}ctx/ }))?.text).toBe('  ctx ◼◼◼◼◼◼◼◼◼◼  │  5h —  │  7d —  │  cache —')
    expect(await ui.find({ type: 'Text', text: /overtone guard/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /kerd-laptop-result\.patch/ })).toBeDefined()
    await ui.unmount()
    await clock.advance(30_000)
    await call
    expect(w.ran).toEqual([])
  })
})

describe('guard: git however the command starts it', () => {
  test('env, sudo, timeout, bash -c, eval: git add .env asks each time and runs nothing', async ($, on) => {
    const { w, clock } = world(on, { status: '?? .env\0', answer: "Don't run it" })
    const forms = [
      'env git add .env',
      'env FOO=1 git add .env',
      'sudo git add .env',
      'timeout 5 git add .env',
      'bash -c "git add .env"',
      'eval "git add .env"',
      'bin/git add .env',
    ]
    for (const command of forms) {
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect([command, r.deny?.includes('.env (kept out of Git by instruction)')]).toEqual([command, true])
    }
    expect(w.asked).toHaveLength(forms.length)
    expect(w.ran).toEqual([])
  })

  test('xargs and find -exec: the add cannot be read, so it asks', async ($, on) => {
    const { w, clock } = world(on, { status: ' M README.md\0', answer: "Don't run it" })
    const denies: (string | undefined)[] = []
    for (const command of ['xargs git add < f', 'find . -exec git add {} +', 'watch git commit -am wip']) {
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      denies.push(((await call) as { deny?: string }).deny)
    }
    expect(w.asked).toHaveLength(3)
    expect(denies[0]).toContain('xargs adds arguments the guard cannot read')
    expect(denies[1]).toContain('find -exec runs it on paths the guard cannot list')
    expect(denies[2]).toContain('`watch` runs git in a way the guard does not read')
    expect(w.ran).toEqual([])
  })

  test('no false asks: git status, git log, echo push, npm run push, a heredoc that mentions git push', async ($, on) => {
    const { w } = world(on)
    const quiet = [
      'git status',
      'git log --oneline',
      'echo push',
      'npm run push',
      'grep -rn "git push" docs',
      "cat > notes.md <<'EOF'\nthen git add -A and git push\nEOF",
    ]
    for (const command of quiet) await $.tool.call(bash(command))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(quiet)
  })

  test('timeout 5 git push is read like a bare push: its files are listed and judged', async ($, on) => {
    const { w, clock } = world(on, { log: () => '.env\n', answer: "Don't run it" })
    const call = $.tool.call(bash('timeout 5 git push'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.argv).toContainEqual(['git', 'log', '--format=', '--name-only', '-z', '--diff-merges=separate', 'HEAD', '--not', '--remotes=origin', '--'])
    expect(r.deny).toContain('.env (kept out of Git by instruction)')
    expect(w.ran).toEqual([])
  })

  test('git subtree push: toward public origin it asks; toward the private vault remote it passes', async ($, on) => {
    const remotes =
      REMOTES + 'vault\tgit@github.com:alex/notes.git (fetch)\nvault\tgit@github.com:alex/notes.git (push)\n'
    const { w, clock } = world(on, { remotes, answer: "Don't run it" })
    const call = $.tool.call(bash('git subtree push --prefix x origin main'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('public github.com/alex/Kerd')
    expect(r.deny).toContain('subtree push publishes commits split out of a folder')
    await $.tool.call(bash('git subtree push --prefix x vault main'))
    expect(w.asked).toHaveLength(1)
    expect(w.ran).toEqual(['git subtree push --prefix x vault main'])
  })

  test('a git alias is read where git runs: one that runs status passes, one that runs add -A asks', async ($, on) => {
    const { w, clock } = world(on, {
      config: { 'alias.st': ['status\n', 0], 'alias.aa': ['add -A\n', 0] },
      answer: "Don't run it",
    })
    await $.tool.call(bash('git st'))
    expect(w.argv).toContainEqual(['git', 'config', '--get', 'alias.st'])
    expect(w.asked).toEqual([])
    const call = $.tool.call(bash('git aa'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('kerd-laptop-result.patch')
    expect(w.ran).toEqual(['git st'])
  })

  test('not an alias (a git-<name> program), or an alias read that fails: asks', async ($, on) => {
    const { w, clock } = world(on, { throws: ['config --get alias.zz'], answer: "Don't run it" })
    for (const command of ['git frob', 'git zz']) {
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      await call
    }
    expect(w.asked).toHaveLength(2)
    expect(w.asked[0]).toContain('git frob')
    expect(w.ran).toEqual([])
  })

  test('an alias with config the read cannot see asks without reading it', async ($, on) => {
    const { w, clock } = world(on, { config: { 'alias.st': ['status\n', 0] }, answer: "Don't run it" })
    const call = $.tool.call(bash('HOME=/tmp git st'))
    await clock.advance(5_000)
    await call
    expect(w.argv.some(a => a[1] === 'config' && a[3] === 'alias.st')).toBe(false)
    expect(w.asked).toHaveLength(1)
  })

  test('a shell alias is read from the top of the work tree: the guard reads that top, and asks when it cannot', async ($, on) => {
    const PRIVATE = remotesOf('git@github.com:alex/notes.git')
    const config = { 'alias.sa': ['!git add -A\n', 0] as [string, number] }
    // The top found: the alias reads there, and a private remote passes.
    const { w } = world(on, { config, remotes: PRIVATE })
    await $.tool.call(bash('git sa'))
    expect(w.argv).toContainEqual(['git', 'config', '--get', 'alias.sa'])
    expect(w.argv.filter(a => a.join(' ') === 'git rev-parse --show-toplevel').length).toBeGreaterThan(1)
    expect(w.asked).toEqual([])
  })

  test('a plain alias is read as before, with no top read for the alias itself', async ($, on) => {
    const { w } = world(on, { config: { 'alias.aa': ['add -A\n', 0] }, remotes: remotesOf('git@github.com:alex/notes.git') })
    await $.tool.call(bash('git aa'))
    expect(w.asked).toEqual([])
  })

  test('a shell alias whose top cannot be read asks, even where the repo is private', async ($, on) => {
    const PRIVATE = remotesOf('git@github.com:alex/notes.git')
    const { w, clock } = world(on, {
      config: { 'alias.sa': ['!git add -A\n', 0] },
      remotes: PRIVATE,
      answer: "Don't run it",
      answers: { 'rev-parse --show-toplevel': ['', 128, false] },
    })
    const call = $.tool.call(bash('git sa'))
    await clock.advance(5_000)
    await call
    expect(w.asked).toHaveLength(1)
    expect(w.asked[0]).toContain('git sa')
    expect(w.ran).toEqual([])
  })

  test('text mode: an alias it cannot read is not asked about', async ($, on) => {
    const { w } = world(on, { noProcess: true })
    await $.tool.call(bash('git st'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git st'])
  })
})

describe("guard: a push reads HEAD's and each pushed revision's committed vault.json", () => {
  const SECRET = JSON.stringify({ private_paths: ['secret.txt'] })
  for (const [where, rev] of [
    ['HEAD', 'HEAD'],
    ['the pushed revision', 'topic'],
  ] as const) {
    test(`first push of a new branch, working copy deleted: ${where}'s private_paths still ask`, async ($, on) => {
      const { w, clock } = world(on, {
        files: {},
        committed: base => (base === rev ? SECRET : null),
        missingBases: ['refs/remotes/origin/newbranch'],
        log: () => 'secret.txt\n',
        answer: "Don't run it",
      })
      const call = $.tool.call(bash('git push origin topic:newbranch'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.argv).toContainEqual(['git', 'show', 'HEAD:kivna/vault.json'])
      expect(w.argv).toContainEqual(['git', 'show', 'topic:kivna/vault.json'])
      // Never a base: no work-folder tree is read from them.
      expect(w.argv.some(a => a[1] === 'ls-tree' && (a[4] === 'HEAD' || a[4] === 'topic'))).toBe(false)
      expect(r.deny).toContain('secret.txt (kept out of Git by instruction)')
      expect(w.ran).toEqual([])
    })
  }

  test('add-only: no copy names it, the push passes; a thrown read adds nothing and removes nothing', async ($, on) => {
    const { w, clock } = world(on, {
      files: {},
      committed: null,
      missingBases: ['refs/remotes/origin/newbranch'],
      log: () => 'secret.txt\n',
    })
    await $.tool.call(bash('git push origin topic:newbranch'))
    expect(w.asked).toEqual([])
    // HEAD's read throws; the pushed revision's copy still adds its path.
    w.throws = ['show HEAD:kivna/vault.json']
    w.committed = base => (base === 'topic' ? SECRET : null)
    w.answer = "Don't run it"
    const call = $.tool.call(bash('git push origin topic:newbranch'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('secret.txt (kept out of Git by instruction)')
    expect(w.ran).toEqual(['git push origin topic:newbranch'])
  })
})

describe('guard: the reader decides, never a text match for "git"', () => {
  test('git spelled with an escape or a variable reaches the reader, and asks', async ($, on) => {
    const { w, clock } = world(on, { status: '?? .env\0', answer: "Don't run it" })
    const forms = ['gi\\t add -f .env', 'G=git; "$G" add -f .env']
    const denies: (string | undefined)[] = []
    for (const command of forms) {
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      denies.push(((await call) as { deny?: string }).deny)
    }
    expect(w.asked).toHaveLength(2)
    expect(denies[0]).toContain('.env (kept out of Git by instruction)')
    expect(denies[1]).toContain('is a shell expansion that may be git')
    expect(w.ran).toEqual([])
  })

  test('a command with no git op in it still reads no git and asks nothing', async ($, on) => {
    const { w } = world(on)
    const quiet = ['ls -la', 'echo push', 'npm run push', 'grep "git push" notes.md', 'make 2>&1 | tee build.log']
    for (const command of quiet) await $.tool.call(bash(command))
    expect(w.argv).toEqual([])
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(quiet)
  })
})

describe("guard: a ref-set push reads every pushed tip's committed vault.json", () => {
  const SECRET = JSON.stringify({ private_paths: ['secret.txt'] })
  const TIP_A = 'b'.repeat(40)
  const TIP_B = 'c'.repeat(40)
  const tips = (oids: string[]): Record<string, [string, number, boolean]> => ({
    'for-each-ref --format=%(objectname)': [oids.map(o => `${o}\n`).join(''), 0, false],
  })
  for (const [command, pattern] of [
    ['git push --all origin', 'refs/heads/'],
    ['git push --branches origin', 'refs/heads/'],
    ['git push --mirror origin', 'refs/'],
    ['git push --tags origin', 'refs/tags/'],
  ] as const) {
    test(`\`${command}\`: a private path another tip keeps asks`, async ($, on) => {
      const { w, clock } = world(on, {
        files: {},
        committed: base => (base === TIP_B ? SECRET : null),
        log: () => 'secret.txt\n',
        answers: tips([TIP_A, TIP_B]),
        answer: "Don't run it",
      })
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.argv).toContainEqual(['git', 'for-each-ref', '--format=%(objectname)', pattern])
      expect(w.argv).toContainEqual(['git', 'show', `${TIP_B}:kivna/vault.json`])
      expect(r.deny).toContain('secret.txt (kept out of Git by instruction)')
      expect(w.ran).toEqual([])
    })
  }

  test('add-only: no tip names the path, the push passes', async ($, on) => {
    const { w } = world(on, { files: {}, committed: null, log: () => 'secret.txt\n', answers: tips([TIP_A, TIP_B]) })
    await $.tool.call(bash('git push --all origin'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push --all origin'])
    // Absent, as the tip's own tree says: not a failed read.
    expect(w.argv).toContainEqual(['git', 'ls-tree', '--full-tree', TIP_B, '--', 'kivna/vault.json'])
  })

  const FAILS: [string, Partial<World>, string][] = [
    ['more tips than it reads', { answers: tips(Array.from({ length: 65 }, (_, i) => i.toString(16).padStart(40, '0'))) }, 'more than the 64'],
    ['a listing that fails', { answers: { 'for-each-ref --format=%(objectname)': ['', 128, false] } }, 'could not list the refs'],
    ['a cut listing', { answers: { 'for-each-ref --format=%(objectname)': [`${TIP_A}\n`, 0, true] } }, 'could not list the refs'],
    ['a listing that throws', { throws: ['for-each-ref --format=%(objectname)'] }, 'could not list the refs'],
    ['a tip whose copy cannot be read', { answers: tips([TIP_A, TIP_B]), throws: [`show ${TIP_B}:kivna/vault.json`] }, 'at a ref this push sends'],
    [
      'a tip whose tree has the file but git will not show it',
      {
        committed: base => (base === TIP_B ? SECRET : null),
        answers: { ...tips([TIP_A, TIP_B]), [`show ${TIP_B}:kivna/vault.json`]: ['', 128, false] },
      },
      'at a ref this push sends',
    ],
    [
      'a tip whose copy will not show and whose tree cannot be listed',
      {
        answers: {
          ...tips([TIP_A, TIP_B]),
          [`show ${TIP_B}:kivna/vault.json`]: ['', 128, false],
          [`ls-tree --full-tree ${TIP_B} -- kivna/vault.json`]: ['', 128, false],
        },
      },
      'at a ref this push sends',
    ],
    [
      'a tip whose tree listing throws',
      { answers: tips([TIP_A, TIP_B]), throws: [`ls-tree --full-tree ${TIP_B}`] },
      'at a ref this push sends',
    ],
  ]
  for (const [what, over, why] of FAILS) {
    test(`${what}: asks`, async ($, on) => {
      const { w, clock } = world(on, { files: {}, committed: null, log: () => 'README.md\n', answer: "Don't run it", ...over })
      const call = $.tool.call(bash('git push --all origin'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain(why)
      expect(w.ran).toEqual([])
    })
  }
})

describe('guard: a ref-set push reads the remote live before it trusts the tracking refs', () => {
  const PUBLIC = 'git@github.com:alex/Kerd.git'
  const REWOUND = 'b'.repeat(40)
  const SETS = ['git push --all origin', 'git push --branches origin', 'git push --tags origin', 'git push --mirror origin']
  const ls = (w: { argv: string[][] }) => w.argv.filter(a => a[1] === 'ls-remote')

  for (const command of SETS) {
    test(`\`${command}\`: the remote still has what the tracking refs say: passes, one live read of its branches`, async ($, on) => {
      const { w } = world(on, { log: () => 'README.md\n' })
      await $.tool.call(bash(command))
      expect(ls(w)).toEqual([['git', 'ls-remote', PUBLIC, 'refs/heads/*']])
      expect(w.argv.some(a => a[1] === 'cat-file')).toBe(false)
      expect(w.argv).toContainEqual(expect.arrayContaining(['log', '--not', '--remotes=origin']))
      expect(w.asked).toEqual([])
      expect(w.ran).toEqual([command])
    })

    test(`\`${command}\`: the remote was rewound since the last fetch: asks, and the log is never read against the stale ref`, async ($, on) => {
      // The tracking ref still holds the commit that added .env; the remote
      // has gone back to another commit this clone has. Measured against the
      // tracking refs (`--not --remotes=origin`) that commit reads as
      // published; the log lists .env only when it is not.
      const { w, clock } = world(on, {
        live: () => REWOUND,
        commits: [OID_TRACKED, REWOUND],
        log: a => (a.includes('--remotes=origin') ? 'README.md\n' : '.env\n'),
        answer: "Don't run it",
      })
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.asked).toHaveLength(1)
      expect(w.asked[0]).toContain('toward public github.com/alex/Kerd.')
      expect(r.deny).toContain("the remote no longer has what this clone's tracking refs say for feature")
      expect(w.argv.some(a => a[1] === 'log')).toBe(false)
      expect(w.ran).toEqual([])
    })
  }

  test('the branch is gone from the remote while its tracking ref stays: asks', async ($, on) => {
    const { w, clock } = world(on, { live: () => null, answer: "Don't run it" })
    const call = $.tool.call(bash('git push --all origin'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('no longer has what this clone')
    expect(w.ran).toEqual([])
  })

  test('the remote moved to a commit this clone does not have: asks (fetch first)', async ($, on) => {
    const { w, clock } = world(on, { live: () => 'c'.repeat(40), answer: "Don't run it" })
    const call = $.tool.call(bash('git push --tags origin'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('which this clone does not have')
    expect(w.ran).toEqual([])
  })

  test('only a branch other than the pushed ones is stale: still asks (every tracking ref is excluded)', async ($, on) => {
    const other = 'refs/remotes/origin/old-release'
    const { w, clock } = world(on, {
      tracking: { 'refs/remotes/origin/feature': OID_TRACKED, [other]: OID_TRACKED },
      live: (_url, ref) => (ref === 'refs/heads/old-release' ? REWOUND : OID_TRACKED),
      commits: [OID_TRACKED, REWOUND],
      answer: "Don't run it",
    })
    const call = $.tool.call(bash('git push --all origin'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('for old-release')
    expect(r.deny).not.toContain('for feature')
    expect(w.ran).toEqual([])
  })

  test('many stale branches: the why names three and counts the rest', async ($, on) => {
    const names = ['a', 'b', 'c', 'd', 'e']
    const { w, clock } = world(on, {
      tracking: Object.fromEntries(names.map(n => [`refs/remotes/origin/${n}`, OID_TRACKED])),
      live: () => REWOUND,
      commits: [OID_TRACKED, REWOUND],
      answer: "Don't run it",
    })
    const call = $.tool.call(bash('git push --all origin'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('for a, b, c, and 2 more')
    expect(w.ran).toEqual([])
  })

  const FAILS: [string, Partial<World>, string][] = [
    ['git ls-remote failing', { live: 'fail' }, 'git ls-remote failed'],
    ['a cut git ls-remote', { live: 'cut' }, 'git ls-remote failed'],
    ['a git ls-remote that throws or times out', { throws: ['ls-remote'] }, 'git ls-remote failed'],
    ['a check of the live commit that throws', { live: () => REWOUND, throws: ['cat-file'] }, 'could not check whether this clone has'],
    ['a tracking-ref listing that fails', { answers: { 'for-each-ref --format=%(refname)': ['', 128, false] } }, "could not list this clone's tracking refs"],
    [
      'a cut tracking-ref listing',
      { answers: { 'for-each-ref --format=%(refname)': [`refs/remotes/origin/feature ${OID_TRACKED} \n`, 0, true] } },
      "could not list this clone's tracking refs",
    ],
    ['a tracking-ref listing that throws', { throws: ['for-each-ref --format=%(refname)'] }, "could not list this clone's tracking refs"],
    [
      'a tracking ref that points outside the remote',
      { tracking: { 'refs/remotes/origin/HEAD': 'symref:refs/remotes/vault/main' } },
      'points outside the remote',
    ],
  ]
  for (const [what, over, why] of FAILS) {
    test(`${what}: asks`, async ($, on) => {
      const { w, clock } = world(on, { log: () => 'README.md\n', answer: "Don't run it", ...over })
      const call = $.tool.call(bash('git push --all origin'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain(why)
      expect(w.ran).toEqual([])
    })
  }

  test('origin/HEAD pointing at another origin branch is read as that branch: passes in sync', async ($, on) => {
    const { w } = world(on, {
      tracking: { 'refs/remotes/origin/feature': OID_TRACKED, 'refs/remotes/origin/HEAD': 'symref:refs/remotes/origin/feature' },
    })
    await $.tool.call(bash('git push --all origin'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push --all origin'])
  })

  test('no tracking refs: nothing is excluded, so no live read and the push passes', async ($, on) => {
    const { w } = world(on, { tracking: {} })
    await $.tool.call(bash('git push --all origin'))
    expect(ls(w)).toEqual([])
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push --all origin'])
  })

  // A remote with custom fetch refspecs (2026-10-07): GitHub's pull-request
  // refs fetched into origin/pr/*. Each tracking ref is read live as the ref
  // it was fetched from, never as a branch the remote never had.
  const PR_FETCH = '+refs/heads/*:refs/remotes/origin/*\n+refs/pull/*/head:refs/remotes/origin/pr/*\n'
  const PR_TRACKING = { 'refs/remotes/origin/feature': OID_TRACKED, 'refs/remotes/origin/pr/1': OID_TRACKED }

  test('custom fetch refspecs, the remote unchanged: passes, pull-request refs read as themselves', async ($, on) => {
    const { w } = world(on, {
      config: { 'remote.origin.fetch': [PR_FETCH, 0] },
      tracking: PR_TRACKING,
      remoteRefs: ['refs/pull/1/head'],
      remoteBranches: ['feature'],
    })
    await $.tool.call(bash('git push --all origin'))
    expect(ls(w)).toEqual([['git', 'ls-remote', PUBLIC, 'refs/heads/*', 'refs/pull/*/head']])
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push --all origin'])
  })

  test('custom fetch refspecs, a pull-request ref moved: asks, naming it', async ($, on) => {
    const { w, clock } = world(on, {
      config: { 'remote.origin.fetch': [PR_FETCH, 0] },
      tracking: PR_TRACKING,
      remoteRefs: ['refs/pull/1/head'],
      remoteBranches: ['feature'],
      live: (_url, ref) => (ref === 'refs/pull/1/head' ? REWOUND : OID_TRACKED),
      commits: [OID_TRACKED, REWOUND],
      answer: "Don't run it",
    })
    const call = $.tool.call(bash('git push --all origin'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('for pr/1')
    expect(w.ran).toEqual([])
  })

  const UNEXPLAINED: [string, Partial<World>, string][] = [
    [
      'a tracking ref no fetch refspec explains',
      { config: { 'remote.origin.fetch': ['+refs/heads/main:refs/remotes/origin/main\n', 0] } },
      'no fetch setting of the remote explains the tracking ref feature',
    ],
    [
      'two sources of one tracking ref both on the remote',
      { config: { 'remote.origin.fetch': [PR_FETCH, 0] }, tracking: PR_TRACKING, remoteRefs: ['refs/pull/1/head'], remoteBranches: ['feature', 'pr/1'] },
      'the remote has both refs/heads/pr/1 and refs/pull/1/head',
    ],
    ['an unreadable fetch setting', { config: { 'remote.origin.fetch': ['', 128] } }, "could not read the remote's fetch settings"],
    ['a cut fetch setting', { config: { 'remote.origin.fetch': ['+refs/heads/*:refs/remotes/origin/*\n', 0, true] } }, "could not read the remote's fetch settings"],
    ['a fetch setting that throws', { throws: ['config --get-all remote.origin.fetch'] }, "could not read the remote's fetch settings"],
    ['a fetch refspec with two stars', { config: { 'remote.origin.fetch': ['+refs/*/x/*:refs/remotes/origin/*\n', 0] } }, "could not read the remote's fetch setting"],
  ]
  for (const [what, over, why] of UNEXPLAINED) {
    test(`${what}: asks`, async ($, on) => {
      const { w, clock } = world(on, { log: () => 'README.md\n', answer: "Don't run it", ...over })
      const call = $.tool.call(bash('git push --all origin'))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect(w.asked).toHaveLength(1)
      expect(r.deny).toContain(why)
      expect(w.ran).toEqual([])
    })
  }

  test('a ref set to a private remote reads nothing live and passes', async ($, on) => {
    const remotes = REMOTES + 'vault\tgit@github.com:alex/notes.git (fetch)\nvault\tgit@github.com:alex/notes.git (push)\n'
    const { w } = world(on, { remotes, live: 'fail' })
    await $.tool.call(bash('git push --all vault'))
    expect(ls(w)).toEqual([])
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push --all vault'])
  })

  test('a named-branch push is unchanged: no tracking-ref listing', async ($, on) => {
    const { w } = world(on)
    await $.tool.call(bash('git push origin feature'))
    expect(w.argv.some(a => a[1] === 'for-each-ref' && a[2]?.startsWith('--format=%(refname)'))).toBe(false)
    expect(ls(w)).toEqual([['git', 'ls-remote', PUBLIC, 'refs/heads/feature']])
  })
})

describe('guard: push file names git would quote', () => {
  test('a private folder file with a non-ASCII name asks', async ($, on) => {
    const { w, clock } = world(on, { log: () => '.playwright-mcp/é.png\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('.playwright-mcp/é.png')
    expect(w.ran).toEqual([])
  })

  test('a new work folder with a non-ASCII name asks', async ($, on) => {
    const fresh = world(on, { log: () => 'docs/work/é/notes.md\n', answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await fresh.clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(r.deny).toContain('docs/work/é/notes.md')
    expect(fresh.w.ran).toEqual([])
  })

  test('a work folder with a non-ASCII name the base already has passes', async ($, on) => {
    const { w } = world(on, { log: () => 'docs/work/é/notes.md\n', workTree: ['docs/work/é', 'docs/work/question-sets'] })
    await $.tool.call(bash('git push origin feature'))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual(['git push origin feature'])
  })
})

describe('guard: merges, and repositories the guard cannot name', () => {
  test('a file only a merge brings (a conflict resolution) is in what the push publishes: it asks', async ($, on) => {
    // git log lists a merge commit's own changes only when asked for its
    // diff against each parent; without that, the merge lists nothing.
    const log = (a: string) => (a.includes('--diff-merges=separate') ? 'README.md\nkerd-laptop-result.patch\n' : 'README.md\n')
    const { w, clock } = world(on, { log, answer: "Don't run it" })
    const call = $.tool.call(bash('git push origin feature'))
    await clock.advance(5_000)
    const r = (await call) as { deny?: string }
    expect(w.asked).toHaveLength(1)
    expect(r.deny).toContain('kerd-laptop-result.patch')
    expect(w.ran).toEqual([])
  })

  test("find -execdir git push, or one after cd \"$DIR\", asks even from a private repo, reading none of the caller's git", async ($, on) => {
    const { w, clock } = world(on, { remotes: remotesOf('git@github.com:alex/notes.git'), answer: "Don't run it" })
    // The caller's own private push passes, as before.
    await $.tool.call(bash('git push origin HEAD'))
    expect(w.ran).toEqual(['git push origin HEAD'])
    for (const command of [
      'find /work/repos -name .git -prune -execdir git push origin HEAD \\;',
      'find /work/repos -maxdepth 1 -type d -exec git -C {} push origin HEAD \\;',
      'cd "$DIR" && git push origin HEAD',
    ]) {
      w.argv.length = 0
      const call = $.tool.call(bash(command))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect([command, r.deny]).toEqual([command, expect.stringContaining('cannot name')])
      expect([command, w.argv.filter(a => a[0] === 'git')]).toEqual([command, []])
    }
    expect(w.ran).toEqual(['git push origin HEAD'])
    expect(w.asked).toHaveLength(3)
  })
})

describe('guard: a cd into a folder that is not there', () => {
  // The file system as the engine answers it: these paths are missing, these are files.
  const disk = (on: On, gone: string[], files: string[] = []) => {
    on('fs.exists', ($, e) => ({ value: !gone.includes(e.path) }) as never)
    on('fs.stat', ($, e) => {
      if (gone.includes(e.path)) throw new Error('ENOENT')
      return { value: { kind: files.includes(e.path) ? 'file' : 'dir', size: 0, mtimeMs: 0, isLink: false } } as never
    })
  }

  test('after a failed cd, git runs in the folder before it: it asks, reading no git', async ($, on) => {
    const { w, clock } = world(on, { answer: "Don't run it" })
    disk(on, ['/work/typo'], [`${KERD}/README.md`])
    for (const [command, bad] of [
      [`cd ${KERD} && cd /work/typo; git push origin HEAD`, '/work/typo'],
      ['cd /work/typo || true; git add .', '/work/typo'],
      [`cd ${KERD}; cd /work/typo; git commit -m x`, '/work/typo'],
      // A later move from where the failed cd would have been lands somewhere real.
      [`cd ${KERD}/docs; cd /work/typo; cd ..; git push origin HEAD`, '/work/typo'],
      [`cd ${KERD}; cd /work/typo; git -C .. push origin HEAD`, '/work/typo'],
      // A file is there, but cd cannot enter it.
      [`cd ${KERD}; cd README.md; git push origin HEAD`, `${KERD}/README.md`],
    ]) {
      w.argv.length = 0
      const call = $.tool.call(bash(command!))
      await clock.advance(5_000)
      const r = (await call) as { deny?: string }
      expect([command, r.deny]).toEqual([command, expect.stringContaining(`\`${bad}\`, which is not a folder`)])
      expect([command, w.argv.filter(a => a[0] === 'git')]).toEqual([command, []])
    }
    expect(w.asked).toHaveLength(6)
    expect(w.ran).toEqual([])
  })

  test('folders that are there are followed as before', async ($, on) => {
    const { w } = world(on)
    disk(on, ['/work/typo'])
    await $.tool.call(bash(`cd /work && cd ${KERD} && git add README.md`))
    // A missing folder after the git command does not touch it.
    await $.tool.call(bash(`cd ${KERD} && git add README.md; cd /work/typo`))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual([`cd /work && cd ${KERD} && git add README.md`, `cd ${KERD} && git add README.md; cd /work/typo`])
  })

  test('no file access: the folder counts as there, as before', async ($, on) => {
    const { w } = world(on)
    on('fs.exists', () => {
      throw new Error('no file access')
    })
    await $.tool.call(bash(`cd ${KERD} && git add README.md`))
    expect(w.asked).toEqual([])
    expect(w.ran).toEqual([`cd ${KERD} && git add README.md`])
  })
})
