"""
Data models for clinical tables: Appointments, Triage Logs, Prescriptions,
Discharge Summaries, Mental Health Screenings, Care Plans.
"""
from __future__ import annotations
from pydantic import BaseModel
from typing import Any


class Appointment(BaseModel):
    id: str | None = None
    patient_id: str
    doctor_id: str
    specialty: str | None = None
    appointment_date: str
    slot_time: str
    status: str = "scheduled"
    notes: str | None = None


class SymptomLog(BaseModel):
    id: str | None = None
    patient_id: str
    symptoms: list[str]
    urgency_level: str
    recommended_specialty: str
    triage_notes: str
    is_emergency: bool = False
    created_at: str | None = None


class Prescription(BaseModel):
    id: str | None = None
    patient_id: str
    doctor_id: str
    medications: list[dict[str, Any]]
    dosage_instructions: str | None = None
    created_at: str | None = None


class DischargeSummary(BaseModel):
    id: str | None = None
    patient_id: str
    admission_date: str
    discharge_date: str
    diagnosis: str
    summary: str
    post_discharge_instructions: list[str] = []
    follow_up_appointment_id: str | None = None


class MentalHealthScreening(BaseModel):
    id: str | None = None
    patient_id: str
    phq9_score: int
    gad7_score: int
    risk_level: str
    coping_strategies: list[str] = []
    escalate: bool = False
    created_at: str | None = None


class CarePlan(BaseModel):
    id: str | None = None
    patient_id: str
    nutrition_plan: dict[str, Any] = {}
    fitness_plan: dict[str, Any] = {}
    preventive_care: list[str] = []
    created_at: str | None = None
    updated_at: str | None = None
