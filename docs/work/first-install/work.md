# Work: the front door — install 0.142.0 the way the README tells a stranger to

## Direction

For a newcomer, and for Anthony who has to trust what the front page claims. The
README prints two commands as the way to install Kerd (`README.md:73-76`):

```
claude plugin marketplace add anthonymaley/Kerd
claude plugin install kerd@kerd-marketplace
```

Nobody has ever run them. They were transcribed from the CLI's help text, and three
releases on 2026-09-19 changed what installs: the package's corrected commands
(0.140.0), four skills removed (0.141.0), the ladder of machine checks and its risk
ledger removed (0.142.0). Eight skills should be there afterwards: switch, conductor,
visuals, agent, tend, slainte, kivna, skriv.

Deliverables: a plain report of what actually happens, and fixes for what breaks.

View: [who-can-install-kerd.html](who-can-install-kerd.html) — who can install Kerd today
and what the proposed fix changes.

## Worth it and design

Worth doing because it is the first thing a newcomer does and the one claim nothing
else in the package can compensate for. The site not having been seen in a browser is
a blemish; an install that fails is a closed door.

Two things have to be true before the test means anything, and neither was known at
entry, so both went out first as independent read-only jobs:

- **R1** — can a stranger reach that marketplace at all? Public visibility of
  `github.com/anthonymaley/Kerd`, and whether `.claude-plugin/marketplace.json`
  satisfies what `claude plugin marketplace add` expects, with a source an anonymous
  user can fetch.
- **R2** — how does the install run without touching Anthony's real profile? The
  mechanism, the verbatim command sequence, the teardown, and a before/after check
  that the real profile was untouched.

The install itself stays with Conductor: shared global state, sequential, and it
needs Anthony's go at the gate.

## Risks to keep in view

- The install could write into Anthony's real profile at `~/.claude`. **Countermeasure
  in place, still open until the run:** isolation verified twice (F2), a structural
  before/after check built and shown repeatable, and nothing runs until he gives the
  go. If the redirect ever failed, the damage would be his working 0.142.0 install row
  and marketplace entry overwritten in place — recoverable by reinstalling, but his
  real setup. Named 2026-09-19.
- **Closed:** the published install command could not work for a stranger. Confirmed
  (F1), reproduced (F3) and fixed with the fix itself proved (F4). Named and closed
  2026-09-19.
- **Still open.** A fix may need a release rather than an edit. It is now one line and
  the release check is clean either way, so the question is honesty rather than
  mechanics: 0.142.0 as published cannot be installed by anyone without a GitHub key, so a
  distinguishable fixed version may be truer than quietly repairing what that tag
  points at. His call, being put to him now. Named 2026-09-19.
- **Named 2026-09-19, accepted for the moment:** the fix was proved against a local
  marketplace serving the fixed manifest, not against GitHub serving it. Publishing is
  what closes that gap, and the first install after a push is the check.

## Findings

### F1 — the published install command cannot work for a stranger (2026-09-19)

`.claude-plugin/marketplace.json` lines 12-16 declare the plugin's source as an SSH
URL:

```json
"source": { "source": "url", "url": "git@github.com:anthonymaley/Kerd.git" }
```

**Reproduced.** Queried that exact URL with no key and no agent, which is what a
stranger has:

```
GIT_SSH_COMMAND='ssh -o BatchMode=yes -o IdentitiesOnly=yes -o IdentityFile=/dev/null -o IdentityAgent=none'   git ls-remote git@github.com:anthonymaley/Kerd.git HEAD
  -> git@github.com: Permission denied (publickey). fatal: Could not read from remote repository.
```

The same repository over anonymous HTTPS answers normally and returns `ac4d4db`,
this repo's current tip:

```
git ls-remote https://github.com/anthonymaley/Kerd.git HEAD  ->  ac4d4dbc...  HEAD
```

So the repository is public — R1 also confirmed `"private": false` and HTTP 200
unauthenticated on the API, the web page and the raw manifest — and the failure is
entirely the URL Kerd itself publishes in its manifest.

