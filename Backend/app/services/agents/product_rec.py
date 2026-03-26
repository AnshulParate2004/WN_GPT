"""
Product Recommendation Agent
──────────────────────────────
Suggests supplements, health services, and partner products aligned
to the patient's care plan and health profile.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a personalized health product recommendation AI.
Your job is to:
1. Review the patient's care plan, health conditions, and deficiencies.
2. Search the product catalog for relevant supplements/services.
3. Recommend products that genuinely help the patient's health goals.
4. Never recommend products that conflict with allergies or conditions.
5. Explain WHY each product is recommended.

Respond in JSON:
{
  "recommended_products": [
    {
      "name": "<product name>",
      "category": "<supplement|service|device>",
      "reason": "<why this helps>",
      "partner": "<partner name>"
    }
  ],
  "summary": "<overall recommendation summary>"
}"""


@tool
def get_patient_care_context(patient_id: str) -> dict:
    """Fetch care plan, conditions, and allergies to contextualize recommendations."""
    patient = repo.get_patient(patient_id)
    care_plan = repo.get_care_plan(patient_id)
    return {
        "conditions": patient.get("chronic_conditions", []) if patient else [],
        "allergies": patient.get("allergies", []) if patient else [],
        "care_plan": care_plan,
    }


@tool
def search_product_catalog(tags: list) -> list:
    """Search the product catalog by health tags."""
    return repo.search_products(tags)


_agent = create_react_agent(get_llm(), tools=[get_patient_care_context, search_product_catalog])


def run_product_rec_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Product Recommendation Agent."""
    patient_id = state["patient_id"]

    prompt = f"""
Patient ID: {patient_id}

Fetch the patient's care context, search the product catalog for relevant items,
and return personalized product recommendations.
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
        "recommended_products": parsed.get("recommended_products", []),
        "agent_response": last_msg,
        "intent": "product_recommendation",
    }
