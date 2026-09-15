# Score: context-aware Claude Roll (design revisions 2–4)

Authority: Anthony, 2026-09-15 14:07, "check with codex but looks good". Codex's four
design reviews then cleared the design, the last finding closed by Codex's own proposed
fix. This score covers the build and its checks. Commit, push and release are asked when
reached.

The contract is [work.md](work.md): "Design, revision 2", then the "revision 3 changes",
the "Bootstrap probe", the "Revision 4 changes" and "Codex design review 4". Where they
differ, the later section wins. Conductor (Claude) writes every step, so a defect in a
step returns to Conductor.

Review cadence for `codex-tui`: checkpoints + before-push (Anthony 15:43, recorded
through Agent). Checkpoint C follows S1+S2. Review R covers the full change set before
any commit.

| Step | Owner / route | Model requested | Effort | Tag |
| --- | --- | --- | --- | --- |
| S1 `claude_roll.py` adapter + tests | Player, native subagent `kerd:effort-xhigh` | Opus 5 | xhigh | [delegate] |
| S2 `roll.py` wiring and recovery + tests | Player, native subagent `kerd:effort-high` | Opus 5 | high | [delegate] |
| C checkpoint review of S1+S2 | codex-tui (cadence: checkpoints) | existing session | unverified | — |
| D docs (to-roll, managed-conductor, README, Switch skill) | written after C | — | — | — |
| V suites, gates, live trial, release surfaces | Conductor | current session | — | [keep] |
| R change-set review | codex-tui (cadence: before-push) | existing session | unverified | — |

S1 and S2 own disjoint files and run in parallel. S2 codes against S1's interface as
written below, not against S1's return.

Change reads use `change_read.py` baselines `ctx-s1` and `ctx-s2`, taken before
dispatch.

---

## S1: `claude_roll.py`, the Claude stream-json context-aware bridge

**Intended result.** A Roll worker running as a fresh `claude -p` process is watched
for context usage. At 65% of its reported window (used tokens) it is asked, at a tool
boundary, to return its saved place. Its reply is kept as a durable receipt before
cleanup. The run then ends with verified cleanup, so `roll.py` can start a genuinely
fresh Claude run. It stops rather than guesses at every uncertain point, as
`codex_roll.AppServerBridge` does.

**Why this shape.** Codex's route has a live app-server with `turn/steer` and a
`thread/start` authority response. Claude has neither. The probes (work.md) showed that
the stream-json CLI emits `init` only after the first input and repeats it per input.
It reports the window only in a `result`, injects a mid-turn user message at the next
tool boundary, and emits hook events after results. Hence the bootstrap turn, the
per-input `init` validation, the tool-boundary latch and the post-result allowlist.

**Owned paths.**
- New `skills/switch/scripts/claude_roll.py`.
- New `skills/switch/scripts/tests/test_claude_roll.py`.
- Optionally a new fixture module `skills/switch/scripts/tests/claude_stream_fixture.py`.
- `skills/switch/scripts/codex_roll.py`, limited to two behaviour-preserving
  extractions:
  1. `ContextWatch.observe_tokens(used, window, detail)` holds the threshold logic.
     `observe(usage)` keeps its exact validation and messages and delegates to it.
     `detail` is stored as the reading's `last` value.
  2. A module-level `shutdown_owned(transport, server, record)` holds the current
     `AppServerBridge._shutdown` body verbatim, and `_shutdown` calls it.

  The existing `test_codex_roll.py` must pass unmodified.

Nothing else. No docs, no `roll.py`, no version files.

**Interface (S2 depends on this exactly).**
- `class ClaudeStreamBridge`: `context_aware = True`.
  `__init__(self, project, transport, fraction=0.65, test_tokens=None)` is the same as
  `AppServerBridge.__init__`, validating through `ContextWatch`, with attributes
  `transport`, `core`, `root`, `state`, `fraction`, `test_tokens`.
