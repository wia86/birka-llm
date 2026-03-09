---
name: RAG Config and Secrets
description: Validate provider config changes, env keys, and safe defaults
---

Focus on RAG/LLM configuration changes in this PR and fix issues.

Look for:

- New provider-specific env vars referenced in code but missing in `.env.example`.
- Changes to provider selection or API base/key handling without matching docs updates.
- Defaults that can break local startup unexpectedly (for example, incompatible default model/provider combinations) without guardrails or clear errors.
- Error messages for connection/config failures that do not help the user recover.

Prefer fixes that preserve current behavior while improving reliability and onboarding clarity.
