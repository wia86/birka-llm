"""Пример использования профилей."""

from birka_rag import (
    RAGAssistant,
    available_profile_names,
    format_profiles,
    select_profile,
)

# Показать все доступные профили
print("Доступные профили:")
print(format_profiles())
print()

# Список имён профилей
print("Имена профилей:", available_profile_names())
print()

# Выбрать профиль
profile_name = "ollama_local"  # или "gigachat", "openai_cloud" и др.
profile = select_profile(profile_name)

print(f"Выбран профиль: {profile.name}")
print(f"LLM: {profile.llm_model} ({profile.llm_provider})")
print(f"Embeddings: {profile.model_name}")
print()

# Создать ассистента из профиля
assistant = RAGAssistant(**profile.to_kwargs())

# Задать вопрос
answer = assistant.ask("Что такое ПЗ?")
print(f"Ответ: {answer}")
