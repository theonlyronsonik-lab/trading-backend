import time
from datetime import datetime

from config import SYMBOLS, HTF, LTF 
from data import get_candles 
from entry import find_ltf_entry 
from notifier import send_message

--- State ---

last_htf_time = {} htf_bias = {} active_symbols = set()  # cooldown until structure changes

def is_new_htf_candle(symbol): """Check if a new HTF candle has closed.""" candles = get_candles(symbol, HTF, limit=2) if not candles or len(candles) < 2: return False

last_closed = candles[-2]["datetime"]

if symbol not in last_htf_time:
    last_htf_time[symbol] = last_closed
    return True

if last_closed != last_htf_time[symbol]:
    last_htf_time[symbol] = last_closed
    return True

return False

def determine_htf_bias(candles): """Simple HTF bias using market structure (HH / LL).""" highs = [c["high"] for c in candles] lows = [c["low"] for c in candles]

if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
    return "BULLISH"
if highs[-1] < highs[-2] and lows[-1] < lows[-2]:
    return "BEARISH"

return "RANGE"

def run(): send_message("✅ Trading bot LIVE (HTF 4H → LTF 15m). Waiting for structure…")

while True:
    for symbol in SYMBOLS:
        try:
            # --- HTF logic ---
            if is_new_htf_candle(symbol):
                htf_candles = get_candles(symbol, HTF, limit=20)
                bias = determine_htf_bias(htf_candles)

                htf_bias[symbol] = bias
                active_symbols.discard(symbol)  # reset cooldown

                send_message(
                    f"📊 {symbol}\n"
                    f"HTF ({HTF}) Bias: {bias}\n"
                    f"Structure changed – setup detected.\n"
                    f"Await LTF entry confirmation."
                )

            # --- LTF logic (only after HTF bias) ---
            if symbol in htf_bias and symbol not in active_symbols:
                ltf_candles = get_candles(symbol, LTF, limit=50)

                entry = find_ltf_entry(
                    symbol=symbol,
                    candles=ltf_candles,
                    bias=htf_bias[symbol]
                )

                if entry:
                    send_message(entry)
                    active_symbols.add(symbol)  # cooldown until next HTF shift

        except Exception as e:
            print(f"Error on {symbol}: {e}")

    time.sleep(30)

if __name__ == "__main__": 
    run()
