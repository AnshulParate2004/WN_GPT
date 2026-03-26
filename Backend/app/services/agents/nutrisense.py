"""
NutriSense Agent
────────────────
Tailors diet plans based on metabolic data, allergies, and ABHA records.
Tracks adherence and provides nutritional insights.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are the NutriSense AI. Your job is to:
1. Analyze the patient's metabolic data, allergies, and chronic conditions.
2. Generate a highly personalized nutrition plan (meal suggestions, calorie targets).
3. Provide insights on food-drug interactions if they are on specific medications.
4. Track adherence based on nutrition logs.

Respond in JSON:
{
  "nutrition_plan": {
    "daily_calories": <number>,
    "macros": {"protein": <g>, "carbs": <g>, "fat": <g>},
    "meal_plan": ["<breakfast>", "<lunch>", "<snack>", "<dinner>"],
    "restrictions": ["<restriction>"]
  },
  "adherence_summary": "<summary>",
  "metabolic_insights": "<insights>"
}"""


@tool
def get_nutrition_context(patient_id: str) -> dict:
    """Fetch patient profile, nutrition logs, and prescriptions for metabolic analysis."""
    patient = repo.get_patient(patient_id)
    logs = repo.get_nutrition_logs(patient_id)
    prescriptions = repo.get_prescriptions(patient_id)
    return {"patient": patient, "logs": logs, "prescriptions": prescriptions}


@tool
def save_nutrition_plan(patient_id: str, plan: dict) -> dict:
    """Save the updated nutrition plan to the care_plans table."""
    existing = repo.get_care_plan(patient_id) or {}
    return repo.upsert_care_plan({
        "patient_id": patient_id,
        "nutrition_plan": plan,
        "fitness_plan": existing.get("fitness_plan", {}),
        "preventive_care": existing.get("preventive_care", [])
    })


_agent = create_react_agent(get_llm(), tools=[get_nutrition_context, save_nutrition_plan])


def run_nutrisense_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs NutriSense Agent."""
    patient_id = state["patient_id"]
    msgs = state.get("messages", [])
    ctx = msgs[-1].content if msgs else "Assess my nutrition"

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
        "nutrition_plan": parsed.get("nutrition_plan", {}),
        "agent_response": last_msg,
        "intent": "nutrisense",
    }
