#!/usr/bin/env python3
"""Скрипт для проверки подключения к GigaChat API.

Использование::

    set GIGACHAT_API_KEY=ваш_ключ
    python test_gigachat_connection.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Загрузка .env из корня проекта
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from rag_assistant import AssistantProfile, RAGAssistant


def check_environment() -> bool:
    """Проверяет наличие и формат GIGACHAT_API_KEY."""
    api_key = os.getenv("GIGACHAT_API_KEY")
    if not api_key:
        print("Переменная окружения GIGACHAT_API_KEY не установлена")
        print("Следуйте инструкциям в файле GIGACHAT_SETUP.md")
        return False

    print(f"GIGACHAT_API_KEY найден (длина: {len(api_key)} символов)")

    if len(api_key) != 36 or api_key.count("-") != 4:
        print("Предупреждение: API-ключ имеет необычный формат")
        print("  Обычно ключ выглядит как UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

    return True


def test_connection() -> bool:
    """Тестирует подключение к GigaChat API."""
    try:
        profile = AssistantProfile(
            name="GigaChat Test",
            persist_directory=Path(os.environ.get(
                "RAG_PERSIST_DIR",
                "./data/chroma_default",
            )),
            model_name=os.environ.get("RAG_MODEL_NAME", "").strip() or "d0rj/e5-large-en-ru",
            llm_model="GigaChat",
            llm_provider="openai",
            llm_api_base="https://gigachat.devices.sberbank.ru/api/",
            llm_api_key=None,
            temperature=0.2,
            top_k=1,
            preload=False,
        )

        print("Создание подключения к GigaChat API...")
        assistant = RAGAssistant(**profile.to_kwargs())

        print("Отправка тестового запроса...")
        response = assistant.ask("Скажи 'Тест подключения прошел успешно' если ты GigaChat")

        print(f"Подключение успешно!\nОтвет GigaChat: {response}")
        return True

    except Exception as e:
        print(f"Ошибка подключения: {e}")
        print(
            "\nВозможные причины:\n"
            "  - Неправильный API-ключ\n"
            "  - Закончились токены\n"
            "  - Проблемы с интернет-соединением\n"
            "  - Технические работы на стороне Сбера"
        )
        return False


def main() -> None:
    """Точка входа: проверка окружения и подключения."""
    print("Проверка настройки GigaChat API\n")

    if not check_environment():
        sys.exit(1)

    print()

    if test_connection():
        print("\nНастройка GigaChat API завершена успешно!")
        print("  Теперь можно использовать профиль 'gigachat' в run_lln.py")
    else:
        print("\nНастройка не завершена. Проверьте ошибки выше.")
        sys.exit(1)


if __name__ == "__main__":
    main()
