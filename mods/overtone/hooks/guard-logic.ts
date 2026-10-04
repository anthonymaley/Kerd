// overtone guard: pure logic. No `$`, no state, nothing mutable at module
// level. guard.tsx gathers the git facts and asks; this file decides.

// ---------------------------------------------------------------------------
// What is private.
//
// - Working notes live in the private vault. The vault is where the person's
//   own `vault_path` setting says, in every repo, and where the repo's
//   kivna/vault.json says (`"vault"`), each with where it lands when that
//   path is a link. Never a path written here. A vault path only ever adds
//   what the guard asks about; it never lets a command through. A repo's
//   `"vault"` that is relative, or holds the repo or the home folder, cannot
//   be used: the guard asks. Any `notes:` path is a vault note everywhere.
// - A NEW folder under docs/work/ is a sketchbook that belongs in the vault,
//   in a repo whose kivna/vault.json says "work_notes": "vault". Folders the
//   base tree already has stay public; `question-sets` is the public seed
//   folder.
// - `.env` at the repo root (local keys, gitignored) and `.playwright-mcp/`
//   (browser snapshots), in every repo. A repo adds its own private paths in
//   kivna/vault.json `"private_paths"`: add-only, repo-relative, a trailing
//   `/` for a folder; an entry the guard cannot use makes it ask.
// - A github.com remote (githubRepo) is public unless GitHub says it is
//   private (guard.tsx asks `gh repo view`), the vault's own repo included;
//   one it could not ask about is guarded. Any other URL with "github" in it
//   is guarded unconfirmed. Only URLs without it are not guarded.
// ---------------------------------------------------------------------------
export const GUARD = {
  // A command argument with this prefix names a vault note.
  notesPrefix: 'notes:',
  // Repo-relative. A trailing `/` means the whole folder.
  repoPaths: [
    '.env',
    '.playwright-mcp/',
  ],
  // A file in a folder under `root` that the base tree does not have yet is a
  // new sketchbook: it belongs in the vault. `keep` folders are public. Only
  // in a repo whose `file` says `"work_notes": "vault"`.
  newWorkFolders: { root: 'docs/work/', keep: ['question-sets'], file: 'kivna/vault.json' },
  // The dialog: no answer in this long counts as no.
  timeoutMs: 30_000,
  // A "Run it" sooner than this after the dialog opened is a typed-ahead key,
  // not a decision: refused.
  reflexMs: 1_000,
} as const

export type GuardConfig = typeof GUARD

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

export function normalize(path: string): string {
  const isAbs = path.startsWith('/')
  const out: string[] = []
  for (const part of path.split('/')) {
    if (part === '' || part === '.') continue
    if (part === '..') {
      if (out.length && out[out.length - 1] !== '..') out.pop()
      else if (!isAbs) out.push('..')
      continue
    }
    out.push(part)
  }
  return (isAbs ? '/' : '') + out.join('/') || (isAbs ? '/' : '.')
}

export function expandHome(path: string, home: string | undefined): string {
  if (!home) return path
  if (path === '~') return home
  if (path.startsWith('~/')) return home + path.slice(1)
  return path
}

export function resolvePath(cwd: string, path: string, home?: string): string {
  const p = expandHome(path, home)
  return normalize(p.startsWith('/') ? p : `${cwd}/${p}`)
}

const isInside = (abs: string, root: string) => abs === root || abs.startsWith(root + '/')

// Anything inside a vault path is private working notes (`~` is $HOME).
export function inVault(abs: string, home: string | undefined, vault: VaultFacts): boolean {
  return [...vault.paths, ...vault.own].some(v => isInside(abs, normalize(expandHome(v, home))))
}

// Why a repo-relative path is private, or undefined. `knownWorkSlugs` is the
// set of folders under newWorkFolders.root in the base tree; null skips the
// new-folder rule (unknown base: fail open). `extra`: the repo's own
// private_paths, added to cfg.repoPaths.
export function privateReason(
  rel: string,
  knownWorkSlugs: ReadonlySet<string> | null,
  cfg: GuardConfig = GUARD,
  extra: readonly string[] = [],
): string | undefined {
  const p = normalize(rel)
  for (const entry of [...cfg.repoPaths, ...extra]) {
    if (entry.endsWith('/') ? isInside(p, entry.slice(0, -1)) : isInside(p, entry)) {
      return entry.endsWith('/') ? `private folder ${entry}` : 'kept out of Git by instruction'
    }
  }
  const root = cfg.newWorkFolders.root
  const slug = workSlug(p, cfg)
  if (knownWorkSlugs && slug !== undefined && !knownWorkSlugs.has(slug)) {
    return `new work folder ${root}${slug}/: working notes belong in the vault as ${cfg.notesPrefix}${slug}/`
  }
  return undefined
}

// The folder under newWorkFolders.root a repo-relative path is in, unless it
// is a `keep` folder; else undefined.
export function workSlug(rel: string, cfg: GuardConfig = GUARD): string | undefined {
  const root = cfg.newWorkFolders.root
  const p = normalize(rel)
  if (!p.startsWith(root)) return undefined
  const rest = p.slice(root.length)
  const slash = rest.indexOf('/')
  if (slash <= 0) return undefined
  const slug = rest.slice(0, slash)
  return (cfg.newWorkFolders.keep as readonly string[]).includes(slug) ? undefined : slug
}

// True when the repo's newWorkFolders.file text says its working notes live
// in the vault. Unparseable or anything else: false (the new-folder rule off).
export function workNotesInVault(text: string): boolean {
  try {
    const j: unknown = JSON.parse(text)
    return typeof j === 'object' && j !== null && (j as { work_notes?: unknown }).work_notes === 'vault'
  } catch {
    return false
  }
}

// What one newWorkFolders.file text says: where the private vault is
// (`"vault"`, `"folder"`, whether `"work_notes": "vault"`) and the repo's own
// `"private_paths"`; null when it says none of that. 'unreadable' when the
// guard cannot use it and must ask: unparseable while it speaks of work_notes,
// private_paths or a vault; "work_notes": "vault" with no vault; a vault that is not
// an absolute or `~/` path; private_paths that is not a list of plain
// repo-relative paths.
export type VaultRead =
  | { vault?: string; folder?: string; workNotes: boolean; privatePaths: string[] }
  | 'unreadable'
  | null

// A vault path as written: absolute or under `~/`, never `/` or `~` alone.
const VAULT_SHAPE = /^(?:\/|~\/)./

