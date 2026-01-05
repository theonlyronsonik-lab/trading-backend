import time
from market_data import get_candles
from telegram_bot import send_telegram

if __name__ == "__main__":
    send_telegram("📡 Bot is LIVE. Testing market data feed for XAUUSD (H1)...")

    candles = get_candles(symbol="XAUUSD", timeframe="1h", limit=50)

    if candles:
        send_telegram(f"📊 Market data OK: {len(candles)} H1 candles received.")
    else:
        send_telegram("❌ Market data FAILED. No candles received.")

    # keep service alive
    while True:
        time.sleep(300)
