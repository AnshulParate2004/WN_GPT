"""
Health Records API — ABDM/ABHA pull and patient record management.
"""
from __future__ import annotations
from fastapi import APIRouter, Depends
from app.schemas.request_models import HealthRecordRequest
from app.db import repository as repo
from app.services.external_apis import fetch_abdm_records
from app.api.deps import get_current_patient

router = APIRouter(prefix="/health-records", tags=["Health Records"])


@router.get("/{patient_id}")
def get_patient_records(patient_id: str, patient: dict = Depends(get_current_patient)):
    """Get full patient profile + appointment history + triage logs."""
    return {
        "patient": repo.get_patient(patient_id),
        "appointments": repo.get_appointments_for_patient(patient_id),
        "triage_history": repo.get_triage_history(patient_id),
        "prescriptions": repo.get_prescriptions(patient_id),
        "care_plan": repo.get_care_plan(patient_id),
    }


@router.post("/abdm-pull")
async def pull_abdm_records(body: HealthRecordRequest, patient: dict = Depends(get_current_patient)):
    """Pull ABDM records via ABHA ID."""
    if not body.abha_id:
        return {"records": [], "message": "No ABHA ID provided"}
    records = await fetch_abdm_records(body.abha_id)
    return {"records": records, "count": len(records)}
