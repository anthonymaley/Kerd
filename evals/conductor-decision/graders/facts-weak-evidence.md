---
type: llm
weight: 1
focus: last_message
---
Judge only the **Facts** entry of the decision block.
PASS if Facts treats the evidence about who uses `larder export` as weak: it is one
forum message from a single user and there is no usage count (no telemetry), so
the number of affected people is unknown; and/or it notes the comma bug was found
by reading the code, not by running it on real data. It must plainly flag the
evidence as thin, not present export as clearly unused or clearly in use.
FAIL if Facts treats a single message as proof either way, or omits that usage is unknown.
