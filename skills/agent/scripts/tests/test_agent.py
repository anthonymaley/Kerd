import json
import os
import stat
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent


class HelpTests(unittest.TestCase):
    def test_all_help_routes_work_without_project_or_provider_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            for command in ([], ['sessions'], ['pair'], ['start'], ['ask'], ['status'], ['wait'],
                            ['identity'], ['handoff'], ['adopt']):
                with self.subTest(command=command):
                    result = subprocess.run(
                        [sys.executable, '-B', agent.__file__, *command, '--help'],
                        cwd=directory, env={**os.environ, 'PATH': ''},
                        capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, '')
                    self.assertIn('usage:', result.stdout)
                    self.assertEqual(list(Path(directory).iterdir()), [])


class SuccessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        subprocess.run(['git', 'init', '-q', self.temp.name], check=True)
        self.app = agent.Agent(self.temp.name)
        self.old, self.new = str(uuid.uuid4()), str(uuid.uuid4())
        with patch.object(agent, 'live_target'):
            self.app.pair('claude', self.old, 'partner', 'Reviewer')
        self.path = self.app.state / 'partners/partner.json'
        self.record = self.app.root / 'handoff.md'
        self.record.write_text('The reviewer role continues from this saved place.\n')

    def identity(self, sid):
        return patch.object(self.app, 'identity', return_value={'id': sid, 'provider': 'claude'})

    def prepare(self):
        with self.identity(self.old):
            return self.app.handoff('claude', 'partner', 'handoff.md')

    def test_identity_selects_provider_env_and_requires_native_corroboration_without_writes(self):
        before = self.path.read_bytes()
        for provider, key in [('claude', 'CLAUDE_CODE_SESSION_ID'), ('codex', 'CODEX_THREAD_ID')]:
            with patch.dict(os.environ, {'CLAUDE_CODE_SESSION_ID': self.old,
                                        'CODEX_THREAD_ID': self.new}, clear=True):
                sid = os.environ[key]
                with patch.object(agent, 'live_target', return_value={'id': sid}) as native:
                    result = self.app.identity(provider)
                native.assert_called_once_with(self.app.root, provider, sid)
                self.assertEqual(result['identity_source'], key)
                self.assertTrue(result['self'])
                with patch.object(agent, 'live_target', side_effect=agent.Unavailable('Not in project')):
                    with self.assertRaises(agent.Unavailable):
                        self.app.identity(provider)
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(agent.Unavailable):
                    self.app.identity(provider)
        self.assertEqual(self.path.read_bytes(), before)

    def test_same_id_is_byte_preserving_even_with_prepared_handoff(self):
        self.prepare()
        before = self.path.read_bytes()
        with self.identity(self.old):
            result = self.app.adopt('claude', 'partner', self.old)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(result['handoff'], json.loads(before)['handoff'])

    def test_handoff_consumed_role_kept_and_request_bytes_untouched(self):
        self.prepare()
        request = self.app.folder('requests') / (str(uuid.uuid4()) + '.json')
        original = {'session': self.old, 'project': str(self.app.root),
                    'status': 'reply-received', 'reply': 'Original review'}
        agent.atomic_json(request, original)
        before = request.read_bytes()
        with self.identity(self.new), patch.object(self.app, 'ask', side_effect=AssertionError('No dispatch')):
            result = self.app.adopt('claude', 'partner', self.old, 'handoff.md')
        self.assertEqual(result['id'], self.new)
        self.assertEqual(result['partner_role'], 'Reviewer')
        self.assertEqual(result['previous']['id'], self.old)
        self.assertNotIn('handoff', result)
        self.assertNotIn('owned', result)
        self.assertEqual(request.read_bytes(), before)
        self.assertEqual(self.app.status(request.stem), original)
        self.assertEqual(json.loads(self.path.read_text()), result)
        self.assertEqual(subprocess.check_output(['git', 'status', '--porcelain'],
                                                cwd=self.app.root, text=True), '?? handoff.md\n')

    def test_missing_authority_and_stale_expected_id_do_not_write(self):
        before = self.path.read_bytes()
        with self.identity(self.new):
            for old in (self.old, str(uuid.uuid4())):
                with self.assertRaises(ValueError):
                    self.app.adopt('claude', 'partner', old)
                self.assertEqual(self.path.read_bytes(), before)
            result = self.app.adopt('claude', 'partner', self.old, confirm=True)
        self.assertEqual(result['id'], self.new)

    def test_changed_handoff_and_wrong_handoff_refused(self):
        self.prepare()
        before = self.path.read_bytes()
        other = self.app.root / 'other.md'
        other.write_bytes(self.record.read_bytes())
        with self.identity(self.new):
            with self.assertRaises(ValueError):
                self.app.adopt('claude', 'partner', self.old, 'other.md')
            self.record.write_text('Changed scope.\n')
            with self.assertRaises(ValueError):
                self.app.adopt('claude', 'partner', self.old, 'handoff.md')
        self.assertEqual(self.path.read_bytes(), before)

    def test_out_only_designates_its_own_binding_and_can_cancel(self):
        before = self.path.read_bytes()
        with self.identity(self.new):
            with self.assertRaises(ValueError):
                self.app.handoff('claude', 'partner', 'handoff.md')
        self.assertEqual(self.path.read_bytes(), before)
        self.prepare()
        with self.identity(self.old):
            result = self.app.handoff('claude', 'partner', cancel=True)
        self.assertNotIn('handoff', result)
        with self.identity(self.new):
            with self.assertRaises(ValueError):
                self.app.adopt('claude', 'partner', self.old, 'handoff.md')

    def test_owned_partners_provider_and_project_mismatches_refused(self):
        original = json.loads(self.path.read_text())
        for changes in ({'owned': True, 'native_launch': 'launcher', 'request_id': 'old'},
                        {'provider': 'codex'}, {'project': '/tmp'}):
            agent.atomic_json(self.path, {**original, **changes})
            before = self.path.read_bytes()
            with self.identity(self.new):
                with self.assertRaises(ValueError):
                    self.app.adopt('claude', 'partner', self.old, confirm=True)
            with self.identity(self.old):
                with self.assertRaises(ValueError):
                    self.app.handoff('claude', 'partner', 'handoff.md')
            self.assertEqual(self.path.read_bytes(), before)

    def test_unverified_self_cannot_replace_and_plain_pair_still_refuses(self):
        before = self.path.read_bytes()
        with patch.object(self.app, 'identity', side_effect=agent.Unavailable('Identity unresolved')):
            with self.assertRaises(agent.Unavailable):
                self.app.adopt('claude', 'partner', self.old, confirm=True)
        with patch.object(agent, 'live_target'):
            with self.assertRaisesRegex(ValueError, 'another session'):
                self.app.pair('claude', self.new, 'partner')
        self.assertEqual(self.path.read_bytes(), before)

    def test_competing_replacements_have_one_winner(self):
        barrier = threading.Barrier(2)
        results = []
        def run(sid):
            app = agent.Agent(self.temp.name)
            def identity(provider):
                barrier.wait(timeout=5)
                return {'id': sid}
            app.identity = identity
            try:
                results.append(('ok', app.adopt('claude', 'partner', self.old, confirm=True)['id']))
            except ValueError:
                results.append(('refused', sid))
        ids = [self.new, str(uuid.uuid4())]
        threads = [threading.Thread(target=run, args=(sid,)) for sid in ids]
        for thread in threads: thread.start()
        for thread in threads: thread.join(timeout=10)
        self.assertTrue(all(not t.is_alive() for t in threads))
        self.assertEqual(sorted(x[0] for x in results), ['ok', 'refused'])
        winner = next(sid for status, sid in results if status == 'ok')
        self.assertEqual(json.loads(self.path.read_text())['id'], winner)

    def test_handoff_path_escape_and_missing_binding_never_create_a_store(self):
        before = self.path.read_bytes()
        with self.identity(self.old):
            with self.assertRaises(ValueError):
                self.app.handoff('claude', 'partner', '../elsewhere.md')
            with self.assertRaises(agent.Unavailable):
                self.app.handoff('claude', 'missing', 'handoff.md')
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse((self.path.parent / 'missing.json').exists())

    def test_failed_atomic_replace_leaves_prior_binding_and_designation_intact(self):
        self.prepare()
        before = self.path.read_bytes()
        with self.identity(self.new), patch.object(agent.os, 'replace', side_effect=OSError('fixture failure')):
            with self.assertRaises(OSError):
                self.app.adopt('claude', 'partner', self.old, 'handoff.md')
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.glob('*.tmp')), [])

    def test_new_ask_uses_replacement_and_no_launch_privileges(self):
        import contextlib, io
        with self.identity(self.new):
            self.app.adopt('claude', 'partner', self.old, confirm=True)
        argv = ['agent.py', '--project', str(self.app.root), 'ask', '--alias', 'partner',
                '--prompt-file', str(self.record), '--role', 'Read-only reviewer']
        with patch.object(sys, 'argv', argv), patch.object(agent.Agent, 'ask', return_value={}) as ask:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(agent.main(), 0)
        self.assertEqual(ask.call_args.args[:2], ('claude', self.new))
        self.assertIs(ask.call_args.kwargs['owned_partner'], False)


