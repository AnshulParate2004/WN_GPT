"""
Main Chat API — runs any message through the LangGraph state machine.
"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage

from app.schemas.request_models import ChatRequest, ChatResponse
from app.core.graph_factory import get_graph
from app.api.deps import get_current_patient

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(body: ChatRequest, patient: dict = Depends(get_current_patient)):
    """
    Main entry point — send any message and the supervisor router
    dispatches it to the appropriate agent.
    """
    session_id = body.session_id or str(uuid.uuid4())
    graph = get_graph()

    initial_state = {
        "patient_id": body.patient_id,
        "session_id": session_id,
        "messages": [HumanMessage(content=body.message)],
        "intent": body.intent or "",
        "symptoms": [],
        "metadata": {},
    }

    result = graph.invoke(initial_state)

    return ChatResponse(
        patient_id=body.patient_id,
        session_id=session_id,
        intent=result.get("intent", "general"),
        response=result.get("agent_response", "I'm here to help with your health needs."),
        metadata=result.get("metadata", {}),
    )
