"""CLI для интерактивного чата с RAG."""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from birka_rag.core import (
    RAGAssistant,
    format_profiles,
    get_active_profile,
    set_active_profile,
)


def main() -> None:
    """Точка входа CLI для чата с RAG.
    
    Конфигурация из env:
    - RAG_PROFILE: имя профиля (ollama_local, gigachat, openai_cloud и др.)
    - RAG_DEMO_QUESTION: демонстрационный вопрос для теста
    """
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    load_dotenv(override=True)

    profile_name = (
        os.environ.get("RAG_PROFILE") or 
        os.environ.get("RAG_CLOUD_MODEL") or 
        "ollama_local"
    )
    demo_question = os.environ.get(
        "RAG_DEMO_QUESTION", 
        "query: какие есть схемно-режимные мероприятия?"
    )

    print("Доступные профили:\n")
    print(format_profiles())
    print()

    try:
        set_active_profile(profile_name)
        profile = get_active_profile()
        assistant = RAGAssistant(**profile.to_kwargs())
    except ValueError as e:
        if "API-ключ" in str(e):
            print(f"Ошибка настройки: {e}")
            print("\nПроверьте переменные окружения для выбранного провайдера.")
            sys.exit(1)
        raise

    print(f"Используется профиль: {profile_name} — {profile.name}\n")

    try:
        start = time.time()
        answer = assistant.ask(demo_question)
        query_time = time.time() - start

        print(f"Вопрос: {demo_question}")
        print(f"Ответ: {answer}\n")
        print(f"Время ответа: {query_time:.2f}с\n")
    except Exception as e:
        print("Не удалось выполнить демонстрационный запрос.\n")
        print(f"Ошибка: {e}\n")
        print("Переходим сразу к интерактивному режиму.\n")

    assistant.chat()


if __name__ == "__main__":
    main()