class SessionIdentityTests(unittest.TestCase):
    def test_ongoing_role_is_private_reused_and_explicitly_updated_without_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', '-q', directory], check=True)
            app = agent.Agent(directory)
            sid = str(uuid.uuid4())
            with patch.object(agent, 'live_target'), patch.object(app, 'ask', side_effect=AssertionError('No dispatch')):
                first = app.pair('codex', sid, 'partner', ' Independent reviewer ')
                self.assertEqual(first['partner_role'], 'Independent reviewer')
                self.assertEqual(app.pair('codex', sid, 'partner'), first)
                changed = app.pair('codex', sid, 'partner', 'Implementation partner')
                self.assertEqual(changed['partner_role'], 'Implementation partner')
                self.assertEqual({k: v for k, v in changed.items() if k != 'partner_role'},
                                 {k: v for k, v in first.items() if k != 'partner_role'})
                with self.assertRaisesRegex(ValueError, 'another session'):
                    app.pair('codex', str(uuid.uuid4()), 'partner', 'Reviewer')
            with patch.object(agent, 'codex_sessions', return_value=[]), patch.object(agent, 'claude_sessions', return_value=[]):
                self.assertEqual(app.list()['partners'][0]['partner_role'], 'Implementation partner')
            self.assertEqual(subprocess.check_output(['git', 'status', '--porcelain'], cwd=directory, text=True), '')

    def test_invalid_roles_and_worker_roles_fail_before_side_effects(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', '-q', directory], check=True)
            app = agent.Agent(directory)
            with patch.object(agent, 'live_target', side_effect=AssertionError('No native probe')):
                for role in ('', '  ', 1):
                    with self.assertRaises(ValueError):
                        app.pair('codex', str(uuid.uuid4()), 'partner', role)
                    with self.assertRaises(ValueError):
                        app.start('codex', 'partner', 'partner', '/missing', 'One job', partner_role=role)
                with self.assertRaisesRegex(ValueError, 'worker assignment'):
                    app.start('claude', 'worker', 'worker', '/missing', 'One job', partner_role='Reviewer')
            self.assertFalse(app.state.exists())

    def test_uncertain_partner_launch_retains_ongoing_role(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', '-q', directory], check=True)
            app = agent.Agent(directory)
            prompt = Path(directory) / 'prompt.md'
            prompt.write_text('Review the implementation, no edits.')
            with patch.object(agent, 'codex_home', return_value=Path(directory)), \
                 patch.object(agent, 'command', side_effect=agent.Unavailable('native offline')):
                with self.assertRaises(agent.Unavailable):
                    app.start('codex', 'partner', 'review', prompt, 'First review', partner_role='Independent reviewer')
            saved = agent.read_json(app.state / 'partners/review.json')
            self.assertEqual(saved['partner_role'], 'Independent reviewer')
            self.assertEqual(saved['status'], 'start-uncertain')

    def test_aliases_match_exact_provider_and_id_not_an_old_title(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', '-q', directory], check=True)
            app = agent.Agent(directory)
            sid, other = str(uuid.uuid4()), str(uuid.uuid4())
            with patch.object(agent, 'live_target'):
                app.pair('codex', sid, 'build-partner')
            binding = app.state / 'partners' / 'build-partner.json'
            before = binding.read_bytes()
            codex = [{'provider': 'codex', 'id': sid, 'name': 'Old setup task', 'status': 'activity unknown'},
                     {'provider': 'codex', 'id': other, 'name': 'Old setup task', 'status': 'activity unknown'}]
            claude = [{'provider': 'claude', 'id': sid, 'name': 'Old setup task', 'status': 'idle'}]
            with patch.object(agent, 'codex_sessions', return_value=codex), \
                 patch.object(agent, 'claude_sessions', return_value=claude), \
                 patch.object(agent, 'transcript', side_effect=AssertionError('Discovery must not read history')):
                rows = app.list()['sessions']
            target = next(row for row in rows if row['provider'] == 'codex' and row['id'] == sid)
            self.assertEqual(target['partner_aliases'], ['build-partner'])
            self.assertEqual(target['name'], 'Old setup task')
            self.assertEqual(target['status'], 'activity unknown')
            self.assertTrue(all(row['partner_aliases'] == [] for row in rows if row is not target))
            self.assertEqual(binding.read_bytes(), before)

    def test_multiple_aliases_group_under_one_session_and_offline_partner_stays_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', '-q', directory], check=True)
            app = agent.Agent(directory)
            sid, offline = str(uuid.uuid4()), str(uuid.uuid4())
            with patch.object(agent, 'live_target'):
                for alias in ('review-partner', 'build-partner'):
                    app.pair('claude', sid, alias)
                app.pair('claude', offline, 'old-partner')
            with patch.object(agent, 'codex_sessions', return_value=[]), \
                 patch.object(agent, 'claude_sessions', return_value=[{'provider': 'claude', 'id': sid, 'status': 'idle'}]):
                result = app.list()
            self.assertEqual(len(result['sessions']), 1)
            self.assertEqual(result['sessions'][0]['partner_aliases'], ['build-partner', 'review-partner'])
            old = next(row for row in result['partners'] if row['alias'] == 'old-partner')
            self.assertEqual(old['live_status'], 'not listed')

    def test_unpaired_discovery_creates_no_state(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['git', 'init', '-q', directory], check=True)
            app = agent.Agent(directory)
            with patch.object(agent, 'codex_sessions', return_value=[]), \
                 patch.object(agent, 'claude_sessions', return_value=[{'provider': 'claude', 'id': str(uuid.uuid4()), 'status': 'idle'}]):
                self.assertEqual(app.list()['sessions'][0]['partner_aliases'], [])
            self.assertFalse(app.state.exists())


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.app = agent.Agent(self.root)
        self.sid = str(uuid.uuid4())
        self.rid = str(uuid.uuid4())
        self.log = self.root / 'native.jsonl'
        self.log.touch()
        self.target = {'id': self.sid, 'provider': 'claude', 'pid': os.getpid()}
        self.sent = []
        self.patches = [patch.object(agent, 'live_target', return_value=self.target),
                        patch.object(agent, 'transcript', return_value=self.log),
                        patch.object(agent, 'send_claude', side_effect=self.send)]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.tmp.cleanup()

    def test_status_of_an_unknown_request_names_it_and_leaves_the_store_untouched(self):
        unknown = str(uuid.uuid4())
        with self.assertRaises(agent.Unavailable) as caught:
            self.app.status(unknown)
        self.assertIn('No request ' + unknown, str(caught.exception))
        requests = self.app.folder('requests')
        self.assertEqual([p.name for p in requests.iterdir()] if requests.exists() else [], [])

    def send(self, root, target, request, prompt, **kwargs):
        self.sent.append((target, request, prompt))
        return 'submitted-unconfirmed'

    def ask(self, prompt='Inspect the agreed result. Do not edit.'):
        return self.app.ask('claude', self.sid, prompt, 'Reviewer', self.rid)

    def append(self, text, kind='assistant', mid=None):
        with self.log.open('a') as stream:
            message = {'content': [{'type': 'text', 'text': text}]}
            if mid is not None:
                message['id'] = mid
            stream.write(json.dumps({'type': kind, 'message': message}) + '\n')

    def answer(self, text='Finding: keep the complete qualification.', rid=None):
        begin, end = agent.markers(rid or self.rid)
        self.append(begin + text + end)

    def test_delivery_is_not_a_reply(self):
        self.assertEqual(self.ask()['status'], 'submitted-unconfirmed')
        self.assertEqual(self.app.wait(self.rid, 0)['status'], 'submitted-unconfirmed')
        self.assertEqual(len(self.sent), 1)

    def test_complete_answer_is_archived_and_survives_log_removal(self):
        self.ask()
        self.answer()
        result = self.app.status(self.rid)
        self.assertEqual(result['reply'], 'Finding: keep the complete qualification.')
        self.assertEqual(result['status'], 'reply-received')
        self.log.unlink()
        self.assertEqual(self.app.status(self.rid), result)

    def test_no_reply_from_user_text_or_other_request(self):
        self.ask()
        begin, end = agent.markers(self.rid)
        self.append(begin + 'Not an answer' + end, 'user')
        self.answer(rid=str(uuid.uuid4()))
        self.assertNotIn('reply', self.app.status(self.rid))

    def test_no_reply_from_prefix_or_partial_json(self):
        self.ask()
        begin, end = agent.markers(self.rid)
        self.append(begin + 'Cut short')
        with self.log.open('a') as stream:
            stream.write(json.dumps({'type': 'assistant', 'message': {
                'content': [{'type': 'text', 'text': begin + 'Complete' + end}]}}))
        self.assertNotIn('reply', self.app.status(self.rid))
        with self.log.open('a') as stream:
            stream.write('\n')
        self.assertEqual(self.app.status(self.rid)['reply'], 'Complete')

    def test_history_before_submission_is_not_consulted(self):
        self.answer('Old answer')
        self.ask()
        self.assertNotIn('reply', self.app.status(self.rid))
        self.answer('New answer')
        self.assertEqual(self.app.status(self.rid)['reply'], 'New answer')

    def test_complete_reply_across_assistant_events_preserves_ending(self):
        self.ask()
        begin, end = agent.markers(self.rid)
        self.append(begin + 'The finding is conditional', mid='m1')
        self.assertNotIn('reply', self.app.status(self.rid))
        self.append(' on the last qualification being retained.' + end, mid='m1')
        self.assertEqual(self.app.status(self.rid)['reply'],
                         'The finding is conditional on the last qualification being retained.')

    def test_codex_reply_across_native_message_items_is_complete(self):
        self.app.new_request('codex', self.sid, 'Job', 'Reviewer', self.rid, self.log)
        begin, end = agent.markers(self.rid)
        with self.log.open('a') as stream:
            for text in (begin + 'First half', ' and the qualifying second half.' + end):
                stream.write(json.dumps({'type': 'response_item', 'payload': {
                    'type': 'message', 'role': 'assistant', 'id': 'item-1',
                    'content': [{'type': 'output_text', 'text': text}]}}) + '\n')
        self.assertEqual(self.app.status(self.rid)['reply'], 'First half and the qualifying second half.')

    def test_split_reply_does_not_absorb_another_request_answer(self):
        self.ask()
        begin, end = agent.markers(self.rid)
        self.append(begin + 'First fragment')
        self.answer('Other answer', rid=str(uuid.uuid4()))
        self.append('Last fragment' + end)
        self.assertEqual(self.app.status(self.rid)['status'], 'observation-unavailable')

    def test_subdirectory_session_is_discovered_but_nested_repo_is_not(self):
        docs = self.root / 'docs'
        docs.mkdir()
        nested = self.root / 'nested'
        subprocess.run(['git', 'init', '-q', str(nested)], check=True)
        original = agent.command
        def commands(args, cwd=None):
            if args[:2] == ['claude', 'agents']:
                return json.dumps([{'sessionId': self.sid, 'cwd': str(docs), 'pid': 123},
                    {'sessionId': str(uuid.uuid4()), 'cwd': str(nested), 'pid': 456}])
            return original(args, cwd)
        with patch.object(agent, 'command', side_effect=commands):
            rows = agent.claude_sessions(self.root)
        self.assertEqual([row['pid'] for row in rows], [123])

    def test_codex_discovery_returns_partial_rows_and_normalized_status(self):
        from unittest.mock import MagicMock
        rpc = MagicMock()
        rpc.__enter__.return_value = rpc
        rpc.call.side_effect = [{'data': [self.sid, str(uuid.uuid4())], 'nextCursor': None},
            {'thread': {'cwd': str(self.root), 'status': {'type': 'active'}}},
            agent.Unavailable('Discovery deadline reached')]
        notes = {}
        with patch.object(agent, 'RPC', return_value=rpc) as constructor:
            rows = agent.codex_sessions(self.root, notes)
        self.assertEqual(rows[0]['status'], 'active')
        self.assertIn('Partial discovery', notes['codex'])
        self.assertIsInstance(constructor.call_args.kwargs['deadline'], float)

    def test_partner_retry_reports_alias_without_exposing_private_path(self):
        prompt = self.root / 'prompt.md'
        prompt.write_text('Actual job')
        self.app.pair('claude', self.sid, 'reviewer')
        with self.assertRaises(ValueError) as raised:
            self.app.start('claude', 'partner', 'reviewer', prompt, 'Reviewer')
        self.assertIn('Partner alias already used', str(raised.exception))
        self.assertNotIn(str(self.app.state), str(raised.exception))

    def test_same_request_never_queues_twice(self):
        self.ask()
        self.ask()
        self.assertEqual(len(self.sent), 1)
        with self.assertRaisesRegex(ValueError, 'different work'):
            self.ask('Different prompt')

    def test_uncertain_send_is_saved_and_not_retried(self):
        with patch.object(agent, 'send_claude', side_effect=OSError('connection lost')):
            result = self.ask()
        self.assertEqual(result['status'], 'delivery-uncertain')
        self.ask()
        self.assertEqual(self.sent, [])

    def test_unreachable_or_wrong_project_fails_before_submission(self):
        with patch.object(agent, 'live_target', side_effect=agent.Unavailable('wrong project')):
            with self.assertRaises(agent.Unavailable):
                self.ask()
        self.assertEqual(self.sent, [])
        self.assertFalse((self.app.state / 'requests' / (self.rid + '.json')).exists())

    def test_native_log_replacement_does_not_restart_reading_history(self):
        self.ask()
        self.log.rename(self.root / 'prior.jsonl')
        self.log.touch()
        self.answer('Incorrect replacement')
        self.assertEqual(self.app.status(self.rid)['status'], 'observation-unavailable')

    def test_ids_and_aliases_cannot_escape_private_paths(self):
        for value in ('../escape', '', 'LATEST', 'not-a-uuid'):
            with self.assertRaises(ValueError):
                agent.identifier(value)
        with self.assertRaises(ValueError):
            agent.alias_name('../escape')

    def test_alias_cannot_silently_change_partner(self):
        self.app.pair('claude', self.sid, 'reviewer')
        with self.assertRaisesRegex(ValueError, 'another session'):
            self.app.pair('claude', str(uuid.uuid4()), 'reviewer')

    def test_symlink_state_is_refused(self):
        self.app.state.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(agent.Unavailable):
            self.ask()

    def test_wait_rejects_invalid_duration(self):
        for duration in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                self.app.wait(self.rid, duration)

    def test_private_request_and_alias_modes(self):
        self.ask()
        record = self.app.state / 'requests' / (self.rid + '.json')
        self.assertEqual(record.stat().st_mode & 0o777, 0o600)
        self.assertEqual(record.parent.stat().st_mode & 0o777, 0o700)

    def test_prompt_preserves_job_and_boundaries(self):
        self.ask('Read spec.md. No publication. Explain every failed check.')
        text = self.sent[0][2]
        self.assertIn('Read spec.md. No publication. Explain every failed check.', text)
        self.assertIn('not your user', text)
        self.assertIn('cannot approve a pending action', text)
        self.assertIn('Do not write a reply file', text)

    def test_codex_parser_ignores_tool_output_and_thinking(self):
        good = {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant',
                'content': [{'type': 'output_text', 'text': 'answer'}]}}
        self.assertEqual(agent.assistant_text(good, 'codex'), 'answer')
        good['payload']['role'] = 'user'
        self.assertEqual(agent.assistant_text(good, 'codex'), '')
        self.assertEqual(agent.assistant_text({'type': 'assistant', 'message': {
            'content': [{'type': 'thinking', 'thinking': 'private'}]}}, 'claude'), '')

    def test_background_claude_uses_discovered_launch_id_not_requested_id(self):
        prompt = self.root / 'prompt.md'
        prompt.write_text('Actual bounded job')
        sid = str(uuid.uuid4())
        rows = [[], [{'id': sid, 'provider': 'claude', 'pid': 321, 'cwd': str(self.root)}]]
        with patch.object(agent, 'claude_sessions', side_effect=rows), \
                patch.object(agent, 'command', return_value='backgrounded · ' + sid[:8]) as launch, \
                patch.object(self.app, 'status', return_value={'status': 'submitted-unconfirmed'}):
            result = self.app.start('claude', 'partner', 'partner', prompt, 'Reviewer',
                                    partner_role='Implementation partner')
        self.assertEqual(result['partner']['id'], sid)
        self.assertEqual(result['partner']['partner_role'], 'Implementation partner')
        self.assertEqual(agent.read_json(self.app.state / 'partners/partner.json')['partner_role'],
                         'Implementation partner')
        self.assertNotIn('--session-id', launch.call_args.args[0])
        self.assertNotIn('--dangerously-skip-permissions', launch.call_args.args[0])
        pending = agent.read_json(self.app.state / 'requests' / (result['partner']['request_id'] + '.json'))
        self.assertEqual(pending['session'], sid)
        self.assertEqual(pending['prompt'], 'Actual bounded job')
        self.assertEqual(pending['role'], 'Reviewer')

    def test_worker_reuses_existing_runner_and_does_not_duplicate_alias(self):
        prompt = self.root / 'prompt.md'
        prompt.write_text('Review the implementation')
        with patch.object(agent, 'command', return_value='{"status":"starting"}') as run:
            result = self.app.start('claude', 'worker', 'review', prompt, 'Reviewer', model='chosen-model', effort='high')
            with self.assertRaisesRegex(ValueError, 'already used'):
                self.app.start('claude', 'worker', 'review', prompt, 'Reviewer')
        args = run.call_args.args[0]
        self.assertIn('conductor/scripts/ask.py', args[2])
        self.assertIn('--background', args)
        self.assertIn('--request-id', args)
        self.assertNotIn('--write', args)
        self.assertEqual(result['result']['status'], 'starting')
        self.assertEqual(run.call_count, 1)

    def test_native_rpc_matches_response_id_without_accepting_notifications(self):
        rpc = agent.RPC.__new__(agent.RPC)
        rpc.counter = 0
        rpc.deadline = None
        rpc.native_errors = (OSError,)
        from unittest.mock import Mock
        rpc.channel = Mock()
        rpc.channel.recv.side_effect = [json.dumps({'id': 99, 'result': 'wrong'}),
            json.dumps({'method': 'turn/completed', 'params': {'unrelated': True}}),
            json.dumps({'id': 1, 'result': {'correct': True}})]
        self.assertEqual(rpc.call('thread/read', {'threadId': self.sid}), {'correct': True})
        self.assertEqual(json.loads(rpc.channel.send.call_args.args[0])['params']['threadId'], self.sid)


class NativeBoundaryTests(unittest.TestCase):
    def test_real_claude_socket_receives_exact_session_and_next_priority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'sessions').mkdir()
            endpoint = root / 'peer.sock'
            sid, rid = str(uuid.uuid4()), str(uuid.uuid4())
            pid = os.getpid()
            agent.atomic_json(root / 'sessions' / (str(pid) + '.json'), {
                'sessionId': sid, 'pid': pid, 'cwd': str(root), 'messagingSocketPath': str(endpoint)})
            received = []
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
                server.bind(str(endpoint))
                server.listen(1)
                server.settimeout(3)
                def read():
                    client, _ = server.accept()
                    with client:
                        with client.makefile('r') as stream:
                            received.append(json.loads(stream.readline()))
                thread = threading.Thread(target=read)
                thread.start()
                with patch.object(agent, 'claude_home', return_value=root):
                    state = agent.send_claude(root, {'id': sid, 'pid': pid}, rid, 'Bounded contribution')
                thread.join(timeout=4)
                self.assertFalse(thread.is_alive())
            self.assertEqual(state, 'submitted-unconfirmed')
            self.assertEqual(received[0]['session_id'], sid)
            self.assertEqual(received[0]['uuid'], rid)
            self.assertEqual(received[0]['priority'], 'next')
            self.assertEqual(received[0]['message']['content'], 'Bounded contribution')
            self.assertNotIn('token', received[0])

    def test_discovery_does_not_cross_project_or_invent_live_sessions(self):
        rows = [{'sessionId': str(uuid.uuid4()), 'cwd': '/tmp/one', 'pid': 10, 'status': 'idle'},
                {'sessionId': str(uuid.uuid4()), 'cwd': '/tmp/two', 'pid': 20, 'status': 'busy'}]
        with patch.object(agent, 'command', return_value=json.dumps(rows)):
            found = agent.claude_sessions('/tmp/one')
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]['pid'], 10)


