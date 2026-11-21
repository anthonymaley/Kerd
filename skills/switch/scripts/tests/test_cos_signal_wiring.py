"""The chief-of-staff signal in Switch In's helpers, and its off path.

Design: eolas vault kerd/work/chief-of-staff/design.md (v2, v2.1 E, v2.2 item 6).
With no config file, or one this process cannot stat, `handoff.py prepare` and
`pickup` print exactly the bytes 0.199.0 printed, and the arrival renderer draws
exactly the 0.199.0 screen. The goldens in fixtures/cos_off_path/ were captured
from the code before the signal was wired in (main at ac5103ae) and must never
be regenerated from the code under test.

Every helper run here gets a fake, empty HOME, so the real
~/.config/kerd/chief-of-staff.json on this machine is never read.
"""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
HANDOFF = SCRIPTS / "handoff.py"
GOLDEN = Path(__file__).resolve().parent / "fixtures" / "cos_off_path"
FIXED_DATE = "2026-11-20T10:00:00+00:00"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


handoff = load("switch_handoff_cos_tested", HANDOFF)
view = load("switch_view_cos_tested", SCRIPTS / "where_we_are.py")


# The helper runs the golden covers: name -> argv after --project P.
RUNS = {
    "pickup": ["pickup", "--branch", "main", "--record", "CONTEXT.md"],
    "prepare": ["prepare", "--branch", "main", "--record", "CONTEXT.md", "--file", "TODO.md",
                "--section", "CONTEXT.md", "## Now"],
    "pickup_scoped": ["pickup", "--branch", "main", "--record", "area/record.md", "--scope", "area"],
    "prepare_scoped": ["prepare", "--branch", "main", "--record", "area/record.md", "--scope", "area",
                       "--file", "area/TODO.md"],
}

FILES = {
    "CONTEXT.md": "# Context\n\n## Now\n\nFixture project for the chief-of-staff off-path golden.\n\n"
                  "## Next\n\nNothing else.\n",
    "TODO.md": "# TODO\n\n## Now\n\n- [ ] Golden fixture task\n\n## Backlog\n\n- Nothing yet\n",
    "area/record.md": "# Area record\n\nA scoped project inside a shared repo.\n",
    "area/TODO.md": "# Area TODO\n\n## Now\n\n- [ ] Scoped fixture task\n",
}

# The arrival summary the renderer goldens are drawn from (not the guide's
# example, which other work may edit).
SUMMARY = {
    "project": "Fixture",
    "phase": "Deliver: 2 of 3 done",
    "where": "The fixture project is half built and its tests pass.",
    "open_work": ["Finish the fixture task", "**Codex:** review the fixture"],
    "recommendation": {"text": "Finish the fixture task", "why": "It unblocks the review."},
    "last_session": "The first two pieces were built.",
    "team": [{"provider": "codex", "id": "abc", "role": "reviewer"}],
    "question": {"text": "Start a Conductor session?"},
    "documents": [],
    "warnings": ["One fixture warning."],
    "insight": "A fixture insight.",
    "base": ".",
    "restored": "yes",
}
NOW = "2026-11-20 10:00 UTC"
RENDERS = {
    "arrival_plain.txt": dict(width=80, color=False, markdown=False),
    "arrival_color.txt": dict(width=80, color=True, markdown=False),
    "arrival_markdown.txt": dict(width=80, color=False, markdown=True),
}


def clean_env(home):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") and key not in ("KERD_COS_CONFIG", "XDG_CONFIG_HOME")}
    env["HOME"] = str(home)
    return env


