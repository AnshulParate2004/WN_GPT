"""
Patient Channeling Agent
─────────────────────────
Applies symptom-to-specialty mapping logic to route patients to the
correct department. Integrates ABDM record pulls for prior history.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SPECIALTY_MAP = {
    "chest pain": "cardiology",
    "heart": "cardiology",
    "breathing": "pulmonology",
    "cough": "pulmonology",
    "skin": "dermatology",
    "rash": "dermatology",
    "bone": "orthopedics",
    "joint": "orthopedics",
    "stomach": "gastroenterology",
    "abdomen": "gastroenterology",
    "brain": "neurology",
    "headache": "neurology",
    "eye": "ophthalmology",
    "ear": "ent",
    "mental": "psychiatry",
    "anxiety": "psychiatry",
    "depression": "psychiatry",
    "diabetes": "endocrinology",
    "thyroid": "endocrinology",
    "children": "pediatrics",
    "child": "pediatrics",
    "pregnancy": "gynecology",
    "urine": "urology",
    "kidney": "nephrology",
}

SYSTEM_PROMPT = """You are a patient channeling AI. Your job is to:
1. Map symptoms to the most appropriate medical specialty.
2. Pull ABDM/prior records to check for established specialist relationships.
3. Route the patient to the right department.

Respond in JSON:
{
  "recommended_specialty": "<specialty>",
  "routing_reason": "<explanation>",
  "priority": "<routine|urgent|emergency>"
}"""


@tool
def map_symptoms_to_specialty(symptoms: list) -> str:
    """Rule-based pre-mapping of symptoms to specialty before LLM refinement."""
    syms_lower = " ".join(symptoms).lower()
    for keyword, specialty in SPECIALTY_MAP.items():
        if keyword in syms_lower:
            return specialty
    return "general_medicine"


@tool
def fetch_abdm_records(patient_id: str) -> dict:
    """Fetch ABDM/prior health records for the patient from Supabase."""
    patient = repo.get_patient(patient_id)
    triage_history = repo.get_triage_history(patient_id)
    appointments = repo.get_appointments_for_patient(patient_id)
    return {
        "patient_profile": patient,
        "triage_history": triage_history[:3],
        "past_appointments": appointments[:3],
    }


_agent = create_react_agent(get_llm(), tools=[map_symptoms_to_specialty, fetch_abdm_records])


def run_channeling_agent(state: AgentState) -> AgentState:
    """LangGraph node: routes patient to the correct specialty."""
    patient_id = state["patient_id"]
    symptoms = state.get("symptoms", [])

    prompt = f"""
Patient ID: {patient_id}
Symptoms: {', '.join(symptoms)}

First apply the symptom-to-specialty mapping, then fetch ABDM records
and determine the best specialty routing with priority level.
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
        "recommended_specialty": parsed.get("recommended_specialty", "general_medicine"),
        "agent_response": last_msg,
        "intent": "channeling",
    }
