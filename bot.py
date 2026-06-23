import os
import time
import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def generate_signal(df):
    df["ema9"] = EMAIndicator(df["close"], 9).ema_indicator()
    df["ema21"] = EMAIndicator(df["close"], 21).ema_indicator()
    df["rsi"] = RSIIndicator(df["close"], 14).rsi()

    last = df.iloc[-1]

    if last["ema9"] > last["ema21"] and last["rsi"] > 55:
        return "CALL"
    elif last["ema9"] < last["ema21"] and last["rsi"] < 45:
        return "PUT"
    return None

def get_data():
    prices = [6900, 6920, 6950, 6980, 7010, 7030, 7050]
    return pd.DataFrame({"close": prices})

while True:
    try:
        df = get_data()
        signal = generate_signal(df)

        if signal == "CALL":
            send_msg("🟢 CRUDEOIL BUY CALL
Entry: 295
TP1: 300
TP2: 305
SL: 292")

        elif signal == "PUT":
            send_msg("🔴 CRUDEOIL BUY PUT
Entry: 295
TP1: 290
TP2: 285
SL: 298")

        time.sleep(60)

    except Exception as e:
        print(e)
        time.sleep(10)
