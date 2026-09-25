"""Private working notes (work_notes): a public project's repo can stay public
while its sketchbooks (docs/work/) move to a private vault repo. This pins the
switch-side half of that fixed contract: Out saves and pushes the notes repo
alongside the project under the same boundary check, names the few findings
that must survive as --carry phrases on the measure call it already runs, and
In reads a `notes:<path>` reading-set entry from the notes root. This checks
presence of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]


def read(rel):
    return " ".join((ROOT / rel).read_text(encoding="utf-8").split())


class PrivateNotesWordingTests(unittest.TestCase):
    def test_each_file_carries_its_fragment(self):
        for rel, fragment in (
            # In: a notes: entry is read from the notes root, not the repo.
            ("skills/switch/references/in-out.md",
             "A reading-set entry written `notes:<path>` "
             "is read from the notes root (`kivna/vault.json`'s `work_notes`), not the repo."),
            # Out: measure refuses an untracked file, same as prepare.
            ("skills/switch/references/in-out.md",
             "`measure` refuses a file Git does not track, the same check `prepare` already "
             "makes."),
            # Out: --carry phrases, fixed by writing them in or widening the set, never a stop.
            ("skills/switch/references/in-out.md",
             "Name the few findings that must survive this sitting, three to five, one "
             "line each, and pass them on the same call as `--carry \"<phrase>\"`"),
            ("skills/switch/references/in-out.md",
             "A phrase `measure` reports as not in the reading set is "
             "fixed by writing it into CONTEXT.md or TODO.md, or by adding its source to "
             "the set, then measuring again. This never blocks the save and asks the "
             "person nothing."),
            # Out: same named-file save reaches the notes repo too.
            ("skills/switch/references/in-out.md",
             "When `kivna/vault.json` sets `work_notes`, "
             "save and push the private notes repo the same way, by the same named-file save, "
             "alongside the project; the sketchbook it holds is part of this sitting's saved "
             "place, not a separate closeout."),
            # Out: the boundary check now proves both repos.
            ("skills/switch/references/in-out.md",
             "With `work_notes` set, this includes the notes repo: the boundary check now "
             "covers both, and the box shows both as saved only when each passes."),
            # Sketchbook location moves with the key when the Out owner starts a fresh record.
            ("skills/switch/references/in-out.md",
             "When `kivna/vault.json` sets `work_notes`, start it instead at "
             "`<notes root>/<slug>/work.md` in the private vault repo and point to it as "
             "`notes:<slug>/work.md`."),
            # SKILL.md: the git helper's two capabilities, stated once at the top.
            ("skills/switch/SKILL.md",
             "refuses a file Git does not track, as `prepare` "
             "does"),
            ("skills/switch/SKILL.md",
             "When a project keeps a private notes repo (`kivna/vault.json`'s `work_notes`), "
             "Out saves and pushes it the same way and the boundary check covers both repos."),
            # kivna: recognizes the key, does not own the folder.
            ("skills/kivna/SKILL.md",
             "the notes root is `<vault>/<folder>/work` (a private git repo, separate from "
             "this project's), and Conductor writes each piece of work's sketchbook there "
             "instead of `docs/work/`. Kivna does not create or maintain this folder; it "
             "only recognizes the key."),
            ("skills/kivna/SKILL.md",
             "Conductor writes it; Switch Out saves and "
             "pushes it, alongside the project, at the session boundary."),
            # vault-spec: the fixed contract, in the human-facing spec.
            ("docs/vault-spec.md",
             "A project whose repo is public can still keep its working notes private. When "
             "`kivna/vault.json` sets `\"work_notes\": \"vault\"`, the notes root moves to "
             "`<vault>/<folder>/work`"),
            ("docs/vault-spec.md",
             "Switch Out saves and "
             "pushes the notes repo alongside the project at the session boundary."),
            # state-contract: ownership entry and both table updates.
            ("docs/state-contract.md",
             "**Owner:** conductor (writes the sketchbook, its diagrams, evidence and drafts)"),
            ("docs/state-contract.md",
             "Switch Out saves and pushes the notes repo the same way it saves the "
             "project, at the same session boundary; the `boundary` check covers both "
             "repos. This is not a second closeout"),
            ("docs/state-contract.md",
             "| vault work/ | W/R | W/R | - | - | - | - | - |"),
            ("docs/state-contract.md",
             "| Vault `work/` writes | **conductor** (the sketchbook, opt-in via `work_notes`) "
             "| Kivna does not write it; it only recognizes the key |"),
            ("docs/state-contract.md",
             "| Vault `work/` save + push | **the Switch Out flow**, alongside the project "
             "| No other skill commits or pushes the notes repo |"),
        ):
            with self.subTest(rel=rel, fragment=fragment[:50]):
                self.assertIn(" ".join(fragment.split()), read(rel))


if __name__ == "__main__":
    unittest.main()
