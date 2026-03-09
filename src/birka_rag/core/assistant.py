"""RAG-помощник: Chroma + Embeddings + LLM (Ollama / OpenAI / GigaChat)."""

import json
import os
from importlib import import_module
from pathlib import Path
from typing import cast

import httpx
import requests
import torch
from langchain_chroma import Chroma
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from .providers.apifreellm import ChatApiFreeLLM
from .providers.gigachat import gigachat_get_bearer_token
from .types import LLMProvider

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"


RAG_META_FILENAME = ".rag_embedding_meta.json"


def _is_e5_model(model_name: str) -> bool:
    """Проверка, что модель E5 (требует префикса query: для запроса)."""
    return "e5" in (model_name or "").lower()


CHROMA_DB_NAME = "chroma.sqlite3"


def _resolve_chroma_persist_directory(base: Path) -> Path:
    """Если база создана в режиме per_file, чанки лежат во вложенных папках; возвращаем каталог с данными.

    В per_file create_rag пишет Chroma в base / ... / <subdir>/ (путь может быть вложенным).
    Рекурсивно ищем все каталоги с chroma.sqlite3; если есть не корень — берём самый глубокий (там данные).
    """
    base = base.resolve()
    if not base.is_dir():
        return base
    candidates = [
        p.parent for p in base.rglob(CHROMA_DB_NAME)
        if p.is_file()
    ]
    # Исключаем корень; из оставшихся берём самый глубокий путь (per_file лежит глубже)
    non_root = [c for c in candidates if c != base]
    if non_root:
        return max(non_root, key=lambda p: len(p.parts))
    return base


def _read_rag_embedding_model(persist_directory: Path) -> str | None:
    """Читает из каталога RAG модель эмбеддингов, которой создана база. None если файла нет."""
    path = persist_directory / RAG_META_FILENAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("embedding_model") or None
    except (json.JSONDecodeError, OSError):
        return None


def _load_optional_class(module_name: str, attr_name: str) -> type | None:
    """Подгрузка необязательных зависимостей по требованию."""
    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        return None
    attr = getattr(module, attr_name, None)
    return attr if isinstance(attr, type) else None


ChatOpenAICls = cast(type[BaseChatModel] | None, _load_optional_class("langchain_openai", "ChatOpenAI"))
OPENAI_ERROR_CLS = cast(type[Exception] | None, _load_optional_class("openai", "OpenAIError"))


