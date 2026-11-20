"""The optional chief of staff (design v2.2, 2026-11-20): guide wording.

Pins the five moments Conductor keeps the `### Queue` table, that a cold start or a
hand pickup has no signal (off), that the table is written only through `cos.py
write` and never by hand, that Kerd never writes `docs/work/queue.md`, and that a
finished task's completion is recorded before its row leaves. This checks presence
of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]

CONDUCTOR = "skills/conductor/SKILL.md"
RECORD = "skills/conductor/references/work-record.md"
IN = "skills/switch/references/in.md"
OUT = "skills/switch/references/out.md"
CONTRACT = "docs/state-contract.md"
README = "README.md"


def read(rel):
    return " ".join((ROOT / rel).read_text(encoding="utf-8").split())


class ChiefOfStaffWordingTests(unittest.TestCase):
    def test_five_moments(self):
        self.assertIn(
            "Conductor keeps it at five moments: when it **adds** a task, **starts** one, "
            "**finishes** one, when one **slips or blocks**, and when it **reorders** tasks.",
            read(RECORD))
        self.assertIn(
            "keep its `### Queue` table at five moments (adds, starts, finishes, slips or "
            "blocks, reorders a task)", read(CONDUCTOR))

    def test_cold_start_and_hand_pickup_are_off(self):
        record = read(RECORD)
        self.assertIn("a cold start (Conductor with no Switch In this sitting) and a hand "
                      "pickup (Switch In done by hand, or from records the caller supplied) "
                      "carry no signal, so the chief of staff is off for that sitting.", record)
        self.assertIn("With the signal off or absent, none of this exists and nothing is "
                      "said about it", record)
        self.assertIn("(never on a cold start or a hand pickup)", read(CONDUCTOR))
        self.assertIn("A hand pickup (Switch In done by hand) or an arrival from records "
                      "the caller supplied runs no helper, so it has no signal: the chief of "
                      "staff is off for that sitting", read(IN))
        self.assertIn("a cold start or a hand pickup included, none of this exists",
                      read(OUT))

    def test_written_only_through_cos_py(self):
        self.assertIn("python3 <switch skill dir>/scripts/cos.py write --project P "
                      "[--scope S]", read(RECORD))
        self.assertIn("Never edit the `### Queue` block by hand: it is written only through "
                      "`cos.py write`", read(RECORD))
        self.assertIn("through `cos.py write` alone, never by hand", read(CONDUCTOR))
        self.assertIn("scripts/cos.py write --project P [--scope S]`, never by hand",
                      read(OUT))
        self.assertIn("It is written only through `skills/switch/scripts/cos.py write`, "
                      "never by hand", read(CONTRACT))

    def test_never_writes_queue_md(self):
        self.assertIn("Conductor never writes it and never reads its contents.", read(RECORD))
        self.assertIn("Out never writes or reads the contents of `docs/work/queue.md`.",
                      read(OUT))
        self.assertIn("Kerd never writes or reads the contents of a hand-kept "
                      "`docs/work/queue.md`.", read(CONTRACT))
        self.assertIn("Kerd never writes it or reads its contents", read(README))
        self.assertIn("it never reads its contents.", read(IN))

    def test_completion_recorded_before_row_removal(self):
        record = read(RECORD)
        fragment = ("Before writing a table without a finished row, record the completion "
                    "in that task's own record")
        self.assertIn(fragment, record)
        self.assertIn("The session log stays Switch Out's.", record)
        self.assertIn("the completion recorded in the task's own record before its row "
                      "leaves", read(CONDUCTOR))

    def test_exit_codes_three_and_five(self):
        record = read(RECORD)
        self.assertIn("Exit 3: the chief of staff was switched off", record)
        self.assertIn("say so once, in one plain line, and stop updating the table", record)
        self.assertIn("re-read `TODO.md` and retry once", record)

    def test_switch_in_role_and_warnings(self):
        text = read(IN)
        self.assertIn('put `"role": "chief of staff"` in the summary JSON', text)
        self.assertIn("never resumes the chief of staff's checks", text)
        self.assertIn("Put one line in `warnings` naming which problem it is", text)
        self.assertIn("the project keeps two lists and should choose one", text)
        self.assertIn("never Kerd's", text)

    def test_out_runs_check_and_mentions_reorders(self):
        text = read(OUT)
        self.assertIn("scripts/cos.py check --project P [--scope S]`", text)
        self.assertIn("The session log mentions a reorder like any other change", text)


if __name__ == "__main__":
    unittest.main()
