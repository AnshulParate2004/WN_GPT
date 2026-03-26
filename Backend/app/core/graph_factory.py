"""
Graph Factory — compiles the master LangGraph StateMachine.
All agents are registered as nodes; the supervisor router conditionally
dispatches to the right agent based on detected intent.
"""
from __future__ import annotations
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, AIMessage

from app.schemas.state import AgentState
from app.services.routing import detect_intent, route_to_agent
from app.services.agents.triage import run_triage_agent
from app.services.agents.scheduler import run_booking_agent
from app.services.agents.channeling import run_channeling_agent
from app.services.agents.adherence import run_adherence_agent
from app.services.agents.care_manager import run_care_manager_agent
from app.services.agents.discharge import run_discharge_agent
from app.services.agents.insurance import run_insurance_agent
from app.services.agents.hospital_ops import run_hospital_ops_agent
from app.services.agents.pharmacy import run_pharmacy_agent
from app.services.agents.mental_health import run_mental_health_agent
from app.services.agents.family_care import run_family_care_agent
from app.services.agents.product_rec import run_product_rec_agent
from app.services.agents.nutrisense import run_nutrisense_agent
from app.services.agents.fitguide import run_fitguide_agent
from app.utils.llm_wrapper import get_llm


# ─── Health Records Node (inline / utility) ───────────────────────────────────
from app.services.external_apis import fetch_abdm_records
import asyncio

def run_health_records_node(state: AgentState) -> AgentState:
    abha_id = state.get("abha_id", "")
    records = asyncio.run(fetch_abdm_records(abha_id)) if abha_id else []
    return {
        **state,
        "abdm_records": records,
        "agent_response": f"Fetched {len(records)} ABDM record(s) for ABHA ID: {abha_id}",
        "intent": "health_records",
    }


# ─── Intent Detection Node ────────────────────────────────────────────────────
def intent_detection_node(state: AgentState) -> AgentState:
    """Detects intent and stores it in state."""
    intent = detect_intent(state)
    return {**state, "intent": intent}


# ─── General Response Node ────────────────────────────────────────────────────
def general_response_node(state: AgentState) -> AgentState:
    llm = get_llm()
    messages = state.get("messages", [])
    result = llm.invoke([
        SystemMessage(content="You are WellnessGPT, a helpful healthcare AI assistant."),
        *messages,
    ])
    return {
        **state,
        "agent_response": result.content,
        "intent": "general",
    }


# ─── Build the Graph ──────────────────────────────────────────────────────────
def build_graph() -> StateGraph:
    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("detect_intent", intent_detection_node)
    builder.add_node("triage_agent", run_triage_agent)
    builder.add_node("booking_agent", run_booking_agent)
    builder.add_node("channeling_agent", run_channeling_agent)
    builder.add_node("adherence_agent", run_adherence_agent)
    builder.add_node("care_manager_agent", run_care_manager_agent)
    builder.add_node("discharge_agent", run_discharge_agent)
    builder.add_node("insurance_agent", run_insurance_agent)
    builder.add_node("hospital_ops_agent", run_hospital_ops_agent)
    builder.add_node("pharmacy_agent", run_pharmacy_agent)
    builder.add_node("mental_health_agent", run_mental_health_agent)
    builder.add_node("family_care_agent", run_family_care_agent)
    builder.add_node("product_rec_agent", run_product_rec_agent)
    builder.add_node("nutrisense_agent", run_nutrisense_agent)
    builder.add_node("fitguide_agent", run_fitguide_agent)
    builder.add_node("health_records_node", run_health_records_node)
    builder.add_node("general_response", general_response_node)

    # Entry point
    builder.set_entry_point("detect_intent")

    # Conditional routing from intent detector
    builder.add_conditional_edges(
        "detect_intent",
        route_to_agent,
        {
            "triage_agent": "triage_agent",
            "booking_agent": "booking_agent",
            "channeling_agent": "channeling_agent",
            "adherence_agent": "adherence_agent",
            "care_manager_agent": "care_manager_agent",
            "discharge_agent": "discharge_agent",
            "insurance_agent": "insurance_agent",
            "hospital_ops_agent": "hospital_ops_agent",
            "pharmacy_agent": "pharmacy_agent",
            "mental_health_agent": "mental_health_agent",
            "family_care_agent": "family_care_agent",
            "product_rec_agent": "product_rec_agent",
            "nutrisense_agent": "nutrisense_agent",
            "fitguide_agent": "fitguide_agent",
            "health_records_node": "health_records_node",
            "general_response": "general_response",
        },
    )

    # All agents end after running
    for node in [
        "triage_agent", "booking_agent", "channeling_agent", "adherence_agent",
        "care_manager_agent", "discharge_agent", "insurance_agent", "hospital_ops_agent",
        "pharmacy_agent", "mental_health_agent", "family_care_agent", "product_rec_agent",
        "nutrisense_agent", "fitguide_agent",
        "health_records_node", "general_response",
    ]:
        builder.add_edge(node, END)

    return builder.compile()


# Singleton compiled graph
_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
