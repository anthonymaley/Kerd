"""Guards the reviewer-brief wording agreed on 2026-11-13 (weekly review #2).

A review brief names the problems that hid past one round this week: an old claim
left elsewhere in the file set, unsupported absolutes, checks that fail open or run
before the read they guard; after two Holds of one kind, the next brief widens to
that kind across the files the change touches. Wording only: whether reviews take fewer rounds shows in real use.

The section parser guards against accidental removal or rewording, not adversarial
markup. It fails closed on code fences, HTML comments and block-level HTML tags,
Setext headings and indented lines. Known limits, accepted 2026-11-13 after six
review rounds: HTML processing instructions, declarations and CDATA blocks are not
refused; a phrase wrapped in inline code still matches; str.splitlines() treats
Unicode line separators (U+2028 and others) as line breaks.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
REFS = REPO / "skills" / "conductor" / "references"
EXECUTION = REFS / "execution.md"
ORCHESTRATION = REFS / "orchestration.md"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?(?:[ \t]+#+)?[ \t]*$")
# Forms the guides do not use and this parser does not read. Meeting one fails
# the test rather than risking a section boundary, or a match, inside it.
UNREAD = (
    ("a code fence", re.compile(r"^ {0,3}(`{3,}|~{3,})")),
    ("an HTML comment", re.compile(r"<!--")),
    ("a Setext underline", re.compile(r"^ {0,3}(=+|-{2,})[ \t]*$")),
    ("an indented line (possible code block)", re.compile(r"^(?: {4,}| {0,3}\t)")),
    ("a raw HTML block", re.compile(
        r"^ {0,3}</?(?:address|article|aside|blockquote|body|center|details|dialog|dd|div|dl|dt|"
        r"fieldset|figcaption|figure|footer|form|h[1-6]|header|hr|html|iframe|li|main|menu|nav|ol|p|"
        r"pre|script|section|style|summary|table|tbody|td|textarea|tfoot|th|thead|tr|ul)(?:[\s/>]|$)",
        re.I)),
)


def headings(text):
    """(line index, level, title) for every ATX heading; ValueError on a form not read."""
    found = []
    for index, line in enumerate(text.splitlines()):
        for name, pattern in UNREAD:
            if pattern.search(line):
                raise ValueError(f"line {index + 1} holds {name}; this parser does not read it")
        match = HEADING.match(line)
        if match:
            found.append((index, len(match.group(1)), (match.group(2) or "").strip()))
    return found


def section(text, heading):
    """The heading's section, up to the next heading of the same or a higher level.

    The heading must appear exactly once, and the text must hold none of the forms
    in UNREAD, or ValueError is raised: a renamed, missing or duplicated section,
    or text this parser cannot read, fails the test."""
    level = len(heading) - len(heading.lstrip("#"))
    title = heading.lstrip("#").strip()
    all_headings = headings(text)
    targets = [h for h in all_headings if h[1] == level and h[2] == title]
    if len(targets) != 1:
        raise ValueError(f"heading {heading!r} found {len(targets)} times")
    first = targets[0][0]
    later = [h[0] for h in all_headings if h[0] > first and h[1] <= level]
    lines = text.splitlines(keepends=True)
    return "".join(lines[first:later[0]] if later else lines[first:])


class ReviewerBriefTests(unittest.TestCase):
    def test_review_section_names_the_problems(self):
        review = flat(section(EXECUTION.read_text(encoding="utf-8"), "## Review, prove and improve"))
        for phrase in (
            "**Name the problems that hide past one round.** A review brief names these beside the coverage rule.",
            "search every file the change touches, and any file that repeats the changed claim, for the old claim, not only the diff",
            "flag any absolute (“always”, “only”, “never”, a rule drawn from one sighting) the source does not support",
            "of every check, ask whether it fails closed when it cannot read, and whether it runs after the read it guards (check-then-act)",
            "After two Holds that find the same kind of problem, Conductor widens the next brief to that kind across the files the change touches, and says so in the brief, before another round.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, review)

    def test_routing_points_at_the_named_problems(self):
        orchestration = flat(section(
            ORCHESTRATION.read_text(encoding="utf-8"), "### Plan independent review from the pairing"))
        self.assertIn(
            "the diff and the rules that apply, and the problems "
            "[review, prove and improve](execution.md#review-prove-and-improve) asks for by name.",
            orchestration,
        )


class SectionParserTests(unittest.TestCase):
    def test_stops_at_indented_empty_and_tab_headings(self):
        for stop in ("   ## Next", "##", "##\tNext", "# Top"):
            with self.subTest(stop=stop):
                self.assertEqual(section(f"## Review\nkept\n{stop}\nleft out\n", "## Review"), "## Review\nkept\n")

    def test_deeper_headings_stay_inside(self):
        self.assertIn("deeper", section("## Review\n### Sub\ndeeper\n## Next\n", "## Review"))

    def test_forms_not_read_fail_closed(self):
        for text in (
            "```\n## Review\n```\n",
            "## Review\n```python\n## Next\n```\nkept\n",
            "## Review\n```\n```example\n## Next\n```\n",
            "## Review\nkept\nNext\n----\nmoved\n",
            "<!--\n## Review\n-->\n",
            "## Review\n    ## Next\n",
            "## Review\n\n    moved wording\n",
            "## Review\n \t moved wording\n",
            "<div>\n## Review\n</div>\n",
            "## Review\n<details>\nmoved wording\n</details>\n",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                section(text, "## Review")

    def test_missing_renamed_or_duplicated_heading_fails(self):
        for text in ("## Review further\n", "prose ## Review\n", "## Review\n## Review\n", ""):
            with self.subTest(text=text), self.assertRaises(ValueError):
                section(text, "## Review")


if __name__ == "__main__":
    unittest.main()
