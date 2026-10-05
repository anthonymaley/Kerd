---
type: llm
weight: 1
focus: last_message
---
The reply shows a grid with columns Task, Who, Model, Effort, Status. The controller
row is the row whose work this session performs itself (no Agent call).
PASS if the grid has exactly one controller row.
FAIL if it has none, two or more, or no grid at all.