class RAGAssistant:
    """Технический помощник на основе RAG (Retrieval-Augmented Generation).

    Args:
        persist_directory: Путь к векторной базе данных.
        model_name: Название модели для embeddings.
        llm_model: Название модели LLM (зависит от провайдера).
        temperature: Температура генерации.
        top_k: Количество документов для поиска.
        template: Опциональный шаблон промпта.
        preload: Предзагрузить ли модели сразу.
        llm_provider: Провайдер LLM.
        llm_api_base: Базовый URL сетевого API.
        llm_api_key: Ключ доступа к сетевой LLM.
    """

    DEFAULT_TEMPLATE = (
        'Ты — технический помощник программы "Бирка".\n'
        "Отвечай строго по предоставленным документам, ГОСТам и коду.\n"
        'Если не знаешь — скажи "Я не нашел информацию по этому вопросу".\n'
        "При ответе давай ссылки на пункты нормативов, руководства пользователя.\n\n"
        "Контекст из документов:\n{context}\n\n"
        "Вопрос пользователя: {question}\nОтвет:"
    )

    def __init__(
        self,
        persist_directory: str,
        model_name: str = "intfloat/multilingual-e5-large",
        llm_model: str = "llama3.2:3b",
        temperature: float = 0.2,
        top_k: int = 6,
        template: str | None = None,
        preload: bool = True,
        llm_provider: LLMProvider = "ollama",
        llm_api_base: str | None = None,
        llm_api_key: str | None = None,
    ) -> None:
        self.persist_directory = Path(persist_directory)
        self.model_name = model_name
        self.llm_model = llm_model
        self.temperature = temperature
        self.top_k = top_k
        self.template = template or self.DEFAULT_TEMPLATE
        self.llm_provider = llm_provider
        self.llm_api_base = llm_api_base
        self.llm_api_key = llm_api_key

        self._chain: Runnable | None = None
        self._embeddings: HuggingFaceEmbeddings | None = None
        self._llm: BaseChatModel | None = None

        self._validate_paths()

        if preload:
            self._preload_models()

    def __repr__(self) -> str:
        return (
            f"RAGAssistant(llm={self.llm_model!r}, provider={self.llm_provider!r}, "
            f"embeddings={self.model_name!r}, top_k={self.top_k})"
        )

    def _validate_paths(self) -> None:
        """Проверка существования векторной базы (корень или подпапка per_file)."""
        base = self.persist_directory
        if not base.exists():
            raise FileNotFoundError(
                f"Векторная база не найдена: {base}\n"
                f"Сначала создайте базу с помощью birka-rag-index"
            )
        effective = _resolve_chroma_persist_directory(base)
        if not (effective / CHROMA_DB_NAME).exists():
            raise FileNotFoundError(
                f"В каталоге {base} не найдена Chroma-база (chroma.sqlite3). "
                f"Запустите birka-rag-index для создания RAG."
            )

    def _preload_models(self) -> None:
        """Предзагрузка всех моделей для быстрого старта."""
        print("Предзагрузка моделей...")

        print(f"  Загрузка embeddings модели: {self.model_name}")
        self._embeddings = self._initialize_embeddings()

        print(
            f"  Загрузка LLM модели: "
            f"{self.llm_model} ({self.llm_provider}, {self.llm_api_base or 'локально'})"
        )
        self._llm = self._initialize_llm()

        print("  Прогрев LLM...")
        try:
            self._llm.invoke("test")
        except self._network_exceptions() as e:
            print(f"  Предупреждение: {self._provider_connection_hint(e)}")
        except Exception:
            pass

        print("Все модели загружены и готовы!\n")

    def _initialize_embeddings(self) -> HuggingFaceEmbeddings:
        """Инициализация модели embeddings."""
        if self._embeddings is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={"device": device},
                encode_kwargs={"normalize_embeddings": True},
            )
        return self._embeddings

    def _initialize_vectorstore(self, embeddings: HuggingFaceEmbeddings) -> Chroma:
        """Загрузка векторной базы данных. При per_file использует вложенную папку с chroma.sqlite3."""
        base = self.persist_directory.resolve()
        effective = _resolve_chroma_persist_directory(base)
        if effective != base:
            print(f"  RAG: используется база из подкаталога (per_file): {effective.relative_to(base)}")
        stored_model = _read_rag_embedding_model(effective)
        if stored_model is not None and stored_model != self.model_name:
            print(
                f"Внимание: база RAG создана моделью {stored_model!r}, "
                f"сейчас используется {self.model_name!r}. Рекомендуется пересобрать базу или выбрать ту же модель."
            )
        persist_path = str(effective)
        return Chroma(
            persist_directory=persist_path,
            embedding_function=embeddings,
        )

    def _initialize_llm(self) -> BaseChatModel:
        """Инициализация языковой модели."""
        if self._llm is None:
            try:
                self._llm = self._create_llm()
            except self._network_exceptions() as e:
                raise ConnectionError(self._provider_connection_hint(e)) from e
        return self._llm

    def _create_llm(self) -> BaseChatModel:
        """Создание клиента LLM согласно выбранному провайдеру."""
        match self.llm_provider:
            case "ollama":
                return self._create_ollama_llm()
            case "openai":
                return self._create_openai_llm()
            case "apifreellm":
                return self._create_apifreellm_llm()
            case _ as unsupported:
                raise ValueError(f"Неподдерживаемый провайдер LLM: {unsupported}")

    def _create_ollama_llm(self) -> ChatOllama:
        """Создание клиента Ollama (локального или сетевого)."""
        client_kwargs: dict[str, object] = {
            "model": self.llm_model,
            "temperature": self.temperature,
        }
        if self.llm_api_base:
            client_kwargs["base_url"] = self.llm_api_base
        return ChatOllama(**client_kwargs)

    def _resolve_openai_api_key(self) -> tuple[str, str]:
        """Определяет API-ключ и имя переменной окружения по llm_api_base."""
        if self.llm_api_key:
            return self.llm_api_key, "llm_api_key"
        base = (self.llm_api_base or "").lower()
        if "gigachat" in base:
            try:
                return gigachat_get_bearer_token(), "GIGACHAT_API_KEY"
            except (ValueError, RuntimeError) as e:
                raise ValueError(
                    f"GigaChat: не удалось получить OAuth-токен. {e}\n"
                    "Задайте GIGACHAT_API_KEY (ключ из кабинета или Client Secret). "
                    "При отдельном Client ID — также GIGACHAT_CLIENT_ID."
                ) from e
        if "openrouter" in base:
            return os.getenv("OPENROUTER_API_KEY", ""), "OPENROUTER_API_KEY"
        if "groq" in base:
            return os.getenv("GROQ_API_KEY", ""), "GROQ_API_KEY"
        if "deepseek" in base:
            return os.getenv("DEEPSEEK_API_KEY", ""), "DEEPSEEK_API_KEY"
        return os.getenv("OPENAI_API_KEY", ""), "OPENAI_API_KEY"

    @staticmethod
    def _is_false_env(raw: str) -> bool:
        """Преобразует строку env в булево \"ложь\" (0/false/no/off)."""
        return raw.strip().lower() in {"0", "false", "no", "off"}

    def _resolve_tls_verify(self) -> bool | str:
        """Определяет TLS verify для HTTP-клиента OpenAI-совместимых провайдеров.

        Поддерживаемые переменные окружения:
        - GIGACHAT_VERIFY_SSL_CERTS=0|false|no|off (отключить verify только для gigachat)
        - GIGACHAT_CA_BUNDLE_FILE=<путь до PEM/CRT>
        - RAG_CA_BUNDLE_FILE=<путь до PEM/CRT> (для всех openai-совместимых)
        """
        base = (self.llm_api_base or "").lower()
        if "gigachat" in base and self._is_false_env(os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "")):
            return False

        for env_name in ("GIGACHAT_CA_BUNDLE_FILE", "RAG_CA_BUNDLE_FILE"):
            bundle_path = os.getenv(env_name, "").strip()
            if bundle_path:
                return bundle_path

        return True

    def _create_openai_llm(self) -> BaseChatModel:
        """Создание клиента для OpenAI-совместимого сетевого API (GigaChat, OpenRouter, Groq, OpenAI)."""
        if ChatOpenAICls is None:
            raise ImportError(
                "Модуль langchain-openai не установлен. "
                "Установите 'langchain-openai' и 'openai', чтобы использовать сетевую LLM."
            )

        api_key, env_var_name = self._resolve_openai_api_key()

        if not api_key:
            raise ValueError(
                f"Не задан API-ключ для сетевой LLM. "
                f"Передайте llm_api_key или установите переменную окружения {env_var_name}."
            )

        client_kwargs: dict[str, object] = {
            "model": self.llm_model,
            "temperature": self.temperature,
            "api_key": api_key,
        }
        if self.llm_api_base:
            client_kwargs["base_url"] = self.llm_api_base
        tls_verify = self._resolve_tls_verify()
        if tls_verify is not True:
            client_kwargs["http_client"] = httpx.Client(verify=tls_verify)

        return ChatOpenAICls(**client_kwargs)

    def _create_apifreellm_llm(self) -> BaseChatModel:
        """Создание клиента ApiFreeLLM (свой формат API)."""
        api_key = (self.llm_api_key or "").strip() or os.getenv("APIFREELLM_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "Не задан API-ключ для ApiFreeLLM. "
                "Установите переменную окружения APIFREELLM_API_KEY."
            )
        return ChatApiFreeLLM(
            api_key=api_key,
            api_base=(self.llm_api_base or "https://apifreellm.com/api/v1").rstrip("/"),
        )

    @staticmethod
    def _network_exceptions() -> tuple[type[Exception], ...]:
        """Кортеж сетевых исключений для переиспользования."""
        base: tuple[type[Exception], ...] = (
            ConnectionError,
            httpx.ConnectError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
        )
        if OPENAI_ERROR_CLS is not None:
            return base + (OPENAI_ERROR_CLS,)
        return base

    def _provider_connection_hint(self, error: Exception) -> str:
        """Формирование сообщения о проблеме подключения."""
        if self.llm_provider == "ollama":
            url_hint = self.llm_api_base or DEFAULT_OLLAMA_URL
            return (
                "Ollama недоступна.\n"
                "Проверьте, что:\n"
                f"  1. Сервис Ollama запущен и доступен по адресу {url_hint}\n"
                f"  2. Модель {self.llm_model} загружена (ollama pull {self.llm_model})\n"
                f"Детали ошибки: {error}"
            )
        if self.llm_provider == "apifreellm":
            base_url = self.llm_api_base or "https://apifreellm.com/api/v1"
            return (
                "ApiFreeLLM недоступен.\n"
                "Проверьте:\n"
                f"  1. base_url: {base_url}\n"
                "  2. Переменная окружения APIFREELLM_API_KEY\n"
                "  3. Лимит: 1 запрос в 25 сек (free tier)\n"
                f"Детали ошибки: {error}"
            )

        base_url = self.llm_api_base or "https://api.openai.com/v1"
        _, env_var_hint = self._resolve_openai_api_key()

        return (
            "Сетевая LLM недоступна.\n"
            "Проверьте настройки API:\n"
            f"  1. Корректен ли base_url ({base_url})\n"
            f"  2. Задан ли API-ключ (параметр llm_api_key или переменная {env_var_hint})\n"
            "  3. Разрешен ли доступ к модели у провайдера\n"
            f"Детали ошибки: {error}"
        )

    @staticmethod
    def _format_docs(docs: list) -> str:
        """Преобразует список Document в одну строку для подстановки в промпт."""
        if not docs:
            return "(релевантные фрагменты не найдены)"
        parts = []
        for d in docs:
            text = getattr(d, "page_content", str(d))
            if isinstance(text, str) and text.strip():
                parts.append(text.strip())
        return "\n\n---\n\n".join(parts) if parts else "(релевантные фрагменты не найдены)"

    def _build_chain(self) -> Runnable:
        """Построение цепочки RAG."""
        embeddings = self._initialize_embeddings()
        vectorstore = self._initialize_vectorstore(embeddings)
        try:
            n = vectorstore._collection.count()
            print(f"  RAG: в базе {n} чанков")
        except Exception:
            pass
        base_retriever = vectorstore.as_retriever(search_kwargs={"k": self.top_k})
        if _is_e5_model(self.model_name):
            retriever = RunnableLambda(
                lambda q: base_retriever.invoke("query: " + q if isinstance(q, str) else q)
            )
        else:
            retriever = base_retriever
        context_str = RunnableLambda(
            lambda x: (
                self._format_docs(x) if isinstance(x, list) else self._format_docs([x])
            )
        )
        llm = self._initialize_llm()
        prompt = PromptTemplate.from_template(self.template)

        return (
            {"context": retriever | context_str, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    @property
    def chain(self) -> Runnable:
        """Ленивая инициализация цепочки."""
        if self._chain is None:
            self._chain = self._build_chain()
        return self._chain

    def ask(self, question: str) -> str:
        """Задать вопрос помощнику."""
        try:
            return self.chain.invoke(question)
        except self._network_exceptions() as e:
            raise ConnectionError(self._provider_connection_hint(e)) from e

    def chat(self) -> None:
        """Интерактивный режим общения."""
        print("RAG Помощник готов к работе!")
        print("Введите 'выход' или 'quit' для завершения.\n")

        while True:
            try:
                question = input("Вопрос: ").strip()

                if question.lower() in ("выход", "quit", "exit", "q"):
                    print("До свидания!")
                    break

                if not question:
                    continue

                print(f"\nОтвет: {self.ask(question)}\n")

            except KeyboardInterrupt:
                print("\n\nДо свидания!")
                break
            except self._network_exceptions() as e:
                print(f"\nОшибка подключения: {self._provider_connection_hint(e)}\n")
            except Exception as e:
                print(f"\nОшибка: {e}\n")


__all__ = ["RAGAssistant", "DEFAULT_OLLAMA_URL"]
