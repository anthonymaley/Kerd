"""R6 of tools/release_check.py: skill and agent frontmatter parses as YAML,
`description` is a non-empty string of at most 1,024 characters with no '<'
or '>', and a SKILL.md body is under 500 lines.

Each case runs twice: with PyYAML when it is installed, and with PyYAML
hidden, which is the narrow fallback parser CI uses when its interpreter
lacks PyYAML. The fallback may refuse more than PyYAML (it asks for PyYAML
instead of guessing) but must never pass what PyYAML refuses.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import release_check  # noqa: E402

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

ASK_FOR_PYYAML = "install PyYAML"


def frontmatter(description_line, body="Body.\n"):
    return f"---\nname: x\n{description_line}\n---\n{body}"


class FrontmatterRuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def with_pyyaml(self):
        if not HAVE_YAML:
            return None
        return release_check._release_frontmatter(self.root)

    def without_pyyaml(self):
        with mock.patch.dict(sys.modules, {"yaml": None}):
            return release_check._release_frontmatter(self.root)

    def assert_verdict(self, problems, fragment):
        """fragment None: clean. Otherwise exactly one problem carrying it."""
        if fragment is None:
            self.assertEqual(problems, [])
        else:
            self.assertEqual(len(problems), 1, problems)
            self.assertIn(fragment, problems[0])

    def assert_verdicts(self, pyyaml, fallback):
        """Expected fragment (or None for clean) under each parser."""
        got = self.with_pyyaml()
        if got is not None:
            with self.subTest(parser="PyYAML"):
                self.assert_verdict(got, pyyaml)
        with self.subTest(parser="fallback"):
            self.assert_verdict(self.without_pyyaml(), fallback)

    def assert_both(self, fragment):
        self.assert_verdicts(fragment, fragment)

    # ── the shapes Kerd uses read the same way under both parsers ───────

    def test_plain_and_double_quoted_descriptions_are_clean(self):
        self.write("skills/a/SKILL.md", frontmatter('description: "Use when: it fits \\"well\\"."'))
        self.write("agents/b.md", frontmatter("description: Internal routing agent, high effort."))
        self.assert_both(None)

    def test_unquoted_colon_space_is_invalid_yaml(self):
        self.write("skills/a/SKILL.md", frontmatter("description: Use when: it fits."))
        self.assert_both("skills/a/SKILL.md — frontmatter is not valid YAML")

    def test_unquoted_colon_space_in_an_agent_is_invalid_yaml(self):
        self.write("agents/b.md", frontmatter("description: Sets effort: high."))
        self.assert_both("agents/b.md — frontmatter is not valid YAML")

    def test_description_at_the_limit_passes_and_one_over_refuses(self):
        self.write("skills/a/SKILL.md", frontmatter(f'description: "{"a" * 1024}"'))
        self.assert_both(None)
        self.write("skills/a/SKILL.md", frontmatter(f'description: "{"a" * 1025}"'))
        self.assert_both("description is 1025 characters (limit 1024)")

    def test_angle_brackets_refuse(self):
        for text in ("names kerd:<model>-<effort>", "before -> after", "a <tag>"):
            with self.subTest(text=text):
                self.write("skills/a/SKILL.md", frontmatter(f'description: "{text}"'))
                self.assert_both("description contains '<' or '>' (no XML tags)")

    def test_missing_or_empty_description_refuses(self):
        for line in ("license: MIT", 'description: ""', "description:"):
            with self.subTest(line=line):
                self.write("skills/a/SKILL.md", frontmatter(line))
                self.assert_both("'description' missing or empty")

    def test_missing_frontmatter_refuses(self):
        self.write("skills/a/SKILL.md", "# No frontmatter\n")
        self.assert_both("skills/a/SKILL.md — no frontmatter")

    def test_skill_body_must_be_under_500_lines(self):
        self.write("skills/a/SKILL.md", frontmatter('description: "ok"', body="line\n" * 499))
        self.assert_both(None)
        self.write("skills/a/SKILL.md", frontmatter('description: "ok"', body="line\n" * 500))
        self.assert_both("body is 500 lines (must be under 500")

    def test_body_limit_applies_to_skills_not_agents(self):
        self.write("agents/b.md", frontmatter('description: "ok"', body="line\n" * 900))
        self.assert_both(None)

    def test_audit_includes_the_rule(self):
        self.write("skills/a/SKILL.md", frontmatter("description: Use when: it fits."))
        self.assertTrue(any("not valid YAML" in p for p in release_check.release_audit(self.root)))

    # ── reviewer cases: the fallback asks for PyYAML, never guesses ─────

    def test_trailing_comment_is_valid_yaml_but_the_fallback_asks_for_pyyaml(self):
        self.write("skills/a/SKILL.md", frontmatter("description: Useful work # comment"))
        self.assert_verdicts(None, ASK_FOR_PYYAML)

    def test_non_string_descriptions_refuse_under_both(self):
        for value in ("null", "~", "Null", "true", "yes", "off", "123", "1.5", ".inf",
                      "2026-10-05", "2001-12-14 21:59:43.10 -5"):
            with self.subTest(value=value):
                self.write("skills/a/SKILL.md", frontmatter(f"description: {value}"))
                self.assert_verdicts("'description' missing or empty", ASK_FOR_PYYAML)

    def test_block_scalars_ask_for_pyyaml(self):
        long_text = "a" * 1025
        for line in ("description: |+\n  keep\n\n", "description: >-\n  Folded text.\n  Two lines.",
                     "description: >\n   over\n  under", f"description: >-\n  {long_text}"):
            with self.subTest(line=line[:30]):
                self.write("skills/a/SKILL.md", frontmatter(line))
                self.assertEqual(len(self.without_pyyaml()), 1)
                self.assertIn(ASK_FOR_PYYAML, self.without_pyyaml()[0])
        if HAVE_YAML:
            self.write("skills/a/SKILL.md", frontmatter(f"description: >-\n  {long_text}"))
            self.assert_verdict(self.with_pyyaml(), "description is 1025 characters")

    def test_other_shapes_ask_for_pyyaml(self):
        for line in ("# a comment\ndescription: Fine words here.",
                     "description: 'single quoted words'",
                     "description: [a, b]",
                     "description: {a: b}",
                     "description: \"opens\n  and continues\"",
                     "description: two\n  lines of plain text",
                     "description: &anchor some words",
                     "description: \"text\" # trailing"):
            with self.subTest(line=line[:30]):
                self.write("skills/a/SKILL.md", frontmatter(line))
                problems = self.without_pyyaml()
                self.assertEqual(len(problems), 1, problems)
                self.assertIn(ASK_FOR_PYYAML, problems[0])

    @unittest.skipUnless(HAVE_YAML, "needs PyYAML to compare against")
    def test_the_fallback_never_passes_what_pyyaml_refuses(self):
        lines = ["description: Useful work # comment", "description: null", "description: ~",
                 "description: |+\n  keep\n\n", "description: >\n   over\n  under",
                 f"description: >-\n  {'a' * 1025}", "description: \"a\\qb\"",
                 "description: Use when: it fits.", "description: a:", "description: \"x\" y",
                 "description:\n  nested: map", "description: 'it''s'", "description: [1]",
                 "description: yes", "description: 12", "description: \"\"",
                 f"description: \"{'b' * 1025}\"", "description: \"\\x41 \\u00e9 ok\"",
                 "description: Plain words, fine.", "description: \"a <b>\"",
                 "description: \tleading tab words", "description: two words\t",
                 "description: words\x85more words", "description: \"a\x85b c\"",
                 "description: some\u2028words here"]
        for line in lines:
            with self.subTest(line=line[:40]):
                self.write("skills/a/SKILL.md", frontmatter(line))
                if self.without_pyyaml() == []:
                    self.assertEqual(self.with_pyyaml(), [])


class FallbackParserTests(unittest.TestCase):
    def test_reads_the_kerd_shapes_as_pyyaml_does(self):
        block = ("name: x\n"
                 'description: "Quoted: with \\"escapes\\", \\u00e9 and \\\\ slash"\n'
                 "effort: high\n"
                 "license: MIT\n")
        got = release_check._fallback_parse(block)
        self.assertEqual(got["description"], 'Quoted: with "escapes", é and \\ slash')
        self.assertEqual(got["effort"], "high")
        if HAVE_YAML:
            import yaml
            self.assertEqual(got, yaml.safe_load(block))

    def test_refuses_invalid_yaml(self):
        for block in ("description: a: b\n", "name: a\nname: b\n", 'description: "a\\q"\n'):
            with self.subTest(block=block):
                with self.assertRaises(ValueError):
                    release_check._fallback_parse(block)


class LiveTreeTests(unittest.TestCase):
    def test_every_skill_and_agent_in_this_repo_meets_the_limits(self):
        self.assertEqual(release_check._release_frontmatter(str(REPO_ROOT)), [])
        with mock.patch.dict(sys.modules, {"yaml": None}):
            self.assertEqual(release_check._release_frontmatter(str(REPO_ROOT)), [])


if __name__ == "__main__":
    unittest.main()