- `close(alias)` delegates to `self.core.close(alias)`.
- `run(target, prompt, role, session, request_id, writable=False, model=None,
  effort=None, timeout=None, hold=False, checkpoint_requested=None,
  checkpoint_instruction=None)`:
  - Take the same session lock and `ensure_resolved` as `AppServerBridge.run`.
  - `ValueError` unless `target == "claude"` and model and effort are given.
  - `ProtocolError` (from `codex_roll`) if `hold` is true or `checkpoint_requested`
    is not None: "Claude context-aware Roll has no retainable source or live control
    in v1".
  - `ProtocolError` if the session alias file already exists (fresh alias only).
- **Do not define** `inspect_held`, `held_result`, `held_cancelled` or `release_held`.
  S2 uses the absence of `release_held` to refuse `--control`.
- Returned record keys, as in the Codex record where named the same:
  - identity: `request_id`, `session`, `target`, `project`, `owner_pid`,
    `requested_model`, `requested_effort`, `authority`, `route: "claude-stream-json"`,
    `context_test_trigger`;
  - lifecycle: `status` (`completed` | `failed` | `cancelled` | `interrupted`),
    `provider_completed`, `started_at`, `finished_at`, `process_id`, `error`;
  - session: `session_id`, `model` (from `init.model`);
  - reply: `reply`, `checkpoint_candidates` (a one-element list on success),
    `num_turns`, `estimated_cost_usd` (the work `result.total_cost_usd` when numeric);
  - context: `context_window`, `bootstrap_tokens`, `context_readings`,
    `context_trigger`, `checkpoint_requested` (the reason string or absent),
    `steer_race`;
  - `protocol_events`: a list of `{"type", "subtype"}` only, never content;
  - cleanup: `owned_children`, `owned_child_count`, `owned_children_gone`,
    `cleanup_error`.
- Files: `request.json`, `result.json` and `stderr.txt` (mode 0600) under
  `core.request_path(request_id)`, created as in `AppServerBridge._run`. The session
  alias file is saved in `finally` exactly as there.

**Command.** `self.core.command("claude", None, writable, model, effort)` plus
`["--input-format", "stream-json"]`. Popen with `cwd=root`, stdin and stdout pipes,
stderr to the request's file, `text=True`, `start_new_session=True`. A reader thread
puts parsed JSON lines on a queue, as `codex_roll.AppServer` does. Make the process
class patchable, like `AppServer`. A user input is one line:
`{"type":"user","message":{"role":"user","content":TEXT}}`.
- Requested tools: `{"Read","Glob","Grep"}`, plus `{"Edit","Write"}` when writable.
- `BOOTSTRAP = "Reply READY and nothing else. Do not use any tools."`
- Timeouts as class attributes, so tests can shrink them: `STARTUP_TIMEOUT = 60`
  (per `init`), `DRAIN_TIMEOUT = 10`.

**Event rules, all phases.**
- A line that is not a JSON object stops the run.
- Every event carrying `session_id` must match the first `init`'s.
- `type == "system"`:
  - `init` is handled per phase.
  - `hook_started`, `hook_progress` and `hook_response` must pass `hook_ok` (below).
  - `commands_changed`, `thinking_tokens`, `task_started`, `task_notification` and
    `api_retry` are recorded only.
  - `compact_boundary`, `permission_denied`, and any other subtype stop the run.
- `type == "rate_limit_event"` is recorded only.
- `assistant`, `user` and `result` are handled per phase. Any other type stops the run.
- **`hook_ok(event, sid)`:** `session_id == sid`. For `hook_response`, also
  `outcome == "success"` and `exit_code == 0`. Then the `output` string is inspected:
  parse it whole as JSON, or else each line that parses as JSON, skipping non-JSON
  lines. It fails if any dict at any depth has `decision == "block"` or
  `continue is False`.
