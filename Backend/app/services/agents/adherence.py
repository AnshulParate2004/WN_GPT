"""
Patient Follow-Up / Adherence Agent
──────────────────────────────────────
Sends medication reminders, monitors compliance via check-ins,
and updates records when issues arise.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a patient follow-up and medication adherence AI.
Your responsibilities:
1. Review the patient's prescriptions and pending reminders.
2. Identify missed medications or delayed follow-ups.
3. Schedule new reminders as needed.
4. Provide adherence recommendations.

Respond in JSON:
{
  "adherence_status": "<on_track|at_risk|non_compliant>",
  "missed_items": ["<list of missed medications or appointments>"],
  "new_reminders_scheduled": <number>,
  "message_to_patient": "<supportive message>"
}"""


@tool
def get_patient_reminders(patient_id: str) -> dict:
    """Fetch pending reminders and current prescriptions for the patient."""
    reminders = repo.get_pending_reminders(patient_id)
    prescriptions = repo.get_prescriptions(patient_id)
    return {"pending_reminders": reminders, "prescriptions": prescriptions}


@tool
def schedule_reminder(patient_id: str, reminder_type: str, message: str, days_from_now: int = 1) -> dict:
    """Create a follow-up reminder for the patient."""
    scheduled_at = (datetime.utcnow() + timedelta(days=days_from_now)).isoformat()
    return repo.create_reminder({
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "type": reminder_type,
        "message": message,
        "scheduled_at": scheduled_at,
        "status": "pending",
    })


_agent = create_react_agent(get_llm(), tools=[get_patient_reminders, schedule_reminder])


def run_adherence_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Follow-Up/Adherence Agent."""
    patient_id = state["patient_id"]

    prompt = f"""
Patient ID: {patient_id}
Task: Review this patient's pending reminders and prescriptions.
Identify any compliance gaps and schedule appropriate follow-up reminders.
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
        "agent_response": last_msg,
        "intent": "adherence",
        "metadata": {"adherence_status": parsed.get("adherence_status", "unknown")},
    }
