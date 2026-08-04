#!/usr/bin/env python3
"""Entry gates: route a work slug through the ladder, or refuse a rung whose
declared inputs are missing.

    python3 tools/gates/gate.py route <slug> [--json]
    python3 tools/gates/gate.py check <slug> <rung> [--json]
    python3 tools/gates/gate.py audit [--json]
    python3 tools/gates/gate.py selftest

route always exits 0 — it reports where work enters, it never refuses.
check is the refuser: exit 0 on pass or spike bypass, 1 on refusal. audit is
the repo-wide mechanical sweep: exit 0 clean, 1 with problems. selftest runs
kit's fixture suite in a temp tree: exit 0 or 1. Any other invocation prints
this usage text and exits 2. Every decision lives in kit.py; this module
only parses argv and renders kit's dicts as line-based text, or as JSON via
--json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit


def _print_have_need(result):
    for item in result["have"]:
        print(f"have: {item}")
    for item in result["need"]:
        print(f"need: {item}")


def _cmd_route(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if len(argv) != 1:
        print(__doc__)
        return 2
    slug = argv[0]
    result = kit.route(kit.ROOT, slug)

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
    if len(argv) != 2:
        print(__doc__)
        return 2
    slug, rung = argv
    if rung not in kit.RUNGS:
        print(__doc__)
        return 2

    result = kit.check_rung(kit.ROOT, slug, rung)
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
    route_result = kit.route(kit.ROOT, slug)
    print(f'enters at: {route_result["enters_at"]}')
    return 1


def _cmd_audit(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv:
        print(__doc__)
        return 2

    problems = kit.audit(kit.ROOT)

    if as_json:
        print(json.dumps(problems))
        return 0 if not problems else 1

    if not problems:
        print("audit: clean")
        return 0
    for p in problems:
        print(f"problem: {p}")
    print(f"audit: {len(problems)} problems")
    return 1


def _cmd_selftest(argv):
    if argv:
        print(__doc__)
        return 2
    return kit.selftest()


COMMANDS = {
    "route": _cmd_route,
    "check": _cmd_check,
    "audit": _cmd_audit,
    "selftest": _cmd_selftest,
}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print(__doc__)
        return 2
    return COMMANDS[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
