# RAG Assistant с поддержкой GigaChat

Этот модуль предоставляет систему Retrieval-Augmented Generation (RAG) с поддержкой различных LLM провайдеров, включая GigaChat от Сбера.

## Доступные профили

- **ollama_local**: Локальная модель через Ollama
- **openai_cloud**: OpenAI-совместимый API
- **gigachat**: GigaChat от Сбера (требует настройки API ключа)

## Быстрый старт с GigaChat

### 1. Настройка API ключа

```bash
# Установите переменную окружения
export GIGACHAT_API_KEY="ваш_ключ_авторизации"
```

Подробные инструкции по получению API ключа см. в файле [GIGACHAT_SETUP.md](GIGACHAT_SETUP.md).

### 2. Проверка настройки

```bash
python test_gigachat_connection.py
```

### 3. Запуск

```bash
# Интерактивный режим с GigaChat
python run_lln.py

# Или программно
from rag_assistant import RAGAssistant, set_active_profile

set_active_profile("gigachat")
# Ассистент автоматически использует переменную GIGACHAT_API_KEY
```

## Структура проекта

- `rag_assistant/`: Основной модуль RAG ассистента
  - `assistant.py`: Класс RAGAssistant
  - `profiles.py`: Конфигурации профилей моделей
  - `giga_get_token.py`: Утилиты для работы с GigaChat
  - `llm_types.py`: Типы данных для LLM
- `run_lln.py`: Демонстрационный скрипт
- `test_gigachat_connection.py`: Скрипт проверки подключения
- `GIGACHAT_SETUP.md`: Инструкции по настройке GigaChat API

## API Reference

### RAGAssistant

```python
assistant = RAGAssistant(
    persist_directory="путь/к/векторной/базе",
    model_name="BAAI/bge-m3",  # Модель для embeddings
    llm_model="GigaChat",      # Название модели LLM
    llm_provider="openai",     # Провайдер (openai для GigaChat)
    llm_api_base="https://gigachat.devices.sberbank.ru/api/",
    llm_api_key=None,          # Будет взят из GIGACHAT_API_KEY
)

# Задание вопроса
answer = assistant.ask("Ваш вопрос")

# Интерактивный режим
assistant.chat()
```

### Управление профилями

```python
from rag_assistant import set_active_profile, get_active_profile, available_profile_names

# Просмотр доступных профилей
print(available_profile_names())

# Установка активного профиля
set_active_profile("gigachat")

# Получение текущего профиля
profile = get_active_profile()
```

## Требования

Для работы с GigaChat необходимо:

1. **Зарегистрироваться** в [Studio](https://developers.sber.ru/studio/)
2. **Создать проект** GigaChat API
3. **Сгенерировать ключ авторизации**
4. **Установить переменную окружения** `GIGACHAT_API_KEY`

## Устранение проблем

### ModuleNotFoundError
Установите недостающие зависимости:
```bash
pip install torch langchain-chroma langchain-huggingface langchain-ollama
```

### Ошибка API ключа
- Проверьте, что переменная `GIGACHAT_API_KEY` установлена
- Убедитесь, что ключ скопирован правильно из личного кабинета
- Проверьте срок действия ключа

### Ошибка подключения
- Проверьте интернет-соединение
- Убедитесь, что есть доступные токены в аккаунте
- Проверьте статус проекта в личном кабинете Studio

## Разработка

Для добавления нового провайдера LLM:

1. Добавьте новый профиль в `profiles.py`
2. Обновите логику в `assistant.py` для обработки нового провайдера
3. Добавьте необходимые зависимости в requirements

## Лицензия

Проект "Бирка" - внутренний инструмент для электротехнических расчетов.
