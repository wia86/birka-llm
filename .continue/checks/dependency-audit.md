---
name: Dependency Audit
description: Review dependency changes for safety and maintainability
---

If dependency files are unchanged, pass this check.

When dependency files are changed (`pyproject.toml`, lock files, CI install steps), review for:

- New dependency added without clear usage in changed code.
- Major version jumps without any migration note in docs or PR description.
- Dev-only tools added to runtime dependencies by mistake.
- Multiple dependencies introduced for the same purpose when one existing dependency already covers the need.

If issues are found, propose the minimal safe correction.
