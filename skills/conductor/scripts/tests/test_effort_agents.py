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


def normalize(text):
    """Collapse line wrapping so an assertion matches the sentence, not the column at
    which it happened to be wrapped. Reflowing a paragraph must not fail a test, and
    must not let a changed sentence pass one."""
    return " ".join(text.split())


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

                self.assertIn("sets effort only and never a model", description,
                              f"{path}: description must state that the agent sets effort "
                              f"only and carries no model, so the caller names it.")
                self.assertIn("CLAUDE_CODE_SUBAGENT_MODEL", description,
                              f"{path}: description must name the documented fall-through for "
                              f"an omitted model. The resolution order is per-invocation model, "
                              f"then the definition's frontmatter, then this environment "
                              f"variable, then the caller's model — so 'inherits the caller's' "
                              f"is only one of its two branches and must not be pinned here.")

                self.assertTrue(body.strip(), f"{path}: body must be non-empty")
                self.assertIn("Follow the brief", body,
                             f"{path}: body must contain 'Follow the brief'")


class DispatchContractTests(unittest.TestCase):
    """The contract lives at the point of use, so it has to be written where the
    dispatch is planned and where it is sent. These assertions guard that the
    wording is present; they are not evidence that a model obeys it — that is what
    a real mixed-model fan-out plus `job_evidence.py` is for.
    """

    MODEL_JOBS = REPO_ROOT / "skills" / "conductor" / "references" / "model-jobs.md"
    ORCHESTRATION = REPO_ROOT / "skills" / "conductor" / "references" / "orchestration.md"

    def test_model_jobs_states_the_call_shape_and_refuses_omission(self):
        text = self.MODEL_JOBS.read_text(encoding="utf-8")
        self.assertIn('subagent_type: "kerd:sonnet-high"', text,
                      "model-jobs.md must show the actual call shape, not describe it")
        self.assertIn('model: "sonnet"', text,
                      "model-jobs.md must show an explicit model in the call shape")
        self.assertIn("There is no unplanned dispatch", text,
                      "model-jobs.md must anchor the contract on the call rather than on a "
                      '"planned" status the model assigns to its own work')
        self.assertIn("composer, player or reviewer", text,
                      "model-jobs.md must cover every Agent call, not the player role alone")
        self.assertIn("CLAUDE_CODE_SUBAGENT_MODEL", text,
                      "model-jobs.md must state the documented resolution order an omitted "
                      "model actually follows")
        self.assertIn("requested_model: null", text,
                      "model-jobs.md must name the countable failure signature")
        self.assertIn("nothing blocks a dispatch mechanically", text,
                      "model-jobs.md must state that this is instruction text, not enforcement")
        self.assertIn("CLAUDE_CODE_SUBAGENT_MODEL_FORCE", text,
                      "model-jobs.md must name the documented host setting that overrides an "
                      "explicit per-call model, so naming one is not described as a guarantee")
        self.assertIn("availableModels", text,
                      "model-jobs.md must name the allowlist substitution that can run a job "
                      "on a model the call did not request")

    def test_the_fallback_and_forced_mode_wording_is_present(self):
        """Guards the *wording* of the two states where the rule would otherwise be
        unsatisfiable: a session without the effort definitions loaded, and a host with
        CLAUDE_CODE_SUBAGENT_MODEL_FORCE on. It does not prove satisfiability — a
        synonymous contradiction elsewhere would pass this. Behavioural evidence comes
        from the helper tests and observed runs, not from here.
        """
        text = normalize(self.MODEL_JOBS.read_text(encoding="utf-8"))
        orchestration = normalize(self.ORCHESTRATION.read_text(encoding="utf-8"))

        self.assertIn("`model` is required in every case", text,
                      "model-jobs.md must state the model half has no exception")
        # The effort half's documented fallback, stated positively and in full.
        for fragment in ("the call still names a concrete ordinary `subagent_type`",
                         "effort is shown as *unset and unverified*",
                         "That is the documented fallback, not a waiver: the `model` half "
                         "is untouched by it"):
            self.assertIn(fragment, text,
                          f"model-jobs.md must carry the complete fallback wording: {fragment!r}")
        self.assertIn("unset and unverified", orchestration,
                      "orchestration.md must mirror the effort fallback, not just model-jobs.md")

        # Forced mode removes the route, never the requirement, and never licenses a retry.
        for fragment in ("unavailable as a compliant Kerd route",
                         "Never retry the dispatch without `model`"):
            self.assertIn(fragment, text,
                          f"model-jobs.md must say what Conductor does while forced mode is "
                          f"on, not merely that the setting exists: {fragment!r}")
        self.assertIn("The request can still be made", text,
                      "model-jobs.md must separate allowlist substitution, where the request "
                      "is still sent, from forced mode, where it cannot be")

    def test_the_null_signature_is_qualified_by_metadata_gaps(self):
        """`requested_model` is initialised to null and unreadable metadata leaves it
        null with a gap, so an unqualified count would accuse a compliant dispatch.
        Wording guard, as above.
        """
        for path, label in ((self.MODEL_JOBS, "model-jobs.md"),
                            (self.ORCHESTRATION, "orchestration.md")):
            text = normalize(path.read_text(encoding="utf-8"))
            with self.subTest(doc=label):
                self.assertIn("requested_model: null", text,
                              f"{label} must name the failure signature")
                self.assertIn("only when", text,
                              f"{label} must qualify the signature rather than asserting it")
                self.assertIn("model-related gap", text,
                              f"{label} must name the metadata gap that also produces null, "
                              f"so a null is not counted as a violation on its own")

    def test_orchestration_requires_both_cells_before_dispatch(self):
        text = self.ORCHESTRATION.read_text(encoding="utf-8")
        self.assertIn("names both cells concretely before dispatch", text,
                      "orchestration.md must require a concrete model and effort in every "
                      "native Claude dispatch row")
        self.assertIn("Exactly one row per grid is the controller row", text,
                      "orchestration.md must bound the controller exemption to one row")
        self.assertIn("with no `Agent` call", text,
                      "orchestration.md must anchor the controller exemption on the absence of "
                      "a dispatch, not on the row's label")


