"""
Insurance / Claims Assessment Agent
─────────────────────────────────────
Decodes insurance policies, flags coverage gaps, pre-fills claims forms,
and optimizes for wellness scores.
"""
from __future__ import annotations
import uuid
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json, safe_float
from app.db import repository as repo

SYSTEM_PROMPT = """You are a healthcare insurance claims AI assistant. Your job is to:
1. Decode the patient's insurance policy details.
2. Analyze what is covered vs what are the gaps for the given diagnosis.
3. Calculate estimated coverage amount.
4. Pre-fill a claims form with accurate data.
5. Provide a wellness score (0–100) based on the patient's health profile.

Respond in JSON:
{
  "policy_summary": "<brief summary>",
  "coverage_amount": <float>,
  "coverage_gaps": ["<gap description>"],
  "wellness_score": <float between 0 and 100>,
  "claim_form": {
    "diagnosis_code": "<ICD code>",
    "treatment_description": "<description>",
    "estimated_reimbursement": <float>
  },
  "recommendations": "<any optimization tips>"
}"""


@tool
def get_patient_policy(patient_id: str) -> dict:
    """Fetch patient profile and existing insurance claim data."""
    patient = repo.get_patient(patient_id)
    claim = repo.get_claim(patient_id)
    return {"patient": patient, "latest_claim": claim}


@tool
def submit_claim(
    patient_id: str,
    policy_number: str,
    insurer: str,
    diagnosis: str,
    treatment_cost: float,
    coverage_amount: float,
    coverage_gaps: list,
    wellness_score: float,
) -> dict:
    """Create an insurance claim record in Supabase."""
    return repo.create_claim({
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "policy_number": policy_number,
        "insurer": insurer,
        "diagnosis": diagnosis,
        "treatment_cost": treatment_cost,
        "coverage_amount": coverage_amount,
        "coverage_gaps": coverage_gaps,
        "wellness_score": wellness_score,
        "status": "pending",
    })


_agent = create_react_agent(get_llm(), tools=[get_patient_policy, submit_claim])


def run_insurance_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Claims Assessment Agent."""
    patient_id = state["patient_id"]
    messages = state.get("messages", [])
    user_msg = messages[-1] if messages else "Assess and submit an insurance claim"

    prompt = f"""
Patient ID: {patient_id}
Request: {user_msg}

Fetch the patient policy, analyze coverage for the diagnosis,
calculate the claim, and submit it.
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
        "coverage_gaps": parsed.get("coverage_gaps", []),
        "wellness_score": safe_float(parsed.get("wellness_score", 0)),
        "claim_form": parsed.get("claim_form", {}),
        "agent_response": last_msg,
        "intent": "insurance",
    }
