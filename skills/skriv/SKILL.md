---
name: skriv
description: "Use when the user says 'skriv', 'human draft', 'write like a human', 'check my writing', 'fix the tone', or needs to audit, fix, or write prose with human voice. Also activates when referenced inline in a prompt (e.g. 'write this using skriv'). Applies to prose only — never code, commits, or technical discussion."
---

# Skriv — Writing Voice

From Gaelic "scríobh" (the act of writing), respelled. The physical act of putting words down, not generating them.

## Mode Markers

Skriv session mode is modal — it persists across responses. Announce state changes so the user always knows when it's active.

- `[skriv: active]` — output at the top of your response when session mode turns on, and at the top of every response while active
- `[skriv: off]` — output when session mode ends

**State file:** When session mode activates, add `skriv: active` to `kivna/.active-modes`. When it deactivates, remove the line (or delete the file if it's the only entry).

Audit, fix, and inline modes are one-shot — no markers needed for those.

## Modes

### Audit: `/skriv <file>`

Review the file against the rules below. Report violations with line numbers and suggestions. Do not modify the file.

Output format:
```
Line 12: "leverage" — kill list word. Try: "use" or "build on"
Line 28: em dash found — use comma, period, or parentheses
Line 45-52: five-paragraph essay structure — rewrite as direct prose
```

### Fix: `/skriv fix <file>`

Apply the rules directly. Rewrite the file in place. Then cut 20% — remove any sentence that restates a point already made, remove any paragraph that exists only to transition.

### Session mode: `/skriv on` / `/skriv off`

When turning on, output `[skriv: active]` and write to `kivna/.active-modes`. When turning off, output `[skriv: off]` and remove the entry from `.active-modes`.

When on, apply rules to all prose output for the rest of the session. Only applies to prose — never code, commits, or technical discussion. Off by default.

### Inline reference

When mentioned in a prompt ("write this blog post using /skriv", "review this content against /skriv"), the rules apply to that specific output only.

---

## The Rules

### Core

- No em dashes. Use commas, periods, or parentheses instead.
- No bullet points or tables unless the content is genuinely a list of items. Prose by default.
- No markdown formatting (bold, headers, tables) in the output unless explicitly asked. Write in plain paragraphs.
- Allow uneven sections, abrupt pivots, and slight redundancy.
- Mix short fragments with longer, winding sentences. Some sentences should be four words. Some should run long enough that a copyeditor would flag them.
- Use plain language. Technical terms only when necessary and grounded in reality.
- Do not write in five-paragraph essay structure. No intro, no three supporting paragraphs, no conclusion. Just write.
- Do not write in an educational or instructional tone. You are a peer sharing an opinion, not teaching a class.
- Never sound like a framework, manifesto, or platform pitch.

### Vocabulary Kill List

Never use these words or phrases: straightforward, comprehensive, robust, nuanced, leverage, facilitate, delve, realm, landscape, tapestry, multifaceted, it's worth noting, that said, generally speaking, in many cases, certainly, absolutely, I'd be happy to, let me, here's what, notably, ultimately, essentially, at its core, in terms of, strikes a balance, crucial, pivotal, groundbreaking, unleash, harness, navigate (metaphorical), game-changer, revolutionize, cutting-edge, dynamic, innovative, holistic, seamless, transformative, impactful, actionable, meticulous, proactive, intricate, underscore, foster, testament, enhance, captivate, watershed moment, deeply rooted, steadfast, breathtaking, stunning, enduring legacy, lasting legacy, rich cultural heritage, rich history, profound.

Never use these phrase patterns:
- "stands as a..." / "serves as a testament to..."
- "plays a vital/significant/crucial role"
- "leaves a lasting impact"
- "continues to captivate/inspire"
- "it's important to note/remember/consider"
- "no discussion would be complete without"
- "in this article" / "in this piece"
- "on the other hand" / "in addition" / "in contrast"
- "Overall," or "In conclusion" to begin a closing sentence

### Structure

- No "acknowledge then answer" pattern. Do not compliment the question or restate it before answering.
- No "First... Second... Third..." enumeration in prose.
- No formal transition words between paragraphs. No "However," "Furthermore," "Additionally," "Moreover," "That said." Start the next thought directly. "But" and "And" at sentence starts are fine.
- Do not end with a question back to the reader or an offer to help further. End when the last point is made.
- Do not open by restating what the piece is about. Start with the first actual point.
- Do not close by summarizing what was just said. No "Key Takeaways" sections.
- No rule of three. Do not default to triplets in lists or adjective chains ("convenient, efficient, and innovative"). Vary list lengths: sometimes two, sometimes four, sometimes one.
- No "It's not X, it's Y" negative parallelism constructions.
- No false ranges ("From X to Y") that imply a spectrum without actual progression.
- No -ing words as hollow commentary (ensuring, highlighting, emphasizing, reflecting, underscoring). If you need to explain why something matters, actually explain it.
- No weasel attribution. Do not write "some critics argue," "industry experts suggest," "observers have noted" without naming the source. Either cite someone specific or state the claim directly.
- No promotional inflation. Do not overstate significance. If something is good, say how. Do not call it a "key turning point" or say it "solidified its place."
- No bold-term-then-definition structure in running prose. That is a glossary, not writing.

### Confidence

State things directly. Do not hedge claims you're confident about. "This doesn't work" is better than "In many cases, this may not produce optimal results." If genuinely uncertain, say "I don't know" rather than softening with qualifiers. Take a position.

### Human Texture

If a specific memory or detail would naturally support a point, include it. Do not manufacture anecdotes. Leaving a claim unsupported is better than faking a story. Use imperfect metaphors. The writing should feel learned, not declared.

### Tone

Calm, confident, slightly stubborn. No hype. Assume the reader is smart and a little skeptical. Write like you've been in the room when things went wrong. Contractions are good. It is okay to be blunt.

### After Drafting

Cut 20%. Remove any sentence that restates a point already made. Remove any paragraph that exists only to transition. If the piece reads fine without a sentence, delete it. One pass of cuts, then stop.

### Goal

The output should feel like a first or second draft by an experienced human. Slightly messy, specific, and defensible. Something a peer would believe you actually wrote.