- **Readings.** An `assistant` event with `parent_tool_use_id` null needs
  `message.id` as a string and `message.usage` with non-negative ints
  `input_tokens`, `cache_creation_input_tokens` and `cache_read_input_tokens`,
  otherwise the run stops. `used` is their sum. Dedupe by `message.id`: call
  `watch.observe_tokens(used, window, {"message_id": id, "used": used})` only when
  that id is new or its `used` changed. Subagent assistant events (non-null
  `parent_tool_use_id`) are ignored for readings.

**Phase 1: bootstrap.**
1. Send `BOOTSTRAP`.
2. Require a valid `init` within `STARTUP_TIMEOUT`, before any `assistant`, `user` or
   `result`:
   - `session_id` is a non-empty string;
   - `Path(cwd).resolve() == root`;
   - `permissionMode == "dontAsk"`;
   - `set(tools)` equals the requested set;
   - `model` is a non-empty string.

   Keep it as the reference `init`.
3. Main assistant content may be `text` or `thinking` only. A `tool_use` stops the run.
4. Exactly one `result`, with:
   - `subtype == "success"`, `is_error is False`;
   - `num_turns == 1`, `queued_turn_count == 0`, `permission_denials == []`;
   - a matching `session_id`;
   - `modelUsage[init.model].contextWindow` a positive int, which becomes
     `context_window`.

   Otherwise stop, with "no guessed window".
5. `bootstrap_tokens` is the last deduped main reading. Bootstrap readings are not
   passed to the watch.

**Phase 2: work.**
1. Send `prompt`.
2. Require a second `init` equal to the reference on `session_id`, `cwd`,
   `permissionMode`, `set(tools)` and `model`, within `STARTUP_TIMEOUT` and before any
   `assistant`, `user` or `result` of this phase. Missing, late or different stops
   the run.
3. Track outstanding main tool uses: add each main assistant `tool_use` block `id`, and
   remove on a `user` event content block `tool_result` with that `tool_use_id`.
4. **Pressure latch.** When `observe_tokens` returns True:
   - emit the `saving_place` status line, as Codex does;
   - set `latched`, and record `context_trigger` durably by saving `result.json`, as
     the Codex route does on each reading.
5. While `latched` and not yet sent, write the checkpoint input once, at the moment a
   main `tool_use` is outstanding (now, or when the next main `tool_use` block
   arrives). Its text is `"Roll requested from observed context usage. " +
   (checkpoint_instruction or the same default wording as codex_roll)`. Set
   `checkpoint_requested` to the reason. Never send a second one.
6. If the `result` arrives while latched and unsent, record `steer_race = "turn
   completed before a tool boundary"` and send nothing.
7. Exactly one `result` for this phase, with:
   - `subtype == "success"`, `is_error is False`;
   - `queued_turn_count == 0`, `permission_denials == []`;
   - a matching `session_id`;
   - `result` a non-empty string.

   Record `num_turns` without asserting it.
8. A second `result`, or any `assistant` or `user` event after it, stops the run.
9. No main reading at all in this phase stops the run: "context-aware continuation is
   unproved".

**Receipt, then drain, then cleanup.**
1. Set `record.update(provider_completed=True, reply=text, checkpoint_candidates=[text])`
   and save `result.json` as `{**record, "status": "running", "phase":
   "checkpoint_saved"}`. Read it back, and stop unless `checkpoint_candidates` match.
   This receipt is provisional and never promotable.
2. Close stdin. Read to EOF within `DRAIN_TIMEOUT`. Only `system` events with subtype
   `commands_changed`, `hook_started`, `hook_progress` or `hook_response` (the last
   three passing `hook_ok`) are allowed. Anything else, or no EOF in time, sets
   `status="failed"` and `provider_completed=False`.
