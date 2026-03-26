"""
Family Care Agent
──────────────────
Aggregates household health records, provides group insights,
and surfaces family-wide recommendations.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a family healthcare AI. Your job is to:
1. Aggregate health profiles of all family members.
2. Identify shared risk factors (genetic, lifestyle, environmental).
3. Generate group insights and family-wide health recommendations.
4. Flag any member who needs urgent attention.

Respond in JSON:
{
  "family_summary": "<overall family health snapshot>",
  "shared_risks": ["<risk>"],
  "member_alerts": [{"member_name": "<name>", "alert": "<alert>"}],
  "family_recommendations": ["<recommendation>"],
  "insights": "<detailed family insights>"
}"""


@tool
def get_family_health_profiles(family_id: str) -> list:
    """Fetch all family members and their health profiles."""
    members = repo.get_family_members(family_id)
    profiles = []
    for m in members:
        pid = m["id"]
        plan = repo.get_care_plan(pid)
        triage = repo.get_triage_history(pid)
        profiles.append({
            "member": m,
            "care_plan": plan,
            "recent_triage": triage[:2] if triage else [],
        })
    return profiles


_agent = create_react_agent(get_llm(), tools=[get_family_health_profiles])


def run_family_care_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Family Care Agent."""
    family_id = state.get("family_id", "")

    prompt = f"""
Family ID: {family_id}

Fetch all family member health profiles and generate comprehensive
family health insights and recommendations.
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
        "family_insights": parsed.get("insights", last_msg),
        "agent_response": last_msg,
        "intent": "family_care",
    }
