# Score — 0.127.0 build (design revision 2)

Authority: Anthony's "yes" (2026-09-14 23:32 EDT) to "May I build 0.127.0 as designed?".
Build only: no commit, push or release (each needs its own approval). The contract is
[work.md](work.md) "Design, revision 2"; a step never re-decides it. All steps are
written by Conductor (Claude); a defect in a step returns to Conductor.

## Baseline (before dispatch, 2026-09-14 23:35 EDT)

HEAD `331726c` (resolve with Git). Owned paths `skills/agent`, `skills/conductor`,
`skills/switch`, `README.md`, `.claude-plugin`: no tracked or untracked changes.
Ignored entries: three `.DS_Store` files (6,148 bytes each; sha256 prefixes
`eb680fbb7432ea08` agent/scripts, `e88fb036724f5a8d` conductor/references/guidance,
`9f8b087efe71cd0a` conductor/scripts) and `__pycache__/` trees. Declared generated:
`**/__pycache__/`. Agent suite baseline: 168 tests OK.

## Steps and routes

| Step | Owner / route | Model | Tag |
| --- | --- | --- | --- |
| S1 Agent code + tests | Player, native subagent | Opus 5 | [delegate] |
| S2 Agent docs (4 files) | Player, native subagent | Sonnet 5 | [delegate] |
| S3 Conductor docs + Switch in-out | Conductor inline | current session | [keep] |
| S4 README, versions, descriptions | after S1–S3 | decided then | — |
| S5 All suites and gates | Conductor | current session | [keep] |
| S6 Codex full change-set review (`before-push`) | codex-tui | existing session | — |

Fit · S1 — needs correct edits across succession, validation and a new command in a
1,233-line script where the failure mode is a silent drop; Opus 5 because the
correctness bar is high and the paths interact. Fit · S2 — needs faithful prose from
a settled contract in four disjoint files; Sonnet 5 because the wording is specified
and checkable against the design. Fit · S3 kept inline — eight interlocking Conductor
clauses (Fit, change read, cadence planning) cross-reference each other; briefing them
separately would cost about what writing them does and risk drift between files.

S1 and S2 own disjoint paths and run in parallel.

---

## S1 — Agent review cadence: code and tests

**Intended result.** `agent.py` supports a per-binding review cadence and a read-only
`partners` command exactly as work.md design A ("Agent code", "Output contract",
"Agent tests") specifies, with tests proving each rule.

**Owned paths.** `skills/agent/scripts/agent.py`, `skills/agent/scripts/tests/test_agent.py`
(and `test_arrival.py` only if an arrival test must change). Nothing else.

**Exact behaviour.**
1. Constant `REVIEW_CADENCES = ('checkpoints', 'before-push', 'end', 'on-request')`.
   One validator `validate_review_cadence(value)` returning a normalized list
   (order preserved as given, duplicates removed) or raising
   `ValueError` with a clear message for: not a list of strings / empty list, unknown
   value, `on-request` combined with any other value.
