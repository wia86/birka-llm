# Архитектура birka-rag

RAG-система и чат с LLM по нормативным документам (эмбеддинги, Chroma, GigaChat/Ollama/OpenAI).
Вынесена из основного репозитория Birka.

## Новая структура (пакет)

```
birka-rag/
├── src/birka_rag/               # Основной пакет
│   ├── __init__.py              # Публичный API
│   ├── core/                    # Ядро RAG
│   │   ├── __init__.py
│   │   ├── assistant.py         # RAGAssistant — ядро (Chroma + LLM)
│   │   ├── profiles.py          # Профили конфигурации
│   │   ├── types.py             # LLMProvider и другие типы
│   │   └── providers/           # Провайдеры LLM
│   │       ├── __init__.py
│   │       ├── gigachat.py      # GigaChat OAuth
│   │       └── apifreellm.py    # ApiFreeLLM клиент
│   ├── indexing/                # Создание индекса
│   │   ├── __init__.py
│   │   └── indexer.py           # create_rag_index()
│   ├── cli/                     # CLI утилиты
│   │   ├── __init__.py
│   │   ├── chat.py              # birka-rag (чат)
│   │   └── index.py             # birka-rag-index (индексация)
│   └── py.typed                 # PEP 561 marker
├── examples/                    # Примеры использования
│   ├── basic_usage.py
│   ├── using_profiles.py
│   ├── create_index.py
│   └── gigachat_example.py
├── docs/                        # Документация
│   ├── README.md
│   └── INSTALLATION.md
├── tests/                       # Тесты
│   └── test_basic.py
├── pyproject.toml               # Конфигурация пакета
├── README.md
├── ARCHITECTURE.md
├── MIGRATION.md
└── .env.example
```

## Модули

### src/birka_rag/core/ — ядро RAG

| Модуль | Назначение |
|---|---|
| `assistant.py` | `RAGAssistant` — загрузка Chroma, embeddings, LLM, цепочка RAG, методы `ask()` / `chat()` |
| `profiles.py` | `AssistantProfile` (dataclass) — конфигурация провайдеров; `select_profile()`, `set_active_profile()` |
| `types.py` | `LLMProvider = Literal["ollama", "openai", "apifreellm"]` |
| `providers/gigachat.py` | Утилита для получения токена GigaChat (OAuth) |
| `providers/apifreellm.py` | Клиент для ApiFreeLLM API |

### src/birka_rag/indexing/ — индексация

| Модуль | Назначение |
|---|---|
| `indexer.py` | `create_rag_index()` — загрузка PDF, разбивка на чанки, создание Chroma-базы |

### src/birka_rag/cli/ — CLI

| Модуль | Назначение |
|---|---|
| `chat.py` | `birka-rag` — интерактивный чат с RAG |
| `index.py` | `birka-rag-index` — создание индекса из PDF |

### Legacy (корень)

Зависят от `moduls` и `dir_common` из основного репозитория Birka — **не запускаются** в этом проекте.

| Модуль | Назначение |
|---|---|
| `create_model_machine.py` | Обучение SentenceTransformer на Excel-парах |
| `create_data_for_machine.py` | Подготовка данных: сравнение строк, обработка xlsx |
| `search_with_machine_learning.py` | Поиск совпадений энергообъектов по эмбеддингам |

## Зависимости

Основные:
- `langchain` + `langchain-chroma`, `langchain-huggingface`, `langchain-ollama`, `langchain-openai`
- `chromadb`, `sentence-transformers`, `torch`
- `pypdf` (загрузка PDF)

Конфигурация — через переменные окружения (см. `.env.example`).

## Потоки данных

### Индексация

```
PDF файлы
    ↓  birka-rag-index (create_rag_index)
PyPDFLoader → Documents
    ↓  RecursiveCharacterTextSplitter
Чанки (chunks)
    ↓  HuggingFaceEmbeddings
Векторы (embeddings)
    ↓  Chroma.from_documents
Chroma DB (persist_directory)
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

## LLM-провайдеры

- **Ollama** (локальный) — `ChatOllama`
- **OpenAI / GigaChat / OpenRouter / Groq / DeepSeek** (сетевой) — `ChatOpenAI` (OpenAI-совместимый API)
- **ApiFreeLLM** (сетевой) — `ChatApiFreeLLM` (собственный формат API)

## Публичный API

### Основные классы

```python
from birka_rag import RAGAssistant, AssistantProfile

# Создание ассистента
assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

# Запрос
answer = assistant.ask("Вопрос")

# Интерактивный режим
assistant.chat()
```

### Профили

```python
from birka_rag import select_profile, available_profile_names

# Список профилей
print(available_profile_names())

# Выбор профиля
profile = select_profile("gigachat")
assistant = RAGAssistant(**profile.to_kwargs())
```

### Индексация

```python
from birka_rag import create_rag_index

create_rag_index(
    persist_directory="./data/chroma",
    source_paths=["./docs"],
    model_name="d0rj/e5-large-en-ru",
)
```

## CLI команды

```bash
# Создание индекса
birka-rag-index

# Чат с ассистентом
birka-rag
```

## Миграция

Подробное руководство по миграции со старой структуры: [MIGRATION.md](MIGRATION.md)

### Основные изменения

```python
# Импорты
from birka_rag import RAGAssistant, select_profile

# CLI команды
birka-rag-index  # создание индекса
birka-rag        # интерактивный чат
```
