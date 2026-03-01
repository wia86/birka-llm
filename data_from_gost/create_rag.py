"""Создание RAG векторной базы (PDF → Chroma) с эмбеддингами."""

import hashlib
import json
import os
import re
import time
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Имя файла метаданных RAG (модель эмбеддингов, дата создания)
RAG_META_FILENAME = ".rag_embedding_meta.json"


def _write_rag_meta(persist_directory: str | Path, model_name: str) -> None:
    """Записывает в каталог RAG метаданные: какая модель эмбеддингов использована."""
    path = Path(persist_directory) / RAG_META_FILENAME
    meta = {
        "embedding_model": model_name,
        "created_at": datetime.now(UTC).isoformat(),
    }
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def _parse_bool(value: str, default: bool = True) -> bool:
    """Парсинг булевой переменной из env (1/0, true/false, yes/no)."""
    if not value or not value.strip():
        return default
    v = value.strip().lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    return default


def _collect_pdf_paths(source_paths: list[str], recursive: bool) -> list[Path]:
    """Собирает пути ко всем PDF: из папок (с вложенными или только корень) и одиночных файлов."""
    collected: list[Path] = []
    seen: set[Path] = set()
    for raw in source_paths:
        p = Path(raw.strip()).resolve()
        if not p.exists():
            continue
        if p.is_file():
            if p.suffix.lower() == ".pdf":
                if p not in seen:
                    seen.add(p)
                    collected.append(p)
            continue
        if recursive:
            for f in p.rglob("*.pdf"):
                if f.is_file() and f not in seen:
                    seen.add(f)
                    collected.append(f)
        else:
            for f in p.glob("*.pdf"):
                if f.is_file() and f not in seen:
                    seen.add(f)
                    collected.append(f)
    return sorted(collected)


def _safe_dir_name(file_path: Path) -> str:
    """Имя подпапки для Chroma при режиме per_file."""
    s = str(file_path).replace(":", "_")
    s = re.sub(r"[<>\"|?*\n\r]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if len(s) > 100:
        s = s[:100]
    h = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
    return f"{s}_{h}" if s else h


def _load_docs_from_pdf_paths(pdf_paths: list[Path]) -> list:
    """Загружает страницы из списка PDF. Возвращает list of Document."""
    from langchain_core.documents import Document

    all_docs: list[Document] = []
    for path in pdf_paths:
        loader = PyPDFLoader(str(path))
        docs = loader.load()
        all_docs.extend(docs)
    return all_docs


def _is_e5_model(model_name: str) -> bool:
    """Проверка, что модель E5 (требует префиксов query:/passage:)."""
    return "e5" in (model_name or "").lower()


def _apply_passage_prefix(chunks: list, model_name: str) -> list:
    """Для моделей E5 добавляет префикс passage: к тексту чанков."""
    if not _is_e5_model(model_name):
        return chunks
    from langchain_core.documents import Document

    return [
        Document(page_content=("passage: " + doc.page_content), metadata=doc.metadata)
        for doc in chunks
    ]


def _run_common(
    pdf_paths: list[Path],
    persist_directory: str,
    embeddings: HuggingFaceEmbeddings,
    text_splitter: RecursiveCharacterTextSplitter,
    batch_size: int,
    model_name: str,
    device: str,
    start_time: float,
) -> None:
    """Одна общая Chroma на все PDF."""
    print("\nЗагрузка PDF документов...")
    load_start = time.time()
    all_docs = _load_docs_from_pdf_paths(pdf_paths)
    load_time = time.time() - load_start
    print(f"Загружено страниц: {len(all_docs)} за {load_time:.1f}с\n")

    if not all_docs:
        raise ValueError("Ни одного документа не загружено.")

    print("Разбивка на чанки...")
    chunks = text_splitter.split_documents(all_docs)
    chunks = _apply_passage_prefix(chunks, model_name)
    print(f"Чанков: {len(chunks)}\n")

    print("Создание векторной базы...")
    if len(chunks) > batch_size:
        vectorstore = Chroma.from_documents(
            documents=chunks[:batch_size],
            embedding=embeddings,
            persist_directory=persist_directory,
        )
        for i in range(batch_size, len(chunks), batch_size):
            vectorstore.add_documents(chunks[i : i + batch_size])
    else:
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory,
        )
    _write_rag_meta(persist_directory, model_name)
    total_time = time.time() - start_time
    _print_stats(
        total_docs=len(all_docs),
        total_chunks=len(chunks),
        model_name=model_name,
        device=device,
        chunk_size=getattr(text_splitter, "chunk_size", 1000),
        load_time=load_time,
        total_time=total_time,
    )


