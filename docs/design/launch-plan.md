# Launch plan: from Anthony's own work to people who come back

**Status: accepted by Anthony, 2026-09-22 09:38, as drafted by Claude the same
morning.** Still open and his: the 2026-09-13 hold, who the invited few are, and where and
when the open launch is announced. Its sketchbook and route picture
(`docs/work/launch-plan/`) are working notes, kept on the Mac Studio, not in Git.

This replaces the 2026-09-02 plan of five outcomes and a ladder pilot, retired with the
ladder on 2026-09-19. That plan's dated render, `docs/plans/2026-09-02-launch-plan.html`,
stays as it was.

## What launched means

**Kerd is ready to launch when someone other than Anthony carries a real piece of work, in
their own repository, to its agreed result, unaided.** Anthony, 2026-09-02; reworded
without the ladder and confirmed 2026-09-22.

"Agreed result" means the goals that person set with Conductor in rehearsal, not a rung.
"Unaided" means Anthony doesn't step in during the sitting. What they tell him afterwards
is evidence, not help.

## The route

1. **Prove it at home.** Anthony takes one real piece of work on a project that isn't Kerd
   through Kerd, over at least two sittings: Switch In, rehearsal with Conductor, a concert
   if the work calls for one, Switch Out. Kept light by Anthony's choice (2026-09-22): Kerd's own
   sittings count as proof of use alongside it. The project is 3of3, proving its iCloud
   sync. A general proof of use, not
   meeting the 2026-09-13 hold. That hold ("prove Kerd works as it should before any
   consumer pickup", `docs/decisions.md` #28) clears only when rows 1 to 5 of that day's
   shared verification list carry evidence of their fixes working, and this run is not
   mapped to those rows. Rows 1, 2 and 4 were observed on 2026-09-13, closed 2026-09-14
   (`docs/backlog-archive.md`). Rows 3 and 5 are not recorded as closed: each has partial
   observations from 2026-09-13 (`kivna/sessions/2026-09-13.md`), and their remaining gaps
   were not re-checked for this draft. Whether the hold is lifted is Anthony's call.
2. **Invite a few.** Three to five people Anthony picks, from the audience agreed on
   2026-09-18: developers, product people, anyone using AI to make something that matters.
   Proposed: at least one should not be a developer, because the front page promises them too.
3. **Install.** Claude Code, then the two commands in the README's Install section. Keyless
   install was proven on 2026-09-20. They start from `docs/guide/getting-started.md`.
4. **First sitting.** Their own real work, not a demo task. They start with Switch In and
   work through Conductor's rehearsal. They end with Switch Out. Anthony isn't in the room.
5. **Come back.** A second sitting, on a later day, picks up where they left off.
6. **Open launch.** Announce publicly only once the invited round shows Kerd working.
   Where and when is Anthony's call.

## How anyone will know it worked

Each invited person is one observation. For each one, record:

- **Their own repository:** was the work in a repository they own or work in, not one
  set up for them?
- **Unaided:** did Anthony stay out of the sitting? Anything he did is written down.
- **Finished:** did the work reach the goals they set in rehearsal? Yes, partly or no, with
  the goals in their words.
- **Came back:** did they start a second sitting without being asked?
- **What broke:** everything that stopped or confused them, written down as they report it.
  Nothing gets patched while their round is running, so the round measures Kerd as released.

The first person's round is an instrument, not a verdict. It's expected to find breaks.
Fixes are released as ordinary Kerd versions between people, never during a round.

**Ready for the open launch** when at least one invited person meets the definition
above, and every break the invited round found is either fixed in a release or written
where a new user will meet it. That second condition is the 2026-09-02 plan's "known limits
documented where a user meets them", kept.

## What this rests on, and what it doesn't

- **Exists today:** install from the marketplace; the site (https://kerd-six.vercel.app/)
  and README, checked against what Kerd does (2026-09-21); Switch In and Out, and
  Conductor's rehearsal, all seen in Anthony's own sittings.
- **Never exercised in a real session:** the composer, managed Conductor and a roll. A
  first user's work may not need them. If it does, that sitting is their first observation.
- **Known to strain:** a concert can't roll mid-build without publishing half-built work
  (open in `TODO.md`). An invited user with a large build could hit it.
- **Codex:** the plan is Claude Code first, matching the front page. The four-skill Codex
  core has been built but never used in a Codex conversation, so it isn't part of this
  launch.

## Anthony's rulings

- ~~This plan~~: accepted 2026-09-22.
- Whether the 2026-09-13 hold is lifted, and on what evidence (rows 3 and 5 still open).
- Who the invited few are.
- Where and when the open launch is announced.

**Declared limit:** this file is kept by hand. Nothing derives its status.
