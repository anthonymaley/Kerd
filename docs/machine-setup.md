# Machine Setup

What a development machine needs to run Kerd and the Kerd workflow, and the
checklist for moving to a new one.

**Living document — no date in the filename, rewritten in place.** It records
what is *currently* required, never what was required on some past move.

**Every row carries the command that proves it.** A setup list written as prose
is a declared contract that nothing checks — this repo's recurring defect class
(three instances found on 2026-08-27 alone). Run the commands; do not read the
list and believe it.

---

## 1. Prerequisites

Run this block. Every line must print a version, not `MISSING`.

```bash
for c in python3 git gh; do
  printf "%-8s " "$c"; command -v $c >/dev/null && $c --version 2>&1 | head -1 || echo "MISSING"
done
```

| Tool | Why Kerd needs it | Verified on the 2026-08-27 move |
|---|---|---|
| `python3` | Every gate, render and check is Python: `tools/gates/`, `tools/diagram/`, `tools/design/`. Stdlib only — **no pip install, no venv, no PyYAML.** | 3.14.6 |
| `git` | Switch owns `git pull` and the session-state commit; the progress board derives position from `git log`. | 2.50.1 (Apple Git) |
| `gh` | CI status and any PR flow — the gate records' `CI green headSha-verified` claim reads the Actions API. Not needed for the switch boundary itself. | 2.97.0, authenticated after `gh auth login` |

**Python is a stdlib-only dependency and that is deliberate** (2026-08-08
decision, CONTEXT.md): `/usr/bin/python3` is the same `xcode-select` shim inode
as `/usr/bin/git`, so requiring an interpreter is implied by the thing Kerd
already requires. Nothing to install if Xcode command line tools are present.

`node`/`npm` are **not** Kerd requirements — they belong to sibling repos.

---

## 2. Repository and identity

```bash
git config user.name && git config user.email      # Anthony Maley / tony@maley.be
git remote -v                                       # git@github.com:anthonymaley/Kerd.git
ssh -T git@github.com                               # "Hi anthonymaley! ..."
```

The remote is **SSH, not HTTPS**. An SSH key must be present and loaded on the
new machine or `git pull` at switch-in fails before anything else runs. A
successful `ssh -T` is the proof; a green `git pull` on an already-current tree
is **not** — it can succeed from cache.

```bash
gh auth login          # interactive — must be run by the user, not by a session
```

**An SSH key does not authenticate `gh`.** They are different doors: the key
signs *git* transport (clone, pull, push), while `gh` is a REST/GraphQL client
needing its own OAuth token. A machine can have working `git push` and a `gh`
with no config at all — which is exactly what this move produced. At the login
prompt choose GitHub.com → SSH → the existing key → browser login; that reuses
the key for git and mints the API token beside it. Verify with a call that
actually hits the API, not with `--version`:

```bash
gh auth status                                   # names the account and token scopes
gh run list --limit 3 --json headSha,conclusion   # proves the Actions API answers
```

---

## 3. Claude Code plugin state

Kerd is a plugin, so the skills and hooks come from the **plugin cache**, not
from this working tree.

```bash
# is the plugin enabled?
python3 -c "import json;d=json.load(open('$HOME/.claude/settings.json'));print(d['enabledPlugins'].get('kerd@kerd-marketplace'))"
# which version is cached?
ls ~/.claude/plugins/cache/kerd-marketplace/kerd/
# does that match the repo?
python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['version'])"
```

**The cache version and the repo version should match.** When they diverge, the
session is running *older skill text* than the repo contains — the standing
"plugin cache repin debt" row in TODO. Hooks are unaffected: since v0.96.0 they
auto-load and resolve `${CLAUDE_PLUGIN_ROOT}` at runtime, so they do not rot
with the cache version.

### Hooks must NOT be wired by hand — anywhere

Since v0.96.0 the plugin's own `hooks/hooks.json` registers all three hooks
(`session-start.sh`, `pair.sh`, `skill-complete.sh`) automatically when the
plugin is enabled. **A repo or a user-global settings file that also wires them
double-fires every hook.** The dev-repo exception was dropped deliberately —
no repo wires manually, including Kerd itself.

```bash
# must print nothing:
grep -l 'kivna/.pair\|kerd' ~/.claude/settings.json .claude/settings.local.json 2>/dev/null
for d in ~/development/product/*/; do grep -l kerd "$d.claude/settings.local.json" 2>/dev/null; done
```

