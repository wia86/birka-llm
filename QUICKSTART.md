# Быстрый старт

Этот файл содержит минимальные инструкции для быстрого начала работы.

## 1. Установка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd birka-rag

# Создайте виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Установите пакет
pip install -e ".[openai]"

# Проверьте установку
python verify_installation.py
```

## 2. Настройка

Скопируйте `.env.example` в `.env` и настройте:

```bash
cp .env.example .env
```

Минимальная конфигурация для локальной Ollama:

```env
RAG_PERSIST_DIR=./data/chroma
RAG_SOURCE_PATHS=./docs
RAG_MODEL_NAME=d0rj/e5-large-en-ru
RAG_PROFILE=ollama_local
```

## 3. Создание индекса

```bash
# Убедитесь, что Ollama запущена
ollama serve

# Создайте индекс из PDF
birka-rag-index
```

## 4. Запуск чата

```bash
birka-rag
```

## 5. Использование в коде

```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Ваш вопрос")
print(answer)
```

## Примеры

Смотрите готовые примеры в папке `examples/`:

```bash
python examples/basic_usage.py
python examples/using_profiles.py
python examples/create_index.py
```

## Документация

- [README.md](README.md) — основная документация
- [docs/README.md](docs/README.md) — подробное руководство
- [MIGRATION.md](MIGRATION.md) — миграция со старой структуры
- [CONTRIBUTING.md](CONTRIBUTING.md) — руководство разработчика

## Помощь

Если что-то не работает:

1. Проверьте установку: `python verify_installation.py`
2. Запустите базовые тесты: `python tests/test_basic.py`
3. Проверьте логи и переменные окружения
4. Создайте issue в репозитории
