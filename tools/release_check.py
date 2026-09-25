#!/usr/bin/env python3
"""Standalone release-rules check: version sync across the three manifest
locations, capability-list identity between the two manifests, the
`kerd:` slash-command namespace rule, release-history parity between
README.md and CHANGELOG.md, and README's "What's New" header version.

    python3 tools/release_check.py [--root PATH] [--json]
    python3 tools/release_check.py selftest

Exit 0 with `release: clean` when nothing is wrong, or exit 1 printing one
`problem: ...` line per issue followed by `release: N problem(s)`. `--json`
prints the problems list as JSON (same exit codes). `selftest` runs this
file's own fixture cases in temporary directories and prints
`selftest: N ok` (exit 0) or the failures (exit 1).

This file is deliberately self-contained: no import of `kit` or `gate`, so
it keeps working after `tools/gates/` is deleted. It ports
`release_audit`, `_release_files`, `_release_versions`, `_release_capability`
and `_release_namespace` from `tools/gates/kit.py` unchanged in behaviour.

Root resolution: `--root PATH`, else the Git top level of the current
directory (via `git rev-parse --show-toplevel`), else the current
directory. This is a narrower rule than the ladder's gate.py (no
$CLAUDE_PROJECT_DIR, no "looks like a project" refusal) — this check has
one job and no session machinery to defer to.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile


# ── root resolution ─────────────────────────────────────────────────────

def _pop_root(argv):
    """Take `--root PATH` or `--root=PATH` out of argv and resolve it.

    Returns (root, remaining_argv). Resolution order: --root, else the Git
    top level of the current directory, else the current directory."""
    rest, explicit = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--root":
            if i + 1 >= len(argv):
                raise SystemExit("--root needs a path: --root /path/to/project")
            explicit = argv[i + 1]
            i += 2
            continue
        if a.startswith("--root="):
            explicit = a.split("=", 1)[1]
            if not explicit:
                raise SystemExit("--root needs a path: --root /path/to/project")
            i += 1
            continue
        rest.append(a)
        i += 1

    if explicit is not None:
        root = os.path.abspath(os.path.expanduser(explicit))
    else:
        root = _git_top_level(os.getcwd())
        if root is None:
            root = os.getcwd()
    return root, rest


def _git_top_level(start):
    """The Git top level of `start`, or None when it is not inside a repo."""
    try:
        out = subprocess.run(
            ["git", "-C", start, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    if out.returncode != 0:
        return None
    top = out.stdout.strip()
    return top or None


# ── release rules (R1–R3), ported unchanged from tools/gates/kit.py ────

def _release_files(root):
    """Load .claude-plugin/plugin.json and .claude-plugin/marketplace.json.
    Returns (plugin, marketplace, problems). When NEITHER file exists:
    (None, None, []) — vacuous pass, a tree without plugin metadata is not
    in violation. Otherwise each path that is absent or fails json.load
    contributes the problem '<relpath> — missing or invalid JSON' and
    loads as None."""
    rel_plugin = ".claude-plugin/plugin.json"
    rel_marketplace = ".claude-plugin/marketplace.json"
    abs_plugin = os.path.join(root, ".claude-plugin", "plugin.json")
    abs_marketplace = os.path.join(root, ".claude-plugin", "marketplace.json")

    if not os.path.isfile(abs_plugin) and not os.path.isfile(abs_marketplace):
        return None, None, []

    problems = []
    docs = []
    for rel, path in ((rel_plugin, abs_plugin), (rel_marketplace, abs_marketplace)):
        doc = None
        if not os.path.isfile(path):
            problems.append(f"{rel} — missing or invalid JSON")
        else:
            try:
                with open(path, encoding="utf-8") as f:
                    doc = json.load(f)
            except ValueError:
                problems.append(f"{rel} — missing or invalid JSON")
                doc = None
        docs.append(doc)

    return docs[0], docs[1], problems


def _release_versions(plugin, marketplace):
    """R1 — the three version fields must be identical: plugin['version'],
    marketplace['metadata']['version'], marketplace['plugins'][0]['version'].
    A None document contributes nothing (its load problem is already
    reported). Missing/non-string field → one problem naming it. All three
    present but not all equal → ONE problem showing all three values."""
    problems = []
    vals = {}

    if plugin is not None:
        v = plugin.get("version")
        if isinstance(v, str):
            vals["plugin"] = v
        else:
            problems.append(".claude-plugin/plugin.json — 'version' missing")

    if marketplace is not None:
        metadata = marketplace.get("metadata") or {}
        mv = metadata.get("version")
        if isinstance(mv, str):
            vals["metadata"] = mv
        else:
            problems.append(".claude-plugin/marketplace.json — 'metadata.version' missing")

        plugins = marketplace.get("plugins")
        pv = None
        if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
            pv = plugins[0].get("version")
        if isinstance(pv, str):
            vals["plugins0"] = pv
        else:
            problems.append(".claude-plugin/marketplace.json — 'plugins[0].version' missing")

    if len(vals) == 3 and not (vals["plugin"] == vals["metadata"] == vals["plugins0"]):
        problems.append(
            "version drift — plugin.json='{}' metadata.version='{}' plugins[0].version='{}' "
            "(all three must match)".format(vals["plugin"], vals["metadata"], vals["plugins0"])
        )

    return problems


def _release_capability(plugin, marketplace):
    """R2 — plugin['description'] must be byte-identical to
    marketplace['plugins'][0]['description']. metadata.description is
    NEVER read — it is intentionally a different shape (marketplace
    one-liner), and checking it would homogenize what CLAUDE.md says to
    keep distinct."""
    problems = []
    plugin_desc = None
    plugins0_desc = None

    if plugin is not None:
        d = plugin.get("description")
        if isinstance(d, str):
            plugin_desc = d
        else:
            problems.append(".claude-plugin/plugin.json — 'description' missing")

    if marketplace is not None:
        plugins = marketplace.get("plugins")
        d = None
        if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
            d = plugins[0].get("description")
        if isinstance(d, str):
            plugins0_desc = d
        else:
            problems.append(".claude-plugin/marketplace.json — 'plugins[0].description' missing")

    if plugin_desc is not None and plugins0_desc is not None and plugin_desc != plugins0_desc:
        i = 0
        min_len = min(len(plugin_desc), len(plugins0_desc))
        while i < min_len and plugin_desc[i] == plugins0_desc[i]:
            i += 1
        problems.append(
            f"capability-list drift — plugin.json description != plugins[0].description "
            f"(first differs at char {i}; metadata.description is exempt by design)"
        )

    return problems


def _skill_names(root):
    """Sorted names of skills/<name>/ directories that contain SKILL.md.
    Derived from the tree, not hardcoded — a new skill extends R3
    automatically, with no list to drift."""
    names = []
    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        return names
    for entry in os.listdir(skills_dir):
        full = os.path.join(skills_dir, entry)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "SKILL.md")):
            names.append(entry)
    return sorted(names)


def _release_namespace(root):
    """R3 — scan the living-file allowlist for bare slash references to
    Kerd skills. The correct form is /kerd:<name>; a bare /<name> is a
    violation. Allowlist (see spec): skills/**/*.md, modes/**/*.md,
    docs/design/*.md, top-level docs/*.md, CLAUDE.md. docs/plans/,
    docs/gates/, kivna/, README.md are out by construction — immutable
    dated records never retroactively fail CI; README's shorthand
    exception is human-adjudicated."""
    names = _skill_names(root)
    if not names:
        return []

    problems = []
    patterns = [
        (name, re.compile(r'(?<![\w:/.\-])/' + re.escape(name) + r'\b'))
        for name in names
    ]

    targets = []
    for d in ("skills", "modes", os.path.join("docs", "design")):
        targets += glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True)
    targets += glob.glob(os.path.join(root, "docs", "*.md"))
    claude_md = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude_md):
        targets.append(claude_md)

    for path in sorted(set(targets)):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                for name, pat in patterns:
                    if pat.search(line):
                        problems.append(
                            f"{rel}:{lineno} — bare '/{name}' (write '/kerd:{name}')"
                        )

    return problems


# ── R4: the release history says the same thing in both files ───────────

_README_ENTRY = re.compile(r"\n### v(\d+\.\d+\.\d+)\n")
_CHANGELOG_ENTRY = re.compile(r"\n## (\d+\.\d+\.\d+)\n")


def _history_entries(text, pattern, level):
    """Map version -> its note text, from one file's release history.

    `level` is the heading depth of an entry (3 for README's `### v1.2.3`,
    2 for CHANGELOG's `## 1.2.3`). A note ends at the next entry or at the
    first heading of that depth or shallower — that is what stops README's
    `## License` from being read as part of its last note. The scan skips
    fenced code blocks, so a `# comment` inside one is not a heading.
    """
    parts = pattern.split("\n" + text)
    entries = {}
    for i in range(1, len(parts), 2):
        entries[parts[i]] = _note_before_next_heading(parts[i + 1], level)
    return entries


def _note_before_next_heading(body, level):
    """Take the lines of `body` up to the first heading at `level` or
    shallower, ignoring headings inside ``` or ~~~ fenced blocks."""
    kept = []
    fence = None
    for line in body.split("\n"):
        stripped = line.lstrip()
        if fence is None:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                fence = stripped[:3]
            else:
                hashes = len(line) - len(line.lstrip("#"))
                if 1 <= hashes <= level and line[hashes:hashes + 1] == " ":
                    break
        elif stripped.startswith(fence):
            fence = None
        kept.append(line)
    return "\n".join(kept).strip()


def _release_history(root):
    """R4 — every version in both README.md and CHANGELOG.md carries the
    same note. CHANGELOG may hold older entries the README has trimmed;
    that is the decided shape, not drift. Either file missing skips the
    check. Notes compare exactly; each entry stops at the next heading that
    is not an entry, so a trailing section is not read as part of a note."""
    problems = []
    readme_path = os.path.join(root, "README.md")
    changelog_path = os.path.join(root, "CHANGELOG.md")
    if not (os.path.exists(readme_path) and os.path.exists(changelog_path)):
        return problems
    try:
        readme = _history_entries(_read(readme_path), _README_ENTRY, 3)
        changelog = _history_entries(_read(changelog_path), _CHANGELOG_ENTRY, 2)
    except OSError as exc:
        return [f"release history — unreadable: {exc}"]
    missing = sorted(set(readme) - set(changelog))
    for version in missing:
        problems.append(
            f"release history — {version} is in README.md but not CHANGELOG.md"
        )
    for version in sorted(set(readme) & set(changelog)):
        if readme[version] != changelog[version]:
            problems.append(
                f"release history — {version} reads differently in README.md and CHANGELOG.md"
            )
    return problems


# ── R5: README's "What's New" header matches plugin.json's version ──────

_WHATS_NEW_HEADER = re.compile(r"^## What's New \(v(\d+\.\d+\.\d+)\)\s*$", re.MULTILINE)


def _release_whats_new(root, plugin):
    """R5 — the README `## What's New (vX.Y.Z)` header version must equal
    plugin.json's version. plugin is None (no plugin.json, or its version
    is missing/invalid — already reported by R1) or README.md missing skip
    the check. No header present skips too — README not carrying a What's
    New section is not this rule's concern."""
    problems = []
    if plugin is None:
        return problems
    plugin_version = plugin.get("version")
    if not isinstance(plugin_version, str):
        return problems

    readme_path = os.path.join(root, "README.md")
    if not os.path.isfile(readme_path):
        return problems

    match = _WHATS_NEW_HEADER.search(_read(readme_path))
    if match is None:
        return problems

    header_version = match.group(1)
    if header_version != plugin_version:
        problems.append(
            "README.md — \"What's New\" header is v{} but plugin.json version is "
            "'{}' (must match)".format(header_version, plugin_version)
        )
    return problems


def _version_key(version):
    return tuple(int(part) for part in version.split("."))


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()

def release_audit(root):
    """Release-rules sweep (R1–R5). Empty list = clean. R1/R2 skip
    vacuously when neither plugin file exists; R3 runs regardless (it
    depends only on the tree); R4 skips unless both history files exist;
    R5 skips unless plugin.json and README.md both exist."""
    plugin, marketplace, problems = _release_files(root)
    if plugin or marketplace or problems:
        problems.extend(_release_versions(plugin, marketplace))
        problems.extend(_release_capability(plugin, marketplace))
    problems.extend(_release_namespace(root))
    problems.extend(_release_history(root))
    problems.extend(_release_whats_new(root, plugin))
    return problems


# ── CLI ──────────────────────────────────────────────────────────────────

def _cmd_release(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    root, argv = _pop_root(argv)
    if argv:
        print(__doc__)
        return 2

    problems = release_audit(root)

    if as_json:
        print(json.dumps(problems))
        return 0 if not problems else 1

    if not problems:
        print("release: clean")
        return 0
    for p in problems:
        print(f"problem: {p}")
    print(f"release: {len(problems)} problem{'' if len(problems) == 1 else 's'}")
    return 1


# ── selftest ─────────────────────────────────────────────────────────────

def _sw(path, content):
    """Write a fixture file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _selftest_cases():
    cases = []

    # Case 1 — clean tree passes.
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, ".claude-plugin", "plugin.json"),
            '{"name": "kerd", "version": "1.0.0", "description": "caps A"}',
        )
        _sw(
            os.path.join(root, ".claude-plugin", "marketplace.json"),
            '{"metadata": {"description": "different one-liner", "version": "1.0.0"}, '
            '"plugins": [{"version": "1.0.0", "description": "caps A"}]}',
        )
        _sw(
            os.path.join(root, "skills", "tend", "SKILL.md"),
            "Use /kerd:tend here.\nSee skills/tend/SKILL.md for the source.\n",
        )
        problems = release_audit(root)
        cases.append(("clean tree passes", problems == [], problems))

    # Case R4a — a note that differs between the two histories refuses.
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, "README.md"),
            "# P\n\n## What's New (v1.1.0)\n\n### v1.1.0\n\nThe new thing.\n\n"
            "### v1.0.0\n\nThe first thing.\n",
        )
        _sw(
            os.path.join(root, "CHANGELOG.md"),
            "# Changelog\n\n## 1.1.0\n\nThe new thing, worded differently.\n\n"
            "## 1.0.0\n\nThe first thing.\n",
        )
        problems = _release_history(root)
        cases.append((
            "a note that differs between the histories refuses",
            problems == ["release history — 1.1.0 reads differently in README.md and CHANGELOG.md"],
            problems,
        ))

    # Case R4b — an older entry the README trimmed is the decided shape, and
    # a trailing section after a file's last entry is not part of its note.
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, "README.md"),
            "# P\n\n### v1.1.0\n\nThe new thing.\n\n### v1.0.0\n\nThe first thing.\n\n"
            "## License\n\nMIT\n",
        )
        _sw(
            os.path.join(root, "CHANGELOG.md"),
            "# Changelog\n\n## 1.1.0\n\nThe new thing.\n\n## 1.0.0\n\nThe first thing.\n\n"
            "## 0.9.0\n\nOlder, trimmed from the README.\n",
        )
        problems = _release_history(root)
        cases.append(("a trimmed older entry passes", problems == [], problems))

    # Case R4c — a truncated final note refuses (the trailing-section cut
    # must not become a prefix exemption).
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, "README.md"),
            "# P\n\n### v1.0.0\n\nThe first\n\n## License\n\nMIT\n",
        )
        _sw(
            os.path.join(root, "CHANGELOG.md"),
            "# Changelog\n\n## 1.0.0\n\nThe first thing.\n",
        )
        problems = _release_history(root)
        cases.append((
            "a truncated final note refuses",
            problems == ["release history — 1.0.0 reads differently in README.md and CHANGELOG.md"],
            problems,
        ))

    # Case R4d — a `#` comment inside a fenced block is not a heading, so a
    # difference after it is still caught.
    with tempfile.TemporaryDirectory() as root:
        fenced = "Install it:\n\n```sh\n# comment\nclaude plugin install kerd\n```\n\n"
        _sw(
            os.path.join(root, "README.md"),
            "# P\n\n### v1.0.0\n\n" + fenced + "Then restart.\n",
        )
        _sw(
            os.path.join(root, "CHANGELOG.md"),
            "# Changelog\n\n## 1.0.0\n\n" + fenced + "Then do something else.\n",
        )
        problems = _release_history(root)
        cases.append((
            "a difference after a fenced # comment refuses",
            problems == ["release history — 1.0.0 reads differently in README.md and CHANGELOG.md"],
            problems,
        ))

    # Case R4e — a version in the README but not the changelog refuses.
    with tempfile.TemporaryDirectory() as root:
        _sw(os.path.join(root, "README.md"), "# P\n\n### v2.0.0\n\nNew.\n")
        _sw(os.path.join(root, "CHANGELOG.md"), "# Changelog\n\n## 1.0.0\n\nOld.\n")
        problems = _release_history(root)
        cases.append((
            "a README-only version refuses",
            problems == ["release history — 2.0.0 is in README.md but not CHANGELOG.md"],
            problems,
        ))

    # Case R5 — a README "What's New" header that disagrees with
    # plugin.json's version refuses.
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, ".claude-plugin", "plugin.json"),
            '{"name": "kerd", "version": "1.0.0", "description": "caps A"}',
        )
        _sw(
            os.path.join(root, "README.md"),
            "# P\n\n## What's New (v0.9.0)\n\nThe old thing.\n",
        )
        problems = release_audit(root)
        ok = any("\"What's New\" header" in p for p in problems)
        cases.append(("a What's New header behind plugin.json's version refuses", ok, problems))

    # Case 2 — version drift refuses.
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, ".claude-plugin", "plugin.json"),
            '{"name": "kerd", "version": "1.0.0", "description": "caps A"}',
        )
        _sw(
            os.path.join(root, ".claude-plugin", "marketplace.json"),
            '{"metadata": {"description": "one-liner, different by design", '
            '"version": "1.0.1"}, "plugins": [{"version": "1.0.0", "description": "caps A"}]}',
        )
        problems = release_audit(root)
        ok = any("version drift" in p for p in problems)
        cases.append(("version drift refuses", ok, problems))

    # Case 3 — capability drift refuses.
    with tempfile.TemporaryDirectory() as root:
        _sw(
            os.path.join(root, ".claude-plugin", "plugin.json"),
            '{"name": "kerd", "version": "1.0.0", "description": "caps A"}',
        )
        _sw(
            os.path.join(root, ".claude-plugin", "marketplace.json"),
            '{"metadata": {"description": "one-liner, different by design", '
            '"version": "1.0.0"}, "plugins": [{"version": "1.0.0", "description": "caps B"}]}',
        )
        problems = release_audit(root)
        ok = any("capability-list drift" in p for p in problems)
        cases.append(("capability drift refuses", ok, problems))

    return cases


def _cmd_selftest(argv):
    if argv:
        print(__doc__)
        return 2
    bad = 0
    total = 0
    for name, ok, problems in _selftest_cases():
        total += 1
        if not ok:
            bad += 1
            print(f"FAIL: {name}\n  problems: {problems}")
    if bad:
        print(f"selftest: {total - bad} ok, {bad} failed")
        return 1
    print(f"selftest: {total} ok")
    return 0


def main(argv):
    if argv and argv[0] == "selftest":
        return _cmd_selftest(argv[1:])
    return _cmd_release(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
