import time
from config import SYMBOLS, HTF_TIMEFRAME, LTF_TIMEFRAME, LOOP_INTERVAL
from entry import (
fetch_candles,
analyse_htf_structure,
analyse_ltf_entry
)
from telegram_bots import send_telegram_message




def run():
print("Bot started successfully")


while True:
for symbol in SYMBOLS:
# =========================
# HTF ANALYSIS (CONTEXT)
# =========================
htf_candles = fetch_candles(symbol, HTF_TIMEFRAME, limit=200)
print(f"{symbol} HTF candles: {len(htf_candles)}")


if not htf_candles:
continue


htf_bias = analyse_htf_structure(htf_candles)
print(f"HTF Bias: {htf_bias}")


if htf_bias == "NO_DATA":
continue


# =========================
# LTF ENTRY CONFIRMATION
# =========================
ltf_candles = fetch_candles(symbol, LTF_TIMEFRAME, limit=300)
print(f"{symbol} LTF candles: {len(ltf_candles)}")


if not ltf_candles:
continue


ltf_signal = analyse_ltf_entry(ltf_candles, htf_bias)
print("LTF CHECK:", ltf_signal)


if ltf_signal:
message = f"""
🚨 *LTF TRADE CONFIRMATION*


Symbol: {symbol}
HTF Bias: {ltf_signal['bias']}


Direction: {ltf_signal['direction']}
Entry: {ltf_signal['entry']}
Stop Loss: {ltf_signal['sl']}
Take Profit: {ltf_signal['tp']}


Confirmation:
{ltf_signal['reason']}
"""
send_telegram_message(message)


time.sleep(LOOP_INTERVAL)




if __name__ == "__main__":
run()
