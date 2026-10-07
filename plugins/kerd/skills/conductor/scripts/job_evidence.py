#!/usr/bin/env python3
"""Reads only structured model and effort fields from Claude job transcript records; never emits conversation text.

Locates one native subagent transcript (<projects-root>/*/<session>/subagents/agent-<ID>.jsonl)
and its .meta.json. Each record is parsed, but only the top-level effort and message.model of
assistant records are used and counted; metadata contributes agentType and model.
The format is private to Claude Code and was observed in 2.1.270-2.1.272; it is not a
documented interface. So anything missing, refused, unexpected or partial (the 50 MB limit
reached, or a malformed record) returns "status": "unverified" with a reason and exit 0,
keeping whatever counts were made. Only invalid arguments exit 2 ("refused").
The session is the current host session (CLAUDE_CODE_SESSION_ID); an explicit --session is
accepted only with an explicit --projects-root (fixtures) that does not resolve to the default
store ~/.claude/projects, and a located file or folder that resolves into that store is refused
before anything is opened. Both files are lstat-checked,
opened without following links, and must be regular files owned by the current user.
Output carries no paths, session or agent IDs, prompts, tool input or message text;
field values are included only when their type, length and characters validate.
"""

import argparse
from collections import Counter
import glob
import json
import os
import re
import stat
import sys


TRANSCRIPT_LIMIT = 50 * 1024 * 1024
META_LIMIT = 1024 * 1024
AGENT_ID = re.compile(r"a?[0-9a-f]{8,40}")
SESSION = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
EFFORT = re.compile(r"[a-z]{1,16}")
MODEL = re.compile(r"[A-Za-z0-9._-]{1,64}")
LABEL = re.compile(r"[A-Za-z0-9:._-]{1,64}")
DEFAULT_ROOT = os.path.join("~", ".claude", "projects")
OPEN_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)


class Refused(Exception):
    """Invalid arguments: exit 2."""


class Unverified(Exception):
    """Evidence unavailable: the reason names the check, never a path or ID."""


def identity_problem(st):
    # Group/other permission bits are not refused: native files are 0644 or 0600 by host default.
    if stat.S_ISLNK(st.st_mode):
        return "it is a symbolic link"
    if not stat.S_ISREG(st.st_mode):
        return "it is not a regular file"
    if st.st_uid != os.getuid():
        return "it is not owned by the current user"
    return None


def open_checked(path, label):
    """lstat the file, open it without following links, and confirm the same regular, owned file."""
    try:
        linked = os.lstat(path)
    except FileNotFoundError:
        raise Unverified(label + " missing") from None
    except OSError as exc:
        raise Unverified(f"{label} could not be inspected: {exc.strerror}") from None
    problem = identity_problem(linked)
    if problem:
        raise Unverified(f"{label} refused: {problem}")
    try:
        fd = os.open(path, OPEN_FLAGS)
    except FileNotFoundError:
        raise Unverified(label + " missing") from None
    except OSError as exc:
        raise Unverified(f"{label} unreadable: {exc.strerror}") from None
    try:
        opened = os.fstat(fd)
    except OSError as exc:
        os.close(fd)
        raise Unverified(f"{label} could not be inspected: {exc.strerror}") from None
    problem = identity_problem(opened)
    if problem or (opened.st_dev, opened.st_ino) != (linked.st_dev, linked.st_ino):
        os.close(fd)
        raise Unverified(f"{label} refused: {problem or 'it changed while being opened'}")
    return fd


def read_metadata(path, result):
    """Fill agent_type and requested_model from .meta.json; every problem is a gap, not a failure."""
    gaps = result["gaps"]
    try:
        fd = open_checked(path, "metadata")
    except Unverified as exc:
        gaps.append(str(exc))
        return
    try:
        with os.fdopen(fd, "rb") as stream:
            data = stream.read(META_LIMIT + 1)
    except OSError as exc:
        gaps.append(f"metadata unreadable: {exc.strerror}")
        return
    if len(data) > META_LIMIT:
        gaps.append("metadata exceeds 1 MB")
        return
    try:
        meta = json.loads(data)
    except (ValueError, RecursionError):
        gaps.append("metadata is not valid JSON")
        return
    if not isinstance(meta, dict):
        gaps.append("metadata is not a JSON object")
        return
    # An absent model means the call made no per-call request; resolution then continues
    # through the definition, CLAUDE_CODE_SUBAGENT_MODEL and the caller. An absent agent
    # type is a gap.
    for field, key, name, absent_gap in (("agent_type", "agentType", "agent type", True),
                                         ("requested_model", "model", "requested model", False)):
        value = meta.get(key)
        if isinstance(value, str) and LABEL.fullmatch(value):
            result[field] = value
        elif key not in meta:
            if absent_gap:
                gaps.append(f"metadata has no {name}")
        else:
            gaps.append(f"metadata {name} is not a valid value")


def count_records(fd, result):
    """Stream the transcript line by line up to TRANSCRIPT_LIMIT, counting validated assistant values only.

    Returns True when the limit cut the transcript short.
    """
    models, efforts = Counter(), Counter()
    consumed = 0
    truncated = False
    try:
        with os.fdopen(fd, "rb") as stream:
            while True:
                remaining = TRANSCRIPT_LIMIT - consumed
                if remaining <= 0:
                    truncated = bool(stream.read(1))
                    break
                line = stream.readline(remaining)
                if not line:
                    break
                consumed += len(line)
                if not line.endswith(b"\n") and consumed >= TRANSCRIPT_LIMIT and stream.read(1):
                    truncated = True
                    break
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except (ValueError, RecursionError):
                    result["malformed_lines"] += 1
                    continue
                if not isinstance(record, dict):
                    result["malformed_lines"] += 1
                    continue
                if record.get("type") != "assistant":
                    continue
                effort = record.get("effort")
                if isinstance(effort, str) and EFFORT.fullmatch(effort):
                    efforts[effort] += 1
                message = record.get("message")
                if isinstance(message, dict):
                    model = message.get("model")
                    if isinstance(model, str) and MODEL.fullmatch(model):
                        models[model] += 1
    except OSError as exc:
        raise Unverified(f"transcript unreadable: {exc.strerror}") from None
    finally:
        result["observed_models"] = dict(sorted(models.items()))
        result["observed_effort"] = dict(sorted(efforts.items()))
    return truncated


