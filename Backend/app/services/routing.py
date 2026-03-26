"""
Supervisor Routing Logic
────────────────────────
Detects user intent using keyword matching and LLM classification.
Provides the routing map for the LangGraph StateMachine.
"""
from __future__ import annotations
from langchain_core.messages import HumanMessage
from app.utils.llm_wrapper import get_llm
from app.utils.parsers import normalize_enum
from app.schemas.state import AgentState

INTENT_PROMPT = """You are a medical intent classifier. Categorize the user's message.
Intents:
- triage           → symptoms, pain, bleeding, emergency, scoring
- booking          → schedule, appointment, book, doctor available
- channeling       → which doctor, which specialty, where to go
- adherence        → reminders, follow-up, compliance, med check
- care_plan        → general wellness, preventative care, trends
- discharge        → summary of stay, post-discharge instructions
- insurance        → policy, coverage, gaps, claims, bills
- hospital_ops     → beds, inventory, ward, status (admin/ops)
- pharmacy         → medications, drugs, refills, interaction
- mental_health    → anxiety, depression, stress, PHQ, GAD, mental wellness
- family_care      → family health, household, spouse, children records
- product_rec      → supplements, products, health products, recommend
- nutrisense       → diet, nutrition, meal plan, calories, metabolic
- fitguide         → exercise, workout, fitness, steps, gym, activity
- health_records   → ABDM, ABHA, health record, medical history pull
- general          → everything else

RESPOND ONLY WITH THE INTENT NAME."""


def detect_intent(state: AgentState) -> str:
    """Detects intent using hybrid logic: keyword matching + LLM fallback."""
    msgs = state.get("messages", [])
    if not msgs: return "general"
    
    text = msgs[-1].content.lower()

    # 1. Quick Keyword Matching (Efficiency)
    intents_keywords = {
        "triage": ["pain", "symptom", "hurt", "ache", "emergency", "bleeding", "fever"],
        "booking": ["book", "appointment", "schedule", "slot", "doctor"],
        "channeling": ["specialty", "specialist", "department", "which doctor"],
        "adherence": ["reminder", "compliance", "take my med", "follow up"],
        "care_plan": ["preventive", "wellness", "lifestyle"],
        "discharge": ["discharge", "summary", "going home", "post stay"],
        "insurance": ["insurance", "claim", "policy", "coverage", "billing"],
        "hospital_ops": ["bed", "inventory", "ward", "stock", "ops"],
        "pharmacy": ["medication", "drug", "refill", "pharmacy", "pill"],
        "mental_health": ["anxiety", "depress", "stress", "phq", "gad", "mental"],
        "family_care": ["family", "household", "children", "spouse"],
        "product_rec": ["supplement", "product", "recommend", "suggest"],
        "nutrisense": ["diet", "nutrition", "meal plan", "calorie", "metabolic", "food"],
        "fitguide": ["exercise", "workout", "fitness", "steps", "gym", "activity"],
        "health_records": ["abdm", "abha", "health record", "history"],
    }

    for intent, keywords in intents_keywords.items():
        if any(k in text for k in keywords):
            return intent

    # 2. LLM Fallback (Accuracy)
    llm = get_llm()
    result = llm.invoke([
        HumanMessage(content=f"{INTENT_PROMPT}\n\nUser: {text}")
    ])
    return normalize_enum(result.content.strip().lower(), list(intents_keywords.keys()) + ["general"])


def route_to_agent(state: AgentState) -> str:
    """Callback for conditional edges in LangGraph."""
    intent = state.get("intent", "general")
    mapping = {
        "triage": "triage_agent",
        "booking": "booking_agent",
        "channeling": "channeling_agent",
        "adherence": "adherence_agent",
        "care_plan": "care_manager_agent",
        "discharge": "discharge_agent",
        "insurance": "insurance_agent",
        "hospital_ops": "hospital_ops_agent",
        "pharmacy": "pharmacy_agent",
        "mental_health": "mental_health_agent",
        "family_care": "family_care_agent",
        "product_rec": "product_rec_agent",
        "nutrisense": "nutrisense_agent",
        "fitguide": "fitguide_agent",
        "health_records": "health_records_node",
        "general": "general_response",
    }
    return mapping.get(intent, "general_response")
