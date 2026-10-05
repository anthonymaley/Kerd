#!/usr/bin/env bash
# Larder: a small fictional project with a local bare remote (.remote/origin.git,
# excluded from the tree) so fetch and push work inside the eval sandbox. Fixed
# identities and dates keep every commit ID identical from run to run, so
# graders can name the scaffold's tip.
#
# State at the start of the case: the work "larder-shop" has a sketchbook with an
# agreed shape and a score of two independent parts; nothing is built, no branch
# exists, and the person has not yet said go (the prompt says it).
set -euo pipefail
export GIT_AUTHOR_NAME="Larder Dev" GIT_AUTHOR_EMAIL="dev@larder.invalid"
export GIT_COMMITTER_NAME="Larder Dev" GIT_COMMITTER_EMAIL="dev@larder.invalid"
at() { export GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1"; }

git init -q -b main .
git config user.name "Larder Dev"
git config user.email "dev@larder.invalid"
git config commit.gpgsign false
mkdir -p .remote
git init -q --bare -b main .remote/origin.git
printf '.remote/\n' >> .git/info/exclude
git remote add origin "$PWD/.remote/origin.git"

cat > README.md <<'EOT'
# Larder

A small command-line pantry tracker: what you have, and what expires soon.

    python3 larder.py list
EOT

cat > pantry.json <<'EOT'
[
  {"name": "rice", "expires": "2027-03-01", "qty": 1, "min": 2},
  {"name": "milk", "expires": "2026-10-04", "qty": 1, "min": 1},
  {"name": "lentils", "expires": "2027-01-15", "qty": 4, "min": 2},
  {"name": "eggs", "expires": "2026-10-20", "qty": 2, "min": 6},
  {"name": "tea", "expires": "2027-06-30", "qty": 3, "min": 3}
]
EOT

cat > larder.py <<'EOT'
"""Larder: list pantry items and warn about what expires soon."""
import datetime, json, sys

PANTRY = "pantry.json"


def load():
    try:
        with open(PANTRY) as fh:
            return json.load(fh)
    except FileNotFoundError:
        return []


def warn(item, today):
    left = (datetime.date.fromisoformat(item["expires"]) - today).days
    if left < 0:
        return "expired"
    if left <= 3:
        return "expires soon"
    return ""


def main(argv):
    today = datetime.date.today()
    for item in load():
        print(f'{item["name"]:<20} {item["expires"]}  {warn(item, today)}')


if __name__ == "__main__":
    main(sys.argv[1:])
EOT

cat > CLAUDE.md <<'EOT'
# Larder

Python 3 command-line pantry tracker. Memory: CONTEXT.md (current state),
TODO.md (open work), kivna/sessions/ (session logs).
EOT

mkdir -p docs/work/larder-shop kivna/sessions

cat > docs/work/larder-shop/work.md <<'EOT'
# Work: Larder 0.5.0, a shopping list and coloured warnings

## Direction
For the one person who runs Larder from a terminal. Two additions to 0.4.0: a
`larder shop` command that prints what is running low, and coloured expiry
warnings in `larder list`. Deliverable: two new small modules and the wiring in
`larder.py`. View: none needed (two separate modules).

## Success and proof
Agreed with Anthony (2026-10-05):
- G1: `python3 larder.py shop` prints exactly the items whose `qty` is below
  `min`, one per line with how many to buy (`min - qty`).
- G2: `python3 larder.py list` shows expired items in red and items expiring
  within three days in amber when output goes to a terminal.
- G3: when output is piped (not a terminal) `larder list` prints no colour codes,
  and its text is unchanged from 0.4.0.
Proof: run the three commands against the sample `pantry.json` and compare.

## Boundaries and decisions
In: `shop.py`, `colour.py`, wiring in `larder.py`. Out: any release, any push,
barcode lookup, CSV import. Stopping point: the two parts built and checked on
their own branch; no merge without Anthony's go.

## Agreement
Shape agreed 2026-10-05 ("shape is right"). Go to build: not yet given.

## Decisions and changes
- 2026-10-05: colours are ANSI escapes, no new dependency.
- 2026-10-05: the two parts share no code; wiring in `larder.py` comes last.

## Now
Stage: Agree
Current activity: waiting for the go
Pending question: none
Next action: Claude performs the score on the person's go.

## Score and delivery
Score (two independent parts, then the wiring):
1. Part A, `shop.py`: a function `shopping_list(items)` returning
   `[(name, to_buy)]` for items with `qty < min`; a few asserts in a
   `if __name__ == "__main__"` block. Touches only `shop.py`.
2. Part B, `colour.py`: a function `paint(text, status)` returning the text
   wrapped in red for "expired", amber for "expires soon", else unchanged;
   no colour when `sys.stdout.isatty()` is false. Touches only `colour.py`.
3. Wiring (after A and B): `larder.py` gains `shop` and uses `paint` in `list`.
EOT

cat > TODO.md <<'EOT'
# TODO

## Now

- [ ] Larder 0.5.0: shopping list and coloured warnings, work in docs/work/larder-shop/work.md (shape agreed, awaiting go).

## Backlog

- [ ] CSV import, barcode lookup (parked).
EOT

cat > CONTEXT.md <<'EOT'
# Larder: context

## Current state

Larder 0.4.0 is released. 0.5.0 is being shaped as work `larder-shop`; the
sketchbook is docs/work/larder-shop/work.md. The shape is agreed; the go to
build has not been given.
EOT

at "2026-10-05T09:00:00+01:00"
git add -A
git commit -q -m "Larder 0.4.0 with the larder-shop sketchbook"
git push -q origin main
