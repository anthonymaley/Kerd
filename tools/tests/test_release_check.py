"""R6 of tools/release_check.py: skill and agent frontmatter parses as YAML,
`description` is non-empty, at most 1,024 characters and carries no '<' or
'>', and a SKILL.md body is at most 500 lines.

Each refusal runs twice: with PyYAML when it is installed, and with the
strict fallback parser the check uses where it is not (CI's interpreter may
lack it), so both paths give the same verdict.
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


def frontmatter(description_line, body="Body.\n", extra=""):
    return f"---\nname: x\n{description_line}\n{extra}---\n{body}"


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

    def problems_both_ways(self):
        """(PyYAML verdict or None when absent, fallback verdict)."""
        with_yaml = release_check._release_frontmatter(self.root) if HAVE_YAML else None
        with mock.patch.dict(sys.modules, {"yaml": None}):
            fallback = release_check._release_frontmatter(self.root)
        return with_yaml, fallback

    def assert_one_problem(self, fragment):
        for label, problems in zip(("PyYAML", "fallback"), self.problems_both_ways()):
            if problems is None:
                continue
            with self.subTest(parser=label):
                self.assertEqual(len(problems), 1, problems)
                self.assertIn(fragment, problems[0])

    def assert_clean(self):
        for label, problems in zip(("PyYAML", "fallback"), self.problems_both_ways()):
            if problems is None:
                continue
            with self.subTest(parser=label):
                self.assertEqual(problems, [])

    def test_quoted_description_with_colon_is_clean(self):
        self.write("skills/a/SKILL.md", frontmatter('description: "Use when: it fits."'))
        self.write("agents/b.md", frontmatter("description: >-\n  Folded: still fine.\n  Two lines."))
        self.assert_clean()

    def test_unquoted_colon_space_is_invalid_yaml(self):
        self.write("skills/a/SKILL.md", frontmatter("description: Use when: it fits."))
        self.assert_one_problem("skills/a/SKILL.md — frontmatter is not valid YAML")

    def test_unquoted_colon_space_in_an_agent_is_invalid_yaml(self):
        self.write("agents/b.md", frontmatter("description: Sets effort: high."))
        self.assert_one_problem("agents/b.md — frontmatter is not valid YAML")

    def test_description_at_the_limit_passes_and_one_over_refuses(self):
        self.write("skills/a/SKILL.md", frontmatter(f'description: "{"a" * 1024}"'))
        self.assert_clean()
        self.write("skills/a/SKILL.md", frontmatter(f'description: "{"a" * 1025}"'))
        self.assert_one_problem("description is 1025 characters (limit 1024)")

    def test_angle_brackets_refuse(self):
        for text in ("names kerd:<model>-<effort>", "before -> after", "a <tag>"):
            with self.subTest(text=text):
                self.write("skills/a/SKILL.md", frontmatter(f'description: "{text}"'))
                self.assert_one_problem("description contains '<' or '>' (no XML tags)")

    def test_missing_or_empty_description_refuses(self):
        for line in ("license: MIT", 'description: ""', "description:"):
            with self.subTest(line=line):
                self.write("skills/a/SKILL.md", frontmatter(line))
                self.assert_one_problem("'description' missing or empty")

    def test_missing_frontmatter_refuses(self):
        self.write("skills/a/SKILL.md", "# No frontmatter\n")
        self.assert_one_problem("skills/a/SKILL.md — no frontmatter")

    def test_skill_body_limit_is_500_lines(self):
        self.write("skills/a/SKILL.md", frontmatter('description: "ok"', body="line\n" * 500))
        self.assert_clean()
        self.write("skills/a/SKILL.md", frontmatter('description: "ok"', body="line\n" * 501))
        self.assert_one_problem("body is 501 lines (limit 500")

    def test_body_limit_applies_to_skills_not_agents(self):
        self.write("agents/b.md", frontmatter('description: "ok"', body="line\n" * 900))
        self.assert_clean()

    def test_audit_includes_the_rule(self):
        self.write("skills/a/SKILL.md", frontmatter("description: Use when: it fits."))
        self.assertTrue(any("not valid YAML" in p for p in release_check.release_audit(self.root)))


class FallbackParserTests(unittest.TestCase):
    def test_reads_the_kerd_shapes(self):
        block = ("name: x\n"
                 'description: "Quoted: with \\"escapes\\" and \\u00e9"\n'
                 "single: 'it''s: fine'\n"
                 "folded: >\n  one\n  two\n\n  three\n"
                 "literal: |-\n  keep\n  lines\n"
                 "license: MIT\n")
        got = release_check._fallback_parse(block)
        self.assertEqual(got["description"], 'Quoted: with "escapes" and \u00e9')
        self.assertEqual(got["single"], "it's: fine")
        self.assertEqual(got["folded"], "one two\nthree\n")
        self.assertEqual(got["literal"], "keep\nlines")
        self.assertEqual(got["license"], "MIT")
        if HAVE_YAML:
            import yaml
            self.assertEqual(got, yaml.safe_load(block))

    def test_refuses_what_it_does_not_read(self):
        for block in ("tools:\n  - Bash\n", "description: one\n  two\n",
                      'description: "never closes\n'):
            with self.subTest(block=block):
                with self.assertRaises(release_check._FallbackUnsupported):
                    release_check._fallback_parse(block)

    def test_refuses_invalid_or_ambiguous_yaml(self):
        for block in ("description: a: b\n", "description: a # b\n", "name: a\nname: b\n",
                      "description: @x\n", 'description: "a" b\n'):
            with self.subTest(block=block):
                with self.assertRaises(ValueError):
                    release_check._fallback_parse(block)

    def test_unsupported_shape_is_reported_as_such(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "agents", "b.md")
            os.makedirs(os.path.dirname(path))
            with open(path, "w", encoding="utf-8") as handle:
                handle.write('---\ndescription: "ok"\ntools:\n  - Bash\n---\nBody.\n')
            with mock.patch.dict(sys.modules, {"yaml": None}):
                problems = release_check._release_frontmatter(root)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("install PyYAML", problems[0])


class LiveTreeTests(unittest.TestCase):
    def test_every_skill_and_agent_in_this_repo_meets_the_limits(self):
        self.assertEqual(release_check._release_frontmatter(str(REPO_ROOT)), [])
        with mock.patch.dict(sys.modules, {"yaml": None}):
            self.assertEqual(release_check._release_frontmatter(str(REPO_ROOT)), [])


if __name__ == "__main__":
    unittest.main()