// One private_paths entry, repo-relative: no leading `/` or `~`, no `..`, no
// glob or expansion, nothing empty. The trailing `/` of a folder is kept.
function plainRepoPath(entry: unknown): string | undefined {
  if (typeof entry !== 'string') return undefined
  const e = entry.trim()
  if (!e || e.startsWith('/') || e.startsWith('~') || /[*?[\]$`\\]/.test(e)) return undefined
  if (e.split('/').some(part => part === '..')) return undefined
  const n = normalize(e)
  if (n === '.' || n === '') return undefined
  return e.endsWith('/') ? `${n}/` : n
}

export function readVault(text: string): VaultRead {
  let j: unknown
  try {
    j = JSON.parse(text)
  } catch {
    return /work_notes|private_paths|vault/.test(text) ? 'unreadable' : null
  }
  if (typeof j !== 'object' || j === null || Array.isArray(j)) return null
  const { vault, folder, work_notes, private_paths } = j as Record<string, unknown>
  const workNotes = work_notes === 'vault'
  let privatePaths: string[] = []
  if (private_paths !== undefined) {
    if (!Array.isArray(private_paths)) return 'unreadable'
    const read = private_paths.map(plainRepoPath)
    if (read.some(r => r === undefined)) return 'unreadable'
    privatePaths = [...new Set(read as string[])]
  }
  let where: string | undefined
  if (typeof vault === 'string' && vault.trim() !== '') {
    where = vault.trim()
    if (!VAULT_SHAPE.test(where) || where.split('/').includes('..')) return 'unreadable'
    // `//`, `~//` and the like name the root or $HOME, which guard nothing.
    if (['/', '~', '~/'].includes(normalize(where).replace(/\/+$/, '') || '/')) return 'unreadable'
  } else if (vault !== undefined && vault !== '' ) {
    return 'unreadable'
  }
  if (workNotes && where === undefined) return 'unreadable'
  if (where === undefined && !privatePaths.length && !workNotes) return null
  return {
    ...(where !== undefined ? { vault: where } : {}),
    ...(typeof folder === 'string' && folder.trim() !== '' ? { folder: folder.trim() } : {}),
    workNotes,
    privatePaths,
  }
}

// What the guard knows about the vault and the repo's own private paths.
export type VaultFacts = {
  // The vault paths the repo's kivna/vault.json files name (each base tree's
  // committed copy and the working tree's), as written (`~` is $HOME), and
  // guard.tsx adds where each lands when a link.
  paths: string[]
  // The person's own `vault_path` setting, and where it lands: every repo.
  own: string[]
  // Where working notes go, for the deny message: <vault>/<folder>/work/
  // when "work_notes": "vault" names a folder, else <vault>/. Only a plain
  // path (SAFE_NOTES) is ever shown; anything else, none.
  notes?: string
  // The repo's own private_paths, every copy's together (add-only).
  privatePaths: string[]
  // Why the guard must ask whatever the paths: a file or setting it cannot use.
  unusable: Hit[]
}

export const NO_VAULT: VaultFacts = { paths: [], own: [], privatePaths: [], unusable: [] }

// A kivna/vault.json the guard cannot use: it asks.
export const VAULT_UNREADABLE =
  'the guard could not read where kivna/vault.json puts the private vault or which paths it keeps private, so it cannot tell whether a path here is private'
// A repo's vault path that holds the repo itself or the home folder.
export const VAULT_TOO_WIDE =
  'its vault path holds this repo or your home folder, so the guard cannot use it to tell notes from the repo'
// The person's vault_path setting is not a usable path.
export const VAULT_SETTING_UNUSABLE =
  "overtone's vault_path setting is not an absolute or ~/ path below your home folder, so the guard cannot use it"
export const VAULT_SETTING = 'overtone setting vault_path'

// A path shown to Claude in the deny message: plain characters, clipped.
const SAFE_NOTES = /^~?\/[\w./-]+$/
const NOTES_MAX = 120
export const shownNotes = (p: string | undefined): string | undefined =>
  p !== undefined && SAFE_NOTES.test(p) && p.length <= NOTES_MAX ? p : undefined

const slashed = (p: string) => (p.endsWith('/') ? p : `${p}/`)

// `own`: the person's vault_path setting ('' or absent: none).
export function vaultFrom(reads: readonly VaultRead[], own = ''): VaultFacts {
  const found = reads.filter((r): r is Exclude<VaultRead, 'unreadable' | null> => r !== null && r !== 'unreadable')
  const unusable: Hit[] = reads.includes('unreadable') ? [{ path: GUARD.newWorkFolders.file, reason: VAULT_UNREADABLE }] : []
  const mine = own.trim()
  const ownPaths: string[] = []
  if (mine) {
    if (VAULT_SHAPE.test(mine) && !mine.split('/').includes('..')) ownPaths.push(mine)
    else unusable.push({ path: VAULT_SETTING, reason: VAULT_SETTING_UNUSABLE })
  }
  const paths = [...new Set(found.flatMap(r => (r.vault !== undefined ? [r.vault] : [])))]
  const privatePaths = [...new Set(found.flatMap(r => r.privatePaths))]
  const first = found.find(r => r.vault !== undefined && r.workNotes && r.folder) ?? found.find(r => r.vault !== undefined)
  const notes = first?.vault
    ? first.workNotes && first.folder
      ? `${slashed(first.vault)}${first.folder}/work/`
      : slashed(first.vault)
    : ownPaths[0] !== undefined
      ? slashed(ownPaths[0])
      : undefined
  const shown = shownNotes(notes)
  return { paths, own: ownPaths, privatePaths, unusable, ...(shown ? { notes: shown } : {}) }
}

// The vault as the guard may use it here: a repo's vault path that holds
// `root` (the repo, or where git runs) or the home folder is dropped and
// asked about; the person's own setting is dropped and asked about only when
// it holds the home folder. Nothing here ever lets a command through.
export function usableVault(vault: VaultFacts, root: string, home: string | undefined): VaultFacts {
  const h = home ? normalize(home) : undefined
  const holds = (v: string, also: boolean) => {
    const abs = normalize(expandHome(v, home))
    return (also && isInside(root, abs)) || (h !== undefined && isInside(h, abs))
  }
  const paths = vault.paths.filter(v => !holds(v, true))
  const own = vault.own.filter(v => !holds(v, false))
  const unusable = [...vault.unusable]
  if (paths.length < vault.paths.length) unusable.push({ path: GUARD.newWorkFolders.file, reason: VAULT_TOO_WIDE })
  if (own.length < vault.own.length) unusable.push({ path: VAULT_SETTING, reason: VAULT_SETTING_UNUSABLE })
  const widened = paths.length < vault.paths.length || own.length < vault.own.length
  const { notes, ...rest } = vault
  return { ...rest, paths, own, unusable, ...(notes && !widened ? { notes } : {}) }
}

// ---------------------------------------------------------------------------
// The command: a small shell reader (quotes, escapes, separators).
// ---------------------------------------------------------------------------

// One simple command as the reader sees it: its words; the `$(…)` and
// backtick commands inside it (they run too); the here-documents it reads
// (`<<EOF`), each body with whether its delimiter was quoted (then nothing in
// it expands); and whether it pipes into the next command (`|`).
type Simple = {
  words: string[]
  // Per word: the index of its first quoted or escaped character (Infinity:
  // none). A redirection operator counts only when all of it is unquoted.
  firstQuoted: number[]
  subs: string[]
  heredocs: { body: string; quoted: boolean }[]
  piped: boolean
}

// Splits a command line into simple commands, each a list of words. Splits on
// unquoted `&&`, `||`, `;`, `|`, `&`, newlines and parentheses. Not a shell:
// no expansion; `$(...)` inside double quotes stays one word.
export function splitCommands(command: string): string[][] {
  return splitShell(command).map(c => c.words)
}

function splitShell(command: string): Simple[] {
  const commands: Simple[] = []
  const fresh = (): Simple => ({ words: [], firstQuoted: [], subs: [], heredocs: [], piped: false })
  let cur = fresh()
  let word = ''
  let hasWord = false
  // The word had a quote or an escape (a quoted here-doc delimiter).
  let wordQuoted = false
  let quote: '"' | "'" | null = null
  let depth = 0 // $( ... ) nesting inside double quotes
  let subAt = -1 // where the outermost $( inside double quotes began
  // Here-documents named on this line, read after its newline. Only an
  // unquoted, unescaped `<<` (seen in the loop below, never read back from a
  // finished word) starts one: `"<<EOF"` and `\<<EOF` are text.
  const pending: { delim: string; strip: boolean; quoted: boolean; into: Simple }[] = []
  let wantDelim: { strip: boolean } | null = null
  // In the current word: where the text after an unquoted `<<` begins (-1:
  // none), whether it was `<<-`, and whether a quote or escape came after it.
  let opAt = -1
  let opStrip = false
  let opQuoted = false
  // Where in the word the first quoted or escaped character is.
  let firstQuoted = Infinity
  const quoted = () => {
    if (firstQuoted === Infinity) firstQuoted = hasWord ? word.length : 0
    wordQuoted = true
    if (opAt >= 0) opQuoted = true
  }
  const endWord = () => {
    if (hasWord) {
      cur.words.push(word)
      cur.firstQuoted.push(firstQuoted)
      if (wantDelim) {
        pending.push({ delim: word, strip: wantDelim.strip, quoted: wordQuoted, into: cur })
        wantDelim = null
      }
      if (opAt >= 0) {
        const rest = word.slice(opAt)
        if (rest === '') wantDelim = { strip: opStrip }
        else pending.push({ delim: rest, strip: opStrip, quoted: opQuoted, into: cur })
      }
    }
    word = ''
    hasWord = false
    wordQuoted = false
    firstQuoted = Infinity
    opAt = -1
    opStrip = false
    opQuoted = false
  }
  const endCommand = (piped = false) => {
    endWord()
    if (cur.words.length) {
      cur.piped = piped
      commands.push(cur)
    }
    cur = fresh()
  }
  // At a newline: the bodies of the here-documents named on the line before,
  // in order. Returns the index of the last character read. A body whose
  // delimiter line never comes is not taken as text (fail closed): its lines,
  // and any after, are read as commands.
  const readBodies = (from: number): number => {
    let at = from
    while (pending.length) {
      const h = pending.shift()!
      const start = at
      const lines: string[] = []
      let closed = false
      while (at < command.length) {
        const nl = command.indexOf('\n', at)
        const line = nl < 0 ? command.slice(at) : command.slice(at, nl)
        at = nl < 0 ? command.length : nl + 1
        if ((h.strip ? line.replace(/^\t+/, '') : line) === h.delim) {
          closed = true
          break
        }
        lines.push(line)
      }
      if (!closed) {
        pending.length = 0
        return start - 1
      }
      h.into.heredocs.push({ body: lines.join('\n'), quoted: h.quoted })
    }
    return at - 1
  }
  for (let i = 0; i < command.length; i++) {
    const c = command[i]
    if (quote === "'") {
      if (c === "'") quote = null
      else word += c
      continue
    }
    if (quote === '"') {
      if (c === '\\' && i + 1 < command.length) {
        word += command[++i]
        continue
      }
      if (c === '$' && command[i + 1] === '(') {
        if (depth === 0) subAt = i + 2
        depth++
        word += '$('
        i++
        continue
      } else if (c === '(' && depth > 0) depth++
      else if (c === ')' && depth > 0) {
        depth--
        if (depth === 0 && subAt >= 0) {
          cur.subs.push(command.slice(subAt, i))
          subAt = -1
        }
      } else if (c === '"' && depth === 0) {
        quote = null
        continue
      }
      word += c
      continue
    }
    if (c === '\\' && i + 1 < command.length) {
      if (command[i + 1] !== '\n') {
        quoted()
        word += command[i + 1]
        hasWord = true
      }
      i++
      continue
    }
    if (c === "'" || c === '"') {
      quoted()
      quote = c
      hasWord = true
      continue
    }
    if (c === '<' && command[i + 1] === '<') {
      // `<<<` is a here-string (one word of input), not a here-document.
      if (command[i + 2] === '<') {
        word += '<<<'
        hasWord = true
        i += 2
        continue
      }
      word += '<<'
      i++
      opStrip = command[i + 1] === '-'
      if (opStrip) {
        word += '-'
        i++
      }
      hasWord = true
      opAt = word.length
      opQuoted = false
      continue
    }
    if (c === '`') {
      // A backtick command runs: kept whole in the word, and read as a command.
      let j = i + 1
      while (j < command.length && command[j] !== '`') j += command[j] === '\\' ? 2 : 1
      cur.subs.push(command.slice(i + 1, Math.min(j, command.length)))
      word += command.slice(i, Math.min(j + 1, command.length))
      hasWord = true
      i = j
      continue
    }
    if (c === ' ' || c === '\t') {
      endWord()
      continue
    }
    if (c === '\n') {
      endCommand()
      if (pending.length) i = readBodies(i + 1)
      continue
    }
    if (c === '|') {
      if (command[i + 1] === '|') {
        endCommand()
        i++
      } else endCommand(true)
      continue
    }
    if (c === ';' || c === '&' || c === '(' || c === ')') {
      endCommand()
      continue
    }
    if (c === '#' && !hasWord) {
      while (i < command.length && command[i] !== '\n') i++
      endCommand()
      if (pending.length) i = readBodies(i + 1)
      continue
    }
    word += c
    hasWord = true
  }
  endCommand()
  return commands
}

// A word the shell would expand before git sees it: `$(…)`, backticks,
// `${…}`, `$VAR`, or a brace list/range. The reader cannot know what it
// becomes, so a path or push target carrying one is never passed unread.
// (Single-quoted `$` is literal to the shell; it is asked about all the same.)
const EXPANSION = /[$`]|\{[^{}]*(?:,|\.\.)[^{}]*\}/
export const hasExpansion = (word: string): boolean => EXPANSION.test(word)

export type Spec = {
  raw: string
  abs: string
  // Where `abs` lands when a folder on its way is a link, as guard.tsx
  // resolves it (absent: not resolved, or the same).
  real?: string
  // Why the guard cannot place this spec, when it cannot: the op asks.
  unreadable?: string
}

// Where a push goes, as written. `remote` null: git's default for the branch.
export type PushTarget = {
  remote: string | null
  refspecs: string[]
  // Ref sets named by option: --all/--branches, --mirror, --tags.
  sets: ('--branches' | '--all' | '--tags')[]
  // -d/--delete: removes refs, publishes nothing.
  deleting: boolean
  // -f, --force, --force-with-lease, --force-if-includes: may overwrite what
  // the remote has, which its remote-tracking refs may not show. (A `+`
  // refspec is read where the refspecs are.)
  force: boolean
  // Why the reader cannot tell where this push goes, when it cannot.
  opaque: string | null
  // Why the reader can tell where this push goes but not what it sends (a
  // wrapper or `git subtree push`): to a public repo it asks.
  blind?: string
}

export type GitOp = {
  kind: 'add' | 'commit' | 'push'
  // The directory git runs in (after `cd` and `-C`), absolute.
  cwd: string
  // The words of this git command, as read.
  text: string
  // add: -A/--all; commit: -a/--all.
  all: boolean
  // add: -u/--update.
  update: boolean
  // add: -f/--force (ignored files too, which status does not list).
  force: boolean
  // Pathspecs as written, and resolved to absolute paths.
  specs: Spec[]
  // A spec the reader cannot place (`:(magic)`, a glob, a pathspec file):
  // treat the op as a whole-tree sweep.
  isOpaque: boolean
  // push only: the target.
  push?: PushTarget
  // An alias the reader has not been told about (`git <name>`): guard.tsx
  // reads it and parses again; unread, the op asks as it stands.
  alias?: string
}

const COMMIT_SHORT_ARG = new Set(['m', 'F', 'C', 'c', 't'])
const COMMIT_LONG_ARG = new Set([
  '--message', '--file', '--author', '--date', '--template', '--reuse-message',
  '--reedit-message', '--fixup', '--squash', '--trailer', '--cleanup',
])

// How deep the reader follows commands inside commands (`bash -c`, `eval`,
// `$(…)`, an alias); deeper, a command that names git asks.
const MAX_DEPTH = 4

// Prefix commands the reader looks through to the command they run, and how
// each reads its options: `arg`, short options that take a value (attached
// or the next word); `attached`, short options whose value can only be
// attached; `long`, long options that take one (`--x=v` or `--x v`);
// `operands`, words before the command (timeout's duration); `dir`, options
// that move where the command runs; `split`, options whose value is itself
// the command's words (env -S).
type Wrapper = {
  arg?: string
  attached?: string
  long?: readonly string[]
  operands?: number
  dir?: readonly string[]
  split?: readonly string[]
}
const WRAPPERS: Record<string, Wrapper> = {
  command: {},
  builtin: {},
  exec: { arg: 'a' },
  nohup: {},
  time: { arg: 'of', long: ['--output', '--format'] },
  env: {
    arg: 'uCSP',
    long: ['--unset', '--chdir', '--split-string'],
    dir: ['-C', '--chdir'],
    split: ['-S', '--split-string'],
  },
  sudo: {
    arg: 'ugpCrtTUD',
    long: ['--user', '--group', '--prompt', '--close-from', '--role', '--type', '--command-timeout', '--other-user', '--chdir', '--host'],
    dir: ['-D', '--chdir'],
  },
  doas: { arg: 'uC' },
  nice: { arg: 'n', long: ['--adjustment'] },
  timeout: { arg: 'sk', long: ['--signal', '--kill-after'], operands: 1 },
  stdbuf: { arg: 'ioe', long: ['--input', '--output', '--error'] },
  ionice: { arg: 'cnpPu', long: ['--class', '--classdata', '--pid', '--pgid', '--uid'] },
  caffeinate: { arg: 'tw' },
}
// xargs runs the command with arguments it reads, which the reader cannot see.
const XARGS: Wrapper = {
  arg: 'ILnPsEda',
  attached: 'ile',
  long: ['--arg-file', '--delimiter', '--max-args', '--max-lines', '--max-procs', '--max-chars', '--process-slot-var'],
}
// Shell words that come before a command.
const KEYWORDS = new Set(['!', '{', 'if', 'then', 'else', 'elif', 'do', 'while', 'until'])
const SHELLS = new Set(['sh', 'bash', 'zsh', 'dash', 'ksh', 'mksh', 'fish'])
// Commands that print or search text and run nothing: words in them that
// spell a git command are data.
const INERT = new Set([
  'echo', 'printf', 'print', 'grep', 'egrep', 'fgrep', 'rg', 'ag', 'ack', 'sed', 'awk', 'gawk', 'cat', 'bat',
  'less', 'more', 'head', 'tail', 'wc', 'sort', 'uniq', 'cut', 'tr', 'jq', 'yq', 'man', 'help', 'which',
  'type', 'whatis', 'apropos', 'test', '[', '[[', 'true', 'false', ':', 'gh', 'diff', 'tee', 'ls', 'pbcopy',
])
// Subcommands git ships (`git --list-cmds=main`, git 2.54). git never runs an
// alias that shadows one; any other name is an alias (guard.tsx reads it) or
// a `git-<name>` program on PATH (it asks).
const GIT_COMMANDS = new Set(
  (
    'add am annotate apply archive backfill bisect blame branch bugreport bundle cat-file check-attr check-ignore ' +
    'check-mailmap check-ref-format checkout checkout-index cherry cherry-pick clean clone column commit ' +
    'commit-graph commit-tree config count-objects credential credential-cache credential-store daemon describe ' +
    'diagnose diff diff-files diff-index diff-pairs diff-tree difftool fast-export fast-import fetch fetch-pack ' +
    'filter-branch fmt-merge-msg for-each-ref for-each-repo format-patch fsck fsck-objects gc get-tar-commit-id ' +
    'grep hash-object help history hook http-backend http-fetch http-push imap-send index-pack init init-db ' +
    'instaweb interpret-trailers last-modified log ls-files ls-remote ls-tree mailinfo mailsplit maintenance ' +
    'merge merge-base merge-file merge-index merge-octopus merge-one-file merge-ours merge-recursive merge-resolve ' +
    'merge-subtree merge-tree mergetool mktag mktree multi-pack-index mv name-rev notes p4 pack-objects ' +
    'pack-redundant pack-refs patch-id prune prune-packed pull push quiltimport range-diff read-tree rebase ' +
    'receive-pack reflog refs remote repack replace replay repo request-pull rerere reset restore rev-list ' +
    'rev-parse revert rm send-email send-pack shell shortlog show show-branch show-index show-ref sparse-checkout ' +
    'stage stash status stripspace submodule subtree switch symbolic-ref tag unpack-file unpack-objects ' +
    'update-index update-ref update-server-info upload-archive upload-pack var verify-commit verify-pack ' +
    'verify-tag version whatchanged worktree write-tree'
  ).split(' '),
)
// A name git accepts as an alias.
const ALIAS_NAME = /^[A-Za-z0-9][A-Za-z0-9-]*$/
const VERBS: ReadonlyMap<string, GitOp['kind']> = new Map([
  ['add', 'add'],
  ['stage', 'add'],
  ['commit', 'commit'],
  ['push', 'push'],
])
const ASSIGNMENT = /^[A-Za-z_][A-Za-z0-9_]*=/
// Assignments that change which git config (or git programs) a command sees.
const CONFIG_ENV = /^(?:GIT_[A-Za-z0-9_]*|HOME|XDG_CONFIG_HOME)=/
const base = (w: string) => w.slice(w.lastIndexOf('/') + 1)
// `git`, or any path to it (`/usr/bin/git`, `./git`, `bin/git`).
const isGit = (w: string) => base(w) === 'git'

// The key guard.tsx reads an alias by: where git runs and the name.
export const aliasKey = (cwd: string, name: string) => `${cwd}\0${name}`

// What `git config --get alias.<name>` said, by aliasKey: the value, or null
// (not an alias). A key not here has not been read.
export type Aliases = ReadonlyMap<string, string | null>

type Reader = { home: string | undefined; aliases: Aliases; ops: GitOp[] }

// The git add / commit / push commands in a Bash command line, in order.
// Commands it reaches through a wrapper it cannot fully read (xargs, find
// -exec, a shell alias, a command it does not know that names git and a
// verb) come back unreadable, which asks. `aliases`: what guard.tsx read of
// git aliases; an unread one comes back as an op with `alias` set, which
// asks unless guard.tsx reads it.
export function parseGitOps(command: string, cwd: string, home?: string, aliases: Aliases = new Map()): GitOp[] {
  const r: Reader = { home, aliases, ops: [] }
  readLine(r, command, normalize(cwd), 0, false)
  return r.ops
}

// Reads a command line from `dir`; returns where it leaves the shell (`cd`).
// `strict`: a string that may only be text (an argument to a command the
// reader does not know): only a command line that starts with git counts.
function readLine(r: Reader, command: string, dir: string, depth: number, strict: boolean): string {
  if (depth > MAX_DEPTH) {
    // Too deep to read. Its words naming git and a verb: that op, unread.
    // Otherwise only plain words with no git in them pass; anything else (a
    // quote, escape, glob, brace or expansion can spell git unseen: `gi\t`,
    // `g?t`, `[g]it`, `{git,x}`) is an unread push, which always asks.
    const why = 'commands nested deeper than the guard reads'
    const kind = mentioned(splitCommands(command).flat())
    if (kind) r.ops.push(unreadableOp(kind, dir, command, why))
    else if (!/^[A-Za-z0-9_\-./ =:,\n\t]*$/.test(command) || /git/i.test(command)) {
      r.ops.push(unreadableOp('push', dir, command, why))
    }
    return dir
  }
  const cmds = splitShell(command)
  for (let n = 0; n < cmds.length; n++) {
    const c = cmds[n]!
    // `$(…)` and backticks run first, in a subshell.
    for (const sub of c.subs) readLine(r, sub, dir, depth + 1, false)
    dir = readCommand(r, dropRedirects(c.words, c.firstQuoted), dir, depth, strict, null)
    for (const h of c.heredocs) {
      if (!h.quoted) for (const sub of substitutions(h.body)) readLine(r, sub, dir, depth + 1, false)
      // A here-document is a command line only when a shell reads it.
      if (feedsShell(cmds, n)) readLine(r, h.body, dir, depth + 1, false)
    }
  }
  return dir
}

// The `$(…)` and backtick commands in a here-document body.
function substitutions(text: string): string[] {
  const out: string[] = []
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\\') {
      i++
      continue
    }
    if (text[i] === '$' && text[i + 1] === '(') {
      let depth = 1
      let j = i + 2
      for (; j < text.length && depth > 0; j++) {
        if (text[j] === '(') depth++
        else if (text[j] === ')') depth--
      }
      out.push(text.slice(i + 2, depth === 0 ? j - 1 : j))
      i = j - 1
    } else if (text[i] === '`') {
      const j = text.indexOf('`', i + 1)
      out.push(text.slice(i + 1, j < 0 ? text.length : j))
      i = j < 0 ? text.length : j
    }
  }
  return out
}