**Why the first command still works and the second does not.** The two commands take
different code paths in the CLI. `marketplace add anthonymaley/Kerd` uses the
`github` shorthand source, which probes SSH (`ssh -T -o BatchMode=yes ... git@github.com`)
and falls back to HTTPS when that probe fails; the strings `CLAUDE_CODE_REMOTE ||
a.CLAUDE_CODE_PLUGIN_PREFER_HTTPS` and `successfully authenticated` are present in
the installed CLI (2.1.278), confirming that mechanism. `plugin install` then resolves
the manifest's own `url` source, which R1 read as a literal `git clone --depth 1 -- <url>`
with no fallback on that path. That second half is read from the shipped CLI binary,
not yet reproduced; the install test is what proves it end to end.

**Why this machine never noticed.** This machine has a registered key, so the SSH
probe succeeds and everything resolves: `~/.claude/plugins/marketplaces/kerd-marketplace`
has origin `git@github.com:anthonymaley/Kerd.git` and the plugin auto-updated to
0.142.0 tonight. The defect is invisible to anyone whose machine already has a key,
which is everyone who has installed Kerd so far.

**Proposed fix, not yet agreed:** change the plugin's source to the same GitHub
shorthand the README's own first command uses —
`"source": { "source": "github", "repo": "anthonymaley/Kerd" }` — so the CLI's
SSH-probe-then-HTTPS-fallback applies to the install as well. That keeps Anthony's
own SSH route working and gives a stranger HTTPS. Not applied: it is a manifest
change, it is what CI's release check governs, and the install test should first
reproduce the failure so the fix can be shown to cure it.


### F2 — isolated installation works, and the obvious integrity check is a false-alarm generator (2026-09-19)

`CLAUDE_CONFIG_DIR` relocates the whole profile, plugins included, so the published
commands can be run without touching `~/.claude`. Verified twice, independently: R2
probed it, and Conductor repeated the probe — a redirected `claude plugin list`
reports no plugins while the real profile reports Kerd, and everything the redirected
run creates lands inside the temp directory. It is documented in Claude Code's
environment-variable reference and resolved in the CLI as
`CLAUDE_CONFIG_DIR ?? homedir()/.claude`. There is no `--config-dir` flag; the
`--scope project|local` options on the plugin commands would write into a repository,
which is worse, so the default `user` scope plus the environment variable is the route.

**The correction.** R2 proposed comparing checksums of the real profile's plugin
files before and after. That check cries wolf: `known_marketplaces.json` changed
between two of this session's readings, and the cause is ordinary marketplace
auto-update — six registered marketplaces all took a new `lastUpdated` at
2026-09-20T02:22:3xZ because a `claude` command ran against the real profile. The
file is stable across twenty seconds with no `claude` invocation, so it does not
drift by itself, but any un-redirected `claude` call rewrites it. `~/.claude.json`
churns even harder, from the live session this work runs inside.

So the integrity check compares *structure*, not bytes, ignoring `lastUpdated` and
the usage counters: `scripts` in this session's scratchpad as `profile_snapshot.py`,
covering the installed-plugin rows, the marketplace registry minus timestamps, the
`enabledPlugins` list from `settings.json`, and listings of `marketplaces/` and
`cache/`. Baseline taken and shown repeatable: digest
`11ba723cb87ea06c333734c0e910e2754a81d7de7c3f6054181c2365731d1503`, 78 installed
plugin rows, 12 marketplaces, 75 enabled plugins.

One earlier scare was also a false alarm and is recorded so it is not rediscovered:
`marketplaces/` appeared to gain an entry between two counts. It was `.DS_Store`,
which `ls -1` hides and Python's `listdir` does not.

**Still unverified:** whether `plugin install` needs Anthropic credentials, which a
throwaway profile does not have. Credentials are keyed per config directory, and a
marketplace add is a git clone while an install is a file copy, so it probably does
not — but that is inference. The install test settles it, and a credential failure
would be loud and confined to the temp directory.


### F3 — the test, run (2026-09-19)

Both published commands were run twice in throwaway profiles, once with this machine's
GitHub key available and once with SSH refused, which is the newcomer's situation.
The view is [who-can-install-kerd.html](who-can-install-kerd.html).

