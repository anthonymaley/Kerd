import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("job_evidence", ROOT / "job_evidence.py")
job_evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(job_evidence)

AGENT = "a434d67120ca1df6d"
SESSION = "4f1c2b3a-5d6e-4f70-8a9b-0c1d2e3f4a5b"
SECRET = "SECRET-MARKER"
META = {"agentType": "kerd:effort-low", "model": "sonnet", "description": SECRET + " description",
        "toolUseId": "toolu_" + SECRET, "spawnDepth": 1}
RECORDS = [
    {"type": "user", "effort": "low", "message": {"role": "user", "content": SECRET + " prompt"}},
    {"type": "assistant", "effort": "low",
     "message": {"model": "claude-sonnet-5", "content": [{"type": "text", "text": SECRET + " reply"}]}},
    {"type": "assistant", "message": {"model": "claude-sonnet-5", "content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "echo " + SECRET}}]}},
]


class JobEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.scratch = Path(self.temp.name).resolve()
        self.root = self.scratch / "projects"
        self.home = self.scratch / "home"
        self.home.mkdir()
        # In-process calls resolve the default store under the fixture home, never the real one.
        patcher = mock.patch.dict(os.environ, {"HOME": str(self.home)})
        patcher.start()
        self.addCleanup(patcher.stop)

    def folder(self, project="-fixture-project", session=SESSION, root=None):
        path = (root or self.root) / project / session / "subagents"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_job(self, records=RECORDS, meta=META, project="-fixture-project", root=None):
        """Write a transcript (dicts as JSON, strings verbatim) and, unless meta is None, its metadata."""
        folder = self.folder(project, root=root)
        transcript = folder / f"agent-{AGENT}.jsonl"
        transcript.write_text("".join((r if isinstance(r, str) else json.dumps(r)) + "\n" for r in records))
        if meta is not None:
            (folder / f"agent-{AGENT}.meta.json").write_text(meta if isinstance(meta, str) else json.dumps(meta))
        return transcript

    def meta_path(self, project="-fixture-project"):
        return self.folder(project) / f"agent-{AGENT}.meta.json"

    def observe(self, agent=AGENT, session=SESSION):
        code, result = job_evidence.evidence(["--agent-id", agent, "--session", session,
                                              "--projects-root", str(self.root)], environ={})
        self.assertEqual(code, 0, result)
        return result

    def cli(self, *args, env_session=None):
        """Run the script with HOME pointed at a fixture, so the default root is never the real store."""
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
        env["HOME"] = str(self.home)
        if env_session is not None:
            env["CLAUDE_CODE_SESSION_ID"] = env_session
        return subprocess.run([sys.executable, str(ROOT / "job_evidence.py"), *args],
                              cwd=self.scratch, capture_output=True, text=True, env=env)

    def assert_unverified(self, result, reason):
        self.assertEqual((result["status"], result["reason"]), ("unverified", reason))

    def assert_refused(self, completed):
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "refused")

    def assert_no_leak(self, output):
        for value in (str(self.root), str(self.scratch), SESSION, AGENT, SECRET):
            self.assertNotIn(value, output)

    def test_normal_fixture_is_observed_with_exact_counts(self):
        self.write_job()
        completed = self.cli("--agent-id", AGENT, "--projects-root", str(self.root), env_session=SESSION)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout), {
            "status": "observed", "reason": None, "agent_type": "kerd:effort-low", "requested_model": "sonnet",
            "observed_models": {"claude-sonnet-5": 2}, "observed_effort": {"low": 1}, "malformed_lines": 0,
            "gaps": []})  # the user record's effort is not counted

    def test_default_root_is_under_home(self):
        self.write_job(root=self.home / ".claude" / "projects")
        completed = self.cli("--agent-id", AGENT, env_session=SESSION)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "observed")

    def test_not_found_and_ambiguous_are_unverified(self):
        self.assert_unverified(self.observe(), "not found")
        self.write_job()
        self.assert_unverified(self.observe(agent="a0123456789abcdef"), "not found")
        self.assert_unverified(self.observe(session="00000000-0000-4000-8000-000000000000"), "not found")
        self.write_job(project="-another-project")
        result = self.observe()
        self.assert_unverified(result, "ambiguous")
        self.assertEqual((result["observed_models"], result["observed_effort"]), ({}, {}))

    def test_malformed_lines_are_counted_and_content_never_leaks(self):
        self.write_job(RECORDS + ["", "   "])
        result = self.observe()
        self.assertEqual((result["status"], result["malformed_lines"]), ("observed", 0))  # blank lines are skipped
        self.write_job(RECORDS + ["not json " + SECRET, '{"effort": "low", ', "[1, 2]", "", "   "])
        completed = self.cli("--agent-id", AGENT, "--projects-root", str(self.root), env_session=SESSION)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        result = json.loads(completed.stdout)
        self.assert_unverified(result, "malformed records; counts are partial")
        self.assertEqual(result["malformed_lines"], 3)
        self.assertEqual((result["observed_models"], result["observed_effort"]),
                         ({"claude-sonnet-5": 2}, {"low": 1}))
        self.assertNotIn(SECRET, completed.stdout + completed.stderr)

    def test_missing_metadata_is_a_gap_and_still_observed(self):
        self.write_job(meta=None)
        result = self.observe()
        self.assertEqual(result["status"], "observed")
        self.assertEqual((result["agent_type"], result["requested_model"]), (None, None))
        self.assertEqual(result["gaps"], ["metadata missing"])

    def test_metadata_fields_are_validated_and_absent_model_is_unspecified(self):
        self.write_job(meta={"agentType": "general-purpose"})
        result = self.observe()
        # Null means the call did not specify a model, not that the caller's model was
        # inherited: resolution can reach CLAUDE_CODE_SUBAGENT_MODEL before the caller.
        # With no gaps recorded, this null is qualified evidence of an omitted argument.
        self.assertEqual((result["agent_type"], result["requested_model"]), ("general-purpose", None))
        self.assertEqual(result["gaps"], [])
        self.write_job(meta={"model": "sonnet"})
        result = self.observe()
        self.assertEqual((result["agent_type"], result["requested_model"]), (None, "sonnet"))
        self.assertEqual(result["gaps"], ["metadata has no agent type"])
        for meta, gap in (({"agentType": SECRET + " with spaces", "model": "x" * 65},
                           ["metadata agent type is not a valid value", "metadata requested model is not a valid value"]),
                          ({"agentType": ["kerd:effort-low"], "model": 5},
                           ["metadata agent type is not a valid value", "metadata requested model is not a valid value"]),
                          ("not json " + SECRET, ["metadata is not valid JSON"]),
                          ('["kerd:effort-low"]', ["metadata is not a JSON object"])):
            with self.subTest(meta=meta):
                self.write_job(meta=meta)
                result = self.observe()
                self.assertEqual(result["status"], "observed")
                self.assertEqual((result["agent_type"], result["requested_model"], result["gaps"]), (None, None, gap))
                self.assertNotIn(SECRET, json.dumps(result))

    def test_missing_effort_or_model_records_are_unverified(self):
        without_effort = [{k: v for k, v in r.items() if k != "effort"} for r in RECORDS]
        self.write_job(without_effort)
        result = self.observe()
        self.assert_unverified(result, "no effort records")
        self.assertEqual(result["observed_models"], {"claude-sonnet-5": 2})
        user_effort_only = [{"type": "user", "effort": "high"}, {"type": "attachment", "effort": "high"},
                            {"type": "assistant", "message": {"model": "claude-sonnet-5"}}]
        self.write_job(user_effort_only)
        result = self.observe()
        self.assert_unverified(result, "no effort records")  # effort outside assistant records is ignored
        self.assertEqual((result["observed_effort"], result["observed_models"]), ({}, {"claude-sonnet-5": 1}))
        without_model = [{"type": "user", "effort": "low"}, {"type": "assistant", "effort": "low", "message": {}}]
        self.write_job(without_model)
        result = self.observe()
        self.assert_unverified(result, "no model records")
        self.assertEqual(result["observed_effort"], {"low": 1})
        self.write_job([{"type": "attachment"}])
        self.assert_unverified(self.observe(), "no effort or model records")

    def test_symlinked_transcript_is_unverified_and_symlinked_metadata_is_a_gap(self):
        transcript = self.write_job()
        real = self.scratch / "elsewhere.jsonl"
        os.replace(transcript, real)
        os.symlink(real, transcript)
        self.assert_unverified(self.observe(), "transcript refused: it is a symbolic link")
        transcript.unlink()
        os.symlink(self.scratch / "dangling.jsonl", transcript)
        self.assert_unverified(self.observe(), "transcript refused: it is a symbolic link")
        transcript.unlink()
        self.write_job()
        meta = self.meta_path()
        real_meta = self.scratch / "elsewhere.meta.json"
        os.replace(meta, real_meta)
        os.symlink(real_meta, meta)
        result = self.observe()
        self.assertEqual(result["status"], "observed")
        self.assertEqual((result["agent_type"], result["requested_model"]), (None, None))
        self.assertEqual(result["gaps"], ["metadata refused: it is a symbolic link"])

    def test_fifo_or_directory_transcript_is_unverified(self):
        folder = self.folder()
        transcript = folder / f"agent-{AGENT}.jsonl"
        os.mkfifo(transcript)
        self.assert_unverified(self.observe(), "transcript refused: it is not a regular file")
        transcript.unlink()
        transcript.mkdir()
        self.assert_unverified(self.observe(), "transcript refused: it is not a regular file")
        transcript.rmdir()
        self.write_job(meta=None)
        os.mkfifo(self.meta_path())
        result = self.observe()
        self.assertEqual(result["status"], "observed")
        self.assertEqual(result["gaps"], ["metadata refused: it is not a regular file"])

    def test_foreign_owner_and_unreadable_transcript_are_unverified(self):
        self.write_job()
        with mock.patch.object(job_evidence.os, "getuid", return_value=os.getuid() + 1):
            self.assert_unverified(self.observe(), "transcript refused: it is not owned by the current user")
        if os.getuid() == 0:
            self.skipTest("root reads files regardless of permission bits")
        transcript = self.folder() / f"agent-{AGENT}.jsonl"
        os.chmod(transcript, 0)
        self.addCleanup(os.chmod, transcript, 0o600)
        result = self.observe()
        self.assertEqual(result["status"], "unverified")
        self.assertTrue(result["reason"].startswith("transcript unreadable: "), result["reason"])

    def test_group_readable_native_files_are_accepted(self):
        transcript = self.write_job()
        os.chmod(transcript, 0o644)
        os.chmod(self.meta_path(), 0o644)
        self.assertEqual(self.observe()["status"], "observed")

    def test_unexpected_schema_values_are_ignored(self):
        self.write_job([
            {"type": "assistant", "effort": 3},
            {"type": "assistant", "effort": "LOW"},
            {"type": "assistant", "effort": "x" * 17},
            {"type": "assistant", "effort": SECRET.lower()[:6] + " x"},
            {"type": "assistant", "message": {"model": "claude sonnet 5"}},
            {"type": "assistant", "message": {"model": "m" * 65}},
            {"type": "assistant", "message": {"model": ["claude-sonnet-5"]}},
            {"type": "assistant", "message": "claude-sonnet-5"},
            {"type": "user", "message": {"model": "claude-sonnet-5"}},
            {"effort": {"level": "low"}, "message": {"model": None}},
        ], meta=None)
        result = self.observe()
        self.assert_unverified(result, "no effort or model records")
        self.assertEqual((result["observed_models"], result["observed_effort"], result["malformed_lines"]),
                         ({}, {}, 0))

    def test_transcript_over_the_limit_is_counted_up_to_it(self):
        line = json.dumps(RECORDS[1]) + "\n"
        self.write_job([RECORDS[1]] * 4)
        with mock.patch.object(job_evidence, "TRANSCRIPT_LIMIT", len(line) * 2 + 5):
            result = self.observe()
        self.assert_unverified(result, "transcript exceeds 50 MB; counts are partial")
        self.assertEqual((result["observed_effort"], result["observed_models"], result["malformed_lines"],
                          result["gaps"]), ({"low": 2}, {"claude-sonnet-5": 2}, 0, []))
        with mock.patch.object(job_evidence, "TRANSCRIPT_LIMIT", len(line) * 4):  # limit exactly at EOF
            result = self.observe()
        self.assertEqual((result["status"], result["reason"], result["observed_effort"], result["gaps"]),
                         ("observed", None, {"low": 4}, []))

    def test_invalid_arguments_exit_2_refused(self):
        root = ("--projects-root", str(self.root))
        for agent in ("", "a434d67", "x434d67120ca1df6d", "A434D67120CA1DF6D", "a" + "0" * 41,
                      "../" + AGENT, AGENT + "\n", AGENT + "*", "a434d671-20ca"):
            with self.subTest(agent=agent):
                completed = self.cli("--agent-id=" + agent, *root, env_session=SESSION)
                self.assert_refused(completed)
                self.assert_no_leak(completed.stdout)
        for session in ("not-a-uuid", SESSION.upper(), SESSION + "0", "*", "../" + SESSION):
            with self.subTest(session=session):
                self.assert_refused(self.cli("--agent-id", AGENT, "--session=" + session, *root))
        self.assert_refused(self.cli("--agent-id", AGENT, "--session", SESSION, env_session=SESSION))
        self.assert_refused(self.cli("--agent-id", AGENT, "--session", SESSION, "--projects-root="))

    def test_explicit_session_against_the_default_store_is_refused(self):
        store = self.home / ".claude" / "projects"
        self.write_job(root=store)
        alias = self.scratch / "store-link"
        os.symlink(store, alias)
        roots = [str(store), str(store) + "/", str(store) + "/.", str(alias), str(alias) + "/",
                 str(self.home / ".claude" / "x" / ".." / "projects")]
        upper = self.home / ".CLAUDE" / "PROJECTS"
        if upper.exists():
            roots.append(str(upper))  # case-insensitive file system: same directory, different spelling
        for root in roots:
            with self.subTest(root=root):
                for env_session in (None, SESSION):
                    completed = self.cli("--agent-id", AGENT, "--session", SESSION, "--projects-root", root,
                                         env_session=env_session)
                    self.assert_refused(completed)
                    self.assertEqual(json.loads(completed.stdout)["reason"],
                                     "--session is not accepted against the default projects store")
                    self.assert_no_leak(completed.stdout + completed.stderr)
                    self.assertNotIn(str(self.home), completed.stdout + completed.stderr)
        completed = self.cli("--agent-id", AGENT, "--projects-root", str(store), env_session=SESSION)
        self.assertEqual(json.loads(completed.stdout)["status"], "observed")

    def test_explicit_session_through_links_into_the_default_store_is_refused(self):
        store = self.home / ".claude" / "projects"
        self.write_job(root=store, project="-p")
        real_session = store / "-p" / SESSION
        reason = "--session is not accepted for a transcript inside the default projects store"
        farm = self.scratch / "farm"
        farm.mkdir()
        os.symlink(store / "-p", farm / "-p")  # symlinked project folder
        session_farm = self.scratch / "session-farm"
        (session_farm / "-p").mkdir(parents=True)
        os.symlink(real_session, session_farm / "-p" / SESSION)  # symlinked session folder
        file_farm = self.scratch / "file-farm"
        subagents = file_farm / "-p" / SESSION / "subagents"
        subagents.mkdir(parents=True)
        os.symlink(real_session / "subagents" / f"agent-{AGENT}.jsonl", subagents / f"agent-{AGENT}.jsonl")
        meta_farm = self.scratch / "meta-farm"
        self.write_job(root=meta_farm, project="-p", meta=None)
        os.symlink(real_session / "subagents" / f"agent-{AGENT}.meta.json",
                   meta_farm / "-p" / SESSION / "subagents" / f"agent-{AGENT}.meta.json")
        for root in (farm, session_farm, file_farm, meta_farm):
            with self.subTest(root=root.name):
                opened = mock.patch.object(job_evidence.os, "open", side_effect=AssertionError("opened"))
                with opened:
                    code, result = job_evidence.evidence(["--agent-id", AGENT, "--session", SESSION,
                                                          "--projects-root", str(root)], environ={})
                self.assertEqual((code, result), (2, {"status": "refused", "reason": reason}))
                completed = self.cli("--agent-id", AGENT, "--session", SESSION, "--projects-root", str(root))
                self.assert_refused(completed)
                self.assertEqual(json.loads(completed.stdout)["reason"], reason)
                self.assert_no_leak(completed.stdout + completed.stderr)
                self.assertNotIn(str(self.home), completed.stdout + completed.stderr)
        self.write_job(project="-p")
        self.write_job(project="-q")
        os.symlink(store / "-p", self.root / "-linked")
        code, result = job_evidence.evidence(["--agent-id", AGENT, "--session", SESSION,
                                              "--projects-root", str(self.root)], environ={})
        self.assertEqual((code, result["reason"]), (2, reason))  # refused even where it would be ambiguous
        for root, status in ((farm, "observed"), (file_farm, "unverified")):
            with self.subTest(default_session=root.name):
                completed = self.cli("--agent-id", AGENT, "--projects-root", str(root), env_session=SESSION)
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertEqual(json.loads(completed.stdout)["status"], status)

    def test_no_session_is_unverified_exit_0(self):
        self.write_job()
        for args in ((), ("--projects-root", str(self.root))):
            with self.subTest(args=args):
                completed = self.cli("--agent-id", AGENT, *args)
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assert_unverified(json.loads(completed.stdout), "no session")
        for value, reason in (("", "no session"), ("not-a-uuid", "host session id is not a UUID"),
                              (SESSION.upper(), "host session id is not a UUID")):
            with self.subTest(env_session=value):
                completed = self.cli("--agent-id", AGENT, "--projects-root", str(self.root), env_session=value)
                self.assertEqual(completed.returncode, 0, completed.stdout)
                self.assert_unverified(json.loads(completed.stdout), reason)

    def test_output_never_contains_root_session_or_agent_id(self):
        self.write_job()
        base = ("--agent-id", AGENT, "--projects-root", str(self.root))
        outputs = [self.cli(*base, env_session=SESSION)]
        self.meta_path().unlink()
        outputs.append(self.cli(*base, env_session=SESSION))
        self.write_job(project="-another-project")
        outputs.append(self.cli(*base, env_session=SESSION))
        outputs.append(self.cli("--agent-id", "a0123456789abcdef", "--projects-root", str(self.root),
                                env_session=SESSION))
        outputs.append(self.cli("--agent-id", AGENT + "zz", "--projects-root", str(self.root), env_session=SESSION))
        outputs.append(self.cli("--agent-id", AGENT, "--session", SESSION))
        statuses = [json.loads(c.stdout)["status"] for c in outputs]
        self.assertEqual(statuses, ["observed", "observed", "unverified", "unverified", "refused", "refused"])
        for completed in outputs:
            self.assert_no_leak(completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
