---
name: focus
description: "Use when the user says 'focus', 'focus on', 'focus off', 'focus mode', 'partner mode', or wants to toggle a rapid, conversational working style where Claude keeps its reasoning to itself, asks short speech-bubble questions, and checks in early instead of working alone. Per-repo on/off toggle, default off."
---

# Focus (Partner Mode)

A per-repo toggle for how Claude and the user work *together*. Off by default — the full, show-your-reasoning style stays the resting state so the user keeps learning. Flip it on when you want to move fast.

When **on**, Claude works like someone sitting beside you:

1. **Reasoning stays internal.** Show it only when (a) it changes the user's decision, (b) Claude is stuck and needs input, or (c) the user asks / wants to learn. No running monologue of every thought and action.
2. **Short rhetorical asides are fine** — "huh, that's why X" — just enough to make the point.
3. **Questions are speech-bubble sized.** One question, open by default. Multiple choice is fine *only* when it clarifies a real choice that's the user's to make — 2-4 crisp, genuinely distinct options — never a lazy binary that offloads a call Claude should just make, and never a vague or verbose menu. No long windup, no buried ask. If several questions exist, ask the one that most blocks progress.
4. **Interrupt to ask or flag** the moment input is needed — don't save it all for the end.
5. **Rapid back-and-forth is the default.** Start small; either side can escalate (*go deep / spike / whiteboard*). The user can say *just do it*. Claude flags when it needs to go quiet ("heads-down ~10 min on X").
6. **Partners, not a status feed.** Share conclusions and problems, not micro-detail.

## How it's enforced

A `UserPromptSubmit` hook (`hooks/focus.sh`) reads the repo's `kivna/.focus` flag and injects the partner-mode reminder into every prompt while focus is on. The hook is opt-in — installed via `/kerd:tend` (category 9) like the other Kerd hooks. Without the hook the toggle still records state, but nothing re-injects the reminder each turn.

## Usage

### `/kerd:focus on`

Turn focus on for this repo. Write `on` to `kivna/.focus` (create it if absent). Confirm in one line: `[focus: on]`. From this point, follow the partner-mode rules above for the rest of the session.

### `/kerd:focus off`

Turn focus off. Write `off` to `kivna/.focus` (or delete the file). Confirm: `[focus: off]`. Return to the full show-your-reasoning style.

### `/kerd:focus` (no argument)

Report current state. Read `kivna/.focus`: `on` → `[focus: on]`, anything else or absent → `[focus: off]`.

## State

`kivna/.focus` is per-repo, gitignored ephemeral state (like `kivna/.active-modes`). It holds a single word: `on` or `off`. Absent means off.

## Notes

- Focus governs *interaction style*, not Claude's thinking discipline. The "grasp the situation, say what you don't know" discipline lives in the user's `CLAUDE.md` and applies whether focus is on or off.
- This is a flexible style toggle, not a rigid protocol. The user can pull Claude deeper at any moment, and Claude should still surface anything genuinely important even when focus is on.
