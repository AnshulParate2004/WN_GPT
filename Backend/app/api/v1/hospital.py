"""
Hospital Operations API — bed management and inventory.
"""
from __future__ import annotations
from fastapi import APIRouter, Depends
from app.schemas.request_models import HospitalOpsRequest
from app.db import repository as repo
from app.api.deps import get_current_patient

router = APIRouter(prefix="/hospital", tags=["Hospital Operations"])


@router.get("/beds/{clinic_id}")
def list_beds(clinic_id: str):
    """List all beds for a clinic with their current status."""
    beds = repo.list_beds(clinic_id=clinic_id)
    available = sum(1 for b in beds if b.get("status") == "available")
    occupied = sum(1 for b in beds if b.get("status") == "occupied")
    return {"clinic_id": clinic_id, "beds": beds, "available": available, "occupied": occupied}


@router.patch("/beds/{bed_id}")
def update_bed(bed_id: str, status: str):
    """Update a specific bed's status."""
    return repo.update_bed_status(bed_id, status)


@router.get("/inventory/{clinic_id}")
def list_inventory(clinic_id: str):
    """List all inventory for a clinic, with low-stock alerts."""
    items = repo.list_inventory(clinic_id=clinic_id)
    low_stock = [i for i in items if i.get("quantity", 0) <= i.get("reorder_level", 0)]
    return {"inventory": items, "low_stock_count": len(low_stock), "low_stock_items": low_stock}
