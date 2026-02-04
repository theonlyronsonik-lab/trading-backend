from market_data import get_candles
from structure import get_market_bias
from telegram_bot import send_telegram
import time

TIMEFRAME_LABEL = "1H"
SYMBOL = "XAUUSD"

def run():
    send_telegram("✅ Trading bot LIVE\nAnalyzing HTF structure (1H)...")

    while True:
        candles = get_candles()

        if not candles:
            send_telegram("❌ No market data received.")
            time.sleep(300)
            continue

        bias = get_market_bias(candles)

        send_telegram(
            f"📈 Market Structure Update\n"
            f"Symbol: {SYMBOL}\n"
            f"HTF: {TIMEFRAME_LABEL}\n"
            f"Bias: {bias}"
        )

        # HTF updates every 15 minutes is fine
        time.sleep(900)


if __name__ == "__main__":
    run()
