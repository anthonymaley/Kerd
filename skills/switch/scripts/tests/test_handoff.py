"""Git handoff behavior in temporary repos with a local bare remote only."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
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

    def publish(self, files=None, push=False, preserve=()):
        return handoff.publish(self.source, self.branch, files or ["record.md", "result.txt"],
                               "Save exact handoff", push=push, preserve=preserve)

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

    def test_acknowledged_untracked_file_is_preserved_and_reported_as_local_only(self):
        (self.source / "local.patch").write_text("kept on this machine\n")
        (self.source / "result.txt").write_text("work to save\n")
        result = self.publish(files=["result.txt"], push=True, preserve=["local.patch"])
        self.assertEqual(result["status"], "saved_to_remote")
        self.assertEqual(result["preserved_local_only"], ["local.patch"])
        self.assertIn("local only", result["note"])
        self.assertEqual(self.git(self.source, "show", "--format=", "--name-only", "HEAD"), "result.txt")
        self.assertEqual((self.source / "local.patch").read_text(), "kept on this machine\n")
        self.assertEqual(self.git(self.source, "ls-files", "--", "local.patch"), "")

    def test_unacknowledged_change_still_blocks_when_another_path_is_preserved(self):
        (self.source / "local.patch").write_text("kept on this machine\n")
        (self.source / "surprise.txt").write_text("nobody decided about this\n")
        (self.source / "result.txt").write_text("work to save\n")
        with self.assertRaisesRegex(handoff.HandoffError, "surprise.txt"):
            self.publish(files=["result.txt"])
        self.assertEqual(self.git(self.source, "diff", "--cached", "--name-only"), "")
        self.assertEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)

    def test_pickup_proceeds_past_preserved_leftovers_without_touching_them(self):
        latest = self.advance_remote()
        (self.dest / "local.patch").write_text("kept at the destination\n")
        result = handoff.pickup(self.dest, self.branch, "record.md", sync=True, preserve=["local.patch"])
        self.assertEqual(result["status"], "record_loaded")
        self.assertEqual(result["commit"], latest)
        self.assertEqual(result["preserved_local_only"], ["local.patch"])
        self.assertEqual((self.dest / "local.patch").read_text(), "kept at the destination\n")

    def test_incoming_revision_carrying_a_preserved_path_stops_the_pickup(self):
        (self.dest / "local.patch").write_text("kept at the destination\n")
        before = self.git(self.dest, "rev-parse", "HEAD")
        (self.source / "local.patch").write_text("a tracked file at the same path\n")
        self.publish(files=["local.patch"], push=True)
        with self.assertRaisesRegex(handoff.HandoffError, "preserved local files"):
            handoff.pickup(self.dest, self.branch, "record.md", sync=True, preserve=["local.patch"])
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), before)
        self.assertEqual((self.dest / "local.patch").read_text(), "kept at the destination\n")

    def test_preserved_path_must_be_an_existing_untracked_file(self):
        for value, message in (("record.md", "tracked work"), ("absent.txt", "does not exist")):
            with self.subTest(value=value):
                (self.source / "result.txt").write_text("work to save\n")
                with self.assertRaisesRegex(handoff.HandoffError, message):
                    self.publish(files=["result.txt"], preserve=[value])
                self.assertEqual(self.git(self.source, "diff", "--cached", "--name-only"), "")
                self.assertEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)

    def test_record_naming_an_already_contained_revision_is_hinted_not_refused(self):
        """A record whose sitting committed after writing it: hinted, never treated as stale."""
        observed = self.git(self.source, "rev-parse", "HEAD")
        (self.source / "record.md").write_text(
            f"Observed HEAD {observed}. Next action: record the boundary.\n")
        self.publish(files=["record.md"], push=True)
        boundary = self.git(self.source, "rev-parse", "HEAD")
        (self.source / "result.txt").write_text("the boundary this record does not know about\n")
        self.publish(files=["result.txt"], push=True)
        result = handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(result["status"], "record_loaded")
        self.assertEqual(result["overtaken_revisions"], [observed])
        self.assertIn("Diagnostic only", result["hint"])
        self.assertNotIn(self.git(self.dest, "rev-parse", "HEAD"), result["overtaken_revisions"])
        self.assertNotEqual(boundary, self.git(self.dest, "rev-parse", "HEAD"))

    def test_foreign_and_current_revisions_are_not_reported_as_overtaken(self):
        """Another project's HEAD is unknown here; this checkout's own revision is not staleness."""
        foreign = "47733d292268f8186c6e0b1e2f6b0e87cdf253da"
        (self.source / "record.md").write_text(f"The other project sits at {foreign}.\n")
        self.publish(files=["record.md"], push=True)
        result = handoff.pickup(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(result["overtaken_revisions"], [])
        self.assertNotIn("hint", result)
        # A record cannot contain the commit that saves it, so the current-HEAD leg is checked
        # directly rather than through a save that would place the ID one commit behind.
        head = self.git(self.dest, "rev-parse", "HEAD")
        self.assertEqual(handoff.overtaken_revisions(self.dest, f"Saved at {head}.", head), [])

    def test_prepared_packet_carries_the_same_reconciliation_signal(self):
        observed = self.git(self.source, "rev-parse", "HEAD")
        (self.source / "record.md").write_text(f"Observed HEAD {observed}.\n")
        self.publish(files=["record.md"], push=True)
        (self.source / "result.txt").write_text("later boundary\n")
        self.publish(files=["result.txt"], push=True)
        packet = handoff.prepare(self.dest, self.branch, "record.md", sync=True)
        self.assertEqual(packet["status"], "pickup_prepared")
        self.assertEqual(packet["overtaken_revisions"], [observed])
        self.assertIn("Diagnostic only", packet["hint"])

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

    def test_measure_sizes_each_source_and_compares_to_the_target(self):
        (self.dest / "tasks.md").write_text("# Tasks\n## Now\n" + "x" * 30 + "\n## Backlog\nlong\n")
        result = handoff.measure(self.dest, "record.md", ["result.txt"], [("tasks.md", "## Now")])
        self.assertEqual(result["status"], "measured")
        self.assertEqual([s["file"] for s in result["sources"]], ["record.md", "result.txt", "tasks.md"])
        self.assertEqual(result["sources"][2]["bytes"], len("## Now\n" + "x" * 30 + "\n"))
        self.assertEqual(result["total_bytes"], sum(s["bytes"] for s in result["sources"]))
        self.assertEqual(result["approx_tokens"], -(-result["total_bytes"] // 4))
        self.assertTrue(result["within_target"])
        self.assertIn("not a tokenizer", result["method"])

    def test_measure_over_target_is_information_not_a_refusal(self):
        (self.dest / "big.md").write_text("y" * 4000 + "\n")
        result = handoff.measure(self.dest, "record.md", ["big.md"], target=500)
        self.assertEqual(result["status"], "measured")
        self.assertFalse(result["within_target"])
        self.assertEqual(result["target_tokens"], 500)

    def test_measured_arguments_replay_the_entire_single_heading_section(self):
        content = "## Now\nCurrent task.\n" + "Older detail must not vanish.\n" * 4000
        (self.dest / "tasks.md").write_text(content)
        before = self.commit(self.dest, "single heading with long tail")
        measured = handoff.measure(self.dest, "record.md", sections=[("tasks.md", "## Now")])
        self.assertFalse(measured["within_target"])
        self.assertEqual(measured["sources"][1]["bytes"], len(content.encode("utf-8")))
        self.assertTrue(measured["sources"][1]["reaches_eof"])
        self.assertNotIn("content", measured["sources"][1])
        result = subprocess.run(["python3", str(SCRIPT), "--project", str(self.dest),
                                 "prepare", "--branch", self.branch, *measured["read_args"]],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        prepared = json.loads(result.stdout)
        self.assertEqual(prepared["sources"][1]["content"], content)
        self.assertEqual(measured["total_bytes"], sum(
            len(source["content"].encode("utf-8")) for source in prepared["sources"]))
        self.assertEqual(self.git(self.dest, "rev-parse", "HEAD"), before)
        self.assertEqual(self.git(self.dest, "status", "--porcelain"), "")

    def test_real_heading_boundary_narrows_both_measurement_and_pickup(self):
        current = "## Now\r\nCurrent café.\r\n### Permission\r\nDo not deploy.\r\n"
        content = current + "## Archive\r\n" + "Historical detail.\r\n" * 6000
        (self.dest / "task notes.md").write_bytes(content.encode("utf-8"))
        self.commit(self.dest, "bounded current work")
        measured = handoff.measure(self.dest, "./record.md", sections=[("task notes.md", "## Now  ")])
        self.assertEqual(measured["read_args"], ["--record", "record.md", "--section", "task notes.md", "## Now"])
        self.assertTrue(measured["within_target"])
        self.assertFalse(measured["sources"][1]["reaches_eof"])
        result = subprocess.run(["python3", str(SCRIPT), "--project", str(self.dest),
                                 "prepare", "--branch", self.branch, *measured["read_args"]],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        sources = json.loads(result.stdout)["sources"]
        self.assertEqual(sources[1]["content"], current)
        self.assertEqual(measured["total_bytes"], sum(len(s["content"].encode("utf-8")) for s in sources))
        self.assertEqual((self.dest / "task notes.md").read_bytes(), content.encode("utf-8"))

    def test_measure_refuses_a_repeated_source_rather_than_counting_it_twice(self):
        with self.assertRaises(handoff.HandoffError):
            handoff.measure(self.dest, "record.md", ["result.txt", "result.txt"])

    def test_measure_refuses_normalized_file_and_heading_aliases(self):
        (self.dest / "tasks.md").write_text("## Now\nCurrent\n## Later\nLater\n")
        with self.assertRaises(handoff.HandoffError):
            handoff.measure(self.dest, "record.md", ["./record.md"])
        with self.assertRaises(handoff.HandoffError):
            handoff.measure(self.dest, "record.md", sections=[
                ("tasks.md", "## Now"), ("./tasks.md", "## Now  ")])
        result = handoff.measure(self.dest, "record.md", sections=[
            ("tasks.md", "## Now"), ("tasks.md", "## Later")])
        self.assertEqual(len(result["sources"]), 3)

    def test_measure_file_section_overlap_is_disclosed_not_refused(self):
        (self.dest / "tasks.md").write_text("## Now\nCurrent\n")
        result = handoff.measure(self.dest, "record.md", ["tasks.md"], [("tasks.md", "## Now")])
        self.assertIn("overlap", result["method"])
        self.assertEqual(result["total_bytes"], sum(s["bytes"] for s in result["sources"]))

    def test_measure_cli_reports_json_and_a_blocked_failure_exits_two(self):
        ok = subprocess.run(["python3", str(SCRIPT), "--project", str(self.dest), "measure",
                             "--record", "record.md", "--file", "result.txt", "--target", "10"],
                            capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        packet = json.loads(ok.stdout)
        self.assertEqual(packet["status"], "measured")
        self.assertFalse(packet["within_target"])
        bad = subprocess.run(["python3", str(SCRIPT), "--project", str(self.dest), "measure",
                              "--record", "record.md", "--file", "missing.md"],
                             capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(json.loads(bad.stderr)["status"], "blocked")

    def test_measure_reads_the_working_tree_and_refuses_an_empty_section(self):
        (self.dest / "tasks.md").write_text("## Now\n\n## Later\nbody\n")  # uncommitted on purpose
        with self.assertRaises(handoff.HandoffError):
            handoff.measure(self.dest, "record.md", [], [("tasks.md", "## Now")])
        with self.assertRaises(ValueError):
            handoff.measure(self.dest, "record.md", target=0)

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


    def boundary_cli(self, *extra):
        result = subprocess.run([sys.executable, str(SCRIPT), "--project", str(self.source), "boundary", *extra],
                                capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout) if result.stdout else result.stderr

    def test_boundary_passes_when_pushed_and_clean(self):
        code, result = self.boundary_cli()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["status"], "boundary_ok")
        self.assertTrue(result["fetched"])
        self.assertIn(f"origin/{self.branch}", result["remote_refs_containing_head"])
        self.assertEqual(result["failures"], [])

    def test_boundary_refuses_an_unpushed_commit_on_a_clean_tree(self):
        (self.source / "result.txt").write_text("local only\n")
        self.commit(self.source, "unpushed")
        self.assertEqual(self.git(self.source, "status", "--porcelain"), "")
        code, result = self.boundary_cli()
        self.assertEqual(code, 1)
        self.assertEqual(result["remote_refs_containing_head"], [])
        self.assertTrue(any("only on this machine" in item for item in result["failures"]))

    def test_boundary_refuses_a_dirty_tree_and_staged_work(self):
        for change in ("tracked", "untracked", "staged"):
            with self.subTest(change=change):
                target = self.source / ("new.txt" if change == "untracked" else "result.txt")
                target.write_text(change + "\n")
                if change == "staged":
                    self.git(self.source, "add", "result.txt")
                code, result = self.boundary_cli()
                self.assertEqual(code, 1)
                self.assertEqual(result["unsaved_paths"], [target.name])
                self.assertTrue(any("not clean" in item for item in result["failures"]))
                self.git(self.source, "reset", "-q", "--hard")
                self.git(self.source, "clean", "-qfd")

    def test_boundary_refuses_when_the_fetch_fails_even_if_cached_refs_contain_head(self):
        self.git(self.source, "remote", "set-url", "origin", str(self.folder / "missing.git"))
        code, result = self.boundary_cli()
        self.assertEqual(code, 1)
        self.assertFalse(result["fetched"])
        self.assertIn(f"origin/{self.branch}", result["remote_refs_containing_head"])
        self.assertTrue(any("fetch failed" in item for item in result["failures"]))

    def test_boundary_with_no_remote_is_refused(self):
        self.git(self.source, "remote", "remove", "origin")
        code, result = self.boundary_cli()
        self.assertEqual(code, 1)
        self.assertFalse(result["fetched"])

    def test_boundary_leaves_preserved_paths_out_and_counts_stashes_without_refusing(self):
        (self.source / "result.txt").write_text("stashed\n")
        self.git(self.source, "stash", "-q")
        (self.source / "scratch.patch").write_text("kept locally\n")
        code, result = self.boundary_cli()
        self.assertEqual(code, 1, "an unacknowledged local file is unsaved work")
        code, result = self.boundary_cli("--preserve", "scratch.patch")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["stashes"], 1)
        self.assertEqual(result["preserved_local_only"], ["scratch.patch"])
        self.assertEqual((self.source / "scratch.patch").read_text(), "kept locally\n")


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

    def test_trailing_spaces_on_a_heading_line_still_match_the_named_heading(self):
        self.assertEqual(handoff.named_section("## Now  \nbody\n", "## Now"), "## Now  \nbody\n")

    def test_last_section_runs_to_eof(self):
        self.assertEqual(handoff.named_section("# Top\n## Now\nlast", "## Now"), "## Now\nlast")


if __name__ == "__main__":
    unittest.main()
