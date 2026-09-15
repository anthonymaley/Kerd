# Score — 0.128.0 build (design revision 2)

Authority: Anthony's "yes" (2026-09-15 07:59) to building, with Codex reviewing the
design before build and the change set before release. Release is asked when reached.
The contract is [work.md](work.md) "Design, revision 2" together with revision 1 where
unchanged. All steps are written by Conductor (Claude); a defect in a step returns to
Conductor. Players can't use `kerd:effort-*` yet (not installed in this session), so
their effort inherits the host's per-model setting and is observed afterwards.

| Step | Owner / route | Model | Tag |
| --- | --- | --- | --- |
| A agent definitions (5 files) | Conductor inline, done 08:08 | current session | [keep] |
| P1 `job_evidence.py` + tests | Player, native subagent | Opus 5 | [delegate] |
| P2 packaging includes `agents/` + definitions test | Player, native subagent | Sonnet 5 | [delegate] |
| D docs, route matrix, README, versions, `CLAUDE.md` | Conductor inline | current session | [keep] |
| V suites, gates, `claude plugin validate`, post-build probe | Conductor | current session | [keep] |
| R Codex change-set review (before-push) | codex-tui | existing session | — |

Fit · A kept inline: five near-identical short files whose wording is itself the
routing contract. Fit · P1: best-effort reader of private formats with file-identity,
no-leak and schema-tolerance rules. Opus 5, because the safety edge cases interact.
Fit · P2: a bounded packaging change and a parse test, checkable by the existing suite.
Sonnet 5, because the spec is exact. Fit · D kept inline: interlocking Conductor
clauses and the route matrix cross-reference each other.

Change reads use `change_read.py` baselines `e128-p1` and `e128-p2`, taken before
dispatch.

---

## P1 — `job_evidence.py`: observed model and effort for a dispatched Claude job

**Intended result.** Conductor can show what model and effort a native Claude job
actually ran with, by reading only the structured model and effort fields of that
job's own transcript and never emitting conversation content, and degrade to
`unverified` whenever the private format isn't as expected.

**Owned paths.** New `skills/conductor/scripts/job_evidence.py` and
`skills/conductor/scripts/tests/test_job_evidence.py`. Nothing else.

**Observed format (Claude Code 2.1.270–2.1.272; not a documented interface).**
- Subagent transcript: `<projects-root>/<encoded-project>/<session-uuid>/subagents/agent-<agentId>.jsonl`.
- Metadata: the same path with `.meta.json` in place of `.jsonl`. It is a JSON
  object that includes `agentType` and `model` (the requested alias, or absent).
