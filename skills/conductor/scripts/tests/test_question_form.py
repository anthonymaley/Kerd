"""Guards Kerd's one question form: `> 💬 **The question?**` as the last prose line.

Every skill entry point carries the shared rule, including the clause allowing a
native picker to follow the bubble, and links to Conductor's question surface; the
legacy forms it replaced, and the withdrawn picker ban, do not come back. This checks
presence and known legacy text, not the meaning of prose.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "skills"
JOURNEY = SKILLS / "conductor" / "references" / "journey.md"
ANCHOR = "question-surface-and-host-adaptation"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


LEGACY = (
    "bounded card",
    "plain-text question",
    "answer panel",
    "email-forward blockquote",
    "email-style blockquote",
    "no native picker or multi-select control replaces the bubble",
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
        # Exact prose, compared whitespace-normalized so a rewrap is not a failure.
        prose = flat(text)
        for phrase in (
            "the last prose line and holds the single question",
            "native single- or multi-select picker may follow it",
            "never replaces or precedes the bubble",
            # The two bounds that stop a picker becoming a menu or widening consent.
            "never narrows a question meant to stay open",
            "never broadens what an approval",
            "always leaves a free-form answer open",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)

    def test_every_skill_entry_point_carries_the_picker_clause(self):
        """The bubble rule alone is not the whole rule: a picker may follow it."""
        entries = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(entries), 12)
        for path in entries:
            with self.subTest(skill=path.parent.name):
                prose = flat(path.read_text(encoding="utf-8"))
                self.assertIn("the last prose line of the message", prose)
                self.assertIn(
                    flat(
                        "where the host offers one, a native picker may follow the "
                        "bubble carrying those same options and always leaving a "
                        "free-form answer open, never replacing or preceding it"
                    ),
                    prose,
                )

    def test_the_arrival_bubble_may_carry_a_picker(self):
        """Switch's arrival is the most-asked Kerd question; its picker allowance
        was withdrawn once by mistake and is guarded in both places that state it."""
        journey = flat(JOURNEY.read_text(encoding="utf-8"))
        # Each phrase runs past the permission into the bound that makes it safe:
        # a permission alone would survive being narrowed back to "only if asked".
        self.assertIn("A native picker may still follow the rendered output, carrying "
                      "that same offer", journey)
        self.assertIn("so the renderer's output stays unchanged", journey)
        in_out = flat((SKILLS / "switch" / "references" / "in-out.md").read_text(encoding="utf-8"))
        self.assertIn("a native picker may follow that rendered output carrying the "
                      "same offer", in_out)
        self.assertIn("as a separate surface, never replacing or preceding the bubble "
                      "and never adding another task to it", in_out)
        # The countermeasure is the visible label, not the claim that one exists:
        # a bare "Yes" is what could read as approving the saved task.
        for text in (journey, in_out):
            self.assertIn("“Yes — open direction-setting”", text)
        self.assertIn("never a bare Yes", in_out)

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
            text = flat(path.read_text(encoding="utf-8"))
            for legacy in LEGACY:
                with self.subTest(file=str(path.relative_to(REPO)), legacy=legacy):
                    self.assertNotIn(flat(legacy), text)


if __name__ == "__main__":
    unittest.main()
