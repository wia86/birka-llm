import os
from typing import Generator

import pandas as pd

from moduls.network_structure.string_matching import calculate_similarity_string

def calculate_match(row: pd.Series) -> pd.Series:
    """Расчет совпадения строк"""

    row['ratio'] = calculate_similarity_string(row['1'], row['2'])
    return row

def processing_df(df: pd.DataFrame) -> pd.DataFrame:

    print(len(df))

    if 'dname' in df.columns:
        df = df[['dname', 'name']]
    else:
        df = df[['ny_name', 'ny_name_node2']]
    df.columns = ['1', '2']
    # Удалить пробелы вначале и в конце 1 и 2 колонки
    df.iloc[:, 0] = df.iloc[:, 0].str.strip()
    df.iloc[:, 1] = df.iloc[:, 1].str.strip()

    # Удалить строки с пустыми строками в 1 или 2 колонке
    df = df[df.iloc[:, 0].str.len() > 0]
    df = df[df.iloc[:, 1].str.len() > 0]

    # Только отличающиеся строки
    df = df[df.iloc[:, 0] != df.iloc[:, 1]]
    # Оставить только уникальные строки
    df = df.drop_duplicates(subset=['1', '2'], keep='first')

    # добавить коленку 3 со значением 1
    df['3'] = 1
    df = df.apply(calculate_match, axis=1)
    print(df.head(15))

    print(len(df))

    return df

def cycle_in_folder(path_folder: str, extension: str) -> Generator[str]:
    """
    Цикл по всем файлам в папке с заданным расширением
    :param path_folder: Папка
    :param extension: Расширение файла
    :return: Путь к файлу
    """
    import os

    for root, dirs, files in os.walk(path_folder):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def processing_excel(path_folder,
                     save_file='обработка.xlsx'
                     ):
    """Обработка всех файлов в папке с расширением .xlsx
    :param path_folder: Папка с файлами
    :param save_file: Имя файла для сохранения"""

    all_df = None
    for path_file in cycle_in_folder(path_folder, '.xlsx'):
        print('\n', path_file)

        df = pd.read_excel(path_file)
        df = processing_df(df)
        all_df = df if all_df is None else pd.concat([all_df, df], ignore_index=True)

    # Сохранить в новый файл
    all_df = all_df.drop_duplicates(subset=['1', '2'], keep='first')
    path_file_new = os.path.join(path_folder, save_file)
    all_df.to_excel(path_file_new, index=False)

if __name__ == '__main__':
    processing_excel(r'/machine_learning/machine_learning_model\eq')
