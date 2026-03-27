#!/usr/bin/env python
"""
WellnessGPT — Streaming CLI Bot
────────────────────────────────
Run:  uv run python cli.py
      uv run python cli.py --patient P002

Words stream to the terminal in real-time as GPT-4o generates them.
The supervisor router auto-detects intent and picks the right agent.
"""
from __future__ import annotations
import sys
import argparse
import asyncio
from pathlib import Path

# ── make Backend/ the root so app.* imports work ─────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

from app.core.config import get_settings
from app.db.repository import get_patient
from app.services.routing import detect_intent

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
DIM    = "\033[2m"

INTENT_COLORS = {
    "triage":          RED,
    "booking":         GREEN,
    "channeling":      CYAN,
    "adherence":       YELLOW,
    "care_plan":       GREEN,
    "discharge":       CYAN,
    "insurance":       YELLOW,
    "hospital_ops":    CYAN,
    "pharmacy":        RED,
    "mental_health":   YELLOW,
    "family_care":     GREEN,
    "product_rec":     CYAN,
    "report_analysis": RED,
    "nutrisense":      GREEN,
    "fitguide":         YELLOW,
    "health_records":  BOLD,
    "general":         RESET,
}


def get_streaming_llm() -> AzureChatOpenAI:
    s = get_settings()
    return AzureChatOpenAI(
        azure_deployment=s.azure_openai_deployment,
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.openai_api_version,
        temperature=0.3,
        max_tokens=1024,
        streaming=True,
    )


AGENT_SYSTEM_PROMPTS: dict[str, str] = {
    "triage": "You are a clinical triage AI. Analyze symptoms and determines urgency.",
    "booking": "You are a medical appointment scheduling assistant.",
    "channeling": "You are a patient routing AI. Map symptoms to specialities.",
    "adherence": "You are a medication adherence and follow-up AI.",
    "care_plan": "You are a personalized care plan AI.",
    "discharge": "You are a hospital discharge AI. Summarize stay and provide instructions.",
    "insurance": "You are a healthcare insurance AI. Decode coverage and pre-fill claims.",
    "hospital_ops": "You are a hospital operations AI. Manage beds and inventory.",
    "pharmacy": "You are a clinical pharmacy AI. Check interactions and refills.",
    "mental_health": "You are a compassionate mental health AI. Screen PHQ-9/GAD-7.",
    "family_care": "You are a family health AI. Household-level health insights.",
    "product_rec": "You are a health product recommendation AI.",
    "report_analysis": "You are a Clinical Report Analysis AI. Extract findings from PDFs/Images.",
    "nutrisense": "You are the NutriSense AI. Tailor diet plans based on metabolic data.",
    "fitguide": "You are the FitGuide AI. Build fitness routines from health profiles.",
    "general": "You are WellnessGPT, a health AI assistant.",
}


async def stream_response(
    patient: dict,
    chat_history: list,
    intent: str,
    llm: AzureChatOpenAI,
) -> str:
    system_prompt = AGENT_SYSTEM_PROMPTS.get(intent, AGENT_SYSTEM_PROMPTS["general"])
    patient_ctx = f"Patient: {patient.get('name', 'Unknown')} | Conditions: {patient.get('chronic_conditions')} | Allergies: {patient.get('allergies')}"

    messages = [
        SystemMessage(content=f"{system_prompt}\n\n{patient_ctx}"),
        *chat_history,
    ]

    color  = INTENT_COLORS.get(intent, RESET)
    full   = ""

    print(f"\n{color}{BOLD}[{intent.upper()}]{RESET} ", end="", flush=True)

    async for chunk in llm.astream(messages):
        token = chunk.content
        if token:
            print(f"{color}{token}{RESET}", end="", flush=True)
            full += token

    print()
    return full


async def run_cli(patient_id: str) -> None:
    patient = get_patient(patient_id)
    if not patient:
        print(f"{RED}✗ Patient '{patient_id}' not found.{RESET}")
        return

    llm = get_streaming_llm()
    print(f"{BOLD}{CYAN}WellnessGPT CLI started for {patient['name']}{RESET}")

    chat_history: list = []

    while True:
        try:
            user_input = input(f"\n{BOLD}{CYAN}You:{RESET} ").strip()
        except EOFError: break

        if not user_input: continue
        if user_input.lower() in {"/quit", "exit"}: break

        intent = detect_intent({"patient_id": patient_id, "messages": [HumanMessage(content=user_input)]})
        chat_history.append(HumanMessage(content=user_input))

        response = await stream_response(patient, chat_history, intent, llm)
        from langchain_core.messages import AIMessage
        chat_history.append(AIMessage(content=response))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patient", "-p", default="P001")
    args = parser.parse_args()
    asyncio.run(run_cli(args.patient))


if __name__ == "__main__":
    main()
