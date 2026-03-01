"""Утилита для получения токена GigaChat API.

В современных версиях GigaChat API (2024+) API-ключ используется напрямую
без дополнительной OAuth-аутентификации.
"""


def gigachat_get_token(client_id: str, client_secret: str) -> str:
    """Получить токен для GigaChat API.

    Args:
        client_id: UUID приложения (для совместимости, не используется).
        client_secret: API-ключ GigaChat.

    Returns:
        API-ключ для заголовка ``Authorization: Bearer {token}``.
    """
    return client_secret


if __name__ == "__main__":
    import os

    _id = os.environ.get("GIGACHAT_CLIENT_ID", "")
    _secret = os.environ.get("GIGACHAT_API_KEY", "")
    if not _secret:
        print("Задайте переменную окружения GIGACHAT_API_KEY")
        raise SystemExit(1)

    print(gigachat_get_token(_id, _secret))
