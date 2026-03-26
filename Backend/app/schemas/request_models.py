"""
Pydantic models for all API request/response payloads.
"""
from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


# ─── Generic ─────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    patient_id: str
    session_id: str | None = None
    message: str
    intent: str | None = None          # optional override; graph will detect automatically


class ChatResponse(BaseModel):
    patient_id: str
    session_id: str
    intent: str
    response: str
    metadata: dict[str, Any] = {}


# ─── Triage ──────────────────────────────────────────────────────────────────

class TriageRequest(BaseModel):
    patient_id: str
    symptoms: list[str]
    text_input: str | None = None


class TriageResponse(BaseModel):
    urgency_level: str
    is_emergency: bool
    recommended_specialty: str
    triage_notes: str


# ─── Booking ─────────────────────────────────────────────────────────────────

class BookingRequest(BaseModel):
    patient_id: str
    specialty: str
    preferred_date: str           # YYYY-MM-DD
    preferred_time: str | None = None
    doctor_id: str | None = None


class BookingResponse(BaseModel):
    appointment_id: str
    doctor_name: str
    clinic_name: str
    slot_time: str
    status: str


# ─── Care Plan ───────────────────────────────────────────────────────────────

class CarePlanRequest(BaseModel):
    patient_id: str
    feedback: str | None = None   # patient feedback to update plan


class CarePlanResponse(BaseModel):
    patient_id: str
    nutrition_plan: dict[str, Any]
    fitness_plan: dict[str, Any]
    preventive_care: list[str]


# ─── Discharge ───────────────────────────────────────────────────────────────

class DischargeRequest(BaseModel):
    patient_id: str
    admission_date: str
    discharge_date: str
    diagnosis: str
    treating_doctor_id: str


class DischargeResponse(BaseModel):
    summary: str
    post_discharge_instructions: list[str]
    follow_up_appointment_id: str | None = None
    insurance_claim_id: str | None = None


# ─── Claims ──────────────────────────────────────────────────────────────────

class ClaimsRequest(BaseModel):
    patient_id: str
    diagnosis: str
    treatment_cost: float


class ClaimsResponse(BaseModel):
    claim_id: str
    coverage_amount: float
    coverage_gaps: list[str]
    wellness_score: float
    status: str


# ─── Hospital Ops ────────────────────────────────────────────────────────────

class HospitalOpsRequest(BaseModel):
    clinic_id: str
    action: str              # "list_beds" | "update_bed" | "list_inventory"
    bed_id: str | None = None
    bed_status: str | None = None


# ─── Pharmacy ────────────────────────────────────────────────────────────────

class PharmacyRequest(BaseModel):
    patient_id: str
    query: str               # e.g. "check interactions for metformin + aspirin"


class PharmacyResponse(BaseModel):
    recommendations: list[str]
    drug_interactions: list[str]
    refill_needed: bool


# ─── Mental Health ───────────────────────────────────────────────────────────

class MentalHealthRequest(BaseModel):
    patient_id: str
    responses: dict[str, int]    # PHQ-9 / GAD-7 question → score


class MentalHealthResponse(BaseModel):
    phq9_score: int
    gad7_score: int
    risk_level: str
    coping_strategies: list[str]
    escalate: bool


# ─── NutriSense ──────────────────────────────────────────────────────────────

class NutriSenseRequest(BaseModel):
    patient_id: str
    feedback: str | None = None


# ─── FitGuide ────────────────────────────────────────────────────────────────

class FitGuideRequest(BaseModel):
    patient_id: str
    goal: str | None = None       # e.g. "weight loss", "strength"


# ─── Family Care ─────────────────────────────────────────────────────────────

class FamilyCareRequest(BaseModel):
    family_id: str


# ─── Product Recommendation ──────────────────────────────────────────────────

class ProductRecRequest(BaseModel):
    patient_id: str


# ─── Health Records (ABDM) ───────────────────────────────────────────────────

class HealthRecordRequest(BaseModel):
    patient_id: str
    abha_id: str | None = None
