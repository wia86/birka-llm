"""Клиент ApiFreeLLM (apifreellm.com) — свой формат API, не OpenAI-compatible."""

from __future__ import annotations

import os
from typing import Any

import httpx
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

APIFREELLM_API_BASE = "https://apifreellm.com/api/v1"
APIFREELLM_ENV_KEY = "APIFREELLM_API_KEY"


def _messages_to_text(messages: list[BaseMessage]) -> str:
    """Собрать текст из списка сообщений для одного запроса."""
    parts: list[str] = []
    for m in messages:
        content = getattr(m, "content", None)
        if isinstance(content, str) and content.strip():
            parts.append(content.strip())
    return "\n\n".join(parts) if parts else ""


class ChatApiFreeLLM(BaseChatModel):
    """Чат-модель для ApiFreeLLM (POST /api/v1/chat, body: {message})."""

    api_key: str = ""
    api_base: str = APIFREELLM_API_BASE
    model: str = "apifreellm"
    timeout: float = 120.0

    def __init__(self, api_key: str | None = None, **kwargs: Any) -> None:
        key = api_key or os.environ.get(APIFREELLM_ENV_KEY, "").strip()
        super().__init__(api_key=key, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "apifreellm"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        text = _messages_to_text(messages)
        if not text:
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=""))])

        if not self.api_key:
            raise ValueError(
                f"Не задан API-ключ. Установите переменную окружения {APIFREELLM_ENV_KEY}."
            )

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(
                f"{self.api_base.rstrip('/')}/chat",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                json={"message": text},
            )
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise ValueError("Ответ API не является объектом")
        answer = data.get("response") or data.get("message") or ""
        if not isinstance(answer, str):
            answer = str(answer)

        generation = ChatGeneration(message=AIMessage(content=answer))
        return ChatResult(generations=[generation])


__all__ = ["ChatApiFreeLLM"]
