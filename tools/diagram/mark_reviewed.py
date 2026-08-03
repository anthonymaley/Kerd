#!/usr/bin/env python3
"""Mark a generated diagram as read. Blue resets to nothing.

    python3 tools/diagram/mark_reviewed.py docs/plans/<file>.excalidraw

Baseline for BLUE is an explicit act, not a commit or a regeneration — both of
those happen far more often than anyone reads the thing, which would make blue
mean "changed since some moment nobody chose".
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import mark_reviewed

if len(sys.argv) != 2:
    sys.exit(__doc__)
path = os.path.abspath(sys.argv[1])
print("marked reviewed:", mark_reviewed(path))
