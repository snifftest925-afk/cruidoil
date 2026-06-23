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
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def get_crude_price():
    headers = {
        "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    # Replace instrument_key with actual MCX Crude Oil instrument key
    instrument_key = "MCX_FO|YOUR_CRUDEOIL_INSTRUMENT"

    url = f"https://api.upstox.com/v2/market-quote/ltp?instrument_key={instrument_key}"

    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    send_msg("🚀 Upstox Crude Oil Bot Started")

    while True:
        try:
            data = get_crude_price()
            print(data)

            # TODO:
            # 1. Fetch option chain
            # 2. Calculate EMA / RSI
            # 3. Select ATM strike
            # 4. Send Telegram signal

            time.sleep(60)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)
