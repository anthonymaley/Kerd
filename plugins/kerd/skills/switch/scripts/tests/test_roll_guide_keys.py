"""Guards the Roll guide's saved-place keys and its retirement of a finished worker record
(0.153.3, from the first real Claude Roll runs on 2026-09-24). The key test reads
check_state's source, so renaming a key the guide names fails here; it does not prove the
guide describes every rule check_state enforces."""
from pathlib import Path
import inspect
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "skills/switch/scripts"))
import roll  # noqa: E402


def normalize(text):
    return " ".join(text.split())


class RollGuideKeyTests(unittest.TestCase):
    def test_guide_names_every_key_check_state_reads(self):
        guide = normalize((REPO_ROOT / "skills/switch/references/to-roll.md").read_text(encoding="utf-8"))
        source = inspect.getsource(roll.check_state)
        for key in ("status", "next_action", "memory", "evidence", "failures", "pending_jobs"):
            self.assertIn(f'"{key}"', source)
            self.assertIn(f"`{key}`", guide)

    def test_guide_retires_only_finished_records_through_the_locked_command(self):
        guide = normalize((REPO_ROOT / "skills/switch/references/to-roll.md").read_text(encoding="utf-8"))
        for fragment in ("A finished worker Roll record — `review` or `blocked`, no pending job, owner lock free — is retired",
                         'python3 "$switch_scripts/roll_retire.py" --project "$project"',
                         "It holds the owner lock, re-reads the record and its saved place's `pending_jobs`",
                         "never move it by hand, and never retire a `running`, `uncertain` or `failed` record"):
            self.assertIn(fragment, guide)
        managed = normalize((REPO_ROOT / "skills/conductor/references/managed-conductor.md").read_text(encoding="utf-8"))
        self.assertIn("for a finished worker Roll record, see the retirement paragraph", managed)


if __name__ == "__main__":
    unittest.main()
