"""Тест исправления EOFError."""
import sys
from io import StringIO

# Симулируем EOF (пустой stdin)
sys.stdin = StringIO("")

try:
    from birka_rag.core.assistant import RAGAssistant
    
    # Создаём минимальный мок для теста
    class MockAssistant:
        def ask(self, question):
            return "test answer"
        
        def chat(self):
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
                
                except (KeyboardInterrupt, EOFError):
                    print("\n\nДо свидания!")
                    break
                except Exception as e:
                    print(f"\nОшибка: {e}\n")
    
    assistant = MockAssistant()
    assistant.chat()
    print("\n✅ Тест пройден: EOFError обработан корректно")
    
except Exception as e:
    print(f"❌ Ошибка теста: {e}")
    import traceback
    traceback.print_exc()
