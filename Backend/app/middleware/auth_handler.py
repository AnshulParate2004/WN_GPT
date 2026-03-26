"""
Auth middleware — validates the patient_id header or ABHA token on protected routes.
For the demo this is a simple API-key style check; integrate JWT / ABHA OAuth in prod.
"""
from __future__ import annotations
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.repository import get_patient


# Routes that do not require authentication
PUBLIC_PATHS = {"/", "/health", "/docs", "/openapi.json", "/redoc"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS or request.url.path.startswith("/docs"):
            return await call_next(request)

        patient_id = request.headers.get("X-Patient-ID")
        if not patient_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing X-Patient-ID header"},
            )

        # Lightweight DB check — patient must exist
        patient = get_patient(patient_id)
        if not patient:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Patient '{patient_id}' not found"},
            )

        # Attach patient to request state for downstream use
        request.state.patient = patient
        return await call_next(request)
