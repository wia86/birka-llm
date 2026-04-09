"""Минимальный тест для проверки базовой функциональности."""

import sys


def test_imports():
    """Тест импортов основных компонентов."""
    try:
        from birka_rag import (
            RAGAssistant,
            AssistantProfile,
            LLMProvider,
            available_profile_names,
            select_profile,
            create_rag_index,
        )
        print("✓ Импорты успешны")
        return True
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False


def test_profile_selection():
    """Тест выбора профилей."""
    try:
        from birka_rag import available_profile_names, select_profile
        
        profiles = available_profile_names()
        assert len(profiles) > 0, "Нет доступных профилей"
        
        profile = select_profile("ollama_local")
        assert profile.name == "Локальная Ollama"
        assert profile.llm_provider == "ollama"
        
        print("✓ Профили работают корректно")
        return True
    except Exception as e:
        print(f"✗ Ошибка профилей: {e}")
        return False


def test_profile_to_kwargs():
    """Тест преобразования профиля в kwargs."""
    try:
        from birka_rag import select_profile
        
        profile = select_profile("ollama_local")
        kwargs = profile.to_kwargs()
        
        assert "persist_directory" in kwargs
        assert "model_name" in kwargs
        assert "llm_model" in kwargs
        assert "llm_provider" in kwargs
        
        print("✓ Преобразование профиля в kwargs работает")
        return True
    except Exception as e:
        print(f"✗ Ошибка преобразования: {e}")
        return False


def test_types():
    """Тест типов."""
    try:
        from birka_rag import LLMProvider
        from birka_rag.core.types import LLMProvider as LLMProviderDirect
        
        assert LLMProvider is not None
        assert LLMProviderDirect is not None
        
        print("✓ Типы доступны")
        return True
    except Exception as e:
        print(f"✗ Ошибка типов: {e}")
        return False


def main():
    """Запуск всех тестов."""
    print("=" * 60)
    print("Базовые тесты birka-rag")
    print("=" * 60)
    
    tests = [
        ("Импорты", test_imports),
        ("Выбор профилей", test_profile_selection),
        ("Преобразование профилей", test_profile_to_kwargs),
        ("Типы", test_types),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nТест: {name}")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Критическая ошибка: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ Все тесты пройдены")
        return 0
    else:
        print("✗ Некоторые тесты не пройдены")
        return 1


if __name__ == "__main__":
    sys.exit(main())
