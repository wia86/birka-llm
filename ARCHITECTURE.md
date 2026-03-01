# Архитектура birka-llm

RAG-система и чат с LLM по нормативным документам (эмбеддинги, Chroma, GigaChat/Ollama/OpenAI).
Вынесена из основного репозитория Birka.

## Структура

```
birka-llm/
├── data_from_gost/              # RAG-система
│   ├── rag_assistant/           # Пакет RAG-помощника
│   │   ├── __init__.py          # Публичный API
│   │   ├── assistant.py         # RAGAssistant — ядро (Chroma + LLM)
│   │   ├── profiles.py          # Профили конфигурации (Ollama / OpenAI / GigaChat)
│   │   ├── llm_types.py         # Тип LLMProvider
│   │   └── giga_get_token.py    # Утилита токена GigaChat
│   ├── create_rag.py            # Создание векторной базы (PDF → Chroma)
│   ├── run_lln.py               # Точка входа: чат с RAG
│   ├── load_llm.py              # Фабрика эмбеддингов (bge-m3, e5-large)
│   ├── giga_api.py              # OAuth-аутентификация GigaChat
│   └── test_gigachat_connection.py  # Проверка подключения GigaChat
├── create_model_machine.py      # [legacy] Обучение SentenceTransformer
├── create_data_for_machine.py   # [legacy] Подготовка данных для ML
├── search_with_machine_learning.py  # [legacy] Поиск совпадений энергообъектов
├── requirements.txt
└── .env.example
```

## Модули

### data_from_gost/rag_assistant/ — ядро RAG

| Модуль | Назначение |
|---|---|
| `assistant.py` | `RAGAssistant` — загрузка Chroma, embeddings, LLM, цепочка RAG, методы `ask()` / `chat()` |
| `profiles.py` | `AssistantProfile` (dataclass) — конфигурация провайдеров; `select_profile()`, `set_active_profile()` |
| `llm_types.py` | `LLMProvider = Literal["ollama", "openai"]` |
| `giga_get_token.py` | Утилита для получения токена GigaChat |

### data_from_gost/ — скрипты

| Модуль | Назначение |
|---|---|
| `create_rag.py` | Загрузка PDF, разбивка на чанки, создание Chroma-базы |
| `run_lln.py` | Точка входа: выбор профиля, демо-вопрос, интерактивный чат |
| `load_llm.py` | Фабрика `HuggingFaceEmbeddings` (bge-m3, multilingual-e5-large) |
| `giga_api.py` | OAuth-авторизация через Sber API для GigaChat |
| `test_gigachat_connection.py` | Проверка переменных окружения и тестовый запрос к GigaChat |

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

```
PDF файлы
    ↓  create_rag.py
Chroma DB (persist_directory)
    ↓  RAGAssistant.ask(question)
Retriever → top_k чанков → PromptTemplate → LLM → StrOutputParser → ответ
```

LLM-провайдеры:
- **Ollama** (локальный) — `ChatOllama`
- **OpenAI / GigaChat** (сетевой) — `ChatOpenAI` (OpenAI-совместимый API)