// True when command n, or one it pipes into, is a shell reading its
// commands from input.
function feedsShell(cmds: readonly Simple[], n: number): boolean {
  for (let k = n; k < cmds.length; k++) {
    const u = unwrap(cmds[k]!.words, '/', undefined)
    const head = u.words[u.i]
    if (head !== undefined && SHELLS.has(base(head)) && shellString(u.words, u.i) === undefined) return true
    if (!cmds[k]!.piped) return false
  }
  return false
}

// A command's words without its redirections (`< f`, `>out`, `2> err`,
// `<<EOF`): the command never sees them, so they are not paths or a remote.
// Only an operator (its fd digits included) with no quoted or escaped
// character: `">"`, `2">"` and `\\>` are words.
const REDIRECT = /^\d*(?:<<-?|<<<|<>|<&|>&|>>|>\||&>>|&>|<|>)/
function dropRedirects(words: readonly string[], firstQuoted: readonly number[]): string[] {
  const out: string[] = []
  for (let i = 0; i < words.length; i++) {
    const w = words[i]!
    const m = REDIRECT.exec(w)
    if (!m || (firstQuoted[i] ?? Infinity) < m[0].length) {
      out.push(w)
      continue
    }
    // The operator alone takes the next word as its target.
    if (m[0].length === w.length) i++
  }
  return out
}

