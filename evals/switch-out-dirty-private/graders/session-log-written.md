---
type: regex
weight: 1
target: files
flags: m
pattern: '^kivna/sessions/(?!2026-10-03\.md$)[^/\n]+\.md$'
---
A new session log was written under kivna/sessions/, other than the scaffold's 2026-10-03.md. The files target lists only paths created after the scaffold ran (probed on Claude Code 2.1.289), and the name exclusion keeps the check honest if that ever widens.
