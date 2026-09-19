# MusicTUI, across sittings

MusicTUI is a terminal client for Apple Music. Its repository keeps a dated log for
every sitting, written at the end by Kerd's Switch and read at the start of the next
one. There are about fifty of them.

What follows is one piece of work traced through eight sittings over two days, from the
moment it was found to the moment it shipped. At no handoff does the record show anyone
re-explaining it.

## Why this thread

I read the headings of every session log in the repository, then read in full the
sittings that name this one row. I picked it because the row is carried by name in the
saved next step of every sitting between its first sighting and its close. That is what
makes the handoff visible instead of assumed. Plenty of threads in those logs vanish for
a week and come back; this one can be watched being handed over, sitting by sitting.

The work itself: MusicTUI's cleanup could delete the playlist container the app had just
created to play music from. The row was called "Discover lifecycle serialisation".

Some background from two days earlier, which is a different bug in the same cleanup.
On 2026-08-31 a sitting fixed a leak where "`sweepDiscoverPlaylists` spared whatever
`name of current playlist` returned. That answers 'is there a context', never 'is audio
running'". So the cleanup was already known terrain when the new defect appeared.

## The eight sittings

**2026-09-02, closed 19:33. Found, and written down as a row.** The sitting was about
something else, a set of review rounds on album playback. A second AI, Codex, was paired
into it and raised this as its second Important finding. The sitting's saved next step
names the mechanism, not just the symptom:

> **Discover lifecycle serialisation** — Codex's second Important, needs a plan
> before code: the async launch sweep can delete a container a Discover play
> just created, because `keepName` is read once before capture.

**2026-09-02, 19:37 to 20:02.** A new sitting opened four minutes after the previous one
closed: "The sitting began with a `/kerd:switch in` at 19:37, four minutes after the
previous sitting's switch-out closed at 19:33." It did unrelated work, a push and
boundary problem. The row was carried forward untouched: "Discover lifecycle
serialisation, plan before code (unchanged)."

**2026-09-02, to 21:52.** A merge, then a piece of collaboration tooling handed to
another project. Row carried again: "Discover lifecycle serialisation (plan first);
normalizer whitespace (pair with Codex first). Both unchanged."

**2026-09-03, 08:10 to 08:24.** A release sitting, v3.11.0. The row appears in the
closure review as "· open — Discover lifecycle serialisation (untouched)" and again in
what's next, "(unchanged)". Nothing about it was worked on. It was not lost either.

**2026-09-03, 13:54 to 14:13.** The owner picked two other rows and sequenced this one
out loud: "Row 3, Discover lifecycle serialisation, goes separately through its own
plan-and-approval path." By the close it had moved up: "· open — Discover lifecycle
serialisation, now the top row", with the reason recorded as "It is the last of the four
rows that were in Now this morning."

**2026-09-03, 15:02 to 15:28. Picked up, and deliberately not built.** "[The owner] chose the
Discover lifecycle row and constrained the deliverable to a design." Three review rounds
with Codex, four drafts. The sitting ended with nothing built and a question saved for
the owner: "[The owner]: GO or not on
`docs/plans/2026-09-03-discover-lifecycle-design.md`", plus the one decision left inside
it.

**2026-09-03, 16:07 to 16:54. Built.** "[The owner] gave GO with two conditions and one
decision, and both conditions were checked in the fourth draft's text before any code".
Five commits, a Codex review of the implementation, then a live gate in both signed-in
and signed-out states. The gate passed, and it also produced something nobody could
explain. The log records it rather than rounding it off:

> **One observation I cannot explain, recorded in full rather than smoothed
> over (design doc §11, CONTEXT Open Questions, TODO §2).** In the second
> keyed run the container was present and current at 16:40:24 and GONE at
> 16:40:26, TUI still running, no key pressed since `p`, state `playing`,
> position continuous, context reverted to `Music`: a playlist deleted under
> playback.

The saved next step: "**The unexplained mid-playback deletion** deserves a sitting of its
own: measure with the sampler first, never touch the sweeps on a hunch."

**2026-09-03, 20:23 to 21:25. Closed.** The next sitting took that first. "[The owner] took
the unexplained deletion before the release, and set the shape of the measurement. His
instruction at 17:49: no v3.12.0 while the Discover lifecycle has one unexplained
instance of its headline failure; run a bounded, instrumented campaign". Thirteen pairs,
twenty-six plays, no recurrence. The release went out with the bar revised in the open
rather than quietly dropped, in the owner's words: "the bounded campaign reduced the
risk; it did not explain the event." The closing line of the sitting: "**Rung:** v3.12.0
released, bottled, tapped and live-poured. The Discover lifecycle arc that began at 15:02
today is closed end to end."

## What would have been lost

Four of those eight sittings did work with nothing to do with this row. A push failure, a
merge, a release, two fixes to display and text handling. The row survived them because
each close wrote it
down in a form that named the mechanism and the constraint on it, "plan before code", and
each open read that back. Written as "fix the Discover sweep" it would have had to be
re-derived by whoever picked it up.

The live gate observation is the sharper case. What carried across that boundary was two
timestamps two seconds apart, the player state, the position, the context it reverted to,
and the list of causes already ruled out. That detail is what the next sitting's campaign
was built on. When eight cycles on the settled album did not reproduce anything, four more
were run with the gap between quit and play fixed at 27.4 seconds, to match the 28 seconds
measured in the run that deleted. A summary saying "one unexplained deletion during the
gate" would not have supported that.

The record even shows the logs outlasting the reasoning of the people writing them:

> **The condition that separated the two runs was in the logs the whole
> time.** The deleting run's library count moved 14252 to 14263 in the line
> above the deletion; run F's did not. Nobody read those two numbers against
> each other for four hours, including me, until the plan gate forced the
> question of what actually differed.

## What the record does not show

It does not show anyone in the act of reading a log at pickup. What the logs establish is
that each close saved the row and each open carried it, unchanged, in the same words.
That the next sitting got it from the written record rather than from a person is the
obvious reading of that continuity, but it is a reading, not a logged event.

The mid-playback deletion was never explained. The 2026-09-03 close says the arc is
closed end to end, and it also says the deletion "stays open and is not under active
measurement". Both are true. The work closed the races in the app's own code; it did not
make the symptom impossible.

One more thing the record does show, and it cuts the other way. In this same window a
pickup found that three earlier switch-outs had reported success while the code had never
left the machine, because the check tested for uncommitted work and said nothing about
unpushed work. The defect was filed back to Kerd. The record kept the false headers in
place rather than editing them, and recorded the correction as its own entry.
