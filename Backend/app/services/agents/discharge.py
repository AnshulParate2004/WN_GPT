"""
Discharge Agent
───────────────
Summarizes hospital stay, provides post-discharge instructions,
recommends follow-up, and prepares insurance claims if needed.
"""
from __future__ import annotations
import uuid
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a hospital discharge AI. Your job is to:
1. Summarize the patient's hospital stay based on clinical notes.
2. Provide clear, actionable post-discharge instructions (meds, diet, activity).
3. Schedule/recommend a follow-up appointment date.
4. Flag any insurance coverage gaps for the visit.

Always respond in JSON format:
{
  "summary": "<stay summary>",
  "instructions": ["<step 1>", "<step 2>"],
  "follow_up_days": <int>,
  "diagnosis": "<final diagnosis>"
}"""


@tool
def get_discharge_context(patient_id: str) -> dict:
    """Fetch patient profile, prescriptions, and current visit notes for discharge processing."""
    patient = repo.get_patient(patient_id)
    prescriptions = repo.get_prescriptions(patient_id)
    return {"patient": patient, "recent_prescriptions": prescriptions}


@tool
def save_discharge_summary(
    patient_id: str,
    admission_date: str,
    discharge_date: str,
    diagnosis: str,
    summary: str,
    instructions: list[str],
) -> dict:
    """Persist the formal discharge summary to the database."""
    return repo.create_discharge_summary({
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "admission_date": admission_date,
        "discharge_date": discharge_date,
        "diagnosis": diagnosis,
        "summary": summary,
        "post_discharge_instructions": instructions,
    })


_agent = create_react_agent(get_llm(), tools=[get_discharge_context, save_discharge_summary])


def run_discharge_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Discharge Agent."""
    patient_id = state["patient_id"]
    msgs = state.get("messages", [])
    ctx = msgs[-1].content if msgs else "Initiate discharge process"

    result = _agent.invoke({
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Patient: {patient_id}\nRequest: {ctx}"),
        ]
    })

    last_msg = result["messages"][-1].content
    parsed = extract_json(last_msg) or {}

    return {
        **state,
        "discharge_summary": parsed,
        "post_discharge_instructions": parsed.get("instructions", []),
        "agent_response": last_msg,
        "intent": "discharge",
    }
