#!/usr/bin/env python
"""Финальная проверка готовности проекта к использованию."""

import sys
from pathlib import Path


def check_structure():
    """Проверка структуры пакета."""
    print("Проверка структуры пакета...")
    
    required_files = [
        "src/birka_rag/__init__.py",
        "src/birka_rag/py.typed",
        "src/birka_rag/core/__init__.py",
        "src/birka_rag/core/assistant.py",
        "src/birka_rag/core/profiles.py",
        "src/birka_rag/core/types.py",
        "src/birka_rag/core/providers/__init__.py",
        "src/birka_rag/core/providers/gigachat.py",
        "src/birka_rag/core/providers/apifreellm.py",
        "src/birka_rag/indexing/__init__.py",
        "src/birka_rag/indexing/indexer.py",
        "src/birka_rag/cli/__init__.py",
        "src/birka_rag/cli/chat.py",
        "src/birka_rag/cli/index.py",
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"[FAIL] Отсутствуют файлы: {len(missing)}")
        for f in missing:
            print(f"  - {f}")
        return False
    else:
        print(f"[OK] Все файлы пакета на месте ({len(required_files)} файлов)")
        return True


def check_documentation():
    """Проверка документации."""
    print("\nПроверка документации...")
    
    docs = [
        "README.md",
        "QUICKSTART.md",
        "ARCHITECTURE.md",
        "MIGRATION.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "docs/README.md",
        "docs/INSTALLATION.md",
    ]
    
    existing = [d for d in docs if Path(d).exists()]
    
    print(f"[OK] Документация: {len(existing)}/{len(docs)} файлов")
    return len(existing) >= 6


def check_examples():
    """Проверка примеров."""
    print("\nПроверка примеров...")
    
    examples = list(Path("examples").glob("*.py")) if Path("examples").exists() else []
    
    if len(examples) >= 4:
        print(f"[OK] Примеры: {len(examples)} файлов")
        return True
    else:
        print(f"[WARN] Примеры: {len(examples)} файлов (ожидалось >= 4)")
        return False


def check_config():
    """Проверка конфигурационных файлов."""
    print("\nПроверка конфигурации...")
    
    configs = [
        "pyproject.toml",
        ".env.example",
        ".gitignore",
    ]
    
    existing = [c for c in configs if Path(c).exists()]
    
    if len(existing) == len(configs):
        print(f"[OK] Конфигурация: все файлы на месте")
        return True
    else:
        print(f"[FAIL] Конфигурация: {len(existing)}/{len(configs)}")
        return False


def check_tests():
    """Проверка тестов."""
    print("\nПроверка тестов...")
    
    if Path("tests/test_basic.py").exists():
        print("[OK] Тесты созданы")
        return True
    else:
        print("[FAIL] Тесты отсутствуют")
        return False


def check_utilities():
    """Проверка утилит."""
    print("\nПроверка утилит...")
    
    utils = [
        "verify_installation.py",
        "migrate.py",
    ]
    
    existing = [u for u in utils if Path(u).exists()]
    
    print(f"[OK] Утилиты: {len(existing)}/{len(utils)}")
    return len(existing) >= 1


def main():
    """Основная функция."""
    print("=" * 60)
    print("ФИНАЛЬНАЯ ПРОВЕРКА ГОТОВНОСТИ ПРОЕКТА")
    print("=" * 60)
    
    checks = {
        "Структура пакета": check_structure(),
        "Документация": check_documentation(),
        "Примеры": check_examples(),
        "Конфигурация": check_config(),
        "Тесты": check_tests(),
        "Утилиты": check_utilities(),
    }
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 60)
    
    for name, result in checks.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"{name:25} {status}")
    
    all_passed = all(checks.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] ПРОЕКТ ПОЛНОСТЬЮ ГОТОВ К ИСПОЛЬЗОВАНИЮ!")
        print("\nСледующие шаги:")
        print("1. pip install -e \".[openai]\"")
        print("2. cp .env.example .env")
        print("3. birka-rag-index")
        print("4. birka-rag")
    else:
        print("[WARNING] ТРЕБУЮТСЯ ДОПОЛНИТЕЛЬНЫЕ ДЕЙСТВИЯ")
        print("\nПроверьте отсутствующие компоненты выше")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
