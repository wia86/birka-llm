import os

import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer, InputExample, losses
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

def create_model(path_init: list[str],
                 path_new_model: str = '',
                 model_name: str = 'all-MiniLM-L6-v2',
                 test: float or int = 0) -> SentenceTransformer:
    """ Создание модели из файла excel
    :param path_init: Путь к файлу excel с данными для обучения
    :param path_model: Путь для сохранения модели
    :param test: 0 - обучение и сохранение модели, если больше 0 - тестирование (доля тестируемых данных)
    :return: Обученная модель SentenceTransformer
    """

    # Пример подготовки данных для обучения из csv файла
    df_data = pd.DataFrame()
    for path in path_init:

        df_data_i = pd.read_excel(path)
        # Берем первые 3 столбца
        df_data_i = df_data_i.iloc[:, :3]
        df_data_i.columns = ['working_name', 'official_name', 'label']

        df_data = pd.concat([df_data, df_data_i], ignore_index=True) if not df_data.empty else df_data_i

    # Удалим строки с пропущенными значениями
    df_data.dropna(inplace=True)
    print(df_data.head(10))

    # Преобразуем все в строки
    df_data['working_name'] = df_data['working_name'].astype(str)
    df_data['official_name'] = df_data['official_name'].astype(str)

    # Загрузка базовой модели  #  pip install --upgrade transformers accelerate
    model = SentenceTransformer(model_name)

    # Если параметр test > 0, разделяем данные на тренировочную и тестовую выборки
    if test > 0:
        train_df, test_df = train_test_split(df_data, test_size=test, random_state=42)
        print(f"Размер тренировочной выборки: {len(train_df)}")
        print(f"Размер тестовой выборки: {len(test_df)}")

        # Обучение на тренировочных данных
        train_model(model, train_df)

        # Тестирование модели
        metrics = evaluate_model(model, test_df)

        # Дообучение на тестовых данных после тестирования
        print("\nНачало дообучения модели на тестовых данных...")
        train_model(model, test_df)
        print("Дообучение завершено!")

    else:
        # Обучение на всех данных
        train_model(model, df_data)
        # test_df = None

    # # Подготовь данные в формате InputExample
    # # Создаём список InputExample
    # train_examples = [
    #     InputExample(texts=[row.working_name, row.official_name], label=float(row.label))
    #     for row in train_df.itertuples(index=False)
    # ]
    #
    # # Создаём DataLoader
    # train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    #
    # # Модель для векторных представлений
    # #  pip install --upgrade transformers accelerate
    # model = SentenceTransformer(model_name)
    #
    # #  Выбираем функцию потерь
    # train_loss = losses.CosineSimilarityLoss(model)
    #
    # model.fit(
    #     train_objectives=[(train_dataloader, train_loss)],
    #     epochs=1,
    #     warmup_steps=100,
    #     show_progress_bar=True
    # )  # pip install datasets
    #
    # # Если test > 0, проводим тестирование модели
    # if test > 0:
    #     evaluate_model(model, test_df)

    if path_new_model:
        os.makedirs(path_new_model, exist_ok=True)
        model.save(path_new_model)
    return model

def train_model(model: SentenceTransformer, data_df: pd.DataFrame, epochs: int = 1):
    """
    Обучение модели на заданных данных
    :param model: Модель для обучения
    :param data_df: DataFrame с данными для обучения
    :param epochs: Количество эпох обучения
    """
    # Подготовка данных в формате InputExample
    train_examples = [
        InputExample(texts=[row.working_name, row.official_name], label=float(row.label))
        for row in data_df.itertuples(index=False)
    ]

    # Создаём DataLoader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

    # Выбираем функцию потерь
    train_loss = losses.CosineSimilarityLoss(model)

    # Обучение модели
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=100,
        show_progress_bar=True
    )  # pip install datasets

def evaluate_model(model, test_df):
    """
    Тестирование модели на тестовой выборке
    :param model: Обученная модель
    :param test_df: DataFrame с тестовыми данными
    """
    print("\nНачало тестирования модели...")

    # Получаем эмбеддинги для названий из тестовой выборки
    working_embeddings = model.encode(test_df['working_name'].tolist())
    official_embeddings = model.encode(test_df['official_name'].tolist())

    # Вычисляем косинусное сходство между эмбеддингами
    similarities = []
    for i in range(len(working_embeddings)):
        sim = np.dot(working_embeddings[i], official_embeddings[i]) / (
                np.linalg.norm(working_embeddings[i]) * np.linalg.norm(official_embeddings[i])
        )
        similarities.append(sim)

    # Преобразуем сходство в бинарные метки (1, если сходство > 0.5, иначе 0)
    predicted_labels = [1 if sim > 0.5 else 0 for sim in similarities]
    true_labels = test_df['label'].tolist()

    # Вычисляем метрики
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, zero_division=0)
    recall = recall_score(true_labels, predicted_labels, zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, zero_division=0)

    print(f"Результаты тестирования:")
    print(f"Точность: {accuracy:.4f}")
    print(f"Прецизионность: {precision:.4f}")
    print(f"Отзывать: {recall:.4f}")
    print(f"F1 счет: {f1:.4f}")

    # Выводим некоторые примеры предсказаний
    print("\nПримеры предсказаний:")
    for i in range(min(10, len(test_df))):
        print(f"Пример {i + 1}:")
        print(f"Working name: {test_df['working_name'].iloc[i]}")
        print(f"Official name: {test_df['official_name'].iloc[i]}")
        print(f"True label: {true_labels[i]}")
        print(f"Predicted label: {predicted_labels[i]}")
        print(f"Similarity: {similarities[i]:.4f}")
        print("-" * 50)

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }



if __name__ == '__main__':

    # C:\Users\ADMIN\.cache\huggingface\hub

    # Создание и сохранение модели
    create_model(path_init = [
        # r"D:\birka\machine_learning_model\data_tkz_arm.xlsx",
        # r"D:\birka\machine_learning_model\data_tkz_equipment.xlsx",
        r"D:\birka\machine_learning_model\data_tkz_err.xlsx",
        ],
        path_new_model=r"/machine_learning/machine_learning_model\sberbank_ai_sbert_large_nlu_ru_model_tkz_arm_and_equipment_2",
        # 'all-MiniLM-L6-v2'
        # 'sberbank-ai/sbert_large_nlu_ru'
        # 'DeepPavlov/rubert-base-cased'
        # 'paraphrase-multilingual-MiniLM-L12-v2'
        model_name = r'D:\birka\machine_learning_model\sberbank_ai_sbert_large_nlu_ru_model_tkz_arm_and_equipment',
        test=0)
    # all-MiniLM-L6-v2
    #
    # Результаты тестирования:
    # Точность: 0.9678
    # Прецизионность: 0.9693
    # Отзывать: 0.9970
    # F1 счет: 0.9830
    #
    # sberbank-ai/sbert_large_nlu_ru
    #
    # Начало тестирования модели...
    # Результаты тестирования:
    # Точность: 0.9733
    # Прецизионность: 0.9767
    # Отзывать: 0.9951
    # F1 счет: 0.9858
    #
    # DeepPavlov/rubert-base-case
    # Начало тестирования модели...
    # Результаты тестирования:
    # Точность: 0.9687
    # Прецизионность: 0.9702
    # Отзывать: 0.9970
    # F1 счет: 0.9834

    #
    # paraphrase-multilingual-MiniLM-L12-v2
    # Начало тестирования модели...
    # Результаты тестирования:
    # Точность: 0.9705
    # Прецизионность: 0.9712
    # Отзывать: 0.9980
    # F1 счет: 0.9844
