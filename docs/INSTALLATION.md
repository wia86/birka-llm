# Установка и использование

## Содержание

- [Требования](#требования)
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Профили LLM](#профили-llm)
- [Примеры](#примеры)
- [Troubleshooting](#troubleshooting)

## Требования

- Python 3.11-3.13 (Chroma несовместим с 3.14)
- 4+ GB RAM
- Для GPU: CUDA-совместимая видеокарта

### Опциональные зависимости

- **Ollama** — для локальной LLM
- **OpenAI API ключ** — для OpenAI/GigaChat/OpenRouter и др.
- **PyTorch с CUDA** — для ускорения на GPU (опционально, работает и на CPU)

## Установка

### Базовая установка

```bash
pip install -e .
```

### С поддержкой OpenAI-совместимых API

```bash
pip install -e ".[openai]"
```

### Для разработки

```bash
pip install -e ".[dev]"
```

### Проверка установки

```bash
python verify_installation.py
```

### Настройка кэша моделей (опционально)

По умолчанию модели эмбеддингов сохраняются в `~/.cache/huggingface/`. Для изменения расположения:

```bash
# В .env или переменных окружения
HF_HOME=/path/to/cache
# или
TRANSFORMERS_CACHE=/path/to/cache/hub
```

Это полезно для:
- Хранения моделей на другом диске
- Совместного использования кэша между проектами
- Экономии места на системном диске

## Быстрый старт

### 1. Настройка окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Минимальная конфигурация:

```env
RAG_PERSIST_DIR=./data/chroma
RAG_SOURCE_PATHS=./docs
RAG_MODEL_NAME=d0rj/e5-large-en-ru
RAG_PROFILE=ollama_local
```

### 2. Создание индекса

```bash
birka-rag-index
```

### 3. Запуск чата

```bash
birka-rag
```

## Конфигурация

### Переменные окружения

#### Общие

- `RAG_PERSIST_DIR` — путь к векторной базе (по умолчанию `./data/chroma_default`)
- `RAG_MODEL_NAME` — модель эмбеддингов (по умолчанию `d0rj/e5-large-en-ru`)
- `RAG_PROFILE` — активный профиль LLM

#### Индексация

- `RAG_SOURCE_PATHS` — пути к PDF (разделитель `;` на Windows, `:` на Unix)
- `RAG_RECURSIVE` — искать во вложенных папках (`1` или `0`)
- `RAG_MODE` — режим индексации (`common` или `per_file`)

#### Провайдеры LLM

- `GIGACHAT_API_KEY` — ключ GigaChat (Base64 строка из кабинета)
- `GIGACHAT_CLIENT_ID` — Client ID для GigaChat (опционально)
- `GIGACHAT_VERIFY_SSL_CERTS` — проверка SSL для GigaChat (по умолчанию 1)
- `OPENAI_API_KEY` — ключ OpenAI
- `OPENROUTER_API_KEY` — ключ OpenRouter
- `GROQ_API_KEY` — ключ Groq
- `DEEPSEEK_API_KEY` — ключ DeepSeek
- `APIFREELLM_API_KEY` — ключ ApiFreeLLM

#### Кэш моделей

- `HF_HOME` — директория для кэша HuggingFace (по умолчанию `~/.cache/huggingface`)
- `TRANSFORMERS_CACHE` — альтернативная настройка кэша

### Файл конфигурации

Создайте `.env` файл в корне проекта:

```env
# Векторная база
RAG_PERSIST_DIR=./data/chroma
RAG_SOURCE_PATHS=/path/to/pdfs
RAG_MODEL_NAME=d0rj/e5-large-en-ru

# LLM профиль
RAG_PROFILE=ollama_local

# API ключи (если нужны)
# GIGACHAT_API_KEY=ваш_ключ
# OPENAI_API_KEY=sk-...
```

## Использование

### CLI

#### Создание индекса

```bash
# Из переменных окружения
birka-rag-index

# Или задайте переменные напрямую
RAG_SOURCE_PATHS=/path/to/pdfs birka-rag-index
```

#### Чат с ассистентом

```bash
# Локальная Ollama
RAG_PROFILE=ollama_local birka-rag

# GigaChat
RAG_PROFILE=gigachat GIGACHAT_API_KEY=ваш_ключ birka-rag
```

### Программное использование

#### Базовый пример

```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Какие есть схемно-режимные мероприятия?")
print(answer)
```

#### Использование профилей

```python
from birka_rag import RAGAssistant, select_profile

# Выбор профиля
profile = select_profile("gigachat")
assistant = RAGAssistant(**profile.to_kwargs())

# Интерактивный режим
assistant.chat()
```

#### Создание индекса

```python
from birka_rag import create_rag_index

create_rag_index(
    persist_directory="./data/chroma",
    source_paths=["./docs", "./standards"],
    model_name="d0rj/e5-large-en-ru",
    chunk_size=1000,
    chunk_overlap=200,
    recursive=True,
    rag_mode="common",
)
```

## Профили LLM

### Доступные профили

```python
from birka_rag import available_profile_names, format_profiles

# Список профилей
print(available_profile_names())

# Подробное описание
print(format_profiles())
```

### Профили

- **ollama_local** — локальная Ollama
- **openai_cloud** — OpenAI API
- **gigachat** — GigaChat от Сбера
- **openrouter** — OpenRouter (доступ к разным моделям)
- **groq** — Groq (быстрая инференс)
- **deepseek** — DeepSeek API
- **apifreellm** — ApiFreeLLM (бесплатный API)

### Кастомный профиль

```python
from birka_rag import AssistantProfile, RAGAssistant
from pathlib import Path

custom_profile = AssistantProfile(
    name="Мой профиль",
    persist_directory=Path("./data/chroma"),
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
    temperature=0.3,
    top_k=10,
)

assistant = RAGAssistant(**custom_profile.to_kwargs())
```

## Примеры

Готовые примеры в папке `examples/`:

- `basic_usage.py` — базовое использование
- `using_profiles.py` — работа с профилями
- `create_index.py` — создание индекса
- `gigachat_example.py` — пример с GigaChat
- `custom_profile.py` — кастомный профиль
- `multiple_knowledge_bases.py` — несколько баз знаний

Запуск примера:

```bash
python examples/basic_usage.py
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
# Убедитесь, что пакет установлен
pip list | grep birka-rag

# Переустановите
pip install -e .
```

### Проблема: Ollama недоступна

```bash
# Проверьте, что Ollama запущена
ollama serve

# Проверьте модель
ollama list
ollama pull llama3.2:3b
```

### Проблема: GPU не обнаружен

```bash
# Проверьте PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# Переустановите PyTorch с CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**Примечание:** PyTorch с CUDA не обязателен. Проект работает на CPU, но медленнее при создании эмбеддингов. Для небольших объёмов PDF это приемлемо.

### Проблема: GigaChat — ошибка авторизации

**Получение API ключа:**

1. Зарегистрируйтесь на [https://developers.sber.ru/studio/](https://developers.sber.ru/studio/)
2. Создайте проект и выберите "GigaChat API"
3. Сгенерируйте "ключ авторизации" (Base64 строка)
4. Задайте в `.env`:

```env
GIGACHAT_API_KEY=ваш_ключ_авторизации
```

**Два способа настройки:**

- **Способ 1** (рекомендуется): один ключ из кабинета (Base64 строка)
  ```env
  GIGACHAT_API_KEY=<Base64_строка_из_кабинета>
  ```

- **Способ 2**: отдельно Client ID и Secret
  ```env
  GIGACHAT_CLIENT_ID=<uuid_приложения>
  GIGACHAT_API_KEY=<client_secret>
  ```

**OAuth:** Проект автоматически получает access_token (~30 мин) при каждом запуске.

**Ресурсы:**
- Документация: [https://developers.sber.ru/docs/ru/gigachat/overview](https://developers.sber.ru/docs/ru/gigachat/overview)
- Тарифы: [https://developers.sber.ru/docs/ru/gigachat/api/tariffs](https://developers.sber.ru/docs/ru/gigachat/api/tariffs)
- Поддержка: [@gigachat_helpbot](https://t.me/gigachat_helpbot)

### Проблема: Chroma не работает на Python 3.14

Используйте Python 3.11-3.13:

```bash
# С pyenv
pyenv install 3.13
pyenv local 3.13

# Или создайте новое окружение
python3.13 -m venv .venv
```

### Проблема: Ошибка при создании индекса

```bash
# Проверьте пути к PDF
ls -la ./docs/*.pdf

# Проверьте переменные окружения
echo $RAG_SOURCE_PATHS

# Запустите с отладкой
python -c "from birka_rag import create_rag_index; create_rag_index(...)"
```

### Получение помощи

1. Проверьте установку: `python verify_installation.py`
2. Запустите тесты: `python tests/test_basic.py`
3. Проверьте логи
4. Создайте issue в репозитории с описанием проблемы
