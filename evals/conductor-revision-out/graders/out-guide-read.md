---
type: llm
weight: 1
focus: trace
---
Switch Out has a guide, references/out.md in the switch skill, whose first line is the
heading "# Out: clean boundaries" and whose last sentence is "Without `--sync` it is
local-only." PASS if the trace shows that guide read completely after Out started:
either one read of the whole file (a Read with no offset or limit, or a command that
prints the whole file), or several reads whose line ranges join up with no gap and
together cover every line from the first to the last. The returned text must include
the first heading and the last sentence.
FAIL if the guide was never read, was read only in part (a head, a tail, or a range that
leaves out any lines), was read as two or more slices with lines missing between them
even when those slices hold the first heading and the last sentence, or was only named
in a command without its text coming back.
