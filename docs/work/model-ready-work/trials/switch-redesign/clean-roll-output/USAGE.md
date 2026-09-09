# Roll status

`roll_status.py` prints a small, human-readable view of a managed Roll without
exposing the helper's native session or request identifiers.

```sh
python3 roll_status.py --project REPO
```

`REPO` may be a repository root or a path inside one. The command asks Git for
both the actual work-tree root and the absolute private Git directory, so it
works with an ordinary clone (`.git` is a directory) and a linked worktree
(`.git` is a file). It then reads `<resolved-git-dir>/roll/run.json`.

The panel reports the current state, the record's exact next action, completed
worker count, last returned status, and whether a context-triggered Roll was
observed. A `review` state only means that independent assessment is next; it
does not mean the work was accepted. Likewise, exit status 0 means only that a
known, valid status was read and displayed. It is not evidence that the work
passed review or that a previous command succeeded.

Unknown current states and missing, malformed, unreadable, or wrongly typed
records produce a concise error and a nonzero exit status. Older history that
omits optional observations is labeled unknown. Unknown historical status names
are also labeled unknown rather than treated as proof or echoed.

The command is read-only. It runs only Git's `rev-parse` query and reads the
resolved ledger. It does not fetch, checkout, merge, stage, run repository
scripts, create fallback records, or infer completion from files or command
success. ANSI and control characters are removed from displayed saved text, and
private history content is not printed.

Run the isolated standard-library test suite with:

```sh
python3 -m unittest -v test_roll_status.py
```

The tests create temporary Git repositories and linked worktrees; they do not
use a live project's Roll ledger.
