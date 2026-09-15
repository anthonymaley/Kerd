# Context-window awareness for Claude sessions

## Now

Owner: Claude (Conductor controller, Kerd). Stage: Understand.
Request (Anthony, 2026-09-15 13:25): "context window awareness - i have it on the cli
status line all the time, so you can read it - we need to know when to switch out into
rolling a new session and continue work when needed during loops and other longer agent
run sessions."
Nothing is agreed or authorized beyond direction-setting. No build.

Anthony, 13:29: "lets explore better ways to do this? ... or is that the best?"
**Ruling, Anthony, 13:39: "no, we dont use compact. that why the skill existis, so we
dont lose context."** Route B is dead. A roll is a fresh session restored from Kerd's
saved place, and the line must come early enough that auto-compaction never fires.

**Ruling, Anthony, 13:42: "we dont have auto-compact enabled. its like you forgot what
switch in/out was for. interactive session we dont need to do anything as the user will
decide and fire swtich out when they think they need new context window. this is only
for rolling loops where the use is not interactive."** Interactive sessions are out of
scope: the person chooses when to Switch Out. No status-line bridge, no interactive
notice, no compaction hooks.

Proposed scope (not agreed): give managed Roll a Claude context-aware route matching the
Codex one. A Claude run is watched from its own output stream. At the line it is asked to
finish the current safe operation and return its saved place, and then a genuinely fresh
Claude run continues. Today `roll.py` refuses `--context-aware` for Claude ("Claude
remains on bounded CLI pieces"), and managed Conductor's decision and implementation
sessions are Codex only.

Scope agreed, Anthony 13:45: "yes".
**Threshold ruling, Anthony, 13:57: "65% used is good. not 200k used, we have 880k at that
point."** Roll at 65% of the reported window, used tokens, the same as the Codex route.
No absolute cap. Record each roll's reading to tune it later.

Design: Anthony, 14:07, "check with codex but looks good". Codex design reviews 1–4
(14:12–14:37) are recorded below, and design review 4's single finding was closed by
Codex's own fix.
Review cadence for `codex-tui`: checkpoints + before-push (Anthony, 15:43, "yes",
recorded through Agent `pair --review-cadence`). The cadence was explained with
`review-cadence.html` (diagram-design swimlane).
**Build started, 15:50:** see [score.md](score.md). S1 (`claude_roll.py`, Opus 5 via
`kerd:effort-xhigh`) and S2 (`roll.py` wiring, Opus 5 via `kerd:effort-high`) were
dispatched in parallel as native subagents, with change-read baselines `ctx-s1` and
`ctx-s2`. Baseline suites at `1f5bb8f`: 170 Roll tests OK, 94 Conductor tests OK.
Next: read both returns, run checkpoint review C with Codex, docs, verification and the
live trial, then the before-push review. Commit, push and release are asked when
reached.

## Probe, 2026-09-15 14:03 (approved by Anthony, "y"; one run, tested but not yet verified)

A throwaway run in the scratchpad: `claude -p --input-format stream-json --output-format
stream-json --verbose --model sonnet`, Claude Code 2.1.272, with plugins and hooks loaded
as usual. It cost $0.125.

- **Usage streams live.** Each `assistant` event carries `message.usage`
  (`input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`). Their sum
  is the last request's context, the same count the status line uses (45,740 at the
  final call).
- **The window arrives only at the end of a turn.** `result.modelUsage["claude-sonnet-5"]
  .contextWindow` was 1000000. `system/init` carries `model` but no window. `modelUsage`
  also listed an internal `claude-haiku-4-5` entry (window 200000), so choose the entry
  matching `init.model`. A Roll worker's whole job is usually one turn, so the adapter
  must learn the window before the work starts. A tiny first turn, then the work
  prompt, does that.
- **A mid-turn message is injected at the next tool boundary.** The steer was sent at
  4.6s while the first `sleep 4` ran. After that tool result the model wrote
  "done 1\n\nSAVED", made no further calls, and the run ended in one `result`
  (`num_turns` 2), with four of the five requested sleeps not run. That is the Claude
  counterpart of Codex's `turn/steer`. `init.capabilities` listed `interrupt_receipt_v1`,
  `interrupt_cancel_queued_v1` and `msg_lifecycle_v1`. The result carries
  `queued_turn_count`.