**With a key — works.** `marketplace add` reported *Cloning via SSH:
git@github.com:anthonymaley/Kerd.git*; `plugin install` installed 0.142.0 from commit
`ac4d4db`. Exactly the eight skills the README names — agent, conductor, kivna, skriv,
slainte, switch, tend, visuals — and none of the four retired ones.

**Without a key — the front door is shut.** `marketplace add` reported *SSH not
configured, cloning via HTTPS: https://github.com/anthonymaley/Kerd.git* and succeeded,
confirming the fallback. `plugin install` then failed:

```
✘ Failed to install plugin "kerd@kerd-marketplace": Failed to clone repository:
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

No `installed_plugins.json` was written and zero skills were available. F1 is therefore
reproduced end to end, and the half that was previously inference — that the `url`
source clones the literal SSH address with no fallback — is now observed in the failure
message itself.

**Anthony's own profile was untouched.** Structural snapshot identical before and after,
digest `11ba723cb87ea06c333734c0e910e2754a81d7de7c3f6054181c2365731d1503`: same 78
installed plugin rows, 12 marketplaces, 75 enabled plugins, same directory listings. All
three throwaway directories were removed.

**Still to prove:** that the proposed fix cures it. The next step tests a fixed manifest
through a local marketplace with SSH refused, so the cure is demonstrated before anything
is published rather than after.

**Side finding, not this work:** the real plugin cache holds 27 abandoned `temp_git_*`
clone directories, the oldest from 2026-09-11. They are Claude Code's install scratch
space, not Kerd's, and they predate this test.


### F4 — the fix, and the obvious fix that did not work (2026-09-19)

**Applied in the working tree, one line, tested both ways:**

```json
"source": { "source": "url", "url": "https://github.com/anthonymaley/Kerd.git" }
```

Proved by rebuilding the stranger's situation and pointing a marketplace at the fixed
manifest. With SSH refused and no environment variable set: *Successfully installed
plugin*, all eight skills. With this machine's key available: also installed, 0.142.0
from `ac4d4db`, all eight skills. Release check clean, 757 tests pass.

**The first attempt failed, and the failure is the interesting part.** The tidy-looking
repair was to name the project the same way the README's working first command names it,
`{"source": "github", "repo": "anthonymaley/Kerd"}`. It was applied, and it still failed
with the identical `Permission denied (publickey)`. The clone directory was named
`temp_github_*` rather than `temp_git_*`, which showed the new path was being taken and
still reached for SSH.

The reason, established by running the same install with the CLI's documented
`CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`, which made it succeed: the `github` source prefers
SSH on the **install** path and only falls back when that variable is set. The
SSH-probe-then-fall-back behaviour that rescues `marketplace add` is not applied when
installing. So the shorthand fix depends on a variable no newcomer will ever set, and
only an explicit public address works unaided.

This is the seventh-instance finding again, in its own file: reading the CLI's code
suggested the shorthand would inherit the fallback, and the run showed it does not. The
static read was wrong and the real run corrected it.

**Not yet done:** nothing is committed or pushed, and Codex has not read the change.
Whether this ships as a bare edit or as 0.142.1 with a release-history entry is Anthony's
call. The argument for a version: 0.142.0 as published is uninstallable for anyone
without a GitHub key, so a distinguishable fixed version is more honest than silently
repairing what the tag points at.


### F5 — Codex's before-push review, and a claim of mine it corrected (2026-09-20)

Codex read the change set under its recorded before-push cadence and returned **not clear
to push**, with two findings, both about the release note rather than the fix:

1. **The blast radius was overstated.** The note called the SSH address "a private one"
   and said only the author could follow the instructions. Wrong: the repository is
   public, and an SSH clone of a public repository succeeds for *anyone with a GitHub key
   registered*, not only its owner. The accurate claim is that the published source was
   SSH-only, so people without a key failed and people with one succeeded. Corrected in
   `README.md`, `CHANGELOG.md` and the view, which carried the same error in its headings
   and row labels.
2. **"Nothing else changed, no skill, no wording and no behaviour" was too broad**, since
   the release necessarily changes manifest metadata and adds release-note wording.
   Narrowed to "No skill behaviour changed."

It confirmed the rest: the explicit `https://` source is the right public declaration and
avoids the install path's SSH preference without relying on an environment variable; no
other newcomer-facing instruction blocks installation; the SSH lines in `docs/playbook.md`
and `docs/machine-setup.md` are maintainer instructions and fine; the three versions are
in sync, the capability descriptions identical, and PATCH is the right call. It noted it
ran no install, no tests and no independent GitHub query, reviewing the supplied evidence
and the repository.

