"""Streaming LLM client for the CLI."""
from __future__ import annotations

from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI

from app.core.config import get_settings
from cli.display import print_intent_header, print_stream_token
from cli.prompts import patient_context, system_prompt_for


def get_streaming_llm() -> AzureChatOpenAI:
    settings = get_settings()
    return AzureChatOpenAI(
        azure_deployment=settings.azure_openai_deployment,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.openai_api_version,
        temperature=0.3,
        max_tokens=1024,
        streaming=True,
    )


async def stream_response(
    patient: dict,
    chat_history: list,
    intent: str,
    llm: AzureChatOpenAI,
) -> str:
    messages = [
        SystemMessage(content=f"{system_prompt_for(intent)}\n\n{patient_context(patient)}"),
        *chat_history,
    ]

    print_intent_header(intent)
    full = ""

    async for chunk in llm.astream(messages):
        token = chunk.content
        if token:
            print_stream_token(token, intent)
            full += token

    print()
    return full
