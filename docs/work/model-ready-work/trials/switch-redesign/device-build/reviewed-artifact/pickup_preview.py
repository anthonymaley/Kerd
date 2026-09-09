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


# Punctuation that would otherwise close a table cell, open markup, or begin
# raw HTML. Each is shown as a decimal character reference, so it survives as
# readable data instead of being interpreted. "&" is included so that a label
# containing a literal reference cannot forge one.
_MARKDOWN_ACTIVE = {
    character: f"&#{ord(character)};" for character in '&<>|`\\*_[]~":.'
}


def _markdown_cell(value: str) -> str:
    """Render a label as one inert Markdown table cell.

    Control characters, formatting characters and newlines first become the
    same visible escapes the text format uses, so no label can open a second
    row. Markdown- and HTML-active punctuation then becomes decimal character
    references, so no label can produce emphasis, a code span, a link or
    executable HTML. The result is wrapped in quotation marks, which are
    therefore the only unescaped quotation marks in the cell and mark exactly
    where the recorded label begins and ends.
    """
    # GitHub can link an email even after decoding an &#64; reference. A visible
    # escape prevents that second pass without inserting an invisible character.
    # Run after _terminal_safe so literal backslash-u text remains distinguishable.
    visible = _terminal_safe(value).replace("@", r"\u0040")
    escaped = "".join(_MARKDOWN_ACTIVE.get(character, character) for character in visible)
    return f'"{escaped}"'


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


def summarize_markdown(packet: Any) -> str:
    """Return Markdown containing only the allowed metadata for a valid packet.

    Source bodies, the optional note and unrecognized packet fields are
    deliberately never rendered, so the result can be pasted into a work report.
    Every recorded label passes through _markdown_cell, so no label can add a
    row, produce markup or emit executable HTML.
    """
    summary, _ = _validated_summary(packet)
    sources = summary["selected_sources"]
    lines = [
        "# Prepared pickup preview",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Branch | {_markdown_cell(summary['branch'])} |",
        f"| Revision | {_markdown_cell(summary['revision'])} |",
        (
            "| Working tree at check | clean |"
            if summary["clean_at_check"]
            else "| Working tree at check | not clean |"
        ),
        (
            "| Synchronization | synchronized |"
            if summary["synchronized"]
            else "| Synchronization | local-only (not synchronized) |"
        ),
        f"| Selected sources | {len(sources)} |",
        f"| Total source text | {summary['total_utf8_bytes']} UTF-8 bytes |",
        "",
        "| # | File | Selection | UTF-8 bytes |",
        "| --- | --- | --- | --- |",
    ]

    for index, source in enumerate(sources, start=1):
        lines.append(
            f"| {index} | {_markdown_cell(source['file'])} "
            f"| {_markdown_cell(source['selection'])} "
            f"| {source['utf8_bytes']} |"
        )

    lines.append("")
    lines.append("Prepared does not mean restored or accepted.")
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview a prepared pickup packet without displaying source text."
    )
    parser.add_argument("packet", type=Path, help="path to a pickup packet JSON file")
    parser.add_argument(
        "--format",
        choices=("text", "json", "markdown"),
        default="text",
        help="output format (default: text)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        with args.packet.open("r", encoding="utf-8") as stream:
            packet = json.load(stream)
        renderers = {
            "text": summarize,
            "json": summarize_json,
            "markdown": summarize_markdown,
        }
        output = renderers[args.format](packet)
        print(output)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"pickup_preview: error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
