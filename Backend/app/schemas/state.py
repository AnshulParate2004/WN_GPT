"""
AgentState — the single global memory / state TypedDict shared across
all LangGraph nodes in the WellnessGPT state machine.
"""
from __future__ import annotations
from typing import Annotated, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    # ── Routing ──────────────────────────────────────────────────────────────
    intent: str               # detected intent: "triage", "book", "care_plan", …
    agent_response: str       # final text response to return to the caller

    # ── Session / Identity ───────────────────────────────────────────────────
    patient_id: str
    abha_id: str
    family_id: str
    session_id: str

    # ── Conversation History (append-only via add_messages) ──────────────────
    messages: Annotated[list, add_messages]

    # ── Triage ───────────────────────────────────────────────────────────────
    symptoms: list[str]
    urgency_level: str        # "low" | "medium" | "high" | "emergency"
    recommended_specialty: str
    triage_notes: str
    is_emergency: bool

    # ── Booking ───────────────────────────────────────────────────────────────
    preferred_date: str
    preferred_time: str
    doctor_id: str
    appointment_id: str
    available_slots: list[dict]

    # ── Care Plan ─────────────────────────────────────────────────────────────
    care_plan: dict[str, Any]
    nutrition_plan: dict[str, Any]
    fitness_plan: dict[str, Any]

    # ── Discharge ─────────────────────────────────────────────────────────────
    discharge_summary: dict[str, Any]
    post_discharge_instructions: list[str]

    # ── Insurance / Claims ────────────────────────────────────────────────────
    policy_details: dict[str, Any]
    coverage_gaps: list[str]
    claim_form: dict[str, Any]
    wellness_score: float

    # ── Hospital Ops ──────────────────────────────────────────────────────────
    clinic_id: str
    bed_status: list[dict]
    inventory_status: list[dict]

    # ── Pharmacy ──────────────────────────────────────────────────────────────
    medications: list[dict]
    drug_interactions: list[str]
    refill_needed: bool

    # ── Mental Health ─────────────────────────────────────────────────────────
    phq9_score: int
    gad7_score: int
    mental_health_risk: str   # "low" | "moderate" | "high"
    coping_strategies: list[str]
    escalate_to_specialist: bool

    # ── Nutrition / Fitness logs ──────────────────────────────────────────────
    nutrition_logs: list[dict]
    fitness_logs: list[dict]
    wearable_data: list[dict]

    # ── Product Recommendations ───────────────────────────────────────────────
    recommended_products: list[dict]

    # ── Family Care ───────────────────────────────────────────────────────────
    family_members: list[dict]
    family_insights: str

    # ── Reminders / Follow-up ─────────────────────────────────────────────────
    pending_reminders: list[dict]
    reminder_id: str

    # ── External / ABDM ───────────────────────────────────────────────────────
    abdm_records: list[dict]

    # ── Errors / Metadata ─────────────────────────────────────────────────────
    error: str | None
    metadata: dict[str, Any]
