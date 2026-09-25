#!/usr/bin/env python3
"""Local native sessions and queues; no Kerd listener, inbox or terminal takeover.

Claude socket framing and native transcript formats are version-sensitive.
See ../references/native-sessions.md for tested versions and limits.
"""

import argparse
from contextlib import closing, contextmanager
import fcntl
import hashlib
import json
import math
import os
import plistlib
from pathlib import Path
import re
import socket
import sqlite3
import stat
import struct
import subprocess
import sys
import time
import uuid


class Unavailable(RuntimeError):
    pass


def describe(exc):
    """An error for a record or the screen: names the file, never where it
    lives, and never the command line — a timeout's argv carries the prompt."""
    if isinstance(exc, subprocess.TimeoutExpired):
        name = Path(str(exc.cmd[0] if isinstance(exc.cmd, (list, tuple)) else exc.cmd)).name
        return f'Native command timed out after {exc.timeout:g}s ({name})'
    if isinstance(exc, OSError) and getattr(exc, 'errno', None):
        return os.strerror(exc.errno) + ((' (' + Path(exc.filename).name + ')') if exc.filename else '')
    return str(exc)


def command(args, cwd=None, timeout=30):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise Unavailable(result.stderr.strip() or result.stdout.strip() or 'Native command failed')
    return result.stdout


def identifier(value):
    if str(uuid.UUID(value)) != value:
        raise ValueError('Use the exact, canonical session/request UUID')
    return value


def machine_identity():
    """Private host fingerprint: a shared Git directory is not a local host."""
    if sys.platform == 'darwin':
        data = command(['ioreg', '-a', '-rd1', '-c', 'IOPlatformExpertDevice'], timeout=5)
        rows = plistlib.loads(data.encode())
        value = (rows[0].get('IOPlatformUUID') if isinstance(rows, list) and rows
                 and isinstance(rows[0], dict) else None)
    elif sys.platform.startswith('linux'):
        value = Path('/etc/machine-id').read_text().strip()
    else:
        raise Unavailable('Machine identity unavailable for restart recovery')
    if not isinstance(value, str) or not value.strip():
        raise Unavailable('Machine identity unavailable for restart recovery')
    return hashlib.sha256(value.strip().encode()).hexdigest()


def alias_name(value):
    if not value or len(value) > 80 or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in value):
        raise ValueError('Alias must use lowercase letters, numbers, hyphens or underscores')
    return value


REVIEW_CADENCES = ('checkpoints', 'before-push', 'end', 'on-request')


def validate_review_cadence(value):
    """The one check for a partner's review cadence, from the CLI or a stored
    binding. Returns the values in the order given, duplicates removed. It
    schedules review inside authorized work only; it grants no permission."""
    if (not isinstance(value, list) or not value
            or any(not isinstance(item, str) for item in value)):
        raise ValueError('Review cadence must be a nonempty list of: ' + ', '.join(REVIEW_CADENCES))
    unknown = [item for item in value if item not in REVIEW_CADENCES]
    if unknown:
        raise ValueError('Unknown review cadence ' + json.dumps(unknown[0])
                         + '; use ' + ', '.join(REVIEW_CADENCES))
    normalized = list(dict.fromkeys(value))
    if 'on-request' in normalized and len(normalized) > 1:
        raise ValueError('Review cadence on-request stands alone; do not combine it with another value')
    return normalized


def same_project(a, b):
    return Path(a).resolve() == Path(b).resolve()


def belongs_to_project(cwd, root, deadline=None):
    cwd, root = Path(cwd).resolve(), Path(root).resolve()
    if cwd == root:
        return True
    if not cwd.is_relative_to(root):
        return False
    # Containment alone would admit a different nested Git repository.
    args = ['git', '-C', str(cwd), 'rev-parse', '--show-toplevel']
    if deadline is None:
        actual = command(args).strip()
    else:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Unavailable('Discovery deadline reached; results are partial')
        actual = command(args, timeout=remaining).strip()
    return same_project(actual, root)


def status_name(value):
    if isinstance(value, dict):
        return value.get('type', 'unknown')
    return value if isinstance(value, str) else 'unknown'


def owned(path, kind):
    try:
        info = path.lstat()
    except OSError as exc:
        raise Unavailable(os.strerror(exc.errno or 0) + ': ' + path.name) from None
    if info.st_uid != os.getuid() or stat.S_ISLNK(info.st_mode) or not kind(info.st_mode):
        raise Unavailable('Expected a real, locally owned path: ' + path.name)
    return info


def read_json(path):
    owned(path, stat.S_ISREG)
    return json.loads(path.read_text())


def atomic_json(path, value):
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, ensure_ascii=True, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def private_text(path, text):
    """Write text readable only by this account: temp file, fsync, rename."""
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


TAIL_BYTES = 64


def log_tail(stream, offset):
    """The bytes just before offset, hex: a rewrite in place changes them."""
    stream.seek(max(0, offset - TAIL_BYTES))
    return stream.read(min(TAIL_BYTES, max(0, offset))).hex()


@contextmanager
def locked(path):
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


class RPC:
    """A short-lived client of Codex's native server, never a server itself."""
    def __init__(self, root, deadline=None):
        try:
            from websockets.sync.client import unix_connect
            from websockets.exceptions import WebSocketException
        except ImportError:
            raise Unavailable('Codex discovery needs the optional websockets dependency; see native-sessions.md setup') from None
        path = codex_home() / 'app-server-control' / 'app-server-control.sock'
        if not path.exists():
            raise Unavailable('Codex native server is not running')
        owned(path.parent, stat.S_ISDIR)
        owned(path, stat.S_ISSOCK)
        self.native_errors = (WebSocketException, OSError)
        self.deadline = deadline
        try:
            opening = min(3, max(.01, deadline - time.monotonic())) if deadline is not None else 3
            self.channel = unix_connect(str(path), compression=None, open_timeout=opening,
                                        close_timeout=1, max_size=16 * 1024 * 1024)
        except self.native_errors as exc:
            raise Unavailable('Codex native connection failed: ' + str(exc)) from None
        self.counter = 0
        try:
            self.call('initialize', {'clientInfo': {'name': 'kerd_agent', 'version': '1'},
                                    'capabilities': {'experimentalApi': True}})
            self.send({'method': 'initialized', 'params': {}})
        except Exception:
            self.close()
            raise

    def send(self, value):
        try:
            self.channel.send(json.dumps(value))
        except self.native_errors as exc:
            raise Unavailable('Codex send outcome uncertain: ' + str(exc)) from None

    def call(self, method, params):
        deadline = min(time.monotonic() + 10, self.deadline) if self.deadline is not None else time.monotonic() + 10
        if time.monotonic() >= deadline:
            raise Unavailable('Discovery deadline reached; results are partial')
        self.counter += 1
        request = self.counter
        self.send({'id': request, 'method': method, 'params': params})
        while time.monotonic() < deadline:
            try:
                event = json.loads(self.channel.recv(timeout=max(.01, deadline - time.monotonic())))
            except TimeoutError:
                break
            except self.native_errors as exc:
                raise Unavailable('Codex response unavailable: ' + str(exc)) from None
            if event.get('id') == request and 'method' not in event:
                if 'error' in event:
                    raise Unavailable(str(event['error']))
                return event.get('result')
            # Never grant a native approval, answer a user question, or
            # mistake an unrelated turn notification for this RPC's result.
        raise Unavailable('Native RPC timed out; delivery may be uncertain, do not resend automatically')

    def close(self):
        self.channel.close()  # Close our connection, never the native daemon/session.

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def claude_home():
    return Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home() / '.claude'))).resolve()


def codex_home():
    return Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).resolve()


