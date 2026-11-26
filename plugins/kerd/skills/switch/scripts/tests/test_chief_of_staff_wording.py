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
    text = (ROOT / rel).read_text(encoding="utf-8")
    if rel == IN:
        text += "\n" + (ROOT / "skills/switch/references/in-detail.md").read_text(encoding="utf-8")
    return " ".join(text.split())


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

    def test_compare_and_swap_claim_is_narrowed(self):
        """Review finding 1: no lock, so every guide states the window it cannot close."""
        limit = "between the final check and the replace can still be lost"
        self.assertIn("`cos.py write` is a compare-and-swap at the last moment, not a lock", read(RECORD))
        self.assertIn(limit, read(RECORD))
        self.assertIn("That write is a compare-and-swap at the last moment, not a lock", read(CONTRACT))
        self.assertIn("between that final check and the replace can still be lost", read(CONTRACT))
        self.assertIn("between that final check and the replace can still be lost", read(README))
        cos_doc = read("skills/switch/scripts/cos.py")
        self.assertIn("compare-and-swap at the last moment, not a locked one", cos_doc)
        self.assertIn("between that final check and the replace can still be lost", cos_doc)
        for rel in (CONDUCTOR, RECORD, IN, OUT, CONTRACT, README, "CHANGELOG.md",
                    "skills/switch/scripts/cos.py"):
            text = read(rel).lower()
            for promise in ("atomic compare", "atomically compare", "atomic cas", "fully atomic"):
                self.assertNotIn(promise, text, rel)

    def test_role_needs_the_signal_on(self):
        """Review finding 4: ROLE only when on and is_cos_repo."""
        text = read(IN)
        self.assertIn("`on: true` and `is_cos_repo: true` (this is the chief of staff's own "
                      'project, and the config covers it): put `"role": "chief of staff"`', text)
        self.assertIn("With `on: false` (the chief of staff's repo skipped, opted out or not in "
                      "`projects`) there is no role", text)
        self.assertIn("“chief of staff” when the file covers that project too", read(README))

    def test_out_runs_check_and_mentions_reorders(self):
        text = read(OUT)
        self.assertIn("scripts/cos.py check --project P [--scope S]`", text)
        self.assertIn("The session log mentions a reorder like any other change", text)


class AsksWordingTests(unittest.TestCase):
    """0.203.0 (design: eolas vault kerd/work/cos-mode/work.md): open decisions go in the
    `### Asks` table through `cos.py ask` alone, with a default, and a relayed answer counts
    only where the project's relay rule says so, never for an operation."""

    def test_asks_written_only_through_cos_py_ask(self):
        self.assertIn("put each decision Needs you names in its `### Asks` table through `cos.py ask` "
                      "alone, never by hand, with a default, still asking it once here", read(CONDUCTOR))
        self.assertIn("python3 <switch skill dir>/scripts/cos.py ask --project P [--scope S]", read(RECORD))
        self.assertIn("Never edit the `### Asks` block by hand.", read(RECORD))
        self.assertIn("scripts/cos.py ask --project P [--scope S]`, never by hand", read(OUT))
        self.assertIn("written only through `skills/switch/scripts/cos.py ask`, never by hand", read(CONTRACT))

    def test_default_required_and_ask_once_in_the_helper(self):
        record = read(RECORD)
        self.assertIn("`default` is required: the choice that runs unless the person objects", record)
        self.assertIn("An id already open is refused (exit 2, naming when it was asked)", record)
        self.assertIn("send the restated decision with `--again`", record)
        self.assertIn("record the answer in its task's own record first", record)
        self.assertIn("`cos.py ask --answered ID --project P [--scope S]` (no stdin)", record)

    def test_relay_rule_wording(self):
        conductor, record, in_guide = read(CONDUCTOR), read(RECORD), read(IN)
        self.assertIn("A relayed answer counts only where the signal's `relay` is `decisions`, never for "
                      "a push, release, install or live change.", conductor)
        self.assertIn('`"none"`, unset or any other value gives `this window` (fail closed', record)
        self.assertIn("`operation` is required, `true` or `false`", record)
        self.assertIn("An ask that leaves it out is refused (exit 2), so nothing unclassified is ever "
                      "relayed.", record)
        self.assertIn("an operation row always reads `this window`, and `check` refuses one that says "
                      "`relay ok`.", record)
        self.assertIn("A relayed answer to a `this window` row is a report of what the person said "
                      "elsewhere, not their answer here", record)
        self.assertIn("`relay` (present only when on) is the project's `chief_of_staff_relay` rule", in_guide)
        self.assertIn("so it reads as `none`; put one line in `warnings` saying so.", in_guide)
        readme = read(README)
        self.assertIn('`"chief_of_staff_relay": "decisions"` lets an answer you give the chief of staff '
                      "count for a decision, never for a push, release, install or live change", readme)
        self.assertIn("Kerd's own repo says `\"none\"`.", readme)

    def test_out_keeps_open_decisions_and_does_not_ask_them_again(self):
        out = read(OUT)
        self.assertIn("an open decision the sitting asked that is not in the table goes in through "
                      "`cos.py ask`, with its default", out)
        self.assertIn("Switch Out does not ask it again: the box's next step names it with the time it "
                      "was asked.", out)


if __name__ == "__main__":
    unittest.main()