3. Cleanup through `codex_roll.shutdown_owned(self.transport, server, record)`. Call it
   with the identity snapshot taken before stdin closes, because that function
   snapshots descendants first. If needed, split it so that `ClaudeStreamBridge`
   snapshots before the drain, keeping the Codex path unchanged. It stops the owned
   process group through `transport.Bridge.stop`, then still-matching escaped
   descendants, and confirms both the group and the children are gone.
4. `status="completed"` only when the drain passed and `owned_children_gone` is True
   with no `cleanup_error`.

**Cancel and timeout.** Same as Codex: `cancel.json` or an elapsed optional `timeout`
leads to `status="cancelled"`, the error recorded and the owned process stopped. Any
exception sets `failed` (or `cancelled`), with `provider_completed=False`, and cleanup
still runs in `finally`.

**Tests** (`test_claude_roll.py`, unittest, no model or network calls). Use a fake
process scripted per phase: a queue of events that becomes available after each
`send`, and a mock `proc`, patching `descendants`, `children_gone`, `os.killpg`,
`stop_owned_children` and `time.sleep` as `test_codex_roll.py` does. Shapes are copied
from the probe events in work.md. Required cases:
1. Happy path. `init` × 2, bootstrap `result` with window, work readings under the
   threshold, success `result`, hook events after it, EOF. Status completed,
   `bootstrap_tokens`, `context_window` and readings recorded, command includes
   `--input-format stream-json` and the exact `--tools`.
2. Pressure crossing on a `thinking`-only event, then a later `tool_use`: the
   checkpoint is sent once, after the `tool_use`.
3. Crossing while a `tool_use` is outstanding: sent immediately. A second crossing
   sends nothing.
4. Crossing on a final `text` event, then `result`: `steer_race` recorded, nothing
   sent, completed.
5. `init` failures: missing within the timeout, wrong cwd, wrong permission mode, an
   extra tool, missing model, work `init` differing (model or tools), content before
   the work `init`.
6. Bootstrap failures: a `tool_use`, `num_turns` of 2, a missing or zero window, a
   model missing from `modelUsage`.
7. Duplicate `message.id` with the same usage is observed once. Changed usage on the
   same id is observed again.
8. Subagent assistant events are ignored for readings.
9. Result failures: `queued_turn_count` 1, non-empty `permission_denials`, a
   conflicting `session_id`, a second `result`, an assistant event after `result`,
   `is_error`, an empty `result`.
10. Malformed JSON line, malformed usage, an unknown system subtype, and
    `compact_boundary`.
11. Hook validation: a benign `hook_response` passes. Failing cases are
    `outcome: "error"`, a non-zero `exit_code`, compact JSON `{"decision":"block"}`,
    pretty-printed multi-line JSON with a nested `"continue": false`, NDJSON with a
    blocking second line, and a mismatched `session_id`. Non-JSON output passes.
12. Post-result: an unknown system subtype during the drain fails it.
    `commands_changed` passes.
13. The receipt is saved and read back before stdin closes (assert ordering, as
    `test_reply_is_saved_and_read_back_before_source_shutdown` does). A failed
    read-back leaves the run not completed.
14. Cleanup: a leader that ignores EOF (the wait times out) goes through `Bridge.stop`,
    a survivor child is stopped, and uncertain shutdown leaves the run not completed.
15. `hold=True` or `checkpoint_requested` is refused. No `release_held` attribute
    exists. A target other than claude, or a missing model or effort, is refused.
16. Cancel file and timeout stop the run and record cancelled.

**Verification.**
- `python3 -m unittest discover -s skills/switch/scripts/tests -p 'test_*roll*.py'`:
  all pass, including the 170 existing tests unchanged in count and content for
  `test_codex_roll.py` and `test_roll.py`.
- `python3 -m py_compile skills/switch/scripts/claude_roll.py`.

**Stop and report** with files changed, test counts, any spec point you could not meet
and why, and any place where the probe shapes were ambiguous. Don't commit.

---

## S2: `roll.py` wiring, the `--control` refusal and recovery parity

