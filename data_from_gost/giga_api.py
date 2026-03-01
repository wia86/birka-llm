
API_KEY = "MDE5YWJhNmItMmQ2OS03ZGI1LTg2N2ItZmY3MzI3NzJkZjQzOmQzNjI1NTBhLWI5NjMtNDg2Zi1hMzJhLTFkMzgwODY2MmRjZA=="

# giga_oauth_working.py
import requests
import base64
import uuid
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
CLIENT_ID     = "019aba6b-2d69-7db5-867b-ff732772df43"      # например: 1a2b3c4d-...
CLIENT_SECRET = API_KEY  # например: 5e6f7g8h-...
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

# Правильная base64-кодировка (именно так хочет Сбер)
auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
auth_bytes  = auth_string.encode("utf-8")
auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

oauth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload = {
    "scope": "GIGACHAT_API_PERS"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "RqUID": str(uuid.uuid4()),
    "Authorization": f"Basic {auth_base64}"   # ← вот так точно работает
}

response = requests.post(
    oauth_url,
    data=payload,
    headers=headers,
    verify=False,          # отключаем проверку сертификата
    timeout=30
)

print("Статус OAuth:", response.status_code)
print(response.json())

if response.status_code == 200:
    access_token = response.json()["access_token"]
    print("\nТокен получен! Действует ≈ 30 минут")
    print(access_token[:50] + "...")
else:
    print("\nНе получилось. Самые частые причины:")
    print("1. Client ID или Client Secret скопированы с пробелами")
    print("2. В личном кабинете выбран scope GIGACHAT_API_CORP вместо PERS")
    print("3. Приложение не подтверждено (для PERS обычно подтверждается мгновенно)")