"""Guards Kerd's one question form: `> 💬 **The question?**` at the end of the message.

Every skill entry point carries the shared rule and links to Conductor's question
surface, and the legacy forms it replaced do not come back. This checks presence and
known legacy text, not the meaning of prose.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "skills"
JOURNEY = SKILLS / "conductor" / "references" / "journey.md"
ANCHOR = "question-surface-and-host-adaptation"
LEGACY = (
    "bounded card",
    "plain-text question",
    "answer panel",
    "email-forward blockquote",
    "email-style blockquote",
    "multi-select question control",
    "Fix all? [",
    "> Where is your Obsidian vault?",
)


class QuestionFormTests(unittest.TestCase):
    def test_every_skill_entry_point_carries_the_rule_and_link(self):
        entries = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(entries), 12)
        for path in entries:
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("**Asking the person:**", text)
                self.assertIn("`> 💬 **The question?**`", text)
                self.assertIn("journey.md#" + ANCHOR, text)

    def test_the_linked_section_exists_and_shows_the_form(self):
        text = JOURNEY.read_text(encoding="utf-8")
        headings = {re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-")
                    for h in re.findall(r"^## (.+)$", text, flags=re.M)}
        self.assertIn(ANCHOR, headings)
        self.assertRegex(text, r"(?m)^> 💬 \*\*[^*]+\?\*\*$")
        self.assertIn("no native picker", text)

    def test_bubble_questions_are_never_inside_code_fences(self):
        """A fenced bubble renders as literal Markdown, not a question (e.g. Tend's report)."""
        for path in sorted(SKILLS.rglob("*.md")):
            if "archive" in path.parts:
                continue
            fence = None  # the opening line of the code fence we are inside, if any
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                stripped = line.lstrip()
                if stripped.startswith("```"):
                    fence = None if fence is not None else stripped
                    continue
                # A ```markdown fence is a deliberate example of the rendered form.
                if fence is not None and not fence.startswith("```markdown") and stripped.startswith("> 💬"):
                    with self.subTest(file=str(path.relative_to(REPO)), line=number):
                        self.fail("speech-bubble question inside a non-markdown code fence")

    def test_legacy_question_forms_do_not_return(self):
        for path in sorted(SKILLS.rglob("*.md")):
            if "archive" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for legacy in LEGACY:
                with self.subTest(file=str(path.relative_to(REPO)), legacy=legacy):
                    self.assertNotIn(legacy, text)


if __name__ == "__main__":
    unittest.main()
