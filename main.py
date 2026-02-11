import time
from datetime import datetime
from config import PAIRS, HTF, LTF, SCAN_INTERVAL, TWELVEDATA_API_KEY, HTF_SECONDS
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE TRACKING PER PAIR
# ==============================
PAIR_STATE = {}

# ==============================
# FETCH HTF WITH CACHING (Free Plan)
# ==============================
LAST_HTF_FETCH = {}

def fetch_htf_cached(symbol, tf, tf_seconds):
    now = time.time()
    last_fetch = LAST_HTF_FETCH.get(symbol, 0)

    if now - last_fetch < tf_seconds:
        return None  # Skip fetch to save API calls

    candles = fetch_candles(symbol, tf, limit=100, api_key=API_KEY)
    if candles:
        LAST_HTF_FETCH[symbol] = now
    return candles

# ==============================
# SCAN FUNCTION
# ==============================
def scan_pair(symbol):
    if symbol not in PAIR_STATE:
        PAIR_STATE[symbol] = {
            "bias": None,
            "choch_alerted": False,
            "entry_alerted": False
        }

    # -------- HTF BIAS --------
    htf_candles = fetch_htf_cached(symbol, HTF, HTF_SECONDS)
    if not htf_candles:
        return

    bias = analyse_htf_structure(htf_candles)
    if bias and bias != PAIR_STATE[symbol]["bias"]:
        PAIR_STATE[symbol]["bias"] = bias
        PAIR_STATE[symbol]["choch_alerted"] = False
        PAIR_STATE[symbol]["entry_alerted"] = False

        send_telegram_message(
            f"🔎 {symbol} HTF Bias Update\n\n"
            f"HTF: {HTF}\n"
            f"Bias: {bias.upper()}\n"
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )

    if not bias:
        return

    # -------- LTF CHOCH --------
    ltf_candles = fetch_candles(symbol, LTF, limit=100, api_key=API_KEY)
    if not ltf_candles:
        return

    choch_entry = analyse_ltf_entry(ltf_candles, bias)
    if choch_entry and not PAIR_STATE[symbol]["choch_alerted"]:
        PAIR_STATE[symbol]["choch_alerted"] = True
        send_telegram_message(
            f"⚡ {symbol} LTF CHoCH Detected\n\n"
            f"Direction: {bias.upper()}\n"
            f"Waiting for retest confirmation..."
        )

    if not choch_entry:
        return

    # -------- ENTRY ALERT --------
    if PAIR_STATE[symbol]["entry_alerted"]:
        return

    entry = choch_entry["entry"]
    sl = choch_entry["sl"]
    tp = choch_entry["tp"]

    PAIR_STATE[symbol]["entry_alerted"] = True
    send_telegram_message(
        f"🚀 TRADE SETUP CONFIRMED\n\n"
        f"Pair: {symbol}\n"
        f"Bias: {bias.upper()}\n"
        f"Entry: {round(entry, 5)}\n"
        f"SL: {round(sl, 5)}\n"
        f"TP: {round(tp, 5)}\n"
        f"R:R ≈ {round((tp - entry)/(entry - sl), 2) if bias=='bullish' else round((entry - tp)/(sl - entry),2)}"
    )

# ==============================
# MAIN LOOP
# ==============================
def run():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

    while True:
        for symbol in SYMBOLS:
            try:
                scan_pair(symbol)
            except Exception as e:
                print(f"Error scanning {symbol}: {e}")
        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
