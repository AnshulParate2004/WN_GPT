"""
Mental Health Agent
────────────────────
Screens for mental health conditions using PHQ-9 / GAD-7,
suggests coping strategies, and escalates to specialists when needed.
"""
from __future__ import annotations
import uuid
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json, normalize_risk, safe_int
from app.db import repository as repo

SYSTEM_PROMPT = """You are a compassionate mental health AI assistant. Your responsibilities:
1. Analyze PHQ-9 (depression) and GAD-7 (anxiety) questionnaire responses.
2. Calculate total scores and determine risk level (low/moderate/high).
3. Suggest evidence-based coping strategies appropriate for the risk level.
4. Decide if escalation to a human psychiatrist/psychologist is needed.
5. Use a warm, empathetic tone — never be clinical or cold.

PHQ-9 scoring: 0-4 minimal, 5-9 mild, 10-14 moderate, 15-19 moderately severe, 20+ severe.
GAD-7 scoring: 0-4 minimal, 5-9 mild, 10-14 moderate, 15+ severe.

Respond in JSON:
{
  "phq9_score": <0-27>,
  "gad7_score": <0-21>,
  "risk_level": "<low|moderate|high>",
  "coping_strategies": ["<strategy>"],
  "escalate_to_specialist": <true|false>,
  "message_to_patient": "<warm supportive message>"
}"""


@tool
def get_mental_health_history(patient_id: str) -> list:
    """Fetch past mental health screening results."""
    return repo.get_mental_health_history(patient_id)


@tool
def save_screening(
    patient_id: str,
    phq9_score: int,
    gad7_score: int,
    risk_level: str,
    coping_strategies: list,
    escalate: bool,
) -> dict:
    """Save mental health screening result to Supabase."""
    return repo.create_mental_health_screening({
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "phq9_score": phq9_score,
        "gad7_score": gad7_score,
        "risk_level": risk_level,
        "coping_strategies": coping_strategies,
        "escalate": escalate,
    })


_agent = create_react_agent(get_llm(), tools=[get_mental_health_history, save_screening])


def run_mental_health_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Mental Health Screening Agent."""
    patient_id = state["patient_id"]
    phq9 = safe_int(state.get("phq9_score", 0))
    gad7 = safe_int(state.get("gad7_score", 0))
    messages = state.get("messages", [])
    context = messages[-1] if messages else ""

    prompt = f"""
Patient ID: {patient_id}
PHQ-9 total score provided: {phq9}
GAD-7 total score provided: {gad7}
Additional context: {context}

Fetch screening history, assess risk level, suggest coping strategies,
and save the screening result.
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
        "phq9_score": safe_int(parsed.get("phq9_score", phq9)),
        "gad7_score": safe_int(parsed.get("gad7_score", gad7)),
        "mental_health_risk": normalize_risk(parsed.get("risk_level", "low")),
        "coping_strategies": parsed.get("coping_strategies", []),
        "escalate_to_specialist": bool(parsed.get("escalate_to_specialist", False)),
        "agent_response": last_msg,
        "intent": "mental_health",
    }
