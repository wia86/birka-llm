"""birka-rag: RAG-система для работы с нормативными документами.

Основные компоненты:
- core: RAGAssistant, профили, провайдеры LLM
- indexing: создание векторной базы из PDF
- cli: консольные утилиты

Пример использования как библиотеки:

    from birka_rag import RAGAssistant

    assistant = RAGAssistant(
        persist_directory="./data/chroma_default",
        model_name="d0rj/e5-large-en-ru",
        llm_model="llama3.2:3b",
        llm_provider="ollama",
    )
    
    answer = assistant.ask("Какие есть схемно-режимные мероприятия?")
    print(answer)

Пример с профилями:

    from birka_rag import RAGAssistant, select_profile

    profile = select_profile("gigachat")
    assistant = RAGAssistant(**profile.to_kwargs())
    assistant.chat()

Создание индекса:

    from birka_rag import create_rag_index

    create_rag_index(
        persist_directory="./data/chroma",
        source_paths=["./docs"],
        model_name="d0rj/e5-large-en-ru",
    )
"""

from .core import (
    ACTIVE_PROFILE,
    ASSISTANT_PROFILES,
    DEFAULT_OLLAMA_URL,
    DEFAULT_PROFILE,
    AssistantProfile,
    LLMProvider,
    RAGAssistant,
    available_profile_names,
    format_profiles,
    get_active_profile,
    select_profile,
    set_active_profile,
)
from .indexing import create_rag_index

__version__ = "0.1.0"

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
    "create_rag_index",
    "__version__",
]
