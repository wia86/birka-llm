# 📖 Навигация по документации birka-rag

Этот файл поможет найти нужную информацию в проекте.

---

## 🚀 Быстрый старт

**Новичок?** Начните здесь:
1. [START.md](START.md) — главная точка входа (2 мин)
2. [NEXT_STEPS.md](NEXT_STEPS.md) — что делать дальше (5 мин)
3. [QUICKSTART.md](QUICKSTART.md) — быстрый старт (5 мин)

**Опытный пользователь?**
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) — быстрая справка
- [COMMANDS.md](COMMANDS.md) — все команды

---

## 📚 Основная документация

### Для пользователей

| Документ | Описание | Время |
|----------|----------|------|
| [README.md](README.md) | Основная документация | 5 мин |
| [docs/README.md](docs/README.md) | Подробное руководство | 15 мин |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Установка и настройка | 10 мин |

### Для разработчиков

| Документ | Описание | Время |
|----------|----------|------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Руководство разработчика | 10 мин |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Архитектура проекта | 10 мин |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Структура файлов | 5 мин |

### Миграция

| Документ | Описание | Время |
|----------|----------|------|
| [MIGRATION.md](MIGRATION.md) | Миграция со старой структуры | 10 мин |
| [CHANGELOG.md](CHANGELOG.md) | История изменений | 5 мин |

---

## 🎯 По задачам

### Хочу установить пакет
→ [docs/INSTALLATION.md](docs/INSTALLATION.md)

### Хочу быстро начать
→ [QUICKSTART.md](QUICKSTART.md)

### Хочу понять, как работает
→ [ARCHITECTURE.md](ARCHITECTURE.md)

### Хочу мигрировать со старой версии
→ [MIGRATION.md](MIGRATION.md)

### Хочу разрабатывать
→ [CONTRIBUTING.md](CONTRIBUTING.md)

### Хочу посмотреть примеры
→ Папка [examples/](examples/)

### Нужна быстрая справка
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 📂 Примеры кода

Все примеры в папке [examples/](examples/):

| Файл | Описание | Сложность |
|------|----------|-----------|
| [basic_usage.py](examples/basic_usage.py) | Базовое использование | ⭐ |
| [using_profiles.py](examples/using_profiles.py) | Работа с профилями | ⭐ |
| [create_index.py](examples/create_index.py) | Создание индекса | ⭐⭐ |
| [gigachat_example.py](examples/gigachat_example.py) | Пример с GigaChat | ⭐⭐ |
| [custom_profile.py](examples/custom_profile.py) | Кастомный профиль | ⭐⭐⭐ |
| [multiple_knowledge_bases.py](examples/multiple_knowledge_bases.py) | Несколько баз | ⭐⭐⭐ |

---

## 🛠️ Утилиты

| Скрипт | Назначение |
|--------|------------|
| [verify_installation.py](verify_installation.py) | Проверка установки |
| [check_readiness.py](check_readiness.py) | Проверка готовности проекта |
| [pre_commit_check.py](pre_commit_check.py) | Проверка перед коммитом |
| [migrate.py](migrate.py) | Помощь при миграции |
| [demo.py](demo.py) | Демонстрация возможностей |
| [tests/test_basic.py](tests/test_basic.py) | Базовые тесты |

---

## 🔍 Поиск информации

### Установка и настройка
- Как установить? → [docs/INSTALLATION.md](docs/INSTALLATION.md)
- Как настроить? → [.env.example](.env.example)
- Проблемы? → [docs/INSTALLATION.md](docs/INSTALLATION.md) (Troubleshooting)

### Использование
- CLI? → [COMMANDS.md](COMMANDS.md)
- В коде? → [docs/README.md](docs/README.md)
- Примеры? → [examples/](examples/)

### Профили LLM
- Какие доступны? → [README.md](README.md)
- Создать свой? → [examples/custom_profile.py](examples/custom_profile.py)
- GigaChat? → [examples/gigachat_example.py](examples/gigachat_example.py)

### Разработка
- Начать? → [CONTRIBUTING.md](CONTRIBUTING.md)
- Архитектура? → [ARCHITECTURE.md](ARCHITECTURE.md)
- Структура? → [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### Миграция
- Как? → [MIGRATION.md](MIGRATION.md)
- Что изменилось? → [CHANGELOG.md](CHANGELOG.md)
- Помощь? → `python migrate.py`

---

## 📞 Получение помощи

1. **Проверьте документацию** — возможно, ответ уже есть
2. **Запустите утилиты**:
   ```bash
   python verify_installation.py
   python check_readiness.py
   ```
3. **Посмотрите примеры** в [examples/](examples/)
4. **Создайте issue** в репозитории

---

## 🎓 Рекомендуемый порядок

### Для новичков
1. [START.md](START.md) — начало
2. [NEXT_STEPS.md](NEXT_STEPS.md) — что делать
3. [QUICKSTART.md](QUICKSTART.md) — быстрый старт
4. [examples/basic_usage.py](examples/basic_usage.py) — первый пример

### Для опытных
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) — справка
2. [ARCHITECTURE.md](ARCHITECTURE.md) — архитектура
3. [examples/](examples/) — все примеры

### Для миграции
1. [MIGRATION.md](MIGRATION.md) — руководство
2. `python migrate.py` — проверка
3. [CHANGELOG.md](CHANGELOG.md) — изменения

---

## 📝 Быстрые ссылки

- **Установка**: `pip install -e ".[openai]"`
- **Проверка**: `python verify_installation.py`
- **Индекс**: `birka-rag-index`
- **Чат**: `birka-rag`
- **Примеры**: `python examples/basic_usage.py`

---

**Не нашли?** Создайте issue в репозитории.

Последнее обновление: 2025-01-XX | Версия: 0.1.0
