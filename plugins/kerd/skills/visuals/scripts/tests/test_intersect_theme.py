"""Guards the opt-in Intersect diagram theme shipped in Visuals.

Anthony, 2026-10-15 08:43: "i want anyone that uses kerd to have it as an option -
'use intersect diagrm theme' or a 'switch to intersect theme'". This checks the
shipped file and the written rule, not whether a model follows it.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILL = REPO / "skills" / "visuals" / "SKILL.md"
THEME = REPO / "skills" / "visuals" / "themes" / "intersect.md"
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")


def flat(text):
    return " ".join(text.split())


class IntersectThemeTests(unittest.TestCase):
    def test_the_theme_is_a_valid_diagram_design_profile(self):
        text = THEME.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("<!-- diagram-design-profile\n"))
        self.assertEqual(text.count("<!-- diagram-design-profile"), 1)
        header = text[: text.index("-->")]
        self.assertIn("\nslug: intersect\n", header)
        self.assertTrue(SLUG.fullmatch("intersect"))
        body = text[text.index("-->") + 4:]
        self.assertTrue(body.startswith("# Style Guide"))

    def test_the_theme_carries_every_semantic_role_and_type_role(self):
        text = THEME.read_text(encoding="utf-8")
        for role in ("paper", "paper-2", "ink", "muted", "soft", "rule", "rule-solid",
                     "accent", "accent-tint", "link"):
            with self.subTest(role=role):
                self.assertRegex(text, rf"\n\| `{re.escape(role)}` \|")
        for role in ("title", "node-name", "sublabel", "eyebrow", "arrow-label", "callout"):
            with self.subTest(role=role):
                self.assertRegex(text, rf"\n\| `{re.escape(role)}` \| [A-Z]")
        self.assertIn("### Semantic roles", text)
        self.assertIn("## Typography", text)
        self.assertIn("@media (prefers-color-scheme: dark)", text)

    def test_the_theme_keeps_the_floor_and_visuals_states(self):
        text = THEME.read_text(encoding="utf-8")
        for role in ("eyebrow", "arrow-label", "sublabel"):
            with self.subTest(role=role):
                self.assertRegex(text, rf"\n\| `{role}` \| IBM Plex Mono \| 13px \|")
        self.assertNotIn("white two-digit", text)
        prose = flat(text)
        self.assertIn("solid `accent` border, heavier, no tinted fill", prose)
        self.assertIn("never overrides Visuals' rules for states", prose)

    def test_the_published_theme_names_no_tv_series(self):
        text = THEME.read_text(encoding="utf-8").lower()
        for word in ("chuck", "tv series", "nbc"):
            with self.subTest(word=word):
                self.assertNotIn(word, text)

    def test_visuals_names_the_requests_scopes_and_switch_back(self):
        prose = flat(SKILL.read_text(encoding="utf-8"))
        for phrase in (
            "“use the intersect diagram theme”, “switch to intersect theme”",
            "“draw this in the intersect theme”",
            "“make intersect my default”",
            "No profile or setting is changed; the next diagram is back to their default.",
            "then ask before writing the project's `.diagram-design` file with exactly `profile: intersect`",
            "never through a project's `.diagram-design` file, which this scope does not touch",
            "never substitute `default` for it.",
            "which you snapshot as `default.md` first by diagram-design's own recovery-snapshot step",
            "copy the profile you named before switching back over the installed style guide",
            "which you offer to save as a named profile before replacing it",
            "Switching back follows the same scope",
            "Never delete the person's other profiles.",
            "Archify keeps its own look",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)

    def test_the_trigger_description_names_the_theme_request(self):
        front = SKILL.read_text(encoding="utf-8").split("---")[1]
        self.assertIn("switch to intersect theme", front)


if __name__ == "__main__":
    unittest.main()
