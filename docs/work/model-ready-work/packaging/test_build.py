import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

from build import AGENT_LEVELS, PACK, SKILLS, build, build_marketplace, inputs


class PackageTests(unittest.TestCase):
    def test_four_core_skills_and_agent_dependencies_ship_at_current_version(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "kerd"
            build(destination)
            self.assertEqual({p.name for p in (destination / "skills").iterdir()},
                             {"conductor", "switch", "visuals", "agent"})
            self.assertEqual((destination / "skills/agent/scripts/requirements.txt").read_bytes(),
                             (PACK.parents[2] / "skills/agent/scripts/requirements.txt").read_bytes())
            self.assertEqual(sorted(p.name for p in (destination / "agents").iterdir()),
                             sorted(f"effort-{level}.md" for level in AGENT_LEVELS))
            version = json.loads((PACK.parents[2] / ".claude-plugin/plugin.json").read_text())["version"]
            for host in ("claude", "codex"):
                self.assertEqual(json.loads((destination / f".{host}-plugin/plugin.json").read_text())["version"], version)

    def test_packaged_agent_help_runs_outside_repo_without_provider_tools(self):
        import os
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "kerd"
            build(destination)
            script = destination / "skills/agent/scripts/agent.py"
            for command in ([], ["sessions"], ["pair"], ["start"], ["ask"], ["status"], ["wait"]):
                result = subprocess.run([sys.executable, "-B", str(script), *command, "--help"],
                                        cwd=directory, env={**os.environ, "PATH": ""},
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((Path(directory) / ".git").exists())

    def test_packaged_switch_saves_and_restores_a_bounded_reading_set(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "kerd"
            build(destination)
            project = root / "consumer"
            project.mkdir()

            def run(*args):
                result = subprocess.run(args, cwd=project, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout

            run("git", "init", "-q", "-b", "main")
            for key, value in (("user.name", "Package test"), ("user.email", "test@example.invalid"),
                               ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
                run("git", "config", key, value)
            args = ["--record", "work.md", "--section", "TODO.md", "## Now"]
            # The reusable selection is written before measurement, not replaced
            # with a broader prose selection when the handoff is saved.
            (project / "work.md").write_text("Next: review the draft. No publication.\nread_args: " + json.dumps(args) + "\n")
            (project / "TODO.md").write_text("## Now\nReview the draft.\n## Archive\n" + "History stays available.\n" * 5000)
            helper = destination / "skills/switch/scripts/handoff.py"
            prefix = [sys.executable, "-B", str(helper), "--project", str(project)]
            measured = json.loads(run(*prefix, "measure", *args))
            saved = json.loads(run(*prefix, "save", "--branch", "main", "--file", "work.md",
                                   "--file", "TODO.md", "--message", "Save bounded pickup"))
            self.assertEqual(saved["status"], "saved_locally")
            # A separate process restores the saved source, not the original
            # Python objects or an already-loaded reader's interpretation.
            pickup = json.loads(run(*prefix, "prepare", "--branch", "main", *measured["read_args"]))
            self.assertEqual(pickup["commit"], saved["commit"])
            self.assertEqual(pickup["sources"][1]["content"], "## Now\nReview the draft.\n")
            self.assertIn("No publication.", pickup["sources"][0]["content"])
            self.assertEqual(measured["total_bytes"], sum(len(s["content"].encode()) for s in pickup["sources"]))
            self.assertIn("History stays available.", (project / "TODO.md").read_text())
            self.assertEqual(run("git", "status", "--porcelain"), "")

    def test_relocated_copy_is_exact_and_self_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "a different place" / "kerd"
            count, size = build(destination)
            selected = inputs(PACK)
            self.assertEqual(count, len(selected))
            self.assertEqual(size, sum((destination / p).stat().st_size for p in selected))
            self.assertEqual(sorted(p.name for p in (destination / "skills").iterdir()),
                             sorted(SKILLS))
            self.assertEqual(sorted(p.name for p in (destination / "agents").iterdir()),
                             sorted(f"effort-{level}.md" for level in AGENT_LEVELS))
            for relative, source in selected.items():
                if relative.parts[0] in (".claude-plugin", ".codex-plugin"):
                    expected = json.loads(source.read_text())
                    expected["version"] = json.loads((PACK.parents[2] / ".claude-plugin/plugin.json").read_text())["version"]
                    self.assertEqual(json.loads((destination / relative).read_text()), expected)
                else:
                    self.assertEqual((destination / relative).read_bytes(), source.read_bytes())
            for path in destination.rglob("*.md"):
                for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                    url = urlsplit(link)
                    if url.scheme or not url.path:
                        continue
                    target = (path.parent / unquote(url.path)).resolve()
                    self.assertTrue(target.is_relative_to(destination.resolve()), (path, link))
                    self.assertTrue(target.exists(), (path, link))
            for host in ("codex", "claude"):
                manifest = json.loads((destination / f".{host}-plugin/plugin.json").read_text())
                self.assertEqual(manifest["name"], destination.name)
                self.assertNotIn("hooks", manifest)
                self.assertNotIn("mcpServers", manifest)
            self.assertFalse((destination / "hooks").exists())
            self.assertFalse((destination / "website").exists())
            self.assertFalse((destination / "trials").exists())

    def test_catalog_resolves_only_the_generated_plugin_and_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "catalog"
            build_marketplace(destination)
            path = destination / ".agents/plugins/marketplace.json"
            catalog = json.loads(path.read_text())
            self.assertEqual(catalog["name"], "kerd-core")
            self.assertEqual(len(catalog["plugins"]), 1)
            entry = catalog["plugins"][0]
            plugin = destination / entry["source"]["path"]
            self.assertEqual(json.loads((plugin / ".codex-plugin/plugin.json").read_text())["name"], entry["name"])
            self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
            before = {p.relative_to(destination): p.read_bytes() for p in destination.rglob("*") if p.is_file()}
            with self.assertRaises(FileExistsError):
                build_marketplace(destination)
            self.assertEqual(before, {p.relative_to(destination): p.read_bytes() for p in destination.rglob("*") if p.is_file()})

    def test_existing_destination_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "kerd"
            destination.mkdir()
            sentinel = destination / "keep.txt"
            sentinel.write_text("user material")
            with self.assertRaises(FileExistsError):
                build(destination)
            self.assertEqual(list(destination.iterdir()), [sentinel])
            self.assertEqual(sentinel.read_text(), "user material")

    def test_wrong_name_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "other"
            with self.assertRaises(ValueError):
                build(destination)
            self.assertFalse(destination.exists())

    def test_symlink_destination_is_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "kerd"
            destination.symlink_to(root / "absent", target_is_directory=True)
            with self.assertRaises(FileExistsError):
                build(destination)
            self.assertFalse((root / "absent").exists())

    def test_missing_sources_do_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "kerd"
            with self.assertRaises(ValueError):
                build(destination, pack=root / "missing")
            self.assertFalse(destination.exists())

    def _minimal_pack(self, root, agent_levels):
        """A self-contained fixture repository, not the real checkout, so this
        test is independent of anything else touching the real agents/."""
        repo = root / "fixture-repo"
        for name in SKILLS:
            skill = repo / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"# {name}\n")
        agents = repo / "agents"
        agents.mkdir()
        for level in agent_levels:
            (agents / f"effort-{level}.md").write_text("---\nname: x\neffort: x\n---\nbody\n")
        (repo / ".claude-plugin").mkdir()
        (repo / ".claude-plugin/plugin.json").write_text(json.dumps({"version": "0.0.0-fixture"}))
        (repo / "LICENSE").write_text("license\n")
        pack = repo / "docs" / "work" / "model-ready-work"
        packaging = pack / "packaging"
        packaging.mkdir(parents=True)
        for host in ("claude", "codex"):
            (packaging / f"{host}-plugin.json").write_text(json.dumps({"name": "kerd"}))
        (packaging / "START.md").write_text("start\n")
        return pack

    def test_missing_effort_agent_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pack = self._minimal_pack(root, agent_levels=[l for l in AGENT_LEVELS if l != "max"])
            destination = root / "out" / "kerd"
            with self.assertRaises(ValueError) as cm:
                build(destination, pack=pack)
            self.assertIn("effort-max", str(cm.exception))
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
