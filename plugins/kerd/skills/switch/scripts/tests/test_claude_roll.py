"""Claude stream-json Roll bridge regressions using isolated files and scripted fake streams.

No provider processes, model or network calls, installed skills, or live sessions are touched.
Event shapes follow the 2026-09-15 probes recorded in docs/work/context-awareness/work.md.
"""

import collections
import contextlib
import importlib.util
import inspect
import io
import itertools
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


SCRIPTS = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


codex = load("claude_roll_codex_under_test", SCRIPTS / "codex_roll.py")
ask = load("claude_roll_transport_under_test", SCRIPTS.parents[1] / "conductor/scripts/ask.py")
with patch.dict(sys.modules, {"codex_roll": codex}):
    adapter = load("claude_roll_under_test", SCRIPTS / "claude_roll.py")


SID = "f696fe37-dba3-47bc-a02e-010ccc44b67f"
MODEL = "claude-haiku-4-5-20251001"
REPLY = '{"status":"review"}'
CHECKPOINT_PREFIX = "Roll requested from observed context usage. "
LEADER_START = "Tue Sep 15 16:20:00 2026"


def hook(subtype="hook_response", output="", hook_event="Stop", **changes):
    event = {"type": "system", "subtype": subtype, "hook_id": "d14d1d48-a3e5-4d22-a4cf-5647acf21c32",
             "hook_name": f"{hook_event}:startup", "hook_event": hook_event,
             "uuid": "52cbdeb1-d9c0-4aed-a52c-dfedb62e4a71", "session_id": SID}
    if subtype == "hook_response":
        event.update(output=output, stdout=output, stderr="", exit_code=0, outcome="success")
    elif subtype == "hook_progress":
        event.update(stdout=output, stderr="", output=output)
    event.update(changes)
    return event


def system(subtype, **fields):
    return {"type": "system", "subtype": subtype, "session_id": SID, "uuid": "u-" + subtype, **fields}


def rate_limit():
    return {"type": "rate_limit_event", "rate_limit_info": {"status": "allowed", "rateLimitType": "five_hour"},
            "uuid": "f3cd6695", "session_id": SID}


def thinking():
    return {"type": "thinking", "thinking": "", "signature": "EpYGCrIBCBEYAipA"}


def text(value):
    return {"type": "text", "text": value}


def tool_use(ident, name="Glob"):
    return {"type": "tool_use", "id": ident, "name": name, "input": {"pattern": "*.py"},
            "caller": {"type": "direct"}}


def assistant(message_id, used, *blocks, parent=None):
    fresh = min(used, 10)
    creation = (used - fresh) // 3
    usage = {"input_tokens": fresh, "cache_creation_input_tokens": creation,
             "cache_read_input_tokens": used - fresh - creation,
             "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": creation},
             "output_tokens": 1, "service_tier": "standard"}
    return {"type": "assistant", "message": {"model": MODEL, "id": message_id, "type": "message",
            "role": "assistant", "content": list(blocks), "stop_reason": None, "usage": usage},
            "parent_tool_use_id": parent, "session_id": SID, "uuid": "a-" + message_id,
            "request_id": "req_011Cf5hjBfAT8tSXBue7NEwN"}


def tool_result(ident, parent=None):
    return {"type": "user", "message": {"role": "user", "content": [
                {"tool_use_id": ident, "type": "tool_result", "content": "probe.py\nbootstrap.py"}]},
            "parent_tool_use_id": parent, "session_id": SID, "uuid": "t-" + ident}


def result(reply, num_turns=1, window=1000, **changes):
    entry = {"inputTokens": 909, "outputTokens": 136, "costUSD": 0.0125, "contextWindow": window,
             "maxOutputTokens": 32000, "canonicalModel": "claude-haiku-4-5"}
    if window is None:
        del entry["contextWindow"]
    event = {"type": "result", "subtype": "success", "is_error": False, "num_turns": num_turns,
             "result": reply, "session_id": SID, "total_cost_usd": 0.0169358,
             "usage": {"input_tokens": 18}, "permission_denials": [], "terminal_reason": "completed",
             "queued_turn_count": 0, "result_index": 0,
             "modelUsage": {"claude-internal-helper": {"contextWindow": 5}, MODEL: entry}}
    event.update(changes)
    return event


class FakeStdin(io.StringIO):
    def __init__(self, on_close):
        super().__init__()
        self.on_close = on_close

    def close(self):
        if not self.closed:
            self.on_close()
        super().close()


class FakeClaude:
    """Scripted per input: script N becomes readable after the Nth send; drain after stdin closes."""

    def __init__(self, scripts, drain=(), eof=True, stall=False):
        self.scripts, self.drain, self.eof, self.stall = [list(s) for s in scripts], list(drain), eof, stall
        self.pending = collections.deque()
        self.sent, self.timeline = [], []
        self.on_close = None
        self.proc = types.SimpleNamespace(pid=123456789, stdin=FakeStdin(self._closed), stdout=io.StringIO(),
                                          wait=Mock(return_value=0), poll=Mock(return_value=None))
        self.reader = Mock()
        self.reader.is_alive.return_value = False

    def send(self, value):
        self.sent.append(value)
        self.timeline.append(("send", value))
        if len(self.sent) <= len(self.scripts):
            self.pending.extend(self.scripts[len(self.sent) - 1])

    def _closed(self):
        self.timeline.append(("close", None))
        if self.on_close:
            self.on_close()
        self.pending.extend(self.drain)
        if self.eof:
            self.pending.append(adapter.EOF)

    def receive(self, timeout=0.25):
        if not self.pending:
            if self.stall:
                return None
            raise codex.ProtocolError("Fixture stream exhausted")
        item = self.pending.popleft()
        if isinstance(item, BaseException):
            raise item
        if callable(item):
            return item()
        if item is not adapter.EOF:
            self.timeline.append(("event", item))
        return item

    def checkpoints(self):
        return [value for value in self.sent if value.startswith(CHECKPOINT_PREFIX)]


class ClaudeStreamBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="claude-roll-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.stop = Mock()
        self.calls = 0
        self.writable = True

        class Core:
            def __init__(self, root):
                self.root = root
                self.state = root / ".git/cross-llm"
                (self.state / "sessions").mkdir(parents=True)
                (self.state / "requests").mkdir()
                self.commands = {"codex": ["codex"], "claude": ["claude"]}

            def session_path(self, alias):
                return self.state / "sessions" / (alias + ".json")

            def request_path(self, ident):
                return self.state / "requests" / ident

            status = ask.Bridge.status
            resolve = ask.Bridge.resolve
            ensure_resolved = ask.Bridge.ensure_resolved
            command = ask.Bridge.command
            close = ask.Bridge.close

        Core.stop = staticmethod(self.stop)
        self.transport = types.SimpleNamespace(Bridge=Core, save=ask.save, read=ask.read, now=ask.now,
                                               shutdown_signals=contextlib.nullcontext,
                                               exclusive=ask.exclusive)
        self.bridge = adapter.ClaudeStreamBridge(self.root, self.transport)
        self.descendants = self.enterContext(patch.object(codex, "descendants", return_value={}))
        self.children_gone = self.enterContext(patch.object(codex, "children_gone", return_value=True))
        self.group_probe = self.enterContext(patch.object(codex.os, "killpg", side_effect=ProcessLookupError))
        self.stop_children = self.enterContext(patch.object(codex, "stop_owned_children"))
        self.leader_start = self.enterContext(patch.object(adapter, "leader_start", return_value=LEADER_START))
        self.enterContext(patch.object(codex.time, "sleep"))
        self.output = self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    # Fixtures -----------------------------------------------------------------

    def tools(self):
        return ["Glob", "Grep", "Read"] + (["Edit", "Write"] if self.writable else [])

    def init(self, **changes):
        event = {"type": "system", "subtype": "init", "cwd": str(self.root), "session_id": SID,
                 "tools": self.tools(), "mcp_servers": [], "model": MODEL, "permissionMode": "dontAsk",
                 "apiKeySource": "none", "claude_code_version": "2.1.272", "output_style": "default",
                 "capabilities": ["interrupt_receipt_v1", "interrupt_cancel_queued_v1", "msg_lifecycle_v1"],
                 "uuid": "3fae5c4a-9042-472d-a579-0dca7097383a"}
        event.update(changes)
        return {k: v for k, v in event.items() if v is not None}

    def bootstrap(self, used=300, **result_changes):
        async_output = '{"async": true, "asyncTimeout": 180000}\n{"metrics": {"sdk_bootstrap": 1}}\n'
        return [hook("hook_started", hook_event="SessionStart"),
                hook(hook_event="SessionStart",
                     output='{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n'
                            '    "additionalContext": "output style"\n  }\n}\n'),
                self.init(), rate_limit(), hook("hook_progress", hook_event="SessionStart", output=async_output),
                system("thinking_tokens", estimated_tokens=50),
                assistant("msg_boot", used, thinking()), assistant("msg_boot", used, text("READY")),
                result("READY", **result_changes),
                system("commands_changed", commands=[]),
                hook(hook_event="SessionStart", output=async_output)]

    def work(self, *events, final=None):
        return [self.init(), *events, final if final is not None else result(REPLY, num_turns=2)]

    def ordinary_work(self):
        return self.work(assistant("msg_w1", 400, thinking()), assistant("msg_w1", 400, tool_use("toolu_1")),
                         tool_result("toolu_1"), assistant("msg_w2", 500, text(REPLY)))

    def run_stream(self, scripts, drain=(), **kwargs):
        options = {key: kwargs.pop(key) for key in ("eof", "stall") if key in kwargs}
        self.server = FakeClaude(scripts, drain, **options)
        if hasattr(self, "wait_effect"):
            self.server.proc.wait.side_effect = self.wait_effect
        self.calls += 1
        self.request_id = f"request-{self.calls}"
        self.alias = f"fresh-alias-{self.calls}"
        with patch.object(adapter, "ClaudeStream", return_value=self.server) as factory:
            outcome = self.bridge.run("claude", "bounded work", "worker", self.alias, self.request_id,
                                      writable=self.writable, model="chosen-model", effort="high", **kwargs)
        self.factory = factory
        return outcome

    def saved(self):
        return ask.read(self.bridge.core.request_path(self.request_id) / "result.json")

    def assert_stopped(self):
        self.assertTrue(self.server.proc.stdin.closed)
        self.server.proc.wait.assert_called()
        self.server.reader.join.assert_called()

    def assert_not_completed(self, outcome):
        self.assertNotEqual(outcome["status"], "completed")
        self.assertFalse(outcome["provider_completed"])
        self.assert_stopped()

    def index(self, event):
        return next(i for i, (kind, value) in enumerate(self.server.timeline) if kind == "event" and value is event)

    def send_index(self, value):
        return next(i for i, (kind, sent) in enumerate(self.server.timeline) if kind == "send" and sent == value)

    # 1 ------------------------------------------------------------------------

    def test_happy_path_bootstraps_validates_observes_and_completes(self):
        drain = [system("commands_changed", commands=[]),
                 hook("hook_progress", output='{"async": true}\n'), hook(output="")]
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()], drain)
        self.assertEqual(outcome["status"], "completed")
        self.assertTrue(outcome["provider_completed"])
        self.assertEqual(self.server.sent, [adapter.BOOTSTRAP, "bounded work"])
        self.assertEqual((outcome["bootstrap_tokens"], outcome["context_window"]), (300, 1000))
        self.assertEqual([r["last"]["used"] for r in outcome["context_readings"]], [400, 500])
        self.assertEqual(outcome["context_readings"][0]["last"], {"message_id": "msg_w1", "used": 400})
        self.assertIsNone(outcome["context_trigger"])
        self.assertIsNone(outcome["steer_race"])
        self.assertNotIn("checkpoint_requested", outcome)
        self.assertEqual((outcome["reply"], outcome["checkpoint_candidates"]), (REPLY, [REPLY]))
        self.assertEqual((outcome["session_id"], outcome["model"]), (SID, MODEL))
        self.assertEqual((outcome["num_turns"], outcome["estimated_cost_usd"]), (2, 0.0169358))
        self.assertEqual(outcome["route"], "claude-stream-json")
        self.assertEqual((outcome["requested_model"], outcome["requested_effort"]), ("chosen-model", "high"))
        self.assertTrue(outcome["owned_children_gone"])
        self.assertTrue(all(set(item) == {"type", "subtype"} for item in outcome["protocol_events"]))
        self.assertNotIn("READY", json.dumps(outcome["protocol_events"]))
        root, _, command = self.factory.call_args.args
        self.assertEqual(root, self.root)
        self.assertEqual(command[:2], ["claude", "-p"])
        at = command.index("--input-format")
        self.assertEqual(command[at:at + 2], ["--input-format", "stream-json"])
        self.assertEqual(command[command.index("--tools") + 1], "Read,Glob,Grep,Edit,Write")
        self.assertEqual(command[command.index("--allowedTools") + 1], "Read,Glob,Grep,Edit,Write")
        self.assertEqual(command[command.index("--permission-mode") + 1], "dontAsk")
        self.assertNotIn("--resume", command)
        self.assertEqual(self.saved(), outcome)
        folder = self.bridge.core.request_path(self.request_id)
        self.assertEqual(ask.read(folder / "request.json")["prompt"], "bounded work")
        self.assertEqual((folder / "stderr.txt").stat().st_mode & 0o777, 0o600)
        self.assertEqual(ask.read(self.bridge.core.session_path(self.alias))["session_id"], SID)
        self.assert_stopped()
        self.stop.assert_not_called()

    def test_read_only_run_requests_and_requires_only_read_tools(self):
        self.writable = False
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(outcome["authority"], "read only")
        command = self.factory.call_args.args[2]
        self.assertEqual(command[command.index("--tools") + 1], "Read,Glob,Grep")

    # 2-4 ------------------------------------------------------------------------

    def test_crossing_on_thinking_waits_for_the_next_tool_use_and_is_durable(self):
        use = assistant("msg_w1", 700, tool_use("toolu_1"))

        def inspect_before_boundary():
            self.assertEqual(self.server.checkpoints(), [])
            retained = self.bridge.core.status(self.request_id)
            self.assertEqual(retained["status"], "running")
            self.assertEqual(retained["context_trigger"]["last"]["used"], 700)
            return None

        outcome = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 700, thinking()), inspect_before_boundary, use, tool_result("toolu_1"),
            assistant("msg_w2", 800, text(REPLY)))])
        self.assertEqual(outcome["status"], "completed")
        checkpoints = self.server.checkpoints()
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(checkpoints[0], CHECKPOINT_PREFIX + adapter.DEFAULT_CHECKPOINT_INSTRUCTION)
        self.assertEqual(self.send_index(checkpoints[0]), self.index(use) + 1)
        self.assertEqual(outcome["checkpoint_requested"], "Roll requested from observed context usage")
        self.assertEqual(outcome["context_trigger"]["last"], {"message_id": "msg_w1", "used": 700})
        self.assertEqual(outcome["context_trigger"]["threshold"], 650)
        self.assertIsNone(outcome["steer_race"])
        self.assertIn('"saving_place"', self.output.getvalue())

    def test_crossing_while_tool_use_is_outstanding_sends_immediately_and_only_once(self):
        crossing = assistant("msg_w1", 700, text("Checking the files"))
        outcome = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 400, tool_use("toolu_1")), crossing,
            assistant("msg_w1", 800, tool_use("toolu_2")), tool_result("toolu_1"), tool_result("toolu_2"),
            assistant("msg_w2", 900, tool_use("toolu_3")), tool_result("toolu_3"),
            assistant("msg_w3", 950, text(REPLY)))])
        self.assertEqual(outcome["status"], "completed")
        checkpoints = self.server.checkpoints()
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(self.send_index(checkpoints[0]), self.index(crossing) + 1)
        self.assertEqual(outcome["context_trigger"]["last"]["used"], 700)

    def test_checkpoint_uses_the_callers_instruction(self):
        instruction = "Return the decision object with action checkpoint and exact ack."
        self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 700, tool_use("toolu_1")), tool_result("toolu_1"),
            assistant("msg_w2", 800, text(REPLY)))], checkpoint_instruction=instruction)
        self.assertEqual(self.server.checkpoints(), [CHECKPOINT_PREFIX + instruction])

    def test_crossing_on_final_text_records_race_and_sends_nothing(self):
        outcome = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 400, thinking()), assistant("msg_w2", 700, text(REPLY)))])
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(self.server.sent, [adapter.BOOTSTRAP, "bounded work"])
        self.assertEqual(outcome["steer_race"], "turn completed before a tool boundary")
        self.assertNotIn("checkpoint_requested", outcome)
        self.assertEqual(outcome["context_trigger"]["last"]["used"], 700)

    # 5 --------------------------------------------------------------------------

    def test_bootstrap_init_failures_stop_before_work_is_sent(self):
        self.bridge.STARTUP_TIMEOUT = 0.01
        cases = {
            "missing within the startup deadline": ([hook("hook_started"), hook(), rate_limit()],
                                                    {"stall": True, "rest": False}),
            "wrong cwd": ([self.init(cwd=str(self.root / "elsewhere"))], {}),
            "wrong permission mode": ([self.init(permissionMode="default")], {}),
            "an extra tool": ([self.init(tools=self.tools() + ["Bash"])], {}),
            "a missing model": ([self.init(model=None)], {}),
            "an empty model": ([self.init(model="")], {}),
            "content before init": ([assistant("msg_boot", 300, text("READY")), self.init()], {}),
            "an earlier event from another session": ([hook(session_id="other-session"), self.init()], {}),
        }
        for name, (events, options) in cases.items():
            with self.subTest(case=name):
                rest = self.bootstrap()[2:] if options.pop("rest", True) else []
                outcome = self.run_stream([events + rest], **options)
                self.assert_not_completed(outcome)
                self.assertEqual(self.server.sent, [adapter.BOOTSTRAP])
                self.assertIsNone(outcome["context_window"])
        self.assertIn("startup deadline", self.run_stream([[hook()]], stall=True)["error"])

    def test_work_init_failures_stop_before_any_work_event_is_used(self):
        self.bridge.STARTUP_TIMEOUT = 0.01
        use = assistant("msg_w1", 400, tool_use("toolu_1"))
        rest = [use, tool_result("toolu_1"), assistant("msg_w2", 500, text(REPLY)), result(REPLY, num_turns=2)]
        cases = {
            "missing within the startup deadline": ([], {"stall": True}),
            "a different model": ([self.init(model="claude-sonnet-5")] + rest, {}),
            "different tools": ([self.init(tools=["Glob", "Grep", "Read"])] + rest, {}),
            "a different session": ([self.init(session_id="other-session")] + rest, {}),
            "content before the work init": ([use, self.init()] + rest[1:], {}),
        }
        for name, (events, options) in cases.items():
            with self.subTest(case=name):
                outcome = self.run_stream([self.bootstrap(), events], **options)
                self.assert_not_completed(outcome)
                self.assertEqual(self.server.sent, [adapter.BOOTSTRAP, "bounded work"])
                self.assertEqual(outcome["context_readings"], [])

    def test_repeated_init_may_confirm_but_never_change_authority(self):
        same = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 700, tool_use("toolu_1")), self.init(), tool_result("toolu_1"),
            assistant("msg_w2", 800, text(REPLY)))])
        self.assertEqual(same["status"], "completed")
        changed = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 700, tool_use("toolu_1")), self.init(tools=self.tools() + ["Bash"]),
            tool_result("toolu_1"), assistant("msg_w2", 800, text(REPLY)))])
        self.assert_not_completed(changed)

    # 6 --------------------------------------------------------------------------

    def test_bootstrap_failures_stop_with_no_guessed_window(self):
        other_model = result("READY")
        del other_model["modelUsage"][MODEL]
        cases = {
            "a tool use": ([assistant("msg_boot", 300, tool_use("toolu_0"))], result("READY")),
            "two turns": ([], result("READY", num_turns=2)),
            "a missing window": ([], result("READY", window=None)),
            "a zero window": ([], result("READY", window=0)),
            "a boolean window": ([], result("READY", window=True)),
            "the model missing from modelUsage": ([], other_model),
            "a failed turn": ([], result("READY", subtype="error_during_execution", is_error=True)),
        }
        for name, (extra, bootstrap_result) in cases.items():
            with self.subTest(case=name):
                events = [self.init(), assistant("msg_boot", 300, text("READY")), *extra, bootstrap_result]
                outcome = self.run_stream([events, self.ordinary_work()])
                self.assert_not_completed(outcome)
                self.assertEqual(self.server.sent, [adapter.BOOTSTRAP])
                self.assertIsNone(outcome["context_window"])
                if "window" in name or "modelUsage" in name:
                    self.assertIn("no guessed window", outcome["error"])

    # 7-8 ------------------------------------------------------------------------

    def test_duplicate_message_usage_is_observed_once_and_changed_usage_again(self):
        with patch.object(adapter.ContextWatch, "observe_tokens", autospec=True,
                          side_effect=codex.ContextWatch.observe_tokens) as observe:
            outcome = self.run_stream([self.bootstrap(), self.work(
                assistant("msg_w1", 400, thinking()), assistant("msg_w1", 400, tool_use("toolu_1")),
                tool_result("toolu_1"), assistant("msg_w2", 500, thinking()),
                assistant("msg_w2", 520, text(REPLY)))])
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual([call.args[1:] for call in observe.call_args_list],
                         [(400, 1000, {"message_id": "msg_w1", "used": 400}),
                          (500, 1000, {"message_id": "msg_w2", "used": 500}),
                          (520, 1000, {"message_id": "msg_w2", "used": 520})])
        self.assertEqual(outcome["bootstrap_tokens"], 300)

    def test_subagent_assistant_events_are_not_readings(self):
        outcome = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 400, tool_use("toolu_1")),
            assistant("msg_sub", 990, text("subagent"), parent="toolu_1"),
            tool_result("toolu_sub", parent="toolu_1"), tool_result("toolu_1"),
            assistant("msg_w2", 500, text(REPLY)))])
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual([r["last"]["message_id"] for r in outcome["context_readings"]], ["msg_w1", "msg_w2"])
        self.assertIsNone(outcome["context_trigger"])
        self.assertEqual(self.server.checkpoints(), [])

    def test_work_user_events_must_be_results_for_outstanding_main_tool_uses(self):
        def user(content, parent=None):
            return {"type": "user", "message": {"role": "user", "content": content},
                    "parent_tool_use_id": parent, "session_id": SID, "uuid": "user-shape"}

        def block(**changes):
            value = {"tool_use_id": "toolu_1", "type": "tool_result", "content": "probe.py"}
            value.update(changes)
            return {k: v for k, v in value.items() if v is not None}

        refused = {
            "string content": user("Roll requested from observed context usage."),
            "a text block": user([{"type": "text", "text": "hello"}]),
            "a text block beside a result": user([block(), {"type": "text", "text": "hello"}]),
            "an unknown id": user([block(tool_use_id="toolu_unknown")]),
            "an empty list": user([]),
            "missing content": {**user([]), "message": {"role": "user"}},
            "a non-object block": user(["tool_result"]),
            "a block without an id": user([block(tool_use_id=None)]),
            "an empty id": user([block(tool_use_id="")]),
            "an integer id": user([block(tool_use_id=1)]),
            "a block without a type": user([block(type=None)]),
            "a repeated id": user([block(), block()]),
        }
        for name, event in refused.items():
            with self.subTest(case=name):
                outcome = self.run_stream([self.bootstrap(), self.work(
                    assistant("msg_w1", 400, tool_use("toolu_1")), event,
                    assistant("msg_w2", 500, text(REPLY)))])
                self.assert_not_completed(outcome)
                self.assertIn("Main user event", outcome["error"])
        with self.subTest(case="a result for an already finished tool use"):
            outcome = self.run_stream([self.bootstrap(), self.work(
                assistant("msg_w1", 400, tool_use("toolu_1")), tool_result("toolu_1"), tool_result("toolu_1"),
                assistant("msg_w2", 500, text(REPLY)))])
            self.assert_not_completed(outcome)
        with self.subTest(case="subagent user events are ignored"):
            outcome = self.run_stream([self.bootstrap(), self.work(
                assistant("msg_w1", 400, tool_use("toolu_1")),
                user("subagent prompt text", parent="toolu_1"), user([], parent="toolu_1"),
                user([block(tool_use_id="toolu_unknown")], parent="toolu_1"),
                tool_result("toolu_1"),
                assistant("msg_w2", 500, text(REPLY)))])
            self.assertEqual(outcome["status"], "completed")
        with self.subTest(case="one event may finish several outstanding tool uses"):
            outcome = self.run_stream([self.bootstrap(), self.work(
                assistant("msg_w1", 400, tool_use("toolu_1")), assistant("msg_w1", 400, tool_use("toolu_2")),
                user([block(), block(tool_use_id="toolu_2")]), assistant("msg_w2", 500, text(REPLY)))])
            self.assertEqual(outcome["status"], "completed")

    def test_parent_tool_use_id_must_be_explicit_on_content_events(self):
        def without_parent(event):
            del event["parent_tool_use_id"]
            return event

        def with_parent(value):
            def change(event):
                event["parent_tool_use_id"] = value
                return event
            return change

        for label, change in {"missing": without_parent, "an empty string": with_parent(""),
                              "an integer": with_parent(7)}.items():
            cases = {
                "work assistant": [self.bootstrap(), self.work(change(assistant("msg_w1", 400, tool_use("toolu_1"))),
                                                               tool_result("toolu_1"),
                                                               assistant("msg_w2", 500, text(REPLY)))],
                "work user": [self.bootstrap(), self.work(assistant("msg_w1", 400, tool_use("toolu_1")),
                                                          change(tool_result("toolu_1")),
                                                          assistant("msg_w2", 500, text(REPLY)))],
                "bootstrap assistant": [[self.init(), change(assistant("msg_boot", 300, text("READY"))),
                                         result("READY")], self.ordinary_work()],
            }
            for where, scripts in cases.items():
                with self.subTest(parent=label, event=where):
                    outcome = self.run_stream(scripts)
                    self.assert_not_completed(outcome)
                    self.assertIn("parent_tool_use_id", outcome["error"])

    def test_work_turn_without_a_main_reading_is_unproved(self):
        outcome = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_sub", 400, text("subagent"), parent="toolu_x"))])
        self.assert_not_completed(outcome)
        self.assertIn("unproved", outcome["error"])

    # 9 --------------------------------------------------------------------------

    def test_result_failures_prevent_completion(self):
        cases = {
            "a queued turn": (result(REPLY, num_turns=2, queued_turn_count=1), ()),
            "permission denials": (result(REPLY, num_turns=2, permission_denials=[{"tool_name": "Write"}]), ()),
            "a conflicting session": (result(REPLY, num_turns=2, session_id="other-session"), ()),
            "an error result": (result(REPLY, num_turns=2, is_error=True), ()),
            "an empty result": (result("", num_turns=2), ()),
            "a second result": (None, (result(REPLY, num_turns=2),)),
            "an assistant event after result": (None, (assistant("msg_w3", 600, text("more")),)),
            "a user event after result": (None, (tool_result("toolu_9"),)),
        }
        for name, (final, drain) in cases.items():
            with self.subTest(case=name):
                outcome = self.run_stream([self.bootstrap(), self.work(
                    assistant("msg_w1", 400, tool_use("toolu_1")), tool_result("toolu_1"),
                    assistant("msg_w2", 500, text(REPLY)), final=final)], drain)
                self.assert_not_completed(outcome)
                self.assertEqual(outcome["status"], "failed")

    # 10 -------------------------------------------------------------------------

    def test_malformed_stream_and_unknown_or_compaction_events_stop_the_run(self):
        missing_id = assistant("msg_w1", 400, thinking())
        del missing_id["message"]["id"]
        missing_usage = assistant("msg_w1", 400, thinking())
        del missing_usage["message"]["usage"]["cache_read_input_tokens"]
        negative = assistant("msg_w1", 400, thinking())
        negative["message"]["usage"]["input_tokens"] = -1
        textual = assistant("msg_w1", 400, thinking())
        textual["message"]["usage"]["cache_creation_input_tokens"] = "12"
        boolean = assistant("msg_w1", 400, thinking())
        boolean["message"]["usage"]["input_tokens"] = True
        cases = {
            "a malformed JSON line": codex.ProtocolError("Invalid Claude stream: a line is not a JSON object"),
            "a JSON line that is not an object": ["not", "an", "object"],
            "a message without an id": missing_id,
            "usage missing a count": missing_usage,
            "negative usage": negative,
            "textual usage": textual,
            "boolean usage": boolean,
            "an unknown system subtype": system("mystery_event"),
            "compact_boundary": system("compact_boundary", compact_metadata={"trigger": "auto"}),
            "permission_denied": system("permission_denied"),
            "an unknown event type": {"type": "stream_event", "session_id": SID},
        }
        for name, bad in cases.items():
            with self.subTest(case=name):
                outcome = self.run_stream([self.bootstrap(), self.work(bad, *self.ordinary_work()[1:-1])])
                self.assert_not_completed(outcome)
                self.assertEqual(outcome["status"], "failed")
        self.assertIn("compaction", self.run_stream([self.bootstrap(), self.work(
            system("compact_boundary"))])["error"])

    def test_early_eof_is_not_a_result(self):
        outcome = self.run_stream([self.bootstrap(), [self.init(), assistant("msg_w1", 400, thinking()),
                                                      adapter.EOF]])
        self.assert_not_completed(outcome)
        self.assertIn("exited", outcome["error"])

    # 11 -------------------------------------------------------------------------

    def test_hook_validation(self):
        pretty_nested = json.dumps({"hookSpecificOutput": {"hookEventName": "Stop",
                                                           "detail": [{"continue": False}]}}, indent=2)
        cases = {
            "a benign response": (hook(), True),
            "a benign pretty-printed response": (hook(output=json.dumps(
                {"hookSpecificOutput": {"additionalContext": "context"}}, indent=2)), True),
            "benign NDJSON": (hook(output='{"async": true}\n{"metrics": {"pv": 1}}\n'), True),
            "non-JSON output": (hook(output="Sync started in background.\n=== REMEMBER ===\n"), True),
            "a started event": (hook("hook_started"), True),
            "an explicit continue true": (hook(output='{"continue": true}'), True),
            "outcome error": (hook(outcome="error"), False),
            "a non-zero exit code": (hook(exit_code=2), False),
            "a boolean exit code": (hook(exit_code=False), False),
            "compact block": (hook(output='{"decision":"block"}'), False),
            "pretty-printed nested continue false": (hook(output=pretty_nested), False),
            "NDJSON with a blocking second line": (hook(output='{"async": true}\n{"decision": "block"}\n'), False),
            "blocking progress output": (hook("hook_progress", output='{"decision": "block"}'), False),
            "a mismatched session": (hook(session_id="other-session"), False),
            "non-string output": (hook(output={"decision": "block"}), False),
        }
        for name, (event, expected) in cases.items():
            with self.subTest(case=name):
                self.assertIs(adapter.hook_ok(event, SID), expected)
        self.assertTrue(pretty_nested.count("\n") > 1)

    def test_blocking_hook_during_work_stops_the_run(self):
        outcome = self.run_stream([self.bootstrap(), self.work(
            assistant("msg_w1", 400, tool_use("toolu_1")),
            hook(hook_event="PostToolUse", output='{\n  "decision": "block"\n}'),
            tool_result("toolu_1"), assistant("msg_w2", 500, text(REPLY)))])
        self.assert_not_completed(outcome)
        self.assertIn("hook", outcome["error"])

    # 12 -------------------------------------------------------------------------

    def test_drain_allows_only_known_non_content_system_events(self):
        passed = self.run_stream([self.bootstrap(), self.ordinary_work()],
                                 [system("commands_changed", commands=[])])
        self.assertEqual(passed["status"], "completed")
        for name, event in {"an unknown system subtype": system("mystery_event"),
                            "thinking tokens": system("thinking_tokens"),
                            "a rate limit event": rate_limit(),
                            "a blocking Stop hook": hook(output='{"decision": "block"}'),
                            "an erroring Stop hook": hook(outcome="error", exit_code=1),
                            "another session": system("commands_changed", session_id="other-session")}.items():
            with self.subTest(case=name):
                failed = self.run_stream([self.bootstrap(), self.ordinary_work()], [event])
                self.assert_not_completed(failed)
                self.assertEqual(failed["status"], "failed")
                self.assertEqual(failed["checkpoint_candidates"], [REPLY])

    def test_drain_without_eof_in_time_fails(self):
        self.bridge.DRAIN_TIMEOUT = 0.01
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()], eof=False, stall=True)
        self.assert_not_completed(outcome)
        self.assertIn("EOF", outcome["error"])

    # 13 -------------------------------------------------------------------------

    def test_snapshot_then_receipt_save_and_read_back_then_stdin_close(self):
        children = {987654321: "Mon Sep 7 10:00:00 2026"}
        order = []

        def snapshot(pid):
            order.append("snapshot")
            return dict(children)

        def save(path, value):
            if isinstance(value, dict) and value.get("phase") == "checkpoint_saved":
                order.append("receipt saved")
            return ask.save(path, value)

        def read(path):
            value = ask.read(path)
            if isinstance(value, dict) and value.get("phase") == "checkpoint_saved":
                order.append("receipt read back")
            return value

        def inspect():
            order.append("stdin closed")
            saved = self.saved()
            self.assertEqual((saved["status"], saved["phase"]), ("running", "checkpoint_saved"))
            self.assertEqual(saved["checkpoint_candidates"], [REPLY])
            self.assertTrue(saved["provider_completed"])
            self.assertEqual((saved["process_id"], saved["process_start"]), (self.server.proc.pid, LEADER_START))
            self.assertEqual(saved["owned_children"], {"987654321": "Mon Sep 7 10:00:00 2026"})
            self.assertEqual((saved["session_id"], saved["context_window"]), (SID, 1000))
            self.descendants.assert_called_once_with(self.server.proc.pid)

        original = FakeClaude.__init__

        def with_inspection(fake, *args, **kwargs):
            original(fake, *args, **kwargs)
            fake.on_close = inspect

        self.descendants.side_effect = snapshot
        with patch.object(FakeClaude, "__init__", with_inspection), \
                patch.object(self.transport, "save", side_effect=save), \
                patch.object(self.transport, "read", side_effect=read):
            outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(order, ["snapshot", "receipt saved", "receipt read back", "stdin closed"])
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(outcome["owned_children"], children)
        self.assertNotIn("phase", outcome)
        self.children_gone.assert_called_with(children)

    def test_snapshot_failure_writes_no_receipt_and_is_not_completed(self):
        phases = []

        def save(path, value):
            if isinstance(value, dict):
                phases.append(value.get("phase"))
            return ask.save(path, value)

        self.descendants.side_effect = OSError("cannot snapshot descendants")
        with patch.object(self.transport, "save", side_effect=save):
            outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assert_not_completed(outcome)
        self.assertNotIn("checkpoint_saved", phases)
        self.assertNotIn("phase", self.saved())
        self.assertNotIn("checkpoint_candidates", self.saved())
        self.assertIn("no checkpoint receipt", outcome["error"])
        self.assertIn("identity unavailable", outcome["cleanup_error"])
        self.assertEqual(outcome["status"], "interrupted")
        self.descendants.assert_called_once_with(self.server.proc.pid)

    def test_failed_receipt_read_back_is_not_completed(self):
        with patch.object(self.transport, "read", return_value={"checkpoint_candidates": ["different"]}):
            outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assert_not_completed(outcome)
        self.assertIn("read-back", outcome["error"])

    def test_receipt_read_back_must_equal_the_whole_receipt(self):
        def altered(change):
            def read(path):
                value = ask.read(path)
                if isinstance(value, dict) and value.get("phase") == "checkpoint_saved":
                    change(value)
                return value
            return read

        changes = {
            "a different session": lambda value: value.update(session_id="other-session"),
            "a different trigger": lambda value: value.update(context_trigger={"last": {"used": 1}}),
            "a dropped leader start": lambda value: value.pop("process_start"),
            "an added field": lambda value: value.update(extra=True),
            "a different phase": lambda value: value.update(phase="checkpoint_saved "),
            # 300.0 == 300 in Python, so only the serialized comparison can catch this one.
            "an equal-comparing float": lambda value: value.update(bootstrap_tokens=float(value["bootstrap_tokens"])),
        }
        for name, change in changes.items():
            with self.subTest(case=name):
                with patch.object(self.transport, "read", side_effect=altered(change)):
                    outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
                self.assert_not_completed(outcome)
                self.assertIn("read-back", outcome["error"])
                self.assertEqual(outcome["checkpoint_candidates"], [REPLY])

    # 14 -------------------------------------------------------------------------

    def test_leader_ignoring_eof_is_stopped_through_bridge_stop(self):
        self.wait_effect = [codex.subprocess.TimeoutExpired("fake-claude", 5), 0]
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "completed")
        self.stop.assert_called_once_with(self.server.proc)
        self.assertEqual(self.server.proc.wait.call_count, 2)
        self.assert_stopped()

    def test_leader_surviving_bridge_stop_is_not_completed(self):
        self.wait_effect = [codex.subprocess.TimeoutExpired("fake-claude", 5)] * 2
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "interrupted")
        self.assertFalse(outcome["provider_completed"])
        self.stop.assert_called_once_with(self.server.proc)

    def test_surviving_child_is_stopped_then_confirmed(self):
        self.bridge.STARTUP_TIMEOUT = self.bridge.DRAIN_TIMEOUT = 10 ** 9
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.side_effect = [False, True]
        with patch.object(codex.time, "monotonic", side_effect=itertools.count(step=10)):
            outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "completed")
        self.assertTrue(outcome["owned_survivor_shutdown_requested"])
        self.assertEqual(outcome["owned_children"], {987654321: "Mon Sep 7 10:00:00 2026"})
        self.stop_children.assert_called_once_with(self.descendants.return_value)

    def test_uncertain_shutdown_leaves_run_not_completed(self):
        self.bridge.STARTUP_TIMEOUT = self.bridge.DRAIN_TIMEOUT = 10 ** 9
        self.descendants.return_value = {987654321: "Mon Sep 7 10:00:00 2026"}
        self.children_gone.return_value = False
        with patch.object(codex.time, "monotonic", side_effect=itertools.count(step=10)):
            outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "interrupted")
        self.assertFalse(outcome["provider_completed"])
        self.assertIn("still present", outcome["cleanup_error"])
        self.assertFalse(outcome.get("owned_children_gone", False))
        self.stop_children.assert_called_once_with(self.descendants.return_value)
        self.assertEqual(self.saved()["status"], "interrupted")

    def test_descendant_snapshot_failure_blocks_completion(self):
        self.descendants.side_effect = OSError("cannot snapshot descendants")
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "interrupted")
        self.assertFalse(outcome["provider_completed"])
        self.assert_stopped()

    def test_leader_start_is_recorded_durably_right_after_launch(self):
        def inspect_saved_identity():
            saved = self.saved()
            self.assertEqual((saved["process_id"], saved["process_start"]), (self.server.proc.pid, LEADER_START))
            return None
        outcome = self.run_stream([[inspect_saved_identity] + self.bootstrap(), self.ordinary_work()])
        self.assertEqual(outcome["status"], "completed")
        self.leader_start.assert_called_once_with(self.server.proc.pid)
        self.assertEqual(outcome["process_start"], LEADER_START)

    def test_unreadable_leader_start_stops_before_bootstrap(self):
        self.leader_start.side_effect = codex.ProtocolError("Cannot record the owned Claude process start time")
        outcome = self.run_stream([self.bootstrap(), self.ordinary_work()])
        self.assert_not_completed(outcome)
        self.assertEqual(outcome["status"], "failed")
        self.assertIn("start time", outcome["error"])
        self.assertEqual(self.server.sent, [])
        self.assertNotIn("process_start", outcome)
        self.assertEqual(outcome["process_id"], self.server.proc.pid)

    def test_failure_before_drain_still_snapshots_and_stops(self):
        outcome = self.run_stream([[self.init(permissionMode="default")]])
        self.descendants.assert_called_once_with(self.server.proc.pid)
        self.assertEqual(outcome["status"], "failed")
        self.assertTrue(outcome["owned_children_gone"])
        self.assert_stopped()

    # 15 -------------------------------------------------------------------------

    def test_hold_live_control_other_targets_and_missing_choices_are_refused(self):
        self.assertTrue(adapter.ClaudeStreamBridge.context_aware)
        for name in ("release_held", "inspect_held", "held_result", "held_cancelled"):
            self.assertFalse(hasattr(self.bridge, name), name)
        refusals = {
            "hold": (codex.ProtocolError, {"hold": True}),
            "live control": (codex.ProtocolError, {"checkpoint_requested": lambda: False}),
            "another target": (ValueError, {"target": "codex"}),
            "no model": (ValueError, {"model": None}),
            "no effort": (ValueError, {"effort": ""}),
        }
        with patch.object(adapter, "ClaudeStream") as factory:
            for name, (error, changes) in refusals.items():
                with self.subTest(case=name):
                    arguments = {"target": "claude", "model": "chosen-model", "effort": "high", **changes}
                    target = arguments.pop("target")
                    with self.assertRaises(error):
                        self.bridge.run(target, "work", "worker", "refused", "refused", **arguments)
            with self.assertRaisesRegex(codex.ProtocolError, "no retainable source or live control"):
                self.bridge.run("claude", "work", "worker", "refused", "refused",
                                model="chosen-model", effort="high", hold=True)
            factory.assert_not_called()
        self.assertFalse(self.bridge.core.request_path("refused").exists())

    def test_existing_alias_and_unresolved_request_are_refused_before_launch(self):
        ask.save(self.bridge.core.session_path("used-alias"), {"closed": True})
        old = self.bridge.core.request_path("older-request")
        old.mkdir()
        ask.save(old / "request.json", {"session": "blocked-alias"})
        ask.save(old / "result.json", {"status": "interrupted"})
        with patch.object(adapter, "ClaudeStream") as factory:
            with self.assertRaisesRegex(codex.ProtocolError, "fresh alias"):
                self.bridge.run("claude", "work", "worker", "used-alias", "request-a",
                                model="chosen-model", effort="high")
            with self.assertRaises(ask.Busy):
                self.bridge.run("claude", "work", "worker", "blocked-alias", "request-b",
                                model="chosen-model", effort="high")
            factory.assert_not_called()

    def test_session_lock_is_held_while_the_provider_runs(self):
        def inspect_lock():
            with self.assertRaises(ask.Busy):
                with ask.exclusive(self.bridge.core.session_path(self.alias).with_suffix(".lock")):
                    pass
            return None
        outcome = self.run_stream([self.bootstrap(), [inspect_lock] + self.ordinary_work()])
        self.assertEqual(outcome["status"], "completed")
        with ask.exclusive(self.bridge.core.session_path(self.alias).with_suffix(".lock")):
            pass

    # 16 -------------------------------------------------------------------------

    def test_cancel_file_stops_the_owned_process_and_records_cancelled(self):
        def cancel():
            ask.save(self.bridge.core.request_path(self.request_id) / "cancel.json", {})
            return None
        outcome = self.run_stream([self.bootstrap(), [self.init(), cancel] + self.ordinary_work()[1:]])
        self.assertEqual(outcome["status"], "cancelled")
        self.assertFalse(outcome["provider_completed"])
        self.assertIn("cancelled", outcome["error"])
        self.assert_stopped()

    def test_optional_timeout_stops_before_work_is_sent_and_records_cancelled(self):
        with patch.object(codex.time, "monotonic", side_effect=itertools.count(step=2)):
            outcome = self.run_stream([self.bootstrap(), self.ordinary_work()], timeout=1)
        self.assertEqual(outcome["status"], "cancelled")
        self.assertEqual(self.server.sent, [adapter.BOOTSTRAP])
        self.assert_stopped()

    def test_keyboard_interrupt_stops_the_owned_process(self):
        outcome = self.run_stream([[self.init(), KeyboardInterrupt()]])
        self.assertEqual(outcome["status"], "cancelled")
        self.assert_stopped()

    def test_invalid_timeout_is_refused(self):
        with self.assertRaises(ValueError):
            self.bridge.run("claude", "work", "worker", "alias", "request", model="m", effort="high", timeout=0)


