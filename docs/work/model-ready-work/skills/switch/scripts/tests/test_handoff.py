"""Git handoff behavior in temporary repos with a local bare remote only."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "handoff.py"
SPEC = importlib.util.spec_from_file_location("switch_handoff_tested", SCRIPT)
handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handoff)


class HandoffTests(unittest.TestCase):
    branch = "handoff-trial"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="switch-handoff-test-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name).resolve()
        self.source = self.folder / "source"
        self.dest = self.folder / "destination"
        self.remote = self.folder / "remote.git"
        self.git(self.folder, "init", "--bare", "-q", str(self.remote))
        self.git(self.folder, "init", "-q", "-b", self.branch, str(self.source))
        self.configure(self.source)
        (self.source / "record.md").write_text("Continue the original bounded task.\n")
        (self.source / "result.txt").write_text("original result\n")
        self.commit(self.source, "initial")
        self.git(self.source, "remote", "add", "origin", str(self.remote))
        self.git(self.source, "push", "-q", "-u", "origin", self.branch)
        self.git(self.folder, "clone", "-q", "--branch", self.branch, str(self.remote), str(self.dest))
        self.configure(self.dest)
        self.original = self.git(self.source, "rev-parse", "HEAD")

    def git(self, root, *args):
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
        if result.returncode:
            self.fail(f"Fixture git {args[0]} failed: {result.stderr}")
        return result.stdout.strip()

    def configure(self, root):
        for key, value in (("user.name", "Isolated Test"), ("user.email", "test@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
            self.git(root, "config", key, value)

    def commit(self, root, message):
        self.git(root, "add", "--all")
        self.git(root, "commit", "-q", "-m", message)
        return self.git(root, "rev-parse", "HEAD")

    def publish(self, files=None, push=False):
        return handoff.publish(self.source, self.branch, files or ["record.md", "result.txt"],
                               "Save exact handoff", push=push)

    def advance_remote(self):
        (self.source / "record.md").write_text("Continue the next exact bounded action.\n")
        return self.publish(push=True)["commit"]

    def test_explicit_files_are_committed_and_remote_save_is_verified(self):
        (self.source / "result.txt").write_text("completed piece\n")
        result = self.publish(push=True)
        self.assertEqual(result["status"], "saved_to_remote")
        self.assertFalse(result["source_session_exited"])
        self.assertEqual(self.git(self.source, "show", "--format=", "--name-only", "HEAD"), "result.txt")
        self.assertEqual(self.git(self.remote, "rev-parse", f"refs/heads/{self.branch}"), result["commit"])
        self.assertEqual(self.git(self.source, "status", "--porcelain"), "")

    def test_tracked_deletion_can_be_explicitly_saved(self):
        (self.source / "result.txt").unlink()
        self.publish(files=["result.txt"])
        self.assertEqual(self.git(self.source, "show", "--format=", "--name-status", "HEAD"), "D\tresult.txt")

    def test_unassigned_tracked_and_untracked_work_block_without_staging(self):
        for name in ("record.md", "unassigned.txt"):
            with self.subTest(name=name):
                path = self.source / name
                old = path.read_bytes() if path.exists() else None
                path.write_text("unassigned changes")
                with self.assertRaisesRegex(handoff.HandoffError, "Unassigned changes"):
                    self.publish(files=["result.txt"])
                self.assertEqual(self.git(self.source, "diff", "--cached", "--name-only"), "")
                self.assertEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)
                if old is None:
                    path.unlink()
                else:
                    path.write_bytes(old)

    def test_existing_index_is_preserved(self):
        (self.source / "record.md").write_text("staged user work")
        self.git(self.source, "add", "--", "record.md")
        before = self.git(self.source, "diff", "--cached", "--binary")
        with self.assertRaisesRegex(handoff.HandoffError, "Index already contains"):
            self.publish()
        self.assertEqual(self.git(self.source, "diff", "--cached", "--binary"), before)
        self.assertEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)

    def test_wrong_branch_and_detached_head_do_not_checkout_or_commit(self):
        with self.assertRaises(handoff.HandoffError):
            handoff.publish(self.source, "different", ["record.md"], "save")
        self.assertEqual(self.git(self.source, "symbolic-ref", "--short", "HEAD"), self.branch)
        self.git(self.source, "checkout", "-q", "--detach")
        with self.assertRaises(handoff.HandoffError):
            self.publish()
        self.assertEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)

    def test_failed_push_keeps_local_commit_and_remote_unchanged(self):
        self.git(self.source, "remote", "set-url", "--push", "origin", str(self.folder / "missing.git"))
        (self.source / "result.txt").write_text("recoverable local work")
        with self.assertRaises(handoff.HandoffError):
            self.publish(push=True)
        self.assertNotEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git(self.remote, "rev-parse", f"refs/heads/{self.branch}"), self.original)
        self.assertEqual(self.git(self.source, "status", "--porcelain"), "")
        self.assertEqual((self.source / "result.txt").read_text(), "recoverable local work")

    def test_clean_behind_pickup_fast_forwards_and_loads_new_record(self):
        latest = self.advance_remote()
        result = handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(result["status"], "record_loaded")
        self.assertEqual(result["commit"], latest)
        self.assertEqual(result["content"], (self.source / "record.md").read_text())
        self.assertEqual(result["bytes"], len((self.dest / "record.md").read_bytes()))

    def test_dirty_pickup_does_not_change_head_or_local_content(self):
        self.advance_remote()
        (self.dest / "record.md").write_text("unsaved destination work")
        with self.assertRaisesRegex(handoff.HandoffError, "Local changes exist"):
            handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), self.original)
        self.assertEqual((self.dest / "record.md").read_text(), "unsaved destination work")

    def test_exact_revision_pickup_updates_to_the_saved_commit(self):
        latest = self.advance_remote()
        result = handoff.prepare(self.dest, self.branch, "record.md", sync=True, expected_commit=latest)
        self.assertEqual(result["commit"], latest)
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), latest)

    def test_newer_remote_does_not_update_checkout_or_load_a_different_record(self):
        self.advance_remote()
        before = (self.dest / "record.md").read_bytes()
        with patch.object(handoff, "source_text") as read:
            with self.assertRaisesRegex(handoff.HandoffError, "checkout not updated"):
                handoff.prepare(self.dest, self.branch, "record.md", sync=True, expected_commit=self.original)
            read.assert_not_called()
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), self.original)
        self.assertEqual((self.dest / "record.md").read_bytes(), before)
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")

    def test_exact_local_pickup_never_silently_uses_another_revision(self):
        latest = self.advance_remote()
        with self.assertRaisesRegex(handoff.HandoffError, "Local revision differs"):
            handoff.pickup(self.dest, self.branch, "record.md", expected_commit=latest)
        result = handoff.pickup(self.dest, self.branch, "record.md", expected_commit=self.original)
        self.assertEqual(result["commit"], self.original)

    def test_revision_must_be_an_exact_commit_not_an_expression(self):
        for revision in ("HEAD", "main", self.original[:8], "--help", "a" * 41, True):
            with self.subTest(revision=revision), patch.object(handoff, "git") as git:
                with self.assertRaisesRegex(handoff.HandoffError, "full Git commit"):
                    handoff.pickup(self.dest, self.branch, "record.md", sync=True, expected_commit=revision)
                git.assert_not_called()

    def test_exact_revision_is_supported_by_the_cli(self):
        latest = self.advance_remote()
        result = subprocess.run(["python3", str(SCRIPT), "--project", str(self.dest), "prepare",
            "--branch", self.branch, "--record", "record.md", "--commit", latest, "--sync"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["commit"], latest)

    def test_replaced_fetch_head_cannot_change_the_checked_merge_target(self):
        latest = self.advance_remote()
        original = handoff.git
        def replace_fetch(root, *args):
            if args[0] == "merge-base":
                self.git(root, "fetch", "origin", self.original)
            return original(root, *args)
        with patch.object(handoff, "git", side_effect=replace_fetch):
            result = handoff.pickup(self.dest, self.branch, "record.md", sync=True, expected_commit=latest)
        self.assertEqual(result["commit"], latest)

    def test_edit_during_exact_record_read_does_not_return_verified_pickup(self):
        original = handoff.source_text
        def changed(path):
            content = original(path)
            path.write_text("Concurrent edit")
            return content
        with patch.object(handoff, "source_text", side_effect=changed):
            with self.assertRaisesRegex(handoff.HandoffError, "Project changed"):
                handoff.pickup(self.dest, self.branch, "record.md", expected_commit=self.original)

    def test_ahead_pickup_does_not_reset_local_commit(self):
        (self.dest / "result.txt").write_text("destination local commit")
        ahead = self.commit(self.dest, "destination ahead")
        with self.assertRaisesRegex(handoff.HandoffError, "ahead or diverged"):
            handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), ahead)

    def test_diverged_pickup_does_not_merge_histories(self):
        self.advance_remote()
        (self.dest / "result.txt").write_text("destination divergence")
        diverged = self.commit(self.dest, "destination diverged")
        with self.assertRaisesRegex(handoff.HandoffError, "ahead or diverged"):
            handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), diverged)

    def test_path_traversal_absolute_directory_and_final_symlink_are_rejected(self):
        (self.source / "alias.md").symlink_to("record.md")
        for path in ("../outside", str(self.source / "record.md"), ".git/config", ".", "alias.md"):
            with self.subTest(path=path):
                with self.assertRaises((handoff.HandoffError, ValueError)):
                    handoff.relative_file(self.source, path)

    def test_escaping_parent_symlink_is_rejected(self):
        (self.source / "external").symlink_to(self.folder)
        (self.folder / "outside.md").write_text("outside content")
        with self.assertRaises(handoff.HandoffError):
            handoff.relative_file(self.source, "external/outside.md")

    def test_directory_symlink_into_git_metadata_cannot_be_loaded_as_record(self):
        (self.dest / "metadata").symlink_to(".git")
        self.commit(self.dest, "directory alias")
        with self.assertRaises(handoff.HandoffError):
            handoff.pickup(self.dest, self.branch, "metadata/config")

    def test_leading_whitespace_filename_cannot_hide_unassigned_work(self):
        (self.source / " stray.txt").write_text("original unassigned file")
        (self.source / "stray.txt").write_text("original assigned file")
        self.commit(self.source, "whitespace filenames")
        (self.source / " stray.txt").write_text("unassigned edit")
        (self.source / "stray.txt").write_text("assigned edit")
        with self.assertRaisesRegex(handoff.HandoffError, "Unassigned changes"):
            self.publish(files=["stray.txt"])

    def test_wrong_pickup_branch_preserves_current_branch_and_commit(self):
        with self.assertRaises(handoff.HandoffError):
            handoff.pickup(self.dest, "different-branch", "record.md", sync=True)
        self.assertEqual(self.git(self.dest, "symbolic-ref", "--short", "HEAD"), self.branch)
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), self.original)

    def test_untracked_destination_work_blocks_pickup(self):
        self.advance_remote()
        (self.dest / "untracked.txt").write_text("unassigned destination work")
        with self.assertRaisesRegex(handoff.HandoffError, "Local changes exist"):
            handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), self.original)
        self.assertEqual((self.dest / "untracked.txt").read_text(), "unassigned destination work")

    def test_missing_named_record_does_not_fall_back_to_project_context(self):
        (self.dest / "CONTEXT.md").write_text("Run the general project readiness check.\n")
        before = self.commit(self.dest, "legacy project context")
        with self.assertRaises(handoff.HandoffError):
            handoff.pickup(self.dest, self.branch, "missing-handoff.md")
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), before)
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")

    def test_empty_named_record_is_not_a_successful_pickup(self):
        (self.dest / "record.md").write_text(" \n\t\n")
        before = self.commit(self.dest, "blank handoff")
        with self.assertRaisesRegex(handoff.HandoffError, "record is empty"):
            handoff.pickup(self.dest, self.branch, "record.md")
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), before)

    def test_prepare_preserves_raw_sources_and_nested_section_without_writes(self):
        content = "# Tasks\nintro\n## Now\nCurrent café.\n### Owed\nDo not deploy.\n\n## Later\nNot needed.\n"
        (self.dest / "tasks.md").write_text(content)
        before = self.commit(self.dest, "current tasks")
        result = handoff.prepare(self.dest, self.branch, "record.md", ["result.txt"],
                                 [("tasks.md", "## Now")])
        self.assertEqual(result["status"], "pickup_prepared")
        self.assertFalse(result["synchronized"])
        self.assertEqual(result["sources"][0]["content"], (self.dest / "record.md").read_text())
        self.assertEqual(result["sources"][1]["content"], "original result\n")
        self.assertEqual(result["sources"][2]["content"], "## Now\nCurrent café.\n### Owed\nDo not deploy.\n\n")
        self.assertEqual(result["commit"], before)
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")
        self.assertEqual((self.dest / "tasks.md").read_text(), content)

    def test_prepare_cli_returns_source_labels(self):
        result = subprocess.run(["python3", str(SCRIPT), "--project", str(self.dest), "prepare",
                                 "--branch", self.branch, "--record", "record.md", "--file", "result.txt"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        packet = json.loads(result.stdout)
        self.assertEqual(packet["sources"][1]["file"], "result.txt")
        self.assertEqual(packet["sources"][1]["selection"], "complete file")

    def test_prepare_in_worktree_and_without_sync(self):
        worktree = self.folder / "worktree"
        self.git(self.dest, "worktree", "add", "-q", "-b", "worktree-test", str(worktree))
        self.assertTrue((worktree / ".git").is_file())
        result = handoff.prepare(handoff.root_for(worktree), "worktree-test", "record.md")
        self.assertEqual(result["commit"], self.original)
        self.assertFalse(result["synchronized"])

    def test_prepare_rejects_dirty_tree_wrong_branch_and_missing_extra_source(self):
        for branch, files in (("wrong", []), (self.branch, ["missing.md"]),
                              (self.branch, ["../outside.md"]), (self.branch, [".git/config"])):
            with self.subTest(branch=branch, files=files):
                with self.assertRaises((handoff.HandoffError, ValueError)):
                    handoff.prepare(self.dest, branch, "record.md", files)
        (self.dest / "result.txt").write_text("unsaved")
        with self.assertRaisesRegex(handoff.HandoffError, "Local changes"):
            handoff.prepare(self.dest, self.branch, "record.md")

    def test_prepare_reads_utf8_bytes_and_preserves_crlf_through_pipeline(self):
        content = "# Tasks\r\n## Now\r\nCafé 東京.\r\n### Owed\r\nKeep this.\r\n## Later\r\nStop.\r\n"
        (self.dest / "tasks.md").write_bytes(content.encode("utf-8"))
        self.commit(self.dest, "UTF-8 CRLF memory")
        result = handoff.prepare(self.dest, self.branch, "tasks.md", sections=[("tasks.md", "## Now")])
        self.assertEqual(result["sources"][0]["content"], content)
        self.assertEqual(result["sources"][1]["content"],
                         "## Now\r\nCafé 東京.\r\n### Owed\r\nKeep this.\r\n")

    def test_prepare_rejects_non_utf8_instead_of_replacing_characters(self):
        (self.dest / "record.md").write_bytes(b"invalid \xff memory")
        self.commit(self.dest, "invalid text encoding")
        with self.assertRaises(UnicodeDecodeError):
            handoff.prepare(self.dest, self.branch, "record.md")

    def test_prepare_rejects_ignored_sources_even_with_clean_tree(self):
        (self.dest / ".gitignore").write_text("ignored.md\n")
        self.commit(self.dest, "ignore local memory")
        (self.dest / "ignored.md").write_text("## Now\nNot saved.\n")
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")
        for record, files, sections in (("ignored.md", [], []),
                                        ("record.md", ["ignored.md"], []),
                                        ("record.md", [], [("ignored.md", "## Now")])):
            with self.subTest(record=record, files=files, sections=sections):
                with self.assertRaises(handoff.HandoffError):
                    handoff.prepare(self.dest, self.branch, record, files, sections)

    def test_prepare_rejects_changes_during_source_read(self):
        (self.dest / "tasks.md").write_text("## Now\nOriginal\n")
        self.commit(self.dest, "task section")
        original_section = handoff.named_section

        def change_during_read(content, heading):
            (self.dest / "record.md").write_text("Concurrent edit")
            return original_section(content, heading)

        with patch.object(handoff, "named_section", side_effect=change_during_read):
            with self.assertRaisesRegex(handoff.HandoffError, "Project changed"):
                handoff.prepare(self.dest, self.branch, "record.md", sections=[("tasks.md", "## Now")])
        self.assertEqual((self.dest / "record.md").read_text(), "Concurrent edit")

    def test_prepare_tracked_check_uses_literal_filename(self):
        (self.dest / "oddx.md").write_text("Tracked")
        self.commit(self.dest, "tracked near-match")
        (self.dest / ".gitignore").write_text("odd?.md\n")
        self.commit(self.dest, "ignore wildcard names")
        (self.dest / "odd?.md").write_text("Not saved")
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")
        with self.assertRaises(handoff.HandoffError):
            handoff.prepare(self.dest, self.branch, "record.md", files=["odd?.md"])
        self.git(self.dest, "add", "-f", "--", ":(literal)odd?.md")
        self.commit(self.dest, "explicitly save literal question-mark file")
        result = handoff.prepare(self.dest, self.branch, "record.md", files=["odd?.md"])
        self.assertEqual(result["sources"][1]["content"], "Not saved")

    def test_prepare_rejects_new_commit_during_read_even_when_tree_is_clean(self):
        (self.dest / "tasks.md").write_text("## Now\nOriginal\n")
        self.commit(self.dest, "task section")
        original_section = handoff.named_section

        def commit_during_read(content, heading):
            (self.dest / "record.md").write_text("Newly committed state")
            self.commit(self.dest, "concurrent commit")
            return original_section(content, heading)

        with patch.object(handoff, "named_section", side_effect=commit_during_read):
            with self.assertRaisesRegex(handoff.HandoffError, "Project changed"):
                handoff.prepare(self.dest, self.branch, "record.md", sections=[("tasks.md", "## Now")])
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")


class SectionTests(unittest.TestCase):
    def test_fenced_headings_do_not_start_or_end_sections(self):
        for fence in ("```", "~~~~"):
            text = f"{fence}md\n## Now\nignore\n{fence}\n## Now\nkept\n{fence}\n## Later\n{fence}\n### Child\nalso kept\n## Later\nexcluded\n"
            selected = handoff.named_section(text, "## Now")
            self.assertTrue(selected.startswith("## Now\nkept\n"))
            self.assertIn("### Child\nalso kept", selected)
            self.assertNotIn("excluded", selected)

    def test_missing_duplicate_empty_and_non_atx_selection_fail(self):
        for text, heading in (("## Other\nbody\n", "## Now"),
                              ("## Now\nfirst\n## Now\nsecond\n", "## Now"),
                              ("## Now\n \n## Later\nbody\n", "## Now"),
                              ("Now\n===\nbody\n", "Now")):
            with self.subTest(text=text):
                with self.assertRaises(handoff.HandoffError):
                    handoff.named_section(text, heading)

    def test_section_ends_at_parent_heading_and_preserves_line_endings(self):
        text = "# Top\r\n## Now\r\nexact\r\n### Child\r\nkeep\r\n# Other\r\nnot this\r\n"
        self.assertEqual(handoff.named_section(text, "## Now"),
                         "## Now\r\nexact\r\n### Child\r\nkeep\r\n")

    def test_last_section_runs_to_eof(self):
        self.assertEqual(handoff.named_section("# Top\n## Now\nlast", "## Now"), "## Now\nlast")


if __name__ == "__main__":
    unittest.main()
