import time

from market_data import fetch_candles
from structure import get_structure_bias
from zones import get_supply_demand_zones
from entry import confirm_entry
from risk import calculate_sl_tp
from telegram_bot import send_telegram
from config import SYMBOLS, HTF, LTF, SLEEP_SECONDS


# Prevent duplicate signals
sent_setups = {}


def analyze_symbol(symbol):

    print(f"\nAnalyzing {symbol}...")

    # Fetch HTF candles
    candles_htf = fetch_candles(symbol, HTF)

    if not candles_htf:
        return

    # Fetch LTF candles
    candles_ltf = fetch_candles(symbol, LTF)

    if not candles_ltf:
        return

    # ------------------------------------------------
    # MARKET STRUCTURE BIAS
    # ------------------------------------------------
    bias, structure = get_structure_bias(candles_htf)

    if bias is None:
        return

    # ------------------------------------------------
    # SUPPLY / DEMAND ZONES
    # ------------------------------------------------
    zones = get_supply_demand_zones(candles_htf)

    # ------------------------------------------------
    # ENTRY PRICE (last close on LTF)
    # ------------------------------------------------
    entry_price = float(candles_ltf[-1]["close"])

    # ------------------------------------------------
    # CALCULATE SL / TP
    # ------------------------------------------------
    levels = calculate_sl_tp(
        bias=bias,
        entry_price=entry_price,
        structure=structure,
        demand_zones=zones["demand"],
        supply_zones=zones["supply"]
    )

    if trade is None:
        return

    sl = trade["sl"]
    tp = trade["tp"]
    rr = trade["rr"]

    if not levels:
        return

    entry = levels["entry"]
    sl = levels["sl"]
    tp = levels["tp"]
    logic = levels["logic"]

    # ------------------------------------------------
    # CONFIRM RR >= 1:3
    # ------------------------------------------------
    if not confirm_entry(bias, entry, sl, tp):
        print(f"{symbol} skipped — RR below 1:3")
        return

    # ------------------------------------------------
    # PREVENT DUPLICATE SIGNALS
    # ------------------------------------------------
    setup_key = f"{symbol}_{bias}_{round(entry, 4)}"

    if sent_setups.get(symbol) == setup_key:
        print(f"{symbol} setup already sent.")
        return

    sent_setups[symbol] = setup_key

    # ------------------------------------------------
    # TELEGRAM ALERT
    # ------------------------------------------------
    message = (
        f"📊 TRADE SETUP FOUND\n\n"
        f"Symbol: {symbol}\n"
        f"Bias: {bias.upper()}\n"
        f"HTF → LTF: {HTF} → {LTF}\n\n"
        f"Entry: {entry}\n"
        f"Stop Loss: {sl}\n"
        f"Take Profit: {tp}\n\n"
        f"Logic: {logic}"
    )

    send_telegram(message)

    print(f"Signal sent for {symbol}")


# ====================================================
# MAIN LOOP
# ====================================================
def run_bot():

    send_telegram("🤖 Trading bot started successfully")

    while True:

        try:
            for symbol in SYMBOLS:
                analyze_symbol(symbol)

            time.sleep(SLEEP_SECONDS)

        except Exception as e:
            print("Bot error:", e)
            time.sleep(60)


# ====================================================
# START BOT
# ====================================================
if __name__ == "__main__":
    run_bot()
