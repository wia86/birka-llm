"""Пример работы с GigaChat."""

import os

from birka_rag import RAGAssistant

# Убедитесь, что установлена переменная окружения
if not os.getenv("GIGACHAT_API_KEY"):
    print("Установите GIGACHAT_API_KEY перед запуском")
    exit(1)

# Создание ассистента с GigaChat
assistant = RAGAssistant(
    persist_directory="./data/chroma_default",
    model_name="d0rj/e5-large-en-ru",
    llm_model="GigaChat-2",
    llm_provider="openai",  # GigaChat использует OpenAI-совместимый API
    llm_api_base="https://gigachat.devices.sberbank.ru/api/v1/",
    temperature=0.2,
    top_k=6,
)

# Задать вопрос
question = "Какие есть схемно-режимные мероприятия?"
answer = assistant.ask(question)

print(f"Вопрос: {question}")
print(f"Ответ: {answer}")
