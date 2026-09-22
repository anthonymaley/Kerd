# Work: every claim on Kerd's front page is either proved or named as wrong

## Direction

For the newcomer who arrives at Kerd's front page and does what it tells them.
On 2026-09-20 the two install commands printed on that page were fixed: until
then, anyone without a GitHub key ran the second one and got nothing. Three
releases shipped over that defect and nothing in the repo could have caught it,
because every check in the repo inspects what Kerd says about itself. Only a
stranger running the command found it.

Two claims on that same page have still never been run:

- **The site.** `site/index.html`, `capabilities.html`, `examples.html` and
  `docs.html` have never been opened in a real browser. Nor have the seven
  pictures the README embeds. The README says the site is part of what Kerd
  made; nobody has looked at it rendered.
- **The trial route.** `claude --plugin-dir /absolute/path/to/kerd` has never
  been run. Its own sentence is already known to be partly false, below.

Deliverable: a defect list with evidence, and — where a claim on the page is
wrong — the corrected page, reviewed and released under the 2026-09-20 ruling.

View: [scope.html](scope.html) — proposed, not yet agreed.

## Worth it and design

The front page is the only part of Kerd a stranger reads before deciding. A
wrong sentence there costs more than a wrong sentence anywhere else in the repo,
and the repo's own checks structurally cannot find one. The last sitting proved
the two halves of that: a real run caught a wrong *mechanism*, and an independent
reader caught a wrong *claim*. Neither substitutes for the other, so this work
uses both — real runs for the site and the trial route, a cold reader over the
prose.

Scope is README lines 1–224, the newcomer-facing page, plus the four site pages.
The release history below line 225 is out.

## Risks to keep in view

- **Running the trial route touches a config directory.** `claude --plugin-dir`
  writes to whatever `~/.claude.json` resolves to. Countermeasure: a throwaway
  profile via `CLAUDE_CONFIG_DIR`, the route established during the install test
  on 2026-09-20; Anthony's own profile is not touched without his word. Named
  2026-09-20, still open — the run has not been authorized yet.
- **A browser check can be faked by reading the HTML.** Reasoning about source
  is not rendering, and would produce exactly the kind of self-inspecting result
  that missed the install defect. Countermeasure: the browser job must name the
  tool that rendered it and return measured pixel sizes and screenshots; a
  source-only answer is rejected. Named 2026-09-20.
- **The site may not be published anywhere.** There is no Pages workflow in
  `.github/workflows/` — only `gate.yml` — and the README links no live URL.
  If the site only exists as files in the repo, "the site you are reading" is a
  claim about something a newcomer cannot reach. Not yet established; the claim
  inventory will settle it. Named 2026-09-20.

## Success and proof

Proposed, not yet agreed with Anthony:

- Every falsifiable claim on README lines 1–224 is classified, with the concrete
  run or artifact that settles it named. A claim that cannot be settled on this
  machine is recorded as such rather than guessed.
- The four site pages have been opened in a real browser at desktop and phone
  width, with screenshots, and every defect carries a measurement.
- The trial route has actually been run, and the sentence the README prints
  about it either matches what was observed or has been corrected.
- Anything corrected is reviewed by Codex before push, per its recorded
  before-push cadence.

Good enough: a newcomer following the front page hits nothing that the page got
wrong. Not in scope: making the site better, only making it true.

## Boundaries and decisions

**Must:** read-only until Anthony gives the go for the trial run; throwaway
profile only; Codex reviews any fix before push; Anthony approves the push.
**Out:** the release history; improving the site's design; the launch plan,
which is Anthony's separate ruling.
**Open:** whether a correction to the front page ships as its own release under
the 2026-09-20 ruling (a defect that changes what installs gets its own version
and a release note) — that ruling is about *installs*, and a wrong sentence
about the trial route may or may not fall inside it.

Time/resources: none stated.
Stopping point: the defect list delivered and any agreed correction pushed.

## Agreement

Anthony answered a plain "y" to Switch In's recommendation on 2026-09-20 14:35,
which selected this work to shape. On 2026-09-20 19:43 he answered "yes" to
running the two unproved commands in a throwaway profile; those runs are done and
the profile is gone. No correction, commit, push or release has been authorized.

## Decisions and changes

- 2026-09-20: scope set at README lines 1–224 plus the four site pages; release
  history excluded. Conductor's call, from the terrain.