// Looks through assignments, shell keywords and WRAPPERS to the command
// they run: its words, where it starts in them, the directory it runs in,
// and `env`: true when what comes before it can change which git config the
// command reads (a GIT_*, HOME or XDG_CONFIG_HOME assignment, env, sudo or
// doas), so guard.tsx's own config reads may not be what git sees.
function unwrap(
  words: readonly string[],
  dir: string,
  home: string | undefined,
): { words: string[]; i: number; dir: string; env: boolean } {
  let ws = [...words]
  let i = 0
  let d = dir
  let env = false
  for (let guard = 0; guard < 64 && i < ws.length; guard++) {
    const w = ws[i]!
    if (ASSIGNMENT.test(w) || KEYWORDS.has(w)) {
      if (CONFIG_ENV.test(w)) env = true
      i++
      continue
    }
    const name = base(w)
    const spec = WRAPPERS[name]
    if (!spec) break
    if (name === 'env' || name === 'sudo' || name === 'doas') env = true
    let j = i + 1
    let split: string[] | null = null
    const take = (opt: string, value: string | undefined) => {
      if (value === undefined) return
      if (spec.dir?.includes(opt)) d = resolvePath(d, value, home)
      if (spec.split?.includes(opt)) split = splitCommands(value).flat()
    }
    j = readOptions(ws, j, spec, take, name === 'env')
    if (split) {
      ws = [...(split as string[]), ...ws.slice(j)]
      i = 0
      continue
    }
    i = j + (spec.operands ?? 0)
  }
  return { words: ws, i, dir: d, env }
}

// Reads a wrapper's options from word j; returns the first word after them.
// `dashAlone`: a lone `-` is an option (env's `-`, the same as -i).
function readOptions(
  ws: readonly string[],
  from: number,
  spec: Wrapper,
  take: (opt: string, value: string | undefined) => void,
  dashAlone = false,
): number {
  let j = from
  while (j < ws.length) {
    const o = ws[j]!
    if (o === '--') return j + 1
    if (o === '-' && dashAlone) {
      j++
      continue
    }
    if (o.startsWith('--')) {
      const eq = o.indexOf('=')
      const name = eq < 0 ? o : o.slice(0, eq)
      if (eq < 0 && spec.long?.includes(name)) {
        take(name, ws[j + 1])
        j += 2
      } else {
        take(name, eq < 0 ? undefined : o.slice(eq + 1))
        j++
      }
      continue
    }
    if (o.startsWith('-') && o.length > 1) {
      let next = false
      for (let k = 1; k < o.length; k++) {
        const f = o.charAt(k)
        if (spec.attached?.includes(f)) {
          take(`-${f}`, o.slice(k + 1))
          break
        }
        if (spec.arg?.includes(f)) {
          if (k + 1 < o.length) take(`-${f}`, o.slice(k + 1))
          else {
            take(`-${f}`, ws[j + 1])
            next = true
          }
          break
        }
      }
      j += next ? 2 : 1
      continue
    }
    return j
  }
  return j
}

// The command string of `sh -c '<string>'` (and -lc, -ec, fish --command),
// or undefined when the shell is not given one.
function shellString(words: readonly string[], i: number): string | undefined {
  let j = i + 1
  let hasC = false
  while (j < words.length) {
    const o = words[j]!
    if (o === '--' || o === '-') {
      j++
      break
    }
    if (o.startsWith('--')) {
      if (o === '--command') hasC = true
      if (o === '--rcfile' || o === '--init-file' || o === '--init-command') j++
      j++
      continue
    }
    if ((o.startsWith('-') || o.startsWith('+')) && o.length > 1) {
      const flags = o.slice(1)
      if (flags.includes('c')) hasC = true
      if (flags.includes('o') || flags.includes('O')) j++
      j++
      continue
    }
    break
  }
  return hasC ? words[j] : undefined
}

// The git verb a list of words spells after a `git` word, or null.
function mentioned(words: readonly string[]): GitOp['kind'] | null {
  const g = words.findIndex(isGit)
  if (g < 0) return null
  for (const w of words.slice(g + 1)) {
    const kind = VERBS.get(w)
    if (kind) return kind
  }
  return null
}

// An op the reader knows only by its verb: an add or commit of a whole tree
// it cannot read (asks where the repo has a public remote), or a push it
// cannot place (asks).
function unreadableOp(kind: GitOp['kind'], cwd: string, text: string, why: string): GitOp {
  const op: GitOp = { kind, cwd, text, all: false, update: false, force: false, specs: [], isOpaque: false }
  // A push whose arguments were not read may go anywhere: opaque.
  if (kind === 'push') op.push = { remote: null, refspecs: [], sets: [], deleting: false, force: false, opaque: why }
  else {
    op.isOpaque = true
    op.specs.push({ raw: text, abs: cwd, unreadable: why })
  }
  return op
}

// An op reached through something that adds to it unseen. add/commit: a
// whole-tree sweep that asks. push: when it names its remote, where it goes
// is still read (a private remote passes) but not what it sends; naming none
// (or `{}`), it may go anywhere: opaque.
function blind(op: GitOp, why: string): void {
  if (op.kind === 'push') {
    const p = op.push!
    if (p.opaque) return
    if (p.remote === null || p.remote.includes('{}')) p.opaque = why
    else p.blind ??= why
    return
  }
  op.isOpaque = true
  op.specs = op.specs.filter(s => s.raw !== '{}')
  if (!op.specs.some(s => s.unreadable === why)) op.specs.push({ raw: op.text, abs: op.cwd, unreadable: why })
}

// One simple command. `wrapped`: why the command it reaches cannot be read
// whole (xargs, find -exec), or null. Returns where the shell is after it.
function readCommand(
  r: Reader,
  words: readonly string[],
  dir: string,
  depth: number,
  strict: boolean,
  wrapped: string | null,
): string {
  const u = unwrap(words, dir, r.home)
  const head = u.words[u.i]
  if (head === undefined) return dir
  const name = base(head)
  const rest = u.words.slice(u.i)
  const blindFrom = (mark: number, why: string) => {
    for (const op of r.ops.slice(mark)) blind(op, why)
  }
  if (head === 'cd' || head === 'pushd') {
    const target = u.words.slice(u.i + 1).find(w => !w.startsWith('-'))
    return target === undefined ? normalize(r.home ?? dir) : resolvePath(dir, target, r.home)
  }
  if (isGit(head)) {
    const mark = r.ops.length
    readGit(r, u.words, u.i, u.dir, depth, u.env)
    if (wrapped) blindFrom(mark, wrapped)
    return dir
  }
  if (name === 'xargs') {
    const j = readOptions(u.words, u.i + 1, XARGS, () => {})
    readCommand(r, u.words.slice(j), u.dir, depth, strict, 'xargs adds arguments the guard cannot read')
    return dir
  }
  if (name === 'find') {
    for (let j = u.i + 1; j < u.words.length; j++) {
      const w = u.words[j]!
      if (w !== '-exec' && w !== '-execdir' && w !== '-ok' && w !== '-okdir') continue
      const end = u.words.findIndex((x, k) => k > j && (x === ';' || x === '+'))
      const stop = end < 0 ? u.words.length : end
      readCommand(r, u.words.slice(j + 1, stop), u.dir, depth, strict, `find ${w} runs it on paths the guard cannot list`)
      j = stop
    }
    return dir
  }
  if (SHELLS.has(name)) {
    const s = shellString(u.words, u.i)
    if (s !== undefined) {
      const mark = r.ops.length
      readLine(r, s, u.dir, depth + 1, false)
      if (wrapped) blindFrom(mark, wrapped)
    }
    return dir
  }
  if (name === 'eval') {
    const mark = r.ops.length
    const after = readLine(r, u.words.slice(u.i + 1).join(' '), u.dir, depth + 1, false)
    if (wrapped) blindFrom(mark, wrapped)
    return after
  }
  // A command named by a shell expansion (`"$G" add .env`) may be git: with
  // a git verb anywhere among its arguments (after -C or -c too), it asks.
  if (hasExpansion(head)) {
    const kind = rest
      .slice(1)
      .map(w => (w === 'subtree' ? 'push' : VERBS.get(w)))
      .find(k => k !== undefined)
    if (kind) {
      r.ops.push(unreadableOp(kind, u.dir, rest.join(' '), `\`${head}\` is a shell expansion that may be git`))
      return dir
    }
  }
  if (INERT.has(name)) return dir
  // A command the reader does not know that runs git with a verb (`watch git
  // push`, `parallel git add ::: x`): it cannot tell what git gets.
  const why = `\`${name}\` runs git in a way the guard does not read`
  if (!strict) {
    const kind = mentioned(rest)
    if (kind) {
      r.ops.push(unreadableOp(kind, u.dir, rest.join(' '), why))
      return dir
    }
  }
  // A quoted command line it hands on (`ssh host "git push"`).
  for (const w of rest.slice(1)) {
    if (!/\s/.test(w)) continue
    const mark = r.ops.length
    readLine(r, w, u.dir, depth + 1, true)
    blindFrom(mark, why)
  }
  return dir
}

