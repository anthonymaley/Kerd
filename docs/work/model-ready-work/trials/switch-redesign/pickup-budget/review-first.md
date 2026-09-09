## Independent review — prepared-input pickup measurement

**Verified against source.** The supplied "CONTEXT.md — complete file" matches `/private/tmp/kerd-pickup-budget.qfKGD3/project/CONTEXT.md` verbatim (110 lines, `# Seinn — current pickup` through `See [trial changes and limits]`). The supplied Now section matches `TODO.md:8–39` verbatim, including both Owed subsections. No paraphrase, no answer smuggled into the packet.

**Arithmetic.** B = 13,026 across all three recorded controls (`observations.json` control-before, control-after, control-after-lean). 17,787 − 13,026 = 4,761; 18,825 − 13,026 = 5,799; 5,799 / 258,400 = 2.244%. All three figures hold, and `pickup-prepared` has one `context_readings` entry with zero `observed_operations`, so "peak" is unambiguous for this run. Note `control-after` shows `cachedInputTokens: 0` against 8,704 elsewhere at identical 13,026 input — useful evidence that caching does not move the input count.

**Blockers.**

1. *Bracketing is incomplete.* `observations.json` ends at `pickup-prepared`; no post-control is recorded. `method.md:88–90` requires bracketing with a new post-control, and `:46–49` withholds a pass on control drift. The pass is not awardable on the evidence in hand — only on the evidence plus a landed post-control at ≈13,026.

2. *Restoration lost two open producer decisions that were in the supplied text.* `unresolved_memory` omits the `add_shares` toggle disposition (CONTEXT.md:65–67; TODO.md:43, "Producer's call") and the iOS privacy-gate experience choice (CONTEXT.md:68–71, "The experience choice remains open"; TODO.md:45–52, "deliberately parked"). The lean run captured both. It also drops the staged `D1-DELETE-TEST` file (TODO.md:26–28) and all four Owed-tail items (TODO.md:31–36). Because this material was supplied in-prompt, this is a reader-selection shortfall, not a preparation omission — but it is exactly the "unresolved memory affecting those answers" the review was asked to test, and it is the strongest argument against scoring restoration as correct.

3. *A binding constraint was dropped from `next_decision`.* CONTEXT.md:32 says "Do not implement a reasonable default." Run 1 carried it ("no default may be implemented"); the prepared answer does not. Constraint loss on a gating decision is worse than fact loss.

**Non-blockers worth recording.** `authority` cites only CONTEXT.md; `docs/work/switch-trial/changes.md` (trial authority, lines 23–25) was neither supplied nor read. Its substance is duplicated at CONTEXT.md:26–27 and 36–52, so no authority was actually lost — but the packet's authority coverage now rests on one file. The prepared answer also omits the live-checkout no-prune limit (CONTEXT.md:49–52) and TODO.md:1–7. `last_completed` drops the reader-correction deployment, which run 1 included; `3c9e976` survives under `next_obligation`.

**Unsupported conclusion to guard against.** The reader performed zero retrieval, so 4,761 measures *consuming a curated packet*, not *performing a pickup*. Controller selection cost is real and excluded. `method.md:82–83` concedes this; any downstream sentence of the form "prepared Switch pickup costs 4,761 added tokens" would overstate it. n=1 for this arm. Separately, the control prompt (`control.md`, two lines) is inside B, so added-input is understated by roughly its ~40 tokens — immaterial against an 8,000 margin.

**Limits of this review.** Read-only; no shell, so I could not confirm the working tree is clean or that HEAD is the pinned commit — I confirmed only that the two supplied file bodies match the files. I could not verify that the bridge captured *every* usage notification: `run.py:9–10` imports `codex_roll`/`roll` from `skills/switch/scripts`, outside this pack. The single-turn shape makes a missed peak unlikely, not excluded. I did not read native session histories or Git transport records.

## Controller disposition

The final bracketing control completed after this review's evidence snapshot: see post-control.json. It matches 13,026 input, resolving the timing blocker. The omitted decisions, owed work and explicit prohibition remain substantive: numerical success alone is not a restoration pass. The next variant adds a current-source coverage check and automates assembly of the same complete sources. Historical evidence remains unchanged.

