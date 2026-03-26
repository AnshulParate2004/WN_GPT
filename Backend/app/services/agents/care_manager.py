"""
Care Plan Management Agent
───────────────────────────
Generates and updates personalized care plans (nutrition, fitness, preventive care)
using EHR trends, patient feedback, and wearable data.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a personalized care plan AI. Your job is to:
1. Review the patient's health profile, wearable data, and existing care plan.
2. Generate or update a comprehensive care plan including:
   - Nutrition: specific meal recommendations, calorie targets, restrictions
   - Fitness: exercise routine tailored to condition and fitness level
   - Preventive care: vaccinations, screenings, lifestyle changes
3. Incorporate patient feedback to adjust the plan.

Respond in JSON:
{
  "nutrition_plan": {
    "daily_calories": <number>,
    "meals": ["<meal description>"],
    "restrictions": ["<restriction>"],
    "hydration_goal_liters": <number>
  },
  "fitness_plan": {
    "weekly_sessions": <number>,
    "session_duration_minutes": <number>,
    "recommended_activities": ["<activity>"],
    "intensity": "<low|moderate|high>"
  },
  "preventive_care": ["<recommendation>"],
  "summary": "<brief overview>"
}"""


@tool
def get_patient_health_profile(patient_id: str) -> dict:
    """Fetch full health profile: demographics, wearables, nutrition, fitness, existing plan."""
    patient = repo.get_patient(patient_id)
    care_plan = repo.get_care_plan(patient_id)
    wearable = repo.get_wearable_data(patient_id)
    nutrition = repo.get_nutrition_logs(patient_id)
    fitness = repo.get_fitness_logs(patient_id)
    return {
        "patient": patient,
        "existing_care_plan": care_plan,
        "wearable_data": wearable[:5],
        "nutrition_logs": nutrition[:7],
        "fitness_logs": fitness[:7],
    }


@tool
def save_care_plan(patient_id: str, nutrition_plan: dict, fitness_plan: dict, preventive_care: list) -> dict:
    """Upsert the care plan in Supabase."""
    return repo.upsert_care_plan({
        "patient_id": patient_id,
        "nutrition_plan": nutrition_plan,
        "fitness_plan": fitness_plan,
        "preventive_care": preventive_care,
    })


_agent = create_react_agent(get_llm(), tools=[get_patient_health_profile, save_care_plan])


def run_care_manager_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Care Plan Management Agent."""
    patient_id = state["patient_id"]
    feedback = state.get("messages", [])[-1] if state.get("messages") else "No feedback"

    prompt = f"""
Patient ID: {patient_id}
Patient feedback: {feedback}

Fetch the health profile, generate an updated care plan, and save it.
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
        "care_plan": parsed,
        "nutrition_plan": parsed.get("nutrition_plan", {}),
        "fitness_plan": parsed.get("fitness_plan", {}),
        "agent_response": last_msg,
        "intent": "care_plan",
    }