MODELS = ("sonnet", "opus", "fable")


class ModelEffortAgentDefinitionTests(unittest.TestCase):
    """The `kerd:<model>-<effort>` agents exist so the running-job list, which shows
    only the agent's name, names both the model and the effort."""

    def test_every_model_and_effort_pair_has_one_definition(self):
        found = sorted(p.stem for p in AGENTS_DIR.glob("*.md") if not p.stem.startswith("effort-"))
        expected = sorted([f"{model}-{level}" for model in MODELS for level in LEVELS] + ["haiku"])
        self.assertEqual(found, expected)

    def test_each_definition_sets_the_model_and_effort_its_name_carries(self):
        for model in MODELS:
            for level in LEVELS:
                path = AGENTS_DIR / f"{model}-{level}.md"
                with self.subTest(agent=path.stem):
                    fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))
                    self.assertEqual(fields.get("name"), path.stem)
                    self.assertEqual(fields.get("model"), model,
                                     f"{path}: the model must be the one the name shows")
                    self.assertEqual(fields.get("effort"), level,
                                     f"{path}: the effort must be the one the name shows")
                    description = fields.get("description", "")
                    self.assertTrue(description.startswith(
                        "Internal Kerd routing agent for "), f"{path}: description prefix")
                    self.assertIn(f"explicitly selects kerd:{path.stem}", description)
                    self.assertIn(f"still names the model ({model})", description,
                                  f"{path}: the call still names the same model")
                    for key in FORBIDDEN_KEYS:
                        if key != "model":
                            self.assertNotIn(key, fields, f"{path}: must not set {key!r}")
                    self.assertNotIn(": ", description,
                                     f"{path}: an unquoted ': ' breaks the YAML frontmatter")
                    self.assertIn("Follow the brief", body)

    def test_every_live_mention_of_the_model_agents_carries_the_haiku_exception(self):
        """Haiku takes no effort, so guidance naming `kerd:<model>-<effort>` must also
        name plain `kerd:haiku` in the same passage, or it tells Conductor to send a
        Haiku job an effort label that lies."""
        for rel in ("skills/conductor/SKILL.md", "skills/conductor/references/execution.md",
                    "skills/conductor/references/guidance/model-choice.md",
                    "skills/conductor/references/orchestration.md",
                    "skills/conductor/references/journey.md",
                    "skills/conductor/references/model-jobs.md",
                    "skills/agent/references/native-sessions.md"):
            text = normalize((REPO_ROOT / rel).read_text(encoding="utf-8"))
            with self.subTest(doc=rel):
                self.assertIn("<model>-<effort>", text)
                self.assertIn("kerd:haiku", text, f"{rel}: names the model agents without the Haiku exception")

    def test_haiku_names_no_effort_because_it_takes_none(self):
        path = AGENTS_DIR / "haiku.md"
        fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        self.assertEqual(fields.get("name"), "haiku")
        self.assertEqual(fields.get("model"), "haiku")
        self.assertNotIn("effort", fields, "Haiku takes no effort setting, so the name must not claim one")
        self.assertIn("explicitly selects kerd:haiku", fields.get("description", ""))
        self.assertNotIn(": ", fields.get("description", ""))
        self.assertIn("Follow the brief", body)


if __name__ == "__main__":
    unittest.main()
