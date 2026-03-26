"""
Data models for hospital operations: Beds, Inventory, Insurance Claims.
"""
from __future__ import annotations
from pydantic import BaseModel
from typing import Any


class HospitalBed(BaseModel):
    id: str | None = None
    clinic_id: str
    ward: str
    bed_number: str
    status: str = "available"   # "available" | "occupied" | "maintenance"
    patient_id: str | None = None


class InventoryItem(BaseModel):
    id: str | None = None
    clinic_id: str
    item_name: str
    category: str
    quantity: int
    reorder_level: int
    unit: str = "units"
    last_updated: str | None = None


class InsuranceClaim(BaseModel):
    id: str | None = None
    patient_id: str
    policy_number: str
    insurer: str
    diagnosis: str
    treatment_cost: float
    coverage_amount: float
    coverage_gaps: list[str] = []
    wellness_score: float = 0.0
    status: str = "pending"
    created_at: str | None = None
