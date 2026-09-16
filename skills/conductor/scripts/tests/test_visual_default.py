"""Guards Kerd's visual default: a connected proposal arrives drawn, not described.

Every skill entry point carries the shared showing rule — the countable threshold that
triggers it, the rendered view, the two required tools, the ban on hand-rolled ASCII
and on an offer question, and the proportional control with its "easy to describe"
escape hatch closed — and links to Conductor's visuals section. Visuals states the
tools as required. The withdrawn clauses do not come back: the optional-tool wording,
the inline-sketch licence, and the offer question in its rendered bubble form. This
checks presence and known banned text, not the meaning of prose.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "skills"
JOURNEY = SKILLS / "conductor" / "references" / "journey.md"
VISUALS = SKILLS / "visuals" / "SKILL.md"
ANCHOR = "visuals-belong-throughout"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


# Exact withdrawn clauses and concrete rendered forms, never short fragments: a
# fragment cannot tell a prohibition from a permission, which is the defect the
# 0.131.0 picker ban had and which "complementary choices" would have here.
BANNED = (
    # The optional-tool wording the 2026-09-15 "yes required" ruling superseded.
    "Keep diagram-design and Archify as complementary choices",
    # Sat near the top of Conductor, so a model met "optional" before it ever
    # reached the visual guidance. Required use and install authority differ.
    "Optional job/diagram tools",
    "Do not present either extra as required",
    # The inline-sketch licence, retired from both places that carried it: it is
    # the exact permission this release exists to withdraw.
    "A small inline relationship can be enough; use a rendered artifact when "
    "spatial detail warrants it",
    "Use a small inline sketch for a simple relationship",
    # The offer question, banned in the rendered bubble form it would actually be
    # asked in, so a sentence forbidding it cannot trip its own ban.
    "> 💬 **Would you like a diagram?**",
    "> 💬 **Shall I draw",
    "> 💬 **Want a diagram",
    "> 💬 **Shall I diagram",
)


class VisualDefaultTests(unittest.TestCase):
    def test_every_skill_entry_point_carries_the_showing_rule_and_link(self):
        entries = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(entries), 12)
        for path in entries:
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                prose = flat(text)
                self.assertIn("**Showing the person:**", text)
                # The countable threshold. "Substantial" alone is classified away by
                # a model that calls a multi-part proposal small; "two or more
                # connected parts" cannot be argued down the same way.
                self.assertIn(
                    flat(
                        "whenever a proposal carries two or more connected parts, a "
                        "branch, an ownership boundary or a before → after change"
                    ),
                    prose,
                )
                # Each phrase runs past the permission into the bound that constrains
                # it: "carries a rendered view" alone would survive being softened back
                # to an offer, an ASCII sketch, or a once-per-session quota.
                self.assertIn(
                    flat(
                        "the answer carries a saved, rendered view drawn with "
                        "diagram-design or Archify — never hand-rolled ASCII in a "
                        "code fence, never an offer question, no quota"
                    ),
                    prose,
                )
                # The proportional control, with the escape hatch closed: being easy
                # to describe in prose is exactly how a wall of text gets shipped.
                self.assertIn(
                    flat(
                        "only a single action or a factual answer stays text, and "
                        "being easy to describe in words does not make it one"
                    ),
                    prose,
                )
                self.assertIn("journey.md#" + ANCHOR, text)

    def test_the_linked_section_exists_and_states_the_default(self):
        text = JOURNEY.read_text(encoding="utf-8")
        headings = {re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-")
                    for h in re.findall(r"^## (.+)$", text, flags=re.M)}
        self.assertIn(ANCHOR, headings)
        # Exact prose, compared whitespace-normalized so a rewrap is not a failure.
        prose = flat(text)
        for phrase in (
            # The required tools, the ban, the no-offer default and the no-quota bound.
            "render through diagram-design or Archify",
            "Hand-rolled ASCII in a code fence is not a visual",
            "carries a rendered view of the solution itself, without asking first",
            # Not the bare "no quota" fragment: that would survive any future
            # sentence containing those two words while the default was gutted.
            "there is no offer question inviting the person to ask for a diagram, "
            "and no quota",
            "Tiny or factual work staying text is the proportional control",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)

    def test_visuals_states_the_tools_as_required(self):
        self.assertIn("diagram-design and Archify are required",
                      flat(VISUALS.read_text(encoding="utf-8")))

    def test_withdrawn_offer_and_optional_tool_wording_does_not_return(self):
        for path in sorted(SKILLS.rglob("*.md")):
            if "archive" in str(path):
                continue
            text = flat(path.read_text(encoding="utf-8")).lower()
            for banned in BANNED:
                with self.subTest(file=str(path.relative_to(REPO)), banned=banned):
                    self.assertNotIn(flat(banned).lower(), text)


if __name__ == "__main__":
    unittest.main()
