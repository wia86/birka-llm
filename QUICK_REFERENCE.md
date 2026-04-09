# 📋 Быстрая справка birka-rag

## Установка

```bash
pip install -e ".[openai]"
```

## Проверка

```bash
python verify_installation.py
```

## CLI команды

```bash
# Создание индекса
birka-rag-index

# Чат
birka-rag
```

## Импорты

```python
from birka_rag import (
    RAGAssistant,           # Основной класс
    AssistantProfile,       # Профиль конфигурации
    LLMProvider,            # Тип провайдера
    available_profile_names,# Список профилей
    select_profile,         # Выбор профиля
    create_rag_index,       # Создание индекса
)
```

## Базовое использование

```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Вопрос")
```

## Профили

```python
from birka_rag import select_profile

profile = select_profile("gigachat")
assistant = RAGAssistant(**profile.to_kwargs())
```

## Переменные окружения

```env
RAG_PERSIST_DIR=./data/chroma
RAG_SOURCE_PATHS=./docs
RAG_MODEL_NAME=d0rj/e5-large-en-ru
RAG_PROFILE=ollama_local
GIGACHAT_API_KEY=ваш_ключ
```

## Доступные профили

- `ollama_local` — локальная Ollama
- `openai_cloud` — OpenAI API
- `gigachat` — GigaChat от Сбера
- `openrouter` — OpenRouter
- `groq` — Groq
- `deepseek` — DeepSeek
- `apifreellm` — ApiFreeLLM

## Документация

- [README.md](README.md) — основная
- [QUICKSTART.md](QUICKSTART.md) — быстрый старт
- [docs/README.md](docs/README.md) — подробная
- [MIGRATION.md](MIGRATION.md) — миграция

## Примеры

```bash
python examples/basic_usage.py
python examples/using_profiles.py
python examples/gigachat_example.py
```

## Помощь

```bash
python verify_installation.py  # Проверка
python migrate.py              # Миграция
python tests/test_basic.py     # Тесты
```
