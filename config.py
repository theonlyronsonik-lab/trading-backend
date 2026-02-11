# ==============================
# CONFIGURATION FILE
# ==============================

# TwelveData API Key
API_KEY = "d2eb6b7532504ac3bc6d720f98b6171c"

# Telegram Bot
TELEGRAM_BOT_TOKEN = "8529456380:AAF2Ed2EoEtGRTfAX4a67Vd89KSnMUImdQc"
TELEGRAM_CHAT_ID = "6599172354"

# Symbols to scan
SYMBOLS = [
    "EUR/USD",
    "GBP/USD",
    "XAU/USD",
]

# Timeframes
HTF = "1h"    # Higher Timeframe for structure
LTF = "5min"  # Lower Timeframe for entries

# Scan interval for main loop (in seconds)
LOOP_DELAY = 60  # 1-minute scan interval for LTF

# Risk-Reward
RISK_REWARD = 3  # 1:3 RR

# Minimum conditions for LTF entry signal
MIN_CONDITIONS = 2
TOTAL_CONDITIONS = 8
