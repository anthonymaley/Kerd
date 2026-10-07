# Codex package distribution

Kerd's four-skill core is distributed through the repository's generated
`codex` branch. Claude's full plugin remains on `main`.

## Install once

Run these in your terminal, not at Codex's chat prompt:

```sh
codex plugin marketplace add anthonymaley/Kerd --ref codex
codex plugin add kerd@kerd-core
```

This installs Conductor, Switch, Visuals and Agent at user level. Tend,
Slainte, Kivna, Skriv and Claude hooks are not included. Claude's full plugin is
unchanged. No source checkout, Python build, or Markdown handoff is needed to
install or update; the bundled helpers still require their usual runtime setup.

## Update (after initial registration)

```sh
codex plugin marketplace upgrade kerd-core && codex plugin add kerd@kerd-core
```

The first command refreshes the Git source; the second explicitly installs Kerd
from it. Both are scoped to `kerd-core`, not every marketplace or plugin.
Confirm the installed version and enabled state:

```sh
codex plugin list --marketplace kerd-core
```

Start a fresh Codex session in your work project and ask “Switch in.” Its heading
names the Kerd version it read. An install listing proves installation, not that
an existing conversation has loaded the new skill text. These commands were
tested with Codex CLI 0.161.0 using an isolated profile and a loopback Git
marketplace with two fixture releases. A public install listing alone is not
an end-to-end test of every skill. This is repository distribution, not a listing in the
universal Plugins Directory.

## Move an existing local-build installation

First inspect `codex plugin marketplace list`. If `kerd-core` points at an
`output/kerd-codex-...` directory, upgrading that local source cannot download a
new release. With approval to change that user-level registration:

```sh
codex plugin marketplace remove kerd-core
codex plugin marketplace add anthonymaley/Kerd --ref codex
codex plugin add kerd@kerd-core
codex plugin list --marketplace kerd-core
```

Keep the old build until the new installation is verified. Removing the
registration does not delete its source directory. If the new registration
fails, re-add the old absolute catalog path and reinstall `kerd@kerd-core`.
Do not replace another source silently.

## Maintainer: prepare and publish a release

The `codex` branch is generated output, never a second maintained skill tree.
The source remains `main`'s four selected skill directories and `agents/`.
Only committed source is packaged; uncommitted changes and local work notes
are not included. Each publication records its source commit in `release.json`.

Prepare from an exact release commit, using a fresh destination:

```sh
python3 tools/codex_release.py output/kerd-codex-check-VERSION --ref RELEASE_COMMIT
```

Inspect and test that artifact, obtain the required independent review and
publication go, then use a different fresh destination to publish:

```sh
python3 tools/codex_release.py output/kerd-codex-publish-VERSION --ref RELEASE_COMMIT --publish
```

Replace `VERSION` and `RELEASE_COMMIT`; do not type them literally. The second
command writes only the generated `codex` branch on `origin`. It neither pushes
`main` nor changes the source checkout, index, user configuration or installation.
It appends history without force-pushing and refuses unchanged releases,
same-version changes, unrelated prior branches and source-history rollbacks.
Old output directories are never overwritten. Repeat this publication for each
new core release: it is not automatic CI, and Claude publication alone does not
update Codex. Use a new release version for changed package contents.

After publication, verify installation from GitHub in an isolated profile and
read back its version, enabled state and cached package contents. Keep fixture
update evidence separate from a real user's fresh-session load check.

Sources: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
and [Codex plugin commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin-marketplace).
