"""Interactive CLI session loop."""
from __future__ import annotations

import cli._path  # noqa: F401

from langchain_core.messages import AIMessage, HumanMessage
from rich.prompt import Prompt

from app.db.repository import get_patient
from app.services.routing import detect_intent
from cli.branding import (
    print_goodbye,
    print_intent_routing,
    print_patient_panel,
    print_session_hint,
    print_welcome_banner,
)
from cli.display import print_error
from cli.llm import get_streaming_llm, stream_response
from cli.theme import make_console

QUIT_COMMANDS = frozenset({"/quit", "exit", "quit", "q", "back"})


async def run_session(patient_id: str) -> int:
    console = make_console()
    patient = get_patient(patient_id)
    if not patient:
        print_error(console, f"Patient '{patient_id}' not found. Run: uv run python -m db_init")
        return 1

    print_welcome_banner(console, patient_name=patient.get("name"))
    print_patient_panel(console, patient)
    print_session_hint(console)

    llm = get_streaming_llm()
    chat_history: list = []

    while True:
        try:
            user_input = Prompt.ask("[bold #00b4a6]You[/]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if not user_input:
            continue
        if user_input.lower() in QUIT_COMMANDS:
            break

        intent = detect_intent({
            "patient_id": patient_id,
            "messages": [HumanMessage(content=user_input)],
        })

        print_intent_routing(console, intent, user_input)
        chat_history.append(HumanMessage(content=user_input))

        response = await stream_response(console, patient, chat_history, intent, llm)
        chat_history.append(AIMessage(content=response))

    print_goodbye(console)
    return 0
