from market_data import get_candles
from telegram_bot import send_telegram
candles = get_candles()

if not candles:
    send_telegram("❌ Market data error: No candles received")
else:
    send_telegram(f"📊 XAUUSD 15m candles received: {len(candles)}")
