"""Поиск совпадений энергообъектов по эмбеддингам + признакам.

Legacy: зависит от dir_common и moduls из основного репозитория Birka.
"""

import logging
from pathlib import Path

from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity

from dir_common.file import exists
from moduls.network_structure.energy_object_name import EnergyObjectName
from moduls.network_structure.energy_objects import extract_type

logger = logging.getLogger(__name__)


class GetModelML:
    """Загрузка SentenceTransformer из локальной директории."""

    @classmethod
    def get_model(cls, path_model: str | Path) -> SentenceTransformer:
        """Загрузить модель по относительному пути (от cwd).

        Args:
            path_model: Относительный путь к модели.

        Returns:
            Загруженная модель SentenceTransformer.

        Raises:
            FileNotFoundError: Если путь не существует.
        """
        full_path = Path.cwd() / path_model
        exists(str(full_path), error=True)
        return SentenceTransformer(str(full_path))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


def feature_score(name1: str, name2: str) -> float:
    """Оценка совпадения признаков (напряжение, тип) двух энергообъектов.

    Returns:
        Нормализованная оценка в диапазоне [0, 1].
    """
    o1 = EnergyObjectName(name1)
    o2 = EnergyObjectName(name2)

    score = calc_score(o1.u_max, o2.u_max, 1, -1)
    score += calc_score(o1.u_all, o2.u_all, 0.7, -0.7)
    score += calc_score(extract_type(name1), extract_type(name2), 0.3, -0.3)

    return (score + 2) / 4


def calc_score(
    v1: object,
    v2: object,
    score_plus: float = 1,
    score_minus: float = -1,
) -> float:
    """Бинарная оценка совпадения двух значений.

    Returns:
        score_plus при совпадении, score_minus при расхождении, 0 если хотя бы одно пустое.
    """
    if v1 and v2:
        return score_plus if v1 == v2 else score_minus
    return 0


def find_best_match_from_model(
    name: str,
    name_list: list[str],
    model: SentenceTransformer,
    coefficient_similarity: float = 0.8,
    coefficient_f_score: float = 0.2,
) -> tuple[str, int, int]:
    """Найти лучшее совпадение имени из списка кандидатов.

    Комбинирует cosine similarity эмбеддингов и feature_score (напряжение/тип).

    Args:
        name: Искомое имя.
        name_list: Список кандидатов.
        model: Обученная модель SentenceTransformer.
        coefficient_similarity: Вес cosine similarity.
        coefficient_f_score: Вес feature_score.

    Returns:
        Кортеж (лучшее_имя, score_в_процентах, индекс).
    """
    emb1 = model.encode(name, convert_to_tensor=True)

    best_score = 0.0
    best_match = ""
    best_index = 0

    logger.info(f"Поиск для {name}")
    for index, name2 in enumerate(name_list):
        emb2 = model.encode(name2, convert_to_tensor=True)
        similarity = max(0.0, cosine_similarity(emb1, emb2, dim=0).item())
        f_score = feature_score(name, name2)
        total_score = coefficient_similarity * similarity + coefficient_f_score * f_score

        logger.info(f"{name2}: similarity={similarity:.3f}, feature_score={f_score:.3f}, total={total_score:.3f}")

        if total_score > best_score:
            best_score = total_score
            best_match = name2
            best_index = index

    return best_match, int(best_score * 100), best_index


def _test_model() -> None:
    name1 = "ПС Северная 110 кВ"
    candidates = [
        "ПС Южная 110 кВ",
        "ПС Северная 220 кВ",
        "ТП-1 Центральная",
        "Северный узел 110кВ",
    ]

    model = GetModelML.get_model("/machine_learning/machine_learning_model/model_tkz_arm_nodes")
    best_match, score, _ = find_best_match_from_model(name1, candidates, model)
    print(f"Лучшее совпадение: {best_match} (score={score})")
