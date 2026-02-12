# config.py

# Symbols to scan
SYMBOLS = ["XAU/USD", "EUR/USD", "GBP/USD", "AUD/CAD"]

# Timeframes
HTF = "4h"      # Higher Timeframe
LTF = "15min"    # Lower Timeframe

# Scan loop delay (seconds) to avoid exceeding API
LOOP_DELAY = 120

RISK_PERCENT = 0.05

# TwelveData API Key
API_KEY = "d2849e2ab0c042edb97b8276d864a41b"

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = "8529456380:AAF2Ed2EoEtGRTfAX4a67Vd89KSnMUImdQc"
TELEGRAM_CHAT_ID = "6599172354"

# Risk/Reward
RR_RATIO = 3

# Minimum conditions to trigger LTF signal
LTF_MIN_CONDITIONS = 3
LTF_TOTAL_CONDITIONS = 8
