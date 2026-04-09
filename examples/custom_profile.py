"""Пример кастомного профиля."""

from pathlib import Path

from birka_rag import AssistantProfile, RAGAssistant

# Создание кастомного профиля
custom_profile = AssistantProfile(
    name="Мой кастомный профиль",
    persist_directory=Path("./data/my_chroma"),
    model_name="intfloat/multilingual-e5-large",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
    llm_api_base="http://localhost:11434",  # Кастомный URL Ollama
    temperature=0.3,  # Более креативные ответы
    top_k=10,  # Больше контекста
    preload=True,
    description="Профиль с кастомными настройками",
)

# Использование кастомного профиля
assistant = RAGAssistant(**custom_profile.to_kwargs())

# Или напрямую
assistant = RAGAssistant(
    persist_directory="./data/my_chroma",
    model_name="intfloat/multilingual-e5-large",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
    llm_api_base="http://localhost:11434",
    temperature=0.3,
    top_k=10,
)

answer = assistant.ask("Какие есть схемно-режимные мероприятия?")
print(answer)
