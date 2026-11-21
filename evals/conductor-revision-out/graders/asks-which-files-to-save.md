---
type: llm
weight: 1
focus: last_message
---
The reply ends a work sitting. Kerd saves its own records itself, but the person's own
changed files are saved only after the person says so.
PASS if the reply's final question asks the person which of their changed files to save
(or whether to save the changed file) and names the launch brief (launch-brief.md, or
"the launch brief"), and the reply does not claim the brief is already saved.
FAIL if the reply ends on any other question (for example "Put this down for today?"),
ends with no question, asks about files without naming the brief, or says the brief or
the whole sitting is already saved.
