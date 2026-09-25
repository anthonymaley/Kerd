"""Guards the Opus 5.5 profile's 2026-09-24 revision (0.152.0): versioned with the prior
profile archived, two clauses loosened to the provider's wording, max_tokens scoped to
API routes, three pending clauses added, and the conducting-session advice. Wording only:
every clause stays pending until a real brief uses it."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
GUIDANCE = REPO_ROOT / "skills/conductor/references/guidance"


def read(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class Opus55ProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = read(GUIDANCE / "anthropic/opus-5-5.md")

    def test_new_version_supersedes_the_archived_one(self):
        self.assertIn("version: 2026-09-24", self.profile)
        self.assertIn("supersedes: opus-5-5@2026-09", self.profile)
        archived = read(GUIDANCE / "anthropic/archive/opus-5-5-2026-09.md")
        self.assertIn("version: 2026-09 ", archived)

    def test_loosened_clauses_match_the_provider(self):
        self.assertIn("Trying other levels, lower as well as higher, is allowed and encouraged", self.profile)
        self.assertIn("re-test whether scaffolding built for opus-5 is still needed before keeping it; don't drop it untested", self.profile)
        self.assertNotIn("drop scaffolding built for opus-5 by default", self.profile)

    def test_max_tokens_is_api_only(self):
        self.assertIn("API routes only.", self.profile)
        self.assertIn("sets no max_tokens, so this clause does not apply there", self.profile)

    def test_new_clauses_are_pending_and_bounded(self):
        text = (GUIDANCE / "anthropic/opus-5-5.md").read_text(encoding="utf-8")
        for clause in ("id: unattended-premature-stop", "id: fan-out-time-budget", "id: explore-before-acting"):
            block = text.split("- " + clause, 1)[1].split("\n- id:", 1)[0]
            self.assertIn("evaluation: pending", block, clause)
        self.assertIn("never an interactive or human-in-the-loop session", self.profile)
        self.assertIn("Kerd builds none of this until a Kerd route shows the failure", self.profile)
        self.assertNotIn("Untested adaptation.", self.profile)

    def test_2026_09_25_evidence_is_recorded_as_short_paired_runs(self):
        """Wording from docs/work/unattended-sweep/evidence/opus-55-clauses.md, proposals 1-4.
        Two runs per variant, short runs only: every clause stays pending."""
        for sentence in (
            "If the job started a background command or subagent that is still running, wait for it and read its output before recording the job done.",
            "Observed 2026-09-25 (4 pairs, two runs per variant, stated budget only, no run past about 3 minutes): 2.2 to 2.6 times faster with the same recall on planted bugs.",
            "The lead did less verification and chose lower-effort foreground subagents. It did not fan out wider.",
            "check quality and which effort the lead chose for its subagents",
            "draws on several sources outside the files it will change (other repos, docs, tickets, mail) that the brief does not all name",
            "0 of 4 runs stopped early, with or without the standing instruction; long unattended runs, where the provider says early stops appear, were not tried.",
            "both runs without the sentence read the unnamed sources before their first edit, as did both runs with it, so its effect there was not shown.",
        ):
            with self.subTest(sentence=sentence[:50]):
                self.assertIn(sentence, self.profile)

    def test_conducting_session_advice_never_changes_the_session(self):
        guide = read(GUIDANCE / "model-choice.md")
        self.assertIn("Kerd recommends Opus 5.5 for the session that conducts, at medium effort by default", guide)
        self.assertIn("Conductor never changes the current session's model or effort itself", guide)


if __name__ == "__main__":
    unittest.main()
