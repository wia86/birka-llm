# Руководство разработчика

## Настройка окружения

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd birka-rag
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Установка в режиме разработки

```bash
# Базовая установка
pip install -e .

# С опциональными зависимостями
pip install -e ".[openai,dev]"
```

### 4. Проверка установки

```bash
python verify_installation.py
```

## Структура проекта

```
birka-rag/
├── src/birka_rag/          # Исходный код пакета
│   ├── __init__.py         # Публичный API
│   ├── core/               # Ядро RAG
│   ├── indexing/           # Индексация
│   └── cli/                # CLI утилиты
├── examples/               # Примеры использования
├── docs/                   # Документация
├── tests/                  # Тесты
├── pyproject.toml          # Конфигурация пакета
└── .env.example            # Шаблон конфигурации
```

## Разработка

### Стиль кода

Проект следует PEP 8 и использует:
- **black** для форматирования
- **ruff** для линтинга
- **mypy** для проверки типов

```bash
# Форматирование
black src/

# Линтинг
ruff check src/

# Проверка типов
mypy src/
```

### Добавление нового провайдера LLM

1. Создайте модуль в `src/birka_rag/core/providers/`:

```python
# src/birka_rag/core/providers/my_provider.py
from langchain_core.language_models.chat_models import BaseChatModel

class ChatMyProvider(BaseChatModel):
    # Реализация
    pass
```

2. Добавьте в `src/birka_rag/core/types.py`:

```python
LLMProvider = Literal["ollama", "openai", "apifreellm", "my_provider"]
```

3. Добавьте метод в `RAGAssistant._create_llm()`:

```python
def _create_llm(self) -> BaseChatModel:
    match self.llm_provider:
        case "my_provider":
            return self._create_my_provider_llm()
        # ...
```

4. Добавьте профиль в `src/birka_rag/core/profiles.py`:

```python
"my_provider": AssistantProfile(
    name="My Provider",
    description="...",
    llm_model="model-name",
    llm_provider="my_provider",
    # ...
)
```

### Добавление новой функциональности

1. Создайте модуль в соответствующем подпакете
2. Добавьте в `__init__.py` подпакета
3. Экспортируйте в корневой `src/birka_rag/__init__.py` если нужно
4. Добавьте примеры в `examples/`
5. Обновите документацию

### Тестирование

```bash
# Запуск тестов (TODO)
pytest

# С покрытием
pytest --cov=birka_rag

# Конкретный тест
pytest tests/test_assistant.py
```

### Документация

Используйте Google-style docstrings:

```python
def function(arg1: str, arg2: int) -> bool:
    """Краткое описание функции.

    Подробное описание, если нужно.

    Args:
        arg1: Описание первого аргумента.
        arg2: Описание второго аргумента.

    Returns:
        Описание возвращаемого значения.

    Raises:
        ValueError: Когда возникает эта ошибка.
    """
    pass
```

## Релиз новой версии

1. Обновите версию в `pyproject.toml`
2. Обновите `CHANGELOG.md`
3. Создайте git tag:

```bash
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

4. Соберите пакет:

```bash
python -m build
```

5. Опубликуйте (если нужно):

```bash
python -m twine upload dist/*
```

## Отладка

### Включение подробного вывода

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Проверка векторной базы

```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="d0rj/e5-large-en-ru")
vectorstore = Chroma(
    persist_directory="./data/chroma",
    embedding_function=embeddings,
)

# Количество документов
print(vectorstore._collection.count())

# Поиск
results = vectorstore.similarity_search("тест", k=3)
for doc in results:
    print(doc.page_content[:100])
```

### Проверка LLM

```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./data/chroma",
    llm_provider="ollama",
    preload=False,  # Не загружать сразу
)

# Проверка LLM отдельно
llm = assistant._initialize_llm()
response = llm.invoke("Привет!")
print(response)
```

## Полезные команды

```bash
# Очистка кэша
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Пересборка пакета
pip install -e . --force-reinstall --no-deps

# Проверка зависимостей
pip list --outdated

# Экспорт зависимостей
pip freeze > requirements-dev.txt
```

## Troubleshooting

### Проблема: CLI команды не найдены

```bash
# Переустановите пакет
pip uninstall birka-rag
pip install -e .
```

### Проблема: Импорты не работают

```bash
# Проверьте PYTHONPATH
echo $PYTHONPATH

# Или установите пакет
pip install -e .
```

### Проблема: Chroma не работает на Python 3.14

Используйте Python 3.11-3.13:

```bash
pyenv install 3.13
pyenv local 3.13
```

## Контакты

Для вопросов и предложений создавайте issue в репозитории.
