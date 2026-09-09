#!/usr/bin/env python3
"""Run the 19 handoff tests against a reviewed artifact, without checkout edits."""
import argparse
import ast
from pathlib import Path
import subprocess
import sys
import types
import unittest

BASE = "6393778c4993405ffec17616ab3950821e9d7795"
FOLDER = "docs/work/switch-trial/device-build"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("repository", type=Path, help="Clone containing the handoff commit")
parser.add_argument("artifact", type=Path)
args = parser.parse_args()
artifact = args.artifact.resolve()

def original(name):
    return subprocess.check_output(
        ["git", "-C", str(args.repository), "show", f"{BASE}:{FOLDER}/{name}"],
        text=True,
    )

sys.path.insert(0, str(artifact))
tests = types.ModuleType("handoff_baseline_tests")
tests.__file__ = str(artifact / "test_pickup_preview.py")
exec(compile(original("test_pickup_preview.py"), tests.__file__, "exec"), tests.__dict__)
suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
assert suite.countTestCases() == 19
result = unittest.TextTestRunner(verbosity=1).run(suite)

def functions(source):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}

before = functions(original("pickup_preview.py"))
after = functions((artifact / "pickup_preview.py").read_text())
changed = [name for name, body in before.items() if after.get(name) != body]
assert sorted(changed) == ["_parser", "main"], changed
print("All pre-existing functions except CLI parser/dispatch have identical ASTs.")
sys.exit(0 if result.wasSuccessful() else 1)
