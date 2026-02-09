import time
from datetime import datetime

from config import SYMBOLS, HTF, LTF
from data import get_candles
from structure import detect_market_structure
from entries import find_ltf_entry
from risk import calculate_sl_tp
from notifier import send_message

# =========================
# STATE
# =========================

htf_bias = {}              # symbol -> "BULLISH" | "BEARISH"
last_htf_time = {}         # symbol -> last HTF candle time
symbol_cooldown = {}       # symbol -> True/False

LOOP_SLEEP = 30  # seconds


# =========================
# HTF LOGIC
# =========================

def new_htf_candle(symbol):
    candles = get_candles(symbol, HTF, limit=2)
    if not candles:
        return False

    latest_time = candles[0]["datetime"]

    if last_htf_time.get(symbol) != latest_time:
        last_htf_time[symbol] = latest_time
        return True

    return False


def process_htf(symbol):
    candles = get_candles(symbol, HTF, limit=200)
    if not candles:
        return

    structure = detect_market_structure(candles)

    previous_bias = htf_bias.get(symbol)
    current_bias = structure["bias"]

    if previous_bias != current_bias:
        htf_bias[symbol] = current_bias
        symbol_cooldown[symbol] = False  # reset cooldown on structure change

        send_message(
            f"📊 *{symbol}*\n"
            f"HTF (4H) Bias: *{current_bias}*\n"
            f"Structure changed – waiting for LTF entry."
        )


# =========================
# LTF LOGIC
# =========================

def process_ltf(symbol):
    if symbol_cooldown.get(symbol):
        return

    bias = htf_bias.get(symbol)
    if not bias:
        return

    candles = get_candles(symbol, LTF, limit=200)
    if not candles:
        return

    entry = find_ltf_entry(candles, bias)
    if not entry:
        return

    sl, tp, rr = calculate_sl_tp(
        entry=entry,
        candles=candles,
        bias=bias,
        use_supply_demand=True
    )

    if rr < 3:
        return

    symbol_cooldown[symbol] = True

    send_message(
        f"🚨 *TRADE SETUP FOUND*\n\n"
        f"📍 Symbol: *{symbol}*\n"
        f"🧭 Bias: *{bias}*\n"
        f"⏱ TF: 15m\n\n"
        f"➡️ Entry: {entry['price']}\n"
        f"🛑 SL: {sl}\n"
        f"🎯 TP: {tp}\n"
        f"📐 RR: *1:{rr:.2f}*\n\n"
        f"🧠 Logic: HTF structure → LTF confirmation"
    )


# =========================
# MAIN LOOP
# =========================

def run():
    send_message("✅ Trading bot LIVE (HTF 4H → LTF 15m). Waiting for structure...")

    while True:
        for symbol in SYMBOLS:
            try:
                # HTF only on new candle
                if new_htf_candle(symbol):
                    process_htf(symbol)

                # LTF only after HTF bias exists
                if symbol in htf_bias:
                    process_ltf(symbol)

            except Exception as e:
                print(f"Error on {symbol}: {e}")

        time.sleep(LOOP_SLEEP)


if name == "main":
    run()
