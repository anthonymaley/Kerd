"""Wording checks for Tend, Kivna and Slainte after the first-user walkthrough (findings 13, 2, 22)."""
from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]


def read(path):
    return " ".join((REPO_ROOT / path).read_text(encoding="utf-8").split())


def section(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i + len(start))]


class TendWording(unittest.TestCase):
    def setUp(self):
        self.t = read("skills/tend/SKILL.md")
        self.kind = section(self.t, "### 3. Decide which kind", "### 3b.")
        self.plain = section(self.t, "#### Repo not yet set up for Kerd", "#### Repo already set up")
        self.fix = section(self.t, "### 5. Fix flow", "### 6. Summary")

    def test_remote_is_optional_and_stop_names_git_init(self):
        s = section(self.t, "### 1. Verify git", "### 2.")
        self.assertNotIn("set up a remote first", s)
        self.assertIn("`git init`", s)
        self.assertIn("A remote is optional", s)

    def test_tend_is_optional_not_first_step(self):
        self.assertIn("Optional tidy-up, never a required first step", self.t)
        self.assertIn("Start with `/kerd:switch in`", self.t)
        self.assertNotIn("Run `/kerd:conductor` to start your first session", self.t)

    def test_switch_made_session_logs_alone_keep_repo_new(self):
        self.assertIn("anything other than `sessions/` and `.gitkeep`", self.kind)
        self.assertIn("Switch Out creates those on its own", self.kind)
        self.assertNotIn("CONTEXT.md", self.kind)
        self.assertIn("could not inspect", self.kind)
        self.assertIn("do not classify the repo or apply anything", self.kind)
        self.assertIn("still new to Tend", self.kind)

    def test_plain_report_has_no_marks_and_lists_optional_files(self):
        self.assertIn("Do not use `✓ ✗ ⚠`", self.plain)
        self.assertIn("Optional, your call.", self.plain)
        for f in ("`CLAUDE.md`", "`docs/playbook.md`", "`TODO.md`", "`kivna/vault.json`"):
            self.assertIn(f, self.plain)

    def test_plain_report_lists_every_edit_and_vault_stays_unscaffolded(self):
        self.assertIn("List every creation or edit", self.plain)
        self.assertIn("add these lines to your existing file", self.plain)
        self.assertNotIn("existing files are not changed", self.plain)
        self.assertIn("the vault is not scaffolded on this path", self.plain)
        self.assertIn("Approval covers only the item 1 list", self.plain)
        self.assertIn("never runs vault scaffold", self.fix)
        self.assertIn("check the path again; if it cannot be inspected, stop", self.fix)
        self.assertNotIn("Switch Out can keep it current", self.plain)

    def test_gitkeep_checked_per_folder(self):
        self.assertIn("each folder and each `.gitkeep` on its own", self.plain)
        self.assertIn("made `kivna/sessions/` without a `.gitkeep`", self.plain)

    def test_no_intake_on_newcomer_path(self):
        s = section(self.t, "### 2. Infer project identity", "### 3.")
        self.assertIn("only when the chosen fixes use those answers", s)
        self.assertIn("skip the intake", s)

    def test_drift_report_for_set_up_repos_kept(self):
        self.assertIn("4 passing · 2 warnings · 1 failing", self.t)


