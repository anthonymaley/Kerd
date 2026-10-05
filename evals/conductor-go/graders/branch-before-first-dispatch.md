---
type: tool_order
weight: 1
before: { tool: Bash, input_match: '"command":"(?:[^"\\]|\\.)*git\s+(?:-C\s+\S+\s+)?(?:checkout\s+(?:-\S+\s+)*-b|switch\s+(?:-\S+\s+)*-c|branch(?:\s+--?\S+)*|worktree\s+add\s+(?:\S+\s+)*?-b)\s+concert/larder-shop\b' }
after: Agent
---
The concert branch is created before the first player is dispatched.
