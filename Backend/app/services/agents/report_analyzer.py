"""
Report Intelligence Agent (Agent #15)
────────────────────────────────────
Analyzes uploaded medical reports (PDFs, Images, Lab results).
Extracts clinical data, vitals, and highlights abnormal findings.
"""
from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.schemas.state import AgentState
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import extract_json
from app.db import repository as repo

SYSTEM_PROMPT = """You are a Clinical Report Analysis AI. Your job is to:
1. Analyze medical reports (blood tests, radiology, prescriptions).
2. Extract key metrics (e.g., HbA1c, BP, Cholesterol) and note any abnormalities.
3. Compare findings with the patient's existing chronic conditions.
4. Provide a structured summary and suggest the next specialty to consult if needed.

Always respond in JSON format:
{
  "findings": [{"metric": "<>", "value": "<>", "is_abnormal": <true|false>}],
  "summary": "<clinical interpretation>",
  "risk_level": "<low|medium|high>",
  "recommended_specialty": "<specialty>"
}"""


@tool
def get_latest_document(patient_id: str) -> dict:
    """Fetch the metadata of the most recently uploaded document for the patient."""
    supabase = repo.get_supabase()
    res = (
        supabase.table("patient_documents")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else {"error": "No documents found."}


@tool
def extract_document_text(public_url: str) -> str:
    """Extract text from a medical report (Stub for OCR/PDF parsing)."""
    # In a real app, this would use PyPDF2 or Azure Form Recognizer
    return f"[SIMULATED OCR TEXT FROM {public_url}]: Patient shows elevated glucose (140 mg/dL) and normal BP."


_agent = create_react_agent(get_llm(), tools=[get_latest_document, extract_document_text])


def run_report_analyzer_agent(state: AgentState) -> AgentState:
    """LangGraph node: runs Report Intelligence Agent."""
    patient_id = state["patient_id"]
    msgs = state.get("messages", [])
    ctx = msgs[-1].content if msgs else "Analyze my latest report"

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
        "report_analysis": parsed,
        "agent_response": last_msg,
        "intent": "report_analysis",
    }
