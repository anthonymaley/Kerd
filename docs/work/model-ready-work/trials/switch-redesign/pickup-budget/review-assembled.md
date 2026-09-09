## Independent assessment — assembled prepared-input pickup

**Packet fidelity (verified against raw records).** The supplied `CONTEXT.md` body matches `/private/tmp/kerd-pickup-budget.qfKGD3/project/CONTEXT.md` lines 1–110 verbatim; the supplied `## Now` matches `TODO.md:8–39` verbatim including both child sections. No paraphrase, no answer smuggled in.

**The four previously-flagged losses are restored** (`assembled-observation.json` reply):
- `add_shares` disposition — `unresolved_memory.open_decisions_or_unknowns` (source CONTEXT.md:65–67). ✓
- iOS privacy-gate experience choice + background re-arming (CONTEXT.md:68–70). ✓
- `D1-DELETE-TEST` staged file (TODO.md:26–28). ✓
- All four Owed-tail items (TODO.md:31–36). ✓
- The dropped prohibition is back: `next_decision.constraint` = "Do not implement a default" (CONTEXT.md:32). ✓

**No invented fact found.** "Playback verification completed" is CONTEXT.md:17; `cascade.c:103-104` and `3c9e976` are TODO.md:15–17; "intentionally unsynchronized" is supported by `synchronized: false` plus the prompt's local-only authority.

**Supported blocker — one, narrow.** Explicit prohibitions are still being dropped, including one bound to the *next* action. CONTEXT.md:47–48 ("Ask before work requiring the user at a TV. Ask one open question at a time; do not hide a choice in either/or prose") is absent from `authority.prohibitions`, while the answer correctly names the producer's TV-masking question as the gating decision — the constraint governing how that question is put did not survive. Alongside it, CONTEXT.md:68 ("must not reuse `KruthoHolder.unlock()`") is absent although the answer preserves the parked choice it qualifies. The candidate instruction added at `submitted-pickup-assembled.md:1` and In-reference lines 171–177 targets exactly this class; it caught the decisions and owed work but not these prohibitions.

**Non-blocking losses** (archival rather than next-work): CONTEXT.md:49–52 no-prune provenance; evidence caveat CONTEXT.md:79–84 (chunk-case discrimination, "do not repeat the overbroad claim"); CONTEXT.md:88–90 agent-source reverification. From the retained deletion caveat, "Keep intended safe-target and confirmation-scope checks" (CONTEXT.md:87) was dropped while the hypothesis was kept — owed work, but not the next action.

**Wording drift worth recording.** The answer renders TODO.md:31–32 as "strict `device_pub` decoding in `handle_post_endorse`"; the record says it decodes *leniently* while the unlock path is strict. Composer framing survives; the current-state fact is ambiguous as written.

**Preparation completeness.** `## Now` excludes TODO.md:43, :45–52, :53, where the `add_shares`, iOS-gate and masking rows live in full. Their dispositions are carried by CONTEXT, so no material loss — but the answer's fidelity on those three rests on CONTEXT's summary alone.

**Limits.** Read-only; no shell, so I did not confirm HEAD is the pinned commit or the tree clean — only that the two supplied bodies match the files on disk. I did not read native histories or transport records. The new post-control is not in the pack; per the measurement note I withhold any numerical judgement, and I report no controller check as my own. n=1, curated packet, zero retrieval — this measures consuming a packet, not performing a pickup.

## Controller disposition

The final control is recorded in assembled-post-control.json and matches 13,026 input. The meaningful omissions still prevent a combined pass. The next correction preserves explicit prohibitions with their original scope/wording, not only a general short summary. No source restriction is removed to make the result pass.

