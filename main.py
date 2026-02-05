from market_data import get_candles
from structure import analyze_structure
from liquidity import liquidity_sweep
from entries import find_fvg, candle_confirmation
from sessions import in_trading_session
from risk import calculate_position
from telegram_bot import send_telegram


def run_bot():
    if not in_trading_session():
        return

    candles = get_candles("XAUUSD", "15m", limit=200)

    if not candles:
        return

    structure = analyze_structure(candles)

    if not structure["event"]:
        return

    if not liquidity_sweep(candles):
        return

    fvg = find_fvg(candles, structure["bias"])
    confirmation = candle_confirmation(candles[-1], structure["bias"])

    if not fvg or not confirmation:
        return

    entry = candles[-1]["close"]
    stop = candles[-1]["low"] if structure["bias"] == "BULLISH" else candles[-1]["high"]

    risk = calculate_position(entry, stop)

    message = (
        f"🔥 XAUUSD 15m TRADE SETUP\n\n"
        f"Structure: {structure['bias']}\n"
        f"Event: {structure['event']}\n"
        f"Liquidity: ✅\n"
        f"Entry Model: FVG + Confirmation\n\n"
        f"Entry: {entry}\n"
        f"Stop: {stop}\n"
        f"TP: {risk['tp']}\n"
        f"RR: {risk['rr']}\n"
        f"Lot Size (est): {risk['lot_size']}"
    )

    send_telegram(message)


