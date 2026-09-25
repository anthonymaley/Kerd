"""roll_retire.py: retires only a finished worker record, under the owner lock, by moving it."""
from datetime import date
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import roll  # noqa: E402
import roll_retire  # noqa: E402

DAY = date(2026, 9, 24)


class RetireTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        self.local = self.root / ".git/roll"
        self.local.mkdir()
        (self.root / "place.json").write_text(json.dumps({"pending_jobs": []}))

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, **fields):
        data = {"status": "review", "place": "place.json", **fields}
        (self.local / "run.json").write_text(json.dumps(data))

    def test_finished_record_moves_to_dated_file(self):
        self.record()
        target = roll_retire.retire(self.root, "wording", DAY)
        self.assertEqual(target.name, "retired-2026-09-24-wording-run.json")
        self.assertFalse((self.local / "run.json").exists())
        self.assertEqual(json.loads(target.read_text())["status"], "review")

    def test_second_retirement_same_day_gets_a_suffix(self):
        (self.local / "retired-2026-09-24-worker-run.json").write_text("{}")
        self.record(status="blocked")
        self.assertEqual(roll_retire.retire(self.root, today=DAY).name, "retired-2026-09-24-worker-2-run.json")

    def test_unfinished_records_are_refused_and_untouched(self):
        for status in ("running", "uncertain", "failed", "paused"):
            self.record(status=status)
            with self.assertRaises(roll.RollError):
                roll_retire.retire(self.root, today=DAY)
            self.assertTrue((self.local / "run.json").exists())

    def test_managed_conductor_record_is_refused(self):
        self.record(kind="conductor")
        with self.assertRaises(roll.RollError):
            roll_retire.retire(self.root, today=DAY)

    def test_pending_jobs_block_retirement(self):
        (self.root / "place.json").write_text(json.dumps({"pending_jobs": [{"id": "x"}]}))
        self.record()
        with self.assertRaises(roll.RollError):
            roll_retire.retire(self.root, today=DAY)
        self.assertTrue((self.local / "run.json").exists())

    def test_held_owner_lock_refuses(self):
        self.record()
        fd = os.open(self.local / "owner.lock", os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(roll.RollError):
                roll_retire.retire(self.root, today=DAY)
        finally:
            os.close(fd)
        self.assertTrue((self.local / "run.json").exists())

    def test_missing_record_is_refused(self):
        with self.assertRaises(roll.RollError):
            roll_retire.retire(self.root, today=DAY)


if __name__ == "__main__":
    unittest.main()
