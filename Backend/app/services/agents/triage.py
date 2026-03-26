"""
Symptom Triage Agent
────────────────────
Analyzes patient-reported symptoms, assesses urgency (low/medium/high/emergency),
flags emergencies, and recommends the appropriate medical specialty.
Uses patient history from Supabase HealthMem (symptoms_logs table).
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json, normalize_urgency
from app.db import repository as repo

SYSTEM_PROMPT = """You are a clinical triage AI assistant. Your job is to:
1. Analyze the reported symptoms carefully.
2. Determine urgency: low | medium | high | emergency
3. Recommend the appropriate medical specialty.
4. Flag life-threatening situations immediately.
5. Consider the patient's history (chronic conditions, allergies, past triage logs).

Always respond in JSON format:
{
  "urgency_level": "<low|medium|high|emergency>",
  "is_emergency": <true|false>,
  "recommended_specialty": "<specialty>",
  "triage_notes": "<detailed clinical reasoning>"
}"""


@tool
def get_patient_history(patient_id: str) -> dict:
    """Fetch patient demographics and recent triage history."""
    patient = repo.get_patient(patient_id)
    history = repo.get_triage_history(patient_id)
    return {"patient": patient, "recent_triage": history}


@tool
def save_triage_result(
    patient_id: str,
    symptoms: list,
    urgency_level: str,
    recommended_specialty: str,
    triage_notes: str,
    is_emergency: bool,
) -> dict:
    """Persist the triage result to Supabase symptoms_logs table."""
    return repo.log_symptom_triage({
        "patient_id": patient_id,
        "symptoms": symptoms,
        "urgency_level": urgency_level,
        "recommended_specialty": recommended_specialty,
        "triage_notes": triage_notes,
        "is_emergency": is_emergency,
    })


_agent = create_react_agent(get_llm(), tools=[get_patient_history, save_triage_result])


def run_triage_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Symptom Triage Agent and updates state."""
    patient_id = state["patient_id"]
    symptoms = state.get("symptoms", [])
    text = state.get("messages", [{}])[-1] if state.get("messages") else ""

    prompt = f"""
Patient ID: {patient_id}
Reported symptoms: {', '.join(symptoms)}
Patient message: {text}

Fetch patient history, analyze symptoms, and save the triage result.
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
        "urgency_level": normalize_urgency(parsed.get("urgency_level", "low")),
        "is_emergency": bool(parsed.get("is_emergency", False)),
        "recommended_specialty": parsed.get("recommended_specialty", "general"),
        "triage_notes": parsed.get("triage_notes", last_msg),
        "agent_response": last_msg,
        "intent": "triage",
    }
