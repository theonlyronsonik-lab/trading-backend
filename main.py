# main.py

import time
import threading
from config import SYMBOLS, HTF, LTF, RISK_REWARD, COOLDOWN_SECONDS
from market_data import fetch_candles
from structure import get_structure_bias
from entry import confirm_entry
from telegram_bot import send_telegram

def analyze_symbol(symbol):
    """Analyze a single symbol and send alert if setup is found."""
    # Fetch HTF (Higher Timeframe) candles
    htf_candles = fetch_candles(symbol, HTF)
    if not htf_candles:
        return

    # Get structure bias from HTF
    bias = get_structure_bias(htf_candles)
    if bias == "NEUTRAL":
        return  # No setup if neutral bias

    # Fetch LTF (Lower Timeframe) candles for entry confirmation
    ltf_candles = fetch_candles(symbol, LTF)
    if not ltf_candles:
        return

    # Confirm entry based on structure and LTF candles
    entry_signal = confirm_entry(bias, ltf_candles)
    if entry_signal:
        send_telegram(f"🚨 {symbol} Setup Found!\nBias: {bias} on {HTF} & entry confirmed on {LTF}.")
    
def run():
    send_telegram("✅ Multi-Analyzer Bot LIVE\nReady to analyze: " + ", ".join(SYMBOLS))
    
    while True:
        # Run analysis for all symbols simultaneously (in parallel)
        threads = []
        for symbol in SYMBOLS:
            thread = threading.Thread(target=analyze_symbol, args=(symbol,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Wait for the next cycle
        print("Sleeping for", COOLDOWN_SECONDS, "seconds.")
        time.sleep(COOLDOWN_SECONDS)

if __name__ == "__main__":
    run()
