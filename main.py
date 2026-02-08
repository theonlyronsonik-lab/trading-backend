from market_data import fetch_candles
from structure import get_structure_bias
from zones import get_supply_demand_zones
from entry import confirm_entry
from risk import calculate_sl_tp
from telegram_bot import send_telegram
from config import SYMBOLS, HTF, LTF, SLEEP_SECONDS


SENT_ALERTS = set()


def analyze_symbol(symbol):
    print(f"🔍 Analyzing {symbol}")

    htf_candles = fetch_candles(symbol, HTF_INTERVAL)
    if not htf_candles:
        return

    bias = get_structure_bias(htf_candles)
    if bias not in ["bullish", "bearish"]:
        return

    zones = detect_supply_demand(htf_candles)
    if not zones:
        return

    ltf_candles = fetch_candles(symbol, LTF_INTERVAL)
    if not ltf_candles:
        return

    price = float(ltf_candles[-1]["close"])

    for zone in zones:
        if bias == "bullish" and zone["type"] != "demand":
            continue

        if bias == "bearish" and zone["type"] != "supply":
            continue

        if price_in_zone(price, zone):
            alert_id = f"{symbol}_{zone['type']}_{zone['low']}_{zone['high']}"

            if alert_id in SENT_ALERTS:
                continue

            message = (
                f"📊 <b>{symbol}</b>\n"
                f"HTF Bias: <b>{bias.upper()}</b>\n"
                f"Zone: <b>{zone['type'].upper()}</b>\n"
                f"Entry Area: {zone['low']} – {zone['high']}\n"
                f"TFs: {HTF_INTERVAL} → {LTF_INTERVAL}"
            )

            send_telegram(message)
            SENT_ALERTS.add(alert_id)


def run_bot():
    send_telegram("✅ Trading bot LIVE. Scanning markets...")

    while True:
        for symbol in SYMBOLS:
            analyze_symbol(symbol)

        time.sleep(SCAN_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_bot()
