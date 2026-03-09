---
name: Security Review
description: Detect hardcoded secrets, unsafe logging, and risky crypto usage
---

Review this pull request for security issues and fix them when possible.

Look for these issues:

- Hardcoded API keys, tokens, passwords, bearer strings, or connection strings in source or config files. Move values to environment variables and keep only placeholders/examples.
- Sensitive data in logs or stdout (API keys, tokens, credentials, personal data). Remove or redact sensitive fields.
- Use of weak cryptography for security-sensitive logic (MD5, SHA1, ECB mode). Replace with stronger alternatives.
- Direct shell execution with user-controlled input (for example, unsafe `subprocess` invocation patterns). Sanitize input or switch to safe argument passing.

If none of these are present in changed code, pass the check.