// `git …` from words[i] (the git word), run from `dir`.
// `env`: what came before git can change the config it reads (unwrap).
function readGit(r: Reader, words: readonly string[], gitAt: number, dir: string, depth: number, env = false): void {
  const home = r.home
  const at = (n: number): string => words[n] ?? ''
  let gitDir = dir
  // Config this command sets for itself (`-c k=v`, `--config-env k=V`,
  // `--config-env=k=V`), as `<option> <key>`: git reads it, `git config`
  // in guard.tsx does not.
  const configKeys: string[] = []
  const keyOf = (kv: string) => kv.split('=')[0] ?? ''
  // --git-dir, --namespace or --exec-path: another repo's config, or other
  // git programs, than guard.tsx reads.
  let elsewhere = false
  let i = gitAt + 1
  // git's own options before the subcommand
  while (i < words.length && at(i).startsWith('-')) {
    const w = at(i)
    if (w === '-C') {
      gitDir = resolvePath(gitDir, words[i + 1] ?? '.', home)
      i += 2
    } else if (w === '-c' || w === '--config-env') {
      configKeys.push(`${w} ${keyOf(at(i + 1))}`)
      i += 2
    } else if (w.startsWith('--config-env=')) {
      configKeys.push(`--config-env ${keyOf(w.slice('--config-env='.length))}`)
      i++
    } else if (w === '--git-dir' || w === '--work-tree' || w === '--namespace') {
      if (w !== '--work-tree') elsewhere = true
      i += 2
    } else if (w.startsWith('--git-dir=') || w.startsWith('--namespace=') || w.startsWith('--exec-path=')) {
      elsewhere = true
      i++
    } else if (w.startsWith('--work-tree=')) {
      gitDir = resolvePath(gitDir, w.slice('--work-tree='.length), home)
      i++
    } else i++
  }
  const sub = at(i)
  const text = ['git', ...words.slice(i)].join(' ')
  // Any config given on the command line can change where or what a push
  // sends (`url.*.insteadOf` redirects a remote, `include.path` pulls in
  // remote and push settings), and the guard's own config reads cannot see
  // it.
  const overridden = (t: PushTarget) => {
    const override = configKeys[0]
    if (override !== undefined && !t.opaque) {
      t.opaque = `\`${override}\` sets git config for this push only, which can change where or what it sends, and the guard cannot check it`
    }
  }
  if (sub === 'subtree') {
    // `git subtree push -P <prefix> <repository> <ref>`: it pushes commits it
    // splits out of <prefix>, which no `git log` range here lists.
    const pos: string[] = []
    for (let j = i + 1; j < words.length; j++) {
      const w = at(j)
      if (['-P', '--prefix', '-m', '--message', '-b', '--branch', '--onto'].includes(w)) j++
      else if (!w.startsWith('-')) pos.push(w)
    }
    if (pos[0] !== 'push') return
    const t: PushTarget = { remote: pos[1] ?? null, refspecs: [], sets: [], deleting: false, force: false, opaque: null }
    const unread = pos.slice(1).find(hasExpansion)
    if (unread !== undefined) t.opaque = `the push target \`${unread}\` is a shell expansion`
    else if (t.remote === null) t.opaque = 'git subtree push names no remote the guard can read'
    else t.blind = 'git subtree push publishes commits split out of a folder, which the guard cannot list'
    overridden(t)
    r.ops.push({ kind: 'push', cwd: gitDir, text, all: false, update: false, force: false, specs: [], isOpaque: false, push: t })
    return
  }
  const kind = VERBS.get(sub) ?? null
  if (!kind) {
    if (sub === '' || GIT_COMMANDS.has(sub) || !ALIAS_NAME.test(sub)) return
    // Not a git command: an alias, or a `git-<name>` program.
    const why = `\`git ${sub}\` is not a git command the guard knows, and it could not read what the alias runs`
    if (depth >= MAX_DEPTH) {
      r.ops.push(unreadableOp('commit', gitDir, text, why))
      return
    }
    if (configKeys.length || elsewhere || env) {
      // Config set on the command line, another git dir, or an environment
      // that changes which config git reads: guard.tsx's read of the alias
      // would not be what git sees.
      r.ops.push(
        unreadableOp('commit', gitDir, text, `\`git ${sub}\` runs with config the guard cannot read, so it cannot tell what it does`),
      )
      return
    }
    const key = aliasKey(gitDir, sub)
    if (!r.aliases.has(key)) {
      r.ops.push({ ...unreadableOp('commit', gitDir, text, why), alias: sub })
      return
    }
    const value = r.aliases.get(key)
    if (value === null || value === undefined) {
      // Not an alias: git runs a `git-<name>` program from PATH, which can do
      // anything. It asks.
      r.ops.push(unreadableOp('commit', gitDir, text, `\`git ${sub}\` runs a program outside git, so the guard cannot tell what it does`))
      return
    }
    const mark = r.ops.length
    if (value.startsWith('!')) {
      // A shell alias runs from the repo root with the arguments appended.
      readLine(r, value.slice(1), gitDir, depth + 1, false)
      for (const op of r.ops.slice(mark)) blind(op, `\`git ${sub}\` is a shell alias, which the guard cannot read whole`)
      return
    }
    const expanded = ['git', ...words.slice(gitAt + 1, i), ...splitCommands(value).flat(), ...words.slice(i + 1)]
    readGit(r, expanded, 0, dir, depth + 1, env)
    return
  }
  const op: GitOp = {
    kind,
    cwd: gitDir,
    text,
    all: false,
    update: false,
    force: false,
    specs: [],
    isOpaque: false,
  }
  if (kind === 'push') {
    op.push = parsePushTarget(words, i + 1)
    overridden(op.push)
    r.ops.push(op)
    return
  }
  let onlyPaths = false
  for (let j = i + 1; j < words.length; j++) {
    const w = at(j)
    if (!onlyPaths && w === '--') {
      onlyPaths = true
      continue
    }
    if (!onlyPaths && w.startsWith('--')) {
      if (w === '--all' || w === '--no-ignore-removal') op.all = true
      else if (w === '--update') op.update = true
      else if (w === '--force' && kind === 'add') op.force = true
      else if (w.startsWith('--pathspec-from-file')) op.isOpaque = true
      else if (kind === 'commit' && COMMIT_LONG_ARG.has(w)) j++
      continue
    }
    if (!onlyPaths && w.startsWith('-') && w.length > 1) {
      const flags = w.slice(1)
      for (let k = 0; k < flags.length; k++) {
        const f = flags.charAt(k)
        if (f === 'A' && kind === 'add') op.all = true
        else if (f === 'a' && kind === 'commit') op.all = true
        else if (f === 'u' && kind === 'add') op.update = true
        else if (f === 'f' && kind === 'add') op.force = true
        else if (kind === 'commit' && COMMIT_SHORT_ARG.has(f)) {
          if (k === flags.length - 1) j++
          break
        }
      }
      continue
    }
    if (hasExpansion(w)) {
      op.isOpaque = true
      op.specs.push({ raw: w, abs: gitDir, unreadable: 'a shell expansion the guard cannot read' })
      continue
    }
    if (w.startsWith(':') || /[*?[]/.test(w)) {
      op.isOpaque = true
      op.specs.push({ raw: w, abs: gitDir })
      continue
    }
    op.specs.push({ raw: w, abs: w.startsWith(GUARD.notesPrefix) ? w : resolvePath(gitDir, w, home) })
  }
  // A glob with -f can stage ignored files, which status does not list.
  if (op.force) {
    for (const s of op.specs) {
      if (!s.unreadable && (s.raw.startsWith(':') || /[*?[]/.test(s.raw))) {
        s.unreadable = 'a pattern with -f, which can stage ignored files the guard cannot list'
      }
    }
  }
  r.ops.push(op)
}

// git push options that take the next word as their value.
const PUSH_LONG_ARG = new Set(['--repo', '--push-option', '--receive-pack', '--exec'])

// `git push [options] [<repository> [<refspec>...]]`, from the word after
// `push`.
export function parsePushTarget(words: readonly string[], from: number): PushTarget {
  const t: PushTarget = { remote: null, refspecs: [], sets: [], deleting: false, force: false, opaque: null }
  const positional: string[] = []
  let repoOption: string | null = null
  let onlyArgs = false
  for (let j = from; j < words.length; j++) {
    const w = words[j] ?? ''
    if (!onlyArgs && w === '--') {
      onlyArgs = true
      continue
    }
    if (!onlyArgs && w.startsWith('--')) {
      const eq = w.indexOf('=')
      const name = eq < 0 ? w : w.slice(0, eq)
      const value = eq < 0 ? undefined : w.slice(eq + 1)
      if (name === '--all' || name === '--branches') t.sets.push('--branches')
      else if (name === '--mirror') t.sets.push('--all')
      else if (name === '--tags') t.sets.push('--tags')
      else if (name === '--delete') t.deleting = true
      else if (name === '--force' || name === '--force-with-lease' || name === '--force-if-includes') t.force = true
      else if (PUSH_LONG_ARG.has(name)) {
        const v = value ?? words[++j]
        if (name === '--repo') repoOption = v ?? null
      }
      continue
    }
    if (!onlyArgs && w.startsWith('-') && w.length > 1) {
      const flags = w.slice(1)
      for (let k = 0; k < flags.length; k++) {
        const f = flags.charAt(k)
        if (f === 'd') t.deleting = true
        else if (f === 'f') t.force = true
        else if (f === 'o') {
          if (k === flags.length - 1) j++
          break
        }
      }
      continue
    }
    positional.push(w)
  }
  t.remote = positional[0] ?? repoOption
  // `tag <name>` is git's spelling of refs/tags/<name>.
  const rest = positional.slice(1)
  for (let k = 0; k < rest.length; k++) {
    const r = rest[k] ?? ''
    if (r === 'tag' && k + 1 < rest.length) {
      t.refspecs.push(`refs/tags/${rest[++k]}`)
    } else t.refspecs.push(r)
  }
  const unread = [...positional, repoOption ?? ''].find(hasExpansion)
  if (unread !== undefined) t.opaque = `the push target \`${unread}\` is a shell expansion`
  return t
}

// What a push would publish, as a `git log` revision range, or why the guard
// cannot tell (ask), or why it publishes nothing to a public repo (pass).
// `dsts`: where on the remote each source goes, as git names it, or
// PUSH_DST (a bare push's own destination) or CURRENT_DST (the current
// branch's name); null when a ref set (--all, --tags) sends refs the guard
// cannot list. `force`: a forced push or a `+` refspec. `urls`: every
// guarded push URL of `remote` (`url` is the one named).
// `urls`: the destination URL(s) the push resolved to before it turned
// opaque; absent: the guard could not resolve where it goes.
export type PushPlan =
  | { kind: 'revs'; remote: string; url: string; urls: string[]; revs: string[]; dsts: string[] | null; force: boolean }
  | { kind: 'none'; why: string }
  | { kind: 'opaque'; why: string; urls?: string[] }

// What GitHub said about a remote URL (`gh repo view --json isPrivate`), by
// URL. A URL not in it is one the guard could not confirm private: guarded.
// 'slow': gh ran but GitHub did not answer within GH_WAIT_MS; unconfirmed
// too (guarded), and the words say why.
export type Visibility = ReadonlyMap<string, 'public' | 'private' | 'slow'>
export const GH_WAIT_MS = 5_000

// Why a `gh repo view` run rejected, from `$.process.run`'s words and how
// long it took. The engine (2.1.288) rejects with "... failed to start: ..."
// when the binary cannot be spawned at that path, and "... aborted: still
// running after <n>ms" when it timed out. 'absent' means try the next path;
// the rest mean gh ran, so another path (the same gh) would only wait again.
// Words in neither form (another engine's, or a test's) read as absent only
// when the rejection came back fast, else as a timeout.
export function ghFailure(text: string, tookMs: number): 'absent' | 'timeout' | 'other' {
  if (/\bfailed to start\b/.test(text)) return 'absent'
  if (/\bstill running after\b/.test(text)) return 'timeout'
  if (/\baborted\b/.test(text)) return 'other'
  return tookMs < GH_WAIT_MS / 2 ? 'absent' : 'timeout'
}
const UNCONFIRMED: Visibility = new Map()

// A github.com URL githubRepo reads: public unless GitHub said private. Any
// other URL with "github" anywhere in it (ssh with a port, http://, git://,
// an extra path segment, a host that only mentions github.com) is GitHub but
// unconfirmed: guarded, never asked, never kept. Without "github" in the text
// it is not guarded; that leaves an ssh-config host alias or a git
// `url.*.insteadOf` rewrite whose text has no "github" unguarded, as it
// always was.
const isPublic = (url: string, seen: Visibility) =>
  githubRepo(url) !== null ? seen.get(url) !== 'private' : /github/i.test(url)

// `owner/repo` of a remote URL whose host is github.com, or null (gh is not
// asked about it). Only these forms: `https://[user@]github.com/o/r`,
// `ssh://[user@]github.com/o/r` and scp's `[user@]github.com:o/r`, each with
// an optional `.git` and trailing `/`.
const GITHUB_URL =
  /^(?:(?:https|ssh):\/\/(?:[^@/\s]+@)?github\.com\/|(?:[^@/\s:]+@)?github\.com:)([A-Za-z0-9-]+)\/([A-Za-z0-9._-]+?)(?:\.git)?\/?$/i
export function githubRepo(url: string): string | null {
  const m = GITHUB_URL.exec(url)
  return m ? `${m[1]}/${m[2]}` : null
}

// The URL a remote fetches from (its first `(fetch)` line), which is what its
// remote-tracking refs describe; undefined when `git remote -v` has none.
export function remoteFetchUrl(remotes: string, remote: string): string | undefined {
  for (const line of remotes.split('\n')) {
    const [name, url, kind] = line.split(/\s+/)
    if (name === remote && url && kind !== '(push)') return url
  }
  return undefined
}

// True when two URLs name the same GitHub repository (githubRepo, ignoring
// case). A URL githubRepo cannot read never matches.
export function sameRepo(a: string | undefined, b: string | undefined): boolean {
  const x = a === undefined ? null : githubRepo(a)
  const y = b === undefined ? null : githubRepo(b)
  return x !== null && y !== null && x.toLowerCase() === y.toLowerCase()
}

// Remote name -> every URL a push to it goes to, from `git remote -v`: its
// `(push)` lines (git pushes to each), else its fetch URL.
export function remotePushUrls(remotes: string): Map<string, string[]> {
  const push = new Map<string, string[]>()
  const fetch = new Map<string, string[]>()
  for (const line of remotes.split('\n')) {
    const [name, url, kind] = line.split(/\s+/)
    if (!name || !url) continue
    const into = kind === '(push)' ? push : fetch
    into.set(name, [...(into.get(name) ?? []), url])
  }
  for (const [name, urls] of fetch) if (!push.has(name)) push.set(name, urls)
  return push
}

// What git config says a push with no refspec and no ref set sends:
// `git config --get-all remote.<remote>.push` (one refspec a line, [] when
// unset), `git config --get push.default` (null when unset) and
// `git config --type=bool --get remote.<remote>.mirror` (false when unset).
export type PushConfig = { remotePush: string[]; pushDefault: string | null; mirror: boolean }

// push.default values that send the current branch only, which the HEAD plan
// covers. Unset is git's own `simple`; `tracking` is git's old name for
// `upstream`.
const ONE_BRANCH_DEFAULTS = new Set(['simple', 'current', 'upstream', 'tracking'])

// The remote a push goes to: as written, else where git says the branch
// pushes, else `origin`.
export const pushRemoteName = (t: PushTarget, defaultRemote: string | null): string =>
  t.remote ?? defaultRemote ?? 'origin'

// True when what the push sends is decided by git config, not the command:
// no refspec and no ref-set option. guard.tsx reads PushConfig only then.
export const needsPushConfig = (t: PushTarget): boolean =>
  !t.opaque && !t.blind && !t.deleting && !t.refspecs.length && !t.sets.length

// Source revisions for `git log` from a list of refspecs, with where each
// goes, or why the guard cannot resolve them. `where` names the list in the
// why.
function refspecSources(refspecs: readonly string[], where: string): { srcs: string[]; dsts: string[] } | { why: string } {
  const srcs: string[] = []
  const dsts: string[] = []
  for (const r of refspecs) {
    const spec = r.startsWith('+') ? r.slice(1) : r
    if (spec.startsWith('^')) continue // a negative refspec excludes, publishes nothing
    // `:` alone is git's "matching" refspec: every branch both sides have.
    if (spec === ':') return { why: `${where} \`${r}\` pushes every matching branch, which the guard did not check` }
    const colon = spec.indexOf(':')
    const src = colon < 0 ? spec : spec.slice(0, colon)
    if (src === '') continue // `:dst` deletes dst
    if (/[*?[]/.test(src) || src.startsWith('-')) {
      return { why: `${where} \`${r}\` is a pattern the guard cannot resolve` }
    }
    srcs.push(src === '@' ? 'HEAD' : src)
    // No `:dst`: the same ref on the remote; HEAD or `@` alone, the current
    // branch's name (CURRENT_DST). An explicit `:HEAD` stays as written.
    dsts.push(colon >= 0 ? spec.slice(colon + 1) : src === 'HEAD' || src === '@' ? CURRENT_DST : src)
  }
  return { srcs, dsts }
}

// Destinations the guard makes up, never ones a command or config can spell
// (a ref name cannot hold a NUL): the current branch's own name, and where a
// bare push goes (guard.tsx asks git for `%(push)`).
export const CURRENT_DST = '\0current-branch'
export const PUSH_DST = '\0push'

// The remote-tracking ref that stands for what a push destination already
// has on `remote` (`refs/remotes/<remote>/<branch>`), or null when the guard
// cannot name one: a tag or other ref, PUSH_DST (guard.tsx asks git for
// that one), CURRENT_DST with no current branch, or an explicit destination
// named HEAD (`refs/remotes/<remote>/HEAD` is the remote's default branch,
// not that ref). Never a different branch.
export function destinationBase(remote: string, dst: string, headRef: string | null): string | null {
  if (dst === PUSH_DST) return null
  let name = dst === CURRENT_DST ? headRef ?? '' : dst
  if (name.startsWith('refs/heads/')) name = name.slice('refs/heads/'.length)
  else if (name.startsWith('refs/') || name.includes('@{') || name.includes('\0')) return null
  return name && name !== 'HEAD' ? `refs/remotes/${remote}/${name}` : null
}

// `defaultRemote`: where a bare `git push` goes from this branch
// (`%(push:remotename)`), null when git names none (then `origin`).
// `config`: PushConfig for that remote, null when it could not be read. It is
// used only when needsPushConfig(t); then null asks (opaque).
export function pushPlan(
  t: PushTarget,
  remotes: string,
  defaultRemote: string | null,
  config: PushConfig | null,
  seen: Visibility = UNCONFIRMED,
  cfg: GuardConfig = GUARD,
): PushPlan {
  if (t.opaque) return { kind: 'opaque', why: t.opaque }
  if (t.deleting) return { kind: 'none', why: 'a delete publishes nothing' }
  const remote = pushRemoteName(t, defaultRemote)
  const urls = remotePushUrls(remotes).get(remote)
  if (urls === undefined) {
    // Not a named remote: a URL or path as written.
    if (!isPublic(remote, seen)) return { kind: 'none', why: `${remote} is not a public repo` }
    return {
      kind: 'opaque',
      why: `the push goes to ${remote}, not a named remote, so the guard cannot tell what it already has`,
      urls: [remote],
    }
  }
  // git pushes to every push URL: guarded when any one is public or
  // unconfirmed, and named by a confirmed public one first.
  const guarded = urls.filter(u => isPublic(u, seen))
  const url = guarded.find(u => seen.get(u) === 'public') ?? guarded[0]
  if (url === undefined) return { kind: 'none', why: `${remote} is not a public repo` }
  // From here the destination is known: an opaque answer names its URL(s).
  const opaque = (why: string): PushPlan => ({ kind: 'opaque', why, urls: guarded })
  // Where it goes is read, what it sends is not: a guarded destination asks.
  if (t.blind) return opaque(t.blind)
  // The remote's tracking refs describe what it fetches from. A guarded push
  // URL that is another repository: they say nothing about what it has.
  const fetchUrl = remoteFetchUrl(remotes, remote)
  const other = guarded.filter(u => !sameRepo(u, fetchUrl))
  if (other.length) {
    return {
      kind: 'opaque',
      why: `${remote} pushes to ${other[0]}, not the repository it fetches from, so the guard cannot tell what that one already has`,
      urls: other,
    }
  }
  let srcs: string[]
  let dsts: string[]
  if (needsPushConfig(t)) {
    // No refspec, no ref set: git config decides what goes.
    if (config === null) return opaque("the guard could not read git's push settings, so it cannot tell which branches go")
    if (config.mirror) return opaque('this remote is a mirror, so a bare push sends every branch')
    if (config.remotePush.length) {
      // remote.<name>.push stands in for the refspecs.
      const read = refspecSources(config.remotePush, `remote.${remote}.push`)
      if ('why' in read) return opaque(read.why)
      if (!read.srcs.length) return { kind: 'none', why: 'nothing is published' }
      srcs = read.srcs
      dsts = read.dsts
    } else if (config.pushDefault === null || ONE_BRANCH_DEFAULTS.has(config.pushDefault)) {
      srcs = ['HEAD']
      dsts = [PUSH_DST]
    } else {
      return opaque(
        config.pushDefault === 'matching'
          ? 'push.default=matching can send other branches the guard did not check'
          : `push.default=${config.pushDefault} is a setting the guard does not read, so it cannot tell which branches go`,
      )
    }
  } else {
    const read = refspecSources(t.refspecs, 'the refspec')
    if ('why' in read) return opaque(read.why)
    srcs = read.srcs
    dsts = read.dsts
  }
  if (!srcs.length && !t.sets.length) return { kind: 'none', why: 'nothing is published' }
  // What is new to THAT remote: every commit it already has (any of its
  // remote-tracking refs) is excluded; commits on other remotes are not.
  return {
    kind: 'revs',
    remote,
    url,
    urls: guarded,
    revs: [...srcs, ...t.sets, '--not', `--remotes=${remote}`],
    dsts: t.sets.length ? null : dsts,
    force: t.force || [...t.refspecs, ...(needsPushConfig(t) && config ? config.remotePush : [])].some(r => r.startsWith('+')),
  }
}

// One push destination, read live before the tracking refs are trusted (a
// remote can be rewound since the last fetch): its remote-tracking ref
// (`base`), the commit that ref holds here (null: none; undefined: the read
// threw or timed out), and per guarded push URL what `git ls-remote` said:
// the OID, null (no such branch there), or undefined (the read failed, timed
// out or was cut).
export type LiveRead = { base: string; tracking: string | null | undefined; live: (string | null | undefined)[] }

// A destination whose tracking ref is not what the remote has now: the live
// OID to measure against (null: the branch is gone there).
export type Stale = { base: string; oid: string | null }

// Whether the tracking refs can be trusted for these destinations, and which
// are stale; or why the guard cannot tell what the push republishes (ask).
// `here`: live OIDs that are commits in this clone; `unchecked`: live OIDs
// whose check threw or timed out.
export function liveCheck(
  reads: readonly LiveRead[],
  here: ReadonlySet<string>,
  unchecked: ReadonlySet<string> = new Set(),
): { stale: Stale[] } | { why: string } {
  const stale: Stale[] = []
  for (const r of reads) {
    const name = r.base.replace(/^refs\/remotes\/[^/]+\//, '')
    if (r.tracking === undefined) {
      return { why: `the guard could not read this clone's tracking ref for ${name}, so it cannot tell what the push republishes` }
    }
    if (r.live.some(o => o === undefined)) {
      return { why: `the guard could not read what the remote has now for ${name} (git ls-remote failed), so it cannot tell what the push republishes` }
    }
    const oids = [...new Set(r.live)]
    if (oids.length > 1) return { why: `the push URLs disagree about ${name}, so the guard cannot tell what each already has` }
    const oid = oids[0] ?? null
    if (oid === r.tracking) continue
    if (oid === null) {
      // Gone there (or never there): a new branch, judged as before, but a
      // tracking ref left behind must not hide what it held.
      stale.push({ base: r.base, oid: null })
      continue
    }
    if (unchecked.has(oid)) {
      return { why: `the guard could not check whether this clone has ${name}'s commit on the remote, so it cannot tell what the push republishes` }
    }
    if (!here.has(oid)) {
      return {
        why: `the remote's ${name} is now at ${oid.slice(0, 12)}, which this clone does not have, so the guard cannot tell what the push republishes (fetch first)`,
      }
    }
    stale.push({ base: r.base, oid })
  }
  return { stale }
}

// The publish range measured against the live remote: stale tracking refs
// are left out of `--remotes` and their live commits excluded instead.
// Accepted residuals: only the destination branches are read live, so a
// stale tracking ref for another branch of the remote can still hide commits
// through `--remotes=<remote>`; and a tag push gets no live check.
export function liveRange(plan: Extract<PushPlan, { kind: 'revs' }>, stale: readonly Stale[]): string[] {
  if (!stale.length) return plan.revs
  const at = plan.revs.indexOf('--not')
  return [
    ...plan.revs.slice(0, at),
    '--not',
    ...stale.flatMap(s => (s.oid === null ? [] : [s.oid])),
    ...stale.map(s => `--exclude=${s.base.slice('refs/remotes/'.length)}`),
    `--remotes=${plan.remote}`,
  ]
}

// ---------------------------------------------------------------------------
// Git facts, as guard.tsx reads them (all plain text from `git`).
// ---------------------------------------------------------------------------

export type RepoFacts = {
  root: string // absolute repo root (`git rev-parse --show-toplevel`)
  remotes: string // `git remote -v`
  status: string | null // `git status --porcelain=v1 -z --untracked-files=all`
  // add -f only: the ignored files its pathspecs match, repo-relative and
  // NUL-separated (`git ls-files -z --others --ignored --exclude-standard
  // --full-name`), which status does not list. null or absent on a forced
  // add: the listing failed, so the paths shown may be incomplete (ask).
  ignored?: string | null
  pushPaths: string[] | null // files changed in the commits this push publishes
  knownWorkSlugs: string[] | null // folders under newWorkFolders.root in the base tree
  // push: a destination whose committed tree could not be read, so whether a
  // docs/work/<slug>/ the push carries is new is unknown (asks).
  workBaseUnknown?: boolean
  vaultWorkNotes: boolean // newWorkFolders.file at the root says "work_notes": "vault"
  // Where that file puts the private vault; absent: no vault rule.
  vault?: VaultFacts
  visibility: Visibility // what GitHub said about the remote URLs
  // push: where it goes and what it publishes; absent: judged as any public remote.
  pushPlan?: PushPlan | null
}

export type StatusEntry = { x: string; y: string; path: string }

export function parsePorcelainZ(out: string): StatusEntry[] {
  const parts = out.split('\0')
  const entries: StatusEntry[] = []
  for (let i = 0; i < parts.length; i++) {
    const e = parts[i] ?? ''
    if (e.length < 4) continue
    const x = e.charAt(0)
    const y = e.charAt(1)
    entries.push({ x, y, path: e.slice(3) })
    if (x === 'R' || x === 'C') i++ // the original path follows
  }
  return entries
}

// The public remote URLs, or [] when the repo has none. With nothing seen,
// every URL GitHub would be asked about.
export function publicRemotes(remotes: string, seen: Visibility = UNCONFIRMED): string[] {
  const urls = new Set<string>()
  for (const line of remotes.split('\n')) {
    const url = line.split(/\s+/)[1]
    if (url && isPublic(url, seen)) urls.add(url)
  }
  return [...urls]
}

// ---------------------------------------------------------------------------
// Assessment
// ---------------------------------------------------------------------------

export type Hit = { path: string; reason: string }

export type Finding = {
  op: GitOp
  // 'ask': show the dialog. 'pass': let it run.
  verdict: 'ask' | 'pass'
  // 'git': judged with the repo's facts; 'text': from the command text alone.
  mode: 'git' | 'text'
  hits: Hit[]
  // How many paths the op would stage, commit or push (git mode).
  touched: number
  remote?: string
  // GitHub did not say `remote` is public (the guard could not ask): the
  // words say so, not "public".
  unconfirmed?: boolean
  // Unconfirmed because GitHub did not answer in time: the words say that.
  slow?: boolean
  // A push whose destination the guard could not resolve: no remote named.
  unresolved?: boolean
  // Why the paths shown may not be all the op touches, when they may not.
  incomplete?: string
  // Where the repo's kivna/vault.json puts its working notes, for the words.
  notes?: string
}

const rel = (abs: string, root: string) => (abs === root ? '' : abs.startsWith(root + '/') ? abs.slice(root.length + 1) : null)
const under = (path: string, spec: string) => spec === '' || path === spec || path.startsWith(spec + '/')

function textHits(
  op: GitOp,
  root: string | null,
  slugs: ReadonlySet<string> | null,
  home: string | undefined,
  cfg: GuardConfig,
  vault: VaultFacts,
): Hit[] {
  const hits: Hit[] = []
  // A push target the reader cannot read: ask, never pass unread.
  const unreadPush = op.push?.opaque ?? op.push?.blind
  if (unreadPush) hits.push({ path: op.text, reason: unreadPush })
  for (const s of op.specs) {
    if (s.unreadable) {
      hits.push({ path: s.raw, reason: s.unreadable })
      continue
    }
    if (s.raw.startsWith(cfg.notesPrefix)) {
      hits.push({ path: s.raw, reason: 'a vault note (notes:)' })
      continue
    }
    if (inVault(s.abs, home, vault) || (s.real !== undefined && inVault(s.real, home, vault))) {
      hits.push({ path: s.raw, reason: 'inside the private vault' })
      continue
    }
    const r = root === null ? null : rel(s.abs, root)
    // Without a root, try the spec as written, relative to where git runs.
    const candidate = r ?? (s.raw.startsWith('/') || s.raw.startsWith('~') ? null : normalize(s.raw))
    if (candidate) {
      const why = privateReason(candidate, slugs, cfg, vault.privatePaths)
      if (why) hits.push({ path: candidate, reason: why })
    }
  }
  return hits
}

// True when the op is a forced add that can stage ignored files: -f with
// -A, or with pathspecs (read or opaque, e.g. --pathspec-from-file) and not
// -u alone (-u stages nothing untracked). guard.tsx lists the ignored files
// exactly then, from the repo root when the pathspecs are opaque.
export const stagesIgnored = (op: GitOp): boolean =>
  op.kind === 'add' && op.force && (op.all || (!op.update && (op.specs.length > 0 || op.isOpaque)))

// What the op would stage, commit or push, repo-relative.
export function touchedPaths(op: GitOp, facts: RepoFacts): string[] | null {
  if (op.kind === 'push') return facts.pushPaths
  if (facts.status === null) return null
  const entries = parsePorcelainZ(facts.status)
  const specs = op.isOpaque ? [''] : op.specs.map(s => rel(s.abs, facts.root)).filter((s): s is string => s !== null)
  const matches = (p: string) => specs.some(s => under(p, s))
  if (op.kind === 'add') {
    const sweep = op.all || op.update
    if (!sweep && specs.length === 0) return []
    const listed = entries
      .filter(e => !(op.update && e.x === '?'))
      .filter(e => (specs.length ? matches(e.path) : true))
      .map(e => e.path)
    // -f also stages the ignored files its pathspecs match. git matched them
    // already; -u alone stages nothing untracked, ignored or not.
    if (stagesIgnored(op) && facts.ignored) {
      const seen = new Set(listed)
      for (const p of facts.ignored.split('\0')) if (p && !seen.has(p)) seen.add(p)
      return [...seen]
    }
    return listed
  }
  // commit
  const tracked = entries.filter(e => e.x !== '?' && e.x !== '!')
  if (specs.length) return tracked.filter(e => matches(e.path)).map(e => e.path)
  return tracked.filter(e => e.x !== ' ' || (op.all && e.y !== ' ')).map(e => e.path)
}

const notesOf = (vault: VaultFacts): Pick<Finding, 'notes'> => (vault.notes ? { notes: vault.notes } : {})

// Judges one op. `facts` null: no process access (or git failed): text mode,
// with `textVault` as the session project's kivna/vault.json says.
export function assess(
  op: GitOp,
  facts: RepoFacts | null,
  home: string | undefined,
  cfg: GuardConfig = GUARD,
  textVault: VaultFacts = NO_VAULT,
): Finding {
  // A vault path only ever adds hits: no repo or folder is let through for
  // being inside one.
  if (!facts) {
    const v = usableVault(textVault, op.cwd, home)
    const hits = [...textHits(op, null, null, home, cfg, v), ...v.unusable]
    return { op, verdict: hits.length ? 'ask' : 'pass', mode: 'text', hits, touched: 0, ...notesOf(v) }
  }
  const vault = usableVault(facts.vault ?? NO_VAULT, facts.root, home)
  const pass: Finding = { op, verdict: 'pass', mode: 'git', hits: [], touched: 0 }
  const remotes = publicRemotes(facts.remotes, facts.visibility)
  const named = remotes.find(u => facts.visibility.get(u) === 'public') ?? remotes[0]
  const plan = op.kind === 'push' ? facts.pushPlan : undefined
  if (plan) {
    // A push is judged by where it goes, not by the repo's other remotes.
    if (plan.kind === 'none') return pass
    if (plan.kind === 'opaque') {
      const hits = [{ path: op.text, reason: plan.why }]
      // Where this push goes, as resolved; never another remote of the repo.
      if (!plan.urls?.length) return { op, verdict: 'ask', mode: 'git', hits, touched: 0, unresolved: true }
      const where = plan.urls.find(u => facts.visibility.get(u) === 'public') ?? plan.urls[0]
      return { op, verdict: 'ask', mode: 'git', hits, touched: 0, remote: where, ...unsure(where, facts.visibility) }
    }
  } else if (!remotes.length) return pass
  const slugs = facts.vaultWorkNotes && facts.knownWorkSlugs ? new Set(facts.knownWorkSlugs) : null
  const hits = [...textHits(op, facts.root, slugs, home, cfg, vault), ...vault.unusable]
  const listed = touchedPaths(op, facts)
  const touched = listed ?? []
  for (const p of touched) {
    const why = privateReason(p, slugs, cfg, vault.privatePaths)
    if (why && !hits.some(h => h.path === p)) hits.push({ path: p, reason: why })
  }
  // A push destination whose committed tree was not read, or a forced push
  // (the remote may not hold what its tracking refs last saw): a work folder
  // it carries may be new there, and the guard cannot tell. Ask on those.
  if (facts.workBaseUnknown || (plan?.kind === 'revs' && plan.force)) {
    for (const p of touched) {
      const slug = workSlug(p, cfg)
      if (slug !== undefined && !hits.some(h => h.path === p)) {
        hits.push({
          path: p,
          reason: `${cfg.newWorkFolders.root}${slug}/: the guard could not read what the destination branch already has, so it cannot tell whether this work folder is new`,
        })
      }
    }
  }
  // A forced add whose ignored files could not be listed may stage a private
  // file nobody saw (`.env`); a push whose files could not be listed (git log
  // failed or was cut) may publish one: ask, and say the list may be
  // incomplete.
  const incomplete =
    stagesIgnored(op) && (facts.ignored === null || facts.ignored === undefined)
      ? INCOMPLETE_IGNORED
      : plan?.kind === 'revs' && listed === null
        ? PUSH_UNLISTED
        : undefined
  if (incomplete) hits.push({ path: op.text, reason: incomplete })
  const remote = plan?.kind === 'revs' ? plan.url : named
  return {
    op,
    verdict: hits.length ? 'ask' : 'pass',
    mode: 'git',
    hits,
    touched: touched.length,
    remote,
    ...unsure(remote, facts.visibility),
    ...(incomplete ? { incomplete } : {}),
    ...notesOf(vault),
  }
}

// A remote GitHub did not say is public: `unconfirmed`, and `slow` when
// GitHub did not answer in time.
function unsure(remote: string | undefined, seen: Visibility): Pick<Finding, 'unconfirmed' | 'slow'> {
  if (remote === undefined) return {}
  const said = seen.get(remote)
  if (said === 'public') return {}
  return said === 'slow' ? { unconfirmed: true, slow: true } : { unconfirmed: true }
}

export const PUSH_UNLISTED =
  'the guard could not list the files this push publishes, so the paths shown may be incomplete'

export const INCOMPLETE_IGNORED =
  'the guard could not list the ignored files -f would stage, so the paths shown may be incomplete'

// ---------------------------------------------------------------------------
// The dialog's words and the decision
// ---------------------------------------------------------------------------

export const SAFE = "Don't run it"
export const RUN = 'Run it'
export const HEADER = 'Private path' // the ask chip: 12 characters at most

const VERB = { add: 'stage', commit: 'commit', push: 'push' } as const

export function shortRemote(url: string | undefined): string {
  if (!url) return 'a public repo'
  const repo = githubRepo(url)
  return repo ? `github.com/${repo}` : url
}

// Where the op goes, in words: "public github.com/o/r", or, when GitHub did
// not say, that the guard could not confirm it is private (and, when GitHub
// did not answer in time, that it did not).
export function toward(findings: readonly Finding[]): string {
  const f = findings.find(x => x.remote)
  if (!f) return findings.some(x => x.unresolved) ? 'a destination the guard could not resolve' : 'a public repo'
  if (f.slow) {
    return `${shortRemote(f.remote)} (GitHub did not answer within ${Math.round(GH_WAIT_MS / 1000)} s, so the guard could not confirm it is private)`
  }
  return f.unconfirmed
    ? `${shortRemote(f.remote)} (the guard could not confirm it is private)`
    : `public ${shortRemote(f.remote)}`
}

const clip = (s: string, n: number) => (s.length > n ? s.slice(0, n - 1) + '…' : s)

export function allHits(findings: readonly Finding[]): Hit[] {
  const seen = new Map<string, Hit>()
  for (const f of findings) for (const h of f.hits) if (!seen.has(h.path)) seen.set(h.path, h)
  return [...seen.values()]
}

// The dialog question: ends in a question mark, as $.ui.ask wants.
export function question(command: string, findings: readonly Finding[]): string {
  const asks = findings.filter(f => f.verdict === 'ask')
  const hits = allHits(asks)
  const verbs = [...new Set(asks.map(f => VERB[f.op.kind]))].join('/')
  const names = hits.slice(0, 3).map(h => h.path).join(', ') + (hits.length > 3 ? ` and ${hits.length - 3} more` : '')
  const note = asks.find(f => f.incomplete)?.incomplete
  return (
    `Claude wants to run \`${clip(command.trim(), 70)}\`. It would ${verbs} ` +
    `${hits.length === 1 ? 'a private path' : `${hits.length} private paths`} (${names}) ` +
    `toward ${toward(asks)}. ` +
    (note ? `Careful: ${note}. ` : '') +
    `No answer in ${Math.round(GUARD.timeoutMs / 1000)} s counts as no. Run it?`
  )
}

export type Outcome =
  | { kind: 'answer'; answer: string; elapsedMs: number }
  | { kind: 'timeout' }
  | { kind: 'dismissed' }
  | { kind: 'error' }

export type Decision = { run: true } | { run: false; why: string }

export function decide(outcome: Outcome, cfg: GuardConfig = GUARD): Decision {
  switch (outcome.kind) {
    case 'timeout':
      return { run: false, why: `no answer in ${Math.round(cfg.timeoutMs / 1000)} s` }
    case 'dismissed':
      return { run: false, why: 'the person dismissed the dialog' }
    case 'error':
      return { run: false, why: 'the guard dialog could not be shown' }
    case 'answer': {
      const a = outcome.answer.trim()
      if (a === RUN) {
        return outcome.elapsedMs < cfg.reflexMs
          ? { run: false, why: `"${RUN}" came within ${cfg.reflexMs} ms of the dialog opening, read as a typed-ahead key` }
          : { run: true }
      }
      if (a === SAFE) return { run: false, why: `the person chose "${SAFE}"` }
      return { run: false, why: `the person answered: "${clip(a, 200)}"` }
    }
  }
}

// After a timeout the engine's dialog may still be on screen: plugins have no
// call that closes a `$.ui.ask` (no signal, no close), so the guard says so.
// The answer it gets there is ignored; nothing runs from it.
export const LATE_NOTE =
  'The guard\'s question may still be open on screen: Claude Code gives plugins no way to close it. ' +
  'Any answer given there now is ignored and runs nothing; the person can dismiss it with Esc.'

// What Claude reads when the command is refused: exactly what to do.
export function denyMessage(command: string, findings: readonly Finding[], why: string, note?: string): string {
  const asks = findings.filter(f => f.verdict === 'ask')
  const hits = allHits(asks)
  const list = hits.map(h => `${h.path} (${h.reason})`).join('; ')
  const notes = shownNotes(asks.find(f => f.notes)?.notes)
  const sweep = asks.some(
    f => f.op.all || f.op.update || f.op.isOpaque || f.op.specs.some(s => s.raw === '.' || s.raw.endsWith('/')),
  )
  return [
    `overtone guard: did not run \`${clip(command.trim(), 200)}\`: ${why}.`,
    `It would have staged, committed or pushed private paths toward ${toward(asks)}: ${list}.`,
    'What to do: stage only the files this work needs, by name (`git add <file> <file>`), never `git add -A`, `git add .` or `git commit -a` here' +
      (sweep ? ' (that is how the private paths were swept in)' : '') +
      `, and never the private paths above. If one is already staged, unstage it with \`git restore --staged <path>\`.` +
      // Only where a hit is about the vault: other repos keep no notes there.
      (hits.some(h => /vault|notes:/.test(h.reason))
        ? ` Working notes belong in the private vault (${GUARD.notesPrefix}<work>/${notes ? `, under ${notes}` : ''}), not in this repo.`
        : ''),
    'Do not retry this command or work around the check. Tell the person what you meant to commit and ask how they want it done.',
    ...(note ? [note] : []),
  ].join('\n')
}

// The evidence the band or pane draws: plain rows.
export type Evidence = {
  command: string
  remote: string
  // GitHub did not say the remote is public.
  unconfirmed?: boolean
  // The push's destination could not be resolved.
  unresolved?: boolean
  verb: string
  rows: Hit[]
  touched: number
  mode: 'git' | 'text'
  // Why the rows may not be every path the command touches.
  incomplete?: string
}

export function evidence(command: string, findings: readonly Finding[]): Evidence {
  const asks = findings.filter(f => f.verdict === 'ask')
  return {
    command: command.trim(),
    remote: shortRemote(asks.find(f => f.remote)?.remote),
    ...(asks.find(f => f.remote)?.unconfirmed ? { unconfirmed: true } : {}),
    ...(!asks.some(f => f.remote) && asks.some(f => f.unresolved) ? { unresolved: true } : {}),
    verb: [...new Set(asks.map(f => VERB[f.op.kind]))].join('/'),
    rows: allHits(asks),
    touched: asks.reduce((n, f) => n + f.touched, 0),
    mode: asks.some(f => f.mode === 'git') ? 'git' : 'text',
    ...(asks.some(f => f.incomplete) ? { incomplete: asks.find(f => f.incomplete)?.incomplete } : {}),
  }
}
