"""Пример работы с несколькими базами знаний."""

from birka_rag import RAGAssistant

# База 1: Нормативные документы
assistant_norms = RAGAssistant(
    persist_directory="./data/chroma_norms",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
    template=(
        "Ты — эксперт по нормативным документам.\n"
        "Контекст: {context}\n"
        "Вопрос: {question}\nОтвет:"
    ),
)

# База 2: Техническая документация
assistant_tech = RAGAssistant(
    persist_directory="./data/chroma_tech",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
    template=(
        "Ты — технический эксперт.\n"
        "Контекст: {context}\n"
        "Вопрос: {question}\nОтвет:"
    ),
)

# Запросы к разным базам
question = "Какие требования к оборудованию?"

print("Ответ из нормативов:")
print(assistant_norms.ask(question))
print()

print("Ответ из технической документации:")
print(assistant_tech.ask(question))
