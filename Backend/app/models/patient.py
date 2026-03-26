"""
Data models for Patient & HealthMem tables (used for IDE type-hints, not ORM).
"""
from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field
from typing import Any


class Patient(BaseModel):
    id: str
    name: str
    dob: date
    gender: str
    blood_group: str
    allergies: list[str] = []
    chronic_conditions: list[str] = []
    abha_id: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    family_id: str | None = None
    created_at: str | None = None


class Doctor(BaseModel):
    id: str
    name: str
    specialty: str
    clinic_id: str
    qualification: str | None = None
    available_days: list[str] = []
    available_times: list[str] = []


class Clinic(BaseModel):
    id: str
    name: str
    location: str
    departments: list[str] = []
    contact: str | None = None


class FamilyGroup(BaseModel):
    family_id: str
    patient_id: str
