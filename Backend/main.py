"""
FastAPI Application Entry Point — WellnessGPT Backend
"""
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.middleware.auth_handler import AuthMiddleware
from app.api.v1 import chat, health_records, hospital
from app.core.graph_factory import get_graph   # pre-warm on startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-compile the LangGraph state machine on startup
    get_graph()
    print("✅ WellnessGPT LangGraph state machine compiled and ready.")
    yield


settings = get_settings()

app = FastAPI(
    title="WellnessGPT API",
    description="14-Agent Healthcare AI Backend powered by LangGraph + Azure OpenAI + Supabase",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Patient Auth Middleware
app.add_middleware(AuthMiddleware)

# ── Routers ──────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"
app.include_router(chat.router, prefix=API_PREFIX)
app.include_router(health_records.router, prefix=API_PREFIX)
app.include_router(hospital.router, prefix=API_PREFIX)


# ── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "WellnessGPT API", "version": "1.0.0"}


@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to WellnessGPT API",
        "docs": "/docs",
        "agents": [
            "Symptom Triage", "Booking/Scheduling", "Patient Channeling",
            "Follow-Up/Adherence", "Care Plan Management", "Discharge",
            "Claims/Insurance", "Hospital Operations", "NutriSense",
            "FitGuide", "Pharmacy", "Mental Health", "Family Care",
            "Product Recommendation",
        ],
    }
