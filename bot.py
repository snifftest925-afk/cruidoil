import os
import time
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

UPSTOX_API_KEY = os.getenv("UPSTOX_API_KEY")
UPSTOX_API_SECRET = os.getenv("UPSTOX_API_SECRET")
UPSTOX_ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def test_upstox_connection():
    headers = {
        "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    print("=== TESTING UPSTOX CONNECTION ===")

    r = requests.get(
        "https://api.upstox.com/v2/user/profile",
        headers=headers
    )
    print("PROFILE RESPONSE:")
    print(r.text)

    r = requests.get(
        "https://api.upstox.com/v2/option/contract?instrument_key=MCX_FO",
        headers=headers
    )
    print("OPTION CHAIN RESPONSE:")
    print(r.text)

if __name__ == "__main__":
    send_msg("🚀 Upstox Debug Bot Started")

    while True:
        try:
            test_upstox_connection()
            time.sleep(300)
        except Exception as e:
            print("ERROR:", e)
            time.sleep(30)