## Findings

**F1 · The front page still points at the broken install address.** `## Rolling back`
tells a reader to pin a consumer repo's marketplace `source.url` at `716a099`
(README.md:207). `git show 716a099:.claude-plugin/marketplace.json` declares the plugin
source as `git@github.com:anthonymaley/Kerd.git` — the exact SSH address 0.142.1 was
released to remove. **Verified:** the manifest content, read directly. **Inferred, not
re-run:** that following the instruction reproduces the same keyless failure; that
follows from the mechanism established by a real run on 2026-09-20 (install clones the
declared address literally), not from a run of this path. Three sections below the fix,
untouched by it.

**F2 · "All four are ordinary Markdown" is false in the repo that says it.**
README.md:157-158. `kivna/vault.json` is tracked and is JSON; Kerd writes rendered HTML
and SVG into `docs/` (`docs/work/first-install/who-can-install-kerd.html`,
`docs/pictures/*.svg`, all tracked); and `.gitignore` shows it writing `.agents/`,
`kivna/.pair`, `kivna/.active-modes`, `kivna/input/`, `kivna/output/`. Kivna also writes
outside the project, into the vault named in `kivna/vault.json`. The section whose whole
job is disclosure is the one that understates.

**F3 · The page's own guarantee is falsified by the page.** "nothing below claims more
than the repo can show" (README.md:68-69), with F1 and F2 above it.

**F4 · The site and the README disagree in six places.** The site states flatly "A second
AI reads the work independently" where the README says "can"; `site/capabilities.html`
describes Agent using Conductor's concert and Visuals using Conductor's sketchbook; the
site names a Codex install route the README front page never mentions, having already
told a Codex reader that Kerd runs there.

**F5 · The reader's second-ranked finding was wrong, and was rejected.** It reported that
the install fix "was verified against a local marketplace" with no post-push run
recorded. That is the mid-work risk list in `docs/work/first-install/work.md`; the same
file's closing read-back records it closed by the live keyless install (F6 there), as do
`CONTEXT.md` and `kivna/sessions/2026-09-20.md`. It read the risk and stopped before the
close. Checked rather than accepted, in line with how the last sitting handled returns.

**Scale:** 55 falsifiable claims on README lines 1-224. Four known wrong (F1, F2, F3 and
the `--plugin-dir` footprint clause already on record), around 25 never run, the rest
proved or not falsifiable as written.

**F6 · The site holds up; its drawings do not.** Opened in a real browser (Chromium via
Playwright) at 1440x900 and 390x844, served over HTTP from the repo root. The four pages
are sound: no horizontal overflow at either width, no non-200 responses, no console
errors, and every link resolves to a file that exists. The pictures fail on a phone. At
390px every text element in every embedded drawing renders under 12px. Worst:
`how-kerd-works.svg`, whose `.sub`/`.span` class is 32px inside a 1600-wide viewBox and
renders in a 348px box — **6.96px**. I verified those inputs directly rather than take
the arithmetic on trust. The standing backlog row said "near 8px"; it was understating.
Borderline at desktop too: `the-concert.svg`'s 28px `.tiny` class lands at 12.04px.
Screenshots in `shots/`.

**F7 · A second failure mode, opened directly.** As bare files rather than embedded, the
drawings do not scale at all — fixed 1280 or 1600 widths — so at 390px they overflow by
890 to 1210px and most of the canvas is off-screen. Which of the two modes GitHub's own
README rendering produces is not established here; that remains Anthony's look at the
repo page.

**Correction to this work's own brief.** It said "seven README pictures". The README
embeds four; the other eight under `docs/pictures/` appear in the guides and on
`site/capabilities.html`. Reported by the browser job rather than guessed at.

**F8 · The rollback instruction is dead for a keyless reader — proved, not inferred.**
Run in an isolated profile on 2026-09-20 evening. A marketplace added from a checkout at
`716a099` is accepted; `claude plugin install kerd@kerd-marketplace` then fails with
`git@github.com: Permission denied (publickey).` and installs nothing. **No environment
variable rescues it.** `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` makes no difference, because
that manifest declares an explicit `url` source rather than the `github` shorthand —
there is no shorthand left to re-resolve. This is *stronger* than the correction proposed
before the run: the wording drafted then would have told the reader to set that variable,
and it would not have worked. The run corrected the fix, again.

