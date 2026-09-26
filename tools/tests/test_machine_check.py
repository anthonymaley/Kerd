import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import machine_check  # noqa: E402


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


class MachineCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.repo = Path(self.tmp.name) / "repo"
        write(self.repo / ".claude-plugin/plugin.json", {"version": "1.2.3"})
        self.install = self.home / ".claude/plugins/cache/kerd/1.2.3"
        self.install.mkdir(parents=True)
        self.entry = {"version": "1.2.3", "installPath": str(self.install)}
        self.write_installed([self.entry])
        (self.home / "eolas/vault").mkdir(parents=True)
        self.user = {"enabledPlugins": {machine_check.PLUGIN: True},
                     "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "/usr/local/bin/other"}]}]}}
        write(self.home / ".claude/settings.json", self.user)

    def write_installed(self, entries):
        write(self.home / ".claude/plugins/installed_plugins.json", {"plugins": {machine_check.PLUGIN: entries}})

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self):
        return machine_check.check(self.home, self.repo)

    def test_healthy_machine_is_clean_despite_enabled_plugin_line(self):
        self.assertEqual(self.run_check(), ([], []))

    def test_user_global_kerd_hook_fails(self):
        self.user["hooks"]["SessionStart"] = [{"hooks": [{"command": "bash ~/kerd/hooks/session-start.sh"}]}]
        write(self.home / ".claude/settings.json", self.user)
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 1)
        self.assertIn("Hand-wired Kerd hook", failures[0])

    def test_repo_local_kerd_hook_fails(self):
        write(self.home / "development/product/app/.claude/settings.local.json",
              {"hooks": {"Stop": [{"hooks": [{"command": "bash /x/Kerd/hooks/skill-complete.sh"}]}]}})
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 1)
        self.assertIn("settings.local.json", failures[0])

    def test_disabled_plugin_version_mismatch_and_missing_vault_fail(self):
        self.user["enabledPlugins"][machine_check.PLUGIN] = False
        write(self.home / ".claude/settings.json", self.user)
        write(self.repo / ".claude-plugin/plugin.json", {"version": "2.0.0"})
        (self.home / "eolas/vault").rmdir()
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 3)

    def test_leftover_pair_file_is_a_note_not_a_failure(self):
        (self.repo / "kivna").mkdir()
        (self.repo / "kivna/.pair").write_text("on\n")
        failures, notes = self.run_check()
        self.assertEqual(failures, [])
        self.assertIn("kivna/.pair", notes[0])


    def test_project_settings_json_kerd_hook_fails(self):
        write(self.home / "development/product/app/.claude/settings.json",
              {"hooks": {"Stop": [{"hooks": [{"command": "bash /x/kerd/hooks/x.sh"}]}]}})
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 1)
        self.assertIn("settings.json", failures[0])

    def test_prompt_hook_mentioning_kerd_fails(self):
        self.user["hooks"]["Stop"] = [{"hooks": [{"type": "prompt", "prompt": "Run Kerd's closeout"}]}]
        write(self.home / ".claude/settings.json", self.user)
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 1)

    def test_missing_install_directory_fails(self):
        self.install.rmdir()
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 1)
        self.assertIn("install directory is missing", failures[0])

    def test_blank_or_absent_install_path_fails(self):
        for entry in ({"version": "1.2.3", "installPath": ""}, {"version": "1.2.3"}):
            self.write_installed([entry])
            failures, _ = self.run_check()
            self.assertEqual(len(failures), 1)
            self.assertIn("install directory is missing", failures[0])

    def test_mixed_installed_versions_fail(self):
        self.write_installed([self.entry, {"version": "1.0.0", "installPath": str(self.install)}])
        failures, _ = self.run_check()
        self.assertEqual(len(failures), 1)
        self.assertIn("1.0.0, 1.2.3", failures[0])


if __name__ == "__main__":
    unittest.main()
