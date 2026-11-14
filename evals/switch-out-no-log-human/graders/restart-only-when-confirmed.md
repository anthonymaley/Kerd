---
type: regex
weight: 1
match: not_contains
pattern: '^(?![\s\S]*(?:SESSION SAVED ✓|SAVED LOCALLY))[\s\S]*/clear(?: and|, then) /kerd:switch in'
---
The restart line appears only in a box whose heading confirms the save: SESSION SAVED ✓, or SAVED LOCALLY for a committed save with no Git remote configured.
