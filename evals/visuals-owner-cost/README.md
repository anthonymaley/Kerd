# visuals-owner-cost

Measures whether Kerd 0.160.0's Visuals rule (skills/visuals/SKILL.md, from 0.134.0)
makes a proposal diagram show **who owns the gap** and **what it costs**, per the
prose invariant: "stripped of those references it must still show what the person
can and cannot do today, where the responsibility sits, what changes, and any
material cost or boundary that exists."

## Route: manual `claude -p`, not `claude plugin eval`

`kerd:visuals` requires a companion plugin (diagram-design or Archify) to render.
`claude plugin eval`'s sandbox loads **only the single target plugin** — confirmed
against `claude plugin eval --help` ("It loads the plugin and runs its eval suite
... on your machine, as you") and https://code.claude.com/docs/en/plugin-evals.md
("Claude Code starts a fresh, isolated non-interactive session with only your
plugin loaded ... other installed plugins ... are absent"). There is no flag or
manifest field to add a second plugin to that sandbox. So a `kerd` eval target
never has diagram-design or Archify available, and `kerd:visuals` cannot render —
this route is not usable for this skill.

Route used instead: a fresh scratch copy of `scaffold.sh`'s scenario per run, then

```
claude -p "/kerd:visuals Draw the proposal view for fixing the invoice export, from notes.md. Save it in this folder." \
  --model opus --effort medium \
  --output-format stream-json --verbose \
  --permission-mode acceptEdits \
  --allowedTools "Read Write Edit Glob Grep Skill Bash" \
  --add-dir <scratch run dir>
```

run from inside each scratch run dir, with the user's normal plugin set loaded
(kerd 0.160.0 + diagram-design 2.6.6 confirmed present in every run's `init`
event; Archify is a `~/.agents/skills/archify` skills-dir skill, also available).
No `timeout`/`gtimeout` binary on this host — each run was launched with `nohup
... &` and polled for its PID to exit rather than wrapped in `timeout`.

## Files

- `scaffold.sh` — writes the invoice-export `notes.md` scenario (owner: billing
  team / Priya; cost: half a day + one release + a one-time template update).
- `prompt.md` — the `/kerd:visuals` prompt, in the same frontmatter shape as
  `evals/question-shape/prompt.md`, for whoever reruns this manually or wires it
  into a future eval-dir mechanism.
- `scenario-b/` — same repo shape (a `git init`'d `acme-billing/` with a
  `# Acme Billing` README so a project name exists), but owner and cost are only
  *implied* in `notes.md` and the run goes through `/kerd:conductor` (not a
  direct `/kerd:visuals` prompt) to test whether Conductor's proposal view still
  surfaces them.

Rerun by copying `scaffold.sh`'s heredoc into a scratch dir, then running the
`claude -p` command above from inside it, 3+ times for a stable read.
