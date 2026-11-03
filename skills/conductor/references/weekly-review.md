# The weekly review, and turning work into skills

Contents:

- [The weekly review](#the-weekly-review)
- [Five lenses](#five-lenses)
- [Missed decisions without nagging](#missed-decisions-without-nagging)
- [The review record](#the-review-record)
- [Make this a skill, in the moment](#make-this-a-skill-in-the-moment)
- [Pasted notes that hold decisions](#pasted-notes-that-hold-decisions)

**Why:** Anthropic's Economics team found, in “How employment is changing at
Anthropic” (2026-10-16), that human attention is the bottleneck when people work
with Claude, and that the share of interactive sessions spent improving the setup
(building agent tools, reviewing agent output, monitoring) rose from 10% to 22%.
The review spends a little of the person's attention once a week so the rest of
the week asks for less of it.

## The weekly review

The weekly review is a look-back over the current project's own work, in any
project using Kerd: it reviews that project's work, not Kerd. It covers the
last 7 days, or the window the person names. It runs as ordinary Conductor work,
offered by Switch In's open work when the last review is over 7 days old or none
has run.

It reads, bounded to the window:

- the project's Switch session logs (`kivna/sessions/` by convention);
- its Claude Code chat history, candidates in `~/.claude/projects/<project-dir>/*.jsonl`,
  where `<project-dir>` is the project's absolute path with each `/` written as `-`;
- its Codex history where it exists, candidates in `~/.codex/sessions/`.

The folder name is only a candidate: different paths can map to the same Claude
folder name. Choose files from their metadata first, before any chat content is
read: keep a file only when its recorded working directory (`cwd` on each Claude
event, `session_meta` for Codex) is this project's canonical absolute path. Then
take only the events whose own timestamps fall inside the window; a resumed
conversation can span several weeks, so a file's dates do not bound it. Nothing
outside the window and nothing from other projects enters the review. The review
writes nothing until the person says go.

Its report opens with Conductor's three lines, **Found**, **Needs you** and
**Unsure** (the [shape of every report](journey.md#the-shape-of-every-report)),
then ranks items by the time each would save the person. At most five items are
on screen; the rest go in the [review record](#the-review-record).

## Five lenses

The review reads the window through five lenses:

1. **Corrections.** Each time the person corrected Claude or redid its work. For
   each, say where the fix belongs: the project's instructions (`CLAUDE.md` or
   its equivalent), a skill, or nowhere because it was one-off. When it belongs
   somewhere, give the exact wording to add.
2. **Repeated jobs.** Jobs done twice or more in the window. Each is a candidate
   skill, built through [the in-the-moment path](#make-this-a-skill-in-the-moment).
3. **Questions.** Did each closing bubble ask what its Needs you line said, and
   could the person answer it cold?
4. **Unsure items.** Defaults taken mid-run under the concert stop rule (an
   undoable gap takes its safest default and is reported for reversal) that
   nobody reviewed afterwards.
5. **Missed decisions.** Decisions the person stated in chat or in pasted
   material that never reached a record. These follow the rules below.

## Missed decisions without nagging

Only a decision whose subject is still live in open work survives. A decision
whose subject the work has moved on from is dropped without being raised; the
review record counts how many were dropped, and the screen does not.

Survivors appear as one grouped list, each a single line saying where it came
from (“Tuesday's chat: exports keep the original file names”). One bubble asks
whether they are settled:

> 💬 **Are these settled?**

Per item, the person's answer decides:

- **Settled:** write it into the record it belongs in, shown as a before → after
  edit. The person may add detail, links or files, and those go in with it.
- **Solved or drop:** never raised again.
- **Skipped:** stays as it is and is not asked again.

Every item raised is written to the decision ledger in the review folder
(`decisions.md` beside the dated records), one line each: where it came from
(conversation and time, or the pasted file), the decision, and its answer:
settled, dropped or skipped. Writing those lines is part of answering the list,
not a separate approval. Before asking, every review and every pasted-notes list
checks the ledger and leaves out anything already there, so a skipped or dropped
decision is not asked again even when a later window reads the same conversation.
If the person declines the ledger, say that the no-repeat promise cannot hold
without it.

## The review record

Each run writes one dated record. With `kivna/vault.json` carrying
`"work_notes": "vault"`, it is `notes:weekly-review/<YYYY-MM-DD>.md`; otherwise
`docs/work/weekly-review/<YYYY-MM-DD>.md`. It holds the window, the exact time it reviewed
through, the full findings under each lens, the count of dropped decisions, and
what the person settled or dropped. The next review starts from that reviewed-through
time, so overlapping windows do not raise the same item twice.

Writing this record after the person's go is part of the review, not a separate
approval. Its date is what Switch In reads to decide whether to offer the next
review.

## Make this a skill, in the moment

When the person says “make this a skill”, or a Repeated jobs finding is chosen,
it is ordinary Conductor work, built only on the person's go:

- Build the skill in the person's own project with Anthropic's skill-creator,
  asking for its light path: no full eval or benchmark loop unless the person
  asks for one.
- Instructions come first; a script only for deterministic work, which is
  skill-creator's own rule.
- With the skill, Conductor adds two lines: how to run it, and what to check
  after each run.

A host without skill-creator: say so, and follow Anthropic's published skill
guidance instead.

## Pasted notes that hold decisions

When the person pastes notes, links or files and says they hold decisions,
Conductor does the same as [missed decisions](#missed-decisions-without-nagging)
at once, rather than waiting for the week: one grouped list, each line saying
where it came from, one bubble asking whether they are settled, and each answer
handled the same way, and each answer written to the
[decision ledger](#missed-decisions-without-nagging).
