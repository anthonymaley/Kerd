"""Generated Codex releases never change the source checkout or include local notes."""
import functools
import http.server
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest

from tools.codex_release import PACKAGING, ROOT, git, prepare, publish


class CodexReleaseTests(unittest.TestCase):
    def test_public_guides_share_the_install_and_update_commands(self):
        for name in ("docs/guide/getting-started.md", "docs/guide/codex-distribution.md",
                     f"{PACKAGING}/START.md"):
            with self.subTest(path=name):
                text = (ROOT / name).read_text()
                self.assertIn("codex plugin marketplace add anthonymaley/Kerd --ref codex", text)
                self.assertIn("codex plugin add kerd@kerd-core", text)
                self.assertIn("codex plugin marketplace upgrade kerd-core && codex plugin add kerd@kerd-core", text)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        # A fixture identity is also scoped to generated repositories, not user config.
        self.author = {"GIT_AUTHOR_NAME": "Package test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
                       "GIT_COMMITTER_NAME": "Package test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
        from unittest.mock import patch
        self.patch = patch.dict("os.environ", self.author)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        for name in ("conductor", "switch", "visuals", "agent", "tend"):
            self.write(f"skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: Fixture\n---\n{name}\n")
        for level in ("low", "medium", "high", "xhigh", "max"):
            self.write(f"agents/effort-{level}.md", "fixture\n")
        self.write("LICENSE", "Fixture license\n")
        self.write("hooks/hooks.json", '{"hooks": {}}\n')
        for name in ("build.py", "START.md", "claude-plugin.json", "codex-plugin.json"):
            self.write(f"{PACKAGING}/{name}", (ROOT / PACKAGING / name).read_text())
        self.version("1.0.0")
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(self.remote)], check=True)
        git(self.repo, "remote", "add", "origin", str(self.remote))
        self.push_main()

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def version(self, version):
        self.write(".claude-plugin/plugin.json", json.dumps({"name": "kerd", "version": version}))
        self.write(".claude-plugin/marketplace.json", json.dumps({"metadata": {"version": version},
                   "plugins": [{"name": "kerd", "version": version}]}))
        git(self.repo, "add", "--all")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", version)
        if getattr(self, "remote", None):
            self.push_main()

    def push_main(self):
        git(self.repo, "push", "-q", "--force", "origin", "HEAD:refs/heads/main")

    def test_prepare_uses_committed_inputs_only_and_keeps_the_checkout(self):
        expected = git(self.repo, "rev-parse", "HEAD")
        self.write("skills/switch/SKILL.md", "uncommitted change\n")
        self.write("skills/switch/private.md", "private untracked note\n")
        before = git(self.repo, "status", "--porcelain")
        output = self.root / "package"
        result = prepare(output, repo=self.repo)
        self.assertEqual(result, {"version": "1.0.0", "source_commit": expected})
        self.assertEqual(git(self.repo, "status", "--porcelain"), before)
        plugin = output / "plugins/kerd"
        self.assertEqual({p.name for p in (plugin / "skills").iterdir()},
                         {"conductor", "switch", "visuals", "agent"})
        self.assertNotIn("uncommitted", (plugin / "skills/switch/SKILL.md").read_text())
        self.assertFalse((plugin / "skills/switch/private.md").exists())
        self.assertFalse((plugin / "hooks").exists())
        self.assertFalse((output / ".git").exists())
        for host in ("codex", "claude"):
            manifest = json.loads((plugin / f".{host}-plugin/plugin.json").read_text())
            self.assertEqual(manifest["version"], "1.0.0")

    def test_existing_destination_is_untouched(self):
        output = self.root / "keep"
        output.mkdir()
        (output / "sentinel").write_text("keep")
        with self.assertRaises(FileExistsError):
            prepare(output, repo=self.repo)
        self.assertEqual(list(output.iterdir()), [output / "sentinel"])

    def test_publish_appends_only_codex_and_refuses_a_changed_same_version(self):
        source_head = git(self.repo, "rev-parse", "HEAD")
        first = self.root / "first"
        release = prepare(first, repo=self.repo)
        first_commit = publish(first, release, repo=self.repo)
        # Publishing adds codex only; the fixture's main is the one it pushed itself.
        self.assertEqual(git(self.remote, "for-each-ref", "--format=%(refname)"),
                         "refs/heads/codex\nrefs/heads/main")
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main"), source_head)
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), source_head)
        self.version("1.0.1")
        second = self.root / "second"
        second_commit = publish(second, prepare(second, repo=self.repo), repo=self.repo)
        self.assertEqual(git(self.remote, "rev-parse", f"{second_commit}^"), first_commit)
        self.write("skills/switch/SKILL.md", "changed without version bump")
        self.version("1.0.1")
        third = self.root / "third"
        with self.assertRaisesRegex(ValueError, "new release version"):
            publish(third, prepare(third, repo=self.repo), repo=self.repo)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/codex"), second_commit)

    def test_a_commit_missing_from_main_cannot_publish(self):
        first = self.root / "first"
        current = publish(first, prepare(first, repo=self.repo), repo=self.repo)
        self.write("skills/switch/SKILL.md", "local only")
        self.write(".claude-plugin/plugin.json", json.dumps({"name": "kerd", "version": "1.0.1"}))
        self.write(".claude-plugin/marketplace.json", json.dumps({"metadata": {"version": "1.0.1"},
                   "plugins": [{"name": "kerd", "version": "1.0.1"}]}))
        git(self.repo, "add", "--all")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", "local only")
        local = self.root / "local"
        with self.assertRaisesRegex(ValueError, "not on origin's main"):
            publish(local, prepare(local, repo=self.repo), repo=self.repo)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/codex"), current)
        self.push_main()
        pushed = self.root / "pushed"
        self.assertNotEqual(publish(pushed, prepare(pushed, repo=self.repo), repo=self.repo), current)

    def test_rollback_cannot_publish(self):
        old = git(self.repo, "rev-parse", "HEAD")
        self.version("1.0.1")
        first = self.root / "first"
        current = publish(first, prepare(first, repo=self.repo), repo=self.repo)
        old_package = self.root / "old"
        with self.assertRaisesRegex(ValueError, "not an ancestor"):
            publish(old_package, prepare(old_package, ref=old, repo=self.repo), repo=self.repo)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/codex"), current)

    def test_descendant_cannot_publish_a_lower_version(self):
        first = self.root / "first"
        current = publish(first, prepare(first, repo=self.repo), repo=self.repo)
        self.version("0.9.9")
        older = self.root / "older-version"
        with self.assertRaisesRegex(ValueError, "go backwards"):
            publish(older, prepare(older, repo=self.repo), repo=self.repo)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/codex"), current)

    def test_mismatched_release_versions_create_no_artifact(self):
        self.write(".claude-plugin/plugin.json", json.dumps({"name": "kerd", "version": "1.0.2"}))
        git(self.repo, "add", "--all")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", "mismatch")
        output = self.root / "bad"
        with self.assertRaisesRegex(ValueError, "versions disagree"):
            prepare(output, repo=self.repo)
        self.assertFalse(output.exists())

    @unittest.skipUnless(os.environ.get("KERD_TEST_CODEX_PLUGIN_CLI"),
                         "opt-in installed Codex CLI test; isolated config and loopback Git server")
    def test_codex_installs_and_updates_from_a_git_marketplace(self):
        first = self.root / "first"
        publish(first, prepare(first, repo=self.repo), repo=self.repo)
        git(self.remote, "update-server-info")

        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
                    functools.partial(QuietHandler, directory=str(self.root)))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        test_home = self.root / "isolated-codex"
        test_home.mkdir()
        env = {**os.environ, "CODEX_HOME": str(test_home)}
        env.pop("CODEX_THREAD_ID", None)

        def codex(*args):
            result = subprocess.run(["codex", "plugin", *args, "--json"], env=env,
                                    cwd=self.root, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            return json.loads(result.stdout)

        source = f"http://127.0.0.1:{server.server_port}/remote.git"
        codex("marketplace", "add", source, "--ref", "codex")
        installed = codex("add", "kerd@kerd-core")
        self.assertEqual(installed["version"], "1.0.0")
        self.version("1.0.1")
        second = self.root / "second"
        publish(second, prepare(second, repo=self.repo), repo=self.repo)
        git(self.remote, "update-server-info")
        codex("marketplace", "upgrade", "kerd-core")
        after_refresh = codex("list", "--marketplace", "kerd-core")["installed"][0]["version"]
        updated = codex("add", "kerd@kerd-core")
        self.assertEqual(updated["version"], "1.0.1")
        entry = codex("list", "--marketplace", "kerd-core")["installed"][0]
        self.assertEqual(entry["version"], "1.0.1")
        self.assertTrue(entry["enabled"])
        cache = Path(updated["installedPath"])
        self.assertTrue(cache.resolve().is_relative_to(test_home.resolve()))
        self.assertEqual({p.name for p in (cache / "skills").iterdir()},
                         {"conductor", "switch", "visuals", "agent"})
        self.assertFalse((cache / "hooks").exists())
        print(f"\nCodex CLI: installed 1.0.0; catalogue refresh read {after_refresh}; "
              "plugin add installed/enabled 1.0.1; four skills, no hooks; real user config untouched.")

    @unittest.skipUnless(os.environ.get("KERD_TEST_CODEX_PLUGIN_CLI"),
                         "opt-in real package installation in a throwaway Codex profile")
    def test_real_committed_release_installs_with_exact_package_bytes(self):
        output = self.root / "real-package"
        release = prepare(output)
        test_home = self.root / "isolated-codex"
        test_home.mkdir()
        env = {**os.environ, "CODEX_HOME": str(test_home)}
        env.pop("CODEX_THREAD_ID", None)

        def codex(*args):
            result = subprocess.run(["codex", "plugin", *args, "--json"], env=env,
                                    cwd=self.root, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            return json.loads(result.stdout)

        codex("marketplace", "add", str(output))
        result = codex("add", "kerd@kerd-core")
        self.assertEqual(result["version"], release["version"])
        cache = Path(result["installedPath"])
        self.assertTrue(cache.resolve().is_relative_to(test_home.resolve()))
        source = output / "plugins/kerd"
        expected = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
        actual = {p.relative_to(cache): p.read_bytes() for p in cache.rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)
        self.assertTrue(codex("list", "--marketplace", "kerd-core")["installed"][0]["enabled"])
        print(f"\nReal Kerd {release['version']}: isolated install enabled; "
              f"{len(actual)} files exactly match the prepared package; no user install changed.")


if __name__ == "__main__":
    unittest.main()
