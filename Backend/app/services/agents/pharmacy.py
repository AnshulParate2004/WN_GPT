"""
Pharmacy Agent
───────────────
Recommends medications/dosages, checks drug interactions,
and handles refill requests via linked patient records.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a clinical pharmacy AI assistant. Your responsibilities:
1. Review current medications for drug-drug interactions.
2. Check for contraindications given patient allergies and conditions.
3. Recommend appropriate medications and dosages.
4. Identify refill needs based on prescription history.

Always prioritize patient safety — flag any dangerous interactions immediately.

Respond in JSON:
{
  "recommendations": ["<medication recommendation>"],
  "drug_interactions": ["<interaction description>"],
  "refill_needed": <true|false>,
  "safety_alerts": ["<alert>"],
  "dosage_notes": "<notes>"
}"""


@tool
def get_current_medications(patient_id: str) -> dict:
    """Fetch all active prescriptions and patient allergy profile."""
    patient = repo.get_patient(patient_id)
    prescriptions = repo.get_prescriptions(patient_id)
    return {
        "allergies": patient.get("allergies", []) if patient else [],
        "chronic_conditions": patient.get("chronic_conditions", []) if patient else [],
        "prescriptions": prescriptions,
    }


@tool
def check_interactions(medications: list) -> str:
    """
    Placeholder for real drug interaction API.
    Returns a description of known interactions for the given medication list.
    In production, integrate with DrFirst, Surescripts, or similar.
    """
    if not medications:
        return "No medications provided."
    names = [m.get("name", str(m)) if isinstance(m, dict) else str(m) for m in medications]
    return f"Interaction check requested for: {', '.join(names)}. Please use clinical judgment."


_agent = create_react_agent(get_llm(), tools=[get_current_medications, check_interactions])


def run_pharmacy_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Pharmacy Agent."""
    patient_id = state["patient_id"]
    messages = state.get("messages", [])
    query = messages[-1] if messages else "Review medications and check interactions"

    prompt = f"""
Patient ID: {patient_id}
Pharmacy query: {query}

Fetch current medications, check for interactions, and provide recommendations.
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
        "drug_interactions": parsed.get("drug_interactions", []),
        "refill_needed": bool(parsed.get("refill_needed", False)),
        "agent_response": last_msg,
        "intent": "pharmacy",
    }
