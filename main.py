import time
from datetime import time as dtime

from config import (
    SYMBOLS,
    HTF,
    LTF,
    HTF_SECONDS,
    LTF_SECONDS,
    LOOP_SLEEP
)

from market_data import fetch_candles
from structure import get_structure_bias
from telegram_bot import send_telegram
from state import is_new_structure, update_structure

last_htf_fetch = {}
last_ltf_fetch = {}


def now_ts():
    return int(time.time())


def should_fetch(last_fetch, interval):
    return now_ts() - last_fetch >= interval


def run():
    send_telegram("✅ Trading bot LIVE (HTF 4H → LTF 15m). Waiting for structure...")

    while True:
        for symbol in SYMBOLS:
            try:
                # =========================
                # HTF FETCH CONTROL
                # =========================
                if symbol not in last_htf_fetch:
                    last_htf_fetch[symbol] = 0

                if not should_fetch(last_htf_fetch[symbol], HTF_SECONDS):
                    continue

                htf_candles = fetch_candles(symbol, HTF)
                if not htf_candles:
                    continue

                htf_bias = get_structure_bias(htf_candles)
                last_htf_fetch[symbol] = now_ts()

                if htf_bias not in ["bullish", "bearish"]:
                    continue

                # =========================
                # LTF FETCH CONTROL
                # =========================
                if symbol not in last_ltf_fetch:
                    last_ltf_fetch[symbol] = 0

                if not should_fetch(last_ltf_fetch[symbol], LTF_SECONDS):
                    continue

                ltf_candles = fetch_candles(symbol, LTF)
                if not ltf_candles:
                    continue

                last_ltf_fetch[symbol] = now_ts()

                structure = {
                    "bias": htf_bias,
                    "htf_high": max(c["high"] for c in htf_candles),
                    "htf_low": min(c["low"] for c in htf_candles)
                }

                if not is_new_structure(symbol, structure):
                    continue

                update_structure(symbol, structure)

                message = (
                    f"📊 {symbol}\n"
                    f"HTF (4H) Bias: {htf_bias.upper()}\n"
                    f"Structure changed – setup detected.\n"
                    f"Await LTF entry confirmation."
                )

                send_telegram(message)

            except Exception as e:
                print(f"Error processing {symbol}: {e}")

        time.sleep(LOOP_SLEEP)


if __name__ == "__main__":
    run()
