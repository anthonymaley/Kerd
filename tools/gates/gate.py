#!/usr/bin/env python3
"""Entry gates: route a work slug through the ladder, or refuse a rung whose
declared inputs are missing.

    python3 tools/gates/gate.py route <slug> [--root PATH] [--json]
    python3 tools/gates/gate.py check <slug> <rung> [--root PATH] [--json]
    python3 tools/gates/gate.py audit [--root PATH] [--json]
    python3 tools/gates/gate.py release [--root PATH] [--json]
    python3 tools/gates/gate.py selftest

route always exits 0 — it reports where work enters, it never refuses.
check is the refuser: exit 0 on pass or spike bypass, 1 on refusal. audit is
the repo-wide mechanical sweep: exit 0 clean, 1 with problems. release is
the release-rules sweep (version sync, capability-list identity, kerd: namespace):
exit 0 clean, 1 with problems. selftest runs kit's fixture suite in a temp tree:
exit 0 or 1. Any other invocation prints this usage text and exits 2. Every
decision lives in kit.py; this module only parses argv and renders kit's dicts
as line-based text, or as JSON via --json.

WHICH TREE IS AUDITED. The gate aims at the PROJECT, never at its own install
path. Kerd ships inside a plugin cache, so a tool that derived its root from
its own file location would audit the cache when a consuming project ran it —
the one thing the machinery must not do. Resolution order, first match wins:

    --root PATH          explicit, and it always wins
    $CLAUDE_PROJECT_DIR  the harness's own name for the project directory
    the nearest .git ancestor of the working directory
    the working directory

A root that looks like no project at all (no `.git`, no `docs/product/`) is
refused by name rather than audited into a false clean. selftest takes no
--root: it builds its own temp trees, which is why every kit function takes
`root` as a parameter.
"""
import json
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit


class RootError(Exception):
    """A --root that cannot be used, carrying the message the user needs."""


def _pop_root(argv):
    """Take `--root PATH` or `--root=PATH` out of argv and resolve it.

    Returns (root, remaining_argv). Raises RootError with a message naming the
    fix — never falls back to the install path, because a silent fallback to
    the plugin cache is the exact failure this flag exists to prevent."""
    rest, explicit = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--root":
            if i + 1 >= len(argv):
                raise RootError("--root needs a path: --root /path/to/project")
            explicit = argv[i + 1]
            i += 2
            continue
        if a.startswith("--root="):
            explicit = a.split("=", 1)[1]
            if not explicit:
                raise RootError("--root needs a path: --root /path/to/project")
            i += 1
            continue
        rest.append(a)
        i += 1

    if explicit is not None:
        root, why = os.path.abspath(os.path.expanduser(explicit)), "--root"
        if not os.path.isdir(root):
            raise RootError(f"--root is not a directory: {root}")
    elif os.environ.get("CLAUDE_PROJECT_DIR"):
        root, why = os.path.abspath(os.environ["CLAUDE_PROJECT_DIR"]), "$CLAUDE_PROJECT_DIR"
        if not os.path.isdir(root):
            raise RootError(f"$CLAUDE_PROJECT_DIR is not a directory: {root}")
    else:
        root, why = _walk_up_for_git(os.getcwd())

    if not _looks_like_project(root):
        raise RootError(
            f"{root}\n"
            f"  (resolved from {why})\n"
            "  has no `.git` and no `docs/product/`, so it is not a project this\n"
            "  gate can audit. Run from inside the project, or name it:\n"
            "      python3 <path>/gate.py audit --root /path/to/project")
    return root, rest


def _walk_up_for_git(start):
    """The nearest ancestor holding `.git`, else the starting directory.

    Walking up handles being run from a subdirectory. It deliberately cannot
    reach the install path: it only ever moves toward the filesystem root from
    where the user actually is."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur, "the nearest .git ancestor of the working directory"
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start), "the working directory"
        cur = parent


def _looks_like_project(root):
    return (os.path.isdir(os.path.join(root, ".git"))
            or os.path.isdir(os.path.join(root, "docs", "product")))


def _print_have_need(result):
    for item in result["have"]:
        print(f"have: {item}")
    for item in result["need"]:
        print(f"need: {item}")


def _cmd_route(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    root, argv = _pop_root(argv)
    if len(argv) != 1:
        print(__doc__)
        return 2
    slug = argv[0]
    result = kit.route(root, slug)

    if as_json:
        print(json.dumps(result))
        return 0

    for r in result["rungs"]:
        n = len(r["need"])
        print(f'{r["rung"]}  pass' if n == 0 else f'{r["rung"]}  need {n}')
    print(f'enters at: {result["enters_at"]}')
    if result["next"]:
        print(f'missing for {result["next"]}:')
        for item in result["missing_for_next"]:
            print(f"need: {item}")
    return 0


def _cmd_check(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    root, argv = _pop_root(argv)
    if len(argv) != 2:
        print(__doc__)
        return 2
    slug, rung = argv
    if rung not in kit.RUNGS:
        print(__doc__)
        return 2

    result = kit.check_rung(root, slug, rung)
    passed = not result["need"]

    if as_json:
        print(json.dumps(result))
        return 0 if passed else 1

    if passed:
        if result["bypass"]:
            print("SPIKE — ladder bypassed; output re-enters through the gates")
        else:
            print(f'PASS {rung} — {slug}: {len(result["have"])} inputs on disk')
        return 0

    print(f'gate: {rung} — {slug}')
    _print_have_need(result)
    print(f'REFUSED at {rung} — {slug}: {len(result["need"])} missing')
    route_result = kit.route(root, slug)
    print(f'enters at: {route_result["enters_at"]}')
    return 1


def _cmd_audit(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    root, argv = _pop_root(argv)
    if argv:
        print(__doc__)
        return 2

    problems = kit.audit(root)
    findings = kit.register_findings(root)

    if as_json:
        # the JSON shape stays a bare problems list — the stable contract;
        # findings are non-blocking and ride the text output only
        print(json.dumps(problems))
        return 0 if not problems else 1

    for f in findings:
        print(f"finding: {f}")
    if not problems:
        tail = f" ({len(findings)} findings)" if findings else ""
        print(f"audit: clean{tail}")
        return 0
    for p in problems:
        print(f"problem: {p}")
    print(f"audit: {len(problems)} problems")
    return 1


def _cmd_release(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    root, argv = _pop_root(argv)
    if argv:
        print(__doc__)
        return 2

    problems = kit.release_audit(root)

    if as_json:
        print(json.dumps(problems))
        return 0 if not problems else 1

    if not problems:
        print("release: clean")
        return 0
    for p in problems:
        print(f"problem: {p}")
    print(f"release: {len(problems)} problems")
    return 1


def _root_selftest():
    """Pin the resolution order. The case that matters is the last one: a tool
    run outside any project REFUSES rather than falling back to where it is
    installed. A silent fallback would audit the plugin cache and report clean,
    which is worse than reporting nothing."""
    import shutil
    # realpath: on macOS /var is a symlink to /private/var, and os.getcwd()
    # returns the resolved form — so an unresolved fixture path compares unequal
    # for a reason that has nothing to do with the resolution order under test.
    cases, cwd0 = [], os.getcwd()
    tmp = os.path.realpath(tempfile.mkdtemp(prefix="gateroot-"))
    env0 = os.environ.get("CLAUDE_PROJECT_DIR")

    def case(name, want, fn):
        try:
            got = fn()
        except RootError as e:
            got = "REFUSED: " + str(e).split("\n")[0]
        cases.append((name, got, want, got == want))

    try:
        proj = os.path.join(tmp, "proj")
        sub = os.path.join(proj, "docs", "product")
        other = os.path.join(tmp, "other")
        bare = os.path.join(tmp, "bare")
        os.makedirs(os.path.join(proj, ".git"))
        os.makedirs(sub)
        os.makedirs(os.path.join(other, ".git"))
        os.makedirs(bare)

        os.environ.pop("CLAUDE_PROJECT_DIR", None)
        os.chdir(bare)
        case("--root wins", proj, lambda: _pop_root(["--root", proj])[0])
        case("--root=PATH form", proj, lambda: _pop_root(["--root=" + proj])[0])
        case("--root is removed from argv", ["audit"],
             lambda: _pop_root(["audit", "--root", proj])[1])
        case("no root anywhere -> REFUSED",
             "REFUSED: " + bare,
             lambda: _pop_root([])[0])

        os.environ["CLAUDE_PROJECT_DIR"] = proj
        case("$CLAUDE_PROJECT_DIR used", proj, lambda: _pop_root([])[0])
        case("--root beats $CLAUDE_PROJECT_DIR", other,
             lambda: _pop_root(["--root", other])[0])

        os.environ.pop("CLAUDE_PROJECT_DIR", None)
        os.chdir(sub)
        case("walk up to the .git ancestor", proj, lambda: _pop_root([])[0])
    finally:
        os.chdir(cwd0)
        if env0 is None:
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
        else:
            os.environ["CLAUDE_PROJECT_DIR"] = env0
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


def _cmd_selftest(argv):
    if argv:
        print(__doc__)
        return 2
    bad = 0
    for name, got, want, good in _root_selftest():
        if not good:
            bad += 1
            print(f"FAIL root: {name}\n  got  {got!r}\n  want {want!r}")
    if bad:
        print(f"root resolution: {bad} failures")
        return 1
    print("root resolution: 7 cases passed")
    return kit.selftest()


COMMANDS = {
    "route": _cmd_route,
    "check": _cmd_check,
    "audit": _cmd_audit,
    "release": _cmd_release,
    "selftest": _cmd_selftest,
}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print(__doc__)
        return 2
    try:
        return COMMANDS[argv[0]](argv[1:])
    except RootError as e:
        print(f"gate: cannot resolve the project root.\n  {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
