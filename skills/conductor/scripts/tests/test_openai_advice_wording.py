"""Guards Conductor's OpenAI advice (0.193.2, 2026-11-12). The model-choice page said "GPT-6
has no Terra tier" while the catalogue's 2026-11-03 GPT-6 profile lists GPT-6.1 Sol and
GPT-6.1 Terra; main's shipped profile was still the September one. The page is also read
from the catalogue copy (guidance/ at that branch's root, cached outside the skill), where
links that leave the guidance folder lead nowhere. Wording only."""
from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
GUIDANCE = REPO_ROOT / "skills/conductor/references/guidance"


def read(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class OpenAIAdviceTests(unittest.TestCase):
    def setUp(self):
        self.page = read(GUIDANCE / "model-choice.md")
        self.profile = read(GUIDANCE / "openai/gpt-6.md")

    def test_no_terra_claim_is_gone(self):
        self.assertNotIn("no Terra", self.page)
        self.assertNotIn("there is no GPT-6 Terra —", self.profile)

    def test_rows_match_the_profile_tiers(self):
        for model in ("gpt-6-astra", "gpt-6.1-sol", "gpt-6.1-terra", "gpt-6-luna"):
            with self.subTest(model=model):
                self.assertIn(f"`{model}` |", self.page)
                self.assertIn(model, self.profile)
        self.assertNotIn("`gpt-6-sol` |", self.page)
        self.assertIn("GPT-6 Sol (`gpt-6-sol`) is no longer on the models page", self.page)

    def test_profile_is_the_catalogue_revision_with_its_archive(self):
        for fragment in ("version: 2026-11-03", "supersedes: gpt-6@2026-09",
                         "gpt-6.1-terra", "The earlier statement that there is no GPT-6 Terra no longer holds"):
            self.assertIn(fragment, self.profile)
        self.assertIn("there is no GPT-6 Terra", read(GUIDANCE / "openai/archive/gpt-6-2026-09.md"))

    def test_links_stay_inside_the_guidance_folder(self):
        raw = (GUIDANCE / "model-choice.md").read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#]+)", raw):
            if target.startswith("http"):
                continue
            with self.subTest(target=target):
                self.assertFalse(target.startswith("../"), target)
                self.assertTrue((GUIDANCE / target).exists(), target)

    def test_conductor_guides_named_in_words(self):
        for fragment in ("“Plan independent review from the pairing” in Conductor's orchestration guide",
                         "“Prepare work the chosen model can do well” in Conductor's `references/model-jobs.md`",
                         "“One visible startup view” in Conductor's `references/orchestration.md`"):
            self.assertIn(fragment, self.page)
        for heading in ("### Plan independent review from the pairing", "## One visible startup view"):
            self.assertIn(heading, (REPO_ROOT / "skills/conductor/references/orchestration.md").read_text(encoding="utf-8"))
        self.assertIn("## Prepare work the chosen model can do well",
                      (REPO_ROOT / "skills/conductor/references/model-jobs.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