**F9 · The trial route does write to the reader's config, and does so even when the
session does nothing.** Measured in the isolated profile, before and after. `claude
--plugin-dir <copy> plugin list` wrote nothing at all — a subcommand is not a session. A
session through the same route, one that got as far as the login prompt and did no work,
added `pluginUsage: {"kerd@inline": {"usageCount": 1, ...}}`. So the README sentence is
true as written and misleading as read: nothing was *installed* and nothing *disabled*,
but something was written, by a session that accomplished nothing.

**F10 · "Takes precedence" is not what the CLI reports.** With 0.142.1 installed and a
local copy marked `9.9.9` passed to `--plugin-dir`, `plugin list` shows both:
`kerd@kerd-marketplace 0.142.1 · enabled` and `kerd@inline 9.9.9 · loaded`, under a
separate "Session-only plugins" heading. They coexist; the installed one is not
displaced. Which copy's skill text wins inside a running session is **unproved**.

**Limit of this route, named.** A throwaway profile carries no credentials, so no model
session can run inside it — the session above stopped at `Not logged in`. Nothing about
in-session behaviour can be settled this way. Logging a throwaway profile in was outside
what was authorized and was not attempted.

**Isolation held.** Everything the runs created landed inside the temp directory,
including all clone scratch. The real plugin cache gained no entries; only
`known_marketplaces.json` and two directory mtimes moved, which is the ordinary
marketplace auto-update the install test already identified as a false-alarm generator.
The real profile's own `.claude.json` was not read, only its metadata.

## Now

Stage: Complete for the agreed corrections, 2026-09-21.
Current activity: none. Committed as `1f8e8f5` and pushed to `main` on Anthony's
"yes" (2026-09-21 10:27); remote verified to contain it; CI `entry-gate` green.
No version bump, on his decision.
Analysis so far: the front page carries at least four wrong claims, not one. The
worst, F1, is the same defect 0.142.1 fixed, still live three sections lower.
Around 25 claims have never been run. No Pages workflow exists, so where the site
is published is an open question rather than a known fact.
Open issues: whether the site is reachable by a newcomer at all; whether these
corrections ship as 0.142.2 under the 2026-09-20 ruling; what the rollback
section should say instead, which needs a run to state truthfully rather than
plausibly.
Pending question: may the two unproved commands — the trial route, and an
install from a marketplace pinned at `716a099` — be run in a throwaway profile?
Decision context: it is the only half of this work that touches machine state,
and it is the half most likely to find a wrong sentence, since one clause of it
is already known wrong.
Next action: none inside this work. Two follow-ons remain open and unstarted:
the pictures' legibility on a phone, and the six site/README disagreements.

## Score and delivery

Score: none yet; the work is in rehearsal.
Assignment: both steps written by Conductor, performed by native Claude players.
Fit: claim inventory — a cold reader deciding what is falsifiable; Opus 5 at
high, because the last defect was a wrong sentence every mechanical check
passed. Site in a browser — a browser driven and text measured against a stated
threshold; Sonnet 5 at high, the step being fully specified but browser driving
needing adaptation.
Settings: claim inventory requested Opus 5 / high, observed `claude-opus-5` at
high across 54 records, no gaps — requested and observed agree. Site check requested
Sonnet 5 / high, observed `claude-sonnet-5` at high across 202 records, no gaps —
requested and observed agree.
Review plan: Codex (`codex-tui`), recorded cadence checkpoints and before-push.
The before-push gate fired on 2026-09-20 evening: the three-file change set was
sent with the brief at `review-brief.md`, status submitted-unconfirmed. **Three rounds, each one finding a real overstatement in the same sentence.**
Round 1: "every commit before 0.142.1 carries an SSH address" — false; the
manifest was born HTTPS at `34d212d` and the SSH address entered at `bc0d78e`.
Verified against the url's full history before acting. Two non-blocking
findings the same round: the two rollback routes were presented as usable
without being run, and "Kerd adds those to your `.gitignore`" was unsupported —
tend's Category 7 checks only `kivna/input/`, `kivna/output/` and `.DS_Store`,
and no skill source mentions `.agents/`. Both confirmed before changing.
Round 2: the narrowed sentence introduced a *new* overstatement — "commits
before `bc0d78e` are unaffected", false for the commits with no manifest at all.
Exactly one commit predates it, so the sentence was deleted rather than given
two more clauses.
Round 3: **clear to push.**
Codex ran no installs and no session tests, and said so each time.
Change set: `README.md`, `site/index.html`, `docs/guide/getting-started.md` —
29 insertions, 8 deletions in the README plus the two repeated copies. Release
check clean; 757 tests pass.
Evidence: both jobs returned and checked. F1 verified against the repo; F5
rejected as wrong; F6's headline measurement re-derived from the SVG's own
viewBox and font classes rather than accepted.

