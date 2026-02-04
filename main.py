import time
import os

from market import get_candles
from structure import get_structure_bias
from telegram_bot import send_telegram

SYMBOL = "XAUUSD"
TIMEFRAME = "15m"

CHECK_INTERVAL = 60  # seconds

last_bias = None  # stores previous bias


def run():
    global last_bias

    send_telegram("✅ Trading bot is LIVE on Railway.\nAwaiting market conditions...")

    while True:
        candles = get_candles(SYMBOL, TIMEFRAME)

        if not candles:
            send_telegram("⚠️ Market data failed, no candles received.")
            time.sleep(CHECK_INTERVAL)
            continue

        bias = get_structure_bias(candles)

        if bias is None:
            time.sleep(CHECK_INTERVAL)
            continue

        # ALERT ONLY ON CHANGE
        if bias != last_bias:
            message = (
                f"📊 {SYMBOL} – {TIMEFRAME}\n"
                f"🧠 Structure Bias: {bias.upper()}\n"
            )
            send_telegram(message)
            last_bias = bias

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
