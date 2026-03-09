"""Типы провайдеров LLM."""

from typing import Literal

LLMProvider = Literal["ollama", "openai", "apifreellm"]

__all__ = ["LLMProvider"]