**Intended result.** `roll.py --target claude --context-aware` uses S1's
`ClaudeStreamBridge`. `--control`, and held sources generally, are refused for any
bridge without `release_held`. Recovery demands cleanup evidence for both
context-aware routes. The Codex behaviour is unchanged.

**Owned paths.** `skills/switch/scripts/roll.py` and
`skills/switch/scripts/tests/test_roll.py`. Nothing else.

**Changes.**
1. `main()`: with `--context-aware`, `--target codex` keeps its current code. With
   `--target claude`, `from claude_roll import ClaudeStreamBridge` (lazy, inside
   `main`) and `bridge = ClaudeStreamBridge(args.project, connection(),
   args.context_fraction, args.test_roll_at_tokens)`. Remove the "Codex only" refusal.
   The help text becomes "Use observed context usage (Codex app-server stdio or Claude
   stream-json)".
2. `main()`: `--control` with `--target claude` gives
   `RollError("Live control and held sources are Codex-only; Claude context-aware Roll
   has no retainable source")`, before `LiveControl` is constructed. Exit 2 with the
   JSON error on stderr, as other RollErrors do.
3. `Roller.run`: replace `if control is not None and not getattr(self.bridge,
   "context_aware", False)` with a check that also refuses when
   `callable(getattr(self.bridge, "release_held", None))` is false. Same message
   family: "Live control requires the held-source Codex adapter".
4. `Roller.recover`: the cleanup-evidence rule currently applies only when
   `route == "app-server-stdio"`. It must apply when `route in {"app-server-stdio",
   "claude-stream-json"}`, keeping `from codex_roll import children_gone`. The accepted
   request statuses stay exactly as they are. A result left as `status: "running"`,
   `phase: "checkpoint_saved"` (a controller lost after the receipt) therefore remains
   unrecoverable automatically. That is intended for v1 and pinned by a test.

**Tests** (add to `test_roll.py`; no provider launch). Patch `sys.modules["claude_roll"]`
with a stub module whose `ClaudeStreamBridge` records its constructor arguments.
1. `main` with `--target claude --context-aware --context-fraction 0.5
   --test-roll-at-tokens 1000` constructs `ClaudeStreamBridge` with those values. Patch
   `Roller` to avoid a run.
2. `main` with `--target claude --context-aware --control` exits 2 with the Codex-only
   message, and `LiveControl` is not constructed.
3. `Roller.run(control=<object>)` with a bridge lacking `release_held` raises the
   held-source RollError before any dispatch.
4. `recover` for a `claude-stream-json` result without `owned_children_gone`: with
   `children_gone` False it is refused, and with `children_gone` True it proceeds as
   the existing Codex recovery test does. Mirror that test's setup.
5. `recover` for a result `{"status": "running", "phase": "checkpoint_saved"}` on
   either route is refused ("Resolve the retained provider request…").
6. The existing Codex `--context-aware` construction path is still used for `--target
   codex`. Add a test if none exists.

**Verification.** `python3 -m unittest discover -s skills/switch/scripts/tests -p
'test_roll.py'` passes. The `test_*roll*.py` pattern passes too, once S1 has landed; if
S1 isn't there yet, report that only.

**Stop and report** with files changed, test counts and any spec ambiguity. Don't
commit.

---

## Returns and checks (Conductor, 2026-09-15)

**S2** returned at 15:52, checked.
- Change read `ctx-s2`: 2 tracked paths changed, no unexpected changes, HEAD unchanged.
  The paths outside S2's scope were the controller's own work-record files.
- `job_evidence.py`: `kerd:effort-high`, requested `opus`, observed claude-opus-5 ×31
  at high ×31.
- The diff matches the step. `test_roll.py` has 28 tests (21 before), and the new
  tests failed against the HEAD `roll.py`.
- Player notes, both accepted:
  1. `--target claude --control` is refused with the Codex-only message even without
     `--context-aware`.
  2. The recovery fixture needs `owned_children` for `children_gone` to be reached.