2. CLI: `pair` and `start` gain `--review-cadence` (`action='append'`, help: "How this
   partner reviews: checkpoints, before-push, end or on-request (repeatable; on-request
   alone). Schedules review only inside authorized work; grants no permission.").
   Thread it like `--partner-role` (`agent.py:1168,1176,1205,1207`).
3. `pair(..., review_cadence=None)`: validate before any side effect (as roles at
   `:810-813`); on update set `prior['review_cadence']` only when supplied (`:821-822`);
   on new binding set `record['review_cadence']` when supplied (`:826-827`). A role-only
   update leaves an existing cadence untouched; a cadence-only update leaves the role.
4. `start(..., review_cadence=None)`: validate before side effects; refuse for
   `kind != 'partner'` with `ValueError('A review cadence is not a worker assignment')`
   (mirroring `:834-835`); store in the reservation and final record (`:878,:883`).
5. `adopt`: after the `partner_role` copy (`:613-614`), copy `review_cadence` when present
   in `prior`. Do not validate-and-drop here silently: if the stored value is invalid,
   still copy it unchanged (readers report it); add a comment that readers validate.
6. Readers: `notice_binding` (`:660`) additionally rejects an invalid stored
   `review_cadence` the same way it rejects a non-string role. `checked_binding`
   (`:504-515`) must not crash on it.
7. New subcommand `partners` (no extra arguments): read every `kerd-agent/partners/*.json`
   for this project without native discovery, socket, CLI or network calls. Output JSON
   `{"partners": [rows]}` sorted by alias; row keys exactly `alias`, `provider`, `kind`
   (default `"partner"` when absent), `role` (stored `partner_role` or null),
   `review_cadence` (validated list or null), `valid` (bool), and `error` (string) only
   when `valid` is false. A row is invalid when JSON is unreadable, provider/alias
   missing, project mismatched, role not a string, or cadence invalid; an invalid row
   keeps what can be read and sets `review_cadence: null`. **Repair (Conductor,
   23:50):** a binding with no session `id` yet (for example a `start-uncertain`
   reservation) is also invalid, error `Binding has no confirmed session yet`, so
   Conductor never selects an unreachable partner. Mixed results exit 0.
   Non-zero only for store-level failure (partners directory unreadable, not a Git
   project). Do not include session IDs.

**Tests (add to `test_agent.py`, following `:409-439` and `:84-129` patterns).**
- pair stores cadence; re-pair with cadence replaces; role-only update keeps cadence;
  cadence-only update keeps role.
- refuses unknown value, `on-request` + `end`, empty, and cadence on `start --kind worker`,
  each before any file is written.
- handoff → adopt keeps cadence; a second restart keeps it; explicit
  `--confirm-replacement` keeps it. Include one assertion that would fail if the adopt
  copy line were removed.
- `partners` with two valid bindings: alias order, exact row keys, no discovery calls
  (patch or assert the discovery/socket helpers are not invoked, using the file's
  existing mocking approach).
- `partners` with one malformed cadence and one valid binding: exit 0, both rows, bad row
  `valid: false` with `error`, `review_cadence: null`.
- `notice_binding`/arrival treats a binding with malformed cadence as invalid the same
  way as a malformed role (follow the existing role test).

**Verification.**
`cd skills/agent/scripts && python3 -m unittest discover -s tests -q` → all tests pass
(baseline 168 plus the new ones); report the count. Also
`python3 skills/agent/scripts/agent.py --project /Users/anthonymaley/development/product/Kerd partners`
→ valid JSON; report it with session IDs removed.

**Boundaries.** Edit only the owned paths. No commits, no `pair`/`start`/`ask` against
real sessions, no changes to `.git/kerd-agent/` real bindings (tests use temp dirs as the
existing suite does). Do not edit docs.

**Return.** Summary of changes by function with line ranges, the test names added, the
verification output (test count, `partners` output), and any place the design could not
be followed exactly (stop and report rather than improvise).

---

## S2 — Agent docs for review cadence

**Intended result.** Agent's person-facing and CLI docs describe the cadence exactly as
work.md design A ("Contract", "Values", "Coalescing" authority sentence, "Agent docs")
specifies, consistent with S1's CLI (`--review-cadence`, repeatable; `partners`).

**Owned paths.** `skills/agent/SKILL.md`, `skills/agent/references/user-guide.md`,
`skills/agent/references/native-sessions.md`, `skills/agent/references/session-succession.md`.

**Edits.**
1. `SKILL.md` step 3 (`:55-63`): after the role sentence, add: when pairing or starting a
   persistent partner without a recorded role or review cadence, ask once for both in one
   question — the host's multi-select question control where available (for example
   Claude's multi-select), otherwise one plain question listing the four values with
   one-line meanings — and record them with `--partner-role` and `--review-cadence`; do
   not re-ask on later requests; the person changes either by saying so. State the
   authority limit in one sentence: a cadence schedules this partner's review only inside
   authorized work and grants no work, contact beyond it, commit, push or release. Add
   that Conductor reads bindings through `agent.py partners`.
2. `SKILL.md` frontmatter `description`: mention that pairing records the ongoing role
   and review cadence. Keep the rest of the description's meaning; keep it one line.
3. `user-guide.md`: help row at `:18` gains a cadence example (e.g. "Pair Codex as
   reviewer before push"); section at `:64-72` explains the four values, `on-request`
   exclusivity, that it can be changed by telling any session, and the authority limit.
4. `native-sessions.md` (`:30-45`): document `--review-cadence VALUE` (repeatable,
   values, `on-request` alone, workers refused), replacement vs role-only preservation,
   and the `partners` command and its row shape (from S1's contract; valid/invalid rows,
   exit 0 on mixed).
5. `session-succession.md`: where the role's carry-forward is described, state the
   cadence travels with it through prepared handoff, restart recovery and explicit
   replacement, and that an invalid stored cadence is carried unchanged and reported by
   readers.

**Style.** Match each file's existing voice and line width (~80 columns); no new
headings unless the file's structure needs one; all slash references use `/kerd:`.

**Verification.** `grep -n "review-cadence\|review cadence" <each owned file>` shows the
additions; `python3 tools/gates/gate.py release` from the project root reports no bare
slash references (version drift failures are expected until S4 and are not yours).

**Boundaries.** Edit only the owned paths; no code, no Conductor/Switch docs, no README.
No commits. Do not change existing rules beyond these additions.

**Return.** Per file: lines changed and the added text; the grep and gate output; any
contract point you could not express without changing another rule (stop and report).

---

## S3–S6 — recorded after execution (Codex review, 2026-09-14 23:52)

Codex's before-push review found that S3–S6 had no written step before they ran.
These entries are **reconstructed after execution**, not a score used beforehand.
Only S1 and S2 were scored in advance. The routes table above named S3–S6, and
the controller ran them as follows.

- **S3 Conductor docs and Switch in-out (Conductor inline, 23:36–23:42).** The
  contract was design revision 2, sections A (Conductor docs, Switch docs), B and C.
  It edited `orchestration.md`, `execution.md`, `journey.md`, `model-jobs.md`,
  `guidance/model-choice.md`, `work-record.md`, `managed-conductor.md`, the
  Conductor `SKILL.md` description and Switch `in-out.md`. No pre-written
  verification command. It was checked by S5's suites and gates, and is reviewed
  by S6.
- **S4 README, versions, descriptions (Conductor inline, 23:44).** It edited the
  three version fields, the byte-identical capability description and two README
  paragraphs. Verified by `python3 tools/gates/gate.py release` → `release: clean`.
  It missed the README "What's New" entry (Codex finding 4).
- **S5 suites and gates (Conductor, 23:46).** Agent, Switch and Conductor unittest
  suites; `tests/hooks_test.sh`; `gate.py selftest/audit/release`; progress,
  matrix, journey and fidelity checks. All passed. The audit's one note is the
  pre-existing requirements-register trace gap.
- **S6 Codex change-set review (`before-push`, 23:47–23:52).** Returned "not ready
  to commit" with five findings. Their routing follows.

## Review findings routing (2026-09-14 23:55)

Anthony, "yes" (23:55): keep 0.127.0's scope, fix the findings, and make
effort-sized player definitions the next release.

1. Score incomplete: fixed by the section above (Conductor).
2. Change-baseline procedure untested, ignored directories not inventoried: new
   step **S7** (Conductor-written, player), and Conductor points `execution.md` at
   its helper.
3. `partners` accepts a non-partner `kind` and non-UUID IDs: repair to S1 item 7
   (Conductor), then resume the S1 player.
4. README "What's New" still at 0.126.0: Conductor inline (S4 follow-up).
5. Agent re-asks an established role: repair to S2 item 1 (Conductor), then resume
   the S2 player.

After all five: S5 re-runs, then S6 repeats (any change invalidates the before-push
gate).

**S1 item 7 repair (23:55):** a row is also invalid when `kind` is present and not
`"partner"`, or when `id` is not a canonical session UUID string. Validate it with
the same identifier check `checked_binding` uses.

**S2 item 1 repair (23:55):** ask only for missing values. When both role and
cadence are missing at initial setup, ask for both together. When a role is
recorded and the cadence is missing, ask only for the cadence. Never re-ask a
recorded role.

---

## S7 — Tested change-read helper

**Intended result.** Conductor's returned-edit read (design C, `execution.md`
"Review, prove and improve") runs through one tested helper instead of hand-typed
Git commands. The helper records a content baseline of owned paths before dispatch,
compares after return, and reports exactly what changed, including in ignored
directories.

**Owned paths.** New `skills/conductor/scripts/change_read.py` and new
`skills/conductor/scripts/tests/test_change_read.py`. Nothing else.

**Rationale.** `git status --ignored` lists an ignored directory as one entry, and
`git diff` omits untracked, ignored and pre-dirty content. So the inventory must
walk the filesystem under the owned paths and hash contents.

**CLI (stdlib only, Python 3.9+, match `ask.py` style).**
- `python3 change_read.py --project ROOT baseline --path P [--path P ...]
  [--generated GLOB ...] --out FILE`
  - Writes a JSON snapshot:
    - `head`: `git rev-parse HEAD`, or null in a repository with no commits;
    - `paths` and `generated`: as given;
    - `tracked_patch`: per tracked path under the owned paths, the sha256 of
      `git diff HEAD -- <path>` (staged and unstaged together), keyed by path;
    - `entries`: every non-directory filesystem entry under the owned paths,
      found by walking the filesystem. It never follows symlinks and skips
      `.git`. Each entry records `kind` (`file` or `symlink`), `size`, `sha256`
      (files), `target` (symlinks) and `git` status (`tracked`, `untracked` or
      `ignored`, from `git ls-files` and `git check-ignore`);
    - entries under a `--generated` glob are not listed one by one. They are
      summarized per matching top-level directory as `{count, sha256}`, over the
      sorted `path+hash` pairs.
  - Owned paths must be inside ROOT. Refuse `..`, absolute paths outside ROOT,
    and a non-Git ROOT with exit 2 and a message.
- `python3 change_read.py --project ROOT compare --baseline FILE`
  - Takes the same snapshot now, using the baseline's paths and generated globs,
    and prints JSON:
    - `tracked_changed`: paths whose patch hash differs, including a pre-dirty
      file edited further;
    - `added`, `modified`, `deleted`: entries by content, with `kind`, `git` and
      `binary` (NUL byte in the first 8,000 bytes) flags;
    - `symlinks_changed`;
    - `generated`: per summary `{before, after, changed}`;
    - `unexpected`: every added, modified or deleted entry whose `git` is
      `ignored` and is outside a declared generated glob;
    - `outside`: tracked, staged or untracked (non-ignored) changes outside the
      owned paths since the baseline, from `git status --porcelain=v1
      --untracked-files=all` compared with a whole-repo status list stored in the
      baseline as `outside_status`;
    - `summary`: the one-line `Change read · N tracked paths changed, M text files
      to read, K binary/symlink to check, generated <changed|unchanged>,
      unexpected: none|<count>`.
  - Exit 0 always on a successful comparison. Findings are data, not errors.
    Exit 2 for a missing or invalid baseline or a non-Git ROOT.
- The helper never reads file contents into its output (hashes only) and writes
  only `--out`.

**Tests (`tests/test_change_read.py`, temp Git repos, load the module like
`test_ask.py`).**
1. Clean owned path: compare after no change reports nothing, with `unexpected`
   and `outside` empty.
2. Staged-only edit and unstaged edit to a tracked file: both in `tracked_changed`.
3. New untracked text file: `added`, with `git: untracked`, not binary.
4. **Pre-dirty tracked file edited further:** already modified at baseline, edited
   again → `tracked_changed`.
5. **Pre-dirty untracked file modified:** exists at baseline, content changed →
   `modified`.
6. New file inside an ignored directory (`.gitignore` has `build/`) not declared
   generated → `added` and `unexpected`.
7. The same under a declared `--generated 'build/**'` → `generated.changed` true,
   and `unexpected` empty.
8. Binary file added → `binary: true`.
9. Symlink retargeted → `symlinks_changed`. Symlinks are not followed.
10. Deletion and rename → `deleted` plus `added`.
11. Change outside owned paths → `outside`, not in `added`.
12. Owned path `../x` and a non-Git project → exit 2.
13. The summary line matches the counts.

**Verification.** `cd skills/conductor/scripts && python3 -m unittest discover -s
tests -q` → all pass (existing `test_ask.py` included). Report the count.

**Boundaries.** Only the two new files. No docs (Conductor updates `execution.md`).
No commits. Report unrelated issues rather than fixing them.

**Return.** The CLI as built (usage output), the test names, verification output,
and any point where this step was ambiguous (stop and report).

**S7 repair (Conductor, 2026-09-15 00:10), from the controller's change read of
S7's return:** the `outside` check had two gaps in this step's own spec.
1. Each `outside_status` record also stores a content hash: the patch sha256
   against the baseline commit for tracked paths, the file sha256 for untracked
   ones. Compare on (status code, hash), so a pre-dirty outside file edited again
   is reported.
2. When `head` changed, files changed by commits between the baseline commit and
   the current HEAD that lie outside the owned paths are also reported in
   `outside`, with `"committed": true`.

New tests: a pre-dirty outside tracked file edited again; a pre-dirty outside
untracked file edited again; a commit touching an outside path after the baseline.

**S7 repair 2 (Conductor, 2026-09-15 00:18), from Codex's repeated before-push
review:**
1. **Index and commit state.** For each tracked owned path, record the index patch
   (`git diff --cached <base> -- path`) and the worktree patch (`git diff -- path`)
   separately. Report staging-only changes in `tracked_changed` with `"staged"` or
   `"unstaged"` detail. When HEAD changed, report owned paths changed by commits
   since the baseline commit in a new `committed` list, even with unchanged bytes.
   Tests: pre-dirty unstaged → staged; staged → unstaged; pre-dirty content
   committed unchanged.
2. **Private, disposable storage.** Replace `--out`/`--baseline` with `--name NAME`
   (letters, digits, `.-_`). Store at `$(git rev-parse --git-path
   kerd-conductor/baselines)/NAME.json`, created `0700`, file `0600`. Refuse any
   location inside the work tree. Add `discard --name NAME` to delete it after the
   return is accepted. Output names the baseline, never its path contents. Tests:
   the file is under the Git dir and not in `git status`; bad names are refused;
   `discard` removes it; `compare` after `discard` exits 2.
3. **Schema version and strict validation.** `"schema": 1`. `load_baseline`
   validates that:
   - every path is normalized, project-relative, has no `..` and no `.git`;
   - tracked and entry keys fall under an owned path;
   - outside paths are not under one;
   - status codes come from Git's porcelain v1 two-character set;
   - digests are 64 lowercase hex characters, or null where allowed;
   - `file` entries carry `sha256`, `symlink` entries carry `target`;
   - generated summaries carry an integer `count` and a SHA-256.

   Anything else exits 2. Tests: a tampered baseline with a traversal path, a
   bad hash, a file with no `sha256`, a bad status code, and a wrong schema.

**S7 repair 3 (Conductor, 2026-09-15 00:31), from Codex review 3:**
1. **Any HEAD change is a finding.** The summary line ends with `, head: unchanged`
   or `, head: changed (<n> commits)`. `committed` lists owned paths from
   commit-history enumeration (`git log --format= --name-only -z --no-renames
   <before>..<after>` when the baseline commit is an ancestor), unioned with the
   endpoint diff for divergent or rewritten histories. The same applies to
   `outside`. Add a `commits` count to `head`, or `null` when the histories
   diverge. Tests: an empty commit, and a commit followed by its revert, each
   yield `head.changed`, a non-empty history count, the summary marker and
   (for the revert) the path in `committed`.
2. **Baseline file identity.** Before reading or discarding, `lstat` the file.
   Refuse, with exit 2, a symlink, a non-regular file, an owner other than the
   current user, or any group or other permission bits. Tests: the file replaced
   by a symlink; mode `0644`.
3. **Porcelain pairs.** Accept `??`, the unmerged pairs `DD AU UD UA DU AA UU`,
   and otherwise an X in `[ MTADRC]` with a Y in `[ MTADRC]`, excluding a double
   space. Refuse `!!` and any `?` or `!` mixed with another character. Test:
   `"?M"` refused.

## Review loop result

Codex before-push reviews ran at 23:52, 00:16, 00:30 and 00:41. Each round's findings
went to their author (Conductor) as repairs 1–3 to S7 and repairs to S1 and S2.
Review 4 resolved every item and found nothing new, and its verdict was "ready to
commit and release". Release authority: Anthony, 00:25, "GO until SOLVED ALL issues,
after alignment with codex and tests then release".
