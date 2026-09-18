"""Guards Conductor's step check (gate-reachability, 0.137.0).

Conductor asks the user's own project where a work item stands, through the
command written in its SKILL.md. The fixture runs that exact command, with the
plugin placeholder filled in as Claude Code fills it in skill text, from a
working directory inside Kerd, against temporary repositories that are not
Kerd: one item on the build step and one missing its Scope. Neither answer may
come from Kerd's own tree. The prose checks are presence checks, not proof a
model follows them.
"""
from pathlib import Path
import os
import re
import shlex
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
PLACEHOLDER = "${CLAUDE_PLUGIN_ROOT}"

LEDGER = (
    "## Risk ledger\n\n"
    "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment "
    "| Countermeasure | Treatment evidence | Review trigger |\n"
    "|---|---|---|---|---|---|---|---|---|---|\n"
    "| Checkout double-charges | yes | refunds | low | measured | non-fatal "
    "| countermeasure - permanent | idempotency key | | fires on a new payment path |\n"
)


def flat(text):
    return " ".join(text.split())


def write(root, rel, text):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def foreign_repo(root):
    """A project that is not Kerd: one item on the build step, one before scope."""
    subprocess.run(["git", "init", "-q", root], check=True)
    write(root, "docs/product/checkout.md",
          "---\nroute: new\nstage: handed-off\n---\n\n# Checkout redesign\n\n"
          "## Value\n\nFewer abandoned carts.\n\n" + LEDGER +
          "\n## Scope\n\nRigor level: mvp\n\nThe new checkout page.\n")
    write(root, "docs/design/checkout.md", "# Checkout design\n\nOne page.\n")
    write(root, "docs/gates/2026-01-01-checkout-design.md",
          "---\nroute: new\nstage: designed\n---\n\n## GO\n\nApproved.\n")
    write(root, "docs/plans/2026-01-02-checkout-spec.md",
          "# Checkout — build spec\n\n## Pieces\n\n- [ ] 1. The page\n\n"
          "### Step 1: the page\n**What:** build it.\n**Verify:** `true`\n")
    write(root, "docs/product/search.md",
          "---\nroute: new\nstage: framed\n---\n\n# Search\n\n"
          "## Value\n\nFind products faster.\n\n" + LEDGER)


class StepCheckTextTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")
        self.section = self.text.split("## Check where the work stands", 1)[1].split("\n## ", 1)[0]

    def command(self):
        found = re.findall(r"^python3 .*gate\.py.*$", self.section, flags=re.M)
        self.assertEqual(len(found), 1, "the step check carries exactly one command")
        return found[0]

    def test_the_command_names_the_plugin_and_the_project_explicitly(self):
        command = self.command()
        self.assertIn(PLACEHOLDER + "/tools/gates/gate.py", command)
        self.assertIn(" route <slug> ", command)
        self.assertIn('--root "<project root>"', command)

    def test_the_placeholder_lives_only_where_claude_code_fills_it_in(self):
        """Measured 2026-09-18: it resolves in SKILL.md text, stays literal in a
        reference file, and is unset as a shell variable."""
        self.assertEqual(self.text.count(PLACEHOLDER), 1)
        for path in (CONDUCTOR / "references").rglob("*.md"):
            with self.subTest(path=path.name):
                self.assertNotIn("CLAUDE_PLUGIN_ROOT", path.read_text(encoding="utf-8"))

    def test_the_section_states_the_agreed_behaviour(self):
        prose = flat(self.section)
        for phrase in (
            "on picking it up, and when a build on it first starts (not again on a "
            "managed Roll continuation)",
            "if the work cannot be tied to exactly one such file, say so and do not check",
            "`enters at:` is the step the work is on",
            "Small standalone fixes and work with no such record get no check and no reminder",
            "git rev-parse --show-toplevel",
            "say the project could not be identified and do not check; never fall back "
            "to Kerd's own tree or guess a root",
            "by the item's plain name, not its slug",
            "name what is missing and offer to do that groundwork now",
            "Going ahead anyway is the person's call, never refused",
            "under `## Decisions and changes` in the work record already tied to this "
            "item, creating `docs/work/<slug>/work.md` when it has none, never in the "
            "`docs/product/` record the check reads",
            "the step skipped, what was missing and the person's words",
            "At pickup, show any go-ahead already recorded for the item",
            "A check that cannot run is reported as not checked, never as passed",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, prose)

    def test_the_entry_rule_names_the_step_check_as_its_one_exception(self):
        self.assertIn(flat("Do not invoke Drive, gate tools or old session machinery to run "
                           "this skill; the single exception is the "
                           "[step check](#check-where-the-work-stands), which only reads the "
                           "gate tool."), flat(self.text))


class ForeignRepoFixture(unittest.TestCase):
    """The command as written, run from inside Kerd against a project that is not Kerd."""

    def run_check(self, slug, project):
        section = SKILL.read_text(encoding="utf-8").split("## Check where the work stands", 1)[1]
        template = re.search(r"^python3 .*gate\.py.*$", section, flags=re.M).group(0)
        command = (template.replace(PLACEHOLDER, str(REPO))
                   .replace("<slug>", slug).replace('"<project root>"', shlex.quote(project)))
        return subprocess.run(command, shell=True, cwd=REPO, capture_output=True, text=True)

    def test_one_item_on_the_build_step_and_one_missing_its_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = os.path.realpath(tmp)
            foreign_repo(project)
            root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=project,
                                  capture_output=True, text=True, check=True).stdout.strip()
            self.assertEqual(os.path.realpath(root), project)

            ready = self.run_check("checkout", root)
            self.assertEqual(ready.returncode, 0, ready.stderr)
            self.assertIn("enters at: loop", ready.stdout)

            gap = self.run_check("search", root)
            self.assertEqual(gap.returncode, 0, gap.stderr)
            self.assertIn("enters at: viability", gap.stdout)
            self.assertIn('need: docs/product/search.md — section "Scope"', gap.stdout)

            # Answers come from the project, never Kerd's own tree.
            kerd_items = {p.stem for p in (REPO / "docs" / "product").glob("*.md")}
            for out in (ready.stdout, gap.stdout):
                self.assertNotIn(str(REPO), out)
                for slug in kerd_items:
                    self.assertNotIn(f"docs/product/{slug}.md", out)

    def test_an_item_missing_from_the_project_is_not_answered_from_kerd(self):
        """risk-state-split exists in Kerd, not in the project: the route must
        not find it, which is the wrong-repository risk in its plainest form."""
        with tempfile.TemporaryDirectory() as tmp:
            project = os.path.realpath(tmp)
            foreign_repo(project)
            result = self.run_check("risk-state-split", project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("enters at: frame", result.stdout)
            self.assertIn("need: docs/product/risk-state-split.md — file exists", result.stdout)
            self.assertNotIn("enters at: acceptance", result.stdout)
            self.assertNotIn("enters at: ready-to-release", result.stdout)


if __name__ == "__main__":
    unittest.main()