- Transcript lines are JSON objects. Records carry a top-level string `effort`
  (observed on assistant records, next to `message.model`; corrected 08:16 from
  P1's report).
- The default projects root is `~/.claude/projects`.

**CLI (stdlib, Python 3.9+, style like `change_read.py`).**
`python3 job_evidence.py --agent-id ID [--session UUID --projects-root DIR]`
- `--agent-id` must match `^a?[0-9a-f]{8,40}$`, which covers observed IDs like
  `a434d67120ca1df6d`. Otherwise print `{"status":"refused","reason":...}` and
  exit 2.
- Session: default `CLAUDE_CODE_SESSION_ID`, which must be a UUID. An explicit
  `--session` is accepted only together with an explicit `--projects-root`
  (fixtures); otherwise exit 2 refused. No session available → `unverified`,
  exit 0.
- Locate: glob `<root>/*/<session>/subagents/agent-<ID>.jsonl`. Zero → unverified
  ("not found"). More than one → unverified ("ambiguous"). The glob pattern is
  built from the validated values only.
- Identity for both files: `lstat`, then refuse a symlink, a non-regular file, or
  `st_uid != getuid()`. Open with `O_NOFOLLOW`, `fstat`, and match dev/inode.
  Group/other permission bits are *not* refused, because native files are 0644
  or 0600 by host default. A missing `.meta.json` → `requested_model: null`,
  `agent_type: null`, noted in `gaps`.
- Stream the JSONL line by line, up to 50 MB. Skip lines that don't parse, and
  count them in `malformed_lines`. For each object: if top-level `effort` is a
  string of at most 16 characters in `^[a-z]+$`, count it. If `message` is a
  dict whose `model` is a string of at most 64 characters in `^[A-Za-z0-9._-]+$`
  and `type == "assistant"`, count it. Anything else is ignored, never echoed.
- Output JSON, exit 0:
  `{"status": "observed"|"unverified", "reason": null|str, "agent_type": str|null,
    "requested_model": str|null, "observed_models": {model: count},
    "observed_effort": {level: count}, "malformed_lines": int, "gaps": [str]}`
  - `status` is `observed` when at least one effort value and one model were
    counted, otherwise `unverified` with a reason ("no effort records", "no model
    records", "not found", …).
  - `agent_type` and `requested_model` are included only when they are strings of
    at most 64 characters in `^[A-Za-z0-9:._-]+$`; otherwise null plus a gap.
- It never outputs paths, session IDs, agent IDs, prompts, tool input or message
  text.
- Errors reading a located file (permissions, identity refusal) → `unverified`
  with a reason naming the check, not the path. Only invalid arguments exit 2.

**Tests (`tests/test_job_evidence.py`, fixture projects root in a temp dir; load
the module like `test_change_read.py`).**
1. A normal fixture (meta plus 3 records, effort `low` ×2, model `claude-sonnet-5`)
   → observed with exact counts.
2. Not found → unverified. Two matches under different project dirs →
   unverified, "ambiguous".
3. Malformed lines are counted and skipped. A line whose `message.content`
   contains `SECRET-MARKER` is absent from the output.
4. Missing meta → gaps and null fields, still observed if records exist.
5. No effort records → unverified "no effort records". No model records →
   unverified.
6. Transcript is a symlink → unverified. Meta is a symlink → unverified or gap.
   A FIFO or directory → unverified.
7. An unexpected schema (records with `effort` as a number, `model` with spaces
   or too long) → those values are ignored → unverified.
8. A bad `--agent-id`, a non-UUID session, `--session` without
   `--projects-root` → exit 2 refused. No `CLAUDE_CODE_SESSION_ID` and no
   `--session` → unverified, exit 0.
9. Output never contains the projects-root path, session UUID or agent ID.

**Verification.** `cd skills/conductor/scripts && DEVELOPER_DIR=/Library/Developer/CommandLineTools
python3 -m unittest discover -s tests -q` → all pass; report the count.

**Boundaries.** Only the owned paths. Never read the real `~/.claude/projects` in
tests. No commits. Report unrelated issues rather than fixing them.

**Return.** CLI usage, the test names, verification output, and any ambiguity
(stop and report).

---

## P2 — Portable packaging ships `agents/`; definitions test

**Intended result.** The portable Claude package contains the five `agents/effort-*.md`
definitions exactly, and a test guards the definitions' contract.

**Owned paths.** `docs/work/model-ready-work/packaging/build.py`,
`docs/work/model-ready-work/packaging/test_build.py`, and new
`skills/conductor/scripts/tests/test_effort_agents.py`. Nothing else. The agents
already exist and are owned by Conductor. If they violate the test contract,
report it; don't edit them.

**Edits.**
1. `build.py`:
   - `inputs()` also collects every regular file under the repository root's
     `agents/`, keyed as `agents/<name>.md`, with the same symlink refusal and
     `.md`-only rule.
   - A missing `agents/` directory, or any of the five
     `agents/effort-{low,medium,high,xhigh,max}.md`, raises `ValueError` before
     output is created.
   - Update the module docstring to say it builds the four core skills plus the
     effort agents.
2. `test_build.py`:
   - The existing current-version test asserts all five definitions ship.
   - The relocated-exact test covers them byte-for-byte, extending its existing
     comparison if it doesn't already cover every packaged path.
   - A missing-source test covers a missing `agents/effort-max.md` producing no
     output.
3. `test_effort_agents.py`: parse each `agents/*.md` frontmatter (the block
   between the first two `---` lines, `key: value` per line, no YAML dependency)
   and assert:
   - exactly the five files exist;
   - `name` equals the file stem;
   - `effort` equals the stem's level and is in `low, medium, high, xhigh, max`;
   - `description` starts with "Internal Kerd routing agent at <level> reasoning
     effort. Invoke only when Kerd Conductor or Agent explicitly selects
     kerd:effort-<level>";
   - there are no `model`, `tools`, `hooks`, `mcpServers` or `permissionMode`
     keys;
   - the body is non-empty and contains "Follow the brief".

**Verification.**
- `cd docs/work/model-ready-work/packaging && DEVELOPER_DIR=/Library/Developer/CommandLineTools
  python3 -m unittest test_build -q` → pass. Use whatever invocation the file
  supports if different, and report it.
- `cd skills/conductor/scripts && python3 -m unittest tests.test_effort_agents -q`,
  or discover → pass.
- Report counts.

**Boundaries.** Only the owned paths. Do not run the real build into the repo's
`packaging/build/` output (tests use temp dirs). No commits.

**Return.** Diff summary, test names, verification output, and any agent
definition that fails the contract (report, don't fix).


**P1 repair (Conductor, 2026-09-15 08:17), from the controller's change read:**
1. `--session` together with a `--projects-root` that resolves (realpath) to the
   default `~/.claude/projects` is refused with exit 2. Design [R2] says an explicit
   other session is never read against the real store; this step had said only
   "explicit root". Test: `--session` with `--projects-root` set to the fixture HOME's
   default root → refused.
2. An absent `model` key in `.meta.json` is normal (the model is inherited). Leave
   `requested_model: null` with no gap. Keep the gap only for a present but invalid
   value. Update the existing test.

**P1 repair 2 (Conductor, 2026-09-15 08:18), from P1's own report:** with an explicit
`--session`, a projects root whose project or session folder is a symlink into the
default store still read the real store. That is refused too, checked by the realpath
of the located transcript before either file is opened. Tests: a symlinked project
folder and a symlinked session folder.

## V — verification (Conductor, 2026-09-15 08:24)

- **Suites:** Agent, Switch and Conductor (90, incl. `test_job_evidence.py` 18 and
  `test_effort_agents.py`), packaging `test_build` (10), `tests/hooks_test.sh` 21/21.
- **Gates:** `gate.py selftest`, `audit` (pre-existing register note only) and
  `release`; progress, matrix, journey and render checks clean. `fidelity.py`
  skipped because HEAD is not a boundary commit; forcing it lists artifacts for
  Switch Out to name.
- **`claude plugin validate`:** the marketplace manifest, plugin manifest and
  `agents/` passed. The one warning is the pre-existing root `CLAUDE.md`.
- **End-to-end probe:** the portable package was built from the working tree
  (69 files, all five agents) and loaded with `--plugin-dir` in a fresh headless
  session (`a61c2714`, $0.20). Calling `kerd:effort-low` with `model: sonnet`,
  then the packaged `job_evidence.py` inside that session, returned `observed`:
  agent type `kerd:effort-low`, `claude-sonnet-5` ×1 at `low` ×1, no gaps.
- **Players' observed settings** (inherited, since the agents aren't loaded in
  this session): P1 `claude-opus-5` at `xhigh`; P2 `claude-sonnet-5` at `high`.
- **Change reads:** both baselines compared (unexpected: none) and discarded.

## R — Codex change-set review 1 (08:30) and routing

It confirmed [R1]–[R4] faithful, the release checklist clean, and the Conductor (90) and
packaging (10) suites passing. It found:
1. **Effort counted on all record types:** repair to P1 (Conductor spec defect). Count
   `effort` only on `type == "assistant"` records.
2. **Partial evidence reported as observed:** repair to P1 (Conductor spec defect).
   Keep the partial counts, but return `unverified` when the size limit is reached or
   any non-blank record is malformed.
3. **Overclaiming wording:** Conductor inline for the docs; the `job_evidence.py`
   docstring is repaired with P1. The helper "reads only the structured model and
   effort fields and never emits conversation content". Conductor *requests* effort
   per job, and observation decides what ran.

Then V repeats and the before-push review repeats.