- Earlier failure: `test_roll_control.py` run alone errors on import. Reproduced on a
  clean HEAD copy, so it predates this build; it passes inside discovery.

**S1** returned at 16:04, checked.
- Change read `ctx-s1`: `codex_roll.py` modified, `claude_roll.py` and
  `test_claude_roll.py` added, no unexpected changes, HEAD unchanged.
- `job_evidence.py`: `kerd:effort-xhigh`, requested `opus`, observed claude-opus-5 ×54
  at xhigh ×54.
- `codex_roll.py` diff: `observe_tokens` extracted, and the shutdown body moved
  verbatim into `snapshot_owned`, `finish_owned` and `shutdown_owned`.
  `test_codex_roll.py` is unmodified, 91/91.
- `claude_roll.py` (458 lines) was read in full against the step.
- `test_claude_roll.py`: 39 tests. The player's mutation checks caught 9 of 9
  deliberate breaks. The one uncatchable guard (the final `completed` check) is a
  backstop.
- Player-disclosed choices, accepted pending checkpoint review C:
  1. Hook `session_id`s seen before the first `init` are held and checked when it
     arrives.
  2. A repeated `init` inside a phase must equal the reference.
  3. There is no quiet period after the bootstrap result; late hooks are validated
     during the work phase.
  4. `redacted_thinking` in the bootstrap stops the run.
  5. A missing bootstrap reading leaves `bootstrap_tokens` null.
  6. A missing `parent_tool_use_id` counts as main.
  7. `estimated_cost_usd` is cumulative, including the bootstrap.
  8. Non-tool-result user events in the work phase are accepted.
  9. The default checkpoint wording is copied from Codex's; no test ties them.

**Verification at 16:08:**
- Switch suite: 425 tests OK.
- Agent suite: 182 tests OK.
- `gate.py release`: clean.
- `gate.py audit`: clean, with its existing requirements trace-gap finding.

---

## Codex checkpoint review C (16:14, "not ready for docs and live trial") and repairs

Conductor checked each finding. All five are accepted; the steps are Conductor's, so
Conductor writes the repairs and routes them to the original players.

1. **High: the receipt read-back compares only `checkpoint_candidates`.** Accepted.
   → S1-r1.
2. **High: a provisional receipt can never be recovered, though revision 3 cleared an
   inspected path.** Accepted: S2's step wrongly pinned the refusal, and the defect is
   Conductor's. `ask.exclusive` is `flock`-based, so a dead controller's
   `owner.lock` is free. → S2-r1.
3. **Medium: arbitrary user events are accepted during work.** Accepted. Probe 1
   showed no echo of the injected checkpoint; its only user event was a
   `tool_result`. → S1-r1.
4. **Medium: a missing `parent_tool_use_id` is treated as main.** Accepted. Every
   assistant and user event in both probes carried the key, as null. → S1-r1.
5. **Medium: the leader's start time is not recorded.** Accepted. → S1-r1 records it,
   and S2-r1 uses it in recovery.

Optional, adopted: one shared default checkpoint instruction. → S1-r1.

### S1-r1 (repair to S1; owned paths as in S1, plus the constant in `codex_roll.py`)
- **Receipt.** Build the complete receipt dict once (`{**record, "status": "running",
  "phase": "checkpoint_saved"}`, including `process_start`), save it, and require
  `transport.read(...) == receipt`. Compare `json.dumps(sort_keys=True)` strings too.
  Test a read-back that alters a field other than the candidates (for example
  `session_id` or `context_trigger`): not completed.
- **User events in the work phase.** Accept only a `user` event whose
  `parent_tool_use_id` is null and whose `message.content` is a non-empty list, every
  block being `{"type": "tool_result", "tool_use_id": <non-empty str>}` naming a
  currently outstanding main tool use. Remove each named id. Anything else stops the
  run: a text or string content, an unknown id, an empty list, malformed blocks. A
  user event with a non-null (non-empty string) `parent_tool_use_id` belongs to a
  subagent and is ignored, since `Task` isn't in the tool set. Tests cover each refused
  shape and the subagent case.