def observe(args, environ, result):
    session = args.session
    if session is None:
        session = environ.get("CLAUDE_CODE_SESSION_ID") or None
        if session is None:
            raise Unverified("no session")
        if not SESSION.fullmatch(session):
            raise Unverified("host session id is not a UUID")
    root = args.projects_root if args.projects_root is not None else os.path.expanduser(DEFAULT_ROOT)
    # Only the escaped root and the validated session and agent ID reach the pattern.
    pattern = os.path.join(glob.escape(root), "*", session, "subagents", "agent-" + args.agent_id + ".jsonl")
    matches = glob.glob(pattern)
    if args.session is not None:
        refuse_default_store(matches)
    if not matches:
        raise Unverified("not found")
    if len(matches) > 1:
        raise Unverified("ambiguous")
    transcript = matches[0]
    try:
        fd = open_checked(transcript, "transcript")
    except Unverified as exc:
        raise Unverified("not found" if str(exc) == "transcript missing" else str(exc)) from None
    try:
        read_metadata(transcript[:-len(".jsonl")] + ".meta.json", result)
    except BaseException:
        os.close(fd)
        raise
    truncated = count_records(fd, result)
    if not result["observed_effort"] and not result["observed_models"]:
        raise Unverified("no effort or model records")
    if not result["observed_effort"]:
        raise Unverified("no effort records")
    if not result["observed_models"]:
        raise Unverified("no model records")
    # Partial evidence is never observed; the partial counts stay in the result.
    if truncated:
        raise Unverified("transcript exceeds 50 MB; counts are partial")
    if result["malformed_lines"]:
        raise Unverified("malformed records; counts are partial")
    result["status"] = "observed"


class DefaultStore:
    """The default projects store, compared by realpath and, when it exists, by device and inode."""

    def __init__(self):
        path = os.path.expanduser(DEFAULT_ROOT)
        self.real = os.path.realpath(path)
        try:
            info = os.stat(path)
            self.identity = (info.st_dev, info.st_ino)
        except OSError:
            self.identity = None

    def is_store(self, path):
        if os.path.realpath(path) == self.real:
            return True
        if self.identity is None:
            return False
        try:
            info = os.stat(path)
        except OSError:
            return False
        return (info.st_dev, info.st_ino) == self.identity

    def contains(self, path):
        """True when PATH resolves to the store or anywhere beneath it."""
        current = os.path.realpath(path)
        while True:
            if self.is_store(current):
                return True
            parent = os.path.dirname(current)
            if parent == current:
                return False
            current = parent


def is_default_root(root):
    """True when ROOT resolves to the default store: same realpath, or the same directory when both exist."""
    return DefaultStore().is_store(root)


def refuse_default_store(matches):
    """For an explicit --session: refuse when any match, its metadata or a directory on its chain resolves
    into the default store (a symlinked project or session folder, or a symlinked file). Nothing is opened."""
    store = DefaultStore()
    for match in matches:
        chain = [match, match[:-len(".jsonl")] + ".meta.json"]
        folder = match
        for _ in range(4):  # subagents, session, project, root
            folder = os.path.dirname(folder)
            chain.append(folder)
        if any(store.contains(path) for path in chain):
            raise Refused("--session is not accepted for a transcript inside the default projects store")


def parser():
    build = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    build.add_argument("--agent-id", required=True, help="Native agent ID, e.g. a434d67120ca1df6d")
    build.add_argument("--session", help="Session UUID; only with a --projects-root other than the default "
                                         "store (fixtures). Default: CLAUDE_CODE_SESSION_ID")
    build.add_argument("--projects-root", help="Projects store to read. Default: ~/.claude/projects")
    return build


def evidence(argv=None, environ=None):
    """Return (exit code, result) without printing."""
    environ = os.environ if environ is None else environ
    args = parser().parse_args(argv)
    try:
        if not AGENT_ID.fullmatch(args.agent_id):
            raise Refused("agent id must be an optional 'a' followed by 8-40 lowercase hex digits")
        if args.projects_root is not None and (not args.projects_root or "\0" in args.projects_root):
            raise Refused("--projects-root must be a non-empty path")
        if args.session is not None:
            if args.projects_root is None:
                raise Refused("--session is accepted only together with --projects-root")
            if not SESSION.fullmatch(args.session):
                raise Refused("--session must be a lowercase UUID")
            if is_default_root(args.projects_root):
                raise Refused("--session is not accepted against the default projects store")
    except Refused as exc:
        return 2, {"status": "refused", "reason": str(exc)}
    result = {"status": "unverified", "reason": None, "agent_type": None, "requested_model": None,
              "observed_models": {}, "observed_effort": {}, "malformed_lines": 0, "gaps": []}
    try:
        observe(args, environ, result)
    except Refused as exc:
        return 2, {"status": "refused", "reason": str(exc)}
    except Unverified as exc:
        result["status"], result["reason"] = "unverified", str(exc)
    return 0, result


def main(argv=None):
    code, result = evidence(argv)
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
