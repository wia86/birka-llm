#!/usr/bin/env python
"""Быстрая демонстрация возможностей birka-rag."""

import sys


def print_header(text):
    """Печать заголовка."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def demo_imports():
    """Демонстрация импортов."""
    print_header("1. ИМПОРТЫ")
    
    print("\nИмпорт основных компонентов:")
    print(">>> from birka_rag import RAGAssistant, select_profile")
    
    try:
        from birka_rag import RAGAssistant, select_profile
        print("[OK] Импорты успешны")
        return True
    except ImportError as e:
        print(f"[FAIL] Ошибка импорта: {e}")
        print("\nУстановите пакет: pip install -e .")
        return False


def demo_profiles():
    """Демонстрация профилей."""
    print_header("2. ПРОФИЛИ LLM")
    
    try:
        from birka_rag import available_profile_names, select_profile
        
        profiles = available_profile_names()
        print(f"\nДоступно профилей: {len(profiles)}")
        
        for name in profiles:
            profile = select_profile(name)
            print(f"  - {name}: {profile.name}")
        
        print("\n[OK] Профили загружены")
        return True
    except Exception as e:
        print(f"[FAIL] Ошибка: {e}")
        return False


def demo_usage():
    """Демонстрация использования."""
    print_header("3. ПРИМЕР ИСПОЛЬЗОВАНИЯ")
    
    print("\nСоздание ассистента:")
    print("""
assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Ваш вопрос")
    """)
    
    print("[INFO] Для реального использования нужна векторная база")
    print("       Создайте её командой: birka-rag-index")
    return True


def demo_cli():
    """Демонстрация CLI."""
    print_header("4. CLI КОМАНДЫ")
    
    print("\nДоступные команды:")
    print("  birka-rag-index  - создание индекса из PDF")
    print("  birka-rag        - интерактивный чат")
    
    print("\nПример:")
    print("  $ birka-rag-index")
    print("  $ birka-rag")
    
    return True


def demo_next_steps():
    """Следующие шаги."""
    print_header("5. СЛЕДУЮЩИЕ ШАГИ")
    
    print("\n1. Настройте конфигурацию:")
    print("   cp .env.example .env")
    
    print("\n2. Создайте индекс:")
    print("   birka-rag-index")
    
    print("\n3. Запустите чат:")
    print("   birka-rag")
    
    print("\n4. Попробуйте примеры:")
    print("   python examples/basic_usage.py")
    
    print("\n5. Изучите документацию:")
    print("   cat INDEX.md")


def main():
    """Основная функция."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ BIRKA-RAG")
    print("=" * 60)
    print("\nЭтот скрипт демонстрирует основные возможности пакета.")
    
    results = []
    results.append(demo_imports())
    
    if results[0]:  # Если импорты успешны
        results.append(demo_profiles())
        results.append(demo_usage())
        results.append(demo_cli())
        demo_next_steps()
    
    print("\n" + "=" * 60)
    if all(results):
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО")
        print("\nПакет готов к использованию!")
    else:
        print("ТРЕБУЕТСЯ УСТАНОВКА ПАКЕТА")
        print("\nВыполните: pip install -e .")
    print("=" * 60)
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
