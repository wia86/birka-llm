"""Ядро RAG-системы: assistant, профили, типы."""

from .assistant import DEFAULT_OLLAMA_URL, RAGAssistant
from .profiles import (
    ACTIVE_PROFILE,
    ASSISTANT_PROFILES,
    DEFAULT_PROFILE,
    AssistantProfile,
    available_profile_names,
    format_profiles,
    get_active_profile,
    select_profile,
    set_active_profile,
)
from .types import LLMProvider

__all__ = [
    "RAGAssistant",
    "DEFAULT_OLLAMA_URL",
    "AssistantProfile",
    "ASSISTANT_PROFILES",
    "DEFAULT_PROFILE",
    "ACTIVE_PROFILE",
    "LLMProvider",
    "available_profile_names",
    "format_profiles",
    "get_active_profile",
    "select_profile",
    "set_active_profile",
]
