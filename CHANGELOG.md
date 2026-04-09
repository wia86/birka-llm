# Changelog

Все значимые изменения в проекте документируются в этом файле.

## [0.1.0] - 2025-01-XX

### Добавлено

#### Структура пакета
- Создана структура Python-пакета в `src/birka_rag/`
- Добавлен `pyproject.toml` с метаданными и зависимостями
- Публичный API в `src/birka_rag/__init__.py`
- Marker файл `py.typed` для поддержки типизации

#### Модули
- `src/birka_rag/core/` — ядро RAG-системы
  - `assistant.py` — класс RAGAssistant
  - `profiles.py` — профили конфигурации LLM
  - `types.py` — типы данных (LLMProvider)
  - `providers/` — провайдеры LLM (GigaChat, ApiFreeLLM)
- `src/birka_rag/indexing/` — создание векторной базы
  - `indexer.py` — функция create_rag_index()
- `src/birka_rag/cli/` — CLI утилиты
  - `chat.py` — интерактивный чат (команда birka-rag)
  - `index.py` — создание индекса (команда birka-rag-index)

#### CLI команды
- `birka-rag` — интерактивный чат с RAG-ассистентом
- `birka-rag-index` — создание векторной базы из PDF

#### Документация
- `docs/README.md` — подробная документация по использованию
- `MIGRATION.md` — руководство по миграции со старой структуры
- Обновлён `ARCHITECTURE.md` с описанием новой структуры
- Обновлён корневой `README.md`

#### Примеры
- `examples/basic_usage.py` — базовый пример использования
- `examples/using_profiles.py` — работа с профилями
- `examples/create_index.py` — создание индекса программно
- `examples/gigachat_example.py` — пример с GigaChat

#### Инструменты
- `verify_installation.py` — скрипт проверки установки
- `.env.example` — шаблон конфигурации

#### Опциональные зависимости
- `[openai]` — для работы с OpenAI-совместимыми API
- `[dev]` — инструменты разработки (pytest, black, ruff, mypy)

### Изменено

#### Импорты
- Старые импорты `from rag_assistant import ...` заменены на `from birka_rag import ...`
- Все публичные API экспортируются из корневого `__init__.py`

#### Структура
- Код из `data_from_gost/rag_assistant/` перенесён в `src/birka_rag/core/`
- Функция `create_rag()` переименована в `create_rag_index()`
- Скрипты `create_rag.py` и `run_lln.py` заменены на CLI команды

#### Провайдеры
- GigaChat утилиты перенесены в `core/providers/gigachat.py`
- ApiFreeLLM клиент перенесён в `core/providers/apifreellm.py`

### Сохранено (обратная совместимость)

- API классов и методов не изменился
- Формат конфигурации профилей
- Переменные окружения
- Формат векторной базы Chroma

### Удалено

- `data_from_gost/` — legacy код (весь функционал перенесён в `src/birka_rag/`)

## Планы на будущее

### [0.2.0]
- [ ] Добавить unit-тесты
- [ ] Добавить интеграционные тесты
- [ ] Улучшить обработку ошибок
- [ ] Добавить логирование
- [ ] Поддержка конфигурации через YAML/TOML

### [0.3.0]
- [ ] Web-интерфейс (опциональный)
- [ ] REST API
- [ ] Поддержка других форматов документов (DOCX, TXT)
- [ ] Кэширование запросов

### [1.0.0]
- [ ] Стабильный публичный API
- [ ] Полное покрытие тестами
- [ ] Документация на английском
- [ ] Публикация на PyPI
