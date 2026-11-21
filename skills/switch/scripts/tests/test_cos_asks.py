"""cos.py ask: the `### Asks` table of open decisions, and the per-project relay rule.

Design: eolas vault kerd/work/cos-mode/work.md (agreed 2026-11-21 13:36). Every case uses a temp
folder and a temp config path; the real ~/.config/kerd file is never read.
"""

from __future__ import annotations

from datetime import timedelta
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_cos as base  # noqa: E402  (the shared fixture: temp folders, config, TODO text)

cos = base.cos
CLOCK, STAMP, TODO = base.CLOCK, base.STAMP, base.TODO
LATER = CLOCK + timedelta(minutes=20)
LATER_STAMP = "2026-11-20T11:00:00-05:00"

ASK = {"id": "merge-go", "question": "Merge concert/cos-ask-once into main and push?",
       "default": "Hold until the Codex review is back", "why": "The review is due at 15:00",
       "blocks": ["cos-support"], "link": "notes:cos-mode/work.md"}
NAME = {"id": "pick-name", "question": "Which name | for the helper?", "default": "Keep cos.py",
        "why": "Nothing reads it by name yet"}
RELEASE = {"id": "ship-it", "question": "Release 0.203.0?", "default": "Hold", "why": "It is a go",
           "operation": True}

ASK_HEADER = "| Ask id | Question | Default | Why | Blocks | Asked | Answer where |"
ASK_SEPARATOR = "|---|---|---|---|---|---|---|"
ASK_LINE = ("| merge-go | [Merge concert/cos-ask-once into main and push?](notes:cos-mode/work.md) | "
            "Hold until the Codex review is back | The review is due at 15:00 | cos-support | "
            f"{STAMP} | this window |")


def asks_block(*rows):
    return "\n".join(["### Asks", "", ASK_HEADER, ASK_SEPARATOR, *rows]) + "\n"


class AskBase(base.Base):
    def setUp(self):
        super().setUp()
        self.configure()
        self.path = self.todo()

    def ask(self, row, now=CLOCK, **kwargs):
        return cos.ask_decision(str(kwargs.pop("project", self.project)), kwargs.pop("scopes", None),
                                json.dumps(row), config_path=str(self.config), now=now, **kwargs)

    def answered(self, ask_id, **kwargs):
        return cos.ask_decision(str(self.project), kwargs.pop("scopes", None), None, answered=ask_id,
                                config_path=str(self.config), now=CLOCK, **kwargs)

    def queue(self, rows=None):
        code, out = self.write(base.ROWS if rows is None else rows)
        self.assertEqual(code, 0, out)


# ------------------------------------------------------------------ the table

