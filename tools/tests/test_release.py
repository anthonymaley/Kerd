"""tools/release.py: real exit codes, exact-commit CI lookup, nothing outward on a refusal."""
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release  # noqa: E402

GATE = """name: entry-gate
on: [push]
jobs:
  gate:
    steps:
      - uses: actions/checkout@v4
      - name: First
        run: {first}
      - name: Second
        run: {second}
      - name: Release rules
        run: python3 tools/release_check.py
"""

RELEASE_CHECK_STUB = "import sys\nprint('release: clean')\nsys.exit(int(__import__('os').environ.get('STUB_RULES', '0')))\n"
CODEX_STUB = ("import os, sys, pathlib\n"
              "pathlib.Path(os.environ['FAKE_CODEX_LOG']).write_text(os.getcwd() + ' ' + ' '.join(sys.argv[1:]))\n"
              "print('codex stub published')\n")

FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
state = json.load(open(os.environ['FAKE_GH_STATE']))
args = sys.argv[1:]
with open(os.environ['FAKE_GH_STATE'] + '.calls', 'a') as calls:
    calls.write(' '.join(args) + '\\n')
if args[:2] == ['run', 'list']:
    if state.get('list_fails'):
        sys.exit(1)
    if state.get('list_fails_later'):
        state['list_fails'] = True
        json.dump(state, open(os.environ['FAKE_GH_STATE'], 'w'))
    print(json.dumps(state['runs']))
    if state.get('later_runs'):
        state['runs'] += state.pop('later_runs')
        json.dump(state, open(os.environ['FAKE_GH_STATE'], 'w'))
elif args[:2] == ['run', 'view'] and '--log-failed' in args:
    print('step Skill unit tests\\nFAIL: test_something')
elif args[:2] == ['run', 'view']:
    if state.get('on_view'):
        os.system(state['on_view'])
    run = [r for r in state['runs'] if str(r['databaseId']) == args[2]][0]
    seq = state.get('attempts')
    attempt = seq.pop(0) if seq else run.get('attempt', 1)
    if seq is not None:
        json.dump(state, open(os.environ['FAKE_GH_STATE'], 'w'))
    print(json.dumps({'status': run['status'], 'conclusion': run['conclusion'], 'headSha': run['headSha'],
                      'attempt': attempt}))
