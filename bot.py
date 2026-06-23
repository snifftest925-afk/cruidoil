import os
import time
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

UPSTOX_API_KEY = os.getenv("UPSTOX_API_KEY")
UPSTOX_API_SECRET = os.getenv("UPSTOX_API_SECRET")
UPSTOX_ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

def send_msg(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram credentials missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

def test_upstox_connection():
    headers = {
        "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    print("\n===== TESTING UPSTOX CONNECTION =====")

    try:
        r = requests.get(
            "https://api.upstox.com/v2/user/profile",
            headers=headers,
            timeout=30
        )

        print("\nPROFILE RESPONSE:")
        print(r.text)

    except Exception as e:
        print("PROFILE ERROR:", e)

    try:
        r = requests.get(
            "https://api.upstox.com/v2/search/instruments",
            headers=headers,
            params={
                "query": "CRUDEOIL"
            },
            timeout=30
        )

        print("\nCRUDEOIL SEARCH RESPONSE:")
        print(r.text)

    except Exception as e:
        print("SEARCH ERROR:", e)

if __name__ == "__main__":
    send_msg("🚀 Upstox Debug Bot Started")

    while True:
        try:
            test_upstox_connection()
            time.sleep(300)

        except Exception as e:
            print("MAIN LOOP ERROR:", e)
            time.sleep(30)
