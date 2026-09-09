"""Deliberately broken fixture for the model-ready work trial."""

LEGAL = {"fatal", "non-fatal"}


def normalize_severity(raw: str) -> str:
    """Normalize spelling before validating severity."""
    return raw.strip()


def validate_row(row: dict[str, str]) -> list[str]:
    """Return every problem in one risk-ledger row."""
    problems: list[str] = []
    severity = normalize_severity(row.get("Severity", ""))
    treatment = row.get("Treatment", "").strip().lower()

    if severity and severity not in LEGAL:
        problems.append(f"illegal severity: {severity}")
    if severity == "fatal" and treatment == "accepted":
        problems.append("fatal risk cannot be accepted")
    if not row.get("Risk evidence", "").strip():
        problems.append("risk evidence empty")

    return problems[:1]
