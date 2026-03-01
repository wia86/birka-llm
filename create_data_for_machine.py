"""Подготовка данных для ML: сравнение строк, обработка Excel.

Legacy: зависит от moduls.network_structure из основного репозитория Birka.
"""

from collections.abc import Generator
from pathlib import Path

import pandas as pd

from moduls.network_structure.string_matching import calculate_similarity_string


def calculate_match(row: pd.Series) -> pd.Series:
    """Расчёт коэффициента сходства двух строк."""
    row["ratio"] = calculate_similarity_string(row["1"], row["2"])
    return row


def processing_df(df: pd.DataFrame) -> pd.DataFrame:
    """Очистка DataFrame: оставить пары отличающихся непустых строк.

    Args:
        df: Исходный DataFrame с колонками dname/name или ny_name/ny_name_node2.

    Returns:
        DataFrame с колонками '1', '2', '3' (метка), 'ratio'.
    """
    print(len(df))

    if "dname" in df.columns:
        df = df[["dname", "name"]]
    else:
        df = df[["ny_name", "ny_name_node2"]]
    df.columns = ["1", "2"]

    df["1"] = df["1"].str.strip()
    df["2"] = df["2"].str.strip()

    df = df[(df["1"].str.len() > 0) & (df["2"].str.len() > 0)]
    df = df[df["1"] != df["2"]]
    df = df.drop_duplicates(subset=["1", "2"], keep="first")

    df["3"] = 1
    df = df.apply(calculate_match, axis=1)
    print(df.head(15))
    print(len(df))

    return df


def cycle_in_folder(path_folder: str | Path, extension: str) -> Generator[Path]:
    """Рекурсивный обход папки с фильтром по расширению.

    Args:
        path_folder: Корневая папка.
        extension: Расширение файла (например, '.xlsx').

    Yields:
        Путь к каждому подходящему файлу.
    """
    for path in Path(path_folder).rglob(f"*{extension}"):
        yield path


def processing_excel(path_folder: str | Path, save_file: str = "обработка.xlsx") -> None:
    """Обработка всех xlsx-файлов в папке и сохранение результата.

    Args:
        path_folder: Папка с файлами.
        save_file: Имя файла для сохранения.
    """
    folder = Path(path_folder)
    all_df: pd.DataFrame | None = None

    for path_file in cycle_in_folder(folder, ".xlsx"):
        print(f"\n{path_file}")
        df = pd.read_excel(path_file)
        df = processing_df(df)
        all_df = df if all_df is None else pd.concat([all_df, df], ignore_index=True)

    if all_df is None:
        print("Не найдено xlsx-файлов")
        return

    all_df = all_df.drop_duplicates(subset=["1", "2"], keep="first")
    all_df.to_excel(folder / save_file, index=False)


if __name__ == "__main__":
    processing_excel(Path("/machine_learning/machine_learning_model/eq"))
