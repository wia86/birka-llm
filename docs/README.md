# birka-rag

RAG-система для работы с нормативными документами (эмбеддинги, Chroma, LLM).

## Установка

```bash
pip install -e .

# Для работы с OpenAI-совместимыми API (GigaChat, OpenRouter и др.)
pip install -e ".[openai]"

# Для разработки
pip install -e ".[dev]"
```

## Быстрый старт

### 1. Создание индекса

```bash
# Настройте переменные окружения
export RAG_PERSIST_DIR="./data/chroma"
export RAG_SOURCE_PATHS="/path/to/pdfs"
export RAG_MODEL_NAME="d0rj/e5-large-en-ru"

# Создайте индекс
birka-rag-index
```

### 2. Чат с ассистентом

```bash
# Локальная Ollama
export RAG_PROFILE="ollama_local"
birka-rag

# GigaChat
export RAG_PROFILE="gigachat"
export GIGACHAT_API_KEY="ваш_ключ"
birka-rag
```

## Использование как библиотеки

### Базовый пример

```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Какие есть схемно-режимные мероприятия?")
print(answer)
```

### Использование профилей

```python
from birka_rag import RAGAssistant, select_profile

# Список доступных профилей
from birka_rag import available_profile_names
print(available_profile_names())

# Выбор профиля
profile = select_profile("gigachat")
assistant = RAGAssistant(**profile.to_kwargs())

# Интерактивный режим
assistant.chat()
```

### Создание индекса программно

```python
from birka_rag import create_rag_index

create_rag_index(
    persist_directory="./data/chroma",
    source_paths=["./docs", "./standards"],
    model_name="d0rj/e5-large-en-ru",
    chunk_size=1000,
    chunk_overlap=200,
    recursive=True,
    rag_mode="common",  # или "per_file"
)
```

## Профили LLM

Доступные профили (настраиваются через переменные окружения):

- **ollama_local**: Локальная Ollama
- **openai_cloud**: OpenAI API (требует `OPENAI_API_KEY`)
- **gigachat**: GigaChat от Сбера (требует `GIGACHAT_API_KEY`)
- **openrouter**: OpenRouter (требует `OPENROUTER_API_KEY`)
- **groq**: Groq (требует `GROQ_API_KEY`)
- **deepseek**: DeepSeek (требует `DEEPSEEK_API_KEY`)
- **apifreellm**: ApiFreeLLM (требует `APIFREELLM_API_KEY`)

## Переменные окружения

### Общие

- `RAG_PERSIST_DIR`: путь к векторной базе (по умолчанию `./data/chroma_default`)
- `RAG_MODEL_NAME`: модель эмбеддингов (по умолчанию `d0rj/e5-large-en-ru`)
- `RAG_PROFILE`: активный профиль LLM

### Индексация

- `RAG_SOURCE_PATHS`: пути к PDF (разделитель `;` на Windows, `:` на Unix)
- `RAG_RECURSIVE`: искать во вложенных папках (`1` или `0`)
- `RAG_MODE`: режим индексации (`common` или `per_file`)

### Провайдеры LLM

- `GIGACHAT_API_KEY`: ключ GigaChat
- `GIGACHAT_CLIENT_ID`: Client ID (опционально)
- `OPENAI_API_KEY`: ключ OpenAI
- `OPENROUTER_API_KEY`: ключ OpenRouter
- `GROQ_API_KEY`: ключ Groq
- `DEEPSEEK_API_KEY`: ключ DeepSeek
- `APIFREELLM_API_KEY`: ключ ApiFreeLLM

## Архитектура

```
birka-rag/
├── src/birka_rag/
│   ├── core/              # Ядро RAG
│   │   ├── assistant.py   # RAGAssistant
│   │   ├── profiles.py    # Профили конфигурации
│   │   ├── types.py       # Типы
│   │   └── providers/     # Провайдеры LLM
│   ├── indexing/          # Создание индекса
│   │   └── indexer.py
│   └── cli/               # CLI утилиты
│       ├── chat.py
│       └── index.py
├── examples/              # Примеры использования
└── docs/                  # Документация
```

## Требования

- Python 3.11-3.13 (Chroma несовместим с 3.14)
- Для GPU: CUDA-совместимая видеокарта и PyTorch с CUDA

## Разработка

```bash
# Установка с dev-зависимостями
pip install -e ".[dev]"

# Форматирование
black src/

# Линтинг
ruff check src/

# Типы
mypy src/
```

## Лицензия

Proprietary - внутренний инструмент для электротехнических расчётов (проект Birka).