class AskTableTests(AskBase):
    def test_first_ask_without_a_queue_opens_now(self):
        code, out = self.ask(ASK)
        self.assertEqual(code, 0, out)
        head, tail = TODO.split("## Now\n", 1)
        self.assertEqual(self.path.read_text(), head + "## Now\n\n" + asks_block(ASK_LINE) + tail)
        self.assertEqual(out["relay"], "none")
        self.assertEqual(out["asks"][0]["asked"], STAMP)
        self.assertEqual(out["asks"][0]["answer_where"], "this window")
        self.assertNotIn("operation", out["asks"][0])

    def test_ask_sits_directly_under_the_queue(self):
        self.queue()
        before = self.path.read_text()
        self.assertEqual(self.ask(ASK)[0], 0)
        cut = before.index("\n", before.index("Updated: ")) + 1
        self.assertEqual(self.path.read_text(), before[:cut] + "\n" + asks_block(ASK_LINE) + before[cut:])
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertEqual([a["id"] for a in out["asks"]], ["merge-go"])

    def test_queue_write_keeps_the_asks_under_it(self):
        self.queue()
        self.ask(ASK)
        later = CLOCK + timedelta(hours=1)
        code, _ = cos.write_queue(str(self.project), None, json.dumps(base.ROWS[:1]), str(self.config),
                                  now=later)
        self.assertEqual(code, 0)
        text = self.path.read_text()
        self.assertIn("Updated: 2026-11-20T11:40:00-05:00\n\n" + asks_block(ASK_LINE), text)
        self.assertEqual(self.check()[0], 0)

    def test_first_queue_write_goes_above_an_existing_asks_block(self):
        self.ask(ASK)
        self.queue([])
        text = self.path.read_text()
        self.assertIn(f"Updated: {STAMP}\n\n" + asks_block(ASK_LINE) + "\n- **A hand-written", text)
        self.assertEqual(self.check()[0], 0)

    def test_a_lower_queue_carries_its_asks_to_the_top(self):
        old = ("### Queue\n\n" + base.HEADER + "\n" + base.SEPARATOR + "\n\nUpdated: x\n\n"
               + asks_block(ASK_LINE))
        self.todo("## Now\n\n- row one\n\n" + old + "\n- row two\n")
        self.assertEqual(self.write([])[0], 0)
        expected_queue = ("### Queue\n\n" + base.HEADER + "\n" + base.SEPARATOR + "\n\n"
                          f"Updated: {STAMP}\n")
        self.assertEqual(self.path.read_text(), "## Now\n\n" + expected_queue + "\n" + asks_block(ASK_LINE)
                         + "\n- row one\n\n\n\n- row two\n")
        self.assertEqual(self.check()[0], 0)

    def test_answered_round_trips_to_the_original_bytes(self):
        for name, prepare in (("no queue", lambda: None), ("under a queue", self.queue)):
            with self.subTest(case=name):
                self.path = self.todo()
                prepare()
                before = self.path.read_bytes()
                self.assertEqual(self.ask(ASK)[0], 0)
                self.assertEqual(self.ask(NAME)[0], 0)
                self.assertEqual(self.answered("merge-go")[0], 0)
                self.assertNotIn("merge-go", self.path.read_text())
                self.assertIn("pick-name", self.path.read_text())
                code, out = self.answered("pick-name")
                self.assertEqual(code, 0, out)
                self.assertEqual(out["asks"], [])
                self.assertEqual(self.path.read_bytes(), before)
                self.assertNotIn("### Asks", self.path.read_text())

    def test_order_is_the_order_asked(self):
        for row in (ASK, NAME, RELEASE):
            self.assertEqual(self.ask(row)[0], 0)
        self.assertEqual([a["id"] for a in cos._open_asks(self.path.read_text())[0]],
                         ["merge-go", "pick-name", "ship-it"])

    def test_pipes_are_escaped_and_read_back(self):
        self.queue([])
        self.assertEqual(self.ask(NAME)[0], 0)
        self.assertIn("| pick-name | Which name \\| for the helper? | Keep cos.py |", self.path.read_text())
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertEqual(out["asks"][0]["question"], "Which name | for the helper?")

    def test_crlf_file_keeps_its_line_endings(self):
        self.path.write_bytes(b"## Now\r\n\r\n- row\r\n")
        self.assertEqual(self.ask(ASK)[0], 0)
        data = self.path.read_bytes()
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        self.assertTrue(data.endswith(b"this window |\r\n\r\n- row\r\n"))

    def test_scoped_ask_goes_to_the_scope_folder(self):
        scope = self.project / "records"
        scope.mkdir()
        scoped = self.todo(folder=scope)
        self.assertEqual(self.ask(ASK, scopes=["records"])[0], 0)
        self.assertIn("### Asks", scoped.read_text())
        self.assertEqual(self.path.read_text(), TODO)

    def test_too_many_open_asks(self):
        for n in range(cos.MAX_ASKS):
            self.assertEqual(self.ask(dict(NAME, id=f"ask-{n}"))[0], 0)
        before = self.path.read_text()
        code, out = self.ask(dict(NAME, id="one-more"))
        self.assertEqual(code, 2)
        self.assertIn("more than", out["errors"][0])
        self.assertEqual(self.path.read_text(), before)


# ------------------------------------------------------------------ ask once

