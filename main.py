import time
from market_data import fetch_candles
from structure import get_structure_bias
from zones import get_supply_demand_zones
from risk import calculate_sl_tp
from telegram_bot import send_telegram
from config import SYMBOLS, HTF, LTF, LOOP_SLEEP

# ─────────────────────────────────────────────
# Memory (prevents API abuse & duplicate alerts)
# ─────────────────────────────────────────────
last_htf_fetch = {}
last_ltf_fetch = {}
last_signal_time = {}

HTF_SECONDS = {
    "4h": 4 * 60 * 60,
    "1h": 60 * 60
}

LTF_SECONDS = {
    "15min": 15 * 60,
    "5min": 5 * 60
}

COOLDOWN_SECONDS = 60 * 60  # 1 hour per symbol


def process_symbol(symbol):
    now = time.time()

    # ───── HTF FETCH (TIME-GATED) ─────
    if symbol not in last_htf_fetch or now - last_htf_fetch[symbol] >= HTF_SECONDS[HTF]:
        htf_candles = fetch_candles(symbol, HTF)
        last_htf_fetch[symbol] = now
    else:
        return

    if not htf_candles:
        print(f"No HTF data for {symbol}")
        return

    bias = get_structure_bias(htf_candles)
    if bias is None:
        return

    # ───── LTF FETCH (TIME-GATED) ─────
    if symbol not in last_ltf_fetch or now - last_ltf_fetch[symbol] >= LTF_SECONDS[LTF]:
        ltf_candles = fetch_candles(symbol, LTF)
        last_ltf_fetch[symbol] = now
    else:
        return

    if not ltf_candles:
        print(f"No LTF data for {symbol}")
        return

    zones = get_supply_demand_zones(ltf_candles)
    entry_price = ltf_candles[-1]["close"]

    trade = calculate_sl_tp(
        bias=bias,
        entry_price=entry_price,
        structure_levels=htf_candles,
        zones=zones
    )

    if not trade:
        return

    # ───── SYMBOL COOLDOWN ─────
    if symbol in last_signal_time:
        if now - last_signal_time[symbol] < COOLDOWN_SECONDS:
            return

    last_signal_time[symbol] = now

    message = (
        f"📊 {symbol} SETUP FOUND\n\n"
        f"Bias: {bias.upper()}\n"
        f"HTF: {HTF} → LTF: {LTF}\n\n"
        f"Entry: {entry_price}\n"
        f"Stop Loss: {trade['sl']}\n"
        f"Take Profit: {trade['tp']}\n"
        f"Risk:Reward ≈ 1:{trade['rr']}\n"
    )

    send_telegram(message)
    print(f"Signal sent for {symbol}")


def main():
    send_telegram("✅ Trading bot LIVE. Scanning markets...")

    while True:
        for symbol in SYMBOLS:
            try:
                process_symbol(symbol)
            except Exception as e:
                print(f"Error processing {symbol}: {e}")

        time.sleep(LOOP_SLEEP)


if name == "main":
    main()
