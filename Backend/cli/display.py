"""Terminal styling and intent colour mapping."""
from __future__ import annotations

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"

INTENT_COLORS: dict[str, str] = {
    "triage": RED,
    "booking": GREEN,
    "channeling": CYAN,
    "adherence": YELLOW,
    "care_plan": GREEN,
    "discharge": CYAN,
    "insurance": YELLOW,
    "hospital_ops": CYAN,
    "pharmacy": RED,
    "mental_health": YELLOW,
    "family_care": GREEN,
    "product_rec": CYAN,
    "report_analysis": RED,
    "nutrisense": GREEN,
    "fitguide": YELLOW,
    "health_records": BOLD,
    "general": RESET,
}


def color_for_intent(intent: str) -> str:
    return INTENT_COLORS.get(intent, RESET)


def print_banner(patient_name: str) -> None:
    print(f"{BOLD}{CYAN}WellnessGPT CLI started for {patient_name}{RESET}")


def print_error(message: str) -> None:
    print(f"{RED}✗ {message}{RESET}")


def print_user_prompt() -> str:
    return input(f"\n{BOLD}{CYAN}You:{RESET} ").strip()


def print_intent_header(intent: str) -> None:
    color = color_for_intent(intent)
    print(f"\n{color}{BOLD}[{intent.upper()}]{RESET} ", end="", flush=True)


def print_stream_token(token: str, intent: str) -> None:
    color = color_for_intent(intent)
    print(f"{color}{token}{RESET}", end="", flush=True)
