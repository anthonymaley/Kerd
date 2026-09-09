# Roll status

`roll_status.py` reads the private ledger for a managed Roll and presents its
current workflow state in a small text panel.

Run it with Python 3 and a path to the project (or any directory inside its Git
worktree):

```sh
python3 roll_status.py --project REPO
```

The command asks Git for both the actual worktree root and that worktree's
private Git directory. It therefore supports an ordinary clone whose `.git` is
a directory and a linked worktree whose `.git` is a file. It reads
`roll/run.json` below the private Git directory. It does not fetch, checkout,
merge, stage, run project scripts, create a missing record, or otherwise write
project data.

For a valid record with a known state, exit status 0 means only that the status
was read and displayed. It does **not** mean that the work passed, and `review`
means awaiting independent assessment rather than accepted. The panel reports
the saved next action and, when available, the completed-worker count, last
returned status, and whether a context-triggered Roll was observed. Native
session/request identifiers, raw history, and private error fields are never
shown.

Missing, malformed, or type-invalid records and unknown current states produce
a concise message on standard error and a nonzero exit status. Older records
that omit optional history details remain readable; unavailable facts are
labeled `Unknown`. Saved display text is reduced to one line and terminal
control sequences are suppressed.

Run the isolated standard-library test suite with:

```sh
python3 -m unittest -v test_roll_status.py
```

The tests create only temporary Git repositories and fixtures. The command uses
the Python standard library and the local `git` executable; it makes no network
requests.
