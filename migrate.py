#!/usr/bin/env python
"""Скрипт помощи при миграции со старой структуры на новую."""

import os
import sys
from pathlib import Path


def check_old_imports():
    """Проверка использования старых импортов в проекте."""
    print("Поиск старых импортов...")
    
    old_patterns = [
        "from rag_assistant import",
        "from rag_assistant.",
        "import rag_assistant",
    ]
    
    found = []
    for pattern in ["*.py"]:
        for file in Path(".").rglob(pattern):
            if "data_from_gost" in str(file) or ".venv" in str(file):
                continue
            
            try:
                content = file.read_text(encoding="utf-8")
                for old_pattern in old_patterns:
                    if old_pattern in content:
                        found.append((file, old_pattern))
            except Exception:
                pass
    
    if found:
        print(f"\n✗ Найдено {len(found)} файлов со старыми импортами:")
        for file, pattern in found:
            print(f"  {file}: {pattern}")
        print("\nРекомендация: замените на 'from birka_rag import ...'")
        return False
    else:
        print("✓ Старые импорты не найдены")
        return True


def check_installation():
    """Проверка установки пакета."""
    print("\nПроверка установки пакета...")
    
    try:
        import birka_rag
        print(f"✓ Пакет birka-rag установлен (версия {birka_rag.__version__})")
        return True
    except ImportError:
        print("✗ Пакет birka-rag не установлен")
        print("  Выполните: pip install -e .")
        return False


def check_cli_commands():
    """Проверка доступности CLI команд."""
    print("\nПроверка CLI команд...")
    
    import subprocess
    
    commands = ["birka-rag", "birka-rag-index"]
    all_ok = True
    
    for cmd in commands:
        try:
            result = subprocess.run(
                [cmd, "--help"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0 or "usage" in result.stdout.decode().lower():
                print(f"✓ {cmd} доступна")
            else:
                print(f"✗ {cmd} недоступна")
                all_ok = False
        except FileNotFoundError:
            print(f"✗ {cmd} не найдена")
            all_ok = False
        except Exception as e:
            print(f"✗ {cmd}: {e}")
            all_ok = False
    
    if not all_ok:
        print("  Переустановите пакет: pip install -e .")
    
    return all_ok


def check_env_file():
    """Проверка наличия .env файла."""
    print("\nПроверка конфигурации...")
    
    if Path(".env").exists():
        print("✓ Файл .env существует")
        return True
    else:
        print("✗ Файл .env не найден")
        print("  Скопируйте .env.example в .env и настройте")
        return False


def suggest_next_steps(results):
    """Предложить следующие шаги на основе результатов проверки."""
    print("\n" + "=" * 60)
    print("СЛЕДУЮЩИЕ ШАГИ")
    print("=" * 60)
    
    if not results["installation"]:
        print("\n1. Установите пакет:")
        print("   pip install -e \".[openai]\"")
    
    if not results["env"]:
        print("\n2. Настройте конфигурацию:")
        print("   cp .env.example .env")
        print("   # Отредактируйте .env")
    
    if results["installation"] and results["env"]:
        print("\n✓ Всё готово к использованию!")
        print("\nСоздайте индекс:")
        print("  birka-rag-index")
        print("\nЗапустите чат:")
        print("  birka-rag")
        print("\nИли используйте в коде:")
        print("  from birka_rag import RAGAssistant")
    
    if results["old_imports"]:
        print("\n⚠ Обновите импорты в вашем коде:")
        print("  from rag_assistant import ... → from birka_rag import ...")


def main():
    """Основная функция."""
    print("=" * 60)
    print("Помощник миграции birka-rag")
    print("=" * 60)
    
    results = {
        "old_imports": check_old_imports(),
        "installation": check_installation(),
        "cli": check_cli_commands(),
        "env": check_env_file(),
    }
    
    suggest_next_steps(results)
    
    print("\n" + "=" * 60)
    if all(results.values()):
        print("✓ Миграция завершена успешно!")
        return 0
    else:
        print("⚠ Требуются дополнительные действия")
        return 1


if __name__ == "__main__":
    sys.exit(main())
