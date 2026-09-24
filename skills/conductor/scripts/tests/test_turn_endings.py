"""Guards the two turn endings real use showed missing (0.153.1, from 2026-09-24:
ten status prompts across four sessions): a named wait on a job, and a line to
the person after answering a partner. Wording only: whether a session follows it
shows in real use."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]


def normalize(text):
    return " ".join(text.split())


class TurnEndingTests(unittest.TestCase):
    def test_journey_names_the_wait_and_the_partner_reply(self):
        text = normalize((REPO_ROOT / "skills/conductor/references/journey.md").read_text(encoding="utf-8"))
        for fragment in ("**Waiting on a job**",
                         "the last line names the job, says how the session resumes",
                         "or “return time unknown” with that next check; it never invents an estimate",
                         "A bare “nothing is needed from you” or a status tick without the job and how it resumes is not that line",
                         "Claim an automatic wake-up only where the route provides one",
                         "**Answering a partner's contribution**",
                         "Informational arrival notices stay unanswered, and unattended workers keep their own result contract",
                         "Never end a turn on a suggestion",
                         "Switch Out's closing box, a pause the person asked for, agreed completion, and a finish with nothing left open"):
            self.assertIn(fragment, text)

    def test_skill_entries_carry_the_endings(self):
        conductor = normalize((REPO_ROOT / "skills/conductor/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("a turn waiting on a job names the job and how and when it resumes", conductor)
        agent = normalize((REPO_ROOT / "skills/agent/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("a turn that took in a partner's contribution still ends with a line to the person", agent)


if __name__ == "__main__":
    unittest.main()