class SharedExtractionTests(unittest.TestCase):
    def test_observe_tokens_keeps_detail_as_last_and_shares_the_threshold(self):
        watch = codex.ContextWatch()
        self.assertFalse(watch.observe_tokens(100, 1000, {"message_id": "m1", "used": 100}))
        self.assertTrue(watch.observe_tokens(650, 1000, {"message_id": "m2", "used": 650}))
        self.assertFalse(watch.observe_tokens(900, 1000, {"message_id": "m3", "used": 900}))
        self.assertEqual(watch.trigger, {"last": {"message_id": "m2", "used": 650},
                                         "model_context_window": 1000, "threshold": 650})
        for used, window in ((None, 1000), (True, 1000), (-1, 1000), (5, None), (5, 0), (5, True)):
            with self.subTest(used=used, window=window), self.assertRaises(codex.ProtocolError):
                codex.ContextWatch().observe_tokens(used, window, {})

    def test_both_routes_share_one_default_checkpoint_instruction(self):
        self.assertIs(adapter.DEFAULT_CHECKPOINT_INSTRUCTION, codex.DEFAULT_CHECKPOINT_INSTRUCTION)
        self.assertEqual(codex.DEFAULT_CHECKPOINT_INSTRUCTION,
                         "Finish the current safe local operation; do not start another work package. "
                         "Return the saved-place JSON now, retaining actual progress, decisions, evidence "
                         "and failed attempts. Use continue if work remains, review only if genuinely ready. "
                         "Do not launch any other job.")
        self.assertIn("checkpoint_instruction or DEFAULT_CHECKPOINT_INSTRUCTION",
                      inspect.getsource(codex.AppServerBridge._run))

    def test_leader_start_reads_the_stripped_ps_start_time_or_stops(self):
        with patch.object(adapter.subprocess, "run") as run:
            run.return_value = types.SimpleNamespace(returncode=0, stdout=f"  {LEADER_START}  \n")
            self.assertEqual(adapter.leader_start(4242), LEADER_START)
            run.assert_called_once_with(["ps", "-p", "4242", "-o", "lstart="], text=True, capture_output=True)
            for returncode, stdout in ((1, ""), (0, "  \n"), (2, LEADER_START)):
                with self.subTest(returncode=returncode, stdout=stdout):
                    run.return_value = types.SimpleNamespace(returncode=returncode, stdout=stdout)
                    with self.assertRaisesRegex(codex.ProtocolError, "start time"):
                        adapter.leader_start(4242)

    def test_bridge_validates_threshold_options_like_the_codex_route(self):
        transport = types.SimpleNamespace(Bridge=Mock())
        for fraction, tokens in ((0.9, None), (0, None), (0.65, 0), (0.65, 2.5)):
            with self.subTest(fraction=fraction, tokens=tokens), self.assertRaises(ValueError):
                adapter.ClaudeStreamBridge(".", transport, fraction, tokens)
        transport.Bridge.assert_not_called()