## Corrections written and reviewed (not pushed)

1. **Rolling back** — the pin row is gone, replaced by a warning that every commit
   before 0.142.1 carries the SSH manifest and cannot be installed without a GitHub
   key, with the two routes that do work.
2. **The trial route** — says what it actually writes, drops "takes precedence" for
   what `plugin list` really shows, and marks in-session precedence as untested.
   Corrected in all three places it appeared: README, `site/index.html`,
   `docs/guide/getting-started.md`. Correcting one and leaving two would have been
   the project's own "two homes for one fact" failure.
3. **What it writes** — keeps the four-file table and adds what else Kerd writes:
   committed HTML and SVG, `kivna/vault.json`, the gitignored state.
4. **The meta-guarantee** — replaced with a statement that the page marks proved and
   unproved claims for what they are.

Deliberately out of this set: the pictures' legibility, and the six site/README
disagreements the reading pass found.

## Goal check, 2026-09-21

- **Every falsifiable claim on README lines 1–224 classified, with what settles
  it.** Met: 55 claims.
- **The site opened in a real browser at both widths, defects measured.** Met:
  Chromium via Playwright, 1440 and 390, eight screenshots, every defect with a
  number.
- **The trial route actually run, and its sentence matching what was observed.**
  Met with a stated limit: run, and corrected in all three places it appeared.
  In-session precedence stays unproved — a throwaway profile cannot log in — and
  the page now says so.
- **Anything corrected reviewed by Codex before push.** Met: three rounds.
- **Good enough — a newcomer following the front page hits nothing the page got
  wrong.** Met for what the page *says*. The site and README still disagree in
  six places, deliberately left out of this change set.
- **The phone measurement, re-read against the real audience (2026-09-21).**
  Anthony: Kerd's readers are on desktops and laptops, not phones. At 1440px
  every picture clears 12px, so the 6.96px phone finding does not describe the
  people who use this. One remnant: `the-concert.svg`'s smallest labels land at
  12.04px at 1440 — on the line, and a narrower laptop window was not measured.

## Risks, read back at the close

- Running the trial route touches a config directory — **closed.** Isolation held:
  all scratch landed in the throwaway, the real plugin cache gained nothing, and
  the real `.claude.json` was read by metadata only.
- A browser check faked by reading HTML — **closed.** The job named its tool and
  returned computed pixel sizes and screenshots; its headline number was re-derived
  from the SVG source rather than accepted.
- **The site may not be published anywhere — still open.** No Pages workflow
  exists and the README links no live URL. Never settled by this work.

## Results and evidence

Checked: F1's manifest content, read directly at `716a099`. F2's tracked JSON, HTML
and SVG, and the gitignored state paths. F5's closure, in the install test's own
closing risk read-back.
Unproved: every claim that needs a command run — the trial route, the pinned
rollback, uninstall, the cross-machine round trip, and the cost claims. The site's rendering is now
measured, and the view at `scope.html` was itself checked at 390px and 1440px —
no text under 12px, no overflow.

## Follow-on: publishing the site on Vercel (2026-09-21)

**Why.** Checked before recommending the six site/README disagreements: the site is not
published anywhere. `gh api repos/anthonymaley/Kerd` reports `has_pages: false` and no
homepage, so the README's "the README, guides and site you are reading" is false, and the
six disagreements sit on a page nobody can reach. Publishing comes first. Anthony chose
Vercel.

**Written:** `vercel.json` at the repo root, three redirects — `/`, `/site` and `/site/` —
all to `/site/index.html` with `permanent: false`. The root is deployed rather than
`site/` because every page loads its pictures from `../docs/pictures/`. Redirecting to
the file itself removes any dependence on Vercel's trailing-slash default, which per its
docs serves `/site` and `/site/` alike without redirecting and would otherwise break every
relative link for a visitor on `/site`. Syntax checked against
vercel.com/docs/project-configuration/vercel-json (last updated 2026-08-14). Every
relative link on all four pages resolves when served from `/site/`.

