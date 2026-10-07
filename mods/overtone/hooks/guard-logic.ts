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
  // A tilde form the shell expands other than `~` and `~/` (`~-` is OLDPWD,
  // `~+`/`~N`/`~+N`/`~-N` the directory stack, `~user` another home): a
  // directory the guard cannot name, so an expansion, and it asks.
  if (p.startsWith('~')) return `\${${p}}`
  // `..` must not cancel an expansion, in the directory or the path itself
  // (`${OLDPWD}/..`, `"$X/.."` are not where they started): left unresolved,
  // it stays one, and asks.
  if (hasExpansion(p)) return p.startsWith('/') ? p : `${cwd}/${p}`
  if (!p.startsWith('/') && hasExpansion(cwd)) return `${cwd}/${p}`
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
  // `$(…)` inside double quotes whose end the reader cannot find (it never
  // closes, or a `case` inside makes a `)` ambiguous): the text from there
  // on, which asks.
  unread: string[]
  heredocs: { body: string; quoted: boolean }[]
  piped: boolean
  // Unquoted parentheses between the command before and this one, in order:
  // a `(` opens a subshell, a `)` closes it.
  parens: ('(' | ')')[]
}

// From just after `$(`: the index of the `)` that closes it, read as the
// shell reads it (quotes, escapes, nested `$(…)`, backticks, comments and
// here-document bodies), or -1 when it never closes. `ambiguous`: a `case`
// inside, whose patterns end in a `)` this scan does not pair.
function scanSub(s: string, from: number): { end: number; ambiguous: boolean } {
  let depth = 1
  let ambiguous = false
  const fail = () => ({ end: -1, ambiguous })
  const heredocs: { delim: string; strip: boolean }[] = []
  // The next character starts a word (a command word may be `case` or `#`).
  let atWord = true
  for (let i = from; i < s.length; i++) {
    const c = s[i]!
    if (c === '\\') {
      i++
      atWord = false
      continue
    }
    if (c === "'") {
      const j = s.indexOf("'", i + 1)
      if (j < 0) return fail()
      i = j
      atWord = false
      continue
    }
    if (c === '"') {
      const j = dquoteEnd(s, i + 1)
      if (j < 0) return fail()
      i = j
      atWord = false
      continue
    }
    if (c === '`') {
      const j = backtickEnd(s, i + 1)
      if (j < 0) return fail()
      i = j
      atWord = false
      continue
    }
    if (c === '$' && s[i + 1] === '(') {
      const r = scanSub(s, i + 2)
      if (r.end < 0) return fail()
      ambiguous ||= r.ambiguous
      i = r.end
      atWord = false
      continue
    }
    if (c === '<' && s[i + 1] === '<' && s[i + 2] === '<') {
      i += 2
      atWord = true
      continue
    }
    if (c === '<' && s[i + 1] === '<') {
      // A here-document: its delimiter, quotes removed; the body is skipped
      // at the next newline.
      let j = i + 2
      const strip = s[j] === '-'
      if (strip) j++
      while (s[j] === ' ' || s[j] === '\t') j++
      let delim = ''
      for (; j < s.length && !/[\s;&|()<>]/.test(s[j]!); j++) {
        const d = s[j]!
        if (d === "'" || d === '"') {
          const k = s.indexOf(d, j + 1)
          if (k < 0) return fail()
          delim += s.slice(j + 1, k)
          j = k
        } else if (d === '\\') {
          delim += s[j + 1] ?? ''
          j++
        } else delim += d
      }
      heredocs.push({ delim, strip })
      i = j - 1
      atWord = false
      continue
    }
    if (c === '\n') {
      let at = i + 1
      while (heredocs.length) {
        const h = heredocs.shift()!
        let closed = false
        while (at < s.length) {
          const nl = s.indexOf('\n', at)
          const line = nl < 0 ? s.slice(at) : s.slice(at, nl)
          at = nl < 0 ? s.length : nl + 1
          if ((h.strip ? line.replace(/^\t+/, '') : line) === h.delim) {
            closed = true
            break
          }
        }
        if (!closed) return fail()
      }
      i = at - 1
      atWord = true
      continue
    }
    if (c === '#' && atWord) {
      const nl = s.indexOf('\n', i)
      if (nl < 0) return fail()
      i = nl - 1
      continue
    }
    if (c === '(') {
      depth++
      atWord = true
      continue
    }
    if (c === ')') {
      depth--
      if (depth === 0) return { end: i, ambiguous }
      atWord = true
      continue
    }
    if (/[\s;&|]/.test(c)) {
      atWord = true
      continue
    }
    if (atWord && /^case(?:[\s;&|()]|$)/.test(s.slice(i, i + 5))) ambiguous = true
    atWord = false
  }
  return fail()
}

// From just after an opening `"`: the index of its closing `"`, or -1.
function dquoteEnd(s: string, from: number): number {
  for (let j = from; j < s.length; j++) {
    const c = s[j]
    if (c === '\\') j++
    else if (c === '"') return j
    else if (c === '`') {
      j = backtickEnd(s, j + 1)
      if (j < 0) return -1
    } else if (c === '$' && s[j + 1] === '(') {
      j = scanSub(s, j + 2).end
      if (j < 0) return -1
    }
  }
  return -1
}

// From just after an opening backtick: the index of its closing one, or -1.
function backtickEnd(s: string, from: number): number {
  let j = from
  while (j < s.length && s[j] !== '`') j += s[j] === '\\' ? 2 : 1
  return j < s.length ? j : -1
}

// Splits a command line into simple commands, each a list of words. Splits on
// unquoted `&&`, `||`, `;`, `|`, `&`, newlines and parentheses. Not a shell:
// no expansion; `$(...)` inside double quotes stays one word.
export function splitCommands(command: string): string[][] {
  return splitShell(command).map(c => c.words)
}

