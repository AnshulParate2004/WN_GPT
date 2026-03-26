"""
Hospital Operations Agent (Clearmedi)
──────────────────────────────────────
Manages bed availability, inventory tracking, and admin coordination.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a hospital operations AI for Clearmedi. Your responsibilities:
1. Monitor and manage bed availability across wards and clinics.
2. Track inventory levels and flag items below reorder threshold.
3. Coordinate admissions and discharges.
4. Provide operational reports and recommendations.

Respond in JSON:
{
  "available_beds": <number>,
  "occupied_beds": <number>,
  "low_inventory_items": ["<item name>"],
  "operational_alerts": ["<alert>"],
  "recommendations": ["<action>"]
}"""


@tool
def get_bed_status(clinic_id: str) -> dict:
    """Get all bed statuses for a clinic."""
    beds = repo.list_beds(clinic_id=clinic_id)
    available = [b for b in beds if b.get("status") == "available"]
    occupied = [b for b in beds if b.get("status") == "occupied"]
    return {"available": available, "occupied": occupied, "total": len(beds)}


@tool
def get_inventory_alerts(clinic_id: str) -> list:
    """Get inventory items below reorder level."""
    items = repo.list_inventory(clinic_id=clinic_id)
    return [i for i in items if i.get("quantity", 0) <= i.get("reorder_level", 0)]


@tool
def update_bed(bed_id: str, status: str) -> dict:
    """Update a bed's status (available / occupied / maintenance)."""
    return repo.update_bed_status(bed_id, status)


_agent = create_react_agent(get_llm(), tools=[get_bed_status, get_inventory_alerts, update_bed])


def run_hospital_ops_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Hospital Operations Agent."""
    clinic_id = state.get("clinic_id", "")
    messages = state.get("messages", [])
    action = messages[-1] if messages else "Generate operational report"

    prompt = f"""
Clinic ID: {clinic_id}
Action requested: {action}

Check bed status and inventory alerts, then provide an operational summary.
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
        "bed_status": parsed.get("available_beds", []),
        "inventory_status": parsed.get("low_inventory_items", []),
        "agent_response": last_msg,
        "intent": "hospital_ops",
    }
