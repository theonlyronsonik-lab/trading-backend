import time
import requests
from config import *
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)


send_telegram("🤖 Ron_Market Scanner is LIVE.\nAnalysing existing HTF structure...")


htf_bias = {}

# 🔥 ANALYSE EXISTING HTF IMMEDIATELY
for symbol in SYMBOLS:
    htf_candles = fetch_candles(symbol, HTF, HTF_CANDLES)
    bias = analyse_htf_structure(htf_candles)
    htf_bias[symbol] = bias

    send_telegram(
        f"📊 HTF ANALYSIS (STARTUP)\n"
        f"Symbol: {symbol}\n"
        f"Timeframe: {HTF}\n"
        f"Candles: {len(htf_candles)}\n"
        f"Bias: {bias}"
    )


# 🔁 CONTINUOUS LTF SCAN
while True:
    for symbol in SYMBOLS:
        bias = htf_bias.get(symbol)
        if bias in ["NO_DATA", "RANGE"]:
            continue

        ltf_candles = fetch_candles(symbol, LTF, LTF_CANDLES)
        setup = analyse_ltf_entry(ltf_candles, bias)

        if setup:
            send_telegram(
                f"🚨 TRADE SETUP FOUND\n\n"
                f"Symbol: {symbol}\n"
                f"Bias ({HTF}): {bias}\n"
                f"Entry TF: {LTF}\n\n"
                f"📍 Entry: {setup['entry']}\n"
                f"🛑 SL: {setup['sl']}\n"
                f"🎯 TP: {setup['tp']}\n\n"
                f"⚠️ Wait for confirmation. No FOMO."
            )

    time.sleep(SCAN_INTERVAL)
