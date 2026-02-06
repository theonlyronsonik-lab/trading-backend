import time
from market_data import fetch_candles
from structure import get_structure_bias
from entry import confirm_entry
from telegram_bot import send_telegram
from config import SYMBOLS, HTF, LTF, RISK_REWARD, COOLDOWN_SECONDS, BOT_NAME

def run_bot():
    for symbol in SYMBOLS:
        try:
            print(f"Fetching {symbol} candles...")
            candles = fetch_candles(symbol, HTF, CANDLE_LIMIT)
            if candles:
                print(f"{symbol} candles received: {len(candles)}")

                # Check structure bias
                bias = get_structure_bias(symbol, candles)
                if bias:
                    print(f"{symbol} structure bias: {bias}")
                    entry = confirm_entry(symbol, bias)
                    if entry:
                        message = f"{symbol} entry confirmed with bias: {bias} at {entry['price']}"
                        send_telegram(message)

            time.sleep(COOLDOWN_SECONDS)

        except Exception as e:
            print(f"Error processing {symbol}: {str(e)}")

if __name__ == "__main__":
    run_bot()