- **Ownership field.** On `assistant` and `user` events, `parent_tool_use_id` must be
  present. Explicit null means main, a non-empty string means subagent, and anything
  else (missing, empty string, non-string) stops the run. Tests cover missing, empty
  string and an integer.
- **Leader identity.** Immediately after `ClaudeStream` starts, record
  `record["process_start"]` as the leader's `ps -p <pid> -o lstart=` output (stripped),
  via a small patchable helper. Failure to read it stops the run with an error. Save
  `result.json`. Test that it is recorded and that a failure stops before bootstrap.
- **Shared wording.** Move the default checkpoint instruction into `codex_roll.py` as
  the module constant `DEFAULT_CHECKPOINT_INSTRUCTION`. Use it in `AppServerBridge._run`
  with byte-identical text, and import it in `claude_roll.py`. `test_codex_roll.py`
  stays unmodified and passing.
- **Verification.** The `test_*roll*.py` pattern passes. List the new tests.

### S2-r1 (repair to S2; owned paths `roll.py` and `test_roll.py`)
`Roller.recover` gains one inspected path for a controller lost after the receipt, on
either context-aware route. It applies only when **all** of the following hold:
- **Ledger:** `prior["status"] == "running"`. The `owner.lock` is already held by this
  `recover` call through `exclusive`, which proves no live controller, since the lock
  is `flock`-based.
- **Request:** the retained result has `status == "running"`,
  `phase == "checkpoint_saved"`, `route` in `{"app-server-stdio",
  "claude-stream-json"}`, a matching `project` and `request_id`, and
  `provider_completed is True`.
- **Owner:** `owner_pid` is an int and not alive (`os.kill(pid, 0)` raises
  `ProcessLookupError`). Otherwise it is refused as "controller may still be alive".
- **Process group:** the existing `killpg(pid, 0)` probe must show the group gone. As
  the one exception, the group is treated as gone when `process_start` is recorded,
  `ps -p pid -o lstart=` returns a *different* non-empty start time, and that PID leads
  its own group. A reused PID can only lead a new group once the original group is
  gone. Never signal it.
- **Children:** `owned_children` is a dict and `children_gone(owned_children)` is True.
- **State:** the supplied prepared state passes the existing `check_state(...,
  old_state)` and `artifact_snapshot` checks, and a non-empty reason is given, as today.

Everything else is unchanged:
- no automatic promotion, and the receipt's candidate is never read as the new place;
- the existing statuses and paths stay as they are;
- the recoveries entry records `previous_status: "running"` and
  `previous_phase: "checkpoint_saved"`.

Tests:
- replace `test_receipt_saved_but_controller_lost_is_not_recoverable_on_either_route`
  with a refusal test for each missing condition (live owner, group present, children
  present, wrong phase, `provider_completed` false, a bad prepared state) and an
  acceptance test when all hold, both routes;
- the ledger `running` without a receipt is still refused;
- a reused-leader start time allows recovery, and the same start time is refused.

Verification: `test_roll.py` and the `test_*roll*.py` pattern pass.

---

## Live trials (Conductor, 2026-09-15 16:20–16:25; disclosed test thresholds, not real exhaustion)

Both trials used throwaway Git repos in the session scratchpad, a 37KB `source.md`, and
the agreement "write notes/1–6.md, then review". The command was `roll.py --target
claude --model sonnet --effort low --context-aware --max-runs 2`, on Claude Code 2.1.272
with the user's global hooks and plugins loaded. Total cost $0.86.

**Trial 1, `--test-roll-at-tokens 52000`, $0.34.**
- Bootstrap: `init` validated, model claude-sonnet-5, window 1,000,000 from
  `modelUsage`, `bootstrap_tokens` 18,865.
