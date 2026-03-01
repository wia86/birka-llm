# birka-llm

Отдельный проект для RAG и чата с LLM по нормативам (эмбеддинги, Chroma, GigaChat/Ollama/OpenAI). Вынесен из репозитория Birka.

Рекомендуется Python 3.11–3.13 (Chroma и часть LangChain могут некорректно работать на 3.14).

## Быстрый старт

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

2. Настройте переменные окружения (скопируйте `.env.example` в `.env` и задайте пути):

- `RAG_PERSIST_DIR` — каталог для сохранения векторной базы Chroma.
- `RAG_SOURCE_PATHS` — пути к папкам с PDF (разделитель `;` на Windows).
- Для GigaChat: `GIGACHAT_API_KEY`.

3. Создание индекса эмбеддингов (офлайн):

```bash
python data_from_gost/create_rag.py
```

Запуск из корня репозитория; при необходимости задайте `PYTHONPATH=.` или перейдите в `data_from_gost` и запустите `python create_rag.py`.

4. Чат с ассистентом:

```bash
cd data_from_gost
python run_lln.py
```

Или из корня: `python data_from_gost/run_lln.py` (при корректном PYTHONPATH).

Подробнее по RAG и GigaChat — в [data_from_gost/README.md](data_from_gost/README.md) и [data_from_gost/GIGACHAT_SETUP.md](data_from_gost/GIGACHAT_SETUP.md).

## Структура

- `data_from_gost/` — RAG: создание индекса (`create_rag.py`), чат (`run_lln.py`), модуль `rag_assistant/`.
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
