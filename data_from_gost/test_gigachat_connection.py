#!/usr/bin/env python3
"""
Скрипт для проверки подключения к GigaChat API.

Использование:
    python test_gigachat_connection.py

Скрипт проверит:
1. Наличие переменной окружения GIGACHAT_API_KEY
2. Корректность формата API ключа
3. Возможность подключения к GigaChat API
"""

import os
import sys
from pathlib import Path

# Добавляем путь к rag_assistant в sys.path
sys.path.insert(0, str(Path(__file__).parent))

from rag_assistant import AssistantProfile, RAGAssistant


def check_environment() -> bool:
    """Проверяет наличие переменной окружения GIGACHAT_API_KEY."""
    api_key = os.getenv("GIGACHAT_API_KEY")
    if not api_key:
        print("❌ Переменная окружения GIGACHAT_API_KEY не установлена")
        print("📖 Следуйте инструкциям в файле GIGACHAT_SETUP.md")
        return False

    print(f"✅ Переменная окружения GIGACHAT_API_KEY найдена (длина: {len(api_key)} символов)")

    # Простая проверка формата ключа (должен быть UUID-like)
    if len(api_key) != 36 or api_key.count('-') != 4:
        print("⚠️  Предупреждение: API ключ имеет необычный формат")
        print("   Обычно ключ выглядит как UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

    return True


def test_connection() -> bool:
    """Тестирует подключение к GigaChat API."""
    try:
        # Создаем профиль для тестирования
        profile = AssistantProfile(
            name="GigaChat Test",
            persist_directory=Path(r"D:\birka\network_data\data_gost\bge_m3_mu_2022"),
            model_name="BAAI/bge-m3",
            llm_model="GigaChat",
            llm_provider="openai",
            llm_api_base="https://gigachat.devices.sberbank.ru/api/",
            llm_api_key=None,  # Будет взят из переменной окружения
            temperature=0.2,
            top_k=1,  # Минимальный для быстрого теста
            preload=False,  # Не предзагружать embeddings для быстрого теста
        )

        print("🔄 Создание подключения к GigaChat API...")
        assistant = RAGAssistant(**profile.to_kwargs())

        print("🔄 Отправка тестового запроса...")
        test_question = "Скажи 'Тест подключения прошел успешно' если ты GigaChat"

        response = assistant.ask(test_question)

        print("✅ Подключение успешно!")
        print(f"📝 Ответ GigaChat: {response}")

        return True

    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\n🔍 Возможные причины:")
        print("   - Неправильный API ключ")
        print("   - Закончились токены (проверьте баланс в личном кабинете)")
        print("   - Проблемы с интернет-соединением")
        print("   - Технические работы на стороне Сбера")
        return False


def main() -> None:
    """Основная функция скрипта."""
    print("🧪 Проверка настройки GigaChat API\n")

    # Шаг 1: Проверка переменной окружения
    if not check_environment():
        sys.exit(1)

    print()

    # Шаг 2: Тест подключения
    if test_connection():
        print("\n🎉 Настройка GigaChat API завершена успешно!")
        print("   Теперь вы можете использовать профиль 'gigachat' в run_lln.py")
    else:
        print("\n❌ Настройка не завершена. Проверьте ошибки выше.")
        sys.exit(1)


if __name__ == "__main__":
    import os

    os.environ[
        'GIGACHAT_API_KEY'] = 'MDE5YWJhNmItMmQ2OS03ZGI1LTg2N2ItZmY3MzI3NzJkZjQzOmQzNjI1NTBhLWI5NjMtNDg2Zi1hMzJhLTFkMzgwODY2MmRjZA=='
    print(os.getenv('GIGACHAT_API_KEY'))
    main()
