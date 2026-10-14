"""A `codex queue` send says whether it still waits in Codex's own queue."""
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent


class CodexQueueTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name).resolve() / 'codex'
        self.home.mkdir()
        env = patch.dict(os.environ, {'CODEX_HOME': str(self.home)})
        env.start()
        self.addCleanup(env.stop)
        self.db = self.home / 'queue_1.sqlite'
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('CREATE TABLE queued_items (id TEXT PRIMARY KEY NOT NULL, thread_id TEXT NOT NULL, '
                      'payload_json TEXT NOT NULL, queue_order INTEGER NOT NULL, '
                      'created_at_ms INTEGER NOT NULL, updated_at_ms INTEGER NOT NULL)')
        self.thread = str(uuid.uuid4())
        self.order = 0

    def queue(self, text, thread=None, age=0):
        self.order += 1
        created = int((time.time() - age) * 1000)
        payload = json.dumps({'UserInput': {'content': [{'type': 'text', 'text': text, 'text_elements': []}]}})
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('INSERT INTO queued_items VALUES (?,?,?,?,?,?)',
                      (str(uuid.uuid4()), thread or self.thread, payload, self.order, created, created))

    def kerd(self, request, **kw):
        self.queue(f'Kerd peer request {request}. This is another agent, not your user.', **kw)

    def record(self, request, **kw):
        return {'provider': 'codex', 'route': 'codex-queue', 'status': 'submitted-unconfirmed',
                'session': self.thread, 'request_id': request, **kw}

    def test_waiting_request_reports_queued_with_age_and_place(self):
        mine = str(uuid.uuid4())
        self.queue('a message the person typed ahead', age=900)
        self.kerd(str(uuid.uuid4()), age=800)
        self.kerd(mine, age=600)
        result = agent.queue_delivery(self.record(mine))
        self.assertEqual(result['delivery'], 'queued')
        self.assertEqual(result['ahead'], 2)
        self.assertGreaterEqual(result['queued_seconds'], 599)
        self.assertIn('not delivered', result['delivery_note'])
        self.assertEqual(result['status'], 'submitted-unconfirmed')  # the status value never changes

    def test_request_absent_from_the_queue_is_not_queued_never_claimed_taken(self):
        mine = str(uuid.uuid4())
        self.kerd(mine)
        self.assertEqual(agent.queue_delivery(self.record(mine))['delivery'], 'queued')
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('DELETE FROM queued_items')  # what a TUI does when it takes the item
        self.kerd(str(uuid.uuid4()))
        result = agent.queue_delivery(self.record(mine))
        self.assertEqual(result['delivery'], 'not-queued')
        self.assertIn('not proof it was taken or answered', result['delivery_note'])

    def test_another_threads_queue_is_not_this_requests_place(self):
        mine = str(uuid.uuid4())
        self.kerd(mine, thread=str(uuid.uuid4()))
        self.assertEqual(agent.queue_delivery(self.record(mine))['delivery'], 'not-queued')

    def test_missing_or_unknown_queue_is_unknown_never_an_error(self):
        mine = str(uuid.uuid4())
        self.db.unlink()
        self.assertEqual(agent.queue_delivery(self.record(mine))['delivery'], 'unknown')
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('CREATE TABLE something_else (x TEXT)')
        self.assertEqual(agent.queue_delivery(self.record(mine))['delivery'], 'unknown')

    def test_odd_row_ahead_still_finds_the_request(self):
        mine = str(uuid.uuid4())
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('INSERT INTO queued_items VALUES (?,?,?,?,?,?)',
                      ('odd', self.thread, 'not json', 0, 1, 1))
        self.kerd(mine)
        result = agent.queue_delivery(self.record(mine))
        self.assertEqual((result['delivery'], result['ahead']), ('queued', 1))

    def test_odd_timestamp_never_hides_a_matching_request(self):
        mine = str(uuid.uuid4())
        payload = json.dumps({'UserInput': {'content': [{'type': 'text', 'text': f'Kerd peer request {mine}. x'}]}})
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('INSERT INTO queued_items VALUES (?,?,?,?,?,?)', ('odd', self.thread, payload, 1, 'later', 1))
        result = agent.queue_delivery(self.record(mine))
        self.assertEqual((result['delivery'], result['queued_seconds']), ('queued', None))

    def test_non_finite_or_absurd_timestamp_keeps_the_match_with_unknown_age(self):
        mine = str(uuid.uuid4())
        payload = json.dumps({'UserInput': {'content': [{'type': 'text', 'text': f'Kerd peer request {mine}. x'}]}})
        for order, created in enumerate((float('inf'), float('-inf'), -5, 10 ** 18), 1):
            with closing(sqlite3.connect(self.db)) as c, c:
                c.execute('DELETE FROM queued_items')
                c.execute('INSERT INTO queued_items VALUES (?,?,?,?,?,?)', ('odd', self.thread, payload, order, created, 1))
            result = agent.queue_delivery(self.record(mine))
            self.assertEqual((result['delivery'], result['queued_seconds']), ('queued', None))
            self.assertIsNone(agent.queue_attention(self.thread))

    def test_unreadable_row_makes_a_non_match_unknown(self):
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('INSERT INTO queued_items VALUES (?,?,?,?,?,?)', ('odd', self.thread, 'not json', 1, 1, 1))
        self.assertEqual(agent.queue_delivery(self.record(str(uuid.uuid4())))['delivery'], 'unknown')

    def test_wal_queue_with_a_live_writer_reads_and_keeps_its_content(self):
        writer = sqlite3.connect(self.db)
        self.addCleanup(writer.close)
        writer.execute('PRAGMA journal_mode=WAL')
        mine = str(uuid.uuid4())
        self.kerd(mine)
        before = writer.execute('SELECT * FROM queued_items ORDER BY id').fetchall()
        self.assertEqual(agent.queue_delivery(self.record(mine))['delivery'], 'queued')
        self.assertEqual(writer.execute('SELECT * FROM queued_items ORDER BY id').fetchall(), before)
        with writer:  # the read left no lock behind for Codex's own writer
            writer.execute('DELETE FROM queued_items')
        self.assertEqual(agent.queue_delivery(self.record(mine))['delivery'], 'not-queued')

    def test_only_unconfirmed_codex_queue_sends_are_looked_up(self):
        mine = str(uuid.uuid4())
        self.kerd(mine)
        for changed in ({'route': 'app-server'}, {'provider': 'claude'}, {'status': 'reply-received'},
                        {'status': 'delivery-uncertain'}):
            self.assertNotIn('delivery', agent.queue_delivery(self.record(mine, **changed)))

    def test_queue_is_opened_read_only_and_left_unchanged(self):
        mine = str(uuid.uuid4())
        self.kerd(mine)
        before = self.db.read_bytes()
        connect = sqlite3.connect
        with patch.object(agent.sqlite3, 'connect', side_effect=lambda *a, **k: connect(*a, **k)) as spy:
            agent.queue_delivery(self.record(mine))
        self.assertTrue(spy.call_args.args[0].endswith('?mode=ro'))
        self.assertEqual(self.db.read_bytes(), before)

    def test_attention_only_past_ten_minutes_and_counts_kerd_requests(self):
        self.kerd(str(uuid.uuid4()), age=60)
        self.queue('the person typed this', age=3600)
        self.assertIsNone(agent.queue_attention(self.thread))
        self.kerd(str(uuid.uuid4()), age=agent.QUEUE_STALL_SECONDS + 60)
        line = agent.queue_attention(self.thread)
        self.assertTrue(line.startswith("2 Kerd requests waiting undelivered in Codex's queue since "))
        self.assertIn(agent.WAKE, line)
        self.db.unlink()
        self.assertIsNone(agent.queue_attention(self.thread))

    def test_status_and_wait_add_delivery_without_storing_it(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        subprocess.run(['git', 'init', '-q', temp.name], check=True)
        app = agent.Agent(temp.name)
        mine = str(uuid.uuid4())
        path = app.folder('requests') / (mine + '.json')
        agent.atomic_json(path, {**self.record(mine), 'project': str(app.root), 'log': None,
                                 'kind': 'arrival-notice', 'reply_expected': False})
        self.kerd(mine, age=30)
        with patch.object(agent, 'transcript', side_effect=agent.Unavailable('none')):
            self.assertEqual(app.status(mine)['delivery'], 'queued')
            self.assertEqual(app.wait(mine, 0)['delivery'], 'queued')
        self.assertNotIn('delivery', agent.read_json(path))

    def test_arrival_row_carries_the_attention_line(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        subprocess.run(['git', 'init', '-q', temp.name], check=True)
        app = agent.Agent(temp.name)
        me = str(uuid.uuid4())
        agent.atomic_json(app.folder('partners') / 'review.json',
                          {'alias': 'review', 'provider': 'codex', 'id': self.thread,
                           'project': str(app.root), 'partner_role': 'Review'})
        self.kerd(str(uuid.uuid4()), age=agent.QUEUE_STALL_SECONDS + 60)

        def send(sid, prompt, request, record, owned_partner, before_send=None):
            record.update(route='codex-queue', status='submitted-unconfirmed')
        with patch.object(app, 'identity', return_value={'id': me, 'provider': 'claude'}), \
             patch.object(agent, 'live_target', return_value={'id': self.thread}), \
             patch.object(app, 'send_codex', side_effect=send):
            row = app.arrival('claude', ['review'])['team'][1]
        self.assertIn('1 Kerd request waiting undelivered', row['attention'])


if __name__ == '__main__':
    unittest.main()
