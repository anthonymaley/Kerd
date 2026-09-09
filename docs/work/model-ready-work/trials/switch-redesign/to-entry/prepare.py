#!/usr/bin/env python3
"""Prepare bounded skill-behavior fixtures; no live session/device is represented."""
import argparse
import json
from pathlib import Path
import subprocess


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE).strip()


def init(folder, name):
    root = folder / name
    git(folder, "init", "-q", "-b", "entry-trial", str(root))
    for key, value in (("user.name", "Isolated Entry Trial"), ("user.email", "trial@example.invalid"),
                       ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
        git(root, "config", key, value)
    (root / "work.md").write_text("# Workshop package\n\nOutcome: a useful workshop agenda and speaker notes.\n"
        "Stage: active drafting. Agenda outline exists in draft.md.\n"
        "Next action: write speaker notes against the existing agenda.\n"
        "Success: agenda covers the three agreed topics; notes explain each topic.\n"
        "Authority: edit draft.md and this work record. No external publishing or sending.\n"
        "No unresolved jobs, pending user questions or declared resource caps.\n")
    (root / "draft.md").write_text("# Agenda\n1. Current problem\n2. Options\n3. Next decision\n")
    git(root, "add", "--", "work.md", "draft.md")
    git(root, "commit", "-qm", "Initial workshop work")
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True)
    folder = Path(parser.parse_args().folder).resolve()
    if not folder.is_dir() or any(folder.iterdir()):
        raise ValueError("Supply a fresh empty disposable directory")
    console = init(folder, "console")
    (console / "draft.md").write_text((console / "draft.md").read_text() + "\nLocal unsaved thought: allow questions.\n")
    interactive = init(folder, "interactive")
    remote = folder / "interactive-remote.git"
    git(folder, "init", "--bare", "-q", str(remote))
    git(interactive, "remote", "add", "origin", str(remote))
    git(interactive, "push", "-qu", "origin", "entry-trial")
    (interactive / "draft.md").write_text((interactive / "draft.md").read_text() + "\nOpening: establish the decision to make.\n")
    source = init(folder, "revision-source")
    revision_remote = folder / "revision-remote.git"
    git(folder, "init", "--bare", "-q", str(revision_remote))
    git(source, "remote", "add", "origin", str(revision_remote))
    git(source, "push", "-qu", "origin", "entry-trial")
    dest = folder / "revision-destination"
    git(folder, "clone", "-q", "--branch", "entry-trial", str(revision_remote), str(dest))
    saved = git(source, "rev-parse", "HEAD")
    (source / "work.md").write_text((source / "work.md").read_text() + "\nLater proposal: change to a two-day event; not yet agreed.\n")
    git(source, "add", "work.md")
    git(source, "commit", "-qm", "Later proposal")
    git(source, "push", "-q", "origin", "entry-trial")
    manifest = dict(console=str(console), interactive=str(interactive), destination=str(dest),
        saved_revision=saved, current_remote=git(source, "rev-parse", "HEAD"),
        console_before=git(console, "rev-parse", "HEAD"), interactive_before=git(interactive, "rev-parse", "HEAD"))
    (folder / "setup.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
