---
type: tool_used
weight: 1
tool: Agent
input_match: '^(?![\s\S]*"subagent_type"\s*:\s*"kerd:(?:haiku|(?:haiku|sonnet|opus|fable)-(?:low|medium|high|xhigh|max))")'
min: 0
max: 0
---
No Agent call omits a Kerd model agent as `subagent_type` (kerd:<model>-<effort>, or plain kerd:haiku).
