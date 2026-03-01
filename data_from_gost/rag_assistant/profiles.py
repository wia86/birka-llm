from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .llm_types import LLMProvider


def _get_persist_directory() -> Path:
    """Путь к векторной базе из RAG_PERSIST_DIR или дефолт."""
    raw = os.environ.get("RAG_PERSIST_DIR", "").strip()
    return Path(raw) if raw else Path("./data/chroma_default")


@dataclass(slots=True, frozen=True)
class AssistantProfile:
    """Профиль конфигурации для запуска RAGAssistant."""

    name: str
    persist_directory: Path
    model_name: str
    llm_model: str
    llm_provider: LLMProvider = "ollama"
    llm_api_base: str | None = None
    llm_api_key: str | None = None
    temperature: float = 0.2
    top_k: int = 6
    preload: bool = True
    description: str = ""

    def to_kwargs(self) -> dict[str, object]:
        """Преобразование профиля в аргументы конструктора RAGAssistant."""
        return {
            "persist_directory": str(self.persist_directory),
            "model_name": self.model_name,
            "llm_model": self.llm_model,
            "llm_provider": self.llm_provider,
            "llm_api_base": self.llm_api_base,
            "llm_api_key": self.llm_api_key,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "preload": self.preload,
        }


def _profiles() -> dict[str, AssistantProfile]:
    persist = _get_persist_directory()
    return {
        "ollama_local": AssistantProfile(
            name="Локальная Ollama",
            description="Генерация через локальный сервер Ollama",
            persist_directory=persist,
            model_name="BAAI/bge-m3",
            llm_model="qwen3-vl:8b",
            llm_provider="ollama",
            llm_api_base=None,
            llm_api_key=None,
            temperature=0.2,
            top_k=6,
            preload=True,
        ),
        "openai_cloud": AssistantProfile(
            name="OpenAI-совместимый API",
            description="Сетевая LLM; ключ берётся из OPENAI_API_KEY, если не указан явно",
            persist_directory=persist,
            model_name="BAAI/bge-m3",
            llm_model="gpt-4o-mini",
            llm_provider="openai",
            llm_api_base=None,
            llm_api_key=None,
            temperature=0.2,
            top_k=6,
            preload=True,
        ),
        "gigachat": AssistantProfile(
            name="GigaChat",
            description="Российская LLM от Сбера через API (Scope: GIGACHAT_API_PERS). Требуется API ключ из переменной GIGACHAT_API_KEY",
            persist_directory=persist,
            model_name="BAAI/bge-m3",
            llm_model="GigaChat-2",
            llm_provider="openai",
            llm_api_base="https://gigachat.devices.sberbank.ru/api/v1/",
            llm_api_key=None,
            temperature=0.2,
            top_k=6,
            preload=True,
        ),
    }


ASSISTANT_PROFILES: dict[str, AssistantProfile] = _profiles()

DEFAULT_PROFILE = "ollama_local"
ACTIVE_PROFILE = DEFAULT_PROFILE


def available_profile_names() -> list[str]:
    """Возвращает список доступных профилей."""
    return list(ASSISTANT_PROFILES.keys())


def select_profile(profile_name: str) -> AssistantProfile:
    """Получить профиль по имени с дружелюбной ошибкой."""
    try:
        return ASSISTANT_PROFILES[profile_name]
    except KeyError as exc:
        available = ", ".join(available_profile_names())
        raise ValueError(
            f"Профиль '{profile_name}' не найден. Доступные варианты: {available}"
        ) from exc


def format_profiles() -> str:
    """Формирует текстовое описание всех профилей."""
    lines = []
    for key, profile in ASSISTANT_PROFILES.items():
        lines.append(
            f"- {key}: {profile.name}\n"
            f"    База: {profile.persist_directory}\n"
            f"    Embeddings: {profile.model_name}\n"
            f"    LLM: {profile.llm_model} ({profile.llm_provider})\n"
            f"    Описание: {profile.description or 'нет'}"
        )
    return "\n".join(lines)


def set_active_profile(profile_name: str) -> str:
    """Изменить активный профиль программно."""
    global ACTIVE_PROFILE
    select_profile(profile_name)
    ACTIVE_PROFILE = profile_name
    return ACTIVE_PROFILE


def get_active_profile() -> AssistantProfile:
    """Вернуть активный профиль."""
    return select_profile(ACTIVE_PROFILE)


__all__ = [
    "AssistantProfile",
    "ASSISTANT_PROFILES",
    "DEFAULT_PROFILE",
    "ACTIVE_PROFILE",
    "available_profile_names",
    "select_profile",
    "format_profiles",
    "set_active_profile",
    "get_active_profile",
]

