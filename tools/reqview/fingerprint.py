#!/usr/bin/env python3
"""Rule 9's fingerprint — the one implementation, shared.

docs/design/requirement-shape.md rule 9 says every implementation must share
the recipe exactly; the way to make that true is to have one. reqview.py
(the register's seal) and tools/gates/kit.py (the design gate's view lock)
both import this module, and nothing else computes a fingerprint.

Recipe: four fields in order — statement, why, traces, depends — each
trimmed with every internal whitespace run collapsed to one space; joined
with single newlines; SHA-256 over the UTF-8 bytes; first twelve hex
characters. A derived statement is prefixed `derived: ` so flipping the
flag un-approves.

A view (a drawing — docs/design/gate-visuals.md) uses the same recipe with
its file content as the statement and the other three fields empty, so the
hashed text is the collapsed content followed by three newlines.
"""
import hashlib


def fingerprint(statement, why, traces, depends, derived):
    """Rule 9. Labels are already stripped by the parser (whole, modifier included).
    A derived statement is prefixed `derived: ` so flipping the flag un-approves."""
    stmt = ("derived: " + statement) if derived else statement
    parts = [stmt, why, traces, depends]
    joined = "\n".join(" ".join(p.split()) for p in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def view_fingerprint(text):
    """A view's lock: the recipe over its file content as the statement,
    the other three fields empty. Whitespace-only edits do not change it."""
    return fingerprint(text, "", "", "", False)
