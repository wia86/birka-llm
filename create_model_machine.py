"""Обучение SentenceTransformer на Excel-данных (working_name → official_name).

Legacy: зависит от machine_learning_model/ из основного репозитория Birka.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import InputExample, SentenceTransformer, losses
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader


def create_model(
    path_init: list[str],
    path_new_model: str = "",
    model_name: str = "all-MiniLM-L6-v2",
    test: float = 0,
) -> SentenceTransformer:
    """Обучить SentenceTransformer на парах (working_name, official_name, label).

    Args:
        path_init: Пути к xlsx-файлам с данными для обучения.
        path_new_model: Путь для сохранения модели (пусто — не сохранять).
        model_name: Базовая модель или путь к ранее обученной.
        test: Доля тестовой выборки (0 — обучение на всех данных).

    Returns:
        Обученная модель SentenceTransformer.
    """
    frames: list[pd.DataFrame] = []
    for path in path_init:
        df_i = pd.read_excel(path)
        df_i = df_i.iloc[:, :3]
        df_i.columns = ["working_name", "official_name", "label"]
        frames.append(df_i)

    df_data = pd.concat(frames, ignore_index=True)
    df_data.dropna(inplace=True)
    df_data["working_name"] = df_data["working_name"].astype(str)
    df_data["official_name"] = df_data["official_name"].astype(str)

    print(df_data.head(10))

    model = SentenceTransformer(model_name)

    if test > 0:
        train_df, test_df = train_test_split(df_data, test_size=test, random_state=42)
        print(f"Тренировочная выборка: {len(train_df)}")
        print(f"Тестовая выборка: {len(test_df)}")

        train_model(model, train_df)
        evaluate_model(model, test_df)

        print("\nДообучение на тестовых данных...")
        train_model(model, test_df)
        print("Дообучение завершено!")
    else:
        train_model(model, df_data)

    if path_new_model:
        out = Path(path_new_model)
        out.mkdir(parents=True, exist_ok=True)
        model.save(str(out))

    return model


def train_model(model: SentenceTransformer, data_df: pd.DataFrame, epochs: int = 1) -> None:
    """Обучение модели на заданных данных.

    Args:
        model: Модель для обучения.
        data_df: DataFrame с колонками working_name, official_name, label.
        epochs: Количество эпох обучения.
    """
    train_examples = [
        InputExample(texts=[row.working_name, row.official_name], label=float(row.label))
        for row in data_df.itertuples(index=False)
    ]

    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=100,
        show_progress_bar=True,
    )


def evaluate_model(model: SentenceTransformer, test_df: pd.DataFrame) -> dict[str, float]:
    """Оценка модели на тестовой выборке (vectorized cosine similarity).

    Args:
        model: Обученная модель.
        test_df: DataFrame с тестовыми данными.

    Returns:
        Словарь метрик: accuracy, precision, recall, f1.
    """
    print("\nТестирование модели...")

    working_emb = model.encode(test_df["working_name"].tolist(), convert_to_numpy=True)
    official_emb = model.encode(test_df["official_name"].tolist(), convert_to_numpy=True)

    # Векторизованное вычисление cosine similarity (вместо поэлементного цикла)
    dot_products = np.sum(working_emb * official_emb, axis=1)
    norms = np.linalg.norm(working_emb, axis=1) * np.linalg.norm(official_emb, axis=1)
    similarities = dot_products / norms

    predicted_labels = (similarities > 0.5).astype(int).tolist()
    true_labels = test_df["label"].tolist()

    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, zero_division=0)
    recall = recall_score(true_labels, predicted_labels, zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, zero_division=0)

    print(f"Результаты тестирования:")
    print(f"  Точность (accuracy):  {accuracy:.4f}")
    print(f"  Прецизионность:       {precision:.4f}")
    print(f"  Полнота (recall):     {recall:.4f}")
    print(f"  F1:                   {f1:.4f}")

    print("\nПримеры предсказаний:")
    for i in range(min(10, len(test_df))):
        print(
            f"  [{i + 1}] working={test_df['working_name'].iloc[i]!r}  "
            f"official={test_df['official_name'].iloc[i]!r}  "
            f"true={true_labels[i]}  pred={predicted_labels[i]}  "
            f"sim={similarities[i]:.4f}"
        )

    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}


if __name__ == "__main__":
    create_model(
        path_init=[
            r"D:\birka\machine_learning_model\data_tkz_err.xlsx",
        ],
        path_new_model=r"/machine_learning/machine_learning_model\sberbank_ai_sbert_large_nlu_ru_model_tkz_arm_and_equipment_2",
        model_name=r"D:\birka\machine_learning_model\sberbank_ai_sbert_large_nlu_ru_model_tkz_arm_and_equipment",
        test=0,
    )
