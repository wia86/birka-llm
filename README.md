# birka-rag

RAG-система для работы с нормативными документами, внутренними knowledge-базами и материалами техподдержки. Проект переведён на пакетную структуру `src/birka_rag/` и CLI-команды `birka-rag` / `birka-rag-index`.

## Установка

```bash
pip install -e .

# Для OpenAI-совместимых API
pip install -e ".[openai]"

# Для разработки
pip install -e ".[dev]"
```

## Быстрый старт

### 1. Подготовьте структуру данных

```text
knowledge/
  docs/          # документация, нормативы
  code_guides/   # безопасные пояснения по коду
  task_samples/  # примеры файлов заданий
storage/
  chroma/        # векторные базы
  uploads/       # загруженные в чат файлы
```

### 2. Настройте `.env`

Скопируйте `.env.example` в `.env` и при необходимости измените:

- `RAG_PERSIST_DIR=./storage/chroma/default`
- `RAG_SOURCE_PATHS=./knowledge/docs;./knowledge/code_guides;./knowledge/task_samples`
- `RAG_SOURCE_EXTENSIONS=.pdf,.md,.txt,.log,.json,.yaml,.yml,.csv`
- `RAG_PROFILE=ollama_local`

### 3. Постройте индекс

```bash
birka-rag-index
```

### 4. Запустите чат

```bash
birka-rag
```

В интерактивном режиме доступны специальные команды:

- `:traceback` — вставить traceback и получить разбор
- `:taskfile <путь> [| вопрос]` — загрузить файл задания и получить диагностику

## Что внутри

- `src/birka_rag/core/` — `RAGAssistant`, профили, провайдеры LLM
- `src/birka_rag/indexing/` — построение Chroma-индекса из `pdf/md/txt/log/json/yaml/csv`
- `src/birka_rag/cli/` — точки входа `birka-rag` и `birka-rag-index`
- `knowledge/` — база знаний для индексации
- `storage/` — runtime-данные

## Использование как библиотеки

```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./storage/chroma/default",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Какие есть схемно-режимные мероприятия?")
print(answer)
```

### Профили

```python
from birka_rag import available_profile_names, select_profile

print(available_profile_names())

profile = select_profile("gigachat")
assistant = RAGAssistant(**profile.to_kwargs())
assistant.chat()
```

### Программное создание индекса

```python
from birka_rag import create_rag_index

create_rag_index(
    persist_directory="./storage/chroma/default",
    source_paths=["./knowledge/docs", "./knowledge/code_guides"],
    model_name="d0rj/e5-large-en-ru",
    chunk_size=1000,
    chunk_overlap=200,
    recursive=True,
    rag_mode="common",
)
```

## Профили LLM

- `ollama_local` — локальная Ollama
- `openai_cloud` — OpenAI API
- `gigachat` — GigaChat
- `openrouter` — OpenRouter
- `groq` — Groq
- `deepseek` — DeepSeek
- `apifreellm` — ApiFreeLLM

## Переменные окружения

- `RAG_PERSIST_DIR` — путь к векторной базе
- `RAG_SOURCE_PATHS` — каталоги и/или файлы-источники
- `RAG_SOURCE_EXTENSIONS` — набор расширений для индексации
- `RAG_RECURSIVE` — рекурсивный поиск файлов
- `RAG_MODE` — `common` или `per_file`
- `RAG_PROFILE` — активный профиль LLM
- `RAG_UPLOADS_DIR` — каталог для загруженных пользователем файлов

## Миграция

Старая структура `data_from_gost/` заменена пакетом `birka_rag` и CLI-командами. Подробности: `MIGRATION.md`.

```python
# Было
from rag_assistant import RAGAssistant

# Стало
from birka_rag import RAGAssistant
```

```bash
# Было
python data_from_gost/create_rag.py
python data_from_gost/run_lln.py

# Стало
birka-rag-index
birka-rag
```