def claude_sessions(root):
    # Native --cwd is an exact filter; it omits sessions opened in subdirectories.
    rows = json.loads(command(['claude', 'agents', '--json']))
    if not isinstance(rows, list):
        raise Unavailable('Unknown Claude agents response; discovery needs an adapter update')
    result = []
    for row in rows:
        if not row.get('sessionId') or not belongs_to_project(row['cwd'], root):
            continue
        try:
            identifier(row['sessionId'])
        except ValueError:
            continue  # one odd row, not the whole listing
        result.append({'provider': 'claude', 'id': identifier(row['sessionId']),
                       'name': row.get('name'), 'cwd': row['cwd'], 'pid': row.get('pid'),
                       'status': status_name(row.get('status')), 'reachability': 'native-listed',
                       'kind': row.get('kind', 'unknown')})
    return result


def codex_sessions(root, unavailable=None):
    result, seen = [], set()
    deadline = time.monotonic() + 5
    # Daemon-loaded threads first. A missing daemon fails fast inside RPC()
    # and is reported as partial; the store scan below still runs.
    try:
        with RPC(root, deadline=deadline) as rpc:
            cursor = None
            while True:
                page = rpc.call('thread/loaded/list', {'cursor': cursor, 'limit': 100})
                for tid in page['data']:
                    row = rpc.call('thread/read', {'threadId': tid, 'includeTurns': False})['thread']
                    if belongs_to_project(row['cwd'], root, deadline):
                        seen.add(identifier(tid))
                        result.append({'provider': 'codex', 'id': tid,
                                       'name': row.get('name'), 'cwd': row['cwd'],
                                       'status': status_name(row.get('status')),
                                       'reachability': 'native-loaded', 'kind': 'session'})
                cursor = page.get('nextCursor')
                if not cursor:
                    break
    except (Unavailable, OSError, subprocess.TimeoutExpired) as exc:
        if unavailable is None:
            raise
        unavailable['codex'] = 'Partial discovery (daemon): ' + str(exc)
    # Then saved threads from the local store: TUIs live here. Bounded, newest
    # first, archived excluded, deduplicated against the daemon's view. Needs
    # no daemon and no optional dependency.
    database = codex_home() / 'state_5.sqlite'
    if database.exists():
        owned(database, stat.S_ISREG)
        with closing(sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)) as db:
            # Sessions a person might pair with: threads they opened, not the
            # subagents those threads spawned (thread_source = 'subagent').
            rows = db.execute("SELECT id, cwd, name FROM threads WHERE archived = 0 "
                              "AND source = 'cli' AND thread_source = 'user' "
                              "ORDER BY updated_at DESC LIMIT 200").fetchall()
        if len(rows) == 200 and unavailable is not None:
            note = 'Store discovery window full (200 newest sessions); older sessions are not listed but remain selectable by UUID'
            unavailable['codex'] = (unavailable['codex'] + ' | ' + note) if unavailable.get('codex') else note
        for tid, cwd, name in rows:
            if tid in seen:
                continue
            try:
                identifier(tid)
                if not belongs_to_project(cwd, root, deadline):
                    continue
            except ValueError:
                continue  # one non-canonical id costs one row, never the listing
            except Unavailable as exc:
                if 'deadline' in str(exc):
                    if unavailable is not None:
                        unavailable['codex'] = (unavailable.get('codex', '') + ' | ' if unavailable.get('codex') else '') + 'Store discovery incomplete: ' + str(exc)
                    break
                continue  # this row's directory cannot be resolved; skip it alone
            seen.add(tid)
            result.append({'provider': 'codex', 'id': tid, 'name': name, 'cwd': cwd,
                           'status': SAVED, 'reachability': 'native-thread', 'kind': 'session'})
    return result


SAVED = 'saved thread \u2014 activity unknown'


def store_row(root, sid):
    """The chosen Codex thread as the local store records it, checked for
    project and archive state — the two refusals every route shares."""
    identifier(sid)
    database = codex_home() / 'state_5.sqlite'
    owned(database, stat.S_ISREG)
    with closing(sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)) as db:
        row = db.execute('SELECT cwd, rollout_path, name, archived, source, thread_source '
                         'FROM threads WHERE id = ?', (sid,)).fetchone()
    if not row:
        raise Unavailable('Chosen Codex thread is not in the local store')
    if row[3]:
        raise Unavailable('Chosen Codex thread is archived; not revived')
    if not belongs_to_project(row[0], root):
        raise Unavailable('Chosen Codex thread belongs to another project')
    return {'cwd': row[0], 'name': row[2], 'source': row[4], 'thread_source': row[5],
            'tui': row[4] == 'cli' and row[5] == 'user'}


def stored_thread(root, sid):
    """A selectable saved thread: one a person opened (a TUI). Membership plus
    a matching project is enough to *select* it, never proof anyone is at the
    keyboard: the store has no PID or heartbeat, so activity stays unknown."""
    row = store_row(root, sid)
    if not row['tui']:
        # Same predicate as discovery: not a headless `codex exec` run, a
        # spawned subagent, or an app-server-created thread.
        raise Unavailable('Chosen Codex thread is not a session a person opened; not selectable')
    return {'provider': 'codex', 'id': sid, 'cwd': row['cwd'], 'name': row['name'],
            'status': SAVED, 'reachability': 'native-thread', 'kind': 'session'}


def daemon_socket():
    return codex_home() / 'app-server-control' / 'app-server-control.sock'


def live_target(root, provider, sid):
    identifier(sid)
    if provider == 'codex':
        # A daemon-loaded thread is live. Anything else the store knows about is
        # a saved thread — a TUI in a terminal, typically — reachable only by
        # `codex queue`, with its activity honestly unknown.
        if daemon_socket().exists():
            try:
                with RPC(root) as rpc:
                    row = rpc.call('thread/read', {'threadId': sid, 'includeTurns': False})['thread']
                if belongs_to_project(row['cwd'], root):
                    loaded = status_name(row.get('status')) != 'notLoaded'
                    return {'provider': 'codex', 'id': sid, 'cwd': row['cwd'],
                            'status': status_name(row.get('status')),
                            'reachability': 'native-loaded' if loaded else 'native-daemon'}
            except Unavailable:
                pass
        return stored_thread(root, sid)
    rows = claude_sessions(root)
    matches = [row for row in rows if row['id'] == sid]
    if len(matches) != 1:
        raise Unavailable('Exact session is not reachable in this project; no fork, resume or replacement attempted')
    return matches[0]


def transcript(root, provider, sid):
    """Locate just the chosen session's native log. Never load its full history."""
    identifier(sid)
    if provider == 'claude':
        paths = list((claude_home() / 'projects').glob('*/' + sid + '.jsonl'))
        if len(paths) != 1:
            raise Unavailable('Chosen Claude transcript is not uniquely available yet')
        path = paths[0]
    else:
        database = codex_home() / 'state_5.sqlite'
        owned(database, stat.S_ISREG)
        with closing(sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)) as db:
            row = db.execute('SELECT cwd, rollout_path FROM threads WHERE id = ?', (sid,)).fetchone()
        if not row or not belongs_to_project(row[0], root):
            raise Unavailable('Chosen Codex transcript does not belong to this project')
        path = Path(row[1])
        if not path.resolve().is_relative_to(codex_home() / 'sessions'):
            raise Unavailable('Native transcript is outside the supported sessions directory')
    owned(path, stat.S_ISREG)
    return path


def assistant_text(event, provider):
    if provider == 'claude' and event.get('type') == 'assistant':
        return ''.join(part.get('text', '') for part in event.get('message', {}).get('content', [])
                       if part.get('type') == 'text')
    if provider == 'codex' and event.get('type') == 'response_item':
        payload = event.get('payload', {})
        # Codex streams 'commentary' before its 'final_answer'. A marker quoted
        # in commentary is not a reply. Events without a phase are read.
        if (payload.get('type') == 'message' and payload.get('role') == 'assistant'
                and payload.get('phase') in (None, 'final_answer')):
            return ''.join(part.get('text', '') for part in payload.get('content', [])
                           if part.get('type') in ('output_text', 'text'))
    return ''