def build_project(base):
    """A deterministic git project: fixed names and dates give fixed hashes."""
    project = base / "project"
    project.mkdir()
    home = base / "home"
    home.mkdir()
    env = clean_env(home)
    env.update(GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_AUTHOR_DATE=FIXED_DATE, GIT_COMMITTER_DATE=FIXED_DATE)

    def git(*args):
        subprocess.run(["git", "-C", str(project), *args], env=env, check=True, capture_output=True)

    git("init", "-q", "-b", "main")
    for key, value in (("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
        git("config", key, value)
    for relative, text in FILES.items():
        (project / relative).parent.mkdir(parents=True, exist_ok=True)
        (project / relative).write_text(text, encoding="utf-8")
    git("add", "--all")
    git("commit", "-q", "-m", "Fixture project")
    return project, home


def run_helper(script, project, home, argv):
    result = subprocess.run([sys.executable, str(script), "--project", str(project), *argv],
                            env=clean_env(home), capture_output=True)
    return result.returncode, result.stdout, result.stderr


def render(summary, width, color, markdown):
    with patch.object(view, "kerd_version", return_value="0.199.0"):
        return view.render_dashboard(summary, NOW, width, color, markdown=markdown)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kerd-cos-wiring-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.project, self.home = build_project(self.base)

    def golden(self, name):
        return (GOLDEN / f"{name}.json").read_bytes()

    def helper(self, name, home=None):
        code, out, err = run_helper(HANDOFF, self.project, home or self.home, RUNS[name])
        self.assertEqual((code, err), (0, b""), err.decode())
        return out


class OffPathGoldenTests(Fixture):
    """Acceptance check 1 and v2.1 E: no file means 0.199.0's bytes."""

    def test_config_absent_is_byte_identical(self):
        for name in RUNS:
            with self.subTest(run=name):
                self.assertEqual(self.helper(name), self.golden(name))

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root ignores permissions")
    def test_config_that_cannot_be_reached_is_byte_identical(self):
        """Permission denied on the config's folder: off, nothing shown."""
        folder = self.home / ".config" / "kerd"
        folder.mkdir(parents=True)
        (folder / "chief-of-staff.json").write_text(json.dumps(
            {"repo": str(self.project), "projects": "all", "skip": []}))
        folder.chmod(0)
        self.addCleanup(folder.chmod, 0o700)
        for name in RUNS:
            with self.subTest(run=name):
                self.assertEqual(self.helper(name), self.golden(name))

    def config_present(self):
        """A config this process can stat, so handoff goes on to load cos.py."""
        config = self.base / "chief-of-staff.json"
        config.write_text(json.dumps({"repo": str(self.project), "projects": "all", "skip": []}))
        return patch.object(handoff, "COS_CONFIG", str(config))

    def test_no_config_never_loads_cos_py(self):
        """Review finding 2: the config's existence is checked before cos.py is imported or run."""
        marker = self.base / "imported"
        sentinel = self.base / "sentinel_cos.py"
        sentinel.write_text(f"open({str(marker)!r}, 'w').close()\n"
                            "def signal(*a, **k):\n"
                            "    return {'on': True, 'is_cos_repo': False, 'why': 'x', 'config_error': None}\n")
        before = set(sys.modules)
        with patch.object(handoff, "COS_SCRIPT", sentinel), \
                patch.object(handoff, "COS_CONFIG", str(self.base / "absent.json")), \
                patch.object(handoff.importlib.util, "spec_from_file_location") as spec:
            self.assertIsNone(handoff.chief_of_staff_signal(self.project, []))
        spec.assert_not_called()
        self.assertFalse(marker.exists())
        self.assertNotIn("kerd_switch_cos", set(sys.modules) - before)
        # The control: with the config present the same sentinel is loaded.
        with patch.object(handoff, "COS_SCRIPT", sentinel), self.config_present():
            self.assertEqual(handoff.chief_of_staff_signal(self.project, [])["on"], True)
        self.assertTrue(marker.exists())

    def test_no_config_never_loads_cos_py_end_to_end(self):
        """Through the real helper: an empty HOME, and a cos.py the run must never touch."""
        scripts = self.base / "scripts"
        shutil.copytree(SCRIPTS, scripts, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        marker = self.base / "imported"
        (scripts / "cos.py").write_text(f"open({str(marker)!r}, 'w').close()\nraise SystemExit(9)\n")
        for name in RUNS:
            with self.subTest(run=name):
                code, out, err = run_helper(scripts / "handoff.py", self.project, self.home, RUNS[name])
                self.assertEqual((code, err), (0, b""), err.decode())
                self.assertEqual(out, self.golden(name))
                self.assertFalse(marker.exists())

    def test_a_broken_cos_module_never_changes_the_off_path(self):
        broken = self.base / "cos.py"
        for body in ("raise RuntimeError('broken at import')\n",
                     "import sys\nprint('noise')\nsys.exit(3)\n",
                     "def signal(*a, **k):\n    print('noise')\n    raise ValueError('broken')\n",
                     "def signal(*a, **k):\n    return 'not a dict'\n",
                     "def signal(*a, **k):\n    return {'on': True, 'is_cos_repo': False, 'why': object()}\n"):
            broken.write_text(body)
            with self.subTest(body=body.splitlines()[0]), patch.object(handoff, "COS_SCRIPT", broken), \
                    self.config_present():
                self.assertIsNone(handoff.chief_of_staff_signal(self.project, []))

    def test_ask_and_check_without_config_change_nothing(self):
        """0.203.0: `cos.py ask` with no config is the same silent off: exit 3, the no-config
        payload, TODO.md's bytes untouched, and the helpers still print the golden bytes."""
        todo = self.project / "TODO.md"
        before = todo.read_bytes()
        ask = json.dumps({"id": "merge-go", "question": "Merge?", "default": "Hold", "why": "Review due"})
        for argv, stdin in ((["ask"], ask), (["ask", "--again"], ask), (["ask", "--answered", "merge-go"], ""),
                            (["check"], ""), (["write"], "[]")):
            with self.subTest(argv=argv):
                result = subprocess.run([sys.executable, str(SCRIPTS / "cos.py"), *argv, "--project",
                                         str(self.project)], input=stdin.encode(), env=clean_env(self.home),
                                        capture_output=True)
                self.assertEqual((result.returncode, result.stderr), (3, b""))
                self.assertEqual(json.loads(result.stdout), {"on": False, "why": "no config"})
                self.assertEqual(todo.read_bytes(), before)
        for name in RUNS:
            with self.subTest(run=name):
                self.assertEqual(self.helper(name), self.golden(name))

    def test_a_missing_cos_module_is_off(self):
        with patch.object(handoff, "COS_SCRIPT", self.base / "absent.py"), self.config_present():
            self.assertIsNone(handoff.chief_of_staff_signal(self.project, []))


class OnPathKeyTests(Fixture):
    """With a signal, the output gains exactly its key(s) and nothing else moves."""

    def main_output(self, name, signal):
        argv = ["handoff.py", "--project", str(self.project), *RUNS[name]]
        out = io.StringIO()
        with patch.object(handoff, "chief_of_staff_signal", return_value=signal) as called, \
                patch.object(sys, "argv", argv), contextlib.redirect_stdout(out):
            self.assertEqual(handoff.main(), 0)
        return out.getvalue(), called

    def test_on_adds_the_signal_and_queue_md_presence_only(self):
        signal = {"on": True, "is_cos_repo": False, "why": "listed", "config_error": None}
        for name in RUNS:
            with self.subTest(run=name):
                text, _ = self.main_output(name, signal)
                golden = json.loads(self.golden(name))
                expected = dict(golden, chief_of_staff=signal, queue_md_present=False)
                self.assertEqual(text, json.dumps(expected, indent=2) + "\n")

    def test_off_signal_adds_only_its_own_key(self):
        """File present, project not included: a machine-only key, nothing else."""
        signal = {"on": False, "is_cos_repo": False, "why": "not listed", "config_error": None}
        for name in RUNS:
            with self.subTest(run=name):
                text, _ = self.main_output(name, signal)
                expected = dict(json.loads(self.golden(name)), chief_of_staff=signal)
                self.assertEqual(text, json.dumps(expected, indent=2) + "\n")

    def test_none_signal_prints_the_golden_bytes(self):
        for name in RUNS:
            with self.subTest(run=name):
                text, _ = self.main_output(name, None)
                self.assertEqual(text.encode(), self.golden(name))

    def test_queue_md_is_looked_for_in_the_project_or_its_scope(self):
        signal = {"on": True, "is_cos_repo": False, "why": "listed", "config_error": None}
        (self.project / "docs" / "work").mkdir(parents=True)
        (self.project / "docs" / "work" / "queue.md").write_text("hand-kept\n")
        (self.project / ".git" / "info" / "exclude").write_text("docs/\n")
        self.assertTrue(json.loads(self.main_output("pickup", signal)[0])["queue_md_present"])
        # The scoped project is the scope folder, so the root's queue.md is not its own.
        self.assertFalse(json.loads(self.main_output("pickup_scoped", signal)[0])["queue_md_present"])
        (self.project / "area" / "docs" / "work").mkdir(parents=True)
        (self.project / "area" / "docs" / "work" / "queue.md").write_text("hand-kept\n")
        (self.project / ".git" / "info" / "exclude").write_text("docs/\narea/docs/\n")
        self.assertTrue(json.loads(self.main_output("pickup_scoped", signal)[0])["queue_md_present"])

    def test_the_signal_is_asked_for_the_project_and_its_validated_scope(self):
        signal = {"on": False, "is_cos_repo": False, "why": "x", "config_error": None}
        _, called = self.main_output("pickup", signal)
        called.assert_called_once_with(self.project, [])
        _, called = self.main_output("prepare_scoped", signal)
        called.assert_called_once_with(self.project, ["area"])

    def test_measure_save_and_boundary_never_ask(self):
        for argv in (["measure", "--record", "CONTEXT.md"],):
            out = io.StringIO()
            with patch.object(handoff, "chief_of_staff_signal") as called, \
                    patch.object(sys, "argv", ["handoff.py", "--project", str(self.project), *argv]), \
                    contextlib.redirect_stdout(out):
                handoff.main()
            called.assert_not_called()
            self.assertNotIn("chief_of_staff", out.getvalue())

    def test_a_blocked_pickup_never_asks(self):
        argv = ["handoff.py", "--project", str(self.project), "pickup", "--branch", "main",
                "--record", "missing.md"]
        with patch.object(handoff, "chief_of_staff_signal") as called, patch.object(sys, "argv", argv), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(handoff.main(), 2)
        called.assert_not_called()


COS = SCRIPTS / "cos.py"


@unittest.skipUnless(COS.is_file(), "cos.py not present yet")
class RealSignalTests(Fixture):
    """End to end through the real cos.py with a config in the fake HOME."""

    def configure(self, config):
        folder = self.home / ".config" / "kerd"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "chief-of-staff.json").write_text(json.dumps(config))

    def test_listed_project_is_on(self):
        self.configure({"repo": str(self.base / "elsewhere"), "projects": [str(self.project)], "skip": []})
        out = json.loads(self.helper("pickup"))
        self.assertIs(out["chief_of_staff"]["on"], True)
        self.assertIs(out["chief_of_staff"]["is_cos_repo"], False)
        self.assertEqual(out["chief_of_staff"]["relay"], "none")
        self.assertIsNone(out["chief_of_staff"]["relay_warning"])
        self.assertIs(out["queue_md_present"], False)
        golden = json.loads(self.golden("pickup"))
        self.assertEqual({k: v for k, v in out.items() if k not in ("chief_of_staff", "queue_md_present")},
                         golden)

    def test_relay_rule_travels_with_the_signal(self):
        self.configure({"repo": str(self.base / "elsewhere"), "projects": "all"})
        (self.project / "kivna").mkdir()
        (self.project / ".git" / "info" / "exclude").write_text("kivna/\n")
        (self.project / "kivna" / "vault.json").write_text(json.dumps({"chief_of_staff_relay": "decisions"}))
        self.assertEqual(json.loads(self.helper("pickup"))["chief_of_staff"]["relay"], "decisions")
        (self.project / "kivna" / "vault.json").write_text(json.dumps({"chief_of_staff_relay": "yes"}))
        signal = json.loads(self.helper("pickup"))["chief_of_staff"]
        self.assertEqual(signal["relay"], "none")
        self.assertIn("read as", signal["relay_warning"])

    def test_excluded_project_gains_only_the_machine_key(self):
        self.configure({"repo": str(self.base / "elsewhere"), "projects": [str(self.base / "other")],
                        "skip": []})
        for name in RUNS:
            with self.subTest(run=name):
                out = json.loads(self.helper(name))
                self.assertIs(out.pop("chief_of_staff")["on"], False)
                self.assertEqual(out, json.loads(self.golden(name)))

    def test_cos_repo_says_so(self):
        self.configure({"repo": str(self.project), "projects": "all", "skip": []})
        out = json.loads(self.helper("pickup"))
        self.assertIs(out["chief_of_staff"]["is_cos_repo"], True)

    def test_cos_repo_skipped_or_unlisted_reports_no_role(self):
        """Review finding 4: is_cos_repo is true only when the signal is on."""
        for name, config in (
                ("skipped", {"repo": str(self.project), "projects": "all", "skip": [str(self.project)]}),
                ("unlisted", {"repo": str(self.project), "projects": [str(self.base / "other")]})):
            with self.subTest(case=name):
                self.configure(config)
                signal = json.loads(self.helper("pickup"))["chief_of_staff"]
                self.assertEqual((signal["on"], signal["is_cos_repo"]), (False, False))

    def test_invalid_config_carries_its_error_and_is_off(self):
        folder = self.home / ".config" / "kerd"
        folder.mkdir(parents=True)
        (folder / "chief-of-staff.json").write_text("{not json")
        out = json.loads(self.helper("pickup"))
        self.assertIs(out["chief_of_staff"]["on"], False)
        self.assertTrue(out["chief_of_staff"]["config_error"])
        self.assertNotIn("queue_md_present", out)


class ArrivalRoleTests(unittest.TestCase):
    """The ROLE cell (design: the chief of staff's own repo) and the off path."""

    def test_without_role_the_arrival_is_byte_identical(self):
        for absent in ({}, {"role": None}, {"role": ""}, {"role": "   "}, {"role": 3}):
            for name, options in RENDERS.items():
                with self.subTest(role=absent, render=name):
                    out = render(dict(SUMMARY, **absent), **options)
                    self.assertEqual(out, (GOLDEN / name).read_text(encoding="utf-8"))

    def test_role_shows_as_a_grid_cell_in_markdown(self):
        out = render(dict(SUMMARY, role="chief of staff"), 80, False, True)
        self.assertIn("| PROJECT | ROLE | PHASE | NEXT | TEAM |", out)
        self.assertIn("|" + " --- |" * 5, out)
        self.assertIn("| Fixture | chief of staff | Deliver: 2 of 3 done |", out)
        golden = (GOLDEN / "arrival_markdown.txt").read_text(encoding="utf-8")
        self.assertEqual(out.count("chief of staff"), 1)
        # Only the grid moved.
        self.assertEqual(out.split("**Where things stand", 1)[1], golden.split("**Where things stand", 1)[1])

    def test_role_shows_as_a_grid_cell_in_plain_text(self):
        out = render(dict(SUMMARY, role="chief of staff"), 80, False, False)
        lines = out.splitlines()
        project = next(i for i, line in enumerate(lines) if line.startswith(" PROJECT"))
        self.assertEqual(lines[project + 1], " ROLE    chief of staff")
        self.assertTrue(lines[project + 2].startswith(" PHASE"))
        golden = (GOLDEN / "arrival_plain.txt").read_text(encoding="utf-8")
        self.assertEqual(out.replace(" ROLE    chief of staff\n", "", 1), golden)

    def test_role_is_not_shown_on_a_first_arrival(self):
        """A first arrival has no grid; it keeps its one line."""
        first = {"project": "Fixture", "first_arrival": True, "restored": "yes"}
        self.assertEqual(render(dict(first, role="chief of staff"), 80, False, False),
                         render(first, 80, False, False))

    def test_the_guide_example_leaves_role_out(self):
        """Every caller copies the guide's example, so role stays out of it."""
        import re
        guide = SCRIPTS.parent / "references" / "in.md"
        example = json.loads(re.findall(r"```json\n(.*?)```", guide.read_text(), re.S)[0])
        self.assertNotIn("role", example)
        self.assertNotIn("role", view.OPEN_WORK_KEYS)
        self.assertIn("role", view.ARRIVAL_OPTIONAL_KEYS)

    def test_warnings_carry_config_and_both_lists_lines_unchanged(self):
        """No new plumbing: the caller's lines reach ATTENTION as given."""
        lines = ["Chief-of-staff config is not valid JSON; chief of staff is off.",
                 "This project keeps docs/work/queue.md and the Now queue table; choose one."]
        out = render(dict(SUMMARY, warnings=lines), 80, False, True)
        for line in lines:
            self.assertIn(f"- {view.md(line)}", out)


class ArrivalAutomaticTests(unittest.TestCase):
    """Review r2 (0.203.0): `"automatic": true` suppresses every arrival question, the
    first-arrival one included, so an arrival nobody asked for asks nothing new. Absent or
    anything but true, the screen is the golden's, byte for byte."""

    @staticmethod
    def without_question(text):
        lines = text.split("\n")
        cut = next(i for i, line in enumerate(lines) if "💬" in line)
        lines = lines[:cut]
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(lines)

    def test_key_absent_or_not_true_is_byte_identical(self):
        for value in ({}, {"automatic": False}, {"automatic": None}, {"automatic": "true"},
                      {"automatic": 1}):
            for name, options in RENDERS.items():
                with self.subTest(value=value, render=name):
                    out = render(dict(SUMMARY, **value), **options)
                    self.assertEqual(out, (GOLDEN / name).read_text(encoding="utf-8"))

    def test_automatic_normal_arrival_ends_on_its_content(self):
        for name, options in RENDERS.items():
            with self.subTest(render=name):
                out = render(dict(SUMMARY, automatic=True), **options)
                golden = (GOLDEN / name).read_text(encoding="utf-8")
                self.assertNotIn("💬", out)
                self.assertNotIn("Start a Conductor session?", out)
                self.assertEqual(out, self.without_question(golden))
                self.assertTrue(out.splitlines()[-1].strip())

    def test_automatic_first_arrival_asks_nothing_either(self):
        first = {"project": "Fixture", "first_arrival": True, "restored": "yes",
                 "question": {"text": "Start a Conductor session?"}}
        for name, options in RENDERS.items():
            with self.subTest(render=name):
                asked = render(first, **options)
                self.assertIn("What do you want to work on?", asked)
                out = render(dict(first, automatic=True), **options)
                self.assertNotIn("💬", out)
                self.assertNotIn("What do you want to work on?", out)
                self.assertNotIn("Start a Conductor session?", out)
                self.assertEqual(out, self.without_question(asked))
                self.assertIn("Kerd has nothing saved here yet.", out)
                self.assertTrue(out.splitlines()[-1].strip())

    def test_automatic_stays_out_of_the_guide_example(self):
        self.assertIn("automatic", view.ARRIVAL_OPTIONAL_KEYS)
        self.assertNotIn("automatic", view.OPEN_WORK_KEYS)


if __name__ == "__main__":
    unittest.main()
