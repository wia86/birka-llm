"""Базовый пример использования birka-rag."""

from birka_rag import RAGAssistant

# Создание ассистента с локальной Ollama
assistant = RAGAssistant(
    persist_directory="./data/chroma_default",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
    temperature=0.2,
    top_k=6,
)

# Задать вопрос
question = "Какие есть схемно-режимные мероприятия?"
answer = assistant.ask(question)

print(f"Вопрос: {question}")
print(f"Ответ: {answer}")

# Интерактивный режим (раскомментируйте для запуска)
# assistant.chat()
