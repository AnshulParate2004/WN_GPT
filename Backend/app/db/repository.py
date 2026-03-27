"""
Repository: Clean async CRUD helpers for all Supabase tables.
All functions return plain dicts or lists – no Supabase response objects leak out.
"""
from __future__ import annotations
from typing import Any
from app.db.supabase import get_supabase


# ─────────────────────────── Patients ────────────────────────────────────────

def get_patient(patient_id: str) -> dict | None:
    res = get_supabase().table("patients").select("*").eq("id", patient_id).single().execute()
    return res.data


def list_patients() -> list[dict]:
    res = get_supabase().table("patients").select("*").execute()
    return res.data or []


def get_patient_by_abha(abha_id: str) -> dict | None:
    res = get_supabase().table("patients").select("*").eq("abha_id", abha_id).single().execute()
    return res.data


def get_family_members(family_id: str) -> list[dict]:
    res = get_supabase().table("family_groups").select("patient_id").eq("family_id", family_id).execute()
    ids = [r["patient_id"] for r in (res.data or [])]
    if not ids:
        return []
    members = get_supabase().table("patients").select("*").in_("id", ids).execute()
    return members.data or []


# ─────────────────────────── Appointments ─────────────────────────────────────

def get_doctor_availability(specialty: str, date: str) -> list[dict]:
    res = (
        get_supabase()
        .table("appointments")
        .select("doctor_id, slot_time, status")
        .eq("specialty", specialty)
        .eq("appointment_date", date)
        .execute()
    )
    return res.data or []


def list_doctors(specialty: str | None = None) -> list[dict]:
    q = get_supabase().table("doctors").select("*")
    if specialty:
        q = q.eq("specialty", specialty)
    return q.execute().data or []


def create_appointment(data: dict) -> dict:
    res = get_supabase().table("appointments").insert(data).execute()
    return res.data[0] if res.data else {}


def get_appointments_for_patient(patient_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("appointments")
        .select("*, doctors(name, specialty)")
        .eq("patient_id", patient_id)
        .execute()
    )
    return res.data or []


# ─────────────────────────── Symptoms / Triage ────────────────────────────────

def log_symptom_triage(data: dict) -> dict:
    res = get_supabase().table("symptoms_logs").insert(data).execute()
    return res.data[0] if res.data else {}


def get_triage_history(patient_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("symptoms_logs")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(10)
        .execute()
    )
    return res.data or []


# ─────────────────────────── Care Plans ───────────────────────────────────────

def get_care_plan(patient_id: str) -> dict | None:
    res = (
        get_supabase()
        .table("care_plans")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


def upsert_care_plan(data: dict) -> dict:
    res = get_supabase().table("care_plans").upsert(data).execute()
    return res.data[0] if res.data else {}


# ─────────────────────────── Prescriptions ───────────────────────────────────

def get_prescriptions(patient_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("prescriptions")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def create_prescription(data: dict) -> dict:
    res = get_supabase().table("prescriptions").insert(data).execute()
    return res.data[0] if res.data else {}


# ─────────────────────────── Discharge ───────────────────────────────────────

def create_discharge_summary(data: dict) -> dict:
    res = get_supabase().table("discharge_summaries").insert(data).execute()
    return res.data[0] if res.data else {}


def get_discharge_summary(patient_id: str) -> dict | None:
    res = (
        get_supabase()
        .table("discharge_summaries")
        .select("*")
        .eq("patient_id", patient_id)
        .order("discharge_date", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


# ─────────────────────────── Insurance Claims ────────────────────────────────

def get_claim(patient_id: str) -> dict | None:
    res = (
        get_supabase()
        .table("insurance_claims")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


def create_claim(data: dict) -> dict:
    res = get_supabase().table("insurance_claims").insert(data).execute()
    return res.data[0] if res.data else {}


def update_claim_status(claim_id: str, status: str) -> dict:
    res = (
        get_supabase()
        .table("insurance_claims")
        .update({"status": status})
        .eq("id", claim_id)
        .execute()
    )
    return res.data[0] if res.data else {}


# ─────────────────────────── Hospital Ops ────────────────────────────────────

def list_beds(clinic_id: str | None = None, status: str | None = None) -> list[dict]:
    q = get_supabase().table("hospital_beds").select("*")
    if clinic_id:
        q = q.eq("clinic_id", clinic_id)
    if status:
        q = q.eq("status", status)
    return q.execute().data or []


def update_bed_status(bed_id: str, status: str) -> dict:
    res = (
        get_supabase()
        .table("hospital_beds")
        .update({"status": status})
        .eq("id", bed_id)
        .execute()
    )
    return res.data[0] if res.data else {}


def list_inventory(clinic_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("inventory")
        .select("*")
        .eq("clinic_id", clinic_id)
        .execute()
    )
    return res.data or []


# ─────────────────────────── Reminders ───────────────────────────────────────

def create_reminder(data: dict) -> dict:
    res = get_supabase().table("followup_reminders").insert(data).execute()
    return res.data[0] if res.data else {}


def get_pending_reminders(patient_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("followup_reminders")
        .select("*")
        .eq("patient_id", patient_id)
        .eq("status", "pending")
        .execute()
    )
    return res.data or []


# ─────────────────────────── Mental Health ───────────────────────────────────

def create_mental_health_screening(data: dict) -> dict:
    res = get_supabase().table("mental_health_screenings").insert(data).execute()
    return res.data[0] if res.data else {}


def get_mental_health_history(patient_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("mental_health_screenings")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )
    return res.data or []


# ─────────────────────────── Nutrition / Fitness ─────────────────────────────

def log_nutrition(data: dict) -> dict:
    res = get_supabase().table("nutrition_logs").insert(data).execute()
    return res.data[0] if res.data else {}


def get_nutrition_logs(patient_id: str, limit: int = 7) -> list[dict]:
    res = (
        get_supabase()
        .table("nutrition_logs")
        .select("*")
        .eq("patient_id", patient_id)
        .order("log_date", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def log_fitness(data: dict) -> dict:
    res = get_supabase().table("fitness_logs").insert(data).execute()
    return res.data[0] if res.data else {}


def get_fitness_logs(patient_id: str, limit: int = 7) -> list[dict]:
    res = (
        get_supabase()
        .table("fitness_logs")
        .select("*")
        .eq("patient_id", patient_id)
        .order("log_date", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def get_wearable_data(patient_id: str) -> list[dict]:
    res = (
        get_supabase()
        .table("wearable_data")
        .select("*")
        .eq("patient_id", patient_id)
        .order("recorded_at", desc=True)
        .limit(10)
        .execute()
    )
    return res.data or []


# ─────────────────────────── Product Catalog ─────────────────────────────────

def search_products(tags: list[str]) -> list[dict]:
    q = get_supabase().table("product_catalog").select("*")
    if tags:
        q = q.overlaps("tags", tags)
    return q.execute().data or []


async def log_patient_document(doc_data: dict) -> dict:
    """Register an uploaded document (PDF/Image) in the patient_documents table."""
    res = get_supabase().table("patient_documents").insert(doc_data).execute()
    return res.data[0] if res.data else {}
