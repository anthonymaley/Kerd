# If you were invited to try Kerd

You have been asked to try Kerd on a piece of your own work and tell us how it
went. This page says what to expect. It takes about five minutes to read.

Kerd is a plugin for Claude Code. It helps you and the AI agree what "done"
means for a piece of work, keeps your place so you can stop and pick the work up
again later, and carries the work out. If you have not installed it yet, start
with [Getting started](getting-started.md); it goes from nothing to a first saved
sitting.

## What to expect

- **It is early, and you may hit rough edges.** Part of the point of asking you is
  to find them. If something stops or confuses you, that is useful, not your
  mistake.
- **Nobody will sit beside you.** Try to work through it on your own, the way a
  stranger would. If you get stuck, note where you got stuck before asking for
  help.
- **Nothing is fixed while you are using it.** You are seeing Kerd as released.
  Fixes come out later as ordinary new versions.

## Use your own real work

Pick something you actually want to get done, in a folder you own or work in. A
practice task tells us much less. The work does not have to be code. It does have
to be in a folder that Git is tracking; the getting-started page shows the
[steps to set that up](getting-started.md#if-your-work-isnt-in-git-yet) if yours is not.

## How to begin

In your project folder, in Claude Code, type:

```
/kerd:switch in
```

The first time, Kerd has nothing saved yet and asks what you want to work on.
Answer in your own words. When you are done for the day, type `/kerd:switch out`,
so that Kerd saves where you got to. Come back on another day and type
`/kerd:switch in` again.

## What we will ask you afterwards

Five plain questions, nothing more:

1. **Was it your own work,** in a folder you own or work in, not one set up for you?
2. **Did you manage on your own,** without anyone helping you through it?
3. **Did you get the work done?** Yes, partly or no, measured against what you said
   you wanted at the start.
4. **Did you come back for a second sitting** without being asked?
5. **What broke or confused you?** Anything that stopped you, anything you had to
   guess, anything that read oddly. Your own words are best.

You do not need to keep notes for these. A few notes on where you got stuck do help.

## If something breaks

Do either of these, whichever is easier:

- **Tell Anthony** directly, in whatever way you usually reach him. A screenshot or a
  pasted copy of the screen is enough.
- **Or, if you have a GitHub account, open an issue** using the "Something broke or confused me" form:
  [open a new issue](https://github.com/anthonymaley/Kerd/issues/new?template=something-broke.md).
  It asks what you were doing, what you expected, what happened, your Kerd
  version, your Claude Code version and the text of the screen. The Kerd version is
  in the heading of the arrival screen that `/kerd:switch in` shows (for example
  "Kerd 0.x.y"). For Claude Code, run `claude --version` in a terminal.

Please do not wait until you have a tidy description. "It said something I did not
understand, here is the screen" is a good report.