Because the corrections changed the reviewed tree, the before-push gate reopened and the
change set went back for a second read rather than being pushed on the first verdict.

**This is the same finding as F4, one layer up.** My own framing was wrong in a way no
test would have caught, because every test I ran was of the mechanism, not of the claim I
wrote about it. An independent reader caught it.


### F6 — published, and proved from the outside (2026-09-20)

0.142.1 is on `main` as `db97b78` and CI passed. The published fix was then tested the
only way that settles it: a throwaway profile with SSH refused ran the README's two
commands against the **live** marketplace.

```
✔ Successfully added marketplace: kerd-marketplace
✔ Successfully installed plugin: kerd@kerd-marketplace
```

It installed version `0.142.1` from commit `db97b78` with all eight skills — agent,
conductor, kivna, skriv, slainte, switch, tend, visuals — and none of the four retired
ones. GitHub now serves `https://github.com/anthonymaley/Kerd.git` as the plugin source.
Anthony's own profile was verified unchanged against the entry baseline for the third
time, and every throwaway profile was deleted.

The gap declared before the push — that the fix had only been proved against a local copy
of the manifest — is closed.

## Goal check

Read against the success criteria proposed at Shape:

- **The two published commands complete and deliver the eight skills the README names,
  with none of the four retired ones.** Met, and met against the live marketplace rather
  than a local stand-in.
- **Anthony's real profile provably unchanged.** Met, by structural comparison at three
  points, digest identical each time.
- **Every failure reported with its exact command and output.** Met; the failures are
  quoted verbatim in F1, F3 and F4.
- **Anything fixed is re-tested by running the commands again, not by reading the
  change.** Met twice over: once locally before the push, once live after it. The first
  candidate fix was rejected precisely because this rule was followed rather than assumed.
- **Not done, and out of scope by agreement:** the README's second route,
  `claude --plugin-dir`, was assessed but never exercised. R2 found it is not footprint
  free — it writes a `pluginUsage` row to `~/.claude.json` — so the README's claim that
  "nothing is installed or disabled globally" is true about plugins and marketplaces but
  not about every trace. That is an untested claim on the front page and belongs in
  `TODO.md`, not in this work.

## Risks, read back at the close

- Install writing into Anthony's real profile — **closed**, verified unchanged three times.
- The marketplace unreachable for a stranger — **closed**, was true, fixed and proved live.
- The fix needing a release rather than an edit — **resolved**, shipped as 0.142.1 on his
  decision.
- The fix proved only against a local manifest — **closed** by the live install in F6.

Nothing open.


## Success and proof

Proposed, not yet agreed with Anthony:

- The two published commands run to completion in a throwaway profile, and the
  result presents the eight skills the README names, with none of the four removed
  ones (Drive, Lorg, Interrogate, Pair) and no reference to the retired ladder.
- Anthony's real profile is provably unchanged afterwards, by comparison against the
  baseline recorded at entry.
- Every failure is reported with the exact command and its exact output, so a fix
  can be argued from evidence rather than inference.
- Anything fixed is re-tested by running the commands again, not by reading the
  change. "I edited it" is not "it installs".

Open: whether the trial route the README also offers, `claude --plugin-dir`, is in
scope for this sitting or a separate item.

## Boundaries and decisions

**Must:** the test runs in a throwaway profile or a second account. Installing
anything into Anthony's own profile needs his explicit word first. Any fix is read
by Codex before it is pushed. A peer session cannot authorize a push.

**Open (delegated to Conductor):** which probe settles an unverified isolation claim;
the order of the checks.

Time/resources: none stated.

Stopping point: a report plus plain fixes. A release, if one turns out to be needed,
is a separate decision that goes back to Anthony.

## Agreement

