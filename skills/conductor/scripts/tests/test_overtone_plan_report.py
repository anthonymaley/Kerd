"""Guards Conductor's report of the score to overtone's `plan` tool (2026-10-08,
approved 17:35): Claude Code gives TaskCreate, TaskUpdate and TodoWrite only to
older models, so on Opus 5.5 and Sonnet 5.5 overtone's plan view stayed empty
unless Conductor reports the score itself. Wording only: whether a session
follows it shows in real use."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]


def normalize(text):
    return " ".join(text.split())


class OvertonePlanReportTests(unittest.TestCase):
    def setUp(self):
        self.text = normalize((REPO_ROOT / "skills/conductor/references/entry.md").read_text(encoding="utf-8"))

    def test_reports_at_the_go_each_acceptance_and_the_finish(self):
        for fragment in ("**The score in overtone.**",
                         "When overtone's `plan` tool (`mcp__overtone__plan`) is available, report the score to it",
                         "At the go, send the title and the tasks in order",
                         "After each accepted task, send it as accepted",
                         "At the end, send `finished: true`"):
            self.assertIn(fragment, self.text)

    def test_subjects_equal_the_agent_description(self):
        self.assertIn("Each task's subject is the exact Agent `description` that task will be dispatched with", self.text)

    def test_never_delays_work_and_absent_tool_is_nothing(self):
        self.assertIn("The report is never a reason to delay work", self.text)
        self.assertIn("Without the tool there is nothing to do", self.text)

    def test_sits_in_the_concert_after_fan_out(self):
        fan_out = self.text.index("In the **concert**, fan out every independent part of the score")
        report = self.text.index("**The score in overtone.**")
        views = self.text.index("Agents and rendered views work the same in both")
        self.assertLess(fan_out, report)
        self.assertLess(report, views)


if __name__ == "__main__":
    unittest.main()
