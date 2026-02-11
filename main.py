import time
from config import PAIRS, HTF, LTF, SCAN_INTERVAL
from market_data import fetch_data, fetch_htf_cached
from structure import get_htf_bias, detect_choch
from entry import retest_entry
from risk import calculate_dynamic_sl, calculate_tp
from zones import get_next_swing_high, get_next_swing_low
from notifier import send_message


HTF_SECONDS = 14400  # 4H


def scan_pair(symbol):
    print(f"Scanning {symbol}")

    htf_data = fetch_htf_cached(symbol, HTF, HTF_SECONDS)
    if not htf_data:
        return

    bias = get_htf_bias(htf_data)
    if not bias:
        return

    ltf_data = fetch_data(symbol, LTF)
    if not ltf_data:
        return

    if not detect_choch(ltf_data, bias):
        return

    entry = retest_entry(ltf_data, bias)
    if not entry:
        return

    if bias == "bullish":
        swing = min([float(c["low"]) for c in ltf_data[-5:]])
        tp_target = get_next_swing_high(htf_data)
    else:
        swing = max([float(c["high"]) for c in ltf_data[-5:]])
        tp_target = get_next_swing_low(htf_data)

    sl = calculate_dynamic_sl(entry, swing, bias)
    tp = calculate_tp(entry, sl, bias, tp_target)

    message = f"""
PAIR: {symbol}
BIAS: {bias.upper()}

ENTRY: {entry}
SL: {sl}
TP: {tp}
"""

    send_message(message)


def main():
    while True:
        for pair in PAIRS:
            scan_pair(pair)

        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
