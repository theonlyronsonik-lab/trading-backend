# main.py

import time
from config import SYMBOL, TIMEFRAME, RISK_REWARD, COOLDOWN_SECONDS
from market_data import fetch_candles
from structure import get_structure_bias
from liquidity import detect_liquidity_sweep
from entry import confirm_entry
from risk import calculate_levels
from telegram_bot import send_telegram

def run():
    send_telegram(
        f"✅ BOT LIVE\n"
        f"Symbol: {SYMBOL}\n"
        f"TF: {TIMEFRAME}\n"
        f"Waiting for setup..."
    )

    last_signal = None

    while True:
        candles = fetch_candles()

        if not candles:
            time.sleep(COOLDOWN_SECONDS)
            continue

        bias = get_structure_bias(candles)
        liquidity = detect_liquidity_sweep(candles)
        entry = confirm_entry(bias, liquidity)

        if entry and entry != last_signal:
            levels = calculate_levels(candles, entry, RISK_REWARD)

            if levels:
                send_telegram(
                    f"📊 TRADE SETUP\n"
                    f"{SYMBOL} | {TIMEFRAME}\n\n"
                    f"Bias: {bias}\n"
                    f"Liquidity: {liquidity}\n\n"
                    f"Direction: {entry}\n"
                    f"Entry: {levels['entry']}\n"
                    f"SL: {levels['sl']}\n"
                    f"TP: {levels['tp']}"
                )

                last_signal = entry

        time.sleep(COOLDOWN_SECONDS)

if __name__ == "__main__":
    run()

