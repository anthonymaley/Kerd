"""The slim plugin branch carries only runtime files, appends only, and refuses what it cannot classify."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.plugin_release import ROOT, commit, git, main, prepare, publish, select, tracked


class PluginReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        env = patch.dict("os.environ", {
            "GIT_AUTHOR_NAME": "Package test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Package test", "GIT_COMMITTER_EMAIL": "test@example.invalid"})
        env.start()
        self.addCleanup(env.stop)
        self.write("skills/switch/SKILL.md", "---\nname: switch\ndescription: Fixture\n---\n")
        self.write("skills/switch/scripts/where_we_are.py", "print('ok')\n")
        self.write("skills/switch/scripts/tests/test_where.py", "# dev only\n")
        self.write("skills/visuals/SKILL.md", "---\nname: visuals\ndescription: Fixture\n---\n")
        self.write("skills/visuals/LICENSE", "Fixture\n")
        self.write("agents/opus-high.md", "fixture\n")
        self.write("hooks/hooks.json", json.dumps({"hooks": {"SessionStart": [{"hooks": [
            {"type": "command", "command": 'bash "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"'}]}]}}))
        self.write("hooks/session-start.sh", "exit 0\n")
        self.write("README.md", "Kerd\n")
        self.write("LICENSE", "Fixture license\n")
        for private in ("CONTEXT.md", "TODO.md", "CHANGELOG.md", "docs/big.png", "evals/case.json",
                        "site/index.html", "kivna/sessions/log.md", "Sensei Input/notes.md",
                        "mods/overtone/.claude-plugin/plugin.json", "tools/release.py"):
            self.write(private, "not for users\n")
        self.version("1.0.0")
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(self.remote)], check=True)
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def version(self, version):
        self.write(".claude-plugin/plugin.json", json.dumps({"name": "kerd", "version": version}))
        self.write(".claude-plugin/marketplace.json", json.dumps(
            {"metadata": {"version": version}, "plugins": [{"name": "kerd", "version": version}]}))
        self.commit(version)

    def commit(self, message):
        git(self.repo, "add", "--all")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", message)

    def files(self, folder):
        return sorted(str(p.relative_to(folder)) for p in folder.rglob("*")
                      if p.is_file() and ".git" not in p.relative_to(folder).parts)

    def build(self, name, **kwargs):
        output = self.root / name
        release, report = prepare(output, repo=self.repo, **kwargs)
        made, parent = commit(output, release, str(self.remote), repo=self.repo)
        return output, release, report, made, parent

    def test_package_holds_runtime_files_only_from_the_commit(self):
        head = git(self.repo, "rev-parse", "HEAD")
        self.write("skills/switch/SKILL.md", "uncommitted change\n")
        self.write("skills/switch/private.md", "untracked note\n")
        before = git(self.repo, "status", "--porcelain")
        output, release, report, made, parent = self.build("package")
        self.assertEqual(release, {"version": "1.0.0", "source_commit": head})
        self.assertEqual(self.files(output), [
            ".claude-plugin/plugin.json", "LICENSE", "README.md", "agents/opus-high.md",
            "hooks/hooks.json", "hooks/session-start.sh", "release.json",
            "skills/switch/SKILL.md", "skills/switch/scripts/where_we_are.py",
            "skills/visuals/LICENSE", "skills/visuals/SKILL.md"])
        self.assertNotIn("uncommitted", (output / "skills/switch/SKILL.md").read_text())
        self.assertEqual(git(self.repo, "status", "--porcelain"), before)
        self.assertIsNone(parent)
        self.assertEqual(git(output, "rev-parse", "refs/heads/plugin"), made)
        self.assertEqual(git(output, "status", "--porcelain"), "")
        self.assertLess(report["bytes"], report["source_bytes"])
        self.assertEqual(report["files"], 11)

    def test_nothing_is_pushed_without_publish(self):
        self.build("package")
        self.assertEqual(git(self.remote, "for-each-ref", "--format=%(refname)"), "refs/heads/main")

    def test_publish_appends_and_refuses_a_changed_same_version(self):
        first, release, _report, first_commit, _ = self.build("first")
        publish(first, release, str(self.remote))
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/plugin"), first_commit)
        self.version("1.0.1")
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        second, release, _report, second_commit, parent = self.build("second")
        self.assertEqual(parent, first_commit)
        publish(second, release, str(self.remote))
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/plugin^"), first_commit)
        self.write("skills/switch/SKILL.md", "changed without a version bump\n")
        self.commit("same version")
        with self.assertRaisesRegex(ValueError, "new release version"):
            self.build("third")
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/plugin"), second_commit)

    def test_rollback_and_lower_version_refuse(self):
        old = git(self.repo, "rev-parse", "HEAD")
        self.version("1.0.1")
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        current, release, _r, made, _p = self.build("current")
        publish(current, release, str(self.remote))
        with self.assertRaisesRegex(ValueError, "not an ancestor"):
            self.build("old", ref=old)
        self.version("0.9.9")
        with self.assertRaisesRegex(ValueError, "go backwards"):
            self.build("lower")
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/plugin"), made)

    def test_source_missing_from_main_cannot_publish(self):
        output, release, _r, _m, _p = self.build("local")
        self.version("1.0.1")
        later, release, _r, _m, _p = self.build("later")
        with self.assertRaisesRegex(ValueError, "not on the remote's main"):
            publish(later, release, str(self.remote))
        self.assertEqual(git(self.remote, "for-each-ref", "--format=%(refname)"), "refs/heads/main")

    def test_unreadable_remote_refuses_rather_than_starting_a_new_branch(self):
        output = self.root / "package"
        release, _report = prepare(output, repo=self.repo)
        with self.assertRaises(ValueError):
            commit(output, release, str(self.root / "no-such-remote.git"), repo=self.repo)

    def test_unknown_file_type_symlink_and_missing_hook_script_refuse(self):
        cases = {
            "new type": lambda: self.write("skills/switch/assets/logo.png", "png"),
            "symlink": lambda: (self.repo / "skills/switch/link.md").symlink_to("SKILL.md"),
            "hook script": lambda: (self.repo / "hooks/session-start.sh").unlink(),
            "skill entry": lambda: (self.repo / "skills/visuals/SKILL.md").unlink(),
        }
        messages = {"new type": "Review new package file type", "symlink": "Linked file",
                    "hook script": "hooks.json runs hooks/session-start.sh",
                    "skill entry": "Missing skill entry"}
        for name, change in cases.items():
            with self.subTest(name):
                base = git(self.repo, "rev-parse", "HEAD")
                change()
                self.commit(name)
                output = self.root / name.replace(" ", "-")
                with self.assertRaisesRegex(ValueError, messages[name]):
                    prepare(output, repo=self.repo)
                self.assertFalse(output.exists())
                git(self.repo, "reset", "-q", "--hard", base)

    def test_mismatched_versions_create_no_artifact(self):
        self.write(".claude-plugin/plugin.json", json.dumps({"name": "kerd", "version": "1.0.2"}))
        self.commit("mismatch")
        output = self.root / "bad"
        with self.assertRaisesRegex(ValueError, "versions disagree"):
            prepare(output, repo=self.repo)
        self.assertFalse(output.exists())

    def test_existing_destination_is_untouched(self):
        output = self.root / "keep"
        output.mkdir()
        (output / "sentinel").write_text("keep")
        with self.assertRaises(FileExistsError):
            prepare(output, repo=self.repo)
        self.assertEqual(list(output.iterdir()), [output / "sentinel"])

    def test_a_refused_build_leaves_no_output_folder(self):
        # Built and committed, then the remote cannot be read: the half-made folder goes.
        output = self.root / "refused"
        with patch("tools.plugin_release.ROOT", self.repo), self.assertRaises(SystemExit) as stopped:
            main([str(output), "--remote", str(self.root / "no-such-remote.git")])
        self.assertEqual(stopped.exception.code, 2)
        self.assertFalse(output.exists())
        kept = self.root / "kept"
        kept.mkdir()
        with patch("tools.plugin_release.ROOT", self.repo), self.assertRaises(SystemExit):
            main([str(kept), "--remote", str(self.remote)])
        self.assertTrue(kept.exists())

    def test_private_records_inside_included_folders_refuse_by_name_or_path(self):
        def entries(*paths):
            return {path: ("100644", "blob", 1) for path in ("skills/switch/SKILL.md", *paths)}
        for path in ("skills/switch/CONTEXT.md", "skills/switch/notes/TODO.md", "agents/MEMORY.md",
                     "hooks/.env", "skills/agent/scripts/.env.json", "skills/tend/CLAUDE.local.md",
                     "skills/tend/CLAUDE.md", "skills/kivna/kivna/sessions/2026-11-14.md",
                     "skills/conductor/docs/work/batch/notes.md", "hooks/sessions/log.md",
                     "skills/switch/.claude/settings.local.json", "skills/kivna/vault.json"):
            with self.subTest(path):
                with self.assertRaisesRegex(ValueError, "Private record in an included folder"):
                    select(entries(path))
        # The Kivna skill's own folder and ordinary names that merely contain the words stay.
        kept = select(entries("skills/kivna/SKILL.md", "skills/conductor/references/work-record.md",
                              "hooks/context-reading.sh", "skills/switch/scripts/claude_roll.py"))
        self.assertEqual(len(kept), 5)
        # Outside the included folders the same names are simply not packaged.
        self.assertEqual(select(entries("CONTEXT.md", "kivna/sessions/x.md", "docs/work/y.md")),
                         ["skills/switch/SKILL.md"])

    def test_an_expected_tip_that_moved_refuses_before_committing(self):
        first, release, _r, first_commit, _p = self.build("first")
        publish(first, release, str(self.remote))
        self.version("1.0.1")
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        for expect, label in (("", "absent"), ("f" * 40, "f" * 12)):
            with self.subTest(expect=label):
                output = self.root / f"expect-{label}"
                release, _report = prepare(output, repo=self.repo)
                with self.assertRaisesRegex(ValueError, "it moved. Not appended"):
                    commit(output, release, str(self.remote), repo=self.repo, expect=expect)
        output = self.root / "expected"
        release, _report = prepare(output, repo=self.repo)
        made, parent = commit(output, release, str(self.remote), repo=self.repo, expect=first_commit)
        self.assertEqual(parent, first_commit)

    def test_a_tip_that_moves_after_the_fetch_makes_the_push_refuse(self):
        first, release, _r, first_commit, _p = self.build("first")
        publish(first, release, str(self.remote))
        self.version("1.0.1")
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        second, release, _r, second_commit, _p = self.build("second")
        publish(second, release, str(self.remote))
        self.version("1.0.2")
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        third, release, _r, third_commit, parent = self.build("third")
        self.assertEqual(parent, second_commit)
        # Between this build's fetch and its push the branch is wound back. A plain
        # push would now fast-forward over the rewind; the lease on the parent refuses.
        subprocess.run(["git", "-C", str(self.remote), "update-ref", "refs/heads/plugin", first_commit], check=True)
        with self.assertRaisesRegex(ValueError, "stale info|rejected"):
            publish(third, release, str(self.remote))
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/plugin"), first_commit)

    def test_this_repository_packages_cleanly(self):
        # The real tree must pass the allowlist: a new file type or a hook script
        # moved outside hooks/ shows up here before it reaches a release.
        head = git(ROOT, "rev-parse", "HEAD")
        chosen = select(tracked(ROOT, head))
        self.assertIn(".claude-plugin/plugin.json", chosen)
        self.assertIn("skills/switch/scripts/where_we_are.py", chosen)
        # Kivna names these two as its source of truth; the rest of docs/ stays out.
        self.assertIn("docs/vault-spec.md", chosen)
        self.assertIn("docs/state-contract.md", chosen)
        allowed_docs = {"docs/vault-spec.md", "docs/state-contract.md"}
        for path in chosen:
            if path in allowed_docs:
                continue
            self.assertFalse(path.startswith(("docs/", "evals/", "site/", "kivna/", "mods/", "tools/")), path)
            self.assertNotRegex(path, r"^skills/[^/]+/scripts/tests/")


if __name__ == "__main__":
    unittest.main()
