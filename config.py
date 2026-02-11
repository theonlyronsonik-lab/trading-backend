# config.py

# Symbols to scan
SYMBOLS = ["XAU/USD", "EUR/USD", "GBP/USD", "AUD/CAD"]

# Timeframes
HTF = "1h"      # Higher Timeframe
LTF = "5min"    # Lower Timeframe

# Scan loop delay (seconds) to avoid exceeding API
LOOP_DELAY = 60

# TwelveData API Key
API_KEY = "YOUR_TWELVEDATA_API_KEY"

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# Risk/Reward
RR_RATIO = 3

# Minimum conditions to trigger LTF signal
LTF_MIN_CONDITIONS = 2
LTF_TOTAL_CONDITIONS = 8
