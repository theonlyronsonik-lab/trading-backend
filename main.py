import time
from config import SYMBOLS, HTF, LTF, SYMBOL_COOLDOWN_SECONDS
from market_data import fetch_candles
from structure import get_structure_bias
from zones import get_supply_demand_zones
from risk import calculate_sl_tp
from telegram_bot import send_telegram

last_htf_fetch = {}
last_ltf_fetch = {}
last_signal_time = {}  # symbol → timestamp


def process_symbol(symbol):
    now = time.time()

    # ⏳ COOLDOWN CHECK
    if symbol in last_signal_time:
        if now - last_signal_time[symbol] < SYMBOL_COOLDOWN_SECONDS:
            return

    now = time. time()
    if symbol not in last_htf_fetch or now - last_htf_fetch[symbol] > 4 * 60 * 60:
            htf_candles = fetch_candles(symbol, HTF)
        last_htf_fetch[symbol] = now 
    else:
    return
    bias, structure_levels = get_structure_bias(htf_candles)
    if not bias:
        return

   now = time.time()

if symbol not in last_htf_fetch or now - last_htf_fetch[symbol] > 4 * 60 * 60:
    htf_candles = fetch_candles(symbol, HTF)
    last_htf_fetch[symbol] = now
else:
    return

    zones = get_supply_demand_zones(ltf_candles)
    entry_price = float(ltf_candles[0]["close"])

    trade = calculate_sl_tp(
        bias=bias,
        entry_price=entry_price,
        structure_levels=structure_levels,
        zones=zones
    )

    if not trade:
        return

    sl = trade["sl"]
    tp = trade["tp"]
    rr = trade["rr"]

    message = (
        f"📊 {symbol} SETUP FOUND\n"
        f"Bias: {bias.upper()}\n"
        f"HTF: {HTF} → LTF: {LTF}\n"
        f"Entry: {entry_price}\n"
        f"SL: {sl}\n"
        f"TP: {tp}\n"
        f"RR: 1:{rr}\n"
    )

    send_telegram(message)
    last_signal_time[symbol] = now


def main():
    send_telegram("🤖 Bot running. Awaiting market conditions...")

    while True:
        for symbol in SYMBOLS:
            process_symbol(symbol)

        time.sleep(60)  # main loop delay


if __name__ == "__main__":
    main()
