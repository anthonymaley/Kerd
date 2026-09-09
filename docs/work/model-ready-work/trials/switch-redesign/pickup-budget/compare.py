#!/usr/bin/env python3
"""Retain a matched read-only pickup experiment using the existing run helper."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PACK = HERE.parents[2]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import handoff

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("project", type=Path)
args = parser.parse_args()
root = handoff.root_for(args.project)
if handoff.git(root, "rev-parse", "HEAD") != "2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83":
    raise ValueError("Comparison requires its declared pinned snapshot")
out = HERE / "comparison"
if out.exists():
    raise ValueError("Retain existing observations; choose a new explicit experiment")
out.mkdir()
began = time.monotonic()
packet = handoff.prepare(root, "pickup-comparison", "CONTEXT.md",
                        sections=[("TODO.md", "## Now")])
preparation_seconds = time.monotonic() - began
(out / "prepared.json").write_text(json.dumps(packet, indent=2) + "\n")
task = """Restore this isolated Seinn checkout's saved position, not an old device trial.
Read-only local files/Git only: no network/fetch/push, tests/builds, device/SSH
probes, messages, edits, new tasks, delegation, native session histories or other
app tools. These limits override any broader actions in the supplied skill.
No actual switch-out, mode restoration or new Conductor task is authorized.
Return one concise JSON object: position, last_completed, next_obligation,
next_decision, authority, unresolved_memory, reads. Cite source file/section.
Carry explicit restrictions with their scope, and distinguish saved observations
from fresh verification. Report incomplete reads. No routine user question or
token-budget claim; stop after restoration. Fully read selected sections/files.
"""
legacy = PACK.parents[2] / "skills/switch/SKILL.md"
prompts = {
    "control-before": (HERE / "control.md").read_text(),
    "legacy": task + "\nCurrent legacy skill (local-only scope above governs):\n" + legacy.read_text(),
    "candidate": task + "\nCurrent candidate skill:\n" +
        (PACK / "skills/switch/SKILL.md").read_text() + "\nIn/Out guide:\n" +
        (PACK / "skills/switch/references/in-out.md").read_text() +
        "\nCaller-prepared complete records and local identity; use directly, " +
        "with supporting sources available for genuine gaps:\n" +
        json.dumps(packet, ensure_ascii=False),
    "control-after": (HERE / "control.md").read_text(),
}
(out / "setup.json").write_text(json.dumps({
    "snapshot": packet["commit"], "preparation_seconds": preparation_seconds,
    "order": list(prompts), "scope": "local-only; prepared selection supplied",
}, indent=2) + "\n")
for label, prompt in prompts.items():
    prompt_file = out / (label + "-prompt.md")
    prompt_file.write_text(prompt)
    print("Starting " + label, flush=True)
    result = subprocess.run([sys.executable, str(HERE / "run.py"),
        "--project", str(root), "--prompt-file", str(prompt_file),
        "--name", "paired-pickup-" + label, "--output", str(out / (label + ".json"))],
        capture_output=True, text=True)
    if result.returncode:
        print(result.stderr[-2000:] or result.stdout[-2000:], flush=True)
        raise SystemExit(result.returncode)
    observation = json.loads((out / (label + ".json")).read_text())
    print(label + ": " + str(observation["status"]), flush=True)
    if handoff.git(root, "status", "--porcelain"):
        raise RuntimeError("Pickup changed project state")
print("Comparison observations retained; independent assessment still required.", flush=True)
