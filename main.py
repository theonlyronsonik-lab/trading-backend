import time
from structure import detect_market_structure
from telegram_bot import send_telegram
from market_data import get_market_data


send_telegram("🟢 XAUUSD STRUCTURE BOT LIVE (H1 → M15)")


while True:
    try:
        candles_htf = get_market_data("XAUUSD", "1H")

        send_telegram("⚙️ Bot heartbeat: checking market structure...")

        structure = detect_market_structure(candles_htf)

        if structure and structure["bias"] != "Range":
            message = f"""
📊 XAUUSD MARKET STRUCTURE

Bias: {structure['bias']}
Event: {structure['BOS']}
Level: {structure['level']}
TF: 1H
"""
            send_telegram(message)

        time.sleep(900)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
