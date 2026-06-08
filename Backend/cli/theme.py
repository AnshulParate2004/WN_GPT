"""Shared terminal theme and console factory."""
from __future__ import annotations

from rich.console import Console
from rich.theme import Theme

VERSION = "1.0.0"

# Healthcare palette (teal + calm blue-green)
TEAL = "#00b4a6"
TEAL_BRIGHT = "#2dd4bf"
TEAL_DIM = "#5ec4bc"
NAVY = "#1e3a5f"
NAVY_LIGHT = "#2d5a87"
GREEN = "#22c55e"
MUTED = "#94a3b8"
ROSE = "#f43f5e"
AMBER = "#f59e0b"

WELLNESS_THEME = Theme(
    {
        "brand.teal": TEAL,
        "brand.navy": NAVY,
        "brand.muted": MUTED,
        "info": TEAL_BRIGHT,
        "success": "green",
        "warning": "yellow",
        "error": "bold red",
    }
)

# Rich styles per detected intent (for panels and streaming)
INTENT_STYLES: dict[str, str] = {
    "triage": "bold red",
    "booking": "bold green",
    "channeling": "bold cyan",
    "adherence": "bold yellow",
    "care_plan": "bold green",
    "discharge": "cyan",
    "insurance": "yellow",
    "hospital_ops": "blue",
    "pharmacy": "bold red",
    "mental_health": "magenta",
    "family_care": "green",
    "product_rec": "cyan",
    "report_analysis": "bold red",
    "nutrisense": "bold green",
    "fitguide": "bold yellow",
    "health_records": "bold white",
    "general": "white",
}

INTENT_LABELS: dict[str, str] = {
    "triage": "Symptom Triage",
    "booking": "Booking & Scheduling",
    "channeling": "Patient Channeling",
    "adherence": "Follow-up & Adherence",
    "care_plan": "Care Plan",
    "discharge": "Discharge",
    "insurance": "Insurance & Claims",
    "hospital_ops": "Hospital Operations",
    "pharmacy": "Pharmacy",
    "mental_health": "Mental Health",
    "family_care": "Family Care",
    "product_rec": "Product Recommendations",
    "report_analysis": "Report Analyzer",
    "nutrisense": "NutriSense",
    "fitguide": "FitGuide",
    "health_records": "Health Records",
    "general": "General Assistant",
}


def make_console(**kwargs) -> Console:
    return Console(theme=WELLNESS_THEME, highlight=True, **kwargs)


def style_for_intent(intent: str) -> str:
    return INTENT_STYLES.get(intent, "white")


def label_for_intent(intent: str) -> str:
    return INTENT_LABELS.get(intent, intent.replace("_", " ").title())
