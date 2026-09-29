"""Guards the wording that tells the person a Kerd-started Codex's commands can't reach
the network by default and offers their own session (0.165.0, from user feedback relayed 2026-09-29: "spins up
codex in a sandbox with no internet access", "anytime i ask it to do anything"). Measured
the same day: an editing job reached the internet only with network_access set; a
read-only job never did, though it could use Codex's own web search. Wording only: whether a session says it shows in real use."""
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]


def normalize(text):
    return " ".join(text.split())


def read(path):
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class CodexOfflineTests(unittest.TestCase):
    def test_agent_says_a_started_codex_is_offline_by_default_and_offers_the_persons_own(self):
        text = normalize(read("skills/agent/SKILL.md"))
        for fragment in ("A Codex that Kerd starts, new partner or fresh worker, runs with native approval prompts disabled",
                         "its shell commands cannot reach the network by default: read-only for a review, workspace-write for an editing job",
                         "open `codex` in a new terminal in this project folder and Agent finds it by discovery, with no ID to copy",
                         "Codex's own web search is a separate tool that follows the effective Codex configuration",
                         "a partial list is not proof that no Codex session is open"):
            self.assertIn(fragment, text)

    def test_guides_explain_the_limit_and_both_ways_round_it(self):
        guide = normalize(read("skills/agent/references/user-guide.md"))
        for fragment in ("**A Codex Kerd starts can't reach the network from its commands by default.**",
                         "native approval prompts disabled",
                         "open `codex` in a new terminal in this project folder and ask Kerd to use it",
                         "[sandbox_workspace_write] network_access = true",
                         "a review's commands never do"):
            self.assertIn(fragment, guide)
        public = normalize(read("docs/guide/agent.md"))
        self.assertIn("its shell commands can't reach the network by default", public)
        roll = normalize(read("skills/switch/references/to-roll.md"))
        self.assertIn("A Codex Roll run starts with native approval prompts disabled and web search off, and is always offline", roll)
        self.assertIn("stops a Roll run instead", roll)
        self.assertIn("a managed Codex Roll refuses to run whenever the setting gives it effective network access", guide)
        jobs = normalize(read("skills/conductor/references/model-jobs.md"))
        self.assertIn("Codex's own web search is a separate tool that follows the effective Codex configuration", jobs)
        self.assertIn("Say so in the Fit line of every fresh Codex job, and when the job needs downloads, offer the person's own open `codex` session through [Agent]", jobs)

    def test_runners_start_codex_as_the_wording_says(self):
        # The wording describes these exact launch settings; change it with them.
        cases = {
            "skills/agent/scripts/agent.py":
                ("'sandbox': 'workspace-write' if writable else 'read-only'", "'approvalPolicy': 'never'"),
            "skills/conductor/scripts/ask.py":
                ('"workspace-write" if writable else "read-only", "-c", \'approval_policy="never"\'',),
            "skills/switch/scripts/codex_roll.py":
                ('"approvalPolicy": "never", "sandbox": "workspace-write" if writable else "read-only"',
                 '"web_search": "disabled"',
                 # Roll refuses a networked thread; the guides say so.
                 'or effective.get("networkAccess") not in {None, False}):'),
        }
        for path, fragments in cases.items():
            source = read(path)
            for fragment in fragments:
                self.assertIn(fragment, source, path)
            for grant in ("network_access", "danger-full-access"):
                self.assertNotIn(grant, source, path)


if __name__ == "__main__":
    unittest.main()
