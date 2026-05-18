"""Interactive CLI session loop."""
from __future__ import annotations

import cli._path  # noqa: F401

from langchain_core.messages import AIMessage, HumanMessage

from app.db.repository import get_patient
from app.services.routing import detect_intent
from cli.display import print_banner, print_error, print_user_prompt
from cli.llm import get_streaming_llm, stream_response

QUIT_COMMANDS = {"/quit", "exit", "quit"}


async def run_session(patient_id: str) -> None:
    patient = get_patient(patient_id)
    if not patient:
        print_error(f"Patient '{patient_id}' not found.")
        return

    llm = get_streaming_llm()
    print_banner(patient["name"])

    chat_history: list = []

    while True:
        try:
            user_input = print_user_prompt()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in QUIT_COMMANDS:
            break

        intent = detect_intent({
            "patient_id": patient_id,
            "messages": [HumanMessage(content=user_input)],
        })
        chat_history.append(HumanMessage(content=user_input))

        response = await stream_response(patient, chat_history, intent, llm)
        chat_history.append(AIMessage(content=response))
