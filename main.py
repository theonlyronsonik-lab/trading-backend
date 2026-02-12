# main.py

from state import BotState
from structure import detect_bos, check_htf_retest
from entry import detect_choch, check_entry
from risk import calculate_lot_size

import pandas as pd

HTF_TIMEFRAME = "1h"
LTF_TIMEFRAME = "5m"
RISK_PERCENT = 0.05

state = BotState()

def get_candles(symbol, timeframe):
    # Replace with your TwelveData fetch
    return pd.DataFrame()

def get_balance():
    return 1000

def send_order(signal, lot):
    print("Placing Trade:")
    print(signal)
    print("Lot:", lot)


def run(symbol):
    htf = get_candles(symbol, HTF_TIMEFRAME)
    ltf = get_candles(symbol, LTF_TIMEFRAME)

    if htf.empty or ltf.empty:
        print("No data returned.")
        return

    detect_bos(htf, state)

    current_price = ltf["close"].iloc[-1]

    check_htf_retest(current_price, state)

    detect_choch(ltf, state)

    signal = check_entry(ltf, state)

    if signal:
        balance = get_balance()
        lot = calculate_lot_size(balance, signal["entry"], signal["sl"], RISK_PERCENT)
        send_order(signal, lot)


if __name__ == "__main__":
    run()

