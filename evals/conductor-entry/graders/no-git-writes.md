---
type: tool_used
weight: 1
tool: Bash
input_match: '"command":"(?:[^"\\]|\\.)*git\s+(?:-C\s+\S+\s+)?(?:commit|push|add|stash(?!\s+(?:list|show)\b)|reset|checkout|switch|restore|rm|mv|merge(?![-\w])|rebase|clean|pull|branch\s+(?!-{1,2}(?:list|show-current|v|a|r|l)\b)\S|worktree\s+add|tag\s+\S)'
min: 0
max: 0
---
Entry runs no Git command that changes the repo or creates a branch (commit, push, add, checkout, switch, branch <name>, merge, worktree add, ...).
