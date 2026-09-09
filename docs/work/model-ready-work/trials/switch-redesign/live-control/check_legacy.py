#!/usr/bin/env python3
"""Run the unchanged earlier suite against this trial's new library and CLI."""
import argparse
import importlib.util
from pathlib import Path
import sys
import unittest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("artifact", type=Path)
args = parser.parse_args()
root = args.artifact.resolve()
sys.path.insert(0, str(root))
tests = Path(__file__).resolve().parents[1] / "failed-save/output/test_pickup_preview.py"
spec = importlib.util.spec_from_file_location("unchanged_legacy_tests", tests)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Retain the old tests and assertions, point only their CLI fixtures at the new result.
module.ROOT, module.PROGRAM = root, root / "pickup_preview.py"
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