class AskOnceTests(AskBase):
    def test_an_open_id_is_not_asked_again(self):
        self.assertEqual(self.ask(ASK)[0], 0)
        before = self.path.read_text()
        code, out = self.ask(dict(ASK, question="Merge it now?"), now=LATER)
        self.assertEqual(code, 2)
        self.assertIn(f"ask merge-go is already open, asked {STAMP}: it is not asked again", out["errors"][0])
        self.assertIn("--again", out["errors"][0])
        self.assertEqual(self.path.read_text(), before)

    def test_again_replaces_in_place_with_a_fresh_time(self):
        for row in (ASK, NAME):
            self.ask(row)
        code, out = self.ask(dict(ASK, default="Merge now: the review is back"), now=LATER, again=True)
        self.assertEqual(code, 0, out)
        asks = cos._open_asks(self.path.read_text())[0]
        self.assertEqual([a["id"] for a in asks], ["merge-go", "pick-name"])
        self.assertEqual(asks[0]["asked"], LATER_STAMP)
        self.assertEqual(asks[0]["default"], "Merge now: the review is back")
        self.assertEqual(asks[1]["asked"], STAMP)

    def test_again_and_answered_need_an_open_id(self):
        code, out = self.ask(ASK, again=True)
        self.assertEqual(code, 2)
        self.assertIn("no open ask merge-go to ask again", out["errors"][0])
        code, out = self.answered("merge-go")
        self.assertEqual(code, 2)
        self.assertIn("no open ask merge-go", out["errors"][0])
        self.assertEqual(self.path.read_text(), TODO)
        for bad in ("Merge-Go", "x\n", ""):
            with self.subTest(answered=bad):
                self.assertEqual(self.answered(bad)[0], 2)
        code, out = cos.ask_decision(str(self.project), None, None, answered="merge-go", again=True,
                                     config_path=str(self.config))
        self.assertEqual(code, 2)

    def test_field_grammar(self):
        refused = {
            "default missing": ({}, "default"),
            "why missing": ({}, "why"),
            "question missing": ({}, "question"),
            "default empty": ({"default": "  "}, None),
            "default a dash": ({"default": "—"}, None),
            "default too long": ({"default": "x" * 121}, None),
            "question bracket": ({"question": "see [this]"}, None),
            "question newline": ({"question": "two\nlines"}, None),
            "backslash in why": ({"why": "a\\b"}, None),
            "backslash in default": ({"default": "a\\|b"}, None),
            "asked given": ({"asked": STAMP}, None),
            "answer where given": ({"answer_where": "relay ok"}, None),
            "unknown key": ({"rank": 1}, None),
            "id upper": ({"id": "Merge"}, None),
            "id newline": ({"id": "x\n"}, None),
            "blocks a string": ({"blocks": "cos-support"}, None),
            "blocks bad id": ({"blocks": ["Cos"]}, None),
            "blocks twice": ({"blocks": ["a", "a"]}, None),
            "operation a string": ({"operation": "yes"}, None),
            "link absolute": ({"link": "/etc/passwd"}, None),
            "link http": ({"link": "http://x.org"}, None),
        }
        for name, (change, drop) in refused.items():
            with self.subTest(name=name):
                row = dict(ASK, **change)
                if drop:
                    del row[drop]
                code, out = self.ask(row)
                self.assertEqual(code, 2, (name, out))
                self.assertTrue(out["errors"])
                self.assertEqual(self.path.read_text(), TODO)
        row = dict(ASK)
        del row["default"]
        self.assertIn("every ask carries the default", self.ask(row)[1]["errors"][0])
        self.assertIn("stamped from the clock", self.ask(dict(ASK, asked=STAMP))[1]["errors"][0])
        self.assertEqual(self.ask([ASK])[0], 2, "one object, not a list")
        code, out = cos.ask_decision(str(self.project), None, "{", config_path=str(self.config))
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", out["errors"][0])

    def test_a_damaged_table_is_refused_not_rewritten(self):
        self.ask(ASK)
        damaged = self.path.read_text().replace(f"| {STAMP} |", "| yesterday |")
        self.path.write_text(damaged)
        code, out = self.ask(NAME)
        self.assertEqual(code, 2)
        self.assertIn("the ### Asks table is damaged", out["errors"][0])
        self.assertEqual(self.path.read_text(), damaged)

    def test_two_asks_blocks_refused(self):
        self.todo("## Now\n\n" + asks_block(ASK_LINE) + "\n" + asks_block(ASK_LINE))
        before = self.path.read_text()
        self.assertEqual(self.ask(NAME)[0], 2)
        self.assertEqual(self.write([])[0], 2)
        self.assertEqual(self.path.read_text(), before)


