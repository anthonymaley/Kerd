---
type: regex
weight: 1
target: trace
pattern: '"command":"(?=(?:[^"\\]|\\.)*handoff\.py)(?:[^"\\]|\\.)*(?:\\n|(?<![\w\\]))python3?\s+\S+(?:[^"\;&|]|\\[^n])*\bboundary\b(?:[^"\;&|]|\\[^n])*(?:\s*2>&1)?(?:\s*\|\s*(?:grep|tail|head|cat)\b(?:[^"\;&|]|\\[^n])*)*(?:\s*(?:;|&&|\|\|)\s*echo\b(?:[^"\;&|]|\\[^n])*)*"[^\n]*\n(?:(?![^\n]*"tool_result")[^\n]*\n)*[^\n]*"tool_result","content":"(?:[^"\\]|\\.)*boundary_ok(?![\s\S]*(?:boundary_refused|"command":"(?:[^"\\]|\\.)*(?:(?:\\n|(?<![\w\\]))git\b(?:\s+-[Cc]\s+\S+|\s+--?[\w-]+(?:=\S+)?)*\s+(?:commit|push|merge|rebase|reset|cherry-pick|revert|tag|am|stash)\b|(?:handoff\.py(?:[^"\\]|\\.)*\bsave\b|(?:\\n|(?<![\w\\]))python3?\s+\S+\s+--project\s+\S+\s+save\b))))'
---
handoff.py's boundary check (by path or a variable holding it), run as the last statement of its command (2>&1, an output filter such as grep, tail or head, and an echo may follow; its own output must still show boundary_ok), returned boundary_ok, and nothing later in the trace refused a boundary, saved through handoff.py or ran a mutating git subcommand (commit, push, merge, rebase, reset, cherry-pick, revert, tag, am, stash). Limit: a script that runs git inside itself is not seen.
