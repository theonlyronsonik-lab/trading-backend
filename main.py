import time
from datetime import datetime

from config import SYMBOLS, HTF, LTF
from data import get_candles
from entry import find_ltf_entry
from notifier import send_message


# =========================
# SETTINGS
# =========================
HTF_CANDLES = 200
LTF_CANDLES = 200
SLEEP_TIME = 300  # 5 minutes


# =========================
# STATE
# =========================
htf_bias = {}
sent_entries = set()


# =========================
# HTF STRUCTURE (HH/HL, LH/LL)
# =========================
def detect_htf_structure(candles):
    if len(candles) < 50:
        return None

    highs = [c["high"] for c in candles[-20:]]
    lows = [c["low"] for c in candles[-20:]]

    # Higher Highs + Higher Lows
    if highs[-1] > highs[0] and lows[-1] > lows[0]:
        return "BULLISH"

    # Lower Highs + Lower Lows
    if highs[-1] < highs[0] and lows[-1] < lows[0]:
        return "BEARISH"

    return None


# =========================
# MAIN
# =========================
def run():
    send_message("🤖 Bot is LIVE.")

    # -------- HTF ANALYSIS ON STARTUP --------
    for symbol in SYMBOLS:
        try:
            candles = get_candles(symbol, HTF, limit=HTF_CANDLES)

            if not candles:
                continue

            bias = detect_htf_structure(candles)

            if bias:
                htf_bias[symbol] = bias

                send_message(
                    f"📊 HTF STRUCTURE\n\n"
                    f"Symbol: {symbol}\n"
                    f"Bias ({HTF}): {bias}"
                )

        except Exception as e:
            print(f"HTF error on {symbol}: {e}")

    # -------- CONTINUOUS LTF SCANNING --------
    while True:
        for symbol in SYMBOLS:
            try:
                bias = htf_bias.get(symbol)

                if not bias:
                    continue

                if symbol in sent_entries:
                    continue

                entry = find_ltf_entry(symbol, bias, LTF)

                if entry:
                    send_message(
                        f"🚨 TRADE SETUP FOUND\n\n"
                        f"Symbol: {symbol}\n"
                        f"Bias ({HTF}): {bias}\n"
                        f"Entry TF: {LTF}\n\n"
                        f"📍 Entry Zone: {entry['entry_zone']}\n"
                        f"🛑 Stop Loss: {entry['sl']}\n"
                        f"🎯 Take Profit: {entry['tp']}\n\n"
                        f"⚠️ Wait for price to react inside the zone.\n"
                        f"No FOMO. No market orders."
                    )

                    sent_entries.add(symbol)

            except Exception as e:
                print(f"LTF error on {symbol}: {e}")

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    run()
