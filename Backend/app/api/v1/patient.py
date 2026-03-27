"""
Patient Data Submission Routes
──────────────────────────────
Dedicated endpoints for structured data submission from the frontend.
(e.g., logging meals, exercise, symptoms, or mental health scores).
"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.db import repository as repo
from app.db.storage import storage_manager
from pydantic import BaseModel, Field
from datetime import date

router = APIRouter(prefix="/patient", tags=["Patient Data"])

# ─── Request Models ──────────────────────────────────────────────────────────

class SymptomSubmission(BaseModel):
    symptoms: list[str]
    notes: str | None = None

class NutritionLog(BaseModel):
    meals: list[dict] = Field(..., example=[{"meal": "breakfast", "food": "oats"}])
    calories: int
    adherence: bool = True
    notes: str | None = None

class FitnessLog(BaseModel):
    activity: str
    duration_minutes: int
    calories_burned: int | None = None
    notes: str | None = None

class MentalHealthScore(BaseModel):
    phq9_score: int = Field(..., ge=0, le=27)
    gad7_score: int = Field(..., ge=0, le=21)
    notes: str | None = None


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/{patient_id}/symptoms")
async def submit_symptoms(patient_id: str, data: SymptomSubmission):
    """Log symptoms directly to the triage history."""
    log = await repo.log_symptom_triage({
        "patient_id": patient_id,
        "symptoms": data.symptoms,
        "urgency_level": "medium", # Default, triage agent will refine later
        "triage_notes": data.notes or "User submitted via form",
        "is_emergency": False
    })
    return {"status": "success", "log_id": log.get("id")}


@router.post("/{patient_id}/nutrition")
async def log_nutrition(patient_id: str, data: NutritionLog):
    """Record daily nutrition data."""
    log = await repo.create_nutrition_log({
        "patient_id": patient_id,
        "log_date": date.today().isoformat(),
        "meals": data.meals,
        "calories": data.calories,
        "adherence": data.adherence,
        "notes": data.notes
    })
    return {"status": "success", "log_id": log.get("id")}


@router.post("/{patient_id}/fitness")
async def log_fitness(patient_id: str, data: FitnessLog):
    """Record exercise/activity data."""
    log = await repo.create_fitness_log({
        "patient_id": patient_id,
        "log_date": date.today().isoformat(),
        "activity": data.activity,
        "duration_minutes": data.duration_minutes,
        "calories_burned": data.calories_burned,
        "notes": data.notes
    })
    return {"status": "success", "log_id": log.get("id")}


@router.post("/{patient_id}/mental-health")
async def submit_mental_health(patient_id: str, data: MentalHealthScore):
    """Submit PHQ-9 or GAD-7 screening results."""
    risk = "low"
    if data.phq9_score > 10 or data.gad7_score > 10: risk = "moderate"
    if data.phq9_score > 15 or data.gad7_score > 15: risk = "high"
    
    log = await repo.create_mental_health_screening({
        "patient_id": patient_id,
        "phq9_score": data.phq9_score,
        "gad7_score": data.gad7_score,
        "risk_level": risk,
        "escalate": risk == "high"
    })
    return {"status": "success", "log_id": log.get("id"), "risk_level": risk}


@router.post("/{patient_id}/upload")
async def upload_document(patient_id: str, file: UploadFile = File(...)):
    """Upload a medical document (PDF, JPG, etc.) and store metadata."""
    content = await file.read()
    
    # Upload to Supabase Storage
    storage_res = await storage_manager.upload_file(
        file_bytes=content,
        file_name=file.filename,
        content_type=file.content_type or "application/octet-stream"
    )
    
    # Save to Database
    doc_res = await repo.log_patient_document({
        "patient_id": patient_id,
        "file_name": file.filename,
        "file_type": file.content_type,
        "bucket_name": storage_res["bucket"],
        "storage_path": storage_res["path"],
        "public_url": storage_res["url"],
        "metadata": {"size": len(content)}
    })
    
    return {
        "status": "success",
        "document_id": doc_res.get("id"),
        "url": storage_res["url"]
    }


@router.get("/{patient_id}/profile")
async def get_patient_profile(patient_id: str):
    """Retrieve full patient profile and history summary."""
    patient = repo.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    return {
        "profile": patient,
        "summary": {
            "appointments": await repo.get_appointments(patient_id),
            "care_plan": repo.get_care_plan(patient_id),
            "recent_triage": repo.get_triage_history(patient_id)
        }
    }
