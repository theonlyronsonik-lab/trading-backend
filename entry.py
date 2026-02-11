# main.py

import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()
htf_last_fetch = {}

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS
# ==============================
def process_htf(symbol):
    now = time.time()
    # fetch HTF only if it's not fetched in the last HTF duration
    last_fetch = htf_last_fetch.get(symbol, 0)
    htf_seconds = 3600 if HTF == "1h" else 14400 if HTF == "4h" else 3600
    if now - last_fetch < htf_seconds:
        return htf_bias.get(symbol)

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_last_fetch[symbol] = now
    htf_bias[symbol] = bias
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol
                if symbol not in htf_reported:
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, htf_bias[symbol])
                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
# main.py

import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()
htf_last_fetch = {}

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS
# ==============================
def process_htf(symbol):
    now = time.time()
    # fetch HTF only if it's not fetched in the last HTF duration
    last_fetch = htf_last_fetch.get(symbol, 0)
    htf_seconds = 3600 if HTF == "1h" else 14400 if HTF == "4h" else 3600
    if now - last_fetch < htf_seconds:
        return htf_bias.get(symbol)

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_last_fetch[symbol] = now
    htf_bias[symbol] = bias
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol
                if symbol not in htf_reported:
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, htf_bias[symbol])
                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
# main.py

import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()
htf_last_fetch = {}

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS
# ==============================
def process_htf(symbol):
    now = time.time()
    # fetch HTF only if it's not fetched in the last HTF duration
    last_fetch = htf_last_fetch.get(symbol, 0)
    htf_seconds = 3600 if HTF == "1h" else 14400 if HTF == "4h" else 3600
    if now - last_fetch < htf_seconds:
        return htf_bias.get(symbol)

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_last_fetch[symbol] = now
    htf_bias[symbol] = bias
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol
                if symbol not in htf_reported:
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, htf_bias[symbol])
                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
# main.py

import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()
htf_last_fetch = {}

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS
# ==============================
def process_htf(symbol):
    now = time.time()
    # fetch HTF only if it's not fetched in the last HTF duration
    last_fetch = htf_last_fetch.get(symbol, 0)
    htf_seconds = 3600 if HTF == "1h" else 14400 if HTF == "4h" else 3600
    if now - last_fetch < htf_seconds:
        return htf_bias.get(symbol)

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_last_fetch[symbol] = now
    htf_bias[symbol] = bias
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol
                if symbol not in htf_reported:
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, htf_bias[symbol])
                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
# main.py

import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()
htf_last_fetch = {}

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS
# ==============================
def process_htf(symbol):
    now = time.time()
    # fetch HTF only if it's not fetched in the last HTF duration
    last_fetch = htf_last_fetch.get(symbol, 0)
    htf_seconds = 3600 if HTF == "1h" else 14400 if HTF == "4h" else 3600
    if now - last_fetch < htf_seconds:
        return htf_bias.get(symbol)

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_last_fetch[symbol] = now
    htf_bias[symbol] = bias
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol
                if symbol not in htf_reported:
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, htf_bias[symbol])
                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
# main.py

import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()
htf_last_fetch = {}

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS
# ==============================
def process_htf(symbol):
    now = time.time()
    # fetch HTF only if it's not fetched in the last HTF duration
    last_fetch = htf_last_fetch.get(symbol, 0)
    htf_seconds = 3600 if HTF == "1h" else 14400 if HTF == "4h" else 3600
    if now - last_fetch < htf_seconds:
        return htf_bias.get(symbol)

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_last_fetch[symbol] = now
    htf_bias[symbol] = bias
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol
                if symbol not in htf_reported:
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, htf_bias[symbol])
                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()
