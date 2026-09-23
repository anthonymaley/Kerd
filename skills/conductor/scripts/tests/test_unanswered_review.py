"""Guards the wording that replaces a recommended waiver with a fresh reviewer when
an established partner leaves a review unanswered (0.149.0, from 3of3 on
2026-09-19). Wording only: whether a session follows it shows in real use."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]


def normalize(text):
    return " ".join(text.split())


class UnansweredReviewTests(unittest.TestCase):
    def test_conductor_recommends_a_fresh_reviewer_not_a_waiver(self):
        text = normalize((REPO_ROOT / "skills/conductor/references/orchestration.md").read_text(encoding="utf-8"))
        for fragment in ("When the partner does not answer a review in time.",
                         "a queued request is not a reply",
                         "Start it only on the person's yes",
                         "The partner's queued request stays open and its later findings still count",
                         "does not take over the partner's role or binding",
                         "Never recommend waiving the review",
                         "Ten minutes after a checkpoint or before-push request with no reply",
                         "on the same provider as the partner, or a fresh Claude reviewer on a different model when that provider cannot start",
                         "hold the gate's protected effect (the push, the release) until it clears"):
            self.assertIn(fragment, text)

    def test_agent_points_to_the_rule_and_keeps_never_substitute(self):
        text = normalize((REPO_ROOT / "skills/agent/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("never substitute.", text)
        self.assertIn("recommends a fresh one-off reviewer, started only on the person's yes, not a waiver", text)
        guide = normalize((REPO_ROOT / "skills/agent/references/user-guide.md").read_text(encoding="utf-8"))
        self.assertIn("Kerd never recommends it", guide)


if __name__ == "__main__":
    unittest.main()
