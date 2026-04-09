# birka-llm

Отдельный проект для RAG и чата с LLM по нормативам и материалам техподдержки (эмбеддинги, Chroma, GigaChat/Ollama/OpenAI). Вынесен из репозитория Birka.

Рекомендуется Python 3.11–3.13 (Chroma и часть LangChain могут некорректно работать на 3.14).

## Быстрый старт

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

2. Подготовьте структуру знаний (локально в проекте):

```text
knowledge/
  docs/          # документация (md/pdf/txt)
  code_guides/   # безопасные пояснения по коду для поддержки
  task_samples/  # примеры файлов заданий
storage/
  chroma/        # векторные базы
  uploads/       # файлы, подаваемые в чат
```

3. Настройте переменные окружения (скопируйте `.env.example` в `.env` и задайте пути):

- `RAG_PERSIST_DIR` — каталог для сохранения векторной базы Chroma.
- `RAG_SOURCE_PATHS` — пути к папкам знаний (разделитель `;` на Windows).
- `RAG_SOURCE_EXTENSIONS` — какие типы файлов индексировать (по умолчанию: `pdf/md/txt/log/json/yaml/csv`).
- Для GigaChat: `GIGACHAT_API_KEY`.

4. Создание индекса эмбеддингов (офлайн):

```bash
python data_from_gost/create_rag.py
```

Запуск из корня репозитория; при необходимости задайте `PYTHONPATH=.` или перейдите в `data_from_gost` и запустите `python create_rag.py`.

5. Чат с ассистентом:

```bash
cd data_from_gost
python run_lln.py
```

Или из корня: `python data_from_gost/run_lln.py` (при корректном PYTHONPATH).

В интерактивном чате доступны специальные команды:
- `:traceback` — вставить traceback (многострочно, завершить `END`) и получить разбор.
- `:taskfile <путь> [| вопрос]` — загрузить файл задания на расчет и получить диагностику.

Подробнее по RAG и GigaChat — в [data_from_gost/README.md](data_from_gost/README.md) и [data_from_gost/GIGACHAT_SETUP.md](data_from_gost/GIGACHAT_SETUP.md).

## Структура

- `data_from_gost/` — RAG: создание индекса (`create_rag.py`), чат (`run_lln.py`), модуль `rag_assistant/`.
- `knowledge/` — база знаний для индексации (документация, code guides, примеры заданий).
- `storage/` — локальные runtime-данные (векторная база, загруженные файлы).
- `machine_learning_model/` — данные для TKZ (xlsx).
- `create_data_for_machine.py`, `create_model_machine.py`, `search_with_machine_learning.py` — **legacy**: скрипты для TKZ/оборудования, зависят от старых путей `dir_common`/`moduls` и в текущем виде в этом репозитории не запускаются; оставлены для истории.

## Публикация на удалённый репозиторий

После создания репозитория на GitHub/GitLab выполните:

```bash
git remote add origin <URL_репозитория>
git push -u origin master
```

## Лицензия

Внутренний инструмент для электротехнических расчётов (проект Birka).
