"""CLI для создания индекса RAG."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from birka_rag.indexing import create_rag_index


def _path_sep() -> str:
    """Разделитель путей: ; на Windows, : на Unix."""
    return ";" if os.name == "nt" else ":"


def main() -> None:
    """Точка входа CLI для индексации.
    
    Конфигурация из env:
    - RAG_PERSIST_DIR: каталог для сохранения базы
    - RAG_SOURCE_PATHS: пути к каталогам и/или файлам (разделитель ; или :)
    - RAG_MODEL_NAME: модель эмбеддингов
    - RAG_RECURSIVE: 1|0 (искать во вложенных папках)
    - RAG_MODE: common|per_file
    """
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    load_dotenv(override=True)

    try:
        import torch
        use_gpu = torch.cuda.is_available()
        if use_gpu:
            print(f"GPU: {torch.cuda.get_device_name(0)}\n")
        else:
            print("GPU не обнаружен, используется CPU\n")
    except ImportError:
        print("PyTorch не установлен, используется CPU\n")
        use_gpu = False

    persist_directory = os.environ.get("RAG_PERSIST_DIR", "").strip() or "./storage/chroma/default"
    source_paths_str = os.environ.get("RAG_SOURCE_PATHS", "").strip()
    sep = _path_sep()
    source_paths = [p.strip() for p in source_paths_str.split(sep) if p.strip()] if source_paths_str else []
    model_name = os.environ.get("RAG_MODEL_NAME", "").strip() or "d0rj/e5-large-en-ru"
    recursive_str = os.environ.get("RAG_RECURSIVE", "1").strip().lower()
    recursive = recursive_str not in ("0", "false", "no", "off")
    rag_mode_raw = os.environ.get("RAG_MODE", "common").strip().lower()
    rag_mode = "per_file" if rag_mode_raw == "per_file" else "common"

    if not source_paths:
        print(
            f"Задайте RAG_SOURCE_PATHS (папки и/или файлы, разделитель {sep}).\n"
            f"Опционально: RAG_SOURCE_EXTENSIONS=.pdf,.md,.txt,.json, "
            f"RAG_RECURSIVE=1|0, RAG_MODE=common|per_file, RAG_PERSIST_DIR.\n"
            f"Пример: RAG_SOURCE_PATHS=./knowledge/docs;./knowledge/code_guides"
        )
        sys.exit(1)

    try:
        create_rag_index(
            persist_directory=persist_directory,
            source_paths=source_paths,
            model_name=model_name,
            chunk_size=1000,
            chunk_overlap=200,
            batch_size=100,
            use_gpu=use_gpu,
            recursive=recursive,
            rag_mode=rag_mode,
        )
    except Exception as e:
        print(f"\nОшибка при создании индекса: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
