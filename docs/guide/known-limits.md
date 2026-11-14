# Known limits

What Kerd has not yet been seen doing, or does with a catch, written for someone
about to use it on their own work. Each line says what you might meet and what to
do about it. When a limit is lifted, its line goes.

## Where it runs

- **macOS or Linux, with Python 3.10 or newer and git.** Kerd's helper scripts
  need them, and the packaged guide names only those two systems. Windows is not
  covered, so nothing here says it works.
- **Your work has to be in a git repository.** Saving and picking up are git
  operations. In a folder without git the save helper reports "not a git
  repository" and stops, and `/kerd:tend` stops and tells you to run `git init`.
  [Getting started](getting-started.md#if-your-work-isnt-in-git-yet) shows the
  steps. A remote such as GitHub is optional.
- **Claude Code is the main path; Codex is early.** The Codex package has four
  skills, not eight: Conductor, Switch, Visuals and Agent. So far it has not been
  seen in use by anyone but its author. Codex has no slash commands for Kerd; you
  ask in words.

## What has not been seen in real use yet

These are built, but nobody has used them on real work yet. If your work needs
one, you may be the first, and what happens is worth reporting.

- **The composer**, Conductor's helper for drafting a hard passage of the plan.
- **Managed Conductor**, which runs a long build without routine questions. It
  runs one player at a time.
- **Rolling a long Conductor build into a fresh window** (`/kerd:switch roll`).
  The session has to run inside tmux. Outside tmux, Kerd saves and shows you one
  line to run.
- **Picking up on a second machine** when your project keeps its working notes in
  a separate private notes repository.

## Things that may catch you

- **Claude Code may ask before Kerd runs its own helper scripts.** Whether it does
  depends on your permission settings; it treats them like any other command. See
  [Permission prompts](getting-started.md#permission-prompts).
- **Diagrams need a drawing tool.** Conductor shows plans and before-and-after
  changes as rendered diagrams, drawn with diagram-design or Archify. If neither
  is installed, Kerd offers to set one up and asks first unless you have already
  approved the installation. If neither can run, it says the diagram is not
  drawn rather than sketching one by hand.
- **Reviews go to the other provider by default.** When Claude builds, a review
  goes by default to a fresh Codex reviewer. If Codex cannot start, the review
  goes to a different Claude model and Kerd says so. If you name a reviewer, the
  request goes to that partner and Kerd does not silently substitute another.
- **Kerd's own words.** Conductor talks about rehearsal (working out what you
  want), the concert (building it), the sketchbook (its notes on your work) and
  players (the helpers it starts). [Conductor](conductor.md) explains each.
