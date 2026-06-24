import os
import time
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UPSTOX_ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

LAST_SIGNAL = None

def send_msg(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )
    except Exception as e:
        print("Telegram Error:", e)

def get_crude_price():
    headers = {
        "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    # IMPORTANT:
    # Replace with actual CRUDEOIL FUTURE instrument key later
    instrument_key = "MCX_FO|YOUR_CRUDE_FUT_KEY"

    url = f"https://api.upstox.com/v2/market-quote/quotes?instrument_key={instrument_key}"

    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(r.text)

        data = r.json()

        # Adjust after real response received
        return data

    except Exception as e:
        print("Price Error:", e)
        return None

def generate_signal(price):
    global LAST_SIGNAL

    if not price:
        return

    # Dummy logic for testing
    if LAST_SIGNAL != "BUY":
        LAST_SIGNAL = "BUY"

        send_msg(
            "🟢 CRUDEOIL BUY\n\n"
            f"Price: {price}\n"
            "Target: +30\n"
            "SL: -20"
        )

def main():
    send_msg("🚀 Crude Oil Signal Bot Started")

    while True:
        try:
            price = get_crude_price()

            print("PRICE:", price)

            generate_signal(price)

            time.sleep(300)

        except Exception as e:
            print("Main Error:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
