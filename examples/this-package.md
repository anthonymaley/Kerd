# This package, from rehearsal to concert

The README, the website, the guides, the pictures and the other two examples were made
in one piece of work with Kerd, across one evening and the next morning. It was the
first real use of rehearsal and the concert, which shipped in 0.139.0 the same night.
This is the record of how it went, including what went wrong.

Written by the conducting session, so it is a self-report. Where something was checked
by someone else, it says who.

## Picking up

The owner sat down and asked Kerd to pick up. The arrival said, in plain words, that
0.139.0 was out, that nobody had used it on real work yet, and recommended one thing:
rehearse one real piece of work with it. It ended on its one question.

> 💬 **Start a Conductor session?**

He said yes. That opened the conversation about the work and approved nothing in it.
Asked which piece of real work, he answered with this package: a website,
documentation, examples and a README, made with Conductor and agents.

## Rehearsal: eight exchanges, no fixed order

Conductor started a sketchbook on the first turn and wrote each answer into it before
asking the next question. One question at a time, each with a proposed answer above it.

- **Who is it for?** Conductor proposed a developer landing on the repository cold. He
  widened it to developers, product people and anyone using AI to produce meaningful
  output. That one answer moved the whole package from protocol-first to
  plain-words-first.
- **Is this the right package?** Shown as a picture: two front doors (the README and a
  website) leading to guides, then examples, with diagrams shared underneath. He agreed
  and corrected it: overview pictures matter more than technical ones, because they are
  how a newcomer understands how it works and why they should care.
- **What is done?** Four goals, the first being that a reader who has never seen Kerd
  can read only the README and say what it does, how it works and why they would care.
- **Which real work may the examples show?** He named two projects. Conductor looked,
  found one was a private, unreleased product, and proposed using only the public one,
  with every quotation held for him to read before anything is published. He agreed.
- **Is this the story Kerd tells?** The old README led with a ladder and gates. The
  proposed story led with three things that go wrong when you work with an AI. He said
  yes, and added a design bar for the whole thing.

Twice Conductor said it was nearly ready and named the one thing still missing. The
third time it said "I think we're ready", showed a picture of the concert in three
batches, and asked for the go. He gave it.

## The concert

**Batch 1, two players in parallel.** One built the look and the home page. One rebuilt
the README from 1,546 lines to about 150 and moved the release history to the changelog.
Conductor checked the second by script rather than by trust: all 967 lines of history
and all 518 lines of reference text are byte-identical in their new homes.

He looked at the home page the next morning, said it worked, and changed two sentences.

**Batch 2, seven players in parallel:** five overview pictures, ten guides across four
players, two real examples, and the remaining site pages. Every return was read against
its part of the score and against a snapshot of the files taken before dispatch.

**Batch 3:** eleven guide pictures, three readers who had never seen Kerd, this page,
and the comparison with the four goals.

## What went wrong, and how it was caught

- **The install commands in the old README did not exist.** A player flagged that it had
  not verified them. Conductor checked them against the installed command-line tool's
  own help and corrected them in three places. Read from help output; not run.
- **An invented eighth step.** Conductor's own brief listed eight step names for the
  ladder. The player wrote a description for the eighth and said plainly that it was an
  inference. Checked against the gate tool: there are seven.
- **Pictures that never appeared.** The first player built frames that fill themselves
  when a picture arrives, and said it had never seen one filled. The picture player
  rendered the real page, found them all empty, and isolated the cause. Repaired.
- **A snapshot taken late.** Conductor took its first before-dispatch snapshot after
  dispatching, because it read that part of its own guide late. Nothing had been
  written yet, so it was recoverable, and the next batch was done in the right order.

Every one of these was caught by somebody reading or rendering the real thing. None was
caught by a player grading its own work, because the briefs told them not to.

## How it ended

Three readers who had never seen Kerd read the pages: a product manager and a sceptical
developer on the README alone, and a first-time user on the getting-started page alone.
The first reading said the pages told you why to care and not what would happen on your
machine: nothing on what Kerd writes, what it costs, how to remove it, or what you
actually see. None of that was wrong in the pages. It was missing, because Conductor's
own steps had never asked for it. The two steps were repaired and performed again, and
three new readers read the result.

Against the four goals agreed in rehearsal:

1. **A newcomer can say what it does, how it works and why they would care, from the
   README alone.** Met in substance on the second reading: both readers described all
   three correctly in their own words. One reservation stands. A product person with no
   Claude Code and no Git folder still cannot use Kerd, and the page now says that first.
2. **A newcomer can install and run a first sitting from the getting-started page
   alone.** Mostly met: the reader could install, confirm it worked, and follow the
   order for a new project, which they called the clearest part of the page. They still
   wanted to see the closing screen rather than read a description of it. And the
   reader read the page; nobody ran an install from it.
3. **Every capability has a guide with its own overview picture.** Met, checked by
   script: nine guides, nine pictures, each guide pointing at its own.
4. **Every example is real.** Met: two are drawn from real session logs with every
   quotation checked against its source line, and the third is this page.

Twenty agents took part, fourteen players and six readers, with one conductor. Every
one ran on the model and effort it was given, read back from the record afterwards.

What this does not show: whether real people find any of it useful. That cannot be read
from inside the work.
