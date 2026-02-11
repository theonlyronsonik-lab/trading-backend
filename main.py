# main.py
import time
from config import SYMBOLS, LOOP_DELAY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
import requests
from datetime import datetime

def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN is None:
        print("Telegram bot token not set.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def scan_symbol(symbol):
    df_htf = fetch_candles(symbol, "1h")
    if df_htf is None:
        print(f"Error fetching HTF candles for {symbol}")
        return

    htf_bias, prev_high, prev_low = analyse_htf_structure(df_htf)
    if htf_bias is None:
        return

    send_telegram_message(f"📊 {symbol} HTF: {htf_bias}")

    ltf_signal = analyse_ltf_entry(symbol, htf_bias, prev_high, prev_low)
    if ltf_signal:
        msg = (f"🚀 {symbol} LTF ENTRY\n"
               f"Direction: {ltf_signal['direction']}\n"
               f"Entry: {ltf_signal['entry']}\n"
               f"SL: {ltf_signal['sl']}\n"
               f"TP: {ltf_signal['tp']}")
        send_telegram_message(msg)

def run():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.now())
    while True:
        for symbol in SYMBOLS:
            try:
                scan_symbol(symbol)
            except Exception as e:
                print(f"Error scanning {symbol}: {e}")
        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    run()

