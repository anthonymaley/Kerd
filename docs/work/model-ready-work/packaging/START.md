# Kerd candidate

Three skills, one working record. No Kerd CI, custom hooks or extra diagram
installation is required. This is a controlled-adoption candidate, not the
replacement for every existing Kerd project.

```text
Your idea → Conductor: understand and agree → build ↔ check → ready to use
                 Visuals: make the direction and work clear
                 Switch: preserve the place between sessions
```

## Try it in Claude, for one session

Open a terminal in the project where the work belongs. Start a fresh session:

```sh
claude --plugin-dir /absolute/path/to/kerd
```

Use this extracted package's actual path. In `/help`, check for
`/kerd:conductor`, `/kerd:switch` and `/kerd:visuals`. Then describe real work,
for example “Help me prepare a proposal for …”. If automatic selection misses,
invoke `/kerd:conductor` explicitly and keep that miss as trial feedback.

The same-name local plugin takes precedence over an installed marketplace Kerd
for this session, except managed policy. Closing this new session and launching
normally restores the ordinary setup; this command does not install or disable
plugins globally. [Claude's documented local-plugin route](https://code.claude.com/docs/en/plugins#test-your-plugins-locally).

This does **not** isolate other plugins, global instructions or project memory.
Before substantial work, check for competing brainstorming/pair instructions and
the saved work's actual direction. Do not pretend this README overrides them.
If a configuration change is needed, explain its exact scope and obtain approval;
do not disable unrelated projects' tools. Do not use `--bare` as an isolation
shortcut: it changes authentication and context behavior too.

## Use it in Codex without installing

In the target project's session, ask:

```text
Read /absolute/path/to/kerd/skills/conductor/SKILL.md and use that
candidate for this project. Begin or continue the saved work.
```

This is explicit loading, **not registered automatic skill discovery** or proof
of environment isolation. Replace the path with the actual package location.
Host instructions still apply. A Codex plugin manifest is included for later
approved installation, but no session-only plugin flag was established in the
checked CLI. Do not substitute a global install without agreement.
[Official packaging guidance](https://developers.openai.com/plugins/build/plugins).

## What happens next

Conductor reuses your description and relevant files, proposes missing details,
and asks only consequential questions. It shows the direction and success checks
before substantial work, then continues within the agreed permissions.
You can ask Claude or Codex for a review. Setup checks only the provider needed;
missing tools require approved setup and you complete account sign-in. Existing
account charges apply. Model and effort choice uses local guidance, task needs
and evidence, not a cheapest-model rule.

Switch handles In, Out and To. Roll continues owned build workers in fresh
context; it does not replace an arbitrary open terminal. Git saves and external
actions require the agreed authority. Completion is not automatic publication.

Keep the `skills/` tree intact, including Conductor's `references/guidance/`.
References load when needed, not as one
large startup prompt. The bundle includes local regression tests and a short
task-evidence summary; development histories, private sessions and optional
upstream diagram tools are not included. Do not edit this generated copy as a
second source: update the development pack and prepare a fresh bundle.
