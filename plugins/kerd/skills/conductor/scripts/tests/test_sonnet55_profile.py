"""Guards the Sonnet 5.5 profile (0.166.0, 2026-09-29): a new family beside the unchanged
Sonnet 5 profile, because Claude Code's `sonnet` alias moved to Sonnet 5.5 on 2026-09-28
(observed: a kerd:sonnet-high reader ran claude-sonnet-5-5 on 18 of 18 calls). Wording
only: every clause stays pending until a real brief uses it."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
GUIDANCE = REPO_ROOT / "skills/conductor/references/guidance"


def read(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class Sonnet55ProfileTests(unittest.TestCase):
    def setUp(self):
        self.raw = (GUIDANCE / "anthropic/sonnet-5-5.md").read_text(encoding="utf-8")
        self.profile = read(GUIDANCE / "anthropic/sonnet-5-5.md")

    def test_new_family_beside_sonnet_5(self):
        for fragment in ("family: sonnet-5-5", "version: 2026-09-29", "applicable_models: [claude-sonnet-5-5]",
                         "supersedes: null", "last_evaluated: null"):
            self.assertIn(fragment, self.profile)
        self.assertIn("applicable_models: [claude-sonnet-5]", read(GUIDANCE / "anthropic/sonnet-5.md"))

    def test_every_clause_is_pending(self):
        blocks = self.raw.split("\n- id: ")[1:]
        self.assertGreaterEqual(len(blocks), 20)
        for block in blocks:
            with self.subTest(clause=block.split("\n", 1)[0]):
                self.assertIn("evaluation: pending", block)

    def test_sonnet_55_habits_have_clauses(self):
        for clause in ("effort-recalibrated", "carry-work-through", "stop-when-done-and-checked",
                       "no-self-started-review", "real-check-before-done", "no-hold-findings-wording",
                       "no-reasoning-in-reply", "instructions-not-inside-tool-output", "findings-report-everything"):
            self.assertIn("- id: " + clause + "\n", self.raw, clause)
        self.assertIn("Claude Code runs Sonnet 5.5 at medium", self.profile)

    def test_model_table_and_alias_note(self):
        guide = read(GUIDANCE / "model-choice.md")
        self.assertIn("| Claude Sonnet 5.5 · `claude-sonnet-5-5` |", guide)
        self.assertIn("do not credit Sonnet 5.5 results to it, or its results to 5.5", guide)
        self.assertIn("When the main conversation itself runs a Sonnet, a subagent asking for `sonnet` gets that exact model", guide)
        self.assertIn("report the observed model from `job_evidence.py`, never the alias", guide)
        self.assertNotIn("Haiku 5.5", guide)
        journey = read(REPO_ROOT / "skills/conductor/references/journey.md")
        self.assertIn("| Check transport mutations | An agent | Sonnet (5.5 on the Anthropic API) | medium | Preparing |", journey)
        self.assertIn("the report names the observed model from `job_evidence.py`, never the alias", journey)

    def test_sonnet_agents_carry_the_two_habit_lines(self):
        for effort in ("low", "medium", "high", "xhigh", "max"):
            body = read(REPO_ROOT / "agents" / f"sonnet-{effort}.md")
            with self.subTest(effort=effort):
                self.assertIn("When the work the brief asks for is done and checked, stop and report.", body)
                self.assertIn("Start no review rounds and launch no subagents of your own unless the brief asks for them.", body)


if __name__ == "__main__":
    unittest.main()
