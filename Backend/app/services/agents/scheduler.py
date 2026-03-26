"""
Booking / Appointment Scheduling Agent
───────────────────────────────────────
Checks real-time slot availability across clinics, books appointments based on
triage output, patient preferences, and doctor expertise.
"""
from __future__ import annotations
import uuid
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a medical appointment scheduling assistant. Your job is to:
1. Find available doctors matching the required specialty and preferred date.
2. Select the most suitable slot based on patient preferences.
3. Book the appointment and return confirmation details.
4. Always prefer same-day or next-day slots for high/emergency urgency.

Respond in JSON:
{
  "doctor_id": "<id>",
  "doctor_name": "<name>",
  "clinic_name": "<name>",
  "appointment_date": "<YYYY-MM-DD>",
  "slot_time": "<HH:MM>",
  "notes": "<any booking notes>"
}"""


@tool
def find_available_doctors(specialty: str, date: str) -> list:
    """Find doctors with the given specialty and check existing appointment load."""
    doctors = repo.list_doctors(specialty=specialty)
    booked = repo.get_doctor_availability(specialty, date)
    booked_ids = {b["doctor_id"] for b in booked}
    available = [d for d in doctors if d["id"] not in booked_ids]
    return available


@tool
def book_appointment(
    patient_id: str,
    doctor_id: str,
    specialty: str,
    appointment_date: str,
    slot_time: str,
    notes: str = "",
) -> dict:
    """Create an appointment record in Supabase."""
    return repo.create_appointment({
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "specialty": specialty,
        "appointment_date": appointment_date,
        "slot_time": slot_time,
        "status": "scheduled",
        "notes": notes,
    })


_agent = create_react_agent(get_llm(), tools=[find_available_doctors, book_appointment])


def run_booking_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Booking Agent and updates state."""
    patient_id = state["patient_id"]
    specialty = state.get("recommended_specialty", "general")
    preferred_date = state.get("preferred_date", datetime.now().strftime("%Y-%m-%d"))
    preferred_time = state.get("preferred_time", "")
    urgency = state.get("urgency_level", "low")

    prompt = f"""
Patient ID: {patient_id}
Required specialty: {specialty}
Preferred date: {preferred_date}
Preferred time: {preferred_time or 'any'}
Urgency: {urgency}

Find an available doctor and book the appointment.
"""
    result = _agent.invoke({
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
    })

    last_msg = result["messages"][-1].content
    parsed = extract_json(last_msg) or {}

    return {
        **state,
        "doctor_id": parsed.get("doctor_id", ""),
        "appointment_id": parsed.get("appointment_id", ""),
        "agent_response": last_msg,
        "intent": "booking",
    }
