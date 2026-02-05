from market_data import get_candles
from structure import analyze_structure
from liquidity import liquidity_sweep
from telegram_bot import send_telegram

def run_bot():
    candles = get_candles("XAUUSD", "15m", limit=200)

    if not candles:
        send_telegram("❌ Market data failed. No candles received.")
        return

    structure = analyze_structure(candles)
    sweep = liquidity_sweep(candles)

    # Only alert on meaningful events
    if structure["event"] and sweep:
        message = (
            f"📊 XAUUSD 15m\n"
            f"Structure: {structure['bias']}\n"
            f"Event: {structure['event']}\n"
            f"Liquidity Sweep: ✅\n"
            f"Awaiting entry confirmation..."
        )
        send_telegram(message)

