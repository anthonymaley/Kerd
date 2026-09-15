import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("change_read", ROOT / "change_read.py")
change_read = importlib.util.module_from_spec(spec)
spec.loader.exec_module(change_read)

ISOLATED_GIT = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
                "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}


class ChangeReadTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, ISOLATED_GIT)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.scratch = Path(self.temp.name).resolve()
        self.project = self.scratch / "repo"
        self.name = "step"
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.write(".gitignore", "build/\n")
        self.write("owned/a.txt", "alpha\n")
        self.write("owned/b.txt", "beta\n")
        self.write("notes/outside.txt", "outside\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "fixture")

    def git(self, *args, project=None):
        return subprocess.run(["git", "-C", str(project or self.project), *args], check=True,
                              capture_output=True, text=True).stdout

    def write(self, relative, content):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content)
        return path

    def baseline(self, paths=("owned",), generated=(), replace=False):
        return change_read.baseline(self.project, list(paths), list(generated), self.name, replace)

    def compare(self):
        return change_read.compare(self.project, self.name)

    def stored(self, project=None):
        git_dir = Path(self.git("rev-parse", "--absolute-git-dir", project=project).strip()).resolve()
        return git_dir / "kerd-conductor" / "baselines" / (self.name + ".json")

    def cli(self, *args, project=None):
        return subprocess.run([sys.executable, str(ROOT / "change_read.py"), "--project",
                               str(project or self.project), *args],
                              cwd=ROOT, capture_output=True, text=True)

    def assert_refused(self, completed, fragment):
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        self.assertIn(fragment, json.loads(completed.stdout)["error"])

    def paths(self, items):
        return [item["path"] for item in items]

    def test_clean_owned_path_reports_nothing(self):
        self.baseline()
        result = self.compare()
        for key in ("tracked_changed", "committed", "added", "modified", "deleted", "symlinks_changed",
                    "unexpected", "outside"):
            self.assertEqual(result[key], [], key)
        self.assertEqual(result["generated"], {})
        self.assertEqual((result["head"]["changed"], result["head"]["commits"]), (False, 0))
        self.assertEqual(result["summary"], "Change read · 0 tracked paths changed, 0 text files to read, "
                                            "0 binary/symlink to check, generated unchanged, unexpected: none, head: unchanged")

    def test_staged_only_and_unstaged_tracked_edits_are_tracked_changes(self):
        self.baseline()
        self.write("owned/a.txt", "alpha staged\n")
        self.git("add", "owned/a.txt")
        self.write("owned/b.txt", "beta unstaged\n")
        result = self.compare()
        self.assertEqual(result["tracked_changed"], [
            {"path": "owned/a.txt", "staged": True, "unstaged": False},
            {"path": "owned/b.txt", "staged": False, "unstaged": True},
        ])
        self.assertEqual(self.paths(result["modified"]), ["owned/a.txt", "owned/b.txt"])

    def test_pre_dirty_unstaged_change_staged_is_tracked_change(self):
        self.write("owned/a.txt", "alpha dirty before dispatch\n")
        self.baseline()
        self.git("add", "owned/a.txt")
        result = self.compare()
        self.assertEqual(result["tracked_changed"], [{"path": "owned/a.txt", "staged": True, "unstaged": True}])
        self.assertEqual(result["modified"], [])

    def test_staged_change_unstaged_is_tracked_change(self):
        self.write("owned/a.txt", "alpha staged before dispatch\n")
        self.git("add", "owned/a.txt")
        self.baseline()
        self.git("reset", "-q", "--", "owned/a.txt")
        result = self.compare()
        self.assertEqual(result["tracked_changed"], [{"path": "owned/a.txt", "staged": True, "unstaged": True}])
        self.assertEqual(result["modified"], [])

    def test_new_untracked_text_file_is_added_and_contents_stay_out_of_output(self):
        self.baseline()
        self.write("owned/new.txt", "secret-marker-text\n")
        result = self.compare()
        self.assertEqual(result["added"], [{"path": "owned/new.txt", "kind": "file", "git": "untracked",
                                            "binary": False, "size": 19}])
        self.assertEqual(result["tracked_changed"], [])
        self.assertNotIn("secret-marker-text", json.dumps(result))
        self.assertNotIn("secret-marker-text", self.stored().read_text())

    def test_pre_dirty_tracked_file_edited_further_is_tracked_change(self):
        self.write("owned/a.txt", "alpha dirty before dispatch\n")
        self.baseline()
        self.assertEqual(self.compare()["tracked_changed"], [])
        self.write("owned/a.txt", "alpha dirty before dispatch\nand edited by the player\n")
        result = self.compare()
        self.assertEqual(result["tracked_changed"], [{"path": "owned/a.txt", "staged": False, "unstaged": True}])
        self.assertEqual(self.paths(result["modified"]), ["owned/a.txt"])

    def test_pre_dirty_untracked_file_modified_is_reported(self):
        self.write("owned/scratch.txt", "draft\n")
        self.baseline()
        self.write("owned/scratch.txt", "draft changed\n")
        result = self.compare()
        self.assertEqual(result["modified"], [{"path": "owned/scratch.txt", "kind": "file",
                                               "git": "untracked", "binary": False, "size": 14}])
        self.assertEqual(result["added"], [])
        self.assertEqual(result["tracked_changed"], [])

    def test_undeclared_ignored_directory_addition_is_unexpected(self):
        self.baseline(paths=("owned", "build"))
        self.write("build/out.o", "compiled\n")
        result = self.compare()
        self.assertEqual(self.paths(result["added"]), ["build/out.o"])
        self.assertEqual(result["added"][0]["git"], "ignored")
        self.assertEqual(result["unexpected"], [{**result["added"][0], "change": "added"}])
        self.assertEqual(result["outside"], [])
        self.assertTrue(result["summary"].endswith("unexpected: 1, head: unchanged"))

    def test_declared_generated_directory_is_summarized_not_unexpected(self):
        self.write("build/old.o", "old\n")
        self.baseline(paths=("owned", "build"), generated=("build/**",))
        before = json.loads(self.stored().read_text())
        self.assertNotIn("build/old.o", before["entries"])
        self.assertEqual(before["generated_summary"]["build"]["count"], 1)
        self.write("build/nested/out.o", "compiled\n")
        result = self.compare()
        self.assertTrue(result["generated"]["build"]["changed"])
        self.assertEqual(result["generated"]["build"]["after"]["count"], 2)
        self.assertEqual(result["unexpected"], [])
        self.assertEqual(result["added"], [])
        self.assertIn("generated changed", result["summary"])

    def test_binary_file_added_is_flagged(self):
        self.baseline()
        self.write("owned/image.bin", b"\x89PNG\x00\x01\x02")
        result = self.compare()
        self.assertEqual(result["added"][0]["path"], "owned/image.bin")
        self.assertTrue(result["added"][0]["binary"])
        self.assertIn("0 text files to read, 1 binary/symlink to check", result["summary"])

    def test_symlink_retarget_is_reported_and_links_are_not_followed(self):
        os.symlink("a.txt", self.project / "owned/link")
        os.symlink("../notes", self.project / "owned/dir-link")
        self.baseline()
        entries = json.loads(self.stored().read_text())["entries"]
        self.assertEqual(entries["owned/dir-link"]["kind"], "symlink")
        self.assertEqual(entries["owned/dir-link"]["target"], "../notes")
        self.assertFalse(any(path.startswith("owned/dir-link/") for path in entries))
        os.unlink(self.project / "owned/link")
        os.symlink("b.txt", self.project / "owned/link")
        result = self.compare()
        self.assertEqual(result["symlinks_changed"], [{"path": "owned/link", "before": "a.txt", "after": "b.txt"}])
        self.assertEqual(self.paths(result["modified"]), ["owned/link"])
        self.assertEqual(result["modified"][0]["kind"], "symlink")

    def test_deletion_and_rename_are_deleted_plus_added(self):
        self.write("owned/scratch.txt", "draft\n")
        self.baseline()
        self.git("mv", "owned/a.txt", "owned/renamed.txt")
        (self.project / "owned/scratch.txt").unlink()
        result = self.compare()
        self.assertEqual(self.paths(result["deleted"]), ["owned/a.txt", "owned/scratch.txt"])
        self.assertEqual(self.paths(result["added"]), ["owned/renamed.txt"])
        self.assertEqual(self.paths(result["tracked_changed"]), ["owned/a.txt", "owned/renamed.txt"])

    def test_change_outside_owned_paths_is_outside_not_added(self):
        self.baseline()
        self.write("notes/outside.txt", "outside edited\n")
        self.write("notes/new.txt", "new\n")
        result = self.compare()
        self.assertEqual(result["outside"], [
            {"path": "notes/new.txt", "before": None, "after": "??", "changed_content": True, "committed": False},
            {"path": "notes/outside.txt", "before": None, "after": " M", "changed_content": True, "committed": False},
        ])
        self.assertEqual(result["added"], [])
        self.assertEqual(result["tracked_changed"], [])

    def test_pre_dirty_outside_tracked_file_edited_again_is_outside(self):
        self.write("notes/outside.txt", "outside dirty before dispatch\n")
        self.baseline()
        self.assertEqual(self.compare()["outside"], [])
        self.write("notes/outside.txt", "outside dirty before dispatch\nand edited again\n")
        self.assertEqual(self.compare()["outside"], [
            {"path": "notes/outside.txt", "before": " M", "after": " M", "changed_content": True, "committed": False},
        ])

    def test_pre_dirty_outside_untracked_file_edited_again_is_outside(self):
        self.write("notes/draft.txt", "draft\n")
        self.baseline()
        self.assertEqual(self.compare()["outside"], [])
        self.write("notes/draft.txt", "draft edited again\n")
        self.assertEqual(self.compare()["outside"], [
            {"path": "notes/draft.txt", "before": "??", "after": "??", "changed_content": True, "committed": False},
        ])

    def test_commit_touching_outside_paths_is_outside_and_merged_with_status(self):
        self.write("notes/second.txt", "second\n")
        self.git("add", "notes/second.txt")
        self.git("commit", "-q", "-m", "second outside file")
        self.write("notes/second.txt", "second dirty before dispatch\n")
        self.baseline()
        self.write("notes/outside.txt", "outside committed by player\n")
        self.git("commit", "-q", "-am", "player commit outside")
        self.write("notes/outside.txt", "outside committed by player\nthen edited again\n")
        self.write("owned/a.txt", "owned edit, not outside\n")
        result = self.compare()
        self.assertTrue(result["head"]["changed"])
        self.assertEqual(result["outside"], [
            {"path": "notes/outside.txt", "before": None, "after": " M", "changed_content": True, "committed": True},
            {"path": "notes/second.txt", "before": " M", "after": None, "changed_content": False, "committed": True},
        ])
        self.assertEqual(result["tracked_changed"], [{"path": "owned/a.txt", "staged": False, "unstaged": True}])
        self.assertEqual(result["committed"], [])

    def test_pre_dirty_owned_content_committed_unchanged_is_committed(self):
        self.write("owned/a.txt", "alpha staged before dispatch\n")
        self.git("add", "owned/a.txt")
        self.baseline()
        self.git("commit", "-q", "-m", "player commits the staged content")
        result = self.compare()
        self.assertTrue(result["head"]["changed"])
        self.assertEqual(result["committed"], ["owned/a.txt"])
        self.assertEqual((result["tracked_changed"], result["modified"], result["outside"]), ([], [], []))

    def test_commit_after_baseline_does_not_hide_tracked_edit(self):
        self.baseline()
        self.write("owned/a.txt", "alpha committed by player\n")
        self.git("commit", "-q", "-am", "player commit")
        result = self.compare()
        self.assertTrue(result["head"]["changed"])
        self.assertEqual(result["tracked_changed"], [{"path": "owned/a.txt", "staged": True, "unstaged": False}])
        self.assertEqual(result["committed"], ["owned/a.txt"])

    def test_empty_commit_after_baseline_is_a_head_finding(self):
        self.baseline()
        self.git("commit", "-q", "--allow-empty", "-m", "empty player commit")
        result = self.compare()
        self.assertEqual((result["head"]["changed"], result["head"]["commits"]), (True, 1))
        self.assertTrue(result["summary"].endswith(", head: changed (1 commits)"))
        for key in ("tracked_changed", "committed", "added", "modified", "deleted", "symlinks_changed",
                    "unexpected", "outside"):
            self.assertEqual(result[key], [], key)

    def test_commit_and_revert_of_owned_file_is_still_committed(self):
        self.write("notes/outside.txt", "outside dirty before dispatch\n")
        self.baseline()
        self.write("owned/a.txt", "alpha changed then reverted\n")
        self.git("commit", "-q", "-m", "player change", "--", "owned/a.txt")
        self.git("revert", "--no-edit", "HEAD")
        result = self.compare()
        self.assertEqual((result["head"]["changed"], result["head"]["commits"]), (True, 2))
        self.assertEqual(result["committed"], ["owned/a.txt"])
        for key in ("tracked_changed", "added", "modified", "deleted", "outside"):
            self.assertEqual(result[key], [], key)
        self.assertTrue(result["summary"].endswith(", head: changed (2 commits)"))

    def test_rewritten_history_reports_diverged_with_endpoint_paths(self):
        self.write("owned/b.txt", "beta committed before dispatch\n")
        self.git("commit", "-q", "-am", "commit later rewritten")
        self.baseline()
        self.git("reset", "-q", "--hard", "HEAD~1")
        self.write("notes/outside.txt", "rewritten outside\n")
        self.git("commit", "-q", "-am", "rewritten history")
        result = self.compare()
        self.assertEqual((result["head"]["changed"], result["head"]["commits"]), (True, None))
        self.assertEqual(result["committed"], ["owned/b.txt"])
        self.assertEqual(self.paths(result["outside"]), ["notes/outside.txt"])
        self.assertTrue(result["outside"][0]["committed"])
        self.assertTrue(result["summary"].endswith(", head: changed (diverged)"))

    def test_first_commit_after_no_commit_baseline_counts_history(self):
        empty = self.scratch / "empty-history"
        subprocess.run(["git", "init", "-q", str(empty)], check=True)
        (empty / "owned").mkdir()
        (empty / "owned/first.txt").write_text("first\n")
        change_read.baseline(empty, ["owned"], [], self.name)
        self.git("add", "owned/first.txt", project=empty)
        self.git("commit", "-q", "-m", "first", project=empty)
        result = change_read.compare(empty, self.name)
        self.assertEqual((result["head"]["before"], result["head"]["commits"]), (None, 1))
        self.assertEqual(result["committed"], ["owned/first.txt"])

    def test_symlinked_or_shared_baseline_file_is_refused(self):
        self.baseline()
        stored = self.stored()
        copy = stored.parent / "copy.json"
        copy.write_bytes(stored.read_bytes())
        os.chmod(copy, 0o600)
        stored.unlink()
        os.symlink(copy, stored)
        self.assert_refused(self.cli("compare", "--name", self.name), "Refused baseline step: it is a symbolic link")
        self.assert_refused(self.cli("discard", "--name", self.name), "Refused baseline step: it is a symbolic link")
        self.assertTrue(stored.is_symlink() and copy.exists())
        stored.unlink()
        os.replace(copy, stored)
        self.assertEqual(self.cli("compare", "--name", self.name).returncode, 0)
        os.chmod(stored, 0o644)
        for action in ("compare", "discard"):
            completed = self.cli(action, "--name", self.name)
            self.assert_refused(completed, "Refused baseline step: it is accessible to group or other users")
            self.assertNotIn(str(stored.parent), completed.stdout)
        self.assertTrue(stored.exists())
        os.remove(stored)
        os.mkdir(stored)
        self.assert_refused(self.cli("compare", "--name", self.name), "it is not a regular file")

    def test_porcelain_status_pairs(self):
        for code in ("??", "DD", "AU", "UD", "UA", "DU", "AA", "UU", " M", "M ", "MM", "A ", "AM", " D",
                     "R ", "RM", "C ", "T ", " T"):
            self.assertTrue(change_read.is_status(code), code)
        for code in ("  ", "!!", "?M", "M?", "!M", " !", "UM", "XY", "M", "MMM", None):
            self.assertFalse(change_read.is_status(code), code)

    def test_escaping_owned_path_and_non_git_project_exit_2(self):
        for path in ("../x", "owned/../../x", str(self.scratch / "elsewhere")):
            with self.subTest(path=path):
                self.assert_refused(self.cli("baseline", "--name", self.name, "--path", path), "Owned path")
        plain = self.scratch / "plain"
        plain.mkdir()
        self.assert_refused(self.cli("baseline", "--name", self.name, "--path", "x", project=plain),
                            "Not a Git work tree")
        self.assertFalse(self.stored().exists())

    def test_summary_line_matches_counts(self):
        self.baseline(paths=("owned", "build"))
        self.write("owned/a.txt", "alpha edited\n")
        self.write("owned/one.txt", "one\n")
        self.write("owned/two.txt", "two\n")
        self.write("owned/blob.bin", b"\x00binary")
        os.symlink("a.txt", self.project / "owned/new-link")
        self.write("build/stray.o", "stray\n")
        completed = self.cli("compare", "--name", self.name)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        result = json.loads(completed.stdout)
        changes = result["added"] + result["modified"]
        to_read = [i for i in changes if i["kind"] == "file" and not i["binary"] and i["git"] != "tracked"]
        to_check = [i for i in changes + result["deleted"] if i["binary"] or i["kind"] != "file"]
        self.assertEqual((len(result["tracked_changed"]), len(to_read), len(to_check), len(result["unexpected"])),
                         (1, 3, 2, 1))
        self.assertEqual(result["summary"], "Change read · 1 tracked paths changed, 3 text files to read, "
                                            "2 binary/symlink to check, generated unchanged, unexpected: 1, head: unchanged")

    def test_repository_without_commits_has_null_head(self):
        empty = self.scratch / "empty"
        subprocess.run(["git", "init", "-q", str(empty)], check=True)
        (empty / "owned").mkdir()
        (empty / "owned/first.txt").write_text("first\n")
        record = change_read.baseline(empty, ["owned"], [], self.name)
        self.assertIsNone(record["head"])
        subprocess.run(["git", "-C", str(empty), "add", "owned/first.txt"], check=True)
        result = change_read.compare(empty, self.name)
        self.assertEqual(result["tracked_changed"], [{"path": "owned/first.txt", "staged": True, "unstaged": False}])
        self.assertEqual(result["added"], [])

    def test_baseline_is_private_in_git_dir_and_absent_from_status(self):
        completed = self.cli("baseline", "--name", self.name, "--path", "owned")
        self.assertEqual(completed.returncode, 0, completed.stdout)
        stored = self.stored()
        self.assertTrue(stored.is_file())
        self.assertEqual(stored.stat().st_mode & 0o777, 0o600)
        for folder in (stored.parent, stored.parent.parent):
            self.assertEqual(folder.stat().st_mode & 0o777, 0o700)
        self.assertEqual(self.git("status", "--porcelain", "--ignored", "--untracked-files=all"), "")
        self.assertEqual(json.loads(completed.stdout)["baseline"], self.name)
        for output in (completed.stdout, self.cli("compare", "--name", self.name).stdout):
            self.assertNotIn(str(stored.parent), output)
            self.assertNotIn("kerd-conductor", output)
        self.assertEqual(sorted(p.name for p in stored.parent.iterdir()), [self.name + ".json"])

    def test_bad_names_are_refused(self):
        for name in ("", "../escape", ".hidden", "a/b", "-dash", "x" * 65, "new\nline", "sp ace"):
            with self.subTest(name=name):
                self.assert_refused(self.cli("baseline", "--name=" + name, "--path", "owned"), "Baseline names")
                self.assert_refused(self.cli("compare", "--name=" + name), "Baseline names")
                self.assert_refused(self.cli("discard", "--name=" + name), "Baseline names")

    def test_existing_name_needs_replace(self):
        self.baseline()
        self.write("owned/a.txt", "alpha changed before the second baseline\n")
        self.assert_refused(self.cli("baseline", "--name", self.name, "--path", "owned"), "already exists")
        self.assertEqual(self.paths(self.compare()["tracked_changed"]), ["owned/a.txt"])
        completed = self.cli("baseline", "--name", self.name, "--path", "owned", "--replace")
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(self.compare()["tracked_changed"], [])
        self.assertEqual(self.stored().stat().st_mode & 0o777, 0o600)

    def test_discard_removes_baseline_and_compare_then_exits_2(self):
        self.baseline()
        completed = self.cli("discard", "--name", self.name)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(json.loads(completed.stdout), {"discarded": self.name})
        self.assertFalse(self.stored().exists())
        self.assert_refused(self.cli("compare", "--name", self.name), "No baseline named step")
        self.assert_refused(self.cli("discard", "--name", self.name), "No baseline named step")

    def test_store_inside_work_tree_is_refused(self):
        project = self.scratch / "separate"
        subprocess.run(["git", "init", "-q", "--separate-git-dir", str(project / "metadata"), str(project)],
                       check=True)
        self.assert_refused(self.cli("baseline", "--name", self.name, "--path", ".", project=project),
                            "inside the work tree")
        self.assertFalse((project / "metadata" / "kerd-conductor").exists())

    def test_tampered_baselines_are_refused(self):
        self.write("owned/scratch.txt", "draft\n")
        os.symlink("a.txt", self.project / "owned/link")
        self.write("notes/outside.txt", "dirty outside\n")
        self.baseline(paths=("owned", "build"), generated=("build/**",))
        original = json.loads(self.stored().read_text())
        self.write("build/out.o", "generated\n")
        self.baseline(paths=("owned", "build"), generated=("build/**",), replace=True)
        with_summary = json.loads(self.stored().read_text())
        self.assertTrue(original["outside_status"] and with_summary["generated_summary"])

        def entry_copy(record):
            record["entries"]["owned/../escape"] = record["entries"]["owned/a.txt"]

        def tracked_outside(record):
            record["tracked"]["notes/outside.txt"] = record["tracked"]["owned/a.txt"]

        cases = [
            ("traversal entry key", entry_copy, "not a normalized path"),
            ("tracked key outside owned", tracked_outside, "under an owned path"),
            ("absolute owned path", lambda r: r.update(paths=[str(self.project / "owned")]), "owned paths"),
            ("bad hash", lambda r: r["entries"]["owned/a.txt"].update(sha256="ABC"), "SHA-256"),
            ("bad tracked hash", lambda r: r["tracked"]["owned/a.txt"].update(staged="0" * 63), "SHA-256"),
            ("file without sha256", lambda r: r["entries"]["owned/scratch.txt"].pop("sha256"), "fields"),
            ("symlink without target", lambda r: r["entries"]["owned/link"].update(target=7), "target"),
            ("bad status code", lambda r: r["outside_status"][0].__setitem__(0, "XY"), "porcelain"),
            ("mixed untracked code", lambda r: r["outside_status"][0].__setitem__(0, "?M"), "porcelain"),
            ("blank status code", lambda r: r["outside_status"][0].__setitem__(0, "  "), "porcelain"),
            ("ignored status code", lambda r: r["outside_status"][0].__setitem__(0, "!!"), "porcelain"),
            ("outside path under owned", lambda r: r["outside_status"][0].__setitem__(1, "owned/a.txt"),
             "outside the owned paths"),
            ("outside git path", lambda r: r["outside_status"][0].__setitem__(1, ".git/config"), "normalized"),
            ("negative count", lambda r: r["generated_summary"]["build"].update(count=-1), "count"),
            ("wrong schema", lambda r: r.update(schema=2), "schema must be 1"),
            ("missing schema", lambda r: r.pop("schema"), "schema must be 1"),
            ("other root", lambda r: r.update(root=str(self.scratch)), "another project"),
        ]
        for label, tamper, fragment in cases:
            with self.subTest(label):
                record = json.loads(json.dumps(with_summary))
                tamper(record)
                self.stored().write_text(json.dumps(record))
                self.assert_refused(self.cli("compare", "--name", self.name), fragment)
                self.assertIn("Invalid baseline step", self.cli("compare", "--name", self.name).stdout)
        self.stored().write_text(json.dumps(with_summary))
        self.assertEqual(self.cli("compare", "--name", self.name).returncode, 0)
        self.stored().write_text("not json")
        self.assert_refused(self.cli("compare", "--name", self.name), "not valid JSON")


if __name__ == "__main__":
    unittest.main()
