#!/usr/bin/env python3
"""Run every skill's unit tests, so CI runs them too.

Discovery is by path, not a maintained list: any `skills/*/scripts/tests/test_*.py` or `tools/tests/test_*.py`
is collected and run as a dotted module from the repository root. A new test file is
picked up by existing it.

Why this exists rather than a bare `unittest discover`: the tests directories are not
packages, so discovery from the root collects nothing, and each skill's tests import
their own siblings. Running them as dotted modules from the root works only when every
test module puts its own directories on `sys.path` before importing them — which is
now the contract this runner depends on, and the reason it is worth having in CI. A
module that violates it fails here as an ImportError rather than silently not running.

Exit 0 when every test passes, 1 on any failure, error or missing test, 2 when no test
files are found at all (which means discovery broke, not that the suite is clean).
"""
from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_GLOBS = ("skills/*/scripts/tests/test_*.py", "tools/tests/test_*.py")


def module_names(root=REPO_ROOT):
    """Dotted module names for every discovered test file, sorted for a stable order."""
    names = []
    for path in sorted(p for pattern in TEST_GLOBS for p in root.glob(pattern)):
        relative = path.relative_to(root).with_suffix("")
        names.append(".".join(relative.parts))
    return names


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    verbosity = 2 if ("-v" in argv or "--verbose" in argv) else 1

    names = module_names()
    if not names:
        print(f"refused: no test files matched {TEST_GLOBS} under {REPO_ROOT}",
              file=sys.stderr)
        return 2

    # Import as dotted modules from the root, the same way a developer runs one file.
    sys.path.insert(0, str(REPO_ROOT))
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)

    print(f"\n{len(names)} test modules, {result.testsRun} tests")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
