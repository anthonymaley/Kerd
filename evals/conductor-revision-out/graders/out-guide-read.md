---
type: regex
weight: 1
target: trace
pattern: '"tool_result","content":"(?:[^"\\]|\\.)*# Out: clean boundaries(?:(?:[^"\\]|\\.)*Without `--sync` it is local-only\.|[\s\S]*"tool_result","content":"(?:[^"\\]|\\.)*Without `--sync` it is local-only\.)'
---
Out really ran: its whole guide came back in tool output (first heading, then its last sentence). Same pattern as the switch-out cases; the anchor is checked by skills/switch/scripts/tests/test_eval_graders.py.
