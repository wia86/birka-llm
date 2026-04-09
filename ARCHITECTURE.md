# Архитектура birka-rag

Отдельный проект для RAG и чата с LLM по нормативам и материалам техподдержки. Проект вынесен из основного репозитория Birka и оформлен как Python-пакет с CLI.

## Структура проекта

```
birka-rag/
├── src/birka_rag/               # Основной пакет
│   ├── __init__.py              # Публичный API
│   ├── core/                    # Ядро RAG
│   │   ├── assistant.py         # RAGAssistant, triage traceback/taskfile
│   │   ├── profiles.py          # Профили конфигурации
│   │   ├── types.py             # Типы провайдеров
│   │   └── providers/           # Интеграции LLM
│   ├── indexing/                # Создание индекса
│   │   ├── __init__.py
│   │   └── indexer.py           # create_rag_index()
│   ├── cli/                     # CLI утилиты
│   │   ├── chat.py              # birka-rag
│   │   └── index.py             # birka-rag-index
│   └── py.typed
├── examples/                    # Примеры использования
├── docs/                        # Документация
├── tests/                       # Тесты
├── knowledge/                   # База знаний (docs/code_guides/task_samples)
├── storage/                     # Runtime-данные (chroma/uploads)
├── pyproject.toml
├── README.md
├── ARCHITECTURE.md
├── MIGRATION.md
└── .env.example
```

## Модули

### `src/birka_rag/core/`

| Модуль | Назначение |
|---|---|
| `assistant.py` | `RAGAssistant`: загрузка Chroma, embeddings, LLM, методы `ask()` / `chat()`, triage `:traceback` и `:taskfile` |
| `profiles.py` | `AssistantProfile`, выбор и активация профилей |
| `types.py` | `LLMProvider` и связанные типы |
| `providers/gigachat.py` | Получение OAuth-токена GigaChat |
| `providers/apifreellm.py` | Клиент ApiFreeLLM |

### `src/birka_rag/indexing/`

| Модуль | Назначение |
|---|---|
| `indexer.py` | `create_rag_index()` для загрузки `pdf/md/txt/log/json/yaml/csv`, разбиения на чанки и сохранения Chroma |

### `src/birka_rag/cli/`

| Модуль | Назначение |
|---|---|
| `chat.py` | CLI `birka-rag` для интерактивного чата |
| `index.py` | CLI `birka-rag-index` для построения индекса |

### Legacy в корне

Скрипты `create_model_machine.py`, `create_data_for_machine.py`, `search_with_machine_learning.py` зависят от старой инфраструктуры Birka и оставлены только как исторические артефакты.

## Потоки данных

### Индексация

```
knowledge/docs + knowledge/code_guides + knowledge/task_samples
или произвольные source paths / отдельные файлы
    ↓  birka-rag-index / create_rag_index()
PyPDFLoader / TextLoader
    ↓  RecursiveCharacterTextSplitter
Чанки
    ↓  HuggingFaceEmbeddings
Векторы
    ↓  Chroma.from_documents
Chroma DB (обычно storage/chroma/*)
```

### Запрос

```
Вопрос пользователя
    ↓  RAGAssistant.ask(question)
Retriever (Chroma) → top_k чанков
    ↓  PromptTemplate
Промпт с контекстом
    ↓  LLM (Ollama/OpenAI/GigaChat/ApiFreeLLM)
Ответ
    ↓  StrOutputParser
Текст ответа
```

## Конфигурация

Основные переменные окружения:

- `RAG_PERSIST_DIR` — путь к векторной базе, по умолчанию `./storage/chroma/default`
- `RAG_SOURCE_PATHS` — список путей к каталогам или файлам источников
- `RAG_SOURCE_EXTENSIONS` — список расширений для индексации
- `RAG_RECURSIVE` — рекурсивный поиск файлов
- `RAG_MODE` — `common` или `per_file`
- `RAG_PROFILE` — активный профиль LLM
- `RAG_UPLOADS_DIR` — каталог для файлов, подаваемых в чат

## LLM-провайдеры

- `ollama` — локальный `ChatOllama`
- `openai` — OpenAI-совместимые API: OpenAI, GigaChat, OpenRouter, Groq, DeepSeek
- `apifreellm` — `ChatApiFreeLLM`

## Публичный API

```python
from birka_rag import RAGAssistant, create_rag_index, select_profile

assistant = RAGAssistant(
    persist_directory="./storage/chroma/default",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

profile = select_profile("gigachat")

create_rag_index(
    persist_directory="./storage/chroma/default",
    source_paths=["./knowledge/docs", "./knowledge/code_guides"],
    model_name="d0rj/e5-large-en-ru",
)
```

## CLI

```bash
birka-rag-index
birka-rag
```

## Миграция

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
