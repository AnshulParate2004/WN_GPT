"""
Parsers — helpers to extract structured data from LLM text output.
"""
from __future__ import annotations
import json
import re


def extract_json(text: str) -> dict | list | None:
    """
    Extract the first JSON object or array from an LLM response string.
    Handles markdown code fences like ```json … ```.
    """
    # Remove markdown fences
    clean = re.sub(r"```(?:json)?\s*", "", text)
    clean = clean.replace("```", "").strip()

    # Try direct parse
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    # Try to find first {...} or [...]
    match = re.search(r"(\{.*\}|\[.*\])", clean, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    return None


def safe_int(value: str | int | None, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def safe_float(value: str | float | None, default: float = 0.0) -> float:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def normalize_urgency(level: str) -> str:
    level = level.lower().strip()
    if level in {"emergency", "critical", "severe"}:
        return "emergency"
    if level in {"high", "urgent"}:
        return "high"
    if level in {"medium", "moderate"}:
        return "medium"
    return "low"


def normalize_risk(level: str) -> str:
    level = level.lower().strip()
    if level in {"high", "severe", "critical"}:
        return "high"
    if level in {"moderate", "medium"}:
        return "moderate"
    return "low"


def normalize_enum(value: str, options: list[str], default: str = "general") -> str:
    """Matches a string to the closest option in a list, or returns default."""
    val = value.lower().strip()
    if val in options:
        return val
    for opt in options:
        if opt in val or val in opt:
            return opt
    return default
