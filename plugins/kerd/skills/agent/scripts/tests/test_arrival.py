"""Arrival announcements are not contribution requests or availability probes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent


class ArrivalTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        subprocess.run(['git', 'init', '-q', temp.name], check=True)
        self.app = agent.Agent(temp.name)
        self.me, self.peer = str(uuid.uuid4()), str(uuid.uuid4())
        self.bind('self-role', 'claude', self.me, 'Closeout reviewer')
        self.bind('build', 'codex', self.peer, 'Implementation partner')
        self.identity = patch.object(self.app, 'identity', return_value={'id': self.me, 'provider': 'claude'})
        self.identity.start()
        self.addCleanup(self.identity.stop)
        self.live = patch.object(agent, 'live_target', return_value={'id': self.peer})
        self.live.start()
        self.addCleanup(self.live.stop)

    def bind(self, alias, provider, sid, role=None):
        path = self.app.folder('partners') / (alias + '.json')
        agent.atomic_json(path, {'alias': alias, 'provider': provider, 'id': sid,
                                 'project': str(self.app.root), 'partner_role': role})
        return path

    def arrive(self, *peers):
        return self.app.arrival('claude', list(peers or ['build']), 'self-role')

    def send(self, sid, prompt, request, record, owned_partner, before_send=None):
        self.assertFalse(owned_partner)
        self.assertEqual(sid, self.peer)
        self.assertIn(self.me, prompt)
        self.assertIn('Closeout reviewer', prompt)
        self.assertIn('No reply needed; no work requested', prompt)
        self.assertNotIn('<kerd-reply-', prompt)
        if before_send:
            before_send()
        record['status'] = 'submitted-unconfirmed'

    def test_retries_duplicate_aliases_and_self_do_not_send_twice(self):
        self.bind('duplicate', 'codex', self.peer)
        before = (self.app.state / 'partners/self-role.json').read_bytes()
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            first = self.arrive('build', 'duplicate', 'self-role', 'build')
            second = self.arrive('duplicate')
        self.assertEqual(send.call_count, 1)
        self.assertEqual(len(first['team']), 2)
        self.assertEqual(first['team'][1]['request_id'], second['team'][1]['request_id'])
        self.assertFalse(first['team'][1]['reused'])
        self.assertTrue(second['team'][1]['reused'])
        self.assertEqual(first['team'][1]['created_at'], second['team'][1]['created_at'])
        self.assertEqual(before, (self.app.state / 'partners/self-role.json').read_bytes())

    def test_status_and_wait_never_read_transcripts_or_wait_for_notice(self):
        with patch.object(self.app, 'send_codex', side_effect=self.send), \
             patch.object(agent, 'transcript', side_effect=AssertionError('No history')), \
             patch.object(agent.time, 'sleep', side_effect=AssertionError('No wait')):
            result = self.arrive()
            receipt = self.app.wait(result['team'][1]['request_id'], 30)
        self.assertFalse(receipt['reply_expected'])
        self.assertEqual(receipt['status'], 'submitted-unconfirmed')
        self.assertNotIn('reply', receipt)

    def test_uncertain_send_is_retained_and_never_retried(self):
        def fail(*args, **kwargs):
            kwargs['before_send']()
            raise agent.Unavailable('queue failed')
        with patch.object(self.app, 'send_codex', side_effect=fail) as send:
            first = self.arrive()
            second = self.arrive()
        self.assertEqual(send.call_count, 1)
        self.assertEqual(first['team'][1]['status'], 'delivery-uncertain')
        self.assertEqual(second['team'][1]['error'], 'queue failed')

    def test_offline_peer_is_not_resumed_or_replaced(self):
        with patch.object(agent, 'live_target', side_effect=agent.Unavailable('offline')), \
             patch.object(self.app, 'send_codex') as send:
            result = self.arrive()
        send.assert_not_called()
        self.assertEqual(result['team'][1]['status'], 'notice-unavailable')
        self.assertEqual(result['team'][1]['id'], self.peer)

    def test_missing_self_identity_or_wrong_role_sends_nothing(self):
        with patch.object(self.app, 'identity', side_effect=agent.Unavailable('unknown')), \
             patch.object(self.app, 'send_codex') as send:
            with self.assertRaises(agent.Unavailable):
                self.arrive()
        send.assert_not_called()
        self.bind('self-role', 'claude', str(uuid.uuid4()))
        with self.assertRaises(agent.Unavailable):
            self.arrive()
        self.assertFalse((self.app.state / 'requests').exists())

    def test_new_sender_gets_new_notice_and_preserves_previous_id_in_message(self):
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            self.arrive()
            previous = self.me
            self.me = str(uuid.uuid4())
            path = self.bind('self-role', 'claude', self.me, 'Closeout reviewer')
            value = agent.read_json(path)
            value['previous'] = {'id': previous}
            agent.atomic_json(path, value)
            with patch.object(self.app, 'identity', return_value={'id': self.me}):
                self.arrive()
        self.assertEqual(send.call_count, 2)
        self.assertIn('Previous session: ' + previous, send.call_args.args[1])

    def test_new_recipient_sends_again_without_changing_old_request(self):
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            first = self.arrive()['team'][1]
            path = self.app.state / 'requests' / (first['request_id'] + '.json')
            before = path.read_bytes()
            self.peer = str(uuid.uuid4())
            self.bind('build', 'codex', self.peer, 'Implementation partner')
            second = self.arrive()['team'][1]
        self.assertEqual(send.call_count, 2)
        self.assertNotEqual(first['request_id'], second['request_id'])
        self.assertEqual(path.read_bytes(), before)

    def test_unselected_aliases_and_workers_are_not_recipients(self):
        self.bind('historical', 'claude', str(uuid.uuid4()))
        with patch.object(agent, 'claude_sessions', side_effect=AssertionError('No discovery')), \
             patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            self.arrive()
        self.assertEqual(send.call_count, 1)

    def test_no_peers_does_not_create_requests(self):
        result = self.app.arrival('claude', [], 'self-role')
        self.assertEqual(len(result['team']), 1)
        self.assertFalse((self.app.state / 'requests').exists())

    def test_other_project_and_missing_alias_are_reported_without_send(self):
        path = self.app.state / 'partners/build.json'
        saved = agent.read_json(path)
        saved['project'] = str(self.app.root / 'different')
        agent.atomic_json(path, saved)
        with patch.object(self.app, 'send_codex') as send:
            result = self.arrive('build', 'missing')
        send.assert_not_called()
        self.assertEqual(len(result['team']), 3)
        self.assertTrue(all(row.get('error') for row in result['team'][1:]))

    def test_claude_transport_has_no_reply_envelope(self):
        self.bind('review', 'claude', self.peer, 'Reviewer')
        with patch.object(agent, 'send_claude', return_value='submitted-unconfirmed') as send:
            result = self.arrive('review')
        self.assertIn('No reply needed', send.call_args.args[3])
        self.assertNotIn('Return one complete answer', send.call_args.args[3])
        self.assertEqual(result['team'][1]['status'], 'submitted-unconfirmed')

    def test_concurrent_same_arrival_sends_once(self):
        results = []
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            threads = [threading.Thread(target=lambda: results.append(self.arrive())) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=5)
        self.assertEqual(len(results), 2)
        self.assertEqual(send.call_count, 1)

    def test_help_is_offline_and_side_effect_free(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run([sys.executable, '-B', agent.__file__, 'arrival', '--help'],
                                    cwd=cwd, env={**os.environ, 'PATH': ''}, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(Path(cwd).iterdir()), [])

    def test_malformed_binding_is_a_row_error_not_a_traceback(self):
        path = self.app.state / 'partners/build.json'
        for value in ([], None, 'text', 3, {'provider': 'other'}):
            agent.atomic_json(path, value)
            with patch.object(self.app, 'send_codex') as send:
                result = self.arrive()
            self.assertEqual(result['team'][1]['status'], 'notice-unavailable')
            self.assertIn('Invalid', result['team'][1]['error'])
            send.assert_not_called()

    def test_retired_self_and_unassigned_owned_launches_are_not_recipients(self):
        old = str(uuid.uuid4())
        path = self.app.state / 'partners/self-role.json'
        value = agent.read_json(path)
        value.update(previous={'id': old}, recovery={'retired_sessions': [old]})
        agent.atomic_json(path, value)
        self.bind('old-self', 'claude', old)
        worker = self.bind('worker', 'codex', self.peer)
        value = agent.read_json(worker)
        value.update(owned=True, kind='partner')
        agent.atomic_json(worker, value)
        with patch.object(self.app, 'send_codex') as send, patch.object(agent, 'send_claude') as claude:
            result = self.arrive('old-self', 'worker')
        send.assert_not_called()
        claude.assert_not_called()
        self.assertTrue(all(row.get('error') for row in result['team'][1:]))

    def test_a_persistent_owned_partner_with_a_role_is_not_a_worker_and_never_wakes(self):
        path = self.app.state / 'partners/build.json'
        value = agent.read_json(path)
        value.update(owned=True, kind='partner')
        agent.atomic_json(path, value)
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            self.arrive()
        self.assertFalse(send.call_args.kwargs['owned_partner'])
        value['kind'] = 'worker'
        agent.atomic_json(path, value)
        with patch.object(self.app, 'send_codex') as send:
            result = self.arrive()
        send.assert_not_called()
        self.assertIn('Worker', result['team'][1]['error'])

    def test_pre_enqueue_refusal_is_not_delivery_uncertainty(self):
        # Real send_codex, refusal before any native command.
        with patch.object(agent, 'store_row', side_effect=agent.Unavailable('archived')), \
             patch.object(agent, 'command') as command:
            result = self.arrive()
        command.assert_not_called()
        self.assertEqual(result['team'][1]['status'], 'notice-unavailable')
        self.assertIn('archived', result['team'][1]['error'])

    def test_real_codex_queue_boundary_sets_uncertainty_only_when_attempted(self):
        with patch.object(agent, 'store_row', return_value={'tui': True}), \
             patch.object(agent, 'daemon_socket', return_value=self.app.root / 'absent'), \
             patch.object(agent, 'command', side_effect=agent.Unavailable('queue failed')) as command:
            result = self.arrive()
        self.assertEqual(command.call_args.args[0][:2], ['codex', 'queue'])
        self.assertEqual(result['team'][1]['status'], 'delivery-uncertain')

    def test_real_daemon_queue_does_not_resume_a_notice_recipient(self):
        for status, expected, queued in [('notLoaded', 'notice-unavailable', False), ('idle', 'queued', True)]:
            self.peer = str(uuid.uuid4())
            self.bind('build', 'codex', self.peer)
            with patch.object(agent, 'store_row', return_value={'tui': False}), \
                 patch.object(agent, 'daemon_socket', return_value=self.app.root), \
                 patch.object(agent, 'RPC') as rpc:
                calls = []
                def call(method, params):
                    calls.append(method)
                    if method == 'thread/read':
                        return {'thread': {'cwd': str(self.app.root), 'status': status}}
                    if method == 'thread/queue/add':
                        return {'queuedSubmission': {'id': 'native-fixture'}}
                    raise AssertionError(method)
                rpc.return_value.call.side_effect = call
                result = self.arrive()
            self.assertEqual(result['team'][1]['status'], expected)
            self.assertEqual('thread/queue/add' in calls, queued)
            self.assertNotIn('thread/resume', calls)

    def test_missing_or_nonexecutable_codex_is_unavailable_and_not_retried(self):
        for error in (FileNotFoundError(2, 'missing', 'codex'), PermissionError(13, 'denied', 'codex')):
            self.peer = str(uuid.uuid4())
            self.bind('build', 'codex', self.peer)
            with patch.object(agent, 'store_row', return_value={'tui': True}), \
                 patch.object(agent, 'daemon_socket', return_value=self.app.root / 'absent'), \
                 patch.object(agent, 'command', side_effect=error) as command:
                result = self.arrive()
                repeat = self.arrive()
            self.assertEqual(command.call_count, 1)
            self.assertEqual(result['team'][1]['status'], 'notice-unavailable')
            self.assertEqual(repeat['team'][1]['status'], 'notice-unavailable')
            self.assertTrue(repeat['team'][1]['reused'])

    def test_ask_rejects_notice_id_as_different_work(self):
        with patch.object(self.app, 'send_codex', side_effect=self.send):
            row = self.arrive()['team'][1]
        with self.assertRaisesRegex(ValueError, 'different work'):
            self.app.ask('codex', self.peer, 'review', 'Reviewer', row['request_id'])

    def test_real_claude_send_boundary_distinguishes_preflight_and_write_failure(self):
        self.bind('review', 'claude', self.peer, 'Reviewer')
        target = {'id': self.peer, 'pid': 42, 'cwd': str(self.app.root)}
        metadata = {'sessionId': self.peer, 'pid': 42, 'cwd': str(self.app.root),
                    'messagingSocketPath': str(self.app.root / 'fixture.sock')}
        actual_read = agent.read_json
        def read(path):
            return metadata if path.name == '42.json' else actual_read(path)
        actual_owned = agent.owned
        def owned(path, kind):
            return None if kind is agent.stat.S_ISSOCK else actual_owned(path, kind)
        with patch.object(agent, 'live_target', return_value=target), \
             patch.object(agent, 'read_json', side_effect=read), \
             patch.object(agent, 'owned', side_effect=owned), \
             patch.object(agent.socket, 'socket') as socket:
            channel = socket.return_value.__enter__.return_value
            # The fixture's listener is the chosen session (pid 42), as the
            # native peer check reads it on this platform.
            channel.getsockopt.return_value = (agent.struct.pack('i', 42) if sys.platform == 'darwin'
                                               else agent.struct.pack('3i', 42, 0, 0))
            channel.sendall.side_effect = OSError('write failed')
            result = self.arrive('review')
        self.assertEqual(result['team'][1]['status'], 'delivery-uncertain')
        # A different identity creates a new receipt; wrong metadata fails before
        # the socket attempt, rather than falsely reporting uncertain delivery.
        self.peer = str(uuid.uuid4())
        self.bind('review', 'claude', self.peer, 'Reviewer')
        target = dict(target, id=self.peer)
        with patch.object(agent, 'live_target', return_value=target), \
             patch.object(agent, 'read_json', side_effect=read), \
             patch.object(agent.socket, 'socket') as socket:
            result = self.arrive('review')
        socket.assert_not_called()
        self.assertEqual(result['team'][1]['status'], 'notice-unavailable')

    def test_fresh_context_uses_unique_cross_provider_without_inventing_a_role(self):
        self.bind('build', 'codex', self.peer)  # Like Kerd's codex-tui binding.
        self.bind('old-review', 'claude', str(uuid.uuid4()))
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            result = self.app.arrival('claude', None, 'self-role')
        self.assertEqual(send.call_count, 1)
        self.assertEqual(result['team'][1]['id'], self.peer)
        self.assertIn('role not defined', result['team'][1]['role'])

    def test_fresh_context_prefers_recorded_role_but_multiple_roles_stay_unresolved(self):
        self.bind('old-build', 'codex', str(uuid.uuid4()))
        with patch.object(self.app, 'send_codex', side_effect=self.send) as send:
            result = self.app.arrival('claude', None, 'self-role')
        self.assertEqual(send.call_count, 1)
        self.assertEqual(result['team'][1]['id'], self.peer)
        self.bind('second-role', 'codex', str(uuid.uuid4()), 'Designer')
        with patch.object(self.app, 'send_codex') as send:
            result = self.app.arrival('claude', None, 'self-role')
        send.assert_not_called()
        self.assertIn('Multiple established identities', result['team'][1]['error'])


if __name__ == '__main__':
    unittest.main()
