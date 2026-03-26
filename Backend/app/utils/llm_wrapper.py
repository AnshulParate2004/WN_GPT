"""
LLM Wrapper — unified AzureChatOpenAI interface used by all agents.
"""
from __future__ import annotations
from functools import lru_cache
from langchain_openai import AzureChatOpenAI
from app.core.config import get_settings


@lru_cache()
def get_llm(temperature: float = 0.2) -> AzureChatOpenAI:
    """Return a cached AzureChatOpenAI instance."""
    s = get_settings()
    return AzureChatOpenAI(
        azure_deployment=s.azure_openai_deployment,
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.openai_api_version,
        temperature=temperature,
        max_tokens=2048,
    )


def get_creative_llm() -> AzureChatOpenAI:
    """Higher temperature for care plan / product copy generation."""
    return get_llm.__wrapped__(temperature=0.6)  # type: ignore[attr-defined]
