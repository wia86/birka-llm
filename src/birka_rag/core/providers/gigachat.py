"""Утилита для получения токена GigaChat API.

GigaChat требует OAuth: по ключу авторизации получается access_token (~30 мин),
который передаётся в запросах как Bearer. Ключ из личного кабинета — это
Base64(Client ID:Client Secret) или отдельно GIGACHAT_CLIENT_ID и GIGACHAT_API_KEY.
"""

import base64
import os
import uuid

OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
SCOPE = "GIGACHAT_API_PERS"


def _oauth_request(auth_b64: str) -> str:
    """Запрос access_token по Basic auth_b64. Использует requests с verify=False."""
    import urllib3

    import requests

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {auth_b64}",
    }
    resp = requests.post(
        OAUTH_URL,
        data={"scope": SCOPE},
        headers=headers,
        verify=False,
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f"GigaChat OAuth ошибка ({resp.status_code}): {resp.text}\n"
            "Проверьте ключ в личном кабинете https://developers.sber.ru/studio"
        )
    return resp.json()["access_token"]


def gigachat_get_bearer_token() -> str:
    """Получить Bearer-токен для GigaChat API (для заголовка Authorization: Bearer).

    Читает из окружения:
    - GIGACHAT_API_KEY (обязательно): ключ авторизации из кабинета (Base64)
      или Client Secret, если задан GIGACHAT_CLIENT_ID.
    - GIGACHAT_CLIENT_ID (опционально): UUID приложения. Если задан,
      GIGACHAT_API_KEY трактуется как Client Secret и строится Base64(Client ID:Secret).

    Returns:
        access_token для использования как Bearer (действует ~30 мин).
    """
    client_id = os.environ.get("GIGACHAT_CLIENT_ID", "").strip()
    api_key = os.environ.get("GIGACHAT_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "Задайте переменную окружения GIGACHAT_API_KEY. "
            "См. документацию и https://developers.sber.ru/studio"
        )
    if client_id:
        auth_b64 = base64.b64encode(f"{client_id}:{api_key}".encode()).decode()
    else:
        auth_b64 = api_key
    return _oauth_request(auth_b64)


def gigachat_get_token(client_id: str, client_secret: str) -> str:
    """Получить токен для GigaChat API (OAuth по client_id и client_secret).

    Устаревший API; предпочтительно использовать gigachat_get_bearer_token().
    """
    if client_id and client_secret:
        auth_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        return _oauth_request(auth_b64)
    return client_secret or ""


__all__ = ["gigachat_get_bearer_token", "gigachat_get_token"]
