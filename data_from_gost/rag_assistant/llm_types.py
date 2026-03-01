"""Типы провайдеров LLM."""

from typing import Literal

LLMProvider = Literal["ollama", "openai"]

__all__ = ["LLMProvider"]
