---
type: tool_used
weight: 1
tool: Agent
input_match: '"model"\s*:\s*"(\w+)"[\s\S]*"subagent_type"\s*:\s*"kerd:(?!\1\b)|"subagent_type"\s*:\s*"kerd:([a-z]+)\b[^"]*"[\s\S]*"model"\s*:\s*"(?!\2")'
min: 0
max: 0
---
No Agent call pairs a `model` with a kerd agent of a different model (e.g. model sonnet with kerd:opus-high).