Proof the auto-load actually fired: a fresh session prints
`📋 Last session: <date>` — a string built only by `hooks/session-start.sh`.
(Note the source literal is lowercase; grepping for the rendered capitalised
string returns nothing and reads as "the hook didn't fire".)

The **statusline** slot is not Kerd's by default and does not need claiming —
Kerd's statusline composes with an occupied slot rather than taking it.

---

## 4. Machine-local state that does NOT travel with git

This is the part a move actually loses. Each of these is gitignored or lives
outside the repo, so a fresh clone has none of it.

| State | Where | Consequence of losing it | Recovery |
|---|---|---|---|
| **pair mode** | `kivna/.pair` in each repo — gitignored | Partner mode silently off; sessions revert to working alone and dumping | `/kerd:pair on` per repo. CONTEXT.md `## Active Mode` records which repos should have it |
| **conductor mode marker** | `kivna/.active-modes` — gitignored | An open conductor session cannot resume; its `execute` stamp (the sitting's open time) is gone | CONTEXT.md `## Active Mode` snapshot, written by switch-out for exactly this case |
| **`~/.claude/settings.json`** | user-global | Enabled plugins, permissions, model and effort defaults | Not in any repo. Back it up before a move, or re-enable plugins by hand |
| **`AGENTS.md`** | gitignored, per repo | Stale Codex-era fork; needs its own verdict | Not worth restoring |
| **the vault** | `~/eolas` → `~/development/home/eolas` | `/kerd:kivna save` has nowhere to write | Clone `eolas` and recreate the symlink (below) |

### The vault symlink

Every repo's `kivna/vault.json` points at `~/eolas/vault` (the one exception:
`klar` points at `~/ObsidianLLM`). On this machine `~/eolas` is a **symlink**
into the dev tree:

```bash
ln -s ~/development/home/eolas ~/eolas
ls -d ~/eolas/vault                    # must resolve
```

Without the symlink every `kivna/vault.json` in every repo resolves to nothing.
The vault is opt-in since v0.83.0 — nothing reads or writes it at the session
boundary — so a missing vault does not break switch. It breaks
`/kerd:kivna save` only.

---

## 5. The move checklist

In order. Each step's verify is the command beside it.

1. **Install Xcode command line tools** → `git --version` and `python3 --version` both print.
2. **Restore or create the SSH key** → `ssh -T git@github.com` greets you by name.
3. **Set git identity** → `git config --global user.name` / `user.email` print.
4. **Clone the repos** into `~/development/product/` (and `~/development/home/` for `eolas`) → `git status -sb` in each shows a tracking branch.
5. **Create the vault symlink** → `ls -d ~/eolas/vault` resolves.
6. **Install `gh` and authenticate** → `gh auth status` shows a logged-in host.
7. **Enable the Kerd plugin in Claude Code** → `enabledPlugins["kerd@kerd-marketplace"]` is `true` and the cache directory exists.
8. **Strip any hand-wired Kerd hooks** from `~/.claude/settings.json` and every `.claude/settings.local.json` → the grep in §3 prints nothing.
9. **Start a fresh session** → the banner shows `📋 Last session: <date>`, proving auto-load fired.
10. **Restore per-repo pair state** from CONTEXT.md `## Active Mode` → `/kerd:pair on` where it belongs.
11. **Run the smoke tests** → all three green:
    ```bash
    python3 tools/gates/gate.py selftest      # root resolution: 7 · selftest: 49
    bash tests/hooks_test.sh                  # Passed: 21  Failed: 0
    python3 tools/diagram/progress.py stale   # "render current"
    ```
12. **`/kerd:switch in`** → the boundary reads CONTEXT.md, TODO.md and the newest session log.

---

## Gotchas found while doing this

- **A green `git pull` is not proof the remote is reachable.** On an already-current
  tree it can return `Already up to date.` from local state. `ssh -T git@github.com`
  is the real test.
- **`progress.py` has no `check` subcommand** — it is `stale`. And running the
  renderer bare *rewrites the committed trio*, dirtying the tree; `stale` is the
  read-only form.
- **`hostname` is the only thing in the session log that records which machine
  ran the session.** It is written into the log header at switch-out, so a
  machine move is visible in the record only if you read that line.
