# Команды для быстрого старта

## Установка и проверка

```bash
# 1. Установка пакета
pip install -e ".[openai]"

# 2. Проверка установки
python verify_installation.py

# 3. Проверка готовности
python check_readiness.py

# 4. Помощь при миграции
python migrate.py

# 5. Базовые тесты
python tests/test_basic.py
```

## Настройка

```bash
# Копировать шаблон конфигурации
cp .env.example .env

# Отредактировать (Windows)
notepad .env

# Отредактировать (Linux/macOS)
nano .env
```

## Использование CLI

```bash
# Создание индекса из PDF
birka-rag-index

# Интерактивный чат
birka-rag

# С конкретным профилем
RAG_PROFILE=gigachat birka-rag
```

## Примеры

```bash
# Базовое использование
python examples/basic_usage.py

# Работа с профилями
python examples/using_profiles.py

# Создание индекса программно
python examples/create_index.py

# GigaChat
python examples/gigachat_example.py

# Кастомный профиль
python examples/custom_profile.py

# Несколько баз знаний
python examples/multiple_knowledge_bases.py
```

## Git

```bash
# Проверить статус
git status

# Добавить все файлы
git add .

# Коммит
git commit -m "Реорганизация в пакет birka-rag v0.1.0"

# Отправить
git push origin main
```

## Разработка

```bash
# Форматирование
black src/

# Линтинг
ruff check src/

# Типы
mypy src/

# Тесты
pytest

# Сборка
python -m build
```

## Быстрая справка

```bash
# Импорты
from birka_rag import RAGAssistant, select_profile, create_rag_index

# Создание ассистента
assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

# Вопрос
answer = assistant.ask("Вопрос")

# Чат
assistant.chat()
```

## Помощь

```bash
# Документация
cat README.md
cat QUICKSTART.md
cat docs/README.md

# Проверка
python verify_installation.py
python check_readiness.py

# Примеры
ls examples/
```
