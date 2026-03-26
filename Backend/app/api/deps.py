"""
FastAPI dependency injectors shared across all route handlers.
"""
from __future__ import annotations
from fastapi import Header, HTTPException, Request, status
from app.db.supabase import get_supabase
from supabase import Client


def get_db() -> Client:
    """Inject the Supabase client."""
    return get_supabase()


def get_current_patient(request: Request) -> dict:
    """Return the authenticated patient attached by AuthMiddleware."""
    patient = getattr(request.state, "patient", None)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return patient
