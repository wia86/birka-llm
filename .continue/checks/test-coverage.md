---
name: Test Coverage
description: Ensure new or changed behavior is covered by tests
---

Review changed code and add or update tests where behavior changed.

Fail the check if any of these are true:

- New public functions, classes, or CLI behavior were added without corresponding tests.
- Logic in `src/birka_rag/` changed but tests were not added or updated in `tests/`.
- A source feature was modified and existing tests no longer cover the main success and error paths.

No changes needed if the PR only updates docs, comments, formatting, or non-runtime metadata.