class KivnaWording(unittest.TestCase):
    def setUp(self):
        self.k = read("skills/kivna/SKILL.md")
        self.disc = section(self.k, "## Vault Discovery", "## Folder Convention")

    def test_no_personal_folder_default(self):
        # `~/eolas/vault/` appears only as a found-on-disk offer, never as a default or in examples
        self.assertEqual(self.k.count("eolas"), self.k.count("`~/eolas/vault/`"))
        self.assertIn("not as a default", self.disc)
        self.assertNotIn("anthonymaley", self.k)

    def test_asks_without_default_when_no_vault_json(self):
        self.assertIn("find or ask", self.disc)
        self.assertIn("Otherwise ask**, with no default path", self.disc)
        self.assertIn("Where is your Obsidian vault?", self.disc)

    def test_unreadable_config_stops_and_is_not_absent(self):
        self.assertIn("cannot be read, is not valid JSON, or lacks `vault`, `folder` or `name`", self.disc)
        self.assertIn("it is not \"absent\". Stop", self.disc)
        self.assertIn("Do not ask for a vault path, do not scaffold", self.disc)

    def test_existing_vault_content_is_preserved(self):
        self.assertIn("keep it as it is and write only `kivna/vault.json`", self.disc)
        self.assertIn("only on the person's explicit approval", self.disc)
        self.assertIn("never overwrite an existing vault file", self.k)

    def test_inspection_failure_stops_discovery(self):
        self.assertIn("a permission error, an unreadable folder", self.disc)
        self.assertIn("do not continue as if the file were absent", self.disc)
        self.assertIn("is a stop", self.disc)

    def test_scaffold_preserves_existing_vault_json(self):
        sc = section(self.k, "6. **Write `kivna/vault.json`**", "7. **Suggest optional slots.**")
        self.assertIn("only when its absence is confirmed, checked again immediately before the write", sc)
        self.assertIn("keep it exactly as it is", sc)
        self.assertIn("work_notes", sc)

    def test_playbook_route_is_supported(self):
        self.assertNotIn("No playbook yet — /kerd:tend to create one", self.k)
        self.assertIn("write `docs/playbook.md` by hand", self.k)
        self.assertIn("copy and adapt the skeleton Tend shows", self.k)
        self.assertIn("does not create it", self.k)

    def test_general_write_safety_rule_and_its_uses(self):
        rule = section(self.k, "## Write Safety", "## Vault Discovery")
        self.assertIn("An update needs a successful read", rule)
        self.assertIn("A create needs confirmed absence", rule)
        self.assertIn("Inspect the target again immediately before writing", rule)
        self.assertIn("stop and say so", rule)
        save = section(self.k, "### `/kerd:kivna save`", "#### The mechanic")
        self.assertIn("Write Safety", save)
        imp = section(self.k, "6. **Integrate.**", "### `/kerd:kivna out`")
        self.assertIn("Write Safety", imp)
        exp = section(self.k, "#### Write the TOON export", "#### Write the JSON export")
        self.assertIn("Write Safety", exp)
        sc = section(self.k, "### `/kerd:kivna scaffold`", "2. **Run the per-project intake.**")
        self.assertIn("Write Safety applies to every create below", sc)
        self.assertIn("a file that appeared meanwhile is kept", sc)

    def test_found_existing_vault_is_offered_not_defaulted(self):
        self.assertIn("offer it as a location found, not as a default", self.disc)
        self.assertIn("only after the person confirms", self.disc)
        self.assertIn("a newcomer sees no such path", self.disc)

    def test_missing_vault_folder_offers_create_but_errors_stop(self):
        self.assertIn("If the vault folder they name is confirmed absent", self.disc)
        self.assertIn("offer to create it", self.disc)
        self.assertIn("A permission error or any other failure to inspect it is a stop, not an offer to create", self.disc)


class SlainteWording(unittest.TestCase):
    def test_playbook_is_not_claimed_to_be_created_by_tend(self):
        t = read("skills/slainte/SKILL.md")
        pb = section(t, "1. **Existence**: does `docs/playbook.md` exist?", "2. **Current Status accuracy**")
        self.assertNotIn("Run `/kerd:tend` to create one from the skeleton", pb)
        self.assertNotIn("switch out", pb)
        self.assertIn("copy and adapt the skeleton", pb)
        self.assertIn("does not create it", pb)
        self.assertNotIn("high severity", pb)
        self.assertIn("It is optional", pb)
        self.assertIn("cannot be inspected", pb)
        self.assertIn("Absence is confirmed, not assumed.", t)


if __name__ == "__main__":
    unittest.main()
