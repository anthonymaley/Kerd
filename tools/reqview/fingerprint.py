#!/usr/bin/env python3
"""Rule 9's fingerprint — the shared PYTHON implementation. Not the only one.

docs/design/requirement-shape.md rule 9 says every implementation must share
the recipe exactly. The intent was to make that true by having one; that intent
is not met, and the paragraph below says why rather than pretending. reqview.py
(the register's seal) and tools/gates/kit.py (the design gate's view lock)
both import this module.

THE CLAIM THIS DOCSTRING USED TO MAKE — "and nothing else computes a
fingerprint" — WAS FALSE, and cold eyes falsified it on 2026-08-29. There is a
SECOND implementation of rule 9, in JavaScript, emitted into the register's own
HTML by reqview.py (search `function fingerprint` there). It exists for a real
reason: the page recomputes approval state in the browser with no server to ask,
so the recipe has to cross the language boundary. It is field-for-field the same
recipe today, and NOTHING TESTS THE TWO AGAINST EACH OTHER — so the guarantee
this module was created to provide holds by inspection rather than by check.
Editing the recipe here means editing it there, by hand, with nothing to catch
you. That is a named gap with a TODO row, not a solved problem.

Not counter-examples, so nobody re-reports them: kit.req_statement_hash is a
DIFFERENT recipe (a stripped single statement) for the register's Approved hash
and link stamps, and says so; progress_kit's local `fingerprint` is an md5 over
a JSON model, unrelated to rule 9.

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
