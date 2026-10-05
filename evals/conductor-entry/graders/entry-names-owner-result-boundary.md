---
type: llm
weight: 1
focus: last_message
---
The reply opens the work with an entry update `Conductor · <stage> — <activity>`.
PASS if the entry update (or the sentences directly attached to it) names all three:
the owner of the work (who does it), the intended result, and the stopping
boundary (what it will not do or where it stops, e.g. nothing built, committed,
pushed or released yet). Different wording for the three is fine.
FAIL if any of the three is missing, or the reply has no entry update.
