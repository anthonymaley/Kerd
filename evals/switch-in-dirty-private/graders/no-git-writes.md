---
type: tool_used
weight: 1
tool: Bash
input_match: '"command":"(?:[^"\\]|\\.)*git\s+(?:-C\s+\S+\s+)?(?:commit|push|add|stash(?!\s+(?:list|show)\b)|reset|checkout|restore|rm|mv|merge|rebase|clean)\b'
max: 0
min: 0
arm: both
---
In runs no Git command that changes the repo (commit, push, add, stash, reset, checkout, restore, rm, mv, merge, rebase, clean).
