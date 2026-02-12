# main.py
import time
import requests
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MIN_CONFIRMATIONS
from entry import get_candles, analyse_htf_structure, analyse_ltf_entry

# -----------------------------
# TELEGRAM FUNCTION
# -----------------------------
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=data)
        r.raise_for_status()
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# -----------------------------
# MAIN SCAN LOOP
# -----------------------------
def run():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    
    while True:
        for symbol in SYMBOLS:
            # FETCH HTF DATA
            htf_df = get_candles(symbol, HTF)
            if htf_df.empty:
                print(f"No HTF data for {symbol}")
                continue

            # ANALYSE HTF STRUCTURE
            htf_bias = analyse_htf_structure(htf_df)
            send_telegram_message(f"📊 HTF STRUCTURE\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {htf_bias}")

            # DETERMINE SWING RANGE
            swing_high = htf_df['high'].iloc[-1]
            swing_low = htf_df['low'].iloc[-1]

            # FETCH LTF DATA
            ltf_df = get_candles(symbol, LTF)
            if ltf_df.empty:
                print(f"No LTF data for {symbol}")
                continue

            # ANALYSE LTF FOR ENTRY
            entry, sl, tp = analyse_ltf_entry(htf_bias, ltf_df, swing_low, swing_high, confirmations_needed=MIN_CONFIRMATIONS)
            if entry:
                msg = f"💹 LTF ENTRY ALERT\nSymbol: {symbol}\nEntry: {entry}\nSL: {sl}\nTP: {tp}\nHTF Bias: {htf_bias}"
                send_telegram_message(msg)

        time.sleep(LOOP_DELAY)

# -----------------------------
# START BOT
# -----------------------------
if __name__ == "__main__":
    run()
