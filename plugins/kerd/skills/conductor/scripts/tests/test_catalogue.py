"""catalogue.py picks catalogue, cache, stale cache or shipped profile; all offline.

The catalogue is served from a fixture directory by a local http.server on 127.0.0.1,
so no test touches the network or the real ~/.cache/kerd/catalogue.
"""
import functools
import http.server
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "catalogue.py"
spec = importlib.util.spec_from_file_location("catalogue", SCRIPT)
catalogue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalogue)

NAME = "anthropic/opus-5-5"
SHIPPED = (ROOT.parent / "references" / "guidance" / f"{NAME}.md").resolve()
GUIDANCE = (ROOT.parent / "references" / "guidance").resolve()
PROFILE = (b"---\nprofile:\n  provider: anthropic\n  family: opus-5-5\n"
           b"  applicable_models: [claude-opus-5-5]\n---\n\n# Opus 5.5 catalogue copy\n")
OLD_PROFILE = PROFILE.replace(b"catalogue copy", b"old copy")
DAY = 24 * 60 * 60


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.served = tempfile.TemporaryDirectory()
        handler = functools.partial(QuietHandler, directory=cls.served.name)
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.served.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cache = Path(self.temp.name) / "cache"
        self.env = {"KERD_CATALOGUE_CACHE": str(self.cache), "KERD_CATALOGUE_URL": self.base}
        for stale in Path(self.served.name).rglob("*.md"):
            stale.unlink()

    def serve(self, name, body):
        path = Path(self.served.name) / "guidance" / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)

    def cache_copy(self, name, body, age_days):
        path = self.cache / "guidance" / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        then = time.time() - age_days * DAY
        os.utime(path, (then, then))
        return path.resolve()

    def test_fresh_fetch_reads_the_catalogue_and_caches_it(self):
        self.serve(NAME, PROFILE)
        result = catalogue.resolve(NAME, self.env)
        self.assertEqual(result["source"], "catalogue")
        self.assertIsNone(result["reason"])
        self.assertEqual(Path(result["path"]), (self.cache / "guidance" / f"{NAME}.md").resolve())
        self.assertEqual(Path(result["path"]).read_bytes(), PROFILE)
        self.assertEqual([p.name for p in Path(result["path"]).parent.iterdir()],
                         ["opus-5-5.md"], "no temporary file left beside the cached copy")

    def test_cache_within_seven_days_is_used_without_fetching(self):
        cached = self.cache_copy(NAME, PROFILE, age_days=6.9)
        env = dict(self.env, KERD_CATALOGUE_URL="http://127.0.0.1:9")  # nothing listens there
        result = catalogue.resolve(NAME, env)
        self.assertEqual(result, {"path": str(cached), "source": "cache", "reason": None})

    def test_cache_older_than_seven_days_is_refetched(self):
        self.cache_copy(NAME, OLD_PROFILE, age_days=7.1)
        self.serve(NAME, PROFILE)
        result = catalogue.resolve(NAME, self.env)
        self.assertEqual(result["source"], "catalogue")
        self.assertEqual(Path(result["path"]).read_bytes(), PROFILE)

    def test_404_falls_back_to_shipped_with_a_reason(self):
        result = catalogue.resolve(NAME, self.env)
        self.assertEqual(result["source"], "shipped")
        self.assertEqual(Path(result["path"]), SHIPPED)
        self.assertIn("HTTP 404", result["reason"])
        self.assertIn("shipped with Kerd", result["reason"])

    def test_malformed_bodies_fall_back_to_shipped(self):
        bodies = {
            "empty": b"",
            "heading-only profile": b"# Opus 5.5\n\nprofile:\n  provider: anthropic\n",
            "frontmatter never closed": b"---\nprofile:\n  provider: anthropic\n"
                                        b"  applicable_models: [x]\n",
            "frontmatter without provider": b"---\nprofile:\n  applicable_models: [x]\n---\n",
            "frontmatter without applicable_models": b"---\nprofile:\n  provider: openai\n---\n",
            "not utf-8": b"# heading\n\xff\xfe\n",
            "too large": b"# heading\n" + b"x" * (200 * 1024),
        }
        for label, body in bodies.items():
            with self.subTest(label):
                self.serve(NAME, body)
                result = catalogue.resolve(NAME, self.env)
                self.assertEqual(result["source"], "shipped")
                self.assertEqual(Path(result["path"]), SHIPPED)
                self.assertTrue(result["reason"])
                self.assertFalse((self.cache / "guidance" / f"{NAME}.md").exists(),
                                 "a rejected body is never cached")

    def test_every_shipped_profile_is_accepted_when_served(self):
        """Regression: real profiles open with YAML frontmatter, not a heading."""
        names = sorted(str(p.relative_to(GUIDANCE).with_suffix(""))
                       for p in GUIDANCE.glob("*/*.md"))
        self.assertGreaterEqual(len(names), 10)
        for name in names:
            with self.subTest(name):
                self.serve(name, (GUIDANCE / f"{name}.md").read_bytes())
                result = catalogue.resolve(name, self.env)
                self.assertEqual(result["source"], "catalogue", result["reason"])

    def test_documents_need_a_heading_not_frontmatter(self):
        self.serve("README", b"# Local model guidance\n\ntext\n")
        self.assertEqual(catalogue.resolve("README", self.env)["source"], "catalogue")
        self.serve("model-choice", b"no heading here\n")
        result = catalogue.resolve("model-choice", self.env)
        self.assertEqual(result["source"], "shipped")
        self.assertIn("Markdown heading", result["reason"])

    def test_invalid_cached_profile_is_not_used(self):
        self.cache_copy(NAME, b"# heading-only copy\n", age_days=0)
        self.serve(NAME, PROFILE)
        result = catalogue.resolve(NAME, self.env)
        self.assertEqual(result["source"], "catalogue")
        self.assertEqual(Path(result["path"]).read_bytes(), PROFILE)

    def test_failed_fetch_uses_a_stale_cache_and_says_so(self):
        cached = self.cache_copy(NAME, PROFILE, age_days=12)
        result = catalogue.resolve(NAME, self.env)  # nothing served: 404
        self.assertEqual(result["source"], "stale-cache")
        self.assertEqual(Path(result["path"]), cached)
        self.assertIn("HTTP 404", result["reason"])
        self.assertIn("12 days old", result["reason"])

    def test_unreachable_catalogue_falls_back(self):
        env = dict(self.env, KERD_CATALOGUE_URL="http://127.0.0.1:9")
        result = catalogue.resolve(NAME, env)
        self.assertEqual(result["source"], "shipped")
        self.assertIn("could not be reached", result["reason"])

    def test_offline_env_uses_shipped_without_cache_or_network(self):
        self.serve(NAME, PROFILE)
        self.cache_copy(NAME, PROFILE, age_days=0)
        env = dict(self.env, KERD_CATALOGUE_OFFLINE="1")
        result = catalogue.resolve(NAME, env)
        self.assertEqual(result["source"], "shipped")
        self.assertEqual(Path(result["path"]), SHIPPED)
        self.assertIn("KERD_CATALOGUE_OFFLINE=1", result["reason"])

    def test_missing_everywhere_is_a_named_gap(self):
        with self.assertRaises(catalogue.Gap) as caught:
            catalogue.resolve("anthropic/no-such-model", self.env)
        self.assertIn("anthropic/no-such-model", str(caught.exception))

    def test_traversal_and_odd_names_are_refused(self):
        for name in ("../etc/passwd", "anthropic/../../x", "a/b/c", "/etc/passwd", ".hidden",
                     "anthropic/.x", "anthropic/", "", "anthropic\\opus", "anthropic/opus 5",
                     "anthropic/opus%2f..", "anthropic/op..us", "anthropic/opus-5-5\n",
                     "anthropic\n/opus-5-5"):
            with self.subTest(name):
                with self.assertRaises(catalogue.Refused):
                    catalogue.resolve(name, self.env)

    def test_accepted_name_shapes(self):
        env = dict(self.env, KERD_CATALOGUE_OFFLINE="1")
        for name in ("anthropic/shared", "openai/gpt-5-6", "model-choice", "README",
                     "anthropic/opus-5-5.md"):
            with self.subTest(name):
                self.assertEqual(catalogue.resolve(name, env)["source"], "shipped")

    def test_script_is_executable_with_a_shebang(self):
        self.assertTrue(os.access(SCRIPT, os.X_OK))
        self.assertEqual(SCRIPT.read_text().splitlines()[0], "#!/usr/bin/env python3")

    def test_cli_prints_json_and_exit_codes(self):
        env = dict(os.environ, **self.env)
        self.serve(NAME, PROFILE)
        run = subprocess.run([sys.executable, str(SCRIPT), "profile", NAME], env=env,
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["source"], "catalogue")

        refused = subprocess.run([sys.executable, str(SCRIPT), "profile", "../x"], env=env,
                                 capture_output=True, text=True, check=False)
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(refused.stdout, "")

        gap = subprocess.run([sys.executable, str(SCRIPT), "profile", "anthropic/no-such-model"],
                             env=env, capture_output=True, text=True, check=False)
        self.assertEqual(gap.returncode, 1)
        self.assertIn("no profile for anthropic/no-such-model", gap.stderr)


if __name__ == "__main__":
    unittest.main()
