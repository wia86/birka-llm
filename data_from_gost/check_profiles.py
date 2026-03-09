"""Проверка всех RAG-профилей: один тестовый вопрос, статус OK/REFUSAL/ERROR."""

import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

from dotenv import load_dotenv
from rag_assistant import (
    RAGAssistant,
    available_profile_names,
    get_active_profile,
    set_active_profile,
)

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

DEMO_QUESTION = os.environ.get(
    "RAG_DEMO_QUESTION", "query: какие есть схемно-режимные мероприятия?"
)
REFUSAL_MARKER = "чувствительными темами"


def main() -> None:
    print("Проверка профилей (один вопрос):", DEMO_QUESTION[:60], "...\n")
    results: list[tuple[str, str, str]] = []

    for name in available_profile_names():
        set_active_profile(name)
        profile = get_active_profile()
        kwargs = {**profile.to_kwargs(), "preload": False}
        try:
            assistant = RAGAssistant(**kwargs)
            answer = assistant.ask(DEMO_QUESTION)
            if REFUSAL_MARKER in answer:
                results.append((name, "REFUSAL", answer[:120].replace("\n", " ") + "..."))
            else:
                results.append((name, "OK", answer[:120].replace("\n", " ") + "..."))
        except Exception as e:
            results.append((name, "ERROR", str(e)[:150]))

    print("\nРезультаты:")
    print("-" * 70)
    for name, status, detail in results:
        print(f"  {name:18} {status:8} {detail}")
    print("-" * 70)
    ok = sum(1 for _, s, _ in results if s == "OK")
    refusal = sum(1 for _, s, _ in results if s == "REFUSAL")
    err = sum(1 for _, s, _ in results if s == "ERROR")
    print(f"  Итого: OK={ok}, REFUSAL (модерация)={refusal}, ERROR={err}")


if __name__ == "__main__":
    main()
