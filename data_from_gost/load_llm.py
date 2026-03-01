"""Модуль для инициализации моделей эмбеддингов для RAG."""

from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings(
        model_name: str,
        normalize: bool = True,
        device: str | None = None,
        cache_dir: str | None = None,
        trust_remote_code: bool = False
) -> HuggingFaceEmbeddings:
    """
    Универсальная функция для создания эмбеддингов.

    Args:
        model_name: Название модели на HuggingFace
        normalize: Нормализовать векторы
        device: Устройство ('cpu', 'cuda', 'mps' или None для авто)
        cache_dir: Директория для кэша модели
        trust_remote_code: Разрешить выполнение кода из модели

    Returns:
        HuggingFaceEmbeddings: Настроенная модель эмбеддингов
    """
    model_kwargs = {}
    if device:
        model_kwargs["device"] = device
    if cache_dir is not None:
        model_kwargs["cache_dir"] = cache_dir
    if trust_remote_code:
        model_kwargs["trust_remote_code"] = trust_remote_code

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs if model_kwargs else {},
        encode_kwargs={"normalize_embeddings": normalize}
    )

    return embeddings


def get_bge_m3(**kwargs) -> HuggingFaceEmbeddings:
    """
    Получить BAAI/bge-m3 модель эмбеддингов.
    Поддерживает 100+ языков, размерность: 1024.
    """
    return get_embeddings("BAAI/bge-m3", **kwargs)


def get_multilingual_e5_large(**kwargs) -> HuggingFaceEmbeddings:
    """
    Получить intfloat/multilingual-e5-large модель эмбеддингов.
    Поддерживает 100+ языков, размерность: 1024.

    Важно: Для E5 моделей используйте префикс 'query: ' для запросов
    и 'passage: ' для документов.
    """
    return get_embeddings("intfloat/multilingual-e5-large", **kwargs)


def demo_embeddings(
        embeddings: HuggingFaceEmbeddings,
        test_text: str = "query: Это тестовое предложение на русском."
) -> None:
    """
    Пример запуска модели эмбеддингов вручную.

    Args:
        embeddings: Модель эмбеддингов для демонстрации
        test_text: Текст для проверки
    """
    try:
        vector = embeddings.embed_query(test_text)
        print("✓ Модель загружена успешно!")
        print(f"  Длина вектора: {len(vector)}")
        print(f"  Пример значений: {vector[:3]}")
    except Exception as e:
        print(f"✗ Ошибка при тестировании: {e}")


if __name__ == "__main__":
    # для скачивания моделей
    # print("Тестирование multilingual-e5-large...")
    # model = get_multilingual_e5_large()
    # demo_embeddings(model)

    print("\nТестирование bge-m3...")
    model = get_bge_m3()
    demo_embeddings(model, "Это тестовое предложение на русском.")