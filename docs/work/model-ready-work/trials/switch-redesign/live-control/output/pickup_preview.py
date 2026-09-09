#!/usr/bin/env python3
"""Render a privacy-conscious preview of a prepared pickup packet."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any


def _mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _text(
    mapping: dict[str, Any], name: str, *, owner: str = "packet", empty: bool = False
) -> str:
    if name not in mapping:
        raise ValueError(f"{owner}.{name} is required")
    value = mapping[name]
    if not isinstance(value, str) or (not empty and not value):
        qualifier = "a string" if empty else "a non-empty string"
        raise ValueError(f"{owner}.{name} must be {qualifier}")
    return value


def _boolean(mapping: dict[str, Any], name: str) -> bool:
    if name not in mapping or type(mapping[name]) is not bool:
        raise ValueError(f"packet.{name} must be a boolean")
    return mapping[name]


def _terminal_safe(value: str) -> str:
    """Make control and formatting characters visible rather than executable."""
    pieces: list[str] = []
    for character in value:
        if character == "\\":
            pieces.append("\\\\")
        elif unicodedata.category(character) in {"Cc", "Cf", "Cs"}:
            codepoint = ord(character)
            if codepoint <= 0xFFFF:
                pieces.append(f"\\u{codepoint:04X}")
            else:
                pieces.append(f"\\U{codepoint:08X}")
        else:
            pieces.append(character)
    return "".join(pieces)


def _utf8_size(value: str, owner: str) -> int:
    try:
        return len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise ValueError(f"{owner}.content must be valid Unicode text") from error


def _validated_summary(packet: Any) -> tuple[dict[str, Any], str | None]:
    """Validate a packet and return only the metadata allowed in summaries."""
    packet = _mapping(packet, "packet")

    status = _text(packet, "status")
    if status != "pickup_prepared":
        raise ValueError("packet.status must be 'pickup_prepared'")

    branch = _text(packet, "branch")
    commit = _text(packet, "commit")
    clean = _boolean(packet, "clean_at_check")
    synchronized = _boolean(packet, "synchronized")

    if "sources" not in packet or not isinstance(packet["sources"], list):
        raise ValueError("packet.sources must be an array")

    sources: list[dict[str, Any]] = []
    for index, raw_source in enumerate(packet["sources"]):
        owner = f"packet.sources[{index}]"
        source = _mapping(raw_source, owner)
        filename = _text(source, "file", owner=owner)
        selection = _text(source, "selection", owner=owner)
        content = _text(source, "content", owner=owner, empty=True)
        sources.append(
            {
                "file": filename,
                "selection": selection,
                "utf8_bytes": _utf8_size(content, owner),
            }
        )

    note: str | None = None
    if "note" in packet:
        if not isinstance(packet["note"], str):
            raise ValueError("packet.note must be a string")
        note = packet["note"]

    summary = {
        "branch": branch,
        "revision": commit,
        "clean_at_check": clean,
        "synchronized": synchronized,
        "selected_sources": sources,
        "total_utf8_bytes": sum(source["utf8_bytes"] for source in sources),
    }
    return summary, note


def summarize(packet: Any) -> str:
    """Return display text for a valid prepared-pickup packet.

    Source bodies and unrecognized packet fields are deliberately never rendered.
    """
    summary, note = _validated_summary(packet)
    sources = summary["selected_sources"]
    source_word = "source" if len(sources) == 1 else "sources"
    lines = [
        "Prepared pickup preview",
        f"Branch: {_terminal_safe(summary['branch'])}",
        f"Revision: {_terminal_safe(summary['revision'])}",
        (
            "Working tree at check: clean"
            if summary["clean_at_check"]
            else "Working tree at check: not clean"
        ),
        (
            "Synchronization: synchronized"
            if summary["synchronized"]
            else "Synchronization: local-only (not synchronized)"
        ),
        f"Selected sources: {len(sources)} {source_word}",
    ]

    for index, source in enumerate(sources, start=1):
        lines.append(
            f"  {index}. {_terminal_safe(source['file'])} — "
            f"{_terminal_safe(source['selection'])} — "
            f"{source['utf8_bytes']} UTF-8 bytes"
        )

    lines.append(f"Total source text: {summary['total_utf8_bytes']} UTF-8 bytes")
    if note:
        lines.append(f"Note: {_terminal_safe(note)}")
    lines.append("Prepared does not mean restored or accepted.")
    return "\n".join(lines)


def summarize_json(packet: Any) -> str:
    """Return JSON containing only the allowed metadata for a valid packet."""
    summary, _ = _validated_summary(packet)
    return json.dumps(summary, ensure_ascii=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview a prepared pickup packet without displaying source text."
    )
    parser.add_argument("packet", type=Path, help="path to a pickup packet JSON file")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format (default: text)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        with args.packet.open("r", encoding="utf-8") as stream:
            packet = json.load(stream)
        output = summarize_json(packet) if args.format == "json" else summarize(packet)
        print(output)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"pickup_preview: error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
