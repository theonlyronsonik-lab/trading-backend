# main.py

import time
from market_data import fetch_candles
from structure import get_structure_bias
from telegram_bot import send_telegram
from config import SYMBOL, TIMEFRAME

def run():
    send_telegram("✅ Trading bot is LIVE on Railway.\nAwaiting market conditions...")

    last_bias = None

    while True:
        candles = fetch_candles()

        if not candles:
            send_telegram("⚠️ Market data failed. No candles received.")
            time.sleep(300)
            continue

        bias = get_structure_bias(candles)

        if bias != last_bias:
            send_telegram(
                f"📊 MARKET STRUCTURE UPDATE\n"
                f"Symbol: {SYMBOL}\n"
                f"Timeframe: {TIMEFRAME}\n"
                f"Bias: {bias}"
            )
            last_bias = bias

        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    run()
