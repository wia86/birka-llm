---
name: Documentation Freshness
description: Keep README/docs in sync with public API and CLI changes
---

Check whether documentation matches the behavior introduced in this PR.

Flag and fix when:

- Public API usage changed (constructor args, function signatures, supported providers), but `README.md` or `docs/` examples were not updated.
- CLI behavior or commands changed, but docs do not reflect the new invocation or options.
- New required environment variables or config keys were added, but `.env.example` and relevant docs are not updated.

No action is needed when PR changes are internal and do not affect user-facing behavior.
