# Настройка GigaChat API

## Получение API ключа

1. **Регистрация в Studio**
   - Перейдите на [https://developers.sber.ru/studio/](https://developers.sber.ru/studio/)
   - Зарегистрируйтесь, используя Сбер ID

2. **Создание проекта**
   - В личном кабинете нажмите "Создать проект"
   - Выберите "GigaChat API" в разделе "AI-модели"
   - Введите название проекта
   - Ознакомьтесь и примите пользовательское соглашение

3. **Получение ключа авторизации**
   - В интерфейсе проекта сгенерируйте "ключ авторизации" (Authorization key)
   - Этот ключ будет использоваться как API ключ

4. **Получение токенов (опционально)**
   - По умолчанию подключается тариф Freemium с ограниченным количеством токенов
   - Для расширения лимитов приобретите дополнительные пакеты токенов

## Настройка переменной окружения

Создайте переменную окружения `GIGACHAT_API_KEY` со значением вашего ключа авторизации:

### Windows (PowerShell)
```powershell
$env:GIGACHAT_API_KEY = "ваш_ключ_авторизации"
```

### Windows (Командная строка)
```cmd
set GIGACHAT_API_KEY=ваш_ключ_авторизации
```

### Linux/macOS
```bash
export GIGACHAT_API_KEY=ваш_ключ_авторизации
```

### Постоянная настройка (Windows)
1. Откройте "Свойства системы" → "Дополнительные параметры системы"
2. Нажмите "Переменные среды"
3. В разделе "Переменные пользователя" нажмите "Создать"
4. Введите:
   - Имя переменной: `GIGACHAT_API_KEY`
   - Значение переменной: ваш ключ авторизации

## Проверка настройки

Запустите скрипт для проверки:

```python
python no_import_to_birka/machine_learning/data_from_gost/run_lln.py
```

Или в интерактивном режиме:
```python
from rag_assistant import RAGAssistant, get_active_profile, set_active_profile

# Установка профиля GigaChat
set_active_profile("gigachat")
profile = get_active_profile()

# Создание ассистента (автоматически проверит наличие API ключа)
assistant = RAGAssistant(**profile.to_kwargs())

# Тестовый запрос
answer = assistant.ask("Привет, это тест подключения к GigaChat")
print(answer)
```

## Устранение проблем

### Ошибка "Не задан API-ключ"
- Проверьте, что переменная окружения `GIGACHAT_API_KEY` установлена
- Убедитесь, что ключ авторизации скопирован правильно из личного кабинета

### Ошибка подключения
- Проверьте доступность интернета
- Убедитесь, что у вас есть токены (в Freemium тарифе есть лимиты)
- Проверьте статус вашего проекта в личном кабинете

### Ошибка авторизации
- Возможно, срок действия ключа истек - сгенерируйте новый в личном кабинете
- Проверьте, что используете ключ авторизации, а не токен доступа

## Дополнительная информация

- **Scope**: Для физических лиц используется `GIGACHAT_API_PERS`
- **Документация**: [https://developers.sber.ru/docs/ru/gigachat/overview](https://developers.sber.ru/docs/ru/gigachat/overview)
- **Тарифы**: [https://developers.sber.ru/docs/ru/gigachat/api/tariffs](https://developers.sber.ru/docs/ru/gigachat/api/tariffs)
- **Поддержка**: Telegram-бот [@gigachat_helpbot](https://t.me/gigachat_helpbot)
