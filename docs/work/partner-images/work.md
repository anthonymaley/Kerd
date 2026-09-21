# Work: a Codex partner can be shown what the person is looking at

## Direction

Reported 2026-09-21 by a Kerd user other than Anthony, relayed with a screenshot of
their session (not committed: it is a third party's session). The user asked Claude to show some mockup images to Codex and ask for its
thoughts. Claude loaded Agent, found that "the Kerd helper can't attach images", and sent
them through `codex exec -i` instead, "as a bounded read-only worker — disclosing that
fallback rather than pretending the usual route carried it."

The disclosure was right. The outcome was not what the user asked for: the images went
to a **fresh worker with no project context**, not to their established Codex partner.
Agent's own rule is never to substitute a fresh reviewer for a named partner silently;
this was not silent, but it was a substitution the user did not choose.

## Findings (2026-09-21, checked against the code, not the screenshot)

- **Confirmed: the partner route is text only.** `agent.py ask` accepts `--alias`,
  `--prompt-file`, `--role`, `--request-id` and nothing else. It builds
  `codex queue --cd <root> --thread <sid> --message <framed>` (`agent.py:1162`).
- **No guidance exists.** No Agent or Conductor reference mentions images, screenshots or
  attachments for a partner. The fallback in the report was the model improvising.
- **Uncertain: whether Codex's own route can carry an image to an existing thread.**
  `codex queue --help` (codex-cli 0.154.0) lists `-i, --image <FILE>...`, but its text,
  "Optional image(s) to attach to the initial prompt", is identical to the top-level
  `codex --help` entry. It reads like a TUI-start option inherited by the subcommand,
  not one that attaches to a queued message. Not tested.

## The test (2026-09-21 11:30, authorized by Anthony)

A throwaway Codex terminal session was started in a detached tmux window, in an empty
temp folder, and given one typed setup message so it had a thread ID (`01a0c497…`,
distinct from the `codex-tui` partner `01a069ec…`). Everything after that went through
`codex queue --cd … --thread …`, the exact route Kerd's `ask` uses for a Codex partner.
Test images were synthetic, so nothing of the reporting user's went to OpenAI.

- **Attaching the image is refused by Codex itself.** `codex queue … -i probe.png` →
  `Error: codex queue does not support image attachments`. The `-i` in its help is
  inherited from the top-level command. No Kerd flag can carry an image this way.
- **Sending the path as text works.** Asked to open `probe.png` by absolute path, the
  partner ran its own viewer (`Viewed Image └ probe.png`) and answered "OKAPI 73; a red
  circle." — content it could only know by seeing it.
- **It works outside the partner's working folder too**, the realistic case for a
  person's mockups: a second image in a different directory → `Viewed Image`, "HERON 58;
  a blue square." Both correct.

Scope of the evidence: one model (`gpt-5.6-sol` at high), codex-cli 0.154.0, two images,
default sandbox. A Claude partner receiving an image path is untested.

Side effect: accepting Codex's trust prompt for the temp folder wrote
`[projects."/private/tmp/codex-img-probe.kykwaJ"] trust_level = "trusted"` into
`~/.codex/config.toml` (line 196). Left in place; Anthony's config is not edited without
his word. The throwaway session is left idle in tmux session `codexprobe`, as promised.

## Risks to keep in view

- A probe could land in Anthony's own Codex TUI partner, `codex-tui`. **Closed:** the
  probe used a separate throwaway thread; the partner was not contacted.

## Now

Stage: Complete, 2026-09-21
Pending question: none.
Next action: none inside this work. Released as 0.143.0, commit `1c383b9`, pushed on
Anthony's "y" (12:07); remote verified; CI green; the live marketplace manifest reads
0.143.0 with the HTTPS source. Still unproved: a Claude partner receiving an image path,
and a real user's session following the new rule — only the wording is guarded.

## Delivered

Anthony said yes, 2026-09-21 11:54. The fix is guidance, not code: `ask` already carries
text, and the model in the report improvised only because nothing told it the path
route exists.

- `skills/agent/SKILL.md` step 4: show a partner an image by absolute path; never attach;
  a fresh worker only when the person chooses. Trigger description gains "show Codex this
  screenshot".
- `skills/agent/references/native-sessions.md` `## Images`: the evidence and its limits.
- `docs/guide/agent.md`: one paragraph for the user.
- `skills/agent/scripts/tests/test_partner_images.py`: guards the wording and position.
  Fails against the old text (5 failures, 1 error), passes on the new.
- 0.143.0 in all three version fields; identical README and CHANGELOG entries.
- Release check clean; 760 tests pass.
- **Codex, before-push: clear on the first read.** No overstatement found; MINOR agreed
  as right for changed documented behaviour with no code change.