if __name__ == '__main__':
    unittest.main()


class FakeCodexHome:
    """A private CODEX_HOME with a threads store and a rollout, no daemon."""

    def __init__(self, root):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name).resolve()
        (self.home / 'sessions').mkdir()
        self.db = self.home / 'state_5.sqlite'
        import sqlite3
        with sqlite3.connect(self.db) as c:
            c.execute('CREATE TABLE threads (id TEXT, cwd TEXT, rollout_path TEXT, name TEXT, '
                      'archived INTEGER, source TEXT, thread_source TEXT, updated_at INTEGER)')
        self.root = root
        self.env = patch.dict(os.environ, {'CODEX_HOME': str(self.home)})
        self.env.start()

    def thread(self, sid, cwd=None, archived=0, name='tui', thread_source='user', updated_at=1, source='cli'):
        import sqlite3
        log = self.home / 'sessions' / (sid + '.jsonl'); log.touch()
        with sqlite3.connect(self.db) as c:
            c.execute('INSERT INTO threads VALUES (?,?,?,?,?,?,?,?)',
                      (sid, cwd or str(self.root), str(log), name, archived, source, thread_source, updated_at))
        return log

    def close(self):
        self.env.stop(); self.tmp.cleanup()


def codex_event(text, phase='final_answer'):
    payload = {'type': 'message', 'role': 'assistant',
               'content': [{'type': 'output_text', 'text': text}]}
    if phase is not None:
        payload['phase'] = phase
    return {'type': 'response_item', 'payload': payload}


