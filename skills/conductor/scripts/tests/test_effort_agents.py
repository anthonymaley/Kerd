"""Guards the contract for the five `agents/effort-*.md` routing definitions
(work.md "Design, revision 2" [R4]): name matches the file stem, effort
matches the level, the description invariant holds, no host-unsupported keys
are present, and the body carries the shared brief instruction.

These agents are owned by Conductor; this test reports contract violations,
it never edits them.
"""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
AGENTS_DIR = REPO_ROOT / "agents"
LEVELS = ("low", "medium", "high", "xhigh", "max")
FORBIDDEN_KEYS = ("model", "tools", "hooks", "mcpServers", "permissionMode")


def parse_frontmatter(text):
    """Parse the block between the first two '---' lines as key: value pairs,
    one per line, with no YAML dependency. Returns (fields, body)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Missing opening --- frontmatter delimiter")
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        raise ValueError("Missing closing --- frontmatter delimiter")
    fields = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Frontmatter line is not key: value: {line!r}")
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    body = "\n".join(lines[end + 1:])
    return fields, body


class EffortAgentDefinitionTests(unittest.TestCase):
    def test_exactly_the_five_effort_agent_files_exist(self):
        self.assertTrue(AGENTS_DIR.is_dir(), f"Missing agents/ directory: {AGENTS_DIR}")
        found = sorted(p.name for p in AGENTS_DIR.glob("effort-*.md"))
        expected = sorted(f"effort-{level}.md" for level in LEVELS)
        self.assertEqual(found, expected)

    def test_each_definition_matches_its_contract(self):
        for level in LEVELS:
            path = AGENTS_DIR / f"effort-{level}.md"
            with self.subTest(level=level):
                self.assertTrue(path.is_file(), f"Missing definition: {path}")
                fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))

                self.assertEqual(fields.get("name"), f"effort-{level}",
                                 f"{path}: name must equal the file stem")

                self.assertEqual(fields.get("effort"), level,
                                 f"{path}: effort must equal the stem's level")
                self.assertIn(fields.get("effort"), LEVELS, f"{path}: effort out of allowed set")

                expected_prefix = (
                    f"Internal Kerd routing agent at {level} reasoning effort. "
                    f"Invoke only when Kerd Conductor or Agent explicitly selects "
                    f"kerd:effort-{level}"
                )
                description = fields.get("description", "")
                self.assertTrue(description.startswith(expected_prefix),
                                f"{path}: description does not start with the required "
                                f"invocation-scoping text.\nExpected prefix: {expected_prefix!r}\n"
                                f"Got: {description!r}")

                for key in FORBIDDEN_KEYS:
                    self.assertNotIn(key, fields, f"{path}: must not set {key!r}")

                self.assertTrue(body.strip(), f"{path}: body must be non-empty")
                self.assertIn("Follow the brief", body,
                             f"{path}: body must contain 'Follow the brief'")


if __name__ == "__main__":
    unittest.main()
