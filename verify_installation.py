"""Скрипт проверки установки и базовой функциональности."""

import sys
from pathlib import Path


def check_imports():
    """Проверка импортов пакета."""
    print("Проверка импортов...")
    try:
        from birka_rag import (
            RAGAssistant,
            AssistantProfile,
            LLMProvider,
            available_profile_names,
            create_rag_index,
        )
        print("✓ Все импорты успешны")
        return True
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False


def check_profiles():
    """Проверка доступности профилей."""
    print("\nПроверка профилей...")
    try:
        from birka_rag import available_profile_names, select_profile
        
        profiles = available_profile_names()
        print(f"✓ Доступно профилей: {len(profiles)}")
        for name in profiles:
            profile = select_profile(name)
            print(f"  - {name}: {profile.name}")
        return True
    except Exception as e:
        print(f"✗ Ошибка профилей: {e}")
        return False


def check_cli_commands():
    """Проверка доступности CLI команд."""
    print("\nПроверка CLI команд...")
    import subprocess
    
    commands = ["birka-rag", "birka-rag-index"]
    results = []
    
    for cmd in commands:
        try:
            result = subprocess.run(
                [cmd, "--help"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 or "usage" in result.stdout.lower() or "usage" in result.stderr.lower():
                print(f"✓ {cmd} доступна")
                results.append(True)
            else:
                print(f"✗ {cmd} вернула код {result.returncode}")
                results.append(False)
        except FileNotFoundError:
            print(f"✗ {cmd} не найдена (возможно, нужно переустановить пакет)")
            results.append(False)
        except Exception as e:
            print(f"✗ {cmd}: {e}")
            results.append(False)
    
    return all(results)


def check_dependencies():
    """Проверка основных зависимостей."""
    print("\nПроверка зависимостей...")
    
    deps = [
        ("torch", "PyTorch"),
        ("langchain", "LangChain"),
        ("langchain_chroma", "LangChain Chroma"),
        ("langchain_huggingface", "LangChain HuggingFace"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "Sentence Transformers"),
    ]
    
    results = []
    for module, name in deps:
        try:
            __import__(module)
            print(f"✓ {name}")
            results.append(True)
        except ImportError:
            print(f"✗ {name} не установлен")
            results.append(False)
    
    return all(results)


def check_gpu():
    """Проверка доступности GPU."""
    print("\nПроверка GPU...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ GPU доступен: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA версия: {torch.version.cuda}")
            return True
        else:
            print("⚠ GPU не обнаружен, будет использоваться CPU")
            return True
    except Exception as e:
        print(f"✗ Ошибка проверки GPU: {e}")
        return False


def main():
    """Основная функция проверки."""
    print("=" * 60)
    print("Проверка установки birka-rag")
    print("=" * 60)
    
    checks = [
        ("Импорты", check_imports),
        ("Профили", check_profiles),
        ("CLI команды", check_cli_commands),
        ("Зависимости", check_dependencies),
        ("GPU", check_gpu),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n✗ Критическая ошибка в проверке '{name}': {e}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("Результаты проверки")
    print("=" * 60)
    
    for name, result in results.items():
        status = "✓ OK" if result else "✗ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ Все проверки пройдены успешно!")
        print("\nСледующие шаги:")
        print("1. Настройте .env файл (скопируйте .env.example)")
        print("2. Создайте индекс: birka-rag-index")
        print("3. Запустите чат: birka-rag")
    else:
        print("✗ Некоторые проверки не пройдены")
        print("\nРекомендации:")
        print("1. Переустановите пакет: pip install -e .")
        print("2. Установите зависимости: pip install -e '.[openai]'")
        print("3. Проверьте Python версию (требуется 3.11-3.13)")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