Agreed and complete. Anthony chose this work with a plain "yes" to Switch In's
recommendation on 2026-09-19 at 22:18, which selected it without approving any
operation. He then approved each consequential step separately, in this order: the
install test in a throwaway profile, applying and proving the fix, preparing 0.142.1 with
a release note and sending it to Codex, and the push. The boundary he set at the start
held throughout: nothing was installed into his own profile.

## Decisions and changes

- **2026-09-19, entry.** Selected from Switch In's arrival. Conductor opened at Shape.
  Two read-only research jobs dispatched before any write, because the work's first
  unknown is whether the test is even possible.
- **2026-09-19, found at entry.** The real profile already carries `kerd-marketplace`
  registered as `{source: github, repo: anthonymaley/Kerd}` — exactly what the
  README's first command would produce — and it auto-updated at 2026-09-20T02:15Z,
  which is how this machine's plugin cache reached 0.142.0. So the GitHub route works
  for at least this machine. It does not establish public visibility, because this
  machine holds credentials for the repo. R1 owns that question.

## Now

Stage: Complete
Current activity: none. The work is finished and published.
Analysis so far: `claude plugin` exists on this machine (CLI 2.1.278) with `install`
and `marketplace` subcommands, so the published commands are not fiction. The real
profile's plugin state lives in `~/.claude/plugins/installed_plugins.json`,
`known_marketplaces.json`, `marketplaces/` and `cache/`; a checksum baseline of the
two JSON files plus listings of the two directories is in this session's scratchpad.
Current understanding: the work is a from-scratch install test with a hard boundary
around Anthony's own profile. Nothing about the outcome is known yet.
Open issues: none in this work. Left for TODO.md: the `claude --plugin-dir` trial route
is unexercised and the README overstates it as leaving no trace.
Pending question: none. Four were asked and all four answered yes: run the install test
(2026-09-19 23:10), apply and prove the fix (23:30), prepare 0.142.1 and send it to Codex
(2026-09-20 11:42), and push it (12:15).
Decision context: the go decides whether anything is written on this machine; it is
bounded to a throwaway profile and excludes his own.
Next action: none. TODO.md still lists this install test as the selected next and should
be updated when the sitting is saved.

## Score and delivery

Score: none written; the two research steps were written by Conductor directly, the
work being clear enough not to need a composer.
Current passage: R1 and R2, both dispatched.
Assignment: step author Conductor for both; performers are two native Claude players.
Fit: R1 — needs a factual visibility check plus a read of the manifest against the
CLI's expectations; Sonnet 5 at high because the question is bounded and the sources
are named. R2 — needs care about where files land; Opus 5 at high because a wrong
answer writes into Anthony's real setup, the one mistake this work must not make.
Settings: R1 requested Sonnet 5 at high; R2 requested Opus 5 at high. Observed model
and effort unverified until read with `job_evidence.py` after each return.
Review plan: Codex `codex-tui`, recorded cadence checkpoints and before-push. It
reads any fix before a push. No review is due yet, there being no change.
Change read: not applicable; both jobs are read-only and own no files.
Evidence: R1 returned and checked; observed Sonnet 5 at high, matching the request.
R2 returned and checked; observed Opus 5 at high, matching the request. R2's proposed
integrity check was found wrong and replaced — see F2. The install test itself was run
inline by Conductor and is recorded in F3, with the commands' own output as evidence.
Its verdict (a stranger cannot install) is accepted and its transport half was
reproduced independently — see F1. Its inferred half, that the `url` source clones
with no fallback, stays labelled as read from the CLI binary rather than reproduced.
R2 outstanding.
Repair/attempt state: none.

## Results and evidence

Checked: the published install commands fail for anyone without a GitHub key (F3), and
succeed with one, delivering exactly the eight skills the README promises at 0.142.0.
Anthony's profile verified unchanged by structural comparison. Every README guide and
picture link resolves on `origin/main`.

Also checked: the fix installs for a stranger and for the author alike (F4), the release
check is clean and all 757 skill tests pass.

Not proved: that the fix behaves the same once published, since the tested marketplace
was a local copy serving the fixed manifest rather than GitHub. The plugin content was
fetched from GitHub in every case, so what remains untested is only that the same file
works when GitHub is also serving the manifest. Codex has not yet read the change.
