# pip install langchain langchain-community langchain-huggingface chromadb pypdf sentence-transformers torch
import os
import time
from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_rag(
        persist_directory: str,
        source_paths: list[str],
        model_name: str = "intfloat/multilingual-e5-large",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        batch_size: int = 100,  # Размер батча для вставки
        use_gpu: bool = True,  # Использовать GPU если доступен
) -> None:
    """
    Создание RAG векторной базы данных.

    Args:
        persist_directory: Путь для сохранения базы
        source_paths: Список путей к папкам с PDF
        model_name: Название модели embeddings
        chunk_size: Размер чанка текста
        chunk_overlap: Перекрытие между чанками
        batch_size: Размер батча для вставки в БД
        use_gpu: Использовать GPU для ускорения
    """
    start_time = time.time()

    # 1. ЗАГРУЗКА ДОКУМЕНТОВ
    print("📚 Загрузка PDF документов...")
    load_start = time.time()

    all_docs = []
    for path in source_paths:
        if not Path(path).exists():
            print(f"⚠️  Пропущен несуществующий путь: {path}")
            continue

        loader = PyPDFDirectoryLoader(path)
        docs = loader.load()
        all_docs.extend(docs)
        print(f"  ✓ Загружено из {path}: {len(docs)} страниц")

    load_time = time.time() - load_start
    print(f"✓ Всего загружено: {len(all_docs)} страниц за {load_time:.1f}с\n")

    if not all_docs:
        raise ValueError("Не найдено ни одного PDF документа!")

    # 2. РАЗБИВКА НА ЧАНКИ
    print("✂️  Разбивка на чанки...")
    split_start = time.time()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_documents(all_docs)

    split_time = time.time() - split_start
    print(f"✓ Создано чанков: {len(chunks)} за {split_time:.1f}с\n")

    # 3. ИНИЦИАЛИЗАЦИЯ EMBEDDINGS
    print("🤖 Инициализация модели embeddings...")
    embed_init_start = time.time()

    # Настройка для использования GPU
    model_kwargs = {"device": "cuda" if use_gpu else "cpu"}
    encode_kwargs = {"normalize_embeddings": True}  # Ускоряет поиск

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )

    embed_init_time = time.time() - embed_init_start
    device = model_kwargs["device"]
    print(f"✓ Модель загружена на {device.upper()} за {embed_init_time:.1f}с\n")

    # 4. СОЗДАНИЕ И СОХРАНЕНИЕ ВЕКТОРНОЙ БАЗЫ
    print("💾 Создание векторной базы (это займет время)...")
    vectorstore_start = time.time()

    # Создаем базу батчами для экономии памяти
    if len(chunks) > batch_size:
        print(f"  Обработка батчами по {batch_size} чанков...")

        # Первый батч - создание базы
        vectorstore = Chroma.from_documents(
            documents=chunks[:batch_size],
            embedding=embeddings,
            persist_directory=persist_directory,
        )
        print(f"  ✓ Создана база, добавлено {batch_size} чанков")

        # Остальные батчи - добавление
        for i in range(batch_size, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            vectorstore.add_documents(batch)
            progress = min(i + batch_size, len(chunks))
            print(f"  ✓ Добавлено {progress}/{len(chunks)} чанков")
    else:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory,
        )

    # Явное сохранение
    vectorstore.persist()

    vectorstore_time = time.time() - vectorstore_start
    print(f"✓ База сохранена за {vectorstore_time:.1f}с\n")

    # ИТОГОВАЯ СТАТИСТИКА
    total_time = time.time() - start_time

    print("=" * 60)
    print("📊 СТАТИСТИКА")
    print("=" * 60)
    print(f"Документов (страниц): {len(all_docs)}")
    print(f"Чанков создано:       {len(chunks)}")
    print(f"Модель embeddings:    {model_name}")
    print(f"Устройство:           {device.upper()}")
    print(f"Размер чанка:         {chunk_size}")
    print(f"\nВремя выполнения:")
    print(f"  • Загрузка PDF:     {load_time:.1f}с ({load_time / total_time * 100:.0f}%)")
    print(f"  • Разбивка:         {split_time:.1f}с ({split_time / total_time * 100:.0f}%)")
    print(f"  • Инит. модели:     {embed_init_time:.1f}с ({embed_init_time / total_time * 100:.0f}%)")
    print(f"  • Создание базы:    {vectorstore_time:.1f}с ({vectorstore_time / total_time * 100:.0f}%)")
    print(f"\n🎉 ОБЩЕЕ ВРЕМЯ:       {total_time:.1f}с ({total_time / 60:.1f} мин)")
    print("=" * 60)


def _path_sep() -> str:
    """Разделитель путей: ; на Windows, : на Unix."""
    return ";" if os.name == "nt" else ":"


def main() -> None:
    """Точка входа. Конфигурация из env: RAG_PERSIST_DIR, RAG_SOURCE_PATHS, RAG_MODEL_NAME."""
    # Проверка доступности GPU
    try:
        import torch
        use_gpu = torch.cuda.is_available()
        if use_gpu:
            print(f"GPU: {torch.cuda.get_device_name(0)}\n")
        else:
            print("GPU ne obnaruzhen, ispolzuetsya CPU\n")
    except ImportError:
        print("PyTorch ne ustanovlen, ispolzuetsya CPU\n")
        use_gpu = False

    persist_directory = os.environ.get("RAG_PERSIST_DIR", "").strip() or "./data/chroma_default"
    source_paths_str = os.environ.get("RAG_SOURCE_PATHS", "").strip()
    source_paths = [p.strip() for p in source_paths_str.split(_path_sep()) if p.strip()] if source_paths_str else []
    model_name = os.environ.get("RAG_MODEL_NAME", "").strip() or "BAAI/bge-m3"

    if not source_paths:
        print("Задайте RAG_SOURCE_PATHS (пути к папкам с PDF, разделитель " + _path_sep() + ") и при необходимости RAG_PERSIST_DIR.")
        print("Пример: RAG_SOURCE_PATHS=E:\\НОРМАТИВЫ\\ур_му_2022")
        return

    config = {
        "persist_directory": persist_directory,
        "source_paths": source_paths,
        "model_name": model_name,
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "batch_size": 100,
        "use_gpu": use_gpu,
    }

    create_rag(**config)


if __name__ == "__main__":
    main()