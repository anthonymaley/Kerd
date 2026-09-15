# Effort-sized Claude players

## Now

Owner: Claude (Conductor controller, Kerd).
Stage: Deliver. The build and its checks are done; see [score.md](score.md) section V.
Codex's before-push re-review (08:38) resolved all three findings, found nothing new,
and returned "ready for Anthony's release decision". Suites and gates are green.
Released: Anthony, "y" (2026-09-15 08:43), to "May I release Kerd 0.128.0 (commit,
push and CI)?". The boundary commit that adds this line is the release; resolve it with
`git log`.
Next action (proposed, not agreed): update the installed Claude and Codex plugins to
0.128.0 and restart the sessions, then check that the next real Conductor build shows
`kerd:effort-<level>` requests and `job_evidence.py` observations.
Stops before: release. Anthony's approval covers the build, with Codex reviewing the
design before build and the change set before release. Release itself is asked
when reached.

## Agreement

- 2026-09-14 23:55 EDT, Anthony: keep 0.127.0's scope and make effort-sized player
  definitions the next release.
- 2026-09-15 07:56, Anthony: "lets fix the effort level first", before Switch Out.
- 2026-09-15 07:59, Anthony: "yes" to "May I build 0.128.0 this way, with Codex
  reviewing the design before build and the change set before release?"

## Evidence

1. **v0.105.0 never applied effort.** Across 341 Agent tool calls (25 Aug–10 Sep),
   no call passed `effort`; 60 named it only in prompt text. The Agent tool has no
   effort parameter.
2. **Documentation** (code.claude.com, retrieved 2026-09-14/15):
   - `sub-agents.md` frontmatter: `effort` "Overrides the session effort level.
     Default: inherits from session. Options: low, medium, high, xhigh, max".
   - Per-invocation override exists only for `model`, in the order: invocation,
     frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, main conversation.
   - `plugins-reference.md`: plugin agents support `model` and `effort`; `hooks`,
     `mcpServers` and `permissionMode` are not supported.
   - `model-config.md`: "Frontmatter effort applies when that skill or subagent is
     active, overriding the session level but not the environment variable"
     (`CLAUDE_CODE_EFFORT_LEVEL`). `maxEffortLevel` and organization caps still
     apply. An unsupported level falls back to the highest supported level below
     it.
   - `/tasks` shows the effort when a definition sets it.
3. **Observed on this host (Claude Code 2.1.270), without definitions:** effort
   follows the per-model saved settings. Every Sonnet 5 player on 2026-09-14 ran
   `high`; Opus 5 players and this session ran `xhigh`. Each subagent transcript
   records a top-level `effort` on its assistant records, next to `message.model`.
4. **Probe (2026-09-15 07:58, Claude Code 2.1.272, headless, throwaway plugin
   `probe`, session `ec6fc0a6`, cost $0.19):**

   | Call | Observed model | Observed effort |
   | --- | --- | --- |
   | `probe:player-low`, no model | `claude-sonnet-5` | `low` |
   | `probe:player-low`, `model: opus` | `claude-opus-5` | `low` |
   | `probe:player-max`, `model: sonnet` | `claude-sonnet-5` | `max` |

   The definition's effort applies, and a per-call model can be combined with it.
   This is one run, not a benchmark.

## Design, revision 1 (proposed; awaiting Codex review)

### A. Five plugin agents

`agents/effort-low.md`, `effort-medium.md`, `effort-high.md`, `effort-xhigh.md`,
`effort-max.md` at the plugin root. They load as `kerd:effort-<level>`, which
the manifest's default `agents/` discovery picks up with no manifest change.

Frontmatter: `name: effort-<level>`, `effort: <level>`, and a `description`
saying they are used only when Kerd Conductor or Agent names them for a specific
delegated job, never selected automatically. No `model` (the call passes it). No
`tools` (the job inherits the same tools as `general-purpose`).

Body: a short, role-neutral contract for one delegated job:
- follow the supplied brief or score step exactly;
- stay within its owned paths and authority;
- return the evidence it asks for;
- report unrelated problems instead of fixing them;
- stop at its boundary.

It adds no model tuning and no verification ritual beyond the brief's.

### B. Dispatch contract (Conductor)

- A native Claude job (player, composer or independent reviewer) is dispatched
  with `subagent_type: kerd:effort-<level>` plus `model`. This makes effort a
  real per-job setting instead of words in a prompt.
- Its Fit line states the reason for both.
- The grid's Effort cell reads `<level> (requested via definition)` until
  observed.
- Without the agents installed (an older Kerd, or a host without plugin agents),
  say "effort not settable; inherits the host's per-model setting". Never write
  the level into the prompt as if it applied.
- If `CLAUDE_CODE_EFFORT_LEVEL` is set, the definition cannot override it: say
  so, and the observed value is authoritative.
- A skill run in a subagent is out of scope here.
- Codex routes keep their existing CLI effort flag, and managed Conductor keeps
  its explicit settings. Agent's `start --kind partner` for Claude is unchanged,
  its launch controls noted as separate.

### C. Observed evidence

New read-only helper `skills/conductor/scripts/job_evidence.py`:
- Input: `--agent-id ID`, plus optional `--session ID`, which defaults to
  `CLAUDE_CODE_SESSION_ID`.
