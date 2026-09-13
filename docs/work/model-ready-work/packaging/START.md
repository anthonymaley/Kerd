# Kerd core package

Four skills from one maintained source: **Conductor** guides the work,
**Switch** restores and saves its place, **Visuals** makes it understandable,
and **Agent** connects Claude and Codex. No Kerd CI or custom hook is required
in a consumer project. The generated version comes from the source release.

The full Claude marketplace plugin still contains twelve skills. This core
artifact contains four: the other eight legacy skills and all Claude hooks are
deliberately excluded, not claimed compatible with Codex. Don't replace the full
Claude install with this smaller package unless that is what you intend.

## Build from the source checkout

Run in the Kerd source repository. The destination must not already exist:

```sh
python3 docs/work/model-ready-work/packaging/build.py output/kerd-codex-0.113.0 --codex-marketplace
```

This creates a catalog root with `.agents/plugins/marketplace.json` and
`plugins/kerd/.codex-plugin/plugin.json`. It copies only the four selected skill
trees, their references/scripts/tests, this guide and the license. It does not
register a marketplace, install a plugin, change settings, launch models or
contact a provider. Build output is disposable; edit the source, not the copy.
Never point Codex at the full source `skills/` directory as a substitute: that
would expose the unverified legacy skills too.

## Install in Codex

After approving user-level installation, use the actual absolute path to the
generated **catalog root**, not its `plugins/kerd` subdirectory:

```sh
codex plugin marketplace add /absolute/path/to/kerd-codex-0.113.0
codex plugin list --marketplace kerd-core --available --json
codex plugin add kerd@kerd-core
```

If `kerd-core` already names a different source, inspect and resolve that choice
first; do not silently replace it. These commands register a local catalog and
install into this user's Codex configuration/cache. They are not project-only
or a session-only trial, and do not change Claude's installation.

Start a new Codex session **in your work project**, not in the Kerd package.
Open `/plugins` in the CLI (or Plugins in the app), check Kerd's installed
version, and confirm Conductor, Switch, Visuals and Agent appear. Use the host's
skill picker to choose Kerd's Switch and ask **"Switch in."** You can also ask:

- "Use Kerd Switch to restore this project. Don't start work yet."
- "Use Kerd Conductor to help me build …"
- "Use Kerd Visuals to show the proposed design."
- "Use Kerd Agent to ask our Claude partner to review this. Read-only."
- "Use Kerd Switch to save this sitting within the existing Git permissions."

`/kerd:switch` and similar spellings in the shared guides are Claude commands,
not a promise of identical Codex slash commands. Use the installed Kerd skill
entry; if automatic selection misses, select it explicitly and record that miss.
Report a missing skill rather than claiming Kerd loaded. Startup alone is not
evidence of installation or update.

## Updates and removal

Claude updates do not update Codex. Build each new release into a fresh catalog
directory. Check `codex plugin marketplace list` for the registered local source.
To change the `kerd-core` source path, with approval, run
`codex plugin marketplace remove kerd-core`, then add the new catalog root and
run `codex plugin add kerd@kerd-core`. Start a new session and check the installed
version. Keep the previous catalog until the replacement is verified; removing
a catalog registration is not deletion of its source files.

For same-version development iterations, use Codex's `plugin-creator` update
workflow to refresh the generated manifest's cachebuster and reinstall from the
confirmed local catalog. Do not maintain a second edited skill tree in the cache.
`marketplace upgrade` refreshes Git catalogs, not this local build's contents.
To uninstall, use `codex plugin remove kerd@kerd-core`; remove the catalog
registration separately if no longer wanted. Don't assume a lower version is
automatically picked up as a rollback.

## Runtime setup and host boundaries

Use Python 3.10+ and Git on macOS/Linux for the bundled helpers. Model jobs and
pairing require the relevant provider's installed CLI and your own sign-in.
Nothing installs dependencies or asks for credentials in chat. Agent's Codex
shared-server route needs its optional WebSocket dependency; see the setup
section of the packaged `skills/agent/references/native-sessions.md`
for an approved private virtual environment. Use that environment's Python
when invoking Agent. The Claude route uses the standard library.

A Codex-native subagent is not a Claude session. Use Agent for an existing
Claude partner; choose a fresh cross-provider worker explicitly. An alias does
not grant inbound trust. A held message needs the recipient's real approval;
"submitted" is not "reply received". Never kill or resume another person's
occupied session to make pairing work. Help is in the packaged
`skills/agent/references/user-guide.md`.

The skills do not override host permissions, project instructions or other
plugins. Use native task controls only when actually exposed; otherwise show the
compact progress fallback. Only claim colors or clickable controls the client
supports. Switch Out saves memory, not the native conversation: start fresh
context separately using your client's controls, then run Switch In.

## Check the experience

In an isolated project first: confirm discovery of exactly four core skills;
In restores status and stops at its actual decision; an approved small task runs
under Conductor with visible progress; Visuals produces a real artifact; Agent
retrieves an identified partner's reply; Out saves a bounded reading set and
shows the truthful completion state; a new session restores that place. Don't
claim this whole journey from package validation or helper tests alone.

For one-session explicit loading without installation, ask the model to read
`/absolute/package/path/skills/switch/SKILL.md` and run In for the current project.
That is not registered discovery. In Claude, the core package can be tried with
`claude --plugin-dir /absolute/package/path` and `/kerd:switch in`; other plugins
and global/project instructions still apply.

Sources: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Codex plugin use](https://learn.chatgpt.com/docs/plugins), and the installed
`codex plugin ... --help` command surfaces checked during development. Behavior
and availability can differ by client/version; verify the actual installed entry.
