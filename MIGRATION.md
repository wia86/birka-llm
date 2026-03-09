# Миграция на новую структуру пакета

## Обзор изменений

Проект реорганизован в полноценный Python-пакет с разделением на:
- **Библиотека** (`src/birka_rag/`) — core функциональность
- **CLI утилиты** — консольные команды
- **Примеры** — демонстрация использования

## Установка нового пакета

```bash
# Из корня проекта
pip install -e .

# С поддержкой OpenAI API
pip install -e ".[openai]"
```

## Изменения в импортах

### Основные классы

```python
# Было
from rag_assistant import RAGAssistant, select_profile

# Стало
from birka_rag import RAGAssistant, select_profile
```

### Профили

```python
# Было
from rag_assistant import (
    AssistantProfile,
    ASSISTANT_PROFILES,
    available_profile_names,
    format_profiles,
)

# Стало
from birka_rag import (
    AssistantProfile,
    ASSISTANT_PROFILES,
    available_profile_names,
    format_profiles,
)
```

### Типы

```python
# Было
from rag_assistant.llm_types import LLMProvider

# Стало
from birka_rag import LLMProvider
```

### Провайдеры

```python
# Было
from rag_assistant.giga_get_token import gigachat_get_bearer_token

# Стало
from birka_rag.core.providers import gigachat_get_bearer_token
```

## Изменения в CLI

### Создание индекса

```bash
# Было
python data_from_gost/create_rag.py

# Стало
birka-rag-index
```

### Чат с ассистентом

```bash
# Было
python data_from_gost/run_lln.py

# Стало
birka-rag
```

## Изменения в коде

### Создание ассистента

Без изменений в API:

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

### Использование профилей

Без изменений в API:

```python
from birka_rag import select_profile

profile = select_profile("gigachat")
assistant = RAGAssistant(**profile.to_kwargs())
```

### Создание индекса программно

```python
# Было
from data_from_gost.create_rag import create_rag

# Стало
from birka_rag import create_rag_index

create_rag_index(
    persist_directory="./data/chroma",
    source_paths=["./docs"],
    model_name="d0rj/e5-large-en-ru",
)
```

## Переменные окружения

Без изменений:

```bash
RAG_PERSIST_DIR=./data/chroma
RAG_SOURCE_PATHS=/path/to/pdfs
RAG_MODEL_NAME=d0rj/e5-large-en-ru
RAG_PROFILE=gigachat
GIGACHAT_API_KEY=ваш_ключ
```

## Структура файлов

```
src/birka_rag/
├── __init__.py              # Публичный API
├── core/
│   ├── __init__.py
│   ├── assistant.py
│   ├── profiles.py
│   ├── types.py
│   └── providers/
│       ├── __init__.py
│       ├── gigachat.py
│       └── apifreellm.py
├── indexing/
│   ├── __init__.py
│   └── indexer.py
└── cli/
    ├── __init__.py
    ├── chat.py
    └── index.py
```

## Что осталось без изменений

- API классов и функций
- Переменные окружения
- Формат конфигурации профилей
- Формат векторной базы Chroma
- Логика работы RAG

## Преимущества новой структуры

1. **Установка через pip** — `pip install -e .`
2. **CLI команды** — `birka-rag`, `birka-rag-index`
3. **Публичный API** — явные экспорты в `__init__.py`
4. **Типизация** — `py.typed` для IDE
5. **Опциональные зависимости** — `pip install ".[openai]"`
6. **Примеры** — готовые скрипты в `examples/`
7. **Документация** — структурированная в `docs/`

## Полная миграция

Весь функционал перенесён в новую структуру. Legacy код `data_from_gost/` удалён. Используйте только новые команды и импорты.

## Проверка миграции

```bash
# Установка пакета
pip install -e .

# Проверка CLI
birka-rag --help
birka-rag-index --help

# Проверка импортов
python -c "from birka_rag import RAGAssistant; print('OK')"

# Запуск примеров
python examples/basic_usage.py
```
