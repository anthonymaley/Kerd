# Roll status

Adopted into the candidate at [roll_status.py](../../../skills/switch/scripts/roll_status.py)
with [tests](../../../skills/switch/scripts/tests/test_roll_status.py). The original
trial kept both beside this agreement. In the pack, invoke the linked script and
run `python3 -m unittest discover -s docs/work/model-ready-work/skills/switch/scripts/tests -p test_roll_status.py` from the Kerd root.

`roll_status.py` prints a compact, human-readable view of a managed Roll's
private status record.

```sh
python3 roll_status.py --project REPO
```

`REPO` may be the worktree root or any directory inside it. The command asks
Git for the actual worktree root and private Git directory, so it works with a
normal clone (`.git` is a directory) and a linked worktree (`.git` is a file).
It then reads `<resolved-git-dir>/roll/run.json`.

The panel reports the current state, the record's next action, and available
history summary: completed worker count, last returned status, and whether a
context-triggered Roll was observed. `review` specifically means that the work
is awaiting independent assessment; it does not mean accepted. Missing fields
in older history, unavailable context readings, and unfamiliar historical
status strings are handled without inventing facts; an unfamiliar last status
is shown as unknown.

The command is strictly read-only. It does not fetch, checkout, merge, stage,
run project scripts, or create a fallback status record. It never derives
completion or quality from files or command success, and it does not display
native session/request identifiers, raw history, or private error fields.

Exit code `0` means only that a valid, known status was read and displayed. It
does **not** mean the Roll's work passed. A missing, malformed, unreadable, or
unknown record produces a concise message and a nonzero exit code.

Run the isolated standard-library test suite with:

```sh
python3 -m unittest -v test_roll_status.py
```
