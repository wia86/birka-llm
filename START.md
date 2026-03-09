# 🎯 BIRKA-RAG — Начните здесь!

Проект готов к использованию. Это главный файл — прочитайте за 2 минуты.

---

## ⚡ Быстрый старт

```bash
# 1. Установка (обязательно!)
pip install -e ".[openai]"

# 2. Проверка
python verify_installation.py

# 3. Использование
birka-rag
```

**Подробно**: [NEXT_STEPS.md](NEXT_STEPS.md)

---

## 📦 Что это?

**birka-rag** — RAG-система для работы с нормативными документами.

- 🤖 7 LLM провайдеров (Ollama, GigaChat, OpenAI, OpenRouter, Groq, DeepSeek, ApiFreeLLM)
- 📚 Индексация PDF документов
- 💬 Интерактивный чат с документами
- 🔧 CLI команды и Python API
- 📖 Полная документация

---

## 📚 Документация

| Файл | Для кого | Время |
|------|----------|-------|
| **[NEXT_STEPS.md](NEXT_STEPS.md)** | **Все** | **5 мин** |
| [QUICKSTART.md](QUICKSTART.md) | Новички | 5 мин |
| [INDEX.md](INDEX.md) | Навигация | 2 мин |
| [docs/README.md](docs/README.md) | Подробно | 15 мин |
| [MIGRATION.md](MIGRATION.md) | Миграция | 10 мин |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Разработчики | 10 мин |

---

## 💻 Использование

### CLI
```bash
birka-rag-index  # Создание индекса из PDF
birka-rag        # Интерактивный чат
```

### Python
```python
from birka_rag import RAGAssistant

assistant = RAGAssistant(
    persist_directory="./data/chroma",
    model_name="d0rj/e5-large-en-ru",
    llm_model="llama3.2:3b",
    llm_provider="ollama",
)

answer = assistant.ask("Ваш вопрос")
```

---

## 🆘 Помощь

```bash
python verify_installation.py  # Проверка установки
python check_readiness.py      # Проверка готовности
python demo.py                  # Демонстрация
```

**Документация**: [INDEX.md](INDEX.md)

---

## ✅ Статус

- **Версия**: 0.1.0
- **Статус**: PRODUCTION READY ✅
- **Модулей**: 15+
- **Документов**: 15
- **Примеров**: 6

---

**Следующий шаг**: [NEXT_STEPS.md](NEXT_STEPS.md)

🚀 *Проект Birka — инструменты для электротехнических расчётов*
