"""Пример создания индекса программно."""

from birka_rag import create_rag_index

# Создание индекса из PDF-файлов
create_rag_index(
    persist_directory="./data/my_chroma",
    source_paths=[
        "./docs/standards",  # папка с PDF
        "./docs/manual.pdf",  # отдельный файл
    ],
    model_name="d0rj/e5-large-en-ru",
    chunk_size=1000,
    chunk_overlap=200,
    batch_size=100,
    use_gpu=True,
    recursive=True,  # искать во вложенных папках
    rag_mode="common",  # одна общая база на все файлы
)

print("Индекс создан успешно!")