- It locates exactly one
  `~/.claude/projects/*/<session>/subagents/agent-<ID>.jsonl` and its
  `.meta.json`, and refuses zero or multiple matches.
- It prints JSON: `agent_type`, `requested_model` (from the metadata), and counts
  of `observed_models` (assistant `message.model`) and `observed_effort`
  (top-level `effort`).
- It never prints message content, prompts or tool input. It refuses IDs that
  aren't `[A-Za-z0-9]+` and sessions that aren't a UUID.
- `--projects-root` is available for tests.

`orchestration.md:33` currently says "Do not mine native transcripts … to fill
the display". It narrows to allow this helper's metadata read for a job
Conductor dispatched in this session, and nothing else. After each return, the
work view shows `observed <model> at <effort>`. A mismatch with the request is a
finding, not a failure to hide.

### D. Doc edits

- `orchestration.md`: evidence labels at `:25-39` (the observed effort route) and
  the startup view example.
- `model-jobs.md:36-38`: effort is set through the definition for native Claude
  jobs; label it requested until observed.
- `execution.md`: where a job is dispatched, name the route.
- `journey.md`: the grid example.
- `guidance/model-choice.md`: effort selection maps to `kerd:effort-<level>`.
- `work-record.md`: requested versus observed.
- Conductor `SKILL.md` description.
- Agent `references/native-sessions.md`: the note separating partner launch
  effort.
- README: Conductor section and What's New.
- `CLAUDE.md` project structure: `agents/`.

### E. Tests and checks

- `skills/conductor/scripts/tests/test_job_evidence.py`, using a fixture projects
  root: single match, no match, multiple matches, bad ID or session, content
  never in output, counts correct.
- A test that parses every `agents/*.md` frontmatter and checks:
  - the name matches the file;
  - `effort` is in the allowed set, and all five levels exist;
  - the description is present;
  - no `hooks`, `mcpServers` or `permissionMode`;
  - no `model`.
- `claude plugin validate .` (local).
- All suites and CI gates.
- A post-build probe: the built plugin loaded via `--plugin-dir`, one cheap
  `kerd:effort-low` call with `model: sonnet`, read through `job_evidence.py`.

### F. Release shape

0.128.0 (MINOR). The version is set in three places, and both capability
descriptions gain "effort-sized native players". Codex reviews the change set
before release.

## Design, revision 2 (Codex design review 2026-09-15 08:05 applied)

Codex found the central claim supported and the design not yet ready to build. Its
four findings are applied here and override revision 1 where they differ.

**[R1] Portable packaging.** `docs/work/model-ready-work/packaging/build.py`
packages only `skills/`. It must also package the root `agents/`, and
`test_build.py` asserts that all five definitions survive an exact, relocated build.

**[R2] Best-effort, bounded evidence helper.** `job_evidence.py` reads private
Claude Code transcript details that are observed, not a documented interface. It
is host-version-specific and best-effort:
- Missing or unknown data returns `"status": "unverified"` with a reason and
  exits 0. Observation never fails the job.
- The session is strictly the current host session (`CLAUDE_CODE_SESSION_ID`).
  An explicit other session is accepted only together with `--projects-root`
  (tests or a recorded fixture), never against the real store.
- Both files are opened after `lstat`/`O_NOFOLLOW`, and must be regular files
  owned by the current user.
- Records are streamed, returned field types and lengths are validated, and
  malformed records are counted, never echoed.
- Output carries no paths, native IDs, prompts, tool input or message content.
- A requested-versus-observed mismatch is a finding. Unavailable observation is
  an evidence gap.
- Tests: malformed JSON, symlink, non-regular file, missing metadata, missing
  model or effort, unknown schema, a foreign session without a fixture root, and
  a content-leak check.

**[R3] Route matrix** (goes into `model-jobs.md` and `orchestration.md`):

| Route | How effort is set | What is shown |
| --- | --- | --- |
| Claude native subagent, definitions installed | `subagent_type: kerd:effort-<level>` plus per-call `model` | requested via definition; observed via `job_evidence.py` |
| Claude native subagent, definitions absent | ordinary native route | "inherits host per-model setting; unverified", never written into the prompt |
| Fresh Codex worker or native Codex subagent | that route's supported `model` and `effort` controls | requested; observed where the route reports it |
| Established Codex partner or TUI | not retunable by a queued contribution; that session keeps its own pair | configured, observed or unknown |
| Managed Conductor | its existing explicit pair | as today |

Effective effort can still differ from the request because of
`CLAUDE_CODE_EFFORT_LEVEL`, `maxEffortLevel` or organization caps, or a fallback
to a lower supported level. Keep the requested level and report the observed one
separately. A Claude session loads agent definitions at start, so an already-open
session does not gain newly installed ones: require a fresh session and don't
claim a reload route. Codex models are not added as Claude agent files.

**[R4] Selection wording.** Descriptions read "Internal Kerd routing agent at
<level> reasoning effort. Invoke only when Kerd Conductor or Agent explicitly
selects kerd:effort-<level> …". This is routing guidance, not a hard host
prohibition, and the docs say so. Omitting `tools` means the agent inherits all
tools available to that subagent (the documented claim). The definitions test
asserts the exact description invariant.
