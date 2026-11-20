"""cos.py: the chief-of-staff signal, the `### Queue` writer and its read-only check.

Every case uses a temp folder and a temp config path; the real ~/.config/kerd file is never read.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "cos.py"
SPEC = importlib.util.spec_from_file_location("switch_cos_tested", SCRIPT)
cos = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cos)

COSPLAY_QUEUES = Path("/Users/anthonymaley/development/product/cosplay/cosplay/queues.py")

CLOCK = datetime(2026, 11, 20, 10, 40, 0, tzinfo=timezone(timedelta(hours=-5)))
STAMP = "2026-11-20T10:40:00-05:00"

TODO = """# TODO

Intro line.

## Now

- **A hand-written Now row** with a link `notes:x/work.md`.
- Another row | with a pipe.

```markdown
## Now
### Queue
```

**Release boundary:** text.

## Backlog

- Later.
"""

ROWS = [
    {"id": "cos-support", "task": "Chief-of-staff support", "link": "notes:chief-of-staff/design.md",
     "outcome": "Optional table and role, trialled in Kerd", "status": "in progress", "qualifier": "review",
     "eta": "~1 sitting", "depends": []},
    {"id": "walk-sam-6", "task": "Walk Sam | round 6", "outcome": "Findings in first-user-6",
     "status": "queued", "eta": "", "depends": ["cos-support"]},
    {"id": "slim-market", "task": "Slim marketplace", "link": "docs/work/slim.md",
     "outcome": "Install from the plugin branch", "status": "blocked", "qualifier": "his decision",
     "eta": "unknown", "depends": ["cos-support", "walk-sam-6"]},
]


def rendered_rows():
    return [
        "| 1 | cos-support | [Chief-of-staff support](notes:chief-of-staff/design.md) | "
        "Optional table and role, trialled in Kerd | in progress (review) | ~1 sitting | — |",
        "| 2 | walk-sam-6 | Walk Sam \\| round 6 | Findings in first-user-6 | queued | unknown | cos-support |",
        "| 3 | slim-market | [Slim marketplace](docs/work/slim.md) | Install from the plugin branch | "
        "blocked (his decision) | unknown | cos-support, walk-sam-6 |",
    ]


HEADER = "| Rank | Task id | Task | Outcome | Status | ETA | Depends on |"
SEPARATOR = "|---|---|---|---|---|---|---|"


def normalized(rows):
    """What write stores and check reads back: trimmed text, empty eta as unknown, depends listed."""
    out = []
    for row in rows:
        row = dict(row)
        row["eta"] = row.get("eta", "").strip() or "unknown"
        row.setdefault("depends", [])
        out.append(row)
    return out


def run_cli(*args, stdin=""):
    result = subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, text=True,
                            capture_output=True, check=False)
    return result.returncode, (json.loads(result.stdout) if result.stdout.strip() else None), result.stderr


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kerd-cos-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(os.path.realpath(self.temp.name))
        self.config = self.base / "config" / "chief-of-staff.json"
        self.config.parent.mkdir()
        self.project = self.base / "work" / "app"
        self.project.mkdir(parents=True)
        self.cos_repo = self.base / "work" / "cosplay"
        self.cos_repo.mkdir()

    def configure(self, projects="all", skip=None, repo=None, **extra):
        body = {"repo": str(repo or self.cos_repo), "projects": projects, "skip": skip or []}
        body.update(extra)
        self.config.write_text(json.dumps(body))

    def sig(self, project=None, scopes=None):
        return cos.signal(str(project or self.project), scopes, str(self.config))

    def vault(self, folder, body):
        (Path(folder) / "kivna").mkdir(parents=True, exist_ok=True)
        (Path(folder) / "kivna" / "vault.json").write_text(body if isinstance(body, str) else json.dumps(body))

    def todo(self, text=TODO, folder=None):
        path = Path(folder or self.project) / "TODO.md"
        path.write_text(text)
        return path

    def write(self, rows, project=None, scopes=None, **kwargs):
        return cos.write_queue(str(project or self.project), scopes, json.dumps(rows), str(self.config),
                               now=CLOCK, **kwargs)

    def check(self, project=None, scopes=None):
        return cos.check_queue(str(project or self.project), scopes, str(self.config))


# ------------------------------------------------------------------- config

class ConfigTests(Base):
    def test_absent_config_is_none(self):
        self.assertIsNone(self.sig())

    def test_absent_config_cli_status_off(self):
        code, out, _ = run_cli("status", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual(code, 3)
        self.assertEqual(out, {"on": False, "why": "no config"})

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root ignores permissions")
    def test_config_that_cannot_be_stated_is_none(self):
        self.configure()
        os.chmod(self.config.parent, 0)
        self.addCleanup(os.chmod, self.config.parent, 0o755)
        self.assertIsNone(self.sig())

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root ignores permissions")
    def test_unreadable_config_is_off_with_error(self):
        self.configure()
        os.chmod(self.config, 0)
        self.addCleanup(os.chmod, self.config, 0o644)
        sig = self.sig()
        self.assertFalse(sig["on"])
        self.assertTrue(sig["config_error"].startswith("unreadable"))

    def test_invalid_json_is_off_with_error(self):
        self.config.write_text("{not json")
        sig = self.sig()
        self.assertEqual(set(sig), {"on", "is_cos_repo", "why", "config_error"})
        self.assertFalse(sig["on"])
        self.assertTrue(sig["config_error"].startswith("invalid JSON"))

    def test_wrong_types_name_the_bad_key(self):
        cases = [
            ([], "the top level"),
            ({"repo": 5, "projects": "all"}, "repo"),
            ({"repo": str(self.cos_repo), "projects": 5}, "projects"),
            ({"repo": str(self.cos_repo), "projects": "some"}, "projects"),
            ({"repo": str(self.cos_repo), "projects": [7]}, "projects[0]"),
            ({"repo": str(self.cos_repo), "projects": "all", "skip": "x"}, "skip"),
            ({"projects": "all"}, "repo is missing"),
            ({"repo": str(self.cos_repo)}, "projects is missing"),
        ]
        for body, key in cases:
            with self.subTest(body=body):
                self.config.write_text(json.dumps(body))
                sig = self.sig()
                self.assertFalse(sig["on"])
                self.assertFalse(sig["is_cos_repo"])
                self.assertTrue(sig["config_error"].startswith("invalid schema"), sig)
                self.assertIn(key, sig["config_error"])

    def test_relative_paths_are_invalid(self):
        for body, key in [({"repo": "cosplay", "projects": "all"}, "repo"),
                          ({"repo": str(self.cos_repo), "projects": ["work/app"]}, "projects[0]"),
                          ({"repo": str(self.cos_repo), "projects": "all", "skip": ["/a", "b"]}, "skip[1]")]:
            with self.subTest(key=key):
                self.config.write_text(json.dumps(body))
                sig = self.sig()
                self.assertFalse(sig["on"])
                self.assertIn(key + " is not an absolute path", sig["config_error"])

    def test_unknown_keys_are_ignored(self):
        self.configure(colour="blue", nested={"a": 1})
        sig = self.sig()
        self.assertTrue(sig["on"])
        self.assertIsNone(sig["config_error"])

    def test_tilde_is_expanded(self):
        with patch.dict(os.environ, {"HOME": str(self.base)}):
            self.configure(projects=["~/work/app", "~/work/cosplay"], repo="~/work/cosplay")
            self.assertTrue(self.sig()["on"])
            self.assertTrue(self.sig(self.cos_repo)["is_cos_repo"])

    def test_fresh_check_flips_when_file_removed(self):
        self.configure()
        code, out, _ = run_cli("status", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual((code, out["on"]), (0, True))
        self.config.unlink()
        code, out, _ = run_cli("status", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual((code, out), (3, {"on": False, "why": "no config"}))

    def test_status_prints_full_signal_when_off(self):
        self.configure(projects=[])
        code, out, _ = run_cli("status", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual(code, 3)
        self.assertEqual(out, {"on": False, "is_cos_repo": False, "why": "not in projects", "config_error": None})


# ---------------------------------------------------------------- matching

class MatchingTests(Base):
    def test_listed_and_all(self):
        self.configure(projects=[str(self.project)])
        self.assertTrue(self.sig()["on"])
        self.configure(projects="all")
        self.assertTrue(self.sig()["on"])
        self.configure(projects=[str(self.cos_repo)])
        self.assertFalse(self.sig()["on"])

    def test_skip_beats_list_and_all(self):
        for projects in ("all", [str(self.project)]):
            with self.subTest(projects=projects):
                self.configure(projects=projects, skip=[str(self.project)])
                sig = self.sig()
                self.assertFalse(sig["on"])
                self.assertTrue(sig["why"].startswith("skipped"))

    def test_skipped_parent_beats_included_child(self):
        child = self.project / "sub"
        child.mkdir()
        self.configure(projects=[str(child)], skip=[str(self.project)])
        self.assertFalse(self.sig(child)["on"])

    def test_prefix_on_components(self):
        sibling = self.base / "work" / "app2"
        sibling.mkdir()
        child = self.project / "deep" / "er"
        child.mkdir(parents=True)
        self.configure(projects=[str(self.project)])
        self.assertTrue(self.sig(child)["on"])
        self.assertFalse(self.sig(sibling)["on"])
        self.configure(projects="all", skip=[str(self.project)])
        self.assertTrue(self.sig(sibling)["on"])

    def test_nested_scope_matched_by_its_own_path(self):
        (self.project / "a" / "b").mkdir(parents=True)
        self.configure(projects=[str(self.project / "a")])
        self.assertFalse(self.sig()["on"])
        self.assertTrue(self.sig(scopes=["a/b"])["on"])
        self.configure(projects=[str(self.project / "a" / "b" / "c")])
        self.assertFalse(self.sig(scopes=["a/b"])["on"])

    def test_vault_opt_out_in_root(self):
        self.configure()
        self.vault(self.project, {"chief_of_staff": False, "vault": "x"})
        sig = self.sig()
        self.assertFalse(sig["on"])
        self.assertTrue(sig["why"].startswith("opted out"))

    def test_vault_true_is_no_override(self):
        (self.project / "scope").mkdir()
        self.configure(projects=[str(self.project / "scope")])
        self.vault(self.project, {"chief_of_staff": False})
        self.vault(self.project / "scope", {"chief_of_staff": True})
        self.assertFalse(self.sig(scopes=["scope"])["on"])

    def test_vault_opt_out_in_scope_not_root(self):
        (self.project / "scope").mkdir()
        self.configure()
        self.vault(self.project / "scope", {"chief_of_staff": False})
        self.assertFalse(self.sig(scopes=["scope"])["on"])
        self.assertTrue(self.sig()["on"], "the scope's opt-out does not reach the root project")

    def test_vault_opt_out_in_root_covers_scope(self):
        (self.project / "scope").mkdir()
        self.configure()
        self.vault(self.project, {"chief_of_staff": False})
        self.assertFalse(self.sig(scopes=["scope"])["on"])

    def test_vault_without_key_is_fine(self):
        self.configure()
        self.vault(self.project, {"vault": "somewhere"})
        self.assertTrue(self.sig()["on"])

    def test_invalid_vault_is_off(self):
        self.configure()
        for body in ("{broken", "[1, 2]", json.dumps({"chief_of_staff": "no"})):
            with self.subTest(body=body):
                self.vault(self.project, body)
                sig = self.sig()
                self.assertFalse(sig["on"])
                self.assertIsNone(sig["config_error"])

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root ignores permissions")
    def test_unreadable_vault_is_off(self):
        self.configure()
        self.vault(self.project, {"vault": "x"})
        path = self.project / "kivna" / "vault.json"
        os.chmod(path, 0)
        self.addCleanup(os.chmod, path, 0o644)
        self.assertFalse(self.sig()["on"])

    def test_multiple_scopes_are_off(self):
        (self.project / "a").mkdir()
        (self.project / "b").mkdir()
        self.configure()
        sig = self.sig(scopes=["a", "b"])
        self.assertFalse(sig["on"])
        self.assertIn("more than one --scope", sig["why"])
        code, out, _ = run_cli("status", "--project", str(self.project), "--scope", "a", "--scope", "b",
                               "--config", str(self.config))
        self.assertEqual((code, out["on"]), (3, False))

    def test_scope_escaping_project_is_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        os.symlink(outside, self.project / "link-out")
        self.configure()
        for scope in ("../outside", str(outside), "link-out", ".", "missing", ""):
            with self.subTest(scope=scope):
                sig = self.sig(scopes=[scope])
                self.assertFalse(sig["on"])
                self.assertTrue(sig["why"].startswith("refused"), sig)

    def test_symlinked_project_path(self):
        link = self.base / "linked-app"
        os.symlink(self.project, link)
        self.configure(projects=[str(self.project)])
        self.assertTrue(self.sig(link)["on"])
        self.configure(projects=[str(link)], repo=str(link))
        sig = self.sig(self.project)
        self.assertTrue(sig["on"])
        self.assertTrue(sig["is_cos_repo"])

    def test_worktree_is_its_own_path(self):
        if shutil.which("git") is None:
            self.skipTest("git not installed")
        repo = self.base / "work" / "main"
        tree = self.base / "work" / "main-wt"

        def git(*args):
            subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
        git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "init")
        git("worktree", "add", "-q", "-b", "wt", str(tree))
        self.configure(projects=[str(repo)])
        self.assertTrue(self.sig(repo)["on"])
        self.assertFalse(self.sig(tree)["on"], "a worktree is not collapsed to its main repo")
        self.configure(projects="all")
        self.assertTrue(self.sig(tree)["on"])
        self.vault(repo, {"chief_of_staff": False})  # uncommitted: this checkout only
        self.assertFalse(self.sig(repo)["on"])
        self.assertTrue(self.sig(tree)["on"])
        self.configure(projects=[str(tree)])
        self.assertTrue(self.sig(tree)["on"])

    def test_is_cos_repo(self):
        self.configure(projects="all")
        self.assertFalse(self.sig()["is_cos_repo"])
        sig = self.sig(self.cos_repo)
        self.assertEqual((sig["on"], sig["is_cos_repo"]), (True, True))
        self.configure(projects=[str(self.cos_repo)])
        sig = self.sig(self.cos_repo)
        self.assertEqual((sig["on"], sig["is_cos_repo"]), (True, True))

    def test_is_cos_repo_false_unless_on(self):
        """Review finding 4: a skipped, opted-out or unlisted chief-of-staff repo shows no role."""
        cases = {
            "skipped": lambda: self.configure(projects="all", skip=[str(self.cos_repo)]),
            "skipped parent": lambda: self.configure(projects="all", skip=[str(self.cos_repo.parent)]),
            "unlisted": lambda: self.configure(projects=[str(self.project)]),
            "empty projects": lambda: self.configure(projects=[]),
            "opted out": lambda: (self.configure(projects="all"),
                                  self.vault(self.cos_repo, {"chief_of_staff": False})),
            "invalid vault": lambda: (self.configure(projects="all"), self.vault(self.cos_repo, "{")),
        }
        for name, make in cases.items():
            with self.subTest(name=name):
                shutil.rmtree(self.cos_repo / "kivna", ignore_errors=True)
                make()
                sig = self.sig(self.cos_repo)
                self.assertFalse(sig["on"], sig)
                self.assertIs(sig["is_cos_repo"], False, sig)
                code, out, _ = run_cli("status", "--project", str(self.cos_repo), "--config", str(self.config))
                self.assertEqual(code, 3)
                self.assertIs(out["is_cos_repo"], False)


# ------------------------------------------------------------------- write

class WriteTests(Base):
    def setUp(self):
        super().setUp()
        self.configure()
        self.path = self.todo()

    def block(self, rows_lines):
        return "\n".join(["### Queue", "", HEADER, SEPARATOR, *rows_lines, "", f"Updated: {STAMP}"]) + "\n"

    def test_valid_table_created_as_first_child(self):
        code, out = self.write(ROWS)
        self.assertEqual(code, 0, out)
        text = self.path.read_text()
        head, tail = TODO.split("## Now\n", 1)
        self.assertEqual(text, head + "## Now\n\n" + self.block(rendered_rows()) + tail)
        self.assertEqual(out["updated"], STAMP)
        self.assertEqual(out["rows"], normalized(ROWS))

    def test_block_created_before_non_blank_line_keeps_a_gap(self):
        self.todo("## Now\n- row\n## Backlog\n")
        self.assertEqual(self.write([])[0], 0)
        self.assertEqual(self.path.read_text(), "## Now\n\n" + self.block([]) + "\n- row\n## Backlog\n")

    def test_now_at_end_of_file_without_newline(self):
        self.todo("# T\n\n## Now")
        self.assertEqual(self.write([])[0], 0)
        self.assertEqual(self.path.read_text(), "# T\n\n## Now\n\n" + self.block([]))
        self.assertEqual(self.check()[0], 0)

    def test_empty_queue_is_header_and_separator(self):
        self.assertEqual(self.write([])[0], 0)
        self.assertIn(self.block([]), self.path.read_text())
        self.assertNotIn("Nothing queued", self.path.read_text())

    def test_replace_keeps_every_other_byte(self):
        self.write(ROWS)
        first = self.path.read_text()
        start = first.index("### Queue")
        end = first.index("\n", first.index("Updated: ")) + 1
        later = CLOCK + timedelta(hours=1)
        code, _ = cos.write_queue(str(self.project), None, json.dumps(ROWS[:1]), str(self.config), now=later)
        self.assertEqual(code, 0)
        second = self.path.read_text()
        self.assertEqual(second[:start], first[:start])
        self.assertTrue(second.endswith(first[end:]))
        self.assertIn("Updated: 2026-11-20T11:40:00-05:00\n", second)
        self.assertNotIn("walk-sam-6", second)
        self.assertEqual(second.count("### Queue"), 2, "the fenced example in Now is untouched")

    def test_damaged_block_never_swallows_following_now_content(self):
        text = "## Now\n\n### Queue\n\n| Rank | Task |\n|---|---|\n- kept row\n\n## Backlog\n"
        self.todo(text)
        self.assertEqual(self.write([])[0], 0)
        self.assertEqual(self.path.read_text(), "## Now\n\n" + self.block([]) + "- kept row\n\n## Backlog\n")

    def test_block_lower_in_now_is_moved_to_first(self):
        self.todo("## Now\n\n- row one\n\n### Queue\n\n" + HEADER + "\n" + SEPARATOR + "\n\nUpdated: x\n\n- row two\n")
        self.assertEqual(self.write([])[0], 0)
        # Exactly the block's lines leave: the blank line before it and the one after it both stay.
        self.assertEqual(self.path.read_text(), "## Now\n\n" + self.block([]) + "\n- row one\n\n\n- row two\n")
        self.assertEqual(self.check()[0], 0)

    def test_relocation_keeps_every_byte_outside_the_block(self):
        """Review finding 5: lifting a lower block out of Now removes exactly its lines."""
        old_block = ("### Queue\n\n" + HEADER + "\n" + SEPARATOR + "\n"
                     "| 1 | old | Old | O | queued | unknown | — |\n\nUpdated: x\n")
        cases = {
            "blank before, blanks and whitespace after": (
                "# T\n\n## Now\n\n- row one\n  \n\n", "\n\n  \n- row two\n\n## Backlog\n- b\n"),
            "no blank after Now heading": (
                "# T\n\n## Now\n- row one\n\n", "\n\n\n- row two\n## Backlog\n"),
            "block last in Now": ("# T\n\n## Now\n\n- row one\n\n", "\n\n## Backlog\n"),
            "block last in file": ("# T\n\n## Now\n\n- row one\n\n", ""),
            "trailing spaces kept": ("## Now\n\n- one  \n \t\n", " \n\t\n- two\n"),
        }
        head_end = "## Now\n"
        for name, (before, after) in cases.items():
            with self.subTest(name=name):
                self.todo(before + old_block + after)
                code, out = self.write([])
                self.assertEqual(code, 0, out)
                cut = before.index(head_end) + len(head_end)
                rest = before[cut:]
                gap = "" if rest.startswith("\n") else "\n"
                expected = before[:cut] + "\n" + self.block([]) + gap + rest + after
                self.assertEqual(self.path.read_text(), expected)
                self.assertEqual(self.check()[0], 0)

    def test_crlf_file_keeps_its_line_endings(self):
        self.path.write_bytes(b"## Now\r\n\r\n- row\r\n")
        self.assertEqual(self.write([])[0], 0)
        data = self.path.read_bytes()
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        self.assertTrue(data.endswith(b"\r\n- row\r\n"))

    def test_file_mode_kept(self):
        os.chmod(self.path, 0o640)
        self.write(ROWS)
        self.assertEqual(os.stat(self.path).st_mode & 0o777, 0o640)

    def test_done_row_refused(self):
        rows = [dict(ROWS[0], status="done")]
        code, out = self.write(rows)
        self.assertEqual(code, 2)
        self.assertTrue(any("done row is refused" in e for e in out["errors"]))
        self.assertEqual(self.path.read_text(), TODO)

    def test_field_grammar(self):
        base = {"id": "a-task", "task": "Task", "outcome": "Out", "status": "queued", "eta": "soon"}
        refused = {
            "newline in task": {"task": "two\nlines"},
            "carriage return in outcome": {"outcome": "x\ry"},
            "line separator": {"eta": "a b"},
            "bracket in task": {"task": "see [this]"},
            "id upper case": {"id": "A-task"},
            "id leading hyphen": {"id": "-a"},
            "id too long": {"id": "a" * 41},
            "id not string": {"id": 3},
            "id trailing newline": {"id": "a-task\n"},
            "id short trailing newline": {"id": "x\n"},
            "id trailing carriage return": {"id": "x\r"},
            "id tab": {"id": "x\t"},
            "backslash in task": {"task": "a\\b"},
            "backslash in linked task": {"task": "a\\b", "link": "docs/a.md"},
            "backslash in outcome": {"outcome": "back\\|slash"},
            "backslash in qualifier": {"status": "blocked", "qualifier": "wait\\here"},
            "backslash in eta": {"eta": "\\"},
            "link with backslash": {"link": "docs\\a.md"},
            "depends with backslash": {"depends": ["a\\b"]},
            "task too long": {"task": "x" * 121},
            "outcome empty": {"outcome": "  "},
            "eta too long": {"eta": "x" * 31},
            "qualifier with paren": {"status": "blocked", "qualifier": "a)b"},
            "qualifier with pipe": {"status": "blocked", "qualifier": "a|b"},
            "qualifier too long": {"status": "blocked", "qualifier": "q" * 61},
            "qualifier empty": {"qualifier": ""},
            "qualifier null": {"qualifier": None},
            "bad status": {"status": "started"},
            "task not string": {"task": 5},
            "depends a string": {"depends": "b"},
            "depends unknown": {"depends": ["nope"]},
            "depends self": {"depends": ["a-task"]},
            "unknown key": {"rank": 1},
            "link with space": {"link": "docs/a b.md"},
            "link with paren": {"link": "https://x.org/a)b"},
            "link with bracket": {"link": "docs/a]b.md"},
            "link absolute path": {"link": "/etc/passwd"},
            "link http": {"link": "http://example.org"},
            "link javascript": {"link": "javascript:alert(1)"},
            "link empty": {"link": ""},
            "link bare notes": {"link": "notes:"},
            "link not string": {"link": 7},
        }
        for name, change in refused.items():
            with self.subTest(name=name):
                code, out = self.write([dict(base, **change)])
                self.assertEqual(code, 2, (name, out))
                self.assertTrue(out["errors"])
                self.assertEqual(self.path.read_text(), TODO)
        missing = dict(base)
        del missing["task"]
        self.assertEqual(self.write([missing])[0], 2)
        self.assertEqual(self.write([base, dict(base)])[0], 2, "duplicate id")
        self.assertEqual(self.write({"rows": []})[0], 2, "not an array")
        code, out = cos.write_queue(str(self.project), None, "[{", str(self.config), now=CLOCK)
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", out["errors"][0])

    def test_pipes_escaped(self):
        rows = [{"id": "esc", "task": "a|b", "outcome": "|edge|", "status": "in progress",
                 "qualifier": "wait here", "eta": "1|2", "link": "https://x.org/p?q=1#f"},
                {"id": "esc-2", "task": "plain | pipe", "outcome": "o", "status": "queued", "eta": "|"}]
        self.assertEqual(self.write(rows)[0], 0)
        lines = [l for l in self.path.read_text().splitlines() if l.startswith(("| 1 |", "| 2 |"))]
        self.assertEqual(lines, [
            "| 1 | esc | [a\\|b](https://x.org/p?q=1#f) | \\|edge\\| | in progress (wait here) | 1\\|2 | — |",
            "| 2 | esc-2 | plain \\| pipe | o | queued | \\| | — |",
        ])
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertEqual(out["rows"], normalized(rows))

    def test_backslash_refused_in_every_rendered_field(self):
        """Review finding 6: Cosplay unescapes only `\\|`, so a backslash is invalid input."""
        base = {"id": "a-task", "task": "Task", "outcome": "Out", "status": "blocked", "qualifier": "q",
                "eta": "soon", "link": "docs/a.md"}
        for key in ("id", "task", "outcome", "qualifier", "eta", "link"):
            with self.subTest(field=key):
                code, out = self.write([dict(base, **{key: base[key] + "\\"})])
                self.assertEqual(code, 2, out)
                self.assertTrue(out["errors"])
                self.assertEqual(self.path.read_text(), TODO)
        code, _, _ = run_cli("write", "--project", str(self.project), "--config", str(self.config),
                             stdin=json.dumps([dict(base, task="a\\b")]))
        self.assertEqual(code, 2)
        self.assertEqual(self.path.read_text(), TODO)

    def test_text_is_trimmed(self):
        rows = [{"id": "t", "task": "  padded  ", "outcome": " o ", "status": "queued", "eta": "   "}]
        code, out = self.write(rows)
        self.assertEqual(code, 0)
        self.assertEqual(out["rows"][0]["task"], "padded")
        self.assertEqual(out["rows"][0]["eta"], "unknown")

    def test_off_writes_nothing(self):
        cases = {
            "no config": lambda: self.config.unlink(),
            "not listed": lambda: self.configure(projects=[str(self.cos_repo)]),
            "invalid config": lambda: self.config.write_text("{"),
            "opted out": lambda: self.vault(self.project, {"chief_of_staff": False}),
        }
        for name, make_off in cases.items():
            with self.subTest(name=name):
                self.configure()
                shutil.rmtree(self.project / "kivna", ignore_errors=True)
                make_off()
                code, out = self.write(ROWS)
                self.assertEqual(code, 3)
                self.assertFalse(out["on"])
                self.assertEqual(self.path.read_text(), TODO)

    def test_off_cli_exit_3(self):
        self.config.unlink()
        code, out, _ = run_cli("write", "--project", str(self.project), "--config", str(self.config),
                               stdin=json.dumps(ROWS))
        self.assertEqual((code, out), (3, {"on": False, "why": "no config"}))
        self.assertEqual(self.path.read_text(), TODO)

    def test_missing_todo_or_now_is_exit_4(self):
        self.path.unlink()
        self.assertEqual(self.write(ROWS)[0], 4)
        self.assertFalse(self.path.exists())
        self.todo("# TODO\n\n## Backlog\n\n```\n## Now\n```\n")
        self.assertEqual(self.write(ROWS)[0], 4)
        self.assertEqual(self.path.read_text(), "# TODO\n\n## Backlog\n\n```\n## Now\n```\n")

    def test_symlinked_todo_not_replaced(self):
        real = self.base / "elsewhere.md"
        real.write_text(TODO)
        self.path.unlink()
        os.symlink(real, self.path)
        self.assertEqual(self.write(ROWS)[0], 4)
        self.assertTrue(self.path.is_symlink())
        self.assertEqual(real.read_text(), TODO)

    def test_two_queue_blocks_refused(self):
        block = self.block([])
        self.todo("## Now\n\n" + block + "\n" + block)
        before = self.path.read_text()
        self.assertEqual(self.write([])[0], 2)
        self.assertEqual(self.path.read_text(), before)
        self.assertEqual(self.check()[0], 2)

    def test_scoped_write_goes_to_scope_folder(self):
        scope = self.project / "records"
        scope.mkdir()
        scoped_todo = self.todo(folder=scope)
        self.assertEqual(self.write(ROWS, scopes=["records"])[0], 0)
        self.assertIn("### Queue", scoped_todo.read_text())
        self.assertEqual(self.path.read_text(), TODO)
        self.assertEqual(self.write(ROWS, scopes=["records", "records"])[0], 3)

    def leftovers(self):
        return [p.name for p in self.project.iterdir() if p.name.startswith(".TODO.md.")]

    def test_race_config_removed_before_replace(self):
        code, out = self.write(ROWS, before_commit=self.config.unlink)
        self.assertEqual(code, 3)
        self.assertEqual(out, {"on": False, "why": "no config"})
        self.assertEqual(self.path.read_text(), TODO)
        self.assertEqual(self.leftovers(), [])

    def test_race_project_skipped_before_replace(self):
        code, _ = self.write(ROWS, before_commit=lambda: self.configure(skip=[str(self.project)]))
        self.assertEqual(code, 3)
        self.assertEqual(self.path.read_text(), TODO)

    def test_race_todo_changed_before_replace(self):
        changed = TODO + "- added by someone else\n"
        code, out = self.write(ROWS, before_commit=lambda: self.path.write_text(changed))
        self.assertEqual(code, 5)
        self.assertIn("changed underneath", out["error"])
        self.assertEqual(self.path.read_text(), changed)
        self.assertEqual(self.leftovers(), [])

    def test_final_check_and_hash_compare_are_the_last_steps_before_replace(self):
        """Review finding 1: config re-check, hash compare, then os.replace, nothing between."""
        events = []
        real_signal, real_hash, real_replace = cos.signal, cos._current_hash, os.replace

        def signal(*args, **kwargs):
            events.append("signal")
            return real_signal(*args, **kwargs)

        def current_hash(*args, **kwargs):
            events.append("hash")
            return real_hash(*args, **kwargs)

        def replace(*args, **kwargs):
            events.append("replace")
            return real_replace(*args, **kwargs)

        with patch.object(cos, "signal", signal), patch.object(cos, "_current_hash", current_hash), \
                patch.object(cos.os, "replace", replace):
            code, out = self.write(ROWS, before_commit=lambda: events.append("before_commit"))
        self.assertEqual(code, 0, out)
        self.assertEqual(events, ["signal", "before_commit", "signal", "hash", "replace"])

    def test_change_during_final_config_check_is_caught(self):
        """A write that lands while the config is re-checked is seen by the hash compare after it."""
        changed = TODO + "- added during the config check\n"
        calls = []
        real_signal = cos.signal

        def signal(*args, **kwargs):
            calls.append(1)
            if len(calls) == 2:
                self.path.write_text(changed)
            return real_signal(*args, **kwargs)

        with patch.object(cos, "signal", signal):
            code, out = self.write(ROWS)
        self.assertEqual(code, 5, out)
        self.assertEqual(self.path.read_text(), changed)
        self.assertEqual(self.leftovers(), [])

    def test_change_after_the_hash_compare_is_lost_as_the_guide_says(self):
        """The narrowed claim: compare-and-swap at the last moment, not a lock. A write by another
        program between the final check and os.replace is lost; this pins that honest limit."""
        real_hash = cos._current_hash

        def current_hash(path):
            value = real_hash(path)
            Path(path).write_text(TODO + "- lost\n")
            return value

        with patch.object(cos, "_current_hash", current_hash):
            code, _ = self.write(ROWS)
        self.assertEqual(code, 0)
        self.assertNotIn("- lost", self.path.read_text())

    def test_race_todo_removed_before_replace(self):
        self.assertEqual(self.write(ROWS, before_commit=self.path.unlink)[0], 5)
        self.assertFalse(self.path.exists())

    def test_cli_write_then_check(self):
        code, out, err = run_cli("write", "--project", str(self.project), "--config", str(self.config),
                                 stdin=json.dumps(ROWS))
        self.assertEqual(code, 0, err)
        self.assertEqual(out["rows"], normalized(ROWS))
        stamp = out["updated"]
        self.assertIsNotNone(datetime.fromisoformat(stamp).tzinfo)
        code, out, err = run_cli("check", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual(code, 0, err)
        self.assertEqual(out["rows"], normalized(ROWS))
        self.assertEqual(out["updated"], stamp)
        code, out, _ = run_cli("write", "--project", str(self.project), "--config", str(self.config),
                               stdin=json.dumps([dict(ROWS[0], status="done")]))
        self.assertEqual(code, 2)


# ------------------------------------------------------------------- check

class CheckTests(Base):
    def setUp(self):
        super().setUp()
        self.configure()
        self.path = self.todo()

    def written(self, rows=ROWS):
        self.assertEqual(self.write(rows)[0], 0)
        return self.path.read_text()

    def test_check_agrees_with_write(self):
        cases = [[], ROWS, ROWS[:1],
                 [{"id": "x", "task": "a|", "outcome": "|", "status": "blocked", "qualifier": "(nested",
                   "eta": "|x|", "depends": []}]]
        for rows in cases:
            with self.subTest(rows=len(rows)):
                self.written(rows)
                code, out = self.check()
                self.assertEqual(code, 0, out)
                self.assertEqual(out["rows"], normalized(rows))
                self.assertEqual(out["updated"], STAMP)

    def test_check_never_writes(self):
        self.written()
        before = (self.path.read_bytes(), os.stat(self.path).st_mtime_ns)
        names = sorted(os.listdir(self.project))
        self.check()
        run_cli("check", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual((self.path.read_bytes(), os.stat(self.path).st_mtime_ns), before)
        self.assertEqual(sorted(os.listdir(self.project)), names)

    def test_check_off_is_exit_3(self):
        self.written()
        self.config.unlink()
        self.assertEqual(self.check(), (3, {"on": False, "why": "no config"}))
        code, _, _ = run_cli("check", "--project", str(self.project), "--config", str(self.config))
        self.assertEqual(code, 3)

    def refused(self, old, new, expect):
        text = self.written()
        self.assertIn(old, text)
        self.path.write_text(text.replace(old, new, 1))
        code, out = self.check()
        self.assertEqual(code, 2, out)
        self.assertTrue(any(expect in e for e in out["errors"]), out["errors"])

    def test_refusals(self):
        cases = [
            ("### Queue\n", "### Queued\n", "no ### Queue"),
            ("| Rank | Task id |", "| Rank | Id |", "columns must be"),
            ("| queued |", "| started |", "is not one of"),
            ("| queued |", "| done |", "done row"),
            ("| 2 | walk-sam-6 |", "| 2 | cos-support |", "appears twice"),
            ("| 2 | walk-sam-6 |", "| 2 | Walk_Sam |", "must match"),
            ("| 2 | walk-sam-6 |", "| 2 | walk-sam-6\x07 |", "must match"),
            (f"\nUpdated: {STAMP}\n", "\n", "missing Updated"),
            (f"Updated: {STAMP}", "Updated: 2026-11-20T10:40:00", "offset"),
            (f"Updated: {STAMP}", "Updated: yesterday", "offset"),
            ("| 2 | walk-sam-6 |", "| 7 | walk-sam-6 |", "rank"),
            ("| cos-support |\n| 3", "| nope |\n| 3", "not a task id"),
            ("Walk Sam \\| round 6", "Walk Sam \\x round 6", "stray backslash"),
            ("Walk Sam \\| round 6", "Walk Sam \\\\ round 6", "stray backslash"),
            ("Findings in first-user-6", "Findings in first\\\\user-6", "stray backslash"),
            ("| unknown | cos-support |", "| un\\known | cos-support |", "ETA"),
            ("(review)", "(rev\\iew)", "qualifier"),
            ("(review)", "(rev)iew)", "qualifier"),
            ("(notes:chief-of-staff/design.md)", "(/abs/path)", "link"),
            ("| unknown | cos-support |", "|  | cos-support |", "ETA"),
        ]
        for old, new, expect in cases:
            with self.subTest(expect=expect, new=new):
                self.refused(old, new, expect)

    def test_missing_heading_or_now_or_todo(self):
        self.assertEqual(self.check()[0], 2, "no block yet")
        self.path.write_text("# TODO\n")
        self.assertEqual(self.check()[0], 2)
        self.path.unlink()
        self.assertEqual(self.check()[0], 2)

    def test_not_first_child_refused(self):
        text = self.written()
        self.path.write_text(text.replace("## Now\n\n", "## Now\n\nA line first.\n\n", 1))
        code, out = self.check()
        self.assertEqual(code, 2)
        self.assertIn("### Queue is not the first block of ## Now", out["errors"])


# --------------------------------------------------- Cosplay's parser, read-only

class CosplayParserTests(Base):
    def setUp(self):
        if not COSPLAY_QUEUES.is_file():
            self.skipTest(f"{COSPLAY_QUEUES} is absent")
        super().setUp()
        self.configure()
        self.path = self.todo()
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True  # read-only: no __pycache__ in Cosplay's checkout
        try:
            spec = importlib.util.spec_from_file_location("cosplay_queues_readonly", COSPLAY_QUEUES)
            self.queues = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.queues)
        finally:
            sys.dont_write_bytecode = previous

    def parse(self):
        return self.queues.parse(self.path.read_text(), section="now")

    def test_empty_queue(self):
        self.assertEqual(self.write([])[0], 0)
        parsed = self.parse()
        self.assertEqual(parsed["rows"], [])
        self.assertEqual(parsed["updated_stamp"], STAMP)
        self.assertEqual(parsed["updated_at"], CLOCK.timestamp())
        self.assertIsNone(parsed["stamp_note"])
        code, out = self.check()
        self.assertEqual((code, out["rows"]), (0, []))

    def test_populated_queue_same_rows(self):
        self.assert_agree(ROWS)

    def test_pipes_in_task_outcome_and_eta_read_the_same(self):
        """Review finding 6: `|` round-trips identically through check and Cosplay's parser."""
        rows = [
            {"id": "pipe-task", "task": "a | b", "outcome": "x|y", "status": "queued", "eta": "1|2"},
            {"id": "pipe-link", "task": "c|d", "link": "notes:x/y.md", "outcome": "|edge|",
             "status": "blocked", "qualifier": "wait", "eta": "|", "depends": ["pipe-task"]},
            {"id": "pipe-end", "task": "ends with|", "outcome": "|starts", "status": "in progress",
             "eta": "a || b"},
        ]
        out = self.assert_agree(rows)
        self.assertEqual([r["task"] for r in out], ["a | b", "c|d", "ends with|"])
        self.assertEqual([r["outcome"] for r in out], ["x|y", "|edge|", "|starts"])
        self.assertEqual([r["eta"] for r in out], ["1|2", "|", "a || b"])

    def test_id_with_control_character_refused_and_readers_agree(self):
        """Review finding 3: an id with a trailing newline never reaches the file."""
        self.assertEqual(self.write([dict(ROWS[0], id="x\n", depends=[])])[0], 2)
        self.assertEqual(self.path.read_text(), TODO)
        self.assert_agree([dict(ROWS[0], id="x", depends=[])])

    def assert_agree(self, rows):
        self.assertEqual(self.write(rows)[0], 0)
        parsed = self.parse()
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertTrue(parsed["ids_stable"])
        self.assertEqual([r["task_id"] for r in parsed["rows"]], [r["id"] for r in out["rows"]])
        self.assertEqual(parsed["updated_stamp"], out["updated"])
        self.assertEqual(parsed["updated_at"], CLOCK.timestamp())
        for n, (theirs, ours) in enumerate(zip(parsed["rows"], out["rows"]), 1):
            with self.subTest(row=n):
                self.assertEqual(theirs["rank"], str(n))
                expected_task = f"[{ours['task']}]({ours['link']})" if "link" in ours else ours["task"]
                self.assertEqual(theirs["task"], expected_task)
                self.assertEqual(theirs["outcome"], ours["outcome"])
                status = ours["status"] + (f" ({ours['qualifier']})" if "qualifier" in ours else "")
                self.assertEqual(theirs["status"], status)
                self.assertEqual(theirs["eta"], ours["eta"])
                self.assertEqual(theirs["depends_on"], ", ".join(ours["depends"]) or "—")
        self.assertEqual(out["rows"], normalized(rows))
        return out["rows"]


if __name__ == "__main__":
    unittest.main()
