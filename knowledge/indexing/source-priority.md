# Source Priority

Приоритет источников для retrieval и генерации ответов support-RAG.

## Приоритет чтения

1. `knowledge/code_guides/known-safe-response-patterns.md`
2. `knowledge/code_guides/question-templates.md`
3. `knowledge/code_guides/errors-and-fixes.md`
4. `knowledge/code_guides/traceback-triage.md`
5. `knowledge/code_guides/task-file-triage.md`
6. `knowledge/code_guides/workflows.md`
7. `knowledge/code_guides/features-overview.md`
8. `knowledge/code_guides/panel-reference.md`
9. `knowledge/code_guides/glossary.md`
10. `docs/*.md`, если документ прошел safety-check и нужен для уточнения политики

## Принцип

Сначала использовать готовые безопасные шаблоны и operational guides, затем описания workflow и только после этого справочные материалы более общего характера.
