"""Guards Kerd's written question form: `> 💬 **The question?**` as the last prose line.

Every skill entry point carries the shared rule, including the clause allowing a
native picker to follow the bubble, and links to Conductor's question surface; the
legacy forms it replaced, and the withdrawn picker ban, do not come back. This checks
written structure and known legacy text, not model behavior or pronoun semantics.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "skills"
JOURNEY = SKILLS / "conductor" / "references" / "journey.md"
ANCHOR = "question-surface-and-host-adaptation"
QUESTION_CONTEXT_RULE = (
    "**Putting a decision to the person:** a consequential question — its answer commits to work, "
    "spends real effort, releases or deletes something, or reverses a ruling — comes after a "
    "decision block: Problem, Facts (with how we know the problem is real and how strong that "
    "evidence is), Known options (or \u201cneeds study\u201d), Recommendation, Why, Cost, What we "
    "lose, Input (who else checked it, or nobody yet). Its bubble is \u201cDo you agree?\u201d or one "
    "genuine question the recommendation depends on, never the proposal restated as its own "
    "yes/no or several operations bundled into one question. A factual question or a small, "
    "easily undone step stays one line — see [the question form]({link})."
)


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
    "💬 **Fix all of these?**",
)


class QuestionFormTests(unittest.TestCase):
    def test_every_skill_entry_point_carries_the_rule_and_link(self):
        entries = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertEqual(len(entries), 8)
        for path in entries:
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("**Asking the person:**", text)
                self.assertIn("`> 💬 **The question?**`", text)
                self.assertIn("journey.md#" + ANCHOR, text)
                relative_journey = (
                    "references/journey.md"
                    if path.parent.name == "conductor"
                    else "../conductor/references/journey.md"
                )
                expected = QUESTION_CONTEXT_RULE.format(
                    link=relative_journey + "#" + ANCHOR
                )
                self.assertEqual(text.count(expected), 1)

    def test_the_linked_section_states_the_decision_block(self):
        """Static wording guard; it does not prove a model follows the form."""
        prose = flat(JOURNEY.read_text(encoding="utf-8"))
        for phrase in (
            "is put as a **decision block** immediately above its bubble",
            "including how we know the problem is real and how strong that evidence is",
            "Options are facts about the terrain, not choices handed over.",
            "Problem, Recommendation, Why, Cost and What we lose are always present",
            "Nothing unrelated intervenes between that block and the bubble",
            "**The bubble never loads the answer.**",
            "It never restates the proposal as its own yes/no",
            "A question that bundles several operations is a proposal restated",
            "it does not need a ceremonial block",
            "the Recommendation and the bubble still carry exactly one proposal",
            "The ordinary Switch In **“Start a Conductor session?”** arrival is exempt from "
            "the decision block",
            "choosing work opens Shape for it only",
            "holds one of two questions: **“Do you agree?”**",
            "After “Do you agree?” the picker carries only “Yes — <the recommendation>” and "
            "the host's free-form route, never the Known options",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)
        labels = ["**Problem:**", "**Facts:**", "**Known options:**", "**Recommendation:**",
                  "**Why:**", "**Cost:**", "**What we lose:**", "**Input:**"]
        positions = [prose.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions), "labels must keep the template's order")

    def test_the_old_capsule_rule_does_not_return(self):
        """The capsule let the bubble restate the proposal as its own yes/no."""
        for path in sorted(SKILLS.rglob("*.md")):
            if "archive" in path.parts:
                continue
            text = flat(path.read_text(encoding="utf-8"))
            for legacy in ("Keeping the decision with the question",
                           "name the concrete action and target in the bubble",
                           "The bubble names the concrete action and target"):
                with self.subTest(file=str(path.relative_to(REPO)), legacy=legacy):
                    self.assertNotIn(flat(legacy), text)

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
        self.assertGreaterEqual(len(entries), 8)
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
        self.assertIn("A native picker may follow the rendered output with exactly two "
                      "options, “Yes — <the recommended work>” and “Something else”", journey)
        self.assertIn("so the renderer's output stays unchanged", journey)
        in_out = flat((SKILLS / "switch" / "references" / "in-out.md").read_text(encoding="utf-8"))
        self.assertIn("follow the rendered output with exactly two options: **“Yes — <the "
                      "recommended work>”**, naming the work it opens, and **“Something else”**, "
                      "which opens Conductor to ask what", in_out)
        self.assertIn("The picker never replaces or precedes the bubble.", in_out)
        # The Yes names the work it opens, so it cannot read as approving an
        # unnamed task's operations; Something else still routes through Conductor.
        for text in (journey, in_out):
            self.assertIn("Yes — <the recommended work>", text)
            self.assertNotIn("Not now", text)

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
