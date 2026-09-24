"""Guards Tend's and Slainte's hook instructions against spelling the plugin-root
placeholder out (0.151.1). Claude Code substitutes that placeholder with the install
path when it loads a plugin skill, and no escape keeps it literal, so an instruction
that means the unexpanded text must describe it instead. Scoped to these two skills:
elsewhere the placeholder is a supported way to locate bundled files. Wording only:
whether a real Tend run then catches a stale settings entry has not been observed."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
PLACEHOLDER = "$" + "{CLAUDE_PLUGIN_ROOT}"
DESCRIBED = "`$` followed by `{CLAUDE_PLUGIN_ROOT}`"


def read(path):
    return " ".join((REPO_ROOT / path).read_text(encoding="utf-8").split())


class LiteralPlaceholderTests(unittest.TestCase):
    def test_tend_and_slainte_never_spell_the_placeholder_out(self):
        for path in ("skills/tend/SKILL.md", "skills/slainte/SKILL.md"):
            self.assertNotIn(PLACEHOLDER, read(path), path)

    def test_tend_still_names_the_unexpanded_form_it_looks_for(self):
        text = read("skills/tend/SKILL.md")
        self.assertIn("starts with the plugin-root variable written out unexpanded (" + DESCRIBED, text)
        self.assertIn("a `/hooks/` path starting with the unexpanded plugin-root variable (" + DESCRIBED + ")", text)

    def test_slainte_still_names_the_hook_script_paths(self):
        self.assertIn("a `/hooks/*.sh` path under the plugin-root variable, " + DESCRIBED,
                      read("skills/slainte/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
