import os
import time
import requests
import pandas as pd

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UPSTOX_ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

SYMBOL = "CRUDEOIL"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


# ---------- Indicators ----------
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = df['high'].rolling(period).max() - df['low'].rolling(period).min()

    final_upper = hl2 + (multiplier * atr)
    final_lower = hl2 - (multiplier * atr)

    trend = []
    for i in range(len(df)):
        if i == 0:
            trend.append("BUY")
        else:
            if df['close'][i] > final_upper[i-1]:
                trend.append("BUY")
            elif df['close'][i] < final_lower[i-1]:
                trend.append("SELL")
            else:
                trend.append(trend[i-1])

    return trend


# ---------- Fetch Data ----------
def get_candles():
    url = "https://api.upstox.com/v2/historical-candle/intraday/CRUDEOIL/5minute"
    headers = {
        "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    candles = data['data']['candles']

    df = pd.DataFrame(candles, columns=[
        "time", "open", "high", "low", "close", "volume"
    ])

    df = df.astype({"open": float, "high": float, "low": float, "close": float})

    return df


# ---------- Signal Logic ----------
last_signal = None

def check_signal():
    global last_signal

    df = get_candles()

    df["ema200"] = ema(df["close"], 200)
    df["st"] = supertrend(df)

    latest = df.iloc[-1]

    signal = None

    if latest["st"] == "BUY" and latest["close"] > latest["ema200"]:
        signal = "BUY"

    elif latest["st"] == "SELL" and latest["close"] < latest["ema200"]:
        signal = "SELL"

    if signal and signal != last_signal:
        last_signal = signal

        msg = f"""
🚨 CRUDEOIL SIGNAL (5M)

Type: {signal}
Price: {latest['close']}

Strategy: Supertrend + EMA200

Time: {latest['time']}
"""
        send_msg(msg)


# ---------- Main Loop ----------
if __name__ == "__main__":
    send_msg("🚀 CRUDEOIL Bot Started (5M Strategy)")

    while True:
        try:
            check_signal()
            time.sleep(300)  # 5 min

        except Exception as e:
            print("ERROR:", e)
            time.sleep(30)
