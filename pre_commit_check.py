#!/usr/bin/env python
"""Финальная проверка перед коммитом."""

import sys
from pathlib import Path


def check_critical_files():
    """Проверка критически важных файлов."""
    print("Проверка критических файлов...")
    
    critical = [
        "pyproject.toml",
        "src/birka_rag/__init__.py",
        "src/birka_rag/core/assistant.py",
        "src/birka_rag/cli/chat.py",
        "src/birka_rag/cli/index.py",
        "README.md",
        "START.md",
        ".env.example",
    ]
    
    missing = [f for f in critical if not Path(f).exists()]
    
    if missing:
        print(f"[FAIL] Отсутствуют критические файлы:")
        for f in missing:
            print(f"  - {f}")
        return False
    
    print(f"[OK] Все критические файлы на месте ({len(critical)} файлов)")
    return True


def check_documentation():
    """Проверка документации."""
    print("\nПроверка документации...")
    
    docs = [
        "START.md",
        "QUICKSTART.md",
        "INDEX.md",
        "README.md",
        "MIGRATION.md",
        "CONTRIBUTING.md",
    ]
    
    existing = [d for d in docs if Path(d).exists()]
    
    if len(existing) >= 5:
        print(f"[OK] Документация: {len(existing)}/{len(docs)}")
        return True
    else:
        print(f"[WARN] Документация: {len(existing)}/{len(docs)}")
        return False


def check_examples():
    """Проверка примеров."""
    print("\nПроверка примеров...")
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("[FAIL] Папка examples не найдена")
        return False
    
    examples = list(examples_dir.glob("*.py"))
    
    if len(examples) >= 4:
        print(f"[OK] Примеры: {len(examples)} файлов")
        return True
    else:
        print(f"[WARN] Примеры: {len(examples)} файлов")
        return False


def check_git_status():
    """Проверка git статуса."""
    print("\nПроверка git...")
    
    if Path(".git").exists():
        print("[OK] Git репозиторий инициализирован")
        return True
    else:
        print("[WARN] Git репозиторий не найден")
        return False


def print_next_steps():
    """Вывод следующих шагов."""
    print("\n" + "=" * 60)
    print("СЛЕДУЮЩИЕ ШАГИ")
    print("=" * 60)
    
    print("\n1. Установите пакет:")
    print("   pip install -e \".[openai]\"")
    
    print("\n2. Проверьте установку:")
    print("   python verify_installation.py")
    
    print("\n3. Настройте конфигурацию:")
    print("   cp .env.example .env")
    
    print("\n4. Создайте git коммит:")
    print("   git add .")
    print("   git commit -m \"Реорганизация в пакет birka-rag v0.1.0\"")
    print("   git push")
    
    print("\n5. Попробуйте использовать:")
    print("   birka-rag-index")
    print("   birka-rag")


def main():
    """Основная функция."""
    print("=" * 60)
    print("ФИНАЛЬНАЯ ПРОВЕРКА ПЕРЕД КОММИТОМ")
    print("=" * 60)
    
    checks = {
        "Критические файлы": check_critical_files(),
        "Документация": check_documentation(),
        "Примеры": check_examples(),
        "Git": check_git_status(),
    }
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 60)
    
    for name, result in checks.items():
        status = "[OK]" if result else "[WARN]"
        print(f"{name:25} {status}")
    
    all_critical = checks["Критические файлы"]
    
    print("\n" + "=" * 60)
    if all_critical:
        print("[SUCCESS] ПРОЕКТ ГОТОВ К КОММИТУ!")
        print_next_steps()
    else:
        print("[FAIL] ТРЕБУЮТСЯ ИСПРАВЛЕНИЯ")
        print("\nИсправьте критические проблемы перед коммитом")
    print("=" * 60)
    
    return 0 if all_critical else 1


if __name__ == "__main__":
    sys.exit(main())
