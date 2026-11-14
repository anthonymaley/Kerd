# Out: clean boundaries

Contents:

- [Out](#out): read what changed, the session account, collaboration in history
  - [One coordinated closeout](#one-coordinated-closeout): one owner, the contribution checkpoint, reconciling active work
  - [Add to Conductor's sketchbook](#add-to-conductors-sketchbook): what the sitting settled
  - [Keep the outside-the-repo list](#keep-the-outside-the-repo-list): live links outside the repository
  - [Save the selected continuation](#save-the-selected-continuation): the next action, its boundary, urgent risks
  - [Leave a lean start point](#leave-a-lean-start-point): rulings, closed rows, the reading set, `measure`, the named-file save and the `boundary` check
  - [Close with the saved-place box](#close-with-the-saved-place-box): the closing renderer, its JSON shape and the restart line
- [Default verified save when pushing is authorized](#default-verified-save-when-pushing-is-authorized): `save --push`, `pickup`, `prepare` and `boundary` shapes

Picking up is in [In](in.md).

## Out

Read the active state and inspect what actually changed. Preserve the current
agreement, decisions, exact next action, unresolved jobs and important findings.
After the contribution checkpoint below, append an evidence-backed session
account to the existing history, under its own heading for this sitting even
when that day's log already holds an earlier one, so the next In's Last session
reads the newest sitting; read the clock
for dates/times written now. Unknown start time stays unknown. Do not retain the
whole native conversation or private session IDs as project history.

**When the session log or TODO.md is missing.** Setting a project up with
`/kerd:tend` is optional, so Out may meet a project with no `kivna/sessions/`
folder or no `TODO.md`. Missing means a successful read found it absent; a path
that exists but cannot be read is not missing, so Out does not write over it and
names it in `warnings` instead. Out creates what is missing: `kivna/sessions/<date>.md`
for this sitting's account, and a minimal `TODO.md` whose `## Now` section holds
the open items Out saves (or the line “Nothing open.” when there are none, so the
section is never empty). Save them with the other named files, and name them in
the box's `this_session` in plain words (“Started a session log and a to-do list
for this project”). If either cannot be created, say so in `warnings` with the
reason, and save the rest. The reading set and the `measure` call then name only
records that exist: leave the missing file out of `--file` and `--section`
rather than naming a path `measure` cannot read. Carry what it would have held
into a record that does exist (the session account and the open items into
`CONTEXT.md`'s current section), and measure again. When no existing record can
carry them, so a fresh reader could not recover the open work and next action,
set `handoff_ready: false` and name the gap in `next`.

When collaboration matters to the next pickup, retain a short provider,
contribution and evidenced result, plus the relevant next-action/work-record
link in that existing account. Do not copy private pairing IDs or aliases into
Git history. This is project memory, not a session registry or proof that a
particular partner has read it; Agent resolves live identities separately.

### One coordinated closeout

The owner is the session the person asked to run Out, or the session controlling
the agreed work when it starts Out itself at the end of finished work (Conductor's
[One clear finish](../../conductor/references/journey.md#one-clear-finish)); a
contributing partner session never starts one. If another Out owner is
already known, return this session's account to that owner instead of rewriting
shared pointers. If both sessions were asked to own the closeout, the person
names one before either writes. Before editing the handoff, check the owner's
existing pairing-role continuity using Agent's
[Out ownership check](../../agent/references/session-succession.md#out-designate-this-roles-continuation).
Reuse an explicit replacement choice already given; Out alone grants no role.
No binding means no setup stop. Unresolved routing does not prevent a safe memory
save, but its continuation limit must remain visible.

**Contribution checkpoint — before drafting or editing closeout records.**
Identify the known sessions that contributed to this sitting, including the
owner. Compare their necessary decisions, authority, results, limits and unfinished
work with the accounts already available. Returned subagent results and adequate
work records count; do not request ceremonial acknowledgements or fresh accounts
for material already captured. If a necessary delta remains with a participant,
request it directly through Agent and retrieve the response before drafting the
combined closeout. Submission or timeout is not receipt. The owner drives this
collection; the person must not have to ask each agent or relay their accounts.
A known pending job is covered when its owner, current state and result-retrieval
location are captured. Its unfinished result is not itself missing memory; carry
the wait/retrieval step forward instead of waiting merely to finish Out or
claiming the job done.

Show the checkpoint in one short line, for example: “Contributions captured:
Claude (review) + Codex (implementation); missing: none.” Name actual contributors
and roles, not private IDs; this is an accountable coverage statement, not a
machine proof. When this session is the only contributor there is nothing to
reconcile, so show no checkpoint line. An unavailable participant is not itself missing necessary memory:
if other evidence restores the scope, authority, known outcomes, limits and next
action, record any residual gap and why it does not prevent safe continuation.
Never turn an unresolved observation into a verified result. If necessary memory
is unavailable, explicitly report incomplete coverage, the missing contribution
and the recovery step before writing a partial account.
Preserve known memory, but set `handoff_ready: false` and do not offer to clear
or designate a ready successor. Do not wait indefinitely or invent completeness.
Only after coverage is complete—or its specific gap is explicitly reported as
incomplete—draft the closeout. A material contribution arriving during drafting
reopens the checkpoint; incorporate its delta before finalizing, not in a late
repair after claiming completion. Reuse one account, not duplicate session logs.
If a necessary delta arrives after saving, reopen the account and correct the
completion claim. Save the amendment within existing authority, then re-designate
after any pointer change; if saving is not authorized, report the pending amendment
instead of claiming the old handoff includes it.

During Out, the owner alone writes the shared pointer, active list,
session account and any work record it is reconciling. Contributors write only
an already-owned record no other session is editing; otherwise they return their
account to the owner. Re-read affected records from disk after a contributor
finishes editing, before reconciling them. Contributors retain decisions, scope/authority,
findings, verification limits and unfinished work in their existing work record
as contributions finish. A read-only contributor returns that account for the
owner to record, rather than gaining write permission.

Use the sibling [Agent](../../agent/SKILL.md) for missing accounts and own their
retrieval. No all-session sweep, whole-transcript read or new inbox. The reply
does not grant approval, prove a claimed observation or settle a contradiction.
Discovery lists sessions, not what they hold; unknown standalone contributions
are not covered by a known-partner check. If there is concrete uncertainty about
who holds necessary work, ask the person to identify the contributor. Do not
make every ordinary Out repeat a session census or assume an unseen session
has nothing relevant.

The owner reconciles the contributions into the existing account, work record
and lean start point; other sessions do not run competing shared-file closeouts.
Link the detailed contribution instead of copying it into every file. Work on
another branch or worktree is named by branch, record and saved location in the
start point, with local-only/uncommitted limits carried; retain the necessary
account in the handoff if its record is not reachable there. Out does not merge,
push an additional branch or sweep another session's edits into this save.
Check that a fresh reader can recover the agreement, restrictions, evidence
limits, unresolved work and next action without either old conversation open.
Before finalizing, verify the checkpoint's captured contributions are actually
represented in that reading set, rather than only in the owner's native context.
A pending job keeps its actual owner/status; do not stop it or call it finished
to close the record. If a peer is unavailable, preserve known work and name the
specific missing context and recovery step. Do not claim the handoff ready or
advise clearing context while necessary detail is still unsaved.

Reconcile active work against evidence. Remove completed tasks from active lists
while retaining their completion record. Retire redundant work only with a known
reason. Keep independent sub-findings and migration-sensitive work open. Archive
historical detail with reachable links; age alone doesn't retire a decision,
dependency or risk. For an initial legacy reorganization, keep a recoverable
original. Do not rewrite dated history or maintain duplicate living plans.

### Add to Conductor's sketchbook

Conductor owns one sketchbook per piece of work, its existing work record, and
keeps it as the work goes. Out makes sure nothing the sitting settled is missing
from it, whether or not Conductor ran: for each piece of work the sitting moved
forward, the Out owner adds what the sitting settled and the record is missing.
Reuse any existing record for that work. Where substantial work has none, the Out
owner starts one at `docs/work/<slug>/work.md` from Conductor's
[writing aid](../../conductor/references/work-record.md); a small fix needs none.
When `kivna/vault.json` sets `work_notes`, start it instead at
`<notes root>/<slug>/work.md` in the private vault repo and point to it as
`notes:<slug>/work.md`.
Add only what the sitting actually settled: the person's words as theirs,
proposals as proposals, nothing invented. When what it adds resolves a header or
position line (stage, what is or is not yet approved) or a field marked pending or
asked, rewrite that line too, never only append below it: a fresh reader trusts the
header first. Ask the person nothing to fill it, and
add no step to their closeout. Link it from the active list.

### Keep the outside-the-repo list

When `kivna/vault.json` sets `work_notes`, Out keeps one private list at
`notes:outside-the-repo.md`, the notes root's `outside-the-repo.md`: the live
things the work leans on that sit outside the repository, such as a claude.ai
artifact, a message awaiting a reply or an open pull request. One line each: what
it is, its link, who owns it and what it is waiting on. A thing earns a line when
someone will open it again or something waits on it; a link used once stays in
the session log. A line leaves when its thing is saved in the repo, merged,
answered or no longer needed. Out adds what this sitting created or still waits
on and prunes what closed, asking the person nothing. Past about eight lines, the
pruning is not gripping: say so rather than let it become a link dump. It stays
in the vault because such links can be private while the repo is public. Always
name it in the pickup reading set; without `work_notes`, Out keeps no such list.

### Save the selected continuation

Update the next session's lean start point with what is true and what to do next.
After reconciling contributions and active work, leave one concise continuation
in the existing pointer's current section, or a directly linked current work
record included in the pickup reading set. Save the choice the sitting reached,
not only its collection of open tasks:

- the selected next action and owner, with agreed/proposed/awaiting-approval status;
- the completion steps within that scope and where it stops, including exclusions;
- its pending question, if any, distinguished from other open questions.

Use existing prose or headings; these are meanings to preserve, not three new
required fields. If the selection already exists clearly, reconcile it in place
rather than copy it to several living records. Keep the session log as the dated
account and the broader TODO list as open work; link instead of duplicating them.
Do not turn a proposed next step into agreement. Where the person has not selected
work, retain a grounded recommendation as proposed or a genuine unresolved choice;
Out does not need a ceremonial approval just to save that uncertainty.

For example: “Pending approval: Claude builds main, installs it on Master,
verifies and records the installation; stop before playback. Question: build
main, install it on Master, verify and record it, stopping before playback —
approve?” is one scope. A later playback check can remain
in the wider plan without becoming part of that approval. If no action is
selected and none can be grounded, say so. Never change a user's priority to
make the handoff neater.

Before saving, check that the pointer/current record and the log's next-action
account agree on that scope and stopping point; a fresh reader should not have
to assemble them from competing lists. Then confirm that every file or section the
next step names as already there (to read, change or follow) exists: run the
helper's `measure` on those targets alone, `--record` the start point, `--file`
each named whole file and `--section FILE HEADING` each named section. Only
`status: "measured"` with exit 0 confirms them. A blocked result (exit 2: a
missing file, a heading not found exactly once, an empty section) or a check
that could not run or be read is not "exists": point the step at the real file
or heading, or word it as something to create, and check again before saving.
A target reported `tracked: false` exists only on this computer, so it is saved
with Out's records or the step says so. A file the step says to create is not
checked. Include this selection in the measured
reading set and carry it into the closing box's `next`, with its reason in
`why`, and up to two other open items worth offering beside it into `next_in`,
each with its reason; save those beside the selection as proposed choices for
the next arrival, not agreement and not a replacement for its weighing. Save why it matters to the product, not only what it is: the next In weighs it against
the other open work and shows only a reason a person can check. Work that only
proves the project's own mechanics is saved as open work, not as the selection,
unless it blocks product work or the person chose it. So is watching for
behaviour in real use, and only waiting for the person to decide: those stay open
work, never the selection (a grounded route that resolves a pending choice is a
concrete item). When nothing in the active list can be built now, select one
concrete item from the Backlog or the records that they do not defer, park or
hold, with its why, and make the `next_in` choices concrete items too; “keep using
it and watch” is never the saved next step; with no eligible item, say so. In restores
the meaning even when an older handoff has no named fields; it does not declare
the selection missing merely because it was written as a sentence. New user
direction can supersede it. Changed evidence can make it stale; Switch
explains that and proposes a replacement, never calls that replacement agreed.

Alongside that selection, keep each known, unresolved risk the active records
flag as urgent or imminent **inside the pickup reading set**, even when it does
not affect the selected action. A concise line in the pointer's current section
can carry the risk, its recorded observation date and source, clearly labelled
saved or freshly checked; otherwise include the relevant source section in
`read_args`. Unknown dates stay unknown. A link to an unread section is not
coverage. Reconcile an existing risk line rather than adding a second stale copy.
If the risk is only a bullet inside a large Backlog, prefer the concise carried
line rather than loading that whole section; the existing heading-boundary rule
also allows a narrow source selection. When the source section is selected,
the pointer can identify the risk and source without repeating its figures.
This carries recorded urgency, not a fresh operational verdict or authority to
investigate; routine owed work does not become urgent to justify inclusion.

When the person stated how much technical detail they want (“keep the technical
stuff out of my way”, “show me the commands”), save it in
CONTEXT.md's governing lines (in a new CONTEXT.md, the first line under its title),
in their own words and dated, as one line:
`Person's preference (2026-11-14): “keep the technical stuff out of my way”.`
Only a preference they stated is saved: a self-description (“I'm not a developer”)
or an impression shapes this sitting's words but is never saved as one.
Reconcile an existing line rather than adding a second; drop it only when they
take it back. It is a standing preference, not a ruling about the work, and Switch
In passes it to Conductor, which follows it as written: less detail means a fresh
session does not lead with Kerd's stage words; more detail means it shows them.

Historical decisions needed by a future feature remain discoverable by subject;
the active memory must include constraints that affect the next work. Be explicit
about unreconciled historical sections rather than calling the migration lossless.

Alongside the next action, name the small reading set that supports it: actual
files or complete sections, why they matter, and where deeper history lives.
Use the existing handoff/work record; do not add a parallel manifest or duplicate
source text. This lets the next pickup reuse the outgoing session's knowledge
of the work instead of rediscovering the entire repository. Preserve unresolved
decisions and authority even when the next action looks simple.

### Leave a lean start point

The next pickup pays for every byte the start point carries, so Out ends by
making it small on purpose, not by reading less next time. Four moves, in this
order, each leaving a reachable link behind:

1. **Rulings stay, cases move.** The loaded pointer keeps each standing decision
   as its ruling — the bold sentence and its date — only for decisions that
   govern the next work or a constraint the next sitting must honour. The full
   entry (the case, the evidence, the argument) lives in a living decisions
   record (`docs/decisions.md` by convention), newest first with an index of
   rulings so history is discoverable by subject. Superseded decisions are
   marked there, never deleted. A ruling without its case is a link, not a loss.
2. **Closed work leaves the active list with its reason.** The closure review
   already gives every open row a verdict; rows judged done or dead move to a
   backlog archive (`docs/backlog-archive.md` by convention) with the verdict,
   the evidence and the date. Open and unsure rows stay. Age alone closes
   nothing.
3. **Name the reading set in the start point** as exact files and complete
   sections, in the pointer's current-state section, with why each matters.
   The default set is the pointer, its designated complete active list (including
   child sections), explicitly current linked work records, and the newest session
   log, plus `notes:outside-the-repo.md` when `work_notes` is set; add source
   sections for governing current decisions, standing constraints
   or known risks when they are not already covered. Before measuring or claiming
   memory ready, compare those active records used for this closeout with the
   actual selected text, including unresolved urgent/imminent flags in their
   Backlog sections. Carry any missing risk, constraint or decision into that
   text or select its source section. Do not search the whole archive or recheck
   live systems to perform this coverage check. An unresolved gap stays disclosed,
   not a complete handoff claim. Size targets never justify dropping material
   active-work context or an urgent risk; re-measure after changing the set.
4. **Measure it and record the reading.** Run the helper's `measure` on that
   set and write the result beside the reading set. The example below is the
   ordinary case, with both `TODO.md` and the session log present; when either
   could not be created, use the adjusted selection from
   [When the session log or TODO.md is missing](#out) instead:

   ```sh
   python3 /path/to/switch/scripts/handoff.py --project /path/to/project measure \
     --record CONTEXT.md --section TODO.md '## Now' --file kivna/sessions/<date>.md
   ```

   It counts bytes exactly and estimates tokens at four bytes each, labelled as
   an estimate; the target is the trial's 8,000 unless the work agreement sets
   another (`--target`). Over target is information: prune further under the
   rules above, or record why the set must stay larger. It never blocks a save.
   The measurement is for the record only: never tell the person the token or
   byte figures, the target or the reading set's size.
   `measure` now warns when a source is not tracked: `prepare` refuses an
   untracked source and a `notes:` source must be tracked in the vault, while
   pickup can still read a project record the project deliberately keeps out
   of Git, named with `--preserve`.

   Name the few findings that must survive this sitting, three to five, one
   line each, and pass them on the same call as `--carry-file <path>`, a file
   with one phrase per line that only its owner can read, or `--carry-file -`
   to pipe them on stdin. Never pass a phrase as a bare argument: argv is
   visible to other local accounts on the machine. **Pipe them on stdin**, one
   phrase per line, with the shell's own `printf`. That keeps them out of the
   helper's arguments, but a host that runs the whole command through `sh -c`
   still shows that shell's command line, phrases included, so a carry phrase
   never holds a secret. On a machine used only by its owner, the ordinary case:

   ```sh
   printf '%s\n' 'first finding' 'second finding' | python3 /path/to/switch/scripts/handoff.py \
     --project /path/to/project measure --record CONTEXT.md --section TODO.md '## Now' \
     --file kivna/sessions/<date>.md --carry-file -
   ```

   On a machine shared with other accounts, do not pipe them: make an owner-only
   file with `mktemp` (readable only by you), write the phrases into it with the
   host's file-write tool, never a shell command, pass `--carry-file <that path>`,
   remove it after the call, and say so:

   ```sh
   python3 /path/to/switch/scripts/handoff.py --project /path/to/project measure \
     --record CONTEXT.md --section TODO.md '## Now' --file kivna/sessions/<date>.md \
     --carry-file /path/from/mktemp
   ```

   Otherwise do not make a temporary file for them: `mktemp`, a write and an `rm`
   outside the project are three permission prompts a new user cannot judge. Every
   Out input that accepts `-` goes on stdin the same way (`measure --carry-file -`,
   the closing box's `--closing -`). Only for the carry phrases on a shared
   machine (above), or for any input where a host cannot pipe at all, make the
   file with `mktemp`, remove it after the call, and say so in that turn;
   never a fixed name in a shared folder such as
   `/tmp`, where another project's run can read or overwrite it. A phrase `measure` reports
   as not in the reading set is fixed by writing it into CONTEXT.md or TODO.md,
   or by adding its source to the set, then measuring again. This never blocks
   the save and asks the person nothing.

   The measurement and `read_args` are for Kerd, not the person, who may open
   `CONTEXT.md`: keep them in it, under its last heading,
   `## For Kerd's next pickup (you can ignore this)`, which Out creates when
   missing and keeps last. Save the returned `read_args` array beside that measurement
   under that heading. It is the exact selection to reuse at In, not another manifest.
   For the example above (both files present) it is:
   `["--record", "CONTEXT.md", "--file", "kivna/sessions/<date>.md", "--section", "TODO.md", "## Now"]`.
   When the project's records sit in a Git repo it shares with other projects
   (a vault holding several projects' folders, the project run as that repo),
   add `"--scope", "<its folder>"` to the saved `read_args`: `prepare` and
   `pickup` then refuse only unsaved changes inside that folder, so another
   project's unsaved notes elsewhere in the repo no longer stop this pickup,
   and every project source must lie inside it. Pass it to `measure` too, which
   carries it into the `read_args` it returns.
   Measure and prepare resolve these arguments through the same selector. Never
   measure an excerpt then hand off its containing file or section. Each source
   reports its byte count and `reaches_eof`. Complete files always reach EOF;
   for a section, true means no later same-level or higher-level heading ends
   the selection: a lone `## Now` includes the entire remainder, not just the
   first task. If that is too broad, give the intended
   block a real heading boundary (preserving the history), select it and measure
   again; do not substitute a smaller estimate or silently truncate the read.
   Re-measure changed selections or source content; a previous reading is not a
   size guarantee for edited files. Keep findings archives available on demand.

The first run on a legacy pointer is a migration: keep a recoverable original
(the move itself, in Git, plus a dated note in the session log), reconcile any
conflicting current claims, and say what was not reconciled. Do not apply the
migration to an unrelated live project.

The living handoff describes the sitting that is ending, not the moment it was
written. A record states the revision observed while writing, so a boundary
commit made afterwards leaves it naming an ancestor with a next action already
done. Keep those apart: label the observed revision as the position before the
save, and let the next action be what remains after it. Never write the
resulting commit ID into a file inside that commit; name the boundary by branch
and record, and let `git log`/`git show` supply the ID. When the save completes
work the record still lists as pending, correct that record in the same
boundary. Say plainly which the handoff reached — prepared locally, committed,
or verified at the remote; a local memory save is neither of the last two.

Record the scope rule and where the boundary is, not an exhaustive file list.
`git show --name-only <commit>` reproduces that inventory on demand, so a copied
path list costs every later pickup and proves nothing Git does not already hold.
Existing manifests stay as reachable history, not required pickup reading.

Inspect pending jobs before ending a sitting. A running job is not saved merely
because its task name appears in a file. Respect existing direction on whether
it continues; a genuine unresolved ownership issue needs a decision.

Each command is one plain call: one helper or git command on its own, with absolute paths (`--project /abs/project`, `git -C /abs/project …`) instead of `cd`, never `cd … &&`, `; echo`, `| head` or another command chained on, so the person can allow it once; read files with the host's file reader, not `cat` or `head`, and edit prose with the host's file-edit tool, never `python3 - <<EOF`.

Under the agreed Git authority, commit the relevant work/session files by name
and push to the intended branch. A project with no remote configured
(`git remote` succeeds and prints nothing; a failed read is not “no remote”) has
nowhere to push: save without `--push`, and do
not ask the person to push or add a remote to finish Out. When `kivna/vault.json` sets `work_notes`,
save and push the vault repo the same way, by the same named-file save,
alongside the project; the sketchbook it holds is part of this sitting's saved
place, not a separate closeout. A vault with no remote configured is saved
without `--push`, by the same rule. Run each vault git command (add, commit, push,
rev-parse) as `git -C <the notes repo's literal absolute path> …`, naming files
explicitly. Never put the repo behind a shell variable or a `cd $VAR` prefix: the
git guard cannot read where it points and refuses it. During a concert on its own
branch, that is the concert branch its sketchbook records: before committing, check the checked-out
branch matches it, and stop without saving if it does not. Out saves and pushes
there and does not merge it back; the merge is the person's decision at the
concert's end. A save commits only the named files. Out names its own records:
the start point, `TODO.md`, the session log, any sketchbook it wrote and, with
`work_notes`, `notes:outside-the-repo.md`. Other
files the sitting created or changed and left uncommitted, tracked or untracked
(code, or a generated output such as an export; `git status --untracked-files=all`
lists them), do not join Out's save on its own judgement: name each one to
the person in one question, saying which a tool made (an export, a report), and
include only those they say to keep in the project history. Never leave one
unmentioned either. Ask it once, in Kerd's speech-bubble form and plain words, for example
`> 💬 **These files of yours changed and aren't saved yet: tally.py, and requests-2026-11-14.csv, which the export made. Which should I save too?**`.
To the person, Out “saves”: it does not “commit by name”, and a project with no
remote is “saved on this computer only”, never “no remote”. Git words reach the
person only when they use git words themselves; the helper calls and records keep them.
That includes the short progress lines between steps, which the person sees too
(“checking what's saved”, not “whether there's a remote”). Asked what a word means,
explain it plainly and answer the worry behind it; never claim it wasn't said.
Files the project already ignores are not in the question: the project chose
to ignore them. When that list cannot be read (`git status` fails), say the
other files are unknown, never that there is nothing else. An untracked file
they want left out stays local through `--preserve`, recorded as below, and is
not asked about again. A tracked file they want left out cannot be preserved
(the helper refuses tracked paths) and is never stashed: say plainly, before
saving, that the save will be marked incomplete because that change stays
unsaved, save Out's records, and name it in the box's `tree`, so the boundary
check refuses and the box shows it. When they say an untracked generated file
should never be saved, add one anchored, escaped rule for exactly its path to
`.gitignore` (a leading `/`; `*`, `?`, `[`, `!`, `#` and trailing spaces
escaped with `\`), check with `git check-ignore -v -- <path>` that this rule,
and no wider one, matches it, and save `.gitignore` with Out's records; a
tracked file never gets an ignore rule. Exact paths
the project has already decided to keep locally — a scratch patch, a stray build
artifact — are acknowledged with `--preserve`: they stay untouched and are reported
as local only, not saved. Keep that acknowledgement in the project's existing
memory as exact paths; it is not a pattern, an ignore entry or a new config file,
and it never deletes or stashes. New or unacknowledged work still needs resolution,
not blanket staging. Show locally saved vs committed vs remotely verified. A failed
push leaves useful local work recoverable; do not call that a cross-device handoff.

With `work_notes` set, save the vault repo first and take its commit
(`git -C <notes repo> rev-parse HEAD`, the same value `boundary` reports as
`notes_commit`); write it into the start point beside the pickup reading set
("Notes commit: <sha>") before the project's last commit, so the start point is
committed with it and the tree stays clean afterward. The next In passes it as
`--notes-commit`.

Then prove the boundary, after the last commit and before the box, with the same
helper: `python3 "$SKILL_DIR/scripts/handoff.py" --project <project> boundary`,
repeating `--preserve <path>` for each acknowledged local path. It fetches now
and exits 1 when the fetch fails (cached refs are not verification), when no
remote branch contains HEAD, or when the tree holds anything unsaved beyond the
preserved paths. Read its output whole, never through `tail`, `head`, `grep`
or another filter that can drop the status: the verdict follows the status and
exit code in this call's own result, by the mapping under
[the saved-place box](#close-with-the-saved-place-box), and an unseen status is not
recorded, never passed. `git status` and `git log -1` do not prove this: a clean tree
says nothing about whether any remote has the commits. Its `stashes` count is
information, not a refusal: when it is nonzero, say so in `warnings`
("2 stashes on this machine, not saved"). Run it on every repo the sitting
committed to; a local-only Out is allowed, and its box says so instead of ✓.
For a repo with no remote configured at all, the check skips the fetch and the
remote search and refuses only unsaved work; that repo's verdict is
`local_only`. A repo that has a remote keeps every check: a failed fetch or a
commit no remote branch holds still refuses, and the box still says to keep the
session open. Only remote-tracking refs this fetch refreshes count as holding
the commit: those a configured remote's fetch refspec writes. A leftover ref
from a removed remote, or one outside the refspec, proves nothing. Each remote
is fetched by name. Kerd does not model every Git fetch rule: a remote with a
negative fetch refspec (`^…`) or `skipDefaultUpdate` set makes the check refuse
with “The check can't prove the remote refs are current for this configuration
(…); push and confirm by hand.”, and a refspec Git itself rejects stops the
check with no verdict. It reads
`kivna/vault.json` and each repo's HEAD, remote names and remote settings (URLs,
fetch refspecs) first and checks against those. After every repo is checked, it
reads vault.json and each repo's HEAD, remote names and settings and unsaved
paths again, and any change refuses. A git read that fails stops the check with no verdict (a
detached HEAD is reported as no branch, not a failure). vault.json counts as
absent only when it does not exist; a directory, an unreadable file or anything
other than a JSON object stops the check rather than skipping the vault.
With `work_notes` set, this includes the vault repo, under the same rules: the
boundary check covers both, and the box shows both as saved only when neither is
refused. The result's `verdicts` names each repo's verdict (`ok`, `local_only` or `refused`),
and the combined status is `boundary_ok` only when every repo is `ok`,
`boundary_local_only` (exit 0) when none is refused and at least one is
`local_only`, and `boundary_refused` otherwise.
Its `notes_commit` must equal the commit already written into the start point; if the
vault moved since, record the new one, commit again and re-run `boundary`. Never write
anything after a passed check.

### Close with the saved-place box

End Out on one box, rendered with the same packaged renderer:

```sh
printf '%s' "$closing" | python3 "$SKILL_DIR/scripts/where_we_are.py" --closing - --markdown
```

Pipe the JSON on stdin as shown, not through a fixed-name file in `/tmp`.

The box is the last thing in the message: its closing line ends Out, and nothing
follows it: no note, footer, commit trailer or remark about a preserved file.
Anything worth saying goes into the box (attention or This session) before it is
rendered, or into the records.

Use the same chat-versus-terminal presentation choice as [In](in.md#welcome-back-the-screen-summary). The box
mirrors the arrival, in plain product English: a one-row grid (PROJECT, SAVED,
PHASE, RELEASED), **This session** with what changed for the person one line each,
**Switch In will offer** (proposed, not agreed): the next step first, marked
recommended, with its **Why**, then up to two other open items, each with its
reason, then one closing line. These are the choices the next arrival's picker is
expected to carry; the next Switch In still re-weighs every open item and may
offer different ones. Without other items the section reads **Next time** with
the next step and its **Why**, as before. Save
mechanics (commit, file count, remote, reading set, measurement, log path) stay
in the records the next Switch In reads, not on the screen. A save problem
appears under **ATTENTION**, only when it is true.

`$closing` is filled from the helper's save result and what Out just wrote.
**Copy the shape from here; do not open the script for the keys.** `saved` is
one of `remote-verified` (the helper's `saved_to_remote`), `committed` (a local
commit, push not verified) or `not-saved`; the banner, the SAVED cell and any
attention line follow it. An absent or unrecognised `saved` renders SAVE STATUS
NOT RECORDED, never "nothing committed": unknown is not evidence.
`boundary` is the boundary check's verdict, read from the status and exit code
of that call's own result, both together:

- `status: "boundary_ok"` with exit 0 → `passed`: the ✓ and the restart line.
- `status: "boundary_local_only"` with exit 0 (every repo committed and clean,
  at least one with no Git remote configured) → `local_only`: no ✓, an
  restart line. For the project the SAVED cell reads “Saved on this computer
  only.”, said once and not repeated under ATTENTION; it never claims no backup
  exists. A local-only notes repo gets one attention line, “Your notes are saved
  on this computer only.”. Neither the box nor Out's words say “no remote” to the
  person unless they use git words themselves. Copy the check's `verdicts` object into the box as it reads
  (`{"project": "local_only"}`, or `{"project": "ok", "notes": "local_only"}`);
  the renderer picks the lines from it, not from `saved`. Without a complete
  `verdicts` (missing, malformed or without the project's verdict) a local-only
  save is not confirmed: no restart line, and the box names the missing
  verdicts. The renderer writes these lines, so `warnings` does not repeat them.
- Anything else (another status, a nonzero exit, a status not seen) → not ready:
  copy its `failures` list as written, or leave `boundary` absent when no
  result was seen. Failures appear under attention and the closing line asks to
  keep the session open; an absent value reads as not recorded, never as passed.

`handoff_ready` is the owner's memory-coverage assessment after the coordinated
closeout check, not something a Git push or renderer can prove: `false` or
omitted adds an attention line, and `false` also names the missing detail or
recovery action in `next`. `phase` is where the wider work stands, in the
project's own terms; write the same words into the start point's current section
as one line, `Phase: <phase>`, before the last commit, so the next arrival can
show it rather than “not recorded”. `released` is what this sitting released
("0.136.0 → 0.138.0"), or `null` for "Nothing released".

**`releases` comes from four reads, made before filling the box.** Run them
every Out; they are cheap and inside the project:

1. `git tag --list` succeeds and prints nothing;
2. no `CHANGELOG*` or release-notes file at the root;
3. no version field the project bumps (`package.json`, `pyproject.toml`,
   `plugin.json`);
4. no record (CONTEXT.md, TODO.md, the session logs) mentions a release.

`releases` is `false` only when successful reads show the project has no release
process: all four ran and found nothing; the box then has no RELEASED cell, which
a notes-only project such as a launch brief should not carry. A failed read or
any doubt leaves it `null` and the cell shows as before. With the reads not
made, pass `null`, never `false` and never a guess: the four reads come first,
and skipping them is not the same as finding nothing.
`first_out` is `true` only when a successful read found no earlier session log
in `kivna/sessions/` before this Out; the box then says once what Kerd's own
files are and that the person can ignore them. The renderer writes that line:
do not say it in `this_session` or anywhere else. Anything else is `false`; the next step appears
once, in Next time or first in Switch In will offer. `this_session` is what changed, in product language, not
the files touched. `next` is the exact next action the start point names; `why`
is the reason it comes first. `next_in` is up to two other open items the next
Switch In is likely to offer beside it, each `{"text", "why"}` in product
words, in the order Out would weigh them, and saved with the selection as
proposed, never agreed; the renderer shows two at most and counts any more,
and `null` or `[]` keeps the plain Next time. `tree` is what remains in the working tree, in
words: exactly `clean` when nothing is left; anything else is shown under attention. Files the project
keeps out of Git by decision are expected and not shown. `warnings` carries any
other problem, such as a failed role designation. `host` is `claude` or `codex`:
it chooses the closing line; only `claude` (or an unrecorded host) gets `/clear`. Use `null` or `[]` for anything Out has nothing
for; a missing field renders as "not recorded", never as a claim.

The closing line offers a restart only after a remote-verified or committed save,
`handoff_ready: true` **and** `boundary: "passed"`, or after a committed or
remote-verified save with `handoff_ready: true` and `boundary: "local_only"`: under Claude, "Run /clear, then
/kerd:switch in to pick up from here."; under Codex, "Exit and restart, then switch in to pick up from here."
Otherwise it asks to keep the session open and
resolve the save or the missing handoff first, because clearing context then
would lose the very work that is unsaved. It never says the session exited or
the context was cleared: a save is a Git fact, and restarting is the person's
action.

After the final save, if this session has an established role and the handoff is
ready, prepare the role verified by the pre-save check under the
[succession guide](../../agent/references/session-succession.md) before showing
the closing box. Do not create a role or transfer another session's role here.
Failure affects automatic pairing recovery, not the Git save verdict; name it
in `warnings`. Do not include private IDs or claim memory completeness from
routing. No session is ended by preparing its handoff.

```json
{
  "project": "Kerd",
  "branch": "main",
  "saved": "remote-verified",
  "handoff_ready": true,
  "boundary": "passed",
  "verdicts": {"project": "ok"},
  "phase": "Launch outcomes 0 of 5; sequence steps 1–2 done",
  "released": "0.136.0 → 0.138.0",
  "releases": true,
  "first_out": false,
  "this_session": [
    "The risk-rating change was accepted: launch sequence step 1 done.",
    "Conductor now checks where your work stands in your own project: step 2 done."
  ],
  "next": "Start the diagnostic pilot.",
  "why": "It is the first real work item driven in someone else's project, and the only way to see Kerd work for a real user.",
  "next_in": [
    {"text": "Try the 0.134.0 diagram rules on a real diagram.", "why": "They have never been exercised."},
    {"text": "You: decide whether the \"prove Kerd first\" hold is lifted.", "why": "Two launch steps wait on it."}
  ],
  "tree": "clean",
  "warnings": [],
  "host": "claude"
}
```

If the renderer cannot run, say the same things as plain text.

## Default verified save when pushing is authorized

For an authorized commit-and-push Out, use `handoff.py save ... --push` by default.
Its successful remote check is the evidence for saying the save reached GitHub;
an attempted push or stale local tracking ref is not. Local-only Out remains a
valid choice and does not require GitHub access or new push permission.

If the helper cannot support the agreed workflow, explain the limitation. A
manual route must retain explicit file selection, existing-index protection and
verification that the intended remote branch contains the exact saved tip before
claiming remote success. Report use of that fallback. Do not sweep unrelated
changes into a commit or replace an unsafe checkout to make the helper pass.

Resolve `scripts/handoff.py` from the skill directory. Example shapes, not literal
commands to run against a guessed project/branch:

```sh
python3 /path/to/switch/scripts/handoff.py --project /path/to/project save \
  --branch trial-branch --file CONTEXT.md --file TODO.md \
  --file path/to/session-log.md --message "Save the working place" --push
python3 /path/to/switch/scripts/handoff.py --project /path/to/project pickup \
  --branch trial-branch --record CONTEXT.md --sync
python3 /path/to/switch/scripts/handoff.py --project /path/to/project prepare \
  --branch trial-branch --record CONTEXT.md --section TODO.md '## Now'
python3 /path/to/switch/scripts/handoff.py --project /path/to/project boundary \
  --preserve scratch.patch
```

List actual changed files, including any archive files; the helper refuses unassigned
changes or an existing staged index. It won't check out a different branch for you.
The loaded record is only the entrypoint: follow its relevant context links and
verify the next action. It is not a parser-based declaration of complete memory.

`prepare` is an optional caller convenience: it returns local Git identity and
raw, source-labelled records together for a fresh reader. Repeat `--file` for
complete files or `--section FILE '## Exact heading'` for complete Markdown ATX
sections, including child sections. Prepared sources must be Git-tracked UTF-8
text; their line endings are preserved. Missing, empty or ambiguous selections fail;
it does not guess replacements. Conductor chooses from the project's actual
memory structure. The helper does not select relevant sources, write a second
memory file, start a session or grant permission. Without `--sync` it is local-only.
