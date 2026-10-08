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

    def test_wait_only_after_independent_work_starts(self):
        # Real use, 2026-09-26: a correctly named wait sat behind one CI watcher
        # while independent work could run; the person had to ask.
        text = normalize((REPO_ROOT / "skills/conductor/references/journey.md").read_text(encoding="utf-8"))
        self.assertIn("first start every other job the current authority already covers and that does not depend on it", text)
        self.assertIn("A named wait is the right ending only when nothing else authorized can move", text)

    def test_genuine_question_is_open(self):
        # Real use, 2026-09-26: an unblocked genuine question was worded "X, or Y?".
        text = normalize((REPO_ROOT / "skills/conductor/references/journey.md").read_text(encoding="utf-8"))
        self.assertIn("The same holds for a genuine question: it is open, never a two-way pick", text)
        self.assertIn("Where two routes are known, recommend one in the block and ask for approval", text)

    def test_steps_for_the_person_say_where(self):
        # Real use, 2026-10-06 to 10-07 (eight sittings reviewed): six "lost"
        # episodes in four sittings after steps that never said which machine or
        # app, steps in prose under a how-did-it-go bubble, or a step left out.
        text = normalize((REPO_ROOT / "skills/conductor/references/journey.md").read_text(encoding="utf-8"))
        self.assertIn("**Steps the person does themselves.**", text)
        self.assertIn("number them, one action each, and start each with where it happens", text)
        self.assertIn("leave none out, an approval on a second device included", text)
        self.assertIn("When the steps are already authorized work for the person to carry out, the bubble asks about their outcome and nothing else", text)
        self.assertIn("Steps that propose a consequential operation still end on the decision block and its approval bubble", text)
        self.assertIn("In the sittings reviewed, length alone was not the problem", text)

    def test_declined_switch_out_is_not_repeated(self):
        # Real use, 2026-09-27: after "no" to Switch Out, it was asked again on the
        # person's follow-up "results?"; his terms (22:30): defer until the next piece of
        # work is done or another ~100k tokens are spent, not every mini turn.
        text = normalize((REPO_ROOT / "skills/conductor/references/journey.md").read_text(encoding="utf-8"))
        self.assertIn("A declined Switch Out is not asked again as filler", text)
        self.assertIn("it comes back only once the next piece of work they chose is finished or about 100k more tokens have been spent", text)
        self.assertIn("never on the answer to a follow-up question", text)
        self.assertIn("When the next item cannot start yet (it is scheduled for later or waits on someone else), the ending names it and when it can start", text)

    def test_finished_work_runs_switch_out_unasked(self):
        # Real use, 2026-10-08 recheck: five of five apple-music sittings (0.175.0 to
        # 0.177.2) asked "Shall I switch out now?" after the work was done; the
        # 2026-10-03 ruling (run it, never ask) lived only in Kerd's own records.
        text = normalize((REPO_ROOT / "skills/conductor/references/journey.md").read_text(encoding="utf-8"))
        self.assertIn("**Switch Out at the end is run, not asked.**", text)
        self.assertIn("Remaining authorized work comes first", text)
        self.assertIn("runs Switch Out itself through the host's skill mechanism, saying so", text)
        self.assertIn("It never asks “Shall I switch out now?” or puts the Switch Out into an approval bubble", text)
        self.assertIn("The ~200k mark never interrupts unfinished work, and a concert keeps its own Roll", text)
        self.assertIn("a contributing partner session never starts one, and Out's existing-owner check still applies", text)
        self.assertIn("the declined Switch Out terms above apply to this Out too", text)
        self.assertIn("Out's own saves and pushes keep their existing authority", text)
        switch = normalize((REPO_ROOT / "skills/switch/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("Out is also started unasked when the sitting's agreed work is complete with nothing outstanding", switch)
        self.assertIn("or the session controlling finished work that starts Out itself, owns it", switch)
        out = normalize((REPO_ROOT / "skills/switch/references/out.md").read_text(encoding="utf-8"))
        self.assertIn("a contributing partner session never starts one", out)

    def test_skill_entries_carry_the_endings(self):
        conductor = normalize((REPO_ROOT / "skills/conductor/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("a turn waiting on a job first starts every other job its authority already covers, then names the job and how and when it resumes", conductor)
        agent = normalize((REPO_ROOT / "skills/agent/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("a turn that took in a partner's contribution still ends with a line to the person", agent)


if __name__ == "__main__":
    unittest.main()