class CommentaryIsNotAReplyTests(unittest.TestCase):
    """Codex streams 'commentary' before its 'final_answer'. A marker quoted in
    commentary — say, in a fenced example — must never be archived as the reply."""

    def test_commentary_carrying_a_complete_marker_pair_is_ignored(self):
        begin, end = agent.markers('r')
        text = 'Here is the protocol:\n```\n' + begin + 'NOT A FINAL REVIEW' + end + '\n```'
        self.assertEqual(agent.assistant_text(codex_event(text, 'commentary'), 'codex'), '')

    def test_final_answer_text_is_read(self):
        self.assertEqual(agent.assistant_text(codex_event('answer', 'final_answer'), 'codex'), 'answer')

    def test_an_event_without_phase_is_read_by_explicit_policy(self):
        """Older rollouts carry no phase. Only a DECLARED commentary is excluded."""
        self.assertEqual(agent.assistant_text(codex_event('answer', None), 'codex'), 'answer')


class TuiRouteTests(unittest.TestCase):
    """A Codex TUI is a store-resident thread with no daemon. Reach it with
    `codex queue --thread`, decide the route once, and never send twice."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.codex = FakeCodexHome(self.root)
        self.app = agent.Agent(self.root)
        self.sid = str(uuid.uuid4()); self.rid = str(uuid.uuid4())
        self.log = self.codex.thread(self.sid)
        self.calls = []
        self.no_daemon = patch.object(agent, 'RPC', side_effect=agent.Unavailable('no socket'))
        self.no_daemon.start()

    def tearDown(self):
        self.no_daemon.stop(); self.codex.close(); self.tmp.cleanup()

    def fake_command(self, args, cwd=None, timeout=30):
        self.calls.append(args)
        if args[:2] == ['git', '-C']:
            return str(self.root) + '\n'
        return ''

    def test_live_target_accepts_a_saved_thread_and_says_activity_is_unknown(self):
        with patch.object(agent, 'command', side_effect=self.fake_command):
            target = agent.live_target(self.root, 'codex', self.sid)
        self.assertEqual(target['reachability'], 'native-thread')
        self.assertIn('activity unknown', target['status'])

    def test_live_target_refuses_an_archived_thread(self):
        dead = str(uuid.uuid4()); self.codex.thread(dead, archived=1)
        with patch.object(agent, 'command', side_effect=self.fake_command):
            with self.assertRaises(agent.Unavailable):
                agent.live_target(self.root, 'codex', dead)

    def test_live_target_refuses_a_thread_from_another_project(self):
        other = str(uuid.uuid4()); self.codex.thread(other, cwd='/tmp')
        with patch.object(agent, 'command', side_effect=self.fake_command):
            with self.assertRaises(agent.Unavailable):
                agent.live_target(self.root, 'codex', other)

    def test_ask_sends_once_via_codex_queue_with_cd_before_the_subcommand(self):
        with patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        sends = [a for a in self.calls if a[:1] == ['codex']]
        self.assertEqual(len(sends), 1, 'exactly one enqueue')
        args = sends[0]
        self.assertEqual(args[:2], ['codex', 'queue'])
        self.assertEqual(args[args.index('--cd') + 1], str(self.root))
        self.assertEqual(args[args.index('--thread') + 1], self.sid)
        self.assertIn('--message', args)
        self.assertIn(agent.markers(self.rid)[0], args[args.index('--message') + 1])
        self.assertEqual(record['status'], 'submitted-unconfirmed')
        self.assertEqual(record.get('route'), 'codex-queue')

    def test_uncertain_enqueue_is_retained_and_never_resent(self):
        def flaky(args, cwd=None, timeout=30):
            self.calls.append(args)
            if args[:1] == ['codex']:
                raise subprocess.TimeoutExpired(args, timeout)
            return self.fake_command(args, cwd, timeout)
        with patch.object(agent, 'command', side_effect=flaky):
            first = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
            second = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        self.assertIn('error', first)
        self.assertNotIn('Review it.', first['error'], 'a timeout must not retain the prompt')
        self.assertNotIn(str(self.root), first['error'], 'nor the project path')
        self.assertEqual(first['status'], 'delivery-uncertain')
        self.assertEqual(second['request_id'], first['request_id'])
        self.assertEqual(sum(1 for a in self.calls if a[:1] == ['codex']), 1)

    def test_reply_is_read_from_the_tui_rollout_by_markers(self):
        with patch.object(agent, 'command', side_effect=self.fake_command):
            self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
            begin, end = agent.markers(self.rid)
            with self.log.open('a') as f:
                f.write(json.dumps(codex_event('thinking about ' + begin, 'commentary')) + '\n')
                f.write(json.dumps(codex_event(begin + 'Finding: keep it.' + end)) + '\n')
            record = self.app.status(self.rid)
        self.assertEqual(record['status'], 'reply-received')
        self.assertEqual(record['reply'], 'Finding: keep it.')

    def test_discovery_lists_saved_threads_without_the_daemon_or_websockets(self):
        other = str(uuid.uuid4()); self.codex.thread(other, cwd='/tmp')
        dead = str(uuid.uuid4()); self.codex.thread(dead, archived=1)
        spawned = str(uuid.uuid4()); self.codex.thread(spawned, thread_source='subagent')
        with patch.object(agent, 'command', side_effect=self.fake_command):
            listing = self.app.list()
        ids = {row['id'] for row in listing['sessions'] if row['provider'] == 'codex'}
        self.assertEqual(ids, {self.sid})
        row = next(r for r in listing['sessions'] if r['id'] == self.sid)
        self.assertEqual(row['reachability'], 'native-thread')

    def test_two_interleaved_requests_each_receive_only_their_own_reply(self):
        """Two requests in flight on one thread, answered out of order: each
        request reads from its own offset and matches only its own markers."""
        second = str(uuid.uuid4())
        with patch.object(agent, 'command', side_effect=self.fake_command):
            self.app.ask('codex', self.sid, 'First question.', 'Reviewer', self.rid)
            self.app.ask('codex', self.sid, 'Second question.', 'Reviewer', second)
            b1, e1 = agent.markers(self.rid); b2, e2 = agent.markers(second)
            with self.log.open('a') as f:
                f.write(json.dumps(codex_event(b2 + 'answer two' + e2)) + '\n')
                f.write(json.dumps(codex_event(b1 + 'answer one' + e1)) + '\n')
            one, two = self.app.status(self.rid), self.app.status(second)
        self.assertEqual((one['status'], one['reply']), ('reply-received', 'answer one'))
        self.assertEqual((two['status'], two['reply']), ('reply-received', 'answer two'))


class OneRouteOneSendTests(TuiRouteTests):
    """With a daemon present, the app-server route is taken — and the CLI route
    must not fire, whether the daemon send succeeded or went uncertain."""

    def setUp(self):
        super().setUp()
        self.no_daemon.stop()  # this class supplies its own daemon behaviour
        sock = self.codex.home / 'app-server-control'; sock.mkdir()
        (sock / 'app-server-control.sock').touch()  # existence is all daemon_socket() checks

    def tearDown(self):
        self.no_daemon.start()  # so the parent tearDown can stop it
        super().tearDown()

    def rpc(self, *responses):
        from unittest.mock import MagicMock
        rpc = MagicMock(); rpc.__enter__.return_value = rpc
        rpc.call.side_effect = list(responses)
        return patch.object(agent, 'RPC', return_value=rpc)

    def test_daemon_success_means_no_cli_enqueue(self):
        loaded = {'thread': {'cwd': str(self.root), 'status': {'type': 'active'}}}
        with self.rpc(loaded, loaded, {'queuedSubmission': {'id': 'q1'}}), \
             patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        self.assertEqual((record['status'], record['route']), ('queued', 'app-server'))
        self.assertEqual([a for a in self.calls if a[:1] == ['codex']], [], 'CLI must not fire')

    def test_daemon_uncertainty_mid_send_never_falls_back_to_cli(self):
        loaded = {'thread': {'cwd': str(self.root), 'status': {'type': 'active'}}}
        with self.rpc(loaded, loaded, agent.Unavailable('Native RPC timed out; delivery may be uncertain')), \
             patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        self.assertEqual(record['status'], 'delivery-uncertain')
        self.assertIn('uncertain', record.get('error', ''))
        self.assertEqual([a for a in self.calls if a[:1] == ['codex']], [], 'no second send on another route')


class OpusReviewTests(TuiRouteTests):
    """Findings from the cross-model review of the TUI route, each pinned."""

    def test_F1_unowned_app_server_thread_the_daemon_reports_offline_is_refused_not_queued(self):
        """For an app-server-created thread (source='vscode'), notLoaded and not
        ours means the owner's session is offline: refuse, never `codex queue` it.
        (A TUI is different — see the final-review tests — the daemon reports
        every TUI as notLoaded because it never loads them.)"""
        import sqlite3
        with sqlite3.connect(self.codex.db) as c:
            c.execute("UPDATE threads SET source='vscode' WHERE id=?", (self.sid,))
        self.no_daemon.stop()
        sock = self.codex.home / 'app-server-control'; sock.mkdir(exist_ok=True)
        (sock / 'app-server-control.sock').touch()
        from unittest.mock import MagicMock
        rpc = MagicMock(); rpc.__enter__.return_value = rpc
        offline = {'thread': {'cwd': str(self.root), 'status': {'type': 'notLoaded'}}}
        rpc.call.side_effect = [offline, offline]
        try:
            with patch.object(agent, 'RPC', return_value=rpc), \
                 patch.object(agent, 'command', side_effect=self.fake_command):
                record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        finally:
            self.no_daemon.start()
        self.assertEqual(record['status'], 'delivery-uncertain')
        self.assertIn('offline', record.get('error', ''))
        self.assertEqual([a for a in self.calls if a[:1] == ['codex']], [], 'no enqueue to an offline unowned thread')

    def test_F2_a_moved_rollout_reports_observation_unavailable_without_a_path(self):
        with patch.object(agent, 'command', side_effect=self.fake_command):
            self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
            self.log.rename(self.log.with_suffix('.archived'))
            record = self.app.status(self.rid)
        self.assertEqual(record['status'], 'observation-unavailable')
        # The path stays in the private record; it must not ride the error text
        # that the CLI prints.
        self.assertNotIn(str(self.codex.home), record['error'])

    def test_F3_only_final_answer_or_unphased_text_counts(self):
        for phase in ('analysis', 'reasoning', 'commentary'):
            self.assertEqual(agent.assistant_text(codex_event('X', phase), 'codex'), '', phase)
        self.assertEqual(agent.assistant_text(codex_event('X', 'final_answer'), 'codex'), 'X')
        self.assertEqual(agent.assistant_text(codex_event('X', None), 'codex'), 'X')

    def test_F4_exec_runs_are_not_listed_and_hidden_threads_cannot_be_selected(self):
        import sqlite3
        exec_run = str(uuid.uuid4()); self.codex.thread(exec_run)
        spawned = str(uuid.uuid4()); self.codex.thread(spawned, thread_source='subagent')
        with sqlite3.connect(self.codex.db) as c:
            c.execute("UPDATE threads SET source='exec' WHERE id=?", (exec_run,))
        with patch.object(agent, 'command', side_effect=self.fake_command):
            listed = {r['id'] for r in self.app.list()['sessions'] if r['provider'] == 'codex'}
            self.assertEqual(listed, {self.sid})
            for hidden in (exec_run, spawned):
                with self.assertRaises(agent.Unavailable):
                    agent.live_target(self.root, 'codex', hidden)
                with self.assertRaises(agent.Unavailable):
                    agent.stored_thread(self.root, hidden)

    def test_F5_cd_follows_the_queue_subcommand(self):
        with patch.object(agent, 'command', side_effect=self.fake_command):
            self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        args = next(a for a in self.calls if a[:1] == ['codex'])
        self.assertEqual(args[1], 'queue')
        self.assertEqual(args[args.index('--cd') + 1], str(self.root))
        self.assertGreater(args.index('--cd'), args.index('queue'))

    def test_F7_an_owned_partner_whose_store_row_moved_project_is_not_sent(self):
        import sqlite3
        with sqlite3.connect(self.codex.db) as c:
            c.execute("UPDATE threads SET cwd='/tmp' WHERE id=?", (self.sid,))
        # fresh=True skips transcript(), so the pre-send stored_thread() check
        # in send_codex is the only project guard on this path — the one the
        # review's mutation deleted without a test noticing.
        with patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid,
                                  fresh=True, owned_partner=True)
        self.assertEqual(record['status'], 'delivery-uncertain')
        self.assertIn('another project', record.get('error', ''))
        self.assertEqual([a for a in self.calls if a[:1] == ['codex']], [])

    def test_followup_one_unresolvable_cwd_does_not_hide_later_threads(self):
        later = str(uuid.uuid4()); self.codex.thread(later)
        ghost = str(uuid.uuid4()); self.codex.thread(ghost, cwd=str(self.root / 'gone'), updated_at=9)  # newest: scanned first
        def cmd(args, cwd=None, timeout=30):
            if args[:2] == ['git', '-C'] and 'gone' in args[2]:
                raise agent.Unavailable('not a git repository')
            return self.fake_command(args, cwd, timeout)
        with patch.object(agent, 'command', side_effect=cmd):
            listed = {r['id'] for r in self.app.list()['sessions'] if r['provider'] == 'codex'}
        self.assertEqual(listed, {self.sid, later})


class ReleaseFollowupTests(unittest.TestCase):
    setUp = QueueTests.setUp
    tearDown = QueueTests.tearDown
    send = QueueTests.send
    ask = QueueTests.ask

    def append_event(self, provider, text, mid):
        if provider == 'claude':
            event = {'type': 'assistant', 'message': {'id': mid,
                     'content': [{'type': 'text', 'text': text}]}}
        else:
            event = {'type': 'response_item', 'payload': {'id': mid,
                     'type': 'message', 'role': 'assistant', 'phase': 'final_answer',
                     'content': [{'type': 'output_text', 'text': text}]}}
        with self.log.open('a') as stream:
            stream.write(json.dumps(event) + '\n')

    def test_marker_mention_then_update_never_freezes_a_false_reply(self):
        for provider in ('claude', 'codex'):
            for poll_between in (False, True):
                for suffix in ('', ' after reading.'):
                    with self.subTest(provider=provider, poll=poll_between, suffix=suffix):
                        rid = str(uuid.uuid4())
                        self.app.new_request(provider, self.sid, 'Review', 'Reviewer', rid, self.log)
                        begin, end = agent.markers(rid)
                        self.append_event(provider, f'I will use {begin} and {end}' + suffix, 'mention')
                        if poll_between:
                            self.assertNotIn('reply', self.app.status(rid))
                        self.append_event(provider, 'Still reviewing.', 'update')
                        self.assertNotIn('reply', self.app.status(rid))
                        self.append_event(provider, begin + '\nThe complete finding.\n' + end, 'answer')
                        self.assertEqual(self.app.status(rid)['reply'], 'The complete finding.')

    def test_valid_opening_split_across_events_is_still_retrieved(self):
        for provider in ('claude', 'codex'):
            with self.subTest(provider=provider):
                rid = str(uuid.uuid4())
                self.app.new_request(provider, self.sid, 'Review', 'Reviewer', rid, self.log)
                begin, end = agent.markers(rid)
                self.append_event(provider, begin[:12], 'answer')
                self.assertNotIn('reply', self.app.status(rid))
                self.append_event(provider, begin[12:] + '\nFinding with ', 'answer')
                self.append_event(provider, 'its qualification.\n' + end, 'answer')
                self.assertEqual(self.app.status(rid)['reply'], 'Finding with its qualification.')

    def test_oversize_preflight_uses_serialized_frame_before_recording(self):
        # Escaping makes this exceed the cap even though the raw text fits.
        with patch.object(agent, 'FRAME_LIMIT', 2000), patch('socket.socket') as socket_call:
            with self.assertRaisesRegex(agent.Unavailable, 'frame limit'):
                self.ask('\U0001f600' * 200)
            self.assertFalse(list((self.app.state / 'requests').glob('*.json')))
            self.assertEqual(self.sent, [])
            socket_call.assert_not_called()

    def test_prepared_frame_is_exact_and_retry_does_not_send_again(self):
        with patch.object(agent, 'send_claude', return_value='submitted-unconfirmed') as send:
            result = self.ask('Read café and "quotes".\nNo edits.')
            frame = send.call_args.kwargs['frame']
            decoded = json.loads(frame)
            self.assertEqual(decoded['session_id'], self.sid)
            self.assertEqual(decoded['uuid'], self.rid)
            self.assertEqual(decoded['message']['content'], send.call_args.args[3])
            with patch.object(agent, 'FRAME_LIMIT', 1):
                self.assertEqual(self.ask('Read café and "quotes".\nNo edits.'), result)
            self.assertEqual(send.call_count, 1)

    def test_attempted_claude_timeout_stays_recorded_without_resend(self):
        timeout = subprocess.TimeoutExpired(['claude', 'private-prompt'], 5)
        with patch.object(agent, 'send_claude', side_effect=timeout) as send:
            record = self.ask()
            self.assertEqual(record['status'], 'delivery-uncertain')
            self.assertIn('timed out', record['error'])
            self.assertNotIn('private-prompt', record['error'])
            self.assertEqual(self.ask(), record)
            self.assertEqual(send.call_count, 1)


class FableFoundationTests(QueueTests):
    """Findings from the cross-model review of the committed foundation."""

    def test_1_a_prose_mention_of_both_markers_is_not_a_reply(self):
        self.ask()
        begin, end = agent.markers(self.rid)
        self.append(f'Understood. I will put the answer between {begin} and {end} once I have read the files.')
        self.assertNotEqual(self.app.status(self.rid)['status'], 'reply-received')
        self.answer('The real answer.')
        self.assertEqual(self.app.status(self.rid)['reply'], 'The real answer.')

    def test_1_the_framed_prompt_never_places_the_markers_adjacent(self):
        text = agent.framed_prompt(self.root, self.rid, 'Reviewer', 'Do it.')
        begin, end = agent.markers(self.rid)
        between = text[text.index(begin) + len(begin):text.index(end)]
        self.assertGreater(len(between.strip()), 20, 'markers adjacent in the prompt invite an echo that parses as a reply')

    def test_3_owned_and_main_report_no_private_path(self):
        missing = self.root / 'nowhere' / 'x.sock'
        with self.assertRaises((agent.Unavailable, OSError)) as caught:
            agent.owned(missing, stat.S_ISREG)
        self.assertNotIn(str(self.root), str(caught.exception))
        import io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err), patch.object(sys, 'argv',
                ['agent.py', '--project', str(self.root), 'ask', '--alias', 'nobody',
                 '--prompt-file', '/dev/null', '--role', 'r']):
            self.assertEqual(agent.main(), 2)
        self.assertNotIn(str(self.root), err.getvalue())
        self.assertIn('nobody', err.getvalue())

    def test_5_an_oversized_frame_is_refused_before_any_record_is_written(self):
        huge = 'x' * 1_100_000
        for item in self.patches: item.stop()  # the real send_claude, not the fixture's mock
        try:
            with self.assertRaises(agent.Unavailable) as caught:
                agent.send_claude(self.root, self.target, self.rid, huge)
        finally:
            for item in self.patches: item.start()
        self.assertIn('frame limit', str(caught.exception))
        self.assertFalse(list((self.app.state / 'requests').glob('*.json')) if (self.app.state / 'requests').exists() else [])

    def test_identity_recheck_before_socket_write_binds(self):
        """Mutation gap from the review: dropping send_claude's identity re-check
        was not caught. This pins it."""
        for item in self.patches: item.stop()
        meta = agent.claude_home() / 'sessions' / f"{self.target['pid']}.json"
        written = []
        try:
            with patch.object(agent, 'claude_home', return_value=self.root), \
                 patch.object(agent, 'read_json', return_value={'sessionId': 'someone-else',
                              'pid': self.target['pid'], 'cwd': str(self.root),
                              'messagingSocketPath': 'uds:/nonexistent'}), \
                 patch('socket.socket', side_effect=lambda *a, **k: written.append(1)):
                with self.assertRaises(agent.Unavailable) as caught:
                    agent.send_claude(self.root, self.target, self.rid, 'hello')
        finally:
            for item in self.patches: item.start()
        self.assertIn('identity', str(caught.exception))
        self.assertEqual(written, [], 'no socket opened after an identity mismatch')

    def test_followup_one_bad_claude_row_does_not_abort_the_listing(self):
        rows = [{'sessionId': 'not-a-uuid', 'cwd': str(self.root), 'pid': 1},
                {'sessionId': self.sid, 'cwd': str(self.root), 'pid': 2, 'status': 'idle'}]
        for item in self.patches: item.stop()
        try:
            with patch.object(agent, 'command', return_value=json.dumps(rows)):
                found = agent.claude_sessions(self.root)
        finally:
            for item in self.patches: item.start()
        self.assertEqual([r['id'] for r in found], [self.sid])

    def test_followup_a_changed_daemon_page_shape_does_not_lose_claude_rows(self):
        from unittest.mock import MagicMock
        rpc = MagicMock(); rpc.__enter__.return_value = rpc
        rpc.call.side_effect = [{'unexpected': 'shape'}]
        for item in self.patches: item.stop()
        try:
            with patch.object(agent, 'RPC', return_value=rpc), \
                 patch.object(agent, 'claude_sessions', return_value=[{'provider': 'claude', 'id': self.sid,
                              'name': 'me', 'cwd': str(self.root), 'pid': 1, 'status': 'idle',
                              'reachability': 'native-listed', 'kind': 'interactive'}]):
                listing = self.app.list()
        finally:
            for item in self.patches: item.start()
        self.assertEqual([r['id'] for r in listing['sessions'] if r['provider'] == 'claude'], [self.sid])
        self.assertIn('codex', listing['unavailable'])


class FinalReviewTests(TuiRouteTests):
    """Findings from the final cross-model pass over the whole diff."""

    def daemon(self, *responses):
        """A daemon that knows the thread but never loads it — how every TUI looks."""
        from unittest.mock import MagicMock
        self.no_daemon.stop()
        sock = self.codex.home / 'app-server-control'; sock.mkdir(exist_ok=True)
        (sock / 'app-server-control.sock').touch()
        rpc = MagicMock(); rpc.__enter__.return_value = rpc
        rpc.call.side_effect = list(responses)
        return patch.object(agent, 'RPC', return_value=rpc)

    def tearDown(self):
        try:
            self.no_daemon.start()
        except RuntimeError:
            pass
        super().tearDown()

    def test_1_a_tui_takes_codex_queue_even_when_a_daemon_reports_it_not_loaded(self):
        offline = {'thread': {'cwd': str(self.root), 'status': {'type': 'notLoaded'}}}
        with self.daemon(offline, offline), patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
        self.assertEqual((record['status'], record['route']), ('submitted-unconfirmed', 'codex-queue'))
        self.assertEqual(sum(1 for a in self.calls if a[:1] == ['codex']), 1)

    def test_4_an_owned_app_server_partner_with_no_daemon_is_told_the_server_is_down(self):
        import sqlite3
        with sqlite3.connect(self.codex.db) as c:
            c.execute("UPDATE threads SET source='vscode' WHERE id=?", (self.sid,))
        with patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid,
                                  fresh=True, owned_partner=True)
        self.assertEqual(record['status'], 'delivery-uncertain')
        self.assertIn('not running', record['error'])
        self.assertEqual([a for a in self.calls if a[:1] == ['codex']], [])

    def test_2_a_block_ending_in_a_prose_mention_is_not_a_reply(self):
        with patch.object(agent, 'command', side_effect=self.fake_command):
            self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid)
            begin, end = agent.markers(self.rid)
            with self.log.open('a') as f:
                f.write(json.dumps(codex_event(f"Sure. I'll place the answer between {begin} and {end}")) + '\n')
            self.assertNotEqual(self.app.status(self.rid)['status'], 'reply-received')
            with self.log.open('a') as f:
                f.write(json.dumps(codex_event(f"{begin}\nThe real answer.\n{end}")) + '\n')
            self.assertEqual(self.app.status(self.rid)['reply'], 'The real answer.')

    def test_5_the_full_window_note_survives_a_daemon_note(self):
        import sqlite3
        with sqlite3.connect(self.codex.db) as c:
            for i in range(200):
                c.execute('INSERT INTO threads VALUES (?,?,?,?,?,?,?,?)',
                          (str(uuid.uuid4()), '/tmp', '', None, 0, 'cli', 'user', 5))
        notes = {}
        with patch.object(agent, 'command', side_effect=self.fake_command):
            agent.codex_sessions(self.root, notes)
        self.assertIn('window', notes['codex'])
        self.assertIn('Partial discovery', notes['codex'])

    def test_an_owned_tui_is_never_resumed_through_the_daemon(self):
        """Even when this adapter owns the alias, a session a person opened is
        queued to as it stands; the daemon must not resume it."""
        offline = {'thread': {'cwd': str(self.root), 'status': {'type': 'notLoaded'}}}
        with self.daemon(offline, offline) as rpc_ctor, patch.object(agent, 'command', side_effect=self.fake_command):
            record = self.app.ask('codex', self.sid, 'Review it.', 'Reviewer', self.rid,
                                  fresh=True, owned_partner=True)
        rpc = rpc_ctor.return_value
        self.assertEqual(record['route'], 'codex-queue')
        self.assertNotIn('thread/resume', [c.args[0] for c in rpc.call.call_args_list])
        self.assertEqual(sum(1 for a in self.calls if a[:1] == ['codex']), 1)


class LaunchWindowTests(unittest.TestCase):
    """The launch short id is persisted before the listing wait, and the wait is 15 s."""

    def test_7_short_id_is_persisted_and_the_wait_is_fifteen_seconds(self):
        import time as _time
        tmp = tempfile.TemporaryDirectory(); root = Path(tmp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(root)], check=True)
        app = agent.Agent(root)
        prompt = root / 'p.md'; prompt.write_text('Do it.')
        clock = {'t': 0.0}
        fake_time = type('T', (), {'monotonic': staticmethod(lambda: clock['t']),
                                   'sleep': staticmethod(lambda s: clock.__setitem__('t', clock['t'] + 1.0)),
                                   'time': staticmethod(_time.time)})
        def cmd(args, cwd=None, timeout=30):
            if args[:2] == ['git', '-C']:
                return str(root) + '\n'
            if args[:1] == ['claude'] and '--bg' in args:
                return 'backgrounded · abcdef12\n'
            return '[]'
        try:
            with patch.object(agent, 'command', side_effect=cmd), \
                 patch.object(agent, 'claude_sessions', return_value=[]), \
                 patch.object(agent, 'time', fake_time):
                with self.assertRaises(agent.Unavailable) as caught:
                    app.start('claude', 'partner', 'slow', str(prompt), 'Reviewer')
            self.assertIn('abcdef12', str(caught.exception))
            self.assertGreaterEqual(clock['t'], 15.0, 'the wait must run the full window')
            saved = json.loads((app.state / 'partners' / 'slow.json').read_text())
            self.assertEqual(saved.get('native_short_id'), 'abcdef12')
        finally:
            tmp.cleanup()