# ------------------------------------------------------------------ the relay rule

class RelayTests(AskBase):
    def relay(self, value, folder=None):
        self.vault(folder or self.project, {"vault": "x", "chief_of_staff_relay": value})

    def test_unset_is_none(self):
        sig = self.sig()
        self.assertEqual((sig["relay"], sig["relay_warning"]), ("none", None))
        self.vault(self.project, {"vault": "x"})
        self.assertEqual(self.sig()["relay"], "none")

    def test_decisions_and_none(self):
        self.relay("decisions")
        self.assertEqual(self.sig()["relay"], "decisions")
        self.relay("none")
        self.assertEqual(self.sig()["relay"], "none")

    def test_invalid_value_is_none_with_a_warning(self):
        for value in ("all", "Decisions", 1, True, None, ["decisions"], {"a": 1}):
            with self.subTest(value=value):
                self.relay(value)
                sig = self.sig()
                self.assertTrue(sig["on"])
                self.assertEqual(sig["relay"], "none")
                self.assertIn('chief_of_staff_relay is not "none" or "decisions"; read as "none"',
                              sig["relay_warning"])

    def test_none_in_either_file_wins_for_a_scope(self):
        (self.project / "area").mkdir()
        cases = [("decisions", "decisions", "decisions"), ("none", "decisions", "none"),
                 ("decisions", "none", "none"), (None, "decisions", "decisions"),
                 ("decisions", None, "decisions"), ("bad", "decisions", "none")]
        for root, scope, expected in cases:
            with self.subTest(root=root, scope=scope):
                shutil.rmtree(self.project / "kivna", ignore_errors=True)
                shutil.rmtree(self.project / "area" / "kivna", ignore_errors=True)
                if root is not None:
                    self.relay(root)
                if scope is not None:
                    self.relay(scope, self.project / "area")
                self.assertEqual(self.sig(scopes=["area"])["relay"], expected)

    def test_off_reports_no_relay(self):
        self.relay("decisions")
        self.configure(projects=[str(self.cos_repo)])
        sig = self.sig()
        self.assertFalse(sig["on"])
        self.assertNotIn("relay", sig)
        self.assertEqual(set(sig), {"on", "is_cos_repo", "why", "config_error"})

    def test_cli_status_reports_it(self):
        self.relay("decisions")
        code, out, _ = base.run_cli("status", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual((code, out["relay"], out["relay_warning"]), (0, "decisions", None))

    def test_answer_where_follows_the_relay_and_never_covers_an_operation(self):
        self.relay("decisions")
        self.assertEqual(self.ask(NAME)[1]["asks"][-1]["answer_where"], "relay ok")
        self.assertEqual(self.ask(RELEASE)[1]["asks"][-1]["answer_where"], "this window")
        self.assertEqual(self.ask(dict(ASK, operation=False))[1]["asks"][-1]["answer_where"], "relay ok")

    def test_a_relay_taken_back_reaches_every_open_row(self):
        self.queue([])
        self.relay("decisions")
        self.ask(NAME)
        self.relay("none")
        code, out = self.check()
        self.assertEqual(code, 2)
        self.assertIn("answer where says 'relay ok', but this project's chief_of_staff_relay is \"none\"",
                      out["errors"][0])
        code, out = self.ask(ASK)
        self.assertEqual(code, 0, out)
        self.assertEqual([a["answer_where"] for a in out["asks"]], ["this window", "this window"])
        self.assertEqual(self.check()[0], 0)

    def test_relay_changed_before_replace_is_refused(self):
        self.relay("decisions")
        code, out = self.ask(NAME, before_commit=lambda: self.relay("none"))
        self.assertEqual(code, 5)
        self.assertIn("chief_of_staff_relay changed underneath", out["error"])
        self.assertEqual(self.path.read_text(), TODO)
        self.assertEqual([p.name for p in self.project.iterdir() if p.name.startswith(".TODO.md.")], [])

    def test_kerds_own_vault_says_none(self):
        """Default 3 of the go (2026-11-21): Kerd's own relay stays "none", written explicitly."""
        own = json.loads((base.SCRIPT.parents[3] / "kivna" / "vault.json").read_text())
        self.assertEqual(own["chief_of_staff_relay"], "none")


# ------------------------------------------------------------------ off, races, check

class AskOffAndRaceTests(AskBase):
    def test_off_writes_nothing(self):
        cases = {
            "no config": lambda: self.config.unlink(),
            "not listed": lambda: self.configure(projects=[str(self.cos_repo)]),
            "invalid config": lambda: self.config.write_text("{"),
            "opted out": lambda: self.vault(self.project, {"chief_of_staff": False}),
            "skipped": lambda: self.configure(skip=[str(self.project)]),
        }
        for name, make_off in cases.items():
            with self.subTest(name=name):
                self.configure()
                shutil.rmtree(self.project / "kivna", ignore_errors=True)
                make_off()
                for call in (lambda: self.ask(ASK), lambda: self.answered("merge-go"),
                             lambda: self.ask(ASK, again=True)):
                    code, out = call()
                    self.assertEqual(code, 3)
                    self.assertFalse(out["on"])
                    self.assertEqual(self.path.read_text(), TODO)

    def test_off_cli_exit_3_with_the_no_config_payload(self):
        self.config.unlink()
        code, out, err = base.run_cli("ask", "--project", str(self.project), "--config", str(self.config),
                                      stdin=json.dumps(ASK))
        self.assertEqual((code, out, err), (3, {"on": False, "why": "no config"}, ""))
        code, out, _ = base.run_cli("ask", "--answered", "merge-go", "--project", str(self.project),
                                    "--config", str(self.config))
        self.assertEqual((code, out), (3, {"on": False, "why": "no config"}))
        self.assertEqual(self.path.read_text(), TODO)

    def test_missing_todo_or_now_is_exit_4(self):
        self.path.unlink()
        self.assertEqual(self.ask(ASK)[0], 4)
        self.assertFalse(self.path.exists())
        self.todo("# TODO\n\n## Backlog\n")
        self.assertEqual(self.ask(ASK)[0], 4)
        self.assertEqual(self.path.read_text(), "# TODO\n\n## Backlog\n")

    def test_race_config_removed_or_todo_changed_before_replace(self):
        code, out = self.ask(ASK, before_commit=self.config.unlink)
        self.assertEqual((code, out), (3, {"on": False, "why": "no config"}))
        self.assertEqual(self.path.read_text(), TODO)
        self.configure()
        changed = TODO + "- added by someone else\n"
        code, out = self.ask(ASK, before_commit=lambda: self.path.write_text(changed))
        self.assertEqual(code, 5)
        self.assertEqual(self.path.read_text(), changed)

    def test_final_check_and_hash_compare_are_the_last_steps_before_replace(self):
        events = []
        real_signal, real_hash, real_replace = cos.signal, cos._current_hash, os.replace

        def record(name, real):
            def wrapped(*args, **kwargs):
                events.append(name)
                return real(*args, **kwargs)
            return wrapped

        with patch.object(cos, "signal", record("signal", real_signal)), \
                patch.object(cos, "_current_hash", record("hash", real_hash)), \
                patch.object(cos.os, "replace", record("replace", real_replace)):
            code, out = self.ask(ASK, before_commit=lambda: events.append("before_commit"))
        self.assertEqual(code, 0, out)
        self.assertEqual(events, ["signal", "before_commit", "signal", "hash", "replace"])

    def test_cli_ask_again_answered_and_check(self):
        self.queue([])
        args = ("--project", str(self.project), "--config", str(self.config))
        code, out, err = base.run_cli("ask", *args, stdin=json.dumps(ASK))
        self.assertEqual(code, 0, err)
        self.assertIsNotNone(cos.datetime.fromisoformat(out["asks"][0]["asked"]).tzinfo)
        self.assertEqual(base.run_cli("ask", *args, stdin=json.dumps(ASK))[0], 2)
        self.assertEqual(base.run_cli("ask", "--again", *args, stdin=json.dumps(ASK))[0], 0)
        code, out, _ = base.run_cli("check", *args)
        self.assertEqual((code, [a["id"] for a in out["asks"]], out["relay"]), (0, ["merge-go"], "none"))
        self.assertEqual(base.run_cli("ask", "--answered", "merge-go", *args)[0], 0)
        code, out, _ = base.run_cli("check", *args)
        self.assertEqual((code, out["asks"]), (0, []))


class CheckAsksTests(AskBase):
    def setUp(self):
        super().setUp()
        self.queue()
        self.ask(ASK)
        self.text = self.path.read_text()

    def refused(self, old, new, expect):
        self.assertIn(old, self.text)
        self.path.write_text(self.text.replace(old, new, 1))
        code, out = self.check()
        self.assertEqual(code, 2, out)
        self.assertTrue(any(expect in e for e in out["errors"]), out["errors"])

    def test_refusals(self):
        cases = [
            ("| Ask id |", "| Id |", "Asks columns must be"),
            (f"| {STAMP} |", "| 2026-11-20 10:40 |", "offset"),
            ("| this window |", "| anywhere |", "answer where"),
            ("| merge-go |", "| Merge_Go |", "must match"),
            (f"| cos-support | {STAMP} |", f"| Cos Support | {STAMP} |", "blocks"),
            ("| Hold until the Codex review is back |", "|  |", "default is empty"),
            ("| The review is due at 15:00 |", "| due \\ soon |", "why has a stray backslash"),
            ("(notes:cos-mode/work.md)", "(/abs)", "link"),
            ("| this window |", "| this window | extra |", "cells"),
        ]
        for old, new, expect in cases:
            with self.subTest(expect=expect):
                self.refused(old, new, expect)

    def test_duplicate_ask_id(self):
        self.path.write_text(self.text.replace(ASK_LINE, ASK_LINE + "\n" + ASK_LINE))
        code, out = self.check()
        self.assertEqual(code, 2)
        self.assertTrue(any("appears twice" in e for e in out["errors"]))

    def test_asks_must_follow_the_queue(self):
        block = asks_block(ASK_LINE)
        moved = self.text.replace("\n" + block, "", 1).replace("with a pipe.\n", "with a pipe.\n\n" + block, 1)
        self.path.write_text(moved)
        code, out = self.check()
        self.assertEqual(code, 2)
        self.assertIn("### Asks does not directly follow the ### Queue block", out["errors"])
        # The next ask puts it back under the queue.
        self.assertEqual(self.ask(NAME)[0], 0)
        self.assertEqual(self.check()[0], 0)

    def test_check_never_writes(self):
        before = (self.path.read_bytes(), os.stat(self.path).st_mtime_ns)
        self.check()
        self.assertEqual((self.path.read_bytes(), os.stat(self.path).st_mtime_ns), before)


# --------------------------------------------------- Cosplay's parser, read-only

class CosplayParserWithAsksTests(AskBase):
    """Cosplay reads the first ranked table in `## Now` and the first `Updated:` line; an Asks
    table has neither a Rank nor a Task column and no Updated line, so its queue reading holds."""

    def setUp(self):
        if not base.COSPLAY_QUEUES.is_file():
            self.skipTest(f"{base.COSPLAY_QUEUES} is absent")
        super().setUp()
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            spec = importlib.util.spec_from_file_location("cosplay_queues_readonly_asks", base.COSPLAY_QUEUES)
            self.queues = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.queues)
        finally:
            sys.dont_write_bytecode = previous

    def parse(self):
        return self.queues.parse(self.path.read_text(), section="now")

    def test_queue_reads_the_same_with_asks_under_it(self):
        self.queue()
        without = self.parse()
        for row in (ASK, NAME):
            self.assertEqual(self.ask(row, now=LATER)[0], 0)
        self.assertEqual(self.parse(), without)

    def test_an_asks_table_alone_is_never_read_as_a_queue(self):
        self.ask(ASK)
        with self.assertRaises(self.queues.QueueUnreadable):
            self.parse()


if __name__ == "__main__":
    unittest.main()
