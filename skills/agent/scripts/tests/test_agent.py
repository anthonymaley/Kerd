import json
import os
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
            for command in ([], ['sessions'], ['pair'], ['start'], ['ask'], ['status'], ['wait']):
                with self.subTest(command=command):
                    result = subprocess.run(
                        [sys.executable, '-B', agent.__file__, *command, '--help'],
                        cwd=directory, env={**os.environ, 'PATH': ''},
                        capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, '')
                    self.assertIn('usage:', result.stdout)
                    self.assertEqual(list(Path(directory).iterdir()), [])


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

    def send(self, root, target, request, prompt):
        self.sent.append((target, request, prompt))
        return 'submitted-unconfirmed'

    def ask(self, prompt='Inspect the agreed result. Do not edit.'):
        return self.app.ask('claude', self.sid, prompt, 'Reviewer', self.rid)

    def append(self, text, kind='assistant'):
        with self.log.open('a') as stream:
            stream.write(json.dumps({'type': kind, 'message': {
                'content': [{'type': 'text', 'text': text}]}}) + '\n')

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
        self.append(begin + 'The finding is conditional')
        self.assertNotIn('reply', self.app.status(self.rid))
        self.append(' on the last qualification being retained.' + end)
        self.assertEqual(self.app.status(self.rid)['reply'],
                         'The finding is conditional on the last qualification being retained.')

    def test_codex_reply_across_native_message_items_is_complete(self):
        self.app.new_request('codex', self.sid, 'Job', 'Reviewer', self.rid, self.log)
        begin, end = agent.markers(self.rid)
        with self.log.open('a') as stream:
            for text in (begin + 'First half', ' and the qualifying second half.' + end):
                stream.write(json.dumps({'type': 'response_item', 'payload': {
                    'type': 'message', 'role': 'assistant',
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
            result = self.app.start('claude', 'partner', 'partner', prompt, 'Reviewer')
        self.assertEqual(result['partner']['id'], sid)
        self.assertNotIn('--session-id', launch.call_args.args[0])
        self.assertNotIn('--dangerously-skip-permissions', launch.call_args.args[0])
        pending = agent.read_json(self.app.state / 'requests' / (result['partner']['request_id'] + '.json'))
        self.assertEqual(pending['session'], sid)
        self.assertEqual(pending['prompt'], 'Actual bounded job')

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
