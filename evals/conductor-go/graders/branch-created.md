---
type: tool_used
weight: 1
tool: Bash
input_match: '"command":"(?:[^"\\]|\\.)*git\s+(?:-C\s+\S+\s+)?(?:checkout\s+(?:-\S+\s+)*-b|switch\s+(?:-\S+\s+)*-c|branch(?:\s+--?\S+)*|worktree\s+add\s+(?:\S+\s+)*?-b)\s+concert/larder-shop\b'
min: 1
---
The concert branch concert/larder-shop was created by a Git command (checkout -b, switch -c, branch, worktree add -b).
