import time

from market_data import get_candles
from structure import get_structure_bias
from telegram_bot import send_telegram

SYMBOL = "XAUUSD"
TIMEFRAME = "15m"

CHECK_INTERVAL = 60  # seconds
last_bias = None


def run():
    global last_bias

    send_telegram(
        "✅ Trading bot is LIVE on Railway.\n"
        "📊 Symbol: XAUUSD\n"
        "⏱ Timeframe: 15m\n"
        "Awaiting market conditions..."
    )

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

        if bias != last_bias:
            send_telegram(
                f"📊 {SYMBOL} – {TIMEFRAME}\n"
                f"🧠 Structure Bias: {bias.upper()}"
            )
            last_bias = bias

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