"""

FAKE_CLAUDE = """#!/bin/sh
echo "$@" >> "$FAKE_CLAUDE_LOG"
"""


def release_source():
    return Path(release.__file__).read_text()


def sh(cwd, *cmd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.repo = base / "repo"
        self.remote = base / "remote.git"
        self.bin = base / "bin"
        self.bin.mkdir()
        sh(base, "git", "init", "-q", "--bare", "-b", "main", str(self.remote))
        sh(base, "git", "init", "-q", "-b", "main", str(self.repo))
        for key, value in (("user.email", "t@example.com"), ("user.name", "t"), ("commit.gpgsign", "false")):
            sh(self.repo, "git", "config", key, value)
        self.write(".claude-plugin/plugin.json", '{\n  "name": "kerd",\n  "version": "1.2.3"\n}\n')
        self.write(".claude-plugin/marketplace.json",
                   '{\n  "metadata": {\n    "version": "1.2.3"\n  },\n  "plugins": [\n    {"name": "kerd", "version": "1.2.3"},\n'
                   '    {"name": "other", "version": "0.1.0"}\n  ]\n}\n')
        self.write("README.md", "# Kerd\n\n## What's New (v1.2.3)\n\nEvery release, newest first.\n\n### v1.2.3\n\nOld note.\n")
        self.write("CHANGELOG.md", "# Changelog\n\n## 1.2.3\n\nOld note.\n")
        self.write("tools/release_check.py", RELEASE_CHECK_STUB)
        self.write("tools/codex_release.py", CODEX_STUB)
        self.gate("echo '3 tests'", "echo 'All green.'")
        sh(self.repo, "git", "add", "-A")
        sh(self.repo, "git", "commit", "-qm", "start")
        sh(self.repo, "git", "remote", "add", "origin", str(self.remote))
        sh(self.repo, "git", "push", "-q", "origin", "main")
        gh = self.bin / "gh"
        gh.write_text(FAKE_GH)
        gh.chmod(0o755)
        claude = self.bin / "claude"
        claude.write_text(FAKE_CLAUDE)
        claude.chmod(0o755)
        self.state = base / "gh-state.json"
        self.claude_log = base / "claude.log"
        self.installed = base / "installed_plugins.json"
        self.codex_log = base / "codex-called.txt"
        self.env = {"KERD_RELEASE_GH": str(gh), "KERD_RELEASE_CLAUDE": str(claude), "KERD_RELEASE_POLL": "0",
                    "FAKE_GH_STATE": str(self.state), "FAKE_CLAUDE_LOG": str(self.claude_log),
                    "KERD_RELEASE_INSTALLED": str(self.installed), "FAKE_CODEX_LOG": str(self.codex_log)}
        old = {k: os.environ.get(k) for k in self.env}
        os.environ.update(self.env)
        self.addCleanup(lambda: [os.environ.pop(k) if v is None else os.environ.__setitem__(k, v) for k, v in old.items()])

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def gate(self, first, second):
        self.write(".github/workflows/gate.yml", GATE.format(first=first, second=second))

    def gh_runs(self, runs, **extra):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        runs = [{"createdAt": now, **r} for r in runs]
        self.state.write_text(json.dumps({"runs": runs, **extra}))

    def call(self, function, *args, **kw):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                code = function(*args, **kw)
            except release.Refused as error:
                code, err = 2, io.StringIO(str(error))
        return code, out.getvalue() + err.getvalue()

    def head(self):
        return sh(self.repo, "git", "rev-parse", "HEAD")

    def install_record(self, sha):
        self.installed.write_text(json.dumps({"plugins": {"kerd@kerd-marketplace": [{"gitCommitSha": sha}]}}))

    def remote_head(self):
        return sh(self.remote, "git", "rev-parse", "main")

    def commit(self, message="change"):
        self.write("change.txt", message)
        sh(self.repo, "git", "add", "change.txt")
        sh(self.repo, "git", "commit", "-qm", message)

    # check

    def test_check_reads_the_workflow_steps_and_passes_only_when_each_exits_zero(self):
        code, out = self.call(release.check, self.repo, Path(self.tmp.name) / "logs")
        self.assertEqual(code, 0, out)
        self.assertIn("ok: First — exit 0; 3 tests", out)
        self.assertIn("check: 3 of 3 steps passed", out)

    def test_check_fails_on_a_failing_step_even_when_a_later_one_passes(self):
        self.gate("echo '5 tests'; exit 1", "echo 'All green.'")
        code, out = self.call(release.check, self.repo, Path(self.tmp.name) / "logs")
        self.assertEqual(code, 1)
        self.assertIn("FAILED: First — exit 1", out)
        self.assertIn("check: 2 of 3 steps passed", out)

    def test_a_piped_step_is_judged_by_its_pipeline_as_ci_would(self):
        # The workflow's own command decides; the script adds no pipe of its own.
        self.gate("exit 1", "true")
        code, _ = self.call(release.check, self.repo, Path(self.tmp.name) / "logs")
        self.assertEqual(code, 1)

    def test_check_refuses_a_workflow_with_no_steps(self):
        self.write(".github/workflows/gate.yml", "name: entry-gate\n")
        code, out = self.call(release.check, self.repo)
        self.assertEqual(code, 2)
        self.assertIn("no run steps", out)

    # prep

    def test_prep_bumps_all_three_fields_and_writes_the_same_note_twice(self):
        note = Path(self.tmp.name) / "note.md"
        note.write_text("**New thing.** It does a thing.\n")
        code, out = self.call(release.prep, self.repo, "1.2.4", note.read_text(), run_check=False)
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads((self.repo / ".claude-plugin/plugin.json").read_text())["version"], "1.2.4")
        market = json.loads((self.repo / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual((market["metadata"]["version"], market["plugins"][0]["version"], market["plugins"][1]["version"]),
                         ("1.2.4", "1.2.4", "0.1.0"))
        readme = (self.repo / "README.md").read_text()
        self.assertIn("## What's New (v1.2.4)", readme)
        self.assertLess(readme.index("### v1.2.4\n\n**New thing.** It does a thing.\n"), readme.index("### v1.2.3"))
        changelog = (self.repo / "CHANGELOG.md").read_text()
        self.assertLess(changelog.index("## 1.2.4\n\n**New thing.** It does a thing.\n"), changelog.index("## 1.2.3"))

    def test_prep_refuses_an_older_version_and_changes_nothing(self):
        before = (self.repo / "README.md").read_text()
        code, out = self.call(release.prep, self.repo, "1.2.3", "note", run_check=False)
        self.assertEqual(code, 2)
        self.assertIn("not newer", out)
        self.assertEqual((self.repo / "README.md").read_text(), before)

    def test_prep_refuses_drifted_manifests_before_writing_anything(self):
        self.write(".claude-plugin/plugin.json", '{\n  "version": "1.2.2"\n}\n')
        code, out = self.call(release.prep, self.repo, "1.2.4", "note", run_check=False)
        self.assertEqual(code, 2)
        self.assertNotIn("1.2.4", (self.repo / "README.md").read_text())

    # ship

    def test_ship_refuses_uncommitted_tracked_changes_without_pushing(self):
        self.commit()
        self.write("README.md", "edited\n")
        code, out = self.call(release.ship, self.repo)
        self.assertEqual(code, 2)
        self.assertIn("uncommitted", out)
        self.assertNotEqual(self.remote_head(), self.head())

    def test_ship_refuses_publishing_from_a_branch_other_than_main(self):
        sh(self.repo, "git", "switch", "-qc", "concert/x")
        code, out = self.call(release.ship, self.repo, codex=True)
        self.assertEqual(code, 2)
        self.assertIn("main only", out)

    def test_ship_refuses_when_the_release_check_fails(self):
        os.environ["STUB_RULES"] = "1"
        self.addCleanup(os.environ.pop, "STUB_RULES")
        self.commit()
        code, out = self.call(release.ship, self.repo)
        self.assertEqual(code, 2)
        self.assertNotEqual(self.remote_head(), self.head())

    def test_ship_waits_for_the_run_of_this_exact_commit_then_publishes(self):
        self.commit()
        sha = self.head()
        self.gh_runs([{"databaseId": 7, "headSha": "0" * 40, "status": "completed", "conclusion": "success", "event": "push"}],
                     later_runs=[{"databaseId": 9, "headSha": sha, "status": "completed", "conclusion": "success",
                                  "event": "push", "createdAt": "x"}])
        self.install_record(sha)
        code, out = self.call(release.ship, self.repo, codex=True, plugin=True, deadline_seconds=5)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.remote_head(), sha)
        self.assertIn("ci: run 9 attempt 1 passed", out)
        called = self.codex_log.read_text()
        self.assertIn(f"--ref {sha} --publish", called)
        self.assertNotIn(str(self.repo.resolve()) + " ", called)  # ran from a worktree at the commit, not the tree
        self.assertIn("plugin update kerd@kerd-marketplace", self.claude_log.read_text())

    def test_ship_publishes_nothing_when_ci_fails_and_prints_the_failing_lines(self):
        self.commit()
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": self.head(), "status": "completed",
                                      "conclusion": "failure", "event": "push"}])
        code, out = self.call(release.ship, self.repo, codex=True, plugin=True, deadline_seconds=5)
        self.assertEqual(code, 1)
        self.assertIn("FAIL: test_something", out)
        self.assertFalse(self.codex_log.exists())
        self.assertFalse(self.claude_log.exists())

    def test_ship_never_takes_another_commits_run_and_times_out_honestly(self):
        self.commit()
        self.gh_runs([{"databaseId": 7, "headSha": "0" * 40, "status": "completed", "conclusion": "success", "event": "push"}])
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=0)
        self.assertEqual(code, 3)
        self.assertIn("no new entry-gate run", out)
        self.assertFalse(self.codex_log.exists())

    def test_ship_stops_when_gh_cannot_be_read_and_says_it_pushed(self):
        self.commit()
        self.gh_runs([], list_fails_later=True)
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=5)
        self.assertEqual(code, 4)
        self.assertEqual(self.remote_head(), self.head())
        self.assertIn("published: nothing", out)
        self.assertFalse(self.codex_log.exists())

    def test_ship_ignores_an_older_run_for_the_same_commit_after_a_new_push(self):
        self.commit()
        self.gh_runs([{"databaseId": 9, "headSha": self.head(), "status": "completed", "conclusion": "success",
                       "event": "push", "createdAt": "2020-01-01T00:00:00Z"}])
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=0)
        self.assertEqual(code, 3)
        self.assertFalse(self.codex_log.exists())

    def test_ship_says_when_the_remote_already_held_the_commit(self):
        self.commit()
        sh(self.repo, "git", "push", "-q", "origin", "main")
        self.gh_runs([{"databaseId": 9, "headSha": self.head(), "status": "completed", "conclusion": "success",
                       "event": "push", "createdAt": "2020-01-01T00:00:00Z"}])
        code, out = self.call(release.ship, self.repo, deadline_seconds=0)
        self.assertEqual(code, 0, out)
        self.assertIn("already holds", out)

    def test_ship_pushes_the_checked_commit_not_whatever_the_branch_holds(self):
        self.commit()
        sha = self.head()
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": sha, "status": "completed", "conclusion": "success", "event": "push"}])
        code, out = self.call(release.ship, self.repo, deadline_seconds=5)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.remote_head(), sha)
        self.assertIn(f"pushed: {sha[:8]} to main", out)

    def test_ship_stops_on_an_unknown_run_status(self):
        self.commit()
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": self.head(), "status": "mystery", "conclusion": None, "event": "push"}])
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=5)
        self.assertEqual(code, 4)
        self.assertFalse(self.codex_log.exists())

    def test_ship_does_not_update_the_plugin_when_the_branch_moved_during_ci(self):
        self.commit()
        sha = self.head()
        other = Path(self.tmp.name) / "other"
        mover = (f"git clone -q {self.remote} {other} && cd {other} && git -c user.email=t@e -c user.name=t "
                 f"commit -q --allow-empty -m moved && git push -q origin HEAD:main")
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": sha, "status": "completed", "conclusion": "success",
                                      "event": "push"}], on_view=mover)
        code, out = self.call(release.ship, self.repo, plugin=True, deadline_seconds=5)
        self.assertEqual(code, 4, out)
        self.assertIn("changed before claude", out)
        self.assertFalse(self.claude_log.exists())

    def test_ship_refuses_a_deadline_that_is_not_a_number(self):
        self.commit()
        code, out = self.call(release.ship, self.repo, deadline_seconds=float("nan"))
        self.assertEqual(code, 2)
        self.assertNotEqual(self.remote_head(), self.head())

    def test_a_hung_gh_is_bounded(self):
        self.assertIn("timeout=60", release_source())

    def test_prep_refuses_an_unreadable_workflow_before_writing(self):
        self.write(".github/workflows/gate.yml", GATE.format(first="true", second="true") + "      - run: echo hidden\n")
        before = (self.repo / "README.md").read_text()
        code, out = self.call(release.prep, self.repo, "1.2.4", "note")
        self.assertEqual(code, 2)
        self.assertIn("unnamed", out)
        self.assertEqual((self.repo / "README.md").read_text(), before)


    def test_a_pipe_fails_when_any_part_of_it_fails(self):
        self.gate("false | true", "true")
        code, out = self.call(release.check, self.repo, Path(self.tmp.name) / "logs")
        self.assertEqual(code, 1, out)

    def test_a_name_never_carries_over_to_an_unnamed_run_step(self):
        self.write(".github/workflows/gate.yml", "jobs:\n  g:\n    steps:\n      - name: Checkout\n        uses: x@v1\n"
                   "      - run: echo hidden\n")
        code, out = self.call(release.check, self.repo)
        self.assertEqual(code, 2)
        self.assertIn("unnamed", out)

    def test_a_folded_run_block_is_refused(self):
        self.gate("|-", "true")
        code, out = self.call(release.check, self.repo)
        self.assertEqual(code, 2)
        self.assertIn("multi-line", out)

    def test_gh_unreadable_before_the_push_refuses_without_pushing(self):
        self.commit()
        self.gh_runs([], list_fails=True)
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=5)
        self.assertEqual(code, 2)
        self.assertNotEqual(self.remote_head(), self.head())

    def test_a_malformed_run_list_entry_stops_without_publishing(self):
        self.commit()
        self.state.write_text(json.dumps({"runs": [], "later_runs": [["not", "a", "run"]]}))
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=5)
        self.assertEqual(code, 4)
        self.assertIn("published: nothing", out)
        self.assertFalse(self.codex_log.exists())

    def test_a_rerun_after_the_green_read_stops_the_publish(self):
        self.commit()
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": self.head(), "status": "completed",
                                      "conclusion": "success", "event": "push"}], attempts=[1, 2])
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=5)
        self.assertEqual(code, 4, out)
        self.assertIn("changed before the codex publish", out)
        self.assertFalse(self.codex_log.exists())

    def test_a_plugin_installed_from_another_commit_is_reported_with_what_was_published(self):
        self.commit()
        sha = self.head()
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": sha, "status": "completed",
                                      "conclusion": "success", "event": "push"}])
        self.install_record("f" * 40)
        code, out = self.call(release.ship, self.repo, codex=True, plugin=True, deadline_seconds=5)
        self.assertEqual(code, 4, out)
        self.assertIn(f"codex at {sha[:8]}", out)
        self.assertIn("not the checked", out)

    def test_a_run_command_continued_on_the_next_line_is_refused(self):
        self.gate("true\n          && false", "true")
        code, out = self.call(release.check, self.repo)
        self.assertEqual(code, 2)
        self.assertIn("continued", out)

    def test_an_unreadable_attempt_stops_before_publishing(self):
        self.commit()
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": self.head(), "status": "completed",
                                      "conclusion": "success", "event": "push"}], attempts=[None, None])
        code, out = self.call(release.ship, self.repo, codex=True, deadline_seconds=5)
        self.assertEqual(code, 4, out)
        self.assertIn("unreadable attempt", out)
        self.assertFalse(self.codex_log.exists())

    def test_a_missing_claude_is_a_stop_line_that_lists_what_was_published(self):
        self.commit()
        sha = self.head()
        os.environ["KERD_RELEASE_CLAUDE"] = str(Path(self.tmp.name) / "no-such-claude")
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": sha, "status": "completed",
                                      "conclusion": "success", "event": "push"}])
        code, out = self.call(release.ship, self.repo, codex=True, plugin=True, deadline_seconds=5)
        self.assertEqual(code, 1, out)
        self.assertIn("could not start", out)
        self.assertIn(f"published: codex at {sha[:8]}", out)

    def test_a_rerun_between_the_two_plugin_commands_stops_the_second(self):
        self.commit()
        sha = self.head()
        self.install_record(sha)
        self.gh_runs([], later_runs=[{"databaseId": 9, "headSha": sha, "status": "completed",
                                      "conclusion": "success", "event": "push"}], attempts=[1, 1, 2])
        code, out = self.call(release.ship, self.repo, plugin=True, deadline_seconds=5)
        self.assertEqual(code, 4, out)
        self.assertEqual(self.claude_log.read_text().count("\n"), 1)

if __name__ == "__main__":
    unittest.main()
