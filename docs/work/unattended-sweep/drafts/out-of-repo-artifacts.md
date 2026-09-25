# Out-of-repo artifacts: a proposal

Draft by the composer, 2026-09-25, for Anthony to react to. Nothing changed yet.

## The gap

Kerd work produces or leans on things outside the repository: claude.ai artifacts, the live
site, messages to people, pull requests. Each gets written wherever the session happened to
be, and Switch In reads only CONTEXT.md, TODO.md and the newest session log. So a link
survives one sitting, then sinks.

Three real cases:

1. **The launch-outcomes visual (2026-09-02).** A private claude.ai artifact. Its link went
   into a session log and a decisions.md entry marked "owed a home in this repo". It was
   rescued the next day only because someone went looking.
2. **The Kerd Sitting Map (2026-09-14).** A claude.ai artifact of the delegation diagrams.
   Its link is in one place, `kivna/sessions/2026-09-14.md`, which Switch In stopped
   reading the next day. In practice, lost.
3. **The team note to SAM and Aubel.app (2026-09-23).** Sent by Anthony, outside Kerd. The
   waiting replies are tracked only in the launch-plan sketchbook, which is local and not
   in the pickup set.

The site URL went right: it became part of the product, so the README carries it.

## Recommendation

Add one short section to CONTEXT.md, `## Outside the repo`. One line per live thing: what it
is, the link, who owns it, and what it is waiting on. Switch Out keeps it current the same
way it keeps the rest of CONTEXT.md: a line leaves when the thing is saved on disk, merged,
answered or no longer needed.

What earns a line: someone will open it again, or something waits on it. A link used once
stays in the session log as today.

Why CONTEXT.md, not a new file: it is committed, read at every Switch In, and holds "what
is currently true". A live artifact or an unanswered note is exactly that. Sketchbooks are
local now, so they cannot be the home.

## Hypothesis and how we'd know

I believe this stops links sinking, because the one file every arrival reads will carry them
until someone decides they are done. We would know it worked if, over the next three weeks:

- no decisions.md entry or sketchbook says "owed a home" for longer than one sitting, and
- a check at each Switch Out finds no claude.ai link in that day's session log that is
  missing from CONTEXT.md, unless the log says it was finished with.

If the section grows past about eight lines, that is the signal it has become a link dump
and the pruning rule is not gripping.

## What it costs

A few lines in `docs/state-contract.md` and Switch Out's step, a patch release, and a few
lines of pickup reading per Switch In. Seeding it: the Sitting Map and the team note.

## One question

> 💬 **The repository is public: is it acceptable for private claude.ai artifact links, which only you can open, to sit in CONTEXT.md?**
