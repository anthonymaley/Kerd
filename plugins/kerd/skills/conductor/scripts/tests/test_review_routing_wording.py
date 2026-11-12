"""Guards the review routing agreed with Anthony on 2026-11-12.

Reviews (checkpoints, before-push, pull requests) go to a fresh, record-briefed Codex
reviewer started through Agent by default; a standing Codex partner is for multi-turn
Codex work or when the person asks for one; the person's own `codex` window only
while they are at it. A recorded cadence still says when reviews happen. Switch In
stops greeting stale bindings and offers, in one Open work line, to retire them,
which Agent does only on the person's yes. The weekly review counts stalls against
fresh-reviewer catches. Wording only: whether a session follows it shows in real use.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
ORCHESTRATION = REPO / "skills" / "conductor" / "references" / "orchestration.md"
WEEKLY = REPO / "skills" / "conductor" / "references" / "weekly-review.md"
AGENT_SKILL = REPO / "skills" / "agent" / "SKILL.md"
USER_GUIDE = REPO / "skills" / "agent" / "references" / "user-guide.md"
SWITCH_IN = REPO / "skills" / "switch" / "references" / "in.md"
SWITCH_SKILL = REPO / "skills" / "switch" / "SKILL.md"


def flat(path):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(path.read_text(encoding="utf-8").split())


class ConductorPlansFreshReviewTests(unittest.TestCase):
    def setUp(self):
        self.text = flat(ORCHESTRATION)

    def test_fresh_record_briefed_reviewer_is_the_default(self):
        for phrase in (
            "**Reviews go to a fresh reviewer by default.**",
            "goes to a fresh, record-briefed reviewer from the other provider, started through Agent (`start --kind worker`, read only)",
            "the sketchbook, the governing decisions, the diff and the rules that apply",
            "Its verdict, and the route it took, are written to the sketchbook.",
            "A standing Codex partner is for multi-turn Codex work",
            "it takes a review only when the person asks for one",
            "uses a Kerd-started Codex partner where Agent can start one and its first ask is delivered",
            "when start or delivery fails, it uses a fresh Codex worker per turn, briefed from the records, and says so",
            "window takes work only while they are at it",
            "A stale or stalled partner is never planned as reviewer by default.",
            "The person's explicit choice stands: a review they send to a named partner goes to that partner.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_cadence_schedules_when_not_who(self):
        self.assertIn("A partner's recorded cadence still says when reviews happen; the route stays fresh unless the person chose that partner as reviewer.", self.text)

    def test_unanswered_rule_applies_to_a_chosen_standing_reviewer(self):
        self.assertIn("This applies when the person chose a standing partner as reviewer.", self.text)

    def test_stalled_partner_is_a_gap_not_a_reviewer(self):
        for phrase in (
            "**A stalled partner is a gap said at Ready, never a silent reroute.**",
            "Ready lists the gap and recommends the fresh reviewer for this work's reviews",
            "A go given on that Ready is their consent for this work's reviews; without it, the review goes to the partner they named and the unanswered-review rule applies.",
            "Never substitute silently.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
        self.assertNotIn("this work's reviews still go to the partner first", self.text)

    def test_contents_line_names_the_default(self):
        self.assertIn("(#plan-independent-review-from-the-pairing): fresh reviewers by default", self.text)


class AgentSaysTheRoutingTests(unittest.TestCase):
    def test_skill_step_three_says_the_routing(self):
        text = flat(AGENT_SKILL)
        for phrase in (
            "a review is the exception, fresh by default (step 3)",
            "Say this routing when offering routes: a review (checkpoint, before-push, pull request) goes by default to a fresh, record-briefed reviewer from the other provider",
            "Codex when Claude builds, Claude when Codex builds, or a different model of the same provider, said as such, when the other can't start",
            "a standing Codex partner is for multi-turn Codex work, or when the person asks for one",
            "when start or delivery fails, use a fresh Codex worker per turn, briefed from the records, and say so",
            "the person's own `codex` window only while they are at it",
            "A review the person sends to a named partner goes to that partner.",
            "is not offered as reviewer by default; if the person names it, say it is stale and recommend a fresh reviewer, never substituting silently",
            "`retire --alias` sets its binding aside, recoverably, only on the person's yes",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_description_keeps_named_partner_and_states_default(self):
        skill = AGENT_SKILL.read_text(encoding="utf-8")
        description = skill.split("---", 2)[1]
        self.assertIn("sends reviews to a fresh, record-briefed reviewer from the other provider by default but never substitutes one for a named partner", description)
        self.assertLessEqual(len(description.split("description:", 1)[1].strip()), 1024)

    def test_user_guide_routes_reviews_and_explains_stale_and_retire(self):
        text = flat(USER_GUIDE)
        for phrase in (
            "Which route Kerd uses, by the work:",
            "goes to a fresh, record-briefed reviewer from the other provider that Kerd starts through Agent, read only",
            "a Codex reviewer when Claude builds, which is the usual case in Claude Code, and a Claude reviewer when Codex builds",
            "**Multi-turn Codex work**",
            "Kerd uses a fresh Codex worker for each turn, briefed from the records, and tells you so",
            "**Your own `codex` window** is used only while you are at it",
            "The cadence says when reviews happen; who reviews is fresh by default",
            "**Stale pairings.**",
            "when it has not replied in 14 days",
            "a contribution request sent to it since its last reply has gone unconfirmed for over a day",
            "`agent.py retire --alias ALIAS`",
            "`kerd-agent/partners-retired/`",
            "Nothing is deleted: moving the file back restores the pairing.",
            "Kerd retires one only when you say yes",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


class SwitchInOffersRetirementTests(unittest.TestCase):
    def test_in_skips_stale_and_offers_one_line(self):
        text = flat(SWITCH_IN)
        for phrase in (
            "It skips stale bindings",
            "even when they are passed explicitly, so no notice goes to a stale partner",
            "returns them in a top-level `stale` list",
            "“<Person>: retire N stale pairings (<aliases or count>), set aside, recoverable”",
            "never repeated and never the recommendation",
            "Retirement runs through Agent (`retire --alias`) only on the person's yes",
            "The arrival's `stale` list never fills `team`",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_switch_skill_must_hold_names_it(self):
        text = flat(SWITCH_SKILL)
        self.assertIn("stale bindings are not greeted, and a non-empty `stale` list becomes one person-owned Open work line offering to retire them, retired only on their yes", text)


class ReviewDefaultPointersTests(unittest.TestCase):
    def test_model_choice_keeps_cross_provider_and_points_at_the_rule(self):
        text = flat(REPO / "skills" / "conductor" / "references" / "guidance" / "model-choice.md")
        self.assertIn("through a fresh, record-briefed reviewer from the other provider", text)
        self.assertIn("(../orchestration.md#plan-independent-review-from-the-pairing)", text)
        self.assertNotIn("the fresh-reviewer fallback are unchanged", text)

    def test_orchestration_and_model_choice_state_the_same_reviewer(self):
        # Review round 2, 2026-11-12: the two guides named different reviewers.
        # Both carry the standing ruling (2026-09-24, 0.151.0) in the same words.
        shared = (
            "a fresh, record-briefed reviewer from the other provider, started through Agent (`start --kind worker`, read only): "
            "a fresh Codex reviewer when Claude builds (the usual case in Claude Code), a fresh Claude reviewer when Codex builds. "
            "When the other provider can't start, it goes to a fresh reviewer on a different model of the same provider, said as such."
        )
        orchestration = flat(ORCHESTRATION)
        model_choice = flat(REPO / "skills" / "conductor" / "references" / "guidance" / "model-choice.md")
        self.assertIn(shared, orchestration)
        self.assertIn(shared, model_choice)
        self.assertNotIn("fresh Claude reviewer on a different model when Codex cannot start", orchestration)

    def test_execution_makes_reviews_the_exception(self):
        text = flat(REPO / "skills" / "conductor" / "references" / "execution.md")
        self.assertIn("reviews are the exception, going to a fresh, record-briefed reviewer by default", text)


class WeeklyReviewCountsStallsTests(unittest.TestCase):
    def test_review_counts_stalls_against_fresh_catches(self):
        text = flat(WEEKLY)
        self.assertIn("reviews that stalled waiting on a standing partner", text)
        self.assertIn("against fresh reviewers that returned, and how many of each caught a real issue", text)


if __name__ == "__main__":
    unittest.main()