- **Not tested:** a long turn with large tool results (the overshoot risk Codex also
  has), subagent events (they carry `parent_tool_use_id` and must be excluded from the
  main reading), repeat runs, other models.

## Routes compared (2026-09-15 13:30, proposed, not agreed)

- **A. Watch and warn** (the first proposal below): a status-line bridge, a notice at
  the line, then Out and a human-started fresh session, or Roll. Needs plumbing
  through the status-line slot Scorched Earth owns, and a person in the loop for
  interactive work.
- **B. Compaction as the roll** (recommended): set `autoCompactWindow` (docs:
  `/autocompact 400k`, `--autocompact`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`; 100K–1M;
  1M models default to about 967K) to where the roll should happen. A hook computes
  usage from the transcript against that window and asks for a checkpoint shortly
  before it. `PreCompact` (matcher `auto`) is the last point to save mechanically.
  `SessionStart` with matcher `compact` re-injects the saved place and the reading
  set. There is no status-line dependency, no human step, the session ID is kept and
  it works in `/loop`.
  Unverified: whether `PreCompact` can block, whether `SessionStart` `compact`
  context lands after the summary, how far the transcript's `usage` lags.
- **C. Don't fill the controller**: long iterations and jobs run in subagents or fresh
  `claude -p` runs (Conductor delegation and managed Roll already do this). It
  prevents growth but doesn't cover the controller's own judgment-heavy work.
- Recommended shape: C by default, B as the automatic net, managed Roll unchanged for
  managed builds.

## Design, revision 1 (Anthony 14:07: "check with codex but looks good"; awaiting Codex design review)

Outcome: `roll.py --target claude --context-aware` rolls a managed Claude worker at 65%
of its reported window (used tokens) into a genuinely fresh Claude run from the saved
place, the Claude counterpart of the Codex app-server route. Interactive sessions,
status lines and compaction are out of scope (rulings above). Managed Conductor's
Codex-only decision and implementation sessions are unchanged.

A. **Adapter.** A new `skills/switch/scripts/claude_roll.py` bridge with the same
   interface `roll.py` uses for `codex_roll.AppServerBridge`: `run`, `close`,
   `inspect_held`, `held_result`, `held_cancelled`, `release_held`. It reuses
   `ContextWatch` (fraction checks, `--test-roll-at-tokens`, readings), moved or
   imported so both routes share one threshold rule.
B. **Launch.** It uses the same Claude command `ask.py` builds (`-p`, `--output-format
   stream-json`, `--verbose`, `dontAsk`, `--permission-prompts none`, the same
   `--tools`/`--allowedTools` set, `--strict-mcp-config`, `--model`, `--effort`), adds
   `--input-format stream-json`, keeps stdin open and records process identity as today.
   It never uses `--resume`.
C. **Window first.** Turn 1 is a fixed tiny message ("Reply READY"). Its `result`
   supplies `modelUsage[<init.model>].contextWindow`. If `init.model` is missing, or has
   no matching entry, or the window is not a positive int, the run stops blocked with no
   guessed window. Turn 2 is the Roll prompt (the existing context-aware wording in
   `roll.py`) plus the agreement and saved place.
D. **Reading.** Each `assistant` event with `parent_tool_use_id` null contributes
   `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` as the
   latest reading. Subagent events are ignored. A work-turn assistant event without
   valid usage stops the run.
E. **Checkpoint.** At the first reading at or above the threshold, write one stream-json
   user message carrying the existing checkpoint instruction. The model receives it at
   the next tool boundary (probe). If the turn already completed, record a race, as
   Codex does. Never send a second steer.
F. **Completion.** Expect one `result` for the work turn and exactly one final saved
   place in the reply, validated by the existing `check_state`. Then close stdin, wait
   for exit, verify the process group is gone, and only then let `roll.py` start the
   next fresh run.
G. **Stops, as on the Codex route.** Missing usage or window, a changed `init.model`
   between turns, `num_turns` or `queued_turn_count` showing an unexpected extra turn,
   a `permission_denied` blocking the save, a non-success `result`, a read-back failure
   or an uncertain exit all stop automatic continuation. Recovery follows the existing
   inspected path.
H. **Wiring.** `roll.py` accepts `--context-aware` for `--target claude`, picking the
   adapter by target. `--control` and `--test-roll-at-tokens` work for both.
   `roll_status.py` shows the recorded readings unchanged.
I. **Tests.** A fake `claude` executable replays stream-json fixtures built from the probe
   shapes: window learned, steer at threshold, steer racing completion, missing window,
   model mismatch, subagent events ignored, missing usage, extra turn, non-success
   result, and exit and cleanup. There is no live model call in tests. One disclosed
   live trial uses `--test-roll-at-tokens` after the build.
J. **Docs and release.** Change to-roll.md "Observed context route — Codex candidate" to
   cover both providers, remove "Claude remains on bounded CLI pieces", and update
   managed-conductor.md's Claude line and the Switch README section. MINOR release.
   Codex reviews the change set before release, and the release is asked when reached.

Known limits: one large tool result can cross 65% before the steer lands; the probe is
one run on Sonnet and Claude Code 2.1.272; stream-json fields are version-specific.

## Codex design review of revision 1 (14:12, "not ready to build") and dispositions

Claude checked each finding against the probe's `events.jsonl`:

1. **Critical: the two-turn window-first sequence is unsupported. Accepted; the
   evidence is corrected.** Codex said the CLI exited after its result while stdin was
   open. Events 31–33 (`commands_changed` at 18.6s, 32.6s and 34.6s) came after the
   `result` (event 30), so the process was still alive with stdin open. The exit
   followed the watchdog closing stdin. A second turn in the same process was never
   tried, though, so the gap stands. Fix adopted: a separate preflight process.
2. **Critical: held-source and `--control` parity. Accepted as a scope cut; the
   evidence is corrected as in 1.** No probe shows a retainable Claude source for
   Managed To, so v1 refuses `--control` and implements no held-source methods.
3. **High: a durable checkpoint receipt before cleanup. Accepted.**
4. **High: effective authority is assumed. Accepted, and confirmed.** Event 19's `init`
   listed 66 tools, including `Task`, `Bash` and `WebFetch`, under `--allowedTools
   "Bash(sleep *)"`. The probe passed no `--tools`, so the `ask.py` command's effect is
   unproven. The stop field is `result.permission_denials`.
5. **High: cleanup and recovery parity. Accepted.**
6. **Medium: explicit turn and result invariants, and duplicate usage. Accepted, and
   confirmed.** Events 23 and 25 repeat message `msg_011Cf5fYG3opQGyY1pmygW8Q` with
   identical usage.

## Design, revision 2 (replaces revision 1's A–J where they differ)

A. **Adapter.** `skills/switch/scripts/claude_roll.py`, a bridge with `run` and `close`
   only. The shared `ContextWatch` threshold rule is imported, not copied. No
   held-source methods. `roll.py` refuses `--control` with `--target claude`.
B. **Command and authority.** The same Claude command `ask.py` builds (`--tools` and
   `--allowedTools` set to the route's file tools, `dontAsk`, `--permission-prompts
   none`, `--strict-mcp-config`, `--model`, `--effort`), plus `--input-format
   stream-json`, never `--resume`. Before sending anything, validate `init`:
   `cwd` is the project root, `permissionMode` is `dontAsk`, `tools` equals the
   requested set exactly (additions or ambiguity refuse), and `model` is present. The
   project root is checked again after launch.
C. **Preflight process for the window.** A separate short `claude -p` process with the
   same command sends one fixed message and must produce exactly one `result` with
   `num_turns == 1`. Its window is `modelUsage[init.model].contextWindow`, a positive
   int, else blocked. The preflight is closed and its process group confirmed gone. It
   is not a worker run and gets no session in `history`. The worker process's
   `init.model` must equal the preflight's, else blocked before any work is sent.
D. **Reading.** Main-conversation `assistant` events only (`parent_tool_use_id` null).
   Deduplicate by `message.id`, keeping the latest usage. The reading is
   `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. A missing
   or malformed usage stops the run.
E. **Checkpoint.** At the first deduplicated reading at or above the threshold, write
   one stream-json user message with the existing checkpoint instruction. Never a
   second. A `result` that arrives before the write is recorded as a race and not
   steered.
F. **Result invariants.** Exactly one `result` per worker process, with `subtype`
   success and `is_error` false. `num_turns == 1` without a checkpoint, `== 2` with
   one. `queued_turn_count == 0`. `permission_denials` empty. One `session_id`
   throughout. No events are accepted after `result` except the known non-content
   `system` subtypes seen in the probe, and any assistant or user event after it is a
   stop. Malformed JSON stops the run.
G. **Checkpoint receipt before cleanup.** Before closing stdin, atomically save a
   `checkpoint_saved` receipt under the request's private record: the complete final
   reply text, the parsed candidate place, session ID, process ID with its start time,
   the readings and the trigger. Read it back and compare it byte for byte. Only then
   clean up. `roll.py` promotes the place from that receipt, and recovery inspects the
   receipt, never replaying the job.
H. **Cleanup and recovery parity.** Record descendant identities (PID plus start time)
   while owning the parent, as `codex_roll.py` does. After closing stdin, allow an exit
   grace period, then TERM only still-matching owned descendants, then confirm they are
   gone. Unknown or uninspectable survivors stop. `roll.py` recovery requires
   `owned_children_gone` or a fresh `children_gone` check for every context-aware
   route, not only `app-server-stdio`.
I. **Tests.** A fake `claude` executable replays probe-shaped stream-json. Cases:
   - the preflight window, preflight and worker as separate processes, a model
     mismatch;
   - init validation (extra tool, wrong cwd, wrong permission mode);
   - duplicate message usage, subagent events ignored, a steer at threshold, a steer
     racing completion;
   - `num_turns` and `queued_turn_count` violations, duplicate results, conflicting
     session IDs, malformed JSON or usage, permission denials, timeout and
     cancellation;
   - receipt save then controller loss before place promotion;
   - a detached child, a PID identity mismatch, an uninspectable group, uncertain
     shutdown;
   - `--control` refused for Claude, and recovery requiring cleanup evidence on both
     routes.
   One disclosed live trial with `--test-roll-at-tokens` follows the build.
J. **Docs and release.** As revision 1, with the v1 limits stated: no `--control`, no
   Managed To source hold for Claude, and a large tool result can overshoot. MINOR.

## Codex re-review of revision 2 (14:20, "not ready to build") and revision 3 changes

All six original findings were resolved. The five new ones are all accepted:

1. **High: steer only at the boundary the probe proved.** Latch pressure when it is
   reached, and write the checkpoint only while a main-conversation `tool_use` is
   outstanding, or when its `tool_use` event arrives. A `result` first is a
   completion race, and nothing is sent. The reply is then the saved place as normal.
   Tests cover crossings on thinking-only, final-text and tool-use events.
2. **High: recovery from a receipt.** The adapter writes the request status
   `checkpoint_saved` with the receipt before cleanup, and `completed` after
   confirmed cleanup. `roll.py` recovery accepts `checkpoint_saved` only with a fresh
   cleanup check (group and owned descendants gone). It still requires an explicit
   prepared state, which the inspector may take from the receipt's candidate.
   `check_state` keeps the old-state failure and evidence rules, the recoveries entry
   is appended, and the original session is retired as today. The controller-loss
   test asserts: ledger `uncertain`, no dispatch, recovery refused until cleanup
   checks, then accepted with a prepared state.
3. **High: cleanup includes the leader.** Record the parent PID and start time. After
   the grace period, TERM the still-matching owned process group, then separately TERM
   still-matching escaped descendants, then confirm all are gone. This applies to
   preflight and worker. The tests include a leader that ignores EOF.
4. **Medium: `init` timing. Resolved by a free local check, 14:22** (no message sent, so
   no model call). With stream-json input and nothing written, Claude Code 2.1.272
   emitted `hook_response`, `hook_progress` and `commands_changed`, but no `init` within
   20s. It exited 0 when stdin closed, with no result. So `init` follows the first
   input, and validating it before sending the work is impossible. Change: the
   preflight validates `init` from its fixed message. The worker sends the work, then
   requires a valid `init` (tools, permission mode, cwd, preflight model) before any
   `assistant` or `user` event, within a startup deadline. A missing, late or invalid
   `init`, or any content event before it, terminates the group and blocks. In the
   probe, `init` (1.5s) preceded the first assistant event (4.4s). The tests cover a
   late `init`, an invalid `init` and content before `init`.
5. **Medium: post-result allowlist.** Only `system/commands_changed` is allowed after
   `result`. After the durable receipt, close stdin immediately and drain to EOF under
   the cleanup deadline. Any other post-result event stops the run. The tests cover the
   allowed subtype and an unknown system subtype.

**Tool-set check, 14:28** (approved by Anthony, "yes"; two Haiku runs, $0.040 total,
Claude Code 2.1.272, the `ask.py` Claude flags plus stream-json input):
- `--tools Read,Glob,Grep` gave `init.tools` `['Glob','Grep','Read']`, and the writable
  set gave `['Edit','Glob','Grep','Read','Write']`. The exact-set rule holds when
  compared as a set. `init.agents` still lists agent types, but no `Task` or `Agent`
  tool is present, so none can be dispatched.
- Each preflight-shaped run returned one `result`: success, `num_turns` 1,
  `queued_turn_count` 0, empty `permission_denials`. The window came from
  `modelUsage["claude-haiku-4-5-20251001"].contextWindow` (200000), matching
  `init.model`.
- **Finding 5 correction:** post-result events were `system/hook_response` in one run
  and `system/hook_progress` then `system/hook_response` in the other, from the user's
  own Stop hooks, which `-p` runs. Revision 3's allowlist is
  `system/commands_changed`, `system/hook_started`, `system/hook_progress` and
  `system/hook_response`. Any `assistant` or `user` event after `result` (a Stop hook
  that blocks and continues the model, for example) still stops the run.

## Codex design review 3 (14:33, "not ready to build") and dispositions

1. **Critical: authority is validated after the work was sent. Accepted.** Proposed fix:
   a same-process bootstrap. Send only a fixed READY message, validate `init` and learn
   the window from its `result` and drain its post-result hook events. Only then send
   the work as the second input. This also removes the separate preflight process. It
   depends on an untested fact: whether a second stream-json input after a `result` in
   the same process starts a second turn. Probe 1 only showed the process still alive
   after `result`. If it doesn't work, the route must disclose that it cannot match
   Codex's authority guarantee rather than send work under an unverified tool set.
2. **Critical: `checkpoint_saved` before finality. Accepted.** The receipt is
   provisional and never promotable. It becomes `completed` only after stdin closes,
   the stream reaches EOF, every post-result event passes validation and cleanup is
   confirmed. Recovery from a provisional receipt stays blocked unless given an
   explicitly inspected, prepared state. There is no automatic promotion, and the
   controller-loss test changes to match.
3. **Medium: validate hook payloads. Accepted.** Probe 1's `hook_response` shape:
   `hook_event`, `hook_id`, `hook_name`, `exit_code`, `outcome`, `output`, `stdout`,
   `stderr`, `session_id`. Accept a post-result hook event only when its `session_id`
   matches, and, for `hook_response`, `outcome == "success"`, `exit_code == 0`, and
   `output` either empty or parsing to JSON with no `decision` of `block` and no
   `continue: false`. Anything else stops promotion. Fixtures: a benign Stop hook and a
   blocking one.

## Bootstrap probe, 14:32 (approved by Anthony, "yes"; one Haiku run, $0.017, `ask.py` flags)

Events are in the scratchpad's `probe/bootstrap-events.jsonl`.
- **A second input after `result` starts a second turn in the same process.** READY
  gave `result` 1 at 3.2s. The second message was sent at 8.6s, and the model called
  `Glob`, answered "2", and `result` 2 followed. There was one `session_id`, and the
  context carried over (13,419 then 13,640 tokens). Finding 1's bootstrap works.
- **`init` is emitted again for every input** (two inits, identical tools
  `Glob, Grep, Read`, `dontAsk`, model). The work turn's `init` (8.9s) preceded its
  first assistant event (9.8s).
- **`num_turns` counts model iterations within a result, not user inputs.** READY gave
  1. One tool call plus the answer gave 2, and probe 1 (one tool call plus the
  injected checkpoint) also gave 2. Revision 2's "`num_turns == 1` without a checkpoint,
  `== 2` with one" is wrong and is dropped.
- **Post-result hook events include async SessionStart hooks**, not only Stop hooks.
  A `SessionStart` `hook_response` arrived at 8.6s after `result` 1, with a multi-line
  output beginning `{"async": true, ...}`.
- **The user's global SessionStart hooks inject context into the worker**: output-style
  text, Superpowers' `EXTREMELY_IMPORTANT` block and the Remember summary. The existing
  `ask.py` Claude route has the same exposure. `--bare` would exclude them but needs
  API-key auth.

## Revision 4 changes (on revision 2 plus revision 3 and the review-3 dispositions)

- **Bootstrap replaces the preflight process.** One worker process runs as follows:
  1. Send READY and validate `init` 1 (the exact tool set, `dontAsk`, cwd, model).
  2. Require one `result`: success, `num_turns == 1`, no tool use, no denials. Take the
     window from `modelUsage[init.model]`.
  3. Send the work input. Require `init` 2, identical to `init` 1, before any assistant
     or user event.

  An `init` that is missing, late or different terminates the group and blocks before
  any tool runs.
- **Result invariants, replacing revision 2's F turn counts.** The bootstrap input
  yields exactly one `result`. The work input, plus at most one injected checkpoint,
  yields exactly one `result`. `queued_turn_count == 0` and empty
  `permission_denials` on each, with one `session_id` throughout. `num_turns` is
  recorded but not asserted beyond the bootstrap.
- **Hook events are validated wherever they arrive** (before, during or after a
  result), for any `hook_event`. The `session_id` must match. A `hook_response` must
  have `outcome == "success"` and `exit_code == 0`, and no line of `output` may parse
  to a JSON object with `decision == "block"` or `continue == false`. Non-JSON lines
  are allowed. The post-result allowlist is `commands_changed`, `hook_started`,
  `hook_progress` and `hook_response` under those rules. Any assistant or user event
  after the work `result` stops the run.
- **Disclosed limit:** the user's global hooks and settings load into unattended Claude
  workers, as on the existing Claude route. v1 records it and does not fix it.

## Codex design review 4 (14:37): one High finding, fix adopted as proposed

1. **High: line-by-line parsing misses a pretty-printed blocking hook response.**
   Accepted. Parse the whole `output` as one JSON value and inspect every nested object.
   If that fails, parse it as JSON Lines and inspect each decoded value. Non-JSON output
   stays allowed. Any object at any depth with `decision == "block"` or
   `continue == false` stops the run. Fixtures: compact, pretty-printed, NDJSON and a
   nested blocking field.

Optional refinements, both adopted:
- The adapter is written as explicit phases: bootstrap (input, `init`, `result`), work
  (input, `init`, readings, optional checkpoint, `result`), then drain to EOF and clean
  up.
- The bootstrap's reading is recorded as `bootstrap_tokens`, separate from work
  readings, so tuning can tell fixed startup context from work growth.

Codex judged every earlier authority, finality, recovery and cleanup finding resolved.
Design status: agreed by Anthony (14:07) subject to Codex review. The only open finding
is closed by Codex's own proposed fix, so the build may start. Codex reviews the full
change set before release, and the release is asked when reached.

## Findings so far (2026-09-15, bounded local reads and Claude Code docs)

- The model does not see the status line. Claude Code pipes a JSON envelope to the
  status-line command; only the rendered text reaches the terminal.
  `~/.claude/statusline-command.sh` reads `.context_window.remaining_percentage`, run
  inside Scorched Earth's wrapper, which owns the `statusLine` slot.
- Status-line input (docs, code.claude.com/docs/en/statusline): `session_id`,
  `context_window.used_percentage`, `remaining_percentage`, `context_window_size`,
  `current_usage`. The percentage counts input, cache-creation and cache-read tokens,
  not output. Values can be null early and right after `/compact`. The status line
  runs on events, debounced at 300ms, and can go quiet while idle unless
  `refreshInterval` is set.
- Hook input (docs, code.claude.com/docs/en/hooks) carries no token or context
  fields, but does carry `session_id` and `transcript_path`. `additionalContext` can
  inject text for supporting events. `PreCompact` exists (matcher `manual`/`auto`).
- This session's transcript records per-response `usage` (input, cache_creation,
  cache_read); a headless `claude -p` run has a transcript but no status line.
- Kerd today: Roll's Codex route observes context usage and requests a saved place at
  65% (`--context-aware`, `--context-fraction`). `skills/switch/references/to-roll.md`
  says: "observed-pressure steering for Claude has not been implemented or proved."
  This work is that gap.

## Proposed direction (not agreed)

- A reading bridge: the status line writes its session's reading to a small per-session
  file, and a hook reads the file for its own `session_id`. The transcript's last
  `usage` is the fallback where no status line runs.
- A hook injects a short notice only on crossing a line, not every turn.
- Interactive session at the line: finish the current step, Switch Out, stop and ask
  Anthony to start a fresh session.
- Managed or loop run at the line: request a saved place and Roll into a fresh Claude
  run, as the Codex route already does.
