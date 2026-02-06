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
    # 1️⃣ Higher timeframe structure
    htf_candles = fetch_candles(symbol, HTF, CANDLE_LIMIT)
    if not htf_candles:
        return

    bias = get_structure_bias(htf_candles)
    if bias == "RANGE":
        return

    # 2️⃣ Lower timeframe entry
    ltf_candles = fetch_candles(symbol, LTF, CANDLE_LIMIT)
    if not ltf_candles:
        return

    entry = confirm_entry(bias, ltf_candles)
    if not entry:
        return

    # 3️⃣ Send alert
    message = (
        f"🚨 SETUP FOUND\n"
        f"Symbol: {symbol}\n"
        f"Bias ({HTF}): {bias}\n"
        f"Entry TF: {LTF}\n"
        f"Entry Type: {entry}"
    )
    send_telegram(message)


def run():
    send_telegram(
        f"✅ {BOT_NAME} LIVE\n"
        f"Pairs: {', '.join(SYMBOLS)}\n"
        f"HTF: {HTF} → LTF:

