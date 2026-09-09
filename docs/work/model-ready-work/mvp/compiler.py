#!/usr/bin/env python3
"""Offline, deterministic proof of Kerd's model-ready work design."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROFILES = ROOT / "profiles.json"
REQUIRED = (
    "id",
    "objective",
    "deliverable",
    "success",
    "evidence",
    "context",
    "guardrails",
    "authority",
    "completion",
)
LIST_FIELDS = ("deliverable", "success", "evidence", "guardrails", "completion")


class CompileError(ValueError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CompileError(f"not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CompileError(f"invalid JSON: {path}:{exc.lineno}:{exc.colno}: {exc.msg}") from exc


def validate(envelope: dict[str, Any]) -> None:
    problems: list[str] = []
    for field in REQUIRED:
        if field not in envelope:
            problems.append(f"{field}: missing")
        elif envelope[field] in (None, "", [], {}):
            problems.append(f"{field}: empty")
    for field in LIST_FIELDS:
        if field in envelope and not isinstance(envelope[field], list):
            problems.append(f"{field}: must be a list")
    seen: set[str] = set()
    for i, row in enumerate(envelope.get("success", []), 1):
        if not isinstance(row, dict):
            problems.append(f"success[{i}]: must be an object")
            continue
        for field in ("id", "measure", "target"):
            if not row.get(field):
                problems.append(f"success[{i}].{field}: missing or empty")
        row_id = row.get("id")
        if row_id in seen:
            problems.append(f"success[{i}].id: duplicate {row_id!r}")
        seen.add(row_id)
    authority = envelope.get("authority")
    if authority and not isinstance(authority, dict):
        problems.append("authority: must be an object")
    if problems:
        raise CompileError("invalid task envelope:\n- " + "\n- ".join(problems))


def registry() -> dict[str, dict[str, Any]]:
    data = load_json(PROFILES)
    models: dict[str, dict[str, Any]] = {}
    for profile in data["profiles"]:
        for model in profile["models"]:
            if model in models:
                raise CompileError(f"model {model!r} appears in multiple profiles")
            models[model] = profile
    return models


def resolve_profile(model: str) -> dict[str, Any]:
    if model == "neutral":
        return {
            "id": "neutral@1",
            "provider": "neutral",
            "family": "neutral",
            "models": ["neutral"],
            "default_effort": "none",
            "efforts": ["none"],
            "renderer": "neutral",
            "guidance": [],
            "sources": [],
        }
    profiles = registry()
    if model not in profiles:
        raise CompileError(
            f"no local profile for {model!r}; available: " + ", ".join(sorted(profiles))
        )
    return profiles[model]


def bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def success_lines(rows: list[dict[str, str]]) -> str:
    return "\n".join(f"- {r['id']}: {r['measure']} — target: {r['target']}" for r in rows)


def authority_lines(authority: dict[str, list[str]]) -> str:
    may = bullets(authority.get("may_decide", [])) or "- Nothing beyond the stated task"
    owned = bullets(authority.get("producer_owned", [])) or "- None declared"
    return f"May decide:\n{may}\nProducer-owned:\n{owned}"


def render_neutral(e: dict[str, Any], _: dict[str, Any]) -> tuple[str, dict[str, str]]:
    sections = {
        "id": f"# Task ID\n{e['id']}",
        "objective": f"# Objective\n{e['objective']}",
        "deliverable": f"# Deliverable\n{bullets(e['deliverable'])}",
        "success": f"# Success criteria\n{success_lines(e['success'])}",
        "evidence": f"# Evidence\n{bullets(e['evidence'])}",
        "context": f"# Context\n{json.dumps(e['context'], indent=2, ensure_ascii=False)}",
        "guardrails": f"# Guardrails\n{bullets(e['guardrails'])}",
        "authority": f"# Authority\n{authority_lines(e['authority'])}",
        "completion": f"# Completion\n{bullets(e['completion'])}",
    }
    if e.get("unknowns"):
        sections["unknowns"] = f"# Unknowns\n{bullets(e['unknowns'])}"
    return "\n\n".join(sections.values()) + "\n", sections


def xml_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def xml_items(tag: str, values: list[str]) -> str:
    return "\n".join(f"  <{tag}>{xml_escape(v)}</{tag}>" for v in values)


def render_claude(e: dict[str, Any], p: dict[str, Any]) -> tuple[str, dict[str, str]]:
    success = "\n".join(
        f"  <criterion id=\"{xml_escape(r['id'])}\"><measure>{xml_escape(r['measure'])}</measure><target>{xml_escape(r['target'])}</target></criterion>"
        for r in e["success"]
    )
    sections = {
        "id": f"<task_id>{xml_escape(e['id'])}</task_id>",
        "objective": f"<objective>{xml_escape(e['objective'])}</objective>",
        "deliverable": f"<deliverables>\n{xml_items('deliverable', e['deliverable'])}\n</deliverables>",
        "success": f"<success_criteria>\n{success}\n</success_criteria>",
        "evidence": f"<evidence_required>\n{xml_items('item', e['evidence'])}\n</evidence_required>",
        "guardrails": f"<guardrails>\n{xml_items('rule', e['guardrails'])}\n</guardrails>",
        "authority": f"<authority>\n{xml_escape(authority_lines(e['authority']))}\n</authority>",
        "context": f"<context>\n{xml_escape(json.dumps(e['context'], indent=2, ensure_ascii=False))}\n</context>",
        "completion": f"<completion>\n{xml_items('condition', e['completion'])}\n</completion>",
    }
    if e.get("unknowns"):
        sections["unknowns"] = f"<unknowns>\n{xml_items('unknown', e['unknowns'])}\n</unknowns>"
    preface = (
        "<role>You are the executor responsible for producing the stated result and evidence. "
        "Choose the most effective method inside the authority and guardrails.</role>"
    )
    prompt = preface + "\n\n" + "\n\n".join(sections.values()) + "\n"
    return prompt, sections


def render_openai(e: dict[str, Any], p: dict[str, Any]) -> tuple[str, dict[str, str]]:
    sections = {
        "id": f"# Task ID\n{e['id']}",
        "objective": f"# Outcome\n{e['objective']}",
        "success": f"# Success criteria\n{success_lines(e['success'])}",
        "deliverable": f"# Deliverable\n{bullets(e['deliverable'])}",
        "evidence": f"# Evidence\n{bullets(e['evidence'])}",
        "guardrails": f"# Guardrails\n{bullets(e['guardrails'])}",
        "authority": f"# Authority\n{authority_lines(e['authority'])}",
        "completion": f"# Stop condition\n{bullets(e['completion'])}",
        "context": f"# Task context\n{json.dumps(e['context'], indent=2, ensure_ascii=False)}",
    }
    if e.get("unknowns"):
        sections["unknowns"] = f"# Unknowns to resolve\n{bullets(e['unknowns'])}"
    prompt = "\n\n".join(sections.values()) + "\n"
    return prompt, sections


RENDERERS = {
    "neutral": render_neutral,
    "claude_xml": render_claude,
    "openai_outcome": render_openai,
}


def compile_envelope(envelope: dict[str, Any], model: str, effort: str | None) -> tuple[str, dict[str, Any]]:
    validate(envelope)
    profile = resolve_profile(model)
    chosen_effort = effort or profile["default_effort"]
    if chosen_effort not in profile["efforts"]:
        raise CompileError(
            f"effort {chosen_effort!r} not legal for {model}; legal: {', '.join(profile['efforts'])}"
        )
    prompt, sections = RENDERERS[profile["renderer"]](envelope, profile)
    obligation_map = {field: {"present": bool(sections.get(field)), "region": field} for field in REQUIRED}
    missing = [field for field, mapping in obligation_map.items() if not mapping["present"]]
    if missing:
        raise CompileError("compiler dropped required obligation(s): " + ", ".join(missing))
    manifest = {
        "task_id": envelope["id"],
        "envelope_sha256": digest(envelope),
        "model": model,
        "provider": profile["provider"],
        "profile": profile["id"],
        "effort": chosen_effort,
        "configuration": {"reasoning_effort": chosen_effort} if profile["provider"] == "openai" else {"effort": chosen_effort},
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "prompt_characters": len(prompt),
        "prompt_words": len(prompt.split()),
        "obligations": obligation_map,
        "guidance": profile["guidance"],
        "sources": profile["sources"],
        "network_requests": 0,
    }
    return prompt, manifest


def cmd_compile(args: argparse.Namespace) -> int:
    envelope = load_json(Path(args.envelope))
    prompt, manifest = compile_envelope(envelope, args.model, args.effort)
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "prompt.txt").write_text(prompt, encoding="utf-8")
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(out)
    else:
        print(prompt, end="")
        print("\n--- manifest ---")
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


def cmd_profiles(_: argparse.Namespace) -> int:
    for model, profile in sorted(registry().items()):
        print(f"{model}\t{profile['id']}\tdefault={profile['default_effort']}")
    return 0


def selftest() -> int:
    examples = [load_json(path) for path in sorted((ROOT / "examples").glob("*.json"))]
    example = examples[0]
    cases = 0

    for envelope in examples:
        for model in ["neutral", *sorted(registry())]:
            prompt1, manifest1 = compile_envelope(envelope, model, None)
            prompt2, manifest2 = compile_envelope(envelope, model, None)
            assert prompt1 == prompt2
            assert manifest1 == manifest2
            assert all(v["present"] for v in manifest1["obligations"].values())
            assert manifest1["network_requests"] == 0
            cases += 1

    broken = dict(example)
    broken.pop("success")
    try:
        compile_envelope(broken, "neutral", None)
        raise AssertionError("missing success accepted")
    except CompileError as exc:
        assert "success: missing" in str(exc)
        cases += 1

    try:
        compile_envelope(example, "unknown-model", None)
        raise AssertionError("unknown model accepted")
    except CompileError as exc:
        assert "no local profile" in str(exc)
        cases += 1

    try:
        compile_envelope(example, "gpt-5.6-luna", "turbo")
        raise AssertionError("unknown effort accepted")
    except CompileError as exc:
        assert "not legal" in str(exc)
        cases += 1

    with tempfile.TemporaryDirectory() as tmp:
        prompt, manifest = compile_envelope(example, "claude-opus-5", "medium")
        Path(tmp, "prompt.txt").write_text(prompt, encoding="utf-8")
        Path(tmp, "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        assert Path(tmp, "prompt.txt").stat().st_size > 0
        assert manifest["effort"] == "medium"
        cases += 1

    print(f"selftest: {cases} cases passed")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    compile_p = sub.add_parser("compile", help="compile an envelope offline")
    compile_p.add_argument("envelope")
    compile_p.add_argument("--model", required=True)
    compile_p.add_argument("--effort")
    compile_p.add_argument("--out")
    compile_p.set_defaults(func=cmd_compile)
    profiles_p = sub.add_parser("profiles", help="list locally resolved model IDs")
    profiles_p.set_defaults(func=cmd_profiles)
    test_p = sub.add_parser("selftest", help="run deterministic fixtures")
    test_p.set_defaults(func=lambda _: selftest())
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except CompileError as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
