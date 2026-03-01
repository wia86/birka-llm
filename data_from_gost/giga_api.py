"""OAuth-аутентификация для GigaChat API (получение access_token)."""

import base64
import os
import uuid

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


def get_gigachat_token(client_id: str, client_secret: str, scope: str = "GIGACHAT_API_PERS") -> str:
    """Получить access_token для GigaChat через OAuth.

    Args:
        client_id: UUID приложения из личного кабинета Сбера.
        client_secret: API-ключ (или секрет приложения).
        scope: Scope токена (GIGACHAT_API_PERS / GIGACHAT_API_CORP).

    Returns:
        access_token (действует ~30 минут).

    Raises:
        RuntimeError: Если OAuth-запрос завершился ошибкой.
    """
    auth_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {auth_b64}",
    }

    response = requests.post(
        OAUTH_URL,
        data={"scope": scope},
        headers=headers,
        verify=False,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"OAuth ошибка ({response.status_code}): {response.text}\n"
            "Частые причины:\n"
            "  1. Client ID / Secret скопированы с пробелами\n"
            "  2. Scope не соответствует типу подписки\n"
            "  3. Приложение не подтверждено в личном кабинете"
        )

    data = response.json()
    return data["access_token"]


if __name__ == "__main__":
    _client_id = os.environ.get("GIGACHAT_CLIENT_ID", "")
    _client_secret = os.environ.get("GIGACHAT_API_KEY", "")

    if not _client_id or not _client_secret:
        print("Задайте переменные окружения GIGACHAT_CLIENT_ID и GIGACHAT_API_KEY")
        raise SystemExit(1)

    token = get_gigachat_token(_client_id, _client_secret)
    print(f"Токен получен! {token[:50]}...")
