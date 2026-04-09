# Knowledge Directory

Локальная база знаний support-RAG для Birka. Здесь должны храниться только материалы, разрешенные для передачи в LLM после safety-check.

## Что читать первым

Если задача саппорта связана с ответом пользователю, рекомендуемый порядок чтения такой:

1. `code_guides/known-safe-response-patterns.md`
2. `code_guides/question-templates.md`
3. `code_guides/errors-and-fixes.md`
4. `code_guides/traceback-triage.md`
5. `code_guides/task-file-triage.md`
6. `code_guides/workflows.md`
7. `code_guides/features-overview.md`
8. `code_guides/panel-reference.md`
9. `code_guides/glossary.md`

## Структура каталога

### `code_guides/`
Основной curated knowledge для техподдержки.

Ключевые файлы:
- `features-overview.md` — карта возможностей продукта.
- `workflows.md` — пошаговые сценарии в терминах интерфейса.
- `errors-and-fixes.md` — типовые ошибки и исправления.
- `traceback-triage.md` — разбор traceback.
- `task-file-triage.md` — разбор файла задания.
- `limits-and-assumptions.md` — ограничения и допущения.
- `glossary.md` — словарь терминов.
- `indexing-allowlist.md` — что можно индексировать.
- `panel-reference.md` — справочник панелей.
- `module-entrypoints.md` — карта модулей и точек входа.
- `result-artifacts.md` — типы выходных результатов.
- `input-signals-checklist.md` — чеклист входных сигналов для triage.
- `question-templates.md` — шаблоны уточняющих вопросов.
- `known-safe-response-patterns.md` — безопасные шаблоны ответов.

### `indexing/`
Материалы для контроля качества индексации.

Файлы:
- `denylist-patterns.md` — признаки чувствительных данных.
- `source-priority.md` — приоритет источников для retrieval.

### `examples/`
Обезличенные примеры для обучения и тестирования support-RAG.

Файлы:
- `task-file-good-case.md`
- `task-file-missing-source.md`
- `task-file-panel-conflict.md`
- `traceback-sanitized-example.md`
- `support-response-example.md`

### `docs/`
Пользовательская документация и дополнительные материалы, которые можно подключать только после проверки приватности и полезности.

### `task_samples/`
Примеры файлов заданий для тестирования. Хранить только обезличенные и безопасные версии.

## Правила использования

- Не индексировать сырой код напрямую вместо curated guides.
- Не добавлять в knowledge полные пути, ключи, токены, внутренние URL и сырые логи.
- Для triage всегда переводить ответ в термины пользовательского интерфейса.
- Перед индексацией запускать локальную проверку support knowledge.

## Локальная проверка

Скрипт проекта:

```bash
python scripts/check_support_knowledge.py
```

Если `python` не доступен в PATH, использовать локальный launcher вашей среды.