**Reviewed:** Codex, before-push, clear on the first read — no loop, valid config.

**Not yet proved:** that Vercel applies the redirects and serves the root as static files.
Its CLI is not installed and installing it was not agreed; the first real deploy is the
check. Then the README line gets the real URL, and the six disagreements come next.

**Ownership:** the repo file is Claude's; importing the repo in Vercel's dashboard is
Anthony's, on his own account.

**Live, and proved (2026-09-21 11:15).** Anthony imported the repo; the deployment is
at https://kerd-six.vercel.app/. Checked from this machine: `/`, `/site` and `/site/`
each 307 to `/site/index.html`, which returns 200; in Chromium at 1440x900 all ten
pictures load (`naturalWidth > 0`), the stylesheet applies, nothing overflows, and every
relative nav link returns 200. The redirect design worked as reasoned. `vercel.json`
pushed as `77d084e`, CI green.

**README line linked and pushed** (`8ee8464`, CI green, on Anthony's "yes"). `README.md:11` now reads "README, guides and
[live site](https://kerd-six.vercel.app/) are their first real use." Codex cleared the
first version and suggested dropping "you are reading", since a reader on GitHub is not
on the site; taken, re-read, clear.

## Follow-on: the six site/README contradictions (2026-09-21 evening)

**Chosen** at Switch In ("y" to the recommendation), 19:11. That selects the work; it
approves no edit or push. Owner Claude, inline; Codex `codex-tui` reviews before push; the
push is Anthony's. Prose only, so no version bump (2026-09-21 ruling).

**Re-checked live first.** `site/index.html` and `site/capabilities.html` fetched from
https://kerd-six.vercel.app/ are byte-identical to the repo, so the repo copy is what a
reader sees. All six still stand.

**Proposed wording, not agreed.** Settled against what Kerd does, not against whichever copy
reads better:

1. *Second AI.* Site (`index.html`, `capabilities.html`) says "A second AI reads the work
   independently"; README says "can". Kerd plans review from a partner's recorded cadence,
   and `on-request` means no automatic review, so "can" is the true one. Site → "A second
   AI can read the work too."
2. *The third problem.* Site: "nobody checks the whole of it"; README: "done is whatever the
   AI says it is". The heading is about when work is done, so the README's diagnosis fits.
   Site → README's sentence.
3. *Claude or Codex.* `docs.html` says "Claude and Codex together"; README, index and
   capabilities say "Claude or Codex". Agent pairs Claude with Claude as well as with Codex
   (this repo's own bindings do), so "or" is true. `docs.html` → "Claude or Codex".
4. *Agent's card.* `capabilities.html` describes Agent with Conductor's concert paragraph.
   → Agent's own job, from `docs/guide/agent.md`: it gets a contribution from another AI
   session and brings the answer back, and keeps track of which session is which, so "ask
   Codex to review this" reaches the partner you paired with.
5. *Visuals' card.* `capabilities.html` describes Visuals with Conductor's sketchbook
   sentence. → Visuals' own job, from `docs/guide/visuals.md`: it draws how the parts
   connect, who owns what and what changes, as a saved picture you can open, and a picture
   arrives by default when a proposal has connected parts.
6. *Codex install.* The site's Install gives a Codex route (getting started, `#install-in-codex`);
   the README's Install never does. README → one line after the commands: Codex takes a
   different route, a four-skill core built from a source checkout, see getting started.

**Found, kept out of this change:** `docs/guide/getting-started.md:85` says "the other eight
skills" are left out of the Codex core; Kerd has eight skills in all, so it is four. And
"Kerd runs inside Claude Code or Codex" (README and every site page) reads as full support,
while Codex gets a four-skill core built by hand. Both are wording questions for Anthony.

**Agreed** by Anthony ("y", 19:18) and applied to `README.md`, `site/index.html`,
`site/capabilities.html` and `site/docs.html`, as proposed. Picture:
`six-contradictions.html` / `.png` beside this record.

**Checked:** none of the old phrasings remain in the README or site; `release_check.py`
clean; 760 tests pass. Codex (`codex-tui`), before-push, first read: "Clear to push", no
sentence claiming more than the repo supports, no remaining site/README contradiction.
**Not yet proved:** the live site shows the new wording; that follows the push and
Vercel's redeploy.

**Pending:** Anthony's go to commit and push to `main`.
