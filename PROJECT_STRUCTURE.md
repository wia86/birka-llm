# Полная структура проекта birka-rag

## Дерево файлов

```
birka-rag/
│
├── src/birka_rag/                    # Основной пакет
│   ├── __init__.py                   # Публичный API
│   ├── py.typed                      # PEP 561 marker
│   │
│   ├── core/                         # Ядро RAG-системы
│   │   ├── __init__.py
│   │   ├── assistant.py              # RAGAssistant класс
│   │   ├── profiles.py               # Профили конфигурации
│   │   ├── types.py                  # LLMProvider и типы
│   │   └── providers/                # Провайдеры LLM
│   │       ├── __init__.py
│   │       ├── gigachat.py           # GigaChat OAuth
│   │       └── apifreellm.py         # ApiFreeLLM клиент
│   │
│   ├── indexing/                     # Индексация документов
│   │   ├── __init__.py
│   │   └── indexer.py                # create_rag_index()
│   │
│   └── cli/                          # CLI утилиты
│       ├── __init__.py
│       ├── chat.py                   # birka-rag команда
│       └── index.py                  # birka-rag-index команда
│
├── examples/                         # Примеры использования
│   ├── basic_usage.py
│   ├── using_profiles.py
│   ├── create_index.py
│   ├── gigachat_example.py
│   ├── custom_profile.py
│   └── multiple_knowledge_bases.py
│
├── docs/                             # Документация
│   ├── README.md                     # Подробное руководство
│   └── INSTALLATION.md               # Установка и настройка
│
├── tests/                            # Тесты
│   ├── __init__.py
│   └── test_basic.py                 # Базовые тесты
│
├── .github/                          # GitHub Actions
│   └── workflows/
│       └── ci.yml                    # CI/CD конфигурация
│
├── pyproject.toml                    # Конфигурация пакета
├── requirements.txt                  # Legacy зависимости
├── requirements-new.txt              # Ссылка на pyproject.toml
│
├── .env.example                      # Шаблон конфигурации
├── .gitignore                        # Git ignore правила
│
├── README.md                         # Основная документация
├── ARCHITECTURE.md                   # Архитектура проекта
├── MIGRATION.md                      # Руководство по миграции
├── CONTRIBUTING.md                   # Руководство разработчика
├── CHANGELOG.md                      # История изменений
├── QUICKSTART.md                     # Быстрый старт
├── SUMMARY.md                        # Резюме реорганизации
├── LICENSE                           # Лицензия
│
└── verify_installation.py            # Скрипт проверки установки
```

## Ключевые файлы

### Конфигурация пакета

**pyproject.toml**
- Метаданные пакета (name, version, description)
- Зависимости (базовые и опциональные)
- Entry points для CLI команд
- Настройки инструментов (black, ruff, mypy)

### Публичный API

**src/birka_rag/__init__.py**
```python
from .core import (
    RAGAssistant,
    AssistantProfile,
    LLMProvider,
    available_profile_names,
    select_profile,
    # ...
)
from .indexing import create_rag_index
```

### CLI команды

**birka-rag** → `src/birka_rag/cli/chat.py:main`
- Интерактивный чат с RAG-ассистентом
- Выбор профиля через RAG_PROFILE
- Демонстрационный вопрос

**birka-rag-index** → `src/birka_rag/cli/index.py:main`
- Создание векторной базы из PDF
- Конфигурация через переменные окружения
- Поддержка GPU

## Установка

```bash
# Базовая установка
pip install -e .

# С OpenAI-совместимыми API
pip install -e ".[openai]"

# Для разработки
pip install -e ".[dev]"
```

## Использование

### CLI

```bash
# Создание индекса
birka-rag-index

# Чат
birka-rag
```

### Код

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

## Проверка

```bash
# Проверка установки
python verify_installation.py

# Базовые тесты
python tests/test_basic.py

# Примеры
python examples/basic_usage.py
```

## Документация

| Файл | Описание |
|------|----------|
| README.md | Основная документация |
| docs/README.md | Подробное руководство |
| docs/INSTALLATION.md | Установка и настройка |
| QUICKSTART.md | Быстрый старт |
| MIGRATION.md | Миграция со старой структуры |
| CONTRIBUTING.md | Руководство разработчика |
| ARCHITECTURE.md | Архитектура проекта |
| CHANGELOG.md | История изменений |
| SUMMARY.md | Резюме реорганизации |

## Примеры

| Файл | Описание |
|------|----------|
| basic_usage.py | Базовое использование |
| using_profiles.py | Работа с профилями |
| create_index.py | Создание индекса |
| gigachat_example.py | Пример с GigaChat |
| custom_profile.py | Кастомный профиль |
| multiple_knowledge_bases.py | Несколько баз знаний |

## Зависимости

### Базовые (обязательные)

- python-dotenv
- pydantic-settings
- pypdf
- langchain + langchain-community + langchain-chroma
- langchain-huggingface + langchain-text-splitters
- langchain-ollama
- chromadb
- sentence-transformers
- torch
- httpx, requests

### Опциональные

**[openai]**
- langchain-openai
- openai

**[dev]**
- pytest, pytest-cov
- black, ruff, mypy

## Миграция

### Импорты

```python
# Было
from rag_assistant import RAGAssistant

# Стало
from birka_rag import RAGAssistant
```

### CLI

```bash
# Было
python data_from_gost/run_lln.py

# Стало
birka-rag
```

## Статус

✅ Структура пакета создана
✅ Публичный API определён
✅ CLI команды настроены
✅ Документация написана
✅ Примеры подготовлены
✅ Тесты созданы
✅ CI/CD настроен
✅ Обратная совместимость сохранена

**Проект готов к использованию!**
