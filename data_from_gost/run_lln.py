"""Пример использования RAGAssistant с профилями настроек. GIGACHAT_API_KEY — из env."""
from __future__ import annotations

import os
import time

from rag_assistant import (
    AssistantProfile,
    RAGAssistant,
    format_profiles,
    get_active_profile,
    set_active_profile,
)

PROFILE_NAME = os.environ.get("RAG_PROFILE", "ollama_local")
DEMO_QUESTION = os.environ.get("RAG_DEMO_QUESTION", "query: какие есть схемно-режимные мероприятия?")


def list_profiles() -> None:
    """Вывести доступные профили в консоль."""
    print("Доступные профили:\n")
    print(format_profiles())


def build_assistant(profile_name: str = PROFILE_NAME) -> tuple[RAGAssistant, AssistantProfile]:
    """Создать помощника согласно профилю."""
    set_active_profile(profile_name)
    profile = get_active_profile()
    assistant = RAGAssistant(**profile.to_kwargs())
    return assistant, profile


def main() -> None:
    """Демонстрация: выводим профиль, задаём один вопрос."""
    list_profiles()
    try:
        assistant, profile = build_assistant()
    except ValueError as e:
        if "API-ключ" in str(e):
            print(f"❌ Ошибка настройки: {e}")
            print("\n📖 Инструкции по настройке GigaChat API:")
            print("   Откройте файл GIGACHAT_SETUP.md для подробных инструкций")
            return
        raise

    print(f"Используется профиль: {PROFILE_NAME} — {profile.name}\n")

    start = time.time()
    answer = assistant.ask(DEMO_QUESTION)
    query_time = time.time() - start

    print(f"Вопрос: {DEMO_QUESTION}")
    print(f"Ответ: {answer}\n")
    print(f"⏱️  Время ответа: {query_time:.2f}с\n")

    # Для интерактивного режима:
    assistant.chat()


if __name__ == "__main__":
    main()