- Readings: 19,750 → 31,311 → 33,512 → 66,231 (after reading the source) → 70,183.
- The crossing at 66,231 sent the checkpoint while a tool call was outstanding. The
  worker returned a valid `continue` place with memory. Receipt, drain and cleanup
  passed: 1 owned child, gone. Result `completed`.
- `roll.py`'s existing no-progress guard then refused continuation: "No new artifact
  evidence…". No note had been written yet, because the test threshold sat below the
  first unit of work. That was the trial's design, not the adapter's.

**Trial 2, `--test-roll-at-tokens 76000`, $0.52.**
- Readings: 19,756 … 37,836 → 69,101 → 77,096.
- The crossing came on the final text event, so the turn completed before a tool
  boundary: `steer_race` was recorded and nothing was sent.
- The worker wrote all six notes and returned `review`. Receipt, drain and cleanup
  passed (1 child, gone); result `completed`, 32 model iterations.
- `roll.py` refused: "Worker did not return an unambiguous saved place". The reply was
  prose followed by a fenced JSON block, and the existing `parse_reply` accepts only a
  bare or whole-fenced JSON reply.

**Observed live:** bootstrap authority and window; deduped readings; a checkpoint sent
at a tool boundary; the steer race; receipt, drain with real hook events, verified
cleanup; the two existing `roll.py` guards.
**Not observed live:** a completed hand-over to a second fresh Claude run, and receipt
recovery.
**Finding for review:** a Claude worker at low effort prefixed its saved place with a
sentence despite "Return ONLY a JSON object". `parse_reply` failing closed is correct,
but it makes the Claude route brittle. Deciding whether to change the prompt, the
parser or neither is scope for R and Anthony.

**Parser change (Anthony 17:23: "Proceed with the parser change, Codex review, and the third
trial").**
- Change: `roll.parse_reply` accepts a bare JSON reply, or prose around exactly one
  `` ```json `` fence with no other fence. Everything else is refused as before.
- Callers: `roll.py`, `managed_to.py` and `conductor_roll.py` share it.
- Tests: `ParseReplyTests` in `test_roll.py` has 3 tests with 8 refusal subtests.
- Mutation check: the old parser fails 2 of those tests.
- Switch suite: 443 tests OK.

**Trial 3, `--test-roll-at-tokens 72000`, $0.38.**
- Readings: 19,756 → 19,870 → 31,366 → 32,912 → 64,308 → 67,918. The threshold was never
  reached, so no checkpoint was sent.
- The worker wrote all six notes and replied with prose followed by one `` ```json ``
  fence. The new parser accepted it.
- `roll.py` validated and saved the place and recorded the run in history. Ledger
  `review`, exit 0. Cleanup passed (1 child, gone).
- Observed live end to end: a complete Claude Roll run from launch to a saved place and
  the ledger. Still not observed live: a pressure-triggered handover to a second fresh
  run. Pressure crossings came only on the large read, before any artifact existed.
- Trial spend in total: $1.24.

## Codex before-push review R (17:36, "not ready") and fixes

1. **High: loose JSON outside the fence was silently discarded.** Fixed:
   `parse_reply` now refuses when the surrounding prose holds any decodable JSON object
   or array. Added subtests for conflicting JSON before the fence, after it, and an
   array in the prose. The mutation check (removing the refusal) fails all three.
   Replaying the real trial 2 and 3 replies still parses both.
2. **Medium: README still showed v0.129.0 as current.** Fixed: a v0.130.0 What's New
   entry with the evidence boundary (three test-threshold trials, one complete run,
   no live pressure handover to a second run).

Optional refinements not taken: recording prose-wrapped acceptance as a protocol
deviation, and changing the plugin capability descriptions (still true as written).
Switch suite OK, release gate clean. Re-review R2 sent for the before-push gate.