function splitShell(command: string): Simple[] {
  const commands: Simple[] = []
  const fresh = (): Simple => ({ words: [], firstQuoted: [], subs: [], unread: [], heredocs: [], piped: false, parens: [] })
  let cur = fresh()
  let word = ''
  let hasWord = false
  // The word had a quote or an escape (a quoted here-doc delimiter).
  let wordQuoted = false
  let quote: '"' | "'" | null = null
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
    // Parentheses with no command yet carry on to the next one.
    const carry = cur.words.length ? [] : cur.parens
    if (cur.words.length) {
      cur.piped = piped
      commands.push(cur)
    }
    cur = fresh()
    cur.parens = carry
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
        // A command substitution runs: read to its own end, quotes and all.
        const s = scanSub(command, i + 2)
        if (s.end < 0 || s.ambiguous) cur.unread.push(command.slice(i + 2))
        else cur.subs.push(command.slice(i + 2, s.end))
        const end = s.end < 0 ? command.length - 1 : s.end
        word += command.slice(i, end + 1)
        i = end
        continue
      }
      if (c === '`') {
        // So does a backtick command inside double quotes.
        const j = backtickEnd(command, i + 1)
        const end = j < 0 ? command.length : j
        cur.subs.push(command.slice(i + 1, end))
        word += command.slice(i, end + 1)
        i = end
        continue
      }
      if (c === '"') {
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
    // An unquoted redirection operator ends the word before it unless that
    // word is a file descriptor (unquoted digits): `.env>/dev/null` is the
    // path `.env` and a redirection, `2>&1` one redirection. The operator
    // and its attached target are one word, which dropRedirects removes.
    const opStarts = (c === '<' || c === '>' || (c === '&' && command[i + 1] === '>'))
    if (opStarts && hasWord && !(/^\d+$/.test(word) && firstQuoted === Infinity)) endWord()
    if (c === '&' && command[i + 1] === '>') {
      word += '&>'
      i++
      if (command[i + 1] === '>') {
        word += '>'
        i++
      }
      hasWord = true
      continue
    }
    if ((c === '<' || c === '>') && !(c === '<' && command[i + 1] === '<')) {
      word += c
      const n = command[i + 1]
      if ((c === '>' && (n === '>' || n === '|' || n === '&')) || (c === '<' && (n === '&' || n === '>'))) {
        word += n
        i++
      }
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
      if (c === '(' || c === ')') cur.parens.push(c)
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
  // commit: -i/--include (the staged index as well as the named paths).
  include?: boolean
  // commit: -o/--only (the named paths alone; with none, as with --amend,
  // nothing staged is committed).
  only?: boolean
  // add -n/--dry-run, commit --dry-run (or --short, --porcelain, --long,
  // which imply it): it stages or commits nothing.
  dryRun?: boolean
  // Why git runs in a repository the guard cannot name (find -execdir, `git
  // -C {}`): it asks, whatever the caller's repo is.
  unknownRepo?: string
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
  // Every folder a `cd` or `pushd` moved the shell to before this op, in this
  // line. One that is not a folder (`cd /typo`, `cd README.md`) fails, and
  // the shell stays where it was, however the line moves on (`cd ..`):
  // guard.tsx asks.
  via?: string[]
}

const COMMIT_SHORT_ARG = new Set(['m', 'F', 'C', 'c', 't'])
// commit's short options whose value can only be attached (`-uno`, `-S<key>`):
// the rest of the word is the value, never more flags.
const COMMIT_SHORT_ATTACHED = new Set(['u', 'S'])

// The long options of add, commit and push (git 2.54, `git <cmd>
// --git-completion-helper-all`), positive forms; `=`: takes a value
// (`--x=v` or `--x v`). git also reads `--no-<name>`, and for a `no-<name>`
// option `--<name>`, as the negation, and any unique prefix of either.
const longTable = (names: string): ReadonlyMap<string, boolean> =>
  new Map(names.split(' ').map(n => [n.replace(/=$/, ''), n.endsWith('=')]))
const LONG: Record<GitOp['kind'], ReadonlyMap<string, boolean>> = {
  add: longTable(
    'dry-run verbose interactive patch auto-advance unified= inter-hunk-context= edit force update renormalize ' +
      'intent-to-add all ignore-removal refresh ignore-errors ignore-missing sparse chmod= warn-embedded-repo ' +
      'pathspec-from-file= pathspec-file-nul',
  ),
  commit: longTable(
    'quiet verbose file= author= date= message= reedit-message= reuse-message= fixup= squash= reset-author ' +
      'trailer= signoff template= edit cleanup= status gpg-sign all include interactive patch unified= ' +
      'inter-hunk-context= only no-verify dry-run short branch ahead-behind porcelain long null amend ' +
      'no-post-rewrite untracked-files pathspec-from-file= pathspec-file-nul allow-empty allow-empty-message',
  ),
  push: longTable(
    'verbose quiet repo= all branches mirror delete tags dry-run porcelain force force-with-lease force-if-includes ' +
      'recurse-submodules= thin receive-pack= exec= set-upstream progress prune no-verify follow-tags signed atomic ' +
      'push-option= ipv4 ipv6',
  ),
}
// The options whose reading changes what the guard decides (and every one
// that takes a value, which moves the words after it): an abbreviation that
// could be one of them and another option is not guessed at.
const MATTERS: Record<GitOp['kind'], ReadonlySet<string>> = {
  add: new Set([
    'all', 'ignore-removal', 'update', 'force', 'dry-run', 'edit', 'interactive', 'patch', 'pathspec-from-file', 'unified',
    'inter-hunk-context', 'chmod',
  ]),
  commit: new Set([
    'all', 'include', 'only', 'dry-run', 'short', 'porcelain', 'long', 'pathspec-from-file', 'file', 'author', 'date',
    'message', 'reedit-message', 'reuse-message', 'fixup', 'squash', 'trailer', 'template', 'cleanup', 'unified',
    'inter-hunk-context',
  ]),
  push: new Set([
    'repo', 'all', 'branches', 'mirror', 'delete', 'tags', 'force', 'force-with-lease', 'force-if-includes',
    'recurse-submodules', 'receive-pack', 'exec', 'push-option',
  ]),
}

export type LongRead =
  | { name: string; negated: boolean; value: string | undefined; takes: boolean }
  | { ambiguous: { name: string; negated: boolean }[] }
  | null

// A long option word (`--for`, `--no-de`, `--message=x`) as git reads it
// against `known`: the option it names, exactly or by a unique prefix, and
// whether it is the `--no-` form; `ambiguous` when the prefix fits more than
// one (git refuses the command); null when it fits none (git refuses it too).
// As git's parse-options: `--no-x` negates x, `--x` negates `no-x`, and
// `--n`, `--no`, `--no-` fit every option's negation.
export function readLong(word: string, known: ReadonlyMap<string, boolean>): LongRead {
  const arg = word.slice(2)
  const eq = arg.indexOf('=')
  const key = eq < 0 ? arg : arg.slice(0, eq)
  const value = eq < 0 ? undefined : arg.slice(eq + 1)
  const hit = (name: string, negated: boolean) => ({ name, negated, value, takes: known.get(name) ?? false })
  if (key === '') return null
  for (const name of known.keys()) {
    if (key === name) return hit(name, false)
    if (key === `no-${name}`) return hit(name, true)
    if (name.startsWith('no-') && key === name.slice(3)) return hit(name, true)
  }
  const fits = new Map<string, { name: string; negated: boolean }>()
  const fit = (name: string, negated: boolean) => fits.set(`${negated ? 'no-' : ''}${name}`, { name, negated })
  for (const name of known.keys()) {
    if (name.startsWith(key)) fit(name, false)
    if ('no-'.startsWith(key)) fit(name, true)
    if (key.startsWith('no-') && name.startsWith(key.slice(3))) fit(name, true)
    if (!key.startsWith('no-') && name.startsWith('no-') && name.slice(3).startsWith(key)) fit(name, true)
  }
  const all = [...fits.values()]
  if (all.length === 1) return hit(all[0]!.name, all[0]!.negated)
  return all.length ? { ambiguous: all } : null
}

// Why the guard does not guess at an ambiguous long option of `kind`, or
// null when none of what it could be changes anything the guard reads.
function ambiguousWhy(word: string, read: { ambiguous: { name: string; negated: boolean }[] }, kind: GitOp['kind']): string | null {
  if (!read.ambiguous.some(c => MATTERS[kind].has(c.name))) return null
  const names = read.ambiguous.map(c => `--${c.negated ? 'no-' : ''}${c.name}`).slice(0, 3).join(', ')
  return `\`${word}\` could be more than one git ${kind} option (${names}), so the guard cannot tell which`
}

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
// Variables that change the config a push reads (its remotes, push URLs and
// push settings): the push cannot be placed.
const PUSH_ENV = /^(?:GIT_CONFIG\w*|GIT_DIR|GIT_COMMON_DIR|GIT_WORK_TREE|HOME|XDG_CONFIG_HOME)$/
// Variables that point add or commit at another repository, work tree or
// index than the one the guard reads.
const TREE_ENV = /^(?:GIT_DIR|GIT_COMMON_DIR|GIT_WORK_TREE|GIT_INDEX_FILE)$/
// Builtins that set or export shell variables for the commands after them.
const SETS_VARS = new Set(['export', 'declare', 'typeset', 'readonly', 'local'])
const base = (w: string) => w.slice(w.lastIndexOf('/') + 1)
// `git`, or any path to it (`/usr/bin/git`, `./git`, `bin/git`).
const isGit = (w: string) => base(w) === 'git'

// The key guard.tsx reads an alias by: where git runs and the name.
export const aliasKey = (cwd: string, name: string) => `${cwd}\0${name}`

// What `git config --get alias.<name>` said, by aliasKey: the value, or null
// (not an alias). A key not here has not been read.
export type Aliases = ReadonlyMap<string, string | null>

// Where git runs a shell alias (`!…`): the top of the working tree git is in,
// by aliasKey, as `git rev-parse --show-toplevel` said there. A key not here
// (not read, failed, no work tree, a bare repo) is a top the guard does not
// know, and the alias asks.
export type AliasTops = ReadonlyMap<string, string>

// `shellVars`: variables the line set or exported before (`export GIT_DIR=x;
// git add`), which the commands after it may run with. Never scoped to a
// subshell: one set anywhere counts for the rest of the line.
type Reader = { home: string | undefined; aliases: Aliases; tops: AliasTops; ops: GitOp[]; shellVars: Set<string>; visited: string[] }

// Where `cd -` (OLDPWD), `popd` and the `pushd` forms that rotate the stack
// lead is state the guard does not follow: the shell's directory becomes an
// expansion it cannot name, so every git op after it asks. (Following it was
// tried and refused: a failed or conditional `cd`, an `OLDPWD=` assignment,
// a fresh `bash -c` that inherits no stack, each put the guard somewhere the
// shell is not.)
const UNKNOWN_PREV = '${OLDPWD}'
const UNKNOWN_STACK = '${DIRSTACK}'

// The git add / commit / push commands in a Bash command line, in order.
// Commands it reaches through a wrapper it cannot fully read (xargs, find
// -exec, a shell alias, a command it does not know that names git and a
// verb) come back unreadable, which asks. `aliases`: what guard.tsx read of
// git aliases; an unread one comes back as an op with `alias` set, which
// asks unless guard.tsx reads it. `tops`: where git runs each shell alias
// from (the top of the work tree); one it does not hold asks.
export function parseGitOps(
  command: string,
  cwd: string,
  home?: string,
  aliases: Aliases = new Map(),
  tops: AliasTops = new Map(),
): GitOp[] {
  const r: Reader = { home, aliases, tops, ops: [], shellVars: new Set(), visited: [] }
  readLine(r, command, normalize(cwd), 0, false)
  // git run in a directory a shell expansion names (`cd "$DIR"`, `git -C
  // $REPO`): never "not a git repo", which would pass. It asks.
  for (const op of r.ops) {
    if (!hasExpansion(op.cwd)) continue
    const why = `git runs in \`${op.cwd}\`, a directory a shell expansion names, so the guard cannot name its repository`
    op.unknownRepo ??= why
    if (op.push) op.push.opaque ??= why
  }
  return r.ops
}

// The home folder as the shell expands it here: unknown once the line sets
// HOME itself (`HOME=/x; cd ~`).
const homeNow = (r: Reader): string | undefined => (r.shellVars.has('HOME') ? undefined : r.home)

// A directory as the shell hands it over: `~`, `$HOME` or `${HOME}` at its
// start is the home folder; with none known it stays an expansion, so the
// repo is unknown.
function expandDir(path: string, home: string | undefined): string {
  const m = /^(?:~|\$HOME|\$\{HOME\})(?=\/|$)/.exec(path)
  return m ? (home ?? '$HOME') + path.slice(m[0].length) : path
}

// Reads a command line from `dir`; returns where it leaves the shell (`cd`).
// `strict`: a string that may only be text (an argument to a command the
// reader does not know): only a command line that starts with git counts.
function readLine(r: Reader, command: string, dir: string, depth: number, strict: boolean): string {
  if (depth > MAX_DEPTH) {
    unreadText(r, command, dir, 'commands nested deeper than the guard reads')
    return dir
  }
  const cmds = splitShell(command)
  // Where each open `( … )` subshell started: a `cd` inside it ends at its
  // `)`. (A `{ …; }` group runs in this shell, so its `cd` stays.) A `)`
  // with nothing open (a `case` pattern) changes nothing.
  const opened: string[] = []
  for (let n = 0; n < cmds.length; n++) {
    const c = cmds[n]!
    const mark = r.ops.length
    for (const p of c.parens) {
      if (p === '(') opened.push(dir)
      else if (opened.length) dir = opened.pop()!
    }
    // `$(…)` and backticks run first, in a subshell.
    for (const sub of c.subs) readLine(r, sub, dir, depth + 1, false)
    for (const text of c.unread) unreadText(r, text, dir, 'a command substitution the guard cannot read to its end')
    const before = dir
    dir = readCommand(r, dropRedirects(c.words, c.firstQuoted), dir, depth, strict, null)
    // A here-document or here-string is a command line only when a shell
    // reads it, from the directory that shell runs in (`env -C`, `sudo -D`).
    const fed = feedsShell(cmds, n, before, homeNow(r))
    for (const h of c.heredocs) {
      if (!h.quoted) for (const sub of substitutions(h.body)) readLine(r, sub, before, depth + 1, false)
      if (fed !== null) readLine(r, h.body, fed, depth + 1, false)
    }
    if (fed !== null) for (const text of hereStrings(c.words, c.firstQuoted)) readLine(r, text, fed, depth + 1, false)
    for (const op of r.ops.slice(mark)) op.via ??= [...r.visited]
  }
  // A subshell still open here closes at the line's end: the shell is left
  // where it was before it.
  return opened.length ? opened[0]! : dir
}

// Text the reader cannot read as commands. Its words naming git and a verb:
// that op, unread. Otherwise only plain words with no git in them pass;
// anything else (a quote, escape, glob, brace or expansion can spell git
// unseen: `gi\t`, `g?t`, `[g]it`, `{git,x}`) is an unread push, which
// always asks.
function unreadText(r: Reader, text: string, dir: string, why: string): void {
  const kind = mentioned(splitCommands(text).flat())
  if (kind) r.ops.push(unreadableOp(kind, dir, text, why))
  else if (!/^[A-Za-z0-9_\-./ =:,\n\t]*$/.test(text) || /git/i.test(text)) {
    r.ops.push(unreadableOp('push', dir, text, why))
  }
}

// The `$(…)` and backtick commands in a here-document body. One whose end
// cannot be found takes the rest of the body.
function substitutions(text: string): string[] {
  const out: string[] = []
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\\') {
      i++
      continue
    }
    if (text[i] === '$' && text[i + 1] === '(') {
      const s = scanSub(text, i + 2)
      if (s.end < 0 || s.ambiguous) {
        out.push(text.slice(i + 2))
        break
      }
      out.push(text.slice(i + 2, s.end))
      i = s.end
    } else if (text[i] === '`') {
      const j = backtickEnd(text, i + 1)
      out.push(text.slice(i + 1, j < 0 ? text.length : j))
      if (j < 0) break
      i = j
    }
  }
  return out
}

