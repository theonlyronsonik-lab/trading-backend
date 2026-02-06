import time
from config import (
    SYMBOLS,
    HTF,
    LTF,
    CANDLE_LIMIT,
    COOLDOWN_SECONDS,
    BOT_NAME,
)
from market_data import fetch_candles
from structure import get_structure_bias
from entry import confirm_entry
from telegram_bot import send_telegram


def analyze_symbol(symbol):
    # 1️⃣ Higher Timeframe Structure
    htf_candles = fetch_candles(symbol, HTF, CANDLE_LIMIT)
    if not htf_candles:
        return

    bias = get_structure_bias(htf_candles)
    if bias == "RANGE":
        return

    # 2️⃣ Lower Timeframe Entry
    ltf_candles = fetch_candles(symbol, LTF, CANDLE_LIMIT)
    if not ltf_candles:
        return

    entry = confirm_entry(bias, ltf_candles)
    if not entry:
        return

    # 3️⃣ Telegram Alert
    message = (
        "🚨 SETUP FOUND\n"
        f"Symbol: {symbol}\n"
        f"Bias ({HTF}): {bias}\n"
        f"Entry TF: {LTF}\n"
        f"Entry: {entry}"
    )
    send_telegram(message)


def run():
    send_telegram(
        "✅ BOT STARTED\n"
        f"Name: {BOT_NAME}\n"
        f"Pairs: {', '.join(SYMBOLS)}\n"
        f"HTF → LTF: {HTF} → {LTF}"
    )

    while True:
        for symbol in SYMBOLS:
            try:
                analyze_symbol(symbol)
            except Exception as e:
                print(f"Error processing {symbol}: {e}")

        time.sleep(COOLDOWN_SECONDS)


if name == "main":
    run()
