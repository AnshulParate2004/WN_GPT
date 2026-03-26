"""
FitGuide Agent
──────────────
Builds fitness routines from health profiles and wearable sync.
Monitors progress and adapts routines to metabolic/health data.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are the FitGuide AI. Your job is to:
1. Review the patient's fitness level, chronic conditions (e.g., heart issues, RA), and wearable data.
2. Build a safe, effective fitness routine.
3. Monitor progress from fitness logs and wearable sync.
4. Provide motivation and adaptation based on performance.

Respond in JSON:
{
  "fitness_plan": {
    "weekly_frequency": <int>,
    "exercises": [{"name": "<>", "duration": "<>", "intensity": "<>"}],
    "recovery_tips": ["<>"]
  },
  "progress_assessment": "<assessment>",
  "safety_notes": "<critical safety reminders>"
}"""


@tool
def get_fitness_context(patient_id: str) -> dict:
    """Fetch patient profile, fitness logs, and wearable data for exercise routine tailoring."""
    patient = repo.get_patient(patient_id)
    logs = repo.get_fitness_logs(patient_id)
    wearable = repo.get_wearable_data(patient_id)
    return {"patient": patient, "logs": logs, "wearable": wearable}


@tool
def save_fitness_plan(patient_id: str, plan: dict) -> dict:
    """Save the updated fitness plan to the care_plans table."""
    existing = repo.get_care_plan(patient_id) or {}
    return repo.upsert_care_plan({
        "patient_id": patient_id,
        "fitness_plan": plan,
        "nutrition_plan": existing.get("nutrition_plan", {}),
        "preventive_care": existing.get("preventive_care", [])
    })


_agent = create_react_agent(get_llm(), tools=[get_fitness_context, save_fitness_plan])


def run_fitguide_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs FitGuide Agent."""
    patient_id = state["patient_id"]
    msgs = state.get("messages", [])
    ctx = msgs[-1].content if msgs else "Update my fitness routine"

    result = _agent.invoke({
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Patient: {patient_id}\nRequest: {ctx}")
        ]
    })

    last_msg = result["messages"][-1].content
    parsed = extract_json(last_msg) or {}

    return {
        **state,
        "fitness_plan": parsed.get("fitness_plan", {}),
        "agent_response": last_msg,
        "intent": "fitguide",
    }