// The here-strings a command reads (`<<< word`, `<<<word`), as words.
function hereStrings(words: readonly string[], firstQuoted: readonly number[]): string[] {
  const out: string[] = []
  for (let k = 0; k < words.length; k++) {
    const m = /^\d*<<</.exec(words[k]!)
    if (!m || (firstQuoted[k] ?? Infinity) < m[0].length) continue
    const target = words[k]!.length > m[0].length ? words[k]!.slice(m[0].length) : words[k + 1]
    if (target !== undefined) out.push(target)
  }
  return out
}

// Commands that run what they read as shell commands: `eval` and `source`
// can be handed it (`eval "$(cat)"`), and so can a shell whose -c string is
// an expansion.
const READS_COMMANDS = new Set(['eval', 'source', '.'])

// When command n, or one it pipes into, is a shell reading its commands
// from input: the directory that shell runs in (from `dir`, through env -C
// or sudo -D); otherwise null. Redirections are not the command: `<<EOF
// bash` is.
function feedsShell(cmds: readonly Simple[], n: number, dir: string, home: string | undefined): string | null {
  for (let k = n; k < cmds.length; k++) {
    const u = unwrap(dropRedirects(cmds[k]!.words, cmds[k]!.firstQuoted), dir, home)
    const head = u.words[u.i]
    if (head !== undefined) {
      const name = base(head)
      if (READS_COMMANDS.has(name)) return u.dir
      if (SHELLS.has(name)) {
        const s = shellString(u.words, u.i)
        if (s === undefined || hasExpansion(s)) return u.dir
      }
    }
    if (!cmds[k]!.piped) return null
  }
  return null
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
): { words: string[]; i: number; dir: string; env: boolean; vars: string[] } {
  let ws = [...words]
  let i = 0
  let d = dir
  let env = false
  // The names assigned before the command, bare or through env.
  const vars: string[] = []
  for (let guard = 0; guard < 64 && i < ws.length; guard++) {
    const w = ws[i]!
    if (ASSIGNMENT.test(w) || KEYWORDS.has(w)) {
      if (CONFIG_ENV.test(w)) env = true
      if (ASSIGNMENT.test(w)) vars.push(w.slice(0, w.indexOf('=')))
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
      if (spec.dir?.includes(opt)) d = resolvePath(d, expandDir(value, home), home)
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
  return { words: ws, i, dir: d, env, vars }
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

// Ops xargs or find run in a repository the guard cannot name: all of them
// (`every`: find -execdir), or each whose directory is the path the wrapper
// supplies (`{}`, an expansion). They ask, whatever the caller's repo is.
function inUnknownRepo(ops: readonly GitOp[], every: boolean, why: string): void {
  for (const op of ops) {
    if (!every && !op.cwd.includes('{}') && !hasExpansion(op.cwd)) continue
    op.unknownRepo ??= why
    // Its remote names a remote of a repo the guard has not read: never the
    // caller's, which a private origin would pass.
    if (op.push) op.push.opaque ??= why
  }
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
  const u = unwrap(words, dir, homeNow(r))
  const head = u.words[u.i]
  if (head === undefined) {
    // Assignments alone set shell variables the commands after may see (an
    // exported one, HOME, does).
    for (const v of u.vars) r.shellVars.add(v)
    return dir
  }
  const name = base(head)
  const rest = u.words.slice(u.i)
  const blindFrom = (mark: number, why: string) => {
    for (const op of r.ops.slice(mark)) blind(op, why)
  }
  if (head === 'cd' || head === 'pushd' || head === 'popd') {
    const args = u.words.slice(u.i + 1)
    // `popd`, `cd -` (OLDPWD), and a `pushd` that names no plain directory
    // (none, `+N`/`-N`, `-`, `-n`) move the shell somewhere the guard does not
    // follow: an expansion, so the git ops after it ask.
    if (head === 'popd') return UNKNOWN_STACK
    // Options as the shell reads them: known letters up to `--` or the first
    // other word, which is the target even when it starts with `-` (`cd --
    // -pub`). A target starting with `-` (`-`, `-pub`, an unknown option) or
    // a `pushd -n` is not followed: an expansion, so it asks.
    let k = 0
    let opts = ''
    const optRe = head === 'pushd' ? /^-n+$/ : /^-[LPe@]+$/
    while (k < args.length && optRe.test(args[k]!)) opts += args[k++]!.slice(1)
    if (args[k] === '--') k++
    const target = args[k]
    // A word after the target makes the shell refuse it (`cd /a -`, `pushd /a -n`): not followed either.
    if ((target !== undefined && target.startsWith('-')) || args.length > k + 1) return head === 'pushd' ? UNKNOWN_STACK : UNKNOWN_PREV
    // `+N` is a directory-stack entry (pushd; zsh's cd too).
    if (target !== undefined && /^\+\d+$/.test(target)) return UNKNOWN_STACK
    if (head === 'pushd' && (target === undefined || opts.includes('n'))) return UNKNOWN_STACK
    const to = target === undefined ? normalize(homeNow(r) ?? '$HOME') : resolvePath(dir, expandDir(target, homeNow(r)), homeNow(r))
    r.visited.push(to)
    return to
  }
  if (SETS_VARS.has(name)) {
    for (const w of rest.slice(1)) if (/^[A-Za-z_]/.test(w)) r.shellVars.add(w.split('=')[0]!)
    return dir
  }
  if (isGit(head)) {
    const mark = r.ops.length
    const sub = readGit(r, u.words, u.i, u.dir, depth, u.env, u.vars)
    if (wrapped) {
      // xargs or find -exec supplies the subcommand itself (`xargs git`,
      // `-exec git {} ;`): nothing here says what git does. It asks.
      if (r.ops.length === mark && !GIT_COMMANDS.has(sub)) {
        r.ops.push(unreadableOp('push', u.dir, rest.join(' '), `${wrapped}, and it names no git command the guard can read`))
      }
      blindFrom(mark, wrapped)
    }
    return dir
  }
  if (name === 'xargs') {
    // -I/-i/--replace: each word holding the token is replaced by what xargs
    // reads, which the guard cannot see: an expansion, never a known word.
    let token: string | null = null
    const j = readOptions(u.words, u.i + 1, XARGS, (opt, value) => {
      if (opt === '-I') token = value ?? null
      else if (opt === '-i' || opt === '--replace') token = value || '{}'
    })
    const t: string | null = token
    const inner = t ? u.words.slice(j).map(w => (w.includes(t) ? w.split(t).join('${xargs}') : w)) : u.words.slice(j)
    const mark = r.ops.length
    readCommand(r, inner, u.dir, depth, strict, 'xargs adds arguments the guard cannot read')
    inUnknownRepo(r.ops.slice(mark), false, 'xargs runs git in a directory it reads, which the guard cannot name')
    return dir
  }
  if (name === 'find') {
    for (let j = u.i + 1; j < u.words.length; j++) {
      const w = u.words[j]!
      if (w !== '-exec' && w !== '-execdir' && w !== '-ok' && w !== '-okdir') continue
      const end = u.words.findIndex((x, k) => k > j && (x === ';' || x === '+'))
      const stop = end < 0 ? u.words.length : end
      const mark = r.ops.length
      readCommand(r, u.words.slice(j + 1, stop), u.dir, depth, strict, `find ${w} runs it on paths the guard cannot list`)
      // -execdir and -okdir run it in each directory find reaches; -exec
      // with `git -C {}` or `cd {}`, in the one it names.
      inUnknownRepo(r.ops.slice(mark), w.endsWith('dir'), `find ${w} runs git in each directory it finds, which the guard cannot name`)
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
// `env`: what came before git can change the config it reads (unwrap);
// `vars`: the variables assigned before it. Returns the subcommand word.
function readGit(
  r: Reader,
  words: readonly string[],
  gitAt: number,
  dir: string,
  depth: number,
  env = false,
  vars: readonly string[] = [],
): string {
  const home = homeNow(r)
  const at = (n: number): string => words[n] ?? ''
  let gitDir = dir
  // Config this command sets for itself (`-c k=v`, `--config-env k=V`,
  // `--config-env=k=V`), as `<option> <key>`: git reads it, `git config`
  // in guard.tsx does not.
  const configKeys: string[] = []
  const keyOf = (kv: string) => kv.split('=')[0] ?? ''
  // --git-dir, --namespace or --exec-path: another repo's config, or other
  // git programs, than guard.tsx reads.
  let elsewhere: string | null = null
  // --git-dir or --work-tree: another repository or work tree than the one
  // guard.tsx reads the status of.
  let tree: string | null = null
  let i = gitAt + 1
  // git's own options before the subcommand
  while (i < words.length && at(i).startsWith('-')) {
    const w = at(i)
    const opt = w.split('=')[0]!
    if (w === '-C') {
      gitDir = resolvePath(gitDir, expandDir(words[i + 1] ?? '.', home), home)
      i += 2
    } else if (w === '-c' || w === '--config-env') {
      configKeys.push(`${w} ${keyOf(at(i + 1))}`)
      i += 2
    } else if (w.startsWith('--config-env=')) {
      configKeys.push(`--config-env ${keyOf(w.slice('--config-env='.length))}`)
      i++
    } else if (w === '--git-dir' || w === '--work-tree' || w === '--namespace') {
      if (w !== '--work-tree') elsewhere ??= w
      if (w !== '--namespace') tree ??= w
      i += 2
    } else if (w.startsWith('--git-dir=') || w.startsWith('--namespace=') || w.startsWith('--exec-path=')) {
      elsewhere ??= opt
      if (opt === '--git-dir') tree ??= opt
      i++
    } else if (w.startsWith('--work-tree=')) {
      tree ??= opt
      i++
    } else i++
  }
  const sub = at(i)
  const text = ['git', ...words.slice(i)].join(' ')
  const shellVars = [...r.shellVars]
  const pushVar = [...vars, ...shellVars].find(v => PUSH_ENV.test(v))
  const treeVar = [...vars, ...shellVars].find(v => TREE_ENV.test(v))
  // Any config given on the command line can change where or what a push
  // sends (`url.*.insteadOf` redirects a remote, `include.path` pulls in
  // remote and push settings), and the guard's own config reads cannot see
  // it; nor can they see config an environment variable points git at, or
  // another repository's.
  const overridden = (t: PushTarget) => {
    if (t.opaque) return
    const override = configKeys[0]
    if (override !== undefined) {
      t.opaque = `\`${override}\` sets git config for this push only, which can change where or what it sends, and the guard cannot check it`
    } else if (pushVar !== undefined) {
      t.opaque = `\`${pushVar}\` is set for this push, which changes the git config it reads, so the guard cannot tell where or what it sends`
    } else if (elsewhere !== null) {
      t.opaque = `\`${elsewhere}\` points this push at another repository's config, so the guard cannot tell where or what it sends`
    }
  }
  // Expansions as the subcommand (`git "$@"`, `git $CMD -f .env`): it may
  // be any verb, a push included. It asks.
  if (hasExpansion(sub)) {
    r.ops.push(unreadableOp('push', gitDir, text, `\`${sub}\` is a shell expansion that may be any git command`))
    return sub
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
    if (pos[0] !== 'push') return sub
    const t: PushTarget = { remote: pos[1] ?? null, refspecs: [], sets: [], deleting: false, force: false, opaque: null }
    const unread = pos.slice(1).find(hasExpansion)
    if (unread !== undefined) t.opaque = `the push target \`${unread}\` is a shell expansion`
    else if (t.remote === null) t.opaque = 'git subtree push names no remote the guard can read'
    else t.blind = 'git subtree push publishes commits split out of a folder, which the guard cannot list'
    overridden(t)
    r.ops.push({ kind: 'push', cwd: gitDir, text, all: false, update: false, force: false, specs: [], isOpaque: false, push: t })
    return sub
  }
  const kind = VERBS.get(sub) ?? null
  if (!kind) {
    if (sub === '' || GIT_COMMANDS.has(sub) || !ALIAS_NAME.test(sub)) return sub
    // Not a git command: an alias, or a `git-<name>` program.
    const why = `\`git ${sub}\` is not a git command the guard knows, and it could not read what the alias runs`
    if (depth >= MAX_DEPTH) {
      r.ops.push(unreadableOp('commit', gitDir, text, why))
      return sub
    }
    if (configKeys.length || elsewhere || env || shellVars.some(v => /^(?:GIT_\w*|HOME|XDG_CONFIG_HOME)$/.test(v))) {
      // Config set on the command line, another git dir, or an environment
      // that changes which config git reads: guard.tsx's read of the alias
      // would not be what git sees.
      r.ops.push(
        unreadableOp('commit', gitDir, text, `\`git ${sub}\` runs with config the guard cannot read, so it cannot tell what it does`),
      )
      return sub
    }
    const key = aliasKey(gitDir, sub)
    if (!r.aliases.has(key)) {
      r.ops.push({ ...unreadableOp('commit', gitDir, text, why), alias: sub })
      return sub
    }
    const value = r.aliases.get(key)
    if (value === null || value === undefined) {
      // Not an alias: git runs a `git-<name>` program from PATH, which can do
      // anything. It asks.
      r.ops.push(unreadableOp('commit', gitDir, text, `\`git ${sub}\` runs a program outside git, so the guard cannot tell what it does`))
      return sub
    }
    const mark = r.ops.length
    if (value.startsWith('!')) {
      // A shell alias runs from the top of the work tree git is in (not
      // from where git was run; GIT_PREFIX holds the way back) with the
      // arguments appended (git runs `sh -c '<body> "$@"'`): `!git` with
      // `add -f .env` is `git add -f .env`. Read so, and never whole; one
      // that shows no git add, commit or push still asks. The body is read
      // from where git ran AND, when it is known and different, from that
      // top; the ops of both are kept, so the alias asks if either place
      // does (a relative `-C ../x` lands somewhere else from each). With the
      // top unknown (the read failed, no work tree, a bare repo, or
      // --work-tree moved it) every op it yields also asks whatever repo it
      // lands in.
      const why = `\`git ${sub}\` is a shell alias, which the guard cannot read whole`
      const top = r.tops.get(key)
      const known = tree === null && top !== undefined && top.startsWith('/') ? normalize(top) : null
      const args = words.slice(i + 1).map(w => `'${w.replace(/'/g, `'\\''`)}'`)
      const body = [value.slice(1), ...args].join(' ')
      readLine(r, body, gitDir, depth + 1, false)
      if (known !== null && known !== gitDir) readLine(r, body, known, depth + 1, false)
      if (r.ops.length === mark) r.ops.push(unreadableOp('commit', gitDir, text, why))
      for (const op of r.ops.slice(mark)) blind(op, why)
      if (known === null) {
        const lost = `\`git ${sub}\` is a shell alias that runs from the top of the work tree, which the guard could not find, so it cannot tell which repository the alias works in`
        for (const op of r.ops.slice(mark)) {
          op.unknownRepo ??= lost
          if (op.push) op.push.opaque ??= lost
        }
      }
      return sub
    }
    const expanded = ['git', ...words.slice(gitAt + 1, i), ...splitCommands(value).flat(), ...words.slice(i + 1)]
    return readGit(r, expanded, 0, dir, depth + 1, env, vars)
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
    return sub
  }
  let onlyPaths = false
  // add -n/--dry-run, commit --dry-run; commit's status formats imply it.
  let dryRun = false
  let statusFormat = false
  // add -e/--edit, -i/--interactive, -p/--patch: git does not keep these to
  // a dry run (-e stages with -n), so -n proves nothing.
  let editMode = false
  for (let j = i + 1; j < words.length; j++) {
    const w = at(j)
    if (!onlyPaths && w === '--') {
      onlyPaths = true
      continue
    }
    if (!onlyPaths && w.startsWith('--')) {
      // Read as git reads it: a unique prefix names the option, `--no-`
      // negates it, and the last one given wins.
      const o = readLong(w, LONG[kind])
      if (o === null) continue
      if ('ambiguous' in o) {
        const why = ambiguousWhy(w, o, kind)
        if (why) {
          op.isOpaque = true
          op.specs.push({ raw: w, abs: gitDir, unreadable: why })
        }
        continue
      }
      if (o.takes && !o.negated && o.value === undefined) j++
      const on = !o.negated
      if (o.name === 'all') op.all = on
      else if (o.name === 'ignore-removal') op.all = !on // add: --ignore-removal is --no-all
      else if (o.name === 'update') op.update = on
      else if (o.name === 'force') op.force = on
      else if (o.name === 'include') op.include = on
      else if (o.name === 'only') op.only = on
      else if (o.name === 'dry-run') dryRun = on
      else if (kind === 'add' && (o.name === 'edit' || o.name === 'interactive' || o.name === 'patch')) editMode ||= on
      else if (o.name === 'short' || o.name === 'porcelain' || o.name === 'long') statusFormat = on
      else if (o.name === 'pathspec-from-file' && on) op.isOpaque = true
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
        else if (f === 'n' && kind === 'add') dryRun = true
        else if ((f === 'e' || f === 'i' || f === 'p') && kind === 'add') editMode = true
        else if (f === 'i' && kind === 'commit') op.include = true
        else if (f === 'o' && kind === 'commit') op.only = true
        else if (kind === 'commit' && COMMIT_SHORT_ATTACHED.has(f)) break
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
    const abs = w.startsWith(GUARD.notesPrefix) ? w : resolvePath(gitDir, w, home)
    // A path that resolves to an expansion (a tilde form `~-/x`, `~/x` with no
    // known home): the guard cannot name it. It asks.
    if (hasExpansion(abs)) {
      op.isOpaque = true
      op.specs.push({ raw: w, abs: gitDir, unreadable: 'a path the shell expands, which the guard cannot name' })
      continue
    }
    op.specs.push({ raw: w, abs })
  }
  if ((dryRun && !editMode) || (kind === 'commit' && statusFormat)) op.dryRun = true
  // Another repository, work tree or index than the one guard.tsx reads the
  // status of: what it stages or commits cannot be listed. It asks.
  const elsewhereTree = tree ?? treeVar
  if (elsewhereTree !== undefined && elsewhereTree !== null) {
    op.isOpaque = true
    op.specs.push({
      raw: text,
      abs: gitDir,
      unreadable: `\`${elsewhereTree}\` points git at another repository, work tree or index than the guard reads`,
    })
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
  return sub
}


// `git push [options] [<repository> [<refspec>...]]`, from the word after
// `push`.
export function parsePushTarget(words: readonly string[], from: number): PushTarget {
  const t: PushTarget = { remote: null, refspecs: [], sets: [], deleting: false, force: false, opaque: null }
  const positional: string[] = []
  let repoOption: string | null = null
  let onlyArgs = false
  // In the order given, as git applies them: the last of `--x` and
  // `--no-x` wins. --all and --branches are one option.
  const sets = new Set<PushTarget['sets'][number]>()
  const forces = new Set<string>()
  const setOf = { all: '--branches', branches: '--branches', mirror: '--all', tags: '--tags' } as const
  for (let j = from; j < words.length; j++) {
    const w = words[j] ?? ''
    if (!onlyArgs && w === '--') {
      onlyArgs = true
      continue
    }
    if (!onlyArgs && w.startsWith('--')) {
      const o = readLong(w, LONG.push)
      if (o === null) continue
      if ('ambiguous' in o) {
        t.opaque ??= ambiguousWhy(w, o, 'push')
        continue
      }
      const on = !o.negated
      const value = o.takes && on && o.value === undefined ? words[++j] : o.value
      if (o.name in setOf) {
        const set = setOf[o.name as keyof typeof setOf]
        if (on) sets.add(set)
        else sets.delete(set)
      } else if (o.name === 'delete') t.deleting = on
      else if (o.name === 'force' || o.name === 'force-with-lease' || o.name === 'force-if-includes') {
        if (on) forces.add(o.name)
        else forces.delete(o.name)
      } else if (o.name === 'repo') repoOption = on ? value ?? null : null
      continue
    }
    if (!onlyArgs && w.startsWith('-') && w.length > 1) {
      const flags = w.slice(1)
      for (let k = 0; k < flags.length; k++) {
        const f = flags.charAt(k)
        if (f === 'd') t.deleting = true
        else if (f === 'f') forces.add('force')
        else if (f === 'o') {
          if (k === flags.length - 1) j++
          break
        }
      }
      continue
    }
    positional.push(w)
  }
  t.sets = [...sets]
  t.force = forces.size > 0
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

// A ref-set push (--all, --branches, --mirror, --tags) leaves out everything
// every tracking ref of the remote holds, so one stale ref anywhere hides
// commits: it asks, naming up to three of them (null: none is stale).
export function refSetStaleWhy(stale: readonly Stale[]): string | null {
  if (!stale.length) return null
  const names = stale.map(s => s.base.replace(/^refs\/remotes\/[^/]+\//, ''))
  const shown = names.slice(0, 3).join(', ') + (names.length > 3 ? `, and ${names.length - 3} more` : '')
  return `the remote no longer has what this clone's tracking refs say for ${shown} (it changed since the last fetch), so the guard cannot tell what the push republishes (fetch first)`
}

// Where each of a remote's tracking refs was fetched from, read through the
// remote's own fetch refspecs (`git config --get-all remote.<remote>.fetch`,
// [] when unset: git's default `+refs/heads/*:refs/remotes/<remote>/*`), so a
// ref-set push reads `origin/pr/1` live as `refs/pull/1/head`, not as a
// branch the remote never had. `sources`: tracking ref -> every remote ref a
// refspec maps onto it (the default `refs/heads/*` also covers `pr/1`; git
// refuses to fetch two of them into one ref, so at most one exists there);
// `patterns`: what to ask `git ls-remote` for. A tracking ref no refspec
// explains, or a refspec the guard cannot read, is why it cannot tell (ask).
export function trackingSources(
  remote: string,
  fetch: readonly string[],
  refs: readonly string[],
): { sources: Map<string, string[]>; patterns: string[] } | { why: string } {
  const specs: { src: string; dst: string }[] = []
  for (const line of fetch.length ? fetch : [`+refs/heads/*:refs/remotes/${remote}/*`]) {
    const spec = line.trim().replace(/^\+/, '')
    // A negative refspec only leaves refs out of a fetch; it names no tracking ref.
    if (spec.startsWith('^')) continue
    const parts = spec.split(':')
    if (parts.length > 2) return { why: `the guard could not read the remote's fetch setting \`${line.trim()}\`, so it cannot tell what the push republishes` }
    const [src, dst] = [parts[0]!, parts[1] ?? '']
    // No destination: fetched into FETCH_HEAD only, never a tracking ref.
    if (!dst) continue
    const stars = (s: string) => s.split('*').length - 1
    if (stars(src) > 1 || stars(src) !== stars(dst) || !src.startsWith('refs/')) {
      return { why: `the guard could not read the remote's fetch setting \`${line.trim()}\`, so it cannot tell what the push republishes` }
    }
    specs.push({ src, dst })
  }
  const sources = new Map<string, string[]>()
  const patterns = new Set<string>()
  for (const ref of refs) {
    const from: string[] = []
    for (const { src, dst } of specs) {
      let one: string | null = null
      if (!dst.includes('*')) {
        if (ref === dst) one = src
      } else {
        const [pre, post] = dst.split('*') as [string, string]
        if (ref.length > pre.length + post.length && ref.startsWith(pre) && ref.endsWith(post)) {
          one = src.replace('*', ref.slice(pre.length, ref.length - post.length))
        }
      }
      if (one !== null && !from.includes(one)) {
        from.push(one)
        patterns.add(src)
      }
    }
    if (!from.length) {
      const name = ref.replace(/^refs\/remotes\/[^/]+\//, '')
      return { why: `no fetch setting of the remote explains the tracking ref ${name}, so the guard cannot tell what the push republishes` }
    }
    sources.set(ref, from)
  }
  return { sources, patterns: [...patterns] }
}

// What the remote has now for one tracking ref, from one `git ls-remote`
// answer (`said`: ref -> OID, undefined when the read failed): the OID, null
// when none of its sources is there, undefined when the read failed, or why
// two of its sources are both there (git would not have fetched either alone).
export function liveSource(
  ref: string,
  candidates: readonly string[],
  said: ReadonlyMap<string, string> | undefined,
): string | null | undefined | { why: string } {
  if (said === undefined) return undefined
  const there = candidates.filter(c => said.has(c))
  if (there.length > 1) {
    const name = ref.replace(/^refs\/remotes\/[^/]+\//, '')
    return { why: `the remote has both ${there.slice(0, 2).join(' and ')}, which both fetch into ${name}, so the guard cannot tell what the push republishes` }
  }
  return there.length ? said.get(there[0]!)! : null
}

// The publish range measured against the live remote: stale tracking refs
// are left out of `--remotes` and their live commits excluded instead.
// Accepted residuals: only the destination branches are read live, so a
// stale tracking ref for another branch of the remote can still hide commits
// through `--remotes=<remote>`; and a tag named by refspec gets no live check.
// (A ref set, --all/--branches/--mirror/--tags, reads every tracking ref live:
// guard.tsx trackingStale.)
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
  // An op whose destination the guard could not resolve: a push naming no
  // remote, or git run in a repository it cannot name.
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
  // commit. Named paths alone (--only, the default) commit just those;
  // -i/--include commits the staged index as well.
  const tracked = entries.filter(e => e.x !== '?' && e.x !== '!')
  // --only with no paths (--amend, --allow-empty; otherwise git refuses it)
  // commits none of the index.
  if (op.only && !op.include && !op.all && !specs.length && !op.isOpaque) return []
  if (specs.length) return tracked.filter(e => matches(e.path) || (op.include && e.x !== ' ')).map(e => e.path)
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
  // Git runs in a repository the guard cannot name: whatever the caller's
  // repo is, it cannot tell where this goes. It asks.
  if (op.unknownRepo) {
    const hits = [{ path: op.text, reason: op.unknownRepo }]
    return { op, verdict: 'ask', mode: facts ? 'git' : 'text', hits, touched: 0, unresolved: true }
  }
  // A dry run stages or commits nothing, when the guard read all of it: a
  // word it could not read (an expansion, what xargs adds, an alias) may
  // undo the dry run.
  const readWhole = !op.isOpaque && !op.specs.some(s => s.unreadable) && !hasExpansion(op.text) && op.alias === undefined
  if (op.kind !== 'push' && op.dryRun && readWhole) return { op, verdict: 'pass', mode: facts ? 'git' : 'text', hits: [], touched: 0 }
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
