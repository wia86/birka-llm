import base64
import requests


def gigachat_get_token(client_id: str, client_secret: str) -> str:
    """
    Получить токен для GigaChat API.

    В современных версиях GigaChat API (2024+) API ключ можно использовать напрямую
    без дополнительной OAuth аутентификации.

    Параметры:
        - client_id: выдан Сбером (для совместимости, не используется)
        - client_secret: API ключ GigaChat

    Возвращает:
        - access_token (str): API ключ для использования в заголовке Authorization: Bearer {token}
    """
    return client_secret

token = gigachat_get_token(
    client_id="019aba6b-2d69-7db5-867b-ff732772df43",
    client_secret="d362550a-b963-486f-a32a-1d3808662dcd"
)

print(token)