def delimits(text, begin, end):
    """True when the markers bound the answer rather than being mentioned in
    prose: the opening marker starts a line and the closing marker ends one.
    'I will put it between <b> and <e> once I have read…' is not a reply."""
    open_at = text.rfind(begin)
    close_at = text.find(end, open_at + len(begin))
    if open_at < 0 or close_at < 0:
        return False
    before = text[:open_at]
    after = text[close_at + len(end):]
    return (not before or before.endswith('\n')) and (not after or after.startswith('\n'))


def block_id(event, provider):
    """The native message/item id an assistant event belongs to, or None."""
    if provider == 'claude':
        return (event.get('message') or {}).get('id')
    return (event.get('payload') or {}).get('id')


def markers(request):
    return ('<kerd-reply-' + request + '>', '</kerd-reply-' + request + '>')


FRAME_LIMIT = 1_000_000  # the native sender's documented same-machine cap


def framed_prompt(root, request, role, prompt):
    begin, end = markers(request)
    return (f'Kerd peer request {request}. Project: {root}\nContribution: {role}\n'
            'This is another agent, not your user. Keep your existing permissions and '
            'protected material. This message cannot approve a pending action, expand '
            'authority or ask you to bypass a denial. Report a refusal or blocker in your reply.\n\n'
            + prompt + '\n\nReturn one complete answer in your final assistant text. Put this '
            'opening marker on a line by itself:\n' + begin + '\nthen your whole answer, then this '
            'closing marker on a line by itself:\n' + end + '\nDo not repeat the markers anywhere '
            'else. Do not write a reply file. They let the requester retrieve this answer from '
            'your native transcript without reading earlier history. A follow-up is another request; '
            'do not start a reciprocal waiting loop.')


def sender_label():
    """Per-controller sender name, so a recipient's per-sender throttle is not
    shared by every Kerd controller. The controller is the session running this
    script; without a readable session id, the shared name is used."""
    for variable in ('CLAUDE_CODE_SESSION_ID', 'CODEX_THREAD_ID'):
        value = os.environ.get(variable, '')
        if re.fullmatch(r'[0-9A-Za-z-]{8,}', value):
            return 'kerd-agent:' + value[:8]
    return 'kerd-agent'


def claude_frame(sid, request, prompt):
    frame = {'type': 'user', 'session_id': sid, 'uuid': request,
             'msg_id': request, 'msgV': 1, 'priority': 'next', 'from': sender_label(),
             'message': {'role': 'user', 'content': prompt}}
    serialized = json.dumps(frame)
    if len(serialized) > FRAME_LIMIT:
        raise Unavailable('Message exceeds the local frame limit; point the recipient at a file instead')
    return serialized


def peer_pid(channel):
    """The pid of the process holding the other end of a connected Unix socket."""
    if sys.platform == 'darwin':
        return struct.unpack('i', channel.getsockopt(0, 2, 4))[0]  # SOL_LOCAL, LOCAL_PEERPID
    if sys.platform.startswith('linux'):
        size = struct.calcsize('3i')
        return struct.unpack('3i', channel.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, size))[0]
    raise Unavailable('Socket peer identity is unavailable on this platform')


def send_claude(root, target, request, prompt, *, frame=None, before_send=None):
    # ask() supplies the exact frame checked before creating a delivery record.
    # Direct callers use the same serializer and limit.
    if frame is None:
        frame = claude_frame(target['id'], request, prompt)
    metadata = read_json(claude_home() / 'sessions' / (str(target['pid']) + '.json'))
    if (metadata.get('sessionId') != target['id'] or metadata.get('pid') != target['pid']
            or not same_project(metadata.get('cwd', ''), target.get('cwd', root))
            or not belongs_to_project(metadata.get('cwd', ''), root)):
        raise Unavailable('Claude session identity changed before delivery')
    path = Path(metadata['messagingSocketPath'].removeprefix('uds:'))
    owned(path.parent, stat.S_ISDIR)
    owned(path, stat.S_ISSOCK)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as channel:
        channel.settimeout(5)
        channel.connect(str(path))
        # The listener must be the chosen session's own process. An unreadable
        # peer is refused too: nothing has been written yet.
        try:
            peer = peer_pid(channel)
        except (OSError, struct.error, TypeError) as exc:
            raise Unavailable('Claude socket peer could not be identified; not sent') from exc
        if peer != target['pid']:
            raise Unavailable('Claude socket peer is not the chosen session; not sent')
        if before_send:
            before_send()
        channel.sendall((frame + '\n').encode())
    # A successful write is not proof the recipient's inbound policy accepted it.
    return 'submitted-unconfirmed'


