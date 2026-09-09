#!/usr/bin/env python3
"""One read-only measurement job using the existing candidate adapter."""
import argparse
import json
from pathlib import Path
import sys

PACK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK / "skills/switch/scripts"))
import codex_roll
import roll


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--output", help="Save this run's sanitized observation as JSON")
    args = parser.parse_args()
    transport = roll.connection()
    bridge = codex_roll.AppServerBridge(args.project, transport)
    request_path = bridge.core.request_path(args.name)
    if request_path.exists():
        raise ValueError("Choose a fresh measurement name; retain prior evidence")
    commands = []
    original_server = codex_roll.AppServer

    class ObservedServer(original_server):
        def receive(self, *a, **kw):
            event = super().receive(*a, **kw)
            if event.get("method") == "item/completed":
                item = event.get("params", {}).get("item", {})
                if item.get("type") == "commandExecution":
                    commands.append({key: item.get(key) for key in
                        ("type", "command", "cwd", "status", "aggregatedOutput", "exitCode")})
                elif item.get("type") in {"fileChange", "webSearch", "mcpToolCall", "collabToolCall"}:
                    commands.append({"type": item["type"], "tool": item.get("tool"),
                                     "status": item.get("status")})
            return event

    codex_roll.AppServer = ObservedServer
    try:
        result = bridge.run("codex", Path(args.prompt_file).read_text(),
                            "Read-only local pickup context measurement", args.name, args.name,
                            writable=False, model="gpt-5.6-sol", effort="high")
    finally:
        codex_roll.AppServer = original_server
        # Ordinary command outputs only; no native reasoning/transcript content.
        if request_path.is_dir():
            transport.save(request_path / "read-observations.json", commands)
    if result.get("status") == "completed":
        bridge.close(args.name)
    observation = {k: result.get(k) for k in ("status", "error", "cleanup_error",
          "model", "started_at", "finished_at", "owned_children_gone", "context_readings", "reply")}
    if args.output:
        transport.save(Path(args.output), observation)
    print(json.dumps(observation, indent=2))
    return 0 if result.get("status") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
