"""Per-intent system prompts used by the CLI (display layer only)."""
from __future__ import annotations

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


def system_prompt_for(intent: str) -> str:
    return AGENT_SYSTEM_PROMPTS.get(intent, AGENT_SYSTEM_PROMPTS["general"])


def patient_context(patient: dict) -> str:
    return (
        f"Patient: {patient.get('name', 'Unknown')} | "
        f"Conditions: {patient.get('chronic_conditions')} | "
        f"Allergies: {patient.get('allergies')}"
    )