class ClaudeStreamProtocolTests(unittest.TestCase):
    def test_process_is_an_owned_group_with_piped_stream_json(self):
        with patch.object(adapter.subprocess, "Popen") as popen:
            with patch.object(adapter.threading, "Thread"):
                stream = adapter.ClaudeStream(Path("/isolated-fixture"), io.StringIO(), ["claude", "-p"])
        self.assertEqual(popen.call_args.args[0], ["claude", "-p"])
        kwargs = popen.call_args.kwargs
        self.assertEqual(kwargs["cwd"], Path("/isolated-fixture"))
        self.assertEqual((kwargs["stdin"], kwargs["stdout"]), (adapter.subprocess.PIPE, adapter.subprocess.PIPE))
        self.assertTrue(kwargs["text"])
        self.assertTrue(kwargs["start_new_session"])
        stream.proc = types.SimpleNamespace(stdin=io.StringIO())
        stream.send("hello")
        self.assertEqual(json.loads(stream.proc.stdin.getvalue()),
                         {"type": "user", "message": {"role": "user", "content": "hello"}})

    def test_non_object_lines_report_error_then_eof(self):
        for line in ("not-json\n", '["array"]\n', "\n"):
            with self.subTest(line=line):
                stream = adapter.ClaudeStream.__new__(adapter.ClaudeStream)
                stream.messages = adapter.queue.Queue()
                stream.proc = types.SimpleNamespace(stdout=io.StringIO('{"type": "system"}\n' + line))
                stream._read()
                self.assertEqual(stream.receive(), {"type": "system"})
                with self.assertRaisesRegex(codex.ProtocolError, "not a JSON object"):
                    stream.receive()
                self.assertIs(stream.receive(), adapter.EOF)
                self.assertIsNone(stream.receive(timeout=0.001))


if __name__ == "__main__":
    unittest.main()
