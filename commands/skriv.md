---
description: "Enforce human writing voice — audit files, fix prose, or toggle session mode"
argument-hint: "<file>|fix <file>|on|off"
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

The user's argument is: $ARGUMENTS

If no argument is given, tell the user the available modes:
- `/skriv <file>` — audit a file against the rules
- `/skriv fix <file>` — rewrite a file applying the rules
- `/skriv on` / `/skriv off` — toggle session mode for all prose output

Invoke the kerd:skriv skill and follow it exactly as presented to you.