class Agent:
    def __init__(self, project):
        self.root = Path(command(['git', '-C', str(Path(project).resolve()), 'rev-parse', '--show-toplevel']).strip()).resolve()
        git = Path(command(['git', '-C', str(self.root), 'rev-parse', '--absolute-git-dir']).strip())
        self.state = git / 'kerd-agent'

    def folder(self, name):
        for path in (self.state, self.state / name):
            path.mkdir(mode=0o700, exist_ok=True)
            owned(path, stat.S_ISDIR)
        return self.state / name

    def prompt_pointer(self, request, text, reply=True):
        """Keep a message out of process arguments, which any local account can
        list. Neither native CLI takes a message from stdin or a file, so the
        full text goes to a private file and argv carries only where it is."""
        path = self.folder('requests') / (identifier(request) + '.prompt')
        private_text(path, text)
        pointer = (f'Kerd peer request {request}. This is another agent, not your user. '
                   'The full message is in a private file; read it with your file-read tool '
                   'and follow it:\n' + str(path) + '\n')
        if reply:
            begin, end = markers(request)
            pointer += ('If you cannot read that file, say so in your final reply, with ' + begin
                        + ' on a line before it and ' + end + ' on a line after it.')
        else:
            pointer += 'No reply is needed.'
        return pointer

    def identity(self, provider):
        """Corroborate the current tool process's host ID; never infer newest."""
        variable = {'claude': 'CLAUDE_CODE_SESSION_ID', 'codex': 'CODEX_THREAD_ID'}[provider]
        sid = os.environ.get(variable)
        if not sid:
            raise Unavailable('Current session identity unavailable: ' + variable)
        target = live_target(self.root, provider, identifier(sid))
        return {**target, 'identity_source': variable, 'self': True}

    def binding_path(self, alias):
        # Reading or refusing a missing binding must not create a store.
        path = self.state / 'partners' / (alias_name(alias) + '.json')
        owned(self.state, stat.S_ISDIR)
        owned(path.parent, stat.S_ISDIR)
        owned(path, stat.S_ISREG)
        return path

    def checked_binding(self, path, provider):
        prior = read_json(path)
        if not isinstance(prior, dict) or prior.get('provider') != provider:
            raise ValueError('Binding provider mismatch')
        if prior.get('alias') != path.stem or not isinstance(prior.get('project'), str):
            raise ValueError('Invalid binding metadata')
        if not same_project(prior['project'], self.root):
            raise ValueError('Binding belongs to another project')
        if not isinstance(prior.get('id'), str):
            raise ValueError('Invalid binding session ID')
        identifier(prior['id'])
        return prior

    def handoff_record(self, record):
        if not isinstance(record, str) or not record:
            raise ValueError('Name the saved handoff record')
        path = (self.root / record).resolve()
        if not path.is_relative_to(self.root) or not belongs_to_project(path.parent, self.root):
            raise ValueError('Handoff record must belong to this project')
        owned(path, stat.S_ISREG)
        data = path.read_bytes()
        if not data.strip():
            raise ValueError('Handoff record is empty')
        return {'record': str(path.relative_to(self.root)),
                'sha256': hashlib.sha256(data).hexdigest()}

    def handoff(self, provider, alias, record=None, cancel=False):
        current = self.identity(provider)
        path = self.binding_path(alias)
        evidence = None if cancel else self.handoff_record(record)
        with locked(path.with_suffix('.lock')):
            prior = self.checked_binding(path, provider)
            if prior['id'] != current['id']:
                raise ValueError('Only the bound current session can prepare its handoff')
            if prior.get('owned'):
                raise ValueError('Owned launch partners cannot prepare external replacement')
            if cancel:
                if 'handoff' not in prior and 'recovery' not in prior:
                    return prior
                prior.pop('handoff', None)
            else:
                prior['handoff'] = {**evidence, 'from_session': current['id'],
                                    'prepared_at': time.time()}
            # An explicit revocation or newer saved account supersedes the old
            # restart receipt, even when no one-use handoff remains.
            prior.pop('recovery', None)
            atomic_json(path, prior)
            return prior

    def check_restart(self, provider, previous, current, permit):
        if provider != 'claude':
            raise Unavailable('Restart recovery unavailable: Codex saved threads do not establish predecessor absence; use a prepared handoff or explicit selection')
        if permit.get('host') != machine_identity():
            raise Unavailable('Restart recovery requires the same recorded machine')
        retired = permit.get('retired_sessions')
        if not isinstance(retired, list) or any(not isinstance(sid, str) for sid in retired):
            raise Unavailable('Restart recovery receipt has no valid retired-session history')
        if current in retired:
            raise Unavailable('This session previously relinquished the role; no automatic reclaim')
        # Fail closed on an incomplete/unknown response; ordinary discovery may
        # skip malformed rows, which is unsuitable evidence for replacement.
        rows = json.loads(command(['claude', 'agents', '--json'], timeout=5))
        if not isinstance(rows, list):
            raise Unavailable('Restart recovery needs a complete native Claude listing')
        ids = set()
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('cwd'), str) or not row['cwd']:
                raise Unavailable('Restart recovery encountered incomplete native metadata')
            if not isinstance(row.get('sessionId'), str):
                raise Unavailable('Restart recovery encountered a missing native identity')
            ids.add(identifier(row['sessionId']))
            if row['sessionId'] == current and not belongs_to_project(row['cwd'], self.root):
                raise Unavailable('Current identity is no longer in this project')
        if previous in ids:
            raise Unavailable('Predecessor is still natively listed; restart recovery will not replace it')
        if current not in ids:
            raise Unavailable('Current identity is no longer natively listed')

    def adopt(self, provider, alias, expected_session, record=None, confirm=False):
        identifier(expected_session)
        current = self.identity(provider)
        path = self.binding_path(alias)
        with locked(path.with_suffix('.lock')):
            prior = self.checked_binding(path, provider)
            if prior['id'] != expected_session:
                raise ValueError('Binding changed; current session is ' + prior['id'])
            if prior['id'] == current['id']:
                return prior  # Byte-preserving no-op, including metadata.
            if prior.get('owned'):
                raise ValueError('Owned launch partners cannot be replaced by an external session')
            evidence = None
            if not confirm:
                permit = prior.get('handoff')
                recovering = permit is None
                if recovering:
                    permit = prior.get('recovery')
                if not record or not isinstance(permit, dict):
                    raise ValueError('Replacement needs a prepared handoff, restart receipt or explicit user selection')
                evidence = self.handoff_record(record)
                if (permit.get('from_session') != expected_session or
                        any(permit.get(k) != v for k, v in evidence.items())):
                    raise ValueError('Handoff changed or does not designate this binding')
                if recovering:
                    self.check_restart(provider, expected_session, current['id'], permit)
            # No launch settings/ownership migrate. Requests already store their
            # exact target IDs and are deliberately not touched by replacement.
            successor = {'alias': alias, 'provider': provider, 'id': current['id'],
                         'project': str(self.root),
                         'previous': {'id': prior['id'], 'replaced_at': time.time()}}
            if 'partner_role' in prior:
                successor['partner_role'] = prior['partner_role']
            if 'review_cadence' in prior:
                # Copied unchanged, even when malformed. Readers (notice_binding,
                # partners) validate it and report the binding; dropping it here
                # would silently hide the problem.
                successor['review_cadence'] = prior['review_cadence']
            if evidence is not None:
                retired = permit.get('retired_sessions', []) if recovering else []
                try:
                    host = machine_identity()
                except (Unavailable, OSError, ValueError, subprocess.TimeoutExpired):
                    # Recovery is optional; an OS fingerprint outage must not
                    # prevent a planned, record-authorized role handoff.
                    host = None
                successor['recovery'] = {
                    **evidence, 'from_session': current['id'], 'host': host,
                    'retired_sessions': list(dict.fromkeys([*retired, expected_session]))}
            atomic_json(path, successor)
            return successor

    def list(self):
        sessions, unavailable = [], {}
        for provider, discover in (('claude', claude_sessions), ('codex', codex_sessions)):
            try:
                sessions.extend(discover(self.root, unavailable) if provider == 'codex' else discover(self.root))
            except (Unavailable, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
                unavailable[provider] = str(exc)
        aliases = []
        if (self.state / 'partners').exists():
            for path in (self.state / 'partners').glob('*.json'):
                saved = read_json(path)
                live = next((row for row in sessions if row['id'] == saved.get('id')
                             and row['provider'] == saved['provider']), None)
                saved['recorded_status'] = saved.pop('status', 'paired')
                saved['live_status'] = live['status'] if live else 'not listed'
                aliases.append(saved)
        sessions = [{**row, 'partner_aliases': sorted({saved['alias'] for saved in aliases
                     if saved.get('id') == row['id'] and saved['provider'] == row['provider']})}
                    for row in sessions]
        workers = []
        if (self.state / 'workers').exists():
            workers = [read_json(path) for path in (self.state / 'workers').glob('*.json')]
        return {'project': str(self.root), 'sessions': sessions, 'partners': aliases,
                'worker_launch_records': workers, 'unavailable': unavailable,
                'scope': 'Claude native discovery, Codex shared server and the local Codex session store; partner/worker records are not live probes of every app or closed conversation'}

    def notice_binding(self, path):
        raw = read_json(path)
        if not isinstance(raw, dict) or raw.get('provider') not in ('claude', 'codex'):
            raise ValueError('Invalid binding provider or object')
        peer = self.checked_binding(path, raw['provider'])
        if peer.get('partner_role') is not None and not isinstance(peer['partner_role'], str):
            raise ValueError('Invalid partner role')
        if peer.get('review_cadence') is not None:
            try:
                validate_review_cadence(peer['review_cadence'])
            except ValueError as exc:
                raise ValueError('Invalid review cadence: ' + str(exc)) from None
        return peer

    def partners(self):
        """This project's partner bindings from private metadata only.

        No native discovery, session probe, socket, provider CLI or network.
        One unreadable or malformed binding is its own invalid row, never a
        hidden partner or a failed listing. Session IDs are not returned.
        """
        folder = self.state / 'partners'
        for path in (self.state, folder):
            try:
                path.lstat()
            except FileNotFoundError:
                return {'partners': []}  # never paired here; nothing to report
            owned(path, stat.S_ISDIR)  # a symlinked or foreign store is a store failure
        # iterdir, not glob: an unreadable directory must fail, not list nothing.
        paths = [path for path in folder.iterdir() if path.name.endswith('.json')]
        rows = [self.partner_row(path) for path in paths]
        return {'partners': sorted(rows, key=lambda row: row['alias'])}

    def partner_row(self, path):
        row = {'alias': path.stem, 'provider': None, 'kind': 'partner', 'role': None,
               'review_cadence': None, 'valid': False}
        try:
            raw = read_json(path)
        except (Unavailable, OSError, ValueError) as exc:
            return {**row, 'error': 'Unreadable binding: ' + describe(exc)}
        if not isinstance(raw, dict):
            return {**row, 'error': 'Invalid binding object'}
        if isinstance(raw.get('provider'), str):
            row['provider'] = raw['provider']
        if isinstance(raw.get('kind', 'partner'), str):
            row['kind'] = raw.get('kind', 'partner')
        if isinstance(raw.get('partner_role'), str):
            row['role'] = raw['partner_role']
        error = None
        try:
            alias_name(path.stem)
            alias_ok = raw.get('alias') == path.stem
        except ValueError:
            alias_ok = False
        if raw.get('provider') not in ('claude', 'codex'):
            error = 'Invalid binding provider'
        elif not alias_ok:
            error = 'Invalid binding alias'
        elif not isinstance(raw.get('project'), str):
            error = 'Invalid binding project'
        elif not self.stored_project_matches(raw['project']):
            error = 'Binding belongs to another project'
        elif not isinstance(raw.get('kind', 'partner'), str):
            error = 'Invalid binding kind'
        elif raw.get('kind', 'partner') != 'partner':
            error = 'Binding is not a partner'
        elif raw.get('partner_role') is not None and not isinstance(raw['partner_role'], str):
            error = 'Invalid partner role'
        elif raw.get('id') in (None, ''):
            # E.g. a start-uncertain reservation: never offer an unreachable partner.
            error = 'Binding has no confirmed session yet'
        elif not self.canonical_session(raw['id']):
            error = 'Invalid binding session ID'
        elif raw.get('review_cadence') is not None:
            try:
                row['review_cadence'] = validate_review_cadence(raw['review_cadence'])
            except ValueError as exc:
                error = 'Invalid review cadence: ' + str(exc)
        if error:
            return {**row, 'review_cadence': None, 'error': error}
        return {**row, 'valid': True}

    @staticmethod
    def canonical_session(value):
        # The same check checked_binding applies: a string, then identifier().
        if not isinstance(value, str):
            return False
        try:
            identifier(value)
        except ValueError:
            return False
        return True

    def stored_project_matches(self, project):
        try:
            return same_project(project, self.root)
        except (OSError, ValueError, RuntimeError):
            return False  # e.g. an embedded NUL or a symlink loop: not this project

    def arrival_peers(self, provider, excluded):
        """Prefer an explicitly recorded role, otherwise a unique external peer.

        No native discovery, historical requests or binding changes. Multiple
        identities remain a choice, never a newest-session heuristic.
        """
        folder = self.state / 'partners'
        if not folder.exists():
            return [], []
        candidates = []
        try:
            for path in sorted(folder.glob('*.json')):
                peer = self.notice_binding(self.binding_path(path.stem))
                if (peer['provider'], peer['id']) in excluded or peer.get('kind') == 'worker':
                    continue
                role = bool((peer.get('partner_role') or '').strip())
                if peer.get('owned') and not (peer.get('kind') == 'partner' and role):
                    continue
                # Same-provider contact aliases alone do not select teammates.
                if peer['provider'] != provider or role:
                    candidates.append(peer)
        except (Unavailable, OSError, ValueError, KeyError, TypeError) as exc:
            return [], [{'status': 'notice-unavailable', 'error': describe(exc)}]
        aliases, unresolved = [], []
        for target_provider in ('claude', 'codex'):
            rows = [peer for peer in candidates if peer['provider'] == target_provider]
            roles = [peer for peer in rows if (peer.get('partner_role') or '').strip()]
            rows = roles or rows
            groups = {}
            for peer in rows:
                groups.setdefault(peer['id'], peer)
            if len(groups) == 1:
                aliases.append(next(iter(groups.values()))['alias'])
            elif groups:
                unresolved.append({'provider': target_provider, 'status': 'notice-unavailable',
                                   'error': 'Multiple established identities; no notice recipient selected. Use Agent to choose when needed.'})
        return aliases, unresolved

    def arrival(self, provider, peers=None, self_alias=None):
        """One informational notice per exact sender/recipient identity pair.

        Explicit restored aliases or an unambiguous private pairing are recipients.
        Receipts reuse requests, but have no reply protocol or transcript reads.
        """
        current = self.identity(provider)
        sender = {'provider': provider, 'id': current['id'], 'role': 'current session'}
        excluded = {(provider, current['id'])}
        if self_alias:
            binding = self.notice_binding(self.binding_path(self_alias))
            if binding['provider'] != provider:
                raise ValueError('Binding provider mismatch')
            if binding['id'] != current['id']:
                raise Unavailable('Restore this role before announcing its arrival')
            sender.update(role=binding.get('partner_role') or 'role not defined', alias=self_alias)
            previous, recovery = binding.get('previous') or {}, binding.get('recovery') or {}
            if not isinstance(previous, dict) or not isinstance(recovery, dict):
                raise ValueError('Invalid previous identity or recovery metadata')
            retired = recovery.get('retired_sessions', [])
            if not isinstance(retired, list):
                raise ValueError('Invalid retired identity list')
            for sid in retired:
                if not isinstance(sid, str):
                    raise ValueError('Invalid retired identity')
                excluded.add((provider, identifier(sid)))
            if previous.get('id'):
                if not isinstance(previous['id'], str):
                    raise ValueError('Invalid previous identity')
                sender['previous_id'] = identifier(previous['id'])
                excluded.add((provider, sender['previous_id']))
        result = {'team': [{**sender, 'self': True, 'status': 'identity verified'}],
                  'availability': 'unverified; notices do not check availability'}
        if peers is None:
            peers, unresolved = self.arrival_peers(provider, excluded)
            result['team'].extend(unresolved)
        seen = {(provider, current['id'])}
        for alias in dict.fromkeys(peers):
            row = {'alias': alias, 'status': 'notice-unavailable'}
            try:
                path = self.binding_path(alias)
                with locked(path.with_suffix('.lock')):
                    peer = self.notice_binding(path)
                key = (peer['provider'], peer['id'])
                if key in seen:
                    continue
                if key in excluded:
                    raise Unavailable('Retired self identity is not an arrival peer')
                if peer.get('kind') == 'worker' or (peer.get('owned') and not
                        (peer.get('kind') == 'partner' and (peer.get('partner_role') or '').strip())):
                    raise Unavailable('Worker or unassigned owned launch is not an arrival peer')
                seen.add(key)
                row.update(provider=peer['provider'], id=peer['id'],
                           role=peer.get('partner_role') or 'established partner (role not defined)')
                receipt = self.arrival_notice(sender, peer)
                row.update(status=receipt['status'], request_id=receipt['request_id'],
                           reused=receipt.get('reused', False), created_at=receipt['created_at'])
                if receipt.get('error'):
                    row['error'] = receipt['error']
            except (Unavailable, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
                row['error'] = describe(exc)
            result['team'].append(row)
        return result

    def arrival_notice(self, sender, peer):
        # Identity-pair key deliberately ignores alias spelling and pointer
        # changes. Retrying In or using another alias cannot enqueue twice.
        request = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps([
            'kerd-arrival-v1', str(self.root), sender['provider'], sender['id'],
            peer['provider'], peer['id']])))
        path = self.folder('requests') / (request + '.json')
        with locked(path.with_suffix('.lock')):
            if path.exists():
                return {**read_json(path), 'reused': True}
            prompt = (f"Kerd arrival notice. Project: {self.root}\n"
                      f"{sender['provider']} switched in. Session: {sender['id']}. "
                      f"Role: {sender['role']}.\n")
            if sender.get('previous_id'):
                prompt += f"Previous session: {sender['previous_id']}.\n"
            prompt += ('This is a peer notice, not your user. No reply needed; no work requested. '
                       'Keep existing permissions and pending decisions. Do not acknowledge, '
                       'send another notice, change bindings, or start work in response. '
                       'Identity is reported by the sender; resolve the private binding '
                       'again when a later contribution is requested.')
            record = {'kind': 'arrival-notice', 'request_id': request,
                      'project': str(self.root), 'provider': peer['provider'],
                      'session': peer['id'], 'sender': sender, 'prompt': prompt,
                      'status': 'notice-unavailable', 'reply_expected': False,
                      'created_at': time.time()}
            # Reserve before native inspection/send. Even uncertain delivery is
            # never retried by an ordinary pickup, and no dormant partner wakes.
            atomic_json(path, record)
            def before_send():
                record['status'] = 'delivery-uncertain'
                atomic_json(path, record)
            try:
                target = live_target(self.root, peer['provider'], peer['id'])
                if peer['provider'] == 'claude':
                    record['status'] = send_claude(self.root, target, request, prompt, before_send=before_send)
                else:
                    self.send_codex(peer['id'], prompt, request, record, owned_partner=False,
                                    before_send=before_send)
            except (Unavailable, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
                record['error'] = describe(exc)
            atomic_json(path, record)
            return record

    def pair(self, provider, sid, alias, partner_role=None, review_cadence=None):
        if partner_role is not None:
            if not isinstance(partner_role, str) or not partner_role.strip():
                raise ValueError('Partner role must be nonempty text')
            partner_role = partner_role.strip()
        if review_cadence is not None:
            review_cadence = validate_review_cadence(review_cadence)
        live_target(self.root, provider, sid)
        path = self.folder('partners') / (alias_name(alias) + '.json')
        with locked(path.with_suffix('.lock')):
            if path.exists():
                prior = read_json(path)
                if prior['provider'] != provider or prior.get('id') != sid:
                    raise ValueError('Alias already names another session; choose a new alias')
                # Each supplied field replaces only itself; the other is kept.
                if partner_role is not None:
                    prior['partner_role'] = partner_role
                if review_cadence is not None:
                    prior['review_cadence'] = review_cadence
                if partner_role is not None or review_cadence is not None:
                    atomic_json(path, prior)
                return prior
            record = {'alias': alias, 'provider': provider, 'id': sid, 'project': str(self.root)}
            if partner_role is not None:
                record['partner_role'] = partner_role
            if review_cadence is not None:
                record['review_cadence'] = review_cadence
            atomic_json(path, record)
            return record

    def start(self, provider, kind, alias, prompt_file, role, model=None, effort=None, writable=False,
              partner_role=None, review_cadence=None):
        if partner_role is not None:
            if kind != 'partner':
                raise ValueError('An ongoing partner role is not a worker assignment')
            if not isinstance(partner_role, str) or not partner_role.strip():
                raise ValueError('Partner role must be nonempty text')
            partner_role = partner_role.strip()
        if review_cadence is not None:
            if kind != 'partner':
                raise ValueError('A review cadence is not a worker assignment')
            review_cadence = validate_review_cadence(review_cadence)
        alias_name(alias)
        prompt = Path(prompt_file).read_text()
        if not prompt.strip():
            raise ValueError('Supply the first actual contribution, not an empty launch')
        if kind == 'worker':
            # Retain the accepted managed-worker runner, not a second implementation.
            runner = Path(__file__).resolve().parents[2] / 'conductor/scripts/ask.py'
            reservation = self.folder('workers') / (alias + '.json')
            request = str(uuid.uuid4())
            with locked(reservation.with_suffix('.lock')):
                if reservation.exists():
                    raise ValueError('Worker alias already used; inspect its retained request before choosing a new job alias')
                atomic_json(reservation, {'kind': 'worker', 'request_id': request,
                            'runner': str(runner), 'status': 'start-uncertain', 'project': str(self.root)})
            args = [sys.executable, '-B', str(runner), '--project', str(self.root), 'run',
                    '--target', provider, '--session', 'agent-' + alias + '-' + request[:8],
                    '--role', role, '--request-id', request,
                    '--prompt-file', str(Path(prompt_file).resolve()), '--background']
            for flag, value in (('--model', model), ('--effort', effort)):
                if value:
                    args.extend([flag, value])
            if writable:
                args.append('--write')
            result = {'kind': 'worker', 'runner': str(runner), 'request_id': request,
                      'result': json.loads(command(args, self.root))}
            atomic_json(reservation, result)
            return result
        path = self.folder('partners') / (alias + '.json')
        # Reserve before any provider call. A failed/uncertain start cannot become
        # a silent duplicate on the next invocation.
        request = str(uuid.uuid4())
        with locked(path.with_suffix('.lock')):
            try:
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            except FileExistsError:
                raise ValueError('Partner alias already used; inspect its saved launch before choosing another alias') from None
            with os.fdopen(fd, 'w') as stream:
                json.dump({'alias': alias, 'provider': provider, 'project': str(self.root),
                           'status': 'start-uncertain', 'request_id': request,
                           'partner_role': partner_role, 'review_cadence': review_cadence}, stream)
        record = {'alias': alias, 'provider': provider, 'project': str(self.root),
                  'kind': 'partner', 'owned': True, 'requested_model': model,
                  'requested_effort': effort, 'write_requested': writable, 'request_id': request}
        if partner_role is not None:
            record['partner_role'] = partner_role
        if review_cadence is not None:
            record['review_cadence'] = review_cadence
        if provider == 'codex':
            native_socket = codex_home() / 'app-server-control/app-server-control.sock'
            if not native_socket.exists():
                command(['codex', 'app-server', 'daemon', 'start'], self.root)
            params = {'cwd': str(self.root), 'sandbox': 'workspace-write' if writable else 'read-only',
                      'approvalPolicy': 'never', 'allowProviderModelFallback': False}
            if model:
                params['model'] = model
            if effort:
                params['config'] = {'model_reasoning_effort': effort}
            with RPC(self.root) as rpc:
                started = rpc.call('thread/start', params)
            record.update(id=identifier(started['thread']['id']), observed_model=started.get('model'), status='started')
            atomic_json(path, record)
            result = self.ask(provider, record['id'], prompt, role, request, fresh=True, owned_partner=True)
        else:
            sid = str(uuid.uuid4())
            record.update(id=sid, status='start-uncertain', observed_model=None)
            atomic_json(path, record)
            framed = framed_prompt(self.root, request, role, prompt)
            self.new_request(provider, sid, prompt, role, request, None)
            tools = 'Read,Glob,Grep' + (',Edit,Write' if writable else '')
            before = {row['id'] for row in claude_sessions(self.root)}
            args = ['claude', '--bg', '--permission-mode', 'dontAsk',
                    '--permission-prompts', 'none', '--tools', tools, '--allowedTools', tools,
                    '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
                    '--settings', '{"crossSessionInbound":"accept"}',
                    self.prompt_pointer(request, framed)]
            for flag, value in (('--model', model), ('--effort', effort)):
                if value:
                    args.extend([flag, value])
            record['native_launch'] = command(args, self.root).strip()
            record['status'] = 'launched-unconfirmed'
            atomic_json(path, record)
            # --bg assigns its own ID (even when --session-id was supplied).
            # Resolve the launcher's exact short ID, never "latest" or cwd alone.
            match = re.search(r'^backgrounded\s+\S+\s+([0-9a-f]{8})\s*$', record['native_launch'], re.M)
            if not match:
                raise Unavailable('Claude launched but its native ID could not be resolved; do not launch again')
            record['native_short_id'] = match[1]
            atomic_json(path, record)  # the short id survives a slow launch
            deadline = time.monotonic() + 15
            found = []
            while time.monotonic() < deadline:
                found = [row for row in claude_sessions(self.root)
                         if row['id'].startswith(match[1]) and row['id'] not in before]
                if len(found) == 1:
                    break
                time.sleep(.1)
            if len(found) != 1:
                raise Unavailable('Claude launched (short id ' + match[1] + ') but was not listed within '
                                  '15s; it holds the prompt. Pair it by its full id once listed; do not launch again')
            record.update(id=found[0]['id'], status='started')
            atomic_json(path, record)
            pending = self.folder('requests') / (request + '.json')
            initial = read_json(pending)
            initial.update(session=record['id'], status='submitted-unconfirmed')
            initial['fingerprint'] = hashlib.sha256(json.dumps([provider, record['id'], prompt, role]).encode()).hexdigest()
            atomic_json(pending, initial)
            result = self.status(request)
        return {'partner': record, 'request': result,
                'note': 'Persistent native conversation; launch does not prove the contribution passed'}

    def new_request(self, provider, sid, prompt, role, request, log):
        info = owned(log, stat.S_ISREG) if log else None
        tail = ''
        if info:
            with log.open('rb') as stream:
                tail = log_tail(stream, info.st_size)
        record = {'request_id': request, 'provider': provider, 'session': sid,
                  'project': str(self.root), 'role': role, 'prompt': prompt,
                  'fingerprint': hashlib.sha256(json.dumps([provider, sid, prompt, role]).encode()).hexdigest(),
                  'log': str(log) if log else None, 'offset': info.st_size if info else 0,
                  'inode': info.st_ino if info else None, 'tail': tail,
                  'status': 'delivery-uncertain', 'created_at': time.time()}
        atomic_json(self.folder('requests') / (request + '.json'), record)
        return record

    def ask(self, provider, sid, prompt, role, request=None, fresh=False, owned_partner=False):
        request = identifier(request) if request else str(uuid.uuid4())
        path = self.folder('requests') / (request + '.json')
        fingerprint = hashlib.sha256(json.dumps([provider, sid, prompt, role]).encode()).hexdigest()
        lock = path.with_suffix('.lock')
        fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            if path.exists():
                record = read_json(path)
                if record.get('fingerprint') != fingerprint:
                    raise ValueError('Request ID already belongs to different work')
                return record  # Never resubmit, even after uncertain delivery.
            target = None if provider == 'codex' and owned_partner else live_target(self.root, provider, sid)
            framed = framed_prompt(self.root, request, role, prompt)
            frame = claude_frame(sid, request, framed) if provider == 'claude' else None
            log = None if fresh else transcript(self.root, provider, sid)
            record = self.new_request(provider, sid, prompt, role, request, log)
            try:
                if provider == 'claude':
                    record['status'] = send_claude(self.root, target, request, framed, frame=frame)
                else:
                    self.send_codex(sid, framed, request, record, owned_partner)
            except (Unavailable, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
                record['error'] = describe(exc)
            atomic_json(path, record)
        return record

    def send_codex(self, sid, framed, request, record, owned_partner, before_send=None):
        """One enqueue by one route, chosen before anything is sent.

        A daemon-loaded thread goes through the app-server queue. A thread a
        person opened (a TUI, `cli/user` in the store) goes through
        `codex queue` whenever the daemon does not have it loaded — a daemon
        never loads a TUI, so it reports every TUI as notLoaded, and that is
        not "offline". An app-server-created thread that is not loaded is woken
        only if this adapter created it; otherwise its owner's session is
        offline and it is refused. Only a failure to SEE the thread falls
        through; a failure while SENDING stops, retained as uncertain, so one
        request can never be enqueued twice.
        """
        row = store_row(self.root, sid)  # project and archive refusals for every route
        if daemon_socket().exists():
            try:
                rpc = RPC(self.root)
            except Unavailable:
                rpc = None  # No usable daemon; decide from the store.
            if rpc is not None:
                with rpc:
                    try:
                        current = rpc.call('thread/read', {'threadId': sid, 'includeTurns': False})['thread']
                    except Unavailable:
                        current = None  # Daemon has no view of this thread.
                    if current is not None:
                        if not belongs_to_project(current['cwd'], self.root):
                            raise Unavailable('Codex project identity changed')
                        loaded = status_name(current.get('status')) != 'notLoaded'
                        if loaded or (owned_partner and not row['tui']):
                            # From here on, any error is an attempted daemon
                            # send and propagates to be retained — never a
                            # fall-through to a second enqueue elsewhere.
                            record['route'] = 'app-server'
                            if not loaded:
                                # Only sessions this adapter created may be awakened.
                                rpc.call('thread/resume', {'threadId': sid})
                                record['native_wake'] = 'same owned session resumed; no fork'
                            if before_send:
                                before_send()
                            result = rpc.call('thread/queue/add', {'threadId': sid,
                                'clientUserMessageId': request, 'input': [{'type': 'text', 'text': framed}]})
                            record.update(queue_id=result['queuedSubmission']['id'], status='queued')
                            return
        if row['tui']:
            record['route'] = 'codex-queue'
            # Written before anything is attempted: a failed write sends nothing.
            pointer = self.prompt_pointer(request, framed,
                                          reply=record.get('kind') != 'arrival-notice')
            if before_send:
                before_send()
            try:
                command(['codex', 'queue', '--cd', str(self.root), '--thread', sid, '--message', pointer],
                        self.root)
            except (FileNotFoundError, PermissionError):
                # exec failed: no process could enqueue the notice. Other
                # native errors may follow an enqueue and remain uncertain.
                if record.get('kind') == 'arrival-notice':
                    record['status'] = 'notice-unavailable'
                raise
            # Exit 0 means enqueued, not consumed, not answered.
            record['status'] = 'submitted-unconfirmed'
            return
        if owned_partner:
            raise Unavailable('Codex native server is not running; start it to wake this partner')
        raise Unavailable('User session went offline; leave it queued for its owner, do not resume')

    def status(self, request):
        path = self.folder('requests') / (identifier(request) + '.json')
        if not path.exists():  # checked before the lock, so an unknown id leaves no file behind
            raise Unavailable('No request ' + identifier(request) + ' in this project')
        with locked(path.with_suffix('.lock')):
            return self._status(path, request)

    def _status(self, path, request):
        record = read_json(path)
        if not same_project(record['project'], self.root):
            raise Unavailable('Request belongs to another project')
        if record.get('kind') == 'arrival-notice':
            return record  # No expected reply, native log or readiness inference.
        if record['status'] == 'reply-received':
            return record
        if record['log'] is None:
            try:
                log = transcript(self.root, record['provider'], record['session'])
            except (Unavailable, OSError):
                return record
            record.update(log=str(log), inode=owned(log, stat.S_ISREG).st_ino)
            atomic_json(path, record)
        log = Path(record['log'])
        try:
            info = owned(log, stat.S_ISREG)
        except (OSError, Unavailable):
            return {**record, 'status': 'observation-unavailable',
                    'error': 'Native log moved or unreadable (archived thread?); not retried'}
        if info.st_ino != record['inode'] or info.st_size < record['offset']:
            return {**record, 'status': 'observation-unavailable', 'error': 'Native log replaced or truncated; not retried'}
        begin, end = markers(request)
        collected, last_block = '', object()
        with log.open('rb') as stream:
            # Inode and size miss a rewrite in place that keeps or grows the size;
            # the bytes before the offset would differ. Older records carry no tail.
            if 'tail' in record and log_tail(stream, record['offset']) != record['tail']:
                return {**record, 'status': 'observation-unavailable',
                        'error': 'Native log rewritten in place; not retried'}
            stream.seek(record['offset'])
            for raw in stream:
                if not raw.endswith(b'\n'):
                    break
                try:
                    event = json.loads(raw)
                except ValueError:
                    continue
                text = assistant_text(event, record['provider'])
                if not text:
                    continue
                # Events sharing a message id continue one block; a new id (or
                # none) starts another, and that boundary is a line boundary.
                block = block_id(event, record['provider'])
                same_block = block is not None and block == last_block
                last_block = block
                if collected and not same_block and not collected.endswith('\n'):
                    collected += '\n'
                collected += text
                opens_a_line = False
                if begin in collected:
                    at = collected.rfind(begin)
                    opens_a_line = at == 0 or collected[at - 1] == '\n'
                    # Keep the marker's line prefix: dropping it could promote
                    # an inline mention to a valid opening on the next event.
                    collected = collected[collected.rfind('\n', 0, at) + 1:]
                if (begin in collected and end in collected.split(begin, 1)[1]
                        and opens_a_line and delimits(collected, begin, end)):
                    answer = collected.split(begin, 1)[1].split(end, 1)[0]
                    if re.search(r'</?kerd-reply-[0-9a-f-]+>', answer):
                        return {**record, 'status': 'observation-unavailable',
                                'error': 'Overlapping reply markers; do not combine different answers'}
                    record.update(status='reply-received', reply=answer.strip(),
                                  received_at=time.time())
                    if record['provider'] == 'claude':
                        record['observed_model'] = event.get('message', {}).get('model')
                    atomic_json(path, record)  # Archive before returning or printing.
                    break
        return record

    def wait(self, request, seconds):
        if not math.isfinite(seconds) or seconds < 0:
            raise ValueError('Wait duration must be finite and nonnegative')
        deadline = time.monotonic() + seconds
        while True:
            record = self.status(request)
            if record.get('reply_expected') is False or record['status'] == 'reply-received' or time.monotonic() >= deadline:
                return record
            time.sleep(min(.25, max(0, deadline - time.monotonic())))


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        'Every command accepts --help without connecting or starting work. '
        'User guide: skills/agent/references/user-guide.md. '
        'In Claude Code with this skill loaded: /kerd:agent help.'))
    parser.add_argument('--project', default='.', help='Project directory (default: current directory)')
    sub = parser.add_subparsers(dest='action', required=True)
    cadence_help = ('How this partner reviews: checkpoints, before-push, end or on-request '
                    '(repeatable; on-request alone). Schedules review only inside authorized '
                    'work; grants no permission.')
    sub.add_parser('sessions', help='List discoverable project sessions and saved local partners')
    identity = sub.add_parser('identity', help='Read and corroborate this host session ID; no writes or dispatch')
    identity.add_argument('--provider', choices=['claude', 'codex'], required=True)
    arrival = sub.add_parser('arrival', help='Show verified self and restored peers; send deduplicated no-reply arrival notices')
    arrival.add_argument('--provider', choices=['claude', 'codex'], required=True)
    arrival.add_argument('--self-alias', help='Already-restored role held by this verified session')
    arrival.add_argument('--peer', action='append', help='Explicit established peer alias; otherwise use unambiguous private pairing (recorded role preferred)')
    handoff = sub.add_parser('handoff', help='Prepare or revoke this bound session\'s private role handoff')
    handoff.add_argument('--provider', choices=['claude', 'codex'], required=True)
    handoff.add_argument('--alias', required=True)
    handoff_mode = handoff.add_mutually_exclusive_group(required=True)
    handoff_mode.add_argument('--record', help='Final saved handoff file in this project')
    handoff_mode.add_argument('--cancel', action='store_true', help='Revoke handoff and restart recovery evidence')
    adopt = sub.add_parser('adopt', help='Keep this session, adopt a designated role, or recover its saved restart receipt')
    adopt.add_argument('--provider', choices=['claude', 'codex'], required=True)
    adopt.add_argument('--alias', required=True)
    adopt.add_argument('--expected-session', required=True, help='Exact currently bound UUID, never latest')
    adoption = adopt.add_mutually_exclusive_group()
    adoption.add_argument('--record', help='Designated handoff or restart-recovery file already restored by Switch In')
    adoption.add_argument('--confirm-replacement', action='store_true',
                          help='Use only after the person explicitly selects this role replacement')
    start = sub.add_parser('start', help='Launch a fresh worker or persistent partner with its first job',
                          description='Launch a fresh worker or persistent partner; read-only unless --write. '
                          'Workers return their own runner for status/wait; partners use this helper.')
    start.add_argument('--provider', choices=['claude', 'codex'], required=True)
    start.add_argument('--kind', choices=['worker', 'partner'], required=True)
    start.add_argument('--alias', required=True)
    start.add_argument('--prompt-file', required=True)
    start.add_argument('--role', required=True)
    start.add_argument('--partner-role', help='Ongoing partner responsibility; separate from this job and not permissions')
    start.add_argument('--review-cadence', action='append', help=cadence_help)
    start.add_argument('--model')
    start.add_argument('--effort')
    start.add_argument('--write', action='store_true', help='Enable file edits only within already-agreed authority')
    pair = sub.add_parser('pair', help='Remember an exact existing session under a local name; send no work')
    pair.add_argument('--provider', choices=['claude', 'codex'], required=True)
    pair.add_argument('--session', required=True)
    pair.add_argument('--alias', required=True)
    pair.add_argument('--partner-role', help='Set or update the ongoing responsibility of this exact partner; no dispatch')
    pair.add_argument('--review-cadence', action='append', help=cadence_help)
    sub.add_parser('partners', help='List this project\'s partner bindings with role and review cadence; '
                   'private metadata only, no discovery or contact')
    ask = sub.add_parser('ask', help='Send one contribution request to a saved partner')
    ask.add_argument('--alias', required=True)
    ask.add_argument('--prompt-file', required=True)
    ask.add_argument('--role', required=True)
    ask.add_argument('--request-id')
    for action in ('status', 'wait'):
        explanation = ('Retrieve a partner request status and any complete reply' if action == 'status'
                       else 'Wait for a partner reply; timeout does not cancel or resend')
        p = sub.add_parser(action, help=explanation, description=explanation)
        p.add_argument('request_id')
        if action == 'wait':
            p.add_argument('--seconds', type=float, default=30)
    args = parser.parse_args()
    try:
        agent = Agent(args.project)
        if args.action == 'sessions':
            result = agent.list()
        elif args.action == 'identity':
            result = agent.identity(args.provider)
        elif args.action == 'arrival':
            result = agent.arrival(args.provider, args.peer, args.self_alias)
        elif args.action == 'handoff':
            result = agent.handoff(args.provider, args.alias, args.record, args.cancel)
        elif args.action == 'adopt':
            result = agent.adopt(args.provider, args.alias, args.expected_session,
                                 args.record, args.confirm_replacement)
        elif args.action == 'start':
            result = agent.start(args.provider, args.kind, args.alias, args.prompt_file,
                                 args.role, args.model, args.effort, args.write, args.partner_role,
                                 args.review_cadence)
        elif args.action == 'pair':
            result = agent.pair(args.provider, args.session, args.alias, args.partner_role,
                                args.review_cadence)
        elif args.action == 'partners':
            result = agent.partners()
        elif args.action == 'ask':
            partner = read_json(agent.folder('partners') / (alias_name(args.alias) + '.json'))
            result = agent.ask(partner['provider'], partner['id'], Path(args.prompt_file).read_text(),
                               args.role, args.request_id, owned_partner=partner.get('owned', False))
        elif args.action == 'status':
            result = agent.status(args.request_id)
        else:
            result = agent.wait(args.request_id, args.seconds)
        # Keep full prompts and native log locations in private evidence, not
        # repeatedly in the controller's model context on every wait/status.
        def concise(value):
            if isinstance(value, dict):
                return {k: concise(v) for k, v in value.items()
                        if k not in ('prompt', 'fingerprint', 'log', 'offset', 'inode')}
            if isinstance(value, list):
                return [concise(v) for v in value]
            return value
        print(json.dumps(concise(result), ensure_ascii=True, indent=2))
    except (ValueError, OSError, KeyError, Unavailable, sqlite3.Error, subprocess.TimeoutExpired) as exc:
        print('agent: ' + describe(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