def _run_per_file(
    pdf_paths: list[Path],
    persist_directory: str,
    embeddings: HuggingFaceEmbeddings,
    text_splitter: RecursiveCharacterTextSplitter,
    batch_size: int,
    model_name: str,
    device: str,
    start_time: float,
) -> None:
    """Отдельная Chroma на каждый PDF."""
    base = Path(persist_directory)
    base.mkdir(parents=True, exist_ok=True)
    total_docs = 0
    total_chunks = 0
    for i, path in enumerate(pdf_paths):
        print(f"\n[{i + 1}/{len(pdf_paths)}] {path.name}")
        docs = _load_docs_from_pdf_paths([path])
        if not docs:
            print("  Пропуск (пустой или ошибка)")
            continue
        chunks = text_splitter.split_documents(docs)
        chunks = _apply_passage_prefix(chunks, model_name)
        subdir = base / _safe_dir_name(path)
        subdir.mkdir(parents=True, exist_ok=True)
        if len(chunks) > batch_size:
            vs = Chroma.from_documents(
                documents=chunks[:batch_size],
                embedding=embeddings,
                persist_directory=str(subdir),
            )
            for j in range(batch_size, len(chunks), batch_size):
                vs.add_documents(chunks[j : j + batch_size])
        else:
            Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=str(subdir),
            )
        _write_rag_meta(subdir, model_name)
        total_docs += len(docs)
        total_chunks += len(chunks)
        print(f"  Страниц: {len(docs)}, чанков: {len(chunks)} → {subdir}")
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("СТАТИСТИКА (per_file)")
    print("=" * 60)
    print(f"Обработано файлов: {len(pdf_paths)}")
    print(f"Всего страниц:     {total_docs}")
    print(f"Всего чанков:      {total_chunks}")
    print(f"Модель:            {model_name}, устройство: {device}")
    print(f"Время:             {total_time:.1f}с ({total_time / 60:.1f} мин)")
    print("=" * 60)


def _print_stats(
    total_docs: int,
    total_chunks: int,
    model_name: str,
    device: str,
    chunk_size: int,
    load_time: float,
    total_time: float,
) -> None:
    print("=" * 60)
    print("СТАТИСТИКА")
    print("=" * 60)
    print(f"Документов (страниц): {total_docs}")
    print(f"Чанков создано:       {total_chunks}")
    print(f"Модель embeddings:    {model_name}")
    print(f"Устройство:           {device}")
    print(f"Размер чанка:         {chunk_size}")
    print(f"\nВремя: {total_time:.1f}с ({total_time / 60:.1f} мин)")
    print("=" * 60)


def create_rag(
    persist_directory: str,
    source_paths: list[str],
    model_name: str = "intfloat/multilingual-e5-large",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    batch_size: int = 100,
    use_gpu: bool = True,
    recursive: bool = True,
    rag_mode: str = "common",
) -> None:
    """Создание RAG векторной базы данных.

    Args:
        persist_directory: Путь для сохранения базы (или корень для per_file).
        source_paths: Список путей к папкам с PDF и/или к отдельным PDF-файлам.
        model_name: Название модели embeddings.
        chunk_size: Размер чанка текста.
        chunk_overlap: Перекрытие между чанками.
        batch_size: Размер батча для вставки в БД.
        use_gpu: Использовать GPU для ускорения.
        recursive: Искать PDF во вложенных папках (True) или только в корне каждой папки (False).
        rag_mode: "common" — одна общая база на все файлы; "per_file" — отдельная база на каждый PDF.
    """
    start_time = time.time()
    sep_info = "с вложенными папками" if recursive else "только в корне"
    mode_info = "общая база" if rag_mode == "common" else "отдельная база на каждый файл"
    print(f"Режим: {mode_info}, поиск PDF: {sep_info}\n")

    pdf_paths = _collect_pdf_paths(source_paths, recursive)
    if not pdf_paths:
        raise ValueError(
            "Не найдено ни одного PDF. Проверьте RAG_SOURCE_PATHS и RAG_RECURSIVE."
        )

    print(f"Найдено PDF-файлов: {len(pdf_paths)}")
    for path in pdf_paths[:10]:
        print(f"  {path}")
    if len(pdf_paths) > 10:
        print(f"  ... и ещё {len(pdf_paths) - 10}")

    device = "cuda" if use_gpu else "cpu"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True},
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    if rag_mode == "per_file":
        _run_per_file(
            pdf_paths=pdf_paths,
            persist_directory=persist_directory,
            embeddings=embeddings,
            text_splitter=text_splitter,
            batch_size=batch_size,
            model_name=model_name,
            device=device,
            start_time=start_time,
        )
    else:
        _run_common(
            pdf_paths=pdf_paths,
            persist_directory=persist_directory,
            embeddings=embeddings,
            text_splitter=text_splitter,
            batch_size=batch_size,
            model_name=model_name,
            device=device,
            start_time=start_time,
        )


def _path_sep() -> str:
    """Разделитель путей: ; на Windows, : на Unix."""
    return ";" if os.name == "nt" else ":"


def main() -> None:
    """Точка входа. Конфигурация из env: RAG_PERSIST_DIR, RAG_SOURCE_PATHS, RAG_RECURSIVE, RAG_MODE, RAG_MODEL_NAME."""
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

    persist_directory = os.environ.get("RAG_PERSIST_DIR", "").strip() or "./data/chroma_default"
    source_paths_str = os.environ.get("RAG_SOURCE_PATHS", "").strip()
    sep = _path_sep()
    source_paths = [p.strip() for p in source_paths_str.split(sep) if p.strip()] if source_paths_str else []
    model_name = os.environ.get("RAG_MODEL_NAME", "").strip() or "d0rj/e5-large-en-ru"
    recursive = _parse_bool(os.environ.get("RAG_RECURSIVE", "1"), default=True)
    rag_mode_raw = os.environ.get("RAG_MODE", "common").strip().lower()
    rag_mode = "per_file" if rag_mode_raw == "per_file" else "common"

    if not source_paths:
        print(
            f"Задайте RAG_SOURCE_PATHS (папки и/или файлы PDF, разделитель {sep}).\n"
            f"Опционально: RAG_RECURSIVE=1|0, RAG_MODE=common|per_file, RAG_PERSIST_DIR.\n"
            f"Пример: RAG_SOURCE_PATHS=E:\\НОРМАТИВЫ"
        )
        return

    create_rag(
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


if __name__ == "__main__":
    main()
